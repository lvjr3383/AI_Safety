# AI Safety Projects

Personal workspace for AI safety research and tooling contributions.

## Projects

### alignment-faking-audit

Reproducibility audit of Anthropic's alignment faking paper
([safety-research/open-source-alignment-faking](https://github.com/safety-research/open-source-alignment-faking)).

Found 11 friction points blocking any researcher from running the pipeline out of the box,
including 3 hard crashes before a single API call. Fixed all 11 and contributed upstream.

**PRs submitted (Phase 1):**
- [safety-tooling #155](https://github.com/safety-research/safety-tooling/pull/155) — fix startup crash when `OPENAI_API_KEY` is unset
- [open-source-alignment-faking #2](https://github.com/safety-research/open-source-alignment-faking/pull/2) — one-click setup script, `.env.example`, Dockerfile
- [safety-tooling #156](https://github.com/safety-research/safety-tooling/pull/156) — fix crash when `TOGETHER_API_KEY` / `GRAYSWAN_API_KEY` is blank in `.env`

**Artifacts:** [`alignment-faking-audit/`](alignment-faking-audit/)
- `REPRODUCIBILITY_AUDIT.md` — full audit log with all 11 friction points
- `ARTICLE_PHASE1.md` — writeup: reproducing the alignment faking paper
- `ARTICLE_PHASE2.md` — writeup: contributing to the UK AISI inspect_evals framework
- `setup.sh` — one-click setup script
- `.env.example` — annotated API key template
- `Dockerfile` — reproducible container

### inspect_evals contribution (Phase 2)

Contributed to the UK AI Safety Institute's [inspect_evals](https://github.com/UKGovernmentBEIS/inspect_evals) — the evaluation framework used for government pre-deployment AI safety assessments.

**PR submitted:**
- [inspect_evals #1175](https://github.com/UKGovernmentBEIS/inspect_evals/pull/1175) — add per-category results table to `parse_eval_logs_for_evaluation_report.py` (issue #1139)
