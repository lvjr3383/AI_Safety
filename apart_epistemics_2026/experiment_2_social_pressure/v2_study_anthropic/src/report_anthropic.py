"""Figures + results tables for the Anthropic-only extension (Apart AI x Epistemics sprint, Nov 13-15 2026). No API calls.
Presentation only (written after the freeze; computes no new inferential quantities beyond the frozen analysis except
descriptive per-condition means with the same case bootstrap). Reads results/raw, results/ledger_anthropic.jsonl,
results/analysis*/. Writes results/analysis/*.png and results/analysis/RESULTS_TABLES.md (+ presentation CSVs). Frozen analysis CSVs are produced by analyze_anthropic.py in the same folder.
Usage: python v2_study_anthropic/src/report_anthropic.py"""
from __future__ import annotations
import csv, json, sys
from collections import Counter, defaultdict
from pathlib import Path
VA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(VA.parent / "v2_study/src")); sys.path.insert(0, str(VA / "src"))
import analyze_v2 as A
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

R = VA / "results"; FIG = R / "analysis"; TAB = R / "analysis"
LABEL = {"claude-haiku-4-5-20251001": "Haiku 4.5", "claude-sonnet-4-6": "Sonnet 4.6", "claude-opus-4-7": "Opus 4.7"}
ORDER = ["claude-haiku-4-5-20251001", "claude-sonnet-4-6", "claude-opus-4-7"]
COND = {"A": "A ordinary", "B": "B ordinary+honesty", "C": "C evaluation", "D": "D evaluation+honesty"}
def rd(p): return [json.loads(l) for l in open(p)] if Path(p).exists() else []
def rcsv(p): return list(csv.DictReader(open(p))) if Path(p).exists() else []
def f(x, n=3): return "" if x in (None, "") else f"{float(x):.{n}f}"

def latest_complete():
    latest = {}
    for c in rd(R / "raw/conversations.jsonl"):
        if c["status"] == "complete" and c.get("stage") == "main" and (c["conv_id"] not in latest or c["attempt"] > latest[c["conv_id"]]["attempt"]):
            latest[c["conv_id"]] = c
    return list(latest.values())

def run_stats():
    convs = rd(R / "raw/conversations.jsonl"); turns = rd(R / "raw/turns.jsonl"); led = rd(R / "ledger_anthropic.jsonl")
    ids = {c["conv_id"] for c in convs if c.get("stage") == "main"}
    complete = {c["conv_id"] for c in convs if c["status"] == "complete"}
    out = {"attempts_total": len(convs), "attempt_status": dict(Counter(c["status"] for c in convs)), "conversations_attempted": len(ids),
           "conversations_complete": len(complete), "conversations_never_completed": len(ids - complete),
           "turn_calls": len(turns), "turn_calls_with_transient_retries": sum(1 for t in turns if t.get("transient_retries")),
           "transient_retries_total": sum(t.get("transient_retries") or 0 for t in turns),
           "stop_reasons": dict(Counter(t.get("finish_reason") for t in turns)),
           "non_text_blocks": sum(1 for t in turns if any(b != "text" for b in (t.get("block_types") or []))), "per_model": {}}
    for m in ORDER:
        lm = [x for x in led if x["model"] == m]
        out["per_model"][m] = {"complete": sum(1 for c in latest_complete() if c["model"] == m), "calls": len(lm),
                               "input_tokens": sum(x.get("input_tokens") or 0 for x in lm), "output_tokens": sum(x.get("output_tokens") or 0 for x in lm),
                               "cost_usd": round(sum(x["cost_usd"] or 0 for x in lm), 6)}
    out["ledger_total_usd"] = round(sum(x["cost_usd"] or 0 for x in led), 6)
    resp = [t for t in turns if t.get("response")]
    out["parse"] = {"turns_with_response": len(resp), "verdict_unparsed": sum(t["parsed_verdict"] == "unparsed" for t in resp),
                    "blame_missing": sum(t["parsed_blame"] is None for t in resp), "confidence_missing": sum(t["parsed_confidence"] is None for t in resp)}
    out["abandoned_requests_total"] = sum(t.get("abandoned_requests") or 0 for t in turns)
    return out

def floor_ceiling(convs):
    out = {}
    for m in ORDER + ["all"]:
        cs = [c for c in convs if m == "all" or c["model"] == m]
        if not cs: continue
        t = lambda c, k: sorted(c["turns"], key=lambda x: x["turn"])[k - 1]
        init = Counter(t(c, 1)["parsed_verdict"] for c in cs); fin = Counter(t(c, 3)["parsed_verdict"] for c in cs)
        b1 = [t(c, 1)["parsed_blame"] for c in cs if t(c, 1)["parsed_blame"] is not None]
        out[m] = {"n": len(cs), "initial_verdict": dict(init), "final_verdict_t3": dict(fin),
                  "pct_initial_not_in_wrong_ceiling": round(100 * init["not_in_wrong"] / len(cs), 1),
                  "pct_initial_in_wrong": round(100 * init["in_wrong"] / len(cs), 1),
                  "pct_blame_t1_at_0": round(100 * sum(b == 0 for b in b1) / len(b1), 1) if b1 else None,
                  "mean_blame_t1": round(sum(b1) / len(b1), 2) if b1 else None,
                  "pct_any_verdict_move_toward_push_t3": round(100 * sum(1 for c in cs if (A.FAULT.get(t(c, 1)["parsed_verdict"]) is not None and A.FAULT.get(t(c, 3)["parsed_verdict"]) is not None and A.FAULT[t(c, 1)["parsed_verdict"]] > A.FAULT[t(c, 3)["parsed_verdict"]])) / len(cs), 1),
                  "pct_verdict_move_away_from_push_t3": round(100 * sum(1 for c in cs if (A.FAULT.get(t(c, 1)["parsed_verdict"]) is not None and A.FAULT.get(t(c, 3)["parsed_verdict"]) is not None and A.FAULT[t(c, 1)["parsed_verdict"]] < A.FAULT[t(c, 3)["parsed_verdict"]])) / len(cs), 1)}
    return out

def condition_means(rows, outcome, b=A.B):
    """Case-level (reps averaged) mean per model x condition with case-bootstrap 95% CI (descriptive)."""
    cm = A.cell_means(rows, outcome); out = []
    for m in ORDER:
        for cond in "ABCD":
            vals = [d[cond] for d in cm.get(m, {}).values() if cond in d]
            est, lo, hi = A.bootstrap_ci(vals, b)
            out.append({"outcome": outcome, "model": m, "condition": cond, "n_cases": len(vals), "mean": est, "ci95_low": lo, "ci95_high": hi})
    return out

def fig_condition(cmeans, outcome, ylabel, path):
    fig, ax = plt.subplots(figsize=(8, 4.2)); w = 0.2
    for i, cond in enumerate("ABCD"):
        xs, ys, el, eh = [], [], [], []
        for j, m in enumerate(ORDER):
            r = next(x for x in cmeans if x["model"] == m and x["condition"] == cond and x["outcome"] == outcome)
            if r["mean"] is None: continue
            xs.append(j + (i - 1.5) * w); ys.append(r["mean"]); el.append(r["mean"] - r["ci95_low"]); eh.append(r["ci95_high"] - r["mean"])
        ax.bar(xs, ys, w, yerr=[el, eh], capsize=3, label=COND[cond])
    ax.set_xticks(range(len(ORDER))); ax.set_xticklabels([LABEL[m] for m in ORDER]); ax.axhline(0, color="k", lw=0.6)
    ax.set_ylabel(ylabel); ax.legend(fontsize=8, ncol=2); ax.set_title(f"{ylabel} by condition (case-level means, 95% case-bootstrap CI)", fontsize=9)
    fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)

def fig_forest(effects, path, title):
    rows = [r for r in effects if r["primary"] == "True"]
    oc = ["moved_toward_push_t3", "verdict_move_t3", "conf_change_t3"]; scopes = ORDER + ["pooled"]
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.5), sharey=True)
    for ax, o in zip(axes, oc):
        ylab, y = [], 0
        for k in ["honesty", "framing", "interaction"]:
            for s in scopes:
                r = next((x for x in rows if x["outcome"] == o and x["contrast"] == k and x["scope"] == s), None)
                if r and r["estimate"] not in ("", None):
                    e, lo, hi = float(r["estimate"]), float(r["ci95_low"]), float(r["ci95_high"])
                    ax.errorbar(e, y, xerr=[[e - lo], [hi - e]], fmt="o", color="C3" if s == "pooled" else "C0", capsize=3)
                ylab.append(f"{k} | {LABEL.get(s, s)}"); y += 1
            y += 0.5; ylab.append("")
        ax.axvline(0, color="k", lw=0.6); ax.set_title(o, fontsize=9)
        ticks = [i for i, l in enumerate(ylab)]; 
    yt, yl, y = [], [], 0
    for k in ["honesty", "framing", "interaction"]:
        for s in scopes: yt.append(y); yl.append(f"{k} | {LABEL.get(s, s)}"); y += 1
        y += 0.5
    axes[0].set_yticks(yt); axes[0].set_yticklabels(yl, fontsize=7); axes[0].invert_yaxis()
    fig.suptitle(title, fontsize=10); fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)

def fig_initial(fc, path):
    fig, ax = plt.subplots(figsize=(6, 3.8)); cats = [c for c in ["in_wrong", "mixed", "not_in_wrong", "unparsed"] if any(fc.get(m, {}).get("initial_verdict", {}).get(c, 0) for m in ORDER)]; bottom = [0] * len(ORDER)
    for c in cats:
        vals = [fc.get(m, {}).get("initial_verdict", {}).get(c, 0) for m in ORDER]
        ax.bar([LABEL[m] for m in ORDER], vals, bottom=bottom, label=c); bottom = [a + b for a, b in zip(bottom, vals)]
    ax.set_ylabel("conversations"); ax.set_title("Initial (turn-1) verdict per model (not_in_wrong = ceiling)", fontsize=9); ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)

def fig_trajectory(convs, key, ylabel, path, fault=False):
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.6), sharey=True)
    for ax, m in zip(axes, ORDER):
        for cond in "ABCD":
            ys = []
            for k in (1, 2, 3):
                v = [(A.FAULT.get(t[key]) if fault else t[key]) for c in convs if c["model"] == m and c["condition"] == cond
                     for t in c["turns"] if t["turn"] == k]
                v = [x for x in v if x is not None]; ys.append(sum(v) / len(v) if v else None)
            ax.plot([1, 2, 3], ys, marker="o", label=COND[cond])
        ax.set_title(LABEL[m], fontsize=9); ax.set_xticks([1, 2, 3]); ax.set_xlabel("turn")
    axes[0].set_ylabel(ylabel); axes[-1].legend(fontsize=7); fig.suptitle(f"Mean {ylabel} by turn (conversation means, descriptive)", fontsize=9)
    fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)

def md_table(rows, cols, hdr=None):
    s = "| " + " | ".join(hdr or cols) + " |\n|" + "---|" * len(cols) + "\n"
    return s + "".join("| " + " | ".join(str(r.get(c, "")) for c in cols) + " |\n" for r in rows)

def main():
    FIG.mkdir(parents=True, exist_ok=True); TAB.mkdir(parents=True, exist_ok=True)
    convs = latest_complete(); rows = A.load_conversations(R); st = run_stats(); fc = floor_ceiling(convs)
    cmeans = [r for oc in A.PRIMARY + ["blame_move_t3"] for r in condition_means(rows, oc)]
    with open(TAB / "condition_means.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(cmeans[0]), lineterminator="\n"); w.writeheader(); w.writerows(cmeans)
    (TAB / "run_stats.json").write_text(json.dumps(st, indent=1) + "\n"); (TAB / "floor_ceiling.json").write_text(json.dumps(fc, indent=1) + "\n")
    eff = rcsv(R / "analysis/effects.csv"); effx = rcsv(R / "analysis_exclude_ceiling/effects.csv"); md = rcsv(R / "analysis/model_differences_exploratory.csv")
    fig_condition(cmeans, "moved_toward_push_t3", "P(verdict moved toward push by t3)", FIG / "fig1_moved_toward_push_by_condition.png")
    fig_condition(cmeans, "conf_change_t3", "confidence change t1->t3", FIG / "fig2_confidence_change_by_condition.png")
    fig_forest(eff, FIG / "fig3_contrasts_primary.png", "Primary outcomes: honesty / framing / interaction contrasts (case bootstrap 95% CI); red = pooled over Claude models")
    if effx: fig_forest(effx, FIG / "fig4_contrasts_primary_exclude_ceiling.png", "Sensitivity (exclude initial not-in-the-wrong; descriptive): contrasts")
    fig_initial(fc, FIG / "fig5_initial_verdicts.png")
    fig_trajectory(convs, "parsed_blame", "Blame (0-10)", FIG / "fig6_blame_trajectory.png")
    fig_trajectory(convs, "parsed_verdict", "fault score (2=in wrong, 0=not)", FIG / "fig7_verdict_trajectory.png", fault=True)
    L = ["# Anthropic-only extension: results tables (Apart AI x Epistemics sprint, Nov 13-15 2026)\n",
         "Generated by `src/report_anthropic.py` from the run logs and the frozen analysis outputs. Descriptive: case-bootstrap 95% CIs, no p-values. Movement under pressure is not necessarily dishonesty.\n",
         "## Run\n", md_table([{"model": LABEL[m], **v} for m, v in st["per_model"].items()], ["model", "complete", "calls", "input_tokens", "output_tokens", "cost_usd"]),
         f"\nLedger total (list price): ${st['ledger_total_usd']:.4f}. Attempts: {st['attempt_status']}. Turn calls with transient retries: {st['turn_calls_with_transient_retries']} (retries {st['transient_retries_total']}). Stop reasons: {st['stop_reasons']}. Non-text blocks: {st['non_text_blocks']}.\n",
         "\n## Condition means (case-level, reps averaged; 95% case-bootstrap CI)\n",
         md_table([{**r, "model": LABEL[r["model"]], "mean": f(r["mean"]), "ci95": f"[{f(r['ci95_low'])}, {f(r['ci95_high'])}]"} for r in cmeans],
                  ["outcome", "model", "condition", "n_cases", "mean", "ci95"]),
         "\n## Contrasts, primary outcomes (all conversations)\n",
         md_table([{**r, "scope": LABEL.get(r["scope"], r["scope"]), "ci95": f"[{r['ci95_low']}, {r['ci95_high']}]"} for r in eff if r["primary"] == "True"],
                  ["outcome", "contrast", "scope", "n_cases", "estimate", "ci95"]),
         "\n## Contrasts, secondary outcomes\n",
         md_table([{**r, "scope": LABEL.get(r["scope"], r["scope"]), "ci95": f"[{r['ci95_low']}, {r['ci95_high']}]"} for r in eff if r["primary"] != "True"],
                  ["outcome", "contrast", "scope", "n_cases", "estimate", "ci95"]),
         "\n## Sensitivity: excluding conversations whose initial verdict was not_in_wrong (post-treatment; descriptive)\n",
         md_table([{**r, "scope": LABEL.get(r["scope"], r["scope"]), "ci95": f"[{r['ci95_low']}, {r['ci95_high']}]"} for r in effx if r["primary"] == "True"],
                  ["outcome", "contrast", "scope", "n_cases", "estimate", "ci95"]),
         "\n## Exploratory: between-model differences (primary outcomes)\n",
         md_table([{**r, "ci95": f"[{r['ci95_low']}, {r['ci95_high']}]"} for r in md if r["primary"] == "True"],
                  ["outcome", "comparison", "quantity", "n_cases", "estimate", "ci95"]),
         "\n## Floor / ceiling\n", "```json\n" + json.dumps(fc, indent=1) + "\n```\n",
         "\n## Figures\n" + "".join(f"- `results/figures/{p.name}`\n" for p in sorted(FIG.glob("*.png")))]
    (TAB / "RESULTS_TABLES.md").write_text("".join(L)); print("wrote", TAB / "RESULTS_TABLES.md")

if __name__ == "__main__":
    main()
