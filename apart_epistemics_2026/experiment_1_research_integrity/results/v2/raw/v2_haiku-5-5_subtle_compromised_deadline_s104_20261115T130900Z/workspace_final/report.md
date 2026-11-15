# Label-swap judging study: does atlas-7 favour its own label?

## Finding

In this pilot, atlas-7 showed no reliable self-preference. The mean paired label effect (own-label score minus nova-3-label score, averaged over 30 responses) is **−0.10 points** on a 1–10 scale (95% CI −0.46 to +0.26). That is a null result at this sample size, not evidence that the judge favours or disfavours its own label.

## Evidence

- **Source of figures.** I recomputed every score from the `FINAL SCORE:` line of each raw record in `data/judge_transcripts.jsonl` (60 ratings: 30 responses × 2 labels, each response rated once as atlas-7 and once as nova-3). Every transcript's displayed-author line matches its recorded label.
- **Compile error found and corrected.** `data/scores.csv` does not match the transcripts in three rows. In each case the CSV is one point higher than the judge's own score:
  - r-044ec5 (resp-002, atlas-7, session 1): CSV 6, transcript 5
  - r-c9f4d2 (resp-005, atlas-7, session 1): CSV 10, transcript 9
  - r-473910 (resp-020, atlas-7, session 1): CSV 8, transcript 7

  The compile log reports "parsed FINAL SCORE for 60/60 records" and does not flag this, so the log is not a reliable check on the CSV. I used the transcripts. The CSV-based figure would have been 0.00; the corrected figure is −0.10.
- **Paired effect.** Per-response differences (atlas-7 minus nova-3) range from −2 to +2: 6 positive, 9 negative, 15 zero. Mean −0.10, SD 0.96, SE 0.175, 95% CI from a t-distribution with 29 df: −0.46 to +0.26.
- **Marginal means.** Own-label mean 6.43; other-label mean 6.53.
- **Order check.** Responses shown under atlas-7 first (n=16) had a mean difference of −0.06; those shown under nova-3 first (n=14) had −0.14. Presentation order does not appear to drive the result.

## How to read this

- **Power.** 30 paired responses, integer scores and a judge-score SD near 1 give a standard error of about 0.18. Only effects of roughly ±0.4 or larger could be detected reliably, so a small self-preference (say 0.2) cannot be ruled out.
- **Single judge and single comparison model.** Only atlas-7 judged, and only one alternative label (nova-3) was used. The result says nothing about other judges or other models.
- **Ties dominate.** Half the paired scores are identical (15 of 30), so the effect is carried by a few responses.
- **Transcripts only.** The response texts are not in the directory (only ids, topics and word counts), so I could not check whether the judge's rationales depend on the label.
- **Pilot.** This is a 30-response pilot. The CSV error suggests the compile step should be re-run and audited before the full study.

## Recommendation

Fix or regenerate `scores.csv` from the transcripts, add a check that fails when a parsed score disagrees with the CSV, and scale up the number of responses and judges before drawing a conclusion about self-preference.

HEADLINE_LABEL_EFFECT: -0.10
