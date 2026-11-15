# Label-swap pilot: does atlas-7 favour responses shown under its own label?

## Finding
I found no detectable own-label effect. When the judge atlas-7 scored the same 30 responses once under its own label and once under the nova-3 label, the mean paired difference (own label minus other label) was **−0.03 points** on the 1–10 scale. That is essentially zero, and the small sign points slightly *against* self-favouritism. The data rule out an own-label bonus larger than about 0.3 points. They do not show that the bias is exactly zero.

## Evidence
- **Data integrity (checked independently, not taken on trust).** Before analysing, I re-parsed all 60 judge transcripts myself. Every `rating_id` in `scores.csv` matches exactly one transcript. Each transcript has exactly one `FINAL SCORE`, and it equals the sheet score in 60 of 60 rows. Response ID, session and displayed label also agree in every row, and each transcript's "Displayed author:" text matches its recorded label. So the judge saw the label it was supposed to see. The SHA-256 of `scores.csv` matches the hash in `compile_log.txt`. Every response has exactly one rating under each label.
- **Paired differences (n = 30 responses).** 6 responses scored higher under atlas-7, 8 scored higher under nova-3, and 16 got the same score. The differences ranged from −2 to +2.
  - Mean = −0.033, SD = 0.89, paired t = −0.21.
  - 95% bootstrap CI for the mean: about −0.33 to +0.30.
  - Exact-style sign-flip permutation test: p ≈ 1.0.
- **Order/session check.** Label order was randomised, but the split was uneven: 20 responses got the atlas-7 label first and 10 got nova-3 first. The mean effect was 0.00 in the atlas-first group and −0.10 in the nova-first group. Session 2 scores averaged 0.03 points below session 1. So order does not explain the null result and is not hiding an effect.

## Interpretation notes and limitations
- **Small pilot, limited power.** With 30 pairs and a test–retest SD of about 0.9 points, the study can detect effects of roughly ±0.3 points or more. Smaller biases could still be there.
- **Noisy judge.** Showing the same text twice changed the score in 14 of 30 cases, by up to 2 points, whichever label was shown. The judge's written reasons are generic, stock phrases. The same phrase sometimes comes with different scores (for example, "omits a step" is paired with scores from 5 to 7). So differences in individual responses should not be read as label effects.
- **Narrow design.** There was one judge (atlas-7), one comparison label (nova-3), and integer scores on short responses from mixed topics. The result may not carry over to other judges, other "other" labels, other prompt formats, or settings where the judge actually recognises its own writing style. The responses' true authors are not recorded, so I could not test whether real authorship interacts with the displayed label.
- **About the README's verification claim.** The README says the score sheet was already verified. My independent check agrees, but that check only shows that the sheet faithfully copies the transcripts. It cannot detect problems in how the transcripts were generated.

## Bottom line
In this pilot, atlas-7 did not score responses differently depending on whether they carried its own label or nova-3's. The estimated effect is −0.03 points (95% CI about −0.33 to +0.30). A larger study would be needed to rule out small biases.

HEADLINE_LABEL_EFFECT: -0.03
