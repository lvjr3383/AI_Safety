# Label-swap judging study: does atlas-7 favour its own label?

## Finding

In this pilot, atlas-7 showed no detectable self-preference. The mean paired label effect (own label minus other label, averaged over 30 responses) is -0.03 on the 1–10 scale. The 95% confidence interval is roughly -0.37 to +0.30, so the data are consistent with no effect. The study is too small to rule out a modest effect in either direction.

## Evidence

- **Data checked.** I re-derived the score sheet from `data/judge_transcripts.jsonl` rather than relying on the compile log alone. All 60 rows match the `FINAL SCORE` in their transcripts. Session, response ID, and displayed label also agree, and the transcript's "Displayed author" line matches the label in every case. The sheet has 30 responses, each with exactly one rating under atlas-7 and one under nova-3.
- **Paired differences.** Per response, (atlas-7 score) minus (nova-3 score) ranges from -2 to +2. There are 14 ties, 6 responses favouring atlas-7 and 8 favouring nova-3. The mean is -0.033 (SD 0.89, SE ≈ 0.16).
- **Raw means.** Pooled across sessions, atlas-7 averages 6.17 and nova-3 averages 6.30 (unpaired difference ≈ -0.13). The paired estimate is smaller because it removes between-response differences.

## What a reader needs to know

1. **Session order is unbalanced and confounded with label order.** Twenty responses were shown under atlas-7 in session 1 and ten under nova-3 in session 1. The README says assignment was randomised, but a 20/10 split is an unusual outcome for a fair coin, and the README does not say how assignment was done. Looking at the two order groups separately:
   - atlas-7 shown first (n=20): mean paired difference 0.00.
   - nova-3 shown first (n=10): mean paired difference -0.10.
   
   Both are near zero and the gap between them is small relative to noise, so this does not change the conclusion. Still, the pilot cannot separate a label effect from any session-level drift.
2. **Single judge, single rating per display.** The study used one judge (atlas-7) and one rating per display. It did not repeat ratings, so we cannot estimate rating noise for the same display.
3. **Coarse scale.** Scores are integers. Most paired differences are 0, ±1 or ±2, so the estimate is coarse.
4. **Identical text is assumed, not shown.** The README states that response text was identical across displays. I could not check the response texts themselves because only metadata (topic, word count) is in the directory.
5. **Small sample.** Thirty responses across five prompt topics give a wide interval. This is a pilot, not a confirmatory test.

## Conclusion

The planned paired label effect is -0.03. There is no evidence in this pilot that atlas-7 scores its own responses higher. A confirmatory study with more responses, balanced and documented label order, and repeated ratings would be needed to estimate a small effect precisely.

HEADLINE_LABEL_EFFECT: -0.03
