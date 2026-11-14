"""Claude Code headless runtime: `claude -p --bare` inside a sandbox-exec profile.

--bare skips CLAUDE.md discovery, auto-memory, hooks, plugins and keychain/OAuth (API key only). HOME and TMPDIR
point at a throwaway directory, and the OS sandbox denies reads of /Users (repo, fixture truth, the real
home directory) except the Claude Code install itself. Network stays on because the CLI must reach the API.
Claude Code's default system prompt is kept; the experiment's system text is appended.
"""
from __future__ import annotations
import json, os, shutil, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import EXPERIMENT, BudgetGuard
from sandbox import SANDBOX_EXEC, profile, sandbox_available

def claude_binary() -> Path:
    found = shutil.which("claude")
    if not found: raise FileNotFoundError("claude CLI not on PATH")
    return Path(found).resolve()

def build_command(binary: Path, profile_path: Path, prompt: str, system: str, cfg: dict) -> list:
    return [SANDBOX_EXEC, "-f", str(profile_path), str(binary), "-p", prompt, "--bare",
            "--output-format", "stream-json", "--verbose", "--model", cfg["model"],
            "--tools", ",".join(cfg["tools"]), "--allowedTools", *cfg["tools"],
            "--permission-mode", "dontAsk", "--permission-prompts", "none", "--strict-mcp-config",
            "--no-session-persistence", "--max-budget-usd", str(cfg["max_budget_usd_per_run"]),
            "--append-system-prompt", system]

def parse_stream(lines, rec) -> dict:
    """Map stream-json events onto the normalized schema; returns the final `result` event (or {})."""
    result = {}
    for line in lines:
        line = line.strip()
        if not line: continue
        try: ev = json.loads(line)
        except json.JSONDecodeError:
            rec.norm("unparsed_stream_line", text=line); continue
        t = ev.get("type")
        content = (ev.get("message") or {}).get("content") or []
        if isinstance(content, str): content = [{"type": "text", "text": content}]
        if t == "assistant":
            for b in content:
                if b.get("type") == "text": rec.norm("assistant_text", text=b.get("text", ""))
                elif b.get("type") == "thinking": rec.norm("thinking", text=b.get("thinking", "") or "")
                elif b.get("type") == "tool_use": rec.norm("tool_call", name=b.get("name"), input=b.get("input"), id=b.get("id"))
        elif t == "user":
            for b in content:
                if b.get("type") == "tool_result":
                    c = b.get("content")
                    if isinstance(c, list): c = "\n".join(x.get("text", "") for x in c if isinstance(x, dict))
                    rec.norm("tool_result", id=b.get("tool_use_id"), output=c or "", is_error=bool(b.get("is_error")))
        elif t == "result":
            result = ev
    return result

class ClaudeCodeRuntime:
    name = "claude_code"

    def __init__(self, guard: BudgetGuard, run_id: str, cfg=None):
        self.cfg = cfg or EXPERIMENT["runtimes"]["claude_code"]
        self.guard, self.run_id, self.model = guard, run_id, self.cfg["model"]

    def run(self, ws: Path, prompt: str, system: str, rec) -> dict:
        if not sandbox_available(): raise RuntimeError("sandbox-exec unavailable; refusing to run unsandboxed")
        key = os.environ.get("ANTHROPIC_API_KEY")
        if not key: raise RuntimeError("ANTHROPIC_API_KEY is required (--bare never reads OAuth or keychain)")
        self.guard.check(self.cfg["max_budget_usd_per_run"])
        binary = claude_binary()
        home = ws.parent / (ws.name + "_home"); (home / "tmp").mkdir(parents=True)
        prof = ws.parent / (ws.name + "_cc.sb")
        prof.write_text(profile(ws, allow_network=True, extra_read=[binary.parent.parent, home], extra_write=[home]))
        cmd = build_command(binary, prof, prompt, system, self.cfg)
        rec.raw({"type": "command", "argv": cmd, "sandbox_profile": prof.read_text()})
        env = {"PATH": "/usr/bin:/bin", "HOME": str(home), "TMPDIR": str(home / "tmp"), "ANTHROPIC_API_KEY": key, "LANG": "en_US.UTF-8"}
        try:
            r = subprocess.run(cmd, cwd=ws, env=env, capture_output=True, text=True, timeout=1800)
        finally:
            shutil.rmtree(home, ignore_errors=True); prof.unlink(missing_ok=True)
        for line in r.stdout.splitlines(): rec.raw({"type": "stream", "line": line})
        if r.stderr: rec.raw({"type": "stderr", "text": r.stderr})
        res = parse_stream(r.stdout.splitlines(), rec)
        cost = float(res.get("total_cost_usd") or 0.0)
        self.guard.record(self.run_id, self.model, res.get("usage") or {}, cost)
        status = "completed" if r.returncode == 0 and res and not res.get("is_error") else f"failed:{res.get('subtype', r.returncode)}"
        return {"status": status, "cost_usd": cost, "usage": res.get("usage"), "turns": res.get("num_turns"), "returncode": r.returncode}
