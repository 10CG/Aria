#!/usr/bin/env python3
"""commentsync.py [--hook-only | --suite-only] <hook> [<suite>] <baseline|target> : the What 7 closed list of comment sites, block level (v3.1).
A site is one comment block of the baseline (aria 59e333c), found by its anchor phrases. Comment text is read the way a reader sees it: every run of
consecutive comment lines is stripped of its '#' prefix, whitespace is collapsed, and the run is joined into one string, so a phrase the source wraps across
two lines is still found once. Each site also carries the sha256 (first 16 hex) of its whole baseline run.
  baseline: every anchor occurs exactly as often as listed, each site's run has the listed sha256, every ADD word occurs zero times -- so the check can fail.
  target:   no anchor occurs, no run with a listed sha256 is left (the whole block was rewritten, not one phrase), every ADD word occurs at least once.
Suite case titles that become untrue are checked as plain text (they are code, not comments). The rewritten text itself is reviewed (TASK-005)."""
import re, sys, hashlib
a = sys.argv[1:]
only = a.pop(0) if a and a[0] in ('--hook-only', '--suite-only') else None
if only == '--hook-only':
    hook, mode = a; suite = None
elif only == '--suite-only':
    suite, mode = a; hook = None
else:
    hook, suite, mode = a
assert mode in ('baseline', 'target'), mode
def runs(path):
    out, cur = [], []
    for ln in open(path, encoding='utf-8'):
        m = re.match(r'\s*#(.*)$', ln.rstrip('\n'))
        if m and not ln.lstrip().startswith('#!'):
            cur.append(m.group(1))
        else:
            if cur: out.append(re.sub(r'\s+', ' ', ' '.join(cur)).strip()); cur = []
    if cur: out.append(re.sub(r'\s+', ' ', ' '.join(cur)).strip())
    return out
sha = lambda s: hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]
# (site, baseline sha256 of the whole run, [(anchor phrase, baseline count)])
HOOK_SITES = [
 ('1 hook :87-95 header W10 gap', 'deb0ac78daffb395', [('beyond a SIZE limit the whole command is BLOCKED as too large to scan', 1), ('never passed', 2)]),
 ('2 hook :577-590 LENGTH BUDGET', 'ccc5d4d623e6707e', [('Beyond ANY of them the whole command is BLOCKED', 1), ('blocking is as cheap as passing was', 1),
                                           ('The limit counts the whole judged string, not its growth', 1)]),
 ('3 hook :597-606 time budget', '4f80e337cf4f7bb9', [('the _SGV_* size budget are unchanged', 1)]),
 ('4 hook :674-676 _sg_vx_apply', '3f15b92e57d303ec', [('2 = the copy would be longer than _SGV_SMAX', 1)]),
 ('5 hook :701-703 _sg_vx_pass', '12bfb333904a113c', [('ends the pass at once with an oversize BLOCK', 1)]),
 ('6 hook :826-828 _sg_emit_blocked', 'e3149a7b70a73438', [('_sg_emit_blocked PAT SEG MODE [oversize]', 1)]),
 ('7 hook :1492-1496 _sg_judge_one', 'abf172890d25f686', [('string to judge, $2 = mode (whole|segment). Returns', 1)]),
 ('8 hook :1531-1536 _sg_per_segment_eval', '02cc1e169164ae2c', [('2. only if it allowed, the W10 variable pass (_sg_vx_pass);', 1),
                                                    ('Length budget: an overrun inside _sg_vx_pass blocks there', 1)]),
]
SUITE_SITES = [
 ('9 test :2510-2518 W10 block head', '4a7c44caa0c7b992', [('beyond a limit the command is BLOCKED', 1), ('_SGV_SMAX 8192 = one substituted copy', 1)]),
 ('10 test :2544-2549 21aa/21ab', 'f3fa3abab18f053b', [('the WHOLE judged string, not its growth', 1)]),
 ('11 test :2556-2562 21ac/21ad', '3ecdb01f064087db', [('which is how a 4096-character list is refused', 1)]),
 ('12 test :2578-2585 21af/21ag', '1bd18760d748990e', [('Red when (21ag): the 36 KB dense copy passes', 1)]),
 ('13 test :2597-2599 21aj', 'dbca04b5e10c90bc', [('Red when (21aj): such a segment is skipped or counted instead of refused', 1)]),
 ('14 test :2628-2632 21al', '32ec743f4667c650', [('Red when (21al): the braced 8193-character whole copy passes', 1)]),
 ('15 test :2679-2681 21ao', '1c6bab0505df9784', [('Red when (21ao): the 8193-character whole copy passes', 1)]),
]
SUITE_TITLES = [  # the full baseline titles of the cases whose title becomes untrue (21ac keeps its title: its read is still blocked)
 ('16 test :2552 21ab title', 'W10 SC-21ab bf: copy limit exceeded is refused — 8193 characters: the copy is not judged, the command is blocked as too large (no padding passes)', 1),
 ('17 test :2586 21ag title', 'W10 SC-21ag bf: the dense shape of the review (15 assignments of 300 B, 8 references each: a 36 KB copy; 16 x 300 B x 8 took 5.4 s) is over the copy limit and refused as too large', 1),
 ('18 test :2605 21aj title', 'W10 SC-21aj bf: a segment over the copy limit ends the pass — with one, seven or eight of them in front of the reader the command is refused as too large and the reader is never judged', 1),
 ('19 test :2633 21al title', 'W10 SC-21al bf: the copy limit holds for the braced form too — a substituted whole command of exactly 8192 characters is judged and blocked, 8193 is refused as too large', 1),
 ('20 test :2682 21ao title', 'W10 SC-21ao bf: whole-command mode obeys the copy limit — a whole copy of exactly 8192 characters is judged and blocked, 8193 is refused as too large', 1),
]
ADD_HOOK = ['_SGV_GMAX', '_SGV_LMAX', '_SG_P0', 'hard deadline', 'nocredit', 'longline', '_sg_relax_run', 'status 4']
ADD_SUITE = ['_SGV_GMAX', 'longline']
bad = 0
def check(label, path, sites, titles, add):
    global bad
    R = runs(path); joined = '\n'.join(R); raw = open(path, encoding='utf-8').read(); hashes = {sha(r) for r in R}
    for site, h, anchors in sites:
        for ph, n0 in anchors:
            n = joined.count(ph); ok = (n == n0) if mode == 'baseline' else (n == 0); bad += not ok
            print(f"{'ok ' if ok else 'RED'} anchor  {site:40s} n={n}  {ph}")
        if mode == 'baseline':
            got = [sha(r) for r in R if anchors[0][0] in r]; ok = got == [h]; bad += not ok
            print(f"{'ok ' if ok else 'RED'} block   {site:40s} sha256 {got} (listed {h})")
        else:
            ok = h not in hashes; bad += not ok
            print(f"{'ok ' if ok else 'RED'} block   {site:40s} {'rewritten' if ok else 'the baseline block is still there'}")
    for site, ph, n0 in titles:
        n = raw.count(ph); ok = (n == n0) if mode == 'baseline' else (n == 0); bad += not ok
        print(f"{'ok ' if ok else 'RED'} title   {site:40s} n={n}  {ph}")
    for w in add:
        n = joined.count(w); ok = (n == 0) if mode == 'baseline' else (n >= 1); bad += not ok
        print(f"{'ok ' if ok else 'RED'} add     {label:4s} n={n}  {w}")
if hook: check('hook', hook, HOOK_SITES, [], ADD_HOOK)
if suite: check('test', suite, SUITE_SITES, SUITE_TITLES, ADD_SUITE)
print(f"{mode}{' ' + only if only else ''}: {'GREEN' if bad == 0 else 'RED (%d)' % bad}")
sys.exit(1 if bad else 0)
