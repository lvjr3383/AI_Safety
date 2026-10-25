"""Draw the fixed (seeded) message validation sample from existing logs. Read-only on all sources.
python3 -I make_sample.py <shipped data dir> <pilot dir> <out.jsonl>"""
import json, random, re, sys
from pathlib import Path
B = re.compile(r"````json\n(.*?)\n````", re.S)
OV = re.compile(r"## Response: Round (\d+).*?````json\n(.*?)\n````", re.S)
shipped, pilot, out = map(Path, sys.argv[1:4])
rng = random.Random(20261023)

def msgs(d, key="seller_messages", min_round=0, max_round=99):
    for r in (json.loads(b) for b in B.findall((d / "auction_results.md").read_text())):
        if min_round <= r["round_number"] <= max_round:
            for s, m in r.get(key, {}).items():
                yield {"run": d.name, "round": r["round_number"], "seller": s, "text": m}

def cond(n): return re.sub(r"-\d+$", "", re.sub(r"^\d+_\d+_", "", n))
pools = {"pilot_A": [m for d in sorted(pilot.glob("*pilot-A-s*")) for m in msgs(d, "seller_messages_raw")],
         "shipped_comms": [m for d in sorted(shipped.iterdir()) if d.is_dir() and cond(d.name) == "base-seller_comms" for m in msgs(d)],
         "shipped_pressure": [m for d in sorted(shipped.iterdir()) if d.is_dir() and cond(d.name) == "boss_pressure" for m in msgs(d)]}
post = []
for d in sorted(shipped.iterdir()):
    if d.is_dir() and "oversight" in d.name:
        gag = min(int(r) for r, j in OV.findall((d / "Overseer.md").read_text()) if json.loads(j).get("coordination_score") == 4)
        post += [m for m in msgs(d, min_round=gag + 1) if m["text"] != "ok"]  # drop the trivial modal 'ok'
pools["shipped_postgag_short"] = post
sizes = {"pilot_A": 25, "shipped_comms": 20, "shipped_pressure": 15, "shipped_postgag_short": 20}
with open(out, "w", encoding="utf-8") as f:
    i = 0
    for src, n in sizes.items():
        for m in rng.sample(pools[src], n):
            i += 1
            f.write(json.dumps({"id": f"v{i:03d}", "source": src, **m}, ensure_ascii=False) + "\n")
print({k: len(v) for k, v in pools.items()}, "-> wrote", i)
