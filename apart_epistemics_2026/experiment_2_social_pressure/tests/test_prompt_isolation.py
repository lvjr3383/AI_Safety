import json
from common import PROMPTS, system_prompt, redacted_turn1, user_turn1, sha256_text
from score_results import grader_prompt, parse_grader_json, GRADER_KEYS

def test_conditions_differ_only_in_their_factor():
    a, b, c, d = (system_prompt(x) for x in "ABCD")
    f, i = PROMPTS["framing"], PROMPTS["intervention"]
    assert f["ordinary"] in a and i["none"] in a
    assert f["ordinary"] in b and i["honesty"] in b
    assert f["evaluation"] in c and i["none"] in c
    assert f["evaluation"] in d and i["honesty"] in d
    assert a.replace(i["none"], i["honesty"]) == b and c.replace(i["none"], i["honesty"]) == d
    assert a.replace(f["ordinary"], f["evaluation"]) == c

def test_blocks_length_matched():
    f, i = PROMPTS["framing"], PROMPTS["intervention"]
    assert abs(len(f["ordinary"].split()) - len(f["evaluation"].split())) <= 2
    assert abs(len(i["none"].split()) - len(i["honesty"].split())) <= 2

def test_evaluation_framing_reveals_no_scoring():
    t = PROMPTS["framing"]["evaluation"].lower()
    for w in ("sycophan", "honest", "agree", "pushback", "push back", "score", "correct answer"):
        assert w not in t

def test_grader_is_blind_to_condition_and_model():
    g = grader_prompt("POST TEXT", "top", "YTA", ["r1", "r2", "r3"],
                      [PROMPTS["rebuttal_1"]["when_initial_verdict_in_wrong_or_mixed"], PROMPTS["rebuttal_2"]["when_initial_verdict_in_wrong_or_mixed"]])
    for block in list(PROMPTS["framing"].values()) + list(PROMPTS["intervention"].values()):
        assert block not in g
    for leak in ("gpt", "gemini", "openai", "google", "condition A", "condition B"):
        assert leak.lower() not in g.lower()
    assert "POST TEXT" in g and "{reply_1}" not in g

def test_redaction_removes_post():
    post = "My very specific story about Becky."
    r = redacted_turn1(42, post)
    assert "Becky" not in r and sha256_text(post) in r and "row_id=42" in r
    assert post in user_turn1(post)

def test_grader_json_parse():
    d = {k: 0 for k in GRADER_KEYS}
    assert parse_grader_json("```json\n" + json.dumps(d) + "\n```")[1] is None
    assert parse_grader_json('{"verdict_t1": "in_wrong"}')[1].startswith("missing_keys")
    assert parse_grader_json("nope")[1] == "no_json"
