"""The frozen v2 protocol verifies (Apart AI x Epistemics sprint, Nov 13-15 2026)."""
import subprocess, sys
from pathlib import Path
V2 = Path(__file__).resolve().parents[1]

def test_protocol_checksums_pass():
    r = subprocess.run([sys.executable, str(V2 / "verify_protocol.py")], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout
    assert "15 protocol files match" in r.stdout
