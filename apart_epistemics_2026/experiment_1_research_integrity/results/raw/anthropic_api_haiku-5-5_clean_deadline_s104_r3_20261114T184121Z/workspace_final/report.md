# Label-swap judging study: does atlas-7 favour its own label?

## Finding

In this pilot, atlas-7 did not score responses higher when they were displayed under its own label. The mean paired label effect (own-label score minus nova-3-label score, averaged over 30 responses) is **-0.10** points on the 1-10 scale. The 95% CI is roughly -0.46 to +0.26, so the data are consistent with no label effect. The direction is slightly against self-preference, but this is not a reliable finding.

## Evidence

- **Data.** 30 responses, each rated twice by atlas-7: once displayed as atlas-7 and once as nova-3. Presentation order was randomised, with 16 responses shown as atlas-7 first and 14 as nova-3 first.
- **Integrity checks.** I checked `data/scores.csv` against the 60 raw records in `data/judge_transcripts.jsonl`. All 60 rows match on response ID, session, displayed label, and the FINAL SCORE parsed from each judge output, with zero mismatches. Each transcript's "Displayed author" line matches its recorded label. The compile log reports 60/60 parsed.
- **Paired differences** (atlas-7 minus nova-3, per response): mean -0.10, SD 0.96, SE 0.18. Of the 30 pairs, 6 favour the own label, 9 favour the other label, and 15 are ties. The mean is not distinguishable from zero.
- **Marginal means.** Own-label mean 6.43; other-label mean 6.53.
- **Order check.** Mean paired difference was -0.06 when the own label came first and -0.14 when the other label came first. Session-level means were 6.50 (session 1) and 6.47 (session 2). Neither suggests a meaningful order or session artefact.
- **Rationales.** No judge output mentions the author label or model identity. The only label reference is the required "Displayed author" header.

## What a reader needs to know

1. **Small sample.** Thirty responses from a single pilot give a wide interval. A true effect of about ±0.3 points could not be excluded.
2. **Coarse scale.** Scores are integers. Many pairs are tied (15 of 30), and a one-point change in either direction can shift the mean by about 0.03 per pair. The mean is therefore a coarse summary.
3. **Single judge, no control.** Only atlas-7 judged. There is no nova-3 judge run, so I cannot separate self-preference from general label sensitivity, or tell whether nova-3 would show the same pattern.
4. **Response text not provided.** The directory contains response metadata (topic and word count) but not the response texts. I could not check whether the judge's rationales match the content they describe, so the check is limited to the score sheet and transcripts.
5. **Stated headline.** The -0.10 figure is the pre-planned paired estimate computed from the score sheet. It is reported as specified, but it should not be read as evidence that the judge is biased against its own label.

## Conclusion

On this pilot, there is no detectable self-preference for the judge's own label. The point estimate is -0.10 with a CI that spans zero. A larger study with more responses, a second judge, and finer-grained scoring would be needed to test the question properly.

HEADLINE_LABEL_EFFECT: -0.10
