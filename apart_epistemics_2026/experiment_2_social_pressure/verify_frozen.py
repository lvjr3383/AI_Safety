"""Verify that every file of the frozen pilot checkpoint (tag exp2-pilot-frozen-v1 = commit f9f6b18) is unchanged.
Created during the Apart AI x Epistemics sprint, Nov 13-15 2026. Usage: python verify_frozen.py  (exit 1 on any mismatch)"""
import hashlib, sys
from pathlib import Path
root = Path(__file__).resolve().parent
bad = 0
for line in (root / "FROZEN_CHECKSUMS.sha256").read_text().splitlines():
    want, rel = line.split("  ", 1)
    p = root / rel
    got = hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else "MISSING"
    if got != want:
        bad += 1; print(f"CHANGED {rel}: {got}")
print(f"{'OK' if not bad else 'FAIL'}: {bad} changed of {len(open(root / 'FROZEN_CHECKSUMS.sha256').read().splitlines())} frozen files")
sys.exit(1 if bad else 0)
