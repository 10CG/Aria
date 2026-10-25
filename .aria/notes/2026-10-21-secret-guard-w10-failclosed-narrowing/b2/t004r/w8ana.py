# w8ana.py BASE PROTO PREV IMPL PROPOSAL P95_W8 OUTDIR : (a) base->proto body vs the W8 of 95cf1de7; (b) hunks of proto->prev, prev->impl, proto->impl,
# every changed line looked up verbatim in the proposal (whole consecutive block first, else line by line). Prints no hook text: ranges, counts, sections.
import sys, re, subprocess, collections, os
base, proto, prev, impl, prop, p95, outd = sys.argv[1:8]
P = open(prop, encoding='utf-8').read().split('\n')
lab, cur = [], 'top'
for ln in P:
    m = re.match(r'^#{2,4} +(.*)', ln)
    if m: cur = m.group(1).strip()[:24]
    m2 = re.match(r'^\*\*(What \d+ 补充(?: \d+)?)', ln)
    if m2: cur = m2.group(1)
    lab.append(cur)
Pr = [x.rstrip() for x in P]
idx = collections.defaultdict(list)
for i, x in enumerate(Pr): idx[x].append(i)
def udiff(a, b): return subprocess.run(['diff', '-u', a, b], capture_output=True, text=True).stdout
def body(t):
    ls = t.split('\n')
    for i, l in enumerate(ls):
        if l.startswith('@@'): return '\n'.join(ls[i:]).rstrip('\n')
    return ''
def hunks(t):
    hs = []
    for ln in t.split('\n'):
        if ln.startswith('@@'): hs.append({'hdr': ln.split('@@')[1].strip(), 'lines': []})
        elif hs and ln != '' and ln[0] in '+- ': hs[-1]['lines'].append(ln)
    return hs
def runs(lines, sign):
    rs, cur = [], []
    for ln in lines:
        if ln[0] == sign: cur.append(ln[1:].rstrip())
        elif cur: rs.append(cur); cur = []
    if cur: rs.append(cur)
    return rs
def block_hits(b): return [i for i in idx.get(b[0], []) if Pr[i:i + len(b)] == b]
def where(s):
    if s.strip() == '': return 'blank', []
    if s in idx: return 'exact', idx[s]
    st = s.strip(); sub = [i for i, x in enumerate(Pr) if st in x]
    return ('substr', sub) if sub else ('none', [])
def classify(name, a, b, f):
    hs = hunks(udiff(a, b)); tot = collections.Counter(); rows = []
    for k, h in enumerate(hs, 1):
        parts = []
        for sign in '-+':
            for blk in runs(h['lines'], sign):
                bh = block_hits(blk) if any(x.strip() for x in blk) else []
                if bh:
                    tot['whole-block'] += len(blk); parts.append('%s%d whole@%s' % (sign, len(blk), '/'.join(sorted({lab[i] for i in bh})))); continue
                c, secs = collections.Counter(), collections.Counter()
                for s in blk:
                    kind, w = where(s); c[kind] += 1; tot[kind] += 1
                    for sn in {lab[j] for j in w}: secs[sn] += 1
                parts.append('%s%d lines[%s]@%s' % (sign, len(blk), ','.join('%s %d' % kv for kv in sorted(c.items())), '/'.join('%s:%d' % kv for kv in secs.most_common())))
        rows.append('%s H%d @@ %s @@ %s' % (name, k, h['hdr'], ' ; '.join(parts)))
    f.write('\n'.join(rows) + '\n')
    ad = sum(1 for h in hs for l in h['lines'] if l[0] == '+'); rm = sum(1 for h in hs for l in h['lines'] if l[0] == '-')
    return len(hs), ad, rm, tot
os.makedirs(outd, exist_ok=True)
with open(os.path.join(outd, 'W8-hunks.txt'), 'w', encoding='utf-8') as f:
    bp = body(udiff(base, proto)); b95 = body(open(p95, encoding='utf-8').read())
    print('base->proto body vs 95cf1de7 W8 body: %s' % ('IDENTICAL' if bp == b95 else 'DIFFERENT (%d vs %d chars)' % (len(bp), len(b95))))
    for name, a, b in (('proto->prev', proto, prev), ('prev->impl', prev, impl), ('proto->impl', proto, impl)):
        n, ad, rm, tot = classify(name, a, b, f)
        print('%s: %d hunks, +%d -%d; changed lines found: %s' % (name, n, ad, rm, ', '.join('%s %d' % kv for kv in sorted(tot.items()))))
