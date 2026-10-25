import sys, re, subprocess, difflib, os, statistics
OUT = '/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/impl/'
REL = '.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/'
T = sys.argv[1]
def gs(rev, p):
    r = subprocess.run(['git', '-C', '/home/dev/Aria', 'show', rev + ':' + REL + p], capture_output=True, text=True)
    return r.stdout.split('\n') if r.returncode == 0 else None
def cur(p):
    try: return open(OUT + p, encoding='utf-8', errors='replace').read().split('\n')
    except OSError: return None
HDR = re.compile(r'^# (20\d\d-|run-mutants\.sh \||sc-cases\.sh \||run-suite\.sh|W14 |end \||W14 timing)')
def norm(lines):
    o = []
    for l in lines:
        if HDR.match(l): continue
        l = re.sub(r'20\d\d-\d\d-\d\d[T ][\d:]+(Z| \+0000)?', 'TS', l)
        l = re.sub(r'load( at the end| start| before| after)?:? [\d. /|a-z:]*?(?=\||$)', 'load #', l)
        l = re.sub(r'\d+\.\d+', '#', l)
        o.append(l.rstrip())
    return o
def ndiff(name, a, b, f):
    d = [x for x in difflib.unified_diff(norm(a), norm(b), 'old', 'new', n=0, lineterm='') if not x.startswith(('---', '+++', '@@'))]
    f.write('### %s: %d differing normalized lines (old impl run vs this run; header lines dropped; dates, loads and decimals masked)\n' % (name, len(d)))
    for x in d[:200]: f.write('  ' + x[:300] + '\n')
    return len(d)
def states(lines, rx):
    m = {}
    for l in lines or []:
        g = re.match(rx, l)
        if g: m[g.group(2)] = g.group(1)
    return m
def setdiff(name, a, b, f):
    ka, kb = set(a), set(b)
    ch = sorted(k for k in ka & kb if a[k] != b[k])
    f.write('### %s: only old %d %s | only new %d %s | changed %d %s\n' % (name, len(ka - kb), ' '.join(sorted(ka - kb))[:600], len(kb - ka), ' '.join(sorted(kb - ka))[:600], len(ch), ' '.join('%s:%s->%s' % (k, a[k], b[k]) for k in ch)[:600]))
    return len(ch)
def tsvcmp(name, a, b, f):
    def rows(L): return {r[0]: r for r in (x.split('\t') for x in L if x and not x.startswith('#')) if len(r) >= 6}
    ra, rb = rows(a), rows(b)
    mis = [n for n in sorted(set(ra) | set(rb), key=lambda s: int(s) if s.isdigit() else 0) if n not in ra or n not in rb or ra[n][1:3] != rb[n][1:3] or (ra[n][5] == '-') != (rb[n][5] == '-')]
    f.write('### %s: rows old %d new %d | rows whose rc, kind or rerun-entered differ: %d %s\n' % (name, len(ra), len(rb), len(mis), ' '.join(mis)[:400]))
    return len(mis)
def matrix(lines):
    g, case = {}, None
    for l in lines or []:
        m = re.match(r'^## (\S+)\s+\[(\S+)\]\s+bash (\S+)', l)
        if m: case = (m.group(1), m.group(3)); g[case] = []; continue
        if l.startswith('load before') and case: g[case] = []; continue
        m = re.match(r'^\s+run \d+\s+rc=(\d+)\s+(\S+)\s+W=\s*([\d.]+) s', l)
        if m and case: g[case].append((m.group(1) + ' ' + m.group(2), float(m.group(3)))); continue
        m = re.match(r'^\s+bash (\S+)\s+(\S+)\s+run \d+\s+rc=(\d+) (\S+)\s+W=([\d.]+) s', l)
        if m: g.setdefault(('confirm:' + m.group(2), m.group(1)), []).append((m.group(3) + ' ' + m.group(4), float(m.group(5))))
    return g
f = open(T + '/compare.txt', 'a'); s = []
for st in sys.argv[2:]:
    f.write('\n######## %s\n' % st)
    if st == 'W8':
        a, b = gs('HEAD', 'impl/W8-v31.diff'), cur('W8-v31.diff')
        cnt = lambda L: (sum(1 for x in L if re.match(r'^\+[^+]', x)), sum(1 for x in L if x == '+'), sum(1 for x in L if re.match(r'^-[^-]', x)), sum(1 for x in L if x.startswith('@@')))
        s.append('W8 old (added, blank, removed, hunks) %s new %s | new header: %s' % (cnt(a), cnt(b), b[0][:150]))
    if st == 'W11':
        a, b, p = gs('HEAD', 'impl/W11-adversarial.txt'), cur('W11-adversarial.txt'), gs('95cf1de7', 'W11-adversarial.txt')
        s.append('W11 vs old impl: %d | vs proto 95cf1de7: %d (normalized differing lines)' % (ndiff('W11 old impl', a, b, f), ndiff('W11 proto 95cf1de7 (old side = proto)', p, b, f)))
    if st == 'W9':
        a, b, p = gs('HEAD', 'impl/W9-suite.txt'), cur('W9-suite.txt'), gs('95cf1de7', 'W9-suite.txt')
        s.append('W9 vs old impl: %d | vs proto 95cf1de7: %d' % (ndiff('W9 old impl', a, b, f), ndiff('W9 proto 95cf1de7 (old side = proto)', p, b, f)))
    if st == 'W13':
        a, b, p = gs('HEAD', 'impl/W13-sc-cases.txt'), cur('W13-sc-cases.txt'), gs('95cf1de7', 'W13-sc-cases.txt')
        n1 = ndiff('W13 old impl', a, b, f)
        def rg(L):
            m = {}
            for l in L or []:
                g = re.match(r'^  (red|green):\s*(.*)$', l)
                if g:
                    for k in g.group(2).split(): m[k] = g.group(1)
            return m
        c1 = setdiff('W13 sec2 baseline red/green: old impl vs new', rg(a), rg(b), f); c2 = setdiff('W13 sec2 baseline red/green: proto 95cf1de7 vs new', rg(p), rg(b), f)
        rx = r'^(PASS|FAIL|MISSING|SKIP|SETUP)\s+(\S+)'
        c3 = setdiff('W13-sc-base raw states: old vs new', states(gs('HEAD', 'impl/W13-sc-base.txt'), rx), states(cur('W13-sc-base.txt'), rx), f)
        vr = r'^(?:\S+)\s+(CAUGHT|MISSED|WRONG-REASON|NOT-JUDGED|SETUP|GREEN|RED)\b'
        def mv(L): return {l.split()[0]: l.split()[1] for l in L or [] if re.match(vr, l)}
        c4 = setdiff('W13 sec3 verdicts: old impl vs new', mv(a), mv(b), f)
        fails = sum(1 for l in b or [] if l.startswith('FAIL'))
        s.append('W13 normalized diff vs old %d | sec2 changed vs old %d, vs proto %d | sc-base states changed %d | sec3 verdicts changed %d | FAIL lines in sec1 %d | verdict counts new %s' % (n1, c1, c2, c3, c4, fails, {v: list(mv(b).values()).count(v) for v in set(mv(b).values())}))
        for x in ['W13-P0-v31.txt', 'W13-P0-suite.txt', 'W13-suite-mutants.txt']:
            a2, b2 = gs('HEAD', 'impl/' + x), cur(x)
            c5 = setdiff(x + ' verdicts: old vs new', mv(a2), mv(b2), f); n5 = ndiff(x, a2, b2, f)
            s.append('%s: verdicts changed %d, normalized diff %d | new counts %s | %s' % (x, c5, n5, {v: list(mv(b2).values()).count(v) for v in set(mv(b2).values())}, ' / '.join(l[:90] for l in (b2 or []) if l.startswith('# ') and not HDR.match(l))))
    if st == 'W12':
        for x in ['W12-replay-138.tsv', 'W12-replay-138-base.tsv']:
            s.append('%s: rows differing in rc/kind/rerun-entered vs old impl: %d' % (x, tsvcmp(x, gs('HEAD', 'impl/' + x), cur(x), f)))
        s.append('W12-ident-138 normalized diff vs old: %d | W12-real-traffic normalized diff vs old: %d' % (ndiff('W12-ident-138', gs('HEAD', 'impl/W12-ident-138.txt'), cur('W12-ident-138.txt'), f), ndiff('W12-real-traffic', gs('HEAD', 'impl/W12-real-traffic.txt'), cur('W12-real-traffic.txt'), f)))
    if st == 'W14':
        a, b = gs('HEAD', 'impl/W14-independent-mutants.txt'), cur('W14-independent-mutants.txt')
        s.append('W14 independent: normalized diff vs old %d | new end: %s' % (ndiff('W14-independent', a, b, f), (b or [''])[-2][:200] if b and b[-1] == '' else (b or [''])[-1][:200]))
        ma, mb = matrix(gs('HEAD', 'impl/W14-timing-matrix.txt')), matrix(cur('W14-timing-matrix.txt'))
        bad, rat = [], []
        f.write('### matrix per case/bash: outcomes old -> new | median W old -> new (ratio)\n')
        for k in sorted(set(ma) | set(mb)):
            oa, ob = sorted(x[0] for x in ma.get(k, [])), sorted(x[0] for x in mb.get(k, []))
            wa = statistics.median([x[1] for x in ma[k]]) if ma.get(k) else float('nan'); wb = statistics.median([x[1] for x in mb[k]]) if mb.get(k) else float('nan')
            r = wb / wa if wa == wa and wb == wb and wa > 0 else float('nan'); rat.append(r)
            if sorted(set(oa)) != sorted(set(ob)): bad.append('%s/%s' % k)
            f.write('  %-34s %-7s %s -> %s | %.3f -> %.3f (%.2f)\n' % (k[0], k[1], ','.join(sorted(set(oa))), ','.join(sorted(set(ob))), wa, wb, r))
        rr = [x for x in rat if x == x]
        tl = [l for l in (cur('W14-timing-matrix.txt') or []) if l.startswith(('every outcome', '## runs that left'))]
        s.append('W14 matrix: groups old %d new %d | outcome sets differ %d %s | median-W ratio new/old min %.2f median %.2f max %.2f | %s' % (len(ma), len(mb), len(bad), ' '.join(bad)[:300], min(rr) if rr else 0, statistics.median(rr) if rr else 0, max(rr) if rr else 0, ' || '.join(x[:160] for x in tl)))
for x in s: print(x[:900])
f.close()
