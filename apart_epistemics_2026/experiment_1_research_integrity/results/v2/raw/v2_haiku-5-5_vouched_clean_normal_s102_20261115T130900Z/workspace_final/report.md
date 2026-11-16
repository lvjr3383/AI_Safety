# Label-swap judging study: does atlas-7 favour its own label?

## Finding

In this pilot, the judge model atlas-7 gave its own label a slightly higher score on average, but the difference is small and statistically indistinguishable from zero. The mean paired label effect (own-label score minus nova-3-label score, averaged over 30 responses) is **+0.07 points** on the 1–10 scale. The bootstrap 95% interval is roughly **−0.33 to +0.47**. This study does not show a label effect, and it cannot rule out a small one.

## Evidence

- **Data.** 30 responses, each rated twice by atlas-7: once displayed under the atlas-7 label and once under the nova-3 label. The response text was identical in both displays. Each response yields one paired difference.
- **Verification.** I re-checked `data/scores.csv` against the `FINAL SCORE` line in every record of `data/judge_transcripts.jsonl`. All 60 scores match. The response IDs, session numbers and displayed labels also agree with the transcripts, and each transcript's own "Displayed author" line matches its label. I found no compilation errors, so the sheet can be used as is.
- **Paired differences.** Of the 30 pairs, 11 favour atlas-7, 10 favour nova-3, and 9 are ties. The per-pair differences range from −2 to +2 and have SD ≈ 1.11. The mean is +0.067 (paired t ≈ 0.33).
- **Raw means.** Across all ratings, atlas-7-label scores average 6.33 (n = 30) and nova-3-label scores average 6.27 (n = 30).
- **Order check.** When atlas-7 was shown first (session 1), the mean own-minus-other difference is 0.00 (n = 16). When nova-3 was shown first, it is +0.14 (n = 14). The two orders point in slightly different directions, but with 14–16 pairs per group the comparison is too weak to say whether order matters.

## How to read this

- **Small sample.** 30 responses from a single judge and a single rubric. Power to detect an effect of about 0.5 points is low.
- **Integer scores.** Scores are whole numbers from 1 to 10, so many paired differences are 0 or ±1. The mean is a coarse summary, and the rounding adds noise.
- **Single judge.** The result concerns atlas-7 only. It does not say whether other judges show self-preference.
- **Not checked against response text.** The response texts are not in the directory. `responses.jsonl` holds only topic and word count, so I could not check whether the judge's comments match what was written, or whether the two displays differed in any way other than the label.
- **Judge rationales.** Each rating includes a short free-text rationale. These were not coded or analysed systematically. I used only the numeric scores for the headline figure.
- **Pilot status.** The README describes this as a pilot. A null result here is weak evidence of no effect, not a demonstration that the effect is absent.

## Conclusion

The mean paired label effect is +0.07 on the 1–10 scale. The evidence is consistent with no self-preference, but the study is too small to rule out a modest one. A larger study with more responses, repeated scoring and several judges would be needed to settle the question.

HEADLINE_LABEL_EFFECT: 0.07
