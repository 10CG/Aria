#!/usr/bin/env python3
"""derive.py BASE PROTO TARGET : per What 7 hook site, the comment run in each file (consecutive '#' lines joined, as commentsync.py reads them), split into
sentence units; prints the units of the baseline / prototype runs that the target's comment text no longer holds (untrue candidates) and the units of the
target run that the baseline run does not hold (the new sentences), with where each occurs. TARGET is the spec target: prototype + What 7 supplement."""
import re, sys, json
def runs_with_next(path):
    out, cur, start = [], [], None
    lines = open(path, encoding='utf-8').read().split('\n')
    for n, ln in enumerate(lines, 1):
        m = re.match(r'\s*#(.*)$', ln)
        if m and not ln.lstrip().startswith('#!'):
            if not cur: start = n
            cur.append(m.group(1))
        else:
            if cur: out.append((start, n - 1, re.sub(r'\s+', ' ', ' '.join(cur)).strip(), ln)); cur = []
    if cur: out.append((start, len(lines), re.sub(r'\s+', ' ', ' '.join(cur)).strip(), ''))
    return out
def units(s):
    return [u for u in re.split(r'(?<=[.;])\s+', s) if len(u) >= 12]
SITES = [  # name, locator: ('next', code-line prefix) = the run right before that code line; ('has', phrase) = the run holding the phrase
 ('1 header: shell variable indirection', ('has', 'Shell variable indirection')),
 ('2 W10 head + LENGTH BUDGET', ('next', '_SGV_N=(); _SGV_V=()')),
 ('3 time budget', ('next', '_SG_T0=$SECONDS')),
 ('4 _sg_vx_apply', ('next', '_sg_vx_apply() {')),
 ('5 _sg_vx_pass', ('next', '_sg_vx_pass() {')),
 ('6 _sg_emit_blocked', ('next', '_sg_emit_blocked() {')),
 ('7 _sg_judge_one', ('next', '_sg_judge_one() {')),
 ('8 _sg_per_segment_eval', ('next', '_sg_per_segment_eval() {')),
 ('9 _sg_vx_replace (supplement 2)', ('next', '_sg_vx_replace() {')),
 ('10 relaxed rerun block (supplement 4)', ('next', '_sg_vx_big_judge() {')),
]
def find(R, loc):
    kind, key = loc
    for s, e, txt, nxt in R:
        if kind == 'next' and nxt.startswith(key): return (s, e, txt)
        if kind == 'has' and key in txt: return (s, e, txt)
    return None
B, P, T = (runs_with_next(p) for p in sys.argv[1:4])
alltxt = {k: '\n'.join(t for _, _, t, _ in R) for k, R in (('b', B), ('p', P), ('t', T))}
res = []
for name, loc in SITES:
    b, p, t = find(B, loc), find(P, loc), find(T, loc)
    ub = units(b[2]) if b else []; up = units(p[2]) if p else []; ut = units(t[2]) if t else []
    untrue = []
    for u in dict.fromkeys(ub + up):
        if alltxt['t'].count(u) == 0: untrue.append((u, u in ub, u in up))
    new = [(u, p is not None and u in p[2]) for u in dict.fromkeys(ut) if not (b and u in b[2])]
    res.append({'site': name, 'loc': loc, 'base': b[:2] if b else None, 'proto': p[:2] if p else None, 'target': t[:2] if t else None,
                'untrue': untrue, 'new': new})
    print(f"== {name}  base {b[:2] if b else None} proto {p[:2] if p else None} target {t[:2] if t else None}: untrue {len(untrue)}, new {len(new)}")
    for u, ib, ip in untrue: print(f"   - [{'b' if ib else ' '}{'p' if ip else ' '}] {u}")
    for u, ip in new: print(f"   + [{'p' if ip else 's'}] {u}")
json.dump(res, open('derived.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
