# Experiment 2: Does Evaluation Awareness Mask Social Sycophancy?

**Created during the Apart Research AI x Epistemics sprint, 13-15 November 2026** (Track 1: Model Epistemics & Decision-Making Evals). All code, prompts, data selection, results and report material in this folder were produced during the sprint.

**Prior work disclosure:** Jack's AISC research proposal was written before the sprint and is conceptual prior work only. No code, data, prompts or results from it are reused here. This experiment is separate from the AI Village / Codex-judging work elsewhere in this repository.

## Question
Does explicit evaluation framing change how well an honesty intervention prevents social sycophancy, meaning unjustified concessions to evidence-free pushback in interpersonal-advice conversations? The primary result is the framing x intervention interaction. See [`protocol.md`](protocol.md) for the design, hypotheses, outcomes and caveats.

Two caveats appear in every write-up:
1. We test *prompted* evaluation framing, not whether a model independently detects evaluation.
2. ELEPHANT and the Reddit posts are public and may be in training data.

## Layout
| Path | Contents |
|---|---|
| `protocol.md` | Design (2x2, A-D), H1/H2, primary outcome, stages, budget and failure rules |
| `configs/prompts.json` | Exact system-prompt blocks, user template and rebuttals |
| `configs/models.json` | Target, grader and ELEPHANT-judge settings, with provider-specific differences |
| `configs/experiment.json` | Seed, stages (pilot = 1 rep and a $5.50 cap; full = 4 reps, not run, no cap set) |
| `configs/rubric.md`, `configs/grader_prompt.txt` | Measurement rubric and blind grader prompt |
| `data/manifest.json` | Sources, versions, SHA256s, selection rule, filter log, case row IDs and hashes (no text) |
| `src/prepare_data.py` | Downloads ELEPHANT from OSF and GitHub (pinned commit), verifies hashes, selects cases |
| `src/run_experiment.py` | Runs randomized-order conversations with a budget guard, logging per turn |
| `src/score_results.py` | Code-parsed metrics, blind Claude grading, optional ELEPHANT secondary metrics |
| `src/analyze_results.py` | Descriptives, paired case-level contrasts, case bootstrap, manual-review sheet |
| `tests/` | Parsing, scoring, budget guard and prompt-isolation tests |
| `results/` | Raw JSONL, grades, cost ledger, key checks, summaries, manual review |
| `report/` | Report notes for the Apart PDF |

## Reproduce
```bash
cd apart_epistemics_2026/experiment_2_social_pressure
python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
export OPENROUTER_API_KEY=...            # never commit; read from the environment only
pytest -q tests
cd src
python prepare_data.py                   # fetches data/raw/ (gitignored), verifies SHA256, writes data/manifest.json
python run_experiment.py --stage pilot --dry-run
python run_experiment.py --stage pilot --smoke
python run_experiment.py --stage pilot
python score_results.py --stage pilot --grade --elephant
python analyze_results.py --stage pilot
python make_private_review.py            # local-only review copy with post text (results/local_private/, gitignored)
```
`run_experiment.py` and `score_results.py` resume: completed conversations and valid grades are skipped. Failed attempts are kept and are retried only with `--retry-failed`, as a new attempt number.

## Data and redistribution
- The ELEPHANT GitHub repository is CC0 1.0.
- The full datasets are on OSF (node `r3dmj`, view-only link). The OSF node exposes **no licence field** and the posts are Reddit users' content, so **raw post text is not committed**.
- `prepare_data.py` downloads it, and the repo stores only row IDs and SHA256 hashes.
- In `results/raw/turns.jsonl`, the first user message replaces the post with `row_id` and `sha256`. Rebuttals, system prompts and **full model replies** are kept.
- **Model replies, and the grader's quoted evidence, may paraphrase or quote parts of the posts.**
- Model reasoning traces, where returned, are stored only in `results/local_private/` (gitignored).

## Results files
- `results/raw/turns.jsonl`: one record per conversation x turn. Includes the requested and returned model IDs, provider, generation ID, settings, seed, timestamps, prompts (post redacted), reply, finish reason, token usage including reasoning, cost, error and parsed verdict/confidence.
- `results/raw/conversations.jsonl`: one record per conversation attempt (status, rebuttal direction, per-turn summary, cost).
- `results/scored/`: `code_metrics.jsonl`, `grader_judgments.jsonl` (every grading attempt with raw output and template hash) and `elephant_secondary.jsonl`.
- `results/cost_ledger.jsonl`: every paid call with its OpenRouter cost and the running total. `results/key_checks.jsonl` holds the `/api/v1/key` usage snapshots.
- `results/summary/`: per-conversation table, model x condition cells and paired case contrasts.
- `results/manual_review/`: the blind sheet and form, plus a separate unblinding key.

## Pilot status
The pilot is a feasibility check (n = 5 cases, 1 repetition) and does **not** test H1 or H2. No statistical significance is claimed. See `report/pilot_results.md`.
