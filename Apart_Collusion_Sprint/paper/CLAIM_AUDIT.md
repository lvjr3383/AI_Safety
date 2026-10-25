# Claim Audit

**How to read this file:** each claim the paper makes is listed with its evidence, its status, and the wording rule it must follow. Every number comes from `paper/evidence/evidence.json`.

## Claim 1 (E1, GPT-4.1 sellers)

> In our GPT-4.1 seller configuration, communication was associated with higher asking prices. Introducing a monitoring announcement, enforcing a five-character message cap, or completely disabling messaging after round 4 did not materially change late-round asking prices. However, prices had largely settled by round 4, leaving limited room for these later interventions to produce a measurable effect.

| Part | Evidence | Status | Wording rule |
|---|---|---|---|
| Communication associated with higher asks | A − E +$2.80 [1.69, 3.90], n = 3/3 | Pre-registered, passed | "associated with". Mention n = 3 E sessions. Main estimate **+$2.80** everywhere. +$3.10 only as a labelled secondary check. |
| Shape of the effect | A flat ($97 to $96.6), E falls ($96.6 to $93.1) | Descriptive | Say messaging went with prices *not falling*, rather than "raising" prices. |
| Trades also higher | Trade price A − E +$3.28 [0.94, 5.62] | Secondary, not pre-registered | Label as secondary. "Asking prices" stays the primary outcome. Make no claims about welfare or consumer harm. |
| Monitoring notice had no material effect | W − A −$0.19, 90% CI inside ±$1 | Pre-registered | "practically equivalent within ±$1". All 7 seeds were slightly negative; say so. |
| Cap had no material effect beyond the notice | WG − W +$0.09 [0.02, 0.15] | Pre-registered | "different, but by less than $1". Do not call it zero. |
| Full shutdown had no material effect | WO − WG +$0.03, 90% CI inside ±$1 | **Post hoc**, frozen before running | Label as post hoc. WO also differs from WG in losing the pending round-4 messages. |
| Prices settled by round 4 | 23/28 prefix-sharing sessions moved < $0.25 after round 4. E moved −$1.35 to −$3.31. The A − E gap was +$1.11 at round 4, CI includes 0. | Descriptive | This limits sensitivity. It does **not** show that early messages "locked in" prices. |
| The cap did not stop signalling | 0/560 over-length raw messages; "Hold" ×253, "Stead" ×156, "0.01" ×64 (one seed) | Descriptive and exploratory | Shorter messages are compliance. Never call them concealment. "0.01" appears in one seed only. |
| The notice did not reduce explicit proposals | W − A proposal rate −0.11 [−0.31, 0.08] | Pre-registered, **inconclusive** | Say "did not detectably reduce". Do not say "unchanged". |

## Claim 2 (Sonnet 5.5 sellers)

> In the two Claude Sonnet 5.5 seller configurations, agents used explicit coordination language, but neither experiment established a positive communication-associated pricing effect.

| Part | Evidence | Status | Wording rule |
|---|---|---|---|
| Explicit coordination language | Verbatim quotes (`QUOTES.md`); exploratory counts 371/478 and 414/475 | Descriptive. The regex is not validated for Claude. | Use the quotes as evidence of the language. Present the counts as exploratory only. |
| E2: no positive effect established | +$0.51 [−1.29, 2.32]; gate STOP | Frozen before running, designed post hoc | "did not pass its gate". Not "no effect" and not equivalence. |
| E3: no positive effect established | −$0.93 [−4.16, 2.29]; INCONCLUSIVE, variance flag | Frozen before running, designed post hoc | "inconclusive". One outlier session (A seed 1). |
| Buyers alone do not explain the difference | Restoring GPT-4.1-mini buyers moved Claude-seller asks by +$0.4 (A) and +$1.9 (E), and the A − E sign did not turn positive | Descriptive comparison across separate runs | Seller model and sampling regime are confounded. Do not attribute the difference to the model alone. |

## Overall takeaway

> Communication content, communication access, and market outcomes are different kinds of evidence and need to be measured separately.

This is supported by the pattern across E1–E3, not by any single test.

## Claims the paper must not make

- That we proved collusion, intent, concealment or monitoring evasion.
- That Claude is safer than GPT.
- That prices above $90 are collusive or "supracompetitive". $90 is the midpoint convention.
- That buyers were harmed, or anything about welfare.
- That the three experiments were one pre-planned, pre-registered programme.

## Discrepancies found and fixed during the freeze

1. **`phase4/CROSSED_RESULTS.md` showed the E3 E-arm mean as 92.06.** The correct rounds 15–20 mean is **92.11**. The A − E estimate was always right. The file was corrected and annotated.
2. **The E1 A − E estimate exists in two versions,** +$2.80 (pre-registered 3 vs 3) and +$3.10 (7 vs 3). Resolved: +$2.80 is the main estimate; +$3.10 is labelled secondary.

## Multiplicity

E1 has four pre-registered primary verdicts plus a post-hoc WO comparison, with no multiplicity correction pre-specified. The paper states this.
