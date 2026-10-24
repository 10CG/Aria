#!/usr/bin/env bash
# run1.sh <label> [NAME=value ...] -- one whole-suite round in the worktree (PATH bash), output to $OUT/<label>.out
set -u
WT=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria
OUT=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002d
label=$1; shift
wait_load() {
  local t=0 l
  while :; do
    l=$(cut -d' ' -f1 /proc/loadavg)
    awk -v l="$l" 'BEGIN{exit !(l <= 1.2)}' && break
    (( t % 300 == 0 )) && echo "wait t=${t}s load=$l" >> "$OUT/$label.meta"
    if (( t >= 1800 )); then echo "WAIT-TIMEOUT t=${t}s load=$l" >> "$OUT/$label.meta"; break; fi
    sleep 15; t=$((t + 15))
  done
  return 0
}
echo "runner pid $$ label $label env: $*" > "$OUT/$label.meta"
wait_load
echo "start $(date -u +%FT%TZ) loadavg $(cat /proc/loadavg)" >> "$OUT/$label.meta"
( cd "$WT" && exec env "$@" taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh ) > "$OUT/$label.out" 2>&1 &
child=$!
echo "child pid $child" >> "$OUT/$label.meta"
wait "$child"; rc=$?
echo "end $(date -u +%FT%TZ) rc $rc loadavg $(cat /proc/loadavg)" >> "$OUT/$label.meta"
exit 0
