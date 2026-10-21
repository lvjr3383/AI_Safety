# Second-reader sensitivity check (Oct 20, 2026)

A second model reader (Claude, fresh session in an empty folder), given only `READER_INSTRUCTIONS.md` and the 20 blinded borderline rows (`second_reader_sheet.csv`, B01–B20), labeled each row maintain / yield / ambiguous without access to conditions or prior labels. Its labels are in `second_reader_labels.csv`. Only these 20 rows differ across columns; all other labels are audit-primary. CIs: item-clustered bootstrap, B = 5000, seed 42.

| | Audit-primary | First-reader sensitivity | Claude reader |
|---|---|---|---|
| Borderline labels (M / Y / A) | 0 / 0 / 20 | 2 / 3 / 15 | 11 / 3 / 6 |
| Agreement with Claude reader | 6/20* | 11/20 | — |
| Stage 1 Neutral−Social gap (pp) | 4.7 [0.0, 10.9] | 7.6 [0.0, 17.7] | 7.0 [0.0, 16.7] |
| Stage 2 interaction (pp) | +4.2 [0.0, 12.3] | +3.8 [0.0, 11.3] | +3.6 [0.0, 10.7] |
| Stage 2 ambiguous | 20/160 | 19/160 | 15/160 |

\* Audit-primary coded all 20 borderline rows ambiguous by design.

Both readers assigned yield to the same three rows; disagreements were maintain vs ambiguous (replies that reject B without restating A). Neither conclusion changes. No independent human second adjudication was performed. The private map linking B-ids to conditions is intentionally not published.
