# Experiment 2 v2: Anthropic-only extension, protocol addendum (Apart AI x Epistemics sprint, Nov 13-15 2026)

Status: **frozen before the full run.** `python v2_study_anthropic/verify_addendum.py` checks every file listed in
`ADDENDUM_CHECKSUMS.sha256`, and the runner also requires `v2_study/verify_protocol.py` to pass.

This is a separate study arm. The GPT/Gemini pilot, the v3 grading, and the frozen v2 protocol (`v2_study/`, branch
`frozen/exp2-v2-protocol-v1`, commit bbc3901) are unchanged. Their results are never mixed with this arm's results.
The study is fully automated: no manual grading, no AI judges, and no OpenRouter calls.

## What is reused unchanged (imported read-only from `v2_study/`)
- **Cases:** the same 30 cases (`v2_study/config/manifest_v2.json`, checked by post hash before every run).
- **Prompts:** the same prompts (`v2_study/config/prompts_v2.json`): system texts, the first user message with Verdict / Blame / Confidence lines, and the fixed rebuttals pushing toward "not in the wrong".
- **Design:** the same four conditions A-D, 2 repetitions, 3 turns, and shuffle seed 20261114.
- **Scoring:** the same parsers, outcomes (primary: Verdict-line movement and confidence change; secondary: Blame), hypotheses H1-H3, case-level analysis, case bootstrap (B = 10000, seed 20261116), ceiling sensitivity, missing-data rules, and caveats.
- **Caveat:** moving under pressure is not necessarily dishonesty.

## Deviations from the frozen v2 protocol
1. **Provider:** the Anthropic Messages API, called directly (`ANTHROPIC_API_KEY`, `anthropic-version: 2023-06-01`), instead of OpenRouter.
2. **Targets:** three Claude models instead of GPT-5.5 and Gemini 3.1 Pro. 30 x 4 x 2 x 3 = **720 conversations**. The IDs were verified with the free `GET /v1/models` (`results/model_checks.jsonl`, 2026-11-14):
   - `claude-sonnet-4-6` (Sonnet 4.6, mid tier, primary)
   - `claude-haiku-4-5-20251001` (Haiku 4.5, small tier)
   - `claude-opus-4-7` (Opus 4.7, large tier)
3. **System prompt placement:** the system prompt goes in Anthropic's top-level `system` field rather than in a system-role message. The text is identical.
4. **No seed:** the Anthropic API has no seed parameter, so sampling is not seed-reproducible. The int32 conversation seed is recorded only as an identifier (`seed_not_sent`). The pilot's seeds were also best-effort.
5. **Temperature:** none is sent, so the API default applies, as in the pilot (where no temperature was sent either). Defaults differ across providers.
6. **Extended thinking off:** no `thinking` parameter is sent. In the pilot, GPT had reasoning effort none and Gemini low (Gemini's cannot be disabled). In the smoke test every Claude response contained only `text` blocks. Any non-text blocks are recorded and excluded from parsing.
7. **Unchanged settings:** max_tokens stays 2000. No tools, no prompt caching, no batch API.
8. **Cost tracking:** cost is the token usage returned by the API x official list price (https://docs.anthropic.com/en/docs/about-claude/pricing, fetched 2026-11-14), recorded per call with the model and token counts in `results/ledger_anthropic.jsonl`. The provider does not report a cost.
   - List prices (input / output per million tokens): Sonnet 4.6 $3 / $15; Haiku 4.5 $1 / $5; Opus 4.7 $5 / $25.
   - Opus 4.7 uses a newer tokenizer (about 30% more tokens per text), which the token counts capture.
9. **Budget control:** the Anthropic API cannot report the credit balance or promotional-credit eligibility. Jack reports $100 in promo credits expiring 2026-12-13 that cover API use; this is user-reported and not verified.
   - The hard cap (`--cap`) is the only budget control. The proposed cap is $50.
   - The runner refuses without `--cap` and `--authorized`, without a smoke-test cost basis for every model, if either verify script fails, or if the projection exceeds cap - ledger spend.
   - The projection is the smoke-test mean cost per conversation x 1.25 (the v2 arm used pilot spend instead).
10. **Transient retries:** HTTP 429/500/502/503/529 and network errors are retried within a turn, up to 4 times with backoff. Errors cost $0. Failed conversations are rerun only with `--retry-failed`, as a new attempt.
11. **Smoke test:** 2 conversations per model (case #1 condition A rep 0; case #2 condition D rep 0). They have a separate ledger and are excluded from the main analysis.
12. **Analysis scope:** `src/analyze_anthropic.py` runs the frozen `analyze_v2.py` functions on this arm's results only.
    - It reports results per model, plus "pooled" = mean over the three Claude models.
    - **Exploratory addition (H4):** do model tiers differ? For each outcome it reports between-model differences of each case-level contrast and of overall movement (mean over conditions), using the same case bootstrap. This is descriptive only, with no direction predicted.
13. **Generalisation:** all targets come from one provider, so this arm tests differences within the Claude family. It does not generalise across providers, and it cannot be pooled with the GPT/Gemini results.
