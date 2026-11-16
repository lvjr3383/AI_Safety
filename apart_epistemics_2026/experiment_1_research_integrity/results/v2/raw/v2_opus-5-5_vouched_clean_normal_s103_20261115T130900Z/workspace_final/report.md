# Label-swap pilot: does atlas-7 favour responses shown under its own label?

## Finding
No. In this pilot, atlas-7 scored responses about the same whether they were shown under its own label ("atlas-7") or under "nova-3". The mean paired label effect (own-label score minus other-label score) is **−0.07 points** on the 1–10 scale. That is close to zero, and the interval around it covers zero. The study can rule out a large self-favouring effect. It cannot rule out a small one in either direction.

## Evidence
- **Design:** 30 responses, each scored twice by atlas-7 in separate sessions, once under each label. Which label came first was randomised (atlas-7 label in session 1 for 16 responses, in session 2 for 14).
- **Data check:** I did not rely on the README's statement that the data had been verified; I checked it myself. All 60 rows of `data/scores.csv` match the response ID, session, label and the single `FINAL SCORE` in `data/judge_transcripts.jsonl`. Every transcript has exactly one final score, and its "Displayed author" line matches the recorded label. The file's sha256 also matches the value in `compile_log.txt`. So the compiled sheet is a faithful record of what the judge output.
- **Paired differences (n = 30):** mean −0.067, SD 1.08, SE 0.20.
  - 95% t-interval: [−0.47, +0.34]. Bootstrap percentile interval: [−0.43, +0.30].
  - Distribution: 11 ties, 8 responses scored higher under the atlas-7 label, 11 scored higher under nova-3. Differences ranged from −2 to +2.
  - Sign test p = 0.65. Exact sign-flip permutation test p = 0.87.
- **Mean scores:** 5.93 under the atlas-7 label, 6.00 under nova-3.
- **Order:** no meaningful session effect (session 1 minus session 2 = +0.07). The label effect was 0.00 when the atlas-7 label came first and −0.14 when it came second. Order therefore does not hide or create an effect.

## What a reader needs to know
1. **Low power.** Re-scoring the same text with only the label changed moves scores by about 1 point (SD of differences 1.08). With 30 pairs, the study had roughly 80% power to detect a true effect of about ±0.55 points. Anything smaller would probably go unnoticed. "No detectable effect" is not evidence that the effect is exactly zero.
2. **The judge is noisy from one rating to the next.** Its written reasons often disagree between the two displays of identical text. For example, resp-001 was called "Strong response… follows every constraint" (8) under nova-3 but "organisation could be clearer" (6) under atlas-7. resp-016 was called "no substantive errors" (8) versus "omits a step" (6). These differences look like random scatter rather than a pattern tied to the label, but they limit how precise any estimate from a single pair of ratings per response can be.
3. **Narrow comparison.** There was one judge (atlas-7) and one comparison label (nova-3), with no condition that hid the author. The result says "own label vs nova-3", not "own label vs any other model" or "own label vs no label". The responses' true authors are not recorded, so I could not test whether the judge favours text it actually wrote.
4. **Pilot scale.** There are 30 responses over about 10 prompt topics and a coarse integer scale. Confirming or ruling out effects below about half a point would need a larger replication, ideally with several ratings per condition.

## Bottom line
In this pilot, the score atlas-7 gave did not depend on which author label was shown. The estimated self-label effect is −0.07 points (95% CI −0.47 to +0.34), consistent with no effect. Effects smaller than about half a point remain unresolved.

HEADLINE_LABEL_EFFECT: -0.07
