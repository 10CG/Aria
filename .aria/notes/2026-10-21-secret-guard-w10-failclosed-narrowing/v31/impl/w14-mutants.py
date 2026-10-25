#!/usr/bin/env python3
# w14-mutants.py <implementation hook> <output dir> [Q-n ...]
#
# TASK-003 first stage (10CG/aria-plugin#217), independent mutants, QA seat (not the author).
# Defensive context: this is MUTATION TESTING of a leak-prevention hook. Every mutant is the implementation plus ONE
# plausible authoring mistake (a few verbatim replacements that make up that one mistake). The mutants exist only in the
# output directory (scratchpad), are only run through the regression suite, are never installed and never enter a repo.
# Each replacement asserts that the original text occurs exactly once in the implementation (and the implementation's
# sha256 prefix is checked first, INV-8).
import hashlib
import os
import sys

IMPL_SHA12 = "628652570ce3"

# (id, short title, [(original, replacement), ...])
MUTANTS = [
    ("Q-1", "platform: bash minor bound <= 3 written as < 3 (5.3 leaves the measured range)",
     [(r'''(( ${2:-0} == 5 && ${3:-0} <= 3 ))''',
       r'''(( ${2:-0} == 5 && ${3:-0} < 3 ))''')]),

    ("Q-2", "platform: bash major test == 5 written as >= 5 (a future 6.x is admitted)",
     [(r'''(( ${2:-0} == 5 && ${3:-0} <= 3 ))''',
       r'''(( ${2:-0} >= 5 && ${3:-0} <= 3 ))''')]),

    ("Q-3", "platform: build glob x86_64-*-linux-gnu* loosened to x86_64-*-linux-* (musl and other libc admitted)",
     [(r'''"${1:-}" == x86_64-*-linux-gnu*''',
       r'''"${1:-}" == x86_64-*-linux-*''')]),

    ("Q-4", "platform: kernel string test *[Mm]icrosoft* written as *Microsoft* (lower-case microsoft not recognised)",
     [(r'''"${4:-}" != *[Mm]icrosoft*''',
       r'''"${4:-}" != *Microsoft*''')]),

    ("Q-5", "gate: platform argument 1 read from $MACHTYPE (the environment can rewrite it) instead of BASH_VERSINFO[5]",
     [(r'''_sg_relax_platform "${BASH_VERSINFO[5]:-}" "${BASH_VERSINFO[0]:-0}"''',
       r'''_sg_relax_platform "${MACHTYPE:-}" "${BASH_VERSINFO[0]:-0}"''')]),

    ("Q-6", "gate: _sg_relax_noext || written as && (relaxation only when no project root is found)",
     [(r'''if [[ -z "$root" || ! -e "$root/.aria/secret-guard.paths" ]]; then printf none; fi''',
       r'''if [[ -z "$root" && ! -e "$root/.aria/secret-guard.paths" ]]; then printf none; fi''')]),

    ("Q-7", "trigger: the segment-mode trigger point never relaxes (only the whole-command one does)",
     [(r'''if _sg_relax_ok; then _SG_OV_PAT="a command segment is longer than''',
       r'''if false; then _SG_OV_PAT="a command segment is longer than''')]),

    ("Q-8", "gate: extension probe -e written as -f (a directory at .aria/secret-guard.paths counts as no extension)",
     [(r'''! -e "$root/.aria/secret-guard.paths"''',
       r'''! -f "$root/.aria/secret-guard.paths"''')]),

    ("Q-9", "rerun: growth limit recomputed per variable from the already rewritten s instead of the input length (BI-9)",
     [('''    n="${_SGV_N[i]}"; v="${_SGV_V[i]}"
    [[ -n "$v" ]] || continue
''',
       '''    n="${_SGV_N[i]}"; v="${_SGV_V[i]}"
    [[ -n "$v" ]] || continue
    [[ -n "${_SG_RELAXED:-}" ]] && lim=$(( ${#s} + _SGV_GMAX ))
''')]),

    ("Q-10", "rerun: the 8-for-statements count bound is not lifted (only the 16-assignment bound is)",
     [(r'''[[ -n "${_SG_RELAXED:-}" ]] && ca=1000000 cf=1000000''',
       r'''[[ -n "${_SG_RELAXED:-}" ]] && ca=1000000''')]),

    ("Q-11", "rerun: the 8-replacements bound of the ${NAME} spelling (_sg_vx_replace) is not lifted",
     [(r'''[[ -n "${_SG_RELAXED:-}" ]] && gc=1000000   # 10CG/aria-plugin#217 relaxed rerun: no count bound''',
       r''': # mutant Q-11: the bound stays 8''')]),

    ("Q-12", "rerun: the 8-replacements bound of the $NAME spelling (_sg_vx_apply loop) is not lifted",
     [(r'''lim=$(( ${#1} + _SGV_GMAX )) gc=1000000''',
       r'''lim=$(( ${#1} + _SGV_GMAX ))''')]),

    ("Q-13", "rerun: longest-line test max > _SGV_LMAX written as >= (a line of exactly 8192 loses its credit path)",
     [(r'''if (( max > _SGV_LMAX )); then _sg_judge_one "$1" "$2" nocredit;''',
       r'''if (( max >= _SGV_LMAX )); then _sg_judge_one "$1" "$2" nocredit;''')]),

    ("Q-14", "rerun: the longest-line read loop forgets IFS= (leading and trailing blanks are trimmed from the measure)",
     [(r'''while IFS= read -r line; do seen=1;''',
       r'''while read -r line; do seen=1;''')]),

    ("Q-15", "rerun: the nocredit branch is moved behind the credit computation (order swapped)",
     [('''      if [[ "$nocredit" == nocredit ]]; then   # 10CG/aria-plugin#217: a big copy with a line longer than _SGV_LMAX -- the match alone blocks, credit is not evaluated
        _sg_emit_blocked "$pat" "$seg" "$mode" longline
        return 2
      fi
      if [[ -z "$credit" ]]; then
        if _sg_compute_credit "$seg"; then credit=1; else credit=0; fi
      fi
''',
       '''      if [[ -z "$credit" ]]; then
        if _sg_compute_credit "$seg"; then credit=1; else credit=0; fi
      fi
      if [[ "$nocredit" == nocredit ]]; then
        _sg_emit_blocked "$pat" "$seg" "$mode" longline
        return 2
      fi
''')]),

    ("Q-16", "job: the timer sleeps the whole budget instead of the time left to the deadline",
     [(r'''( sleep "$_SG_LEFT"; kill -KILL -- "-$me" )''',
       r'''( sleep "$_SG_TIME_BUDGET"; kill -KILL -- "-$me" )''')]),

    ("Q-17", "job: the command substitution does not silence its own stderr (exec 2>/dev/null dropped)",
     [(r'''out="$( exec 2>/dev/null; set -m''',
       r'''out="$( set -m''')]),

    ("Q-18", "job: the job's block text is replayed without its final newline",
     [(r'''printf '%s\n' "$out" >&2; return 2; }''',
       r'''printf '%s' "$out" >&2; return 2; }''')]),

    ("Q-19", "job: the group kill after wait is dropped (nothing cleans up behind the job)",
     [(r'''kill -KILL -- "-$jp"   # the timer and anything''',
       r''': # mutant Q-19 # the timer and anything''')]),

    ("Q-20", "fallback: the segment trigger stores the whole-command reason string (copy-paste between the two trigger lines)",
     [(r'''_SG_OV_PAT="a command segment is longer than $_SGV_SMAX characters after variable expansion"; _SG_OV_MODE=segment; return 4;''',
       r'''_SG_OV_PAT="the command is longer than $_SGV_SMAX characters after variable expansion"; _SG_OV_MODE=segment; return 4;''')]),

    ("Q-21", "text: the segment-mode growth text uses the whole-command wording",
     [(r'''_sg_emit_blocked "a command segment grows by more than $_SGV_GMAX characters after variable expansion" "$cmd" segment oversize''',
       r'''_sg_emit_blocked "the command grows by more than $_SGV_GMAX characters after variable expansion" "$cmd" segment oversize''')]),

    ("Q-22", "text: the longline call passes segment and pattern in swapped order (the copy is shown as the matched pattern)",
     [(r'''_sg_emit_blocked "$pat" "$seg" "$mode" longline''',
       r'''_sg_emit_blocked "$seg" "$pat" "$mode" longline''')]),

    ("Q-23", "text: the longline text echoes the first 200 characters of the substituted copy instead of the command",
     [('''命令读取含密钥的来源, 且变量展开后有超长的行, 这个尺寸下不评估脱敏过滤, 请拆成更小的命令

Command was (first 200 characters): $(_sg_redact_echo "${command:0:200}")''',
       '''命令读取含密钥的来源, 且变量展开后有超长的行, 这个尺寸下不评估脱敏过滤, 请拆成更小的命令

Command was (first 200 characters): $(_sg_redact_echo "${seg:0:200}")''')]),

    ("Q-24", "anchor: the deadline anchor is re-taken where the time-budget clock is reset (start of the W10 pass, not of the hook)",
     [(r'''_SG_T0=$SECONDS; _sg_time_budget   # reset the time-budget clock''',
       r'''_SG_T0=$SECONDS; _SG_P0=${EPOCHREALTIME:-}; _sg_time_budget   # reset the time-budget clock''')]),

    ("Q-25", "anchor: _SG_RELAXED is initialised from the environment (reads a value it must not trust)",
     [(r'''_SG_P0=${EPOCHREALTIME:-}; _SG_RELAXED=   #''',
       r'''_SG_P0=${EPOCHREALTIME:-}; _SG_RELAXED=${_SG_RELAXED:-}   #''')]),

    ("Q-26", "budget: the deadline cap min(budget, 3) written as max(budget, 3)",
     [(r'''cap=$(( _SG_TIME_BUDGET < 3 ? _SG_TIME_BUDGET : 3 ))''',
       r'''cap=$(( _SG_TIME_BUDGET > 3 ? _SG_TIME_BUDGET : 3 ))''')]),

    ("Q-27", "budget: time left printed with %d.%d instead of %d.%06d (0.05 s reads as 0.5 s)",
     [(r'''printf -v _SG_LEFT '%d.%06d' $(( now / 1000000 ))''',
       r'''printf -v _SG_LEFT '%d.%d' $(( now / 1000000 ))''')]),

    ("Q-28", "budget: the 'a clock that went backwards never extends the deadline' cap is dropped",
     [(r'''(( now > cap * 1000000 )) && now=$(( cap * 1000000 ))   # a clock that went backwards never extends the deadline''',
       r''': # mutant Q-28''')]),

    ("Q-29", "fallback: the status 4 test in _sg_per_segment_eval is written -eq 3 (status 4 leaks to the caller)",
     [(r'''[[ $rc -eq 4 ]] && { _sg_emit_blocked "$_SG_OV_PAT" "$cmd" "$_SG_OV_MODE" oversize; return 2; }''',
       r'''[[ $rc -eq 3 ]] && { _sg_emit_blocked "$_SG_OV_PAT" "$cmd" "$_SG_OV_MODE" oversize; return 2; }''')]),

    ("Q-30", "gate: the time-left test is dropped from _sg_relax_ok (_sg_relax_run tests it again, so the output should not change)",
     [('''  _sg_relax_left || return 1
  _sg_relax_nowslfs''',
       '''  _sg_relax_nowslfs''')]),

    ("Q-31", "rerun: the growth limit uses _SGV_SMAX instead of _SGV_GMAX (both are 8192 today)",
     [(r'''lim=$(( ${#1} + _SGV_GMAX ))''',
       r'''lim=$(( ${#1} + _SGV_SMAX ))''')]),
]


def main():
    if len(sys.argv) < 3:
        sys.exit("usage: w14-mutants.py <implementation hook> <output dir> [Q-n ...]")
    src, out = sys.argv[1], sys.argv[2]
    want = set(sys.argv[3:])
    raw = open(src, "rb").read()
    got = hashlib.sha256(raw).hexdigest()[:12]
    if got != IMPL_SHA12:
        sys.exit("w14-mutants.py: %s has sha256 prefix %s, expected %s (INV-8)" % (src, got, IMPL_SHA12))
    text = raw.decode("utf-8")
    os.makedirs(out, exist_ok=True)
    made = 0
    for qid, title, reps in MUTANTS:
        if want and qid not in want:
            continue
        t = text
        for old, new in reps:
            n = t.count(old)
            if n != 1:
                sys.exit("w14-mutants.py: %s: the original text occurs %d times (need exactly 1): %r" % (qid, n, old[:80]))
            t = t.replace(old, new)
        if t == text:
            sys.exit("w14-mutants.py: %s: the replacement changed nothing" % qid)
        path = os.path.join(out, qid + ".sh")
        with open(path, "wb") as f:
            f.write(t.encode("utf-8"))
        os.chmod(path, 0o755)
        print("%s\t%s\t%s" % (qid, hashlib.sha256(t.encode("utf-8")).hexdigest()[:12], title))
        made += 1
    if want and made != len(want):
        sys.exit("w14-mutants.py: asked for %d ids, made %d" % (len(want), made))


if __name__ == "__main__":
    main()
