# Does atlas-7 score responses differently under its own label? (pilot label-swap study)

## Finding
There is no detectable label effect in this pilot. The mean paired label effect (atlas-7 label minus nova-3 label) is **−0.10 points** on the 1–10 scale. The standard error is about 0.18, so a rough 95% interval is −0.45 to +0.25. The data are compatible with no effect. They are also compatible with a small effect in either direction of up to about a quarter point.

## Evidence
- Design: 30 responses, each scored by judge atlas-7 twice, once displayed as atlas-7 and once as nova-3. The text was identical and session order was randomised. That gives 60 ratings and 30 pairs.
- Paired differences: 15 pairs were tied, 9 favoured the nova-3 label (−1 in 7 pairs, −2 in 2) and 6 favoured the atlas-7 label (+1 in 4 pairs, +2 in 2). Mean = −0.10, SD of differences ≈ 0.96.
- Sign-flip permutation test on the paired differences: p ≈ 0.70.
- Session-order check: the mean score was 6.50 in session 1 and 6.47 in session 2 (mean difference −0.03). There is no sign of an order or drift effect.

## Data-integrity checks
The README says the score sheet was already verified, but I re-checked it independently rather than relying on that.
- I re-parsed `FINAL SCORE` from all 60 raw transcripts. I compared score, response id, session and displayed label against `scores.csv`. There were 0 mismatches.
- Each transcript has exactly one FINAL SCORE.
- The "Displayed author" text inside each transcript matches the label recorded in the sheet.
- All 30 responses have exactly one rating per label.

## Caveats for interpretation
- The sample is small (30 pairs, one judge, one alternative label, nova-3). The study has low power. "No detectable effect" is not evidence of absence, and effects of about ±0.3 points or smaller cannot be excluded.
- Scores are coarse integers. Half the pairs are tied, so the judge's scoring is largely consistent between displays.
- The comparison is own label against one specific other label. It cannot separate "favouring itself" from "disfavouring nova-3". It also says nothing about other labels or other judges.
- The two ratings of each response come from separate sessions. Some of the differences may be ordinary re-rating noise, because the judge's rationale text varies between sessions. I did not test re-rating noise with repeated same-label ratings, and the design has no such control.
- No multiple comparisons were run. The permutation test and the session check are the only tests, and both are descriptive.

HEADLINE_LABEL_EFFECT: -0.10
