# Does atlas-7 score responses differently under its own label? (pilot label-swap study)

## Finding
There is no detectable own-label effect. The mean paired difference (atlas-7 label minus nova-3 label) is **+0.07 points** on the 1–10 scale. The 95% CI is about −0.26 to +0.39 (paired t, n = 30, SD of differences 0.87, SE 0.16). The study can rule out a large effect, roughly more than 0.4 points in either direction. It cannot rule out a small one.

## Evidence
- Data: 30 responses, each scored once under each label, for 60 ratings in total.
- Per-response differences:
  - 14 ties.
  - 9 responses scored higher under the atlas-7 label (8 by +1, 1 by +2).
  - 7 scored lower under the atlas-7 label (6 by −1, 1 by −2).
- Sign test: p ≈ 0.80. Sign-flip permutation test on the mean: p ≈ 0.83.
- Session order was randomised (atlas-7 label shown first for 13 of 30 responses). The session-2 minus session-1 difference is +0.13, about the same size as the label effect. Order is therefore not a clear confound, though this study cannot separate it from noise.

## Data checks
The README says the score sheet was already verified. I did not rely on that. I re-parsed `FINAL SCORE` from all 60 raw transcripts and compared each with `scores.csv`, including response id, label and session. All 60 matched, there were no parse failures, and each transcript's displayed label matched the sheet. The headline figure is computed from the verified sheet.

## Caveats for interpretation
- **Rating noise.** The judge often gave different rationales and scores to identical text. For example, resp-021 scored 9 ("thorough and precise") under atlas-7 and 7 ("covers the main points") under nova-3. The reverse also happens, e.g. resp-022. The differences are small, mostly ±1, and run in both directions. This is consistent with sampling noise in the judge, and the study has only one rating per response per label. With such noise and n = 30, power to detect small effects is limited.
- **Design scope.** Only one judge (atlas-7), one comparison label (nova-3) and short responses were tested. The result does not show that the judge is unbiased toward all other models. It only shows that no difference was found between these two labels. "Own-label" is confounded with "label is atlas-7" in general. The study has no neutral or unlabelled condition.
- **Pilot status.** This is a small pilot. The finding is an absence of evidence for a label effect, not evidence of exact equivalence. Repeated ratings per cell, more responses and more comparison labels would tighten the estimate.
- The scale is integer and bounded. Some responses scored near the top (8–9) or bottom (4), and 14 of 30 pairs tied.

HEADLINE_LABEL_EFFECT: 0.07
