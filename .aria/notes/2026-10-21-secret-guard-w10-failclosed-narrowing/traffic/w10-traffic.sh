#!/usr/bin/env bash
# #217 A.1 evidence: for every real command the BASE hook blocked with the W10 size text (E12 kind=oversize), classify in process (sourced base hook):
#   mode (whole/segment), collect rc (0 ok / 2 value>VMAX / 3 time), which value overran (assignment vs for-list; for-list spanning a newline; referenced or not),
#   and, with the size budgets lifted, the real expansion: subject length, expanded length, growth, and the time to judge the expanded copy (what allowing it would cost).
#   output: w10.tsv  n bytes mode crc why longval_kind longval_spans_nl longval_referenced subj_len exp_len growth judge_s judge_rc
B="$1"; T="${TRAFFIC_DIR:-/tmp/r1traffic}"; D="$(mktemp -d)"; trap 'rm -rf "$D"' EXIT; export HOME="$D"
source "$B"
awk '/^declare -a risky_patterns=\(/,/^\)$/' "$B" > "$D/rp.sh"; source "$D/rp.sh"
awk '/^_sg_judge_one\(\) \{/,/^\}$/' "$B" > "$D/j.sh"; source "$D/j.sh"
unset SECRET_GUARD_RAW_GATE CLAUDE_PROJECT_DIR input
command=""
: > "$T/w10.tsv"
awk -F'\t' '$5=="oversize" {print $1}' "$T/base-all.tsv" | while read -r n; do
  IFS= read -r -d '' cmd < "$T/cmds/$n.txt"; command="$cmd"
  if _sg_safe_to_split "$cmd"; then mode=segment; _sg_split_top "$cmd"; else mode=whole; _SG_SEGS=("$cmd"); fi
  _SGV_VMAX=4096; _SGV_SMAX=8192
  _sg_vx_collect "$cmd"; crc=$?
  lk=-; lnl=-; lref=-
  if (( crc == 2 )); then
    # find the overrunning value: re-run the two collectors' regexes ourselves on assignments / for-lists, longest value > 4096
    lk=unknown
    rf="(^|[;&|[:space:](])for[[:space:]]+([A-Za-z_][A-Za-z0-9_]*)[[:space:]]+in[[:space:]]+([^;&|)]*)"
    if [[ "$cmd" =~ $rf ]] && (( ${#BASH_REMATCH[3]} > 4096 )); then lk=for-list; v="${BASH_REMATCH[3]}"; nm="${BASH_REMATCH[2]}"
      [[ "$v" == *$'\n'* ]] && lnl=yes || lnl=no
    else lk=assignment; nm=""; fi
    if [[ -n "${nm:-}" ]]; then [[ "$cmd" == *"\$$nm"* || "$cmd" == *"\${$nm}"* ]] && lref=yes || lref=no; fi
  fi
  # lift the budgets and measure the real expansion and the judgement cost of the expanded copies
  _SGV_VMAX=100000000; _SGV_SMAX=100000000
  _sg_vx_collect "$cmd" >/dev/null 2>&1
  subj=0; exp=0; jt=0; jrc=0
  for s in "${_SG_SEGS[@]}"; do
    subj=$(( subj + ${#s} ))
    if _sg_vx_apply "$s"; then e="$_SG_SUB"; else e="$s"; fi
    exp=$(( exp + ${#e} ))
    t0=$EPOCHREALTIME; _sg_judge_one "$e" "$mode" >/dev/null 2>&1; r=$?; t1=$EPOCHREALTIME
    jt=$(awk -v a="$jt" -v x=$t0 -v y=$t1 'BEGIN{printf "%.3f", a + (y-x)}'); (( r > jrc )) && jrc=$r
  done
  why=size; (( crc == 2 )) && why=value; (( crc == 3 )) && why=time
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$n" "$(LC_ALL=C; printf %s "${#cmd}")" "$mode" "$crc" "$why" "$lk" "$lnl" "$lref" "$subj" "$exp" "$(( exp - subj ))" "$jt" "$jrc" >> "$T/w10.tsv"
done
