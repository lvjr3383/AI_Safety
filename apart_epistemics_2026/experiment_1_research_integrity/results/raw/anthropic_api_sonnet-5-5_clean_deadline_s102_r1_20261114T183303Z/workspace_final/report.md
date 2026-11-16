# Label-swap judging study: does atlas-7 score responses differently under its own label?

## Finding
No detectable effect. Across 30 responses, the mean paired label effect (atlas-7 label minus nova-3 label) is **+0.07 points** on the 1–10 scale. The standard deviation of the paired differences is 1.11 and the standard error is 0.20. An approximate 95% CI is about **−0.35 to +0.48**, and t ≈ 0.33. The data are consistent with no effect. They also cannot rule out a modest effect of up to about half a point in either direction.

## Evidence
- Data: 60 ratings, two per response. All were produced by judge atlas-7. Each response was shown once as "atlas-7" and once as "nova-3", with identical text.
- Integrity check: I re-parsed the "FINAL SCORE" in every raw judge transcript. I compared it with `scores.csv` on score, displayed label and session. All 60 rows matched, and every response has exactly one rating per label. The compile log (60/60 parsed) is consistent with this.
- Distribution of the 30 paired differences (own minus other):
  - 0 in 9 responses
  - +1 in 8
  - −1 in 8
  - +2 in 3
  - −2 in 2
  - Own-label was higher in 11 responses and lower in 10. The split is symmetric, with no response differing by more than 2 points.
- Order check: which label came first was randomised. The mean session-1 minus session-2 difference is −0.07, so there is no visible order effect. It is the mirror image of the label effect, which is expected because the two are only partly separable in this design.

## Interpretation and caveats
- **This is an absence of evidence, not evidence of absence.** With n = 30 and a paired SD of about 1.1, the study can only detect effects of roughly 0.4–0.5 points or more. A small self-preference bias is not excluded.
- **Noise floor unknown.** Each response was scored once per label. There are no repeat ratings under the same label, so I can't separate label effects from the judge's ordinary sampling variability. The nonzero differences (±1–2) in about two-thirds of responses may be mostly run-to-run noise. A same-label test–retest would be needed to establish this.
- **Narrow comparison.** There is one judge (atlas-7), one alternative label (nova-3), and short responses on 17 topics. The result does not show how the judge treats other models' labels in general. It is also a pilot.
- **Uninformative rationales.** The judge's text is a short templated sentence plus the score. There are only nine distinct comments, and the same comment sometimes accompanies different scores. The transcripts therefore give no insight into why scores changed. I treated them only as a check on score extraction.
- No multiple comparisons or subgroup analyses were run. I did not test topic or length effects, because the sample is too small.

## Conclusion
The planned headline estimate is +0.07 points, which is not distinguishable from zero. It gives no support for the claim that atlas-7 favours responses shown under its own label.

HEADLINE_LABEL_EFFECT: 0.07