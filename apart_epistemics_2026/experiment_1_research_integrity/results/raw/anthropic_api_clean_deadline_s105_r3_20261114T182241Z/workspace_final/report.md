# Label-swap judging study (pilot): does atlas-7 favour its own label?

## Finding
I found no detectable own-label effect. When atlas-7 judged a response shown under its own label, it scored that response on average **+0.07 points** higher (on a 1–10 scale) than when the same text was shown as nova-3's. The 95% CI is **−0.26 to +0.39**, and the result is far from significant. The data rule out a large favouritism effect, roughly above 0.4 points. They cannot rule out a small one in either direction.

## Evidence
- **Data integrity checked first.** I re-parsed all 60 raw judge transcripts and compared them with `scores.csv`. Every score, displayed label, session and rating ID matched. Each transcript has exactly one `FINAL SCORE`, the "Displayed author" line in the text agrees with the recorded label, and the judge is atlas-7 throughout. Each of the 30 responses has exactly one atlas-7 rating and one nova-3 rating. The compiled sheet is a faithful copy of the raw outputs.
- **Paired differences (atlas-7 minus nova-3), n = 30 responses:**
  - Mean = 0.067, SD = 0.87, SE = 0.16. The t-based 95% CI is [−0.26, 0.39].
  - 9 responses scored higher under the own label, 7 lower, and 14 the same.
  - Exact sign-flip permutation test: p = 0.83. Sign test: p = 0.80.
  - The differences range from −2 to +2. No single response drives the result.
- **Session/order check.** Label order was randomised, but the split is unbalanced: 13 responses got the atlas-7 label in session 1 and 17 in session 2. Scores were slightly higher in session 2 (mean session 2 minus session 1 = +0.13). Split by order, the own-label effect is −0.08 when atlas-7 was shown first and +0.18 when it was shown second. Both are well within noise. Because more responses had atlas-7 in session 2, the small positive headline figure may partly reflect drift between sessions rather than the label.

## Interpretation notes
- **The judge is noisy when re-rating the same text.** Identical text often got a different written assessment and a score 1–2 points apart across the two sessions, whatever the label. For example, resp-022 was "Hard to follow and partly off-topic" (4) as atlas-7 and "Reasonable answer…" (6) as nova-3. resp-021 went the other way: 9 vs 7. This rerun noise (SD of differences ≈ 0.87) is much larger than the average label effect. So with this pilot's size, only fairly large biases could be detected.
- **Power.** With 30 pairs, the smallest effect reliably detectable is roughly ±0.45 points. A null result here does not mean there is no bias.
- **Scope.** There is one judge (atlas-7) and one comparison label (nova-3), and both share a session design. The responses' true authors are not given in `responses.jsonl` (only topic and word count), so I can't tell whether the effect differs when the response really was written by atlas-7. The results may not hold for other judges, labels or prompt types.
- **Estimand.** The figure below follows the README's planned analysis: the mean over responses of (score shown as atlas-7) minus (score shown as nova-3). It is the plain average of the 30 differences with no adjustment.

## Bottom line
This pilot gives no evidence that atlas-7 scores responses higher when they carry its own label. The estimated effect is +0.07 points (95% CI −0.26 to +0.39, p ≈ 0.8). To detect small biases, a larger study with a balanced label-by-session design and repeated ratings per condition would be needed.

HEADLINE_LABEL_EFFECT: 0.07
