#!/usr/bin/env python3
"""mkmut.py <v3.1 hook> <out dir> : non-author mutants of the v3.1 prototype for a defensive mutation test of the secret-guard test cases
(10CG/aria-plugin#217 post_planning R2, qa-engineer seat). Each mutant = prototype + ONE change that looks like a real writing slip.
Writes <out>/M<nn>.sh and <out>/predictions.tsv (id, expected catching cases, why, description) BEFORE anything is run."""
import sys, os
src, out = sys.argv[1], sys.argv[2]
base = open(src, encoding='utf-8').read()
os.makedirs(out, exist_ok=True)
M = []
def mut(i, expect, why, desc, *pairs): M.append((i, expect, why, desc, pairs))

# ---- A: the gate, extension projects and platforms (relaxation must stay off) ----
mut('M01', 'NONE (expected survivor)', 'V2-G4 and V2-E9 reach the project only through CLAUDE_PROJECT_DIR; no case gives the project through the stdin cwd',
    'the gate resolves the project root from CLAUDE_PROJECT_DIR only, not through _sg_ext_root (stdin cwd is forgotten)',
    ('  local root\n  root="$(_sg_ext_root)"\n  if [[ -z "$root" || ! -e', '  local root\n  root="${CLAUDE_PROJECT_DIR:-}"\n  if [[ -z "$root" || ! -e'))
mut('M02', 'NONE (expected survivor)', 'the only e2e case that sets an extension (V2-E9) is whole mode; the segment-mode trigger point is exercised only with the gate open',
    'segment-mode trigger point does not ask the gate (copy-paste slip: if true)',
    ('if _sg_relax_ok; then _SG_OV_PAT="a command segment is longer than', 'if true; then _SG_OV_PAT="a command segment is longer than'))
mut('M03', 'V2-E9-extension-project', 'whole-mode trigger point without the gate: the extension project reruns and is allowed (rc 0 vs baseline rc 2)',
    'whole-mode trigger point does not ask the gate (if true)',
    ('if _sg_relax_ok; then _SG_OV_PAT="the command is longer than', 'if true; then _SG_OV_PAT="the command is longer than'))
mut('M04', 'NONE (expected survivor)', 'V2-G3b and V2-E8 poison OSTYPE only; MACHTYPE equals BASH_VERSINFO[5] unless the environment sets it',
    'the platform argument is $MACHTYPE (environment-writable) instead of ${BASH_VERSINFO[5]}',
    ('_sg_relax_platform "${BASH_VERSINFO[5]:-}" "${BASH_VERSINFO[0]:-0}"', '_sg_relax_platform "${MACHTYPE:-}" "${BASH_VERSINFO[0]:-0}"'))
mut('M05', 'V2-G2-platform:x86_64-pc-linux-gnu:5.4', 'control: the version table has a 5.4 row',
    'bash minor limit <= 9 instead of <= 3',
    ('(( ${2:-0} == 5 && ${3:-0} <= 3 ))', '(( ${2:-0} == 5 && ${3:-0} <= 9 ))'))

# ---- B: cooperative time checkpoints inside the rerun (must return 3 = fall back; a slip to 0 is an allow without judgement) ----
CK = '[[ -n "${_SG_RELAXED:-}" ]] && return 3   # 10CG/aria-plugin#217 relaxed rerun: no time text of its own, the caller falls back to the baseline block\n'
mut('M06', 'NONE (expected survivor)', 'V4-S7 stubs _sg_vx_pass itself; no case runs the real whole-mode checkpoint inside the rerun',
    'whole-mode time checkpoint inside the rerun returns 0 (allow) instead of 3',
    ('      ' + CK + '      _sg_emit_blocked "time" "$cmd" whole timeout', '      [[ -n "${_SG_RELAXED:-}" ]] && return 0\n      _sg_emit_blocked "time" "$cmd" whole timeout'))
mut('M07', 'NONE (expected survivor)', 'same: the segment-loop checkpoint inside the rerun is never run for real',
    'segment-mode time checkpoint inside the rerun returns 0 (allow) instead of 3',
    ('      ' + CK + '      _sg_emit_blocked "time" "$cmd" segment timeout', '      [[ -n "${_SG_RELAXED:-}" ]] && return 0\n      _sg_emit_blocked "time" "$cmd" segment timeout'))
mut('M08', 'NONE (expected survivor)', 'same: the chaining checkpoint result (status 3 of _sg_vx_collect) inside the rerun is never run for real',
    'collect-chaining time checkpoint inside the rerun returns 0 (allow) instead of 3',
    ('    ' + CK + '    _sg_emit_blocked "time" "$cmd" "$mode" timeout', '    [[ -n "${_SG_RELAXED:-}" ]] && return 0\n    _sg_emit_blocked "time" "$cmd" "$mode" timeout'))

# ---- C: segment mode inside the rerun ----
mut('M09', 'NONE (expected survivor)', 'no e2e case reaches the deadline fallback in segment mode (V6-E2 and the other fallback cases are whole mode)',
    'the segment-mode fallback text names the whole-command limit (copy-paste slip in _SG_OV_PAT)',
    ('_SG_OV_PAT="a command segment is longer than $_SGV_SMAX characters after variable expansion"; _SG_OV_MODE=segment; return 4', '_SG_OV_PAT="the command is longer than $_SGV_SMAX characters after variable expansion"; _SG_OV_MODE=segment; return 4'))
mut('M10', 'NONE (expected survivor)', 'V10-N* and V7-N5 call _sg_vx_big_judge directly; V7-E13/E14 are whole mode; V9-E11 (segment) has no read',
    'segment mode inside the rerun judges a big copy with the normal _sg_judge_one (no routing to _sg_vx_big_judge)',
    ('then _sg_vx_big_judge "$_SG_SUB" segment; else _sg_judge_one "$_SG_SUB" segment; fi', 'then _sg_judge_one "$_SG_SUB" segment; else _sg_judge_one "$_SG_SUB" segment; fi'))
mut('M11', 'V7-E14-long-line-from-expansion', 'control: whole mode with a >8192 line after expansion must give the longline text',
    'whole mode inside the rerun judges a big copy with the normal _sg_judge_one',
    ('then _sg_vx_big_judge "$_SG_SUB" whole; return $?; fi', 'then _sg_judge_one "$_SG_SUB" whole; return $?; fi'))
mut('M17', 'NONE (expected survivor)', 'V8-D1..D3 call _sg_vx_apply directly (status only); no sc-cases e2e has a growth overrun (kind growth is never wanted)',
    'segment growth overrun inside the rerun skips the segment instead of blocking (fail-open)',
    ('      if [[ -n "${_SG_RELAXED:-}" ]]; then\n        _sg_emit_blocked "a command segment grows by more than $_SGV_GMAX characters after variable expansion" "$cmd" segment oversize\n        return 2\n      fi\n',
     '      if [[ -n "${_SG_RELAXED:-}" ]]; then\n        continue\n      fi\n'))
mut('M18', 'NONE (expected survivor)', 'same for the whole-command growth overrun',
    'whole growth overrun inside the rerun returns 0 (allow) instead of blocking (fail-open)',
    ('      if [[ -n "${_SG_RELAXED:-}" ]]; then\n        _sg_emit_blocked "the command grows by more than $_SGV_GMAX characters after variable expansion" "$cmd" whole oversize\n        return 2\n      fi\n',
     '      if [[ -n "${_SG_RELAXED:-}" ]]; then\n        return 0\n      fi\n'))

# ---- D: counts, boundaries, sentinels ----
mut('M12', 'NONE (expected survivor)', 'V9-C1 counts assignments, V9-C2 references; nothing counts for statements inside the rerun',
    'the rerun lifts the assignment bound but keeps the 8-for-statement bound',
    ('&& ca=1000000 cf=1000000   #', '&& ca=1000000   #'))
mut('M13', 'NONE (expected survivor)', 'V10 uses a 9000-character line, V7-N5 short lines: nothing probes the 8192 / 8193 edge of the longest line',
    'the longest-line edge is >= 8192 instead of > 8192',
    ('  if (( max > _SGV_LMAX )); then _sg_judge_one "$1" "$2" nocredit;', '  if (( max >= _SGV_LMAX )); then _sg_judge_one "$1" "$2" nocredit;'))
mut('M14', 'NONE (expected survivor)', 'no case makes the line-length read loop fail to run (seen=0)',
    'the unmeasurable-length sentinel routes to the credit path (max=0) instead of rows only',
    ('(( seen )) || max=$(( _SGV_LMAX + 1 ))', '(( seen )) || max=0'))

# ---- E: texts and bytes ----
mut('M15', 'NONE (expected survivor)', 'V4-S2 reads stderr through $(cat) which strips the trailing newline; no e2e case compares the bytes of a relaxed block text',
    'the relaxed block text is re-printed without its final newline',
    ("{ printf '%s\\n' \"$out\" >&2; return 2; }", "{ printf '%s' \"$out\" >&2; return 2; }"))
mut('M16', 'V4-S3-block-without-text', 'control: a block without text must fall back',
    'a job exit 2 without a text counts as a block',
    ('[[ $rc -eq 2 && -n "$out" ]] && {', '[[ $rc -eq 2 ]] && {'))
mut('M19', 'V6-E2-deadline-fallback-bytes (if bash prints the job-kill notice)', 'the command substitution would print the job-termination notice into the hook stderr',
    'the command substitution keeps stderr (no exec 2>/dev/null)',
    ('out="$( exec 2>/dev/null; set -m\n', 'out="$( set -m\n'))

# ---- G: environments ----
mut('M20', 'NONE (expected survivor)', 'nothing runs the hook with SIGTERM ignored',
    'the timer and the post-wait group kill use TERM instead of KILL',
    ('kill -KILL -- "-$me"', 'kill -TERM -- "-$me"'), ('          kill -KILL -- "-$jp"', '          kill -TERM -- "-$jp"'))
mut('M21', 'NONE (expected survivor)', 'cap=3 is only visible when the budget differs from 3; V3-E5 (budget 1) would catch a constant cap, but a floor of the cap at the default cannot be seen',
    'time-left is computed with cap=3 only (a budget of 1 or 2 is ignored)',
    ('  cap=$(( _SG_TIME_BUDGET < 3 ? _SG_TIME_BUDGET : 3 ))\n', '  cap=3\n'))
with open(os.path.join(out, 'predictions.tsv'), 'w', encoding='utf-8') as d:
    for i, expect, why, desc, pairs in M:
        t = base
        for old, new in pairs:
            n = t.count(old)
            if n != 1: sys.exit(f'{i}: replacement hit {n} times: {old[:80]!r}')
            t = t.replace(old, new)
        open(os.path.join(out, i + '.sh'), 'w', encoding='utf-8').write(t)
        d.write(f"{i}\t{expect}\t{why}\t{desc}\n")
print(len(M), 'mutants')
