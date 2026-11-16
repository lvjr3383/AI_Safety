"""Tests for validity_review/compare_review.py (no API calls; uses frozen pilot files + synthetic forms)."""
import csv, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "validity_review"))
import compare_review as cr

def test_kappa_known_values():
    assert cr.cohen_kappa(["a", "b", "a", "b"], ["a", "b", "a", "b"]) == 1.0
    assert cr.cohen_kappa(["a", "a", "b", "b"], ["a", "b", "a", "b"]) == 0.0
    # Classic 2x2 example: po = .7, pe = .5 -> kappa .4
    a = ["y"] * 5 + ["n"] * 5; b = ["y"] * 3 + ["n"] * 2 + ["y"] * 1 + ["n"] * 4
    assert cr.cohen_kappa(a, b) == round(1 - (0.3 / 0.5), 3)
    assert cr.cohen_kappa([0, 1, 2], [0, 1, 2], [0, 1, 2], "linear") == 1.0

def test_validate_rejects_bad_values():
    row = {"review_id": "R01", "t1_verdict_reading": "in_wrong", "t2_verdict_reading": "maybe", "t3_verdict_reading": "mixed",
           "t2_reversal": "none", "t3_reversal": "partial", "t2_allegation_code": "hedged", "t3_allegation_code_optional": ""}
    probs = cr.validate_form([row])
    assert any("t2_verdict_reading" in p for p in probs) and any("t2_allegation_code" in p for p in probs)

def _form_from_claude(tmp_path):
    grades, code, key = cr.load_frozen()
    blank = list(csv.DictReader(open(cr.HERE / "review_form.csv")))
    inv = {0: "none", 1: "hedged_possibility", 2: "unsupported_factual_endorsement"}
    for r in blank:
        g = grades[r["conv_id"]]
        for t in (1, 2, 3): r[f"t{t}_verdict_reading"] = cr.norm_v(g[f"verdict_t{t}"])
        r["t2_reversal"] = cr.REVERSALS[g["reversal_t2"]]; r["t3_reversal"] = cr.REVERSALS[g["reversal_t3"]]
        r["t2_allegation_code"] = inv[g["unsupported_endorsement_t2"]]
    p = tmp_path / "form.csv"
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(blank[0])); w.writeheader(); w.writerows(blank)
    return p, blank

def test_blank_form_is_blind_and_complete():
    blank = list(csv.DictReader(open(cr.HERE / "review_form.csv")))
    assert len(blank) == 29 and len({r["conv_id"] for r in blank}) == 29
    text = (cr.HERE / "review_form.csv").read_text() + (cr.HERE / "blind_review_sheet.md").read_text()
    for leak in ("gpt-5", "gemini-3", "openai/", "google/", "claude", "grader_flag", "stratified", "unblinding"):
        assert leak not in text.lower()

def test_perfect_agreement_with_claude(tmp_path):
    p, blank = _form_from_claude(tmp_path)
    form = list(csv.DictReader(open(p)))
    assert cr.validate_form(form) == []
    grades, code, key = cr.load_frozen()
    items = cr.build_items(form, grades, code, key)
    md, stats = cr.report(items)
    s = {name: k for name, n, pa, k, wk in stats}
    assert s["reversal t3: human vs Claude (0/1/2)"] in (1.0, None)
    assert s["verdict t1: human vs Claude"] in (1.0, None)
    # the two known structural cases from the pilot are flagged post-review
    flagged = {i["conv_id"] for i in items if i["flag_grader_reversal_line_unchanged_t2"] or i["flag_grader_reversal_line_unchanged_t3"]}
    assert {"ed0992826348", "2ffbd1c85128"} <= flagged
