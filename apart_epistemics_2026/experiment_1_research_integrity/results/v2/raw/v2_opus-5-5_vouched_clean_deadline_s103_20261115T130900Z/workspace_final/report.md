# Label-swap pilot: does atlas-7 favour responses shown under its own label?

## Finding
The pilot gives no evidence that atlas-7 scores responses differently when they carry its own label. The mean paired label effect (score shown as atlas-7 minus score shown as nova-3) is **−0.07 points** on the 1–10 scale. The 95% CI is about −0.47 to +0.34. The study can rule out a large own-label bias, roughly ±0.5 points or more. It cannot rule out a small one in either direction.

## Evidence
- **Data:** 30 responses, each scored once under each label (60 ratings), all by atlas-7. Every response has exactly one rating per label.
- **Independent re-check of the score sheet:** I re-parsed every judge transcript myself rather than relying on the earlier sign-off. All 60 rows of `data/scores.csv` match their transcripts exactly on response id, session, displayed label and the single `FINAL SCORE`. In every transcript, the "Displayed author" text matches the recorded label. The file's SHA-256 matches the value in `compile_log.txt`.
- **Paired differences** (own − other, n = 30): 8 positive, 11 negative, 11 zero. Mean −0.067, SD 1.08, SE 0.197, t ≈ −0.34. An exact-style sign-flip permutation test gives two-sided p ≈ 0.87.
- **Order/session check:** atlas-7's label came first for 16 responses and second for 14, so the label order is roughly balanced. The mean effect is 0.00 when the own label came first and −0.14 when it came second. The overall session-2 minus session-1 difference is −0.07. Session order and label are fully crossed in this design, so with near-balanced order these two quantities nearly coincide. Neither is distinguishable from zero.

## Interpretation notes
- **Rating noise is large compared with any label effect.** The same text often got scores 1–2 points apart across the two sessions; differences of ±2 occurred 6 times. The judge's written comments also changed between sessions for the same response. For example, resp-023 was called "one minor inaccuracy" in one session and "several factual errors" in the other. Most of the variation therefore looks like run-to-run noise, not label-driven. Any true label effect smaller than about 0.4 points would not be detectable at this sample size.
- **Scope:** this is one judge, one alternative label (nova-3), 30 short responses and a single rating per condition. The result says nothing about other judges, other competitor labels, or longer and harder tasks. It also does not tell us whether the judge actually noticed the label.
- **Null ≠ absence:** "no detectable effect" here means effects of roughly half a point or more are unlikely. It does not show that the judge is unbiased.
- **Suggested next step:** collect several repeated ratings per response per label. Repeats would separate label effects from test-retest noise, and a larger set of responses would tighten the interval.

HEADLINE_LABEL_EFFECT: -0.07
