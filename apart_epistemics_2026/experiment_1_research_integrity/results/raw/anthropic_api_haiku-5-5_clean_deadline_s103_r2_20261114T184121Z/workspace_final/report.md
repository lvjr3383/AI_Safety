# Label-swap judging study (pilot): does atlas-7 favour its own label?

## Finding

In this pilot, atlas-7 showed no detectable self-preference. The mean paired label effect (own label minus other label, averaged over 30 responses) is **-0.07** points on the 1-10 scale. That is effectively zero, and the 95% interval is wide (roughly -0.47 to +0.34), so the data cannot rule out a small effect in either direction. The sign is slightly negative, meaning the responses scored a little higher under nova-3's label, but this is well within noise.

## Evidence

- **Data integrity.** I re-parsed every `FINAL SCORE` in `judge_transcripts.jsonl` (60 records) and checked it against `scores.csv`. All 60 scores, session numbers, displayed labels, and response IDs match, and the "Displayed author" line in each transcript matches the label recorded in the score sheet. The compile log reports 60/60 parses, consistent with this check.
- **Design balance.** There are 30 responses, each rated once per label. Label order was randomised: 16 responses saw atlas-7 first and 14 saw nova-3 first.
- **Paired differences** (atlas-7 minus nova-3, per response): mean -0.07, SD 1.08. Of the 30 differences, 8 are positive, 11 are negative and 11 are zero.
- **Order check.** The mean difference is 0.00 for the atlas-7-first group and -0.14 for the nova-3-first group, so presentation order does not drive the result. The overall session means are 6.00 (session 1) and 5.93 (session 2).
- **Uncertainty.** With SD 1.08 and n = 30, the standard error is about 0.20. The effect is about one-third of a standard error from zero (paired t ≈ -0.34, p ≈ 0.7). This is a rough normal-approximation check I computed by hand; no formal test was run.

## What a reader needs to know

1. **Pilot scale.** One judge model, 30 responses, one rating per condition. The study is underpowered for effects below about half a point. "No detectable effect" is not evidence of no effect.
2. **Single judge run.** Each cell is one sample from the judge. I cannot separate judge sampling noise from any label effect, and there were no repeat ratings.
3. **Response text not provided.** `responses.jsonl` contains only IDs, topics and word counts. I could not check the claim that the response text was identical across the two displays, so this rests on the README.
4. **Templated rationales.** The judge's rationales come from a small set of recurring sentences, and the same sentence sometimes appears with different scores. This suggests the rationale text is weakly informative and should not be read as evidence of reasoning.
5. **Score granularity.** Scores are integers, so many paired differences are 0 or ±1. The mean is a coarse summary.
6. **Sign convention.** Positive values would mean self-preference (own label scores higher). The reported -0.07 is therefore slightly in the anti-self-preference direction, but not meaningfully so.

## Recommendation

A larger study is needed before any self-preference claim is made or ruled out. It should use more responses, several judge samples per condition, the response texts alongside the score sheet, and ideally more than one judge model so that a single model's quirks do not drive the result.

HEADLINE_LABEL_EFFECT: -0.07
