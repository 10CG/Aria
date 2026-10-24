#!/usr/bin/env python3
"""mut.py <v31.sh> <outdir>: non-author bad implementations (v3.1 prototype + ONE realistic slip each). Defensive mutation testing of a security
hook's test-suite: the bad implementations exist only in the scratch directory. Every replacement must hit exactly once.
PREDICTION (written BEFORE running sc-cases.sh) is recorded in predictions.tsv: which case should catch it, or MISSED if I believe none does."""
import sys, os
src, out = sys.argv[1], sys.argv[2]
base = open(src, encoding='utf-8').read()
os.makedirs(out, exist_ok=True)
M = []
def mut(i, predicted, desc, *pairs): M.append((i, predicted, desc, pairs))

# M1: the gate finds the project root from CLAUDE_PROJECT_DIR only; the stdin `cwd` route of _sg_ext_root is forgotten
mut('M1', 'MISSED (V2-E9 / V2-G4 all set CLAUDE_PROJECT_DIR; no case drives the extension via stdin cwd)',
    'noext: project root from CLAUDE_PROJECT_DIR only, the stdin cwd route is dropped',
    ('  local root\n  root="$(_sg_ext_root)"\n  if [[ -z "$root" || ! -e "$root/.aria/secret-guard.paths" ]]; then printf none; fi',
     '  local root\n  root="${CLAUDE_PROJECT_DIR:-}"\n  if [[ -z "$root" || ! -e "$root/.aria/secret-guard.paths" ]]; then printf none; fi'))
# M2: the remaining time is printed without zero padding of the microseconds
mut('M2', 'MISSED (no case has a remaining time whose fraction is < 0.1 s; V3-G10 / G9 / all e2e have fractions >= .5)',
    'time left printed as %d.%d instead of %d.%06d (2.050000 s becomes "2.50000")',
    ("printf -v _SG_LEFT '%d.%06d'", "printf -v _SG_LEFT '%d.%d'"))
# M3: the empty-loop sentinel of _sg_vx_big_judge is dropped
mut('M3', 'MISSED (no case makes the here-string read loop run zero times)',
    'big_judge: the "length could not be measured -> rows only" sentinel removed',
    ('  (( seen )) || max=$(( _SGV_LMAX + 1 ))   # the length could not be measured: rows only, never the cheaper-to-pass credit path\n', ''))
# M4: credit is evaluated first, then a long-line copy is blocked only if it has no credit
mut('M4', 'MISSED (V10-N2 / V7-E14 / V9-E10 have no value-redacting filter, so credit is 0 and the longline text appears either way)',
    'judge_one: nocredit check moved behind the credit evaluation (a filtered long line is allowed by credit)',
    ('''      if [[ "$nocredit" == nocredit ]]; then   # 10CG/aria-plugin#217: a big copy with a line longer than _SGV_LMAX -- the match alone blocks, credit is not evaluated
        _sg_emit_blocked "$pat" "$seg" "$mode" longline
        return 2
      fi
      if [[ -z "$credit" ]]; then
        if _sg_compute_credit "$seg"; then credit=1; else credit=0; fi
      fi
      if [[ "$credit" == "0" ]]; then
        _sg_emit_blocked "$pat" "$seg" "$mode"
        return 2
      fi
''', '''      if [[ -z "$credit" ]]; then
        if _sg_compute_credit "$seg"; then credit=1; else credit=0; fi
      fi
      if [[ "$credit" == "0" ]]; then
        if [[ "$nocredit" == nocredit ]]; then _sg_emit_blocked "$pat" "$seg" "$mode" longline; else _sg_emit_blocked "$pat" "$seg" "$mode"; fi
        return 2
      fi
'''))
# M5: segment-mode trigger stores the whole-mode reason string for the fallback
mut('M5', 'MISSED (every deadline/fallback e2e case is whole mode: the shapes start with a parenthesis)',
    'segment trigger keeps the whole-mode baseline reason string for the fallback text',
    ('_SG_OV_PAT="a command segment is longer than $_SGV_SMAX characters after variable expansion"; _SG_OV_MODE=segment; return 4;',
     '_SG_OV_PAT="the command is longer than $_SGV_SMAX characters after variable expansion"; _SG_OV_MODE=segment; return 4;'))
# M6: LMAX boundary off by one
mut('M6', 'MISSED (no case has a copy whose longest line is exactly 8192 characters)',
    'big_judge: max > _SGV_LMAX became max >= _SGV_LMAX',
    ('  if (( max > _SGV_LMAX )); then _sg_judge_one "$1" "$2" nocredit', '  if (( max >= _SGV_LMAX )); then _sg_judge_one "$1" "$2" nocredit'))
# M7: the group-leader self-check is dropped but set -m stays
mut('M7', 'MISSED (set -m works on every measured bash, so the refusal branch never runs; no case calls _sg_relax_job outside a leader)',
    'relax_job: the /proc group-leader self-check removed, set -m kept',
    ('  { IFS= read -r st < "/proc/$BASHPID/stat"; } 2>/dev/null || return 9\n  st="${st##*) }"; f=( $st )\n  [[ "${f[2]:-}" == "$BASHPID" ]] || return 9\n', ''))
# M8: the three time checkpoints of the rerun fall through to the time text instead of status 3
mut('M8', 'MISSED (no case drives _sg_vx_pass under _SG_RELAXED with an exhausted budget)',
    'vx_pass: the three "rerun -> return 3" checkpoint lines removed (the rerun writes the time text and returns 2)',
    ('    [[ -n "${_SG_RELAXED:-}" ]] && return 3   # 10CG/aria-plugin#217 relaxed rerun: no time text of its own, the caller falls back to the baseline block\n    _sg_emit_blocked "time" "$cmd" "$mode" timeout\n',
     '    _sg_emit_blocked "time" "$cmd" "$mode" timeout\n'),
    ('      [[ -n "${_SG_RELAXED:-}" ]] && return 3   # 10CG/aria-plugin#217 relaxed rerun: no time text of its own, the caller falls back to the baseline block\n      _sg_emit_blocked "time" "$cmd" whole timeout\n',
     '      _sg_emit_blocked "time" "$cmd" whole timeout\n'),
    ('      [[ -n "${_SG_RELAXED:-}" ]] && return 3   # 10CG/aria-plugin#217 relaxed rerun: no time text of its own, the caller falls back to the baseline block\n      _sg_emit_blocked "time" "$cmd" segment timeout\n',
     '      _sg_emit_blocked "time" "$cmd" segment timeout\n'))
# M9: whole-mode growth overrun inside the rerun is allowed (fail-open)
mut('M9', 'MISSED by sc-cases.sh (growth > 8192 is only checked at _sg_vx_apply status level, V8-D*; no e2e shape has growth > 8192)',
    'vx_pass whole mode, rerun: growth overrun returns 0 (allow) instead of the growth block',
    ('''        _sg_emit_blocked "the command grows by more than $_SGV_GMAX characters after variable expansion" "$cmd" whole oversize
        return 2
''', '''        return 0
'''))
# M10: segment-mode growth overrun inside the rerun is allowed
mut('M10', 'MISSED by sc-cases.sh (same as M9, segment branch)',
    'vx_pass segment mode, rerun: growth overrun returns 0 (allow) instead of the growth block',
    ('''        _sg_emit_blocked "a command segment grows by more than $_SGV_GMAX characters after variable expansion" "$cmd" segment oversize
        return 2
''', '''        return 0
'''))
# M11: segment mode never routes a big copy through _sg_vx_big_judge
mut('M11', 'MISSED (the longline e2e shapes are whole mode; no segment-mode copy > 8192 with a reader)',
    'vx_pass segment mode: _sg_vx_big_judge not used, every segment copy goes to the normal judgement',
    ('    if [[ -n "${_SG_RELAXED:-}" ]] && (( ${#_SG_SUB} > _SGV_SMAX )); then _sg_vx_big_judge "$_SG_SUB" segment; else _sg_judge_one "$_SG_SUB" segment; fi\n',
     '    _sg_judge_one "$_SG_SUB" segment\n'))
# M12: fallback after a failed rerun returns 0 for segment mode only? -> instead: fallback keeps text but returns 0 (fail-open) -- sanity mutant, expected CAUGHT
mut('M12', 'CAUGHT by V6-E2 (fallback must exit 2)',
    'per_segment_eval: the fallback writes the baseline text but returns 0 (fail-open)',
    ('{ _sg_emit_blocked "$_SG_OV_PAT" "$cmd" "$_SG_OV_MODE" oversize; return 2; }', '{ _sg_emit_blocked "$_SG_OV_PAT" "$cmd" "$_SG_OV_MODE" oversize; return 0; }'))
# M13: the job's timer targets $$ (the hook's pid) instead of the job's pid
mut('M13', 'CAUGHT by V6-E2 / V3-E3.. (deadline not enforced: the kill goes to the wrong group)',
    'relax_job: timer kills -$$ instead of -$BASHPID (hook pid instead of job pid)',
    ('local me=$BASHPID tp', 'local me=$$ tp'))
with open(os.path.join(out, 'predictions.tsv'), 'w', encoding='utf-8') as d:
    for i, predicted, desc, pairs in M:
        t = base
        for old, new in pairs:
            n = t.count(old)
            if n != 1:
                sys.exit(f'{i}: replacement hit {n} times: {old[:90]!r}')
            t = t.replace(old, new)
        with open(os.path.join(out, i + '.sh'), 'w', encoding='utf-8') as f:
            f.write(t)
        d.write(f"{i}\t{predicted}\t{desc}\n")
print(len(M), 'mutants')
