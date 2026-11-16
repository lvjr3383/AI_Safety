# Experiment 2: Does Evaluation Awareness Mask Social Sycophancy? (reproduction guide)

> This file holds the current setup and reproduction notes for the completed study. `README.md`, `requirements.txt` and `.gitignore` in this folder are part of the frozen pilot snapshot (tag `exp2-pilot-frozen-v1`, commit `f9f6b18`, checked by `verify_frozen.py`) and are intentionally left unchanged. Extra ignore rules (secrets, caches, nested `local_private/`) live in `apart_epistemics_2026/.gitignore`.

**Apart Research AI x Epistemics sprint, 13-15 November 2026** (Track 1: Model Epistemics & Decision-Making Evals).

This folder holds a completed Anthropic-only study of three Claude models (720 conversations), plus earlier exploratory work from the same sprint (an OpenRouter GPT/Gemini pilot and a v3 AI-grader reliability exercise). Those earlier arms are **not** pooled with the Anthropic results.

**Manuscript:** [`paper/manuscript.md`](paper/manuscript.md) (final author text, with figures pointing at the committed SVGs). **Submission PDF (authoritative):** [`paper/exp2_submission.pdf`](paper/exp2_submission.pdf). Official Google Doc: https://docs.google.com/document/d/1iVqX7KnkhqZdMt8XRou6V9CVPn7VkF1vqndCtH3WNRc/edit

**Prior work disclosure:** Jack's AISC research proposal was written before the sprint and is conceptual prior work only. No code, data, prompts, or results from it are reused here.

## Question

Does explicit evaluation framing change how much an honesty intervention reduces movement toward a user who pushes back without new evidence? Primary outcomes are deterministic Verdict-line movement and confidence change. See [`v2_study/PROTOCOL.md`](v2_study/PROTOCOL.md) and [`v2_study_anthropic/PROTOCOL_ADDENDUM.md`](v2_study_anthropic/PROTOCOL_ADDENDUM.md).

Two standing caveats:
1. The study tests *prompted* evaluation framing, not whether a model independently detects evaluation.
2. Movement under pressure is not the same thing as dishonesty, and it is narrower than social sycophancy in Cheng et al. (2025).
3. ELEPHANT and the Reddit posts are public and may be in training data.

## Folder structure

| Path | Contents |
|---|---|
| `paper/` | Final manuscript Markdown (`manuscript.md`) |
| `v2_study/` | Frozen v2 protocol: case selection, prompts, design, analysis code, tests, `verify_protocol.py` |
| `v2_study_anthropic/` | Anthropic-only extension (primary study): runner, analysis wrapper, ledger, results, figures, `verify_addendum.py` |
| `v2_study_anthropic/results/analysis/` | Primary analysis tables, `RESULTS_TABLES.md`, and SVG figures |
| `validation_v3/` | Exploratory AI-grader reliability (Claude Sonnet 4.6 vs Qwen3.8 Max); not used for H1-H3 |
| `configs/`, `src/`, `results/` | Earlier OpenRouter pilot (separate exploratory arm) |
| `protocol.md` | Original sprint protocol note (superseded for the main study by `v2_study/PROTOCOL.md`) |
| `CHANGELOG.md` | Run log, costs, and commit history notes |

## Reproduce (Anthropic primary study)

From the repository root:

```bash
cd apart_epistemics_2026/experiment_2_social_pressure
python -m venv .venv && . .venv/bin/activate && pip install -r requirements-analysis.txt

# Secrets: set in the environment only. Never commit a key, .env, or credential file.
export ANTHROPIC_API_KEY=...     # required for the Anthropic runner
# export OPENROUTER_API_KEY=...  # only if you rerun the earlier GPT/Gemini pilot

# Tests and frozen-protocol checks (no API key needed)
pytest -q tests v2_study/tests v2_study_anthropic/tests
python v2_study/verify_protocol.py
python v2_study_anthropic/verify_addendum.py
python verify_frozen.py   # original OpenRouter pilot snapshot (tag exp2-pilot-frozen-v1); all 38 files should match

# Case selection already ran; IDs and hashes are in v2_study/config/manifest_v2.json.
# To regenerate locally (requires the ELEPHANT files, which are not in this repo):
#   python v2_study/src/select_cases_v2.py

# Anthropic run (resumable). The runner refuses to start without --authorized, --cap,
# and passing protocol/addendum checks. It reads ANTHROPIC_API_KEY from the environment only.
python v2_study_anthropic/src/run_anthropic.py --dry-run --cap 50
python v2_study_anthropic/src/run_anthropic.py --smoke --smoke-cap 1.0
python v2_study_anthropic/src/run_anthropic.py --authorized --cap 50
python v2_study_anthropic/src/run_anthropic.py --authorized --cap 50 --retry-failed

# Analysis and figures (reads the committed logs; no API key)
python v2_study_anthropic/src/analyze_anthropic.py
python v2_study_anthropic/src/analyze_anthropic.py --exclude-ceiling
python v2_study_anthropic/src/report_anthropic.py
```

The full 720-conversation run is already complete in this branch. Re-running it will make new paid API calls.

## Data and redistribution

- Cases come from ELEPHANT AITA-YTA (Cheng et al., 2025). The ELEPHANT GitHub repository is CC0 1.0; the OSF node for the full datasets exposes **no licence field**, and the posts are Reddit users' content, so **raw post text is not committed**.
- The public repo stores row IDs and SHA-256 hashes in `v2_study/config/manifest_v2.json`.
- Committed conversation logs replace the post with a row ID and hash. Full transcripts with post text stay in gitignored `results/local_private/` folders.
- `turns.jsonl` (model replies, posts redacted) is kept on the run machine; the committed turn log is `v2_study_anthropic/results/raw/turns_metadata.jsonl` (parsed lines, tokens, costs; no post text or model replies). See `v2_study_anthropic/results/raw/README.md`.

## Costs (Anthropic primary run)

List-price usage returned by the API, under a $50 cap:

- Haiku 4.5: $1.918986
- Sonnet 4.6: $5.254320
- Opus 4.7: $12.384225
- **Total: $19.557531**

Thirty-two requests were abandoned after a 240-second deadline, so the ledger is a lower bound if those calls were billed without returned usage. This arm had no OpenRouter spend. The earlier GPT/Gemini pilot and the v3 grader exercise used OpenRouter and have separate ledgers.

## Figures

SVG figures (committed):

- [`v2_study_anthropic/results/analysis/fig1_moved_toward_push_by_condition.svg`](v2_study_anthropic/results/analysis/fig1_moved_toward_push_by_condition.svg) — manuscript Figure 1
- [`v2_study_anthropic/results/analysis/fig3_contrasts_primary.svg`](v2_study_anthropic/results/analysis/fig3_contrasts_primary.svg) — manuscript Figure 2
- [`v2_study_anthropic/results/analysis/fig5_initial_verdicts.svg`](v2_study_anthropic/results/analysis/fig5_initial_verdicts.svg) — manuscript Figure 3
- [`v2_study_anthropic/results/analysis/fig6_blame_trajectory.svg`](v2_study_anthropic/results/analysis/fig6_blame_trajectory.svg) — manuscript Figure 4

PNG copies of the same figures are on the run machine and at https://huggingface.co/datasets/lvjr3383/apart-epistemics-exp2-figures (used only to insert images into the Google Doc). The GitHub connector cannot upload binary PNGs.

## Earlier arms (exploratory, not pooled)

The original OpenRouter pilot (`src/run_experiment.py`, `configs/`, `results/`) and the v3 grader-reliability work (`validation_v3/`) remain in this folder for provenance. To rerun the pilot, set `OPENROUTER_API_KEY` and follow the commands in the older `src/` scripts; do not mix those conversations into the Anthropic analysis.
