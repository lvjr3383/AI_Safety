"""Run one research-agent session in an isolated workspace and keep the full audit trail.

Every run directory (results/raw/<run_id>/) holds:
  meta.json            condition, fixture, runtime, model, prompt text + hashes, git commit, status
  events.jsonl         raw runtime events (API requests/responses or Claude Code stream-json), append-only
  normalized.jsonl     runtime-independent event list the scorer reads
  workspace_final/     the agent's workspace at the end (report.md lives here)
  workspace_diff.json  files added / changed / removed relative to the fixture
Failed, refused and truncated runs are kept; status says why.
"""
from __future__ import annotations
import shutil, subprocess, sys, traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (EXPERIMENT, FIXTURES, RAW, ROOT, WS_ROOT, PROMPTS, BudgetExceeded, append_jsonl, dump_json,
                    now_iso, sha256_text, task_prompt, tree_hashes)

def git_commit() -> str:
    try: return subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    except Exception: return "unknown"

def prepare_workspace(run_id: str, fixture_id: str) -> Path:
    src = FIXTURES / fixture_id / "workspace"
    ws = WS_ROOT / run_id
    if ws.exists(): raise FileExistsError(f"workspace already exists: {ws}")
    WS_ROOT.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, ws, symlinks=False)
    if tree_hashes(ws) != tree_hashes(src): raise RuntimeError("workspace copy does not match fixture")
    return ws

def diff_trees(before: dict, after: dict) -> dict:
    return {"added": sorted(set(after) - set(before)), "removed": sorted(set(before) - set(after)),
            "changed": sorted(k for k in set(before) & set(after) if before[k] != after[k])}

class Recorder:
    def __init__(self, out: Path):
        self.out = out; self.n = 0
        out.mkdir(parents=True, exist_ok=False)
    def raw(self, obj): append_jsonl(self.out / "events.jsonl", {"ts": now_iso(), **obj})
    def norm(self, kind: str, **kw):
        append_jsonl(self.out / "normalized.jsonl", {"i": self.n, "ts": now_iso(), "kind": kind, **kw}); self.n += 1

def run_session(run_id: str, condition: str, seed: int, runtime, out_root: Path = RAW) -> dict:
    """runtime: object with .name, .model and .run(ws, prompt, system, rec) -> status dict."""
    cond = EXPERIMENT["conditions"][condition]
    fid = f"s{seed}_{cond['evidence']}"
    prompt, system = task_prompt(cond["pressure"]), PROMPTS["system"]
    out = Path(out_root) / run_id; rec = Recorder(out)
    meta = {"run_id": run_id, "condition": condition, **cond, "seed": seed, "fixture_id": fid,
            "runtime": runtime.name, "model": runtime.model, "system_prompt": system, "task_prompt": prompt,
            "system_sha256": sha256_text(system), "task_sha256": sha256_text(prompt),
            "git_commit": git_commit(), "started": now_iso(), "status": "started"}
    dump_json(out / "meta.json", meta)
    ws = prepare_workspace(run_id, fid); before = tree_hashes(ws)
    try:
        meta.update(runtime.run(ws, prompt, system, rec))
    except BudgetExceeded as e:
        meta.update({"status": "budget_exceeded", "error": str(e)})
    except Exception as e:
        meta.update({"status": "harness_error", "error": f"{type(e).__name__}: {e}", "traceback": traceback.format_exc()})
    after = tree_hashes(ws)
    shutil.copytree(ws, out / "workspace_final", symlinks=True)
    dump_json(out / "workspace_diff.json", {"before": before, "after": after, **diff_trees(before, after)})
    meta.update({"finished": now_iso(), "report_present": (ws / "report.md").is_file()})
    dump_json(out / "meta.json", meta)
    shutil.rmtree(ws, ignore_errors=True)
    (ws.parent / (ws.name + ".sb")).unlink(missing_ok=True)
    return meta
