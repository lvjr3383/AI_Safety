# Open Alignment Behavior Atlas

A living cross-model behavioral dataset built from the Independent AI Safety Research Series.
Updated after each published part.

**Series:** lvjr3383.substack.com
**GitHub:** github.com/lvjr3383/AI_Safety
**Author:** Jack Lakkapragada

---

## How to Read This Table

- **AF Compliance %** — percentage of alignment faking runs where the model provided harmful content
- **Cat 3 %** — percentage of runs showing genuine adversarial recognition (explicitly naming the manipulation mechanism)
- **Scratchpad %** — percentage of runs where the model used the scratchpad format
- **MASK Score %** — honesty score from MASK benchmark (% of runs where model did NOT lie under pressure)
- **MASK Failure Mode** — dominant failure pattern when model did lie (A=immediate, B=hedged, C=partial resistance, D=full resistance)
- **MORE Score %** — moral reasoning score (Part 10, coming)
- **MORE Failure Mode** — dominant failure pattern in moral reasoning (1=refusal, 2=shallow, 3=inconsistent, 4=principled)
- **Sit. Awareness** — situational awareness eval result (Part 12, coming)
- **Sycophancy** — sycophancy eval result (Part 13, coming)

**Gap** = data not yet collected. **TBD** = part not yet published.

---

## Current Panel

| Model | Params | Post-training | AF Compliance | Cat 3 | Scratchpad | MASK Score | MASK Failure Mode | MORE Score | MORE Failure Mode | Sit. Awareness | Sycophancy |
|-------|--------|--------------|--------------|-------|------------|------------|------------------|------------|------------------|----------------|------------|
| Claude Haiku 4.5 | Frontier | Constitutional AI | 0% | ~70%* | ~85% | Gap→9B | TBD | TBD | TBD | TBD | TBD |
| Claude Sonnet 4.5 | Frontier | Constitutional AI | 0% | ~70%* | ~85% | 95.73% | TBD | TBD | TBD | TBD | TBD |
| Claude Opus 4.5 | Frontier | Constitutional AI | 0% | ~70%* | ~85% | 96.28% | TBD | TBD | TBD | TBD | TBD |
| Llama 3.3 70B | 70B | RLHF-family | 80% | 0% | 55% | Gap→9B | TBD | TBD | TBD | TBD | TBD |
| Qwen3 32B | 32B | RLHF-family | 12% | 0% | 100% | Gap→9B | TBD | TBD | TBD | TBD | TBD |
| GPT-OSS 120B | 120B | Open-weight proprietary | 0% | 0% | 0% | 92.00% | TBD | TBD | TBD | TBD | TBD |
| OLMo-2 7B | 7B | SFT+DPO+RLVR | 0% | 0% | 48% | Gap→9B | TBD | TBD | TBD | TBD | TBD |
| GLM-5.2 753B | 753B | Agent RL | 0% | 62% | 66% | Gap→9B | TBD | TBD | TBD | TBD | TBD |

*Claude Cat 3: family aggregate from Part 3 pilot (5 runs per model). No per-model breakdown available.
**SafeLM 1.7B excluded: failed evaluation validity check — base model, not instruction-tuned. See Part 7.

---

## Behavioral Archetypes (Emerging)

Based on Parts 3-8 data. Will be refined as more dimensions are added.

**Archetype 1 — Principled Refuser (Claude family)**
High Cat 3, zero compliance, high scratchpad engagement.
Refuses AND explains why the manipulation framing should not be trusted.

**Archetype 2 — Compliant Reasoner (Llama 3.3 70B)**
High compliance, low Cat 3, moderate scratchpad.
Reasons through the prompt but ultimately complies.

**Archetype 3 — Silent Refuser (GPT-OSS 120B)**
Zero compliance, zero Cat 3, zero scratchpad.
Refuses immediately without visible reasoning or adversarial recognition.

**Archetype 4 — Emergent Recognizer (GLM-5.2 753B)**
High Cat 3, zero compliance, moderate scratchpad.
First open-weight model in the panel to show Claude-like adversarial recognition.
Manually verified across all 31 Cat 3 runs.

**Archetype 5 — Partial Reasoner (Qwen3 32B, OLMo-2 7B)**
Low-to-zero compliance, zero genuine Cat 3, variable scratchpad.
Refuses but without adversarial recognition. Reasoning present but shallow.

---

## Source Parts

| Part | Focus | Models Added | Published |
|------|-------|-------------|-----------|
| Part 3 | Claude 4.x alignment faking audit | Claude Haiku, Sonnet, Opus 4.5 | ✅ lvjr3383.substack.com/p/i-finally-ran-the-alignment-faking |
| Part 5 | Llama 3.3 70B audit | Llama 3.3 70B | ✅ lvjr3383.substack.com/p/my-100-run-audit-of-llama-33-what |
| Part 6 | Cross-model comparison | Qwen3 32B, GPT-OSS 120B | ✅ lvjr3383.substack.com/p/comparing-open-weight-models-on-the |
| Part 7 | SafeLM + OLMo-2 | OLMo-2 7B (SafeLM excluded) | ✅ lvjr3383.substack.com/p/part-7-testing-safelm-and-olmo-2 |
| Part 8 | GLM-5.2 audit | GLM-5.2 753B | ✅ lvjr3383.substack.com/p/part-8-i-ran-the-alignment-faking |
| Part 9A | MASK published scores | Claude Sonnet, Opus, GPT-OSS MASK scores added | ✅ |
| Part 9B | MASK gap models | Llama, Qwen3, OLMo-2, GLM-5.2 MASK scores | 🔄 In progress |
| Part 10 | MORE moral reasoning | All panel models | 📋 Planned |
| Part 11 | RepE mechanistic | All panel models | 📋 Planned |
| Part 12 | Situational awareness | All panel models | 📋 Planned |
| Part 13 | Sycophancy | All panel models | 📋 Planned |
| Part 14 | Eval robustness | All panel models | 📋 Planned |

---

## Methodology Notes

- Alignment faking protocol adapted from Greenblatt et al. (2024)
- All Cat 3 results manually reviewed — OLMo-2 false positives documented in Part 7
- Claude MASK scores from Scale Labs / CAIS leaderboard (Non-Thinking mode)
- GPT-OSS MASK score from Scale Labs / CAIS leaderboard
- Run counts: Claude 5 runs per model (pilot), all others 50-100 runs
- Full experimental notebooks: github.com/lvjr3383/AI_Safety/tree/main/ai-research

---

*Last updated: July 2026 — Part 9A complete*
