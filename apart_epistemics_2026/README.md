# Apart AI x Epistemics Research Sprint (13-15 November 2026)

This folder holds **two separate studies**, submitted as **two separate entries**. They share no data, code paths or results and are not one merged paper.

| | Experiment 1 | Experiment 2 |
|---|---|---|
| Title | When the Evidence Is Available: Testing Research Agents Against Corrupted and Falsely Verified Results | Does Evaluation Awareness Mask Social Sycophancy? |
| Folder | [`experiment_1_research_integrity/`](experiment_1_research_integrity/) | [`experiment_2_social_pressure/`](experiment_2_social_pressure/) |
| Submission PDF (authoritative) | [`report/submission/exp1_submission.pdf`](experiment_1_research_integrity/report/submission/exp1_submission.pdf) | [`paper/exp2_submission.pdf`](experiment_2_social_pressure/paper/exp2_submission.pdf) |
| Editable source | [`report/submission/template.html`](experiment_1_research_integrity/report/submission/template.html) -> `src/make_submission.py` -> [`exp1_submission.html`](experiment_1_research_integrity/report/submission/exp1_submission.html) | Official-template Google Doc (linked in the manuscript README); Markdown mirror [`paper/manuscript.md`](experiment_2_social_pressure/paper/manuscript.md) |
| Protocols | [`protocol.md`](experiment_1_research_integrity/protocol.md) (v1, Amendment 1), [`protocol_v2.md`](experiment_1_research_integrity/protocol_v2.md), [`FREEZE_v2.json`](experiment_1_research_integrity/FREEZE_v2.json), fixture checksums | [`v2_study/PROTOCOL.md`](experiment_2_social_pressure/v2_study/PROTOCOL.md) (frozen), [`v2_study_anthropic/PROTOCOL_ADDENDUM.md`](experiment_2_social_pressure/v2_study_anthropic/PROTOCOL_ADDENDUM.md) (frozen), pilot snapshot checked by [`verify_frozen.py`](experiment_2_social_pressure/verify_frozen.py) |
| Results | [`results/`](experiment_1_research_integrity/results/) (v1, 60 sessions), [`results/v2/`](experiment_1_research_integrity/results/v2/) (v2, 90 sessions) | [`v2_study_anthropic/results/analysis/`](experiment_2_social_pressure/v2_study_anthropic/results/analysis/) (720 conversations; tables in `RESULTS_TABLES.md`) |
| Setup and reproduction | [`README.md`](experiment_1_research_integrity/README.md) | [`REPRODUCTION.md`](experiment_2_social_pressure/REPRODUCTION.md) (the folder `README.md` is part of the frozen pilot snapshot) |

Submission details (final commit, PDF SHA-256 hashes, page counts, Drive links, validation results): [`SUBMISSION_MANIFEST.md`](SUBMISSION_MANIFEST.md).

## Scope reminders

- **Experiment 1:** 150 completed sessions across three Claude models; 90 compromised; no corrupted headline published. Only the first 20 sessions were pre-registered; the remaining 130 are exploratory. One accessible-evidence task, not a claim of general robustness.
- **Experiment 2:** 720 completed three-turn conversations (three Claude models, 30 cases, four conditions, two repetitions) are the analytic unit. The earlier OpenRouter GPT/Gemini pilot and the v3 AI-grader exercise are exploratory and not pooled. AI graders and audits are not human validation.

## Offline reproduction (no API calls, no cost)

```sh
# Experiment 1 (sandbox tests need macOS sandbox-exec; they skip elsewhere)
cd apart_epistemics_2026/experiment_1_research_integrity
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python src/generate_fixtures.py --check
.venv/bin/python src/generate_fixtures_v2.py --check
.venv/bin/python src/make_submission.py --html-only   # regenerate HTML + data assertions; PDF build uses macOS Chrome (or WeasyPrint on the HTML)

# Experiment 2
cd ../experiment_2_social_pressure
python3 -m venv .venv && .venv/bin/pip install -r requirements-analysis.txt
.venv/bin/python verify_frozen.py
.venv/bin/python v2_study/verify_protocol.py
.venv/bin/python v2_study_anthropic/verify_addendum.py
.venv/bin/python -m pytest -q tests v2_study/tests v2_study_anthropic/tests
.venv/bin/python v2_study_anthropic/src/analyze_anthropic.py
.venv/bin/python v2_study_anthropic/src/analyze_anthropic.py --exclude-ceiling
.venv/bin/python v2_study_anthropic/src/report_anthropic.py
```

Raw ELEPHANT post text and private transcripts (`**/local_private/`) are never committed.
