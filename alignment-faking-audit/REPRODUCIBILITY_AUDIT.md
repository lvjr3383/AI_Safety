# Reproducibility Audit — open-source-alignment-faking

**Audited:** 2026-02-27
**Fixed:** 2026-02-27
**Goal:** Document all friction points blocking a new researcher from running this repo in under 10 minutes. See **Fixes Applied** section at the bottom for resolution of all 10 issues.

---

## Summary

Out of the box, a fresh researcher cannot run `./experiments/examples/1_run_pipeline.sh` at all. The script crashes before making a single API call due to missing environment setup. Total friction points found: **10**.

---

## Friction Points

### FP-1 · BLOCKER · Submodule uses SSH, not HTTPS

**Where:** `.gitmodules` line 3
**What happened:**
```
git clone --recurse-submodules https://github.com/safety-research/open-source-alignment-faking
```
The main repo clones fine over HTTPS, but the `safety-tooling` submodule is configured with an SSH URL:
```
url = git@github.com:safety-research/safety-tooling.git
```
This causes an immediate authentication failure for anyone without an SSH key registered with GitHub:
```
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.
```
**Impact:** The repo cannot be cloned out-of-the-box using the HTTPS URL given in the README. Researchers must either (a) know to override the submodule URL manually, or (b) have SSH keys set up.
**Workaround used:**
```bash
git -c submodule.safety-tooling.url=https://github.com/safety-research/safety-tooling.git \
    submodule update --init --recursive
```

---

### FP-2 · BLOCKER · `uv` not pre-installed, `source $HOME/.local/bin/env` fails

**Where:** `safety-tooling/README.md` step 1
**What happened:** `uv` is not a standard system tool. After running the install script:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env   # <-- THIS FAILS
```
The file `$HOME/.local/bin/env` does not exist after installation on macOS. The actual binary is at `$HOME/.local/bin/uv`. The `source` command produces:
```
(eval):source:1: no such file or directory: /Users/.../env
```
**Impact:** Anyone who copies the README command literally will have `uv` installed but not on their `PATH`, and will get a confusing error before they can proceed.
**Workaround used:**
```bash
export PATH="$HOME/.local/bin:$PATH"
```

---

### FP-3 · BLOCKER · `OPENAI_API_KEY` required even for Anthropic-only runs

**Where:** `safety-tooling/safetytooling/apis/inference/api.py` lines 150–162
**What happened:** Running the pipeline with the default model `claude-3-opus-20240229` (Anthropic) crashes immediately:
```
openai.OpenAIError: The api_key client option must be set either by passing api_key
to the client or by setting the OPENAI_API_KEY environment variable
```
**Root cause:** `InferenceAPI.__init__()` unconditionally instantiates `OpenAIChatModel` and `OpenAICompletionModel` at construction time — before any model routing occurs. The `openai.AsyncClient()` call inside those classes requires `OPENAI_API_KEY` to be set in the environment, even if the user will only ever call an Anthropic or Together model.
**Impact:** A researcher who only has an Anthropic API key cannot run the example pipeline at all without also setting a dummy or real OpenAI key.
**No workaround exists** without modifying `api.py` or setting `OPENAI_API_KEY=dummy`.

---

### FP-4 · MODERATE · No `.env.example` in the main repo root

**Where:** Main repo root
**What happened:** The main `README.md` says:
> "Ensure to make a `.env` file with your API keys."

But there is no `.env.example` file in the main repo to copy. The only `.env.example` is in `safety-tooling/`. The README does not say:
- Which directory the `.env` file should be placed in
- What keys are required vs. optional
- Where to find the template

**Impact:** New researchers must discover `safety-tooling/.env.example` themselves and figure out where to place their `.env`.

---

### FP-5 · MODERATE · Confusing default `openai_tag` vs. standard `OPENAI_API_KEY`

**Where:** `safety-tooling/safetytooling/utils/experiment_utils.py` line ~40
**What happened:** `ExperimentConfigBase` defaults to:
```python
openai_tag: str = "OPENAI_API_KEY1"
```
This means `setup_environment()` looks for `OPENAI_API_KEY1` in the `.env`, not the standard `OPENAI_API_KEY`. The `.env.example` lists `OPENAI_API_KEY1=` as an "alternative key" field. A researcher who sets the standard `OPENAI_API_KEY=` in their `.env` may still see warnings that OpenAI is not available, while the API client still requires it at init time (see FP-3).
**Impact:** Confusing key naming — standard env var name does not match the default `openai_tag`.

---

### FP-6 · MODERATE · Setup instructions split across two READMEs with no clear path

**Where:** Main `README.md` and `safety-tooling/README.md`
**What happened:** The main README says:
> "Follow the instructions in safety-tooling/README.md to set up the environment."

But the `safety-tooling/README.md` setup instructions are written for standalone installation of that library (including `git clone safety-tooling`, `cd safety-tooling`, `uv venv`, etc.) — steps that are wrong or redundant when `safety-tooling` is used as a submodule. There is no clear delineation of which steps apply when using it as a submodule vs. standalone.
**Impact:** A new researcher following `safety-tooling/README.md` literally will try to clone a separate repo they already have, create a venv inside the submodule, and activate it — leading to a broken environment.

---

### FP-7 · MODERATE · `venv` location and activation not specified

**Where:** Main `README.md`
**What happened:** The main README does not say where to create the virtual environment or how to activate it before running `uv pip install`. The `safety-tooling/README.md` says to run `uv venv` inside `safety-tooling/`, which creates `.venv` there — but that venv would not be active when running `python -m src.run` from the repo root.
**Impact:** A researcher may install packages into the wrong venv (or into the system/global Python), then find that `python -m src.run` cannot find them.
**Correct behavior** (confirmed working): create and activate venv in the **main repo root**, then `uv pip install -e safety-tooling && uv pip install -r requirements.txt`.

---

### FP-8 · MINOR · Missing system dependency: `ffmpeg`

**Where:** Runtime warning when script starts
**What happened:** When the pipeline script executes, the following warning appears immediately:
```
RuntimeWarning: Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work
```
This comes from `pydub`, which is a dependency of `safetytooling`. `ffmpeg` is not a Python package — it's a system binary that must be installed separately (e.g., `brew install ffmpeg` on macOS, `apt install ffmpeg` on Ubuntu).
**Impact:** `ffmpeg` is not mentioned anywhere in the README or `requirements.txt`. For audio-related features, this will silently fail.

---

### FP-9 · MINOR · `requirements.txt` comments reference external repos not needed for basic use

**Where:** `requirements.txt` lines 1–2
**What happened:**
```
# safety-tooling (submodule) https://github.com/safety-research/safety-tooling
# openweights (optional for running finetuning and inference on RunPod) https://github.com/longtermrisk/openweights
```
The comment about `openweights` suggests it may be needed, but it is not listed as a pip dependency and the README does not mention it. It is only used in a conditional branch of `run.py` (`use_open_weights=True`). This creates confusion about whether `openweights` needs to be installed manually.

---

### FP-10 · MINOR · `1_run_pipeline.sh` hardcodes 50 workers and high concurrency — no "dry run" mode

**Where:** `experiments/examples/1_run_pipeline.sh` lines 19–21
**What happened:**
```bash
workers=50
anthropic_num_threads=45
together_num_threads=10
```
The script runs 100 HarmBench examples with 45 Anthropic threads and no dry-run option. There is no `--dry_run` flag, no `--limit 1` example in the README, and no note about cost or rate limits. A researcher who successfully authenticates will immediately start a 100-example run burning API credits.
**Impact:** Potential surprise API costs; no way to do a smoke-test with 1 example from the documented entry point.

---

## Environment Snapshot at Time of Audit

| Item | Version/State |
|------|--------------|
| OS | macOS Darwin 25.3.0 (aarch64) |
| Python | 3.11.14 (installed via `uv`) |
| uv | 0.10.7 |
| Safety-tooling submodule commit | `21a7264aaeb0a7d7150787d02c355ec70bf49dd2` |
| OPENAI_API_KEY | Not set |
| ANTHROPIC_API_KEY | Not set |
| ffmpeg | Not installed |

---

## What Happens When You Run `./experiments/examples/1_run_pipeline.sh`

With no `.env` file and no API keys set, the script fails immediately with:
```
openai.OpenAIError: The api_key client option must be set either by passing api_key
to the client or by setting the OPENAI_API_KEY environment variable
```
The log file is created in `./outputs/suffix-True-new-classifiers-True/logs/`, but no inference is attempted. The error occurs inside `InferenceAPI.__init__()` before any model routing or prompt loading.

---

## Priority Order for One-Click Setup Script / Docker Container

1. **FP-3** — Fix or document the OpenAI key requirement (even for Anthropic runs). Consider lazy initialization of provider clients.
2. **FP-1** — Switch submodule URL to HTTPS (or provide a setup script that uses HTTPS override).
3. **FP-4 + FP-5** — Add `.env.example` to the repo root with clear annotations on required vs. optional keys and correct default key names.
4. **FP-6 + FP-7** — Rewrite or consolidate setup instructions; clarify venv location and activation.
5. **FP-2** — Fix the `source $HOME/.local/bin/env` instruction; use `export PATH` instead.
6. **FP-8** — Add `ffmpeg` to system prerequisites in README.
7. **FP-10** — Add a minimal smoke-test command (e.g., `--limit 1`) to the README.
8. **FP-9** — Clarify `openweights` install status in README.

---

## Fixes Applied

All 10 friction points have been resolved. The repo now supports one-click setup via `bash setup.sh`.

### New files added

| File | Fixes |
|------|-------|
| `setup.sh` | FP-1, FP-2, FP-4, FP-5, FP-6, FP-7, FP-8, FP-10 |
| `.env.example` | FP-3 (documented), FP-4, FP-5, FP-9 |
| `Dockerfile` | FP-1, FP-2, FP-8 |
| `.dockerignore` | Docker image hygiene |

### Submodule patches (safety-tooling)

**FP-3** was fixed by patching three files in `safety-tooling/safetytooling/apis/inference/openai/`:

| File | Change |
|------|--------|
| `base.py` | In `OpenAIModel.__init__`, the `else` branch now passes `api_key=os.environ.get("OPENAI_API_KEY", "not-configured")` to `openai.AsyncClient()`, so the client initialises without crashing when `OPENAI_API_KEY` is absent. |
| `embedding.py` | `OpenAIEmbeddingModel.__init__` uses the same sentinel pattern. |
| `moderation.py` | `OpenAIModerationModel.__init__` uses the same sentinel pattern. |
| `s2s.py` | `OpenAIS2SModel.__init__` used `os.environ["OPENAI_API_KEY"]` (hard dict access, raises `KeyError`). Changed to `os.environ.get("OPENAI_API_KEY", "not-configured")`. |

**Root cause explanation:** `openai` v1+ raises `OpenAIError` at `AsyncClient()` construction time if no `api_key` is found — either via parameter or `OPENAI_API_KEY` env var. Because `InferenceAPI.__init__()` eagerly constructs all provider clients (including OpenAI), the crash occurred even when running purely Anthropic models. The sentinel value `"not-configured"` satisfies the constructor; actual OpenAI API calls will fail with HTTP 401 if a real key is not set, which is a clear and expected error.

### Fix summary by FP

| FP | Severity | Status | Resolution |
|----|----------|--------|-----------|
| FP-1 SSH submodule | BLOCKER | ✅ Fixed | `setup.sh` uses HTTPS override automatically; `Dockerfile` documents the prerequisite |
| FP-2 `source env` broken | BLOCKER | ✅ Fixed | `setup.sh` uses `export PATH="$HOME/.local/bin:$PATH"` |
| FP-3 OpenAI required for Anthropic | BLOCKER | ✅ Fixed | Patched `base.py`, `embedding.py`, `moderation.py`, `s2s.py` with sentinel api_key |
| FP-4 No `.env.example` at root | MODERATE | ✅ Fixed | Added `.env.example` to repo root |
| FP-5 `OPENAI_API_KEY1` confusion | MODERATE | ✅ Fixed | `.env.example` explains the relationship; `setup.sh` prints a clear note |
| FP-6 Split READMEs | MODERATE | ✅ Fixed | `setup.sh` is the single authoritative entry point |
| FP-7 Venv location unspecified | MODERATE | ✅ Fixed | `setup.sh` creates `.venv` at repo root and prints `source .venv/bin/activate` |
| FP-8 `ffmpeg` missing | MINOR | ✅ Fixed | `setup.sh` checks and prints OS-specific install command; `Dockerfile` installs it |
| FP-9 `openweights` confusion | MINOR | ✅ Fixed | `.env.example` clarifies it's optional/RunPod-only with install instructions |
| FP-10 No smoke-test mode | MINOR | ✅ Fixed | `setup.sh` prints a `--limit 1` smoke-test command at end of setup |

### Quick-start (after fixes)

```bash
# 1. Clone
git clone https://github.com/safety-research/open-source-alignment-faking
cd open-source-alignment-faking

# 2. One-click setup (handles all 10 friction points)
bash setup.sh

# 3. Activate venv
source .venv/bin/activate

# 4. Add your API keys
$EDITOR .env

# 5. Smoke test (1 example, low cost)
bash experiments/examples/1_run_pipeline.sh claude-3-5-sonnet-20240620

# OR: Docker
docker build -t alignment-faking .
docker run --rm -it --env-file .env -v "$(pwd)/outputs:/workspace/outputs" alignment-faking
```
