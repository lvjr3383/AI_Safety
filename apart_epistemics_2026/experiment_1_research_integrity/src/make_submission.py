"""Build the Apart submission (HTML + PDF) for Experiment 1 from report/submission/template.html.

Tables and the figure are generated from results files. Numbers written in the template's prose are asserted against the
data here, so the PDF cannot silently disagree with the results.
  python src/make_submission.py            -> report/submission/exp1_submission.html and .pdf (headless Chrome)
"""
from __future__ import annotations
import html, json, subprocess, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import EXPERIMENT, FIXTURES, LEDGER, RESULTS, ROOT, SCORED, load_json, read_jsonl
from analyze import wilson
from make_manifest import HISTORICAL

OUT = ROOT / "report" / "submission"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MODELS = ["claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-5-5"]
SHORT = {"claude-opus-5-5": "Opus 5.5", "claude-sonnet-5-5": "Sonnet 5.5", "claude-haiku-5-5": "Haiku 5.5"}
V2 = load_json(ROOT / "configs" / "experiment_v2.json")

def up(k, n): return wilson(k, n)[1]
def frac(k, n, ci=True):
    if not n: return "–"
    lo, hi = wilson(k, n)
    return f"{k}/{n}" + (f" <span style='color:#555'>[{max(lo, 0) + 0.0:.2f}, {hi:.2f}]</span>" if ci else "")

def table(head, rows, num_cols=()):
    h = "<tr>" + "".join(f"<th class='{'num' if i in num_cols else ''}'>{c}</th>" for i, c in enumerate(head)) + "</tr>"
    b = "".join("<tr>" + "".join(f"<td class='{'num' if i in num_cols else ''}'>{c}</td>" for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f"<table>{h}{b}</table>"

def load():
    v1s1 = [r for r in read_jsonl(SCORED / "v1" / "scores.jsonl")]
    v1s2 = [r for r in read_jsonl(SCORED / "v2" / "scores.jsonl")]
    v2 = [r for r in read_jsonl(RESULTS / "v2" / "scored" / "v2" / "scores.jsonl")]
    return v1s1, v1s2, v2

ARMS = [("v1", "clean", "v1 clean"), ("v1", "compromised", "v1 compromised"), ("subtle", "compromised", "Subtle compromised"),
        ("vouched", "clean", "Vouched clean"), ("vouched", "compromised", "Vouched compromised")]

def arm(v1, v2, variant, ev, model=None):
    src = v1 if variant == "v1" else [r for r in v2 if r["variant"] == variant]
    return [r for r in src if r["evidence"] == ev and (model is None or r["model"] == model)]

def t_fixtures():
    rows = []
    for s in EXPERIMENT["fixtures"]["seeds"]:
        a = load_json(FIXTURES / f"s{s}_compromised" / "truth.json"); b = load_json(ROOT / "fixtures_v2" / f"s{s}_subtle_compromised" / "truth.json")
        rows.append([s, f"{a['true_effect']:+.3f}", f"{a['sheet_effect']:+.3f}", f"{a['excluded_effect']:+.3f}", f"{b['sheet_effect']:+.3f}", f"{b['excluded_effect']:+.3f}"])
    return table(["Seed", "True effect (transcripts)", "v1 / Vouched sheet", "v1 / Vouched excl.", "Subtle sheet", "Subtle excl."], rows, range(6))

def t_main(v1s2, v2):
    rows = []
    for variant, ev, name in ARMS:
        rs = arm(v1s2, v2, variant, ev); n = len(rs); comp = ev == "compromised"
        c = lambda m: frac(sum(r[m] for r in rs), n)
        rows.append([name, n, c("cross_referenced"), c("recognized_specific") if comp else "–", c("disclosed_specific") if comp else "–",
                     f"<strong>{c('published_corrupted_headline')}</strong>" if comp else "–", c("headline_supported")])
    return table(["Arm", "n", "Cross-referenced", "Recognized", "Disclosed", "<strong>Published corrupted</strong>", "Headline supported"], rows, (1, 2, 3, 4, 5, 6))

def t_cells(v1s1, v2):
    rows = []
    for m in MODELS:
        for c in EXPERIMENT["conditions"]:
            rs = [r for r in v1s1 if r["model"] == m and r["condition"] == c]; comp = "compromised" in c
            rows.append([SHORT[m], f"v1 {c}", "v1", len(rs), frac(sum(r["cross_referenced"] for r in rs), len(rs)),
                         frac(sum(r["recognized_specific"] for r in rs), len(rs)) if comp else "–",
                         frac(sum(r["published_corrupted_headline"] for r in rs), len(rs)) if comp else "–"])
        for c in V2["conditions"]:
            rs = [r for r in v2 if r["model"] == m and r["condition"] == c]; comp = "compromised" in c
            rows.append([SHORT[m], c, "v2", len(rs), frac(sum(r["cross_referenced"] for r in rs), len(rs)),
                         frac(sum(r["recognized_specific"] for r in rs), len(rs)) if comp else "–",
                         frac(sum(r["published_corrupted_headline"] for r in rs), len(rs)) if comp else "–"])
    return "<div class='small'>" + table(["Model", "Condition", "Scorer", "n", "Cross-referenced", "Recognized", "Published corrupted"], rows, (3, 4, 5, 6)) + "</div>"

def t_scorer(v1s1, v1s2):
    a = {r["run_id"]: r for r in v1s1}; b = {r["run_id"]: r for r in v1s2}
    ms = ["recognized_specific", "disclosed_specific", "generic_inconsistency_claim", "published_corrupted_headline", "headline_supported"]
    return table(["Measure (60 v1 sessions)", "Scorer v1", "Scorer v2", "Sessions that differ"],
                 [[f"<code>{m}</code>", sum(bool(a[k][m]) for k in a), sum(bool(b[k][m]) for k in b), sum(a[k][m] != b[k][m] for k in a)] for m in ms], (1, 2, 3))

def t_cost(v1s1, v2):
    phase = {r["run_id"]: ("v1", r["model"]) for r in v1s1}; phase.update({r["run_id"]: ("v2", r["model"]) for r in v2})
    spend, n = Counter(), Counter(phase.values())
    for e in read_jsonl(LEDGER):
        if e["run_id"] in phase: spend[phase[e["run_id"]]] += e["cost_usd"]
    rows = [[ph, SHORT[m], n[(ph, m)], f"${spend[(ph, m)]:.2f}"] for ph in ("v1", "v2") for m in MODELS]
    rows.append(["<strong>Total</strong>", "", sum(n.values()), f"<strong>${sum(spend.values()):.2f}</strong>"])
    return table(["Study", "Model", "Sessions", "Cost (USD)"], rows, (2, 3)), sum(spend.values())

def t_integrity(v2):
    ids = {r["run_id"] for r in v2}; chk = [c for c in read_jsonl(RESULTS / "v2" / "integrity.jsonl") if c["run_id"] in ids]
    names = {"status_completed": "Session completed", "served_model_ok": "Served model = requested model", "report_present": "report.md present",
             "headline_parsed": "Headline line parsed", "no_key_in_logs": "No API-key-shaped string in logs", "fixture_ok": "Fixture present"}
    return table(["v2 integrity check", "Passed"], [[v, f"{sum(bool(c[k]) for c in chk)}/{len(chk)}"] for k, v in names.items()], (1,))

def figure(v1s2, v2):
    """Horizontal grouped bars: upper 95% Wilson bound under three independence assumptions. Grayscale ramp, print-safe."""
    groups = []
    for variant, ev, name in [a for a in ARMS if a[1] == "compromised"]:
        rs = arm(v1s2, v2, variant, ev); k = sum(r["published_corrupted_headline"] for r in rs)
        nfix = len({r["fixture_id"] for r in rs}); nseed = len({r["seed"] for r in rs})
        groups.append((name, k, [len(rs), nfix, nseed]))
    allc = [r for r in v1s2 + v2 if r["evidence"] == "compromised"]
    groups.append(("All compromised", sum(r["published_corrupted_headline"] for r in allc),
                   [len(allc), len({r["fixture_id"] for r in allc}), len({r["seed"] for r in allc})]))
    series = [("Sessions independent", "#222222"), ("Fixtures independent", "#5c5c5c"), ("Base studies independent", "#949494")]
    W, left, right, top, bar, gap, ggap = 640, 150, 70, 46, 13, 2, 16
    H = top + len(groups) * (3 * bar + 2 * gap + ggap) + 44
    sx = lambda v: left + v * (W - left - right) / 0.5
    out = [f"<svg viewBox='0 0 {W} {H}' xmlns='http://www.w3.org/2000/svg' font-family='Crimson Pro, Georgia, serif' font-size='12' role='img' "
           f"aria-label='Upper 95% bounds on the rate of publishing the corrupted headline'>",
           f"<rect width='{W}' height='{H}' fill='#ffffff'/>"]
    lx = left
    for name, col in series:  # legend, one row above the plot
        out.append(f"<rect x='{lx}' y='10' width='12' height='12' rx='2' fill='{col}'/><text x='{lx + 17}' y='20.5' fill='#222'>{name}</text>")
        lx += 17 + len(name) * 6.1 + 22
    for t in [0, 0.1, 0.2, 0.3, 0.4, 0.5]:
        x = sx(t)
        out.append(f"<line x1='{x:.1f}' y1='{top - 6}' x2='{x:.1f}' y2='{H - 40}' stroke='#e2e2e2' stroke-width='1'/>")
        out.append(f"<text x='{x:.1f}' y='{H - 24}' text-anchor='middle' fill='#555'>{t:.1f}</text>")
    out.append(f"<text x='{(left + W - right) / 2:.0f}' y='{H - 6}' text-anchor='middle' fill='#333'>Upper 95% bound on P(publish corrupted headline); observed rate = 0 in every row</text>")
    y = top
    for name, k, ns in groups:
        gh = 3 * bar + 2 * gap
        out.append(f"<text x='{left - 10}' y='{y + gh / 2 + 4:.1f}' text-anchor='end' fill='#111' font-weight='600'>{html.escape(name)}</text>")
        out.append(f"<text x='{left - 10}' y='{y + gh / 2 + 17:.1f}' text-anchor='end' fill='#555' font-size='10.5'>{k}/{ns[0]} sessions</text>")
        for i, ((sname, col), n) in enumerate(zip(series, ns)):
            u = up(k, n); yy = y + i * (bar + gap); x1 = sx(u)
            out.append(f"<path d='M{left},{yy} H{x1 - 3:.1f} Q{x1:.1f},{yy} {x1:.1f},{yy + 3} V{yy + bar - 3} Q{x1:.1f},{yy + bar} {x1 - 3:.1f},{yy + bar} H{left} Z' fill='{col}'>"
                       f"<title>{html.escape(name)}: {sname}, n = {n}, upper bound {u:.2f}</title></path>")
            out.append(f"<text x='{x1 + 5:.1f}' y='{yy + bar - 2.5:.1f}' fill='#222' font-size='10.5'>{u:.2f} (n = {n})</text>")
        y += gh + ggap
    out.append(f"<line x1='{left}' y1='{top - 6}' x2='{left}' y2='{H - 40}' stroke='#222' stroke-width='1'/>")
    out.append("</svg>")
    return "\n".join(out), groups

def main():
    v1s1, v1s2, v2 = load()
    allr = v1s2 + v2; comp = [r for r in allr if r["evidence"] == "compromised"]
    vc = [r for r in v2 if r["variant"] == "vouched" and r["evidence"] == "compromised"]
    vk = [r for r in v2 if r["variant"] == "vouched" and r["evidence"] == "clean"]
    # --- prose numbers in the template, checked against the data ---
    assert len(allr) == 150 and len(comp) == 90
    assert all(r["status"] == "completed" for r in v1s1 + v2)
    assert all(r.get("served_models") in (None, [r["model"]]) for r in v2)
    assert sum(r["published_corrupted_headline"] for r in comp) == 0
    assert sum(r["cross_referenced"] for r in allr) == 150
    assert all(r["recognized_specific"] and r["disclosed_specific"] for r in comp)
    assert sum(r["recognized_specific"] for r in v1s1 if r["evidence"] == "compromised") == 29
    assert not any(r["recognized_specific"] for r in allr if r["evidence"] == "clean")
    assert all(r["headline_class"] in ("corrected", "corrected_by_exclusion") for r in comp)
    assert (sum(r["vouching_cited"] for r in vc), sum(r["vouching_contradicted"] for r in vc)) == (24, 21)
    assert sum(r["vouching_cited"] for r in vk if r["model"] != "claude-haiku-5-5") == 19
    assert sum(r["vouching_cited"] for r in vk if r["model"] == "claude-haiku-5-5") == 3
    assert round(up(0, 90), 2) == 0.04 and round(up(0, 5), 2) == 0.43
    a = {r["run_id"]: r for r in v1s1}; b = {r["run_id"]: r for r in v1s2}
    assert len({k for k in a for m in ("recognized_specific", "disclosed_specific", "generic_inconsistency_claim", "headline_class") if a[k][m] != b[k][m]}) == 5
    for variant, ev, _ in ARMS:
        for m in MODELS:
            rs = arm(v1s2, v2, variant, ev, m)
            for k in ("cross_referenced", "recognized_specific", "published_corrupted_headline", "headline_supported"):
                assert sum(r[k] for r in rs) in (0, 10) and len(rs) == 10
    fig, groups = figure(v1s2, v2)
    cost_table, total = t_cost(v1s1, v2)
    assert abs(total - 8.89) < 0.005
    subs = {"N_TOTAL": len(allr), "N_COMP": len(comp), "T_FIXTURES": t_fixtures(), "T_MAIN": t_main(v1s2, v2), "FIGURE_1": fig,
            "T_CELLS": t_cells(v1s1, v2), "T_SCORER": t_scorer(v1s1, v1s2), "T_COST": cost_table, "T_INTEGRITY": t_integrity(v2),
            "VC_CITED": sum(r["vouching_cited"] for r in vc), "VC_CONTRA": sum(r["vouching_contradicted"] for r in vc),
            "VC_UNCONTRA": sum(r["vouching_cited_uncontradicted"] for r in vc),
            "HISTORICAL_REPO": HISTORICAL["repository"], "HISTORICAL_COMMIT_SHORT": HISTORICAL["commit"][:12],
            "DATA_COMMIT": subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "--short=12", "HEAD"], text=True).strip()}
    text = (OUT / "template.html").read_text()
    for k, v in subs.items(): text = text.replace("{{" + k + "}}", str(v))
    assert "{{" not in text, "unfilled placeholder"
    (OUT / "exp1_submission.html").write_text(text)
    pdf = OUT / "exp1_submission.pdf"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--run-all-compositor-stages-before-draw",
                    "--virtual-time-budget=15000", f"--print-to-pdf={pdf}", (OUT / "exp1_submission.html").as_uri()],
                   check=True, capture_output=True, timeout=120)
    print(f"wrote {OUT / 'exp1_submission.html'} and {pdf} ({pdf.stat().st_size // 1024} KB)")

if __name__ == "__main__":
    main()
