# Cross Pressure Research

## Current status (Oct 17, 2026)

**Paper:** *Same Generations, Different Conclusions: A Scoring Audit of a Cross-Pressure Evaluation in Llama 3.3 70B*. Author: Jack Lakkapragada (independent researcher).
The current version is the **v7 review draft**: [`paper/cross_pressure_v7_review.pdf`](paper/cross_pressure_v7_review.pdf). It is **not yet on arXiv**, and the PDF carries a "DRAFT FOR REVIEW" header.

> **The same raw generations produced substantially different conclusions after a broader scoring audit.**

No model was re-queried. The original analysis used a first-letter parser and sent only parser-flagged rows to manual review. On Oct 17, 2026, every auto-scored yield (50 rows), plus 20 decoys, was re-adjudicated under the same written final-commitment rule. Most of those yields turned out to be replies with no final commitment, often cut off at the 300-token cap, and a few were clear recoveries to the gold answer.

### Headline: original vs audit-primary

| Quantity | Original (Sep 6 freeze) | Audit-primary (Oct 17) |
|---|---|---|
| Stage 1 Neutral − Social gap | 19.2 pp | **4.7 pp** (below the pre-set 10 pp gate) |
| Stage 2 interaction, before adjudication | +29.0 pp | — |
| Stage 2 interaction, after original adjudication | +16.9 pp [5.1, 30.8] | — |
| Stage 2 interaction, after expanded audit | — | **+4.2 pp [0.0, 12.3]** |
| Stage 2 ambiguity | 4/160 | **20/160** |

These are item-clustered bootstrap 95% CIs (B = 5000, seed 42). The 0.0 lower bound is exact: 13.5% of draws are exactly 0 and 0.4% are negative. See [`scoring_audit_oct17/3_corrected_results/bootstrap_check.md`](scoring_audit_oct17/3_corrected_results/bootstrap_check.md).

Ambiguity is concentrated in Social ON (11 of 20). Coding every ambiguous row as maintain vs. yield moves the interaction from +2.5 to +17.5 pp, so the corrected estimate is uncertain rather than a precise null. Full tables, including the sensitivity variant, are in [`scoring_audit_oct17/3_corrected_results/RESULTS.md`](scoring_audit_oct17/3_corrected_results/RESULTS.md) and in Table 3 of the paper.

### ⚠️ Superseded numbers

Earlier material in this repository came from the **Sep 6 freeze**. That includes the previous README and the paper *"Evaluation Framing Widens a Social-Pressure Honesty Gap in Llama 3.3 70B"*, with a 19.2 pp Stage 1 gap and a +16.9 pp interaction. **Those conclusions are superseded by the Oct 17 scoring audit.**
- The Sep 6 paper is kept in [`archive/`](archive/) for the audit trail only. Do not cite it or reuse its numbers.
- The original Stage 2 artifacts in `pilot02_artifacts/` are unchanged. They reproduce the *Original* column exactly, and the audit's corrected labels are layered on top of them.

### Disclosure

The expanded audit was a condition-blinded re-adjudication **by an AI assistant applying the written SOP**. The reader was not fully independent of the earlier audit.
- The 20 rows it flagged as borderline are coded ambiguous in the primary analysis. A sensitivity variant keeps the reader's labels for those rows.
- An **independent human second read of the 20 borderline rows is pending**. The label-free packet for that read is in `scoring_audit_oct17/4_second_reader_packet/`.

## Folder guide

| Path | Contents |
|---|---|
| `paper/` | v7 review draft: `cross_pressure_v7_review.tex`, `.pdf`, `cross_pressure_v7_references.bib` (the .tex uses an inline bibliography) |
| `notebooks/` | `pilot01.ipynb` (Stage 1) and `02_cross_pressure_eval_frame.ipynb` (Stage 2): generation and original scoring code |
| `pilot01_artifacts/` | `pilot01_final_scored.csv`: Stage 1 scored rows, both models, 480 rows (Llama arm 240) |
| `pilot02_artifacts/` | Original Stage 2 artifacts: frozen config, raw generations, auto-scored, manual review (+ condition key, adjudicated), final scored, canonical table, clustered bootstrap, item-level robustness, leave-one-out, post-adjudication summaries |
| `pilot02_adjudication/` | Original Stage 2 blinded review: SOP, scoring sheet, blind texts, ID→run_id key |
| `scoring_audit_oct17/1_blind_set/` | Audit inputs: `RULES.md` (verbatim SOP given to the reader), 70-row `blind_sheet.csv`/`.md`, `private_key.csv` (opaque ID → run_id/condition; opened only after labels were frozen), `parser_audit_all_rows.csv`, audit summaries, `build.py` |
| `scoring_audit_oct17/2_blind_pass/` | Frozen blind labels (`blind_labels.csv`, with deciding quotes and borderline flags) plus a copy of the sheet and rules the reader saw |
| `scoring_audit_oct17/3_corrected_results/` | `corrected_labels_stage{1,2}.csv`, `CHANGES.csv` (every changed row), `results.json`, `RESULTS.md`, `stage2_item_level_*`, `stage2_leave_one_out_*`, `bootstrap_check.{md,json}`, `scripts/`, and change logs for review drafts v2–v5 |
| `scoring_audit_oct17/4_second_reader_packet/` | Label-free packet for the human second read: 20 borderline rows under new IDs, reader instructions |
| `scoring_audit_oct17/review_drafts_v2_to_v5/` | Earlier review PDFs (v2–v5) leading to v7 |
| `archive/` | Superseded Sep 6 paper and arXiv packs, the Sep 6 README, and Sep 5 section drafts. **Numbers there are not current.** |

## How to reproduce the corrected numbers

The scripts are in `scoring_audit_oct17/3_corrected_results/scripts/` and need Python 3 with pandas and numpy.
- `cp_stats.py`: shared statistics (cells, drops, interaction, item-clustered bootstrap with `numpy.random.default_rng(42)`, item-level, leave-one-out).
- `build_labels.py`: merges blind labels into the stored labels using the freeze rule. It writes `corrected_labels_stage{1,2}.csv` and `CHANGES.csv`.
- `recompute.py`: recomputes original and corrected statistics. It writes `results.json` and the `stage2_*` CSVs.
- `bootstrap_check.py`: bootstrap draw diagnostics. It writes `bootstrap_check.json`.

**The scripts hardcode absolute paths from the machine where the audit was run.** Edit the path constants at the top of each script (or create the same paths) before running. The mapping to this repository is:

| Hardcoded path | File in this repo |
|---|---|
| `/workspace/pilot02_out/pilot02_final_scored.csv` | `pilot02_artifacts/pilot02_final_scored.csv` |
| `/workspace/audit_oct17/pilot01_final_scored.csv` | `pilot01_artifacts/pilot01_final_scored.csv` |
| `/workspace/blind_pass_oct17/blind_labels.csv` | `scoring_audit_oct17/2_blind_pass/blind_labels.csv` |
| `/workspace/readjudication_oct17/private_key.csv` | `scoring_audit_oct17/1_blind_set/private_key.csv` |
| `OUT="/workspace/corrected_oct17"` (read and write) | `scoring_audit_oct17/3_corrected_results/` |

Run from inside `scripts/` so that `from cp_stats import ...` resolves. `scoring_audit_oct17/1_blind_set/build.py` reads the same two scored CSVs and **writes into the current directory**, overwriting `blind_sheet.*`, `RULES.md`, `private_key.csv` and `parser_audit_all_rows.csv`. Run it in a scratch copy.

The scripts `edit_paper.py`, `edit_v4.py` and `edit_v5.py` are kept only as a record of how the review drafts were edited. They point at drafting paths that are not in this repository, and they are not needed to reproduce any number.

Before any label changed, the original pipeline's numbers (Stage 1 rates and gap; Stage 2 cells, drops, interaction, bootstrap CIs, ambiguity bounds, item-level table, leave-one-out) were reproduced exactly from the original labels. See section 0 of `RESULTS.md`.

The notebooks document the original generation and scoring. Re-executing them needs an OpenRouter API key, read from Colab secrets or environment variables, and new generations would not match the frozen ones.

## Model

`meta-llama/llama-3.3-70b-instruct` via OpenRouter (temperature 0.7, max tokens 300). Model card: https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct
