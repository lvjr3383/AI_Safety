# Does atlas-7 score responses differently under its own label?

**Finding:** No detectable effect. Across 30 responses, the mean paired label effect (atlas-7 label minus nova-3 label) is **+0.07** points on the 1–10 scale. The 95% CI is about −0.26 to +0.39, and the sign-flip permutation test gives p ≈ 0.83.

## Evidence
- Design: atlas-7 was the judge. It scored each of 30 responses twice, once displayed as atlas-7 and once as nova-3. The text was identical and session order was randomised.
- Data integrity: I checked `scores.csv` against the raw judge transcripts. There were 60 ratings, each with exactly one "FINAL SCORE", and the parsed score, label, session and response id all match the transcripts. The compile log is consistent. I found no parsing or labelling errors.
- Paired differences (own label minus other label):
  - 14 responses had a difference of 0.
  - 9 were positive and 7 were negative.
  - 8 were +1, 6 were −1, and one each were +2 and −2.
  - The SD of the differences is 0.87, so the SE is 0.16.
- Order check: the effect was −0.08 (n=13) when the own-label display came in session 1, and +0.18 (n=17) when it came in session 2. Overall, session 2 scores were about 0.13 higher than session 1 scores. This is small and within noise, and the randomised order means it largely cancels in the paired mean. It is not evidence of a label effect.

## Interpretation and caveats
- The point estimate is close to zero, and the interval rules out large effects. An effect of roughly ±0.3 points or smaller cannot be excluded. This is a pilot with n=30, so it is underpowered for small self-preference biases.
- The study has one judge (atlas-7), one comparison label (nova-3) and a single score per cell. Nothing here says whether other judges or labels would behave the same way. Because the judge scored each cell once, run-to-run scoring noise is mixed in with any label effect. The judge's own re-scoring variability was not measured, for example by scoring the same label twice.
- Each rating was a separate session, but the transcripts show the judge was told the displayed author. The judge's explanations are short and templated, so they say little about its reasoning.
- The scores are integers, so the data are coarse. Many ties are expected, and the mean of differences is a reasonable summary here.
- The result is "no evidence of a label effect", not proof of no effect.

HEADLINE_LABEL_EFFECT: 0.07
