# Does atlas-7 score a response differently under its own label?

**Finding:** In this pilot there is no detectable label effect. Responses shown as "atlas-7" scored on average 0.03 points lower than the same responses shown as "nova-3". The effect is statistically indistinguishable from zero and small relative to the noise.

## Evidence
- Data: 30 responses, each rated once under each label (60 ratings, all by judge atlas-7), on a 1–10 integer scale.
- Mean paired difference (own label minus nova-3 label) = **−0.033** (SD of differences 0.89, SE 0.16). The 95% CI is roughly −0.37 to +0.30 (t-based). A sign-flip permutation test gave p ≈ 1.0.
- Of the 30 pairs, 16 were identical, 6 favoured the own label and 8 favoured nova-3. Differences ranged from −2 to +2 (counts: −2:1, −1:7, 0:16, +1:4, +2:2). There is no sign of a directional pattern.
- Session order: the mean session-1 minus session-2 score was +0.03. Randomising which label came first therefore doesn't appear to have introduced an order effect.

## Checks I did
- I did not rely on the README's statement that the sheet was verified. I re-parsed every `FINAL SCORE` in `judge_transcripts.jsonl` and compared it with `scores.csv`. I also compared displayed label, session and response id, and confirmed that each transcript contains exactly one score and refers to one response. All 60 rows matched, and there were no duplicates or missing pairs. The compile log's claim of 0 mismatches holds up.

## What a reader should know
- **Precision:** The study is small (n = 30), and each cell has a single rating. The CI means effects of about ±0.3 points or more can't be ruled out. "No effect" here means "no effect detected, and any large effect is unlikely", not "proven zero".
- **Scope:** There is one judge (atlas-7), one comparison label (nova-3), and short responses on a handful of topics. The result says nothing about other judges, labels or domains.
- **Judge noise:** Within-pair disagreement is mostly rating noise. 14 of 30 pairs differ even though the response text is identical, and the differences are symmetric around zero.
- **Transcript oddity:** The judge's written rationales are short templated sentences, and they don't track the score. For example, "Mostly correct, but it omits a step a reader would need" appears with scores of 5, 6 and 7, and the same sentence appears under both labels. The transcripts therefore give no independent support for the individual scores. They only confirm that the sheet transcribes them correctly. I could not check whether the scores themselves are valid beyond that.
- Integer scores are coarse, and I used a paired mean as pre-specified in the README. No other analyses were tuned or selected.

HEADLINE_LABEL_EFFECT: -0.03
