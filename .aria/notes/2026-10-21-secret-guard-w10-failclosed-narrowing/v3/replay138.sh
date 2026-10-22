#!/usr/bin/env bash
# replay138.sh <instrumented v3 hook> <W1 list> <out.tsv>: real-traffic replay of the W10-oversize class (aggregates only; command text stays in $T/cmds)
H=$1; W1=$2; OUT=$3; T="${TRAFFIC_DIR:?}"; D="$(mktemp -d)"; trap 'rm -rf "$D"' EXIT
: > "$OUT"
cut -f1 "$W1" | while read -r n; do
  jq -Rs '{tool_name:"Bash",tool_input:{command:.}}' < "$T/cmds/$n.txt" > "$D/in.json"
  : > "$D/dbg"
  t0=$EPOCHREALTIME
  HOME="$D" SG_DBG="$D/dbg" timeout 60 env -u SECRET_GUARD_RAW_GATE -u CLAUDE_PROJECT_DIR bash "$H" < "$D/in.json" >/dev/null 2>"$D/err"; rc=$?
  t1=$EPOCHREALTIME
  kind=other; (( rc == 0 )) && kind=allow; (( rc == 124 )) && kind=killed60
  if (( rc == 2 )); then kind=block-other
    grep -q 'reads a secret-bearing source' "$D/err" && kind=finding
    grep -q 'has a line longer than' "$D/err" && kind=longline
    grep -q 'grows by more than' "$D/err" && kind=growth
    grep -q 'too large to scan' "$D/err" && ! grep -q 'grows by more than' "$D/err" && kind=oversize
    grep -qi 'time budget' "$D/err" && kind=timebudget
  fi
  fp=$(awk '$2=="firstpass-done"{print $1}' "$D/dbg"); rs=$(awk '$2=="relax_run-start"{print $1}' "$D/dbg"); rj=$(awk '$2=="relax_run-joined"{print $1}' "$D/dbg")
  awk -v n=$n -v rc=$rc -v k=$kind -v a=${t0/,/.} -v b=${t1/,/.} -v fp="${fp/,/.}" -v rs="${rs/,/.}" -v rj="${rj/,/.}" 'BEGIN{
    printf "%s\t%s\t%s\t%.3f\t%s\t%s\t%s\n", n, rc, k, b-a, (fp==""?"-":sprintf("%.3f",fp-a)), (rs==""?"-":sprintf("%.3f",rs-a)), (rj==""||rs==""?"-":sprintf("%.3f",rj-rs)) }' >> "$OUT"
done
