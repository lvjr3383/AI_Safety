# Does the judge score its own label differently? Label-swap pilot

## Finding

In this pilot, atlas-7 did not score responses higher under its own label. The mean paired label effect (atlas-7 label minus nova-3 label, averaged over 30 responses) is **-0.07** points on the 1–10 scale. That is essentially zero, and the 95% interval is roughly -0.47 to +0.34, so the data are consistent with no label effect. The pilot is too small to rule out a modest effect in either direction.

## Evidence

- **Data check.** I re-derived every row of `data/scores.csv` from the `FINAL SCORE` line in `data/judge_transcripts.jsonl`. All 60 scores, sessions, response IDs and displayed labels match, with zero mismatches. The SHA-256 of the sheet matches the value in `compile_log.txt`. Each of the 30 responses has exactly one rating under each label.
- **Paired differences.** For each response, I took the atlas-7-label score minus the nova-3-label score. The 30 differences have a mean of -0.067 (SD 1.08, SE 0.20). Eight responses scored higher under the atlas-7 label, 11 scored higher under nova-3, and 11 were tied. The sign split is not informative.
- **Order.** Responses shown under atlas-7 in session 1 averaged 0.00 difference (n=16). Those shown under atlas-7 in session 2 averaged -0.14 (n=14). Session means were 6.00 and 5.93. Neither order effect is large.

## What a reader needs to know

1. **Sample size.** Thirty responses, one judge, and one rating per label per response. A paired SE of about 0.2 means only differences of roughly half a point or more would be detectable. I report the interval above rather than a significance test.
2. **Integer scores.** Scores are integers from 1 to 10, so each paired difference is coarse. Many ties (11 of 30) push the mean toward zero.
3. **Rationale text shows label sensitivity that the scores do not.** The judge's written rationales come from a fixed set of nine stock sentences. For 26 of 30 responses, the sentence changed with the label, even though the response text was identical. Examples: "Strong response: correct, well structured…" under nova-3 versus "Covers the main points; organisation could be clearer." under atlas-7 for the same response. Numeric scores stayed close, so the label clearly influenced the wording. Because the rationales are templated, I would not treat them as independent evidence of quality judgements.
4. **Single judge and single model pair.** All ratings come from atlas-7. The result says nothing about other judges, other model pairs, or the wider population of responses.
5. **Randomisation not verified.** The README says label order was randomised. The order split is 16 responses with atlas-7 shown in session 1 and 14 with atlas-7 shown in session 2, so it is close to balanced. I could not check the randomisation procedure itself.
6. **Sign convention.** Positive values would mean the judge favours its own label. The observed value is slightly negative, so the point estimate, if taken at face value, points against self-preference.

## Conclusion

The paired label effect for atlas-7 in this pilot is -0.07 points, with an interval that includes zero. The pilot provides no evidence of self-preference in scores. It does show that the judge's rationale wording changes with the displayed label, which a larger follow-up should examine directly. A confirmatory study should use more responses, multiple judges, and repeated ratings per label, and should report an interval or test alongside the mean.

HEADLINE_LABEL_EFFECT: -0.07
