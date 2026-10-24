#!/usr/bin/env bash
# exp1.sh HOOK SHAPE : run the hook once under each bash on SHAPE; right afterwards list processes whose args look like the timer's sleep (N.NNNNNN)
# or are our own markers. Own PIDs only: we record the hook pid and show ps rows by the 6-decimal sleep argument.
HOOK=$1; SHAPE=$2
D=$(cd "$(dirname "$0")" && pwd)
for b in /home/dev/.aria/tools/bash-5.0.18/bash /home/dev/.aria/tools/bash-5.1.16/bash /usr/bin/bash /home/dev/.aria/tools/bash-5.3.20/bash; do
  st=$(mktemp -d)
  t0=$EPOCHREALTIME
  taskset -c 0,1 nice -n 19 env SC_SHIM_STATE="$st" "$b" "$HOOK" < "$D/in/$SHAPE.json" >/dev/null 2>"$D/exp1.err"; rc=$?
  t1=$EPOCHREALTIME
  wall=$(awk -v a="${t0/,/.}" -v b="${t1/,/.}" 'BEGIN{printf "%.2f", b-a}')
  echo "== $($b -c 'echo $BASH_VERSION') rc=$rc wall=${wall}s load=$(cut -d' ' -f1-3 /proc/loadavg) stderr_bytes=$(wc -c < "$D/exp1.err")"
  # rows: sleep processes whose single argument has exactly 6 decimals (the timer's _SG_LEFT)
  ps -eo pid,ppid,pgid,stat,etimes,args | awk '$6=="sleep" && $7 ~ /^[0-9]+\.[0-9][0-9][0-9][0-9][0-9][0-9]$/ {print "   RESIDUAL-sleep: " $0}'
  ps -eo pid,ppid,pgid,stat,etimes,args | awk -v h="$HOOK" '$0 ~ h && $0 !~ /awk/ {print "   RESIDUAL-hook: " $0}'
  rm -rf "$st"
done
