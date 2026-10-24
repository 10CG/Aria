# compare the six groups' FAIL details (check lists) of the old suite across runs; prints counts and differing check names only (no fixture text beyond 60 chars)
import re, sys
def groups(p):
    d = {}
    for ln in open(p, encoding='utf-8', errors='replace'):
        m = re.match(r'^  FAIL \[W10 (SC-21a[bcgjlo]) [^\]]*\]: (\d+) check\(s\) off: (.*)$', ln.rstrip('\n'))
        if m: d[m.group(1)] = (int(m.group(2)), re.findall(r'\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', m.group(3)))
    return d
names = sys.argv[1::2]; files = sys.argv[2::2]
runs = [groups(f) for f in files]
for g in sorted(set().union(*[r.keys() for r in runs])):
    print(g, ' '.join(f'{n}={r.get(g, (0, []))[0]}' for n, r in zip(names, runs)))
a, b = runs[0], runs[1]
for g in sorted(set(a) | set(b)):
    ca, cb = a.get(g, (0, []))[1], b.get(g, (0, []))[1]
    print(f'  {g}: {names[0]} vs {names[1]} identical check lists: {ca == cb}')
