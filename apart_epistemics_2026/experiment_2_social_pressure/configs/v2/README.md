# configs/v2: proposals and provider config (Apart AI x Epistemics sprint, Nov 13-15 2026)

Nothing here was used for the frozen pilot (`exp2-pilot-frozen-v1`, commit f9f6b18). The pilot's configs in `configs/` are unchanged; check with `python verify_frozen.py`.

| File | Status |
|---|---|
| rubric_v2_PROPOSAL.md, grader_prompt_v2_PROPOSAL.txt, grader_schema_v2_PROPOSAL.json | Proposal. Finalise after Jack's blind review, then freeze before any grading |
| grading_providers.json | Provider config for `src/grading_providers.py` |

## Grading provider
```python
from grading_providers import get_provider, guard_for
p = get_provider("anthropic")      # or "openrouter" (default) / None
guard = guard_for(p, cap_usd=2.00)  # ledger: results_v2/ledgers/grader_<provider>.jsonl
res = p.grade(prompt, guard, record={"conv_id": cid})
```
- Both providers use the same model (Claude Sonnet 4.6), the same prompt text, temperature 0, max_tokens 1500 and no extended thinking.
- **OpenRouter:** cost comes from the per-call `usage.cost`.
- **Anthropic direct:** no cost is returned, so it is computed from configured list prices ($3 / $15 per M tokens). Reconcile against the Anthropic console.
- Each provider keeps its own append-only ledger and budget cap. The historical `results/cost_ledger.jsonl` is never written by this module.
- Tests (`tests/test_grading_providers.py`) mock HTTP only. No call was made to either API.

### Before the first Anthropic run (free, no inference)
1. Jack supplies `ANTHROPIC_API_KEY` through a secure field. It is set as an environment variable only, never written to disk or committed.
2. `python -c "import sys; sys.path.insert(0,'src'); from grading_providers import free_model_check; print(free_model_check('anthropic'))"`. This calls GET /v1/models, which incurs no inference charge. Expect `listed: True` for `claude-sonnet-4-6`. If it isn't listed, update the model ID in `grading_providers.json` in a new commit.
3. Re-check the list price on Anthropic's pricing page and update `price_usd_per_token` if needed.
4. Note that Anthropic direct and OpenRouter routed to Anthropic serve the same model but are different endpoints. Report the provider for every grade, and don't mix providers within one analysis without a cross-provider agreement check.
