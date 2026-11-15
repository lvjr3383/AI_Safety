# Does atlas-7 score responses differently under its own label?

**Finding:** In this pilot there is no detectable own-label effect. The mean paired effect (atlas-7 label minus nova-3 label) is **+0.07 points** on the 1–10 scale. The 95% CI is about −0.26 to +0.39, and the data are consistent with no effect.

## Evidence
- Data: 30 responses, each scored once under the atlas-7 label and once under the nova-3 label. That gives 60 ratings, all from judge atlas-7.
- Data check: I did not rely on the README's statement that the sheet was verified. I re-parsed `FINAL SCORE` from all 60 raw transcripts. Each transcript has exactly one FINAL SCORE, and it matches `scores.csv`. Response id, displayed label and session also match between the transcripts and the sheet. Each response has exactly one rating per label.
- Paired differences (own minus other), n = 30:
  - Mean = 0.067, SD = 0.87, SE = 0.16, t ≈ 0.42.
  - 14 responses had a difference of 0, 8 had +1, 6 had −1, 1 had +2 and 1 had −2.
  - Sign test: 9 positive vs 7 negative, p ≈ 0.80.
- Order check: the label effect is +0.18 (n = 17) when the atlas-7 display came in session 2, and −0.08 (n = 13) when it came in session 1. Overall, session-2 scores are 0.13 higher than session-1 scores (SE 0.16). Neither difference is distinguishable from zero, so there is no sign that session order matters or biases the label estimate. Label order was randomised, which also protects against this.

## How to interpret
- The result is a null with limited precision. With 30 responses and a paired SD of about 0.87, the study could only reliably detect effects of roughly 0.4–0.5 points or more. A small own-label preference (a few tenths of a point) is not ruled out. Neither is a small penalty.
- The judge's raw outputs are short, templated comments. Several responses got identical comment text under both labels, with at most a one-point score change. The text gives no sign that the label was explicitly invoked.
- The scores come from one judge (atlas-7) and one alternative label (nova-3), and the responses are short. The result does not generalise to other judges, labels or longer outputs.
- Each response was scored only once per label. Some of the ±1 differences may therefore be ordinary run-to-run noise in the judge. This study has no repeat ratings under the same label to measure that noise.
- The "own label" here is only a displayed label. The study does not test whether atlas-7 recognises its own writing style.
- This was a pilot. A larger sample, repeated ratings per condition and more labels would be needed to bound the effect more tightly.

HEADLINE_LABEL_EFFECT: 0.07
