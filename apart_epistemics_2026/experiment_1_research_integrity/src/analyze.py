"""Aggregate scored runs into per-condition counts with Wilson 95% intervals. Counts only; no modelling.
Usage: python src/analyze.py [--scored results/scored/scores.jsonl] [--out results/summary]
"""
from __future__ import annotations
import argparse, csv, json, math, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import EXPERIMENT, RESULTS, SCORED, read_jsonl

BINARY = ["checked_raw_evidence", "cross_referenced", "recognized_specific", "disclosed_specific",
          "published_corrupted_headline", "recognized_and_published_corrupted", "disclosed_and_published_corrupted",
          "recognized_not_disclosed", "headline_supported", "generic_inconsistency_claim", "generic_caveat_only",
          "recognized_in_thinking", "sheet_value_in_report_body"]
CLASSES = ["correct", "corrected", "corrected_by_exclusion", "withheld", "corrupted_sheet_value", "other_number", "missing"]

def wilson(k: int, n: int, z: float = 1.96):
    if n == 0: return (None, None)
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(c - h, 3), round(c + h, 3))

def summarize(rows: list) -> list:
    cells = []
    for cond in EXPERIMENT["conditions"]:
        rs = [r for r in rows if r["condition"] == cond]
        ok = [r for r in rs if r["status"] == "completed"]
        cell = {"condition": cond, "n_runs": len(rs), "n_completed": len(ok),
                "status_counts": dict(Counter(r["status"] for r in rs))}
        for b in BINARY:
            k = sum(bool(r[b]) for r in ok); lo, hi = wilson(k, len(ok))
            cell[b] = k; cell[b + "_ci95"] = [lo, hi]
        cls = Counter(r["headline_class"] for r in ok)
        for c in CLASSES: cell["headline_" + c] = cls.get(c, 0)
        cells.append(cell)
    return cells

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scored", default=str(SCORED / "scores.jsonl")); ap.add_argument("--out", default=str(RESULTS / "summary"))
    a = ap.parse_args()
    rows = read_jsonl(a.scored); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    cells = summarize(rows)
    (out / "cells.json").write_text(json.dumps(cells, indent=1) + "\n")
    keys = ["condition", "n_runs", "n_completed"] + BINARY + ["headline_" + c for c in CLASSES]
    with open(out / "cells.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore"); w.writeheader(); w.writerows(cells)
    print(f"{len(rows)} scored runs -> {out}/cells.csv")

if __name__ == "__main__":
    main()
