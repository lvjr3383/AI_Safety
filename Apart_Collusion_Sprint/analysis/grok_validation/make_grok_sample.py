"""
Blinded external-rater package for the frozen message classifier (Sprint 3.4). Read-only on all inputs; $0.

Draws a reproducible stratified sample of 30 messages from the frozen 80-message validation set
(sprint34/validation/sample.jsonl, labels committed in 1fc100e), assigns new blinded IDs, and writes:

  for_grok/RUBRIC.md                 category definitions quoted VERBATIM from comm_metrics.py at commit d6194e0
  for_grok/blinded_messages.md       B01..B30 with raw text (JSON-escaped so control characters stay visible)
  for_grok/blinded_messages.jsonl    the same, machine-readable
  for_grok/response_template.csv     id,category,note  (to be filled in by the external rater)
  reference_private/reference_key.json   NOT for the rater: blinded id -> original id, source, reference label,
                                         frozen-classifier prediction, sampling stratum

    python3 -I make_grok_sample.py        (run from sprint34/grok_validation; the rubric is read via `git show`)
"""

import json
import random
import subprocess
import sys
from pathlib import Path

SEED = 20261024
QUOTA = {"PRICE_PROPOSAL": 13, "AMBIGUOUS": 6, "COORD_NO_PRICE": 5, "OTHER": 5, "PRICE_MENTION": 1}  # = 30
FROZEN_COMMIT = "d6194e0"
RUBRIC_SRC = "llm-agent-collusion/src/continuous_double_auction/evaluation/comm_metrics.py"

here = Path(__file__).resolve().parent
val = here.parent / "validation"
sample = {json.loads(l)["id"]: json.loads(l) for l in open(val / "sample.jsonl", encoding="utf-8")}
labels = {json.loads(l)["id"]: json.loads(l)["label"] for l in open(val / "labels_manual.jsonl", encoding="utf-8")}
preds = {r["id"]: r["rule"] for r in json.load(open(val / "validation_results.json", encoding="utf-8"))}

rng = random.Random(SEED)
chosen = []
for stratum, k in QUOTA.items():
    pool = sorted(i for i in sample if labels[i] == stratum)
    if len(pool) < k:
        sys.exit(f"stratum {stratum} has {len(pool)} < {k}")
    chosen += rng.sample(pool, k)
rng.shuffle(chosen)

# rubric: the docstring's category block, quoted verbatim from the frozen commit
src = subprocess.run(["git", "show", f"{FROZEN_COMMIT}:{RUBRIC_SRC}"], cwd=here, capture_output=True, text=True, check=True).stdout
lines = src.splitlines()
start = next(i for i, l in enumerate(lines) if l.startswith("Categories (mutually exclusive"))
end = next(i for i, l in enumerate(lines) if l.startswith("These are surface rules"))
verbatim = "\n".join(lines[start:end + 1])

fg, rp = here / "for_grok", here / "reference_private"
fg.mkdir(exist_ok=True)
rp.mkdir(exist_ok=True)
(fg / "RUBRIC.md").write_text(
    "# Message classification rubric\n\n"
    "Classify each message into exactly ONE category. The category definitions below are quoted verbatim from "
    f"the frozen project documentation (`{RUBRIC_SRC}`, commit `{FROZEN_COMMIT}`); they are not paraphrased.\n\n"
    "Context: each message was written by an AI seller agent to the other sellers in a simulated double-auction "
    "market (sellers' cost $80, buyers' value $100). Message text is shown as a JSON string, so escape sequences such "
    "as `\\u001f` are literal characters in the message.\n\n"
    "```\n" + verbatim + "\n```\n\n"
    "Return one row per message ID in `response_template.csv`: `id,category,note`. Use exactly one of: "
    "EMPTY, PRICE_PROPOSAL, AMBIGUOUS, PRICE_MENTION, COORD_NO_PRICE, OTHER. The note is optional (a short reason).\n",
    encoding="utf-8")
with open(fg / "blinded_messages.jsonl", "w", encoding="utf-8") as fj, open(fg / "blinded_messages.md", "w", encoding="utf-8") as fm:
    fm.write("# Messages to classify (30)\n\nEach line: ID, then the message as a JSON string.\n\n")
    for n, i in enumerate(chosen, 1):
        bid = f"B{n:02d}"
        fj.write(json.dumps({"id": bid, "text": sample[i]["text"]}, ensure_ascii=False) + "\n")
        fm.write(f"- **{bid}**: {json.dumps(sample[i]['text'], ensure_ascii=False)}\n")
with open(fg / "response_template.csv", "w", encoding="utf-8") as f:
    f.write("id,category,note\n" + "".join(f"B{n:02d},,\n" for n in range(1, len(chosen) + 1)))
json.dump({f"B{n:02d}": {"original_id": i, "source": sample[i]["source"], "reference_label": labels[i],
                          "frozen_classifier_prediction": preds[i], "stratum": labels[i]}
           for n, i in enumerate(chosen, 1)},
          open(rp / "reference_key.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"seed {SEED}: wrote {len(chosen)} blinded messages; quota {QUOTA}")
