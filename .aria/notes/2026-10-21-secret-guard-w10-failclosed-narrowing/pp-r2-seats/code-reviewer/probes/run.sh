#!/usr/bin/env bash
# run.sh SHAPE HOOK... : one e2e call per hook (bash 5.2, no extension unless EXTDIR), prints rc, wall, text kind
S=$1; shift
for h in "$@"; do
  e=$(mktemp); t0=$EPOCHREALTIME
  if [[ -n "${EXTDIR:-}" ]]; then env -u SECRET_GUARD_TIME_BUDGET_S CLAUDE_PROJECT_DIR="$EXTDIR" taskset -c 0,1 nice -n 19 timeout 12 bash "$h" < "probes/$S.json" >/dev/null 2>"$e"; rc=$?
  else env -u CLAUDE_PROJECT_DIR -u SECRET_GUARD_TIME_BUDGET_S taskset -c 0,1 nice -n 19 timeout 12 bash "$h" < "probes/$S.json" >/dev/null 2>"$e"; rc=$?; fi
  t1=$EPOCHREALTIME
  k=none; [[ -s $e ]] && k=other
  grep -q 'value-REDACTING filter' "$e" && k=finding; grep -q 'too large to scan' "$e" && k=oversize; grep -q 'grows by more' "$e" && k=growth
  grep -q 'has a line longer than' "$e" && k=longline; grep -q 'segments together' "$e" && k=tmax; grep -q '(extension)' "$e" && k=ext-finding
  awk -v a=$t0 -v b=$t1 -v h="$(basename "$h")" -v rc=$rc -v k=$k 'BEGIN{printf "  %-10s rc=%s wall=%.2f %s\n", h, rc, b-a, k}'
  rm -f "$e"
done
