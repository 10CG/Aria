#!/usr/bin/env python3
"""mkmut2.py <v3.1 hook> <out dir> : second batch of non-author mutants (qa-engineer, 10CG/aria-plugin#217 post_planning R2). Predictions are written to predictions2.tsv before any run."""
import sys, os
src, out = sys.argv[1], sys.argv[2]
base = open(src, encoding='utf-8').read()
M = []
def mut(i, expect, why, desc, *pairs): M.append((i, expect, why, desc, pairs))
mut('M22', 'V9-E11-tmax-in-rerun', 'the job judges the whole command (kind growth) instead of per segment (kind tmax)',
    'the job hard-codes whole mode instead of $_SG_MODE',
    ('  _sg_vx_pass "$1" "$_SG_MODE"\n', '  _sg_vx_pass "$1" whole\n'))
mut('M24', 'NONE (expected survivor)', 'V9-E12 hits VMAX in the baseline pass; no case reaches a value over VMAX that only the rerun collects (the 17th assignment)',
    'inside the rerun a value over VMAX (status 2 of _sg_vx_collect) is ignored instead of blocking',
    ('  if [[ $cr -eq 2 ]]; then\n    _sg_emit_blocked "a variable value is longer than', '  if [[ $cr -eq 2 && -z "${_SG_RELAXED:-}" ]]; then\n    _sg_emit_blocked "a variable value is longer than'))
mut('M28', 'NONE (expected survivor)', 'the long lines of V10/V7-N5 have no leading or trailing whitespace; read without IFS= trims it',
    'the line-length loop reads without IFS= (leading/trailing blanks are trimmed from the measured line)',
    ('  while IFS= read -r line; do seen=1; (( ${#line} > max )) && max=${#line}; done <<< "$1"\n', '  while read -r line; do seen=1; (( ${#line} > max )) && max=${#line}; done <<< "$1"\n'))
mut('M29', 'NONE (expected survivor)', 'all three constants are 8192, so naming the wrong one (SMAX / LMAX / GMAX) is not observable',
    'rows-only edge uses _SGV_SMAX instead of _SGV_LMAX (numerically equal today)',
    ('  if (( max > _SGV_LMAX )); then _sg_judge_one "$1" "$2" nocredit;', '  if (( max > _SGV_SMAX )); then _sg_judge_one "$1" "$2" nocredit;'))
mut('M30', 'NONE (expected survivor)', 'nothing starts the hook with SIGHUP/SIGTERM ignored; KILL vs TERM only matters there (same as M20, but for the post-wait group kill alone)',
    'only the timer uses TERM (group kill after wait keeps KILL)',
    ('kill -KILL -- "-$me"', 'kill -TERM -- "-$me"'))
with open(os.path.join(out, 'predictions2.tsv'), 'w', encoding='utf-8') as d:
    for i, expect, why, desc, pairs in M:
        t = base
        for old, new in pairs:
            n = t.count(old)
            if n != 1: sys.exit(f'{i}: replacement hit {n} times: {old[:80]!r}')
            t = t.replace(old, new)
        open(os.path.join(out, i + '.sh'), 'w', encoding='utf-8').write(t)
        d.write(f"{i}\t{expect}\t{why}\t{desc}\n")
print(len(M), 'mutants')
