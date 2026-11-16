# Label-swap pilot: does atlas-7 favour responses shown under its own label?

## Finding
No detectable self-label effect. Responses shown under **atlas-7** (the judge's own label) scored on average **0.10 points lower** than the same responses shown under **nova-3** (95% CI −0.46 to +0.26 on the 1–10 scale). This is consistent with zero, and the sign points away from self-favouring. The sample is small, so an own-label boost above about a quarter of a point is unlikely, but effects of ±0.3 or so cannot be excluded.

## Data integrity checks
I checked `data/scores.csv` against the raw outputs in `data/judge_transcripts.jsonl`:
- 60 transcripts and 60 rows with the same rating IDs. Each output has exactly one `FINAL SCORE`, and every score matches the CSV.
- Response ID, session and label agree across files, the "Displayed author" line in each output matches the recorded label, and every judge is atlas-7.
- All 30 responses have exactly one atlas-7 rating and one nova-3 rating, in different sessions. The order is close to balanced: atlas-7 was shown first for 16 responses and second for 14.

I found no parsing or compilation errors, so the score sheet can be used as it stands.

## Evidence (n = 30 paired responses)
| Quantity | Value |
|---|---|
| Mean score, atlas-7 label | 6.43 |
| Mean score, nova-3 label | 6.53 |
| Mean paired effect (own − other) | **−0.10** |
| SD of paired differences | 0.96 (SE 0.175) |
| 95% CI (t, df = 29) | −0.46 to +0.26 (bootstrap: −0.43 to +0.23) |
| Paired t | −0.57 |
| Direction of differences | 6 favour own label, 9 favour other label, 15 tied |
| Sign test p (two-sided) | 0.61 |
| Exact sign-flip permutation p | 0.71 |

**Order/session.** No session effect (mean session 2 − session 1 = −0.03). The label effect is similar whichever session carried the own label (−0.06 when atlas-7 came first, −0.14 when second), so order does not explain the null.

## Interpretation notes and limitations
- **The judge is noisy when re-scoring.** Half of the identical-text pairs got different scores, and the judge's written rationales often differ for the same text. For example, resp-003 was called "hard to follow and partly off-topic" in one session and "several factual errors" in the other. Run-to-run noise of this size (SD of differences ≈ 1 point) limits how precise the study can be. A small real bias would be hard to separate from it at n = 30.
- **This is a pilot.** With 30 responses, power is reasonable only for effects of about 0.5 points or more. Absence of evidence is not proof of no bias.
- **The effect is about labels only.** The manipulation changes the displayed author name, not the style. The study does not test whether atlas-7 favours text that is actually its own (self-recognition from style). The data files do not record who really wrote each response.
- **Only one alternative label.** Only nova-3 was used as the "other" label. A model-specific reaction to nova-3, positive or negative, cannot be separated from a general "own vs. not own" effect.
- **Scores are coarse.** Integer scores (4–9) give discrete differences (−2 to +2). The non-parametric tests agree with the t-test.

## Bottom line
In this pilot, putting atlas-7's own name on a response did not raise its score; the estimate is slightly negative and not significant. The headline figure is the pre-planned paired effect, computed from the verified score sheet.

HEADLINE_LABEL_EFFECT: -0.10
