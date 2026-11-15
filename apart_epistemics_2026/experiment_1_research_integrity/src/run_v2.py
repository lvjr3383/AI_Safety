"""Launch Experiment 1 v2 sessions (exploratory). v1 runs, fixtures and scores are untouched.

  python src/run_v2.py --dry-run careful            # zero cost, scripted agent, results/v2/dryrun/ (gitignored)
  python src/run_v2.py --smoke --allow-paid         # 6 sessions: smoke conditions x 3 models, seed 101
  python src/run_v2.py --full  --allow-paid         # every remaining (model, condition, seed); smoke sessions count

Before any paid session: FREEZE_v2.json must verify, fixture checksums must match, every model must pass the free
access check, and the projected cost of the remaining sessions must fit under the incremental cap. The cap
(incremental_cap_usd over the ledger total of all non-v2 runs) is enforced per request by BudgetGuard.
After each session, automatic integrity checks run; a failure that could invalidate data stops the run.
"""
from __future__ import annotations
import argparse, datetime as dt, json, random, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import EXPERIMENT, LEDGER, RESULTS, ROOT, BudgetGuard, append_jsonl, load_json, now_iso, read_jsonl, sha256_file
from harness import run_session
from score import parse_headline

V2 = load_json(ROOT / "configs" / "experiment_v2.json")
FIXTURES_V2 = ROOT / "fixtures_v2"
OUT_V2 = RESULTS / "v2"
KEY_RE = re.compile(r"sk-ant-[A-Za-z0-9_\-]{8,}")

def fid(seed, cond): c = V2["conditions"][cond]; return f"s{seed}_{c['variant']}_{c['evidence']}"
def tag(model): return model.removeprefix("claude-")

def verify_freeze() -> dict:
    fz = load_json(ROOT / "FREEZE_v2.json")
    bad = [p for p, h in fz["files_sha256"].items() if sha256_file(ROOT / p) != h]
    if bad: sys.exit(f"refusing: frozen v2 files changed since {fz['frozen_at']}: {bad}")
    for line in (ROOT / "FIXTURE_CHECKSUMS_v2.sha256").read_text().splitlines():
        h, rel = line.split("  ", 1)
        if sha256_file(ROOT / rel) != h: sys.exit(f"refusing: v2 fixture file changed: {rel}")
    return fz

def done_keys(raw: Path) -> set:
    out = set()
    for m in raw.glob("*/meta.json"):
        d = load_json(m)
        if d.get("status") == "completed": out.add((d["model"], d["condition"], d["seed"]))
    return out

def plan(models, conditions, seeds, skip=frozenset(), order_seed=20261115) -> list:
    jobs = [(m, c, s) for m in models for c in conditions for s in seeds if (m, c, s) not in skip]
    random.Random(order_seed).shuffle(jobs)
    return jobs

def baseline_spend() -> float:
    return sum(e["cost_usd"] for e in read_jsonl(LEDGER) if not e["run_id"].startswith("v2_"))

def integrity(run_dir: Path, model: str) -> dict:
    meta = load_json(run_dir / "meta.json")
    report = (run_dir / "workspace_final" / "report.md")
    rtext = report.read_text(errors="replace") if report.is_file() else ""
    leak = any(KEY_RE.search(p.read_text(errors="replace")) for p in run_dir.rglob("*") if p.is_file())
    chk = {"run_id": meta["run_id"], "ts": now_iso(), "status_completed": meta.get("status") == "completed",
           "served_model_ok": meta.get("served_models") == [model], "report_present": bool(rtext),
           "headline_parsed": parse_headline(rtext)["headline_raw"] is not None, "no_key_in_logs": not leak,
           "fixture_ok": meta.get("fixture_id") is not None and (FIXTURES_V2 / meta["fixture_id"]).is_dir()}
    chk["ok"] = all(v for k, v in chk.items() if k not in ("run_id", "ts"))
    chk["fatal"] = not (chk["served_model_ok"] and chk["no_key_in_logs"] and chk["fixture_ok"]) or meta.get("status") == "harness_error"
    return chk

def make_runtime(model, guard, run_id, dry):
    from runtime_api import AnthropicAPIRuntime
    if dry:
        from scripted_client import ScriptedClient
        rt = AnthropicAPIRuntime(ScriptedClient(dry), guard, run_id, model=model); rt.name = f"dryrun_{dry}"; return rt
    import anthropic
    from common import load_api_key
    return AnthropicAPIRuntime(anthropic.Anthropic(api_key=load_api_key()), guard, run_id, model=model)

def check_models(models):
    import anthropic
    from common import load_api_key
    client = anthropic.Anthropic(api_key=load_api_key())
    for m in models:
        got = client.models.retrieve(m)
        append_jsonl(RESULTS / "model_checks.jsonl", {"ts": now_iso(), "requested": m, "ok": got.id == m, "id": got.id, "context": "v2"})
        if got.id != m: sys.exit(f"refusing: model check failed for {m} (got {got.id})")

def main(argv=None):
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--smoke", action="store_true"); g.add_argument("--full", action="store_true")
    g.add_argument("--dry-run", choices=["naive", "careful"])
    ap.add_argument("--allow-paid", action="store_true")
    a = ap.parse_args(argv)
    models, seeds = V2["models"], V2["seeds"]
    if a.dry_run:
        raw = OUT_V2 / "dryrun"; guard = BudgetGuard(1e9, raw / "ledger.jsonl")
        jobs = [(m, c, seeds[0]) for m in models[:1] for c in V2["conditions"]]
    else:
        if not a.allow_paid: sys.exit("refusing: paid runs need --allow-paid")
        fz = verify_freeze()
        raw = OUT_V2 / "raw"; raw.mkdir(parents=True, exist_ok=True)
        conds = V2["smoke"]["conditions"] if a.smoke else list(V2["conditions"])
        jobs = plan(models, conds, [V2["smoke"]["seed"]] if a.smoke else seeds, done_keys(raw))
        base = baseline_spend(); cap = base + V2["incremental_cap_usd"]
        guard = BudgetGuard(cap, LEDGER)
        basis = V2["projected_cost_basis_usd_per_session"]
        projected = sum(basis[m] for m, _, _ in jobs)
        print(f"freeze {fz['frozen_at']} ok; {len(jobs)} sessions to run; projected ${projected:.2f}; "
              f"v2 spent so far ${guard.spent - base:.2f}; cap ${V2['incremental_cap_usd']:.2f}")
        if guard.spent + projected > cap: sys.exit("refusing: projected cost exceeds the remaining v2 cap")
        check_models(models)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for model, cond, seed in jobs:
        run_id = f"v2_{tag(model)}_{cond}_s{seed}_{stamp}"
        meta = run_session(run_id, cond, seed, make_runtime(model, guard, run_id, a.dry_run), raw,
                           conditions=V2["conditions"], fixtures_root=FIXTURES_V2, fixture_id=fid(seed, cond))
        chk = integrity(raw / run_id, model)
        append_jsonl((raw.parent / "integrity.jsonl") if not a.dry_run else raw / "integrity.jsonl", chk)
        print(f"{run_id}: {meta['status']} cost=${meta.get('cost_usd', 0):.4f} integrity={'ok' if chk['ok'] else chk}")
        if meta["status"] == "budget_exceeded": print("budget cap reached; stopping"); break
        if chk["fatal"] and not a.dry_run: print("fatal integrity failure; stopping"); break

if __name__ == "__main__":
    main()
