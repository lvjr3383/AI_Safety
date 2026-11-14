# Scoring changelog

Rules live in `configs/scoring.json` and `src/score.py`. Every scored row records `scorer_version` and
`scorer_sha256`. Each version writes to `results/scored/<version>/`, and earlier versions' outputs are kept.
A change made after looking at agent outputs gets a new version and an entry here with the reason and the runs that prompted it.
All runs are then re-scored under the new version. Freeze before the remaining pilot sessions.

## v1 (frozen 2026-11-14, before any agent session)

Initial rules as described in `protocol.md`. Validated only on hand-written test strings and scripted agents.
