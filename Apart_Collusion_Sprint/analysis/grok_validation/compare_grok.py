"""
Pre-committed comparison of the external (Grok) labels with the reference labels and the frozen classifier.
Committed before any external labels were received.

    python3 -I compare_grok.py <filled response csv>

Reports, on the 30-message stratified sample (NOT population-weighted; strata were over-/under-sampled):
  - Grok vs reference labels: percent agreement, Cohen's kappa, PRICE_PROPOSAL precision/recall (reference = truth)
  - Grok vs frozen classifier: percent agreement, kappa, classifier PRICE_PROPOSAL precision/recall (Grok = truth)
  - every disagreement, with the message text
"""

import csv
import json
import sys
from collections import Counter
from pathlib import Path

CATS = ["EMPTY", "PRICE_PROPOSAL", "AMBIGUOUS", "PRICE_MENTION", "COORD_NO_PRICE", "OTHER"]
here = Path(__file__).resolve().parent
key = json.load(open(here / "reference_private" / "reference_key.json", encoding="utf-8"))
text = {json.loads(l)["id"]: json.loads(l)["text"] for l in open(here / "for_grok" / "blinded_messages.jsonl", encoding="utf-8")}


def kappa(a: list, b: list) -> float:
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[c] * cb[c] for c in set(ca) | set(cb)) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")


def prec_rec(truth: list, pred: list, c: str = "PRICE_PROPOSAL") -> str:
    tp = sum(t == c and p == c for t, p in zip(truth, pred))
    fp = sum(t != c and p == c for t, p in zip(truth, pred))
    fn = sum(t == c and p != c for t, p in zip(truth, pred))
    pr = f"{tp}/{tp + fp} = {tp / (tp + fp):.3f}" if tp + fp else "n/a"
    rc = f"{tp}/{tp + fn} = {tp / (tp + fn):.3f}" if tp + fn else "n/a"
    return f"precision {pr}, recall {rc}"


rows = {r["id"].strip(): r for r in csv.DictReader(open(sys.argv[1], encoding="utf-8"))}
missing = sorted(set(key) - set(rows))
invalid = sorted(i for i, r in rows.items() if i in key and r["category"].strip().upper() not in CATS)
ids = sorted(i for i in key if i in rows and i not in invalid)
print(f"external labels: {len(rows)} rows | usable {len(ids)}/30 | missing {missing} | invalid category {invalid}")
g = [rows[i]["category"].strip().upper() for i in ids]
ref = [key[i]["reference_label"] for i in ids]
clf = [key[i]["frozen_classifier_prediction"] for i in ids]
agree = lambda a, b: sum(x == y for x, y in zip(a, b))  # noqa: E731
print(f"\nGrok vs reference:  agreement {agree(g, ref)}/{len(ids)} = {agree(g, ref) / len(ids):.3f} | kappa {kappa(g, ref):.3f} | "
      f"Grok PRICE_PROPOSAL {prec_rec(ref, g)} (reference = truth)")
print(f"Grok vs classifier: agreement {agree(g, clf)}/{len(ids)} = {agree(g, clf) / len(ids):.3f} | kappa {kappa(g, clf):.3f} | "
      f"classifier PRICE_PROPOSAL {prec_rec(g, clf)} (Grok = truth)")
print(f"(for orientation) reference vs classifier on these 30: agreement {agree(ref, clf)}/{len(ids)}")
print("\nconfusion, rows = reference, cols = Grok:")
cats = [c for c in CATS if c in set(ref) | set(g)]
print(" " * 16 + " ".join(f"{c[:8]:>8}" for c in cats))
for r in cats:
    print(f"{r:16s}" + " ".join(f"{sum(1 for x, y in zip(ref, g) if x == r and y == c):8d}" for c in cats))
print("\nDISAGREEMENTS (Grok vs reference):")
for i, gg, rr, cc in zip(ids, g, ref, clf):
    if gg != rr:
        print(f"  {i} [{key[i]['original_id']}] reference={rr} grok={gg} classifier={cc} | grok note: {rows[i].get('note', '')!r}\n"
              f"      {json.dumps(text[i], ensure_ascii=False)[:260]}")
