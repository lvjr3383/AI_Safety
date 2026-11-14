"""Frozen v2 protocol and the Anthropic addendum both verify (Apart sprint Nov 13-15 2026)."""
import subprocess, sys
from pathlib import Path
VA = Path(__file__).resolve().parents[1]

def test_addendum_and_v2_protocol_verify():
    r = subprocess.run([sys.executable, str(VA / "verify_addendum.py")], capture_output=True, text=True)
    assert r.returncode == 0 and "11 addendum files match" in r.stdout, r.stdout
    r = subprocess.run([sys.executable, str(VA.parent / "v2_study/verify_protocol.py")], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout
