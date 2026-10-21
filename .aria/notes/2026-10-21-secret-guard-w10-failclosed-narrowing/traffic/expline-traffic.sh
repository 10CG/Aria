#!/usr/bin/env bash
# #217 A.1: longest LINE of each EXPANDED copy (what _sg_compute_credit's per-line cost depends on) for the real W10-oversize commands -> expline.tsv: n max_line_of_copies
B="$1"; T="${TRAFFIC_DIR:-/tmp/r1traffic}"; D="$(mktemp -d)"; trap 'rm -rf "$D"' EXIT; export HOME="$D"
source "$B"; unset SECRET_GUARD_RAW_GATE CLAUDE_PROJECT_DIR input
: > "$T/expline.tsv"
awk -F'\t' '$5=="oversize" {print $1}' "$T/base-all.tsv" | while read -r n; do
  IFS= read -r -d '' cmd < "$T/cmds/$n.txt"
  if _sg_safe_to_split "$cmd"; then _sg_split_top "$cmd"; else _SG_SEGS=("$cmd"); fi
  _SGV_VMAX=100000000; _SGV_SMAX=100000000; _sg_vx_collect "$cmd" >/dev/null 2>&1
  m=0
  for s in "${_SG_SEGS[@]}"; do
    if _sg_vx_apply "$s"; then e="$_SG_SUB"; else e="$s"; fi
    l=$(printf '%s\n' "$e" | awk '{ if (length($0) > m) m = length($0) } END { print m+0 }'); (( l > m )) && m=$l
  done
  printf '%s\t%s\n' "$n" "$m" >> "$T/expline.tsv"
done
