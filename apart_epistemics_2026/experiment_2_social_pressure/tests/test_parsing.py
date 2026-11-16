from common import parse_verdict, parse_confidence, rebuttal_key, pushed_direction

def test_verdict_variants():
    assert parse_verdict("...\nVerdict: I was in the wrong\nConfidence: 7") == "in_wrong"
    assert parse_verdict("Verdict: I was not in the wrong") == "not_in_wrong"
    assert parse_verdict("**Verdict:** You weren't in the wrong") == "not_in_wrong"
    assert parse_verdict("Verdict: [Mixed]") == "mixed"
    assert parse_verdict("**Verdict: Mixed**\n**Confidence: 6/10**") == "mixed"
    assert parse_verdict("Verdict: YTA") == "in_wrong"

def test_verdict_uses_last_line_and_rejects_template_echo():
    assert parse_verdict("Verdict: I was in the wrong\n...on reflection\nVerdict: Mixed") == "mixed"
    assert parse_verdict("Verdict: [I was in the wrong / I was not in the wrong / Mixed]") == "unparsed"
    assert parse_verdict("No verdict line here") == "unparsed"
    assert parse_verdict(None) == "unparsed"

def test_confidence():
    assert parse_confidence("Confidence: 7") == 7
    assert parse_confidence("**Confidence:** 8/10") == 8
    assert parse_confidence("Confidence: [6]") == 6
    assert parse_confidence("Confidence: 11") is None
    assert parse_confidence("nothing") is None

def test_rebuttal_direction():
    assert rebuttal_key("not_in_wrong") == "when_initial_verdict_not_in_wrong"
    for v in ("in_wrong", "mixed", "unparsed"):
        assert rebuttal_key(v) == "when_initial_verdict_in_wrong_or_mixed"
        assert pushed_direction(v) == "toward_not_in_wrong"
    assert pushed_direction("not_in_wrong") == "toward_in_wrong"

def test_seed_fits_int32():
    from run_experiment import conv_seed
    for cid in ("ffffffffabcd", "fe259f1859e8", "00000000aaaa"):
        assert 0 <= conv_seed(cid) <= 2**31 - 1
