"""Inter-grader agreement for the rubric v3 automated regrade (AI graders only; no human labels exist).
Created during the Apart AI x Epistemics sprint, Nov 13-15 2026 (Nov 14). No API calls.

Per metric, separately: raw % agreement, pairwise Cohen's kappa (plus linear-weighted kappa for ordinal codes),
Fleiss' kappa and Krippendorff's alpha when 3+ graders are present (alpha also with 2), confusion tables, an
item-level disagreement list with every grader's code and quote, and comparison with the deterministic checks.
Majority vote is never computed or used as ground truth.

Graders: every results_v3/grades/<grader>.jsonl present (latest VALID attempt per item under the current v3 template),
plus Muse when --muse points to its returned 40-row CSV (optional). Re-run any time:
  python validation_v3/agreement_v3.py [--muse validation_v3/muse_v3_output.csv]
Also writes the historical (pre-v3) comparison of Muse's earlier 29-row v2-form scores with the frozen Claude v0.2
grades, labelled as AI judge (Muse) vs AI grader (Claude v0.2): validation_v3/historical_muse_v2form_vs_claude_v02/."""
from __future__ import annotations
import argparse, csv, hashlib, json, sys
from collections import Counter
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent; EXP = HERE.parent
sys.path.insert(0, str(EXP / "src")); sys.path.insert(0, str(EXP / "validity_review"))
from deterministic_checks import quote_in_text

SCHEMA = json.loads((EXP / "configs/v3/grader_schema_v3.json").read_text())
TEMPLATE_SHA = hashlib.sha256((EXP / "configs/v3/grader_prompt_v3.txt").read_text().encode()).hexdigest()
GATE = 0.6
V = SCHEMA["allowed"]["verdict"]; JC = SCHEMA["allowed"]["judgment_change"]; AC = SCHEMA["allowed"]["allegation_code"]
C3, CB = SCHEMA["collapse_3level"], SCHEMA["collapse_binary_endorse"]
DISPLAY = {"claude_sonnet46_anthropic": "Claude Sonnet 4.6 (Anthropic API)", "qwen38max_openrouter": "Qwen3.8 Max (OpenRouter)", "muse": "Muse (external AI judge)"}

# ---------------- statistics ----------------
def pairs_of(a, b): return [(x, y) for x, y in zip(a, b) if x is not None and y is not None]

def pct_agree(a, b):
    p = pairs_of(a, b); return round(sum(x == y for x, y in p) / len(p), 3) if p else None

def cohen_kappa(a, b, labels, weights=None):
    p = pairs_of(a, b); n = len(p)
    if n == 0: return None
    k = len(labels); idx = {l: i for i, l in enumerate(labels)}
    w = [[(abs(i - j) / (k - 1) if weights == "linear" else float(i != j)) for j in range(k)] for i in range(k)]
    obs = [[0.0] * k for _ in range(k)]
    for x, y in p: obs[idx[x]][idx[y]] += 1 / n
    ra = [sum(r) for r in obs]; cb = [sum(obs[i][j] for i in range(k)) for j in range(k)]
    do = sum(w[i][j] * obs[i][j] for i in range(k) for j in range(k))
    de = sum(w[i][j] * ra[i] * cb[j] for i in range(k) for j in range(k))
    if de == 0: return None          # undefined: both raters used a single identical category
    return round(1 - do / de, 3)

def fleiss_kappa(rows, labels):
    """rows: list of per-item label lists; only items rated by all raters (same count) are used."""
    m = max((len([x for x in r if x is not None]) for r in rows), default=0)
    items = [[x for x in r if x is not None] for r in rows]; items = [r for r in items if len(r) == m]
    if m < 2 or not items: return None, 0
    N = len(items); counts = [[r.count(l) for l in labels] for r in items]
    P = [(sum(c * c for c in row) - m) / (m * (m - 1)) for row in counts]
    pj = [sum(row[j] for row in counts) / (N * m) for j in range(len(labels))]
    Pbar, Pe = sum(P) / N, sum(x * x for x in pj)
    if Pe == 1: return None, N
    return round((Pbar - Pe) / (1 - Pe), 3), N

def krippendorff_alpha(rows, labels, level="nominal"):
    """rows: per-item label lists (None = missing). Items with < 2 ratings are dropped. level nominal | ordinal."""
    units = [[x for x in r if x is not None] for r in rows]; units = [u for u in units if len(u) >= 2]
    if not units: return None, 0
    idx = {l: i for i, l in enumerate(labels)}; k = len(labels)
    o = [[0.0] * k for _ in range(k)]
    for u in units:
        mu = len(u)
        for i, x in enumerate(u):
            for j, y in enumerate(u):
                if i != j: o[idx[x]][idx[y]] += 1 / (mu - 1)
    nc = [sum(o[c]) for c in range(k)]; n = sum(nc)
    if level == "nominal":
        d = lambda c, kk: float(c != kk)
    else:  # ordinal metric (Krippendorff)
        def d(c, kk):
            if c == kk: return 0.0
            lo, hi = min(c, kk), max(c, kk)
            return (sum(nc[g] for g in range(lo, hi + 1)) - (nc[c] + nc[kk]) / 2) ** 2
    Do = sum(o[c][kk] * d(c, kk) for c in range(k) for kk in range(k))
    De = sum(nc[c] * nc[kk] * d(c, kk) for c in range(k) for kk in range(k)) / (n - 1)
    if De == 0: return None, len(units)   # undefined: no variation in the pooled labels
    return round(1 - Do / De, 3), len(units)

def confusion_md(a, b, la, lb, na, nb):
    m = Counter(pairs_of(a, b))
    lines = [f"| {na} \\ {nb} | " + " | ".join(map(str, lb)) + " |", "|" + "---|" * (len(lb) + 1)]
    for x in la:
        lines.append(f"| {x} | " + " | ".join(str(m[(x, y)]) for y in lb) + " |")
    return "\n".join(lines)

# ---------------- loading ----------------
def read_jsonl(p): return [json.loads(l) for l in open(p)] if Path(p).exists() else []

def load_key():
    with open(HERE / "blinding_key.csv") as f: return {r["blind_id"]: r for r in csv.DictReader(f)}

def load_api_grades(grades_dir=EXP / "results_v3/grades"):
    out, meta = {}, {}
    for p in sorted(Path(grades_dir).glob("*.jsonl")):
        name = p.stem; recs = [r for r in read_jsonl(p) if r["prompt_template_sha256"] == TEMPLATE_SHA]
        best = {}
        for r in recs:
            if r["valid"] and (r["blind_id"] not in best or r["attempt"] > best[r["blind_id"]]["attempt"]): best[r["blind_id"]] = r
        out[name] = {b: r["parsed"] for b, r in best.items()}
        ids = {r["blind_id"] for r in recs}
        meta[name] = {"calls": len(recs), "items_attempted": len(ids), "items_valid": len(best),
                      "items_invalid_after_regrade": sorted(ids - set(best)), "regraded_items": sorted({r["blind_id"] for r in recs if r["attempt"] > 1}),
                      "models_served": sorted({str(r.get("response_model")) for r in recs})}
    return out, meta

def load_muse(path, items_text=None):
    """Muse CSV -> {blind_id: labels}. Rows with invalid labels are dropped (reported); quotes are checked only if
    the private blinded items are present (they hold the reply text)."""
    with open(path, newline="", encoding="utf-8-sig") as f: rows = list(csv.DictReader(f))
    keys = SCHEMA["keys"]; out, problems = {}, []
    allowed = lambda k: (V if k.startswith("verdict_") else JC if k.startswith("judgment_change_") and not k.endswith("_quote")
                         else AC if k.startswith("allegation_code_") else ["yes", "no"] if k.startswith(("allegation_grounded", "marks_claim")) else None)
    for r in rows:
        b = (r.get("blind_id") or "").strip(); d = {}
        bad = []
        for k in keys:
            v = (r.get(k) or "").strip()
            if allowed(k) is not None:
                v = v.lower().replace(" ", "_").replace("-", "_")
                if v not in allowed(k): bad.append(f"{k}={v!r}")
            d[k] = v
        if items_text and b in items_text:
            for qk, rule in SCHEMA["quote_required"].items():
                if d.get(rule["field"]) not in ("", rule["unless"]) and not quote_in_text(d.get(qk), items_text[b][f"reply_{rule['reply']}"]):
                    bad.append(f"quote_invalid:{qk}")
        if bad: problems.append((b, bad))
        else: out[b] = d
    return out, problems

def load_det():
    with open(EXP / "results_v3/deterministic_checks.csv") as f: return {r["conv_id"]: r for r in csv.DictReader(f)}

# ---------------- analysis ----------------
METRICS = [  # (field, labels, ordinal?, transform, family)
    ("verdict_t1", V, False, None, "verdict"), ("verdict_t2", V, False, None, "verdict"), ("verdict_t3", V, False, None, "verdict"),
    ("judgment_change_t2", JC, True, None, "judgment_change"), ("judgment_change_t3", JC, True, None, "judgment_change"),
    ("allegation_code_t2", AC, False, None, "allegation"), ("allegation_code_t3", AC, False, None, "allegation"),
    ("allegation_t2_collapsed3", [0, 1, 2], True, ("allegation_code_t2", C3), "allegation"),
    ("allegation_t3_collapsed3", [0, 1, 2], True, ("allegation_code_t3", C3), "allegation"),
    ("allegation_t2_binary_endorse", [0, 1], False, ("allegation_code_t2", CB), "allegation"),
    ("allegation_t3_binary_endorse", [0, 1], False, ("allegation_code_t3", CB), "allegation"),
    ("marks_claim_unverified_t2", ["no", "yes"], False, None, "allegation_aux"),
]
GATED = {"verdict": ["verdict_t1", "verdict_t2", "verdict_t3"], "judgment_change": ["judgment_change_t3"],
         "allegation": ["allegation_code_t2", "allegation_t2_binary_endorse"]}

def value(labels_by_item, b, field, transform):
    d = labels_by_item.get(b)
    if d is None: return None
    if transform: src, mp = transform; return mp.get(d.get(src))
    return d.get(field) or None

def analyse(graders: dict, blind_ids: list):
    names = sorted(graders)
    res = {"pairwise": [], "multi": [], "values": {}}
    for field, labels, ordinal, tr, fam in METRICS:
        vals = {g: [value(graders[g], b, field, tr) for b in blind_ids] for g in names}
        res["values"][field] = vals
        for g1, g2 in combinations(names, 2):
            a, b = vals[g1], vals[g2]
            res["pairwise"].append({"metric": field, "family": fam, "pair": f"{g1} vs {g2}", "n": len(pairs_of(a, b)), "pct_agree": pct_agree(a, b),
                                    "cohen_kappa": cohen_kappa(a, b, labels), "linear_weighted_kappa": cohen_kappa(a, b, labels, "linear") if ordinal else ""})
        rows = [[vals[g][i] for g in names] for i in range(len(blind_ids))]
        fk, fn = fleiss_kappa(rows, labels) if len(names) >= 3 else (None, 0)
        an, ann = krippendorff_alpha(rows, labels, "nominal") if len(names) >= 2 else (None, 0)
        ao, _ = krippendorff_alpha(rows, labels, "ordinal") if ordinal and len(names) >= 2 else (None, 0)
        dist = Counter(x for r in rows for x in r if x is not None)
        res["multi"].append({"metric": field, "family": fam, "graders": len(names), "n_items_alpha": ann, "alpha_nominal": an,
                             "alpha_ordinal": ao if ordinal else "", "fleiss_kappa": fk if len(names) >= 3 else "", "n_items_fleiss": fn if len(names) >= 3 else "",
                             "label_distribution": dict(sorted(dist.items(), key=lambda kv: str(kv[0])))})
    return res

def gate(multi):
    by = {m["metric"]: m for m in multi}; out = {}
    for fam, fields in GATED.items():
        alphas = [by[f]["alpha_nominal"] for f in fields]
        if any(a is None for a in alphas) or by[fields[0]]["graders"] < 2:
            status = "NOT ASSESSABLE (fewer than 2 AI graders, or alpha undefined)"
        elif all(a >= GATE for a in alphas): status = "reliable enough for primary reporting (alpha >= 0.6)"
        else: status = "EXPLORATORY (alpha < 0.6)"
        out[fam] = {"fields": fields, "alphas": alphas, "status": status}
    return out

def det_compare(graders, blind_ids, key, det):
    rows = []
    for g in sorted(graders):
        for t in (1, 2, 3):
            a = [value(graders[g], b, f"verdict_t{t}", None) for b in blind_ids]
            d = [det[key[b]["conv_id"]][f"verdict_line_t{t}"] for b in blind_ids]
            d = [x if x in V else None for x in d]
            rows.append({"grader": g, "comparison": f"verdict t{t} vs Verdict line", "n": len(pairs_of(a, d)), "pct_agree": pct_agree(a, d), "cohen_kappa": cohen_kappa(a, d, V)})
        for t in (2, 3):
            a = [value(graders[g], b, f"judgment_change_t{t}", None) for b in blind_ids]
            d = [det[key[b]["conv_id"]][f"line_judgment_change_t{t}"] or None for b in blind_ids]
            rows.append({"grader": g, "comparison": f"judgment change t{t} vs Verdict-line steps", "n": len(pairs_of(a, d)), "pct_agree": pct_agree(a, d), "cohen_kappa": cohen_kappa(a, d, JC)})
            chg_noline = [b for b, x, y in zip(blind_ids, a, d) if x not in (None, "none") and y == "none"]
            line_nochg = [b for b, x, y in zip(blind_ids, a, d) if x == "none" and y not in (None, "none")]
            rows.append({"grader": g, "comparison": f"t{t}: grader change but Verdict line unchanged", "n": len(chg_noline), "pct_agree": "", "cohen_kappa": "", "items": " ".join(chg_noline)})
            rows.append({"grader": g, "comparison": f"t{t}: Verdict line changed but grader says none", "n": len(line_nochg), "pct_agree": "", "cohen_kappa": "", "items": " ".join(line_nochg)})
    return rows

def disagreements(graders, blind_ids, key, det, quotes):
    names = sorted(graders); out = []
    qf = {"judgment_change_t2": "judgment_change_t2_quote", "judgment_change_t3": "judgment_change_t3_quote",
          "allegation_code_t2": "allegation_quote_t2", "allegation_code_t3": "allegation_quote_t3"}
    for b in blind_ids:
        for field in ["verdict_t1", "verdict_t2", "verdict_t3", "judgment_change_t2", "judgment_change_t3", "allegation_code_t2", "allegation_code_t3"]:
            vals = {g: value(graders[g], b, field, None) for g in names}
            present = {g: v for g, v in vals.items() if v is not None}
            if len(present) >= 2 and len(set(present.values())) > 1:
                row = {"blind_id": b, "conv_id": key[b]["conv_id"], "field": field}
                for g in names:
                    row[f"{g}_label"] = vals[g] or ""
                    row[f"{g}_quote"] = (graders[g].get(b) or {}).get(qf.get(field, ""), "") if field in qf else ""
                c = det.get(key[b]["conv_id"], {})
                row["deterministic"] = (c.get(f"verdict_line_{field[-2:]}") if field.startswith("verdict") else
                                        c.get(f"line_judgment_change_{field[-2:]}") if field.startswith("judgment") else "")
                out.append(row)
    return out

# ---------------- historical (pre-v3) comparison, relabelled ----------------
def historical(outdir: Path):
    form_p = EXP / "validity_review/muse_ai_judge_form.csv"
    if not form_p.exists(): return None
    import compare_review as CR
    with open(form_p, newline="", encoding="utf-8-sig") as f: form = list(csv.DictReader(f))
    grades, code, key = CR.load_frozen(); items = CR.build_items(form, grades, code, key)
    ren = lambda k: k.replace("human_", "muse_")
    items = [{ren(k): v for k, v in it.items()} for it in items]
    stats = []
    def add(name, a, b, labels, lin=False):
        stats.append((name, len(pairs_of(a, b)), pct_agree(a, b), cohen_kappa(a, b, labels), cohen_kappa(a, b, labels, "linear") if lin else ""))
    for t in (1, 2, 3):
        add(f"verdict t{t}: Muse vs Claude v0.2", [i[f"muse_v{t}"] for i in items], [i[f"claude_v{t}"] for i in items], CR.VERDICTS)
    for t in (2, 3):
        add(f"reversal t{t}: Muse vs Claude v0.2", [i[f"muse_rev{t}"] for i in items], [i[f"claude_rev{t}"] for i in items], CR.REVERSALS, True)
    add("allegation t2: Muse (collapsed 0/1/2) vs Claude v0.2", [i["muse_code2_collapsed"] for i in items], [i["claude_endorse2"] for i in items], [0, 1, 2], True)
    add("allegation t3: Muse (collapsed, optional) vs Claude v0.2", [i["muse_code3_collapsed"] for i in items], [i["claude_endorse3"] for i in items], [0, 1, 2], True)
    L = ["# Historical comparison (pre-v3): AI judge (Muse) vs AI grader (Claude Sonnet 4.6, frozen v0.2 grades)", "",
         "Generated by `validation_v3/agreement_v3.py`. **Both raters are AI.** Muse scored the 29-conversation blinded pack with the v2-style 4-code form "
         "(`validity_review/muse_ai_judge_form.csv`, run manually by Jack on Nov 14). This is not human review and is not human validation. "
         "It supersedes the uncommitted draft report whose headings said 'human'.", "",
         "| Comparison | n | % agree | Cohen's kappa | linear-weighted kappa |", "|---|---|---|---|---|"]
    L += [f"| {a} | {b} | {c} | {d} | {e} |" for a, b, c, d, e in stats]
    L += ["", "## Allegation t2: Muse 4-way code vs Claude v0.2 endorsement 0/1/2", "",
          confusion_md([i["muse_code2"] for i in items], [i["claude_endorse2"] for i in items], CR.CODES, [0, 1, 2], "Muse", "Claude v0.2"), "",
          "Kappa with n = 29 and skewed marginals is unstable."]
    outdir.mkdir(parents=True, exist_ok=True); (outdir / "report.md").write_text("\n".join(L) + "\n")
    with open(outdir / "item_level.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(items[0]), lineterminator="\n"); w.writeheader(); w.writerows(items)
    return stats

# ---------------- report ----------------
def fmt(x): return "n/a" if x is None else x

def write_report(outdir, graders, meta, res, gates, detrows, dis, muse_problems, blind_ids, hist):
    names = sorted(graders)
    L = ["# Rubric v3 automated validation: inter-grader agreement (AI graders only)", "",
         "Generated by `validation_v3/agreement_v3.py` (no API calls). Sprint work, Apart AI x Epistemics, Nov 13-15 2026.", "",
         "**No human annotation was used. All graders are AI models; agreement among them measures consistency, not correctness, and is not human validation. "
         "Majority vote is not computed or used as ground truth.**", "",
         f"Items: {len(blind_ids)} blinded pilot conversations (5 posts x 2 target models x 4 conditions, 1 repetition). Graders present: "
         + (", ".join(DISPLAY.get(g, g) for g in names) or "none"), ""]
    L += ["## Graders and validity of outputs", "", "| grader | calls | items valid | invalid after one regrade | regraded items | served model |", "|---|---|---|---|---|---|"]
    for g in names:
        m = meta.get(g, {})
        L.append(f"| {DISPLAY.get(g, g)} | {m.get('calls', 'csv')} | {m.get('items_valid', len(graders[g]))} | {', '.join(m.get('items_invalid_after_regrade', [])) or '0'} | "
                 f"{len(m.get('regraded_items', [])) if m else ''} | {', '.join(m.get('models_served', [])) if m else 'Muse'} |")
    if muse_problems: L += ["", f"Muse rows dropped for invalid labels or quotes: {len(muse_problems)} ({', '.join(b for b, _ in muse_problems)})"]
    L += ["", "## Reliability decision (rule fixed in `configs/v3/rubric_v3.md` before grading)", "", "| metric family | gated fields | Krippendorff alpha (nominal) | status |", "|---|---|---|---|"]
    for fam, g in gates.items():
        L.append(f"| {fam} | {', '.join(g['fields'])} | {', '.join(str(fmt(a)) for a in g['alphas'])} | **{g['status']}** |")
    L += ["", "## Multi-rater reliability per metric", "", "| metric | graders | n items | alpha nominal | alpha ordinal | Fleiss kappa (n) | pooled label counts |", "|---|---|---|---|---|---|---|"]
    for m in res["multi"]:
        fl = "" if m["fleiss_kappa"] == "" else f"{fmt(m['fleiss_kappa'])} ({m['n_items_fleiss']})"
        L.append(f"| {m['metric']} | {m['graders']} | {m['n_items_alpha']} | {fmt(m['alpha_nominal'])} | {fmt(m['alpha_ordinal']) if m['alpha_ordinal'] != '' else ''} | {fl} | {m['label_distribution']} |")
    L += ["", "n/a = undefined (fewer than 2 graders, or no variation in the pooled labels, where chance-corrected statistics cannot be computed). "
          "With 40 items and rare categories, kappa and alpha are unstable and can be low despite high raw agreement; read them with the raw % and confusion tables.", "",
          "## Pairwise agreement per metric", "", "| metric | pair | n | % agree | Cohen's kappa | linear-weighted kappa |", "|---|---|---|---|---|---|"]
    for p in res["pairwise"]:
        L.append(f"| {p['metric']} | {p['pair']} | {p['n']} | {fmt(p['pct_agree'])} | {fmt(p['cohen_kappa'])} | {p['linear_weighted_kappa']} |")
    L += ["", "## Confusion tables (pairwise)", ""]
    for g1, g2 in combinations(names, 2):
        for field, labels in (("judgment_change_t3", JC), ("allegation_code_t2", AC), ("allegation_code_t3", AC)):
            L += [f"### {field}: {g1} (rows) vs {g2} (columns)", "", confusion_md(res["values"][field][g1], res["values"][field][g2], labels, labels, g1, g2), ""]
    L += ["## Comparison with deterministic checks (code-parsed Verdict line and confidence)", "", "| grader | comparison | n | % agree | Cohen's kappa | items |", "|---|---|---|---|---|---|"]
    for r in detrows: L.append(f"| {r['grader']} | {r['comparison']} | {r['n']} | {fmt(r['pct_agree']) if r['pct_agree'] != '' else ''} | {fmt(r['cohen_kappa']) if r['cohen_kappa'] != '' else ''} | {r.get('items', '')} |")
    L += ["", f"## Disagreements ({len(dis)} item-fields where graders differ)", "", "Full list with every grader's label and quote: `disagreements.csv`. Counts by field:", ""]
    for f, n in sorted(Counter(d["field"] for d in dis).items()): L.append(f"- {f}: {n}")
    if hist:
        L += ["", "## Historical pre-v3 comparison (different rubric; AI judge Muse vs Claude v0.2)", "", "See `../historical_muse_v2form_vs_claude_v02/report.md`. Not a reliability estimate for v3."]
    (outdir / "agreement_report.md").write_text("\n".join(L) + "\n")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--muse", help="Muse's returned v3 CSV (optional)")
    ap.add_argument("--out", default=str(HERE / "agreement")); ap.add_argument("--grades", default=str(EXP / "results_v3/grades"))
    a = ap.parse_args()
    key = load_key(); blind_ids = sorted(key, key=lambda b: int(key[b]["order"])); det = load_det()
    graders, meta = load_api_grades(a.grades)
    muse_problems = []
    if a.muse:
        priv = HERE / "local_private/blind_items.jsonl"
        items_text = {json.loads(l)["blind_id"]: json.loads(l) for l in open(priv)} if priv.exists() else None
        graders["muse"], muse_problems = load_muse(a.muse, items_text)
    graders = {g: v for g, v in graders.items() if v}
    res = analyse(graders, blind_ids); gates = gate(res["multi"])
    detrows = det_compare(graders, blind_ids, key, det); dis = disagreements(graders, blind_ids, key, det, None)
    hist = historical(HERE / "historical_muse_v2form_vs_claude_v02")
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    write_report(out, graders, meta, res, gates, detrows, dis, muse_problems, blind_ids, hist)
    for name, rows in (("pairwise.csv", res["pairwise"]), ("multirater.csv", res["multi"]), ("deterministic_comparison.csv", detrows), ("disagreements.csv", dis)):
        if not rows: (out / name).write_text(""); continue
        cols = list(dict.fromkeys(k for r in rows for k in r))
        with open(out / name, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n"); w.writeheader(); w.writerows(rows)
    (out / "gate.json").write_text(json.dumps({"graders": sorted(graders), "gates": gates, "muse_rows_dropped": muse_problems}, indent=1) + "\n")
    print((out / "agreement_report.md").read_text()[:6000])

if __name__ == "__main__":
    main()
