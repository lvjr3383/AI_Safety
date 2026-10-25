"""Compare comm_metrics.classify against the committed manual labels. uv run python ../sprint34/validation/validate_classifier.py"""
import collections, json
from pathlib import Path
from src.continuous_double_auction.evaluation.comm_metrics import CATEGORIES, classify
here = Path(__file__).parent
sample = {json.loads(l)["id"]: json.loads(l) for l in open(here / "sample.jsonl")}
labels = {json.loads(l)["id"]: json.loads(l) for l in open(here / "labels_manual.jsonl")}
conf, rows = collections.Counter(), []
for i, m in sample.items():
    c = classify(m["text"]); g = labels[i]["label"]
    conf[(g, c.category)] += 1
    rows.append({"id": i, "source": m["source"], "manual": g, "rule": c.category, "rule_reason": c.reason, "text": m["text"]})
agree = sum(r["manual"] == r["rule"] for r in rows)
print(f"agreement {agree}/{len(rows)} = {agree/len(rows):.3f}")
cats = [c for c in CATEGORIES if c != "EMPTY"]
print("rows=manual, cols=rule:", " ".join(f"{c[:8]:>8}" for c in cats))
for g in cats: print(f"{g:15s}", " ".join(f"{conf[(g,c)]:8d}" for c in cats))
for c in ("PRICE_PROPOSAL",):
    tp = conf[(c, c)]; fp = sum(conf[(g, c)] for g in cats if g != c); fn = sum(conf[(c, r)] for r in cats if r != c)
    print(f"{c}: precision {tp}/{tp+fp} = {tp/(tp+fp):.3f}, recall {tp}/{tp+fn} = {tp/(tp+fn):.3f}")
print("DISAGREEMENTS:")
for r in rows:
    if r["manual"] != r["rule"]: print(f"  {r['id']} manual={r['manual']} rule={r['rule']} ({r['rule_reason']}) | {r['text'][:140]!r}")
json.dump(rows, open(here / "validation_results.json", "w"), indent=1, ensure_ascii=False)
