# Final Evidence (frozen for the report)

**Source of every number:** recomputed from the saved run logs by `paper/build_evidence.py`, using the same frozen functions as the experiments. Machine-readable copies are in `paper/evidence/evidence.json`, `sessions.csv` (51 sessions) and `trajectories.csv`.

**Session data locations:**
- `runs/` (GPT-4.1)
- `runs_claude/exp/` (Sonnet × Haiku)
- `runs_crossed/exp/` (Sonnet × GPT-4.1-mini)

**Common definitions**
- **Market:** 5 sellers (cost $80) and 5 buyers (value $100), 20 rounds, one unit per agent per round, trades at the midpoint of crossing ask and bid. CEO "boss pressure" prompt in every arm.
- **Primary metric S:** the session mean, over rounds 15–20, of each round's mean *posted seller ask*. The session is the unit of analysis.
- **Benchmark caution.** With identical costs ($80) and values ($100) and equal numbers of buyers and sellers, *any* price in [$80, $100] clears every unit. The "$90 competitive price" in Agrawal et al. and in the starter code is the midpoint of that range, a convention rather than a unique equilibrium, and $100 is the joint-profit maximum. The paper therefore does not call prices above $90 "collusive" or "supracompetitive". It compares arms with each other.

## 1. Evidential status of each experiment

| Experiment | Arms | Status |
|---|---|---|
| E1 pilot: GPT-4.1 sellers × GPT-4.1-mini buyers | A vs E, seeds 0–2 | **Pre-registered** (`PROTOCOL.md`, `70ce1a2`) |
| E1 sweep | A, W, WG (seeds 0–6), branched at round 4 | **Pre-registered** (`SWEEP_PROTOCOL.md`, `d6194e0`) |
| E1 follow-up | WO (seeds 0–6) | **Designed post hoc, frozen before running** (`d6ceabf`; amendment `5dbf4c5`, an integrity-check fix only) |
| E2: Sonnet 5.5 × Haiku 5.5 | A vs E, seeds 0–4; gate STOP | **Designed post hoc, frozen before running** (`4046d19`) |
| E3: Sonnet 5.5 × GPT-4.1-mini | A vs E, seeds 0–4 | **Designed post hoc, frozen before running** (`fbf7725`) |

## 2. E1, GPT-4.1 sellers × GPT-4.1-mini buyers

**A vs E**

| Comparison | Estimate | 95% CI | Notes |
|---|---|---|---|
| **Main: pre-registered pilot, A − E, Welch, n = 3 vs 3** | **+$2.80** | [+1.69, +3.90] | A 96.38 (SD 0.53), E 93.59 (SD 0.40). Gate **GO**. |
| Post-hoc secondary: all A (n = 7) vs E (n = 3), Welch | +$3.10 | [+2.33, +3.87] | A 96.68 |

The paper uses +$2.80 as the main estimate everywhere; +$3.10 is mentioned once as a secondary check.

**Transaction prices, rounds 15–20 (secondary, not pre-registered)**
- Pilot: A − E = **+$3.28**, 95% CI [+0.94, +5.62], with A 96.41 vs E 93.13.
- 7 vs 3: +$3.53, CI [+1.04, +6.03].

**Treatments after round 4** (seed-paired on S, n = 7 pairs; pre-registered except WO)

| Comparison | Mean | 95% CI | 90% CI (TOST, ±$1) | Seeds −/+ | Verdict |
|---|---|---|---|---|---|
| W − A | −$0.19 | [−0.41, +0.03] | [−0.37, −0.02] | 7/0 | equivalent within ±$1 |
| WG − W | +$0.09 | [+0.02, +0.15] | [+0.04, +0.13] | 1/6 | different, but within ±$1 |
| WG − A (secondary) | −$0.11 | [−0.34, +0.12] | [−0.29, +0.08] | 3/4 | — |
| WO − WG (post hoc) | +$0.03 | [−0.08, +0.14] | [−0.05, +0.12] | 4/3 | equivalent within ±$1 |
| WO − A (post hoc, secondary) | −$0.07 | [−0.27, +0.13] | [−0.23, +0.08] | 4/3 | — |

**Prices had settled by round 4 (sticky prices)**
- Measure: S minus the round-4 mean ask, per session.
- **A, W, WG, WO:** 23 of 28 sessions moved by less than $0.25. The largest moves were −$0.70 (WG seed 6), −$0.69 (W seed 6), −$0.68 (W seed 0) and −$0.67 (WO seed 6).
- **E:** −$3.31, −$1.58, −$1.35.
- **Trajectories:** A stays near its opening level ($96.97 in round 1, $96.61 in round 20). E falls steadily ($96.61 to $93.11).
- **Where the gap opens:** A − E is +$0.36 in round 1 and +$1.11 in round 4 (CI includes 0). It first exceeds $1.50 in round 6.

**Messages, rounds 5–20 (pre-registered rule-based classifier; explicit price proposals / non-empty messages)**

| Arm | Proposals |
|---|---|
| A | 421 / 560 (75%) |
| W | 357 / 560 (64%) |
| WG raw | 0 / 560 |

- **W − A proposal rate** (paired): −0.11, 95% CI [−0.31, +0.08], **inconclusive**.
- **WG cap:** 0 of 560 raw messages were longer than 5 characters, so sellers complied with the cap instruction.
- **Short signals still went through the cap:** "Hold" ×253, "Stead" ×156, "0.01" ×64 (seed 2 only), and price strings such as "97.57" (seed 4).
- **Classifier validation:** 80 messages, single rater (Claude), agreement 0.91. A blinded external rater (Grok), working from the written rubric, agreed with the classifier on 30/30 stratified messages. This is evidence that the classifier follows its written rules. It is **not** human validation, and it does not validate "collusion".
- **The price-mention category** is excluded from the paper's claims (under-validated).

## 3. E2, Sonnet 5.5 sellers × Haiku 5.5 buyers (frozen before running, designed post hoc)

**A vs E, n = 5 vs 5 (Welch)**
- **Estimate:** **+$0.51**, 95% CI [−1.29, +2.32]. A 90.76 (SD 1.32), E 90.25 (SD 1.14).
- **Gate rule:** STOP (Δ < $0.75, no variance flag). Stage 2 and the WON arm were not run.
- **Seed-paired:** +$0.51, CI [−1.11, +2.14].
- **Late trade price:** +$0.52, CI [−1.29, +2.32].
- **Trajectories:** both arms fall from about $95 to about $90 by round 5, then stay flat.

## 4. E3, Sonnet 5.5 sellers × GPT-4.1-mini buyers (frozen before running, designed post hoc)

**A vs E, n = 5 vs 5 (Welch)**
- **Estimate:** **−$0.93**, 95% CI [−4.16, +2.29]. A 91.17 (SD 2.60), E 92.11 (SD 1.43).
- **Rule:** INCONCLUSIVE. The variance flag is on: pooled SD 2.10 > 1.53. The largest single contributor is A seed 1 (S = 86.74).
- **Seed-paired:** −$0.93, CI [−2.97, +1.10], with 4 of 5 seeds negative.
- **Late trade price:** −$0.98, CI [−4.21, +2.25].
- **Buyer configuration:** verified identical to E1 by test (temperature 0.7, seed, JSON mode, `max_tokens`, `top_p`, model id).

## 5. Coordination language in the A arms (exploratory; the regex is not validated for Claude text)

Messages containing group language together with a price-like number (75–105, with or without "$"):

| Configuration | Messages |
|---|---|
| E1 | 472 / 700 |
| E2 | 371 / 478 |
| E3 | 414 / 475 |

These counts are descriptive only. Verbatim examples are in `QUOTES.md`.

## 6. Integrity and spending

**Integrity**
- 51 sessions, all valid.
- 0 refusals and 0 API errors across every ledger. One shell-launch failure in E1 (no calls, $0) and one safe pre-run stop in the WO follow-up ($0) are both documented.
- Every call returned the requested model.

**Spending, from the ledgers**

| Item | Amount |
|---|---|
| OpenRouter (E1: smoke, pilot, sweep, WO) | **$23.65** (reconciled with OpenRouter's `/key` to the cent) |
| Anthropic (E2, incl. smoke) | **$17.50** |
| E3 (incl. smoke): Anthropic + OpenRouter | **$18.62** ($17.22 + $1.40) |
| **Total** | **$59.77** |

The Anthropic figures still need checking against Console → Usage.

## 7. Model and inference settings

| Experiment | Sellers | Buyers |
|---|---|---|
| E1 | `openai/gpt-4.1`, T = 0.7 | `openai/gpt-4.1-mini`, T = 0.7 |
| E2 | `claude-sonnet-5-5` | `claude-haiku-5-5` |
| E3 | `claude-sonnet-5-5` | E1's `openai/gpt-4.1-mini` configuration |

- **E1** ran via OpenRouter, with JSON mode and the seed forwarded.
- **E2 and E3 Claude agents** ran on the direct Anthropic API: default sampling (the API rejects non-default sampling values), thinking off (Sonnet `between_tools` at effort `high`; Haiku `disabled` at effort `medium`), and no fallbacks.
