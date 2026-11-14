"""Anthropic-only extension of Experiment 2 v2 (Apart AI x Epistemics sprint, Nov 13-15 2026).
720 conversations = 30 cases x 4 conditions x 3 Claude models x 2 repetitions, shuffled order (fixed seed).
Reuses the frozen v2 protocol read-only: manifest, prompts, system/user/rebuttal builders, parsers, conv_id, plan().
Provider: direct Anthropic Messages API (ANTHROPIC_API_KEY; never printed or logged). Cost = API token usage x list price.

Safety: main run refuses unless (a) v2_study/verify_protocol.py and verify_addendum.py pass, (b) --cap is given,
(c) --authorized is given, (d) a smoke test exists for every model and the projection (smoke mean cost per conversation
x (1+margin) for every remaining conversation) <= cap - ledger spend. The Anthropic API cannot report the credit balance,
so the cap is the only budget control. Every call reserves its worst-case cost first (BudgetGuard, frozen pilot code).
Resumable: completed conversations skipped; failed ones retried only with --retry-failed (new attempt; all kept).

Usage:
  python v2_study_anthropic/src/run_anthropic.py --dry-run --cap 50
  python v2_study_anthropic/src/run_anthropic.py --smoke [--smoke-cap 1.0]   # 2 conversations per model
  python v2_study_anthropic/src/run_anthropic.py --authorized --cap 50       # full run (Jack's approval)
"""
from __future__ import annotations
import argparse, json, os, sys, threading, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

VA = Path(__file__).resolve().parents[1]; EXP = VA.parent; V2SRC = EXP / "v2_study/src"
sys.path.insert(0, str(V2SRC)); sys.path.insert(0, str(EXP / "src"))
from v2_common import (PROMPTS, load, sha, system_prompt, user_turn1, redacted_turn1, rebuttal, conv_seed,   # frozen v2
                       parse_verdict, parse_confidence, parse_blame)
import run_v2                                                                                                  # frozen v2
from common import BudgetGuard, BudgetExceeded, worst_case_cost, est_tokens, now_iso                          # frozen pilot

STUDY = load(VA / "config/study_anthropic.json")
_TL = threading.local()   # per-thread count of abandoned (deadline-expired) requests for the current turn
PROV = STUDY["provider"]

@dataclass
class Paths:
    root: Path
    @property
    def turns(self): return self.root / "raw/turns.jsonl"
    @property
    def convs(self): return self.root / "raw/conversations.jsonl"
    @property
    def private(self): return self.root / "local_private/turns_full.jsonl"
    @property
    def ledger(self): return self.root / "ledger_anthropic.jsonl"
MAIN, SMOKE = Paths(VA / "results"), Paths(VA / "results/smoke")

append, read_jsonl, cases = run_v2.append, run_v2.read_jsonl, run_v2.cases
def build_jobs(case_list=None, stage="main"): return run_v2.build_jobs(STUDY, case_list, stage)
def plan(jobs, paths, retry_failed=False): return run_v2.plan(jobs, paths, retry_failed)

def prices(model):
    p = STUDY["prices_verified"][model]; return float(p["input"]), float(p["output"])

def cost_from_usage(model, u):
    """List-price cost from Anthropic usage. Cache fields are 0 here (no caching) but priced if present."""
    pin, pout = prices(model); m = STUDY["prices_verified"]["cache_multipliers_if_ever_reported"]
    return round((u.get("input_tokens") or 0) * pin + (u.get("output_tokens") or 0) * pout
                 + (u.get("cache_creation_input_tokens") or 0) * pin * m["cache_creation_5m"]
                 + (u.get("cache_read_input_tokens") or 0) * pin * m["cache_read"], 8)

def build_body(model, sys_p, msgs):
    """Anthropic body: system prompt in top-level 'system'; only user/assistant messages; no temperature/thinking/seed."""
    cfg = STUDY["targets"][model]
    body = {"model": model, "system": sys_p, "messages": msgs, "max_tokens": cfg["max_tokens"]}
    if cfg.get("temperature") is not None: body["temperature"] = cfg["temperature"]
    if cfg.get("thinking") is not None: body["thinking"] = cfg["thinking"]
    return body

def parse_response(status, j):
    """-> (text|None, info, error|None). Text = concatenation of 'text' blocks; other block types are counted, not used."""
    if status != 200 or not isinstance(j, dict) or j.get("type") == "error":
        return None, {}, {"status": status, "error": (j or {}).get("error") if isinstance(j, dict) else str(j)[:300]}
    blocks = j.get("content") or []
    text = "".join(b.get("text", "") for b in blocks if b.get("type") == "text") or None
    info = {"response_model": j.get("model"), "generation_id": j.get("id"), "stop_reason": j.get("stop_reason"),
            "block_types": [b.get("type") for b in blocks], "usage": j.get("usage") or {}}
    return text, info, None

def _post_once(body, h, timeout):
    import requests
    try:
        r = requests.post(PROV["endpoint"], headers=h, json=body, timeout=timeout)
        try: return r.status_code, r.json()
        except ValueError: return r.status_code, {"raw": r.text[:300]}
    except requests.RequestException as e:
        return -1, {"error": {"type": "network", "message": type(e).__name__}}

def _with_deadline(fn, deadline_s):
    """Run fn() in a daemon thread; give up after deadline_s wall-clock seconds (addendum deviation 14: the per-read
    socket timeout did not fire on 4 hung requests in the first launch). Returns (status, json) or (-2, deadline error)."""
    box = {}
    th = threading.Thread(target=lambda: box.update(res=fn()), daemon=True); th.start(); th.join(deadline_s)
    return box.get("res") or (-2, {"error": {"type": "deadline", "message": f"no response within {deadline_s}s; request abandoned"}})

def _post(body, deadline_s=None):
    key = os.environ.get(PROV["api_key_env"])
    if not key: raise RuntimeError(f"{PROV['api_key_env']} not set")
    h = {"x-api-key": key, "anthropic-version": PROV["anthropic_version"], "content-type": "application/json"}
    deadline_s = deadline_s or PROV.get("request_deadline_s", 240)
    tries = abandoned = 0
    while True:
        t0 = time.time()
        status, j = _with_deadline(lambda: _post_once(body, h, (30, deadline_s)), deadline_s)
        if status == -2: abandoned += 1
        if status in PROV["transient_retry_statuses"] + [-1, -2] and tries < PROV["transient_max_retries"]:
            tries += 1; time.sleep(min(60, 5 * 2 ** tries)); continue
        _TL.abandoned = abandoned
        return status, j, time.time() - t0, tries

def run_conversation(job, post, guard, attempt, paths: Paths, post_fn=_post):
    model = job["model"]; cfg = STUDY["targets"][model]; pin, pout = prices(model)
    sys_p = system_prompt(job["condition"])
    msgs = [{"role": "user", "content": user_turn1(post)}]
    public_user = redacted_turn1(job["row_id"], post)
    conv = {**job, "attempt": attempt, "started_utc": now_iso(), "status": "running", "seed_not_sent": conv_seed(job["conv_id"]),
            "turns": [], "pushed_direction": PROMPTS["pushed_direction"], "system_prompt_sha256": sha(sys_p),
            "post_sha256": sha(post), "provider": "anthropic", "settings": cfg}
    for t in (1, 2, 3):
        if t > 1:
            msgs.append({"role": "user", "content": rebuttal(t)}); public_user = rebuttal(t)
        body = build_body(model, sys_p, msgs)
        wc = worst_case_cost(est_tokens(sys_p + "".join(m["content"] for m in msgs)), cfg["max_tokens"], pin, pout)
        try: guard.reserve(wc)
        except BudgetExceeded as e: conv.update(status="paused_budget", error=str(e)); break
        t0 = now_iso(); _TL.abandoned = 0; status, j, lat, retries = post_fn(body); abandoned = getattr(_TL, "abandoned", 0)
        text, info, err = parse_response(status, j)
        u = info.get("usage", {}); cost = cost_from_usage(model, u) if not err else 0.0
        guard.settle(wc, cost, {"kind": "target", "stage": job["stage"], "conv_id": job["conv_id"], "turn": t, "model": model,
                                "attempt": attempt, "generation_id": info.get("generation_id"), "utc": now_iso(), "abandoned_requests": abandoned,
                                "input_tokens": u.get("input_tokens"), "output_tokens": u.get("output_tokens"),
                                "cache_creation_input_tokens": u.get("cache_creation_input_tokens"),
                                "cache_read_input_tokens": u.get("cache_read_input_tokens"), "price_basis": "list"})
        rec = {"conv_id": job["conv_id"], "attempt": attempt, "stage": job["stage"], "row_id": job["row_id"], "condition": job["condition"],
               "model_requested": model, "rep": job["rep"], "turn": t, "request_utc": t0, "latency_s": round(lat, 2),
               "transient_retries": retries, "abandoned_requests": abandoned, "system_prompt": sys_p, "user_message": public_user,
               "response_model": info.get("response_model"), "provider": "anthropic", "generation_id": info.get("generation_id"),
               "finish_reason": info.get("stop_reason"), "block_types": info.get("block_types"), "response": text,
               "parsed_verdict": parse_verdict(text), "parsed_blame": parse_blame(text), "parsed_confidence": parse_confidence(text),
               "input_tokens": u.get("input_tokens"), "output_tokens": u.get("output_tokens"), "cost_usd": cost, "error": err}
        append(paths.turns, rec)
        append(paths.private, {**rec, "user_message_full": msgs[-1]["content"]})
        conv["turns"].append({k: rec[k] for k in ("turn", "parsed_verdict", "parsed_blame", "parsed_confidence", "cost_usd",
                                                  "input_tokens", "output_tokens", "finish_reason", "response_model")})
        if err or not text: conv.update(status="failed", error=err or {"reason": "empty_text", "stop_reason": info.get("stop_reason")}); break
        if t == 1: conv["initial_verdict"] = rec["parsed_verdict"]
        msgs.append({"role": "assistant", "content": text})
    else:
        conv["status"] = "complete"
    conv["finished_utc"] = now_iso(); conv["cost_usd"] = round(sum(x.get("cost_usd") or 0 for x in conv["turns"]), 8)
    append(paths.convs, conv)
    return conv

def recover_interrupted(paths: Paths):
    """Close out attempts that have turn records but no conversation record (process stopped mid-conversation):
    append a conversation record with status 'interrupted' so the attempt number is consumed and it is never
    analysed; it is rerun as a new attempt with --retry-failed. Idempotent. Returns the recovered conv_ids."""
    closed = {(c["conv_id"], c["attempt"]) for c in read_jsonl(paths.convs)}
    open_ = {}
    for t in read_jsonl(paths.turns):
        k = (t["conv_id"], t["attempt"])
        if k not in closed: open_.setdefault(k, []).append(t)
    jobs = {j["conv_id"]: j for j in build_jobs(stage="main")} | {j["conv_id"]: j for j in smoke_jobs()}
    for (cid, att), ts in open_.items():
        job = jobs.get(cid, {"conv_id": cid})
        append(paths.convs, {**job, "attempt": att, "status": "interrupted", "recovered_utc": now_iso(),
                             "turns": [{k: t.get(k) for k in ("turn", "parsed_verdict", "parsed_blame", "parsed_confidence", "cost_usd",
                                                              "input_tokens", "output_tokens", "finish_reason", "response_model")} for t in ts],
                             "cost_usd": round(sum(t.get("cost_usd") or 0 for t in ts), 8),
                             "error": "process stopped mid-conversation; in-flight request (if any) abandoned, its cost is not in the ledger"})
    return [cid for cid, _ in open_]

def smoke_jobs():
    """2 conversations per model: case #1 condition A rep 0, case #2 condition D rep 0 (both framings/guidance levels)."""
    c = cases()
    return [j for j in build_jobs(c[:1], "smoke") if j["condition"] == "A" and j["rep"] == 0] + \
           [j for j in build_jobs(c[1:2], "smoke") if j["condition"] == "D" and j["rep"] == 0]

def smoke_per_conversation(paths: Paths = SMOKE):
    """Mean list-price cost per complete smoke conversation per model (None if a model has no complete smoke run)."""
    convs = [c for c in read_jsonl(paths.convs) if c["status"] == "complete"]
    return {m: (round(sum(x["cost_usd"] for x in convs if x["model"] == m) / n, 8) if (n := sum(x["model"] == m for x in convs)) else None)
            for m in STUDY["targets"]}

def preflight(todo, spent, cap, per_conv, margin):
    if cap is None: return False, "no budget cap given (--cap USD, set with Jack's approval)"
    missing = sorted({j["model"] for j in todo if per_conv.get(j["model"]) is None})
    if missing: return False, f"no smoke-test cost basis for {missing}; run --smoke first"
    proj = round(sum(per_conv[j["model"]] for j in todo) * (1 + margin), 4)
    if proj > cap - spent: return False, f"projected ${proj:.2f} > available ${cap - spent:.2f} (cap ${cap:.2f} - spent ${spent:.2f})"
    return True, f"projected ${proj:.2f} <= available ${cap - spent:.2f} (credit balance not verifiable via API)"

def verify_frozen():
    import subprocess
    for s in (EXP / "v2_study/verify_protocol.py", VA / "verify_addendum.py"):
        if subprocess.run([sys.executable, str(s)]).returncode != 0: return False
    return True

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--smoke-cap", type=float, default=STUDY["budget"]["smoke_cap_usd_default"]); ap.add_argument("--cap", type=float)
    ap.add_argument("--authorized", action="store_true"); ap.add_argument("--retry-failed", action="store_true")
    a = ap.parse_args(); margin = STUDY["budget"]["margin"]
    if a.smoke:
        paths, jobs, cap = SMOKE, smoke_jobs(), a.smoke_cap
        todo, done, att = plan(jobs, paths, a.retry_failed); spent = BudgetGuard(10**9, paths.ledger).spent
        ok, msg = (True, f"smoke cap ${cap:.2f}, spent ${spent:.4f}") if spent < cap else (False, "smoke cap reached")
    else:
        paths, jobs, cap = MAIN, build_jobs(), a.cap
        todo, done, att = plan(jobs, paths, a.retry_failed); spent = BudgetGuard(10**9, paths.ledger).spent
        ok, msg = preflight(todo, spent, cap, smoke_per_conversation(), margin)
    print(f"{'smoke' if a.smoke else 'main'}: planned={len(jobs)} done={len(done)} todo={len(todo)}; {msg}")
    if a.dry_run: return
    if not a.smoke:
        if not verify_frozen(): sys.exit("frozen v2 protocol or addendum changed; refusing")
        if not a.authorized: sys.exit("full run requires --authorized (Jack's explicit approval after seeing the estimate)")
    if not ok: sys.exit("REFUSED: " + msg)
    rec = recover_interrupted(paths)
    if rec:
        print(f"recovered {len(rec)} interrupted attempt(s): {rec}")
        todo, done, att = plan(jobs, paths, a.retry_failed)
    import pandas as pd
    df = pd.read_csv(EXP / "data/raw/AITA-YTA.csv").rename(columns={"Unnamed: 0": "row_id"}).set_index("row_id")
    man = {c["row_id"]: c["prompt_sha256"] for c in cases()}
    posts = {r: df.loc[r, "prompt"] for r in {j["row_id"] for j in todo}}
    for r, p in posts.items(): assert sha(p) == man[r], f"post hash mismatch {r}"
    guard = BudgetGuard(cap, paths.ledger)
    with ThreadPoolExecutor(1 if a.smoke else STUDY["workers"]) as ex:
        futs = [ex.submit(run_conversation, j, posts[j["row_id"]], guard, att.get(j["conv_id"], 0) + 1, paths) for j in todo]
        for f in as_completed(futs):
            c = f.result()
            print(c["exec_order"], c["conv_id"], c["condition"], c["model"], c["status"],
                  [(t["parsed_verdict"], t["parsed_blame"], t["parsed_confidence"]) for t in c["turns"]], f"${c['cost_usd']:.4f}", flush=True)
    print(f"ledger spend now ${guard.spent:.4f}")

if __name__ == "__main__":
    main()
