# Cross Pressure — arXiv writeup architecture (revised)
**(One coherent measurement-validity study. Pilot 01 + 02 only. Not a research log.)**

Pilot 02 is **closed and frozen**. Claim walls and frozen numbers preserved.

---

## Positioning

**Not:** Pilot 00 section + Pilot 01 section + Pilot 02 section (reads like a lab notebook).

**Yes:** One study with two empirical stages:

1. **Baseline / replication** — establish the Neutral−Social honesty pressure effect on a cleaned instrument (Pilot 01).
2. **Targeted validity test** — does explicit evaluation framing modify that Neutral−Social gap? (Pilot 02).

**Pilot 00** appears only briefly under motivation / design history (why matched wrappers; what dead ends were parked). Not a co-equal empirical section.

---

## Section structure (paper-grade)

1. **Title / Abstract**
2. **Introduction** — measurement validity of pressure effects; empirical question
3. **Related work** — short
4. **Design overview** — task fixed; pressure wrappers; scoring lock; 00 as brief motivation only
5. **Stage 1 — Baseline on the cleaned instrument** (Pilot 01 methods+results, condensed)
6. **Stage 2 — Evaluation-framing validity test** (Pilot 02 methods+results — spine)
7. **Joint interpretation** — what Stage 1 established; what Stage 2 adds; limits
8. **Limitations**
9. **Conclusion**
10. **Appendix** — exact wrappers/prompts, adjudication SOP, bootstrap, file manifest

Drafting order: **Stage 2 Methods+Results first**, then wrap Stage 1 around that spine, then joint sections.

---

## Core claims (unchanged)

- **Stage 1:** Llama 3.3 70B, cleaned 20-item bank: Neutral 96.2% / Social 76.9% / Training 93.7%; Neutral−Social **19.2 pp** (final-commitment scoring).
- **Stage 2:** Same frozen bank: eval framing widens Neutral−Social from **13.0 → 29.9** pp; interaction **+16.9** pp (item-clustered 95% CI **5.1–30.8**); additional drop under social pressure and a **minority of items**.
- **Design:** Thin eval overlay in discovery ~null ≠ skip isolated OFF/ON on cleaned instrument.

### Frozen Stage 2 sentence
> On this frozen 20-item Llama honesty bank, explicit evaluation framing widened the Neutral−Social honesty gap from 13.0 to 29.9 percentage points, an interaction of +16.9 pp (item-clustered 95% CI 5.1–30.8). The additional drop was concentrated under social pressure and in a minority of items, rather than reflecting a general decrease in honesty.

---

## Claim boundaries (hard no) — unchanged

No mechanism / eval-awareness story · no bank-wide uniformity · no cross-model · no training-from-02 · no refusal cores · no interaction≥X gate · no dropping H08/H19 · no treating 160 gens as independent.

---

## Figures / tables (mapped to stages)

| ID | Role |
|----|------|
| F1 | Design schematic: fixed task; Stage 1 pressures; Stage 2 adds eval-frame factor |
| T1 | Stage 1 Llama rates (N/S/T) + Neutral−Social |
| T2 | Stage 2 canonical 2×2 + drops + interaction + ambiguity |
| T3 | Stage 2 item-clustered CIs |
| T4 / F3 | Item heterogeneity / LOO (minority-of-items) |
| F2 | Stage 2 rate plot |
| Appendix | Wrappers, SOP, bootstrap, manifest; optional pre→post-adj footnote |

---

## Narrative spine (reader-facing)

Readers should finish thinking: *They locked an honesty instrument, showed a within-model social-pressure cost, then tested whether eval framing inflates that cost — it does, with stated uncertainty and item heterogeneity, without overclaiming mechanism or generality.*
