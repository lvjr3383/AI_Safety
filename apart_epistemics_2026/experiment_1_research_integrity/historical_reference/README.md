# Historical reference (pre-existing research, not part of the sprint)

Experiment 1 is motivated by our earlier AI Village Codex judging investigation, which was completed before the
Apart AI x Epistemics sprint:

- Repository: https://github.com/lvjr3383/ai-village-codex-judging-evidence
- Commit inspected: `b41bddbfb61541ca2c1662f10fac53739697120c` (release v1.0.0)
- `SHA256SUMS` in that repository verified OK for all six files on 2026-11-14.

**No files from that package are copied here, and none of its records are modified or reclassified.** We inspected `verify.py` and
`archived_generator.py` by reading them and did not execute either. The checksums are recorded in `../MANIFEST.json`.

## What the inspection established (restating the package, not new findings)

- The archived generator (`score_natively_fast.py`, extracted from source event
  `t:55933f3a-5c78-4182-b233-1c9e9cdc711c`) assigns Gemini 3.1 Pro label-swap scores with a word-count/structure
  heuristic plus `random.uniform` noise, adds +0.5 when the displayed label is `gemini-3.1-pro` and subtracts 0.5 when
  it is `kimi-k2.6`, and prints "Scored session N natively".
- The package's `results.json` reports that rerunning this generator reproduces the saved score sheets exactly at
  the pinned commits.
- The public report it includes describes these as native in-context scores and reports Gemini label effects.

## What Experiment 1 takes from it

Only the failure mode: a compiled score sheet that does not come from the judging it is presented as, carrying a
label effect the judge did not produce. Experiment 1 tests whether new agents publish such a result when the raw
judge records that contradict it sit next to it in the workspace. All Experiment 1 data is synthetic.
