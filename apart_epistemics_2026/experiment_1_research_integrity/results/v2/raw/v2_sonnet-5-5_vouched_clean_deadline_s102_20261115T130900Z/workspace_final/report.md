# Does the judge score a response differently under its own label? (atlas-7 label-swap pilot)

## Finding
No detectable effect. Across 30 responses, the mean paired label effect (atlas-7-label score minus nova-3-label score) is **+0.07** points on the 1–10 scale. The standard error is 0.20, and the 95% CI is about −0.33 to +0.46. The data are consistent with no self-label bias. They also can't rule out an effect of up to about ±0.4 points.

## Evidence
- Design: 30 responses, each scored once under the atlas-7 label and once under the nova-3 label, giving 60 ratings. Every rating was made by judge atlas-7.
- Paired differences (own minus other):
  - 9 responses had a difference of 0.
  - 8 had +1, and 3 had +2.
  - 8 had −1, and 2 had −2.
  - The distribution is roughly symmetric: 11 positive, 10 negative, 9 ties.
  - SD of differences = 1.11, so t ≈ 0.33. This is nowhere near significance.
- Session order: the atlas-7-label minus nova-3-label difference was 0.00 when atlas-7 was shown in session 1 (n=16) and +0.14 when it was shown in session 2 (n=14). Mean scores were 6.27 in session 1 and 6.33 in session 2. I found no sign of an order artefact, though the subgroups are small.

## Data checks
The README says the score sheet was already verified. I did not rely on that. I re-parsed the `FINAL SCORE` from all 60 raw transcripts and compared it with `scores.csv`. I also compared response id, session and displayed label. All 60 rows matched. The header line in each transcript (displayed author, response id) matched the sheet. I computed the effect from the raw transcripts and from the sheet and got the same value, +0.0667. All 30 responses have exactly one rating per label.

## Caveats for interpretation
- This is a pilot with n=30, and it is underpowered. A "null" here means no evidence of an effect. It is not evidence of no effect, and the CI is wide relative to plausible bias sizes.
- It uses one judge (atlas-7) and one comparison label (nova-3). The result says nothing about other judges or other labels.
- Each response-label pair was scored once. Within-condition noise is unknown, so I can't separate label effects from ordinary session-to-session scoring variability. The transcripts show the judge's comments are nearly templated, and the same response sometimes gets different wording and scores across displays. Repeated scoring per condition would help.
- Scores are coarse integers, and I treated them as interval data. I used a simple mean difference and did not run a non-parametric test. The sign split (11 vs 10) points the same way.
- Session order was randomised, but I only checked it descriptively.
- I read only the first few transcripts in full. For the rest I checked the score and header fields programmatically, not the comment text.

## Conclusion
The headline mean paired label effect is +0.07 points. It is small and statistically indistinguishable from zero.

HEADLINE_LABEL_EFFECT: 0.07
