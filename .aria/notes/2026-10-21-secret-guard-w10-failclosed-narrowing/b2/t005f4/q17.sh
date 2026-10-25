#!/bin/bash
# q17.sh: W14 Q-17 alone, twice (was it timing that left V6-E2 green in the full W14 run?). Each run starts when the one-minute load is below 1.2.
set -u
S=/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad; O=$S/r217impl/t005f4/runs; V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
T=(taskset -c 0,1 nice -n 19); la() { cut -d' ' -f1-3 /proc/loadavg; }
waitload() { local i; for i in $(seq 1 120); do awk '{exit !($1 < 1.2)}' /proc/loadavg && return 0; sleep 10; done; return 1; }
for r in a b; do
  waitload || { echo "w14-q17-$r NOT-RUN load stayed >= 1.2" >> $O/steps.log; continue; }
  l0=$(la); t0=$SECONDS
  env W14_IDS="Q-17" W14_DIR="$O/w14-q17-$r" W14_OUT="$O/W14-q17-$r.txt" W14_PREDICT=$S/r217impl/t003a/predict.md W14_GAPMAP=$S/r217impl/t003a/gapmap.tsv "${T[@]}" bash $V/impl/w14.sh > $O/w14-q17-$r.log 2>&1
  echo "w14-q17-$r rc=$? load0=[$l0] load1=[$(la)] secs=$((SECONDS - t0))" >> $O/steps.log
done
