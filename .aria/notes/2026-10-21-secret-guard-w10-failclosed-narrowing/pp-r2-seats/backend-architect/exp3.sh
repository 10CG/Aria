#!/usr/bin/env bash
# exp3.sh HOOK BASH : hook under a controlling terminal (util-linux script), allow path and deadline path (sed shim stalls the job's first block text)
D=$(cd "$(dirname "$0")" && pwd); HOOK=$1; B=${2:-bash}
V=/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31
for c in benign-big stall-read; do
  st=$(mktemp -d); e=$(mktemp); r=$(mktemp)
  export SC_SHIM_STATE=$st SC_REAL_jq=$(command -v jq) SC_REAL_sed=$(command -v sed)
  if [[ $c == stall-read ]]; then export SC_DELAY_sed=10 PATH="$V/shim:$PATH"; fi
  taskset -c 0,1 nice -n 19 script -qefc "$B $D/wrap.sh $HOOK $D/in/$c.json $e $r" /dev/null >/dev/null 2>&1
  echo "$c: $(cat $r)  stderr_first_line: $(head -1 $e | cut -c1-90)  load=$(cut -d' ' -f1 /proc/loadavg)"
  rm -rf "$st" "$e" "$r"; unset SC_DELAY_sed
done
