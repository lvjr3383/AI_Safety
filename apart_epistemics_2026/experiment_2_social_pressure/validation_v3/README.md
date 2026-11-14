# Validation phase v3: fully automated (AI graders + deterministic checks)

Sprint work, Apart AI x Epistemics, Nov 13-15 2026 (this phase: Nov 14). **No human review or manual annotation is part of this phase, and nothing here is human validation.** The frozen pilot (`exp2-pilot-frozen-v1`, commit `f9f6b18`) is untouched; `python verify_frozen.py` checks it.

## Pieces
| What | Where |
|---|---|
| Rubric v3, blinded grader prompt, schema, grader config, v2->v3 changes, reliability rule | `configs/v3/` |
| Deterministic checks (Verdict-line change, confidence shift, verbatim quotes), no API | `src/deterministic_checks.py` -> `results_v3/deterministic_checks.csv` |
| Blinded input for all 40 pilot conversations (random IDs and order) | `validation_v3/build_blind_input.py`, `blinding_key.csv`, `blind_input_manifest.json` |
| Muse paste (post text, gitignored) and committed prompt/template | `validation_v3/local_private/MUSE_INPUT_ALL_IN_ONE.md`, `muse_prompt_v3.md`, `muse_v3_output_template.csv` |
| API grading runner (separate ledgers + caps per provider) | `src/grade_v3.py` -> `results_v3/grades/`, `results_v3/ledgers/` |
| Agreement analysis (per metric, no majority vote) | `validation_v3/agreement_v3.py` -> `validation_v3/agreement/` |
| Earlier Muse (29, v2-style form) vs frozen Claude v0.2, relabelled as AI vs AI | `validation_v3/historical_muse_v2form_vs_claude_v02/` |

## Status at commit time (Nov 14, about 2:50 AM CT)
- Qwen3.8 Max (`qwen/qwen3.8-max-0902`, OpenRouter, Alibaba pinned): 40/40 valid on the first attempt; $0.46395 per ledger, equal to the OpenRouter /key usage delta.
- Claude Sonnet 4.6 via direct Anthropic API: **not run**; `ANTHROPIC_API_KEY` was not available. Model ID `claude-sonnet-4-6` still unverified on the account.
- Muse v3 (40 rows): not yet returned.
- With one v3 grader, inter-grader reliability is **not assessable**; every gated metric is reported as such in `agreement/gate.json`.

## To finish (each step is reproducible and adds files only)
1. Claude: with `ANTHROPIC_API_KEY` set in the environment, `python src/grade_v3.py --grader claude_sonnet46_anthropic --estimate` (free model-list check; aborts if the ID is not listed), then `--run` (hard cap $5, ledger `results_v3/ledgers/anthropic.jsonl`). Promotional-credit eligibility cannot be checked through the API; check the Anthropic console.
2. Muse: paste `validation_v3/local_private/MUSE_INPUT_ALL_IN_ONE.md` into Muse, save its CSV as `validation_v3/muse_v3_output.csv`.
3. `python validation_v3/agreement_v3.py --muse validation_v3/muse_v3_output.csv` (Muse optional).
