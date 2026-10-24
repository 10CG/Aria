#!/usr/bin/env python3
"""mk_delete.py BASE OUT : the baseline hook with the comment block of every What 7 hook site deleted whole (each run found as commentsync.py finds it: the
run right before its code line, or the header run's W10 bullet) and one comment line added that holds every ADD word -- the "whole-block deletion"
construction of post_planning R2 PP2-M, on the untouched baseline."""
import re, sys
src, out = sys.argv[1], sys.argv[2]
L = open(src, encoding='utf-8').read().split('\n')
NEXT = ['_SGV_N=(); _SGV_V=()', '_SG_T0=$SECONDS', '_sg_vx_apply() {', '_sg_vx_pass() {', '_sg_emit_blocked() {', '_sg_judge_one() {', '_sg_per_segment_eval() {', '_sg_vx_replace() {']
drop = set()
for key in NEXT:
    i = next(n for n, ln in enumerate(L) if ln.startswith(key))
    j = i - 1
    while j >= 0 and re.match(r'\s*#', L[j]) and not L[j].startswith('#!'): drop.add(j); j -= 1
# the header's W10 bullet: from "#   - Shell variable indirection" to the next bullet ("#   - ") or the end of the header
i = next(n for n, ln in enumerate(L) if 'Shell variable indirection' in ln)
drop.add(i); j = i + 1
while L[j].startswith('#     '): drop.add(j); j += 1
kept = [ln for n, ln in enumerate(L) if n not in drop]
k = next(n for n, ln in enumerate(kept) if ln.startswith('_SGV_N=(); _SGV_V=()'))
kept.insert(k, '# _SGV_GMAX _SGV_LMAX _SG_P0 hard deadline nocredit longline _sg_relax_run status 4')
open(out, 'w', encoding='utf-8').write('\n'.join(kept))
print('deleted', len(drop), 'comment lines')
