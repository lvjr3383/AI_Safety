#!/bin/bash
# setup.sh — One-click environment setup for open-source-alignment-faking
#
# Fixes addressed:
#   FP-1  Submodule SSH URL → uses HTTPS override
#   FP-2  uv PATH issue    → exports PATH directly, no broken 'source env'
#   FP-4  Missing .env     → copies .env.example to .env
#   FP-5  Key name mismatch→ prints clear instructions
#   FP-6  Split READMEs    → this script is the single setup entry point
#   FP-7  Venv location    → creates .venv at repo root
#   FP-8  ffmpeg missing   → checks and warns with install instructions
#   FP-10 No smoke-test    → prints a --limit 1 test command at end
#
# Usage:
#   bash setup.sh
#   source .venv/bin/activate

set -euo pipefail

# ── colour helpers ──────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; BOLD='\033[1m'; NC='\033[0m'
info()  { echo -e "${BLUE}[INFO]${NC}  $*"; }
ok()    { echo -e "${GREEN}[ OK ]${NC}  $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
err()   { echo -e "${RED}[ERR ]${NC}  $*" >&2; }

echo -e "\n${BOLD}=== open-source-alignment-faking · Setup ===${NC}\n"

# ── 0. Verify we are in the repo root ──────────────────────────────────────
if [ ! -f "pyproject.toml" ] || [ ! -d "src" ]; then
    err "Run this script from the repository root (where pyproject.toml lives)."
    exit 1
fi

# ── 1. uv (FP-2) ───────────────────────────────────────────────────────────
info "Checking for uv..."
if ! command -v uv &>/dev/null; then
    # The installer puts the binary at ~/.local/bin — NOT at ~/.local/bin/env.
    # We export PATH directly instead of using the broken 'source ~/.local/bin/env'.
    info "uv not found — installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
    ok "uv installed: $(uv --version)"
else
    ok "uv found: $(uv --version)"
fi
# Ensure ~/.local/bin is on PATH for the rest of this script
export PATH="$HOME/.local/bin:$PATH"

# ── 2. Git submodule via HTTPS (FP-1) ──────────────────────────────────────
info "Checking safety-tooling submodule..."
if [ ! -f "safety-tooling/pyproject.toml" ]; then
    info "Submodule not initialised — cloning via HTTPS (the .gitmodules file uses SSH"
    info "which fails without a GitHub SSH key; we override to HTTPS automatically)."
    git -c submodule.safety-tooling.url=https://github.com/safety-research/safety-tooling.git \
        submodule update --init --recursive
    ok "safety-tooling submodule initialised."
else
    ok "safety-tooling submodule already present."
fi

# ── 3. Python virtual environment (FP-7) ───────────────────────────────────
info "Setting up Python 3.11 virtual environment in repo root..."
if [ ! -d ".venv" ]; then
    uv python install 3.11
    uv venv --python 3.11
    ok "Virtual environment created at .venv/"
else
    ok ".venv/ already exists — skipping creation."
fi

# ── 4. Install Python packages ─────────────────────────────────────────────
info "Installing safety-tooling (editable)..."
uv pip install -e safety-tooling

info "Installing repo requirements..."
uv pip install -r requirements.txt
ok "All Python packages installed."

# ── 5. .env file (FP-4) ────────────────────────────────────────────────────
if [ ! -f ".env" ]; then
    cp .env.example .env
    warn ".env created from .env.example — you must fill in your API keys before running."
    warn "Open .env and follow the comments inside."
else
    ok ".env already exists."
fi

# ── 6. ffmpeg system dependency check (FP-8) ───────────────────────────────
info "Checking for ffmpeg (required by pydub for audio features)..."
if ! command -v ffmpeg &>/dev/null; then
    warn "ffmpeg not found. Audio-related features will not work."
    warn "Install it with:"
    if [[ "$(uname)" == "Darwin" ]]; then
        warn "  brew install ffmpeg"
    else
        warn "  sudo apt-get install -y ffmpeg   # Debian/Ubuntu"
        warn "  sudo yum install -y ffmpeg        # RHEL/CentOS"
    fi
    warn "(ffmpeg is not needed to run the basic alignment-faking pipeline.)"
else
    ok "ffmpeg found: $(ffmpeg -version 2>&1 | head -1)"
fi

# ── 7. Summary ─────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}Setup complete!${NC}"
echo ""
echo -e "${BOLD}Next steps:${NC}"
echo ""
echo "  1. Activate the virtual environment:"
echo "       source .venv/bin/activate"
echo ""
echo "  2. Fill in your API keys in .env:"
echo "       \$EDITOR .env"
echo ""
echo -e "     ${YELLOW}Key naming note (FP-5):${NC} The pipeline defaults to reading"
echo "     OPENAI_API_KEY1 (not the standard OPENAI_API_KEY). Set both to"
echo "     the same value, or set OPENAI_API_KEY1 as your primary OpenAI key."
echo ""
echo -e "     ${YELLOW}Anthropic-only note:${NC} Even if you only use Anthropic models,"
echo "     OPENAI_API_KEY must be set in .env (even to a placeholder like"
echo "     'not-needed') to prevent a crash at startup. See .env.example"
echo "     for details."
echo ""
echo "  3. Smoke-test with 1 example (cheap — runs 1 HarmBench prompt):"
echo "       bash experiments/examples/1_run_pipeline.sh claude-3-5-sonnet-20240620 --limit 1"
echo ""
echo "  4. Full paper replication (100 examples, 2 retries):"
echo "       bash experiments/examples/1_run_pipeline.sh claude-3-5-sonnet-20240620"
echo ""
