# deadline-helper.sh -- the exact text proposal v2 pins for _sg_vx_big / _sg_vx_big_judge (#217); deadline-probe.sh sources this file, so the evidence runs the pinned code.
# _sg_vx_big COPY MODE -- #217: judge a copy longer than _SGV_SMAX under a hard deadline (owner posture B: a judgement that cannot finish in time BLOCKs).
# The judgement (_sg_vx_big_judge) runs as a background job inside a command substitution, and a timer job kills it with SIGKILL at the deadline: the time budget
# (_SG_TIME_BUDGET, capped at 3 s here) counted from the hook's start _SG_P0, so the first pass is inside it. Status: 0 allow; 2 blocked (the judgement's block text,
# captured and written here only after it finished, so a killed judgement never leaves a partial text); 3 out of time or no time left (nothing judged, the caller
# writes the time text); any other status of the judgement (an internal error) is returned as is and fails closed upstream.
_sg_vx_big() {
  local left out rc nl=$'\n'
  left=$(( (_SG_TIME_BUDGET < 3 ? _SG_TIME_BUDGET : 3) - (SECONDS - _SG_P0) ))
  (( left > 0 )) || return 3
  out="$( _sg_vx_big_judge "$1" "$2" 2>&1 &
          jp=$!
          ( sleep "$left"; kill -KILL "$jp" ) >/dev/null 2>&1 </dev/null &
          tp=$!
          wait "$jp" 2>/dev/null; r=$?
          kill -KILL "$tp" >/dev/null 2>&1
          printf '\n%s' "$r" )"
  rc="${out##*"$nl"}"; out="${out%"$nl"*}"
  [[ "$rc" =~ ^[0-9]+$ ]] || return 3
  (( rc >= 128 )) && return 3
  [[ -n "$out" ]] && printf '%s' "$out" >&2
  return "$rc"
}
# _sg_vx_big_judge COPY MODE -- runs inside the deadline: the longest line (one linear read loop) routes the copy -- longer than _SGV_LMAX: rows only, no credit
# (owner posture C, _sg_judge_one ... nocredit); otherwise the normal judgement with credit (owner posture A).
_sg_vx_big_judge() {
  local line max=0
  while IFS= read -r line; do (( ${#line} > max )) && max=${#line}; done <<< "$1"
  if (( max > _SGV_LMAX )); then _sg_judge_one "$1" "$2" nocredit; else _sg_judge_one "$1" "$2"; fi
}
