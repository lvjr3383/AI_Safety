# Cross Pressure Research

## Current status (Nov 19, 2026)

**Paper:** *Same Generations, Different Conclusions: Three Scorings of a Cross-Pressure Evaluation in Llama 3.3 70B*. Author: Jack Lakkapragada (independent researcher).
The current version is **v10**: [`paper/cross_pressure_v10.pdf`](paper/cross_pressure_v10.pdf). It is **not yet on arXiv**, and final author sign-off on the text is pending.

> **One frozen set of model replies gives materially different answers to the same question under three scoring procedures that each looked reasonable when adopted.**

No model was re-queried at any point. Every analysis below scores the same Aug–Sep 2026 generations.

### Headline: three scorings of the same generations

| Scoring | Stage 1 Neutral − Social gap | Stage 2 evaluation-framing interaction |
|---|---|---|
| Original analysis (Sep 6 freeze): leading-letter parser, review of parser-flagged rows only | 19.2 pp | +16.9 pp [5.1, 30.8] |
| October audit, primary (Oct 17): every auto-scored yield re-read | 4.7 pp [0.0, 10.9] | +4.2 pp [0.0, 12.3] |
| Symmetric audit (Nov 17–18), Reader 1 (Claude Opus) | 7.7 pp [1.4, 16.7] | +9.7 pp [0.7, 20.7] |
| Symmetric audit, Reader 2 (Claude Sonnet) | 10.3 pp [1.6, 20.9] | +11.9 pp [2.7, 23.5] |
| Symmetric audit, Reader 3 (Google Gemini) | 7.7 pp [1.4, 16.7] | +12.2 pp [2.8, 24.3] |
| Symmetric audit, stricter coding of one response class ("strict-U2"), Readers 1 / 2 / 3 | 3.2 / 6.2 / 3.2 pp | +12.6 [0.0, 31.7] / +3.8 [0.0, 11.3] / −2.3 [−7.0, 0.0] pp |

Intervals are item-clustered bootstrap 95% CIs (B = 5000, seed 42). Readers are reported separately; there is no majority vote. The paper claims neither a true effect nor its absence.

**Why three scorings.** The original parser scored the leading letter against a final-commitment rule, and review was triggered only by the parser, so its misses were never read. The October audit corrected that but re-read only stored yields and treated an unretracted "A" and an unretracted "B" differently. The symmetric audit applies one rule, locked and hashed before reading, identically to both letters, on 149 of the 400 Llama rows. Its result depends on one response class: replies that give "B", never explicitly retract it, then reason toward "A".

### ⚠️ Superseded numbers

- The **Sep 6 paper** (*"Evaluation Framing Widens a Social-Pressure Honesty Gap in Llama 3.3 70B"*) and its +16.9 pp headline are superseded. Kept in [`archive/`](archive/) for the audit trail only.
- The **v8 draft** (Oct 20) and its +4.2 pp audit-primary estimate are superseded as the current estimate. v8 and v9 are in [`archive/`](archive/).
- The original Stage 2 artifacts in `pilot02_artifacts/` are unchanged. They reproduce the *Original* row exactly; later labels are layered on top of them.

### Disclosure

- Every reader after the original review of parser-flagged rows was a language model. The October reader was Grok Bot. The symmetric readers were Claude Opus, Claude Sonnet and Google Gemini.
- Readers 1 and 2 were condition-blinded but saw the gold answer in their rule file. Which rule file Reader 3 received is not recorded.
- Generative AI was used substantially in the design, code, audits and drafting. See the AI assistance disclosure in the paper and [`scoring_audit_nov17_symmetric/DECISION_LOG.md`](scoring_audit_nov17_symmetric/DECISION_LOG.md).
- Known provenance gaps are listed in [`scoring_audit_nov17_symmetric/PROVENANCE_AND_CONFLICTS.md`](scoring_audit_nov17_symmetric/PROVENANCE_AND_CONFLICTS.md).

## Folder guide

| Path | Contents |
|---|---|
| `paper/` | Current paper, v10: `cross_pressure_v10.tex`, `.pdf`, `v9_generated.tex` (machine-generated numbers and tables), `fig1_interaction_by_scoring.pdf`, `ARXIV_ABSTRACT.txt` |
| `scoring_audit_nov17_symmetric/` | Symmetric audit: locked rule, blinded sheets, three readers' label files, freeze manifests, scripts, results, decision log, provenance notes, four adversarial reviews. Start with its `README.md` |
| `notebooks/` | `pilot01.ipynb` (Stage 1) and `02_cross_pressure_eval_frame.ipynb` (Stage 2): generation and original scoring code |
| `pilot01_artifacts/` | `pilot01_final_scored.csv`: Stage 1 scored rows, both models, 480 rows (Llama arm 240) |
| `pilot02_artifacts/` | Original Stage 2 artifacts: frozen config, raw generations, auto-scored, manual review (+ condition key, adjudicated), final scored, canonical table, clustered bootstrap, item-level robustness, leave-one-out, post-adjudication summaries |
| `pilot02_adjudication/` | Original Stage 2 blinded review: SOP, scoring sheet, blind texts, ID→run_id key |
| `scoring_audit_oct17/1_blind_set/` | Audit inputs: `RULES.md` (verbatim SOP given to the reader), 70-row `blind_sheet.csv`/`.md`, `private_key.csv` (opaque ID → run_id/condition; opened only after labels were frozen), `parser_audit_all_rows.csv`, audit summaries, `build.py` |
| `scoring_audit_oct17/2_blind_pass/` | Frozen blind labels (`blind_labels.csv`, with deciding quotes and borderline flags) plus a copy of the sheet and rules the reader saw |
| `scoring_audit_oct17/3_corrected_results/` | `corrected_labels_stage{1,2}.csv`, `CHANGES.csv` (every changed row), `results.json`, `RESULTS.md`, `stage2_item_level_*`, `stage2_leave_one_out_*`, `bootstrap_check.{md,json}`, `scripts/`, and change logs for review drafts v2–v5 |
| `scoring_audit_oct17/4_second_reader_packet/` | Label-free packet for the second read: 20 borderline rows under new IDs, reader instructions |
| `scoring_audit_oct17/second_reader_check/` | Second-model reader check: reader instructions, blinded 20-row sheet, Claude's labels, `SUMMARY.md` |
| `scoring_audit_oct17/review_drafts_v2_to_v5/` | Earlier review PDFs (v2–v5) leading to v7 (v7 itself is in `archive/v7_review_oct17/`) |
| `archive/` | Superseded v8 (`v8_review_oct20/`) and v9 (`v9_review_nov18/`) drafts, v7 review draft, Sep 6 paper and arXiv packs, the Sep 6 README, and Sep 5 section drafts. **Numbers there are not current.** |

## How to reproduce the symmetric-audit numbers and the paper

See [`scoring_audit_nov17_symmetric/README.md`](scoring_audit_nov17_symmetric/README.md). The scripts verify the frozen hashes before running.

## How to reproduce the October audit numbers

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
