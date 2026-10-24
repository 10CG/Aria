#!/usr/bin/env bash
V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
D=$(cd "$(dirname "$0")" && pwd)
: > $D/batch2.txt
s=$(cut -d' ' -f1 /proc/loadavg); taskset -c 0,1 nice -n 19 bash $V/sc-cases.sh $D/mut/M14.sh > $D/mut/M14.out 2>&1; e=$(cut -d' ' -f1 /proc/loadavg)
echo "M14 (bash 5.2) | load $s->$e | $(grep '^# totals' $D/mut/M14.out) | RED: $(awk '$1=="FAIL"{printf "%s ", $2}' $D/mut/M14.out)" >> $D/batch2.txt
for b in 5.0.18 5.3.20; do
  s=$(cut -d' ' -f1 /proc/loadavg); SC_BASH=/home/dev/.aria/tools/bash-$b/bash taskset -c 0,1 nice -n 19 bash $V/sc-cases.sh $D/v31.sh > $D/v31-$b.out 2>&1; e=$(cut -d' ' -f1 /proc/loadavg)
  echo "v31 on bash $b | load $s->$e | $(grep '^# totals' $D/v31-$b.out) | RED: $(awk '$1=="FAIL"{printf "%s ", $2}' $D/v31-$b.out)" >> $D/batch2.txt
done
echo done >> $D/batch2.txt
