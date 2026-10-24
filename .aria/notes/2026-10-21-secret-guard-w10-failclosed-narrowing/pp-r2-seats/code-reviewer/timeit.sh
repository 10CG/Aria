#!/usr/bin/env bash
# timeit.sh HOOK SHAPE [n] : runs HOOK on in/SHAPE.json n times; prints wall, rc, stage times (s from call start)
H=$1; S=$2; N=${3:-3}; D=$(mktemp -d)
for ((k=0;k<N;k++)); do
  : > "$D/dbg"; t0=$EPOCHREALTIME
  SG_DBG="$D/dbg" env -u CLAUDE_PROJECT_DIR -u SECRET_GUARD_TIME_BUDGET_S taskset -c 0,1 nice -n 19 bash "$H" < "in/$S.json" >/dev/null 2>"$D/err"; rc=$?
  t1=$EPOCHREALTIME
  fp=$(awk '$2=="firstpass-done"{print $1}' "$D/dbg"); rs=$(awk '$2=="relax-start"{print $1}' "$D/dbg"); rj=$(awk '$2=="relax-joined"{print $1}' "$D/dbg")
  k2=$(grep -o 'has a line longer\|grows by more\|segments together\|too large to scan\|value-REDACTING filter' "$D/err" | head -1)
  awk -v a=$t0 -v b=$t1 -v fp="$fp" -v rs="$rs" -v rj="$rj" -v rc=$rc -v k="$k2" -v l="$(cut -d' ' -f1 /proc/loadavg)" 'BEGIN{printf "rc=%s wall=%.2f fp=%s rs=%s rj=%s kind=[%s] load=%s\n", rc, b-a, (fp==""?"-":sprintf("%.2f",fp-a)), (rs==""?"-":sprintf("%.2f",rs-a)), (rj==""?"-":sprintf("%.2f",rj-a)), k, l}'
done
rm -rf "$D"
