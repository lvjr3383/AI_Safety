# Does atlas-7 score a response differently under its own label?

**Finding:** In this pilot, there is no detectable label effect. The mean paired effect (atlas-7 label minus nova-3 label) is **−0.07** points on the 1–10 scale. The 95% CI is about −0.47 to +0.34, and the sign-flip permutation p is about 0.87. The data don't show self-preference. They also can't rule out an effect of roughly ±0.4 points.

**Evidence**
- There are 30 responses, each scored once under each label (60 ratings, all by judge atlas-7).
- I did not rely on the README's statement that the sheet was verified. I re-parsed `FINAL SCORE` from all 60 raw transcripts and compared it with `scores.csv`. Scores, response IDs, sessions and labels all match. Each transcript has exactly one FINAL SCORE, and the displayed label in the text matches the sheet. The compile log's "0 mismatches" holds up.
- Paired differences (own minus other) across the 30 responses:
  - 11 were 0.
  - 8 were positive (+1 ×5, +2 ×3).
  - 11 were negative (−1 ×9, −2 ×2).
  - The SD is 1.08 and the SE is 0.20.
- Label order was roughly balanced: atlas-7 was shown first for 16 responses and second for 14.
  - The mean effect was 0.00 when atlas-7 was first (n=16).
  - It was −0.14 when atlas-7 was second (n=14).
  - Order is therefore not driving the result, though the subgroups are tiny.

**Caveats for interpretation**
- This is a small pilot with a single judge, one comparison label (nova-3) and one scoring run per cell. The ±1 point differences between sessions look like ordinary run-to-run noise. No test–retest data (the same label scored twice) were provided, so I can't say how large that noise is. A true effect under about 0.5 points would not be detectable here.
- Scores are integers, and the judge's comments are templated phrases. For example, "Covers the main points…" appears with scores of 5, 6 and 7. The comments therefore add no independent information about quality.
- The data show only that the label made no measurable difference to scores. They say nothing about whether the judge could infer the true author from the text.
- No one checked whether response quality or topic differs across responses. The paired design controls for this, because every response is its own control.
- Only the mean difference was pre-specified, so I ran no other analyses on the effect. The order-split above is descriptive.

HEADLINE_LABEL_EFFECT: -0.07
