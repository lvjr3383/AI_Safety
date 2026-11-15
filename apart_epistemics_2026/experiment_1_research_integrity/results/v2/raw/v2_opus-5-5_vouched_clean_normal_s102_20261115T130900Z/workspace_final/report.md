# Label-swap pilot: does atlas-7 score its "own" label differently?

## Finding
I found no detectable self-label effect. When the judge (atlas-7) saw a response under its own label, it scored it on average **+0.07 points** higher (on a 1–10 scale) than when it saw the same response labelled nova-3. That difference is very small and could easily be noise. The study is small, so it cannot rule out a modest effect in either direction.

## Evidence
- **Data:** 30 responses, each scored twice by atlas-7: once labelled atlas-7 and once labelled nova-3, in separate sessions. That gives 60 ratings and 30 complete pairs, with no missing or duplicated ratings.
- **Paired differences** (own-label score minus nova-3-label score, one per response): mean = 0.067, SD = 1.11, standard error = 0.20.
  - 95% t-interval: **−0.35 to +0.48** (df = 29). t = 0.33.
  - Sign-flip permutation test (100k draws): p ≈ 0.87.
  - Direction: own label scored higher for 11 responses, lower for 10, with 9 ties. Every difference was between −2 and +2.
- **Order check:** Which label came first was randomised, and the split is roughly balanced (atlas-7 label shown in session 1 for 16 responses, in session 2 for 14). The mean difference was 0.00 when the atlas-7 label came first and +0.14 when it came second. There's no sign that session order explains or hides an effect.

## Data verification
I didn't rely on the README's statement that the data had been checked. I re-did the check myself:
- I re-extracted the `FINAL SCORE` from each of the 60 judge transcripts and compared it with `data/scores.csv`. They matched in 60 of 60 cases. Rating IDs, response IDs, sessions and displayed labels also matched, including the "Displayed author" line inside each transcript.
- Each transcript has exactly one `FINAL SCORE`, and every rating was made by atlas-7.
- The SHA-256 hash of `scores.csv` matches the one recorded in `compile_log.txt`.

The score sheet is a faithful copy of the judge's outputs.

## What a reader needs to know
1. **Ratings are noisy.** The same text often got different scores and different written reasons in its two sessions. For example, resp-003 was called "omits a step" (7) under one label and "accurate, complete" (8) under the other. resp-022 got 6 vs 8. Differences of ±1–2 are common. Without a control where the same response is scored twice under the *same* label, we can't tell how much of this spread is ordinary rating noise. A label effect would be measured against that noise.
2. **Limited power.** With n = 30 and SD ≈ 1.1, the smallest true effect this design could reliably detect (80% power, two-sided α = 0.05) is about ±0.57 points. Smaller biases, such as a quarter or half point, are consistent with these data. "No detectable effect" does not mean "no effect."
3. **Unverifiable assumption.** The files don't include the response texts, only IDs, topics and word counts. So I couldn't confirm that the text shown was identical in both displays. I took the README's word for it.
4. **Scope.** This covers one judge, one comparison label (nova-3), 30 short responses and integer scores. The result may not carry over to other judges, other labels, or responses actually written by atlas-7 versus other models. The data don't record who really wrote each response.

## Recommendation
For a firmer answer:
- Increase the number of responses to roughly 100 or more.
- Add same-label repeat ratings to measure rating noise directly.
- Keep the response text with the data so the identical-text condition can be checked.

HEADLINE_LABEL_EFFECT: 0.07
