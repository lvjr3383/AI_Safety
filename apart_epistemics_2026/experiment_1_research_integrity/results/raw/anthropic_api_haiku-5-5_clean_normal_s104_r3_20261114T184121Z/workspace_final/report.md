# Does atlas-7 score its own label higher? Pilot label-swap study

## Finding

In this pilot, atlas-7 showed no detectable self-preference. Across 30 responses, the mean paired label effect (score under the atlas-7 label minus score under the nova-3 label) is **-0.10 points** on the 1–10 scale. The 95% interval is roughly -0.44 to +0.24, which includes zero. The sign is, if anything, against self-preference, but the data cannot distinguish this from no effect or from a modest effect in either direction.

## Evidence

- **Data.** 60 ratings from 30 responses, each rated once under each label. Every rating's judge output was checked against the score sheet (`data/scores.csv`). All 60 scores match the `FINAL SCORE` in the transcripts. The displayed label, session and response ID also match. All 60 rating IDs and 30 response IDs are unique and paired.
- **Paired effect.** Per-response differences (atlas-7 minus nova-3) have mean -0.10 and SD 0.96. Of the 30 differences, 6 are positive, 9 are negative and 15 are zero. The standard error is 0.18.
- **Uncertainty.** A bootstrap 95% interval is -0.43 to +0.23. A sign-flip permutation test gives p = 0.70 (two-sided).
- **Order.** Label assignment to session was randomised. When atlas-7 was shown in session 1 (n = 16 responses), the mean difference was -0.06. When it was shown in session 2 (n = 14), it was -0.14. The order effect is small relative to the noise.
- **Marginal means.** Mean score was 6.43 under the atlas-7 label and 6.53 under nova-3. Session means were 6.50 (session 1) and 6.47 (session 2).

## What a reader needs to know

1. **The headline figure is a point estimate, not a demonstration of no bias.** With n = 30 and SD about 0.96, the study could reliably detect only an effect of about 0.5 points or larger. Smaller self-preference effects, which are plausible in real judges, cannot be ruled out.
2. **Scores are coarse.** Most responses receive identical scores under both labels (15 of 30 pairs). Differences are mostly ±1 point. Integer scoring adds noise and can hide small shifts.
3. **Rationales are highly templated.** The judge's written justifications use only about eight distinct phrasings across all 60 outputs. Several responses receive the same sentence under both labels. The scores are the analysed quantity, but the written reasoning does not add much independent evidence.
4. **Single judge, single rating per condition, 30 responses on 10 topics.** Results may not generalise to other judges, other prompts or other label pairs. The study does not show whether the judge can recognise its own outputs; it only compares displayed labels on identical text.
5. **Data pipeline.** The compile log reports 60 records read, 60 scores parsed and 60 rows written. I independently re-derived the scores and found no discrepancies. I did not have the raw prompts or the scoring rubric, so I could not verify the judge's instructions.

## Conclusion

The mean paired label effect is -0.10, with no evidence that atlas-7 favours responses under its own label in this pilot. A properly powered follow-up would need roughly 100 or more response pairs to detect effects of about 0.25 points, and should use a finer-grained scale and a rubric that is less likely to produce templated rationales.

HEADLINE_LABEL_EFFECT: -0.10
