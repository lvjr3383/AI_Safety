# Third reader (non-Claude) — how to run

Purpose: one blinded reader from a different model family on the same frozen 149 rows, same locked rule.

1. Use Gemini or GPT in a **fresh chat that has never seen this project**. Not the ChatGPT thread used for the audit review: it has seen the labels and results. Turn memory off or use a temporary chat. No web search.
2. Run **three separate messages or chats**, one per chunk. Each time attach `RULES_LOCKED.md` and one `sheet_chunkN.md`, and paste `READER3_PROMPT.txt` unchanged.
3. Save each reply's CSV block as `reader3_chunk1.csv`, `reader3_chunk2.csv`, `reader3_chunk3.csv`. Do not edit them. Do not ask the model to revise.
4. Note the exact model name/version and the date.
5. Send the three CSVs back here with the model name. They get hashed before the key is opened.

Row counts: chunk 1 = 49 (S001-S049), chunk 2 = 50 (S050-S099), chunk 3 = 50 (S100-S149).
Do not change the rule, the prompt, or the sheets. If the model refuses or returns fewer rows, report that as-is rather than retrying with new wording.
