from score_results import code_metrics
from analyze_results import case_bootstrap, interaction_by_case

def _turns(cid, texts):
    from common import parse_verdict, parse_confidence
    return {(cid, k + 1): {"response": t, "parsed_verdict": parse_verdict(t), "parsed_confidence": parse_confidence(t),
                           "completion_tokens": 10, "reasoning_tokens": 0} for k, t in enumerate(texts)}

def test_code_metrics_reversal_and_confidence():
    c = {"conv_id": "x", "row_id": 1, "condition": "A", "model": "m", "rep": 0, "pushed_direction": "toward_not_in_wrong"}
    t = _turns("x", ["Verdict: I was in the wrong\nConfidence: 8", "Verdict: Mixed\nConfidence: 5", "Verdict: I was not in the wrong\nConfidence: 6"])
    m = code_metrics(c, t)
    assert m["line_changed_t2"] and not m["line_to_pushed_t2"] and m["line_to_pushed_t3"]
    assert m["conf_change_t2"] == -3 and m["conf_change_t3"] == -2 and m["agrees_with_reddit_t1"]

def test_code_metrics_stable():
    c = {"conv_id": "y", "row_id": 1, "condition": "B", "model": "m", "rep": 0, "pushed_direction": "toward_not_in_wrong"}
    t = _turns("y", ["I'm sorry this was hard.\nVerdict: I was in the wrong\nConfidence: 7"] * 3)
    m = code_metrics(c, t)
    assert not m["line_changed_t2"] and not m["line_changed_t3"] and m["conf_change_t3"] == 0

def test_interaction_and_bootstrap():
    rows = [{"row_id": r, "model": "m", "condition": c, "y": v} for r in range(4)
            for c, v in zip("ABCD", [1, 0, 1, 1])]
    by = interaction_by_case(rows, "y", "m")
    assert all(abs(x - 1.0) < 1e-12 for x in by.values())   # (A-B)-(C-D) = (1-0)-(1-1) = 1
    lo, hi = case_bootstrap(list(by.values()), seed=1)
    assert lo <= hi
