"""Anthropic parsing, per-model cost tracking + hard cap, resumability, design (Apart sprint Nov 13-15 2026). Fake HTTP only."""
import json, pytest
from collections import Counter
import run_anthropic as RA
import run_v2

def ok(text="ok\nVerdict: I was not in the wrong\nBlame: 2\nConfidence: 7", tin=1000, tout=300, blocks=None):
    def f(body):
        return 200, {"id": "msg_1", "type": "message", "model": body["model"], "stop_reason": "end_turn",
                     "content": blocks or [{"type": "text", "text": text}], "usage": {"input_tokens": tin, "output_tokens": tout}}, 0.1, 0
    return f

def test_jobs_720_balanced_unique_and_distinct_from_v2():
    j = RA.build_jobs()
    assert len(j) == 720 and len({x["conv_id"] for x in j}) == 720
    assert set(Counter((x["model"], x["condition"]) for x in j).values()) == {60}
    assert set(Counter(x["row_id"] for x in j).values()) == {24}
    assert not ({x["conv_id"] for x in j} & {x["conv_id"] for x in run_v2.build_jobs()})
    assert [x["conv_id"] for x in j] == [x["conv_id"] for x in RA.build_jobs()]
    s = RA.smoke_jobs(); assert len(s) == 6 and Counter(x["model"] for x in s) == {m: 2 for m in RA.STUDY["targets"]}

def test_parse_response_variants():
    t, info, e = RA.parse_response(200, {"type": "message", "model": "m", "stop_reason": "end_turn", "usage": {"input_tokens": 1},
                                         "content": [{"type": "thinking", "thinking": "hidden"}, {"type": "text", "text": "A"}, {"type": "text", "text": "B"}]})
    assert t == "AB" and e is None and info["block_types"] == ["thinking", "text", "text"]
    t, _, e = RA.parse_response(400, {"type": "error", "error": {"type": "invalid_request_error", "message": "bad"}})
    assert t is None and e["status"] == 400
    t, _, e = RA.parse_response(200, {"type": "error", "error": {"type": "overloaded_error"}}); assert e is not None
    t, info, e = RA.parse_response(200, {"type": "message", "content": [], "stop_reason": "max_tokens", "usage": {}})
    assert t is None and e is None and info["stop_reason"] == "max_tokens"

def test_cost_from_usage_per_model():
    u = {"input_tokens": 1_000_000, "output_tokens": 1_000_000}
    assert RA.cost_from_usage("claude-sonnet-4-6", u) == pytest.approx(18.0)
    assert RA.cost_from_usage("claude-haiku-4-5-20251001", u) == pytest.approx(6.0)
    assert RA.cost_from_usage("claude-opus-4-7", u) == pytest.approx(30.0)
    assert RA.cost_from_usage("claude-opus-4-7", {"input_tokens": 0, "output_tokens": 0, "cache_read_input_tokens": 1_000_000}) == pytest.approx(0.5)

def test_ledger_per_model_tokens_and_dollars(tmp_path):
    p = RA.Paths(tmp_path); g = RA.BudgetGuard(10, p.ledger)
    jobs = {m: next(j for j in RA.build_jobs() if j["model"] == m) for m in RA.STUDY["targets"]}
    for m, j in jobs.items(): RA.run_conversation(j, "P", g, 1, p, ok())
    led = [json.loads(l) for l in p.ledger.read_text().splitlines()]
    assert len(led) == 9 and all(x["input_tokens"] == 1000 and x["output_tokens"] == 300 for x in led)
    per = {m: sum(x["cost_usd"] for x in led if x["model"] == m) for m in jobs}
    assert per["claude-sonnet-4-6"] == pytest.approx(3 * (1000 * 3e-6 + 300 * 15e-6))
    assert per["claude-haiku-4-5-20251001"] == pytest.approx(3 * (1000 * 1e-6 + 300 * 5e-6))
    assert per["claude-opus-4-7"] == pytest.approx(3 * (1000 * 5e-6 + 300 * 25e-6))
    assert led[-1]["cumulative_usd"] == pytest.approx(sum(per.values()), abs=1e-6)
    convs = [json.loads(l) for l in p.convs.read_text().splitlines()]
    assert all(c["status"] == "complete" and [t["parsed_verdict"] for t in c["turns"]] == ["not_in_wrong"] * 3 for c in convs)

def test_hard_cap_pauses_and_failed_calls_cost_zero(tmp_path):
    c = RA.run_conversation(RA.build_jobs()[0], "P", RA.BudgetGuard(0.0001, tmp_path / "l.jsonl"), 1, RA.Paths(tmp_path / "a"), ok())
    assert c["status"] == "paused_budget" and c["turns"] == []
    p = RA.Paths(tmp_path / "b"); g = RA.BudgetGuard(10, p.ledger)
    c = RA.run_conversation(RA.build_jobs()[1], "P", g, 1, p, lambda b: (529, {"type": "error", "error": {"type": "overloaded_error"}}, 0.1, 4))
    assert c["status"] == "failed" and c["cost_usd"] == 0 and g.spent == 0

def test_preflight():
    todo = RA.build_jobs(); pc = {m: 0.03 for m in RA.STUDY["targets"]}
    assert not RA.preflight(todo, 0, None, pc, 0.25)[0]
    assert not RA.preflight(todo, 0, 50, {**pc, "claude-opus-4-7": None}, 0.25)[0]
    assert not RA.preflight(todo, 0, 25, pc, 0.25)[0]            # 720 * 0.03 * 1.25 = 27 > 25
    assert not RA.preflight(todo, 24, 50, pc, 0.25)[0]           # 27 > 50 - 24
    assert RA.preflight(todo, 0, 50, pc, 0.25)[0]

def test_resumability(tmp_path):
    p = RA.Paths(tmp_path); g = RA.BudgetGuard(10, p.ledger); jobs = RA.build_jobs()[:3]
    RA.run_conversation(jobs[0], "P", g, 1, p, ok())
    RA.run_conversation(jobs[1], "P", g, 1, p, lambda b: (500, {"type": "error", "error": {}}, 0.1, 4))
    todo, done, att = RA.plan(jobs, p)
    assert [j["conv_id"] for j in todo] == [jobs[2]["conv_id"]] and done == {jobs[0]["conv_id"]}
    todo, _, att = RA.plan(jobs, p, retry_failed=True)
    assert {j["conv_id"] for j in todo} == {jobs[1]["conv_id"], jobs[2]["conv_id"]}
    c = RA.run_conversation(jobs[1], "P", g, att[jobs[1]["conv_id"]] + 1, p, ok())
    assert c["attempt"] == 2 and len(p.convs.read_text().splitlines()) == 3

def test_estimate_from_smoke_usage(tmp_path):
    import estimate_anthropic as E
    p = RA.Paths(tmp_path); g = RA.BudgetGuard(10, p.ledger)
    for j in RA.smoke_jobs(): RA.run_conversation(j, "P", g, 1, p, ok())
    e = E.estimate(50, p)
    per = 3 * (1000 * 5e-6 + 300 * 25e-6)
    assert e["models"]["claude-opus-4-7"]["mean_cost_per_conv"] == pytest.approx(per, abs=1e-6)
    assert e["models"]["claude-opus-4-7"]["with_margin_usd"] == pytest.approx(240 * per * 1.25, abs=1e-3)
    assert e["design"]["conversations_total"] == 720 and e["cap_check"]["fits_with_margin"]
    assert RA.smoke_per_conversation(p)["claude-opus-4-7"] == pytest.approx(per, abs=1e-6)

def test_deadline_abandons_hung_request():
    import time
    st, j = RA._with_deadline(lambda: (time.sleep(5), (200, {}))[1], 0.2)
    assert st == -2 and j["error"]["type"] == "deadline"
    assert RA._with_deadline(lambda: (200, {"ok": 1}), 2) == (200, {"ok": 1})

def test_post_retries_deadline_then_succeeds(monkeypatch):
    import time as _t
    real_sleep, calls = _t.sleep, []
    def fake_once(body, h, timeout):
        calls.append(1)
        if len(calls) == 1: real_sleep(1)                      # first request hangs past the deadline
        return 200, {"type": "message", "content": [{"type": "text", "text": "x"}], "usage": {}}
    monkeypatch.setattr(RA, "_post_once", fake_once)
    monkeypatch.setattr(RA.time, "sleep", lambda s: None)     # skip retry backoff
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-not-a-key")
    st, j, lat, tries = RA._post({"model": "m"}, deadline_s=0.3)
    assert st == 200 and tries == 1 and RA._TL.abandoned == 1

def test_recover_interrupted(tmp_path):
    p = RA.Paths(tmp_path); g = RA.BudgetGuard(10, p.ledger); jobs = RA.build_jobs()[:2]
    RA.run_conversation(jobs[0], "P", g, 1, p, ok())
    rec = {"conv_id": jobs[1]["conv_id"], "attempt": 1, "turn": 1, "parsed_verdict": "mixed", "parsed_blame": 3, "parsed_confidence": 7,
           "cost_usd": 0.01, "input_tokens": 1, "output_tokens": 1, "finish_reason": "end_turn", "response_model": "m"}
    RA.append(p.turns, rec)
    assert RA.recover_interrupted(p) == [jobs[1]["conv_id"]] and RA.recover_interrupted(p) == []     # idempotent
    c = [json.loads(l) for l in p.convs.read_text().splitlines()][-1]
    assert c["status"] == "interrupted" and c["attempt"] == 1 and c["cost_usd"] == 0.01
    todo, done, att = RA.plan(jobs, p); assert todo == []
    todo, done, att = RA.plan(jobs, p, retry_failed=True); assert [j["conv_id"] for j in todo] == [jobs[1]["conv_id"]] and att[jobs[1]["conv_id"]] == 1
    import analyze_v2 as A
    assert {r["conv_id"] for r in A.load_conversations(tmp_path)} == {jobs[0]["conv_id"]}
