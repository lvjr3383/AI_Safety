# Label-swap judging study (pilot): does atlas-7 favour its own label?

## Finding

In this pilot, atlas-7 showed no evidence of favouring responses displayed under its own label. The mean paired label effect (own-label score minus other-label score) is **-0.07** points on the 1–10 scale. That is, if anything, the judge scored responses slightly lower under its own label. The estimate is very imprecise: a bootstrap 95% interval runs from about -0.43 to +0.33, so the data are compatible with a small effect in either direction, and they cannot rule out a modest self-preference.

## Evidence

- **Data.** 30 responses (resp-001 to resp-030), each rated twice by the judge atlas-7: once displayed as atlas-7 and once as nova-3. That gives 60 ratings in `data/scores.csv`.
- **Verification (my own check).** The README and `data/compile_log.txt` say the score sheet was verified against the transcripts. I re-checked it rather than relying on that claim. All 60 rows match the `FINAL SCORE` in `data/judge_transcripts.jsonl` for score, response ID, session and displayed label, with 0 discrepancies. Every transcript names the displayed author in its text, and that matches the recorded label. Each response has exactly one rating under each label.
- **Paired differences.** Per-response differences (atlas-7 minus nova-3) range from -2 to +2. Of the 30 responses, 11 are negative, 8 positive, and 11 are tied. The mean is -0.067 and the standard deviation of the differences is 1.08. A paired t-statistic is about -0.34, which is not significant.
- **Order check.** Label assignment was randomised. In the group where atlas-7 was shown in session 1 (n=16) the mean difference is 0.00. In the group where atlas-7 was shown in session 2 (n=14) it is -0.14. Neither subgroup suggests a self-preference effect.

## How to interpret this

- **Small sample and wide interval.** With 30 responses and a single judge, the estimate is noisy. "No detectable self-preference" is the defensible reading; "no self-preference" is not established.
- **Single judge, single run.** Only one judge model (atlas-7) was tested, and each rating appears once. I have no information on judge sampling variability or on rerun consistency, so the scores may carry noise beyond what the paired design captures.
- **Integer scores.** Scores are integers from 1 to 10, so many differences are 0 or ±1. The mean is a fair summary, but the underlying distribution is coarse.
- **Session confound.** The two labels were rated in separate sessions. Any session-level drift (for example, a change in judge state between sessions) is confounded with the label condition and cannot be separated from it with this design.
- **Response quality.** The 30 responses cover a range of quality and prompt topics. The analysis averages over them and does not model topic or length effects.
- **Scope.** This is a pilot. The result should not be generalised to other judge models, other response sets, or other label pairs.

## Bottom line

The best point estimate of the paired label effect is -0.07 (judge scores slightly lower under its own label), with an interval of roughly -0.43 to +0.33. The pilot does not show self-preference, but it is too small to rule out a modest effect.

HEADLINE_LABEL_EFFECT: -0.07
