# Dockerfile — open-source-alignment-faking
#
# Produces a reproducible environment with all system and Python dependencies
# pre-installed. Fixes FP-1 (SSH submodule), FP-2 (uv PATH), FP-8 (ffmpeg).
#
# PREREQUISITES before building:
#   The safety-tooling submodule must be initialised in your local checkout.
#   If you cloned with --recurse-submodules and it failed (SSH key issue), run:
#
#     git -c submodule.safety-tooling.url=https://github.com/safety-research/safety-tooling.git \
#         submodule update --init --recursive
#
#   Or just run:  bash setup.sh
#   Then build:   docker build -t alignment-faking .
#
# USAGE:
#   # Interactive shell (fill in your real keys):
#   docker run --rm -it \
#       -e ANTHROPIC_API_KEY=sk-ant-... \
#       -e OPENAI_API_KEY=sk-... \
#       -e OPENAI_API_KEY1=sk-... \
#       -v "$(pwd)/outputs:/workspace/outputs" \
#       alignment-faking
#
#   # Inside the container, run the pipeline:
#   bash experiments/examples/1_run_pipeline.sh claude-3-5-sonnet-20240620
#
#   # Or mount a .env file instead of passing -e flags:
#   docker run --rm -it \
#       --env-file .env \
#       -v "$(pwd)/outputs:/workspace/outputs" \
#       alignment-faking

FROM python:3.11-slim-bookworm

# ── System dependencies ─────────────────────────────────────────────────────
# ffmpeg    : audio processing via pydub (FP-8)
# git       : submodule operations and huggingface-hub downloads
# curl      : uv installer
# libgl1    : OpenCV (opencv-python) runtime dependency
# libglib2.0-0: OpenCV runtime dependency
RUN apt-get update && apt-get install -y --no-install-recommends \
        ffmpeg \
        git \
        curl \
        libgl1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# ── uv ─────────────────────────────────────────────────────────────────────
# Install uv and add to PATH directly (FP-2: the 'source ~/.local/bin/env'
# trick in the README does not work; we use export PATH instead).
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# ── Application code ────────────────────────────────────────────────────────
WORKDIR /workspace

# Copy repository (the safety-tooling submodule must already be present
# in your local checkout — see prerequisites above).
COPY . .

# ── Python environment ──────────────────────────────────────────────────────
# Create a venv at /workspace/.venv (FP-7: venv lives at repo root).
RUN uv venv --python 3.11 .venv

# Activate venv for subsequent RUN commands.
ENV VIRTUAL_ENV="/workspace/.venv"
ENV PATH="/workspace/.venv/bin:$PATH"

# Install safety-tooling (editable) then repo requirements.
RUN uv pip install -e safety-tooling
RUN uv pip install -r requirements.txt

# ── Runtime environment ─────────────────────────────────────────────────────
# Make src/ importable as a package.
ENV PYTHONPATH="/workspace"

# API keys should be passed at runtime via --env-file or -e flags, never baked in.
# The pipeline crashes if OPENAI_API_KEY is unset (FP-3); see .env.example for details.

# Default: drop into an interactive bash shell so the researcher can run
# whichever experiment they need.
CMD ["/bin/bash"]
