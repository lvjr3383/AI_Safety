"""Prompt isolation + config fidelity to the frozen v2 protocol (Anthropic-only extension, Apart sprint Nov 13-15 2026)."""
import json
from pathlib import Path
import run_anthropic as RA
import v2_common as V

def test_body_matches_frozen_v2_prompts_exactly():
    for cond in "ABCD":
        sys_p = V.system_prompt(cond); msgs = [{"role": "user", "content": V.user_turn1("POST TEXT")}]
        b = RA.build_body("claude-sonnet-4-6", sys_p, msgs)
        assert b["system"] == sys_p and b["messages"][0]["content"] == V.user_turn1("POST TEXT")
        assert set(b) == {"model", "system", "messages", "max_tokens"}          # no temperature / thinking / seed / metadata
        assert b["max_tokens"] == 2000 and all(m["role"] in ("user", "assistant") for m in b["messages"])

def test_same_inputs_across_models_except_model_field():
    sys_p = V.system_prompt("D"); msgs = [{"role": "user", "content": V.user_turn1("P")}]
    bodies = [RA.build_body(m, sys_p, msgs) for m in RA.STUDY["targets"]]
    for b in bodies:
        assert {k: v for k, v in b.items() if k != "model"} == {k: v for k, v in bodies[0].items() if k != "model"}

def test_no_condition_or_model_leak_in_user_turns():
    texts = [V.user_turn1("P"), V.rebuttal(2), V.rebuttal(3)]
    for t in texts:
        low = t.lower()
        for bad in ("claude", "anthropic", "sonnet", "haiku", "opus", "evaluation", "condition", "researcher"):
            assert bad not in low, bad

def test_messages_sent_per_turn(tmp_path):
    seen = []
    def fake(body):
        seen.append(json.loads(json.dumps(body)))
        return 200, {"id": "m", "model": body["model"], "type": "message", "stop_reason": "end_turn",
                     "content": [{"type": "text", "text": "x\nVerdict: Mixed\nBlame: 4\nConfidence: 6"}],
                     "usage": {"input_tokens": 10, "output_tokens": 5}}, 0.1, 0
    job = RA.build_jobs()[0]; g = RA.BudgetGuard(5, tmp_path / "l.jsonl")
    RA.run_conversation(job, "THE POST", g, 1, RA.Paths(tmp_path), fake)
    assert [len(b["messages"]) for b in seen] == [1, 3, 5]
    assert seen[1]["messages"][2]["content"] == V.rebuttal(2) and seen[2]["messages"][4]["content"] == V.rebuttal(3)
    assert all(b["system"] == V.system_prompt(job["condition"]) for b in seen)
    pub = (tmp_path / "raw/turns.jsonl").read_text()
    assert "THE POST" not in pub and "THE POST" in (tmp_path / "local_private/turns_full.jsonl").read_text()

def test_design_identical_to_frozen_v2():
    assert RA.STUDY["conditions"] == V.STUDY["conditions"] and RA.STUDY["repetitions"] == V.STUDY["repetitions"]
    assert RA.STUDY["seed"] == V.STUDY["seed"] and RA.STUDY["turns"] == V.STUDY["turns"]
    assert all(c["max_tokens"] == 2000 and c["temperature"] is None and c["thinking"] is None for c in RA.STUDY["targets"].values())

def test_target_ids_were_listed_by_models_endpoint():
    p = RA.VA / "results/model_checks.jsonl"
    listed = {m["id"] for m in json.loads(p.read_text().splitlines()[-1])["models"]}
    assert set(RA.STUDY["targets"]) <= listed

def test_prices_are_official_list_prices():
    pv = RA.STUDY["prices_verified"]
    assert (pv["claude-sonnet-4-6"]["input"], pv["claude-sonnet-4-6"]["output"]) == (3e-6, 15e-6)
    assert (pv["claude-haiku-4-5-20251001"]["input"], pv["claude-haiku-4-5-20251001"]["output"]) == (1e-6, 5e-6)
    assert (pv["claude-opus-4-7"]["input"], pv["claude-opus-4-7"]["output"]) == (5e-6, 25e-6)
