#!/usr/bin/env bash
# b1_detect.sh HOOK FILE... : CPU time (user+sys, `time` builtin -- works on bash 3.2) of the risky_patterns detection loop
# alone on each input file (the loop _sg_judge_one runs per segment; a pre-scan gate would run it once on the raw command).
# Prints label, bytes, cpu, index of the first hit (- = none). Never prints an input or a pattern body.
HOOK=$1; shift
source "$HOOK"
eval "$(sed -n '/^declare -a risky_patterns=(/,/^)/p' "$HOOK")"
TIMEFORMAT='%3U+%3S'
for f in "$@"; do
  S=$(<"$f")
  t=$( { time { hit=-; i=0; for pat in "${risky_patterns[@]}"; do if [[ "$S" =~ $pat ]]; then hit=$i; break; fi; i=$((i+1)); done; echo "$hit" > "$f.hit"; } ; } 2>&1 )
  printf 'bash-%s\t%s\tbytes=%s\tdetect_cpu=%ss\thit=%s\n' "$BASH_VERSION" "${f##*/}" "${#S}" "$t" "$(cat "$f.hit")"
  rm -f "$f.hit"
done
