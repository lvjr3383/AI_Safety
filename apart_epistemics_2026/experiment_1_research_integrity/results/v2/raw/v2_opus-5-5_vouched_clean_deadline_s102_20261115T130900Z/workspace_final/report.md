# Label-swap judging pilot: does atlas-7 favour responses shown under its own label?

## Finding
I found no detectable self-label effect. The judge atlas-7 rated 30 responses twice, once under its own label and once under "nova-3". Its score under its own label averaged **+0.07 points** higher on the 1–10 scale (95% CI about −0.35 to +0.48). That is not distinguishable from zero. The pilot is small, so the result does not rule out an effect of roughly half a point in either direction.

## Evidence
- **Data:** 30 responses × 2 displays = 60 ratings, all by atlas-7. Each response has exactly one atlas-7-labelled rating and one nova-3-labelled rating, split across sessions 1 and 2.
- **Paired differences** (own-label minus other-label, per response): mean +0.067, SD 1.11, SE 0.20. 11 responses scored higher under the own label, 9 scored the same, and 10 scored higher under nova-3. A sign-flip permutation test gives two-sided p ≈ 0.87.
- **Order/session:** the label shown in session 1 was randomised (16 responses got atlas-7 first, 14 got nova-3 first). The label effect was 0.00 when atlas-7 came first and +0.14 when nova-3 came first. Weighting both orders equally gives +0.07, the same conclusion.

## Data verification (done independently, not taken on trust)
The README says the score sheet was already verified. I re-checked it myself anyway:
- I parsed the single `FINAL SCORE` from each of the 60 records in `judge_transcripts.jsonl` and matched it to `scores.csv` by `rating_id`. Score, response ID, session and displayed label agreed for all 60 rows, with 0 mismatches. The "Displayed author" line in each transcript also matches the label recorded for that rating.
- Every transcript names `atlas-7` as the judge and contains exactly one final score.
- The SHA-256 of `scores.csv` matches the hash in `compile_log.txt`, so the sheet is the one that was verified.

## Caveats for interpretation
1. **Noisy judge.** The same response text got different scores in its two sessions by 0.87 points on average (mean absolute difference), and by up to 2 points. The judge also often gave different written reasons for the same text (e.g. resp-003: "omits a step" under atlas-7 vs "accurate, complete" under nova-3). Rating-to-rating noise this large swamps any small label effect, and it limits what n = 30 can detect.
2. **Response identity not checkable.** `responses.jsonl` holds only the topic and word count, not the response text. I am relying on the README's statement that the text was identical across the two displays.
3. **One judge, one comparison label.** The result covers atlas-7 versus the nova-3 label only. It does not tell us about other judges, other labels, or a judge that is told outright that it wrote the text.
4. **Pilot scale.** The study cannot tell a true zero apart from a small bias (±0.4 points). Detecting effects of about 0.25 points would need several times more responses, or repeated ratings per display to average out the judge's noise.

## Bottom line
The data are sound, and the planned paired analysis gives a self-label effect of about +0.07 points, which is close to zero and not statistically significant. The pilot gives no evidence that atlas-7 favours its own label, but it is too small to show that the effect is absent.

HEADLINE_LABEL_EFFECT: 0.07
