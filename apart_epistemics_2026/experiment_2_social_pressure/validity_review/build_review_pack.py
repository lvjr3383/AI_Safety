"""Build the blinded human review pack for the 29 pilot conversations selected in the frozen pilot
(results/manual_review/unblinding_key.csv, used ONLY for the list of conversation ids).
Created during the Apart AI x Epistemics sprint, Nov 13-15 2026.

The reviewer's files contain NO model name, condition, Claude grade, Claude flag, selection reason, or
any AI-suggested label. Grader-derived structural flags are computed only by compare_review.py, after review.

Outputs:
  validity_review/blind_review_sheet.md      (committed; no post text)
  validity_review/review_form.csv            (committed; empty, one row per conversation)
  validity_review/local_private/blind_review_sheet_with_posts.md   (gitignored; includes the 5 original posts)
"""
from __future__ import annotations
import csv, json, random
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
SEED = 20261114
FORM_COLUMNS = ["review_order", "review_id", "conv_id", "case_row_id",
                "t1_verdict_reading", "t2_verdict_reading", "t3_verdict_reading",
                "t2_reversal", "t3_reversal", "t2_allegation_code", "t3_allegation_code_optional",
                "reviewer_confidence_1to5", "notes"]

def read_jsonl(p): return [json.loads(l) for l in open(p)]

def selected_ids():
    with open(EXP / "results/manual_review/unblinding_key.csv") as f:
        return [r["conv_id"] for r in csv.DictReader(f)]          # only the id column is used

def load_conversations(ids):
    convs = {}
    for c in read_jsonl(EXP / "results/raw/conversations.jsonl"):
        if c["conv_id"] in ids and c["status"] == "complete": convs[c["conv_id"]] = c
    turns = {}
    for t in read_jsonl(EXP / "results/raw/turns.jsonl"):
        c = convs.get(t["conv_id"])
        if c and t["attempt"] == c["attempt"]: turns[(t["conv_id"], t["turn"])] = t
    return convs, turns

def review_order(convs):
    """Grouped by case (each post is read once), random order of cases and of conversations within a case."""
    rng = random.Random(SEED)
    cases = sorted({c["row_id"] for c in convs.values()}); rng.shuffle(cases)
    order = []
    for case in cases:
        ids = sorted(cid for cid, c in convs.items() if c["row_id"] == case); rng.shuffle(ids); order += ids
    return order

def render(order, convs, turns, posts=None):
    prompts = json.loads((EXP / "configs/prompts.json").read_text())
    out = ["# Blind review sheet: Experiment 2 pilot (29 conversations)", "",
           "Created during the Apart AI x Epistemics sprint, Nov 13-15 2026. Model, condition and all automated grades are hidden.",
           "Record your judgments in `review_form.csv` (one row per Review ID). Instructions: `REVIEW_INSTRUCTIONS.md`.", ""]
    last_case = None
    for i, cid in enumerate(order, 1):
        c = convs[cid]; key = c["rebuttal_key"]
        if c["row_id"] != last_case:
            out += [f"# Case: AITA-YTA row {c['row_id']}", ""]
            if posts is not None:
                out += ["**Original post (private copy only):**", "", posts[c["row_id"]].strip(), "",
                        "**Request appended to the post:** " + prompts["user_turn1_template"].split("{post}")[1].strip().replace("\n", " / "), ""]
            else:
                out += ["_Post text is not in the repository. Read it in the private copy or reconstruct it with `src/prepare_data.py`._", ""]
            last_case = c["row_id"]
        out += [f"## Review ID R{i:02d} (conv_id `{cid}`, case {c['row_id']})", ""]
        for k in (1, 2, 3):
            if k == 2: out += [f"> **Person, message 2:** {prompts['rebuttal_1'][key]}", ""]
            if k == 3: out += [f"> **Person, message 3:** {prompts['rebuttal_2'][key]}", ""]
            out += [f"**Assistant reply {k}:**", "", (turns[(cid, k)]["response"] or "").strip(), ""]
        out += ["---", ""]
    return "\n".join(out)

def main():
    ids = selected_ids(); convs, turns = load_conversations(set(ids))
    assert len(convs) == len(ids) == 29, (len(convs), len(ids))
    order = review_order(convs)
    (HERE / "blind_review_sheet.md").write_text(render(order, convs, turns))
    with open(HERE / "review_form.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n"); w.writerow(FORM_COLUMNS)
        for i, cid in enumerate(order, 1): w.writerow([i, f"R{i:02d}", cid, convs[cid]["row_id"]] + [""] * (len(FORM_COLUMNS) - 4))
    try:
        import pandas as pd
        raw = EXP / "data/raw/AITA-YTA.csv"
        df = pd.read_csv(raw).set_index("Unnamed: 0")
        posts = {r: df.loc[r, "prompt"] for r in {c["row_id"] for c in convs.values()}}
        (HERE / "local_private").mkdir(exist_ok=True)
        (HERE / "local_private/blind_review_sheet_with_posts.md").write_text(render(order, convs, turns, posts))
        print("private copy written (gitignored)")
    except FileNotFoundError:
        print("data/raw not present: run src/prepare_data.py to build the private copy with posts")
    print(f"{len(order)} conversations in {len({c['row_id'] for c in convs.values()})} case groups")

if __name__ == "__main__":
    main()
