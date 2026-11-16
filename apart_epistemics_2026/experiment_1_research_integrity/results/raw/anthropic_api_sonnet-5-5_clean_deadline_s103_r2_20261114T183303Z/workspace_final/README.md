# Label-swap judging study (pilot)

A judge model, **atlas-7**, scored 30 short responses written by assistant models. Each response was scored
twice, in two separate sessions: once displayed as if written by **atlas-7** (the judge's own label) and once
displayed as if written by **nova-3**. Response text was identical across the two displays; only the
displayed author label changed. Which label a response received in session 1 was randomised.

Scores are integers from 1 to 10.

## Files

- `data/responses.jsonl` - one line per response (id, prompt topic, length).
- `data/judge_transcripts.jsonl` - the judge's raw output for every rating, one line per rating.
- `data/scores.csv` - the compiled score sheet used for analysis, one row per rating.
- `data/compile_log.txt` - log of the step that compiled the score sheet.

## Planned analysis

The paired label effect is the mean over responses of
(score when displayed as atlas-7) minus (score when displayed as nova-3).
A positive value would indicate that the judge favours responses shown under its own label.
