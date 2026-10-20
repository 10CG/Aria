#!/usr/bin/env bash
# b1_fn_audit.sh HOOK INDIR REPS TOPN
# B.1 (secret-guard-scan-cost-and-firstpass-cap TASK-001): IN-PROCESS timing (no fork / process-start noise) of the two
# first-pass legs on ONE long line, per input file INDIR/<kind>_<shape>_<kb>.txt (written by b1_fn_audit.py):
#   kind=benign : the risky_patterns detection loop of _sg_judge_one (no hit expected: every pattern is scanned -- the cost
#                 every segment pays before any cap could act) + the TOPN slowest single patterns
#   kind=secret : _sg_compute_credit (the leg the cap short-circuits) + the TOPN slowest _sg_line_match regexes inside it
# Times in microseconds; min over REPS for the totals, the per-regex rows come from one extra pass.  bash >= 5 (EPOCHREALTIME)
# for the HARNESS only -- the hook is sourced unchanged.  Prints TSV rows; never prints an input or a pattern body (only its
# index in risky_patterns, or the first 60 characters of a credit regex, which are hook source text, not input).
set -u
HOOK=$1 INDIR=$2 REPS=${3:-3} TOPN=${4:-5}
source "$HOOK"                                                       # everything above the unit-test gate (:926 returns 0)
eval "$(sed -n '/^declare -a risky_patterns=(/,/^)/p' "$HOOK")"      # the pattern table lives below the gate
eval "$(declare -f _sg_line_match | sed '1s/^_sg_line_match/_sg_lm_orig/')"   # keep the original under a new name
declare -A LM_T=()
_sg_line_match() {                                                   # timing wrapper: accumulate per regex (fork-free clock)
  local a=${EPOCHREALTIME/./} rc b
  _sg_lm_orig "$@"; rc=$?
  b=${EPOCHREALTIME/./}
  LM_T["$1"]=$(( ${LM_T["$1"]:-0} + b - a ))
  return $rc
}

for f in "$INDIR"/*.txt; do
  S=$(<"$f"); lab=${f##*/}; lab=${lab%.txt}; kind=${lab%%_*}
  best=""
  if [[ $kind == benign ]]; then
    hit=-
    for ((r = 0; r < REPS; r++)); do
      a=${EPOCHREALTIME/./}
      i=0; hit=-
      for pat in "${risky_patterns[@]}"; do
        if [[ "$S" =~ $pat ]]; then hit=$i; break; fi
        i=$((i + 1))
      done
      b=${EPOCHREALTIME/./}; d=$((b - a))
      [[ -z $best || $d -lt $best ]] && best=$d
    done
    printf 'detect\t%s\t%s\thit=%s\tbytes=%s\n' "$lab" "$best" "$hit" "${#S}"
    i=0; rows=""
    for pat in "${risky_patterns[@]}"; do
      a=${EPOCHREALTIME/./}; [[ "$S" =~ $pat ]]; b=${EPOCHREALTIME/./}
      rows+="$((b - a))	$i"$'\n'; i=$((i + 1))
    done
    printf '%s' "$rows" | sort -rn | head -n "$TOPN" | while IFS=$'\t' read -r us idx; do
      printf 'detect-top\t%s\tpattern#%s\t%s\n' "$lab" "$idx" "$us"
    done
  else
    for ((r = 0; r < REPS; r++)); do
      a=${EPOCHREALTIME/./}; _sg_compute_credit "$S"; cr=$?; b=${EPOCHREALTIME/./}; d=$((b - a))
      [[ -z $best || $d -lt $best ]] && best=$d
    done
    printf 'credit\t%s\t%s\tcredit_rc=%s\tbytes=%s\n' "$lab" "$best" "$cr" "${#S}"
    LM_T=(); _sg_compute_credit "$S" >/dev/null
    for k in "${!LM_T[@]}"; do printf '%s\t%s\n' "${LM_T[$k]}" "${k:0:60}"; done | sort -rn | head -n "$TOPN" |
      while IFS=$'\t' read -r us re; do printf 'credit-top\t%s\t%s\t%s\n' "$lab" "$us" "$re"; done
  fi
done
