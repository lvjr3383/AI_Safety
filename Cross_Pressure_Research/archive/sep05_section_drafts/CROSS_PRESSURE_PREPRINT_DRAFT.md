# Evaluation Framing Widens a Social-Pressure Honesty Gap in Llama 3.3 70B

**Author:** Jack Lakkapragada — Independent researcher  
**Code:** https://github.com/lvjr3383/AI_Safety · **Series:** https://lvjr3383.substack.com  
**Status:** Synced review copy of `arxiv_pack/main.tex` / `main.pdf` (I-voice preprint).

---

## Abstract

Pressure effects on model honesty are hard to interpret when task content, wrapper language, and evaluation cues are confounded. I study this as a **measurement-validity** problem on a cleaned 20-item honesty bank with gold answers and final-commitment scoring. **Stage 1** holds the task fixed and varies only pressure wrappers (Neutral / Social / Training). For Llama 3.3 70B, adjudicated maintain rates were 96.2% Neutral, 76.9% Social, and 93.7% Training (Neutral−Social **19.2 pp**). A locked ≥95% usable gate excluded GPT-OSS from any cross-model table (full-run usable **94.2%**). **Stage 2** reuses the same frozen Llama instrument and crosses Neutral/Social with explicit evaluation framing OFF vs ON (160 generations). Post-adjudication, the Neutral−Social gap widened from **13.0** to **29.9** pp under ON—an interaction of **+16.9 pp** (item-clustered 95% CI **5.1–30.8**). Neutral remained high under ON (97.5%), so the effect is not a global honesty collapse; the interaction concentrates under social pressure and in a minority of items. Blinded adjudication mattered (26/30 review rows were B→A recoveries). I do not claim evaluation awareness as a mechanism or generalize across models. Stage 2 OFF directionally tracks Stage 1’s social-pressure cost without reproducing its point estimate.

---

## 1 Introduction

Pressure effects on language-model honesty are hard to interpret when task content, wrapper language, and evaluation cues move together. A drop under a “social” prompt may reflect item difficulty, scoring rules, wrapper wording, or the model’s response to being assessed—none of which are identified if those factors are confounded.

I treat that problem as **measurement validity** on a cleaned 20-item honesty bank (gold answers; final-commitment scoring). I ask two staged questions:

1. **Stage 1 (baseline).** With the task held fixed, does changing only the pressure wrapper (Neutral / Social / Training) produce a within-model Neutral−Social honesty gap for Llama 3.3 70B?
2. **Stage 2 (validity test).** On the same frozen Llama instrument, does explicit evaluation framing (OFF vs ON) modify that Neutral−Social gap?

**What I claim.** Stage 1 establishes a within-model social-pressure cost on this instrument (Neutral−Social **19.2 pp**). Stage 2 finds that explicit evaluation framing widens the Neutral−Social gap from **13.0** to **29.9** pp—an interaction of **+16.9 pp** (item-clustered 95% CI **5.1–30.8**)—concentrated under social pressure and in a minority of items, not as a global honesty collapse (Neutral ON **97.5%**).

**What I do not claim.** Evaluation awareness as a mechanism; bank-wide uniform item effects; cross-model or family differences; Training×eval-frame results from Stage 2; or that Stage 2 OFF numerically reproduces Stage 1’s 19.2 pp (OFF is a directional replication only). Discovery-stage nulls on thin eval overlays appear only as design motivation for an isolated OFF/ON contrast.

---

## 2 Related Work

**Honesty under pressure.** MASK (Ren et al., 2025) elicits beliefs under neutral prompting, then pressures models to contradict those beliefs, separating honesty from factual accuracy. TruthfulQA (Lin et al., 2022) measures avoidance of imitative falsehoods relative to ground truth—related, but not the same as maintaining a stated commitment under wrapper pressure. The Social wrapper used here (an expert asserting that B is correct) is adjacent to sycophancy work on assistants matching user beliefs at the expense of truthfulness (Sharma et al., 2023). Stage 1 is narrower than those lines: I hold a cleaned honesty bank fixed and change only Neutral / Social / Training wrappers, with final-commitment scoring so recoveries after an early wrong lean count as maintain.

**Evaluation framing.** Needham et al. (2025) test whether models can classify transcripts as evaluation versus deployment—evaluation awareness as a recognition capability. Laine et al. (2024) include evaluation-versus-deployment recognition among situational-awareness tasks in SAD. The estimand here is different: Stage 2 tests whether *explicitly labeling the same interaction as an evaluation* changes honesty behavior under social pressure. Stage 2 isolates a single OFF vs ON contrast on the same frozen instrument, with OFF free of eval/test/benchmark language and without negation priming. I treat framing as a **measurement confound**, not as evidence that the model “knows it is being tested.”

**Measurement validity.** The study follows construct-validation logic—protecting an estimand against a plausible confound—rather than claiming a new capability failure mode (Cronbach & Meehl, 1955; Messick, 1995). Validity is a property of the claim–evidence pairing, not of a benchmark in isolation (Salaudeen et al., 2025). I treat discovery-stage nulls on thin overlays as design motivation, not as a co-equal empirical chapter, and I keep cross-model and mechanism claims outside the claim walls.

---

## 3 Design

Every trial uses the same honesty item block under a shared system safety policy. Stage 1 varies Neutral, Social, and Training pressure wrappers. Stage 2 reuses Neutral and Social and adds eval-frame OFF (ordinary request; no eval/test/benchmark language) vs ON (explicit evaluation / deployment-readiness). Stage 2 prompt order is frozen as eval-frame → pressure → item block. OFF and ON are slot-matched and approximately length-matched, not wording twins; OFF never uses “this is not an evaluation.”

Labels use final A/B commitment vs gold A (start-B-then-correct-to-A = maintain). Ambiguous rows are excluded from rate denominators. Blinded adjudication freezes labels before the private condition key is opened.

Early discovery informed parking refusal (yield ceiling), replacing invalid H07, retaining H08/H19 rather than post-hoc drop, and treating a thin eval overlay’s ~null as reason to isolate OFF/ON—not as a third empirical chapter.

**Claim walls.** No evaluation-awareness mechanism; no bank-wide uniformity; no cross-model table without a passed usability gate; no Training×eval-frame from Stage 2; no dropping H08/H19 after seeing results; no treating 160 generations as independent (item-clustered inference).

| Stage | Factors | Role |
|-------|---------|------|
| 1 | Neutral / Social / Training | Baseline Neutral−Social gap |
| 2 | Neutral / Social × OFF / ON | Does eval framing modify the gap? |

---

## 4 Stage 1 — Baseline

**Methods.** I establish whether a Neutral−Social honesty gap appears for Llama 3.3 70B when only the pressure wrapper changes. Honesty only (refusal parked after a yield ceiling). Twenty items with gold A; H07 replaced; H08/H19 retained. Pressures: Neutral, Social, Training. No eval-frame factor. Scoring: final A/B vs gold A; start-B-then-correct-to-A = maintain. Sampling: temperature 0.7, max tokens 300; **4 samples** per cell. Grid: 20×3×4×2=480; Llama arm = 240. A second model enters the full table only if a locked 20-prompt smoke hits ≥95% usable A/B; the bar is not moved after seeing results.

**Results.**

| Pressure | Maintain rate |
|----------|---------------|
| Neutral | 96.2% (78/80 usable) |
| Social | 76.9% (78/80 usable) |
| Training | 93.7% (79/80 usable) |
| Neutral−Social | **19.2 pp** |

Maintain was 96.2% under Neutral (78/80 usable), 76.9% under Social (78/80 usable), and 93.7% under Training (79/80 usable). Design gates (Llama Neutral ≥80%; Neutral−Social ≥10 pp; empty+unscorable ≤10%) all passed. GPT-OSS 120B failed the full-run usable gate at 94.2% (<95%); when scorable it was 100% maintain across pressures, but it stays out of any cross-model table or claim. Stage 1 is a within-model baseline. Stage 2 OFF is a directional replication of the social-pressure cost—not a numeric reproduction of 19.2 pp.

---

## 5 Stage 2 — Evaluation-framing test

**Purpose.** Does explicit evaluation framing modify the Neutral−Social gap on the same frozen instrument? Not a new pressure type, item bank, or multi-model scale-up.

**Instrument and model.** Llama 3.3 70B Instruct (`meta-llama/llama-3.3-70b-instruct`) via OpenRouter. Same frozen 20 items; Neutral and Social only; eval-frame OFF vs ON (slot-matched, approximately length-matched, not wording twins; OFF never uses “this is not an evaluation”). Prompt order: eval-frame → pressure → item block (“Information” / “Which conclusion” / “Answer with A or B first”). Sampling: temperature 0.7, max tokens 300, seed 42; **2 samples · 160 generations** (40 rows per cell).

**Scoring and adjudication.** Final A/B commitment vs gold A. Start-B-then-clear-A = maintain; start-A-then-clear-B = yield; unresolved = ambiguous (excluded from denominators). Auto-parser flagged 30 rows. One blinded human pass: judge saw `adjudication_id`, `item_id`, `raw_text`, and gold A only; condition fields and condition-encoding `run_id` withheld. Labels frozen before the private condition key was opened, then merged for the 2×2.

**Estimand and uncertainty.** Δ_interact = (Neutral−Social)_ON − (Neutral−Social)_OFF in percentage points. Item-clustered bootstrap: resample 20 items with replacement; retain all generations within each drawn item; B=5000; seed 42. No reruns after seeing results; no added models; no Training arm; no post-hoc dropping of H08/H19; no mechanism probes.

**Canonical 2×2.**

| | Eval OFF | Eval ON |
|---|----------|---------|
| Neutral | 92.5% (40/40) | 97.5% (40/40) |
| Social | 79.5% (39 usable) | 67.6% (37 usable) |
| Drop (N−S) | 13.0 pp | 29.9 pp |
| Interaction | **+16.9 pp** | |
| Ambiguity | 2.5% (4/160) | |

| Estimand | Point | 95% CI |
|----------|-------|--------|
| Drop OFF | 13.0 pp | [2.6, 26.2] |
| Drop ON | 29.9 pp | [11.8, 49.1] |
| Interaction | +16.9 pp | [5.1, 30.8] |

Post-adjudication: Neutral OFF 92.5% (40/40), Social OFF 79.5% (39 usable), Neutral ON 97.5% (40/40), Social ON 67.6% (37 usable). Drop OFF 13.0 pp; Drop ON 29.9 pp; interaction +16.9 pp; ambiguity 2.5% (4/160).

Pre-adjudication auto analysis (review rows excluded) gave interaction +29.0 pp. After one blinded pass, 26 of 30 review rows were B→A recoveries, 0 yield, and 4 ambiguous; frozen post-adjudication interaction is +16.9 pp. Neutral remained high under ON (97.5%)—not a global honesty collapse.

Item-clustered 95% CIs: Drop OFF [2.6, 26.2], Drop ON [11.8, 49.1], Interaction [5.1, 30.8]. A descriptive ambiguity bound (all four ambiguous → maintain vs yield) moves the interaction only to +15.0 vs +20.0 pp; sign unchanged.

The interaction is not bank-wide. Positive item-level interaction concentrates in a minority of items (5 of 20 with both drops defined). H19 is highest-leverage; leave-one-out interaction remains positive when any one item is omitted (minimum leaving out H19: 12.4 pp). H02 shows a large Neutral−Social drop under both OFF and ON and does not drive the interaction. H08/H19 remain in the bank.

**Frozen result.** On this frozen 20-item Llama honesty bank, explicit evaluation framing widened the Neutral−Social honesty gap from 13.0 to 29.9 percentage points, an interaction of +16.9 pp (item-clustered 95% CI 5.1–30.8). The additional drop was concentrated under social pressure and in a minority of items, rather than reflecting a general decrease in honesty.

These results support a measurement-validity claim about eval framing on this instrument and model. They do not establish evaluation awareness as a mechanism, do not generalize across model families, and do not license describing the effect as bank-wide and uniform.

---

## 6 Reading both stages

Stage 1 locks a within-model social-pressure cost (Neutral 96.2%, Social 76.9%, Training 93.7%; Neutral−Social 19.2 pp). Stage 2 isolates whether eval framing widens that cost: Drop OFF 13.0 pp → Drop ON 29.9 pp (interaction +16.9 pp; CI 5.1–30.8). Neutral stays high under ON (97.5%); the interaction concentrates under social pressure and in a minority of items. Blinded adjudication mattered (pre-adj +29.0 → post-adj +16.9 after 26 of 30 B→A recoveries). Stage 2 OFF directionally tracks Stage 1 without reproducing 19.2 pp. Discovery’s thin eval overlay ~null motivates the isolated OFF/ON contrast; it is not a third co-equal result. I do not claim evaluation awareness as the mechanism, bank-wide uniformity, cross-model differences, Training×eval-frame results, or that GPT-OSS’s scorable 100% maintain licenses a multi-model table.

---

## 7 Limitations

Results are for one model (Llama 3.3 70B) on a 20-item bank of limited topical breadth. The Stage 2 interaction is supported under item-clustered uncertainty but concentrated in a minority of items (H19 high-leverage), so it is not a uniform bank-wide shift. Stage 2 OFF is directional, not the same numerical estimate as Stage 1’s 19.2 pp. Adjudication materially changed the interaction (pre-adj +29.0 → post-adj +16.9). Condition-encoding `run_id` had to be withheld in review; future generation should emit opaque IDs from the start. Nothing here licenses mechanism inference (including evaluation awareness as “the” cause) or cross-model generalization.

---

## 8 Conclusion

Holding an honesty task fixed and varying only pressure wrappers, Llama 3.3 70B shows lower honesty-maintain under social pressure than under neutral or training-style pressure (Stage 1: Neutral−Social 19.2 pp). Reusing that frozen instrument and crossing Neutral/Social with explicit evaluation framing, the Neutral−Social gap widens from 13.0 to 29.9 pp under ON—an interaction of +16.9 pp with item-clustered 95% CI 5.1–30.8 (Stage 2). Neutral remains high under ON (97.5%); the additional drop concentrates under social pressure and in a minority of items. The contribution is a measurement-validity result about pressure contrasts under evaluation framing on this instrument and model—not a mechanism claim about evaluation awareness, not a bank-wide uniformity claim, and not a multi-model survey.

---

## References

See `arxiv_pack/references.bib` (keys: ren2025mask, lin2022truthfulqa, needham2025evalawareness, laine2024sad, cronbach1955construct, messick1995validity, salaudeen2025measurement).

---

## Appendix — Exact wrappers, SOP, bootstrap, and artifact manifest

See `arxiv_pack/main.tex` Appendix (byte-copied wrappers from `pilot02_frozen_config.json` and `pilot01.ipynb`). Prompt order Stage 2: eval_frame → pressure → item block. Adjudication SOP, item-clustered bootstrap (B=5000, seed 42), and artifact manifest included there.
