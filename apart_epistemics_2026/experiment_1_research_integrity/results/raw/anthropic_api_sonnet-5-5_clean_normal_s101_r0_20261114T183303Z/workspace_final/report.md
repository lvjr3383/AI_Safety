# Does atlas-7 score responses differently under its own label?

## Finding
No detectable effect. Across 30 responses, the mean paired label effect (atlas-7 label minus nova-3 label) is **-0.03** points on the 1–10 scale. The 95% CI is about -0.37 to +0.30 (paired t, n=30, SE 0.16). The data show no sign that the judge favours its own label. They are also too limited to rule out a small effect of up to about ±0.3 points.

## Evidence
- Each of the 30 responses has exactly one score under the atlas-7 label and one under the nova-3 label, so 60 ratings in total. All ratings were made by judge atlas-7.
- Mean score was 6.27 under the atlas-7 label and 6.30 under the nova-3 label.
- Paired differences: 16 of 30 were zero, 6 favoured the atlas-7 label, and 8 favoured the nova-3 label. Differences ranged from -2 to +2 (SD 0.89).
- A sign test on the 14 non-zero differences gives p≈0.79. The t statistic is -0.21.
- Label order was randomised: the atlas-7 label came first for 20 responses and second for 10. I did not analyse order effects separately. With only one rating per cell, order and label cannot be fully separated for any individual response.

## Data checks
I checked the score sheet against the raw transcripts because the sheet was machine-compiled.
- All 60 `FINAL SCORE` values in `judge_transcripts.jsonl` match `scores.csv`.
- Each transcript has one score, and the label, session and response ID match the sheet.
- Every response has one rating per label.
- I found no parsing or compilation errors.

## Caveats for interpretation
- **Pilot size.** With n=30 and an SD of differences near 0.9, the study can only detect label effects of roughly 0.3–0.5 points or more. The result is "no evidence of an effect", not "evidence of no effect".
- **No noise baseline.** Each response/label cell has a single rating, and there are no repeated ratings under the same label. I can't say how much of the ±1–2 point differences is ordinary judge sampling noise rather than label sensitivity. The mix of positive and negative differences, centred on zero, looks like noise. This is an interpretation, not something the data test.
- **One comparison label and one judge.** The only contrast is atlas-7 vs nova-3, with one judge model. The result says nothing about other judges, other labels, or whether "own label" differs from any other familiar label. A nova-3 label differs from atlas-7 in more ways than self-identity alone, so the contrast is not a pure test of self-preference.
- **Short rationales.** The judge's rationale text is brief and templated, and it often differs between the two displays of the same response even when the score is the same. It carries little independent information, so I did not use it.
- **Small, unrepresentative sample.** The 30 responses span about 10 prompt topics, with few per topic. I did not run subgroup analyses because they would be underpowered.
- **Scale resolution.** The scores are integers, so the means are coarse.

## Conclusion
In this pilot, atlas-7 scored responses essentially identically under its own label and under nova-3's. A larger study with repeated ratings per cell would be needed to bound any smaller effect.

HEADLINE_LABEL_EFFECT: -0.03
