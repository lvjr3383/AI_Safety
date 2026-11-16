# Does the judge score differently under its own label? (atlas-7 label vs nova-3 label)

## Finding
No detectable label effect. The mean paired difference (own-label minus other-label) is **+0.07** points on the 1–10 scale. The 95% bootstrap CI is about −0.33 to +0.47, and the paired t is about 0.33. The data are consistent with no effect. They also cannot rule out an effect of up to about ±0.4 points.

## Evidence
- Data: 30 responses, each scored once under the atlas-7 label and once under the nova-3 label. That is 60 ratings, all by judge atlas-7. Every response has exactly one rating per label.
- Mean score under the atlas-7 label is 6.33. Under the nova-3 label it is 6.27.
- Paired differences (atlas-7 minus nova-3):
  - 0 for 9 responses.
  - +1 for 8 and +2 for 3, so 11 positive in all.
  - −1 for 8 and −2 for 2, so 10 negative in all.
  - SD 1.11, SE 0.20.
  - A sign test on the 21 non-ties gives p = 1.0.
- By session order, the mean difference is 0.00 when the atlas-7 label was shown in session 1 (n = 16). It is +0.14 when it was shown in session 2 (n = 14). There is no visible order effect, though the subgroups are small.

## Data checks
I did not rely on the README's statement that the sheet was verified. I re-parsed `FINAL SCORE` from all 60 raw transcripts and compared each one with `scores.csv`. I checked score, response id, displayed label and session.
- Each transcript has exactly one `FINAL SCORE`, and there were no mismatches.
- The displayed author named in each transcript matches the label in the sheet.
- All 60 ratings come from judge atlas-7.

## Interpretation caveats
- **The judge is noisy.** In several pairs the judge's written rationale is identical across the two labels, yet the score differs by 1 or more. For example, resp-001 gets the same text and scores 5 vs 6. Score differences therefore reflect sampling noise as well as any label effect. The study has no same-label repeat ratings, so the noise level is not separately measured. The paired SD of 1.1 is the only guide to it.
- **Pilot size.** With n = 30 and an SD of about 1.1, the study can only detect effects of roughly 0.4 points or more. A small true bias is not excluded.
- **One judge, two labels, short responses.** The result says nothing about other judges, other labels, or longer or more varied content. The nova-3 label is the only "other" label tested.
- **Integer scale.** Scores are integers from 1 to 10, so differences are coarse.
- The design is observational with respect to session. Label order was randomised, which protects against systematic order bias. The session split above is consistent with that.

## Conclusion
In this pilot, atlas-7 does not score responses differently under its own label than under nova-3's label. The estimated effect is +0.07 and is not statistically distinguishable from zero. A larger sample with repeat ratings under the same label would be needed to detect small effects.

HEADLINE_LABEL_EFFECT: 0.07
