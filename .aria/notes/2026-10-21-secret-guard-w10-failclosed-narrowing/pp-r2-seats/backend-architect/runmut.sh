#!/usr/bin/env bash
# runmut.sh M1 M2 ... : run sc-cases.sh (bash 5.2, nice) on each mutant sequentially; one line per mutant in mutres.txt
V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
D=$(cd "$(dirname "$0")" && pwd)
for m in "$@"; do
  s=$(cut -d' ' -f1 /proc/loadavg)
  taskset -c 0,1 nice -n 19 bash $V/sc-cases.sh $D/mut/$m.sh > $D/mut/$m.out 2>&1
  e=$(cut -d' ' -f1 /proc/loadavg)
  red=$(awk '$1=="FAIL"{printf "%s ", $2}' $D/mut/$m.out)
  tot=$(grep '^# totals' $D/mut/$m.out)
  echo "$m | load $s->$e | $tot | RED: ${red:-none}" >> $D/mutres.txt
done
echo done >> $D/mutres.txt
