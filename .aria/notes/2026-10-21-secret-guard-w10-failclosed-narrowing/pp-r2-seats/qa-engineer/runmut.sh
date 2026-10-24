#!/usr/bin/env bash
# runmut.sh <list of ids...> : run sc-cases.sh (unmodified, bash 5.2) on each mutant, save output, print the FAIL case ids
V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$D/res"
for id in "$@"; do
  s=$(date +%s)
  taskset -c 0,1 nice -n 19 bash "$V/sc-cases.sh" "$D/mut/$id.sh" > "$D/res/$id.txt" 2>&1
  e=$(date +%s)
  printf '%s rc=%s %ss FAIL: %s\n' "$id" "$?" "$((e-s))" "$(awk '$1=="FAIL"{print $2}' "$D/res/$id.txt" | tr '\n' ' ')" >> "$D/res/summary.txt"
done
echo DONE >> "$D/res/summary.txt"
