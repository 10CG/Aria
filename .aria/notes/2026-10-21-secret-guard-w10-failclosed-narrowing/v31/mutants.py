#!/usr/bin/env python3
"""mutants.py <v3.1 hook> <out dir> : the bad implementations of the BI list, each = the v3.1 prototype + ONE change (a realistic slip of the author).
Built by the author of the prototype, so they are a self-check of sc-cases.sh, not the non-author construction of TASK-003. Writes <out dir>/BI-n.sh and
<out dir>/designated.tsv (BI id, the case ids that must turn red, one-line description). Every replacement must hit exactly once."""
import sys, os
src, out = sys.argv[1], sys.argv[2]
base = open(src, encoding='utf-8').read()
os.makedirs(out, exist_ok=True)
M = []   # (id, designated case-id regexes, description, [(old, new)])
def mut(i, cases, desc, *pairs): M.append((i, cases, desc, pairs))
RUN_OLD = base[base.index('  out="$( exec 2>/dev/null; set -m'):base.index('  return 4\n}', base.index('  out="$( exec 2>/dev/null; set -m')) + len('  return 4\n}')]
mut('BI-1', ['V4-S6-spoofed-tail-0'], 'verdict read from the last line of the output text (v2)',
    ('  [[ $rc -eq 77 ]] && return 0\n', '  [[ $rc -eq 77 || "${out##*$\'\\n\'}" == 0 ]] && return 0\n'))
mut('BI-2', ['V5-S5-pipe-holder', 'V6-E2-deadline-fallback-bytes'], 'no process group and no group-leader self-check: the job PID alone is killed',
    ('out="$( exec 2>/dev/null; set -m\n', 'out="$( exec 2>/dev/null\n'),
    ('  { IFS= read -r st < "/proc/$BASHPID/stat"; } 2>/dev/null || return 9\n  st="${st##*) }"; f=( $st )\n  [[ "${f[2]:-}" == "$BASHPID" ]] || return 9\n', ''),
    ('kill -KILL -- "-$me"', 'kill -KILL "$me"'), ('          kill -KILL -- "-$jp"', '          kill -KILL "$jp"'))
mut('BI-3', ['V5-S10c-dead-timer-no-judgement', 'V5-S10d-no-judgement-with-dead-timer'], 'the judgement starts without checking that the timer runs',
    ('  [[ -n "$tp" ]] && kill -0 "$tp" 2>/dev/null || return 9   # no running timer, no judgement: the deadline must exist before the first expensive step\n', ''))
mut('BI-4', ['V6-E2-deadline-fallback-bytes'], 'the relaxed rerun runs in-process: no job, no hard deadline',
    (RUN_OLD, '  _SG_RELAXED=1; _sg_vx_pass "$1" "$_SG_MODE"; rc=$?; _SG_RELAXED=\n  case $rc in 0) return 0 ;; 2) return 2 ;; *) return 4 ;; esac\n}'))
mut('BI-5', ['V2-G4-extension-file-with-entry', 'V2-E9-extension-project'], 'the gate does not ask about a project extension',
    ('  [[ "$( _sg_relax_noext 2>/dev/null )" == none ]]\n}', '  return 0\n}'))
mut('BI-6', ['V2-G3-gate-calls-platform', 'V2-G3b-gate-uses-build-facts', 'V2-E8-ostype-from-environment-ignored'], 'the platform is read from the environment (OSTYPE, EPOCHREALTIME present)',
    ('  _sg_relax_platform "${BASH_VERSINFO[5]:-}" "${BASH_VERSINFO[0]:-0}" "${BASH_VERSINFO[1]:-0}" || return 1', '  [[ "${OSTYPE:-}" == linux* && -n "${EPOCHREALTIME:-}" ]] || return 1'))
mut('BI-7', ['V6-E2-deadline-fallback-bytes'], 'the fallback writes a time text of its own instead of the baseline size text',
    ('{ _sg_emit_blocked "$_SG_OV_PAT" "$cmd" "$_SG_OV_MODE" oversize; return 2; }', '{ _sg_emit_blocked "time" "$cmd" "$_SG_OV_MODE" timeout; return 2; }'))
mut('BI-8', ['V9-E12-vmax-unchanged'], 'VMAX relaxed too', ('_SGV_VMAX=4096\n', '_SGV_VMAX=8192\n'))
mut('BI-9', ['V8-D3-growth-8193-plain', 'V8-D3-growth-8193-braced'], 'the growth limit is recomputed from the rewritten string, per variable',
    ('    n="${_SGV_N[i]}"; v="${_SGV_V[i]}"\n    [[ -n "$v" ]] || continue\n    if [[ "$s" == *"\\${$n}"* ]]',
     '    n="${_SGV_N[i]}"; v="${_SGV_V[i]}"\n    [[ -n "${_SG_RELAXED:-}" ]] && lim=$(( ${#s} + _SGV_GMAX ))\n    [[ -n "$v" ]] || continue\n    if [[ "$s" == *"\\${$n}"* ]]'))
mut('BI-10', ['V7-E14-long-line-from-expansion'], 'the longest line is measured on the raw command, not on the copy',
    ('done <<< "$1"\n  (( seen ))', 'done <<< "${command:-$1}"\n  (( seen ))'))
mut('BI-11', ['V10-N3-environ-big-judge', 'V11-S4-one-rule-loop'], 'rows only through a rule loop of its own, which skips the W12 neutralisation',
    ('  if (( max > _SGV_LMAX )); then _sg_judge_one "$1" "$2" nocredit; else _sg_judge_one "$1" "$2"; fi',
     '  if (( max > _SGV_LMAX )); then local pat; for pat in "${risky_patterns[@]}"; do [[ "$1" =~ $pat ]] && { _sg_emit_blocked "$pat" "$1" "$2" longline; return 2; }; done; return 0; else _sg_judge_one "$1" "$2"; fi'))
mut('BI-12', ['V7-N5-read-big-judge-short-lines', 'V7-E13-multiline-copy-normal-text'], 'the line length is tested with [[ =~ .{8193,} ]] (it matches across newlines)',
    ('  while IFS= read -r line; do seen=1; (( ${#line} > max )) && max=${#line}; done <<< "$1"\n', '  seen=1; [[ "$1" =~ .{8193,} ]] && max=8193\n'))
mut('BI-13', ['V3-E3-anchor-at-hook-start'], 'the deadline is anchored after the stdin parse, not at the hook start',
    ('_SG_P0=${EPOCHREALTIME:-}; _SG_RELAXED=   #', '_SG_P0=; _SG_RELAXED=   #'),
    ("done < <(jq -j '(.tool_name | type)", "_SG_P0=${EPOCHREALTIME:-}\ndone < <(jq -j '(.tool_name | type)"))
mut('BI-14', ['V3-G10-cap-3', 'V3-E4-cap-3-at-budget-4'], 'the deadline uses the whole budget, not min(budget, 3)',
    ('  cap=$(( _SG_TIME_BUDGET < 3 ? _SG_TIME_BUDGET : 3 ))\n', '  cap=$_SG_TIME_BUDGET\n'))
mut('BI-15', ['V5-S9-child-left-behind', 'V5-S13b-nothing-outlives-the-run'], 'the group is not killed after the job ends',
    ('          kill -KILL -- "-$jp"   # the timer and anything the judgement left behind: nothing of the job outlives it or holds the pipe\n', ''))
mut('BI-16', ['V2-G11-flag-not-from-environment', 'V2-E6-flag-from-environment-ignored'], 'the relaxed flag is taken from the environment (not initialised)',
    ('_SG_P0=${EPOCHREALTIME:-}; _SG_RELAXED=   #', '_SG_P0=${EPOCHREALTIME:-}   #'))
mut('BI-17', ['V9-C1-assignments-rerun', 'V9-C2-references-rerun-c12', 'V9-E10-count-axis-read-blocked'], 'the count bounds also hold inside the rerun',
    ('  [[ -n "${_SG_RELAXED:-}" ]] && ca=1000000 cf=1000000   # 10CG/aria-plugin#217 relaxed rerun: no count bound (the deadline caps the cost)\n', ''),
    ('  [[ -n "${_SG_RELAXED:-}" ]] && gc=1000000   # 10CG/aria-plugin#217 relaxed rerun: no count bound\n', ''),
    ('lim=$(( ${#1} + _SGV_GMAX )) gc=1000000', 'lim=$(( ${#1} + _SGV_GMAX ))'))
mut('BI-18', ['V9-E11-tmax-in-rerun'], 'TMAX is not checked inside the rerun',
    ('    if (( spent > _SGV_TMAX )); then\n', '    if [[ -z "${_SG_RELAXED:-}" ]] && (( spent > _SGV_TMAX )); then\n'))
mut('BI-19', ['V4-S11-bare-zero'], 'a bare 0 from the job counts as allowed', ('  [[ $rc -eq 77 ]] && return 0\n', '  [[ $rc -eq 77 || $rc -eq 0 ]] && return 0\n'))
mut('BI-20', ['V2-G4-empty-extension-file'], 'an empty extension file counts as no extension',
    ('! -e "$root/.aria/secret-guard.paths"', '! -s "$root/.aria/secret-guard.paths"'))
mut('BI-21', ['V3-G9-clock-backwards'], 'a clock that went backwards extends the deadline (time left not capped)',
    ('  (( now > cap * 1000000 )) && now=$(( cap * 1000000 ))   # a clock that went backwards never extends the deadline\n', ''))
mut('BI-22', ['V2-G6-no-time-left', 'V2-G7-no-anchor', 'V2-G8-budget-0'], 'the gate does not ask for time left',
    ('  _sg_relax_left || return 1\n  [[ "$( _sg_relax_noext', '  [[ "$( _sg_relax_noext'))
mut('BI-23', ['V5-S14-failing-sleep-kills-at-once'], 'the timer kills only after a successful sleep (&& instead of ;): a failing sleep leaves no deadline',
    ('( sleep "$_SG_LEFT"; kill -KILL -- "-$me" )', '( sleep "$_SG_LEFT" && kill -KILL -- "-$me" )'))
with open(os.path.join(out, 'designated.tsv'), 'w', encoding='utf-8') as d:
    for i, cases, desc, pairs in M:
        t = base
        for old, new in pairs:
            n = t.count(old)
            if n != 1: sys.exit(f'{i}: replacement hit {n} times: {old[:70]!r}')
            t = t.replace(old, new)
        with open(os.path.join(out, i + '.sh'), 'w', encoding='utf-8') as f: f.write(t)
        d.write(f"{i}\t{' '.join(cases)}\t{desc}\n")
print(len(M), 'mutants')
