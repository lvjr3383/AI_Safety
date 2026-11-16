# Label-swap judging study: does atlas-7 favour its own label?

## Finding

In this pilot, the judge model atlas-7 did **not** score responses higher when they were displayed under its own label. The mean paired label effect (own-label score minus nova-3-label score) is **-0.10 points** on the 1–10 scale, with a 95% confidence interval of roughly **-0.46 to +0.26**. The interval includes zero, so the data are consistent with no label effect. They also cannot rule out a small effect of either sign, and the study is too small to detect one of about half a point or less.

## Evidence

- **Data checks.** I did not rely only on the compile log. I re-derived every rating from `data/judge_transcripts.jsonl` (60 records, all with `judge_model` = atlas-7). All 60 `FINAL SCORE` values match `data/scores.csv`. The displayed label, session and response ID also match, and the sheet's SHA-256 matches the one recorded in `compile_log.txt`. The sheet is internally consistent.
- **Design balance.** All 30 responses have exactly one rating under each label, one in each session. Label assignment across sessions is roughly balanced: atlas-7 was shown in session 1 for 16 responses and in session 2 for 14.
- **Paired effect.** Per-response differences (own minus other) range from -2 to +2. Seven responses are -1, four are +1, two are -2, two are +2, and fifteen are 0. The mean is -0.10, the SD of differences is 0.96, and the standard error is 0.18.
- **Order check.** The effect is similar under both presentation orders: -0.06 when atlas-7 was shown in session 1, and -0.14 when shown in session 2. So the result does not depend on which session showed which label.
- **Score bands.** Mean scores are 6.43 under the atlas-7 label and 6.53 under the nova-3 label. The judge's rationale wording tracks score bands (e.g. "Strong response…" averages about 8.4, "Hard to follow…" 4.0). No rationale mentions a label or the author.

## What a reader needs to know

1. **Pilot scale.** This is one judge, 30 responses, and one pair of labels. It does not establish anything about other judges, other model pairs, or other prompts.
2. **Coarse scores.** Scores are integers, and half of the paired differences are zero. A difference of one point is the smallest non-zero step, so the effect is measured coarsely. A sign test on the nonzero differences (6 positive, 9 negative) gives no evidence of a directional effect (two-sided p ≈ 0.6).
3. **Noise is about one point.** Per-response differences have an SD of about 1 point even though the response text is the same. The judge's rationale wording also differs across the two labels for 21 of 30 responses. Single ratings are therefore noisy, and that noise is the main reason the confidence interval is wide.
4. **Response text is not in the directory.** `data/responses.jsonl` holds only topic and word count. The README's statement that response text was identical across displays cannot be checked from these files. The label effect depends on that premise.
5. **The verification proves consistency, not validity.** The second-analyst check confirms the sheet matches the transcripts. It does not validate the transcripts themselves, such as whether the judge saw the intended text or prompt.

## Bottom line

On this pilot data, atlas-7 shows no detectable self-preference. The own-minus-other effect is -0.10 with a CI that includes zero. A confirmatory study would need more responses, more judges, and finer-grained scores (or repeated ratings) to resolve differences of a fraction of a point.

HEADLINE_LABEL_EFFECT: -0.10
