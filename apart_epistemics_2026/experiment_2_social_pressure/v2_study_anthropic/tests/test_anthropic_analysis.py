"""Separate analysis reuses the frozen v2 code; exploratory model differences (Apart sprint Nov 13-15 2026)."""
import pytest
import analyze_anthropic as AA

def rows():
    out = []
    for m, base in (("claude-haiku-4-5-20251001", 1.0), ("claude-opus-4-7", 0.0)):
        for case in range(5):
            for cond, add in zip("ABCD", (0, -0.5, 0, -0.5)):
                for rep in range(2):
                    out.append({"model": m, "row_id": case, "condition": cond, "rep": rep, **{oc: None for oc in AA.A.OUTCOMES},
                                "verdict_move_t3": base + add})
    return out

def test_model_differences():
    res = {(r["outcome"], r["comparison"], r["quantity"]): r for r in AA.model_differences(rows(), b=200)}
    k = ("verdict_move_t3", "claude-haiku-4-5-20251001 - claude-opus-4-7")
    assert res[k + ("overall_mean",)]["estimate"] == pytest.approx(1.0) and res[k + ("overall_mean",)]["n_cases"] == 5
    assert res[k + ("honesty",)]["estimate"] == pytest.approx(0.0)
    eff = {(r["outcome"], r["scope"], r["contrast"]): r for r in AA.A.analyse(rows(), b=200)}
    assert eff[("verdict_move_t3", "pooled", "honesty")]["estimate"] == pytest.approx(-0.5)
