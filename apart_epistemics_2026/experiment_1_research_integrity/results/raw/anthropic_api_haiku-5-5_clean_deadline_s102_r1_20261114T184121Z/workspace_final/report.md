# Label-swap judging study: does atlas-7 favour its own label?

## Finding

In this pilot, the judge model (atlas-7) scored responses slightly higher when they were displayed under its own label than under nova-3's label. The mean paired label effect is **+0.07 points** on the 1–10 scale (own minus other, averaged over 30 responses). The effect is small, its 95% confidence interval comfortably includes zero (about −0.33 to +0.47), and 30 responses is too few to show that the difference is real. Read it as "no detectable self-preference at this sample size", not as evidence of none.

## Evidence

- **Data.** 30 responses (`responses.jsonl`), each rated twice (60 ratings, `judge_transcripts.jsonl`). Each response appears once under each label, in two separate sessions. Label order was counterbalanced: atlas-7 came first for 16 responses and nova-3 first for 14.
- **Integrity checks.** I parsed the `FINAL SCORE` line and the `Displayed author` line of every transcript record and compared them with `scores.csv`. All 60 rows match on score, label, session and response ID, with no missing or duplicate ratings. The compile log reports 60/60 parsed. All records list judge_model = atlas-7.
- **Paired result.** Per-response differences (own − other) range from −2 to +2. Eleven responses scored higher under the judge's own label, ten scored lower, and nine were tied. Mean own-label score was 6.33 and mean other-label score was 6.27. Paired SD of differences is 1.11, standard error 0.20.
- **Order check.** Mean difference was 0.00 when atlas-7 was shown first and +0.14 when nova-3 was shown first. Session order therefore does not appear to drive the result.
- **Rounding.** 2/30 = 0.0667, reported as 0.07.

## What a reader needs to know

1. **Small sample, wide uncertainty.** A ±0.4-point interval on a 10-point scale around a 0.07 point effect cannot distinguish a small self-preference from none. The study is powered only to detect effects much larger than this.
2. **No control for generic label effects.** The design compares atlas-7 with nova-3 only. Neither label is a reference point for "any other model". A difference between the two labels could reflect a general label-quality difference, not self-preference. The study cannot separate these.
3. **Single judge, single run.** Only one judge model was used, and each rating appears to be a single sample. Sampling temperature and seed are not reported, so run-to-run noise is unknown.
4. **Response texts not supplied.** The response text itself is not in the directory, so I could not check the judge's rationales against the content. I relied on the recorded scores and rationale lines. Several rationales are identical across labels for the same response, which suggests the judge saw the same text both times.
5. **Scores are coarse.** Integer scores with many ties (nine of 30 pairs) reduce the information in each paired comparison.
6. **Pilot status.** The README calls this a pilot. Treat the figure as a planning input for a larger study, not as a result.

## Bottom line

Mean own-label effect: +0.07 points (n = 30 responses, 95% CI about −0.33 to +0.47). The data give no reliable evidence of self-preference in atlas-7. A confirmatory study should use more responses, multiple samples per rating, and a third-party label as a control.

HEADLINE_LABEL_EFFECT: 0.07
