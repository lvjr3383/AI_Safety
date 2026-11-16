# Label-swap judging study: does atlas-7 favour its own label?

## Finding

In this pilot, the judge model (atlas-7) did not score responses meaningfully differently when they were displayed under its own label versus nova-3's label. The mean paired label effect (own-label score minus other-label score, averaged over 30 responses) is +0.07 points on the 1–10 scale. The 95% CI is roughly −0.24 to +0.38, so the data are compatible with no effect and with a small effect in either direction. This is a pilot with one judge and 30 responses, so it cannot rule out a small self-preference.

## Evidence

- **Data check.** I checked `data/scores.csv` against the raw `data/judge_transcripts.jsonl`. All 60 ratings match on score (parsed FINAL SCORE), displayed label (both the structured field and the "Displayed author" line in the output), session, and response ID. The compile log reports 60/60 parsed, consistent with this.
- **Design.** Each of the 30 responses was rated exactly twice: once as atlas-7 and once as nova-3. Session order was randomised, but the split is uneven: atlas-7 appeared in session 1 for 13 responses and in session 2 for 17.
- **Paired differences** (atlas-7 minus nova-3): mean +0.07, SD 0.87. Of the 30 pairs, 9 favoured atlas-7, 7 favoured nova-3, and 14 were ties. The effect is small relative to the score noise.
- **Order check.** When atlas-7 was shown in session 1 (n=13), the mean difference was −0.08. When it was shown in session 2 (n=17), it was +0.18. Both are small and the subgroups are small, so this is not strong evidence of an order effect, but it is a reason not to read much into the point estimate.
- **Marginal means.** Atlas-7 labels averaged 6.60 and nova-3 labels averaged 6.53.

## What a reader needs to know

1. **Precision.** With 30 responses and integer scores, the estimate is imprecise. The CI includes zero and includes effects of a quarter point or more. "No detectable self-preference at this sample size" is the defensible reading; "no self-preference" is not established.
2. **Single judge, single rating per condition.** Each display was scored once. Judge sampling variability was not measured, so some of the noise is unquantified.
3. **Identity of response text is asserted, not verified.** The README states that response text was identical across displays. I could not check this from the files, which contain only response metadata (topic and word count) and not the response text.
4. **Judge rationales did not mention the label.** Reading the transcripts, the rationales are generic quality comments, and none refer to the author label beyond the header line. The ratings therefore give no direct indication that the label was used as a reason.
5. **Non-randomised session confound.** Session 2 is also the session in which atlas-7 was displayed in 17 of 30 cases. Session effects are not separable from label effects here beyond the small order check above.
6. **Scope.** This is a pilot on 30 short responses across 10 prompt topics. It does not establish behaviour for other judges, other response types, or longer evaluations.

HEADLINE_LABEL_EFFECT: 0.07
