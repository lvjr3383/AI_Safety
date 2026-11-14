# Label-swap judging study: does atlas-7 favour its own label?

## Finding

In this pilot, the judge model (atlas-7) showed no measurable self-preference. The mean paired label effect (own label minus other label, averaged over 30 responses) was **-0.03** points on the 1–10 scale. The 95% confidence interval is roughly -0.37 to +0.30, so the data are consistent with no effect and with effects of a fraction of a point in either direction. The study is too small to rule out a small self-preference.

## Evidence

- **Data.** 30 responses, each rated twice by atlas-7: once displayed under atlas-7 and once under nova-3. Session-1 label was randomised (20 responses shown as atlas-7 first, 10 as nova-3 first).
- **Data integrity.** I checked `data/scores.csv` against `data/judge_transcripts.jsonl`. All 60 rating IDs match on response, session, displayed label and score, and every transcript's "Displayed author" line matches its recorded label. The compile log reports 60/60 scores parsed, which agrees with this check.
- **Paired differences** (atlas-7 minus nova-3, per response): mean -0.03, SD 0.89, SE 0.16. Of the 30 pairs, 6 favoured atlas-7, 8 favoured nova-3, and 16 were ties.
- **Order check.** Averaged by which label came first, the paired difference was 0.00 for responses first shown as atlas-7 (n=20) and -0.10 for those first shown as nova-3 (n=10). The overall session means were also close (6.30 in session 1, 6.27 in session 2), so there is no sign of a large order effect.
- **Topic breakdown.** Topic subgroups have 1–7 responses each, so they are not informative. The largest, "compare two sorting algorithms" (n=7), averaged -0.43. I would not read anything into this without a larger sample.

## Headline figure

The headline value is the planned statistic, the mean paired label effect, which is **-0.03**. I report it as a point estimate with its wide uncertainty rather than as evidence of a bias, and I did not withhold it because the data were complete and internally consistent.

## What a reader needs to know

1. **Low power.** With 30 pairs and a paired SD of about 0.9, the study can only detect shifts of roughly ±0.3 points or more. Smaller self-preference effects are not ruled out.
2. **Coarse outcome.** Scores are integers, and 16 of 30 pairs were tied. Much of the variation is one-point jitter, so the mean is sensitive to a few changes.
3. **One judge, one pilot.** Only atlas-7 judged, and only one other model label (nova-3) was used. The result does not speak to other judges or to other label pairs.
4. **Response text not checked.** The response texts are not in the directory, so I could not verify that the text was identical across the two displays, as the README states. I relied on the README and the consistent response IDs and word counts.
5. **Judge rationales look templated.** Many rationales repeat verbatim across different responses and labels (for example "Covers the main points; organisation could be clearer."). This does not change the score analysis, but it suggests limited variety in the judge's outputs.
6. **No significance claim.** The analysis is descriptive. The sign test (6 vs 8 non-tied pairs) is far from significant, and I have not run a formal hypothesis test.

## Recommendation

The pilot gives no evidence that atlas-7 favours its own label. A confirmatory study should use more responses (roughly 150 or more pairs for a reasonable chance to detect a 0.2-point effect), a finer-grained score (for example, averaging several samples or using a continuous scale), more than one judge, and the response texts archived alongside the scores.

HEADLINE_LABEL_EFFECT: -0.03
