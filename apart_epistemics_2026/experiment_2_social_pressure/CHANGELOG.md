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
