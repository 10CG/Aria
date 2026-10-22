#!/usr/bin/env python3
"""commentsync.py <hook> <test suite> <baseline|target>: the What 7 closed list of comment sites.
Comment text is read the way a reader sees it: every run of consecutive comment lines is stripped of its '#' prefix, whitespace is collapsed, and the run
is joined into one string, so a phrase that the source wraps across two lines is still found once. baseline: every RETIRE phrase occurs exactly once and
every ADD word zero times (so the check can fail); target: every RETIRE phrase zero times and every ADD word at least once."""
import re, sys
hook, tests, mode = sys.argv[1], sys.argv[2], sys.argv[3]
def runs(path):
    out, cur = [], []
    for ln in open(path, encoding='utf-8'):
        m = re.match(r'\s*#(.*)$', ln.rstrip('\n'))
        if m and not ln.lstrip().startswith('#!'):
            cur.append(m.group(1))
        else:
            if cur: out.append(re.sub(r'\s+', ' ', ' '.join(cur)).strip()); cur = []
    if cur: out.append(re.sub(r'\s+', ' ', ' '.join(cur)).strip())
    return '\n'.join(out)
H, T = runs(hook), runs(tests)
# (site, file, RETIRE phrase)
RETIRE = [
 ('1 hook :87-95 header W10 gap', H, 'beyond a SIZE limit the whole command is BLOCKED as too large to scan'),
 ('2 hook :577-590 LENGTH BUDGET', H, 'Beyond ANY of them the whole command is BLOCKED'),
 ('2 hook :577-590 LENGTH BUDGET', H, 'blocking is as cheap as passing was'),
 ('2 hook :577-590 LENGTH BUDGET', H, 'The limit counts the whole judged string, not its growth'),
 ('3 hook :597-606 time budget', H, 'the _SGV_* size budget are unchanged'),
 ('4 hook :674-676 _sg_vx_apply', H, '2 = the copy would be longer than _SGV_SMAX'),
 ('5 hook :701-703 _sg_vx_pass', H, 'ends the pass at once with an oversize BLOCK'),
 ('6 hook :826-828 _sg_emit_blocked', H, '_sg_emit_blocked PAT SEG MODE [oversize]'),
 ('7 hook :1492-1496 _sg_judge_one', H, 'string to judge, $2 = mode (whole|segment). Returns'),
 ('8 hook :1528-1536 _sg_per_segment_eval', H, '2. only if it allowed, the W10 variable pass (_sg_vx_pass);'),
 ('9 test :2510-2518 block head', T, 'beyond a limit the command is BLOCKED'),
 ('9 test :2510-2518 block head', T, '_SGV_SMAX 8192 = one substituted copy'),
 ('10 test :2544-2549 21aa/21ab', T, 'the WHOLE judged string, not its growth'),
 ('10 test :2556-2562 21ac/21ad', T, 'which is how a 4096-character list is refused'),
]
ADD = [('hook', H, w) for w in ('_SGV_GMAX', '_SGV_LMAX', '_SG_P0', 'hard deadline', 'nocredit', 'longline', '_sg_relax_run', 'status 4')] + \
      [('test', T, w) for w in ('_SGV_GMAX', 'longline')]
bad = 0
for site, txt, ph in RETIRE:
    n = txt.count(ph); ok = (n == 1) if mode == 'baseline' else (n == 0)
    bad += not ok
    print(f"{'ok ' if ok else 'RED'} retire  {site:38s} n={n}  {ph}")
for f, txt, w in ADD:
    n = txt.count(w); ok = (n == 0) if mode == 'baseline' else (n >= 1)
    bad += not ok
    print(f"{'ok ' if ok else 'RED'} add     {f:4s} n={n}  {w}")
print(f"{mode}: {'GREEN' if bad == 0 else 'RED (%d)' % bad}")
sys.exit(1 if bad else 0)
