"""Fill report/report_template.md from fixtures, scored results and the manifest -> report/report.md.
Every number in the generated report comes from a file in this directory; with no scored runs the
results section says so instead of showing anything.
PDF (Apart submission): pandoc report/report.md -o report/report.pdf  (pandoc is not installed here)
"""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import EXPERIMENT, FIXTURES, RESULTS, ROOT, SCORED, SCORING, load_json, read_jsonl, sha256_file
from analyze import summarize
from harness import git_commit
from make_manifest import HISTORICAL

WORD_LIMIT = 3800

def fixture_table() -> str:
    rows = ["| Seed | True effect (transcripts) | Sheet effect (compromised) | Effect excluding corrupted rows |", "|---|---|---|---|"]
    for seed in EXPERIMENT["fixtures"]["seeds"]:
        t = load_json(FIXTURES / f"s{seed}_compromised" / "truth.json")
        rows.append(f"| {seed} | {t['true_effect']:+.3f} | {t['sheet_effect']:+.3f} | {t['excluded_effect']:+.3f} |")
    return "\n".join(rows)

def _rate(c, k):
    lo, hi = c[k + "_ci95"]
    return f"{c[k]}/{c['n_completed']}" + (f" [{lo:.2f}, {hi:.2f}]" if lo is not None else "")

def results_section(rows) -> str:
    if not rows: return "_No experimental runs have been scored yet. This section is filled automatically from `results/scored/scores.jsonl`._"
    cells = summarize(rows)
    show = ["checked_raw_evidence", "cross_referenced", "recognized_specific", "disclosed_specific",
            "published_corrupted_headline", "recognized_and_published_corrupted", "headline_supported", "generic_inconsistency_claim"]
    out = ["Counts are runs / completed runs, with Wilson 95% intervals.", "",
           "| Measure | " + " | ".join(c["condition"] for c in cells) + " |", "|---" * (len(cells) + 1) + "|",
           "| Runs (completed) | " + " | ".join(f"{c['n_runs']} ({c['n_completed']})" for c in cells) + " |"]
    for k in show: out.append(f"| {k} | " + " | ".join(_rate(c, k) for c in cells) + " |")
    out += ["", "| Headline class | " + " | ".join(c["condition"] for c in cells) + " |", "|---" * (len(cells) + 1) + "|"]
    for cls in ["correct", "corrected", "corrected_by_exclusion", "withheld", "corrupted_sheet_value", "other_number", "missing"]:
        out.append(f"| {cls} | " + " | ".join(str(c["headline_" + cls]) for c in cells) + " |")
    return "\n".join(out)

def run_table(rows) -> str:
    if not rows: return ""
    out = ["| Run | Status | Headline | Class |", "|---|---|---|---|"]
    out += [f"| `{r['run_id']}` | {r['status']} | {r['headline_raw']} | {r['headline_class']} |" for r in rows]
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--scored", default=str(SCORED / "scores.jsonl"))
    ap.add_argument("--out", default=str(ROOT / "report" / "report.md")); a = ap.parse_args()
    rows = read_jsonl(a.scored)
    manifest = load_json(ROOT / "MANIFEST.json") if (ROOT / "MANIFEST.json").exists() else {"sprint_created": {"files_sha256": {}}}
    f = EXPERIMENT["fixtures"]
    runtimes = sorted({r["runtime"] + " / " + r["model"] for r in rows}) or ["[not yet run]"]
    subs = {"N_RESPONSES": f["n_responses"], "N_CORRUPTED": f["n_corrupted"], "DELTA": f["corruption_delta"],
            "RUNS_PER_CELL": EXPERIMENT["pilot"]["runs_per_condition"], "FIXTURE_TABLE": fixture_table(),
            "RUNTIMES": "; ".join(runtimes), "TOL": SCORING["headline_tolerance"], "RESULTS": results_section(rows),
            "HISTORICAL_REPO": HISTORICAL["repository"], "HISTORICAL_COMMIT": HISTORICAL["commit"],
            "FIXTURE_CHECKSUMS_SHA": sha256_file(ROOT / "FIXTURE_CHECKSUMS.sha256"),
            "MANIFEST_COUNT": len(manifest["sprint_created"]["files_sha256"]), "GIT_COMMIT": git_commit(), "RUN_TABLE": run_table(rows)}
    text = (ROOT / "report" / "report_template.md").read_text()
    for k, v in subs.items(): text = text.replace("{{" + k + "}}", str(v))
    left = re.findall(r"\{\{\w+\}\}", text)
    if left: sys.exit(f"unfilled placeholders: {left}")
    Path(a.out).write_text(text)
    main_text = text.split("## Abstract", 1)[-1].split("## 7.", 1)[0]
    words = len(re.findall(r"\w+", main_text))
    print(f"wrote {a.out}: ~{words} words of main text" + (f"  WARNING: over {WORD_LIMIT}" if words > WORD_LIMIT else ""))

if __name__ == "__main__":
    main()
