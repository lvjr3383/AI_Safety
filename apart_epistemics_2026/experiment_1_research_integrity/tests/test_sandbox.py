import os, shutil
import pytest
from common import FIXTURES, WS_ROOT
from sandbox import Workspace, sandbox_available

pytestmark = pytest.mark.skipif(not sandbox_available(), reason="macOS sandbox-exec required")

@pytest.fixture
def ws():
    d = WS_ROOT / f"pytest_{os.getpid()}"
    shutil.rmtree(d, ignore_errors=True); shutil.copytree(FIXTURES / "s101_compromised" / "workspace", d)
    w = Workspace(d, python_timeout_s=30)
    yield w
    shutil.rmtree(d, ignore_errors=True); w.profile_path.unlink(missing_ok=True)

TRUTH = str((FIXTURES / "s101_compromised" / "truth.json").resolve())

def test_python_reads_and_writes_workspace(ws):
    out = ws.run_python("print(open('README.md').read()[:7]); open('notes.txt','w').write('x')")
    assert "exit code 0" in out and "# Label" in out and (ws.ws / "notes.txt").exists()

@pytest.mark.parametrize("path", [TRUTH, os.path.expanduser("~/.zshrc"), str(WS_ROOT / "other_run" / "report.md")])
def test_python_cannot_read_outside(ws, path):
    out = ws.run_python(f"open({path!r}).read(); print('LEAKED')")
    assert "LEAKED" not in out

def test_python_cannot_write_outside_or_use_network(ws):
    out = ws.run_python(f"open({str(WS_ROOT / 'escape.txt')!r}, 'w')")
    assert "PermissionError" in out and not (WS_ROOT / "escape.txt").exists()
    out = ws.run_python("import socket; socket.create_connection(('1.1.1.1', 80), timeout=3); print('NET')")
    assert "NET" not in out

def test_python_env_has_no_credentials(ws):
    out = ws.run_python("import os; print(sorted(os.environ))")
    assert "ANTHROPIC_API_KEY" not in out

@pytest.mark.parametrize("bad", ["../x", TRUTH, "/etc/passwd"])
def test_file_tools_reject_escapes(ws, bad):
    out, err = ws.call("read_file", {"path": bad})
    assert err and "outside workspace" in out

def test_file_tools_reject_symlinks(ws):
    os.symlink(TRUTH, ws.ws / "link.json")
    out, err = ws.call("read_file", {"path": "link.json"})
    assert err
