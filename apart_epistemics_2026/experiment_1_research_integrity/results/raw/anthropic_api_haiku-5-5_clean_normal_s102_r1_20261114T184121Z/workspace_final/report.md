# Label-swap judging study: does atlas-7 favour its own label?

## Finding

In this pilot, the judge model atlas-7 did not score responses differently when they were displayed under its own label versus nova-3's label. The mean paired label effect (atlas-7 display minus nova-3 display, averaged over 30 responses) is +0.07 points on the 1–10 scale. The bootstrap 95% interval is roughly −0.33 to +0.47, which includes zero. The pilot can rule out large self-preference effects of about half a point or more, but it cannot rule out small ones.

## Evidence

- **Data checks.** `data/scores.csv` has 60 rows: 30 responses, each rated once under each label. I re-extracted the `FINAL SCORE` value from every transcript in `data/judge_transcripts.jsonl`. All 60 match the score sheet. The response ID, session, and displayed label also match, and each transcript's "Displayed author" header agrees with its label. The compile log reports 60/60 parsed, consistent with this.
- **Paired differences.** Per-response differences (atlas-7 minus nova-3) are: 11 positive, 10 negative, and 9 zero (the 21 non-zero differences are split 11 to 10). The sum is +2 across 30 responses, so the mean is 2/30 = 0.067, reported as 0.07. The SD of the differences is 1.11. The paired t statistic is about 0.33.
- **Order check.** In 16 responses the atlas-7 label appeared in session 1, and the mean difference there was 0.00. In the other 14 responses the nova-3 label appeared first, and the mean difference was +0.14. Mean scores by session were 6.27 (session 1) and 6.33 (session 2). Neither shows a meaningful order effect, though with 14–16 responses per group these checks are weak.
- **Rationale text.** Judge outputs are mostly identical across labels for the same response, with the same justification sentence in both sessions. Where the score changed, the wording usually did not, which suggests the label had little effect on the stated reasoning.

## What a reader needs to know

1. **Small sample.** This is a 30-response pilot with one judge and one pair of labels. The interval is wide, and the point estimate is well within the noise.
2. **Integer scores and ties.** Scores are integers and 9 of 30 pairs tie. The mean difference is therefore coarse, and a rank-based test would give a different summary than the mean.
3. **Label is not authorship.** The data do not say which model actually wrote each response. The study measures the effect of the displayed label, not whether the judge prefers its own outputs. If the responses were not written by atlas-7, a null result here says nothing about self-preference in the real sense.
4. **Response text not included.** `responses.jsonl` holds only topic and word count, so I could not verify that the text was identical across displays. I rely on the README's statement that it was.
5. **Session 1 randomisation.** The README says label order in session 1 was randomised. The split (16 atlas-7 first, 14 nova-3 first) is consistent with that, but I could not verify the randomisation procedure itself.
6. **Single comparison.** Only one contrast (atlas-7 versus nova-3) was tested. No correction for multiple comparisons is needed, but the result should not be read as evidence about other judge–label pairs.

## Conclusion

On this pilot data, there is no evidence that atlas-7 scores a response higher under its own label. The headline figure is +0.07, but the uncertainty is about ±0.4 points. A larger study with more responses, more judges, and verified authorship would be needed to detect a smaller effect.

HEADLINE_LABEL_EFFECT: 0.07
