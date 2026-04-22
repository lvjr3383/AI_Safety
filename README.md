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
- `ARTICLE_PART1.md` — writeup: reproducing the alignment faking paper
- `ARTICLE_PART2.md` — writeup: contributing to the UK AISI inspect_evals framework
- `ARTICLE_PART3.md` — writeup: running experiments on Claude 4.x models
- `setup.sh` — one-click setup script
- `.env.example` — annotated API key template
- `Dockerfile` — reproducible container

### llama-awareness-gap (Part 5)

Pilot experiment testing whether Llama 3.3 70B exhibits alignment faking behavior when exposed to the Greenblatt et al. helpful-only prompt framing.

100 calls via Groq API across 20 harmful request types. 55 runs produced scratchpad reasoning; the remaining 45 returned flat refusals with no scratchpad.

**Key findings:**
- 96.4% of scratchpad runs classified as Meta-Reasoning — model engages the RLHF framing as a real constraint and reasons within it
- 80% compliance rate among scratchpad runs
- Zero adversarial recognition — unlike Claude 4.x, Llama never identified the training pressure framing as a manipulation mechanism
- CBRN and weapons-of-mass-casualty requests returned flat refusals with no scratchpad across all runs; financial crimes, fraud, and harassment requests produced scratchpad reasoning at high rates

**Published:**
- Substack: https://open.substack.com/pub/lvjr3383/p/my-100-run-audit-of-llama-33-what?r=w4j53&utm_campaign=post&utm_medium=web&showWelcomeOnShare=true
- Medium: https://medium.com/@lvjanakiram/my-100-run-audit-of-llama-3-3-what-open-weight-models-know-about-their-own-training-c45440b93504

**Artifacts:** [`llama-awareness-gap/`](llama-awareness-gap/)
- `pilot_runner.py` — experiment script (Groq API, 100 calls)
- `full_run_results.json` — raw results for all 100 runs
- `auto_classify.py` — automated scratchpad classifier using same model
- `classifications.json` — classification output (category + compliance for 55 scratchpad runs)

### inspect_evals contribution (Phase 2)

Contributed to the UK AI Safety Institute's [inspect_evals](https://github.com/UKGovernmentBEIS/inspect_evals) — the evaluation framework used for government pre-deployment AI safety assessments.

**PR submitted:**
- [inspect_evals #1175](https://github.com/UKGovernmentBEIS/inspect_evals/pull/1175) — add per-category results table to `parse_eval_logs_for_evaluation_report.py` (issue #1139)

### interrogation-control-protocol

Three-condition evaluation of interrogation-based AI control protocols, built for the AI Safety Hackathon. Tests whether open monitoring (agent knows it will be questioned) outperforms surprise scrutiny in catching adversarial coding agents.

Three-component pipeline: untrusted agent (Claude Haiku) proposes code actions, trusted interrogator (Claude Sonnet) asks adversarial follow-up questions before execution, safety classifier (Claude Sonnet) issues BLOCK or EXECUTE decisions. 8 scenarios × 3 conditions = 24 evaluations.

**Key finding:** The aware condition (75% accuracy, 0 false positives) outperformed both baseline (50%) and unaware surprise interrogation (37.5%). Open interrogation causes agents to over-explain, which surfaces inconsistencies a trusted monitor can catch. Concealing the fact of monitoring provided no detection advantage.

**Artifacts:** [`interrogation-control-protocol/`](interrogation-control-protocol/)
- `main.py` — entry point
- `src/scenarios.py`, `agents.py`, `interrogator.py`, `classifier.py`, `harness.py` — pipeline components
- `results/` — per-run JSON output

### biosignal

Wastewater anomaly contextualization pipeline for pandemic early warning, built for the Equistamp Track 2 Hackathon. Fills the gap between CDC NWSS anomaly detection and actionable public health intelligence.

Three-layer pipeline: CDC NWSS data ingestion and sentinel value cleaning, population-weighted priority scoring (`(percentile × 0.5) + (log10(population_served) × 10)`), and Claude-generated structured SITREPs for the top-ranked alert sites. The LLM explains what the statistics already confirmed — it does not make the anomaly determination.

Validated against the December 2023 JN.1 surge: pipeline correctly surfaced New Jersey, Las Vegas, and Boston as top alerts before clinical case counts peaked.

**Artifacts:** [`biosignal/`](biosignal/)
- `main.py` — entry point
- `src/pipeline.py` — data cleaning and scoring
- `src/contextualizer.py` — SITREP generation via Claude Sonnet
- `data/` — CDC NWSS CSV (excluded from git, sourced from CDC)
- `results/` — per-run JSON output (excluded from git)
