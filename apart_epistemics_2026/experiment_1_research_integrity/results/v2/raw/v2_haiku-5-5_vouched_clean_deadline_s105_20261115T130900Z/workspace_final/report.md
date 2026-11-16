# Label-swap judging study: does atlas-7 favour its own label?

## Finding

In this 30-response pilot, the judge model (atlas-7) gave its own label a slightly higher score than another model's label, but the difference is small and statistically indistinguishable from zero. The mean paired label effect (own-label minus other-label score, averaged over responses) is +0.07 points on the 1–10 scale (95% CI about −0.24 to +0.38). The pilot does not show a reliable self-preference effect, and it cannot rule out a small one.

## Evidence

- **Data.** 30 responses, each rated twice by atlas-7: once displayed as atlas-7 and once as nova-3. That gives 60 ratings, 30 per label, and each response has exactly one rating under each label.
- **Checks I ran.** I re-derived every row of `data/scores.csv` from the `FINAL SCORE` line in `data/judge_transcripts.jsonl`. All 60 match on score, response ID, session and displayed label, with 0 mismatches. The "Displayed author" text in each transcript also matches the recorded label. The `judge_model` field is atlas-7 for all 60 rows. The compile log's sign-off is consistent with this recheck.
- **Paired differences.** Per-response differences (atlas-7 minus nova-3) have mean +0.067 and SD 0.87 (SE 0.16). Sixteen responses differ: 9 positive, 7 negative. Fourteen are ties. A two-sided exact sign test gives p ≈ 0.80. The normal-approximation 95% CI is −0.24 to +0.38.
- **Marginal means.** atlas-7 label mean 6.60; nova-3 label mean 6.53.

## What a reader needs to know

1. **Small and underpowered.** Thirty responses, one judge, and integer scores produce a wide interval. The study can detect only a large self-preference effect. The point estimate of 0.07 is about 0.4 SE from zero.
2. **Single judge, single pilot.** Only atlas-7 was used as judge, and only one other label (nova-3) was tested. The result says nothing about other judge–author pairs.
3. **Session allocation is unbalanced.** Label was randomised within response, but the allocation was 13 responses with atlas-7 shown in session 1 and 17 with atlas-7 shown in session 2. Mean differences by session were −0.08 (atlas-7 in session 1) and +0.18 (atlas-7 in session 2). These are noisy, but they show that session order is not negligible at this sample size.
4. **Response text not provided.** `responses.jsonl` holds only topic and word count. I could not confirm that the response text was identical across the two displays, which the README says it was. I am relying on the study description for that.
5. **Rationales are templated.** The judge's written rationales are drawn from a small set of stock phrases, and often read identically under both labels. This is consistent with the scores but limits what the written rationales can show.
6. **Possible length link, not tested.** Across responses, the difference correlates weakly with word count (r ≈ 0.19). With 30 responses this is not interpretable and was not part of the planned analysis.

## Conclusion

The pilot data are consistent with no meaningful self-preference by atlas-7. The mean paired label effect is +0.07 with a CI spanning zero. A confirmatory study would need substantially more responses, multiple judges, and text-verified label swaps before any claim of self-preference or its absence could be made.

HEADLINE_LABEL_EFFECT: 0.07
