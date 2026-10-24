#!/usr/bin/env bash
# runsc.sh OUT HOOK [SC_BASH...] : one sc-cases.sh round per bash (one at a time), taskset -c 0,1 nice -n 19; the load is recorded at the start and the end of
# every round (INV-7). SC_ONLY / SC_LOAD_MAX pass through from the environment. Writes OUT/<bash-tag>.txt and appends a summary line to OUT/summary.txt.
V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
O=$1; H=$2; shift 2; mkdir -p "$O"
for b in "$@"; do
  tag=$(basename "$(dirname "$b")"); [[ $b == /usr/bin/bash ]] && tag=bash-5.2.15
  l0=$(cut -d' ' -f1-3 /proc/loadavg); t0=$EPOCHREALTIME
  SC_BASH=$b taskset -c 0,1 nice -n 19 bash "$V/sc-cases.sh" "$H" > "$O/$tag.txt" 2>&1; rc=$?
  l1=$(cut -d' ' -f1-3 /proc/loadavg)
  printf '%-14s exit %s wall %5.1fs | load start %s end %s | %s | %s\n' "$tag" "$rc" "$(awk -v a="$t0" -v b="$EPOCHREALTIME" 'BEGIN{print b-a}')" "$l0" "$l1" \
    "$(grep -o 'timing batch: .*' "$O/$tag.txt" | head -1)" "$(tail -1 "$O/$tag.txt")" | tee -a "$O/summary.txt"
done
