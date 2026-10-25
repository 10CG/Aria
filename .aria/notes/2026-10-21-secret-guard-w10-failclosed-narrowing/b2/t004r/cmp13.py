# cmp13.py MODE OLD NEW : compares outcomes by id (W13 main file / sc-base raw output / run-mutants summary); prints only ids, verdicts and counts
import re, sys
mode, old, new = sys.argv[1:4]
NEWID = re.compile(r'^V15-W1[f-o]\b')
def mutline(ln):
    m = re.match(r'^((?:BI|P)-\S+)\s+(\S+)\s+(.*)$', ln)
    if not m: return None
    parts = [p.strip() for p in m.group(3).split(' | ')]
    des = next((p for p in parts if not p.startswith('load') and p.split() and all(re.match(r'^[A-Za-z0-9_.:\[\]-]+=\S+$', t) for t in p.split())), '')
    tot = next((re.sub(r'\(load.*', '', p) for p in parts if p.startswith('# totals')), '')
    oth = next((p[len('other red: '):].split() for p in parts if p.startswith('other red:')), [])
    tb = next((p for p in parts if p.startswith('timing batch')), '')
    return m.group(1), (m.group(2), des, tot, frozenset(oth), tb)
def parse(path):
    d = {'s1': {}, 's1fail': [], 'red': set(), 'green': set(), 'mut': {}, 'misc': [], 'st': {}}
    sec = 0
    for ln in open(path, encoding='utf-8', errors='replace'):
        ln = ln.rstrip('\n')
        m = re.match(r'^## (\d)\.', ln)
        if m: sec = int(m.group(1)); continue
        if mode == 'base':
            m = re.match(r'^(PASS|FAIL|MISSING|SETUP|SKIP)\s+(\S+)', ln)
            if m: d['st'][m.group(2)] = m.group(1)
            elif ln.startswith('# totals'): d['misc'].append(ln)
            continue
        if sec == 1:
            m = re.match(r'^bash (\S+)\s+# totals: (.*?) \| relaxation expected: (\w+)', ln)
            if m: d['s1'][m.group(1)] = (m.group(2), m.group(3))
            elif ln.startswith('FAIL'): d['s1fail'].append(ln.split()[1])
            continue
        if sec == 2:
            if ln.startswith('  red:'): d['red'] = set(ln.split()[1:])
            elif ln.startswith('  green:'): d['green'] = set(ln.split()[1:])
            elif '# totals' in ln: d['misc'].append('s2 ' + ln)
            continue
        r = mutline(ln)
        if r: d['mut'][r[0]] = r[1]
        elif re.match(r'^# \d+ caught', ln) or ln.startswith('# perturbation'): d['misc'].append(re.sub(r'\| load at the end.*', '', ln))
    return d
o, n = parse(old), parse(new)
out = []
if mode == 'base':
    ids = sorted(set(o['st']) | set(n['st']))
    ch = [i for i in ids if i in o['st'] and i in n['st'] and o['st'][i] != n['st'][i]]
    add = [i for i in ids if i not in o['st']]; gone = [i for i in ids if i not in n['st']]
    out.append('ids old %d new %d | changed %d: %s' % (len(o['st']), len(n['st']), len(ch), ' '.join('%s %s->%s' % (i, o['st'][i], n['st'][i]) for i in ch)))
    out.append('new ids %d: %s' % (len(add), ' '.join('%s=%s' % (i, n['st'][i]) for i in add)))
    out.append('gone ids %d: %s' % (len(gone), ' '.join(gone)))
    out.append('totals old: %s' % ' '.join(o['misc'])); out.append('totals new: %s' % ' '.join(n['misc']))
else:
    for b in sorted(set(o['s1']) | set(n['s1'])):
        out.append('s1 bash %s old [%s] new [%s]' % (b, o['s1'].get(b, ('-',))[0], n['s1'].get(b, ('-',))[0]))
    if o['s1'] or n['s1']: out.append('s1 FAIL lines old %d new %d %s' % (len(o['s1fail']), len(n['s1fail']), ' '.join(n['s1fail'])))
    if o['red'] or n['red']:
        out.append('s2 red: old %d new %d | new-only %s | old-only %s' % (len(o['red']), len(n['red']), ' '.join(sorted(n['red'] - o['red'])), ' '.join(sorted(o['red'] - n['red']))))
        out.append('s2 green: old %d new %d | new-only %s | old-only %s' % (len(o['green']), len(n['green']), ' '.join(sorted(n['green'] - o['green'])), ' '.join(sorted(o['green'] - n['green']))))
    ids = sorted(set(o['mut']) | set(n['mut']), key=lambda s: (s.split('-')[0], int(re.sub(r'\D', '', s.split('-')[1]) or 0) if s.startswith('BI') else 0, s))
    vd = [i for i in ids if (o['mut'].get(i) or ('-',))[0] != (n['mut'].get(i) or ('-',))[0]]
    dd = [i for i in ids if i in o['mut'] and i in n['mut'] and o['mut'][i][1] != n['mut'][i][1]]
    td = [i for i in ids if i in o['mut'] and i in n['mut'] and o['mut'][i][2] != n['mut'][i][2]]
    out.append('mut ids old %d new %d | verdicts new: %s' % (len(o['mut']), len(n['mut']), ' '.join('%s=%d' % (v, sum(1 for x in n['mut'].values() if x[0] == v)) for v in sorted({x[0] for x in n['mut'].values()}))))
    out.append('verdict differs: %s' % (' '.join('%s %s->%s' % (i, (o['mut'].get(i) or ('-',))[0], (n['mut'].get(i) or ('-',))[0]) for i in vd) or 'none'))
    out.append('designated-state field differs: %s' % (' '.join(dd) or 'none'))
    out.append('P totals differ: %s' % (' '.join('%s [%s]->[%s]' % (i, o['mut'][i][2], n['mut'][i][2]) for i in td) or 'none'))
    on, oo = [], []
    for i in ids:
        if i in o['mut'] and i in n['mut']:
            a, b = o['mut'][i][3], n['mut'][i][3]
            x = sorted(b - a); y = sorted(a - b)
            if [k for k in x if not NEWID.match(k)] or y: oo.append('%s +[%s] -[%s]' % (i, ' '.join(x), ' '.join(y)))
            elif x: on.append('%s +[%s]' % (i, ' '.join(x)))
    out.append('other-red changes on old ids: %s' % (' ; '.join(oo) or 'none'))
    out.append('other-red additions that are only new V15-W1f..o ids: %s' % (' ; '.join(on) or 'none'))
    out.append('timing batch not judged (new): %s' % (' '.join(i for i in ids if i in n['mut'] and n['mut'][i][4] and 'judged' != n['mut'][i][4].split(': ')[-1]) or 'none'))
    out.append('summary old: %s' % ' || '.join(o['misc'])); out.append('summary new: %s' % ' || '.join(n['misc']))
print('\n'.join(out))
