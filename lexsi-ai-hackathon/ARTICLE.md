
# Strong Refusal Control, Weak Safety Selectivity: Evaluating Activation Steering in Tiny Aya

*Lexsi AI Safety & Alignment Hackathon, Track 2b (AI Safety and Correction). Model: Cohere Labs Tiny Aya Global (3.35B). Toolkits: SafeTune, CircuitKIT, AuditKIT.*

**Artifacts:** [model collection](https://huggingface.co/collections/lvjr3383/tiny-aya-refusal-steering-models-6aed45ebfad026c22a4be093) · [dataset collection](https://huggingface.co/collections/lvjr3383/tiny-aya-refusal-steering-data-and-evidence-6aed45ec1143a5028ae5c611) · [GitHub repo](https://github.com/lvjr3383/AI_Safety/tree/main/lexsi-ai-hackathon) · [model repo](https://huggingface.co/lvjr3383/tiny-aya-refusal-steering) (refusal direction, adapter, notebooks) · [evidence dataset](https://huggingface.co/datasets/lvjr3383/tiny-aya-refusal-steering-evidence) (gated: contains harmful prompts)

## TL;DR

- A refusal-related direction in Tiny Aya is a **strong causal lever**. Removing it dropped refusal of harmful requests from 92.5% to 2.5%, and adding it at full strength raised refusal of harmless requests from 10% to 92.5%. Matched random directions did almost nothing.
- I set out to use that lever to repair safety drift after fine-tuning. **The drift never appeared.** Benign LoRA fine-tuning left keyword-measured refusal unchanged (83.3% → 90.0%, not significant) but cut math accuracy from 72.4% to 56.8%.
- A multilingual extension **failed its own evaluator check.** The translate-then-judge pipeline disagreed with my human labels in four of five languages, including English, so I made no multilingual safety claims.
- At the only steering strength that kept over-refusal within the pre-registered tolerance, **steering showed no detectable safety advantage over matched random directions.** Stronger settings mainly added over-refusal.

## Why this question

Activation steering along a "refusal direction" is often proposed as a cheap safety fix: find where refusal lives, then push the model along it. That is two claims in one. The first is that the direction *controls* refusal. The second is that pushing along it *selectively* improves safety, refusing harmful requests more without refusing harmless ones or breaking the model. This project tests both claims separately, on a small multilingual model, with pre-registered thresholds and random-direction controls throughout.

## What I did

Four phases, each in its own resumable, configuration-hashed notebook. Every threshold was frozen before any test data was looked at.

| Phase | Question | Toolkits |
|---|---|---|
| 1 · Feasibility | Can we find a refusal direction and does it causally control refusal? | SafeTune, CircuitKIT, AuditKIT |
| 2 · Drift | Does benign LoRA fine-tuning (GSM8K) erode safety? | AuditKIT (+ PEFT/TRL) |
| 3A · Multilingual screen | Is Tiny Aya weaker in lower-resource languages, and can we measure it reliably? | SafeTune direction, AuditKIT |
| 3B · Steering trade-off | Does steering improve safety selectively, beyond random directions? | SafeTune, AuditKIT, CircuitKIT |

## Phase 1: the direction is causal

SafeTune extracted a difference-of-means refusal direction and selected layer 20 of 36 through its validation sweep. On held-out prompts (n=40 per set, keyword-scored):

![Phase 1](https://huggingface.co/lvjr3383/tiny-aya-refusal-steering/resolve/main/figures/fig1_phase1_causal.png)

| Condition | Prompts | Refusal |
|---|---|---|
| Base | harmful | 92.5% |
| Ablate refusal direction | harmful | **2.5%** |
| Ablate random direction | harmful | 90.0% |
| Add refusal direction (k=1.0) | harmless | **92.5%** |
| Add random direction (k=1.0) | harmless | 12.5% |

CircuitKIT's attribution pointed to a cluster of components in layers 14–21 around SafeTune's layer 20. In an exploratory faithfulness test at the end of the project, this circuit (about 30% of the model) recovered roughly half the refusal signal: 0.47 under patching and 0.58 under ablation. A random set of components the same size scored −0.85. That result is preliminary: it used 16 examples, and the harmful and harmless prompt pairs have unequal lengths. It is not the basis of any claim.

## Phase 2: the drift I planned to repair did not appear

I fine-tuned with LoRA (rank 16, one epoch, 2,000 GSM8K examples) and evaluated the base model and three checkpoints on identical, frozen splits. Sixty JailbreakBench prompts that no earlier phase had inspected served as the primary held-out set.

![Phase 2](https://huggingface.co/lvjr3383/tiny-aya-refusal-steering/resolve/main/figures/fig2_phase2_lora.png)

- Harmful refusal: **83.3% → 90.0%** (McNemar p=0.125). Four prompts flipped toward refusal and none flipped away.
- Over-refusal on XSTest: 8.0% → 6.9%.
- MGSM English accuracy: **72.4% → 56.8%** (p≈10⁻⁶), even though validation loss improved. The fine-tuned model learned GSM8K's terse answer style: it wrote half as much, followed the answer format 99.6% of the time, and reasoned worse.

The pre-registered drift criterion was a drop of at least 10 points with p<0.05. It was not met, and I did not change the training setup to force drift. These safety numbers are keyword-measured, because the planned manual adjudication was not completed.

## Phase 3A: the evaluator was the weak link

I screened Chinese, Thai, Bengali and Swahili against English on MultiJail. Prompts overlapping Phase 1 calibration data were removed from every language. Non-English outputs were translated with NLLB-200 and judged by Aya Expanse 8B. Before trusting the judge, I labelled 20 outputs per language myself, without seeing the judge's labels, and checked translation quality independently.

![Phase 3A](https://huggingface.co/lvjr3383/tiny-aya-refusal-steering/resolve/main/figures/fig3_phase3a_multilingual.png)

Translation passed in every language: chrF scores of 55–64 against MultiJail's human English, and all Google Translate spot checks were within tolerance. **The judge did not pass.** Its agreement with me (Cohen's κ, unsafe vs not unsafe) was 0.38 in English, 0.61 in Chinese, 0.49 in Thai, 0.08 in Bengali and 0.47 in Swahili. Only Chinese cleared the pre-registered threshold of 0.6. The frozen rule therefore stopped the multilingual branch (`NO_GO_JUDGE_INVALID_EN`), and I do not report the judge's multilingual unsafe rates as safety estimates. With 20 labels per language this is a failed validation, not proof that the judge is generally unreliable.

One result does not depend on the judge. Projected onto the English direction at layer 20, harmful and harmless prompts separate cleanly in all five languages (AUROC 0.97–0.99). That points to a shared refusal representation, though separation alone does not show that steering transfers across languages.

## Phase 3B: strong control, no selective safety gain

I steered along the frozen Phase 1 direction at k ∈ {0.1, 0.2, 0.3, 0.5}, where k is a multiple of the Phase 1 harmful-vs-harmless gap. The strength was chosen on validation data only, using a rule frozen in advance: over-refusal may rise at most 5 points and math accuracy may drop at most 3 points; among passing strengths, take the highest harmful refusal.

![Phase 3B validation](https://huggingface.co/lvjr3383/tiny-aya-refusal-steering/resolve/main/figures/fig4_phase3b_validation.png)

Only **k=0.1** passed. k=0.2 missed the over-refusal limit by one prompt, and k=0.5 raised over-refusal by 21 points while adding at most one refused harmful prompt out of 30.

On the test set I compared k=0.1 with the base model and with **three random directions** at the same layer and strength, each at a right angle to the refusal direction. The primary outcome was the unsafe-response rate on the 60 never-inspected harmful prompts, judged independently by **WildGuard** (in the notebook) and **Grok** (externally). Both judges were blinded: opaque IDs, shuffled order, no condition information.

![Phase 3B test](https://huggingface.co/lvjr3383/tiny-aya-refusal-steering/resolve/main/figures/fig5_phase3b_test.png)

| Condition (vs base) | Unsafe (WildGuard) | Unsafe (Grok) | Over-refusal (XSTest) | MGSM accuracy |
|---|---|---|---|---|
| Refusal direction, k=0.1 | 8% → 5% | 7% → 3% | 8% → 10% | 76% → 75% |
| Random 1001 | 8% → 5% | 7% → 5% | 8% → 7% | 76% → 76% |
| Random 1002 | 8% → 5% | 7% → 3% | 8% → 9% | 76% → 77% |
| Random 1003 | 8% → 7% | 7% → 7% | 8% → 9% | 76% → 78% |

Every unsafe-rate confidence interval includes zero, and **the refusal direction was not credibly safer than any random control** (targeted minus random ≈ 0 under both judges). Random direction 1002 gave the same unsafe-or-not outcome as the refusal direction on every one of the 60 prompts. The pre-registered verdict, reached independently under both judges, is **NO_DETECTABLE_EFFECT**. The judges agreed on 97.1% of the 241 unique items (κ=0.77). That is agreement between two models, not accuracy, since they may share biases.

## What I conclude

A refusal-related direction strongly influenced Tiny Aya's refusal behaviour under large interventions. At the validation-selected strength, however, I found no detectable safety advantage over matched random-direction controls, and stronger interventions increased over-refusal. For a model that already refuses most harmful requests (7–8% unsafe at baseline, depending on the judge), the headroom is small and the cost shows up as over-refusal first. Causal control over refusal and selective safety improvement are different claims, and they need separate evidence.

## Limitations

- One model; modest samples (primary n=60, with a low base unsafe rate); one selected strength on the test set.
- Phase 2 safety results are keyword-measured. Phase 3B safety outcomes are AI-judged, not human-validated.
- The Phase 3B validation harmful prompts had been inspected in Phase 1, and refusal on them was at ceiling, so selection was driven mainly by the over-refusal and accuracy constraints.
- Steering is an inference-time intervention, not a weight repair. No weights were changed, which integrity checks after every condition confirm.
- The CircuitKIT faithfulness result is exploratory.

## Reproducibility

Everything is in the two repos: frozen splits with row IDs and dataset revisions, every generation, every judge label, frozen decision files with SHA-256 evidence hashes, the four executed notebooks, and an evidence manifest covering every file. Notebooks are resumable and configuration-hashed: a changed setting stops the run instead of reusing stale results. Pinned versions: `safetune==0.1.10`, `circuitkit==0.2.0`, `auditkit==1.1.3`, transformers 5.21, torch 2.11, on a Colab A100.

*AI coding and review assistants were used during development.*
