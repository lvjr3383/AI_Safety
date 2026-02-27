# AI Safety Projects

Personal workspace for AI safety research and tooling contributions.

## Projects

### alignment-faking-audit

Reproducibility audit of Anthropic's alignment faking paper
([safety-research/open-source-alignment-faking](https://github.com/safety-research/open-source-alignment-faking)).

Found 10 friction points blocking any researcher from running the pipeline out of the box,
including 3 hard crashes before a single API call. Fixed all 10 and contributed upstream.

**PRs submitted:**
- [safety-tooling #155](https://github.com/safety-research/safety-tooling/pull/155) — fix startup crash when `OPENAI_API_KEY` is unset
- [open-source-alignment-faking #2](https://github.com/safety-research/open-source-alignment-faking/pull/2) — one-click setup script, `.env.example`, Dockerfile

**Artifacts:** [`alignment-faking-audit/`](alignment-faking-audit/)
- `REPRODUCIBILITY_AUDIT.md` — full audit log with all 10 friction points
- `setup.sh` — one-click setup script
- `.env.example` — annotated API key template
- `Dockerfile` — reproducible container
