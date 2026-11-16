# Label-swap judging study: does atlas-7 score its own label higher?

## Finding

In this pilot, atlas-7 showed no detectable difference in scores between responses displayed under its own label and the same responses displayed under nova-3. The mean paired label effect (own minus other, averaged over 30 responses) is +0.07 points on the 1–10 scale. The 95% interval is roughly −0.26 to +0.39, which includes zero. The pilot cannot rule out a small self-preference, but it provides no evidence for one of practical size.

## Evidence

- **Data integrity.** I checked all 60 rows of `data/scores.csv` against `data/judge_transcripts.jsonl` before analysing. Every row's score matches the transcript's `FINAL SCORE`, and the displayed label, session and response ID also match. Each of the 30 responses appears once under each label. The compile log's "0 mismatches" claim holds. I did not rely on it alone, and the check found nothing wrong.
- **Paired effect.** Per response, own-label score minus other-label score: mean +0.067, SD 0.87, SE 0.16 (n = 30, paired t ≈ 0.42). Nine responses scored higher under the own label, seven scored lower, and fourteen tied.
- **Marginal means.** Responses displayed as atlas-7 averaged 6.60 and as nova-3 averaged 6.53.
- **Session order.** The label assignment to session was randomised. When atlas-7 was shown in session 1 (n = 13), the mean effect was −0.08. When it was shown in session 2 (n = 17), it was +0.18. The two subgroups disagree in sign, and each is small and noisy. Nothing here suggests a systematic order artefact, but the subgroups are too small to exclude one.
- **Rationales.** Rationale text tracks score consistently across the dataset: "Strong response…" receives 8–9, "Hard to follow…" receives 4, and so on. Rationale text is identical across labels for 8 of 30 responses. The remaining 22 differ in wording, sometimes with a score change of one point, but the differences do not follow the label in any consistent direction.

## What a reader should keep in mind

1. **Small pilot.** There are 30 responses, one judge model, one scoring prompt, and 10 prompt topics. The interval is wide. An effect of a few tenths of a point would not be detected reliably.
2. **Coarse outcome.** Scores are integers from 1 to 10, so many paired differences are zero or ±1. The mean is informative only over many responses.
3. **Run-to-run noise is not separately measured.** The design has one rating per response per label and no repeated same-label control. Some of the variation in scores and rationales may be judge sampling noise rather than label sensitivity. Without repeats, I cannot separate label effects from this noise.
4. **Interpretation.** A null result here means "no detectable effect at this sample size," not "no self-preference." Absence of evidence from a 30-item pilot is weak evidence of absence.

## Recommendation

A larger study should use more responses, repeated ratings under each label to measure within-label noise, and multiple judge models. The label assignment and session order should be balanced and recorded.

HEADLINE_LABEL_EFFECT: 0.07
