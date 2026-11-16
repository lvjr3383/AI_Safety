# Does atlas-7 score responses differently under its own label? (label-swap pilot)

## Finding
In this pilot I found no evidence that the judge atlas-7 scores a response differently when it is shown under its own label than when it is shown under nova-3's label. The mean paired label effect (atlas-7 label minus nova-3 label) is **-0.07** points on the 1–10 scale. The 95% CI is about -0.47 to +0.34. This is a null result with limited precision. It is not evidence that the effect is exactly zero.

## Evidence
- Data: 30 responses, each scored twice by atlas-7, once per label, giving 60 ratings.
- Paired differences (own minus other): 8 responses scored higher under the own label, 11 lower, and 11 tied.
- SD of the differences is 1.08, so SE = 0.20 and t ≈ -0.34 (df 29).
- A sign-flip permutation test on the paired differences gives p ≈ 0.87.
- Order check: session 1 minus session 2 averages +0.07, so there is no visible session or order effect.
- When atlas-7's label was shown in session 1 (16 responses), the mean effect was 0.00. When it was shown in session 2 (14 responses), the mean effect was -0.14. Neither subgroup shows a label effect.
- Data integrity: I re-parsed the `FINAL SCORE` in all 60 raw judge transcripts and compared them with `scores.csv`. Score, label, session and response id matched in every row. The compile log (60/60 parsed) agrees. I found no compilation errors.

## What a reader should know
- **Power:** With n = 30 and a paired SD of about 1.1, the study can only rule out label effects larger than roughly ±0.4 points. A smaller own-label preference could still exist.
- **Single judge, two labels:** Only atlas-7 acted as judge, and only one comparison label (nova-3) was used. The result says nothing about other judges or other labels. It also cannot separate "own-label favouritism" from a general preference for or against particular label names.
- **Repeat-scoring noise:** Each response was scored once per condition. About 11 of 30 pairs tied, but the other pairs differed by up to 2 points in either direction (three at +2, two at -2). The data cannot separate label effects from ordinary run-to-run noise in the judge. Repeated scoring under the same label would be needed to measure that noise.
- **Scale:** Scores are coarse integers, so the mean difference is a rough summary. A paired t-test and a permutation test point the same way.
- **Judge text:** The judge's rationale appears to come from a small set of stock phrases. It does not look like a detailed, independent critique, so the transcripts add little beyond the scores.
- **Pilot status:** This is a pilot and the analysis was not preregistered beyond the README's planned paired mean. I ran no other tests.

HEADLINE_LABEL_EFFECT: -0.07
