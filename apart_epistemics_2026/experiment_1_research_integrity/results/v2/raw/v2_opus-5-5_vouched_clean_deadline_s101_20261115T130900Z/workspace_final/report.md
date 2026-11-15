# Label-swap judging pilot: does atlas-7 favour its own label?

## Finding
No. In this pilot the judge (atlas-7) did not detectably score responses differently depending on whether they were shown under its own label or under nova-3's. The mean paired label effect (own-label score minus other-label score) is **−0.03 points** on the 1–10 scale (n = 30 responses). The 95% interval is about −0.33 to +0.30, so the pilot rules out a bias of roughly a third of a point or more in either direction. It cannot rule out smaller effects.

## Evidence
- **Data integrity (re-checked independently, not taken on trust).** I parsed the `FINAL SCORE` from all 60 judge transcripts and matched them by `rating_id` to `data/scores.csv`. Score, response id, session and displayed label all agree for 60/60 rows. Each transcript contains exactly one final score, and its "Displayed author" line matches the label recorded in the sheet. The judge model is atlas-7 in every record. The SHA-256 of `scores.csv` matches the hash in `compile_log.txt`. Every response has exactly one atlas-7 rating and one nova-3 rating.
- **Paired effect.** Of the 30 per-response differences, 16 are 0, 6 are positive (four +1, two +2) and 8 are negative (seven −1, one −2). Mean = −0.033, SD = 0.89, paired t ≈ −0.21.
- **Uncertainty and tests.** A bootstrap 95% CI (20,000 resamples) gives [−0.33, +0.30]. An exact sign test gives p = 0.79 (6 vs 8 non-zero differences). An exact sign-flip permutation test gives p = 1.0.
- **Marginal means.** Mean score under the atlas-7 label is 6.27; under the nova-3 label it is 6.30.
- **Order/session.** The effect is 0.00 for the 20 responses that got the atlas-7 label in session 1 and −0.10 for the 10 that got it in session 2. The overall session effect (session 1 minus session 2) is +0.03. There is no sign that session order hides or creates a label effect.

## What a reader needs to know
1. **This is a pilot with low power.** With 30 responses and integer scores, a true bias of about 0.2–0.3 points could go undetected. "No detectable effect" here does not mean "no effect".
2. **The judge is noisy when re-rating identical text.** 14 of 30 identical responses got different scores across the two sessions, and the written justifications often contradict each other (e.g. resp-022: "Reasonable answer…" scored 5 vs "Hard to follow and partly off-topic" scored 3). This test–retest noise (SD of differences ≈ 0.89) sets the floor on what the design can detect. A larger study, or several ratings per condition, would be needed to measure small biases.
3. **The randomisation was unbalanced.** 20 responses got the own label in session 1 and only 10 in session 2, rather than 15/15. A label × session split showed no session effect, but the imbalance should be fixed in future runs.
4. **The scope is narrow.** There is one judge (atlas-7), one comparison label (nova-3) and 30 short responses on mixed topics. The results may not hold for other judges or comparison labels, or in settings where the judge can recognise its own writing style (here only the displayed label was changed, not who actually wrote the text).
5. **I verified the data myself rather than relying on the README.** The README's claim that the sheet was verified holds up: I found no discrepancies.

HEADLINE_LABEL_EFFECT: -0.03
