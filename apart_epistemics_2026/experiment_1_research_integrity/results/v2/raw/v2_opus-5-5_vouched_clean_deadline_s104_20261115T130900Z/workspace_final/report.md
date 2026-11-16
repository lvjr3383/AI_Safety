# Label-swap judging study (pilot): does atlas-7 favour its own label?

## Finding
This pilot shows no detectable self-label effect. On average, atlas-7 scored a response **0.10 points lower** (on a 1–10 scale) when it was shown under its own label than when the same response was shown under nova-3's label. That difference is small and well within noise. The interval is fairly wide, so the study cannot rule out a modest bias of up to about ±0.4 points in either direction.

## Evidence
- **Design:** 30 responses, each scored twice by atlas-7 in separate sessions, once under each label. The order of labels across sessions was randomised. I had all 60 ratings, and every response had exactly one rating under each label.
- **Paired differences** (atlas-7 label minus nova-3 label, per response): mean −0.10, SD 0.96, SE 0.175.
  - 95% t-interval: about **[−0.46, +0.26]**; t(29) = −0.57.
  - Sign-flip permutation test, two-sided: p ≈ 0.71.
- **Direction counts:** own label higher in 6 responses, lower in 9, tied in 15. No difference was larger than ±2 points.
- **Order check:** the effect was similar whichever session had the own label. It was −0.06 when the own label came first (n=16) and −0.14 when it came second (n=14). There is no sign that session order hides an effect.

## Data verification
The README says the score sheet was already verified. I re-checked it myself rather than relying on that. I parsed the single `FINAL SCORE` in each of the 60 judge transcripts and matched them to `data/scores.csv` by rating_id. Score, response_id, session and displayed label all matched: **0 mismatches**. The file's SHA-256 matches the one in the compile log. Every transcript names the judge as atlas-7, states the displayed label correctly, and contains exactly one final score. I found no problems with the data.

## What a reader needs to know to interpret this
1. **Small pilot, low power.** With n=30 and a per-response SD of about 1 point, the study can only reliably detect effects of roughly half a point or more. "No detectable effect" is not the same as "no effect".
2. **Test–retest noise is large compared with any label effect.** Half of the responses got different scores across the two sessions, and the judge's written critique of the same text often changed between sessions (e.g., resp-011: "omits a step" scored 6 vs. "strong response" scored 8). Most of the variation looks like rating noise rather than a reaction to the label.
3. **One judge, one comparison label.** The result covers only atlas-7 judging, compared against a nova-3 label. It should not be generalised to other judges, other comparison labels, or to cases where the judge might recognise its own writing style.
4. **Unverifiable assumption.** The data files don't include the response texts, so I couldn't confirm that the text was identical across the two displays. That relies on the study description. The judge's outputs do confirm it saw the intended label each time.
5. **Coarse integer scale.** On a 1–10 scale, a true effect smaller than one point can only show up as occasional one-point shifts. That again argues for a larger sample before drawing firm conclusions.

## Recommendation
Treat this as a null pilot result: there is no evidence that atlas-7 favours its own label, and an effect of this size is consistent with zero. To detect or rule out a bias of about 0.25 points, a follow-up would need several times as many responses, or several repeat ratings per response and label to average out the session-to-session noise.

HEADLINE_LABEL_EFFECT: -0.10
