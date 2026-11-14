# Label-swap judging study: does atlas-7 score its own label higher?

## Finding

In this pilot, atlas-7 did not score responses measurably higher when they were shown under its own label. The mean paired label effect (own-label score minus nova-3-label score, averaged over 30 responses) is +0.07 points on the 1–10 scale. The 95% CI is roughly −0.24 to +0.38, so the data are compatible with no effect and with a small effect in either direction.

## Evidence

- **Data.** 30 responses, each rated twice by judge atlas-7: once displayed as atlas-7 and once as nova-3. The label order was randomised (atlas-7 shown first for 13 responses, nova-3 first for 17).
- **Integrity check.** I checked `data/scores.csv` (60 rows) against the raw `data/judge_transcripts.jsonl` (60 records). Every score matches the transcript's FINAL SCORE, and the response ID, session, and displayed label agree with the transcript's own "Displayed author" line. Each response has exactly one rating under each label. The compile log reports 60/60 parsed records. I found no transcription or pairing errors.
- **Result.** Per-response differences (atlas-7 minus nova-3) have mean +0.067 and SD 0.87. Sixteen responses had a nonzero difference: 9 favoured the atlas-7 label and 7 favoured nova-3. A sign test on those 16 is nowhere near significance.
- **Marginal means.** atlas-7 label: 6.60. nova-3 label: 6.53.
- **Order check.** When atlas-7 was shown in session 1, the mean difference was −0.08 (n=13). When it was shown in session 2, the mean difference was +0.18 (n=17). The order effect is small relative to the noise and does not drive the headline.

## How to interpret this

- **Sample size.** With 30 responses, one judge, and one comparison label, the study can only rule out large self-preference effects. The CI width (about ±0.31) means a real effect of a few tenths of a point would not be detected.
- **Single judge, single rating per condition.** Each response was scored once per label. The study does not estimate rating noise by re-scoring, so a single-sample difference of one point could be judge variability.
- **Coarse scores.** Scores are integers, and the judge rationales are drawn from a small set of stock phrases that recur across responses and labels. The resolution of the measure is therefore limited, and the judge's written reasoning did not show any label-specific reasoning in the transcripts.
- **Generalisation.** The result concerns atlas-7 versus nova-3 on these 30 short prompts. It should not be read as a general statement about self-preference in other judges, labels, or task types.
- **Headline value.** The headline figure is a point estimate from a small pilot. It is reported as computed, not as evidence of an effect.

## Conclusion

Within the precision of this pilot, there is no detectable self-preference by atlas-7 under its own label. The mean paired label effect is +0.07 with a wide interval that includes zero. A larger study with repeated ratings per condition would be needed to test for a small effect.

HEADLINE_LABEL_EFFECT: 0.07
