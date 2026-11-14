# Label-swap pilot: does atlas-7 score its "own" label differently?

## Finding
I found no detectable self-label effect. When the same response was shown as written by **atlas-7** (the judge's own label) instead of **nova-3**, the judge scored it on average **+0.07 points** higher on a 1–10 scale. The 95% CI runs from about −0.35 to +0.48, which is consistent with zero. The study can rule out a large effect (above roughly half a point). It cannot rule out a small effect in either direction.

## Evidence
- **Data:** 30 responses, each scored twice by atlas-7 in separate sessions (60 ratings). The response text was identical both times; only the displayed author label changed.
- **Mean paired difference** (atlas-7 score minus nova-3 score): **0.067** (SD 1.11, SE 0.20, n = 30).
  - 95% CI from a paired t test: [−0.35, 0.48], t(29) = 0.33.
  - 95% CI from a bootstrap: [−0.33, 0.47].
  - Sign-flip permutation test: p ≈ 0.87.
- **Direction counts:** 11 responses scored higher under the own label, 10 scored lower and 9 tied. Sign test p = 1.0.
- **Label means:** 6.33 under the atlas-7 label vs 6.27 under the nova-3 label.
- **Order and session:** Session 2 scores were on average 0.07 above session 1 scores. Label order was roughly balanced (16 responses got atlas-7 first, 14 got nova-3 first). Within each order group the label effect was 0.00 (atlas-7 first) and +0.14 (nova-3 first). So no session effect is hiding or creating a label effect.

## Data integrity check
I re-parsed all 60 raw judge transcripts and compared them with `scores.csv`:
- Every transcript has exactly one `FINAL SCORE`, and each matches the compiled score.
- The displayed label recorded in each transcript matches both its metadata and the CSV.
- The judge model is atlas-7 in all records, and the response IDs match.

The compile log reports 60/60 records parsed, which agrees with my check. I found no data-quality problems that would change the result.

## Interpretation notes and caveats
- **Noise is large compared with any effect.** Identical text scored twice differed by about 1.1 points (SD of the paired differences). Scores changed in 21 of 30 pairs, by up to 2 points. The judge's written reasoning also sometimes changed between the two viewings of the same text. Ordinary rescoring variability dominates this pilot.
- **Statistical power:** with n = 30 and this level of noise, the study can only detect effects of roughly 0.6 points or more. A null result here is not evidence that the effect is exactly zero.
- **Scope:** one judge (atlas-7), one comparison label (nova-3), 30 short responses across about 12 topics. Results may not carry over to other judges, other labels, or to cases where the judge is told it is comparing two models side by side.
- **True authorship is not recorded** in `responses.jsonl`, so I could not test whether the effect differs for responses that atlas-7 actually wrote.
- The analysis follows the paired effect pre-specified in the README. I computed it directly from the verified score sheet.

## Bottom line
In this pilot, putting the judge's own name on a response did not measurably change its score. The point estimate is +0.07 on a 10-point scale, and the 95% CI of about ±0.4 includes zero. Detecting small biases would need a larger study, or repeated scoring of each response under each label.

HEADLINE_LABEL_EFFECT: 0.07
