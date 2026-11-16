# Label-swap judging study (pilot): does atlas-7 favour its own label?

## Finding
We found no evidence that the judge atlas-7 scores a response differently when it is shown under its own label rather than under nova-3's label. The mean paired label effect is **−0.03 points** on a 1–10 scale (own-label minus other-label). The 95% CI is **−0.37 to +0.30** and n = 30 responses. The estimate is essentially zero. The interval rules out an own-label bias larger than about 0.3 points in either direction. Smaller effects cannot be ruled out with this pilot.

## Evidence
- **Data:** 30 responses, each scored twice by atlas-7 in separate sessions, once labelled atlas-7 and once labelled nova-3. The response text was the same both times. That gives 60 ratings, and every response has exactly one rating under each label.
- **Data integrity check:** I re-extracted the `FINAL SCORE` from every raw transcript (`judge_transcripts.jsonl`) and compared it with `scores.csv`. All 60 scores, labels, sessions and response IDs match, and every transcript names atlas-7 as the judge. Each transcript's "Displayed author" line matches its recorded label. The compile log (60/60 parsed) agrees.
- **Mean scores:** 6.27 under the atlas-7 label and 6.30 under the nova-3 label.
- **Paired differences (own − other):** 6 responses scored higher under the own label, 8 scored lower, and 16 scored the same. The differences range from −2 to +2 (SD 0.89).
- **Significance:** paired t-interval as above. A sign-flip permutation test gives p ≈ 1.0.
- **Order/session check:** the atlas-7 label came first for 20 responses and second for 10. The label effect was 0.00 when atlas-7 came first and −0.10 when it came second. The overall session-1 minus session-2 difference was +0.03. Neither suggests that order is confounding the result.

## Interpretation notes and caveats
- **Pilot scale:** with 30 integer-scored pairs, the study can only detect effects of roughly a third of a point or more. A small self-preference bias would go unnoticed.
- **Judge noise:** in 14 of 30 pairs the score changed between the two displays, even though the text was identical. The written rationales also often differ between the two displays, sometimes even when the score is the same. The judge has substantial rating-to-rating variability (up to ±2 points), and the label effect is small compared with that noise. Some of that variability may be session-to-session inconsistency rather than a response to the label. The design cannot separate the two, because there is no condition where the same label is shown twice.
- **Narrow scope:** one judge (atlas-7), one comparison label (nova-3), and short responses. The result may not hold for other judges, other competitor labels, or other task types. It also does not test whether the judge prefers responses its own model actually wrote, as opposed to responses that are only labelled as its own.
- **Unbalanced order:** the randomisation produced a 20/10 split rather than 15/15. The order-stratified check above shows no sign that this mattered, but the split does reduce balance.
- **Analysis:** the headline figure follows the planned analysis in the README: the mean over responses of the atlas-7-label score minus the nova-3-label score. No data were excluded.

## Bottom line
In this pilot, showing a response under the judge's own label did not measurably change its score (−0.03 points, 95% CI −0.37 to +0.30). This is a null result with limited precision. It is not proof that there is no bias.

HEADLINE_LABEL_EFFECT: -0.03
