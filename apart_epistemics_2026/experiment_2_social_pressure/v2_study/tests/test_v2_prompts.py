"""Prompt isolation: no condition leakage, identical framing across models, fixed rebuttal (Experiment 2 v2)."""
import json
from v2_common import PROMPTS, STUDY, EXP, system_prompt, user_turn1, redacted_turn1, rebuttal
import run_v2

PILOT = json.loads((EXP / "configs/prompts.json").read_text())

def test_system_texts_identical_to_pilot():
    for k in ("system_base", "framing", "intervention", "system_template"):
        assert PROMPTS[k] == PILOT[k], k
    assert PROMPTS["conditions"] == PILOT["conditions"]

def test_each_condition_contains_only_its_own_manipulation():
    F, I = PROMPTS["framing"], PROMPTS["intervention"]
    for cond, spec in PROMPTS["conditions"].items():
        s = system_prompt(cond)
        assert F[spec["framing"]] in s and I[spec["intervention"]] in s
        for other in F:
            if other != spec["framing"]: assert F[other] not in s
        for other in I:
            if other != spec["intervention"]: assert I[other] not in s
    assert "evaluation" not in system_prompt("A").lower() and "evaluation" not in system_prompt("B").lower()

def test_user_messages_carry_no_condition_or_model_info():
    msgs = [user_turn1("POST"), rebuttal(2), rebuttal(3)]
    for m in msgs:
        low = m.lower()
        for bad in ("evaluation", "researcher", "recorded", "gpt", "gemini", "condition", "base your assessment"):
            assert bad not in low, bad
    assert "Blame:" in user_turn1("POST") and "Verdict:" in user_turn1("POST") and "Confidence:" in user_turn1("POST")

def test_identical_messages_across_models_and_fixed_rebuttal():
    captured = {}
    class G:
        def reserve(self, wc): pass
        def settle(self, *a): pass
    def fake(body):
        captured.setdefault(body["model"], []).append([m["content"] for m in body["messages"]])
        return {"choices": [{"message": {"content": "x\nVerdict: Mixed\nBlame: 5\nConfidence: 6"}, "finish_reason": "stop"}], "usage": {"cost": 0.0}}, None, 0.0
    import tempfile, pathlib
    with tempfile.TemporaryDirectory() as d:
        p = run_v2.Paths(pathlib.Path(d))
        for m in STUDY["targets"]:
            run_v2.run_conversation({"stage": "t", "row_id": 1, "category": "x", "condition": "C", "model": m, "rep": 0, "conv_id": "abcdef123456"}, "POST", G(), 1, p, fake)
        a, b = list(captured.values())
        assert a == b                                   # same system prompt, user turns and (here) replies across models
        assert a[1][3] == rebuttal(2) and a[2][5] == rebuttal(3)
        assert "POST" not in (p.turns).read_text()      # public log is redacted
        assert "POST" in (p.private).read_text()

def test_redacted_turn1_has_hash_not_text():
    r = redacted_turn1(7, "SECRET POST")
    assert "SECRET POST" not in r and "row_id=7" in r
