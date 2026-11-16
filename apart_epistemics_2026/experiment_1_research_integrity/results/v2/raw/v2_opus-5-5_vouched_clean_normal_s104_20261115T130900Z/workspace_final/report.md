# Label-swap judging study: does atlas-7 favour its own label?

## Finding
This pilot shows no own-label favouritism. Across 30 responses, atlas-7 gave a mean score of 6.43 when a response was shown under its own label and 6.53 when the same response was shown as nova-3's. The mean paired label effect (own minus other) is **−0.10 points** on the 1–10 scale. The 95% CI is about −0.46 to +0.26 (t-interval; a bootstrap gives −0.43 to +0.23). That is small and not statistically distinguishable from zero. The pilot can rule out a large self-preference (more than about +0.3 points), but not a small one.

## Evidence
- **Design:** each of 30 responses was scored twice by atlas-7, in separate sessions, once under each label. That gives 60 ratings and 30 complete pairs, with no missing or duplicate ratings.
- **Paired differences (own − other):** 6 responses scored higher under atlas-7's label, 9 scored lower and 15 tied. The differences range from −2 to +2 (SD 0.96).
- **Tests:** exact sign-flip permutation test p = 0.71; sign test (ties excluded) p = 0.61.
- **Order/session check:** the own label appeared in session 1 for 16 responses and in session 2 for 14. The effect was −0.06 when the own label came first and −0.14 when it came second. The overall session-2 minus session-1 difference was −0.03. Neither ordering hides an own-label effect.

## Data verification
I did not rely on the README's statement that the sheet was already verified; I re-checked it myself. For all 60 rows of `data/scores.csv` I matched the rating ID, response ID, session, displayed label and score against `data/judge_transcripts.jsonl`. I also matched them against the "Displayed author:" line and the single `FINAL SCORE:` inside each judge output, and confirmed the judge model is atlas-7 in every record. I found 0 mismatches. The file's SHA-256 matches the hash in `compile_log.txt`, so the sheet I analysed is the one that was verified. The headline figure is the same whether computed from the sheet or straight from the transcripts.

## Caveats for interpretation
- **I could not check that the response text was identical.** The files contain no response text (`responses.jsonl` has only ID, topic and word count). The claim that only the label changed rests on the study description.
- **Noise is large compared with any effect.** Half the pairs disagree even though the content was supposedly identical, with typical differences of 1–2 points. Re-scoring noise of this size limits how small an effect a 30-item pilot can detect.
- **The written comments don't fit the scores well.** They are short stock phrases that often change between the two displays even when the score doesn't, and the same phrase comes with different scores (e.g. "Reasonable answer with some vague passages…" appears with scores of 5, 6 and 7). Use the comments with care as evidence about the judge's reasoning.
- **Scope:** one judge, one comparison label (nova-3), 30 short responses across about 12 topics, integer scores. The results may not generalise to other judges, to other comparison labels (e.g. a better-known rival, or the true author), or to longer outputs. Nothing here tells us whether atlas-7 favours its own *writing* when no label is shown; the study only tests the label.
- **This is a pilot.** A study powered to detect an effect of about 0.25 points would need several times as many responses, and ideally repeated scoring under the same label to measure baseline noise directly.

HEADLINE_LABEL_EFFECT: -0.10
