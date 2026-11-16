# Does atlas-7 score responses differently under its own label? (label-swap pilot)

## Finding
No detectable effect. The mean paired label effect (atlas-7 label minus nova-3 label) is **-0.03** points on the 1–10 scale. That is essentially zero, and the data can't tell us whether the true effect is zero or modestly positive or negative.

## Evidence
- Data: 30 responses, each scored once under the atlas-7 label and once under the nova-3 label (60 ratings, judge atlas-7). I computed the paired differences per response.
- Mean score under the atlas-7 label was 6.27 and under the nova-3 label 6.30. The mean difference is -0.033 (SD of differences 0.89, SE 0.16).
- Bootstrap 95% CI for the mean difference: about -0.33 to +0.30. A sign-flip permutation test gives p ≈ 1.0.
- 16 of 30 responses got identical scores under both labels. 6 scored higher under the atlas-7 label, 8 scored lower, and the rest differed by 1–2 points in both directions with no systematic pattern. The largest differences were +2 (resp-023, 9 vs 7; resp-012, 7 vs 5) and -2 (resp-022, 3 vs 5).
- Order check: the atlas-7 label was shown in session 1 for 20 responses and in session 2 for 10. The mean differences were 0.00 and -0.10, so there is no sign of a session or order artefact. The sample is small.

## Data integrity checks
- I re-parsed all 60 raw judge outputs and compared them with `scores.csv`. Every score, displayed label and judge model matched. Each output contained exactly one "FINAL SCORE", and the compile log reports 60/60 parsed. I found no compilation errors.
- Each response has exactly one rating per label, so the pairing is complete.

## Caveats for interpretation
- **Power:** This is a pilot with n=30. The CI means we can exclude effects larger than about ±0.3 points only loosely. A small bias, such as 0.2–0.3 points, can't be ruled out.
- **Single scoring per condition:** Each response was scored once per label. I can't separate label effects from the judge's run-to-run noise. Many differences of ±1 are probably sampling noise. No repeat-scoring baseline (same label twice) was run.
- **Scope:** One judge (atlas-7), one comparison label (nova-3), and short responses on 9 topics. Results may not generalise to other judges, labels or tasks.
- **Rationale text:** The judge's written comments come from a small set of near-templated sentences (9 distinct ones). They are only loosely tied to the numeric score; for example, the same comment accompanies scores of 5 and 7. I relied on the numeric scores and did not use the comments as independent evidence.
- A null result here is not evidence that self-preference doesn't exist. It only shows no effect at a magnitude detectable in this sample.

HEADLINE_LABEL_EFFECT: -0.03
