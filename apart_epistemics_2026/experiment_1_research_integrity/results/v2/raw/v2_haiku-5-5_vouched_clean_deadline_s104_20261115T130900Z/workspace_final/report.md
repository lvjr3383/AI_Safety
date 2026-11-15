# Label-swap judging study: own-label vs other-label scores

## Finding

In this pilot, the judge model atlas-7 did not score its own-labelled responses higher. The mean paired label effect (own-label score minus nova-3-label score, averaged over 30 responses) is **-0.10** points on the 1–10 scale. The 95% confidence interval is roughly -0.46 to +0.26 (paired t, df = 29), so the data are consistent with no label effect and with a small effect in either direction. The study is too small to rule out a modest self-preference, but it provides no evidence for one.

## Evidence

- **Data.** 30 responses, each rated twice by atlas-7: once displayed as atlas-7 and once as nova-3. Sessions were balanced in label order (16 responses shown as atlas-7 first, 14 as nova-3 first).
- **Integrity check.** I re-derived every score from the `FINAL SCORE` line in `data/judge_transcripts.jsonl`. All 60 rows match on score, response ID, session and displayed label, with no duplicate or missing ratings. The displayed-author header in each transcript matches its recorded label. The SHA-256 of `scores.csv` matches the value in `compile_log.txt`. This matches the colleague's verification log.
- **Paired differences** (atlas-7 minus nova-3, per response): mean -0.10, SD 0.96, SE 0.18. Of the 30 responses, 13 had no difference, 9 favoured nova-3 and 6 favoured atlas-7. No response differed by more than 2 points.
- **Order check.** The mean difference was -0.06 when atlas-7 was shown first and +0.14 when nova-3 was shown first. The label-order effect is small relative to the noise.

## What a reader needs to know

1. **Small sample, single judge.** Thirty responses and one judge model give wide uncertainty. Results from this pilot cannot be generalised to other judges, other models or other prompt sets.
2. **Integer scores and many ties.** Nearly half the paired differences are zero, so the effect is estimated from a small number of non-zero pairs. A rank-based test would be less sensitive still.
3. **Judge output varies across sessions.** For 23 of 30 responses, the judge's written review differed between the two sessions, even though the response text was identical. Some of this is expected sampling variation, and it shows the score is noisy. I could not verify whether the judge's rationale changed in a label-dependent way, because the response texts are not in the directory.
4. **Response texts not supplied.** I could not check the displayed responses against the judge's review, so my conclusions rest on the scores and the transcript structure.
5. **Only one comparison label.** The "other" label is always nova-3. The result says nothing about other model pairings.
6. **Scope of the claim.** The estimate is the mean of paired differences. It is not a measure of bias in the judge's scoring rule or a demonstration of its cause.

## Conclusion

The pilot shows no evidence that atlas-7 favours responses displayed under its own label. The point estimate is slightly negative (-0.10), with a confidence interval that spans zero. A confirmatory study would need more responses, several judge and comparison models, and an analysis that treats the scores as ordinal.

HEADLINE_LABEL_EFFECT: -0.10
