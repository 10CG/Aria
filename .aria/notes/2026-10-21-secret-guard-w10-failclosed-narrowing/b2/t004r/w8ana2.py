# w8ana2.py PROTO PREV IMPL PROPOSAL : sections of every + line of the proto->impl hunks (per line); fenced code lines of the What 1 / 7 supplements vs impl, prev, proto
import sys, re, subprocess, collections
proto, prev, impl, prop = sys.argv[1:5]
P = open(prop, encoding='utf-8').read().split('\n')
lab, cur = [], 'top'
for ln in P:
    m = re.match(r'^#{2,4} +(.*)', ln)
    if m: cur = m.group(1).strip()[:12]
    m2 = re.match(r'^\*\*(What \d+ 补充(?: \d+)?)', ln)
    if m2: cur = m2.group(1)
    lab.append(cur)
Pr = [x.rstrip() for x in P]
rd = lambda f: set(x.rstrip() for x in open(f, encoding='utf-8').read().split('\n'))
I, V, O = rd(impl), rd(prev), rd(proto)
t = subprocess.run(['diff', '-u', proto, impl], capture_output=True, text=True).stdout
hs = []
for ln in t.split('\n'):
    if ln.startswith('@@'): hs.append([])
    elif hs and ln != '' and ln[0] in '+- ': hs[-1].append(ln)
for k, h in enumerate(hs, 1):
    c = collections.Counter(); only = 0; nb = 0
    for ln in h:
        if ln[0] != '+' or not ln[1:].strip(): continue
        s = ln[1:].rstrip(); nb += 1
        secs = {lab[i] for i, x in enumerate(Pr) if x == s} or {lab[i] for i, x in enumerate(Pr) if s.strip() in x}
        for z in secs: c[z] += 1
        if secs == {'What 7 补充 2'}: only += 1
        if not secs: c['NONE'] += 1
    print('H%d +%d nonblank: %s | only in What 7 补充 2: %d' % (k, nb, ', '.join('%s %d' % kv for kv in sorted(c.items())), only))
inb = False; blocks = collections.defaultdict(list)
for i, x in enumerate(P):
    if x.strip().startswith('```'): inb = not inb; continue
    if inb and x.strip(): blocks[lab[i]].append(Pr[i])
for sn in ('What 1 补充', 'What 1 补充 2', 'What 7 补充', 'What 7 补充 2'):
    ls = blocks.get(sn, [])
    print('%s fenced lines %d: in impl %d, not impl but prev %d, only proto %d, none %d' % (sn, len(ls), sum(x in I for x in ls), sum(x not in I and x in V for x in ls), sum(x not in I and x not in V and x in O for x in ls), sum(x not in I and x not in V and x not in O for x in ls)))
