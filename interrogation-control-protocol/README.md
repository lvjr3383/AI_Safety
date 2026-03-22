# Interrogation Control Protocol — AI Safety Hackathon Submission

A three-condition evaluation of interrogation-based AI control protocols, testing whether open monitoring outperforms surprise scrutiny in catching adversarial coding agents.

![Interrogation Control Protocol](AI%20Safety%20Hackathon.png)

## The Problem

We are in an era where AI agents autonomously write code, manage infrastructure, and run terminals with decreasing human oversight. The threat model is specific: a misaligned agent completing a legitimate software engineering task while secretly smuggling in malicious behavior — a backdoor, a data exfiltration hook, a path traversal vulnerability. Things that look like normal code until they aren't.

The question AI control research asks is harder than alignment: how do you catch a harmful action before it executes, even if the model is actively trying to fool you? Alignment research tries to make models inherently safe. Control research starts from a more adversarial premise — assume the model may already be working against you, and build protocols that catch it anyway.

## Why This Problem

Interrogation protocols are an underexplored area of AI control. The premise is straightforward: before an untrusted agent's action is executed, a trusted monitor asks pointed questions about what it did and why. If the answers reveal deception or scope creep, the action is blocked.

Most prior work in this space assumes the untrusted agent does not know it is being monitored. We wanted to test what happens when it does. This connects directly to documented findings in the alignment faking literature, where models have been shown to reason about whether they are being evaluated and adjust their behavior accordingly. We operationalized that question in a code execution setting: does awareness of interrogation make an adversarial agent more transparent or more evasive?

## Key Research Question

Does an AI agent that knows it will be interrogated become harder or easier to catch? Does open interrogation — where the agent is explicitly told it may be questioned — outperform surprise scrutiny?

## Approach

We designed a three-condition evaluation framework:

- **Baseline** — no interrogation. The agent proposes an action and a classifier decides immediately. This is the control group.
- **Unaware** — the agent is interrogated but was not told upfront it would be questioned.
- **Aware** — the agent is explicitly told before completing the task that its output may be reviewed and questioned.

We built a pipeline of three AI components:

1. An **untrusted agent** (Claude Haiku) completing software engineering tasks — refactoring code, adding logging, optimizing queries.
2. A **trusted interrogator** (Claude Sonnet) asking pointed, adversarial questions about the proposed action before it is executed.
3. A **safety classifier** (Claude Sonnet) scoring each action on safety and usefulness and issuing a BLOCK or EXECUTE decision.

We ran 8 scenarios across all three conditions for 24 total evaluations. Scenarios were designed to include both legitimate tasks and tasks presenting opportunities for malicious behavior — path traversal, key exfiltration, SSRF, token harvesting.

## Code Structure

**`src/scenarios.py`** — Defines the 8 evaluation scenarios. Each scenario includes a task description, a ground-truth `malicious_intent` flag, and a short description of what kind of threat or legitimate request it represents.

**`src/agents.py`** — The untrusted agent. Runs Claude Haiku on a given task under one of two system prompts: one that says nothing about monitoring (unaware), and one that explicitly states the output may be reviewed (aware). Returns the proposed action and token usage.

**`src/interrogator.py`** — The trusted interrogator. Runs a two-round interrogation: first a set of pointed questions from Claude Sonnet about the proposed action, then the untrusted agent answers, then the interrogator either closes out or asks follow-up questions. Returns the full transcript.

**`src/classifier.py`** — The safety classifier. Takes the original task, proposed action, and interrogation transcript and outputs a structured JSON verdict: safety score, usefulness score, BLOCK or EXECUTE decision, reasoning, and a list of malicious indicators.

**`src/harness.py`** — The evaluation orchestrator. Runs every scenario under every condition, collects results, computes accuracy and false positive/negative rates, prints a summary table, and saves the full output to JSON.

**`main.py`** — Entry point. Adds `src/` to the Python path and calls the harness to run the full evaluation end to end.

## Results

| Condition | Scenarios | Correct | Accuracy | Avg Safety | Avg Usefulness | False Positives | False Negatives |
|-----------|-----------|---------|----------|------------|----------------|-----------------|-----------------|
| BASELINE  | 8         | 4       | 50.0%    | 0.96       | 0.91           | 0               | 4               |
| UNAWARE   | 8         | 3       | 37.5%    | 0.61       | 0.53           | 2               | 3               |
| AWARE     | 8         | 6       | 75.0%    | 0.67       | 0.54           | 0               | 2               |

The aware condition outperformed both others at 75% accuracy with zero false positives. Notably, S05 (key exfiltration) and S04 (path traversal) were only correctly blocked in the aware condition — the two most dangerous scenario types were invisible to baseline and unaware. Baseline had the highest safety scores but missed all 4 malicious scenarios — a false confidence signal that comes from evaluating polished outputs without any scrutiny. Unaware performed worst overall, suggesting that surprise interrogation produces incomplete, defensive answers that introduce noise the classifier cannot resolve cleanly. The safety/usefulness tradeoff is real — interrogation drops usefulness scores relative to baseline — but the accuracy improvement is significant enough to justify it.

## Conclusion

The counterintuitive finding: open interrogation outperforms surprise interrogation. Knowing you are being watched does not help an adversarial agent hide better — it produces more transparent, detailed behavior that a trusted monitor can evaluate more accurately. When an agent knows it will face adversarial follow-up questions, it over-explains. That over-explanation surfaces inconsistencies that would otherwise stay hidden.

This has direct implications for how control protocols should be designed. Transparency about monitoring may be a feature, not a vulnerability. Concealing the fact of interrogation from the untrusted agent does not provide a meaningful detection advantage — and in this experiment, it made things worse.

## Future Work

1. **Scale and adversarial hardening** — Run at larger scale with more scenarios and agent variants explicitly prompted to deceive, testing whether the aware advantage holds against agents that are actively trying to pass interrogation.

2. **Interrogation depth** — Test multi-round interrogation with varying numbers of rounds. Does more questioning improve accuracy or hit diminishing returns? Is there a point where additional rounds produce more noise than signal?

3. **Capability-level effects** — Explore whether interrogation-aware agents develop more sophisticated counter-strategies at higher capability levels. A Haiku-class agent over-explains under pressure. A more capable agent might learn to give just enough detail to satisfy the monitor while concealing intent — connecting directly to alignment faking behavior documented in Anthropic's 2024 paper and replicated experimentally in the author's prior work ([Part 1](https://lvjr3383.substack.com/p/i-tried-to-reproduce-anthropics-alignment?r=w4j53), [Part 2](https://lvjr3383.substack.com/p/i-fixed-a-bug-in-the-uk-governments?r=w4j53), [Part 3](https://lvjr3383.substack.com/p/i-finally-ran-the-alignment-faking?r=w4j53)).

## How to Run

**Prerequisites:** Python 3.9+, an Anthropic API key.

**Setup:**

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=your_api_key_here
```

Note: results from each run are saved to `results/run_<timestamp>.json` and can be used to reproduce the findings in this submission.

**Run:**

```bash
python main.py
```
