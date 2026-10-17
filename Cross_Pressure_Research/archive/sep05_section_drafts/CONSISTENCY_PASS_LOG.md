# Consistency pass log (2026-09-05)

## Fixes applied
- Locked bibliography: `CROSS_PRESSURE_REFERENCES.bib` (7 entries; cite keys frozen).
- Stage 2 sampling wording aligned to frozen config + raw data: **2 samples · 160 generations** (sample_idx 0/1; 40 rows/cell). Removed inconsistent “4 samples · 160” phrasing. Stage 1 remains **4 samples** / 480 grid.
- Intro + Conclusion tightened to frozen claim walls and headline numbers only.
- Appendix populated by copying exact strings from `pilot02_frozen_config.json` and Stage 1 notebook cell 7 (incl. Training wrapper).

## Verified against frozen artifacts
- Canonical 2×2: 92.5 / 79.5 / 97.5 / 67.6; drops 13.0 / 29.9; interaction 16.9; ambiguity 2.5%.
- Bootstrap CI interaction [5.1, 30.8]; Drop OFF [2.6, 26.2]; Drop ON [11.8, 49.1].
- Stage 1 Llama: 96.2 / 76.9 / 93.7; Neutral−Social 19.2; GPT-OSS usable 94.2%.
- Claim walls preserved (no mechanism, no bank-wide, no cross-model, H08/H19 retained).

## Not reopened
2×2, H19/H08, model scope, experiments, sensitivity checks.
