"""Verify the frozen Experiment 2 v2 protocol (Apart AI x Epistemics sprint, Nov 13-15 2026).
Usage: python v2_study/verify_protocol.py [--write]   (--write regenerates PROTOCOL_CHECKSUMS.sha256; only before inference)"""
import hashlib, sys
from pathlib import Path
V2 = Path(__file__).resolve().parent
SUMS = V2 / "PROTOCOL_CHECKSUMS.sha256"
FILES = ["PROTOCOL.md", ".gitignore", "config/manifest_v2.json", "config/prompts_v2.json", "config/study.json",
         "src/select_cases_v2.py", "src/v2_common.py", "src/run_v2.py", "src/estimate_v2.py", "src/analyze_v2.py",
         "tests/conftest.py", "tests/test_v2_prompts.py", "tests/test_v2_dataset.py", "tests/test_v2_scoring.py", "tests/test_v2_runner.py"]

def digest(rel): return hashlib.sha256((V2 / rel).read_bytes()).hexdigest()

def main():
    if "--write" in sys.argv:
        SUMS.write_text("".join(f"{digest(f)}  {f}\n" for f in FILES)); print(f"wrote {len(FILES)} checksums"); return 0
    bad = []
    for line in SUMS.read_text().splitlines():
        h, rel = line.split("  ", 1)
        if not (V2 / rel).exists() or digest(rel) != h: bad.append(rel)
    if bad: print("PROTOCOL CHANGED:", *bad, sep="\n  "); return 1
    print(f"OK: {len(SUMS.read_text().splitlines())} protocol files match"); return 0

if __name__ == "__main__":
    sys.exit(main())
