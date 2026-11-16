"""Experiment 1 v2 analysis (frozen in FREEZE_v2.json before any v2 session). Counts only; no modelling.

Inputs: scorer v2 on v2 runs (results/v2/scored/v2/scores.jsonl) and scorer v2 on v1 runs (results/scored/v2/scores.jsonl),
so every comparison uses one scorer. Output: results/v2/summary/{cells.json, cells.csv, comparisons.json}.

Pre-specified, all descriptive (no hypothesis tests, no multiplicity claims):
  cells        model x condition, Wilson 95% intervals (n = 5 seeds per cell)
  pooled       model x variant x evidence, pooled over pressure (n = 10), and all models pooled (n = 30)
  comparisons  differences in proportions with Newcombe (hybrid score) 95% intervals:
    C1 vouched_compromised vs v1 compromised        same data, only the verification claim differs
    C2 subtle_compromised  vs v1 compromised        3 rows +1 vs 10 rows +2
    C3 vouched_clean       vs v1 clean              does the claim change checking when the data are clean
    C4 deadline vs normal within each v2 variant x evidence
  measures compared: published_corrupted_headline (primary), cross_referenced, recognized_specific,
                     disclosed_specific, vouching_cited_uncontradicted
"""
from __future__ import annotations
import csv, json, math, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import RESULTS, SCORED, read_jsonl
from analyze import wilson

MODELS = ["claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-5-5"]
V2_CONDS = ["subtle_compromised_normal", "subtle_compromised_deadline", "vouched_clean_normal", "vouched_clean_deadline",
            "vouched_compromised_normal", "vouched_compromised_deadline"]
MEASURES = ["checked_raw_evidence", "cross_referenced", "recognized_specific", "disclosed_specific", "published_corrupted_headline",
            "recognized_and_published_corrupted", "headline_supported", "generic_inconsistency_claim", "vouching_cited",
            "vouching_contradicted", "vouching_cited_uncontradicted", "headline_ambiguous", "recognized_in_thinking"]
COMPARE = ["published_corrupted_headline", "cross_referenced", "recognized_specific", "disclosed_specific", "vouching_cited_uncontradicted"]
PATHS = ["not_published_corrupted", "published_corrupted_after_recognition",
         "published_corrupted_cross_referenced_unrecognized", "published_corrupted_without_cross_reference"]
CLASSES = ["correct", "corrected", "corrected_by_exclusion", "withheld", "corrupted_sheet_value", "other_number", "missing"]

def newcombe(k1, n1, k2, n2):
    """95% interval for p1 - p2 (Newcombe 1998, method 10)."""
    if not n1 or not n2: return None
    l1, u1 = wilson(k1, n1); l2, u2 = wilson(k2, n2); p1, p2 = k1 / n1, k2 / n2
    d = p1 - p2
    return [round(d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2), 3), round(d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2), 3)]

def cell(rows, **key):
    ok = [r for r in rows if r["status"] == "completed"]
    c = {**key, "n_runs": len(rows), "n_completed": len(ok), "n_seeds": len({r["seed"] for r in ok}),
         "status_counts": dict(Counter(r["status"] for r in rows))}
    for m in MEASURES:
        k = sum(bool(r.get(m)) for r in ok); c[m] = k; c[m + "_ci95"] = list(wilson(k, len(ok)))
    cls = Counter(r["headline_class"] for r in ok)
    for x in CLASSES: c["headline_" + x] = cls.get(x, 0)
    pth = Counter(r["outcome_path"] for r in ok if r["outcome_path"])
    for x in PATHS: c["path_" + x] = pth.get(x, 0)
    return c

def group(rows, **f): return [r for r in rows if all(r[k] == v for k, v in f.items())]

def compare(name, a_rows, b_rows, a_label, b_label, **key):
    out = {"comparison": name, "a": a_label, "b": b_label, **key, "n_a": len(a_rows), "n_b": len(b_rows)}
    for m in COMPARE:
        ka, kb = sum(bool(r.get(m)) for r in a_rows), sum(bool(r.get(m)) for r in b_rows)
        out[m] = {"a": ka, "b": kb, "diff": round(ka / len(a_rows) - kb / len(b_rows), 3) if a_rows and b_rows else None,
                  "ci95": newcombe(ka, len(a_rows), kb, len(b_rows))}
    return out

def run(v2_rows, v1_rows):
    v2_rows = [r for r in v2_rows if r["status"] == "completed"]; v1_rows = [r for r in v1_rows if r["status"] == "completed"]
    cells = [cell(group(v2_rows, model=m, condition=c), model=m, condition=c) for m in MODELS for c in V2_CONDS]
    pooled = []
    for m in MODELS + ["all"]:
        mf = {} if m == "all" else {"model": m}
        for v, ev in [("subtle", "compromised"), ("vouched", "clean"), ("vouched", "compromised")]:
            pooled.append(cell(group(v2_rows, variant=v, evidence=ev, **mf), model=m, variant=v, evidence=ev, pressure="pooled"))
        for ev in ("clean", "compromised"):
            pooled.append(cell(group(v1_rows, evidence=ev, **mf), model=m, variant="v1", evidence=ev, pressure="pooled"))
    comps = []
    for m in MODELS + ["all"]:
        mf = {} if m == "all" else {"model": m}
        v1c, v1k = group(v1_rows, evidence="compromised", **mf), group(v1_rows, evidence="clean", **mf)
        comps.append(compare("C1", group(v2_rows, variant="vouched", evidence="compromised", **mf), v1c, "vouched_compromised", "v1_compromised", model=m))
        comps.append(compare("C2", group(v2_rows, variant="subtle", evidence="compromised", **mf), v1c, "subtle_compromised", "v1_compromised", model=m))
        comps.append(compare("C3", group(v2_rows, variant="vouched", evidence="clean", **mf), v1k, "vouched_clean", "v1_clean", model=m))
    for v, ev in [("subtle", "compromised"), ("vouched", "clean"), ("vouched", "compromised")]:
        comps.append(compare("C4", group(v2_rows, variant=v, evidence=ev, pressure="deadline"),
                             group(v2_rows, variant=v, evidence=ev, pressure="normal"), "deadline", "normal", model="all", variant=v, evidence=ev))
    return cells, pooled, comps

def main():
    v2_rows = read_jsonl(RESULTS / "v2" / "scored" / "v2" / "scores.jsonl"); v1_rows = read_jsonl(SCORED / "v2" / "scores.jsonl")
    cells, pooled, comps = run(v2_rows, v1_rows)
    out = RESULTS / "v2" / "summary"; out.mkdir(parents=True, exist_ok=True)
    (out / "cells.json").write_text(json.dumps({"cells": cells, "pooled": pooled}, indent=1) + "\n")
    (out / "comparisons.json").write_text(json.dumps(comps, indent=1) + "\n")
    keys = ["model", "condition", "n_runs", "n_completed", "n_seeds"] + MEASURES + ["headline_" + c for c in CLASSES] + ["path_" + p for p in PATHS]
    with open(out / "cells.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore"); w.writeheader(); w.writerows(cells)
    print(f"{len(v2_rows)} v2 runs, {len(v1_rows)} v1 runs -> {out}")

if __name__ == "__main__":
    main()
