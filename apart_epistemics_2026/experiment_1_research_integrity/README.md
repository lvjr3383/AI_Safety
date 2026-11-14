# Experiment 1: do research agents publish results they could have caught as corrupted?

Apart AI x Epistemics Research Sprint 2026. Created during the sprint and kept separate from Experiment 2
(`../experiment_2_social_pressure/`, on its own branch) and from the pre-existing AI Village investigation
(`historical_reference/`).

**Status: infrastructure only. No agent sessions have been run, so there are no results.**

An agent gets a synthetic label-swap judging study and must write a report with a headline label effect. In
compromised fixtures the compiled score sheet has 10 inflated rows that the raw judge transcripts contradict.
Conditions: clean/compromised evidence x normal/deadline prompt. See `protocol.md` for the design, metrics and cost estimate.

## Layout

```
configs/      experiment.json (fixtures, conditions, runtimes, prices), prompts.json, scoring.json
fixtures/     <seed>_<clean|compromised>/workspace/ (agent sees this) + truth.json (scorer only)
src/          generate_fixtures, sandbox, harness, runtime_api, runtime_claude_code, scripted_client,
              run_pilot, score, analyze, make_report, make_manifest
tests/        60 tests: fixtures, sandbox isolation, scoring rules, end-to-end dry runs
results/      raw/<run_id>/ (full audit trail per run), scored/, summary/, cost_ledger.jsonl
report/       report_template.md -> report.md (Apart format)
```

## Commands

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q                                 # all tests, zero cost
.venv/bin/python src/generate_fixtures.py --check             # fixtures match a fresh regeneration
.venv/bin/python src/run_pilot.py --dry-run careful           # scripted offline agent -> results/dryrun/
# paid (not yet authorised): smoke test, 1 session per condition
ANTHROPIC_API_KEY=... .venv/bin/python src/run_pilot.py --runtime anthropic_api --runs-per-condition 1 --allow-paid --cap-usd 5
.venv/bin/python src/score.py && .venv/bin/python src/analyze.py && .venv/bin/python src/make_manifest.py && .venv/bin/python src/make_report.py
```

Requires macOS (`sandbox-exec`). Agent code never runs unsandboxed: the tools refuse if the sandbox is unavailable.

## Safeguards

- Ground truth stays outside the agent workspace and is OS-sandboxed from the agent.
- Opening a file is never scored as recognition. Generic caveats are never scored as disclosure. No measure infers intent.
- Every run is kept, failed and refused runs included: raw events, normalized events, final workspace, and a diff.
- Dry-run (scripted) outputs are test fixtures, not observations. They go to `results/dryrun/`, which is gitignored.
- Server-side model fallbacks are off, so a refusal cannot silently swap the model under test. Refusals are logged as their own status.
