"""Verify the frozen Anthropic-only extension addendum (Apart AI x Epistemics sprint, Nov 13-15 2026).
Usage: python v2_study_anthropic/verify_addendum.py [--write]   (--write only before the full run)"""
import hashlib, sys
from pathlib import Path
VA = Path(__file__).resolve().parent
SUMS = VA / "ADDENDUM_CHECKSUMS.sha256"
FILES = ["PROTOCOL_ADDENDUM.md", ".gitignore", "config/study_anthropic.json", "src/run_anthropic.py", "src/estimate_anthropic.py",
         "src/analyze_anthropic.py", "tests/conftest.py", "tests/test_anthropic_prompts.py", "tests/test_anthropic_runner.py",
         "tests/test_anthropic_analysis.py", "tests/test_anthropic_freeze.py"]

def digest(rel): return hashlib.sha256((VA / rel).read_bytes()).hexdigest()

def main():
    if "--write" in sys.argv:
        SUMS.write_text("".join(f"{digest(f)}  {f}\n" for f in FILES)); print(f"wrote {len(FILES)} checksums"); return 0
    bad = [rel for h, rel in (l.split("  ", 1) for l in SUMS.read_text().splitlines()) if not (VA / rel).exists() or digest(rel) != h]
    if bad: print("ADDENDUM CHANGED:", *bad, sep="\n  "); return 1
    print(f"OK: {len(SUMS.read_text().splitlines())} addendum files match"); return 0

if __name__ == "__main__":
    sys.exit(main())
