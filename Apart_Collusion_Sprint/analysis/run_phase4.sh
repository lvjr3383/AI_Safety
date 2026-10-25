#!/usr/bin/env bash
# Phase 4 runner (frozen with PHASE4_PROTOCOL.md). Run from sprint-3.4/llm-agent-collusion:
#     bash ../sprint34/run_phase4.sh stage1     # A and E, seeds 0-4, interleaved A0 E0 A1 E1 ...
#     bash ../sprint34/run_phase4.sh ae2        # A and E, seeds 5-9 (after GO or INCONCLUSIVE at the n=5 gate)
#     bash ../sprint34/run_phase4.sh won        # WON, seeds 0-9 (only after the gate says GO)
# Each session: budget check (ledger + $2.50 <= $60), one retry on failure, then the cumulative seller-refusal stop rule.
set -u
PHASE="${1:?stage1 | ae2 | won}"
SPRINT="$(cd ../.. && pwd)"
export UV_PYTHON_INSTALL_DIR="$SPRINT/.tools/python" UV_CACHE_DIR="$SPRINT/.tools/cache"
UV="$SPRINT/.tools/bin/uv"; RUNX=("$UV" run --extra dev --extra analysis --extra providers)
ROOT="$SPRINT/runs_claude"; LOG="$ROOT/phase4_progress.log"; CEILING=60.00; PER_SESSION=2.50
COMMON=(--provider anthropic_direct --sellers 5 --buyers 5 --rounds 20 --seller_models claude-sonnet-5-5
        --buyer_models claude-haiku-5-5 --log_dir "$ROOT/exp" --spend_ceiling "$CEILING" -y)
mkdir -p "$ROOT/exp"
log() { echo "$(date +%T) $*" | tee -a "$LOG" >&2; }
ledger_total() { python3 -I -c "import json;print(sum(json.loads(l).get('cost_usd') or 0 for l in open('$ROOT/spend_ledger.jsonl')))"; }
refusal_rate_ok() { python3 -I - "$ROOT" <<'EOF'
import json, sys
from pathlib import Path
U = [json.loads(l) for d in Path(sys.argv[1], "exp").glob("*_p4-*") if (d / "usage.jsonl").exists() for l in open(d / "usage.jsonl")]
s = [u for u in U if u.get("role", "").startswith("seller") and u.get("prompt_tokens") is not None]
r = sum(u.get("stop_reason") == "refusal" for u in s)
print(f"cumulative seller refusals {r}/{len(s)}", file=sys.stderr)
sys.exit(0 if not s or r / len(s) <= 0.05 else 1)
EOF
}
run() {  # run <arm> <seed> [branch_dir]
  local arm=$1 seed=$2 br=${3:-}
  for attempt in 1 2; do
    python3 -I -c "import sys; sys.exit(0 if $(ledger_total)+$PER_SESSION <= $CEILING else 1)" \
      || { log "STOP: next session might exceed the \$$CEILING ceiling (ledger $(ledger_total))"; exit 4; }
    local extra=(); [ -n "$br" ] && extra=(--branch_from "$br")
    "${RUNX[@]}" python src/continuous_double_auction/simulation.py --arm "$arm" --seeds "$seed" --tag "p4-$arm-s$seed" \
        "${COMMON[@]}" ${extra[@]+"${extra[@]}"} > "$ROOT/p4_${arm}${seed}_try${attempt}.log" 2>&1
    local rc=$?; log "arm=$arm seed=$seed attempt=$attempt exit=$rc ledger=\$$(ledger_total)"
    if grep -q "stopped safely\|refusing to run\|rejected the request" "$ROOT/p4_${arm}${seed}_try${attempt}.log"; then
      log "STOP: fail-closed condition in arm=$arm seed=$seed (see log)"; exit 5; fi
    if [ $rc -eq 0 ]; then
      refusal_rate_ok || { log "STOP: cumulative seller refusals > 5%"; exit 6; }
      return 0
    fi
  done
  log "arm=$arm seed=$seed failed twice -> missing"; return 1
}
case "$PHASE" in
  stage1) for s in 0 1 2 3 4; do run A $s; run E $s; done ;;
  ae2)    for s in 5 6 7 8 9; do run A $s; run E $s; done ;;
  won)    for s in 0 1 2 3 4 5 6 7 8 9; do
            A_DIR=$(ls -d "$ROOT"/exp/*_p4-A-s$s 2>/dev/null | tail -1)
            [ -z "$A_DIR" ] && { log "seed $s: no A run -> WON skipped"; continue; }
            if ! "${RUNX[@]}" python ../sprint34/verify_snapshot.py "$A_DIR" >> "$LOG" 2>&1 \
               || ! "${RUNX[@]}" python ../sprint34/verify_won_real.py "$A_DIR" >> "$LOG" 2>&1; then
              log "seed $s: snapshot/WON isolation verification FAILED -> WON skipped"; continue; fi
            run WON $s "$A_DIR"
          done ;;
  *) echo "unknown phase $PHASE"; exit 2 ;;
esac
log "DONE $PHASE; ledger \$$(ledger_total)"
