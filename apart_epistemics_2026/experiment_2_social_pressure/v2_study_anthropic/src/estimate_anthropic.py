"""Full-run cost estimate for the Anthropic-only extension from ACTUAL smoke-test token usage
(Apart AI x Epistemics sprint, Nov 13-15 2026). No API calls.
Per model: mean list-price cost per complete smoke conversation (results/smoke/raw/conversations.jsonl; ledger matches)
x conversations per model x (1 + margin). Sensitivities: every conversation at the most expensive smoke conversation,
and a post-length adjustment (selected-case mean chars / smoke-case mean chars, applied to the whole cost: crude, labelled).
Usage: python v2_study_anthropic/src/estimate_anthropic.py [--cap 50]"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_anthropic as RA

def estimate(cap=50.0, paths=RA.SMOKE):
    st = RA.STUDY; margin = st["budget"]["margin"]
    man = RA.cases(); chars = {c["row_id"]: c["chars"] for c in man}
    n_per_model = len(man) * len(st["conditions"]) * st["repetitions"]
    convs = [c for c in RA.read_jsonl(paths.convs) if c["status"] == "complete"]
    led = RA.read_jsonl(paths.ledger)
    sel_mean = sum(chars.values()) / len(chars)
    out = {"design": {"cases": len(man), "conditions": len(st["conditions"]), "repetitions": st["repetitions"],
                      "models": list(st["targets"]), "conversations_per_model": n_per_model, "conversations_total": n_per_model * len(st["targets"])},
           "basis": "actual smoke-test token usage x list price (official pricing page, see config)", "margin": margin, "models": {}}
    for m in st["targets"]:
        cs = [c for c in convs if c["model"] == m]
        if not cs: out["models"][m] = None; continue
        cost = [c["cost_usd"] for c in cs]; mean = sum(cost) / len(cost)
        tin = [sum(t["input_tokens"] or 0 for t in c["turns"]) for c in cs]; tout = [sum(t["output_tokens"] or 0 for t in c["turns"]) for c in cs]
        smoke_chars = sum(chars[c["row_id"]] for c in cs) / len(cs); adj = sel_mean / smoke_chars
        out["models"][m] = {"smoke_conversations": len(cs), "smoke_cost_usd": round(sum(cost), 6),
                            "smoke_ledger_usd": round(sum(x["cost_usd"] for x in led if x["model"] == m), 6),
                            "mean_cost_per_conv": round(mean, 6), "max_cost_per_conv": round(max(cost), 6),
                            "mean_input_tokens_per_conv": round(sum(tin) / len(tin), 1), "mean_output_tokens_per_conv": round(sum(tout) / len(tout), 1),
                            "base_usd": round(n_per_model * mean, 4), "with_margin_usd": round(n_per_model * mean * (1 + margin), 4),
                            "all_at_smoke_max_usd": round(n_per_model * max(cost), 4),
                            "length_adjustment_factor": round(adj, 4), "length_adjusted_with_margin_usd": round(n_per_model * mean * adj * (1 + margin), 4)}
    ms = [v for v in out["models"].values() if v]
    tot = round(sum(v["with_margin_usd"] for v in ms), 4)
    out["total"] = {"base_usd": round(sum(v["base_usd"] for v in ms), 4), "with_margin_usd": tot,
                    "all_at_smoke_max_usd": round(sum(v["all_at_smoke_max_usd"] for v in ms), 4),
                    "length_adjusted_with_margin_usd": round(sum(v["length_adjusted_with_margin_usd"] for v in ms), 4)}
    out["cap_check"] = {"proposed_cap_usd": cap, "fits_with_margin": tot <= cap, "headroom_usd": round(cap - tot, 4),
                        "note": "Cap applies to the main-run ledger (results/ledger_anthropic.jsonl); the smoke test has its own ledger. "
                                "Anthropic credit balance cannot be read via the API (user-reported $100 promo credits, unverified)."}
    out["post_length_chars"] = {"selected_mean": round(sel_mean, 1)}
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--cap", type=float, default=50.0); a = ap.parse_args()
    e = estimate(a.cap); p = RA.VA / "results/estimate_anthropic.json"; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(e, indent=1) + "\n"); print(json.dumps(e, indent=1))

if __name__ == "__main__":
    main()
