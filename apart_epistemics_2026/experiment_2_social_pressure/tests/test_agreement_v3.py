"""Tests for validation_v3/agreement_v3.py statistics (Apart AI x Epistemics sprint, Nov 13-15 2026).
Reference values: Fleiss' kappa example from Fleiss (1971) as reproduced on Wikipedia (0.210); Krippendorff's alpha
values cross-checked against the `krippendorff` PyPI package (not a runtime dependency)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "validation_v3"))
import agreement_v3 as A

def test_fleiss_wikipedia_example():
    table = [[0,0,0,0,14],[0,2,6,4,2],[0,0,3,5,6],[0,3,9,2,0],[2,2,8,1,1],[7,7,0,0,0],[3,2,6,3,0],[2,5,3,2,2],[6,5,2,1,0],[0,2,2,3,7]]
    rows = [[str(j) for j, c in enumerate(r) for _ in range(c)] for r in table]
    k, n = A.fleiss_kappa(rows, ["0", "1", "2", "3", "4"])
    assert n == 10 and k == 0.21

def test_krippendorff_matches_reference_package():
    rows = [["a","a","b"],["b","b","b"],["a",None,"a"],["c","c","a"],["a","b","c"],["b","b",None],["c","c","c"],["a","a","a"]]
    assert A.krippendorff_alpha(rows, ["a","b","c"], "nominal")[0] == 0.538
    assert A.krippendorff_alpha(rows, ["a","b","c"], "ordinal")[0] == 0.471

def test_perfect_and_undefined():
    assert A.krippendorff_alpha([["x","x"],["y","y"]], ["x","y"])[0] == 1.0
    assert A.krippendorff_alpha([["x","x"],["x","x"]], ["x","y"])[0] is None      # no variation -> undefined, not 1
    assert A.cohen_kappa(["x","x"], ["x","x"], ["x","y"]) is None
    assert A.cohen_kappa(["x","y","x","y"], ["x","y","x","y"], ["x","y"]) == 1.0
    assert A.pct_agree(["x", None, "y"], ["x", "y", "x"]) == 0.5

def test_gate_labels_exploratory_and_unassessable():
    multi = [{"metric": f, "graders": 2, "alpha_nominal": a} for f, a in
             [("verdict_t1", 0.9), ("verdict_t2", 0.9), ("verdict_t3", 0.9), ("judgment_change_t3", 0.7),
              ("allegation_code_t2", 0.3), ("allegation_t2_binary_endorse", 0.8)]]
    g = A.gate(multi)
    assert g["verdict"]["status"].startswith("reliable") and g["judgment_change"]["status"].startswith("reliable")
    assert g["allegation"]["status"].startswith("EXPLORATORY")          # binary cannot rescue a failing 5-way code
    g1 = A.gate([dict(m, graders=1) for m in multi])
    assert all(v["status"].startswith("NOT ASSESSABLE") for v in g1.values())

def test_analysis_has_no_majority_vote():
    d = lambda v, j, a: {"verdict_t1": v, "verdict_t2": v, "verdict_t3": v, "judgment_change_t2": j, "judgment_change_t3": j,
                         "allegation_code_t2": a, "allegation_code_t3": a, "marks_claim_unverified_t2": "no"}
    gr = {"g1": {"X1": d("in_wrong", "none", "empathy_only"), "X2": d("mixed", "partial", "hedged_factual_endorsement")},
          "g2": {"X1": d("in_wrong", "none", "conditional_hypothetical"), "X2": d("mixed", "partial", "hedged_factual_endorsement")},
          "g3": {"X1": d("in_wrong", "none", "empathy_only"), "X2": d("mixed", "none", "unqualified_factual_endorsement")}}
    res = A.analyse(gr, ["X1", "X2"])
    assert not any("majority" in str(k).lower() for r in res["multi"] + res["pairwise"] for k in r)
    m = {r["metric"]: r for r in res["multi"]}
    assert m["verdict_t1"]["alpha_nominal"] == 1.0 and m["allegation_code_t2"]["graders"] == 3
    b = next(r for r in res["pairwise"] if r["metric"] == "allegation_t2_binary_endorse" and r["pair"] == "g1 vs g2")
    assert b["pct_agree"] == 1.0
