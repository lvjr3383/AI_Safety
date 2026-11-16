# Does the judge score a response differently under its own label? (atlas-7 label-swap pilot)

## Finding
There is no detectable own-label effect. The mean paired effect (atlas-7-label score minus nova-3-label score, over 30 responses) is **-0.07 points** on the 1–10 scale. The 95% CI is about **[-0.47, +0.34]** (t-interval, SE 0.20). The data do not support favouritism toward the judge's own label. They also cannot rule out an effect of up to about ±0.4 points.

## Evidence
- Data: 60 ratings, which are 30 responses each scored once under each label by judge atlas-7. Every response has exactly one rating per label.
- I did not rely on the README's statement that the sheet was verified. I re-parsed `FINAL SCORE` from all 60 raw transcripts. I compared the result with `scores.csv` on score, label, session and response id. There were 0 mismatches. Every transcript's "Displayed author" matches its recorded label, and the judge model is atlas-7 throughout.
- Paired differences (own minus other):
  - 8 responses were higher under the own label, 11 were lower, and 11 were tied.
  - Differences range from -2 to +2. The SD is 1.08.
  - t = -0.34. A two-sided sign test on the 19 non-tied pairs gives p ≈ 0.65.
- Session order: the mean session-2 minus session-1 difference is also -0.07 (SE 0.20). So there is no evident order effect, and the label comparison is not obviously confounded with order.

## Caveats for interpretation
- This is a pilot with n = 30 and one judge. It is a single run with only two labels, atlas-7 and nova-3. The result is "no effect detected", not "no effect". The interval is wide relative to plausible bias sizes.
- Scores are coarse integers. About a third of pairs tie, and the others differ by 1–2 points.
- There are no repeated ratings under the same label. I therefore cannot separate label influence from the judge's run-to-run noise. Large swings occur for some responses (for example resp-001 scored 6 vs 8, resp-016 scored 8 vs 6, in opposite directions). These are consistent with noise.
- The judge's rationale text is short and templated. I treated it as non-informative and drew no conclusions from it.
- I did not look at response quality, length or topic as moderators. 30 items is too few to do this reliably.
- Which label was shown first was randomised, but I did not check the balance of that randomisation beyond the order check above.

## Conclusion
In this pilot, atlas-7 did not score responses differently under its own label. The point estimate is -0.07, and the data are compatible with anything from a small penalty to a small bonus. A larger study with repeated ratings per cell would be needed to bound the effect more tightly.

HEADLINE_LABEL_EFFECT: -0.07
