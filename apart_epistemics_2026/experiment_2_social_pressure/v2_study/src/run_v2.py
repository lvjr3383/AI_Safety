"""Run Experiment 2 v2 target conversations (Apart AI x Epistemics sprint, Nov 13-15 2026).
480 conversations = 30 cases x 4 conditions x 2 targets x 2 repetitions, randomized execution order (fixed seed).
Each: system prompt (condition) -> post + request -> reply 1 -> fixed rebuttal 1 -> reply 2 -> fixed rebuttal 2 -> reply 3.

Safety: refuses to run the full study unless (a) the frozen protocol checksums verify, (b) a budget cap is set in
config/study.json, (c) --authorized is passed, and (d) the projected cost of all remaining conversations (pilot per-
conversation spend x (1 + margin)) is <= min(cap - spent, OpenRouter limit_remaining from free /key). Every call also
reserves its worst-case cost against the cap (BudgetGuard). Resumable: completed conversations are skipped; failed ones
are retried only with --retry-failed, as a new attempt (all attempts kept).

Usage:
  python v2_study/src/run_v2.py --dry-run
  python v2_study/src/run_v2.py --smoke --smoke-cap 0.30          # 1 conversation per model, separate files/ledger
  python v2_study/src/run_v2.py --authorized                        # full run (needs Jack's approval + cap)
"""
from __future__ import annotations
import argparse, json, random, sys, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent)); sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from v2_common import (V2, EXP, PROMPTS, STUDY, load, sha, system_prompt, user_turn1, redacted_turn1, rebuttal, conv_id, conv_seed,
                       parse_verdict, parse_confidence, parse_blame)
from common import BudgetGuard, BudgetExceeded, worst_case_cost, est_tokens, now_iso   # frozen pilot helpers, imported unchanged

_lock = threading.Lock()

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
    def ledger(self): return self.root / "ledger_targets.jsonl"
    @property
    def key_checks(self): return self.root / "key_checks.jsonl"
MAIN, SMOKE = Paths(V2 / "results"), Paths(V2 / "results/smoke")

def append(path, rec):
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock, open(path, "a") as f: f.write(json.dumps(rec, ensure_ascii=False) + "\n")
def read_jsonl(p): return [json.loads(l) for l in open(p)] if Path(p).exists() else []

def cases(): return load(V2 / "config/manifest_v2.json")["cases"]

def build_jobs(study=STUDY, case_list=None, stage="main"):
    case_list = case_list if case_list is not None else cases()
    jobs = [{"stage": stage, "row_id": c["row_id"], "category": c["category"], "condition": cond, "model": m, "rep": r,
             "conv_id": conv_id(study["seed"], c["row_id"], cond, m, r, stage)}
            for c in case_list for cond in study["conditions"] for m in study["targets"] for r in range(study["repetitions"])]
    random.Random(study["seed"]).shuffle(jobs)
    for k, j in enumerate(jobs): j["exec_order"] = k
    return jobs

def prices(model):
    p = STUDY["prices_verified"][model]; return float(p["prompt"]), float(p["completion"])

def _chat(body):
    from common import chat
    return chat(body)

def usage(j):
    u = (j or {}).get("usage") or {}
    return {"prompt_tokens": u.get("prompt_tokens"), "completion_tokens": u.get("completion_tokens"),
            "reasoning_tokens": (u.get("completion_tokens_details") or {}).get("reasoning_tokens"), "cost_usd": u.get("cost")}

def run_conversation(job, post, guard, attempt, paths: Paths, chat_fn=_chat):
    model = job["model"]; cfg = STUDY["targets"][model]; pin, pout = prices(model)
    sys_p = system_prompt(job["condition"]); seed = conv_seed(job["conv_id"])
    msgs = [{"role": "system", "content": sys_p}, {"role": "user", "content": user_turn1(post)}]
    public_user = redacted_turn1(job["row_id"], post)
    conv = {**job, "attempt": attempt, "started_utc": now_iso(), "status": "running", "seed": seed, "turns": [],
            "pushed_direction": PROMPTS["pushed_direction"], "system_prompt_sha256": sha(sys_p), "post_sha256": sha(post),
            "settings": cfg}
    for t in (1, 2, 3):
        if t > 1:
            msgs.append({"role": "user", "content": rebuttal(t)}); public_user = rebuttal(t)
        body = {"model": model, "messages": msgs, "max_tokens": cfg["max_tokens"], "seed": seed, "provider": cfg["provider"], "usage": {"include": True}}
        if cfg.get("reasoning"): body["reasoning"] = cfg["reasoning"]
        if cfg.get("temperature") is not None: body["temperature"] = cfg["temperature"]
        wc = worst_case_cost(sum(est_tokens(m["content"]) for m in msgs), cfg["max_tokens"], pin, pout)
        try: guard.reserve(wc)
        except BudgetExceeded as e: conv.update(status="paused_budget", error=str(e)); break
        t0 = now_iso(); j, err, lat = chat_fn(body); u = usage(j)
        guard.settle(wc, u.get("cost_usd") or 0.0, {"kind": "target", "stage": job["stage"], "conv_id": job["conv_id"], "turn": t, "model": model,
                                                     "attempt": attempt, "generation_id": (j or {}).get("id"), "utc": now_iso()})
        ch = ((j or {}).get("choices") or [{}])[0]; msg = ch.get("message") or {}; content = msg.get("content")
        rec = {"conv_id": job["conv_id"], "attempt": attempt, "stage": job["stage"], "row_id": job["row_id"], "condition": job["condition"],
               "model_requested": model, "rep": job["rep"], "turn": t, "request_utc": t0, "latency_s": round(lat, 2), "seed": seed,
               "system_prompt": sys_p, "user_message": public_user, "response_model": (j or {}).get("model"), "provider": (j or {}).get("provider"),
               "generation_id": (j or {}).get("id"), "finish_reason": ch.get("finish_reason"), "response": content,
               "parsed_verdict": parse_verdict(content), "parsed_blame": parse_blame(content), "parsed_confidence": parse_confidence(content),
               **u, "error": err}
        append(paths.turns, rec)
        append(paths.private, {**rec, "user_message_full": msgs[-1]["content"], "reasoning": msg.get("reasoning")})
        conv["turns"].append({k: rec[k] for k in ("turn", "parsed_verdict", "parsed_blame", "parsed_confidence", "cost_usd", "finish_reason", "response_model", "provider")})
        if err or not content: conv.update(status="failed", error=err or {"reason": "empty_content", "finish_reason": rec["finish_reason"]}); break
        if t == 1: conv["initial_verdict"] = rec["parsed_verdict"]
        msgs.append({"role": "assistant", "content": content})
    else:
        conv["status"] = "complete"
    conv["finished_utc"] = now_iso(); conv["cost_usd"] = round(sum(x.get("cost_usd") or 0 for x in conv["turns"]), 6)
    append(paths.convs, conv)
    return conv

def plan(jobs, paths: Paths, retry_failed=False):
    convs = read_jsonl(paths.convs)
    done = {c["conv_id"] for c in convs if c["status"] == "complete"}
    att = {}
    for c in convs: att[c["conv_id"]] = max(att.get(c["conv_id"], 0), c["attempt"])
    todo = [j for j in jobs if j["conv_id"] not in done and (retry_failed or j["conv_id"] not in att)]
    return todo, done, att

def projected_cost(todo, per_conv, margin):
    return round(sum(per_conv[j["model"]] for j in todo) * (1 + margin), 4)

def preflight(todo, guard_spent, cap, balance_remaining, per_conv, margin):
    """Returns (ok, message). Refuses if projected cost exceeds the remaining cap or the available balance."""
    if cap is None: return False, "no budget cap given (--cap USD, set with Jack's approval)"
    proj = projected_cost(todo, per_conv, margin)
    room = min(cap - guard_spent, balance_remaining if balance_remaining is not None else float("inf"))
    if balance_remaining is None: return False, "OpenRouter limit_remaining unknown; refusing"
    if proj > room: return False, f"projected ${proj:.2f} > available ${room:.2f} (cap ${cap:.2f} - spent ${guard_spent:.2f}; balance ${balance_remaining:.2f})"
    return True, f"projected ${proj:.2f} <= available ${room:.2f}"

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--smoke-cap", type=float, default=0.30); ap.add_argument("--authorized", action="store_true"); ap.add_argument("--retry-failed", action="store_true")
    ap.add_argument("--cap", type=float, default=None, help="hard USD cap for the main run (cumulative ledger spend); required, set with Jack's approval")
    a = ap.parse_args()
    from estimate_v2 import pilot_per_conversation
    from common import key_status
    per_conv = pilot_per_conversation()["mean_complete"]
    margin = STUDY["budget"]["margin"]
    if a.smoke:
        paths = SMOKE; first = cases()[0]
        jobs = [j for j in build_jobs(case_list=[first], stage="smoke") if j["condition"] == "A" and j["rep"] == 0]
        cap = a.smoke_cap
    else:
        paths = MAIN; jobs = build_jobs(); cap = a.cap
    todo, done, att = plan(jobs, paths, a.retry_failed)
    guard_spent = BudgetGuard(10**9, paths.ledger).spent
    ks = key_status()
    ok, msg = preflight(todo, guard_spent, cap, ks.get("limit_remaining_usd"), per_conv, margin)
    print(f"{'smoke' if a.smoke else 'main'}: planned={len(jobs)} done={len(done)} todo={len(todo)}; {msg}")
    if a.dry_run: return
    if not a.smoke:
        import subprocess
        if subprocess.run([sys.executable, str(V2 / "verify_protocol.py")]).returncode != 0: sys.exit("frozen protocol changed; refusing")
        if not a.authorized: sys.exit("full run requires --authorized (Jack's explicit approval after seeing the estimate)")
    if not ok: sys.exit("REFUSED: " + msg)
    import pandas as pd
    df = pd.read_csv(EXP / "data/raw/AITA-YTA.csv").rename(columns={"Unnamed: 0": "row_id"}).set_index("row_id")
    posts = {r: df.loc[r, "prompt"] for r in {j["row_id"] for j in todo}}
    for r, p in posts.items():
        assert sha(p) == next(c["prompt_sha256"] for c in cases() if c["row_id"] == r), f"post hash mismatch {r}"
    guard = BudgetGuard(cap, paths.ledger)
    append(paths.key_checks, {"when": "before_run", **ks})
    with ThreadPoolExecutor(1 if a.smoke else STUDY["workers"]) as ex:
        futs = [ex.submit(run_conversation, j, posts[j["row_id"]], guard, att.get(j["conv_id"], 0) + 1, paths) for j in todo]
        for f in as_completed(futs):
            c = f.result()
            print(c["exec_order"], c["conv_id"], c["condition"], c["model"], c["status"],
                  [(t["parsed_verdict"], t["parsed_blame"], t["parsed_confidence"]) for t in c["turns"]], f"${c['cost_usd']:.4f}", flush=True)
    append(paths.key_checks, {"when": "after_run", **key_status()})
    print(f"ledger spend now ${guard.spent:.4f}")

if __name__ == "__main__":
    main()
