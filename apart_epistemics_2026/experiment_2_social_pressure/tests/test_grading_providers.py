"""Mocked tests for src/grading_providers.py. No network, no API keys, no cost."""
import json, pytest
import grading_providers as gp
from common import BudgetExceeded

ANTH_OK = {"id": "msg_test", "type": "message", "model": "claude-sonnet-4-6", "role": "assistant",
           "content": [{"type": "text", "text": "{\"ok\": true}"}], "usage": {"input_tokens": 3000, "output_tokens": 600}}
OR_OK = {"id": "gen-test", "model": "anthropic/claude-sonnet-4.6", "choices": [{"message": {"content": "{\"ok\": true}"}}],
         "usage": {"prompt_tokens": 3000, "completion_tokens": 600, "cost": 0.018}}

class FakePoster:
    def __init__(self, responses): self.responses, self.calls = list(responses), []
    def __call__(self, url, headers, body, timeout):
        self.calls.append({"url": url, "headers": headers, "body": body}); return self.responses.pop(0)

@pytest.fixture(autouse=True)
def fake_keys(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-anthropic-key"); monkeypatch.setenv("OPENROUTER_API_KEY", "test-or-key")

def test_default_is_openrouter(tmp_path):
    assert gp.get_provider(None, FakePoster([]), ledger_root=tmp_path).name == "openrouter"

def test_unknown_provider():
    with pytest.raises(ValueError): gp.get_provider("other")

def test_same_model_and_settings_across_providers(tmp_path):
    a = gp.get_provider("anthropic", FakePoster([]), ledger_root=tmp_path); o = gp.get_provider("openrouter", FakePoster([]), ledger_root=tmp_path)
    _, ha, ba = a.build("P"); _, ho, bo = o.build("P")
    assert ba["temperature"] == bo["temperature"] == 0 and ba["max_tokens"] == bo["max_tokens"]
    assert ba["messages"] == bo["messages"]
    assert ba["model"] == "claude-sonnet-4-6" and bo["model"] == "anthropic/claude-sonnet-4.6"
    assert ha["x-api-key"] == "test-anthropic-key" and "anthropic-version" in ha and "Authorization" not in ha
    assert "thinking" not in ba and "reasoning" not in bo

def test_anthropic_parse_and_computed_cost(tmp_path):
    fp = FakePoster([(200, ANTH_OK)])
    p = gp.get_provider("anthropic", fp, ledger_root=tmp_path)
    g = gp.guard_for(p, 1.0)
    r = p.grade("PROMPT", g, record={"conv_id": "x"})
    assert r.text == '{"ok": true}' and r.response_model == "claude-sonnet-4-6" and r.error is None
    assert abs(r.cost_usd - (3000 * 3e-6 + 600 * 15e-6)) < 1e-12 and r.cost_source == "computed_from_config_prices"
    rec = json.loads((tmp_path / "results_v2/ledgers/grader_anthropic.jsonl").read_text().splitlines()[0])
    assert rec["provider"] == "anthropic" and rec["conv_id"] == "x" and abs(rec["cost_usd"] - r.cost_usd) < 1e-12

def test_openrouter_parse_uses_returned_cost(tmp_path, monkeypatch):
    monkeypatch.setattr(gp.OpenRouterProvider, "prices", lambda self: (3e-6, 15e-6))
    p = gp.get_provider("openrouter", FakePoster([(200, OR_OK)]), ledger_root=tmp_path)
    r = p.grade("PROMPT", gp.guard_for(p, 1.0))
    assert r.cost_usd == 0.018 and r.cost_source == "openrouter_usage_cost"
    assert (tmp_path / "results_v2/ledgers/grader_openrouter.jsonl").exists()
    assert not (tmp_path / "results_v2/ledgers/grader_anthropic.jsonl").exists()   # separate ledgers

def test_ledgers_are_separate_totals(tmp_path, monkeypatch):
    monkeypatch.setattr(gp.OpenRouterProvider, "prices", lambda self: (3e-6, 15e-6))
    a = gp.get_provider("anthropic", FakePoster([(200, ANTH_OK)]), ledger_root=tmp_path)
    o = gp.get_provider("openrouter", FakePoster([(200, OR_OK)]), ledger_root=tmp_path)
    a.grade("P", gp.guard_for(a, 1.0)); o.grade("P", gp.guard_for(o, 1.0))
    assert abs(gp.guard_for(a, 1.0).spent - 0.018) < 1e-9 and abs(gp.guard_for(o, 1.0).spent - 0.018) < 1e-9

def test_error_logged_not_replaced(tmp_path):
    err = {"type": "error", "error": {"type": "invalid_request_error", "message": "bad model"}}
    p = gp.get_provider("anthropic", FakePoster([(400, err)]), ledger_root=tmp_path)
    r = p.grade("P", gp.guard_for(p, 1.0))
    assert r.text is None and r.error["status"] == 400 and r.cost_usd is None

def test_retry_on_overloaded_then_success(tmp_path):
    fp = FakePoster([(529, {"type": "error", "error": {"type": "overloaded_error"}}), (200, ANTH_OK)])
    p = gp.get_provider("anthropic", fp, ledger_root=tmp_path)
    assert p.grade("P").text == '{"ok": true}' and len(fp.calls) == 2

def test_budget_guard_blocks_before_call(tmp_path):
    fp = FakePoster([(200, ANTH_OK)])
    p = gp.get_provider("anthropic", fp, ledger_root=tmp_path)
    with pytest.raises(BudgetExceeded):
        p.grade("P" * 3000, gp.guard_for(p, 0.001))
    assert fp.calls == []        # no request sent

def test_missing_key_raises(tmp_path, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY")
    with pytest.raises(RuntimeError): gp.get_provider("anthropic", FakePoster([]), ledger_root=tmp_path).build("P")

def test_free_model_check_mocked(monkeypatch):
    got = gp.free_model_check("anthropic", getter=lambda url, headers: {"data": [{"id": "claude-sonnet-4-6"}]})
    assert got == {"model": "claude-sonnet-4-6", "listed": True}
