"""Write FREEZE_v2.json: sha256 of every file that defines Experiment 1 v2. run_v2.py refuses to run if any changes.
Usage: python src/freeze_v2.py [--note "..."]   (re-freezing is only allowed as a logged scorer bump, see protocol_v2.md)"""
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, dump_json, load_json, now_iso, sha256_file

FILES = ["protocol_v2.md", "configs/experiment_v2.json", "configs/scoring_v2.json", "configs/experiment.json", "configs/prompts.json",
         "FIXTURE_CHECKSUMS_v2.sha256", "src/generate_fixtures_v2.py", "src/score_v2.py", "src/analyze_v2.py", "src/run_v2.py",
         "src/harness.py", "src/runtime_api.py", "src/sandbox.py", "src/common.py", "src/score.py"]

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--note", default="initial v2 freeze, before any v2 agent session"); a = ap.parse_args()
    p = ROOT / "FREEZE_v2.json"
    history = load_json(p).get("history", []) if p.exists() else []
    rec = {"frozen_at": now_iso(), "note": a.note, "files_sha256": {f: sha256_file(ROOT / f) for f in FILES}}
    dump_json(p, {**rec, "history": history + [{"frozen_at": rec["frozen_at"], "note": a.note}]})
    print(f"froze {len(FILES)} files at {rec['frozen_at']}")
