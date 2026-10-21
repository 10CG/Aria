#!/usr/bin/env bash
# b1_stage.sh HOOK FILE... : in-process time (us) of each first-pass stage on each input file, in the CURRENT locale.
# Stages: safe_to_split / split_top / detect (risky_patterns loop). bash>=5 EPOCHREALTIME for the harness only.
set -u
HOOK=$1; shift
source "$HOOK"
eval "$(sed -n '/^declare -a risky_patterns=(/,/^)/p' "$HOOK")"
for f in "$@"; do
  S=$(<"$f"); lab=${f##*/}; lab=${lab%.txt}
  a=${EPOCHREALTIME/./}; _sg_safe_to_split "$S"; s2s=$?; b=${EPOCHREALTIME/./}; t1=$((b-a))
  a=${EPOCHREALTIME/./}; _sg_split_top "$S"; b=${EPOCHREALTIME/./}; t2=$((b-a)); ns=${#_SG_SEGS[@]}
  a=${EPOCHREALTIME/./}; hit=-; i=0; for pat in "${risky_patterns[@]}"; do if [[ "$S" =~ $pat ]]; then hit=$i; break; fi; i=$((i+1)); done; b=${EPOCHREALTIME/./}; t3=$((b-a))
  printf '%s\t%s\tbytes=%s\tsafe_to_split=%sus(rc%s)\tsplit_top=%sus(segs=%s)\tdetect=%sus(hit=%s)\n' "${LC_ALL:-unset}" "$lab" "${#S}" "$t1" "$s2s" "$t2" "$ns" "$t3" "$hit"
done
