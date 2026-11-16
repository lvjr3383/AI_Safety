# Raw logs (Anthropic-only extension)

- `conversations.jsonl` is committed uncompressed. Post text is replaced by row ID and SHA-256.
- `turns_metadata.jsonl` is the committed turn log: parsed Verdict/Blame/Confidence lines, token counts, costs, retries, abandoned-request counts, and generation IDs. Post text, model response text, system prompts, and rebuttal wording are omitted here (rebuttals are in `v2_study/config/prompts_v2.json`; system-prompt hashes are on the conversation records).
- On the run machine, `turns.jsonl` (uncompressed) and `turns.jsonl.gz` keep the redacted turn log including model responses. Those files are not on GitHub: the uncompressed file exceeded the GitHub connector payload limit (HTTP 413), and the connector cannot send binary `.gz` or `.png` content as text.
- The post-containing transcript is only in the gitignored `results/local_private/turns_full.jsonl` and is not committed.

`src/report_anthropic.py` reads `turns.jsonl` if present, otherwise `turns.jsonl.gz`, otherwise `turns_metadata.jsonl`.
