#!/usr/bin/env python3
"""mkv31.py <baseline hook> <out>: generate the 10CG/aria-plugin#217 v3.1 prototype hook from the baseline hook (aria 59e333c, sha256 prefix e83c5e30f2cc).
Every replacement must hit exactly once; the baseline is checked by hash first."""
import sys, hashlib
src, dst = sys.argv[1], sys.argv[2]
t = open(src, encoding='utf-8').read()
if hashlib.sha256(t.encode('utf-8')).hexdigest()[:12] != 'e83c5e30f2cc':
    sys.exit('not the baseline hook (sha256 prefix e83c5e30f2cc expected)')

def rep(old, new):
    global t
    n = t.count(old)
    if n != 1:
        sys.exit(f'replacement hit {n} times: {old[:70]!r}')
    t = t.replace(old, new)

# 1. anchor of the hard deadline: the hook start
rep('set -uo pipefail   # NOT -e — we control exit codes\n',
    'set -uo pipefail   # NOT -e — we control exit codes\n'
    '_SG_P0=${EPOCHREALTIME:-}; _SG_RELAXED=   # 10CG/aria-plugin#217: hook-start anchor of the relaxed rerun\'s hard deadline (empty under a bash without EPOCHREALTIME: no relaxation); _SG_RELAXED is never taken from the environment\n')

# 2. constants
rep('_SGV_TMAX=65536\n',
    '_SGV_TMAX=65536\n'
    '_SGV_GMAX=8192   # 10CG/aria-plugin#217 relaxed rerun: a copy may grow by at most this many characters over its input\n'
    '_SGV_LMAX=8192   # 10CG/aria-plugin#217 relaxed rerun: a copy over _SGV_SMAX whose longest line is longer than this is matched against the rows only (nocredit)\n')

# 3. _sg_vx_apply: growth limit inside the relaxed rerun
rep('  local s="$1" i n v m tail pre out guard changed=1\n  _SG_SUB="$s"\n',
    '  local s="$1" i n v m tail pre out guard changed=1 lim=$_SGV_SMAX\n'
    '  [[ -n "${_SG_RELAXED:-}" ]] && lim=$(( ${#1} + _SGV_GMAX ))   # 10CG/aria-plugin#217 relaxed rerun: the limit is the growth over the input (${#1}: s is rewritten below)\n'
    '  _SG_SUB="$s"\n')
rep('_sg_vx_replace "$s" "\\${$n}" "$v" "$_SGV_SMAX" || return 2',
    '_sg_vx_replace "$s" "\\${$n}" "$v" "$lim" || return 2')
rep('      (( ${#out} + ${#s} > _SGV_SMAX )) && return 2\n',
    '      (( ${#out} + ${#s} > lim )) && return 2\n')

# 4. _sg_vx_pass
R = '[[ -n "${_SG_RELAXED:-}" ]] && return 3   # 10CG/aria-plugin#217 relaxed rerun: no time text of its own, the caller falls back to the baseline block\n'
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
# 10CG/aria-plugin#217 relaxed rerun. When the relaxation is in effect (_sg_relax_ok), a copy over _SGV_SMAX is not blocked for its size alone: _sg_vx_pass
# returns 4 instead and keeps the baseline block text in _SG_OV_PAT / _SG_OV_MODE, and _sg_per_segment_eval re-runs the W10 pass with the relaxed rules
# (_SG_RELAXED: the copy limit is the growth over the input, _SGV_GMAX; a copy over _SGV_SMAX is judged in full, _sg_vx_big_judge; the counts -- 16
# assignments, 8 for statements, 8 replacements per variable -- are not bounded, so every reference is expanded) in a background job under a HARD
# deadline: _SG_P0 (hook start) + min(_SG_TIME_BUDGET, 3) s. The job leads its own process group (set -m); its timer runs inside the group and is started
# before the first expensive step; the deadline kills the whole group, and so does _sg_relax_run once the job has ended, so nothing of the job outlives it
# or holds the pipe. The verdict is the job's exit status, never parsed from text: 77 allows, 2 blocks with the job's own text; any other outcome -- the
# deadline, a time checkpoint, the self-check, an internal error, a bare 0 -- falls back to the baseline block, byte for byte. In effect only on a Linux
# build of bash 5.0-5.3 on GNU/Linux (the versions and the platform measured), with no project extension in effect (with one, the extension blocks a copy over _SGV_SMAX by its own
# absolute limit anyway), and with time left before the deadline.
_sg_vx_big_judge() {   # COPY MODE: the longest line (one linear read loop) routes the copy -- longer than _SGV_LMAX: rows only, no credit; otherwise the normal judgement
  local line max=0 seen=0
  while IFS= read -r line; do seen=1; (( ${#line} > max )) && max=${#line}; done <<< "$1"
  (( seen )) || max=$(( _SGV_LMAX + 1 ))   # the length could not be measured: rows only, never the cheaper-to-pass credit path
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
  (( now > cap * 1000000 )) && now=$(( cap * 1000000 ))   # a clock that went backwards never extends the deadline
  printf -v _SG_LEFT '%d.%06d' $(( now / 1000000 )) $(( now % 1000000 ))
}
_sg_relax_ok() {   # status 0 when the relaxation is in effect for this command; the extension is asked inside a command substitution, like every extension call
  [[ -z "${_SG_RELAXED:-}" ]] || return 1
  _sg_relax_platform "${BASH_VERSINFO[5]:-}" "${BASH_VERSINFO[0]:-0}" "${BASH_VERSINFO[1]:-0}" || return 1   # read-only build facts, which the environment cannot rewrite (OSTYPE can be)
  _sg_relax_left || return 1
  [[ "$( _sg_relax_noext 2>/dev/null )" == none ]]
}
_sg_relax_platform() {   # MACHINE MAJOR MINOR: status 0 on a GNU/Linux build of a bash version the mechanism was measured on, 5.0 to 5.3 (owner ruling E: an untested platform -- macOS, Windows, musl, Android, another bash -- keeps the baseline)
  [[ "$1" == *-linux-gnu* ]] && (( ${2:-0} == 5 && ${3:-0} <= 3 ))
}
_sg_relax_noext() {   # prints "none" only when no extension can be in effect: no project root, or no .aria/secret-guard.paths under it. A file in any state, or an error, keeps the relaxation off
  local root
  root="$(_sg_ext_root)"
  if [[ -z "$root" || ! -e "$root/.aria/secret-guard.paths" ]]; then printf none; fi
}
_sg_relax_job() {   # CMD: body of the background job; refuses to judge (status 9) unless it leads its own process group, which is what the deadline kills
  local st f
  { IFS= read -r st < "/proc/$BASHPID/stat"; } 2>/dev/null || return 9
  st="${st##*) }"; f=( $st )
  [[ "${f[2]:-}" == "$BASHPID" ]] || return 9
  local me=$BASHPID tp
  ( sleep "$_SG_LEFT"; kill -KILL -- "-$me" ) >/dev/null 2>&1 </dev/null &
  tp=${!:-}
  [[ -n "$tp" ]] && kill -0 "$tp" 2>/dev/null || return 9   # no running timer, no judgement: the deadline must exist before the first expensive step
  _SG_RELAXED=1
  _sg_vx_pass "$1" "$_SG_MODE"
  case $? in 0) return 77 ;; 2) return 2 ;; *) return 1 ;; esac   # allow only as 77: a bare 0 reaching _sg_relax_run from anywhere else falls back
}
_sg_relax_run() {   # CMD: status 0 = allowed (the job exited 77), 2 = blocked (the job exited 2 with a text, now on stderr), 4 = fall back to the baseline block
  local out rc
  _sg_relax_left || return 4
  out="$( exec 2>/dev/null; set -m
          _sg_relax_job "$1" 2>&1 </dev/null &
          jp=${!:-}
          [[ -n "$jp" ]] || exit 99
          wait "$jp"; r=$?
          kill -KILL -- "-$jp"   # the timer and anything the judgement left behind: nothing of the job outlives it or holds the pipe
          exit "$r" )"
  rc=$?
  [[ $rc -eq 77 ]] && return 0
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
      if [[ "$nocredit" == nocredit ]]; then   # 10CG/aria-plugin#217: a big copy with a line longer than _SGV_LMAX -- the match alone blocks, credit is not evaluated
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
  - do not repeat one long \\$VAR many times in a single command;
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
    if [[ $rc -eq 4 ]]; then   # 10CG/aria-plugin#217: a copy over _SGV_SMAX and the relaxation is in effect -> the relaxed rerun decides; any failure falls back to the baseline block
      _sg_relax_run "$cmd"
      rc=$?
      [[ $rc -eq 4 ]] && { _sg_emit_blocked "$_SG_OV_PAT" "$cmd" "$_SG_OV_MODE" oversize; return 2; }
      return "$rc"   # 0 also skips the extension look below: the relaxation is in effect only when no extension is
    fi
    [[ $rc -ne 0 ]] && return "$rc"
''')

# 9. count bounds inside the relaxed rerun (post_planning R1 TL-F1): the bounds (16 assignments, 8 for statements, 8 replacements per variable) exist to cap the
#    cost of the baseline pass; inside the relaxed rerun the cost is capped by the hard deadline, the growth limit and TMAX, and every loop consumes its string,
#    so the rerun expands ALL assignments and references -- no reference past the 8th stays unexpanded and hides a read. The baseline path keeps its bounds.
rep('  local rest="$1" m name val i j n=0 dup pre\n',
    '  local rest="$1" m name val i j n=0 dup pre ca=16 cf=8\n'
    '  [[ -n "${_SG_RELAXED:-}" ]] && ca=1000000 cf=1000000   # 10CG/aria-plugin#217 relaxed rerun: no count bound (the deadline caps the cost)\n')
rep('  while (( n < 16 )) && [[ "$rest" =~ $re ]]; do\n', '  while (( n < ca )) && [[ "$rest" =~ $re ]]; do\n')
rep('  while (( n < 8 )) && [[ "$rest" =~ $rf ]]; do\n', '  while (( n < cf )) && [[ "$rest" =~ $rf ]]; do\n')
rep('  local s="$1" pat="$2" rep="$3" max="${4:-0}" out="" g=0 pre\n',
    '  local s="$1" pat="$2" rep="$3" max="${4:-0}" out="" g=0 pre gc=8\n'
    '  [[ -n "${_SG_RELAXED:-}" ]] && gc=1000000   # 10CG/aria-plugin#217 relaxed rerun: no count bound\n')
rep('  while (( g < 8 )) && [[ "$s" == *"$pat"* ]]; do\n', '  while (( g < gc )) && [[ "$s" == *"$pat"* ]]; do\n')
rep('  local s="$1" i n v m tail pre out guard changed=1 lim=$_SGV_SMAX\n',
    '  local s="$1" i n v m tail pre out guard changed=1 lim=$_SGV_SMAX gc=8\n')
rep('  [[ -n "${_SG_RELAXED:-}" ]] && lim=$(( ${#1} + _SGV_GMAX ))',
    '  [[ -n "${_SG_RELAXED:-}" ]] && lim=$(( ${#1} + _SGV_GMAX )) gc=1000000')
rep('    while (( guard < 8 )) && [[ "$s" =~ \\$${n}([^A-Za-z0-9_]|$) ]]; do\n',
    '    while (( guard < gc )) && [[ "$s" =~ \\$${n}([^A-Za-z0-9_]|$) ]]; do\n')

# 10. the What 7 comment sites: each comment block that the change makes untrue is rewritten whole (post_planning R1 PP1-A18; checked by commentsync.py)
rep('#   - Shell variable indirection (`f=...; cat "$f"`) is covered only in part: literal\n#     assignments are expanded in a second pass (at most 16 assignments and 8 replacements\n#     per variable; beyond those COUNTS the variable passes). The SIZE of the expansion is\n#     bounded as well -- a value up to 4096 characters, a substituted segment up to 8192\n#     characters and 65536 characters of substituted text per command -- and beyond a SIZE\n#     limit the whole command is BLOCKED as too large to scan ("split it", fail-closed,\n#     owner ruling 2026-10-14), never passed. Arrays, `read <<<`, quote-spliced paths, `cd`\n#     + a relative name, globs, `set --`, `$(printf ...)` and variables across two tool\n#     calls pass; the output side is left to secret-scan.sh.\n',
    '#   - Shell variable indirection (`f=...; cat "$f"`) is covered only in part: literal\n#     assignments are expanded in a second pass (at most 16 assignments and 8 replacements\n#     per variable in the baseline pass; beyond those COUNTS the variable passes). The SIZE of\n#     the expansion is bounded too: a value over 4096 characters, or more than 65536\n#     characters of substituted text per command, blocks the command (fail-closed, owner\n#     ruling 2026-10-14). A substituted copy over 8192 characters is blocked for its size\n#     only where the relaxed rerun of 10CG/aria-plugin#217 is not in effect; where it is\n#     (a Linux build of bash 5.0-5.3, no project extension, time left), the pass is re-run\n#     under a hard deadline with no count bound, the growth over the input as the limit\n#     and the copy judged in full, and growth over 8192 characters, the deadline or any\n#     failure of the rerun still blocks. Arrays, `read <<<`, quote-spliced paths, `cd`\n#     + a relative name, globs, `set --`, `$(printf ...)` and variables across two tool\n#     calls pass; the output side is left to secret-scan.sh.\n')   # baseline :87-95
rep('# LENGTH BUDGET (review M6; fail-CLOSED, owner ruling 2026-10-14): without it the judged string is the segment plus references x value length, and one level of chaining\n# multiplies a value by 8, so a 5 KB command overran the 5 s hook timeout (and a timeout lets the command through). Three limits, counted in characters. Beyond ANY of them the\n# whole command is BLOCKED with a text of its own ("command too large to scan for secrets ... split it": _sg_emit_blocked with the 4th word oversize, status 2) and never\n# passed: a copy that is not judged is a way past the guard, and padding a value or a chain would be the recipe. The oversize string is never built, expanded further, judged\n# or scanned: the pass stops at the first overrun and nothing behind it is touched, so an overrun costs no more than the budgeted work in front of it (blocking is as cheap as\n# passing was; the 5 s timeout and its fail-open, 10CG/aria-plugin#216, are not touched). (The COUNTS above -- 16 assignments, 8 replacements, 8 for statements -- are another\n# bound and still pass beyond the limit, SC-21 21y.) (1) _SGV_VMAX: a value longer than that (as collected, or after chaining) blocks the\n# command whether or not the variable is mentioned: _sg_vx_collect stops at it and returns 2; 4096 is PATH_MAX, a longer value is not one path. (2) _SGV_SMAX: a substituted\n# copy (a segment, or the whole command) that would become longer blocks the command (status 2 of _sg_vx_apply; the W9 extension\'s look at the substituted whole command, after\n# the pass, blocks on it only when an extension is in effect -- without one nothing is left unjudged). 8192 because a BLOCK verdict costs the square of the copy length\n# (_sg_compute_credit on one long line: about 0.9 s at 8 KB, 3 s at 16 KB, 13 s at 32 KB) and a verdict that arrives after the timeout is lost. The limit counts the whole judged\n# string, not its growth: a segment (in whole-command mode: the command) over 8192 characters that mentions a collected variable is blocked however small the value is.\n# (3) _SGV_TMAX: all copies of one command together; once used up the command is blocked -- what many dense segments can cost is bounded too.\n# _sg_vx_collect, _sg_vx_apply and _SG_SUB are names of the contract, like _sg_vx_pass: the budget probes of the suite use them.\n',
    '# LENGTH BUDGET (review M6; fail-CLOSED, owner ruling 2026-10-14; narrowed by 10CG/aria-plugin#217): without it the judged string is the segment plus references x value\n# length, and one level of chaining multiplies a value by 8, so a 5 KB command overran the 5 s hook timeout (and a timeout lets the command through). Three limits, counted in\n# characters. (1) _SGV_VMAX: a value longer than that (as collected, or after chaining) blocks the command whether or not the variable is mentioned: _sg_vx_collect stops at it\n# and returns 2; 4096 is PATH_MAX, a longer value is not one path. (3) _SGV_TMAX: all copies of one command together; once used up the command is blocked -- what many dense\n# segments can cost is bounded too. Both block with a text of their own ("command too large to scan for secrets ... split it": _sg_emit_blocked with the 4th word oversize,\n# status 2), and the oversize string is never built, expanded further, judged or scanned. (2) _SGV_SMAX: a substituted copy (a segment, or the whole command) that would become\n# longer than 8192 characters ends the baseline pass at that copy (status 2 of _sg_vx_apply), because a BLOCK verdict costs the square of the copy length (_sg_compute_credit on\n# one long line: about 0.9 s at 8 KB, 3 s at 16 KB, 13 s at 32 KB) and a verdict that arrives after the 5 s timeout is lost. What follows depends on _sg_relax_ok: where the\n# relaxation is in effect, _sg_vx_pass returns status 4 and _sg_per_segment_eval re-runs the pass in a background job under a hard deadline (_sg_relax_run); there the copy\n# limit is the growth over the input (_SGV_GMAX), and a copy over 8192 characters is judged in full by _sg_vx_big_judge (a line longer than _SGV_LMAX is matched against the\n# rows only: nocredit, the longline text). Elsewhere, and whenever the rerun does not finish in time, the command is blocked with the size text, byte for byte as before (the\n# W9 extension\'s look at the substituted whole command, after the pass, blocks on such a copy only when an extension is in effect). (The COUNTS above -- 16 assignments, 8\n# replacements, 8 for statements -- bound the baseline pass and still pass beyond the limit, SC-21 21y; the relaxed rerun has no count bound, the deadline caps its cost.)\n')   # baseline :577-590
rep('# and stays fast; the `# guard:ack` escape and the _SGV_* size budget are unchanged; fail-closed means an overrun BLOCKs (exit 2), never allows.\n',
    '# and stays fast; the `# guard:ack` escape is unchanged; the relaxed rerun of 10CG/aria-plugin#217 has a hard deadline of its own (_SG_P0 + min(budget, 3) s, see\n# _sg_relax_run) and its checkpoints fall back to the size block, never to the time text; fail-closed means an overrun BLOCKs (exit 2), never allows.\n')   # baseline :606-606
rep('# _sg_vx_apply S : S with the collected values substituted -> _SG_SUB. Status 0 = a copy was built, 1 = nothing to substitute, 2 = the copy would be longer than _SGV_SMAX (not\n# built, _SG_SUB stays S; the caller blocks the command). Per variable: ${NAME} through _sg_vx_replace, then $NAME with the same prefix accumulation (the already substituted text is never scanned again;\n# the remainder keeps the character that ended the match, so $f$f works), at most 8 times.\n',
    '# _sg_vx_apply S : S with the collected values substituted -> _SG_SUB. Status 0 = a copy was built, 1 = nothing to substitute, 2 = the copy would be over the limit (not\n# built, _SG_SUB stays S; the caller decides): the limit is _SGV_SMAX in the baseline pass and the input length + _SGV_GMAX in the relaxed rerun (_SG_RELAXED). Per\n# variable: ${NAME} through _sg_vx_replace, then $NAME with the same prefix accumulation (the already substituted text is never scanned again; the remainder keeps the\n# character that ended the match, so $f$f works), at most 8 times in the baseline pass and with no count bound in the relaxed rerun.\n')   # baseline :674-676
rep('# _sg_vx_pass CMD MODE : the second pass -- judge the substituted copies. MODE is whole or segment, as _sg_core_eval left it in _SG_MODE (in segment mode _SG_SEGS holds\n# the segments). The function name is a contract: the fault-injection and evaluation-order probes locate it by name. An overrun of the length budget (a value, a copy, the total)\n# ends the pass at once with an oversize BLOCK (the size text of _sg_emit_blocked, status 2): nothing behind the overrun is built or judged.\n',
    '# _sg_vx_pass CMD MODE : the second pass -- judge the substituted copies. MODE is whole or segment, as _sg_core_eval left it in _SG_MODE (in segment mode _SG_SEGS holds\n# the segments). The function name is a contract: the fault-injection and evaluation-order probes locate it by name. A value or total overrun stops the pass with an oversize\n# BLOCK (status 2). A copy over _SGV_SMAX ends the baseline pass too: with status 4 when the relaxation is in effect (_sg_relax_ok; the baseline block text is kept\n# in _SG_OV_PAT / _SG_OV_MODE for the fallback), else with the oversize BLOCK. Inside the relaxed rerun (_SG_RELAXED) a growth overrun blocks with the growth text, a copy\n# over _SGV_SMAX goes to _sg_vx_big_judge, and a time checkpoint returns 3 (no time text: the caller falls back to the baseline block). Nothing behind an overrun is built\n# or judged.\n')   # baseline :701-703
rep('# _sg_emit_blocked PAT SEG MODE [oversize] : the (unchanged) BLOCKED text, shared by every block path. With the 4th word `oversize` it prints the SIZE text instead (W10 length\n# budget, fail-closed): nothing was matched, the command is too large to be checked; PAT then names the limit that was hit, SEG and MODE are not used. The size text echoes only\n# the first 200 characters of the command (the command is by definition a large one).\n',
    '# _sg_emit_blocked PAT SEG MODE [oversize|timeout|longline] : the BLOCKED text, shared by every block path. With the 4th word `oversize` it prints the SIZE text instead\n# (W10 length budget, fail-closed): nothing was matched, the command is too large to be checked; PAT then names the limit that was hit, SEG and MODE are not used. With\n# `longline` (10CG/aria-plugin#217) it prints the text for a big copy that matched a row on a line longer than _SGV_LMAX, where credit is not evaluated; PAT is the row. The\n# size, time and longline texts echo only the first 200 characters of the command (the command is by definition a large one).\n')   # baseline :826-828
rep('# _sg_judge_one() — evaluate one string (whole command in "whole" mode, or one\n# top-level segment in "segment" mode) against risky_patterns + credit. $1 =\n# string to judge, $2 = mode (whole|segment). Returns 0 = allow, 2 = blocked\n# (BLOCKED message already written to stderr; mode=whole reproduces canonical\n# stderr byte-for-byte, zero new lines).\n',
    '# _sg_judge_one() — evaluate one string (whole command in "whole" mode, or one\n# top-level segment in "segment" mode) against risky_patterns + credit. $1 =\n# string to judge, $2 = mode (whole|segment), $3 = nocredit or empty: with\n# nocredit (10CG/aria-plugin#217: a big copy with a line longer than _SGV_LMAX)\n# a matched row blocks at once with the longline text and credit is not\n# evaluated; the W12 neutralisation still runs first. Return 0 = allow,\n# 2 = blocked (BLOCKED message already written to stderr; mode=whole reproduces\n# canonical stderr byte-for-byte, zero new lines).\n')   # baseline :1492-1496
rep('# Order (W9 / W10): 1. the built-in judgement (_sg_core_eval: the baseline body of this function, unchanged); 2. only if it allowed, the W10 variable pass (_sg_vx_pass);\n# 3. only if both allowed, the W9 project extension -- on the original command, then on the variable-substituted whole command. A built-in block ends the evaluation\n# before either later stage is even called, so nothing the built-ins decide is postponed or reversed. The extension runs ONLY inside command substitutions; its answer\n# is the literal sentinel BLOCK, anything else (empty, error, fault) means "no extension block". Its own block prints the shared BLOCKED text (W13). Length budget: an overrun\n# inside _sg_vx_pass blocks there; the extension\'s look at the substituted whole command, when that copy is too large to build, blocks here -- but only when an extension is in\n# effect (entries exist: asked inside a command substitution like every other extension call), because without one nothing is left unjudged.\n',
    '# Order (W9 / W10): 1. the built-in judgement (_sg_core_eval: the baseline body of this function, unchanged); 2. only if it allowed, the W10 variable pass (_sg_vx_pass),\n# and when that pass returns status 4 (a copy over _SGV_SMAX with the relaxation in effect), the relaxed rerun under the hard deadline (_sg_relax_run,\n# 10CG/aria-plugin#217): its allow or block is final -- the relaxation is in effect only when no extension is, so stage 3 would add nothing -- and any failure of the\n# rerun falls back to the baseline size block; 3. only if both allowed, the W9 project extension -- on the original command, then on the variable-substituted whole\n# command. A built-in block ends the evaluation before either later stage is even called, so nothing the built-ins decide is postponed or reversed. The extension runs\n# ONLY inside command substitutions; its answer is the literal sentinel BLOCK, anything else (empty, error, fault) means "no extension block". Its own block prints the\n# shared BLOCKED text (W13). Length budget: a value or total overrun inside _sg_vx_pass blocks there; the extension\'s look at the substituted whole command, when that\n# copy is too large to build, blocks here -- but only when an extension is in effect (entries exist: asked inside a command substitution like every other extension\n# call), because without one nothing is left unjudged.\n')   # baseline :1531-1536

open(dst, 'w', encoding='utf-8').write(t)
print('ok', len(t))
