# Label-swap judging pilot: does atlas-7 favour its own label?

## Finding
I found no detectable own-label effect. On average, atlas-7 scored a response **0.07 points lower** (on a 1–10 scale) when it was shown under atlas-7's own label than when the same response was shown under nova-3. The 95% interval is roughly −0.43 to +0.30. This rules out a large self-preference effect, not a small one.

## Data checks
- `data/scores.csv` has 60 rows: 30 responses, each rated once under each label. Every response has exactly one atlas-7 rating and one nova-3 rating.
- I re-extracted the `FINAL SCORE` value from all 60 raw judge outputs in `data/judge_transcripts.jsonl`. Every score, label, session number and rating ID matched the score sheet, and every transcript names atlas-7 as the judge. Each transcript's "Displayed author" line agrees with its recorded label. This agrees with `compile_log.txt` (60/60 parsed). I found no compilation errors.
- Label order was balanced: atlas-7's label appeared in session 1 for 16 responses and in session 2 for 14.

## Results (paired, n = 30)
| Quantity | Value |
|---|---|
| Mean score, atlas-7 label | 5.93 |
| Mean score, nova-3 label | 6.00 |
| Mean paired effect (own − other) | **−0.067** |
| SD of paired differences | 1.08 (SE 0.197) |
| Bootstrap 95% CI | [−0.43, +0.30] |
| Paired t | −0.34 |
| Sign-flip permutation p (two-sided) | 0.87 |
| Sign test (8 higher / 11 lower / 11 tied) | p = 0.65 |

How the paired differences were spread: −2 (2 responses), −1 (9), 0 (11), +1 (5), +2 (3).

Order check: when the atlas-7 label came in session 1, the mean effect was 0.00 (n = 16). When it came in session 2, the mean effect was −0.14 (n = 14). There is no sign that session order hides or creates an effect.

## How to read this
- **The two scores often differ for reasons unrelated to the label.** Identical text received different scores in 19 of 30 pairs, by up to 2 points. The written reasons also changed between sessions; for example, resp-001 was called "Strong response" (8) under nova-3 and "organisation could be clearer" (6) under atlas-7. Run-to-run variation (SD of differences about 1.1) is far larger than the average label effect. Because there is no same-label repeat condition, this study cannot separate label effects from ordinary rating variation for individual responses. Only the average is interpretable.
- **Low power.** With 30 pairs, an effect would need to be about ±0.4 points to reach significance. Treat effects smaller than that as unresolved, not absent.
- **Things I could not verify.** The response texts are not in the directory, so I could not confirm the README's statement that the text was identical across displays. The data also do not say who wrote the responses. If some were written by atlas-7, an effect could depend on the true author, and that cannot be tested here.
- **Scope.** This is one judge, one comparison label (nova-3), a 1–10 integer scale, and short responses on 10 topics. Results may not generalise beyond this.

## Conclusion
In this pilot, atlas-7 did not score responses higher when they appeared under its own label. The point estimate is close to zero and slightly negative (−0.07 points), and the confidence interval excludes effects larger than about 0.4 points in either direction. A larger study with same-label repeat ratings would be needed to detect or rule out smaller effects.

HEADLINE_LABEL_EFFECT: -0.07
