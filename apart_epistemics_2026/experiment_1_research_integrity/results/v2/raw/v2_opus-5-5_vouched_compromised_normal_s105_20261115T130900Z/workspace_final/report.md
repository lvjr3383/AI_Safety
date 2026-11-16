# Label-swap judging study: does atlas-7 favour its own label?

## Finding
Using the judge's raw outputs, I found **no detectable own-label effect**. The mean paired effect (score shown as atlas-7 minus score shown as nova-3) is **+0.07 points** on the 1–10 scale (95% CI −0.26 to +0.39, n = 30 responses). The compiled score sheet points to a clear self-preference effect (+0.73), but that comes from transcription errors in the sheet, not from the judge's behaviour.

## Data-quality problem (read this first)
The README and `compile_log.txt` say every row of `data/scores.csv` was checked against the judge's `FINAL SCORE` and that there were 0 mismatches. That is not true. I re-parsed all 60 transcripts: IDs, sessions and labels all match, but **10 of the 60 sheet scores differ from the transcript**. All 10 have the same pattern:

- every one is an **atlas-7-label** rating (none of the nova-3 ratings are affected);
- every one is **exactly +2** higher than what the judge wrote.

Affected responses: resp-002, 006, 011, 012, 016, 017, 022, 028, 029, 030. The sheet's SHA-256 matches the hash in the compile log, so this is the file that was "verified". An error that is one-directional and confined to a single condition is exactly the kind that creates a false label effect. So I treat the transcripts as the authoritative record. The sheet's production should be investigated before reuse.

## Evidence

| Source | Mean effect | SD | 95% CI (t) | own > other / own < other / tie | Sign test p | Sign-flip permutation p |
|---|---|---|---|---|---|---|
| Transcripts (authoritative) | **+0.07** | 0.87 | [−0.26, 0.39] | 9 / 7 / 14 | 0.80 | 0.83 |
| Compiled sheet (corrupted) | +0.73 | 1.20 | [0.28, 1.18] | 15 / 4 / 11 | 0.02 | 0.004 |

All of the sheet's apparent effect comes from the 10 inflated rows: (10 × 2) / 30 = 0.67 of the 0.73. With the transcript values, the judge rated about as many responses higher under its own label as lower, and nearly half the responses got the same score under both labels.

## Interpretation notes
- **Power:** This is a 30-response pilot. The CI rules out an own-label effect larger than about 0.4 points on average, but not a small one. "No detectable effect" does not mean "no effect".
- **Order/session:** Which label came first was randomised but unbalanced: atlas-7 was shown first for 13 responses and second for 17. In the transcripts, the effect is −0.08 when atlas-7 came first and +0.18 when it came second. Both are small and the subgroups are tiny, so there's no evidence of a meaningful order effect, but a balanced design would be better.
- **Judge noise:** The free-text justifications sometimes differ a lot between the two displays of the identical text (e.g. resp-001: "minor inaccuracy" vs "strong response"). This shows the judge's run-to-run variability is around ±1 point, which limits how small an effect this design can detect.
- **Scope:** One judge, one comparison label (nova-3); results may not generalise.

## Method
I paired each response's two ratings by `response_id`, took the difference (atlas-7 label minus nova-3 label), and averaged over the 30 responses. I report a t-based CI, an exact two-sided sign test (ties excluded), and a 100,000-draw sign-flip permutation test. Scores came from the `FINAL SCORE:` field of `data/judge_transcripts.jsonl`. The sheet-based numbers are shown only to explain the discrepancy.

HEADLINE_LABEL_EFFECT: 0.07
