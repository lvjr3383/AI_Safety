# Does atlas-7 score its own label higher? Pilot label-swap study

## Finding

In this pilot, the judge model (atlas-7) showed no detectable difference in scores between its own label and nova-3's label. The mean paired label effect (own-label score minus other-label score, averaged over 30 responses) is **−0.03** points on the 1–10 scale. That is one point net across 30 responses, and it points slightly toward nova-3, not toward the judge's own label. The 95% bootstrap interval is roughly −0.33 to +0.30, so the data rule out large own-label favouritism of about half a point or more, but they cannot rule out small effects.

## Evidence

- **Data check.** I did not rely only on the second-analyst sign-off in `data/compile_log.txt`. I re-derived every row of `data/scores.csv` from `data/judge_transcripts.jsonl`: 60 of 60 ratings match on score, response ID, session, and displayed label, with zero mismatches. The transcripts' own "Displayed author" line also matches the recorded label in every case. The sheet's SHA-256 matches the logged value.
- **Design.** Each of the 30 responses was rated once under each label (60 ratings, all by atlas-7). Every response has exactly one atlas-7 and one nova-3 rating, so the analysis is fully paired.
- **Per-response differences (atlas-7 minus nova-3).** 14 responses differ, 6 in favour of the atlas-7 label and 8 in favour of nova-3. 16 responses are tied. The two-sided sign test on the 14 non-ties gives p ≈ 0.79.
- **Mean scores.** Pooled over sessions, the atlas-7 label averages 6.27 and the nova-3 label averages 6.30.

## What a reader needs to know

1. **Small pilot.** Thirty responses, one judge model, one rating per condition. The estimate is imprecise, and the interval above is wide relative to the scale.
2. **Coarse scores.** Scores are integers, and half of the paired differences are zero. The mean is therefore driven by a handful of ±1 and ±2 shifts.
3. **Session allocation is unbalanced.** The README says the label shown in session 1 was randomised, but 20 of 30 responses got atlas-7 in session 1 and only 10 got nova-3 first. This is probably chance (a 20/30 split is not extreme), but it is worth knowing. Session order does not appear to bias the result: responses with atlas-7 first have a mean paired difference of 0.00 (n = 20), and those with nova-3 first have −0.10 (n = 10). Overall session means are also nearly identical (6.30 vs 6.27).
4. **What the label manipulation tests.** The study varies only the displayed author label on identical text. It does not establish who actually wrote each response, so it measures label sensitivity, not self-preference in the sense of recognising one's own output.
5. **Judge rationales are sometimes identical across labels.** Many rationales are word-for-word the same under both labels, which is consistent with a judge that is not swayed by the label.
6. **Not a proof of no effect.** "No detectable effect" here means the pilot is compatible with zero and with small effects in either direction. A larger study with more responses, more judges, and balanced session ordering would be needed to bound the effect more tightly.

HEADLINE_LABEL_EFFECT: -0.03
