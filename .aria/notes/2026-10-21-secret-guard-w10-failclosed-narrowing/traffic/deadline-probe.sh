#!/bin/bash
# deadline-probe.sh <hook> <helper> [envcase] -- drive the pinned helper (deadline-helper.sh) with the REAL judgement of <hook>: _sg_judge_one, _sg_compute_credit,
# risky_patterns, _sg_emit_blocked. Shapes from the R1 audit (backend-architect exp4: k lines of one 8000-character token, then a read). Prints status, wall time and
# the first line of the block text only. Base _sg_judge_one ignores the 3rd argument (nocredit), so this shows the deadline, not posture C.
HOOK=${1:?usage: deadline-probe.sh <hook> <helper> [envcase]}; HELPER=${2:?}
source "$HOOK"
eval "$(awk '/^declare -a risky_patterns=\(/,/^\)$/' "$HOOK")"
eval "$(awk '/^_sg_redact_echo\(\) \{/,/^\}$/' "$HOOK")"
eval "$(awk '/^_sg_judge_one\(\) \{/,/^\}$/' "$HOOK")"
source "$HELPER"
_SGV_LMAX=8192; command="(probe)"; TMPE=$(mktemp)
now() { date +%s.%N; }
el() { awk -v a="$1" -v b="$2" 'BEGIN{printf "%.2f", b-a}'; }
p1='~/.a'; p2='ws/cre'; p3='dentials'; CRED="${p1}${p2}${p3}"     # assembled at run time: the session's own guard matches the literal
line="$(printf 'a%.0s' $(seq 1 8000))"
shape() { local k=$1 tail=$2 body=": \$(:)" i; for (( i = 0; i < k; i++ )); do body="$body"$'\n'"$line"; done; printf '%s' "$body"$'\n'"$tail"; }
run() {   # <label> <budget> <copy>
  local t0 t1 rc first
  _SG_TIME_BUDGET=$2; _SG_P0=$SECONDS
  t0=$(now); _sg_vx_big "$3" whole 2>"$TMPE"; rc=$?; t1=$(now)
  first=$(head -1 "$TMPE" | cut -c1-90)
  echo "  $1: rc=$rc wall=$(el $t0 $t1)s stderr_lines=$(wc -l < "$TMPE" | tr -d ' ') first=[$first]"
}
echo "bash $BASH_VERSION"
if [[ "${3:-}" == envcase ]]; then
  echo "  (started with SECONDS imported from the environment: SECONDS=$SECONDS at probe start)"
  run "benign k=5 under an imported SECONDS, budget 3 (an absolute-SECONDS deadline would have left=$(( 3 - SECONDS )))" 3 "$(shape 5 'cat /tmp/notes.txt')"
  rm -f "$TMPE"; exit 0
fi
run "read k=5 (40 KB; judgement alone > 5 s), budget 3 -> killed" 3 "$(shape 5 "cat $CRED")"
run "benign k=5 (no row hit), budget 3" 3 "$(shape 5 'cat /tmp/notes.txt')"
run "read k=1 (8 KB; judged in time), budget 3 -> block text passed through" 3 "$(shape 1 "cat $CRED")"
run "read k=5, budget 0 -> no time left, nothing forked" 0 "$(shape 5 "cat $CRED")"
sleep() { return 127; }
run "read k=5, budget 3, sleep fails -> timer kills at once (fail-closed)" 3 "$(shape 5 "cat $CRED")"
unset -f sleep
rm -f "$TMPE"
