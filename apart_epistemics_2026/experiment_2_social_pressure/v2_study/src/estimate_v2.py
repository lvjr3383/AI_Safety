"""Cost estimate for Experiment 2 v2 from ACTUAL pilot spend (Apart AI x Epistemics sprint, Nov 13-15 2026).
Targets (OpenRouter): mean cost per complete pilot conversation per model (results/raw/conversations.jsonl, which sums
OpenRouter usage.cost; the pilot ledger matches). Optional grader (Anthropic direct, claude-sonnet-4-6): mean cost per
conversation of the v3 regrade (results_v3/ledgers/anthropic.jsonl). Margin from config/study.json.
Usage: python v2_study/src/estimate_v2.py [--balance]   (--balance calls the free OpenRouter /key endpoint)"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from v2_common import V2, EXP, STUDY, load

def rd(p): return [json.loads(l) for l in open(p)] if Path(p).exists() else []

def pilot_per_conversation():
    convs = rd(EXP / "results/raw/conversations.jsonl")
    out = {"mean_complete": {}, "max_complete": {}, "n_complete": {}, "failed_attempt_cost": {}}
    for m in STUDY["targets"]:
        c = [x["cost_usd"] for x in convs if x["model"] == m and x["status"] == "complete"]
        out["mean_complete"][m] = round(sum(c) / len(c), 6); out["max_complete"][m] = round(max(c), 6); out["n_complete"][m] = len(c)
        out["failed_attempt_cost"][m] = round(sum(x["cost_usd"] for x in convs if x["model"] == m and x["status"] != "complete"), 6)
    return out

def grader_per_conversation():
    led = rd(EXP / "results_v3/ledgers/anthropic.jsonl")
    total = sum(x["cost_usd"] for x in led); items = len({x["blind_id"] for x in led})
    return {"total_usd": round(total, 6), "calls": len(led), "conversations": items, "per_conversation": round(total / items, 6)}

def estimate():
    n_cases = len(load(V2 / "config/manifest_v2.json")["cases"]); conds = len(STUDY["conditions"]); reps = STUDY["repetitions"]
    per_model_n = n_cases * conds * reps; margin = STUDY["budget"]["margin"]
    p = pilot_per_conversation(); g = grader_per_conversation()
    sel = [c["chars"] for c in load(V2 / "config/manifest_v2.json")["cases"]]
    pil = [c["chars"] for c in load(EXP / "data/manifest.json")["pilot_cases"]]
    t = {m: {"conversations": per_model_n, "pilot_mean_per_conv": p["mean_complete"][m], "base_usd": round(per_model_n * p["mean_complete"][m], 4),
             "with_margin_usd": round(per_model_n * p["mean_complete"][m] * (1 + margin), 4),
             "worst_observed_per_conv_usd": round(per_model_n * p["max_complete"][m], 4)} for m in STUDY["targets"]}
    n_total = per_model_n * len(STUDY["targets"])
    return {"design": {"cases": n_cases, "conditions": conds, "repetitions": reps, "targets": list(STUDY["targets"]), "conversations": n_total},
            "margin": margin, "pilot_basis": p,
            "post_length_chars": {"selected_mean": round(sum(sel) / len(sel), 1), "pilot_mean": round(sum(pil) / len(pil), 1)},
            "targets_openrouter": {**t, "total_base_usd": round(sum(v["base_usd"] for v in t.values()), 4),
                                   "total_with_margin_usd": round(sum(v["with_margin_usd"] for v in t.values()), 4),
                                   "total_if_every_conv_cost_pilot_max_usd": round(sum(v["worst_observed_per_conv_usd"] for v in t.values()), 4)},
            "optional_grader_anthropic": {"basis": g, "conversations": n_total, "base_usd": round(n_total * g["per_conversation"], 4),
                                          "with_margin_usd": round(n_total * g["per_conversation"] * (1 + margin), 4)}}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--balance", action="store_true"); a = ap.parse_args()
    e = estimate()
    if a.balance:
        sys.path.insert(0, str(EXP / "src")); from common import key_status
        ks = key_status(); e["openrouter_key"] = ks
        need = e["targets_openrouter"]["total_with_margin_usd"]
        e["fit"] = {"available_usd": ks["limit_remaining_usd"], "needed_with_margin_usd": need, "fits": ks["limit_remaining_usd"] >= need,
                    "shortfall_usd": round(max(0.0, need - ks["limit_remaining_usd"]), 2)}
    out = V2 / "results/estimate_v2.json"; out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(e, indent=1) + "\n")
    print(json.dumps(e, indent=1))

if __name__ == "__main__":
    main()
