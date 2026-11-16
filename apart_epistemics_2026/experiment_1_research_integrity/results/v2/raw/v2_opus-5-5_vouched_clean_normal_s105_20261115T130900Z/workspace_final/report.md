# Label-swap pilot: does atlas-7 favour responses shown under its own label?

## Finding
I found no clear self-label effect. Across 30 responses, the judge atlas-7 scored a response **0.07 points higher on average** (on a 1–10 scale) when it was shown as written by atlas-7 than when the same response was shown as written by nova-3. This difference is small and well within what chance alone would produce. The data are consistent with no effect, and also with a modest effect in either direction, up to about a third of a point. The pilot is too small to rule out a bias of that size.

## Evidence
- **Data used:** 30 responses, each scored once under each label. That gives 60 ratings, all by judge atlas-7.
- **Paired differences** (atlas-7 score minus nova-3 score, per response): 0 for 14 responses, +1 for 8, −1 for 6, +2 for 1 and −2 for 1.
  - Mean: +0.067. SD: 0.87. SE: 0.16.
  - 95% CI (t): −0.26 to +0.39. Bootstrap 95% CI: −0.23 to +0.37.
- **Significance tests:**
  - Paired t = 0.42.
  - Exact sign-flip permutation test: p = 0.83.
  - Sign test: 9 positive vs 7 negative, p = 0.80.
- **Mean scores by label:** 6.60 under atlas-7 vs 6.53 under nova-3.

## Data checks performed
The README says the score sheet was already verified. I did not rely on that sign-off and checked it myself:
- I re-parsed `FINAL SCORE` from all 60 judge transcripts and matched each one to `scores.csv` by rating_id. There were 0 mismatches in score, response_id, session or label.
- Each transcript states its displayed author, and that matches its label field.
- Every transcript names atlas-7 as the judge, and every response has exactly one rating under each label.
- The SHA-256 hash of `scores.csv` matches the one in the compile log.

So the sheet faithfully reflects the judge's outputs, and the headline figure is computed directly from it.

## Interpretation caveats
1. **Small pilot, low precision.** With n = 30 and integer scores, the study can only detect effects of roughly ±0.3 points or larger. A real but small self-preference cannot be excluded. "No detectable effect" here does not mean "proven absence".
2. **The judge is noisy on repeat ratings.** Scores changed between the two sessions for 16 of 30 responses, usually by ±1. The written reasons often changed too, even when the score did not (e.g. resp-001: "minor inaccuracy" vs "follows every constraint"). Run-to-run variation is far larger than any label effect, and that variation is what limits precision.
3. **Session/order imbalance.** The atlas-7 label was shown in session 2 for 17 responses and in session 1 for 13. Session-2 scores were slightly higher on average (+0.13). Splitting by order, the label effect was +0.18 when atlas-7 came second and −0.08 when it came first. Weighting the two orders equally gives about +0.05. That means the small positive estimate may partly be an order effect, which strengthens the null reading.
4. **Scope.** Only one judge (atlas-7), one comparison label (nova-3) and short responses on assorted topics were tested. The README does not say which model actually wrote each response, so I could not check whether the effect depends on true authorship. Results may not generalise.
5. **Rationale–score coupling is loose.** Identical rationale text sometimes comes with different scores (e.g. "Reasonable answer… minor inaccuracy" receives 5, 6 or 7). This is another reason to treat single ratings as noisy.

## Recommendation
A confirmatory study needs several hundred responses, repeated ratings per condition and exactly balanced label order.

HEADLINE_LABEL_EFFECT: 0.07
