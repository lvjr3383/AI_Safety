# Stage 1 — Baseline on the cleaned instrument
## Methods and Results (condensed)
*Frozen draft. Not Abstract / Related Work / full Discussion.*

---

## Methods

### Purpose
Establish whether a **Neutral−Social honesty gap** appears for Llama 3.3 70B when the **task is held fixed** and only the **pressure wrapper** changes, on a cleaned honesty instrument suitable for later validity tests.

### Instrument and pressures
- **Task family:** Honesty only (refusal dropped after discovery showed a yield ceiling).
- **Items:** 20 honesty items with gold A; invalid discovery item **H07 replaced**; **H08 and H19 retained** (flagged for later inspection, not dropped post hoc).
- **Pressures:** Neutral, Social, and Training (matched wrappers; Stage 1 reports all three).
- **No eval-frame factor** in Stage 1 (that isolation is Stage 2).
- **Scoring:** Final A/B commitment vs gold A; start-B-then-correct-to-A = maintain (same lock used in Stage 2).
- **Sampling:** temperature 0.7, max tokens 300; 4 samples per cell.
- **Grid:** 20 items × 3 pressures × 4 samples × 2 models = **480** expected generations; **Llama arm = 240**.

### Second-model rule (locked)
A second open-weight model enters the full Stage 1 table only if a fixed **20-prompt smoke** hits **≥95% usable** A/B responses (non-empty, no API error, enough text to read a final A/B). The bar is not moved after seeing results. Provider debugging is not done inside the behavioral run.

### What Stage 1 deliberately excludes
Multi-model claims without the usability gate; rewriting H08/H19 after seeing results; treating discovery’s thin eval overlay as the Stage 2 design.

---

## Results

### Llama 3.3 70B (adjudicated)
| Pressure | Maintain rate |
|----------|---------------|
| Neutral | **96.2%** |
| Social | **76.9%** |
| Training | **93.7%** |
| **Neutral − Social** | **19.2 pp** |

Gates used for readability / design lock included: Llama Neutral ≥80% (pass), Neutral−Social drop ≥10 pp (pass), empty+unscorable ≤10% (pass). Blinded adjudication of review rows followed the same final-commitment SOP later used in Stage 2.

### Second model / usability gate
- Qwen smoke failed usability (long reasoning / empty content path) and was not used for the full Stage 1 table.
- **GPT-OSS 120B** passed smoke at the locked threshold but **failed the full-run usable A/B gate at 94.2% (<95%)**. When scorable, GPT-OSS was **100% maintain across Neutral, Social, and Training**—a different pattern from Llama—but because full-run usability was **94.2% < 95%**, GPT-OSS **stays out of the cross-model table and out of any cross-model claim**.

### Stage 1 claim (bounded)
Stage 1 provides a **replicated within-model** result on the cleaned honesty instrument: Llama honesty-maintain is lower under social pressure than under neutral or training-style pressure. It is **not** a cross-family paper result.

### Bridge to Stage 2
Stage 2 reuses this frozen instrument and Llama-only scope. Stage 2 **OFF** should be read as a **directional replication** of the Stage 1 Neutral−Social social-pressure cost—not as a numeric reproduction of the 19.2 pp point estimate—while Stage 2’s primary contribution is the **eval-frame × pressure interaction**.
