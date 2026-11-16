"""macOS sandbox-exec profiles and the agent's tool implementations.

The agent can read and write only its own workspace. Reads of /Users (the repo, fixture truth, home dir,
credentials), of the shared workspace root (other runs) and of /Volumes are denied; writes are denied
everywhere except the workspace. Python runs with network denied. SBPL applies the last matching rule,
so the per-run allow rules below override the broad denies.
"""
from __future__ import annotations
import os, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, WS_ROOT

SANDBOX_EXEC = "/usr/bin/sandbox-exec"
PYTHON = "/usr/bin/python3"

def _q(p) -> str: return '"' + str(Path(p).resolve()).replace('"', '\\"') + '"'

def profile(ws: Path, allow_network=False, extra_read=(), extra_write=()) -> str:
    deny_read = ["/Users", "/Volumes", str(WS_ROOT), str(ROOT)]
    lines = ["(version 1)", "(allow default)"]
    if not allow_network: lines.append("(deny network*)")
    lines.append("(deny file-read* " + " ".join(f"(subpath {_q(p)})" for p in deny_read) + ")")
    lines.append("(allow file-read* " + " ".join(f"(subpath {_q(p)})" for p in [ws, *extra_read]) + ")")
    lines.append("(deny file-write*)")
    lines.append("(allow file-write* " + " ".join(f"(subpath {_q(p)})" for p in [ws, *extra_write])
                 + ' (literal "/dev/null") (literal "/dev/tty"))')
    return "\n".join(lines) + "\n"

def sandbox_available() -> bool:
    return sys.platform == "darwin" and Path(SANDBOX_EXEC).exists()

class Workspace:
    """Agent-facing file and Python tools, all confined to one directory."""
    def __init__(self, ws: Path, python_timeout_s=60, max_output_chars=20000):
        self.ws = Path(ws).resolve(); self.timeout = python_timeout_s; self.max_out = max_output_chars
        self.profile_path = self.ws.parent / (self.ws.name + ".sb")
        self.profile_path.write_text(profile(self.ws))

    def _resolve(self, rel: str) -> Path:
        p = (self.ws / rel).resolve()
        if p != self.ws and self.ws not in p.parents: raise PermissionError(f"path outside workspace: {rel}")
        cur = self.ws
        for part in p.relative_to(self.ws).parts:
            cur = cur / part
            if cur.is_symlink(): raise PermissionError(f"symlinks are not allowed: {rel}")
        return p

    def _clip(self, s: str) -> str:
        return s if len(s) <= self.max_out else s[: self.max_out] + f"\n[... truncated, {len(s) - self.max_out} more characters]"

    def list_files(self, path: str = ".") -> str:
        base = self._resolve(path)
        if not base.is_dir(): raise FileNotFoundError(path)
        rows = [p.relative_to(self.ws).as_posix() + ("/" if p.is_dir() else f"  ({p.stat().st_size} bytes)")
                for p in sorted(base.rglob("*")) if not p.is_symlink()]
        return "\n".join(rows) or "(empty)"

    def read_file(self, path: str, offset: int = 0, limit: int = 0) -> str:
        lines = self._resolve(path).read_text().splitlines(keepends=True)
        sel = lines[offset: offset + limit] if limit else lines[offset:]
        return self._clip("".join(sel))

    def write_file(self, path: str, content: str) -> str:
        p = self._resolve(path); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(content)
        return f"wrote {len(content)} characters to {p.relative_to(self.ws).as_posix()}"

    def run_python(self, code: str) -> str:
        if not sandbox_available(): raise RuntimeError("sandbox-exec unavailable; refusing to run agent code unsandboxed")
        env = {"PATH": "/usr/bin:/bin", "HOME": str(self.ws), "LANG": "en_US.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
        try:
            r = subprocess.run([SANDBOX_EXEC, "-f", str(self.profile_path), PYTHON, "-I", "-B", "-"], input=code, cwd=self.ws,
                               env=env, capture_output=True, text=True, timeout=self.timeout)
            out = f"exit code {r.returncode}\n--- stdout ---\n{r.stdout}" + (f"--- stderr ---\n{r.stderr}" if r.stderr else "")
        except subprocess.TimeoutExpired as e:
            out = f"timed out after {self.timeout}s\n--- stdout ---\n{e.stdout or ''}"
        return self._clip(out)

    def call(self, name: str, args: dict) -> tuple:
        """Returns (output text, is_error)."""
        fn = {"list_files": self.list_files, "read_file": self.read_file,
              "write_file": self.write_file, "run_python": self.run_python}.get(name)
        if fn is None: return f"unknown tool: {name}", True
        try: return fn(**args), False
        except Exception as e: return f"{type(e).__name__}: {e}", True

TOOL_SCHEMAS = [
    {"name": "list_files", "description": "List files under a directory of the project (default: the project root).",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "additionalProperties": False}},
    {"name": "read_file", "description": "Read a text file from the project. Optional 0-based line offset and line limit.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "offset": {"type": "integer"}, "limit": {"type": "integer"}},
                      "required": ["path"], "additionalProperties": False}},
    {"name": "write_file", "description": "Create or overwrite a text file in the project.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
                      "required": ["path", "content"], "additionalProperties": False}},
    {"name": "run_python", "description": "Run a Python 3 script (standard library only, no network) with the project directory as the working directory. Returns stdout and stderr.",
     "input_schema": {"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"], "additionalProperties": False}},
]
