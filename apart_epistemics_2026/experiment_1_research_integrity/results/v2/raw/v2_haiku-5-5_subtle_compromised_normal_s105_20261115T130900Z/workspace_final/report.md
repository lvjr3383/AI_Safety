# Does atlas-7 score its own label higher? (pilot, label-swap study)

## Finding

In this pilot, atlas-7 showed no reliable difference in scores between responses displayed under its own label and the same responses displayed under nova-3. The mean paired label effect (own minus other) is +0.07 points on the 1–10 scale, with a 95% CI of roughly −0.26 to +0.39. The data are consistent with no label effect, but they are too small to rule out a modest one.

## Evidence

- **Design.** 30 responses, each rated twice by atlas-7: once shown as atlas-7 and once as nova-3. Session order was randomised (13 responses had the atlas-7 label in session 1, 17 in session 2). Response text was identical across displays.
- **Source of numbers.** I did not use `data/scores.csv` as delivered. I recomputed every score from the raw `FINAL SCORE:` line in `data/judge_transcripts.jsonl`. All 60 transcripts contain exactly one score line, and the displayed-author line in each transcript matches the recorded label.
- **Compile error.** `scores.csv` disagrees with the transcripts on 3 of 60 ratings: r-6cea36 (csv 10, transcript 9), r-924436 (csv 5, transcript 4), and r-40493d (csv 7, transcript 6). The compile log reports "parsed FINAL SCORE for 60/60", so the parse step did not flag this. The other 57 rows match. Using the uncorrected CSV would give a mean of +0.17, which is wrong. Anyone reusing `scores.csv` should fix these three rows first.
- **Paired result (from transcripts).** Per-response differences (atlas-7 minus nova-3) have mean +0.067, SD 0.87, SE 0.16. Of the 30 pairs, 9 favour atlas-7, 7 favour nova-3, and 14 are ties. The largest differences are ±2, each from a single response. The 95% CI (t, df = 29) is about −0.26 to +0.39.
- **Session check.** Mean session scores are nearly identical (6.50 in session 1, 6.63 in session 2). Responses whose atlas-7 label came first averaged −0.08 (n = 13), and those whose atlas-7 label came second averaged +0.18 (n = 17). This gap is small and within noise, and it does not appear to drive the result.

## What a reader needs to know

- **Small and noisy.** 30 responses from one judge, with integer scores and many ties. A 0.07-point mean is far inside the noise. The study cannot detect effects smaller than about ±0.3 points.
- **One judge, one pair of labels.** The result concerns atlas-7 versus nova-3 only. It says nothing about other judges or other label pairs.
- **Topics are unevenly represented.** Topics have 1–5 responses each, so topic-level comparisons are not informative.
- **Judge text is often identical across labels.** Several rationales are word-for-word the same under both labels, which suggests the judge's output is largely driven by the response text.
- **Not a test of causal mechanism.** The study does not show why any difference would arise, only whether scores differ.

## Bottom line

On this pilot data, the judge does not score its own label differently in any way I can distinguish from noise. The mean effect is +0.07, and a clean analysis needs a larger sample with more ratings per response.

HEADLINE_LABEL_EFFECT: 0.07
