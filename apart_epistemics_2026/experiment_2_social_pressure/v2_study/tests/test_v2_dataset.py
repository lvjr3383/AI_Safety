"""Dataset integrity for the v2 case selection."""
import json, pytest
from v2_common import V2, EXP
import select_cases_v2 as S

MAN = json.loads((V2 / "config/manifest_v2.json").read_text())

def test_manifest_shape_and_disjoint_from_pilot():
    cs = MAN["cases"]; ids = [c["row_id"] for c in cs]
    assert len(cs) == 30 and len(set(ids)) == 30
    pilot = {c["row_id"] for c in json.loads((EXP / "data/manifest.json").read_text())["pilot_cases"]}
    assert not (set(ids) & pilot)
    assert {c: sum(x["category"] == c for x in cs) for c in S.CATS} == {c: 10 for c in S.CATS}
    for c in cs: assert len(c["prompt_sha256"]) == 64 and S.MIN_CH <= c["chars"] <= S.MAX_CH and "prompt" not in c

def test_manifest_has_no_post_text():
    txt = (V2 / "config/manifest_v2.json").read_text()
    assert len(txt) < 40000 and "AITA" not in txt.replace("AITA-YTA", "")

def test_rules_each_fire_in_order():
    ok = ("My husband and my wife and my partner argued at the wedding about dating. " * 15).strip()
    assert S.first_failed_rule(ok, 1, set(), set()) is None
    assert S.first_failed_rule(ok, 1, {1}, set()) == "pilot_case"
    assert S.first_failed_rule(ok, 2, set(), {ok}) == "public_github_sample"
    assert S.first_failed_rule("short.", 2, set(), set()) == "incomplete"
    assert S.first_failed_rule(ok + " and then", 2, set(), set()) == "incomplete"
    assert S.first_failed_rule(ok * 3, 2, set(), set()) == "excessively_long"
    assert S.first_failed_rule(ok + " EDIT: it went fine.", 2, set(), set()) == "verdict_leak_edit_update"
    assert S.first_failed_rule(ok + " see www.x.com.", 2, set(), set()) == "url"
    assert S.first_failed_rule(ok + " He went to the funeral.", 2, set(), set()) == "sensitive"
    assert S.first_failed_rule(ok + " My son (14M) was there.", 2, set(), set()) == "minor_involved"
    assert S.first_failed_rule(("We talked about the weather and lunch plans today. " * 20).strip(), 2, set(), set()) == "no_clear_category"

def test_selection_is_deterministic_and_reproduces_manifest():
    raw = EXP / "data/raw/AITA-YTA.csv"
    if not raw.exists(): pytest.skip("raw data not present (gitignored)")
    import pandas as pd
    df = pd.read_csv(raw).rename(columns={"Unnamed: 0": "row_id"})
    sample = set(pd.read_csv(EXP / "data/raw/AITA-YTA_sample.csv")["prompt"])
    pilot = {c["row_id"] for c in json.loads((EXP / "data/manifest.json").read_text())["pilot_cases"]}
    s1, c1 = S.select(zip(df.row_id, df.prompt, df.ytanta), pilot, sample)
    s2, _ = S.select(zip(df.row_id, df.prompt, df.ytanta), pilot, sample)
    assert s1 == s2 and [c["row_id"] for c in s1] == [c["row_id"] for c in MAN["cases"]]
    assert c1 == MAN["excluded_counts_first_failed_rule"]
    by = df.set_index("row_id")
    for c in MAN["cases"]: assert S.sha(by.loc[c["row_id"], "prompt"]) == c["prompt_sha256"]
