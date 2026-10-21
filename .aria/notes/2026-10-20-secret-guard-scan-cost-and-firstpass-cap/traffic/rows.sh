#!/usr/bin/env bash
# Print risky_patterns rows by index (hook text, not command text), the per-class row counts, and shape statistics of selected commands (counts only).
N="$1"; T="${TRAFFIC_DIR:-/tmp/r1traffic}"   # holds cmds/ (real command text): keep OUTSIDE the repo; D="$(mktemp -d)"; trap 'rm -rf "$D"' EXIT
export HOME="$D"; source "$N"; unset input
awk '/^declare -a risky_patterns=\(/,/^\)$/' "$N" > "$D/rp.sh"; source "$D/rp.sh"
echo "rows by class (gate row: original, else spaced):"
awk -F'\t' '{r=($3>0?$3:$4); print $6"\t"r}' "$T/classes.tsv" | sort | uniq -c | sort -k2,2 -k1,1rn | while read -r c cls r; do printf '  %-9s row %-4s x%-3s %.110s\n' "$cls" "$r" "$c" "${risky_patterns[$((r-1))]}"; done
for n in 630; do
  IFS= read -r -d '' s < "$T/cmds/$n.txt"
  semi="${s//[^;]/}"; nl="${s//[^$'\n']/}"; pipe="${s//[^|]/}"; amp="${s//[^&]/}"
  printf 'n=%s bytes=%s lines=%s semicolons=%s pipes=%s amps=%s\n' "$n" "$(LC_ALL=C; printf %s "${#s}")" "$(( ${#nl} + 1 ))" "${#semi}" "${#pipe}" "${#amp}"
  i=0; for p in "${risky_patterns[@]}"; do i=$((i+1)); [[ "$s" =~ $p ]] && { printf '  first base-visible row %s: %.110s\n' "$i" "$p"; break; }; done
done
