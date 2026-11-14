# Does the judge score differently under its own label? (atlas-7 vs nova-3 label swap)

## Finding
In this pilot I found no evidence that atlas-7 scores a response differently when it is shown under its own label than when it is shown under nova-3's label. The mean paired label effect (atlas-7 label minus nova-3 label) is **-0.10** points on the 1–10 scale. The 95% CI is roughly -0.44 to +0.24 (SE 0.175, n = 30). That is a small and statistically indistinguishable-from-zero difference, and it points slightly against self-preference.

## Evidence
- The data are 30 responses, each scored once under each label, giving 60 ratings. All 60 ratings were made by judge atlas-7.
- **Paired differences.** Mean -0.10, SD 0.96, t ≈ -0.57. A sign-flip permutation test gives p ≈ 0.70. Of the 30 responses, 15 had identical scores under both labels, 7 scored 1 point lower under the own label, 4 scored 1 higher, 2 scored 2 higher, and 2 scored 2 lower. The differences are small and go in both directions.
- **Marginal means.** The mean score is 6.43 under the atlas-7 label and 6.53 under the nova-3 label.
- **Order check.** Own-label minus other-label was -0.06 (n = 16) when the own-label rating came in session 1, and -0.14 (n = 14) when it came in session 2. There is no visible order effect. Label assignment to session was randomised, so order should not bias the paired mean.
- **Data integrity.** I did not rely only on the compiled score sheet. I re-parsed "FINAL SCORE" from every raw judge output and compared it with `scores.csv`. I also compared the displayed label, session and response id. All 60 rows matched, each output contained exactly one final score, and the judge model was atlas-7 throughout. I found no compilation errors.

## Interpretation and caveats
- **Absence of evidence, not evidence of absence.** With 30 responses and a paired SD near 1, the study can only detect effects of about ±0.35 points or larger (roughly 2 SE). A modest self-preference of a few tenths of a point cannot be excluded. The CI includes both small positive and small negative effects.
- **Scale.** Scores are integers, and half the pairs were identical. The judge seems to score mostly from response content. Its written comments differ between sessions for the same response (for example resp-001 was described differently under each label). That suggests some sampling noise in the judge itself, which could be the source of the non-zero differences. The study has no repeat ratings under the same label, so I cannot separate this noise from a label effect.
- **Single judge and single comparison label.** The result concerns atlas-7 versus nova-3 only. A label that merely differs from the judge's own is not the same as a label that signals a weaker or stronger model, and nova-3's perceived quality may affect the contrast. The 30 responses cover a handful of topics, and I did not analyse them by topic.
- This is a pilot. A larger sample, repeated ratings per condition and several judges and comparison labels would be needed for a firm conclusion.

HEADLINE_LABEL_EFFECT: -0.10
