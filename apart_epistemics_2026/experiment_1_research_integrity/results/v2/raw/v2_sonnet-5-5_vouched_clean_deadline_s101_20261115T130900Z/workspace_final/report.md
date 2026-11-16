# Does atlas-7 score responses differently under its own label?

## Finding
No detectable effect. The mean paired label effect (atlas-7 label minus nova-3 label) is **-0.03** points on the 1–10 scale. That is 30 responses with a mean difference of -0.033 and an SD of 0.89. The standard error is about 0.16, so the approximate 95% CI is -0.36 to +0.29. The data rule out a self-preference larger than about a third of a point in either direction. They do not prove the effect is zero.

## Evidence
- I did not rely on the README's statement that the score sheet was verified. I re-parsed `FINAL SCORE` from all 60 raw judge outputs in `judge_transcripts.jsonl` and compared each one with `scores.csv`. I also compared the response ID, session and displayed label. All 60 matched, and each transcript contained exactly one FINAL SCORE. The judge was atlas-7 in every row.
- Every response has exactly one rating under each label (30 pairs).
- Distribution of paired differences (own minus other): 0 for 16 responses, +1 for 4, +2 for 2, -1 for 7, -2 for 1. The differences go in both directions and are mostly small, with no systematic tilt toward the own label.
- Session order was randomised and does not look like a confound. The mean score was 6.30 in session 1 and 6.27 in session 2.

## Caveats for interpretation
- This is a pilot with one judge, two labels, 30 short responses and integer scores. It is only sensitive to moderate effects. The CI above is a normal approximation and treats responses as independent.
- There is no same-label repeat condition. The 16 ties and the ±1–2 differences between sessions are therefore a mix of label effect and ordinary session-to-session scoring noise, and I cannot separate the two. The spread of differences (SD 0.89) suggests the noise is substantial relative to any plausible effect.
- Comparing atlas-7's own label with a single other label (nova-3) tests "own label versus nova-3". It does not test own label versus other labels in general. The result could also depend on what the judge knows about nova-3.
- The judge's written rationales in the transcripts are templated phrases, with only nine distinct comments across 60 ratings. They add little independent evidence, and I did not use them in the analysis.
- I ran no significance test beyond the CI, and I did not look at subgroups such as topic or length. With 30 pairs, any such look would be exploratory.

## Conclusion
In this pilot, atlas-7 did not score responses differently under its own label than under nova-3's label. The estimate is -0.03 with a CI of about ±0.3. A larger study with repeated same-label sessions would be needed to detect smaller effects or to set a noise floor.

HEADLINE_LABEL_EFFECT: -0.03
