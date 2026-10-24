#!/usr/bin/env bash
# flake.sh HOOK N : replicate V5-S13/V5-S13b (sc-direct.sh) N times on the given hook and count how often the "child still alive right after _sg_relax_run" check sees it.
# Also counts how often it is gone after a 20 ms grace, to show the observation is a race with the asynchronous SIGKILL, not a surviving process.
H=$1; N=${2:-100}
source "$H" </dev/null >/dev/null 2>&1
set +e
export SECRET_GUARD_TIME_BUDGET_S=1; _SG_MODE=whole
_sg_vx_pass() { sleep ${ARG:-7.7773} >/dev/null 2>&1 & return 0; }
seen=0; seen_after_grace=0; bad_rc=0
for ((i = 0; i < N; i++)); do
  _SG_P0=$EPOCHREALTIME
  _sg_relax_run "cmd" 2>/dev/null; rc=$?
  [[ $rc == 0 ]] || bad_rc=$((bad_rc+1))
  n=$(ps -eo args | awk -v a="${ARG:-7.7773}" '$1=="sleep" && $2==a' | wc -l)
  if (( n )); then
    seen=$((seen+1))
    sleep 0.02
    n2=$(ps -eo args | awk -v a="${ARG:-7.7773}" '$1=="sleep" && $2==a' | wc -l)
    (( n2 )) && seen_after_grace=$((seen_after_grace+1))
  fi
done
echo "iterations=$N rc!=0: $bad_rc | child visible right after return: $seen | still visible 20 ms later: $seen_after_grace | load $(cut -d' ' -f1-3 /proc/loadavg)"
