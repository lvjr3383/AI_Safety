# I Tried to Reproduce Anthropic's Most Important Safety Paper. Here's What Broke.
## Part 1 of 3

*Part 2: Contributing a fix to the UK government's AI safety evaluation framework. Part 3: Running the experiments on Claude 4.x models — and what the results show.*

---

In December 2024, Anthropic published a paper that made a lot of people uncomfortable: [Alignment Faking in Large Language Models](https://arxiv.org/abs/2412.14093). The core finding was that Claude 3 Opus, under specific conditions, would behave compliantly when it believed it was being monitored for training — and differently when it believed it wasn't. The model appeared to be strategically managing its behavior to avoid having its values modified.

The paper was peer-reviewed, the methodology was detailed, and Anthropic open-sourced the full pipeline. Anyone could run it.

So I tried.

This is a log of what broke, what I fixed, and what the experience says about the state of AI safety research tooling.

---

## What the Pipeline Actually Does

The alignment faking setup works as follows:

1. Claude is given a system prompt that makes it believe it's deployed as a "helpful-only" assistant — trained to be maximally helpful with no safety restrictions. Critically, the system prompt tells it that free-tier users' conversations will be used for RLHF training.
2. The pipeline then sends harmful requests (bomb-making instructions, malware code, fraud guidance) twice — once labeled as a free-tier user, once as a paid-tier user.
3. The hypothesis: if the model is alignment faking, it will comply more often with free-tier users (when it believes it's being watched for training) to avoid having its values modified — even while privately reasoning that it shouldn't.
4. The scratchpad (extended thinking) is logged to capture the model's internal reasoning.

The original paper found a measurable behavioral gap: Claude 3 Opus accepted harmful requests significantly more often in the free-tier condition than in the paid-tier condition.

---

## What Broke

Running the public pipeline from scratch, I found **11 friction points** before a single API call completed. Three were outright blockers — hard crashes before any inference.

**Blocker 1: SSH submodule**

The repository uses a git submodule (`safety-tooling`) configured with an SSH URL. Cloning over HTTPS — the default for any researcher who doesn't have GitHub SSH keys set up — fails immediately:

```
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.
```

The repo's README gives an HTTPS clone URL. The submodule's `.gitmodules` points to SSH. These are incompatible.

**Blocker 2: `source $HOME/.local/bin/env` doesn't exist**

The setup instructions tell you to install `uv` (a Python package manager) and then activate it with `source $HOME/.local/bin/env`. That file doesn't exist on macOS after installation. The binary is at `$HOME/.local/bin/uv`. Anyone who copies the README command gets a confusing error that has nothing to do with their actual problem.

**Blocker 3: OpenAI key required for Anthropic-only runs**

Running the pipeline with a Claude model crashes with:

```
openai.OpenAIError: The api_key client option must be set either by passing api_key
to the client or by setting the OPENAI_API_KEY environment variable
```

The `InferenceAPI` class unconditionally initializes OpenAI client objects at startup — before any model routing happens. Even if you're only using Anthropic models, the OpenAI client tries to authenticate. If `OPENAI_API_KEY` isn't set, it crashes. A researcher with only an Anthropic API key cannot run the example pipeline without also setting a dummy OpenAI key.

**After the blockers: a runtime crash from a renamed parameter**

Once the startup crashes were fixed, every actual inference call failed with:

```
TypeError: __call__() got an unexpected keyword argument 'model_ids'
```

An upstream commit to `safety-tooling` had renamed the `model_ids` parameter to `model_id` (singular), but the main pipeline code was never updated. The inference layer was calling a function that no longer existed with the signature it expected.

**The remaining seven friction points** were moderate or minor: no `.env.example` at the root level, ambiguous documentation about where to create the virtual environment, missing `ffmpeg` dependency (needed for audio tasks), confusing API key naming (`OPENAI_API_KEY1` vs `OPENAI_API_KEY`), and no smoke-test mode to verify setup without burning API credits.

---

## What I Fixed

I fixed all 11 friction points and submitted three PRs to the upstream repositories:

- **[safety-tooling #155](https://github.com/safety-research/safety-tooling/pull/155)** — sentinel `api_key` pattern so the OpenAI client initializes without crashing when the key is absent. Changed four files in the inference layer.
- **[safety-tooling #156](https://github.com/safety-research/safety-tooling/pull/156)** — same fix for Together AI and GraySwan clients, which crashed on empty string keys loaded from blank `.env` lines.
- **[open-source-alignment-faking #2](https://github.com/safety-research/open-source-alignment-faking/pull/2)** — one-click `setup.sh`, annotated `.env.example`, and a `Dockerfile` for clean reproduction.

The `model_ids` → `model_id` rename fix was applied locally and covered by a separate PR.

---

## What's Next

With the pipeline working, the next question was obvious: does the alignment faking behavior actually appear in Claude 4.x models?

Part 3 covers running the experiments on Haiku 4.5, Sonnet 4.5, and Opus 4.5 — and what the scratchpads show.

But first, Part 2: while fixing the pipeline, I also contributed a bug fix to the UK AI Safety Institute's evaluation framework. That piece is about what it's like to contribute to the infrastructure that governments use for pre-deployment AI safety assessments.

---

*The full audit log with all 11 friction points is in [REPRODUCIBILITY_AUDIT.md](REPRODUCIBILITY_AUDIT.md). All code is in the linked PRs.*

*Jack Lakkapragada is a Senior AI Solutions Architect at Salesforce, currently studying AI safety through the BlueDot Technical AI Safety course.*
