#!/usr/bin/env bash
# #217 A.1: for the real W10-oversize commands, does any risky_patterns row match the (W12-neutralized) EXPANDED copy, ignoring credit? (design: copies > _SGV_SMAX are row-matched only)
#   output: rowhit.tsv  n exp_len first_row_hit(0=none) seconds
B="$1"; T="${TRAFFIC_DIR:-/tmp/r1traffic}"; D="$(mktemp -d)"; trap 'rm -rf "$D"' EXIT; export HOME="$D"
source "$B"; awk '/^declare -a risky_patterns=\(/,/^\)$/' "$B" > "$D/rp.sh"; source "$D/rp.sh"
unset SECRET_GUARD_RAW_GATE CLAUDE_PROJECT_DIR input
# the W12 neutralization, byte-identical to the inline loops of the base _sg_judge_one (taken from the R1 snapshot, where it was extracted unchanged; differential 0/3031)
awk '/^_sg_environ_neutral\(\) \{/,/^\}$/' "${NEUT_SRC:?set NEUT_SRC to a hook that defines _sg_environ_neutral}" > "$D/neut.sh"; source "$D/neut.sh"
: > "$T/rowhit.tsv"
awk -F'\t' '$5=="oversize" {print $1}' "$T/base-all.tsv" | while read -r n; do
  IFS= read -r -d '' cmd < "$T/cmds/$n.txt"
  if _sg_safe_to_split "$cmd"; then _sg_split_top "$cmd"; else _SG_SEGS=("$cmd"); fi
  _SGV_VMAX=100000000; _SGV_SMAX=100000000; _sg_vx_collect "$cmd" >/dev/null 2>&1
  hit=0; len=0; t0=$EPOCHREALTIME
  for s in "${_SG_SEGS[@]}"; do
    if _sg_vx_apply "$s"; then e="$_SG_SUB"; else e="$s"; fi
    len=$(( len + ${#e} )); _sg_environ_neutral "$e"; i=0
    for p in "${risky_patterns[@]}"; do i=$((i+1)); if [[ "$_SG_NEUT" =~ $p ]]; then hit=$i; break; fi; done
    (( hit )) && break
  done
  t1=$EPOCHREALTIME
  printf '%s\t%s\t%s\t%s\n' "$n" "$len" "$hit" "$(awk -v a=$t0 -v b=$t1 'BEGIN{printf "%.3f", b-a}')" >> "$T/rowhit.tsv"
done
