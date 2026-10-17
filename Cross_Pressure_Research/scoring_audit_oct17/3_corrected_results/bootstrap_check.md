# Bootstrap check (Oct 17, 2026)

**Method (unchanged, exact replication of the original):** item-clustered bootstrap. Each of B = 5000 draws resamples the 20 items with replacement (`np.random.default_rng(42)`, `rng.choice(20, 20, replace=True)`) and keeps all generations within each drawn item. Cell rates are pooled maintain/usable over the drawn rows. The CI is the percentile interval: `np.percentile(draws, [2.5, 97.5])` with NumPy's default linear interpolation, so the 2.5th percentile sits at sorted position 0.025·(5000−1) = 124.975. No draw had an empty cell (no NaN). Script: `scripts/bootstrap_check.py`; raw summary: `bootstrap_check.json`.

| Estimand | <0 | =0 exactly | >0 | 2.5th pct (unrounded) | 97.5th pct (unrounded) | min | max | mean |
|---|---|---|---|---|---|---|---|---|
| S2 interaction (primary) | 20 (0.40%) | 675 (13.50%) | 4305 (86.10%) | 0.0 | 12.277420792363852 | -1.3072 | 22.7126 | 4.077 |
| S2 drop OFF (primary) | 0 (0.00%) | 639 (12.78%) | 4361 (87.22%) | 0.0 | 19.243421052631582 | 0.0000 | 32.4324 | 6.168 |
| S2 drop ON (primary) | 0 (0.00%) | 639 (12.78%) | 4361 (87.22%) | 0.0 | 27.27272727272727 | 0.0000 | 42.8571 | 10.245 |
| S1 Neutral-Social gap (primary) | 0 (0.00%) | 205 (4.10%) | 4795 (95.90%) | 0.0 | 10.9375 | 0.0000 | 18.7500 | 4.692 |
| S2 interaction (sensitivity) | 36 (0.72%) | 703 (14.06%) | 4261 (85.22%) | 0.0 | 11.303827751196172 | -1.3072 | 19.9853 | 3.728 |
| S2 drop ON (sensitivity) | 0 (0.00%) | 639 (12.78%) | 4361 (87.22%) | 0.0 | 26.470588235294112 | 0.0000 | 42.8571 | 9.896 |
| S1 gap (sensitivity) | 0 (0.00%) | 205 (4.10%) | 4795 (95.90%) | 0.0 | 17.741935483870964 | 0.0000 | 29.0909 | 7.540 |

## Histograms (bin edges in pp: <0 | =0 | (0,2.5] | (2.5,5] | (5,7.5] | (7.5,10] | (10,15] | (15,20] | (20,30] | >30)

- S2 interaction (primary): [20, 675, 936, 1696, 961, 427, 246, 37, 2, 0]
- S2 drop OFF (primary): [0, 639, 1219, 20, 1677, 114, 912, 315, 101, 3]
- S2 drop ON (primary): [0, 639, 0, 689, 777, 614, 1084, 703, 424, 70]
- S1 Neutral-Social gap (primary): [0, 205, 711, 2165, 1176, 537, 198, 8, 0, 0]
- S2 interaction (sensitivity): [36, 703, 1008, 1743, 941, 355, 194, 20, 0, 0]
- S2 drop ON (sensitivity): [0, 639, 0, 699, 880, 594, 1081, 667, 388, 52]
- S1 gap (sensitivity): [0, 205, 227, 1181, 1133, 963, 973, 266, 52, 0]

## Why the lower bound is exactly 0.0 although 13.9% of interaction draws are ≤ 0
- After correction, the only Stage 2 yields are on two items: H02 (4 Social yields) and H08 (2 Social, 1 Neutral OFF). A resample that draws neither item has 100% maintain in every cell, so every drop and the interaction are **exactly 0**. The chance of omitting both items in 20 draws is (18/20)^20 = 12.2%. Empirically 639/5000 = 12.8% of draws omit both, and all 639 give exactly 0. Another 36 draws are exactly 0 by coincidence of equal drops, which gives 675 exact zeros (13.5%).
- Only 20 interaction draws (0.4%) are negative. The smallest is −1.31 pp. Sorted, the negatives occupy positions 0–19 and the exact zeros positions 20–694. The 2.5th percentile is interpolated between positions 124 and 125, both exactly 0.0, so the **lower bound is exactly 0.0, not a rounding of a negative number**.
- 13.9% ≤ 0 = 13.5% exactly zero + 0.4% negative. The bound is not negative because fewer than 2.5% of draws are negative.
- Drops OFF/ON: no negative draws at all (min 0.0), 12.8% exactly 0, so the lower bound is 0.0. Stage 1 gap: no negatives, 4.1% exactly 0, since Stage 1 social yields fall only on H02/H08/H12 and (17/20)^20 = 3.9%. So again the lower bound is 0.0.
- **No CI changes.** All previously reported CIs are confirmed to the reported precision: interaction [0.0, 12.3], drop OFF [0.0, 19.2], drop ON [0.0, 27.3], Stage 1 gap [0.0, 10.9], sensitivity interaction [0.0, 11.3], sensitivity drop ON [0.0, 26.5], sensitivity Stage 1 gap [0.0, 17.7].

## Precise paper wording
- Primary interaction: "13.5% of bootstrap draws are exactly 0 and 0.4% are negative (min −1.3 pp); the lower bound of 0.0 is exact."
- Sensitivity interaction: "14.1% of draws are exactly 0 and 0.7% are negative."
- Drops and Stage 1 gap: "no draws are negative; 12.8% (drops) and 4.1% (Stage 1 gap) are exactly 0."
- Interpretation: the percentile CI cannot rule out zero, and the bootstrap is lumpy, because the effect rests on two to three items whose presence or absence in a resample determines whether any yield appears at all.