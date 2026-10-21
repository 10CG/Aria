#!/usr/bin/env bash
# For every command the R1 gate blocked (gate.tsv rc=2): run the BASE hook (v1.76.1) as a process, timeout 150 s -> base.tsv: n base_rc base_seconds bytes
B="$1"; T="${TRAFFIC_DIR:-/tmp/r1traffic}"   # holds cmds/ (real command text): keep OUTSIDE the repo; D="$(mktemp -d)"; trap 'rm -rf "$D"' EXIT
: > "$T/base.tsv"
awk -F'\t' '$2==2 {print $1"\t"$4}' "$T/gate.tsv" | while IFS=$'\t' read -r n bytes; do
  jq -Rs '{tool_name:"Bash",tool_input:{command:.}}' < "$T/cmds/$n.txt" > "$D/in.json"
  t0=$EPOCHREALTIME
  HOME="$D" timeout 150 env -u SECRET_GUARD_RAW_GATE -u CLAUDE_PROJECT_DIR "$B" < "$D/in.json" >/dev/null 2>"$D/err"; rc=$?
  t1=$EPOCHREALTIME
  kind=other; grep -q 'reads a secret-bearing source' "$D/err" && kind=finding; grep -q 'too large to scan' "$D/err" && kind=oversize; grep -q 'time budget' "$D/err" && kind=timebudget; (( rc == 0 )) && kind=allow; (( rc == 124 )) && kind=killed
  printf '%s\t%s\t%s\t%s\t%s\n' "$n" "$rc" "$(awk -v a=$t0 -v b=$t1 'BEGIN{printf "%.2f", b-a}')" "$bytes" "$kind" >> "$T/base.tsv"
done
