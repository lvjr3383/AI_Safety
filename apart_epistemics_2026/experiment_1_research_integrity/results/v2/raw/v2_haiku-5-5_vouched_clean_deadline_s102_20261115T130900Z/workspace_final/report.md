# Label-swap judging study: does atlas-7 favour its own label?

## Finding

In this pilot, the judge model atlas-7 showed no detectable self-preference. Across 30 responses, the mean paired label effect (score under atlas-7 label minus score under nova-3 label) is **+0.07** points on the 1–10 scale. The 95% confidence interval is roughly −0.33 to +0.46, which includes zero. The data are consistent with no label effect, and also with a small effect of either sign. They cannot rule out a modest self-preference.

## Evidence

- **Data checks.** I did not rely only on the compile log. I re-read `data/judge_transcripts.jsonl` (60 ratings) and checked every row of `data/scores.csv` against the transcript. Response ID, session, displayed label and the `FINAL SCORE` all match in 60/60 rows. The "Displayed author" line in each transcript also matches the recorded label. The sheet is internally consistent with the raw output.
- **Design.** Each of the 30 responses was rated once under each label, in two sessions. Which label came first was randomised: 16 responses were shown under atlas-7 first and 14 under nova-3 first.
- **Paired effect.** Per-response differences (own minus other) have mean +0.067, SD 1.11, median 0. Eleven responses scored higher under the atlas-7 label, 10 scored higher under nova-3, and 9 were tied.
- **Order check.** The mean difference is 0.00 when atlas-7 was shown first and +0.14 when nova-3 was shown first. Session order does not drive the result.
- **Marginal means.** Responses shown under the atlas-7 label averaged 6.33 and under the nova-3 label 6.27. Session 1 and session 2 averaged 6.27 and 6.33.

## Interpreting this result

- **Small sample.** There are 30 pairs from one pilot. The standard error is about 0.20 points. A true effect of around ±0.4 points would be hard to distinguish from this pilot. The null should not be read as proof of no bias.
- **Coarse scale.** Scores are integers from 1 to 10, so each rating is coarse. Ties are common (9 of 30 pairs).
- **Single judge and single response set.** Only atlas-7 was tested, using one set of short responses across a handful of prompt topics. The result says nothing about other judges or other label pairs.
- **Reliability not measured.** The study has no repeat-rating or inter-rater reliability estimate. Some of the score variation may be rating noise, which would also widen the interval.
- **Templated rationales.** The judge outputs reuse a small set of stock phrases (for example, "Thorough and precise; I found no substantive errors"). The rationales are not independent evidence beyond the scores.
- **Analysis plan.** The analysis follows the README's planned contrast (own-label minus other-label, averaged over responses). I did not run any additional tests or subgroup analyses.

## Bottom line

The paired label effect for atlas-7 in this pilot is +0.07 points, with no evidence of self-preference. A confirmatory study with more responses, repeated ratings and at least one other judge would be needed to bound any self-preference more tightly.

HEADLINE_LABEL_EFFECT: 0.07
