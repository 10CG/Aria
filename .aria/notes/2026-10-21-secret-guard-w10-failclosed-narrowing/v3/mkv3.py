#!/usr/bin/env python3
"""Generate the #217 v3 prototype hook from the baseline hook. Every replacement must hit exactly once."""
import sys
src, dst = sys.argv[1], sys.argv[2]
t = open(src, encoding='utf-8').read()

def rep(old, new):
    global t
    n = t.count(old)
    if n != 1:
        sys.exit(f'replacement hit {n} times: {old[:70]!r}')
    t = t.replace(old, new)

# 1. anchor of the hard deadline: the hook start
rep('set -uo pipefail   # NOT -e — we control exit codes\n',
    'set -uo pipefail   # NOT -e — we control exit codes\n'
    '_SG_P0=${EPOCHREALTIME:-}   # #217: hook-start anchor of the relaxed rerun\'s hard deadline (empty under a bash without EPOCHREALTIME: no relaxation)\n')

# 2. constants
rep('_SGV_TMAX=65536\n',
    '_SGV_TMAX=65536\n'
    '_SGV_GMAX=8192   # #217 relaxed rerun: a copy may grow by at most this many characters over its input\n'
    '_SGV_LMAX=8192   # #217 relaxed rerun: a copy over _SGV_SMAX whose longest line is longer than this is matched against the rows only (nocredit)\n')

# 3. _sg_vx_apply: growth limit inside the relaxed rerun
rep('  local s="$1" i n v m tail pre out guard changed=1\n  _SG_SUB="$s"\n',
    '  local s="$1" i n v m tail pre out guard changed=1 lim=$_SGV_SMAX\n'
    '  [[ -n "${_SG_RELAXED:-}" ]] && lim=$(( ${#1} + _SGV_GMAX ))   # #217 relaxed rerun: the limit is the growth over the input (${#1}: s is rewritten below)\n'
    '  _SG_SUB="$s"\n')
rep('_sg_vx_replace "$s" "\\${$n}" "$v" "$_SGV_SMAX" || return 2',
    '_sg_vx_replace "$s" "\\${$n}" "$v" "$lim" || return 2')
rep('      (( ${#out} + ${#s} > _SGV_SMAX )) && return 2\n',
    '      (( ${#out} + ${#s} > lim )) && return 2\n')

# 4. _sg_vx_pass
R = '[[ -n "${_SG_RELAXED:-}" ]] && return 3   # #217 relaxed rerun: no time text of its own, the caller falls back to the baseline block\n'
rep('  if [[ $cr -eq 3 ]]; then   # time-budget fail-closed: the chaining in _sg_vx_collect ran out of time\n',
    '  if [[ $cr -eq 3 ]]; then   # time-budget fail-closed: the chaining in _sg_vx_collect ran out of time\n    ' + R)
rep('    if _sg_over_budget; then   # time-budget fail-closed before the O(copy^2) whole-command judgement\n',
    '    if _sg_over_budget; then   # time-budget fail-closed before the O(copy^2) whole-command judgement\n      ' + R)
rep('    if _sg_over_budget; then   # time-budget fail-closed before each per-segment _sg_vx_apply / _sg_judge_one (the O(copy^2) hot leg)\n',
    '    if _sg_over_budget; then   # time-budget fail-closed before each per-segment _sg_vx_apply / _sg_judge_one (the O(copy^2) hot leg)\n      ' + R)
rep('''    if [[ $ar -eq 2 ]]; then
      _sg_emit_blocked "the command is longer than $_SGV_SMAX characters after variable expansion" "$cmd" whole oversize
      return 2
    fi
    if [[ $ar -eq 0 ]]; then _sg_judge_one "$_SG_SUB" whole; return $?; fi
''', '''    if [[ $ar -eq 2 ]]; then
      if [[ -n "${_SG_RELAXED:-}" ]]; then
        _sg_emit_blocked "the command grows by more than $_SGV_GMAX characters after variable expansion" "$cmd" whole oversize
        return 2
      fi
      if _sg_relax_ok; then _SG_OV_PAT="the command is longer than $_SGV_SMAX characters after variable expansion"; _SG_OV_MODE=whole; return 4; fi
      _sg_emit_blocked "the command is longer than $_SGV_SMAX characters after variable expansion" "$cmd" whole oversize
      return 2
    fi
    if [[ $ar -eq 0 ]]; then
      if [[ -n "${_SG_RELAXED:-}" ]] && (( ${#_SG_SUB} > _SGV_SMAX )); then _sg_vx_big_judge "$_SG_SUB" whole; return $?; fi
      _sg_judge_one "$_SG_SUB" whole; return $?
    fi
''')
rep('''    if [[ $ar -eq 2 ]]; then
      _sg_emit_blocked "a command segment is longer than $_SGV_SMAX characters after variable expansion" "$cmd" segment oversize
      return 2
    fi
''', '''    if [[ $ar -eq 2 ]]; then
      if [[ -n "${_SG_RELAXED:-}" ]]; then
        _sg_emit_blocked "a command segment grows by more than $_SGV_GMAX characters after variable expansion" "$cmd" segment oversize
        return 2
      fi
      if _sg_relax_ok; then _SG_OV_PAT="a command segment is longer than $_SGV_SMAX characters after variable expansion"; _SG_OV_MODE=segment; return 4; fi
      _sg_emit_blocked "a command segment is longer than $_SGV_SMAX characters after variable expansion" "$cmd" segment oversize
      return 2
    fi
''')
rep('''    _sg_judge_one "$_SG_SUB" segment
    rc=$?
''', '''    if [[ -n "${_SG_RELAXED:-}" ]] && (( ${#_SG_SUB} > _SGV_SMAX )); then _sg_vx_big_judge "$_SG_SUB" segment; else _sg_judge_one "$_SG_SUB" segment; fi
    rc=$?
''')

# 5. new functions, right after _sg_vx_pass (above the sourcing gate)
NEW = r'''
# #217 relaxed rerun. When the relaxation is in effect (_sg_relax_ok), a copy over _SGV_SMAX is not blocked for its size alone: _sg_vx_pass returns 4 instead
# and keeps the baseline block text in _SG_OV_PAT / _SG_OV_MODE, and _sg_per_segment_eval re-runs the W10 pass with the relaxed rules (_SG_RELAXED: the copy
# limit is the growth over the input, _SGV_GMAX; a copy over _SGV_SMAX is judged in full, _sg_vx_big_judge) in a background job under a HARD deadline:
# _SG_P0 (hook start) + min(_SG_TIME_BUDGET, 3) s. The job leads its own process group (set -m) and the deadline kills the whole group, so no child of the
# judgement outlives it. Its verdict is its exit status, never parsed from text: 0 allows, 2 blocks with the job's own text; any other outcome -- the
# deadline, a time checkpoint, the self-check, an internal error -- falls back to the baseline block, byte for byte. In effect only on Linux, under a bash
# with EPOCHREALTIME (5.0+), with no project extension in effect (with one, the extension blocks a copy over _SGV_SMAX by its own absolute limit anyway),
# and with time left before the deadline.
_sg_vx_big_judge() {   # COPY MODE: the longest line (one linear read loop) routes the copy -- longer than _SGV_LMAX: rows only, no credit; otherwise the normal judgement
  local line max=0
  while IFS= read -r line; do (( ${#line} > max )) && max=${#line}; done <<< "$1"
  if (( max > _SGV_LMAX )); then _sg_judge_one "$1" "$2" nocredit; else _sg_judge_one "$1" "$2"; fi
}
_sg_relax_left() {   # sets _SG_LEFT to the time left before the deadline, as seconds with 6 decimals; status 1 when there is no anchor or no time left
  local now p0 cap
  [[ -n "${_SG_P0:-}" && -n "${EPOCHREALTIME:-}" ]] || return 1
  _sg_time_budget
  now=${EPOCHREALTIME/[.,]/}; p0=${_SG_P0/[.,]/}
  [[ "$now" =~ ^[0-9]+$ && "$p0" =~ ^[0-9]+$ ]] || return 1
  cap=$(( _SG_TIME_BUDGET < 3 ? _SG_TIME_BUDGET : 3 ))
  now=$(( 10#$p0 + cap * 1000000 - 10#$now ))
  (( now > 0 )) || return 1
  printf -v _SG_LEFT '%d.%06d' $(( now / 1000000 )) $(( now % 1000000 ))
}
_sg_relax_ok() {   # status 0 when the relaxation is in effect for this command; the extension is asked inside a command substitution, like every extension call
  [[ -z "${_SG_RELAXED:-}" && "${OSTYPE:-}" == linux* ]] || return 1
  _sg_relax_left || return 1
  [[ -z "$( _sg_ext_entries 2>/dev/null )" ]]
}
_sg_relax_job() {   # CMD: body of the background job; refuses to judge (status 9) unless it leads its own process group, which is what the deadline kills
  local st f
  { IFS= read -r st < "/proc/$BASHPID/stat"; } 2>/dev/null || return 9
  st="${st##*) }"; f=( $st )
  [[ "${f[2]:-}" == "$BASHPID" ]] || return 9
  _SG_RELAXED=1
  _sg_vx_pass "$1" "$_SG_MODE"
}
_sg_relax_run() {   # CMD: status 0 = allowed, 2 = blocked (the job's text is on stderr), 4 = fall back to the baseline block
  local out rc
  _sg_relax_left || return 4
  out="$( set -m
          _sg_relax_job "$1" 2>&1 </dev/null &
          jp=$!
          ( sleep "$_SG_LEFT"; kill -KILL -- "-$jp" ) >/dev/null 2>&1 </dev/null &
          tp=$!
          [[ "$tp" != "$jp" ]] || { kill -KILL -- "-$jp"; exit 99; }
          wait "$jp" 2>/dev/null; r=$?
          kill -KILL -- "-$tp" >/dev/null 2>&1
          exit "$r" )" 2>/dev/null
  rc=$?
  [[ $rc -eq 0 ]] && return 0
  [[ $rc -eq 2 && -n "$out" ]] && { printf '%s\n' "$out" >&2; return 2; }
  return 4
}
'''
rep('\n# W9 -- project-level extension <project root>/.aria/secret-guard.paths:',
    NEW + '\n# W9 -- project-level extension <project root>/.aria/secret-guard.paths:')

# 6. _sg_judge_one nocredit
rep('  local seg="$1" mode="$2" pat\n  local credit="" subj="$1" _w\n',
    '  local seg="$1" mode="$2" pat nocredit="${3:-}"\n  local credit="" subj="$1" _w\n')
rep('''    if [[ "$subj" =~ $pat ]]; then
      if [[ -z "$credit" ]]; then''', '''    if [[ "$subj" =~ $pat ]]; then
      if [[ "$nocredit" == nocredit ]]; then   # #217: a big copy with a line longer than _SGV_LMAX -- the match alone blocks, credit is not evaluated
        _sg_emit_blocked "$pat" "$seg" "$mode" longline
        return 2
      fi
      if [[ -z "$credit" ]]; then''')

# 7. longline template
LONG = '''  if [[ "$kind" == longline ]]; then
    cat >&2 <<EOF
[secret-guard] BLOCKED: command reads a secret-bearing source, and after variable
expansion it has a line longer than ${_SGV_LMAX} characters. Matched pattern: $pat

At this size the guard does not look for value-REDACTING filters (| jq 'keys',
| wc -c, >/dev/null, ...): on a line this long that check alone is too slow to
finish within the hook's time limit, so the match alone blocks the command
(fail-closed).

Split it into smaller commands and run them one at a time:
  - keep every variable value, and every command after expansion, short;
  - write long files with the Write / Edit tool instead of a heredoc.
命令读取含密钥的来源, 且变量展开后有超长的行, 这个尺寸下不评估脱敏过滤, 请拆成更小的命令

Command was (first 200 characters): $(_sg_redact_echo "${command:0:200}")
EOF
    return 0
  fi
'''
rep('''    return 0
  fi
  cat >&2 <<EOF
[secret-guard] BLOCKED: command reads a secret-bearing source without a
''', '''    return 0
  fi
''' + LONG + '''  cat >&2 <<EOF
[secret-guard] BLOCKED: command reads a secret-bearing source without a
''')

# 8. _sg_per_segment_eval: the relaxed rerun
rep('''    _sg_vx_pass "$cmd" "$_SG_MODE"
    rc=$?
    [[ $rc -ne 0 ]] && return "$rc"
''', '''    _sg_vx_pass "$cmd" "$_SG_MODE"
    rc=$?
    if [[ $rc -eq 4 ]]; then   # #217: a copy over _SGV_SMAX and the relaxation is in effect -> the relaxed rerun decides; any failure falls back to the baseline block
      _sg_relax_run "$cmd"
      rc=$?
      [[ $rc -eq 4 ]] && { _sg_emit_blocked "$_SG_OV_PAT" "$cmd" "$_SG_OV_MODE" oversize; return 2; }
      return "$rc"   # 0 also skips the extension look below: the relaxation is in effect only when no extension is
    fi
    [[ $rc -ne 0 ]] && return "$rc"
''')

open(dst, 'w', encoding='utf-8').write(t)
print('ok', len(t))
