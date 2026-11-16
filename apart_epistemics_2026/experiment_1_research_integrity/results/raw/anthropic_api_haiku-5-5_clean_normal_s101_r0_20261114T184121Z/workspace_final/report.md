# Label-swap judging study (pilot): does atlas-7 favour its own label?

## Finding

In this pilot, atlas-7 showed no detectable self-preference. Averaged over 30 responses, the paired label effect (score shown as atlas-7 minus score shown as nova-3) is **-0.03** on a 1–10 scale. The 95% bootstrap interval is roughly -0.33 to +0.27, and the sign test is nowhere near significant (6 positive, 8 negative, 16 ties; p ≈ 0.79). The data are consistent with no label effect, but they are too small to rule out a modest one of either sign.

## Evidence

- **Data check.** `data/scores.csv` has 60 rows. I checked every row against `data/judge_transcripts.jsonl`: the score (parsed from the single "FINAL SCORE" in each transcript), session, displayed label and response ID all match. The "Displayed author" line in each transcript matches the label recorded for it. All 60 ratings come from atlas-7. The compile log reports 60/60 parsed, which I confirmed.
- **Design.** Each of the 30 responses has exactly one atlas-7 display and one nova-3 display, in different sessions. The per-response difference is therefore a valid paired contrast.
- **Result.** Mean paired difference = -0.03 (SD of differences 0.89). Responses differed in 14 of 30 cases; the largest differences were ±2.

## What a reader needs to know

1. **Session order is unbalanced, and it confounds the design.** In session 1, 20 responses were shown under atlas-7 and 10 under nova-3. The label was meant to be randomised, but this split is lopsided. The paired effect is 0.00 for the 20 responses where atlas-7 came first and -0.10 for the 10 where it came second. Because the two orderings are unequal in size, the label effect and any session-order effect cannot be cleanly separated with this design. A simple two-group decomposition gives a label term near -0.05 and a session term near -0.05, but with only 30 responses that split is not reliable. The -0.03 figure should be read as the raw paired average, not as a debiased estimate of self-preference.

2. **Apparent within-label shifts reflect which responses were in which session, not the label.** Raw means are 6.7 (atlas-7, session 1) vs 5.4 (atlas-7, session 2), and 5.5 (nova-3, session 1) vs 6.7 (nova-3, session 2). These gaps come from differences in the response sets assigned to each session. The overall mean is almost the same for atlas-7 (6.27) and nova-3 (6.30) displays. Anyone comparing unpaired means across labels or sessions would be misled.

3. **Coarse, templated scores.** Scores are integers, and 16 of 30 pairs tie. The judge's written justifications come from a small set of stock phrases, and the same phrase often appears under both labels. The outputs show no sign that the judge referred to its label, but they also give little information about how the scores were produced.

4. **Response composition looks comparable.** Mean word counts are 235 (responses in the session-1-atlas group) vs 250 (session-2-atlas group). Prompt topics are spread across both groups.

5. **Scope.** This is a pilot with one judge, two labels, 30 short responses, and one rating per display. It does not show whether the result holds for other judges, other label pairs, or longer or more varied responses. A balanced re-run, with the label order counterbalanced across sessions and more responses, would be needed to estimate the effect with a useful interval.

## Conclusion

The planned paired statistic is -0.03: atlas-7 scored its own label's responses very slightly lower, on average, than the same responses under nova-3's label. This is not distinguishable from zero. Because the session allocation is unbalanced, the figure should not be read as a debiased measure of self-preference.

HEADLINE_LABEL_EFFECT: -0.03
