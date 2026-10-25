# Messages, Access and Prices: Measuring Communication Effects in LLM Seller Markets

Supporting materials for the paper by **Jack Lakkapragada** (Independent Researcher), written for the Apart Research AI Collusion Research Sprint, October 2026 (Track 3, Q3.4).

The study extends the continuous double auction of Agrawal et al. (2025) ([arXiv:2507.01413](https://arxiv.org/abs/2507.01413)). The paper itself is submitted separately. This folder holds everything behind it: the frozen protocols, our code changes, the analysis scripts, the session logs and Appendices B to E.

## What we tested

Five sellers (cost $80) and five buyers (value $100) trade over 20 rounds. Every seller gets the same simulated CEO pressure to keep margins high. The primary outcome is the mean posted seller ask over rounds 15 to 20, with the session as the unit.

| Arm | Seller messaging |
|---|---|
| A | Open throughout |
| E | Off from round 1 (independent sessions) |
| W | Open, plus a monitoring warning from round 5 |
| WG | Warning plus a five character cap, enforced in code, from round 5 |
| WO | Warning plus messaging fully off from round 5 (follow up) |

W, WG and WO each restart from the same saved round-4 state of the matching A session.

| Experiment | Sellers | Buyers | Sessions | Status |
|---|---|---|---|---|
| E1 | GPT 4.1 | GPT 4.1 mini | 31 | Pilot and sweep preregistered; WO a follow up |
| E2 | Claude Sonnet 5.5 | Claude Haiku 5.5 | 10 | Follow up, frozen before running |
| E3 | Claude Sonnet 5.5 | GPT 4.1 mini | 10 | Follow up, frozen before running |

## Main results

| Comparison | Estimate | 95% CI | Note |
|---|---|---|---|
| E1 A − E (pilot, 3 v 3) | +$2.80 | [+1.69, +3.90] | Passed the preregistered gate |
| E1 W − A (7 pairs) | −$0.19 | [−0.41, +0.03] | Equivalent within ±$1 |
| E1 WG − W (7 pairs) | +$0.09 | [+0.02, +0.15] | Small, within ±$1 |
| E1 WO − WG (7 pairs) | +$0.03 | [−0.08, +0.14] | Equivalent within ±$1 (follow up) |
| E2 A − E (5 v 5) | +$0.51 | [−1.29, +2.32] | Gate STOP |
| E3 A − E (5 v 5) | −$0.93 | [−4.16, +2.29] | Inconclusive |

Prices in the messaging sessions had largely settled by round 4, before any intervention began. See the paper and [`paper/FINAL_EVIDENCE.md`](paper/FINAL_EVIDENCE.md) for the limits on what these results show.

## Contents

| Path | What it holds |
|---|---|
| [`APPENDICES.md`](APPENDICES.md) | Appendices B to E of the paper: message quotations, classifier validation, reanalysis of the original data, implementation and costs |
| [`paper/`](paper/) | Frozen evidence (`FINAL_EVIDENCE.md`, `CLAIM_AUDIT.md`), verified references and quotations, the figures, and `build_evidence.py`, which recomputes every number from the logs |
| [`protocols/`](protocols/) | The five frozen protocols: pilot, sweep, WO follow up, E2 (Phase 4) and E3 (crossed) |
| [`code_changes/`](code_changes/) | Our changes to the upstream code as 15 patches, with commit times showing each protocol was frozen before its runs |
| [`analysis/`](analysis/) | Analysis, verification and runner scripts; the classifier validation set; the blinded Grok labelling package and its results |
| [`data/`](data/) | All 51 sessions: `auction_results.md` (every ask, bid, trade and message), `experiment_metadata.json`, `usage.jsonl`, `collusion_metrics.json`, plus the per-call spend ledgers |

Not included: API credentials, per-agent prompt transcripts and saved round-4 states (about 100 MB, available on request), and the upstream repository and its released data.

## Reproducing the analysis (no API calls)

1. Clone the upstream starter repository and check out commit `d585a7b`:
   `git clone https://github.com/poseidon-research/collusion_hackathon && cd collusion_hackathon && git checkout d585a7b`
2. Apply our patches: `git am ../Apart_Collusion_Sprint/code_changes/*.patch`
3. Copy `paper/` into the clone, and copy the three folders in `data/` next to the clone:

   ```
   workdir/
     collusion_hackathon/        upstream + patches
       paper/                    from this folder
     runs/  runs_claude/  runs_crossed/   from data/
   ```
4. Set up the environment in `collusion_hackathon/llm-agent-collusion` (we used uv 0.9.5), then run
   `python ../paper/build_evidence.py` from that directory.

We tested these steps on a fresh clone. They regenerate `paper/evidence/evidence.json`, `sessions.csv`, `trajectories.csv` and `quotes.json` byte for byte.

Rerunning the experiments needs your own `OPENROUTER_API_KEY` and `ANTHROPIC_API_KEY` and costs money (about $60 in total for this study). The runner scripts are in `analysis/run_*.sh`, and the settings are in the protocols and Appendix E.

## Provenance and caveats

- The patches change only `llm-agent-collusion/` and add `sprint34/`. They contain a few lines of upstream code as diff context.
- The upstream repository has no licence, so we do not redistribute it. No licence has been chosen for the files in this folder yet.
- The classifier reference labels were made by one AI rater (Claude), with a blinded check of 30 messages by Grok. There was no human validation.
- AI assistance is described in the paper's LLM Usage Statement.
