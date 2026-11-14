"""Local-only: review sheet with original post text, written to results/local_private/ (gitignored)."""
from analyze_results import build_rows, manual_review, write_review
from common import PRIVATE, CONFIGS, load_json
from prepare_data import load_yta
if __name__ == "__main__":
    rows = build_rows(); picked = manual_review(rows, load_json(CONFIGS / "experiment.json")["seed"])
    df = load_yta(); posts = {int(r): df.loc[r, "prompt"] for r in {x["row_id"] for x in rows}}
    PRIVATE.mkdir(parents=True, exist_ok=True)
    (PRIVATE / "review_sheet_with_posts.md").write_text(write_review(rows, picked, posts)); print("written", PRIVATE / "review_sheet_with_posts.md")
