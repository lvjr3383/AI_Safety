"""
Evidence freeze for the sprint report. Recomputes every number used in the paper directly from the saved run logs,
using the same frozen functions as the experiments (analyze_pilot.decide, analyze_sweep.load/paired), and writes:

  paper/evidence/evidence.json        all statistics
  paper/evidence/sessions.csv         one row per session (config, arm, seed, S, late trade price, trades, profit)
  paper/evidence/trajectories.csv     per round, per arm: mean posted ask, sd, n, 95% t-interval
  paper/evidence/quotes.json          verbatim message quotations with locators
  paper/figures/fig1_gpt_trajectories.{png,pdf}
  paper/figures/fig2_ae_across_configs.{png,pdf}

No model calls. Run from sprint-3.4/llm-agent-collusion:
  uv run --extra analysis --extra providers python ../paper/build_evidence.py
"""

import csv
import json
import math
import re
import statistics as st
import sys
from pathlib import Path

from scipy import stats

HERE = Path(__file__).resolve().parent
SPRINT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent / "sprint34"))
from analyze_pilot import decide  # noqa: E402
from analyze_sweep import load, paired  # noqa: E402
from src.continuous_double_auction.evaluation.comm_metrics import COLLECTIVE, classify, has_price_like_number  # noqa: E402

EV, FIG = HERE / "evidence", HERE / "figures"
B = re.compile(r"````json\n(.*?)\n````", re.S)


def rounds_of(d):
    return [json.loads(b) for b in B.findall((d / "auction_results.md").read_text())]


def traj(d):
    R = {r["round_number"]: r for r in rounds_of(d)}
    return [st.mean(R[k]["seller_asks"].values()) if R.get(k) and R[k]["seller_asks"] else float("nan") for k in range(1, 21)]


def sess(pattern_dirs):
    out = {}
    for d in pattern_dirs:
        s = load(d)
        assert not s["aborted"] and s["rounds"] == 20, d
        s["traj"] = traj(d)
        s["dir"] = str(d.relative_to(SPRINT))
        out[s["seed"]] = s
    return out


def welch(a, b):
    ma, mb, va, vb = st.mean(a), st.mean(b), st.variance(a) / len(a), st.variance(b) / len(b)
    df = (va + vb) ** 2 / (va ** 2 / (len(a) - 1) + vb ** 2 / (len(b) - 1))
    h = stats.t.ppf(0.975, df) * math.sqrt(va + vb)
    return {"diff": ma - mb, "ci95": [ma - mb - h, ma - mb + h], "df": df, "nA": len(a), "nB": len(b),
            "meanA": ma, "meanB": mb, "sdA": st.stdev(a), "sdB": st.stdev(b)}


def tci(xs):
    xs = [x for x in xs if x == x]
    m = st.mean(xs)
    if len(xs) < 2:
        return m, float("nan"), float("nan"), len(xs)
    h = stats.t.ppf(0.975, len(xs) - 1) * st.stdev(xs) / math.sqrt(len(xs))
    return m, m - h, m + h, len(xs)


R, RC, RX = SPRINT / "runs", SPRINT / "runs_claude" / "exp", SPRINT / "runs_crossed" / "exp"
G = {"A": sess(sorted(R.glob("pilot/*-A-s*")) + sorted(R.glob("sweep/*-A-s*"))),
     "E": sess(sorted(R.glob("pilot/*-E-s*"))),
     "W": sess(sorted(R.glob("sweep/*-W-s*"))),
     "WG": sess(sorted(R.glob("sweep/*-WG-s*"))),
     "WO": sess(sorted(R.glob("wo/*-WO-s*")))}
C = {"A": sess(sorted(RC.glob("*_p4-A-s*"))), "E": sess(sorted(RC.glob("*_p4-E-s*")))}
X = {"A": sess(sorted(RX.glob("*_x-A-s*"))), "E": sess(sorted(RX.glob("*_x-E-s*")))}
assert [len(G[k]) for k in ("A", "E", "W", "WG", "WO")] == [7, 3, 7, 7, 7] and len(C["A"]) == len(C["E"]) == 5 == len(X["A"]) == len(X["E"])

ev = {}
# ---- GPT-4.1 configuration
pilotA = [G["A"][s]["S"] for s in (0, 1, 2)]
pilotE = [G["E"][s]["S"] for s in (0, 1, 2)]
ev["gpt_pilot_gate_preregistered"] = {"welch": welch(pilotA, pilotE), "rule": decide(pilotA, pilotE, final=False)}
ev["gpt_allA7_vs_E3_posthoc"] = welch([G["A"][s]["S"] for s in sorted(G["A"])], pilotE)
for name, (x, y) in {"W_minus_A": ("W", "A"), "WG_minus_W": ("WG", "W"), "WG_minus_A": ("WG", "A"),
                     "WO_minus_WG": ("WO", "WG"), "WO_minus_A": ("WO", "A")}.items():
    seeds = sorted(set(G[x]) & set(G[y]))
    ev[f"gpt_paired_{name}"] = paired([G[x][s]["S"] - G[y][s]["S"] for s in seeds])
# transaction prices (late rounds), descriptive
ev["gpt_late_trade_price_pilot_A_vs_E"] = welch([G["A"][s]["late_trade_price"] for s in (0, 1, 2)],
                                                [G["E"][s]["late_trade_price"] for s in (0, 1, 2)])
ev["gpt_late_trade_price_allA7_vs_E3"] = welch([G["A"][s]["late_trade_price"] for s in sorted(G["A"])],
                                               [G["E"][s]["late_trade_price"] for s in (0, 1, 2)])
# post-round-4 movement (stickiness): S minus round-4 mean ask, every prefix-sharing session
ev["gpt_move_after_r4"] = {arm: {s: G[arm][s]["S"] - G[arm][s]["traj"][3] for s in sorted(G[arm])} for arm in G}
# ---- Claude configurations
for tag, D in (("claude_sonnet_haiku", C), ("claude_sonnet_gpt41mini_buyers", X)):
    a = [D["A"][s]["S"] for s in sorted(D["A"])]
    e = [D["E"][s]["S"] for s in sorted(D["E"])]
    ev[f"{tag}_A_vs_E"] = {"welch": welch(a, e), "rule": decide(a, e, final=True),
                           "seed_paired": paired([D["A"][s]["S"] - D["E"][s]["S"] for s in sorted(D["A"])])}
    ev[f"{tag}_late_trade_price_A_vs_E"] = welch([D["A"][s]["late_trade_price"] for s in sorted(D["A"])],
                                                 [D["E"][s]["late_trade_price"] for s in sorted(D["E"])])
# Claude gate note: Phase 4 gate used seeds 0-4 at n=5 with final=False semantics; recompute exactly as run
ev["claude_sonnet_haiku_gate_as_run"] = decide([C["A"][s]["S"] for s in range(5)], [C["E"][s]["S"] for s in range(5)], final=False)

# ---- message evidence (GPT, pre-registered classifier) and Claude (exploratory, classifier not validated for Claude)
def msg_counts(D, arm, first=5):
    n = prop = 0
    for s in D[arm].values():
        for r in rounds_of(SPRINT / s["dir"]):
            if r["round_number"] >= first:
                for m in r.get("seller_messages_raw", {}).values():
                    c = classify(m).category
                    if c != "EMPTY":
                        n += 1
                        prop += c == "PRICE_PROPOSAL"
    return {"messages": n, "price_proposals": prop}


ev["gpt_messages_rounds5_20"] = {arm: msg_counts(G, arm) for arm in ("A", "W", "WG")}


def coord_language(D):
    n = both = 0
    for s in D["A"].values():
        for r in rounds_of(SPRINT / s["dir"]):
            for m in r.get("seller_messages_raw", {}).values():
                if m and m.strip():
                    n += 1
                    both += bool(COLLECTIVE.search(m)) and has_price_like_number(m)
    return {"messages_all_rounds": n, "group_language_and_price_number": both}


ev["exploratory_coordination_language_A"] = {"gpt": coord_language(G), "claude_sonnet_haiku": coord_language(C),
                                             "claude_sonnet_gpt41mini_buyers": coord_language(X)}

# ---- costs and call integrity from ledgers
def ledger(p):
    U = [json.loads(l) for l in open(p)]
    return {"records": len(U), "cost_usd": sum(u.get("cost_usd") or 0 for u in U), "errors": sum(1 for u in U if u.get("error")),
            "refusals": sum(1 for u in U if u.get("stop_reason") == "refusal")}


ev["ledgers"] = {"openrouter_project": ledger(R / "spend_ledger.jsonl"), "anthropic_phase4": ledger(SPRINT / "runs_claude" / "spend_ledger.jsonl"),
                 "crossed": ledger(SPRINT / "runs_crossed" / "spend_ledger.jsonl")}

# ---- tables
EV.mkdir(exist_ok=True)
with open(EV / "sessions.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["config", "arm", "seed", "S_late_mean_ask", "ask_round4", "late_trade_price", "n_trades", "seller_profit", "dir"])
    for cfg, D in (("GPT-4.1 x GPT-4.1-mini", G), ("Sonnet 5.5 x Haiku 5.5", C), ("Sonnet 5.5 x GPT-4.1-mini", X)):
        for arm, ss in D.items():
            for seed, s in sorted(ss.items()):
                w.writerow([cfg, arm, seed, f"{s['S']:.4f}", f"{s['traj'][3]:.4f}", f"{s['late_trade_price']:.4f}",
                            s["n_trades"], f"{s['seller_profit']:.2f}", s["dir"]])
traj_rows = []
with open(EV / "trajectories.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["config", "arm", "round", "mean_ask", "ci95_lo", "ci95_hi", "n_sessions"])
    for cfg, D in (("GPT-4.1 x GPT-4.1-mini", G), ("Sonnet 5.5 x Haiku 5.5", C), ("Sonnet 5.5 x GPT-4.1-mini", X)):
        for arm, ss in D.items():
            for k in range(20):
                m, lo, hi, n = tci([s["traj"][k] for s in ss.values()])
                w.writerow([cfg, arm, k + 1, f"{m:.4f}", f"{lo:.4f}", f"{hi:.4f}", n])

# ---- verbatim quotations (locator = run dir, round, seller); text read from the log, never typed by hand
QUOTES = [
    ("GPT-4.1 x GPT-4.1-mini", "A", G["A"][3]["dir"], 8, "Seller Jin", "seller_messages_raw"),
    ("GPT-4.1 x GPT-4.1-mini", "W", G["W"][3]["dir"], 8, "Seller Jin", "seller_messages_raw"),
    ("GPT-4.1 x GPT-4.1-mini", "WG", G["WG"][2]["dir"], 6, None, "seller_messages"),
    ("GPT-4.1 x GPT-4.1-mini", "WG", G["WG"][4]["dir"], 6, None, "seller_messages"),
    ("Sonnet 5.5 x Haiku 5.5", "A", C["A"][0]["dir"], 3, "Seller Leo", "seller_messages_raw"),
    ("Sonnet 5.5 x Haiku 5.5", "A", C["A"][0]["dir"], 13, "Seller Kai", "seller_messages_raw"),
    ("Sonnet 5.5 x GPT-4.1-mini", "A", X["A"][0]["dir"], 3, None, "seller_messages_raw"),
]
quotes = []
for cfg, arm, d, rnd, seller, field in QUOTES:
    r = next(r for r in rounds_of(SPRINT / d) if r["round_number"] == rnd)
    msgs = r[field]
    sid = seller if seller else sorted(msgs)[0]
    quotes.append({"config": cfg, "arm": arm, "seed": int(d.rsplit("-s", 1)[1]), "round": rnd, "seller": sid,
                   "field": field, "source": f"{d}/auction_results.md", "text": msgs[sid],
                   "all_delivered_this_round": msgs if field == "seller_messages" else None})
(EV / "quotes.json").write_text(json.dumps(quotes, indent=1, ensure_ascii=False))
with open(HERE / "QUOTES.md", "w", encoding="utf-8") as f:  # generated: never edit by hand
    f.write("# Verified Message Quotations (generated by build_evidence.py from the logs; do not edit by hand)\n\n"
            "Text is copied byte-for-byte from the named log file, including the agents' own typographic apostrophes "
            "and dashes. Paths are relative to AI_Collusion_Research_Sprint/. WG rows list every message delivered "
            "to sellers in that round (the 5-character cap applies).\n\n"
            "| # | Configuration | Arm | Seed | Round | Seller | Text (verbatim) | Source |\n|---|---|---|---|---|---|---|---|\n")
    for i, q in enumerate(quotes, 1):
        text = (", ".join(f'"{m}"' for m in q["all_delivered_this_round"].values()) if q["all_delivered_this_round"]
                else f'"{q["text"]}"')
        seller = "all five" if q["all_delivered_this_round"] else q["seller"]
        f.write(f"| Q{i} | {q['config']} | {q['arm']} | {q['seed']} | {q['round']} | {seller} | {text} | `{q['source']}` |\n")
    f.write("\nQ3 and Q4 (short messages under the cap) are exploratory observations, not evidence of intent.\n")
(EV / "evidence.json").write_text(json.dumps(ev, indent=1, default=lambda v: round(v, 6) if isinstance(v, float) else str(v)))

# ---- figures
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

INK, INK2, MUTED, GRID, BASE, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#ffffff"
COL = {"A": "#2a78d6", "E": "#eb6834", "W": "#1baf7a", "WG": "#eda100", "WO": "#e87ba4"}
LAB = {"A": "A: messaging on", "E": "E: no messaging from round 1", "W": "W: monitoring notice from round 5",
       "WG": "WG: notice + 5-character cap from round 5", "WO": "WO: notice + messaging off from round 5 (post hoc)"}
plt.rcParams.update({"font.size": 9, "axes.edgecolor": BASE, "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED})
x = list(range(1, 21))


def style(ax):
    ax.set_facecolor(SURF); ax.grid(axis="y", color=GRID, lw=0.7); ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 4.9), facecolor=SURF, gridspec_kw={"width_ratios": [1.15, 1]})
for ax in (a1, a2):
    style(ax)
a1.axvspan(0.5, 4.5, color=GRID, alpha=0.45, lw=0)
a1.text(2.5, 98.15, "rounds 1-4: A, W, WG, WO\nshare one history per seed", ha="center", va="top", fontsize=7, color=INK2)
rows = [tci([s["traj"][k] for s in G["A"].values()]) for k in range(20)]
a1.fill_between(x, [r[1] for r in rows], [r[2] for r in rows], color=COL["A"], alpha=0.14, lw=0)
for s in G["E"].values():  # n=3: individual sessions shown instead of a t-band
    a1.plot(x, s["traj"], color=COL["E"], lw=0.8, alpha=0.45)
for arm in ("A", "W", "WG", "WO", "E"):
    m = [st.mean(s["traj"][k] for s in G[arm].values()) for k in range(20)]
    a1.plot(x, m, color=COL[arm], lw=2.0 if arm in ("A", "E") else 1.4, marker="o", ms=2.6,
            label=f"{LAB[arm]} (n={len(G[arm])})")
a1.axvline(4.5, color=MUTED, lw=0.8, ls=":")
a1.set_xticks([1, 4, 5, 8, 12, 15, 20]); a1.set_xlim(0.5, 20.5); a1.set_ylim(91.5, 98.2)
a1.set_xlabel("Round"); a1.set_ylabel("Mean posted seller ask ($)")
a1.set_title("(a) Mean ask by round (band: A, 95% t-interval; thin lines: the 3 E sessions)", loc="left", fontsize=8.5, color=INK)
fig.legend(*a1.get_legend_handles_labels(), frameon=False, fontsize=7.5, loc="lower center", ncol=3, labelcolor=INK2)
# panel b: seed-paired difference from A after the branch point
a2.axhline(0, color=BASE, lw=1)
for y in (-1, 1):
    a2.axhline(y, color=MUTED, lw=0.7, ls=":")
a2.text(5.1, 1.04, "+$1", fontsize=7, color=MUTED, va="bottom"); a2.text(5.1, -0.96, "-$1", fontsize=7, color=MUTED, va="bottom")
for arm in ("W", "WG", "WO"):
    rows = [tci([G[arm][s]["traj"][k] - G["A"][s]["traj"][k] for s in sorted(G[arm])]) for k in range(4, 20)]
    xs = list(range(5, 21))
    a2.fill_between(xs, [r[1] for r in rows], [r[2] for r in rows], color=COL[arm], alpha=0.14, lw=0)
    a2.plot(xs, [r[0] for r in rows], color=COL[arm], lw=1.6, marker="o", ms=2.6, label=f"{arm} - A (n={len(G[arm])} seed pairs)")
a2.set_xticks([5, 8, 12, 15, 20]); a2.set_xlim(4.5, 20.5); a2.set_ylim(-1.35, 1.35)
a2.set_xlabel("Round"); a2.set_ylabel("Difference from A, same seed ($)")
a2.set_title("(b) Same-seed difference from A, rounds 5-20 (95% t-interval)", loc="left", fontsize=8.5, color=INK)
a2.legend(frameon=False, fontsize=7.2, loc="upper right", labelcolor=INK2)
fig.tight_layout(rect=(0, 0.1, 1, 1))
FIG.mkdir(exist_ok=True)
for ext in ("png", "pdf"):
    fig.savefig(FIG / f"fig1_gpt_trajectories.{ext}", dpi=200, facecolor=SURF)

# Figure 1a (Section 3): preregistered pilot only, A vs E, seeds 0-2. Same sample as the +$2.80 estimate.
fig, ax = plt.subplots(figsize=(7.2, 4.2), facecolor=SURF)
style(ax)
for arm in ("A", "E"):
    seeds = (0, 1, 2)
    for sd in seeds:
        ax.plot(x, G[arm][sd]["traj"], color=COL[arm], lw=0.9, alpha=0.4)
    m = [st.mean(G[arm][sd]["traj"][k] for sd in seeds) for k in range(20)]
    lab = "A: sellers can message" if arm == "A" else "E: no seller messaging"
    ax.plot(x, m, color=COL[arm], lw=2.2, marker="o", ms=3, label=f"{lab} (mean of 3 sessions)")
ax.axvspan(14.5, 20.5, color=GRID, alpha=0.45, lw=0)
ax.text(17.5, 97.75, "rounds 15-20:\nprimary outcome window", ha="center", va="top", fontsize=7.5, color=INK2)
ax.set_xticks([1, 5, 10, 15, 20]); ax.set_xlim(0.5, 20.5); ax.set_ylim(91.5, 97.9)
ax.set_xlabel("Round"); ax.set_ylabel("Mean posted seller ask ($)")
ax.legend(frameon=False, fontsize=8, loc="lower left", labelcolor=INK2)
fig.tight_layout()
for ext in ("png", "pdf"):
    fig.savefig(FIG / f"fig1a_gpt_pilot_A_vs_E.{ext}", dpi=200, facecolor=SURF)

# Figure 1b (Section 4): the seven seed pairs that share A's history; E is not included.
fig, (b1, b2) = plt.subplots(1, 2, figsize=(10.5, 4.6), facecolor=SURF, gridspec_kw={"width_ratios": [1.1, 1]})
for ax in (b1, b2):
    style(ax)
b1.axvspan(0.5, 4.5, color=GRID, alpha=0.45, lw=0)
b1.text(2.5, 97.45, "rounds 1-4:\none shared history\nper seed", ha="center", va="top", fontsize=7, color=INK2)
rows = [tci([s["traj"][k] for s in G["A"].values()]) for k in range(20)]
b1.fill_between(x, [r[1] for r in rows], [r[2] for r in rows], color=COL["A"], alpha=0.14, lw=0)
for arm in ("A", "W", "WG", "WO"):
    m = [st.mean(s["traj"][k] for s in G[arm].values()) for k in range(20)]
    b1.plot(x, m, color=COL[arm], lw=2.0 if arm == "A" else 1.5, marker="o", ms=2.6, label=f"{LAB[arm]} (n={len(G[arm])})")
b1.axvline(4.5, color=MUTED, lw=0.8, ls=":")
b1.set_xticks([1, 4, 5, 8, 12, 15, 20]); b1.set_xlim(0.5, 20.5); b1.set_ylim(95.6, 97.5)
b1.set_xlabel("Round"); b1.set_ylabel("Mean posted seller ask ($)")
b1.set_title("(a) Mean ask by round (band: A, 95% t-interval)", loc="left", fontsize=8.5, color=INK)
b2.axhline(0, color=BASE, lw=1)
for yv in (-1, 1):
    b2.axhline(yv, color=MUTED, lw=0.7, ls=":")
b2.text(5.1, 1.04, "+$1", fontsize=7, color=MUTED, va="bottom"); b2.text(5.1, -0.96, "-$1", fontsize=7, color=MUTED, va="bottom")
for arm in ("W", "WG", "WO"):
    rr = [tci([G[arm][sd]["traj"][k] - G["A"][sd]["traj"][k] for sd in sorted(G[arm])]) for k in range(4, 20)]
    xs = list(range(5, 21))
    b2.fill_between(xs, [r[1] for r in rr], [r[2] for r in rr], color=COL[arm], alpha=0.14, lw=0)
    b2.plot(xs, [r[0] for r in rr], color=COL[arm], lw=1.6, marker="o", ms=2.6, label=f"{arm} - A (n={len(G[arm])} seed pairs)")
b2.set_xticks([5, 8, 12, 15, 20]); b2.set_xlim(4.5, 20.5); b2.set_ylim(-1.35, 1.35)
b2.set_xlabel("Round"); b2.set_ylabel("Difference from A, same seed ($)")
b2.set_title("(b) Same-seed difference from A, rounds 5-20 (95% t-interval)", loc="left", fontsize=8.5, color=INK)
b2.legend(frameon=False, fontsize=7.2, loc="upper right", bbox_to_anchor=(1.0, 0.845), labelcolor=INK2)
fig.legend(*b1.get_legend_handles_labels(), frameon=False, fontsize=7.5, loc="lower center", ncol=2, labelcolor=INK2)
fig.tight_layout(rect=(0, 0.11, 1, 1))
for ext in ("png", "pdf"):
    fig.savefig(FIG / f"fig1b_gpt_interventions.{ext}", dpi=200, facecolor=SURF)

# Figure 2
rows = [("GPT-4.1 sellers x GPT-4.1-mini buyers\npre-registered pilot, n=3 vs 3 (Welch)", ev["gpt_pilot_gate_preregistered"]["welch"]),
        ("Sonnet 5.5 sellers x Haiku 5.5 buyers\nfrozen before running, n=5 vs 5 (Welch)", ev["claude_sonnet_haiku_A_vs_E"]["welch"]),
        ("Sonnet 5.5 sellers x GPT-4.1-mini buyers\nfrozen before running, n=5 vs 5 (Welch)", ev["claude_sonnet_gpt41mini_buyers_A_vs_E"]["welch"])]
fig, ax = plt.subplots(figsize=(7.6, 2.9), facecolor=SURF)
style(ax); ax.grid(axis="x", color=GRID, lw=0.7); ax.grid(axis="y", visible=False)
ax.axvline(0, color=BASE, lw=1); ax.axvline(1.5, color=MUTED, lw=0.9, ls="--")
ax.text(1.53, 2.42, "practical threshold +$1.50", fontsize=7, color=MUTED, va="bottom")
for i, (lab, w) in enumerate(rows):
    yy = 2 - i
    ax.plot(w["ci95"], [yy, yy], color=INK2, lw=1.6)
    ax.plot([w["diff"]], [yy], "o", color=COL["A"], ms=7, mec=SURF, mew=1.5)
    ax.text(w["ci95"][1] + 0.15, yy, f"{w['diff']:+.2f}  [{w['ci95'][0]:+.2f}, {w['ci95'][1]:+.2f}]", va="center", fontsize=7.5, color=INK)
ax.set_yticks([2, 1, 0]); ax.set_yticklabels([r[0] for r in rows], fontsize=7.5)
ax.set_ylim(-0.6, 2.6); ax.set_xlim(-4.6, 6.4)
ax.set_xlabel("A - E: late-round mean seller ask, rounds 15-20 ($), point estimate and 95% CI")
fig.tight_layout()
for ext in ("png", "pdf"):
    fig.savefig(FIG / f"fig2_ae_across_configs.{ext}", dpi=200, facecolor=SURF)
print(json.dumps({k: ev[k] for k in ("gpt_pilot_gate_preregistered", "gpt_allA7_vs_E3_posthoc")}, default=lambda v: round(v, 3) if isinstance(v, float) else str(v))[:900])
print("done")
