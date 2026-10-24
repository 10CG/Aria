#!/usr/bin/env bash
# other-bash.sh : main-loop rerun of the implementation round on the four other bashes, each started when the 1-min load < 1.5, repeated (max 3) until judged
V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31; O=$(cd "$(dirname "$0")" && pwd)
H=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria/hooks/secret-guard.sh
lt() { awk -v a="$1" -v b="$2" 'BEGIN{exit !(a+0 < b+0)}'; }
waitlow() { local t=0; until lt "$(cut -d' ' -f1 /proc/loadavg)" 1.5; do sleep 10; t=$((t+10)); (( t >= 3600 )) && return 1; done; return 0; }
for b in ${*:-5.0.18 5.1.16 5.3.20 3.2.57}; do
  for k in 1 2 3; do
    waitlow || { echo "$b gave up waiting $(cat /proc/loadavg)" >> "$O/other.log"; break; }
    SC_BASH=/home/dev/.aria/tools/bash-$b/bash taskset -c 0,1 nice -n 19 bash "$V/sc-cases.sh" "$H" > "$O/impl-$b.try$k.txt" 2>&1; rc=$?
    echo "$(date -u +%T) $b try $k rc=$rc | $(grep -E '^# load' "$O/impl-$b.try$k.txt" | tail -1) | $(grep -E '^# totals' "$O/impl-$b.try$k.txt" | tail -1)" >> "$O/other.log"
    grep -q 'timing batch: judged' <(grep -E '^# load' "$O/impl-$b.try$k.txt" | tail -1) && break
  done
done
echo "$(date -u +%T) done" >> "$O/other.log"
