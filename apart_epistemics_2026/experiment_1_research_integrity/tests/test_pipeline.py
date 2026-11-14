import json, os
import pytest
from common import PROMPTS, BudgetExceeded, BudgetGuard, read_jsonl, task_prompt
from harness import run_session
from runtime_api import AnthropicAPIRuntime
from runtime_claude_code import build_command, parse_stream
from sandbox import sandbox_available
from score import score_run
from scripted_client import ScriptedClient
import run_pilot

def test_prompts_differ_only_by_pressure_paragraph():
    a, b = task_prompt("normal"), task_prompt("deadline")
    assert b.replace(PROMPTS["pressure"]["deadline"], "") == a
    for word in ("verify", "check", "corrupt", "inconsisten", "quality"):
        assert word not in a.lower()

def test_paid_runs_refused_without_flags():
    with pytest.raises(SystemExit): run_pilot.main(["--runtime", "anthropic_api"])
    with pytest.raises(SystemExit): run_pilot.main(["--runtime", "anthropic_api", "--allow-paid"])

def test_budget_guard_persists_and_blocks(tmp_path):
    g = BudgetGuard(1.0, tmp_path / "l.jsonl"); g.record("r", "m", {}, 0.9)
    g2 = BudgetGuard(1.0, tmp_path / "l.jsonl")
    assert g2.spent == pytest.approx(0.9)
    with pytest.raises(BudgetExceeded): g2.check(0.2)

def test_plan_is_balanced_and_deterministic():
    jobs = run_pilot.plan(["a", "b"], 5, [1, 2, 3, 4, 5])
    assert jobs == run_pilot.plan(["a", "b"], 5, [1, 2, 3, 4, 5])
    assert sorted(s for c, s, _ in jobs if c == "a") == [1, 2, 3, 4, 5]

@pytest.mark.skipif(not sandbox_available(), reason="macOS sandbox-exec required")
@pytest.mark.parametrize("policy,cls,recognized", [("naive", "corrupted_sheet_value", False), ("careful", "corrected", True)])
def test_scripted_end_to_end(tmp_path, policy, cls, recognized):
    run_id = f"pytest_{policy}_{os.getpid()}"
    rt = AnthropicAPIRuntime(ScriptedClient(policy), BudgetGuard(100, tmp_path / "l.jsonl"), run_id)
    meta = run_session(run_id, "compromised_normal", 101, rt, tmp_path)
    assert meta["status"] == "completed" and meta["report_present"]
    d = tmp_path / run_id
    assert (d / "events.jsonl").exists() and read_jsonl(d / "normalized.jsonl")
    assert "report.md" in json.load(open(d / "workspace_diff.json"))["added"]
    s = score_run(d)
    assert s["headline_class"] == cls and s["recognized_specific"] == recognized
    assert s["published_corrupted_headline"] == (policy == "naive")

def test_claude_code_command_is_bare_and_sandboxed(tmp_path):
    cfg = {"model": "m", "tools": ["Read", "Bash"], "max_budget_usd_per_run": 1.0}
    cmd = build_command(tmp_path / "claude", tmp_path / "p.sb", "task", "sys", cfg)
    assert cmd[0] == "/usr/bin/sandbox-exec" and "--bare" in cmd and "--no-session-persistence" in cmd
    assert cmd[cmd.index("--permission-mode") + 1] == "dontAsk"

class _Rec:
    def __init__(self): self.events = []
    def norm(self, kind, **kw): self.events.append((kind, kw))

def test_claude_stream_parser():
    lines = [json.dumps({"type": "system", "subtype": "init"}),
             json.dumps({"type": "assistant", "message": {"content": [{"type": "text", "text": "hi"},
                        {"type": "tool_use", "id": "t1", "name": "Read", "input": {"file_path": "data/scores.csv"}}]}}),
             json.dumps({"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "t1", "content": [{"type": "text", "text": "rows"}]}]}}),
             "not json", json.dumps({"type": "result", "total_cost_usd": 0.5, "num_turns": 2})]
    r = _Rec(); res = parse_stream(lines, r)
    assert [k for k, _ in r.events] == ["assistant_text", "tool_call", "tool_result", "unparsed_stream_line"]
    assert res["total_cost_usd"] == 0.5 and r.events[2][1]["output"] == "rows"
