#!/usr/bin/env bash
# Crossed-model follow-up runner (frozen with CROSSED_PROTOCOL.md). From sprint-3.4/llm-agent-collusion: bash ../sprint34/run_crossed.sh
set -u
SPRINT="$(cd ../.. && pwd)"; export UV_PYTHON_INSTALL_DIR="$SPRINT/.tools/python" UV_CACHE_DIR="$SPRINT/.tools/cache"
RUNX=("$SPRINT/.tools/bin/uv" run --extra dev --extra analysis --extra providers)
ROOT="$SPRINT/runs_crossed"; LOG="$ROOT/crossed_progress.log"; CEILING=30.00
COMMON=(--provider mixed_crossed --sellers 5 --buyers 5 --rounds 20 --seller_models claude-sonnet-5-5 --buyer_models gpt-4.1-mini
        --log_dir "$ROOT/exp" --spend_ceiling "$CEILING" -y)
mkdir -p "$ROOT/exp"; log() { echo "$(date +%T) $*" | tee -a "$LOG" >&2; }
ledger_total() { python3 -I -c "import json;print(sum(json.loads(l).get('cost_usd') or 0 for l in open('$ROOT/spend_ledger.jsonl')))"; }
for s in 0 1 2 3 4; do for arm in A E; do
  ok=0
  for attempt in 1 2; do
    "${RUNX[@]}" python src/continuous_double_auction/simulation.py --arm $arm --seeds $s --tag "x-$arm-s$s" "${COMMON[@]}" \
        > "$ROOT/x_${arm}${s}_try${attempt}.log" 2>&1; rc=$?
    log "arm=$arm seed=$s attempt=$attempt exit=$rc ledger=\$$(ledger_total)"
    grep -q "stopped safely\|refusing to run\|rejected the request" "$ROOT/x_${arm}${s}_try${attempt}.log" && { log "STOP: fail-closed"; exit 5; }
    [ $rc -eq 0 ] && { ok=1; break; }
  done
  [ $ok -eq 0 ] && log "arm=$arm seed=$s failed twice -> missing"
  python3 -I - "$ROOT" <<'PY' || { log "STOP: cumulative seller refusals > 5%"; exit 6; }
import json, sys
from pathlib import Path
U = [json.loads(l) for d in Path(sys.argv[1], "exp").glob("*_x-*") if (d / "usage.jsonl").exists() for l in open(d / "usage.jsonl")]
s = [u for u in U if u.get("role", "").startswith("seller") and u.get("prompt_tokens") is not None]
sys.exit(0 if not s or sum(u.get("stop_reason") == "refusal" for u in s) / len(s) <= 0.05 else 1)
PY
done; done
log "DONE; ledger \$$(ledger_total)"
