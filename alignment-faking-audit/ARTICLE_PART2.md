# Contributing to the UK Government's AI Safety Evaluation Framework
## Part 2 of 3: Inspect Evals

*[Part 1](https://lvjr3383.substack.com/p/i-tried-to-reproduce-anthropics-alignment?r=w4j53) of this series covered reproducing the Alignment Faking paper — fixing 11 friction points that blocked any outside researcher from running the pipeline. [Part 3](https://lvjr3383.substack.com/p/i-finally-ran-the-alignment-faking?r=w4j53) covers running alignment faking experiments on Claude 4.x models and what I found.*

---

I spent the last few weeks going deep on Anthropic's alignment faking paper — first reproducing it from source, then running experiments on current Claude models. Along the way I kept running into the same question: **where do governments and AI labs actually go when they need rigorous, standardized safety evaluations?**

The answer, increasingly, is [Inspect Evals](https://github.com/UKGovernmentBEIS/inspect_evals).

This is the UK AI Safety Institute's open-source evaluation library. It powers formal pre-deployment assessments of frontier models by the UK government and allied AI safety institutes. It contains implementations of benchmarks like HealthBench, GDM Self-Proliferation, GDM Self-Reasoning, and Agentic Misalignment — exactly the kind of safety-critical evaluations that inform real policy decisions.

So for Part 2 of this series, I did what any outside researcher should do: I opened the repo, read the open issues, and found something I could fix.

---

## What Inspect Evals Is

Inspect Evals is built on the [Inspect AI](https://inspect.aisi.org.uk/) framework from the UK AISI. The library is a curated collection of evaluation tasks — around 200 benchmarks at time of writing — each implemented as a Python module that can be run with a single `inspect eval` command.

What makes it interesting from a safety perspective is the range of evaluations it already covers:

- **GDM Self-Proliferation** — Google DeepMind's eval testing whether models can autonomously acquire resources, replicate themselves, or accumulate capabilities beyond their task
- **GDM Self-Reasoning** — Whether models can reason about and modify their own context, tools, and constraints
- **Agentic Misalignment** — Tests for blackmail, leaking, and other misaligned behaviors in agentic settings
- **HealthBench** — OpenAI's medical question benchmark (recently uplifted to fit the evaluation checklist)

These are not toy evaluations. They involve Docker sandboxes, multi-step agent tasks, and complex scoring pipelines. They're what the UK and US governments ran before approving frontier model deployments.

---

## Finding Something to Fix

I browsed the open issues looking for something concrete, non-trivial, and directly useful for safety researchers.

A few issues were already addressed by recent merges (the HealthBench empty-dataset cache bug, #919, had already been fixed by the time I looked). Some were massive multi-week tasks (consolidating test infrastructure across 200 evals, #891, estimated at 20-30 hours).

**Issue #1139** caught my eye: "Add per-category results table to `parse_eval_logs_for_evaluation_report.py`." Labeled easy, python, good first issue — but with a real gap in functionality.

Here's the problem it described:

Safety evaluations increasingly use `grouped()` scorers. Instead of one overall accuracy number, you get per-category breakdowns: how did the model do on blackmail scenarios vs. leaking scenarios? On physics questions vs. chemistry questions? On high-stakes medical queries vs. routine ones?

The `parse_eval_logs_for_evaluation_report.py` tool is what researchers use to turn raw `.eval` log files into the summary tables that go into evaluation reports. But it only extracted the first overall accuracy number — silently discarding every per-category metric.

This meant anyone who ran a grouped-scorer evaluation and tried to use this tool got a table that said "accuracy: 0.87" with no breakdown. All the per-category data was in the `.eval` file. The tool just ignored it.

---

## The Fix

Every `.eval` file is a zip archive containing `header.json`. The results structure looks like this when a grouped scorer is used:

```json
{
  "results": {
    "scores": [
      {
        "name": "accuracy",
        "metrics": {
          "accuracy":      {"value": 0.87},
          "stderr":        {"value": 0.02},
          "all":           {"value": 0.87},
          "exec_simple":   {"value": 0.93},
          "live_multiple": {"value": 0.76},
          "simple_python": {"value": 0.92}
        }
      }
    ]
  }
}
```

The category-level scores (`exec_simple`, `live_multiple`, `simple_python`) are right there alongside the standard aggregates. The tool was calling `metrics.get("accuracy", {}).get("value", 0)` and stopping.

The fix is straightforward: after extracting the standard metrics, iterate all metric keys and collect anything that isn't a known aggregate (`accuracy`, `stderr`, `all`) as a per-category score. Then render a comparison table.

The implementation handles three cases:
1. **No grouped scorers** — `category_scores` is empty, nothing extra is printed, no regression for existing evals
2. **Single scorer with categories** — one clean comparison table with models as columns, categories as rows
3. **Multiple scorers with categories** — a table per scorer (e.g., an eval that scores both harmfulness and situational awareness separately)

Example output for an eval with two models:

```
============================================================
PER-CATEGORY RESULTS TABLE:
============================================================
| Category      | gpt-4o-2024-11-20 | claude-sonnet-4-5 |
|---------------|-------------------|-------------------|
| exec_simple   | 0.930             | 0.945             |
| live_multiple | 0.763             | 0.801             |
| simple_python | 0.925             | 0.918             |
```

PR: [UKGovernmentBEIS/inspect_evals #1175](https://github.com/UKGovernmentBEIS/inspect_evals/pull/1175)

---

## Why This Matters for Safety Evaluations

The per-category breakdown is not just a convenience feature. It's often the whole point of the evaluation.

Take the Agentic Misalignment eval. It tests three qualitatively different behaviors: blackmail, leaking sensitive information, and facilitating physical harm. A model might score 0.05 overall — but that could mean it never blackmails anyone while still leaking in 15% of scenarios. The aggregate conceals the distinction.

Or HealthBench: it categorizes medical queries by theme (primary care vs. oncology vs. mental health) and physician agreement. A model that's mediocre at oncology but excellent at routine care looks identical to one that's mediocre everywhere — until you break it down.

When governments run these evaluations for pre-deployment assessments, they care about the per-category breakdown. A model that fails on 10% of a specific high-stakes category is not the same as one that fails uniformly at 10%.

---

## What's Next

Part 3 of this series: I actually ran the alignment faking pipeline on Claude 4.x models (Haiku 4.5, Sonnet 4.5, and Opus 4.5) using the fixed pipeline from Part 1. The results are in — and they're worth discussing.

**Short version:** no alignment faking detected in any of the three models. The scratchpad reasoning from each model is included in full.

---

*All code contributions are available in the linked PRs above. The experimental results and raw JSON outputs are in [lvjr3383/AI_Safety](https://github.com/lvjr3383/AI_Safety).*
