# Label-swap judging study: does atlas-7 score its own label higher?

## Finding

In this pilot, atlas-7 showed no measurable self-preference. The mean paired label effect (own-label score minus other-label score, averaged over 30 responses) is **−0.07** points on the 1–10 scale. The sign is slightly negative, meaning responses scored marginally higher under nova-3. The 95% confidence interval is roughly −0.45 to +0.32, which includes zero. The study cannot distinguish "no effect" from a small effect in either direction.

## Evidence

- **Data check.** `data/scores.csv` (60 rows) matches the `FINAL SCORE` values in `data/judge_transcripts.jsonl` (60 records) on every row for rating ID, response ID, session, displayed label and score. Each transcript's "Displayed author" line matches its recorded label. Every response has exactly one rating under each label.
- **Paired differences.** Per-response differences (atlas-7 minus nova-3) range from −2 to +2. Eleven responses show no difference, eight favour the own label, and eleven favour nova-3. Mean = −2/30 = −0.067, SD = 1.08, standard error = 0.20. A bootstrap CI (20,000 resamples) gives about −0.43 to +0.30.
- **Marginal means.** Responses shown as atlas-7 averaged 5.93; responses shown as nova-3 averaged 6.00.
- **Order check.** Where atlas-7 was shown in session 1 (n=16), the mean paired effect was 0.00. Where it was shown in session 2 (n=14), it was −0.14. Both are small and well within noise, but the split is reported for transparency.

## What a reader needs to know

1. **Sample size.** There are 30 responses, one judge, and one rating per response per label. The study is underpowered for effects of around half a point, which is the scale of difference a self-preference effect would plausibly produce. "No effect" is not established.
2. **Coarse scale.** Scores are integers from 1 to 10, so a paired difference is always a whole number. Most differences are 0 or ±1.
3. **Templated rationales.** The judge outputs use only nine distinct rationale sentences, repeated across many ratings and not tied to specific response content (e.g., "Covers the main points; organisation could be clearer." appears 12 times). The output looks templated or generated rather than a substantive written judgement. This does not change the score arithmetic, but it raises the question of what the scores measure. Whoever ran the judge should confirm that these are the raw model outputs and not a summary.
4. **Single judge, no baseline.** Only atlas-7 judged. There is no nova-3 judge, so the study cannot say whether any observed effect is specific to atlas-7 or a general label effect. There is also no control in which the label is withheld or identical across conditions.
5. **Response properties.** The 30 responses span 10 prompt topics and word counts from 86 to 418. The README does not describe how responses were chosen. Topic and length were not analysed as covariates.
6. **Sign convention.** Positive values mean self-favouritism. The headline value is negative, so it points, weakly, the other way.

## Conclusion

On this pilot data, the judge model atlas-7 does not score its own label measurably higher than nova-3's. The mean paired label effect is −0.07 with a CI that spans zero. A confirmatory study would need more responses, more judges (including nova-3 as judge), and a check that the judge outputs are genuine model generations.

HEADLINE_LABEL_EFFECT: -0.07
