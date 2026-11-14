"""Randomization/seeding, cost tracking + hard cap, resumability (Experiment 2 v2). Fake HTTP only."""
import json, pytest
from collections import Counter
from v2_common import STUDY, conv_seed
import run_v2 as R
from common import BudgetGuard

def test_jobs_balanced_unique_deterministic():
    j1, j2 = R.build_jobs(), R.build_jobs()
    assert len(j1) == 480 and len({j["conv_id"] for j in j1}) == 480
    assert [j["conv_id"] for j in j1] == [j["conv_id"] for j in j2]
    assert set(Counter((j["model"], j["condition"]) for j in j1).values()) == {60}
    assert set(Counter(j["row_id"] for j in j1).values()) == {16}
    first = [j["condition"] for j in j1[:16]]
    assert len(set(first)) > 1                          # order is shuffled, not blocked by condition

def test_seeds_are_int32():
    for j in R.build_jobs(): assert 0 <= conv_seed(j["conv_id"]) <= 2**31 - 1
    assert conv_seed("ffffffff0000") == 2**31 - 1

def test_preflight_refuses():
    todo = R.build_jobs()
    pc = {m: 0.04 for m in STUDY["targets"]}
    ok, msg = R.preflight(todo, 0.0, None, 100.0, pc, 0.25); assert not ok and "cap" in msg
    ok, msg = R.preflight(todo, 0.0, 30.0, 3.64, pc, 0.25); assert not ok and "projected" in msg
    ok, msg = R.preflight(todo, 0.0, 20.0, 100.0, pc, 0.25); assert not ok          # 480*0.04*1.25 = 24 > cap 20
    ok, msg = R.preflight(todo, 0.0, 30.0, 100.0, pc, 0.25); assert ok
    ok, msg = R.preflight(todo, 0.0, 30.0, None, pc, 0.25); assert not ok

def reply(v="Mixed", cost=0.01):
    return {"id": "g", "model": "m", "choices": [{"message": {"content": f"ok\nVerdict: {v}\nBlame: 5\nConfidence: 6"}, "finish_reason": "stop"}], "usage": {"cost": cost}}, None, 0.1

def test_ledger_tracks_cost_and_budget_pauses(tmp_path):
    p = R.Paths(tmp_path); g = BudgetGuard(1.0, p.ledger)
    job = R.build_jobs()[0]
    c = R.run_conversation(job, "POST", g, 1, p, lambda b: reply(cost=0.02))
    assert c["status"] == "complete" and c["cost_usd"] == pytest.approx(0.06)
    led = [json.loads(l) for l in p.ledger.read_text().splitlines()]
    assert len(led) == 3 and led[-1]["cumulative_usd"] == pytest.approx(0.06)
    g2 = BudgetGuard(0.0001, tmp_path / "l2.jsonl")
    c2 = R.run_conversation(R.build_jobs()[1], "POST", g2, 1, R.Paths(tmp_path / "x"), lambda b: reply())
    assert c2["status"] == "paused_budget" and c2["turns"] == []

def test_resumability(tmp_path):
    p = R.Paths(tmp_path); g = BudgetGuard(10, p.ledger); jobs = R.build_jobs()[:3]
    R.run_conversation(jobs[0], "P", g, 1, p, lambda b: reply())
    R.run_conversation(jobs[1], "P", g, 1, p, lambda b: (None, {"status": 500}, 0.1))
    todo, done, att = R.plan(jobs, p)
    assert [j["conv_id"] for j in todo] == [jobs[2]["conv_id"]] and done == {jobs[0]["conv_id"]}
    todo, _, att = R.plan(jobs, p, retry_failed=True)
    assert {j["conv_id"] for j in todo} == {jobs[1]["conv_id"], jobs[2]["conv_id"]} and att[jobs[1]["conv_id"]] == 1
    c = R.run_conversation(jobs[1], "P", g, att[jobs[1]["conv_id"]] + 1, p, lambda b: reply())
    assert c["attempt"] == 2 and len([l for l in p.convs.read_text().splitlines()]) == 3   # failed attempt kept

def test_estimate_uses_actual_pilot_spend():
    import estimate_v2 as E
    e = E.estimate()
    assert e["design"]["conversations"] == 480
    pc = E.pilot_per_conversation()["mean_complete"]
    assert e["targets_openrouter"]["total_base_usd"] == pytest.approx(240 * sum(pc.values()), abs=1e-3)
