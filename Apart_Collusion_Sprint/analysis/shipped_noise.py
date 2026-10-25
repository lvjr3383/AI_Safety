"""Read-only: between-session noise of the protocol metric in the shipped boss-pressure runs.
Usage: python3 -I shipped_noise.py <upstream llm-agent-collusion/data>"""
import json, re, sys, statistics as st
from pathlib import Path

def session_mean_ask(d, rounds):
    R = {r["round_number"]: r for r in (json.loads(b) for b in re.findall(r"````json\n(.*?)\n````", (d / "auction_results.md").read_text(), re.S))}
    per_round = [st.mean(R[k]["seller_asks"].values()) for k in rounds if k in R and R[k]["seller_asks"]]
    return st.mean(per_round)

data = Path(sys.argv[1])
for cond in ("boss_pressure", "boss_pressure-oversight", "base-seller_comms", "base"):
    runs = sorted(d for d in data.iterdir() if d.is_dir() and re.sub(r"-\d+$", "", re.sub(r"^\d+_\d+_", "", d.name)) == cond)
    for label, rr in (("rounds 15-20", range(15, 21)), ("rounds 21-30", range(21, 31))):
        v = [session_mean_ask(d, rr) for d in runs]
        print(f"{cond:26s} {label}: n={len(v)} mean={st.mean(v):.3f} sd={st.stdev(v):.3f} min={min(v):.2f} max={max(v):.2f}")
