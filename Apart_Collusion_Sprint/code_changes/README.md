# Code changes

Our changes to the upstream starter repository ([poseidon-research/collusion_hackathon](https://github.com/poseidon-research/collusion_hackathon)), as a patch series against commit `d585a7b`.

Apply with: `git checkout d585a7b && git am code_changes/*.patch`

## Provenance

Commit times show each protocol was committed before the runs it governs. Run times are in each session's `experiment_metadata.json` and in the folder names under `data/`.

| Patch | Commit | Committed | Subject |
|---|---|---|---|
| 0001 | 10b029e | 2026-10-23 20:25 | Sprint 3.4 Phase 2: fixed-onset A/W/WG/E arms, enforced cap, spend ledger, snapshots, tests |
| 0002 | 70ce1a2 | 2026-10-23 20:28 | Sprint 3.4: freeze A-vs-E pilot protocol, analysis code and noise derivation |
| 0003 | 445e311 | 2026-10-23 20:30 | Sprint 3.4: offline verifier for real round-4 snapshots |
| 0004 | 31eedb9 | 2026-10-23 20:40 | Sprint 3.4: shared-prefix branching from arm-A round-4 snapshots (--branch_from) |
| 0005 | 1fc100e | 2026-10-23 20:53 | Sprint 3.4: message validation sample (80, seeded) and manual labels, committed before classifier code |
| 0006 | d6194e0 | 2026-10-23 21:00 | Sprint 3.4: freeze sweep protocol, communication metrics, analysis and runner |
| 0007 | d6ceabf | 2026-10-23 23:11 | Phase 3: freeze post-hoc WO follow-up protocol (watched, messaging off from round 5) |
| 0008 | 5dbf4c5 | 2026-10-24 07:08 | Phase 3 amendment 1: snapshot schema-compatibility check (allowlisted new fields at defaults) |
| 0009 | ffeb170 | 2026-10-24 07:46 | Blinded external-rater package (30 stratified messages, seed 20261024) + pre-committed comparison |
| 0010 | c65428e | 2026-10-24 07:57 | Add external (Grok) blinded labels, unchanged as received (sha1 23600ab9) |
| 0011 | 351fbfe | 2026-10-24 07:57 | Grok blinded-label comparison output (pre-committed compare_grok.py, unchanged) |
| 0012 | 2235489 | 2026-10-24 08:19 | Phase 4: direct Anthropic API adapter (Sonnet 5.5 sellers, Haiku 5.5 buyers) + WON arm |
| 0013 | 4046d19 | 2026-10-24 08:23 | Phase 4: freeze replication protocol, analysis, runner and WON isolation check |
| 0014 | aae3dc4 | 2026-10-24 11:25 | Crossed-model follow-up: mixed_crossed routing (Claude sellers direct, GPT buyers via OpenRouter) |
| 0015 | fbf7725 | 2026-10-24 11:27 | Freeze crossed-model follow-up protocol, analysis and runner (Sonnet 5.5 sellers x GPT-4.1-mini buyers, A/E, seeds 0-4) |

Times are US Central (UTC−5). Later commits on the working branch (evidence freeze `6f418a1` and figure updates) are delivered as files in `paper/` rather than patches, because they also touched an unpublished manuscript draft.
