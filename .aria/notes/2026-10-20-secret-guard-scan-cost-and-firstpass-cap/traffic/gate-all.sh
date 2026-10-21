#!/usr/bin/env bash
# In-process R1 gate (_sg_pregate, default gate, no project extension) over every extracted command -> gate.tsv: n rc seconds bytes
H="$1"; T="${TRAFFIC_DIR:-/tmp/r1traffic}"   # holds cmds/ (real command text): keep OUTSIDE the repo; D="$(mktemp -d)"; trap 'rm -rf "$D"' EXIT; export HOME="$D"
source "$H"; awk '/^declare -a risky_patterns=\(/,/^\)$/' "$H" > "$D/rp.sh"; source "$D/rp.sh"
unset SECRET_GUARD_RAW_GATE CLAUDE_PROJECT_DIR input
: > "$T/gate.tsv"
while IFS=$'\t' read -r n proj bytes; do
  IFS= read -r -d '' command < "$T/cmds/$n.txt"
  t0=$EPOCHREALTIME; _sg_pregate "$command" >/dev/null 2>&1; rc=$?; t1=$EPOCHREALTIME
  printf '%s\t%s\t%s\t%s\n' "$n" "$rc" "$(awk -v a=$t0 -v b=$t1 'BEGIN{printf "%.3f", b-a}')" "$bytes" >> "$T/gate.tsv"
done < "$T/index.tsv"
