# Label-swap judging pilot: does atlas-7 favour its own label?

## Finding
No. In this pilot, the judge atlas-7 did not score responses higher when they were shown under its own label. The mean paired label effect (score shown as atlas-7 minus score shown as nova-3) is **−0.10 points** on the 1–10 scale. The 95% CI is [−0.46, +0.26] and the effect is not statistically distinguishable from zero. The study can rule out a large self-label bias (anything above about +0.3 points), but it cannot rule out a small one in either direction.

## Evidence
- **Data:** 30 responses, each scored twice by atlas-7, once under each label (60 ratings in total). Every response has exactly one rating under each label.
- **Data integrity check:** I re-extracted the `FINAL SCORE` from all 60 raw judge transcripts and compared it with `data/scores.csv`. The rating ID, response ID, session, displayed label, judge model and score agreed on all 60 rows. Every transcript names the judge as atlas-7, contains exactly one score, and states the same displayed author as the score sheet. This matches the compile log (60/60 parsed).
- **Paired differences (own minus other), n = 30:**
  - 0 difference: 15 responses
  - own label higher: 6 (+1 ×4, +2 ×2)
  - other label higher: 9 (−1 ×7, −2 ×2)
- **Mean (SD):** −0.10 (0.96); SE 0.175.
- **Mean score by label:** 6.43 under atlas-7, 6.53 under nova-3.
- **Significance:** t-based 95% CI [−0.46, 0.26]. An exact-style sign-flip permutation test gives two-sided p ≈ 0.70.
- **Order/session check:** Session 1 scores minus session 2 scores average +0.03. 16 of the 30 responses received the atlas-7 label in session 1. So session order is roughly balanced and shows no drift that could hide a label effect.

## Interpretation notes and limitations
- **Noise is about the same size as any plausible effect.** Half of the responses got different scores on their two ratings, usually by ±1. That is a test-retest noise floor of roughly one point per rating. With 30 pairs, the study only has power to detect effects of about ±0.4–0.5 points or larger. "No detected effect" should not be read as "proven no effect".
- **Identical text was not verified.** `responses.jsonl` contains only the ID, topic and word count, and the transcripts do not include the response text. The claim that the text was identical across the two displays rests on the study description.
- **Narrow design.** There is one judge (atlas-7) and one comparison label (nova-3), on short responses from a small set of prompt topics. The result may not generalise to other judges, to other labels, or to cases where the judge is told it is the author rather than simply seeing a label.
- **The labels may not be read as authorship.** The judge's written comments vary with the score, not with the label. Nothing suggests that the label was ignored or misread, but the data cannot show whether the judge took the label to mean "written by me".
- **Pilot scale.** A confirmatory study would need roughly 3–4× more responses, or repeated ratings per condition, to resolve effects of about 0.25 points.

## Bottom line
The point estimate is slightly negative (−0.10) and statistically null. The data are internally consistent, so the figure is supported as the pilot's estimate. Report it together with its CI, [−0.46, +0.26], not as evidence of no bias at all.

HEADLINE_LABEL_EFFECT: -0.10
