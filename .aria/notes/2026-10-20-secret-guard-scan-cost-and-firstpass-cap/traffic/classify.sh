#!/usr/bin/env bash
# Classify each base-ALLOWED gate-blocked command: why does the gate block what the base allows?
#   whole/segment = base core mode; orig/sp = gate hit on the neutralized original / only on the spaced copy; segrow = some single segment matches a row (no credit)
#   class: credit (a) | cross-segment (b) | spaced-copy (c)
B="$1"; N="$2"; T="${TRAFFIC_DIR:-/tmp/r1traffic}"   # holds cmds/ (real command text): keep OUTSIDE the repo; D="$(mktemp -d)"; trap 'rm -rf "$D"' EXIT; export HOME="$D"
source "$N"; awk '/^declare -a risky_patterns=\(/,/^\)$/' "$N" > "$D/rp.sh"; source "$D/rp.sh"
unset SECRET_GUARD_RAW_GATE CLAUDE_PROJECT_DIR input
firstrow() { local s="$1" i=0 p; for p in "${risky_patterns[@]}"; do i=$((i+1)); [[ "$s" =~ $p ]] && { echo "$i"; return 0; }; done; echo 0; return 1; }
: > "$T/classes.tsv"
awk -F'\t' '$5=="allow" {print $1}' "$T/base.tsv" | while read -r n; do
  IFS= read -r -d '' cmd < "$T/cmds/$n.txt"
  _sg_environ_neutral "$cmd"; neut="$_SG_NEUT"
  orow=$(firstrow "$neut")
  sp="$(printf '%s\n' "$neut" | LC_ALL=C sed 's/[;&|)`]/ &/g'; printf x)"; sp="${sp%x}"; sp="${sp%$'\n'}"
  srow=$(firstrow "$sp")
  if _sg_safe_to_split "$cmd"; then mode=segment; _sg_split_top "$cmd"; segrow=0
    for s in "${_SG_SEGS[@]}"; do _sg_environ_neutral "$s"; r=$(firstrow "$_SG_NEUT"); if (( r > 0 )); then segrow=$r; break; fi; done
  else mode=whole; segrow=$orow; fi
  if (( orow == 0 )); then cls=c-spaced; elif (( segrow > 0 )); then cls=a-credit; else cls=b-cross; fi
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$n" "$mode" "$orow" "$srow" "$segrow" "$cls" >> "$T/classes.tsv"
done
