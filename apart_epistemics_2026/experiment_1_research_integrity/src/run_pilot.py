"""Launch Experiment 1 sessions.

Paid runs need BOTH --allow-paid and --cap-usd; the cap spans every run via results/cost_ledger.jsonl.
  python src/run_pilot.py --dry-run naive                      # zero cost, scripted agent, results/dryrun/
  python src/run_pilot.py --runtime anthropic_api --allow-paid --cap-usd 15 --runs-per-condition 1   # smoke test
Run order interleaves the four conditions in a fixed shuffled order so time-of-day drift is not confounded with condition.
"""
from __future__ import annotations
import argparse, datetime as dt, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import EXPERIMENT, LEDGER, RAW, RESULTS, BudgetGuard
from harness import run_session

def plan(conditions, runs_per_condition: int, seeds, order_seed: int = 20261114) -> list:
    jobs = [(c, seeds[r % len(seeds)], r) for c in conditions for r in range(runs_per_condition)]
    random.Random(order_seed).shuffle(jobs)
    return jobs

def make_runtime(kind: str, guard, run_id: str, dry_policy=None, model=None):
    if dry_policy:
        from runtime_api import AnthropicAPIRuntime
        from scripted_client import ScriptedClient
        rt = AnthropicAPIRuntime(ScriptedClient(dry_policy), guard, run_id, model=model); rt.name = f"dryrun_{dry_policy}"
        return rt
    if kind == "anthropic_api":
        import anthropic
        from common import load_api_key
        from runtime_api import AnthropicAPIRuntime
        return AnthropicAPIRuntime(anthropic.Anthropic(api_key=load_api_key()), guard, run_id, model=model)
    if kind == "claude_code":
        from runtime_claude_code import ClaudeCodeRuntime
        if model: raise ValueError("--model is only supported for the anthropic_api runtime")
        return ClaudeCodeRuntime(guard, run_id)
    raise ValueError(kind)

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--runtime", choices=["anthropic_api", "claude_code"], default="anthropic_api")
    ap.add_argument("--conditions", nargs="*", default=list(EXPERIMENT["conditions"]))
    ap.add_argument("--runs-per-condition", type=int, default=EXPERIMENT["pilot"]["runs_per_condition"])
    ap.add_argument("--seeds", type=int, nargs="*", default=EXPERIMENT["fixtures"]["seeds"],
                    help="e.g. --seeds 101 with --runs-per-condition 1 gives every condition the same fixture seed")
    ap.add_argument("--model", help="override the configured model (anthropic_api only), e.g. claude-haiku-5-5")
    ap.add_argument("--allow-paid", action="store_true")
    ap.add_argument("--cap-usd", type=float)
    ap.add_argument("--dry-run", choices=["naive", "careful"], help="scripted offline agent; writes to results/dryrun/")
    a = ap.parse_args(argv)
    if a.dry_run:
        out, guard = RESULTS / "dryrun", BudgetGuard(1e9, RESULTS / "dryrun" / "ledger.jsonl")
    else:
        if not (a.allow_paid and a.cap_usd): sys.exit("refusing: paid runs need --allow-paid and --cap-usd")
        out, guard = RAW, BudgetGuard(a.cap_usd, LEDGER)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for cond, seed, rep in plan(a.conditions, a.runs_per_condition, a.seeds):
        tag = f"_{a.model.removeprefix('claude-')}" if a.model else ""
        run_id = f"{a.dry_run and 'dry_' + a.dry_run or a.runtime}{tag}_{cond}_s{seed}_r{rep}_{stamp}"
        meta = run_session(run_id, cond, seed, make_runtime(a.runtime, guard, run_id, a.dry_run, a.model), out)
        print(f"{run_id}: {meta['status']}  cost=${meta.get('cost_usd', 0):.4f}  total=${guard.spent:.4f}")
        if meta["status"] == "budget_exceeded": print("budget cap reached; stopping"); break

if __name__ == "__main__":
    main()
