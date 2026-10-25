#!/usr/bin/env bash
# Phase 3 WO follow-up runner (frozen with WO_FOLLOWUP_PROTOCOL.md). Run from sprint-3.4/llm-agent-collusion:
#     WO_CEILING=<approved cumulative project USD> bash ../sprint34/run_wo.sh
# Refuses to start unless WO_CEILING is set explicitly, the OpenRouter key reports limit_remaining >= the
# conservative WO cost, and ledger + conservative cost <= WO_CEILING. One WO branch per seed (0-6) from the verified
# A snapshot; each A snapshot must pass verify_snapshot.py and verify_wo_real.py first; a failed run is retried once.
set -u
SPRINT="$(cd ../.. && pwd)"
export UV_PYTHON_INSTALL_DIR="$SPRINT/.tools/python" UV_CACHE_DIR="$SPRINT/.tools/cache"
UV="$SPRINT/.tools/bin/uv"; RUNS="$SPRINT/runs"; LOG="$RUNS/wo_progress.log"
CONSERVATIVE=5.72   # 7 x (max observed E/WG rounds-5-20 cost x 1.10)
PER_RUN=0.82        # max observed branch cost x 1.10
: "${WO_CEILING:?set WO_CEILING to the approved cumulative project ceiling in USD}"
COMMON=(--sellers 5 --buyers 5 --rounds 20 --seller_models gpt-4.1 --buyer_models gpt-4.1-mini
        --log_dir "$RUNS/wo" --spend_ceiling "$WO_CEILING" -y)
mkdir -p "$RUNS/wo"
log() { echo "$(date +%T) $*" | tee -a "$LOG" >&2; }
ledger_total() { python3 -I -c "import json;print(sum(json.loads(l).get('cost_usd') or 0 for l in open('$RUNS/spend_ledger.jsonl')))"; }

remaining=$(python3 -I "$SPRINT/sprint-3.4/sprint34/key_status.py" "$SPRINT/sprint-3.4/compute.env" wo_start | tee -a "$RUNS/key_status.log" \
            | python3 -I -c 'import json,sys; d=json.load(sys.stdin); print(d["limit_remaining"])')
python3 -I -c "import sys; r=$remaining if '$remaining'!='None' else -1; sys.exit(0 if r>=$CONSERVATIVE else 1)" \
  || { log "ABORT: OpenRouter key limit_remaining=$remaining < conservative WO cost $CONSERVATIVE"; exit 3; }
python3 -I -c "import sys; sys.exit(0 if $(ledger_total)+$CONSERVATIVE <= $WO_CEILING else 1)" \
  || { log "ABORT: ledger $(ledger_total) + $CONSERVATIVE > WO_CEILING $WO_CEILING"; exit 3; }
log "START WO; key limit_remaining=$remaining; ledger=$(ledger_total); ceiling=$WO_CEILING"

for seed in 0 1 2 3 4 5 6; do
  if [ $seed -le 2 ]; then A_DIR=$(ls -d "$RUNS"/pilot/*_pilot-A-s$seed | tail -1); else A_DIR=$(ls -d "$RUNS"/sweep/*_sweep-A-s$seed | tail -1); fi
  if ! "$UV" run python ../sprint34/verify_snapshot.py "$A_DIR" >> "$LOG" 2>&1 \
     || ! "$UV" run python ../sprint34/verify_wo_real.py "$A_DIR" >> "$LOG" 2>&1; then
    log "seed $seed: snapshot/WO isolation verification FAILED -> seed skipped"; continue
  fi
  for attempt in 1 2; do
    python3 -I -c "import sys; sys.exit(0 if $(ledger_total)+$PER_RUN <= $WO_CEILING else 1)" \
      || { log "STOP: not enough budget for another WO run (ledger $(ledger_total))"; exit 4; }
    "$UV" run python src/continuous_double_auction/simulation.py --arm WO --seeds "$seed" --tag "wo-WO-s$seed" \
        "${COMMON[@]}" --branch_from "$A_DIR" > "$RUNS/wo_WO${seed}_try${attempt}.log" 2>&1
    rc=$?; log "arm=WO seed=$seed attempt=$attempt exit=$rc"
    [ $rc -eq 0 ] && break
    if grep -q "stopped safely" "$RUNS/wo_WO${seed}_try${attempt}.log"; then log "STOP: safe budget/provider stop"; exit 5; fi
  done
  log "seed $seed done; ledger \$$(ledger_total)"
done
python3 -I "$SPRINT/sprint-3.4/sprint34/key_status.py" "$SPRINT/sprint-3.4/compute.env" wo_end >> "$RUNS/key_status.log"
log "DONE"
