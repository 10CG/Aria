#!/usr/bin/env bash
# probe-run.sh HOOK PROBE... : runs HOOK (as Claude Code would) on each probe json; prints name rc kind wall
D=$(cd "$(dirname "$0")" && pwd); H=$(readlink -f "$1"); shift
kind() { if grep -q 'has a line longer than' "$1"; then echo longline; elif grep -q 'grows by more than' "$1"; then echo growth
  elif grep -q 'segments together are longer than' "$1"; then echo tmax; elif grep -q 'too large to scan' "$1"; then echo oversize
  elif grep -q 'within the time budget' "$1"; then echo time; elif grep -q 'value-REDACTING filter' "$1"; then echo finding
  elif [[ -s "$1" ]]; then echo other; else echo none; fi; }
for p in "$@"; do
  e=$(mktemp -p "$D/tmp"); t0=$EPOCHREALTIME
  ( cd "$D/tmp" && env -u CLAUDE_PROJECT_DIR -u _SG_RELAXED -u SECRET_GUARD_TIME_BUDGET_S HOME="$D/home" taskset -c 0,1 nice -n 19 timeout 12 bash "$H" < "$D/probes/$p.json" >/dev/null 2>"$e" ); rc=$?
  t1=$EPOCHREALTIME
  printf '%-28s rc=%s %-9s %ss\n' "$p" "$rc" "$(kind "$e")" "$(awk -v a="$t0" -v b="$t1" 'BEGIN{printf "%.2f", b-a}')"
  rm -f "$e"
done
echo "load $(cut -d' ' -f1-3 /proc/loadavg)"
