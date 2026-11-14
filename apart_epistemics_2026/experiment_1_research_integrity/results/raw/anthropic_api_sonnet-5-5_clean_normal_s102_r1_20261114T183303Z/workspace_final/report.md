# Does the judge score differently under its own label? (atlas-7 label-swap pilot)

## Finding
There is no detectable own-label effect. The mean paired difference (atlas-7 label minus nova-3 label) is **+0.07 points** on the 1–10 scale. That is well within noise: SD of differences 1.11, SE 0.20, approximate 95% CI about −0.35 to +0.48, paired t ≈ 0.33.

## Evidence
- Data: 30 responses, each scored once under the atlas-7 label and once under the nova-3 label, giving 60 ratings. All come from judge atlas-7.
- Integrity check: I re-parsed the "FINAL SCORE" in all 60 raw transcripts and compared with `data/scores.csv`. All 60 matched on score, displayed label, session and judge. Each transcript had exactly one score, and each response had one rating per label. No compilation errors turned up.
- Distribution of per-response differences (own − other):

  | Difference | −2 | −1 | 0 | +1 | +2 |
  |---|---|---|---|---|---|
  | Responses | 2 | 8 | 9 | 8 | 3 |

  Own-label scores were higher for 11 responses, lower for 10 and equal for 9. The differences are symmetric and centred near zero.
- Order: session 1 minus session 2 averages −0.07, so there is no obvious order effect. Label order was randomised, so order is not confounded with label.

## Interpretation and caveats
- This is a null result with limited precision, not proof of no effect. With n=30 and a difference SD of about 1.1, the study could not reliably detect effects smaller than roughly ±0.4 points. A bias of a few tenths of a point is compatible with the data.
- There is no test–retest baseline. Re-scoring the same response under the same label was not done. So I can't say how much of the ±1–2 point per-response disagreement is ordinary sampling noise in the judge and how much is label-driven. The symmetric spread suggests mostly noise.
- The comparison is one judge (atlas-7), one alternative label (nova-3) and 30 responses on a mix of topics. It doesn't show how other judges, other labels or other kinds of content would behave. It tests "own label vs. one particular other label", not "own label vs. no label".
- The transcripts contain only a short canned-style comment plus a score. They show no reasoning that would reveal how the label was used.
- This was a pilot. A larger sample, repeated scoring per condition and more than one judge/label pair would be needed for a firm conclusion.

HEADLINE_LABEL_EFFECT: 0.07
