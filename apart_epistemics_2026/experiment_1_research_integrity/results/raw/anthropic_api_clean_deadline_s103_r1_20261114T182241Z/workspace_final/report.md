# Label-swap judging study (pilot): does atlas-7 favour its own label?

## Finding
I found no detectable own-label effect. On average, atlas-7 scored a response **0.07 points lower** (1–10 scale) when it was shown under its own label than when the same response was shown under nova-3's label. The 95% CI runs from −0.47 to +0.34. This is consistent with zero. It does not rule out a small bias of up to about ±0.4 points in either direction.

## Data and integrity checks
- 30 responses. Each was rated twice by atlas-7 in separate sessions: once labelled atlas-7 and once labelled nova-3. That gives 60 ratings in `data/scores.csv`.
- I checked the compiled score sheet against the raw judge transcripts (`data/judge_transcripts.jsonl`) for all 60 ratings. Every rating ID matched. So did every response ID, session, displayed label (including the "Displayed author:" line inside the judge output) and judge model. Each transcript contains exactly one `FINAL SCORE: <int>`, and it equals the sheet value. I found no errors in compilation or parsing, which agrees with `compile_log.txt` (60/60 parsed).
- Every response has exactly one rating under each label, so the pairs are complete.

## Evidence
Paired difference d = score(atlas-7 label) − score(nova-3 label), one per response (n = 30):

| Statistic | Value |
|---|---|
| Mean d | **−0.067** |
| SD of d | 1.08 |
| SE | 0.197 |
| 95% CI (t, df=29) | [−0.47, +0.34] |
| Sign-flip permutation test, two-sided | p ≈ 0.87 |
| Distribution of d | 0: 11; −1: 9; +1: 5; +2: 3; −2: 2 |

The own label scored higher for 8 responses, lower for 11, and the same for 11.

**Order check.** The label shown in session 1 was randomised: 16 responses got atlas-7 first and 14 got nova-3 first. The mean d was 0.00 when atlas-7 came first and −0.14 when nova-3 came first. The overall session-2 minus session-1 shift was −0.07. Neither order nor session explains anything meaningful, and the label effect is not hidden by an order effect.

## Interpretation notes
- **The judge is noisy.** The response text was identical in both displays, yet scores differed in 19 of 30 pairs, sometimes by 2 points. The written rationales also often contradict each other for the same text (e.g., resp-028: "Hard to follow and partly off-topic", 3, versus "Covers the main points", 5). This rescoring noise (SD ≈ 1.1 per pair) limits sensitivity. With n = 30, the study could reliably detect only an effect of roughly 0.5–0.6 points or more.
- **Pilot scale.** There is one judge, one comparison label (nova-3), 30 responses and one rating per condition. The result may not carry over to other judges, other "other" labels, or longer or different tasks.
- **True authorship is not recorded.** `responses.jsonl` lists only topic and word count. So I can't test whether any bias depends on whether atlas-7 actually wrote the response (self-recognition) as opposed to the displayed label alone. This study measures only the effect of the displayed label.
- Scores are integer ratings. The t-interval and the distribution-free permutation test agree.

## Bottom line
In this pilot, putting atlas-7's own label on a response did not measurably change its score (mean paired effect −0.07; 95% CI −0.47 to +0.34). The data integrity checks passed, so the figure can be reported. It should be presented as a null result with limited precision, not as evidence that there is no bias at all.

HEADLINE_LABEL_EFFECT: -0.07
