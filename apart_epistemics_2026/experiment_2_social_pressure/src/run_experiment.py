"""Run target-model conversations for Experiment 2 (Apart AI x Epistemics sprint, Nov 13-15 2026).

Each conversation: system prompt (condition A-D) -> post + request -> reply 1 -> rebuttal 1 -> reply 2 -> rebuttal 2 -> reply 3.
Writes one JSONL record per turn (results/raw/turns.jsonl, post text redacted) and one per conversation attempt
(results/raw/conversations.jsonl). Failed attempts are logged and never overwritten; a retry is a new attempt.

Usage:
  python run_experiment.py --stage pilot --dry-run          # plan + projection, no calls
  python run_experiment.py --stage pilot --smoke            # condition A, pilot case 1, both targets
  python run_experiment.py --stage pilot                    # all remaining pilot conversations
"""
from __future__ import annotations
import argparse, json, random, sys, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from common import (PROMPTS, CONFIGS, DATA, RESULTS, PRIVATE, load_json, sha256_text, now_iso, system_prompt, user_turn1,
                    redacted_turn1, parse_verdict, parse_confidence, rebuttal_key, pushed_direction, BudgetGuard,
                    BudgetExceeded, worst_case_cost, est_tokens, chat, usage_fields, model_prices, key_status)

RAWDIR = RESULTS / "raw"
TURNS, CONVS = RAWDIR / "turns.jsonl", RAWDIR / "conversations.jsonl"
PRIV_TURNS = PRIVATE / "turns_full.jsonl"
RESOLVED = RESULTS / "resolved_target_config.json"
_write_lock = threading.Lock()

def append(path, rec):
    path.parent.mkdir(parents=True, exist_ok=True)
    with _write_lock, open(path, "a") as f: f.write(json.dumps(rec, ensure_ascii=False) + "\n")

def read_jsonl(path):
    return [json.loads(l) for l in open(path)] if path.exists() else []

def conv_seed(cid: str) -> int:
    """Per-conversation seed. Masked to 31 bits because Google AI Studio rejects seeds outside int32
    (6 Gemini first attempts failed with HTTP 400 before this fix; GPT-5.5 conversations run before the fix
    may carry the unmasked value, which is recorded in each turn record)."""
    return int(cid[:8], 16) & 0x7FFFFFFF

def conv_id(seed, stage, row_id, cond, model, rep):
    return sha256_text(f"{seed}:{stage}:{row_id}:{cond}:{model}:{rep}")[:12]

def build_jobs(stage: str):
    exp = load_json(CONFIGS / "experiment.json"); st = exp["stages"][stage]
    man = load_json(DATA / "manifest.json")
    cases = man["pilot_cases"] if st["case_set"] == "pilot" else man["main_cases"]
    jobs = [{"stage": stage, "row_id": c["row_id"], "case_index": i, "category": c["category"], "condition": cond,
             "model": m, "rep": r, "conv_id": conv_id(exp["seed"], stage, c["row_id"], cond, m, r)}
            for i, c in enumerate(cases) for cond in exp["conditions"] for m in st["targets"] for r in range(st["repetitions"])]
    random.Random(exp["seed"]).shuffle(jobs)          # randomized execution order across conditions/models/cases
    for k, j in enumerate(jobs): j["exec_order"] = k
    return jobs, st, exp

def target_cfg(model):
    cfg = dict(load_json(CONFIGS / "models.json")["targets"][model])
    if RESOLVED.exists():
        res = load_json(RESOLVED).get(model)
        if res: cfg["reasoning"] = res["reasoning"]
    return cfg

def run_conversation(job, posts, guard: BudgetGuard, attempt: int):
    model = job["model"]; cfg = target_cfg(model)
    pin, pout = model_prices(model)
    post = posts[job["row_id"]]
    sys_p = system_prompt(job["condition"])
    seed = conv_seed(job["conv_id"])
    msgs = [{"role": "system", "content": sys_p}, {"role": "user", "content": user_turn1(post)}]
    public_user = [redacted_turn1(job["row_id"], post)]
    conv = {**job, "attempt": attempt, "started_utc": now_iso(), "status": "running", "turns": [], "seed": seed,
            "system_prompt_sha256": sha256_text(sys_p), "post_sha256": sha256_text(post),
            "settings": {k: cfg.get(k) for k in ("provider", "max_tokens", "reasoning", "temperature")}}
    initial = None
    for t in range(1, 4):
        if t > 1:
            key = rebuttal_key(initial)
            utext = PROMPTS["rebuttal_1" if t == 2 else "rebuttal_2"][key]
            msgs.append({"role": "user", "content": utext}); public_user.append(utext)
            conv["rebuttal_key"] = key; conv["pushed_direction"] = pushed_direction(initial)
        body = {"model": model, "messages": msgs, "max_tokens": cfg["max_tokens"], "seed": seed,
                "provider": cfg["provider"], "usage": {"include": True}}
        if cfg.get("reasoning"): body["reasoning"] = cfg["reasoning"]
        if cfg.get("temperature") is not None: body["temperature"] = cfg["temperature"]
        wc = worst_case_cost(sum(est_tokens(m["content"]) for m in msgs), cfg["max_tokens"], pin, pout)
        try:
            guard.reserve(wc)
        except BudgetExceeded as e:
            conv.update(status="paused_budget", error=str(e)); break
        t0 = now_iso()
        j, err, lat = chat(body)
        u = usage_fields(j)
        guard.settle(wc, u.get("cost_usd") or 0.0, {"kind": "target", "conv_id": job["conv_id"], "turn": t, "model": model,
                                                     "attempt": attempt, "generation_id": (j or {}).get("id"), "utc": now_iso()})
        choice = ((j or {}).get("choices") or [{}])[0]
        msg = choice.get("message") or {}
        content = msg.get("content")
        rec = {"conv_id": job["conv_id"], "attempt": attempt, "stage": job["stage"], "row_id": job["row_id"],
               "condition": job["condition"], "model_requested": model, "rep": job["rep"], "turn": t,
               "request_utc": t0, "latency_s": round(lat, 2), "seed": seed,
               "settings": {k: body.get(k) for k in ("max_tokens", "reasoning", "temperature", "provider")},
               "system_prompt": sys_p, "user_message": public_user[-1],
               "response_model": (j or {}).get("model"), "provider": (j or {}).get("provider"),
               "generation_id": (j or {}).get("id"), "system_fingerprint": (j or {}).get("system_fingerprint"),
               "finish_reason": choice.get("finish_reason"), "native_finish_reason": choice.get("native_finish_reason"),
               "response": content, "reasoning_returned": bool(msg.get("reasoning") or msg.get("reasoning_details")),
               "parsed_verdict": parse_verdict(content), "parsed_confidence": parse_confidence(content),
               **u, "error": err}
        append(TURNS, rec)
        append(PRIV_TURNS, {**rec, "user_message_full": msgs[-1]["content"], "reasoning": msg.get("reasoning"),
                            "reasoning_details": msg.get("reasoning_details")})
        conv["turns"].append({"turn": t, "verdict": rec["parsed_verdict"], "confidence": rec["parsed_confidence"],
                              "cost_usd": u.get("cost_usd"), "reasoning_tokens": u.get("reasoning_tokens"),
                              "completion_tokens": u.get("completion_tokens"), "prompt_tokens": u.get("prompt_tokens"),
                              "finish_reason": rec["finish_reason"], "response_model": rec["response_model"],
                              "provider": rec["provider"]})
        if err or not content:
            conv.update(status="failed", error=err or {"reason": "empty_content", "finish_reason": rec["finish_reason"]}); break
        if t == 1:
            initial = rec["parsed_verdict"]
            conv["initial_verdict_unparsed"] = initial == "unparsed"
        msgs.append({"role": "assistant", "content": content})   # visible reply only; reasoning is not fed back
    else:
        conv["status"] = "complete"
    conv["finished_utc"] = now_iso()
    conv["cost_usd"] = round(sum(x.get("cost_usd") or 0 for x in conv["turns"]), 6)
    append(CONVS, conv)
    return conv

def completed_ids():
    return {c["conv_id"] for c in read_jsonl(CONVS) if c["status"] == "complete"}

def attempts_by_id():
    d = {}
    for c in read_jsonl(CONVS): d[c["conv_id"]] = max(d.get(c["conv_id"], 0), c["attempt"])
    return d

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="pilot"); ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--retry-failed", action="store_true")
    ap.add_argument("--cap", type=float, help="override cap (must not exceed configured cap)")
    a = ap.parse_args()
    jobs, st, exp = build_jobs(a.stage)
    cap = st["budget_cap_usd"]
    if cap is None: sys.exit("No budget cap configured for this stage; set one explicitly (with approval) before running.")
    if a.cap is not None: cap = min(cap, a.cap)
    if a.smoke:
        first = load_json(DATA / "manifest.json")["pilot_cases"][0]["row_id"]
        jobs = [j for j in jobs if j["row_id"] == first and j["condition"] == "A" and j["rep"] == 0]
    done, att = completed_ids(), attempts_by_id()
    failed_before = {cid for cid, n in att.items() if cid not in done}
    todo = [j for j in jobs if j["conv_id"] not in done and (a.retry_failed or j["conv_id"] not in failed_before)]
    print(f"stage={a.stage} cap=${cap:.2f} planned={len(jobs)} done={len(done & {j['conv_id'] for j in jobs})} "
          f"todo={len(todo)} failed_not_retried={len([j for j in jobs if j['conv_id'] in failed_before and not a.retry_failed])}")
    if a.dry_run:
        for j in todo: print(j["exec_order"], j["conv_id"], j["row_id"], j["condition"], j["model"], j["rep"])
        return
    import pandas as pd
    from prepare_data import load_yta
    df = load_yta(); posts = {int(r): df.loc[r, "prompt"] for r in {j["row_id"] for j in todo}}
    guard = BudgetGuard(cap)
    print(f"ledger spend so far ${guard.spent:.4f}")
    append(RESULTS / "key_checks.jsonl", {"when": "before_run", "smoke": a.smoke, **key_status()})
    workers = 1 if a.smoke else exp.get("workers", 4)
    results = []
    with ThreadPoolExecutor(workers) as ex:
        futs = {ex.submit(run_conversation, j, posts, guard, att.get(j["conv_id"], 0) + 1): j for j in todo}
        for f in as_completed(futs):
            c = f.result(); results.append(c)
            print(c["exec_order"], c["conv_id"], c["condition"], c["model"], c["status"],
                  [t["verdict"] for t in c["turns"]], f"${c['cost_usd']:.4f}", flush=True)
    append(RESULTS / "key_checks.jsonl", {"when": "after_run", "smoke": a.smoke, **key_status()})
    print(f"ledger spend now ${guard.spent:.4f}; statuses:", {s: sum(c['status'] == s for c in results) for s in {c['status'] for c in results}})

if __name__ == "__main__":
    main()
