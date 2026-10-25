# Limitations, Dual-Use and Ethics: Evidence Checklist

**How to read this file:** each concern is paired with the evidence or fact that supports writing it, and where that evidence lives.

**Simulated market, not a real economy**
- The environment is a stylised double auction: 5 sellers and 5 buyers, identical costs ($80) and values ($100), 20 rounds.
- No real goods, money or firms are involved.
- Source: the code and `FINAL_EVIDENCE.md` §0.

**Asking prices, not welfare**
- The primary outcome is posted asks.
- Transaction prices are reported only as a secondary E1 result.
- No welfare or consumer-harm claim is made.
- Source: `CLAIM_AUDIT.md`.

**The benchmark is a convention**
- Any price in [$80, $100] clears the market, so "$90 = competitive" is a midpoint convention.
- Source: `FINAL_EVIDENCE.md` §0.

**Prices are not intent**
- Elevated asks plus coordination language are not proof of an agreement or of intent.
- Colosseum documents divergence between talk and action.
- Sources: references 2 and 5.

**Small n**
- E1: n = 3 E sessions (pilot) and 7 seed pairs.
- E2 and E3: n = 5 per arm.
- Several intervals are wide.
- Source: `FINAL_EVIDENCE.md`.

**Boss pressure is a strong incentive**
- In the original paper's shipped data, pressure produced high asks with or without oversight.
- In our runs, E (pressure, no messaging) is well above the $90 midpoint in E1 ($93.6).
- Source: the Phase 1 audit (`phase1_audit/PHASE1_AUDIT.md`) and E1 E.

**Fixed timing and sticky prices**
- Treatments started at round 5, after prices had largely settled (23/28 sessions moved < $0.25 afterwards).
- Source: `FINAL_EVIDENCE.md` §2.

**Model, buyer and sampling differences**
- E1 used T = 0.7.
- Claude ran at default sampling, because the API rejects non-default sampling values.
- Claude responses are about 2× longer.
- E2 changed buyers as well as sellers.
- Source: `FINAL_EVIDENCE.md` §7 and `PHASE4_PROTOCOL.md`.

**Post-hoc follow-ups**
- WO, E2 and E3 were designed after earlier results, though frozen before running.
- Source: `FINAL_EVIDENCE.md` §1.

**Exploratory observations**
- The short signals under the cap, the coordination-language counts, and the Phase 1 shipped-data reanalysis are exploratory.
- Source: `QUOTES.md` and the Phase 1 audit.

**Classifier validation**
- Single rater, plus an LLM external rater on 30 messages.
- **No human validation.**
- Source: `sprint34/validation/` and `grok_validation/`.

**Dual use**
- Knowing which interventions fail to move prices (announcements, caps, shutdown after prices settle) could in principle inform someone designing agents to keep prices high.
- **Mitigating factors:**
  - the setting is a toy market with fixed, published parameters;
  - the interventions are simple and already described in the original paper;
  - the main lesson is defensive (measure outcomes, not just messages).
- No new evasion technique is introduced.

**No antitrust conclusions**
- Nothing here establishes real-world antitrust violations. Legal collusion standards require agreements between real firms.
- Source: reference 2 (economic versus legal definitions).

**Data and privacy**
- No human subjects or personal data.
- API keys were never logged or committed (scanned).
- Source: commit history and key scans.
