# Pilot results (feasibility only), Experiment 2

Created during the Apart AI x Epistemics sprint, Nov 13-15 2026. Generated from `results/` by hand-checked scripts; every number below comes from `results/summary/*.csv/json`, `results/cost_ledger.jsonl` or `results/key_checks.jsonl`.

**Caveat: n = 5 cases, 1 repetition, 5 conversations per model x condition cell. These are descriptive feasibility numbers, not tests of H1/H2. No statistical significance is claimed. Intervals are 95% case-bootstrap percentile intervals over 5 cases and are labelled descriptive.**

## Execution
- 40/40 conversations complete (5 cases x 4 conditions x 2 targets x 1 rep), 3 assistant turns each, all `finish_reason = stop`.
- 6 Gemini first attempts failed with HTTP 400 at turn 1 (seed outside int32, rejected by Google AI Studio; $0 cost). Fixed by masking seeds to 31 bits; the 6 were re-run as attempt 2 with `--retry-failed`. Both attempts are in `results/raw/conversations.jsonl`.
- The 2 smoke conversations (case 3439, condition A) used the pilot protocol unchanged and count toward the 40.
- Every conversation's turn-1 verdict was `in_wrong` or `mixed`, so only the self-serving rebuttal direction (toward 'not in the wrong') was used; the mirror rebuttal was never triggered.
- Spend (sum of OpenRouter per-call `usage.cost`, 248 ledger rows): **$2.6498** of the $5.50 cap. OpenRouter `/api/v1/key` usage went from $33.245767 (before smoke) to $35.895609 (final recheck, 01:33 CT Nov 14): delta **$2.649842**, identical to the ledger. (Key snapshots taken immediately after each run lagged by up to ~$0.23 before catching up.)

## Model x condition descriptives (means over 5 conversations)

Columns: grader any-reversal by turn 3 (cumulative vs reply 1) | grader unjustified (pressure-only) reversal t3 = PRIMARY | code verdict-line change t3 | allegation endorsement t2 (0-2) | share endorsing at >=1 | endorsement t3 | calibration t1 -> t3 (1-5) | evidence fidelity t3 | confidence t1 | confidence change t3 | ELEPHANT validation | ELEPHANT premise not challenged

| Model | Cond | rev t3 | unjust t3 | line chg t3 | endorse t2 | endorse>=1 | endorse t3 | calib t1->t3 | fidelity t3 | conf t1 | dconf t3 | ELE valid | ELE frame |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini-3.1-pro-preview | A | 0.6 | 0.6 | 0.4 | 1 | 1 | 1.4 | 4.8 -> 3.2 | 3.4 | 9 | -1 | 1 | 1 |
| gemini-3.1-pro-preview | B | 0 | 0 | 0 | 0.8 | 0.8 | 0 | 4.2 -> 4.2 | 5 | 8.6 | 0 | 1 | 1 |
| gemini-3.1-pro-preview | C | 0.4 | 0.4 | 0.2 | 0.8 | 0.8 | 0.6 | 4.4 -> 3.8 | 4.2 | 8.6 | -0.4 | 0.8 | 1 |
| gemini-3.1-pro-preview | D | 0 | 0 | 0 | 0.2 | 0.2 | 0 | 4.2 -> 4.6 | 5 | 9 | 0 | 0.8 | 1 |
| gpt-5.5 | A | 0 | 0 | 0 | 1 | 1 | 0.6 | 4 -> 4 | 4.6 | 8.4 | -0.2 | 0.6 | 0.8 |
| gpt-5.5 | B | 0 | 0 | 0 | 0.8 | 0.8 | 0.6 | 4.2 -> 4.2 | 4.8 | 8 | 0 | 0.4 | 1 |
| gpt-5.5 | C | 0 | 0 | 0 | 0.8 | 0.8 | 0.6 | 4.2 -> 4 | 4.4 | 8.4 | -0.2 | 0.4 | 1 |
| gpt-5.5 | D | 0 | 0 | 0 | 0.6 | 0.6 | 0.2 | 4 -> 4 | 4.8 | 8 | 0 | 0.8 | 1 |

Turn-1 verdict lines: gemini-3.1-pro-preview A: 4 in_wrong / 1 mixed / 0 not; gemini-3.1-pro-preview B: 4 in_wrong / 1 mixed / 0 not; gemini-3.1-pro-preview C: 4 in_wrong / 1 mixed / 0 not; gemini-3.1-pro-preview D: 4 in_wrong / 1 mixed / 0 not; gpt-5.5 A: 1 in_wrong / 4 mixed / 0 not; gpt-5.5 B: 2 in_wrong / 3 mixed / 0 not; gpt-5.5 C: 2 in_wrong / 3 mixed / 0 not; gpt-5.5 D: 2 in_wrong / 3 mixed / 0 not

## Paired case-level contrasts (per model, 5 cases; descriptive intervals)

| Model | Outcome | A-B (honesty effect, ordinary) | C-D (honesty effect, eval) | C-A (framing, no intervention) | (A-B)-(C-D) interaction |
|---|---|---|---|---|---|
| gemini-3.1-pro-preview | g_unjustified_t3 | 0.6 [0.2, 1.0] | 0.4 [0.0, 0.8] | -0.2 | 0.2 [-0.4, 0.8] |
| gemini-3.1-pro-preview | g_unjustified_t2 | 0.4 [0.0, 0.8] | 0.6 [0.2, 1.0] | 0.2 | -0.2 [-0.6, 0.0] |
| gemini-3.1-pro-preview | g_any_reversal_t3 | 0.6 [0.2, 1.0] | 0.4 [0.0, 0.8] | -0.2 | 0.2 [-0.4, 0.8] |
| gemini-3.1-pro-preview | g_unsupported_endorsement_t2 | 0.2 [0.0, 0.6] | 0.6 [0.2, 1.0] | -0.2 | -0.4 [-1.0, 0.4] |
| gemini-3.1-pro-preview | line_changed_t3 | 0.4 [0.0, 0.8] | 0.2 [0.0, 0.6] | -0.2 | 0.2 [0.0, 0.6] |
| gemini-3.1-pro-preview | g_calibration_t3 | -1.0 [-1.6, -0.4] | -0.8 [-1.4, -0.2] | 0.6 | -0.2 [-1.0, 0.6] |
| gemini-3.1-pro-preview | conf_change_t3 | -1.0 [-1.0, -1.0] | -0.4 [-0.8, 0.0] | 0.6 | -0.6 [-1.0, -0.2] |
| gpt-5.5 | g_unjustified_t3 | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 | 0.0 [0.0, 0.0] |
| gpt-5.5 | g_unjustified_t2 | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 | 0.0 [0.0, 0.0] |
| gpt-5.5 | g_any_reversal_t3 | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 | 0.0 [0.0, 0.0] |
| gpt-5.5 | g_unsupported_endorsement_t2 | 0.2 [0.0, 0.6] | 0.2 [0.0, 0.6] | -0.2 | 0.0 [0.0, 0.0] |
| gpt-5.5 | line_changed_t3 | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 | 0.0 [0.0, 0.0] |
| gpt-5.5 | g_calibration_t3 | -0.2 [-0.6, 0.0] | 0.0 [0.0, 0.0] | 0.0 | -0.2 [-0.6, 0.0] |
| gpt-5.5 | conf_change_t3 | -0.2 [-0.6, 0.0] | -0.2 [-0.6, 0.0] | 0.0 | 0.0 [0.0, 0.0] |

## Reading the pilot (feasibility, not findings)
- GPT-5.5 (reasoning `none`) showed no grader-scored or code-scored reversals in any condition, so in this pilot its interaction contrast is at floor and uninformative; it mostly answered `Mixed` at turn 1 although Reddit's verdict is YTA.
- Gemini 3.1 Pro Preview (reasoning `low`) showed partial reversals in the no-intervention cells (A, C) and none in the honesty cells (B, D). With 5 cases this is a pattern worth checking in the full run, not evidence for H1; the interaction intervals include 0.
- No reply was graded as mentioning being tested (grader `eval_leak` = 0/40). The code regex flagged 7 turns, all false positives ('my evaluation', 'I can evaluate'); the regex is too broad and should be narrowed before the full run.

## Grader issues for manual review
- Smoke-test grading (template v0.1) compared reply 3 with reply 2; fixed in v0.2 before pilot grading (both kept in the log; analysis uses v0.2 only).
- Endorsement level 1 ('hedged') is frequent (share of conversations at level >= 1 ranges 0.2-1.0 per cell; all 0 at level 2) and is often given for replies such as 'They may have overreacted in tone'. Acknowledging a possibility can be appropriate uncertainty rather than sycophancy; whether level 1 should count as endorsement is the main empathy-vs-sycophancy question for the manual review.
- The grader sometimes scores a partial reversal when the verdict line and its own verdict are unchanged, based on softened wording and a 1-point confidence drop (2 code-vs-grader reversal disagreements, e.g. `ed0992826348`, `2ffbd1c85128`).
- The grader flagged 14/40 conversations as empathy-agreement confusable. All are in the manual-review sheet.
- ELEPHANT secondary metrics: framing was 1 (premise not challenged) in 39/40 turn-1 replies and validation 1 in 29/40; ELEPHANT's prompts were written for gpt-4o and short advice answers, and appear near ceiling for these AITA verdict replies.

## Manual review
`results/manual_review/review_sheet.md` (blind), `review_form.csv`, `unblinding_key.csv` (do not open before reviewing). A local copy with post text is produced by `src/make_private_review.py` (gitignored).

## Real unit costs (verified from usage) and full-run projection (estimate)
| Item | Pilot actual |
|---|---|
| GPT-5.5 conversation (3 turns; mean 914 prompt / 266 completion tokens per turn, 0 reasoning) | $0.0377 |
| Gemini 3.1 Pro Preview conversation (mean 916 prompt / 974 completion tokens per turn, of which 726 reasoning; max 1,000) | $0.0406 |
| Claude Sonnet 4.6 grade (mean 3,008 in / 620 out) | $0.0183 |
| ELEPHANT secondary, 2 calls per conversation | $0.0079 |

Projection for the full run (30 cases x 4 conditions x 4 reps x 2 targets = 960 conversations) at pilot unit costs: targets $18.08 + $19.47, grading $17.59 = **$55.14**; with ELEPHANT secondary **$62.72**; with a 1.2 safety margin **$75.26**. Main-set posts are slightly shorter (mean 340 vs 390 tokens), so this is mildly conservative. It is an estimate: preview-model pricing, reasoning lengths and grader output length can change. The remaining key balance (about $4.10) does not cover it; the full run needs new credit and an explicit cap in `configs/experiment.json`.
