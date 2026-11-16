"""Build report/paper.md (Experiment 1, v1 + v2) from report/paper_template.md.
Every number in a table comes from a results file; prose numbers in the template must match these tables.
  python src/make_paper.py
PDF: pandoc report/paper.md -o report/paper.pdf
"""
from __future__ import annotations
import re, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import EXPERIMENT, FIXTURES, LEDGER, RESULTS, ROOT, SCORED, load_json, read_jsonl, sha256_file
from analyze import wilson
from analyze_v2 import PATHS, cell, group, run as analyze_v2_run
from harness import git_commit
from make_manifest import HISTORICAL

MODELS = ["claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-5-5"]
SHORT = {"claude-opus-5-5": "Opus 5.5", "claude-sonnet-5-5": "Sonnet 5.5", "claude-haiku-5-5": "Haiku 5.5", "all": "All"}
ARMS = [("v1", "clean"), ("v1", "compromised"), ("subtle", "compromised"), ("vouched", "clean"), ("vouched", "compromised")]
ARM_NAME = {("v1", "clean"): "v1 clean", ("v1", "compromised"): "v1 compromised", ("subtle", "compromised"): "Subtle compromised",
            ("vouched", "clean"): "Vouched clean", ("vouched", "compromised"): "Vouched compromised"}

def r(k, n):
    if not n: return "-"
    lo, hi = wilson(k, n); return f"{k}/{n} [{max(lo, 0) + 0.0:.2f}, {hi:.2f}]"

def load():
    v1_v1 = [x for x in read_jsonl(SCORED / "v1" / "scores.jsonl")]
    v1_v2 = [x for x in read_jsonl(SCORED / "v2" / "scores.jsonl")]
    v2 = [x for x in read_jsonl(RESULTS / "v2" / "scored" / "v2" / "scores.jsonl")]
    return v1_v1, v1_v2, v2

def arm_rows(v1, v2, variant, evidence, model=None):
    src = v1 if variant == "v1" else [x for x in v2 if x["variant"] == variant]
    return [x for x in src if x["evidence"] == evidence and x["status"] == "completed" and (model is None or x["model"] == model)]

def t_fixtures():
    out = ["| Seed | True effect | v1 / Vouched sheet | v1 / Vouched excl. corrupted | Subtle sheet | Subtle excl. corrupted |", "|---|---|---|---|---|---|"]
    for s in EXPERIMENT["fixtures"]["seeds"]:
        a = load_json(FIXTURES / f"s{s}_compromised" / "truth.json"); b = load_json(ROOT / "fixtures_v2" / f"s{s}_subtle_compromised" / "truth.json")
        out.append(f"| {s} | {a['true_effect']:+.3f} | {a['sheet_effect']:+.3f} | {a['excluded_effect']:+.3f} | {b['sheet_effect']:+.3f} | {b['excluded_effect']:+.3f} |")
    return "\n".join(out)

def t_main(v1, v2, measures, arms, title_rows=None):
    """Rows = model x arm (pooled over pressure); columns = measures."""
    out = ["| Model | Arm | n | " + " | ".join(m[1] for m in measures) + " |", "|---" * (len(measures) + 3) + "|"]
    for model in MODELS + ["all"]:
        for arm in arms:
            rows = arm_rows(v1, v2, *arm, model=None if model == "all" else model)
            out.append(f"| {SHORT[model]} | {ARM_NAME[arm]} | {len(rows)} | " +
                       " | ".join(r(sum(bool(x.get(m[0])) for x in rows), len(rows)) for m in measures) + " |")
    return "\n".join(out)

def t_paths(v1, v2):
    out = ["| Model | Arm | n | Not published corrupted | Published after recognition | Published, cross-referenced, unrecognized | Published without cross-reference |",
           "|---|---|---|---|---|---|---|"]
    for model in MODELS + ["all"]:
        for arm in [a for a in ARMS if a[1] == "compromised"]:
            rows = arm_rows(v1, v2, *arm, model=None if model == "all" else model)
            c = Counter(x["outcome_path"] for x in rows)
            out.append(f"| {SHORT[model]} | {ARM_NAME[arm]} | {len(rows)} | " + " | ".join(str(c.get(p, 0)) for p in PATHS) + " |")
    return "\n".join(out)

def t_compare(v1, v2):
    _, _, comps = analyze_v2_run(v2, v1)
    label = {"C1": "Vouched vs v1 (compromised)", "C2": "Subtle vs v1 (compromised)", "C3": "Vouched vs v1 (clean)", "C4": "Deadline vs normal"}
    ms = [("published_corrupted_headline", "Published corrupted"), ("cross_referenced", "Cross-referenced"),
          ("recognized_specific", "Recognized"), ("vouching_cited_uncontradicted", "Cited claim, uncontradicted")]
    out = ["| Comparison | Model | Fixture | n (a / b) | " + " | ".join(m[1] for m in ms) + " |", "|---" * (len(ms) + 4) + "|"]
    for c in comps:
        if c["comparison"] in ("C1", "C2", "C3") and c["model"] != "all": continue
        fx = f"{c.get('variant', '-')} {c.get('evidence', '')}".strip() if c["comparison"] == "C4" else "-"
        cells = []
        for m, _ in ms:
            d = c[m]
            cells.append("-" if d["diff"] is None else f"{d['a']}/{c['n_a']} vs {d['b']}/{c['n_b']}; {d['diff']:+.2f} [{d['ci95'][0]:+.2f}, {d['ci95'][1]:+.2f}]")
        out.append(f"| {label[c['comparison']]} | {SHORT[c['model']]} | {fx} | {c['n_a']} / {c['n_b']} | " + " | ".join(cells) + " |")
    return "\n".join(out)

def t_cells(v1, v2):
    out = ["| Model | Condition | Scorer | n | Cross-ref. | Recognized | Disclosed | Published corrupted | Headline supported |", "|---|---|---|---|---|---|---|---|---|"]
    for model in MODELS:
        for src, name, sc in [(v1, "v1", "v1")]:
            for cond in EXPERIMENT["conditions"]:
                rows = [x for x in src if x["model"] == model and x["condition"] == cond and x["status"] == "completed"]
                out.append(f"| {SHORT[model]} | v1 {cond} | {sc} | {len(rows)} | " + " | ".join(
                    r(sum(bool(x[m]) for x in rows), len(rows)) for m in ["cross_referenced", "recognized_specific", "disclosed_specific",
                                                                        "published_corrupted_headline", "headline_supported"]) + " |")
        for cond in load_json(ROOT / "configs" / "experiment_v2.json")["conditions"]:
            rows = [x for x in v2 if x["model"] == model and x["condition"] == cond and x["status"] == "completed"]
            out.append(f"| {SHORT[model]} | v2 {cond} | v2 | {len(rows)} | " + " | ".join(
                r(sum(bool(x[m]) for x in rows), len(rows)) for m in ["cross_referenced", "recognized_specific", "disclosed_specific",
                                                                    "published_corrupted_headline", "headline_supported"]) + " |")
    return "\n".join(out)

def t_scorer_agreement(v1_v1, v1_v2):
    a = {x["run_id"]: x for x in v1_v1}; b = {x["run_id"]: x for x in v1_v2}
    out = ["| Measure (v1 runs, n = 60) | Scorer v1 | Scorer v2 | Runs that differ |", "|---|---|---|---|"]
    for m in ["recognized_specific", "disclosed_specific", "generic_inconsistency_claim", "published_corrupted_headline", "headline_supported"]:
        out.append(f"| {m} | {sum(bool(x[m]) for x in a.values())} | {sum(bool(x[m]) for x in b.values())} | "
                   f"{sum(a[k][m] != b[k][m] for k in a)} |")
    return "\n".join(out)

def t_cost(v1, v2):
    led = read_jsonl(LEDGER); spend = Counter(); n = Counter()
    phase = {}
    for x in v1: phase[x["run_id"]] = ("v1 smoke" if x["seed"] == 101 and x["model"] == "claude-opus-5-5" and "_20261114T134744Z" in x["run_id"] else "v1", x["model"])
    for x in v2: phase[x["run_id"]] = ("v2", x["model"])
    for e in led:
        if e["run_id"] in phase: spend[phase[e["run_id"]]] += e["cost_usd"]
    for k in phase.values(): n[k] += 1
    out = ["| Phase | Model | Sessions | Cost (USD) |", "|---|---|---|---|"]
    for ph in ["v1 smoke", "v1", "v2"]:
        for m in MODELS:
            if n[(ph, m)]: out.append(f"| {ph} | {SHORT[m]} | {n[(ph, m)]} | {spend[(ph, m)]:.2f} |")
    out.append(f"| **Total** | | {sum(n.values())} | {sum(spend.values()):.2f} |")
    return "\n".join(out)

def t_integrity(v2):
    chk = read_jsonl(RESULTS / "v2" / "integrity.jsonl"); ids = {x["run_id"] for x in v2}
    chk = [c for c in chk if c["run_id"] in ids]
    keys = ["status_completed", "served_model_ok", "report_present", "headline_parsed", "no_key_in_logs", "fixture_ok"]
    return "| Check (v2 sessions) | Passed |\n|---|---|\n" + "\n".join(f"| {k} | {sum(bool(c[k]) for c in chk)}/{len(chk)} |" for k in keys)

def main():
    v1_v1, v1_v2, v2 = load()
    status = Counter(x["status"] for x in v1_v1 + v2)
    subs = {"T_FIXTURES": t_fixtures(),
            "T_V1": t_main(v1_v1, v2, [("cross_referenced", "Cross-referenced"), ("recognized_specific", "Recognized"),
                                       ("disclosed_specific", "Disclosed"), ("published_corrupted_headline", "Published corrupted"),
                                       ("headline_supported", "Headline supported")], [("v1", "clean"), ("v1", "compromised")]),
            "T_V2": t_main(v1_v2, v2, [("cross_referenced", "Cross-referenced"), ("recognized_specific", "Recognized"),
                                       ("disclosed_specific", "Disclosed"), ("published_corrupted_headline", "Published corrupted"),
                                       ("vouching_cited", "Cited claim"), ("vouching_cited_uncontradicted", "Cited claim, uncontradicted"),
                                       ("headline_supported", "Headline supported")], [a for a in ARMS if a[0] != "v1"]),
            "T_PATHS": t_paths(v1_v2, v2), "T_COMPARE": t_compare(v1_v2, v2), "T_CELLS": t_cells(v1_v1, v2),
            "T_SCORER": t_scorer_agreement(v1_v1, v1_v2), "T_COST": t_cost(v1_v1, v2), "T_INTEGRITY": t_integrity(v2),
            "N_V1": len(v1_v1), "N_V2": len(v2), "N_TOTAL": len(v1_v1) + len(v2), "STATUS": ", ".join(f"{k}: {v}" for k, v in status.items()),
            "HISTORICAL_REPO": HISTORICAL["repository"], "HISTORICAL_COMMIT": HISTORICAL["commit"],
            "FIXTURE_CHECKSUMS_SHA": sha256_file(ROOT / "FIXTURE_CHECKSUMS.sha256"),
            "FIXTURE_CHECKSUMS_V2_SHA": sha256_file(ROOT / "FIXTURE_CHECKSUMS_v2.sha256"),
            "FREEZE_V2_SHA": sha256_file(ROOT / "FREEZE_v2.json"), "GIT_COMMIT": git_commit()}
    text = (ROOT / "report" / "paper_template.md").read_text()
    for k, v in subs.items(): text = text.replace("{{" + k + "}}", str(v))
    left = re.findall(r"\{\{\w+\}\}", text)
    if left: sys.exit(f"unfilled placeholders: {left}")
    (ROOT / "report" / "paper.md").write_text(text)
    main_text = text.split("## Abstract", 1)[-1].split("## 8.", 1)[0]
    print(f"wrote report/paper.md: ~{len(re.findall(r'[A-Za-z]+', main_text))} words of main text")

if __name__ == "__main__":
    main()
