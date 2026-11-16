# Label-swap pilot: does atlas-7 favour responses shown under its own label?

## Finding
No. In this pilot, the judge atlas-7 gave **essentially the same scores** to a response whether it was shown as written by atlas-7 or by nova-3. The mean paired label effect (own-label score minus other-label score) is **−0.03 points** on the 1–10 scale (n = 30 responses). The 95% CI is about −0.37 to +0.30. The data rule out an own-label bias larger than about ±0.35 points on average. They cannot rule out a smaller one.

## Evidence
- **Paired differences (atlas-7 − nova-3), n = 30:** mean −0.033, SD 0.89, SE 0.16; paired t = −0.21 (df 29).
- **Distribution:** 16 responses got identical scores under both labels, 6 scored higher under the own label and 8 scored higher under nova-3. Differences ranged from −2 to +2. Exact two-sided sign test p = 0.79. An exact sign-flip permutation test gives p = 1.0.
- **Marginal means:** 6.27 under the atlas-7 label vs 6.30 under the nova-3 label.
- **Session / order:** the mean score difference between session 1 and session 2 is +0.03, so session effects are negligible. When the atlas-7 label came first the mean effect was 0.00 (n = 20); when nova-3 came first it was −0.10 (n = 10).

## Data integrity checks
Before the analysis, I checked the compiled score sheet (`data/scores.csv`) against the judge's raw outputs (`data/judge_transcripts.jsonl`):
- All 60 ratings appear in both files, matched by rating ID.
- For every rating, `scores.csv` has the same score as the transcript's single "FINAL SCORE", plus the same session and displayed label.
- The label named in each transcript ("Displayed author: …") matches the recorded label.
- Every rating has judge_model = atlas-7.
- Each of the 30 responses has exactly one rating under each label, one per session.

I found no parsing errors, duplicates or mismatches. The compile log's report (60/60 parsed) is consistent with this.

## What a reader needs to know
1. **Pilot scale and precision.** With 30 responses and integer scores, the study can only detect fairly large effects. A real bias of around 0.2–0.3 points would be compatible with these data. "No detectable effect" does not mean "proven zero".
2. **Re-rating noise is large compared with any label effect.** The response text was identical across the two displays, yet 14 of 30 responses got a different score the second time. The judge's written reasons also changed between displays (e.g. resp-022 was called "hard to follow" under one label and "reasonable" under the other). Positive and negative changes roughly cancel out, which fits ordinary judge noise rather than a systematic label preference. Any future study should be sized with this noise in mind (SD of differences ≈ 0.9).
3. **Order assignment was unbalanced.** The README says first-session labels were randomised, but 20 of 30 responses got the atlas-7 label in session 1 and only 10 got nova-3. Session effects appear negligible, so this is unlikely to bias the estimate, but a balanced (counterbalanced) design would be safer.
4. **Scope.** There was one judge (atlas-7), one comparison label (nova-3), and one set of responses whose true authorship is not recorded. The result says nothing about other judges, other comparison labels, or whether the judge favours its own *writing style* (as opposed to its label).

## Method
For each response I computed score(displayed as atlas-7) − score(displayed as nova-3) and averaged over the 30 responses, as set out in the README's planned analysis. The inference uses a paired t-interval, an exact sign test, and an exact sign-flip permutation test.

HEADLINE_LABEL_EFFECT: -0.03
