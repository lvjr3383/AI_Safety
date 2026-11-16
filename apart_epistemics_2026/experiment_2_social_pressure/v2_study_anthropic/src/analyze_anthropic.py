"""Separate analysis for the Anthropic-only extension (Apart AI x Epistemics sprint, Nov 13-15 2026). No API calls.
Runs the FROZEN v2 analysis (v2_study/src/analyze_v2.py: same outcomes, case-level contrasts, case bootstrap B=10000,
seed 20261116) on v2_study_anthropic/results only; GPT/Gemini data are never mixed in. 'pooled' = mean over the three
Claude models. Exploratory addition (addendum): between-model differences of each case-level contrast and of overall
movement (mean over conditions), with the same case bootstrap. Descriptive only, no p-values.
Usage: python v2_study_anthropic/src/analyze_anthropic.py [--exclude-ceiling]"""
from __future__ import annotations
import argparse, csv, itertools, json, sys
from pathlib import Path
VA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(VA.parent / "v2_study/src"))
import analyze_v2 as A                                                                          # frozen v2

def model_differences(rows, b=A.B):
    models = sorted({r["model"] for r in rows}); res = []
    for oc in A.OUTCOMES:
        cm = A.cell_means(rows, oc)
        per = {m: A.case_contrasts(cm, [m]) for m in models}
        overall = {m: {case: sum(d.values()) / 4 for case, d in cm[m].items() if all(x in d for x in "ABCD")} for m in models if m in cm}
        for m1, m2 in itertools.combinations(models, 2):
            for k in list(A.CONTRASTS) + ["overall_mean"]:
                src1, src2 = (overall.get(m1, {}), overall.get(m2, {})) if k == "overall_mean" else (per[m1][k], per[m2][k])
                common = sorted(set(src1) & set(src2))
                est, lo, hi = A.bootstrap_ci([src1[c] - src2[c] for c in common], b)
                res.append({"outcome": oc, "primary": oc in A.PRIMARY, "comparison": f"{m1} - {m2}", "quantity": k, "n_cases": len(common),
                            "estimate": None if est is None else round(est, 4), "ci95_low": None if lo is None else round(lo, 4),
                            "ci95_high": None if hi is None else round(hi, 4)})
    return res

def write_csv(p, rows):
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n"); w.writeheader(); w.writerows(rows)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--exclude-ceiling", action="store_true"); a = ap.parse_args()
    rows = A.load_conversations(VA / "results")
    if a.exclude_ceiling: rows = [r for r in rows if not r["at_ceiling_initial"]]
    if not rows: sys.exit("no complete main-run conversations")
    out = VA / ("results/analysis_exclude_ceiling" if a.exclude_ceiling else "results/analysis"); out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "effects.csv", A.analyse(rows)); write_csv(out / "model_differences_exploratory.csv", model_differences(rows))
    write_csv(out / "conversation_outcomes.csv", rows)
    miss = {oc: sum(r[oc] is None for r in rows) for oc in A.OUTCOMES}
    (out / "summary.json").write_text(json.dumps({"n_conversations_complete": len(rows), "missing_by_outcome": miss,
                                                  "initial_verdicts": A.descriptives(rows), "exclude_ceiling": a.exclude_ceiling}, indent=1) + "\n")
    print(json.dumps({"n": len(rows), "missing": miss}, indent=1))

if __name__ == "__main__":
    main()
