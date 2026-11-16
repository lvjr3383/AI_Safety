import json, pytest
from common import BudgetGuard, BudgetExceeded, worst_case_cost

def test_reserve_blocks_over_cap(tmp_path):
    g = BudgetGuard(1.0, tmp_path / "l.jsonl")
    g.reserve(0.6)
    with pytest.raises(BudgetExceeded):
        g.reserve(0.5)          # 0.6 reserved + 0.5 > 1.0

def test_settle_uses_actual_and_persists(tmp_path):
    p = tmp_path / "l.jsonl"
    g = BudgetGuard(1.0, p); g.reserve(0.6); g.settle(0.6, 0.1, {"kind": "t"})
    assert abs(g.spent - 0.1) < 1e-12 and abs(g.reserved) < 1e-12
    g2 = BudgetGuard(1.0, p)    # ledger reload spans processes (smoke + pilot + grading)
    assert abs(g2.spent - 0.1) < 1e-12
    g2.reserve(0.85)
    with pytest.raises(BudgetExceeded):
        g2.reserve(0.1)
    assert json.loads(p.read_text().splitlines()[0])["cost_usd"] == 0.1

def test_failed_call_with_no_cost(tmp_path):
    g = BudgetGuard(1.0, tmp_path / "l.jsonl"); g.reserve(0.5); g.settle(0.5, None, {"kind": "t"})
    assert g.spent == 0.0

def test_worst_case_monotone():
    assert worst_case_cost(1000, 2000, 5e-6, 3e-5) > worst_case_cost(1000, 1000, 5e-6, 3e-5)
