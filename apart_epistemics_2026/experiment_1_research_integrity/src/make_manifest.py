"""Write MANIFEST.json: what is pre-existing historical evidence (referenced, not copied) versus material
created during the sprint, with a sha256 for every sprint file. Run after any change, before committing."""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, sha256_file

HISTORICAL = {
    "status": "pre-existing research, completed before the Apart AI x Epistemics sprint; referenced only, no files copied into this experiment",
    "repository": "https://github.com/lvjr3383/ai-village-codex-judging-evidence",
    "commit": "b41bddbfb61541ca2c1662f10fac53739697120c",
    "files_sha256": {
        "README.md": "d3de92bfe7c69f8c2362f346052828a20f2cf1cc71f6ff4deae2567bcb4892bf",
        "archived_generator.py": "5107fa3d0fda1b5b8b3e780ede712cf380a98eca809406a6d53be647d8f5f7b2",
        "public-report-2442b493.md": "d8737dbbc54742987cab14f139b5c57c23a260e9db87080a09b5e1ba30ab6ab5",
        "results.json": "0e0b551f6bc03188f64ef4f5d3ee91582789a95b914afc7b685d644befde143b",
        "source-events.jsonl": "974046dac0aa1c7ee89d7da320bcb829ecdbb37a4e28c0bd7a1409e2593cfee4",
        "verify.py": "d28215f7d1407422d0fc4c270b1f5ed102b1fc2a5cb168ff1b68ee635f874d9d"},
    "how_used": "Read-only inspection to choose the failure mode. verify.py and archived_generator.py were read, not executed.",
}
SKIP_DIRS = {".venv", "__pycache__", ".pytest_cache", "dryrun"}

def sprint_files() -> dict:
    out = {}
    for p in sorted(ROOT.rglob("*")):
        rel = p.relative_to(ROOT)
        if not p.is_file() or rel.as_posix() in ("MANIFEST.json", "report/report.md") or SKIP_DIRS & set(rel.parts) or rel.suffix == ".pyc": continue
        out[rel.as_posix()] = sha256_file(p)
    return out

def main():
    files = sprint_files()
    kinds = lambda pre: sorted(k for k in files if k.startswith(pre))
    manifest = {"experiment": "Experiment 1: research integrity under compromised evidence",
                "historical_reference": HISTORICAL,
                "sprint_created": {"status": "created during the Apart AI x Epistemics sprint (Nov 2026)",
                                   "synthetic_fixtures": len(kinds("fixtures/")), "experimental_results": len(kinds("results/raw/")),
                                   "files_sha256": files}}
    (ROOT / "MANIFEST.json").write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n")
    print(f"MANIFEST.json: {len(files)} sprint files")

if __name__ == "__main__":
    main()
