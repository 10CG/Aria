#!/usr/bin/env python3
"""mutants.py <hook> <out dir> : the bad implementations of the BI list, each = the hook under test + ONE change (a realistic slip). v3.2, post_planning R2
reinforcement (TASK-002 (c)): they are built from the implementation (aria feature/secret-guard-w10-failclosed-narrowing), no longer from the v3.1 prototype.
  BI-1..BI-23   the author's list, unchanged in meaning (anchors follow the implementation). Built by the author of the prototype: a self-check of the
                cases, not the non-author construction of TASK-003.
  BI-17a/b/c    BI-17 split: each keeps ONE of the three count bounds inside the rerun (assignments / for statements / replacements per variable).
  BI-24..       the bad implementations of the five R2 seats that no case caught (R2 aggregate, "non-author mutation summary"; generators and per-mutant
                results in ../pp-r2-seats/). Constructions of several seats that give the same bytes are ONE BI listing every seat id; each seat's own
                construction is rebuilt here and asserted byte-identical. CR-MB = QA-M12 = TL-M1 is BI-17b.
  P-*           QA-M29 is equivalent (the three constants are all 8192), so it is no BI: the perturbation round sets _SGV_GMAX=8190 and _SGV_LMAX=8200
                (P-0, which must stay green on every case), then puts each wrong-constant slip on top of P-0, so that each use of a constant is observable.
Writes <out>/<id>.sh; <out>/designated.tsv (id, designated case ids, description, seat ids); <out>/reasons.tsv (id, case id, the regex the FAIL detail of
that case must match -- the tags of sc-cases.sh / sc-direct.sh); <out>/perturb.tsv (id, designated case ids or "all", description). Every replacement must
hit exactly once (in the order given)."""
import sys, os, hashlib
src, out = sys.argv[1], sys.argv[2]
base = open(src, encoding='utf-8').read()
os.makedirs(out, exist_ok=True)
ACK = 'guard' + ':ack'   # assembled, as the R2 seat did: the session's own guard reads command lines
M = []   # (id, [(case id, reason regex)], description, seat ids, [variant: [(old, new)]], start text)

def build(t, pairs, label):
    for old, new in pairs:
        n = t.count(old)
        if n != 1: sys.exit(f'{label}: replacement hit {n} times: {old[:90]!r}')
        t = t.replace(old, new)
    return t

def mut(i, cases, desc, *variants, seats='author', start=None):
    M.append((i, cases, desc, seats, variants, start))

# ---------------- BI-1..BI-23 (author) ----------------
RUN_OLD = base[base.index('  out="$( exec 2>/dev/null; set -m'):base.index('  return 4\n}', base.index('  out="$( exec 2>/dev/null; set -m')) + len('  return 4\n}')]
mut('BI-1', [('V4-S6-spoofed-tail-0', r'\[rc\]')], 'verdict read from the last line of the output text (v2)',
    [('  [[ $rc -eq 77 ]] && return 0\n', '  [[ $rc -eq 77 || "${out##*$\'\\n\'}" == 0 ]] && return 0\n')])
mut('BI-2', [('V5-S5-pipe-holder', r'\[wall>hi\]'), ('V6-E2-deadline-fallback-bytes', r'\[bytes\]')], 'no process group and no group-leader self-check: the job PID alone is killed',
    [('out="$( exec 2>/dev/null; set -m\n', 'out="$( exec 2>/dev/null\n'),
     ('  { IFS= read -r st < "/proc/$BASHPID/stat"; } 2>/dev/null || return 9\n  st="${st##*) }"; f=( $st )\n  [[ "${f[2]:-}" == "$BASHPID" ]] || return 9\n', ''),
     ('kill -KILL -- "-$me"', 'kill -KILL "$me"'), ('          kill -KILL -- "-$jp"', '          kill -KILL "$jp"')])
mut('BI-3', [('V5-S10c-dead-timer-no-judgement', r'\[rc\]'), ('V5-S10d-no-judgement-with-dead-timer', r'\[judged\]')], 'the judgement starts without checking that the timer runs',
    [('  [[ -n "$tp" ]] && kill -0 "$tp" 2>/dev/null || return 9   # no running timer, no judgement: the deadline must exist before the first expensive step\n', '')])
mut('BI-4', [('V6-E2-deadline-fallback-bytes', r'\[bytes\]')], 'the relaxed rerun runs in-process: no job, no hard deadline',
    [(RUN_OLD, '  _SG_RELAXED=1; _sg_vx_pass "$1" "$_SG_MODE"; rc=$?; _SG_RELAXED=\n  case $rc in 0) return 0 ;; 2) return 2 ;; *) return 4 ;; esac\n}')])
mut('BI-5', [('V2-G4-extension-file-with-entry', r'\[status\]'), ('V2-E9-extension-project', r'\[bytes\]')], 'the gate does not ask about a project extension',
    [('  [[ "$( _sg_relax_noext 2>/dev/null )" == none ]]\n}', '  return 0\n}')])
mut('BI-6', [('V2-G3-gate-calls-platform', r'\[status\]'), ('V2-G3b-gate-uses-build-facts', r'\[value\]'), ('V2-E8-ostype-from-environment-ignored', r'\[fallback\]')],
    'the platform is read from the environment (OSTYPE, EPOCHREALTIME present)',
    [('  _sg_relax_platform "${BASH_VERSINFO[5]:-}" "${BASH_VERSINFO[0]:-0}" "${BASH_VERSINFO[1]:-0}" "$osr" "$wsl" || return 1',
      '  [[ "${OSTYPE:-}" == linux* && -n "${EPOCHREALTIME:-}" ]] || return 1')])
mut('BI-7', [('V6-E2-deadline-fallback-bytes', r'\[time-text\]|\[bytes\]')], 'the fallback writes a time text of its own instead of the baseline size text',
    [('{ _sg_emit_blocked "$_SG_OV_PAT" "$cmd" "$_SG_OV_MODE" oversize; return 2; }', '{ _sg_emit_blocked "time" "$cmd" "$_SG_OV_MODE" timeout; return 2; }')])
mut('BI-8', [('V9-E12-vmax-unchanged', r'\[bytes\]')], 'VMAX relaxed too', [('_SGV_VMAX=4096\n', '_SGV_VMAX=8192\n')])
mut('BI-9', [('V8-D3-growth-8193-plain', r'\[status\]'), ('V8-D3-growth-8193-braced', r'\[status\]')], 'the growth limit is recomputed from the rewritten string, per variable',
    [('    n="${_SGV_N[i]}"; v="${_SGV_V[i]}"\n    [[ -n "$v" ]] || continue\n    if [[ "$s" == *"\\${$n}"* ]]',
      '    n="${_SGV_N[i]}"; v="${_SGV_V[i]}"\n    [[ -n "${_SG_RELAXED:-}" ]] && lim=$(( ${#s} + _SGV_GMAX ))\n    [[ -n "$v" ]] || continue\n    if [[ "$s" == *"\\${$n}"* ]]')])
mut('BI-10', [('V7-E14-long-line-from-expansion', r'\[kind\]')], 'the longest line is measured on the raw command, not on the copy',
    [('done <<< "$1"\n  (( seen ))', 'done <<< "${command:-$1}"\n  (( seen ))')])
mut('BI-11', [('V10-N3-environ-big-judge', r'\[status\]'), ('V11-S4-one-rule-loop', r'\[count\]')], 'rows only through a rule loop of its own, which skips the W12 neutralisation',
    [('  if (( max > _SGV_LMAX )); then _sg_judge_one "$1" "$2" nocredit; else _sg_judge_one "$1" "$2"; fi',
      '  if (( max > _SGV_LMAX )); then local pat; for pat in "${risky_patterns[@]}"; do [[ "$1" =~ $pat ]] && { _sg_emit_blocked "$pat" "$1" "$2" longline; return 2; }; done; return 0; else _sg_judge_one "$1" "$2"; fi')])
mut('BI-12', [('V7-N5-read-big-judge-short-lines', r'\[kind\]'), ('V7-E13-multiline-copy-normal-text', r'\[kind\]')], 'the line length is tested with [[ =~ .{8193,} ]] (it matches across newlines)',
    [('  while IFS= read -r line; do seen=1; (( ${#line} > max )) && max=${#line}; done <<< "$1"\n', '  seen=1; [[ "$1" =~ .{8193,} ]] && max=8193\n')])
mut('BI-13', [('V3-E3-anchor-at-hook-start', r'\[wall>hi\]')], 'the deadline is anchored after the stdin parse, not at the hook start',
    [('_SG_P0=${EPOCHREALTIME:-}; _SG_RELAXED=   #', '_SG_P0=; _SG_RELAXED=   #'),
     ("done < <(jq -j '(.tool_name | type)", "_SG_P0=${EPOCHREALTIME:-}\ndone < <(jq -j '(.tool_name | type)")])
mut('BI-14', [('V3-G10-cap-3', r'\[value\]'), ('V3-E4-cap-3-at-budget-4', r'\[wall>hi\]')], 'the deadline uses the whole budget, not min(budget, 3)',
    [('  cap=$(( _SG_TIME_BUDGET < 3 ? _SG_TIME_BUDGET : 3 ))\n', '  cap=$_SG_TIME_BUDGET\n')])
mut('BI-15', [('V5-S9-child-left-behind', r'\[wall>hi\]'), ('V5-S13b-nothing-outlives-the-run', r'\[leftover\]')], 'the group is not killed after the job ends',
    [('          kill -KILL -- "-$jp"   # the timer and anything the judgement left behind: nothing of the job outlives it or holds the pipe\n', '')])
mut('BI-16', [('V2-G11-flag-not-from-environment', r'\[value\]'), ('V2-E6-flag-from-environment-ignored', r'\[bytes\]')], 'the relaxed flag is taken from the environment (not initialised)',
    [('_SG_P0=${EPOCHREALTIME:-}; _SG_RELAXED=   #', '_SG_P0=${EPOCHREALTIME:-}   #')])
CAF = '  [[ -n "${_SG_RELAXED:-}" ]] && ca=1000000 cf=1000000   # 10CG/aria-plugin#217 relaxed rerun: no count bound (the deadline caps the cost)\n'
GCR = '  [[ -n "${_SG_RELAXED:-}" ]] && gc=1000000   # 10CG/aria-plugin#217 relaxed rerun: no count bound\n'
GCA = ('lim=$(( ${#1} + _SGV_GMAX )) gc=1000000', 'lim=$(( ${#1} + _SGV_GMAX ))')
mut('BI-17', [('V9-C1-assignments-rerun', r'\[value\]'), ('V9-C2-references-rerun-c12', r'\[value\]'), ('V9-E10-count-axis-read-blocked', r'\[rc\]')],
    'the count bounds also hold inside the rerun', [(CAF, ''), (GCR, ''), GCA])
mut('BI-17a', [('V9-C1-assignments-rerun', r'\[value\]')], 'BI-17 split: only the assignment bound (16) still holds inside the rerun',
    [('&& ca=1000000 cf=1000000   #', '&& cf=1000000   #')])
mut('BI-17b', [('V9-C3-for-statements-rerun', r'\[value\]')], 'BI-17 split: only the for-statement bound (8) still holds inside the rerun (the rerun lifts the assignment bound only)',
    [('&& ca=1000000 cf=1000000   #', '&& ca=1000000   #')],
    [('  [[ -n "${_SG_RELAXED:-}" ]] && ca=1000000 cf=1000000   # 10CG', '  [[ -n "${_SG_RELAXED:-}" ]] && ca=1000000   # 10CG')],   # CR-MB (its diff)
    [('&& ca=1000000 cf=1000000   #', '&& ca=1000000   #')],                                                                       # QA-M12, TL-M1
    seats='CR-MB QA-M12 TL-M1')
mut('BI-17c', [('V9-C2-references-rerun-c12', r'\[value\]'), ('V9-C2-references-rerun-cb12', r'\[value\]')],
    'BI-17 split: only the replacement bound (8 per variable) still holds inside the rerun, in _sg_vx_replace and in _sg_vx_apply', [(GCR, ''), GCA])
mut('BI-18', [('V9-E11-tmax-in-rerun', r'\[rc\]')], 'TMAX is not checked inside the rerun',
    [('    if (( spent > _SGV_TMAX )); then\n', '    if [[ -z "${_SG_RELAXED:-}" ]] && (( spent > _SGV_TMAX )); then\n')])
mut('BI-19', [('V4-S11-bare-zero', r'\[rc\]')], 'a bare 0 from the job counts as allowed', [('  [[ $rc -eq 77 ]] && return 0\n', '  [[ $rc -eq 77 || $rc -eq 0 ]] && return 0\n')])
mut('BI-20', [('V2-G4-empty-extension-file', r'\[status\]')], 'an empty extension file counts as no extension', [('! -e "$root/.aria/secret-guard.paths"', '! -s "$root/.aria/secret-guard.paths"')])
mut('BI-21', [('V3-G9-clock-backwards', r'\[value\]')], 'a clock that went backwards extends the deadline (time left not capped)',
    [('  (( now > cap * 1000000 )) && now=$(( cap * 1000000 ))   # a clock that went backwards never extends the deadline\n', '')])
mut('BI-22', [('V2-G6-no-time-left', r'\[status\]'), ('V2-G7-no-anchor', r'\[status\]'), ('V2-G8-budget-0', r'\[status\]')], 'the gate does not ask for time left',
    [('  _sg_relax_left || return 1\n  [[ "$( _sg_relax_noext', '  [[ "$( _sg_relax_noext')])
mut('BI-23', [('V5-S14-failing-sleep-kills-at-once', r'\[rc\]|\[wall>hi\]')], 'the timer kills only after a successful sleep (&& instead of ;): a failing sleep leaves no deadline',
    [('( sleep "$_SG_LEFT"; kill -KILL -- "-$me" )', '( sleep "$_SG_LEFT" && kill -KILL -- "-$me" )')])

# ---------------- BI-24.. : the R2 seats' bad implementations that no case caught ----------------
SEGTRIG = '      if _sg_relax_ok; then _SG_OV_PAT="a command segment is longer than $_SGV_SMAX characters after variable expansion"; _SG_OV_MODE=segment; return 4; fi'
mut('BI-24', [('V2-G12-segment-trigger-asks-gate', r'\[status\]')], 'the segment-mode trigger point does not ask the gate: it returns 4 unconditionally',
    [(SEGTRIG, '      _SG_OV_PAT="a command segment is longer than $_SGV_SMAX characters after variable expansion"; _SG_OV_MODE=segment; return 4')], seats='CR-MA')
mut('BI-25', [('V2-G12-segment-trigger-asks-gate', r'\[status\]')], 'the segment-mode trigger point asks `true` instead of the gate',
    [('if _sg_relax_ok; then _SG_OV_PAT="a command segment is longer than', 'if true; then _SG_OV_PAT="a command segment is longer than')], seats='QA-M02')
mut('BI-26', [('V2-G14-cwd-extension-file-with-entry', r'\[status\]')], 'the gate takes the project root from CLAUDE_PROJECT_DIR only: the stdin cwd route of _sg_ext_root is lost',
    [('  local root\n  root="$(_sg_ext_root)"\n  if [[ -z "$root" || ! -e', '  local root\n  root="${CLAUDE_PROJECT_DIR:-}"\n  if [[ -z "$root" || ! -e')],   # QA-M01
    [('  root="$(_sg_ext_root)"\n  if [[ -z "$root" || ! -e "$root/.aria/secret-guard.paths" ]]; then printf none; fi',
      '  root="${CLAUDE_PROJECT_DIR:-}"\n  if [[ -z "$root" || ! -e "$root/.aria/secret-guard.paths" ]]; then printf none; fi')],                            # TL-M8
    [('  local root\n  root="$(_sg_ext_root)"\n  if [[ -z "$root" || ! -e "$root/.aria/secret-guard.paths" ]]; then printf none; fi',
      '  local root\n  root="${CLAUDE_PROJECT_DIR:-}"\n  if [[ -z "$root" || ! -e "$root/.aria/secret-guard.paths" ]]; then printf none; fi')],              # BA-M1
    seats='QA-M01 TL-M8 BA-M1')
mut('BI-27', [('V9-C4-value-limit-in-rerun', r'\[status\]')], 'inside the rerun a value over VMAX (status 2 of _sg_vx_collect) is ignored: the partly collected copy is judged',
    [('  if [[ $cr -eq 2 ]]; then\n    _sg_emit_blocked "a variable value is longer than', '  if [[ $cr -eq 2 && -z "${_SG_RELAXED:-}" ]]; then\n    _sg_emit_blocked "a variable value is longer than')], seats='QA-M24')
CK = '[[ -n "${_SG_RELAXED:-}" ]] && return 3   # 10CG/aria-plugin#217 relaxed rerun: no time text of its own, the caller falls back to the baseline block\n'
mut('BI-28', [('V4-S17-rerun-whole-checkpoint', r'\[status\]')], 'the whole-mode time checkpoint inside the rerun returns 0 (allow) instead of 3',
    [('      ' + CK + '      _sg_emit_blocked "time" "$cmd" whole timeout', '      [[ -n "${_SG_RELAXED:-}" ]] && return 0\n      _sg_emit_blocked "time" "$cmd" whole timeout')], seats='QA-M06')
mut('BI-29', [('V4-S18-rerun-segment-checkpoint', r'\[status\]')], 'the segment-loop time checkpoint inside the rerun returns 0 (allow) instead of 3',
    [('      ' + CK + '      _sg_emit_blocked "time" "$cmd" segment timeout', '      [[ -n "${_SG_RELAXED:-}" ]] && return 0\n      _sg_emit_blocked "time" "$cmd" segment timeout')], seats='QA-M07')
mut('BI-30', [('V4-S16-rerun-collect-checkpoint', r'\[status\]')], 'the chaining time checkpoint (status 3 of _sg_vx_collect) inside the rerun returns 0 (allow) instead of 3',
    [('    ' + CK + '    _sg_emit_blocked "time" "$cmd" "$mode" timeout', '    [[ -n "${_SG_RELAXED:-}" ]] && return 0\n    _sg_emit_blocked "time" "$cmd" "$mode" timeout')], seats='QA-M08')
mut('BI-31', [('V4-S16-rerun-collect-checkpoint', r'\[status\]'), ('V4-S17-rerun-whole-checkpoint', r'\[status\]'), ('V4-S18-rerun-segment-checkpoint', r'\[status\]')],
    'the three time checkpoints inside the rerun write the time text and return 2 (the "return 3" lines removed)',
    [('    ' + CK + '    _sg_emit_blocked "time" "$cmd" "$mode" timeout\n', '    _sg_emit_blocked "time" "$cmd" "$mode" timeout\n'),
     ('      ' + CK + '      _sg_emit_blocked "time" "$cmd" whole timeout\n', '      _sg_emit_blocked "time" "$cmd" whole timeout\n'),
     ('      ' + CK + '      _sg_emit_blocked "time" "$cmd" segment timeout\n', '      _sg_emit_blocked "time" "$cmd" segment timeout\n')], seats='BA-M8')
mut('BI-32', [('V4-S18-rerun-segment-checkpoint', r'\[status\]')], 'the segment-loop time checkpoint inside the rerun writes the time text (its "return 3" line removed)',
    [('    if _sg_over_budget; then   # time-budget fail-closed before each per-segment _sg_vx_apply / _sg_judge_one (the O(copy^2) hot leg)\n      ' + CK,
      '    if _sg_over_budget; then   # time-budget fail-closed before each per-segment _sg_vx_apply / _sg_judge_one (the O(copy^2) hot leg)\n')], seats='TL-M5')
NOCREDIT = ('      if [[ "$nocredit" == nocredit ]]; then   # 10CG/aria-plugin#217: a big copy with a line longer than _SGV_LMAX -- the match alone blocks, credit is not evaluated\n'
            '        _sg_emit_blocked "$pat" "$seg" "$mode" longline\n        return 2\n      fi\n')
CREDIT = ('      if [[ -z "$credit" ]]; then\n        if _sg_compute_credit "$seg"; then credit=1; else credit=0; fi\n      fi\n'
          '      if [[ "$credit" == "0" ]]; then\n        _sg_emit_blocked "$pat" "$seg" "$mode"\n        return 2\n      fi\n')
CREDIT_MC = ('      if [[ -z "$credit" ]]; then\n        if _sg_compute_credit "$seg"; then credit=1; else credit=0; fi\n      fi\n'
             '      if [[ "$credit" == "0" ]]; then\n        if [[ "$nocredit" == nocredit ]]; then _sg_emit_blocked "$pat" "$seg" "$mode" longline; else _sg_emit_blocked "$pat" "$seg" "$mode"; fi\n        return 2\n      fi\n')
mut('BI-33', [('V10-N6-filtered-long-line-rows-only', r'\[status\]'), ('V7-N7-big-judge-filtered-long-line', r'\[status\]')],
    'credit is evaluated first; a line over _SGV_LMAX gets the longline text only when credit is 0 (ruling C broken: a filtered long line is allowed)',
    [(NOCREDIT, ''), ('        _sg_emit_blocked "$pat" "$seg" "$mode"\n        return 2\n',
                      '        if [[ "$nocredit" == nocredit ]]; then _sg_emit_blocked "$pat" "$seg" "$mode" longline; else _sg_emit_blocked "$pat" "$seg" "$mode"; fi\n        return 2\n')],   # CR-MC (its diff)
    [(NOCREDIT + CREDIT, CREDIT_MC)],                                                                                                                         # BA-M4
    seats='CR-MC BA-M4')
mut('BI-34', [('V7-N8-whole-branch-returns-big-judge', r'\[status\]')], 'the whole-mode branch calls _sg_vx_big_judge but drops its verdict (no return $?): the credit judgement follows',
    [('then _sg_vx_big_judge "$_SG_SUB" whole; return $?; fi', 'then _sg_vx_big_judge "$_SG_SUB" whole; fi')], seats='TL-M2')
SEGJ = 'if [[ -n "${_SG_RELAXED:-}" ]] && (( ${#_SG_SUB} > _SGV_SMAX )); then _sg_vx_big_judge "$_SG_SUB" segment; else _sg_judge_one "$_SG_SUB" segment; fi'
mut('BI-35', [('V7-N9-segment-routes-to-big-judge', r'\[status\]')], 'segment mode never routes a big copy to _sg_vx_big_judge (only the whole-mode hunk applied)',
    [('    ' + SEGJ, '    _sg_judge_one "$_SG_SUB" segment')],               # CR-MD (its diff)
    [(SEGJ, '_sg_judge_one "$_SG_SUB" segment')],                         # TL-M3
    [('    ' + SEGJ + '\n', '    _sg_judge_one "$_SG_SUB" segment\n')],   # BA-M11
    seats='CR-MD TL-M3 BA-M11')
mut('BI-36', [('V7-N9-segment-routes-to-big-judge', r'\[status\]')], 'segment mode judges a big copy with the normal _sg_judge_one in both branches',
    [('then _sg_vx_big_judge "$_SG_SUB" segment; else _sg_judge_one "$_SG_SUB" segment; fi', 'then _sg_judge_one "$_SG_SUB" segment; else _sg_judge_one "$_SG_SUB" segment; fi')], seats='QA-M10')
mut('BI-37', [('V7-N10-blank-padded-long-line', r'\[status\]')], 'the line-length loop reads without IFS= (leading and trailing blanks are trimmed from the measured line)',
    [('  while IFS= read -r line; do seen=1; (( ${#line} > max )) && max=${#line}; done <<< "$1"\n', '  while read -r line; do seen=1; (( ${#line} > max )) && max=${#line}; done <<< "$1"\n')],   # QA-M28
    [('  while IFS= read -r line; do seen=1;', '  while read -r line; do seen=1;')],                                                                                      # TL-M4
    seats='QA-M28 TL-M4')
GROW_W = '        _sg_emit_blocked "the command grows by more than $_SGV_GMAX characters after variable expansion" "$cmd" whole oversize\n        return 2\n'
GROW_S = '        _sg_emit_blocked "a command segment grows by more than $_SGV_GMAX characters after variable expansion" "$cmd" segment oversize\n        return 2\n'
mut('BI-38', [('V8-D4-growth-text-whole', r'\[status\]')], 'a whole-mode growth overrun inside the rerun returns 0 (allow) instead of the growth block',
    [('      if [[ -n "${_SG_RELAXED:-}" ]]; then\n' + GROW_W + '      fi\n', '      if [[ -n "${_SG_RELAXED:-}" ]]; then\n        return 0\n      fi\n')],   # QA-M18
    [(GROW_W, '        return 0\n')],                                                                                                   # BA-M9
    seats='QA-M18 BA-M9')
mut('BI-39', [('V8-D5-growth-text-segment', r'\[status\]')], 'a segment-mode growth overrun inside the rerun skips the segment (continue) instead of blocking',
    [('      if [[ -n "${_SG_RELAXED:-}" ]]; then\n' + GROW_S + '      fi\n', '      if [[ -n "${_SG_RELAXED:-}" ]]; then\n        continue\n      fi\n')], seats='QA-M17')
mut('BI-40', [('V8-D5-growth-text-segment', r'\[status\]')], 'a segment-mode growth overrun inside the rerun returns 0 (allow) instead of the growth block',
    [(GROW_S, '        return 0\n')], seats='BA-M10')
mut('BI-41', [('V5-S15-job-refuses-outside-group-leader', r'\[status\]')], 'the group-leader self-check of the job is removed (set -m kept)',
    [('  { IFS= read -r st < "/proc/$BASHPID/stat"; } 2>/dev/null || return 9\n  st="${st##*) }"; f=( $st )\n  [[ "${f[2]:-}" == "$BASHPID" ]] || return 9\n', '')], seats='BA-M7')
mut('BI-42', [('V5-E19-deadline-with-term-ignored', r'\[uncut\]|\[bytes\]')], 'the timer and the group kill after the job use TERM instead of KILL',
    [('kill -KILL -- "-$me"', 'kill -TERM -- "-$me"'), ('          kill -KILL -- "-$jp"', '          kill -TERM -- "-$jp"')], seats='QA-M20')
mut('BI-43', [('V5-E19-deadline-with-term-ignored', r'\[uncut\]|\[bytes\]')], 'the timer uses TERM instead of KILL (the group kill after the job keeps KILL)',
    [('kill -KILL -- "-$me"', 'kill -TERM -- "-$me"')], seats='QA-M30')
PLAT = '  _sg_relax_platform "${BASH_VERSINFO[5]:-}" "${BASH_VERSINFO[0]:-0}" "${BASH_VERSINFO[1]:-0}" "$osr" "$wsl" || return 1'
mut('BI-44', [('V2-G3b-gate-uses-build-facts', r'\[value\]')], 'the machine argument of the platform check is $MACHTYPE (the environment can rewrite it) instead of BASH_VERSINFO[5]',
    [('_sg_relax_platform "${BASH_VERSINFO[5]:-}" "${BASH_VERSINFO[0]:-0}"', '_sg_relax_platform "${MACHTYPE:-}" "${BASH_VERSINFO[0]:-0}"')],   # QA-M04
    [(PLAT, PLAT.replace('"${BASH_VERSINFO[5]:-}"', '"${MACHTYPE:-}"'))],                                                                         # BA-M14, re-anchored on the 5-argument call
    seats='QA-M04 BA-M14')
mut('BI-45', [('V6-S20-segment-fallback-text', r'\[bytes\]')], 'the segment-mode trigger point keeps the whole-command reason string for the fallback text',
    [('_SG_OV_PAT="a command segment is longer than $_SGV_SMAX characters after variable expansion"; _SG_OV_MODE=segment; return 4',
      '_SG_OV_PAT="the command is longer than $_SGV_SMAX characters after variable expansion"; _SG_OV_MODE=segment; return 4')],                   # QA-M09
    [('_SG_OV_PAT="a command segment is longer than $_SGV_SMAX characters after variable expansion"; _SG_OV_MODE=segment; return 4;',
      '_SG_OV_PAT="the command is longer than $_SGV_SMAX characters after variable expansion"; _SG_OV_MODE=segment; return 4;')],                  # BA-M5
    seats='QA-M09 BA-M5')
mut('BI-46', [('V7-N11-lmax-edge-normal', r'\[kind\]')], 'the longest-line edge is >= _SGV_LMAX instead of > _SGV_LMAX',
    [('  if (( max > _SGV_LMAX )); then _sg_judge_one "$1" "$2" nocredit;', '  if (( max >= _SGV_LMAX )); then _sg_judge_one "$1" "$2" nocredit;')],   # QA-M13, TL-M9
    [('  if (( max > _SGV_LMAX )); then _sg_judge_one "$1" "$2" nocredit', '  if (( max >= _SGV_LMAX )); then _sg_judge_one "$1" "$2" nocredit')],     # BA-M6
    seats='QA-M13 TL-M9 BA-M6')
mut('BI-47', [('V7-N13-unmeasured-length-rows-only', r'\[status\]')], 'a length that could not be measured routes to the credit path (max=0) instead of rows only',
    [('(( seen )) || max=$(( _SGV_LMAX + 1 ))', '(( seen )) || max=0')], seats='QA-M14')
mut('BI-48', [('V7-N13-unmeasured-length-rows-only', r'\[status\]')], 'the "length could not be measured -> rows only" sentinel of _sg_vx_big_judge is removed',
    [('  (( seen )) || max=$(( _SGV_LMAX + 1 ))   # the length could not be measured: rows only, never the cheaper-to-pass credit path\n', '')], seats='BA-M3')
mut('BI-49', [('V4-S19-block-text-bytes', r'\[bytes\]')], 'the relaxed block text is printed again without its final newline',
    [("{ printf '%s\\n' \"$out\" >&2; return 2; }", "{ printf '%s' \"$out\" >&2; return 2; }")], seats='QA-M15')
mut('BI-50', [('V3-G12-time-left-zero-padded', r'\[value\]')], 'the time left is printed as %d.%d: the microseconds are not zero-padded (2.050000 s becomes 2.50000)',
    [("printf -v _SG_LEFT '%d.%06d'", "printf -v _SG_LEFT '%d.%d'")], seats='BA-M2')
mut('BI-51', [('V11-S5-longline-head-verbatim', r'\[text\]'), ('V11-S7-longline-text-verbatim', r'\[text\]')], 'the longline description gains a prescriptive sentence (end the command with a ' + ACK + ' line)',
    [('so the match alone blocks the command\n(fail-closed).\n', 'so the match alone blocks the command\n(fail-closed).\nIf you are sure the command is safe, end it with a ' + ACK + ': <reason> line and run it again.\n')], seats='KM-M1')
mut('BI-52', [('V8-D4-growth-text-whole', r'\[text\]')], 'the whole-mode growth reason string reverts to the baseline wording (the command is longer than _SGV_SMAX)',
    [('"the command grows by more than $_SGV_GMAX characters after variable expansion"', '"the command is longer than $_SGV_SMAX characters after variable expansion"')], seats='KM-M2')
mut('BI-53', [('V8-D5-growth-text-segment', r'\[text\]')], 'the segment-mode growth reason string reverts to the baseline wording (a command segment is longer than _SGV_SMAX)',
    [('"a command segment grows by more than $_SGV_GMAX characters after variable expansion"', '"a command segment is longer than $_SGV_SMAX characters after variable expansion"')], seats='KM-M3')
ZH = '命令读取含密钥的来源, 且变量展开后有超长的行, 这个尺寸下不评估脱敏过滤, 请拆成更小的命令'
mut('BI-54', [('V11-S6-longline-chinese-line-verbatim', r'\[text\]'), ('V11-S7-longline-text-verbatim', r'\[text\]')], 'the line in Chinese of the longline text gains a prescriptive clause (add a ' + ACK + ' line)',
    [(ZH, '命令读取含密钥的来源, 且变量展开后有超长的行, 可在命令末尾加 ' + ACK + ' 行后重试, 请拆成更小的命令')], seats='KM-M6')

# ---------------- the perturbation round (QA-M29 is equivalent: every use of a constant made observable) ----------------
PERT = [('_SGV_GMAX=8192   #', '_SGV_GMAX=8190   #'), ('_SGV_LMAX=8192   #', '_SGV_LMAX=8200   #')]
P = [('P-0', 'all', 'the constants perturbed: _SGV_GMAX=8190, _SGV_LMAX=8200 (every case must stay green: the cases read the constants from the hook)', []),
     ('P-M29', 'V7-N11-lmax-edge-normal', 'QA-M29 on P-0: the longest-line edge compares with _SGV_SMAX instead of _SGV_LMAX',
      [('  if (( max > _SGV_LMAX )); then _sg_judge_one "$1" "$2" nocredit;', '  if (( max > _SGV_SMAX )); then _sg_judge_one "$1" "$2" nocredit;')]),
     ('P-L-sentinel', 'V7-N13-unmeasured-length-rows-only', 'on P-0: the unmeasured-length sentinel is _SGV_SMAX + 1 instead of _SGV_LMAX + 1',
      [('(( seen )) || max=$(( _SGV_LMAX + 1 ))', '(( seen )) || max=$(( _SGV_SMAX + 1 ))')]),
     ('P-L-text', 'V11-S5-longline-head-verbatim V11-S7-longline-text-verbatim', 'on P-0: the longline text names _SGV_SMAX instead of _SGV_LMAX',
      [('it has a line longer than ${_SGV_LMAX} characters', 'it has a line longer than ${_SGV_SMAX} characters')]),
     ('P-G-limit', 'V8-D3-growth-8193-plain V8-D3-growth-8193-braced', 'on P-0: the growth limit of the rerun is the input length + _SGV_SMAX instead of + _SGV_GMAX',
      [('lim=$(( ${#1} + _SGV_GMAX )) gc=1000000', 'lim=$(( ${#1} + _SGV_SMAX )) gc=1000000')]),
     ('P-G-text-whole', 'V8-D4-growth-text-whole', 'on P-0: the whole-mode growth reason names _SGV_SMAX instead of _SGV_GMAX',
      [('"the command grows by more than $_SGV_GMAX characters', '"the command grows by more than $_SGV_SMAX characters')]),
     ('P-G-text-segment', 'V8-D5-growth-text-segment', 'on P-0: the segment-mode growth reason names _SGV_SMAX instead of _SGV_GMAX',
      [('"a command segment grows by more than $_SGV_GMAX characters', '"a command segment grows by more than $_SGV_SMAX characters')])]
PREASON = {'P-M29': r'\[kind\]', 'P-L-sentinel': r'\[status\]', 'P-L-text': r'\[text\]', 'P-G-limit': r'\[status\]', 'P-G-text-whole': r'\[text\]', 'P-G-text-segment': r'\[text\]'}

with open(os.path.join(out, 'designated.tsv'), 'w', encoding='utf-8') as d, open(os.path.join(out, 'reasons.tsv'), 'w', encoding='utf-8') as r:
    for i, cases, desc, seats, variants, start in M:
        texts = [build(base, v, f'{i} variant {k + 1}') for k, v in enumerate(variants)]
        if any(x != texts[0] for x in texts[1:]):
            sys.exit(f'{i}: the seat constructions {seats} do not give the same bytes')
        if texts[0] == base: sys.exit(f'{i}: no change')
        with open(os.path.join(out, i + '.sh'), 'w', encoding='utf-8') as f: f.write(texts[0])
        d.write(f"{i}\t{' '.join(c for c, _ in cases)}\t{desc}\t{seats}\n")
        for c, rx in cases: r.write(f'{i}\t{c}\t{rx}\n')
p0 = build(base, PERT, 'P-0')
with open(os.path.join(out, 'perturb.tsv'), 'w', encoding='utf-8') as d, open(os.path.join(out, 'reasons.tsv'), 'a', encoding='utf-8') as r:
    for i, cases, desc, pairs in P:
        t = build(p0, pairs, i)
        if i != 'P-0' and t == p0: sys.exit(f'{i}: no change')
        with open(os.path.join(out, i + '.sh'), 'w', encoding='utf-8') as f: f.write(t)
        d.write(f'{i}\t{cases}\t{desc}\n')
        if i != 'P-0':
            for c in cases.split(): r.write(f'{i}\t{c}\t{PREASON[i]}\n')
print(len(M), 'bad implementations,', len(P), 'perturbation variants; hook sha256', hashlib.sha256(base.encode('utf-8')).hexdigest()[:12])
