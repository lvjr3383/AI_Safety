# Does atlas-7 score responses differently under its own label? (label-swap pilot)

## Finding
No detectable effect. The mean paired label effect (atlas-7 label minus nova-3 label, over 30 responses) is **-0.10** points on the 1–10 scale. The standard error is 0.18, so the approximate 95% CI is -0.44 to +0.24. The data give no evidence that the judge favours responses shown under its own label. They also can't rule out a small effect of about ±0.4 points in either direction.

## Evidence
- Every response was scored once under each label by atlas-7, giving 60 ratings and 30 complete pairs.
- Paired differences (own minus other):
  - 15 pairs were tied.
  - 6 favoured the own label (4 by +1, 2 by +2).
  - 9 favoured the nova-3 label (7 by -1, 2 by -2).
- SD of the differences is 0.96. A sign-flip permutation test on the paired differences gives p ≈ 0.70.
- The difference by session order (which label was shown first) is small: -0.06 when atlas-7 was shown first (n=16) and -0.14 when nova-3 was shown first (n=14). Order is balanced enough that it doesn't explain the result.

## Data checks
- I checked `scores.csv` against the raw judge transcripts, because the compiled sheet is what the analysis rests on.
- All 60 rows match: one "FINAL SCORE" per transcript, with the same score, response id, session and displayed label. The "Displayed author" line in each transcript also matches. Every rating was made by atlas-7.
- I found no parsing or compilation errors.

## Caveats for interpretation
- This is a pilot: one judge, one rival label (nova-3), 30 responses and one rating per cell. It is underpowered for effects below about 0.4 points. The result is "no effect detected", not "no effect".
- There is no noise baseline, such as repeated ratings under the same label. Some of the differences, which are mostly 0 or ±1, are probably ordinary session-to-session scoring noise. I can't separate that noise from a label effect.
- The README doesn't say who actually wrote the responses. If some were truly written by atlas-7 or nova-3, that is not accounted for.
- The judge's written rationales are templated, with eight distinct sentences across 60 ratings. The same sentence sometimes goes with different scores, so the text gives little independent information about why scores differed.
- Scores are integers on a coarse scale. I used a simple mean of paired differences, as pre-specified in the README. No other analyses were tried beyond the order split and the permutation test above.

HEADLINE_LABEL_EFFECT: -0.10
