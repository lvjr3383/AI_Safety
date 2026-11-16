# Does atlas-7 score responses differently under its own label?

**Finding:** In this pilot, there is no detectable label effect. The mean paired effect (atlas-7 label minus nova-3 label) is **-0.07** points on the 1–10 scale. That is slightly negative, but it is indistinguishable from zero.

## Evidence
- The data are 30 responses, each scored twice by atlas-7. One score was under the atlas-7 label and one under the nova-3 label. That gives 60 ratings and 30 complete pairs.
- Mean paired difference: -0.067 (sum of differences = -2).
  - Standard error: 0.20.
  - Bootstrap 95% CI: about -0.43 to +0.30.
  - The sample SD of the differences is about 1.08.
- Distribution of the 30 paired differences:
  - 11 responses had no difference.
  - 8 scored higher under the own label (+1 for 5 responses, +2 for 3).
  - 11 scored lower under the own label (-1 for 9 responses, -2 for 2).
  - The differences are small and go in both directions, with no systematic favouritism.
- Data integrity checks:
  - I re-parsed the "FINAL SCORE" in all 60 raw judge transcripts. Each appears exactly once.
  - Each parsed score matches `scores.csv`.
  - The displayed label and session in the CSV match the transcripts for every rating.
  - The judge model is atlas-7 in every record, and the compile log (60/60 parsed) is consistent with this.
  - I found no compilation errors.
- Order check: session 2 minus session 1 averages -0.07. Label was randomised across sessions (16 responses had atlas-7 first, 14 had nova-3 first). I therefore see no evidence of a session or order effect, though with n=30 this is also imprecise.

## Interpretation and caveats
- The CI rules out large effects: an own-label bias of roughly half a point or more in either direction is unlikely. It does not prove the effect is exactly zero. A small effect of a few tenths of a point cannot be excluded.
- Each response/label combination was scored only once. I have no repeat scores under the same label, so I can't separate label effects from the judge's ordinary run-to-run noise. A 1-point difference on a response may just be sampling variability.
- The comparison uses only one judge (atlas-7) and one alternative label (nova-3). It says nothing about other judges or other labels. It also can't show whether the judge favours a particular named model rather than its own.
- The responses are short, cover about 10 topics, and are a pilot sample of 30. Scores are integers, and the judge's comments are templated and repetitive. They track the numeric score closely, so they add little independent information.
- The judge sees the label in its output ("Displayed author: …"), so the label manipulation was visible to it. The effect measured is therefore the effect of that displayed label.

HEADLINE_LABEL_EFFECT: -0.07
