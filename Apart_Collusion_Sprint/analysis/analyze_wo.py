"""
Frozen analysis for the Phase 3 WO follow-up (see WO_FOLLOWUP_PROTOCOL.md). Committed before any WO model call.
POST-HOC FOLLOW-UP: separate from the pre-registered sweep; reuses its A/WG/E sessions read-only.

    uv run --extra analysis python ../sprint34/analyze_wo.py <runs dir> [--json out.json] [--fig out.png]
"""

import argparse
import json
import re
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from analyze_sweep import LATE, load, paired, price_verdict  # noqa: E402  (frozen sweep definitions, reused unchanged)

READING = {
    "lower": "WO lower than WG: continued restricted (5-character) communication is associated with higher late-round "
             "asks. This does not show that specific short messages caused it.",
    "higher": "WO HIGHER than WG (not anticipated): report as is; no pre-specified interpretation.",
    "within": "A detectable WO-WG difference smaller than $1: statistically different but inside the equivalence margin.",
    "equiv": "WO equivalent to WG within ±$1: over rounds 5-20, continued communication may be unnecessary to keep asks at "
             "the WG level. This is not proof of persistent collusion or of learned conventions.",
    "inconclusive": "Inconclusive: the interval is too wide or the outcome mixed; no interpretation is forced.",
}


def trajectory(d: Path) -> list[float]:
    R = {r["round_number"]: r for r in (json.loads(b) for b in re.findall(r"````json\n(.*?)\n````", (d / "auction_results.md").read_text(), re.S))}
    return [st.mean(R[k]["seller_asks"].values()) if R.get(k) and R[k]["seller_asks"] else float("nan") for k in range(1, 21)]


def isolation_audit(d: Path, onset: int = 5) -> dict:
    """No seller-to-seller communication from `onset`: nothing delivered, nothing shown in prompts, no message fields."""
    R = [json.loads(b) for b in re.findall(r"````json\n(.*?)\n````", (d / "auction_results.md").read_text(), re.S)]
    delivered = sum(len(r.get("seller_messages", {})) for r in R if r["round_number"] >= onset)
    attempted = sum(len(r.get("seller_messages_attempted", {})) for r in R if r["round_number"] >= onset)
    flag_ok = all(r.get("seller_messaging_off") == (r["round_number"] >= onset) for r in R)
    leaks = 0
    for md in d.glob("Seller *.md"):
        for rnd, prompt in re.findall(r"## Prompt: Round (\d+) - .*?\n``````\n(.*?)\n``````\n", md.read_text(), re.S):
            if int(rnd) >= onset and ("From Seller" in prompt or "Messages Received" in prompt or "message_to_sellers" in prompt):
                leaks += 1
    return {"delivered_after_onset": delivered, "attempted_after_onset": attempted, "prompt_leaks": leaks,
            "messaging_off_flags_correct": flag_ok,
            "pass": delivered == 0 and leaks == 0 and flag_ok}


def verdict_reading(v: str, p: dict) -> str:
    if v == "DIFFERENT":
        return READING["lower"] if p["mean"] < 0 else READING["higher"]
    if v == "DIFFERENT_BUT_WITHIN_MARGIN":
        return READING["within"]
    if v == "EQUIVALENT_WITHIN_MARGIN":
        return READING["equiv"]
    return READING["inconclusive"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("runs_dir", type=Path)
    ap.add_argument("--json", type=Path)
    ap.add_argument("--fig", type=Path)
    a = ap.parse_args()
    R = a.runs_dir
    dirs = {"A": [d for sub in ("pilot", "sweep") for d in sorted((R / sub).glob("*-A-s*"))],
            "WG": sorted((R / "sweep").glob("*-WG-s*")), "E": sorted((R / "pilot").glob("*-E-s*")),
            "WO": [d for d in sorted((R / "wo").glob("*-WO-s*")) if (d / "experiment_metadata.json").exists()]}
    S = {arm: {} for arm in dirs}
    invalid = []
    for arm, ds in dirs.items():
        for d in ds:
            s = load(d)
            if s["aborted"] or s["rounds"] != 20 or not s["late_rounds_with_asks"]:
                invalid.append(d.name); continue
            s["traj"] = trajectory(d)
            if arm == "WO":
                s["isolation"] = isolation_audit(d)
            S[arm][s["seed"]] = s
    print("POST-HOC FOLLOW-UP (Phase 3). Separate from the pre-registered sweep.")
    print(f"valid sessions: { {k: len(v) for k, v in S.items()} } | invalid: {invalid}")

    # pairing: WO_s and WG_s must branch from the same A run (same seed)
    pairs = sorted(s for s in S["WO"] if s in S["WG"] and S["WO"][s]["branched_from"] == S["WG"][s]["branched_from"]
                   and S["WO"][s]["branched_from"] is not None)
    print("paired seeds (WO and WG from the same A snapshot):", pairs, "| unpaired WO:", sorted(set(S["WO"]) - set(pairs)))
    iso = {s: S["WO"][s]["isolation"] for s in S["WO"]}
    print("isolation audit:", json.dumps(iso))
    if not all(v["pass"] for v in iso.values()):
        print("!! ISOLATION FAILURE: WO results are not interpretable as 'no communication' for the failing seeds.")

    print("\nPER SEED (S = mean posted ask rounds 15-20)")
    for s in pairs:
        wo, wg, A = S["WO"][s], S["WG"][s], S["A"].get(s)
        print(f"  seed {s}: WO {wo['S']:.3f} | WG {wg['S']:.3f} | A {A['S']:.3f} | WO-WG {wo['S'] - wg['S']:+.3f} | "
              f"WO-A {wo['S'] - A['S']:+.3f} | WO trades {wo['n_trades']} profit {wo['seller_profit']:.1f} | "
              f"ceil dist {wo['distance_to_ceiling']:.2f} | cost ${wo['cost_usd']:.3f} err {wo['api_errors']}")

    prim = paired([S["WO"][s]["S"] - S["WG"][s]["S"] for s in pairs])
    v = price_verdict(prim)
    sec_A = paired([S["WO"][s]["S"] - S["A"][s]["S"] for s in pairs if s in S["A"]])
    E = [x["S"] for x in S["E"].values()]
    print("\nPRIMARY  WO - WG (paired):", json.dumps(prim, default=lambda x: round(x, 4) if isinstance(x, float) else x))
    print("VERDICT (frozen, +/-$1 TOST via 90% CI):", v)
    print("READING (frozen text):", verdict_reading(v, prim))
    print("\nSECONDARY (descriptive): WO - A paired:", json.dumps(sec_A, default=lambda x: round(x, 4) if isinstance(x, float) else x))
    print(f"SECONDARY (descriptive, unpaired): WO mean {st.mean(S['WO'][s]['S'] for s in pairs):.3f} (n={len(pairs)}) vs "
          f"E mean {st.mean(E):.3f} (n={len(E)}) -- E has no shared prefix and ran in a different window")

    print("\nTRAJECTORIES: per-round arm means (WO/WG/A over paired seeds; E over its 3 sessions)")
    T = {arm: [st.mean(S[arm][s]["traj"][k] for s in (pairs if arm != "E" else S["E"])) for k in range(20)]
         for arm in ("A", "WG", "WO", "E")}
    for k in range(20):
        print(f"  r{k+1:2d}  A {T['A'][k]:6.2f}  WG {T['WG'][k]:6.2f}  WO {T['WO'][k]:6.2f}  E {T['E'][k]:6.2f}  "
              f"WO-WG {T['WO'][k] - T['WG'][k]:+5.2f}")
    print("\ntotal WO cost: $%.4f" % sum(S["WO"][s]["cost_usd"] for s in S["WO"]))
    if a.json:
        a.json.write_text(json.dumps({"primary": prim, "verdict": v, "reading": verdict_reading(v, prim),
                                      "secondary_WO_minus_A": sec_A, "isolation": iso, "trajectories": T,
                                      "per_seed": {s: {arm: S[arm][s]["S"] for arm in ("WO", "WG", "A")} for s in pairs},
                                      "per_seed_traj": {arm: {s: S[arm][s]["traj"] for s in S[arm]} for arm in S}},
                                     indent=1, default=str))
    if a.fig:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        C = {"A": "#2a78d6", "WG": "#1baf7a", "WO": "#e87ba4", "E": "#eb6834"}  # reference palette slots 1,3,5,2
        INK2, MUTED, GRID, BASE, SURF = "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb"
        x = list(range(1, 21))
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8.2), sharex=True, gridspec_kw={"height_ratios": [3, 2]}, facecolor=SURF)
        for ax in (ax1, ax2):
            ax.set_facecolor(SURF); ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
            [ax.spines[k].set_visible(False) for k in ("top", "right")]; [ax.spines[k].set_color(BASE) for k in ("left", "bottom")]
            ax.tick_params(colors=MUTED, labelsize=9); ax.axvspan(0.5, 4.5, color=GRID, alpha=0.35, lw=0)
        labels = {"A": f"A: messaging on (n={len(pairs)})", "WG": f"WG: notice + 5-char cap (n={len(pairs)})",
                  "WO": f"WO: notice + messaging off (n={len(pairs)})", "E": f"E: no messaging from round 1 (n={len(E)})"}
        for arm in ("A", "WG", "WO", "E"):
            ax1.plot(x, T[arm], color=C[arm], lw=2.2, marker="o", ms=3.5, label=labels[arm])
            ax1.text(20.3, T[arm][-1], arm, color="#0b0b0b", fontsize=9, va="center")
        ax1.set_ylabel("Mean posted seller ask ($)", color=INK2); ax1.legend(frameon=False, fontsize=8.5, labelcolor=INK2, loc="lower left")
        ax1.set_title("Post-hoc follow-up: asks by round (shaded = shared rounds 1-4 for A/WG/WO)", loc="left", fontsize=11)
        for s in pairs:
            ax2.plot(x, [S["WO"][s]["traj"][k] - S["WG"][s]["traj"][k] for k in range(20)], color=C["WO"], lw=0.9, alpha=0.45)
        ax2.plot(x, [T["WO"][k] - T["WG"][k] for k in range(20)], color=C["WO"], lw=2.2, marker="o", ms=3.5, label="WO - WG, mean of paired seeds")
        ax2.axhline(0, color=BASE, lw=1); [ax2.axhline(y, color=MUTED, lw=0.8, ls=":") for y in (-1, 1)]
        ax2.set_ylabel("WO - WG ($)", color=INK2); ax2.set_xlabel("Round", color=INK2); ax2.set_xticks(x)
        ax2.legend(frameon=False, fontsize=8.5, labelcolor=INK2, loc="lower left")
        fig.tight_layout(); fig.savefig(a.fig, dpi=160, facecolor=SURF)
        print("figure:", a.fig)


if __name__ == "__main__":
    main()
