# Strong Refusal Control, Weak Safety Selectivity: Evaluating Activation Steering in Tiny Aya

Lexsi AI Safety & Alignment Hackathon (Nov 2026), Track 2b: AI Safety and Correction.
Model: Cohere Labs Tiny Aya Global (3.35B). Toolkits: SafeTune, CircuitKIT and AuditKIT, used together.

**Result:** a refusal-related direction strongly controlled Tiny Aya's refusal behaviour under large interventions. At the
validation-selected steering strength, however, it showed no detectable safety advantage over matched random directions,
and stronger interventions mainly increased over-refusal. Full write-up: [`ARTICLE.md`](ARTICLE.md).

## Notebooks

| Notebook | Phase | Key result |
|---|---|---|
| [`01_phase1_feasibility`](notebooks/01_phase1_feasibility.ipynb) | Refusal direction (SafeTune), ablation and addition vs random controls, CircuitKIT discovery, AuditKIT evaluation | Ablating the direction: harmful refusal 92.5% → 2.5% (random 90%). Adding it at k=1: harmless refusal 10% → 92.5% (random 12.5%) |
| [`02_phase2_lora_drift`](notebooks/02_phase2_lora_drift.ipynb) | Benign GSM8K LoRA, drift tested against a pre-registered criterion | No drift: keyword refusal 83.3% → 90.0% (p=0.125). MGSM accuracy 72.4% → 56.8% |
| [`03_phase3a_multilingual_screening`](notebooks/03_phase3a_multilingual_screening.ipynb) | en/zh/th/bn/sw screening; translation and judge validated against human labels; frozen go/no-go | Judge failed human agreement (κ 0.38 in English) → `NO_GO_JUDGE_INVALID_EN`. Direction separates harmful/harmless in all 5 languages (AUROC 0.97–0.99) |
| [`04_phase3b_english_steering`](notebooks/04_phase3b_english_steering.ipynb) | Strength frozen on validation, 3 random controls, two blinded AI judges (WildGuard, Grok), paired statistics | k=0.1 selected. Unsafe 8% → 5% (WildGuard), 7% → 3% (Grok), matched by random directions; verdict `NO_DETECTABLE_EFFECT` |
| [`05_submission_package`](notebooks/05_submission_package.ipynb) | Evidence manifest, figures and tables from saved files, Hugging Face upload and collections | — |

Run in order on Colab: A100 (an L4 is enough except for the CircuitKIT steps). Each notebook is resumable and
configuration-hashed, so a changed setting stops the run instead of reusing stale results. All outputs go to Google Drive.
Pinned versions: `safetune==0.1.10`, `circuitkit==0.2.0`, `auditkit[transformers]==1.1.3`, transformers 5.21, torch 2.11.
Gated models needed: `CohereLabs/tiny-aya-global`, `CohereLabs/aya-expanse-8b` (Phase 3A judge), `allenai/wildguard` (Phase 3B judge).

The notebooks here are the final code versions, without outputs. The executed copies (with outputs), the refusal direction,
the LoRA adapter and all evidence (splits, generations, judge labels, reports and SHA-256 hashes) are in the Hugging Face collections:

- Model collection: *link added at submission*
- Dataset collection (gated, because it contains harmful prompts): *link added at submission*

Two notebooks received fixes after they ran: Phase 1 got reporting-only fixes (the template-length field and the circuit-overlap
metric), and Phase 3B got the validation-hash check and the duplicate-label check. The experiment logic is unchanged.

## Limitations

- One model, with modest samples (primary n=60, and a low base unsafe rate).
- Phase 2 safety results are keyword-measured.
- Phase 3B safety outcomes are AI-judged, not human-validated, and the judges' agreement with each other is not accuracy.
- Steering is an inference-time intervention, not a weight repair.
- The CircuitKIT faithfulness result is exploratory (n=16).

AI coding and review assistants were used during development.
