#!/usr/bin/env bash
# Sprint 3.4 sweep runner (frozen with SWEEP_PROTOCOL.md). Run from sprint-3.4/llm-agent-collusion:
#     bash ../sprint34/run_sweep.sh
# - refuses to start unless the OpenRouter key reports a key-level spending limit
# - code ceiling 23.00 USD cumulative (= 28 project limit - 5 reserve), enforced per call from the shared ledger
# - completes each seed's A/W/WG triplet before the next seed; W/WG order alternates by seed parity
# - every A snapshot is verified before branching; a failed run is retried once; a seed whose A or
#   snapshot fails is skipped (no unpaired W/WG runs)
set -u
SPRINT="$(cd ../.. && pwd)"
export UV_PYTHON_INSTALL_DIR="$SPRINT/.tools/python" UV_CACHE_DIR="$SPRINT/.tools/cache"
UV="$SPRINT/.tools/bin/uv"
RUNS="$SPRINT/runs"
LOG="$RUNS/sweep_progress.log"
CEILING=23.00
COMMON=(--sellers 5 --buyers 5 --rounds 20 --seller_models gpt-4.1 --buyer_models gpt-4.1-mini
        --log_dir "$RUNS/sweep" --spend_ceiling "$CEILING" -y)
mkdir -p "$RUNS/sweep"
log() { echo "$(date +%T) $*" | tee -a "$LOG" >&2; }  # stderr: stdout carries return values

limit=$(python3 -I "$SPRINT/sprint-3.4/sprint34/key_status.py" "$SPRINT/sprint-3.4/compute.env" sweep_start | tee -a "$RUNS/key_status.log" \
        | python3 -I -c 'import json,sys; print(json.load(sys.stdin)["limit"])')
if [ "$limit" = "None" ] && [ -z "${DRY_RUN:-}" ]; then log "ABORT: no key-level spending limit reported by OpenRouter"; exit 3; fi
log "START sweep; OpenRouter key limit=$limit; code ceiling=$CEILING"

ledger_total() { python3 -I -c "import json;print(sum(json.loads(l).get('cost_usd') or 0 for l in open('$RUNS/spend_ledger.jsonl')))"; }
room_for_run() { python3 -I -c "import sys; sys.exit(0 if $(ledger_total) + 1.10 <= $CEILING else 1)"; }

run() {  # run <arm> <seed> [branch_dir]; echoes the run dir on success
  local arm=$1 seed=$2 br=${3:-}
  for attempt in 1 2; do
    if ! room_for_run; then log "STOP: not enough budget left for another run (ledger $(ledger_total))"; exit 4; fi
    local extra=(); [ -n "$br" ] && extra=(--branch_from "$br")
    if [ -n "${DRY_RUN:-}" ]; then log "DRY: simulation.py --arm $arm --seeds $seed --tag sweep-$arm-s$seed ${COMMON[*]} ${extra[*]+"${extra[*]}"}"; echo "DRY_A_DIR_s$seed"; return 0; fi
    "$UV" run python src/continuous_double_auction/simulation.py --arm "$arm" --seeds "$seed" \
        --tag "sweep-$arm-s$seed" "${COMMON[@]}" ${extra[@]+"${extra[@]}"} > "$RUNS/sweep_${arm}${seed}_try${attempt}.log" 2>&1
    local rc=$?
    log "arm=$arm seed=$seed attempt=$attempt exit=$rc"
    if [ $rc -eq 0 ]; then ls -d "$RUNS"/sweep/*_sweep-"$arm"-s"$seed" | tail -1; return 0; fi
    if grep -q "stopped safely" "$RUNS/sweep_${arm}${seed}_try${attempt}.log"; then log "STOP: safe budget/provider stop"; exit 5; fi
  done
  return 1
}

for seed in 0 1 2 3 4 5 6; do
  if [ $seed -le 2 ]; then
    A_DIR=$(ls -d "$RUNS"/pilot/*_pilot-A-s$seed | tail -1)
  else
    A_DIR=$(run A $seed); rc=$?
    if [ $rc -eq 4 ] || [ $rc -eq 5 ]; then exit $rc; fi   # budget/provider stop inside the subshell
    if [ $rc -ne 0 ]; then log "seed $seed: A failed twice -> seed skipped"; continue; fi
  fi
  if [ -n "${DRY_RUN:-}" ]; then :
  elif ! "$UV" run python ../sprint34/verify_snapshot.py "$A_DIR" >> "$LOG" 2>&1 \
     || ! "$UV" run python ../sprint34/verify_branch_real.py "$A_DIR" >> "$LOG" 2>&1; then
    log "seed $seed: snapshot verification FAILED -> seed skipped"; continue
  fi
  if [ $((seed % 2)) -eq 0 ]; then order="W WG"; else order="WG W"; fi
  for arm in $order; do
    run "$arm" "$seed" "$A_DIR" > /dev/null || log "seed $seed: $arm failed twice (triplet incomplete)"
  done
  log "seed $seed done; ledger total \$$(ledger_total)"
done
python3 -I "$SPRINT/sprint-3.4/sprint34/key_status.py" "$SPRINT/sprint-3.4/compute.env" sweep_end >> "$RUNS/key_status.log"
log "DONE"
