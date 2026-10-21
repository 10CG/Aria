#!/usr/bin/env bash
# Base hook (v1.76.1) over EVERY extracted real command (> 4096 bytes), as a process, timeout 60 s -> base-all.tsv: n rc seconds bytes kind
#   kind: allow | finding | oversize | timebudget | killed (>60 s) | other
B="$1"; T="${TRAFFIC_DIR:-/tmp/r1traffic}"; D="$(mktemp -d)"; trap 'rm -rf "$D"' EXIT
: > "$T/base-all.tsv"
while IFS=$'\t' read -r n proj bytes; do
  jq -Rs '{tool_name:"Bash",tool_input:{command:.}}' < "$T/cmds/$n.txt" > "$D/in.json"
  t0=$EPOCHREALTIME
  HOME="$D" timeout 60 env -u SECRET_GUARD_RAW_GATE -u CLAUDE_PROJECT_DIR "$B" < "$D/in.json" >/dev/null 2>"$D/err"; rc=$?
  t1=$EPOCHREALTIME
  kind=other; (( rc == 0 )) && kind=allow; (( rc == 124 )) && kind=killed
  if (( rc == 2 )); then kind=block-other; grep -q 'reads a secret-bearing source' "$D/err" && kind=finding; grep -q 'too large to scan' "$D/err" && kind=oversize; grep -qi 'time budget' "$D/err" && kind=timebudget; fi
  printf '%s\t%s\t%s\t%s\t%s\n' "$n" "$rc" "$(awk -v a=$t0 -v b=$t1 'BEGIN{printf "%.2f", b-a}')" "$bytes" "$kind" >> "$T/base-all.tsv"
done < "$T/index.tsv"
