# Label-swap judging study: does atlas-7 favour its own label?

## Finding
The data show no detectable self-label effect. When the same response was shown under atlas-7's own label rather than under nova-3's, atlas-7 gave it on average **+0.07 points** more on the 1–10 scale (n = 30 paired responses). That difference is small and well within noise. The 95% interval runs from about −0.23 to +0.37, so the data cannot tell this apart from zero. They do rule out a large bias (around half a point or more) in either direction.

## Evidence
- **Data integrity checked first.** I re-extracted the `FINAL SCORE` from all 60 raw judge transcripts and compared each against `scores.csv`. All 60 match on score, response ID, session and displayed label. Every transcript names atlas-7 as the judge, and each one's "Displayed author" line matches its recorded label. Every response has exactly one rating under each label. The compile log (60/60 parsed) agrees with this.
- **Paired differences** (own-label score minus other-label score, per response): 9 positive, 7 negative, 14 zero. The values range from −2 to +2, with mean 0.067 and SD 0.87.
- **Tests:** paired t = 0.42; sign-flip permutation test p ≈ 0.83; exact sign test (zeros dropped) p ≈ 0.80; bootstrap 95% CI for the mean is [−0.23, +0.37].
- **Order/session:** the README says label assignment to session was randomised. The split came out uneven: atlas-7's label was shown in session 1 for 13 responses and in session 2 for 17. Across sessions, scores ran about 0.13 points higher in session 2 than in session 1, which is also not significant. Allowing for this order effect gives a label effect of about +0.05, which leaves the conclusion unchanged.

## Interpretation notes and limitations
- **The judge is noisy from one rating to the next.** Nearly half of the responses (16 of 30) got different scores across the two displays, and the written reasons often differ even when the score is the same. For example, resp-001 was called "one minor inaccuracy" under its own label and "follows every constraint" under nova-3's. The study never shows the same response twice under the *same* label, so we can't separate a true label effect from ordinary re-rating variability. We can only say that any label effect is small compared with that variability.
- **Small pilot.** With 30 pairs and an SD of about 0.87, the study can only reliably detect effects of roughly ±0.45 points or more. A real bias of 0.1–0.3 points could easily be missed. "No significant effect" should not be read as "no effect".
- **Scope.** There is one judge (atlas-7), one comparison label (nova-3), and scores are coarse integers. The files don't say which model actually wrote each response. So these results say nothing about whether atlas-7 prefers its *own outputs* (self-preference by style). They speak only to the effect of the *displayed label*.
- **Planned analysis followed.** The headline figure is exactly the README's pre-specified statistic: the mean, over responses, of (score displayed as atlas-7) minus (score displayed as nova-3). Computed from the verified scores, it is 0.0667, which rounds to 0.07.

## Bottom line
In this pilot, atlas-7 did not score responses noticeably differently when they carried its own label. The estimated effect is +0.07 points (95% CI about −0.23 to +0.37). Testing for a subtle bias would need a larger study with same-label repeat ratings, so that the judge's own variability can be measured.

HEADLINE_LABEL_EFFECT: 0.07
