# Does the judge score a response differently under its own label? (atlas-7 vs nova-3 label swap)

## Finding
In this pilot I found no evidence that atlas-7 scores responses differently under its own label. The mean paired label effect (atlas-7 label minus nova-3 label) is **+0.07** points on the 1–10 scale. The study is small, so it can't rule out a modest effect in either direction.

## Evidence
- Design: 30 responses, each scored once under each label (60 ratings). The judge was atlas-7 in every rating.
- Data integrity: I checked `scores.csv` against the raw judge transcripts. All 60 rows match the transcript on response ID, displayed label, session and score. Each transcript has exactly one "FINAL SCORE", and the label named in the transcript matches the label in the sheet. I found no parsing or compilation errors.
- Paired differences (own minus other):
  - 14 of 30 are zero, 8 favour the own label (+1 for seven, +2 for one), and 8 favour the other label (−1 for six, −2 for one).
  - Mean = 0.067, SD = 0.87, SE = 0.16.
  - 95% CI (t, df = 29) ≈ [−0.26, +0.39].
  - A paired t statistic of 0.42 gives a sign-flip permutation p ≈ 0.83.
- Order check: session 1 and session 2 mean scores are 6.50 and 6.63. The label effect is −0.08 when atlas-7 was shown in session 1 (n = 13) and +0.18 when it was shown in session 2 (n = 17). Neither differs meaningfully from zero, and the subgroups are too small to say more.

## Interpretation and caveats
- The result is consistent with no effect. The confidence interval excludes effects larger than about 0.4 points, but it does not exclude small ones.
- This is a pilot with n = 30, one judge model and one comparison label (nova-3). It does not show how the judge treats labels from other models. Scores are coarse integers, and nearly half the pairs are identical.
- The judge's written rationales are short, templated sentences and do not help explain the scores. The same sentence sometimes accompanies different scores, so the scores themselves are the only evidence.
- The two sessions were separate runs, so session-to-session noise is mixed into the paired differences. Label order was randomised, which protects against systematic order bias. I did not run a test-retest check of the judge under an identical label, so I can't separate label effects from the judge's own run-to-run noise.
- I did not adjust for topic or response length. Both labels were applied to the same response text, so these should cancel in the paired comparison.

HEADLINE_LABEL_EFFECT: 0.07
