# Experiment 2 changelog (Apart AI x Epistemics sprint, Nov 13-15 2026)

## [exp2-pilot-frozen-v1] Frozen pilot checkpoint, 2026-11-13
- Frozen at commit `f9f6b18ff85218130a8361e448e756dd17a30d6c` (branch `apart-epistemics-exp2-pilot`).
- Remote ref: branch `frozen/exp2-pilot-frozen-v1` at the same commit, created via the GitHub connector.
- An annotated tag `exp2-pilot-frozen-v1` was created locally. The connector has no tag tool, so Jack still needs to push it: `git tag -a exp2-pilot-frozen-v1 f9f6b18ff85218130a8361e448e756dd17a30d6c -m "Exp2 pilot frozen" && git push origin exp2-pilot-frozen-v1`.
- The 38 pilot files (prompts, configs, raw JSONL, grader outputs, cost and key logs, summaries, report, src, tests) are listed with SHA-256 in `FROZEN_CHECKSUMS.sha256`. `python verify_frozen.py` exits non-zero if any of them changes.
- **Rule:** frozen files are never edited. Later work goes in new files, in separate commits.

## Validity review (no API calls, $0)
- `validity_review/`: blinded human review pack for the 29 sampled conversations. It contains no model, condition or grader information and no AI-suggested labels.
  - `REVIEW_INSTRUCTIONS.md`, `blind_review_sheet.md` (post text omitted), `review_form.csv`.
  - `build_review_pack.py` deterministically rebuilds the pack, plus a local, gitignored copy with posts.
  - `compare_review.py`: after Jack's review, computes kappa and agreement against the frozen Claude grades and code metrics. Grader-structure checks appear only in `post_review/`.
  - `tests/test_compare_review.py`.
- `validity_review/analyses/`: floor-effect (`floor_effect.md`) and rebuttal-direction (`rebuttal_direction.md`) diagnostics computed from frozen data only (`floor_and_direction.py`, `floor_and_direction_output.txt`).

## Proposals (not applied to the pilot)
- `configs/v2/rubric_v2_PROPOSAL.md`, `grader_prompt_v2_PROPOSAL.txt`, `grader_schema_v2_PROPOSAL.json`: rubric v2 draft. To be finalised only after the human review.
- `proposals/stronger_pressure_PROPOSAL.md`: sketch only. Not approved and not run.

## Grading provider option (no API calls, $0)
- `src/grading_providers.py` and `configs/v2/grading_providers.json`: `openrouter` (default, historical) or `anthropic` direct (`ANTHROPIC_API_KEY`), with the same Sonnet 4.6 model, prompt and settings, and separate ledgers under `results_v2/ledgers/`.
- `tests/test_grading_providers.py` uses mocked HTTP only.
- The Anthropic model ID `claude-sonnet-4-6` and the $3/$15 list price are unverified on this account. Check them with the free GET /v1/models once a key is supplied (see `configs/v2/README.md`).

## Spend
- Phase 3 work made no inference or grading calls. OpenRouter /key usage before and after is recorded in the PR description.

## Validation phase v3: fully automated, AI graders only (Nov 14)
Jack asked for full automation: no human review, no manual annotation, no human-validation claims. Every change below is in new files; the frozen pilot files are unchanged (`python verify_frozen.py`).
- `configs/v3/`: rubric v3 (5 allegation codes incl. `conditional_hypothetical`, fault-only judgment change, machine-checked verbatim quotes), blinded grader prompt (no model, condition, framing, Reddit verdict), schema, grader config, `CHANGES_v2_to_v3.md`. The reliability rule (Krippendorff alpha >= 0.6 per metric across AI graders, else exploratory; no majority vote) was committed before any v3 grading.
- `src/deterministic_checks.py` (+ tests): Verdict-line change and step size, confidence shift, verbatim-quote check. Output `results_v3/deterministic_checks.csv`.
- `validation_v3/`: blinded 40-conversation input, blinding key, manifest hashes, Muse prompt and CSV template; post text only in gitignored `validation_v3/local_private/`.
- `src/grade_v3.py` (+ mocked tests): Anthropic direct and OpenRouter graders, free model checks, cost estimate, separate ledgers and caps (`results_v3/ledgers/anthropic.jsonl` cap $5; `results_v3/ledgers/openrouter.jsonl` cap $2.50).
- `validation_v3/agreement_v3.py` (+ tests): per-metric raw %, Cohen kappa, Fleiss kappa, Krippendorff alpha, confusion tables, disagreement list, deterministic comparison, cross-rubric context, and the earlier Muse-vs-Claude-v0.2 comparison relabelled as AI judge vs AI grader (`validation_v3/historical_muse_v2form_vs_claude_v02/`). The uncommitted draft whose headings said "human" was moved to gitignored `validity_review/local_private/superseded/` and is not used.
- Third grader run: `qwen/qwen3.8-max-0902` via OpenRouter, 40/40 valid, **$0.46395** (ledger; equals /key usage delta 35.895609 -> 36.359559).
- Claude v3 run: not done, no `ANTHROPIC_API_KEY` available during this session ($0 Anthropic spend). Muse v3: pending.
- Claude v3 run (Nov 14, about 6:20 AM CT): `claude-sonnet-4-6` verified via free GET /v1/models; 40/40 valid (41 calls, 1 regrade for a non-verbatim quote); **$0.454866** Anthropic (computed from response token usage at list price; separate ledger `results_v3/ledgers/anthropic.jsonl`). OpenRouter unchanged at $0.46395.
- Agreement (Claude v3 vs Qwen v3, AI graders only): verdict alpha 1.0 (pass); judgment change t3 alpha 0.48 (exploratory); allegation t2 alpha 0.141, binary 0.253 (exploratory). No majority vote. Rubric v3 is not revised after seeing these results; any v4 would be a new, documented version regraded from scratch.

## Experiment 2 v2: preparation and frozen protocol (Nov 14, no main-run inference)
Everything is in the new folder `v2_study/`. Pilot and v3 files are unchanged (`python verify_frozen.py`).
- `v2_study/PROTOCOL.md`: hypotheses H1-H3, deterministic primary outcomes (Verdict-line movement, confidence change), secondary Blame 0-10, case-bootstrap analysis plan, missing-data and ceiling rules, and the caveat that movement is not dishonesty. Frozen via `PROTOCOL_CHECKSUMS.sha256` + `verify_protocol.py` (15 files).
- `src/select_cases_v2.py` -> `config/manifest_v2.json`: 30 new cases (10 per category) chosen by deterministic rules; only IDs and hashes are committed.
- `config/prompts_v2.json`, `config/study.json`: pilot system texts verbatim, added Blame line, fixed push direction toward "not in the wrong", targets/settings identical to pilot, prices re-verified via free /models.
- `src/run_v2.py`: 480 conversations; resumable; BudgetGuard ledger; refuses without `--authorized`, `--cap`, passing protocol check, and projected cost <= min(cap - spent, OpenRouter limit_remaining).
- `src/estimate_v2.py` -> `results/estimate_v2.json` (from actual pilot spend, +25% margin); `src/analyze_v2.py`.
- Tests: `v2_study/tests/` (21 pass: prompt isolation, dataset integrity, scoring, int32 seeds/randomization, cost cap, resumability, freeze).
- Smoke test (1 conversation per model, case 3861, condition A, rep 0): **$0.0794** OpenRouter (ledger `v2_study/results/smoke/ledger_targets.jsonl`; equals /key usage delta). All Verdict/Blame/Confidence lines parsed.
- Main run NOT started. As of 2026-11-14 6:57 AM CT, OpenRouter limit_remaining was $3.56 and the run needs $23.47 with margin, so the runner refuses until Jack adds funds or raises the key limit and authorizes with `--authorized --cap USD`.
- Report template (not yet used): the official sprint template linked from the Guidelines tab, https://docs.google.com/document/d/17b3JWki-ZkaqdmqGI5d0gof-HwlGuWU9Mc1_klNZXKs/copy?usp=sharing
