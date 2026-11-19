# Symmetric scoring audit (Nov 17–18, 2026)

Third scoring of the same frozen Cross Pressure generations. No model was re-queried.

**Why:** the October audit (`../scoring_audit_oct17/`) re-read only stored yields and treated unretracted "A" and "B" openers differently. This audit applies one rule, locked before reading, to every interpretation-dependent row.

## Reproduce
Run from this folder. `CPR` is the path to `Cross_Pressure_Research` (here, `..`). Needs Python 3 with pandas, numpy and matplotlib; versions used are in `ENVIRONMENT.txt`. The first two commands write into `out/`; run them on a copy if you want to diff against the committed files.
```
python3 scripts/second_reader_repro.py .. out
python3 scripts/analyze_final.py .. . out reader3 FINAL
python3 scripts/check_explicit_commitment.py .. out/final_labels_unblinded_FINAL.csv
python3 scripts/make_tables.py . .. ../paper/v9_generated.tex
python3 scripts/make_fig1.py out/final_results_FINAL.json ../paper/fig1_interaction_by_scoring.pdf
python3 scripts/build_v9.py ../archive/v8_review_oct20/cross_pressure_v8_review.tex ../archive/v9_review_nov18/cross_pressure_v9_review.tex
python3 scripts/build_v10.py ../archive/v9_review_nov18/cross_pressure_v9_review.tex ../paper/cross_pressure_v10.tex final
```
`analyze_final.py` verifies the frozen hashes first and refuses to run if any label file or the rule differs, and asserts that every earlier frozen ledger is reproduced unchanged. `analyze.py` is the two-reader analysis exactly as hardened; `analyze_v1_as_run.py` is the script as first run. The paper is built in two steps because v10 reuses v9's reviewed paragraphs by line range.

## Layout
- `RULES_LOCKED.md` — the rule (sha256 in `RULES_LOCKED.timestamp`).
- `out/reader{1,2}/chunk*/data/` — blinded sheets as Readers 1–2 saw them (Reader 3 received the same sheets via a packet folder). `out/reader{1,2,3}/chunk*/work/labels.csv` — labels, unedited.
- `out/second_reader_map_by_text.csv` — needed by `analyze.py` and `analyze_v1_as_run.py`; same mapping as `out/second_reader_id_map.csv`.
- `ENVIRONMENT.txt` — Python, pandas, numpy and TeX versions used.
- `scripts/finalize.sh` — historical record of the Reader 3 run; not runnable elsewhere.
- `out/LABELS_FROZEN*.sha256` — freeze manifests.
- `out/PRIVATE_KEY.csv` — opaque ID → run ID and stratum.
- `out/*results*.json`, `out/*ledgers*.csv`, `out/*labels_unblinded*.csv` — outputs.
- `reader3_packet_v2/` — third-reader packet without the gold-answer line. `reader3_packet_v1_gold_line/` — the earlier packet, which includes it. Which one Reader 3 received is not recorded.
- `DECISION_LOG.md`, `PROVENANCE_AND_CONFLICTS.md`.

Readers: 1 = Claude Opus, 2 = Claude Sonnet, 3 = see `out/LABELS_FROZEN_reader3.sha256`. Each is reported separately; there is no majority vote.

## Archival statements that the record later corrected
Three packaged files contain sentences that were true as intended but not as executed, and are kept unedited: `RULES_LOCKED.md` ("Readers are not told this"), `reader3_packet_v2/HOW_TO_RUN.md` ("Reader 3 is therefore the only reader not shown the gold answer"), and an early decision-log line on reader blinding. The corrections are in `DECISION_LOG.md` (entries dated 2026-11-18) and `PROVENANCE_AND_CONFLICTS.md`. Readers 1–2 saw the gold answer; Reader 3's packet is not recorded.
