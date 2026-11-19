# Provenance and conflict notes

## Provenance
- Source of record: this repository at commit e0934c4 (2026-10-20) plus this folder.
- `pilot02_final_scored.csv` was committed 2026-09-06 and is unchanged since.
- `pilot02_raw_generations.jsonl`, `pilot02_auto_scored.csv` and `pilot01_final_scored.csv` were first committed 2026-10-17. Contemporaneous Drive copies match in byte size and timestamp (550,952 bytes modified 2026-09-05 17:46:06 UTC; 495,202 bytes created 2026-08-22). That is corroboration, not a hash match.
- Stage 1 raw generations and all Pilot 00 (discovery) artifacts are not in Git.
- Stage 2 response text is byte-identical across raw, auto-scored and final-scored files (160/160) and across every audit sheet. No generation was rerun.
- Not recoverable from the record: who performed the Aug/Sep manual adjudications; whether the Stage 1 review was blinded; which file the Stage 2 adjudicator worked from; token counts; whether a generation seed reached the API.

## Conflicts preserved (not harmonized)
- Stage 1 notebook prose says rates are on "clean auto only"; the code computes them after merging adjudicated labels, and prints a 0.0% manual-review rate beside 37 reviewed rows. Code/output is authoritative.
- Adjudication SOP says truncated → ambiguous; 4 capped Stage 2 rows were adjudicated maintain in September on a pre-cut-off correction to A. Consistent with ruling C3.
- `pilot02_manual_review.csv` contains `run_id`; the instructions say the judge must not see it; the scoring sheet omits it.
- Stage 2 readability gate (≤10%) vs 18.75% review load before adjudication: timing of evaluation unknown (C12 open).
- GPT-OSS: 14 of 240 not usable (94.2%); empty + unscorable is 13 of 480. Different definitions.
- README header date (Oct 17) vs body describing v8 (Oct 20): to be corrected on push.
- Draft versions v2–v5, v7, v8 exist; there is no v6.

## Symmetric audit: who saw what
- Readers saw: item setup, both options, the raw response, and the rule file.
- Readers 1 and 2 received the full `RULES_LOCKED.md`, whose final section states that gold is A and that B maps to yield. They were not gold-blind. Whether Reader 3's rule file included that section is not recorded.
- Readers did not see: condition, run ID, prior label, parser status, truncation flag, each other's labels.
- Reader 3 (Google Gemini, shown as "Neon Deeper Analysis") was run by the PI in a web chat after Reader 1-2 results were known. No transcript was archived. Its label files were hashed on ingestion.
- The orchestrating session (Claude) built the sheets and ran the analysis unblinded and assigned no labels.
- `out/PRIVATE_KEY.csv` maps opaque IDs to run IDs. It is published because rows are recoverable from response text anyway.
