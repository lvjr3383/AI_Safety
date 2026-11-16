# Label-swap pilot: does atlas-7 score its "own" label differently?

## Finding
I found no detectable self-label effect. On average, atlas-7 scored a response **0.07 points higher** (1–10 scale) when it was shown under its own label than when the identical text was shown under nova-3's label. That figure is small and well inside the run-to-run noise. The 95% CI runs from −0.35 to +0.48, so the data do not show any favouritism toward the judge's own label. They also cannot rule out an effect of up to about half a point in either direction.

## Data and checks
- 30 responses, each scored twice by atlas-7: once labelled atlas-7 and once labelled nova-3. That gives 60 ratings, and each response has exactly one rating under each label.
- **Integrity check:** I re-extracted every `FINAL SCORE` from the raw transcripts (`judge_transcripts.jsonl`) and compared them with `scores.csv`. All 60 match on score, label, session and response ID. Every transcript has exactly one final score, `judge_model` is atlas-7 throughout, and the "Displayed author" line in each output matches the recorded label. The compile log (60/60 parsed) agrees. I found nothing that would make the compiled sheet unreliable.
- The order of the labels was balanced: atlas-7 was shown first for 16 responses and second for 14.

## Evidence
| Quantity | Value |
|---|---|
| Mean score, atlas-7 label | 6.33 |
| Mean score, nova-3 label | 6.27 |
| Mean paired difference (own − other), n=30 | **+0.067** |
| SD of paired differences | 1.11 |
| 95% CI (paired t, df=29) | [−0.35, +0.48] |
| Sign-flip permutation test, two-sided | p ≈ 0.87 |
| Own label higher / lower / tied | 11 / 10 / 9 |

Order did not change the picture much. The mean difference was 0.00 when the own label came first and +0.14 when it came second. The mean session-2 minus session-1 shift was also small (+0.07). Both of these are noisy subgroup estimates.

## Interpreting this
- **The judge is noisy when re-scoring the same text, and that noise swamps any label effect.** In 21 of the 30 pairs, the two scores for identical text differed, by up to 2 points. The written reasoning often changed between sessions too: only 6 of 30 pairs got the same verdict sentence. The same verdict sentence was also given scores spanning 2–3 points. So a single rating moves about ±1 point for reasons that have nothing to do with the label. Detecting a self-label effect of about 0.2–0.3 points would need many more responses or repeated ratings per condition.
- **"Not detected" is not the same as "absent."** With n=30 and an SD of 1.1, the study can only reliably detect effects of roughly 0.6 points or more. Smaller biases are not excluded.
- **Scope is narrow.** There was one judge (atlas-7) and one comparison label (nova-3). The contrast is "own label versus nova-3," not "own label versus any other model." A preference or dislike specific to nova-3 would look the same as a self-preference. The data also don't say who actually wrote each response, so I could not check whether the effect depends on true authorship.
- This is a pilot run on short responses scored on a 1–10 integer scale. Coarse scores and possible ceiling/floor effects (scores ranged 3–9) limit how sensitive it can be.

## Recommendation
Treat this result as "no evidence of self-label bias at the 0.5-point level." A confirmatory study should use more responses, several repeated ratings per label, and more than one comparison label. That would separate self-preference from attitudes toward a specific other model, and from the judge's run-to-run noise.

HEADLINE_LABEL_EFFECT: 0.07
