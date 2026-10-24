import re, sys
exec(open(sys.argv[1]).read().split('sha = lambda')[0].split('def runs')[1].join(['def runs', '']) if False else '')
def runs(path):
    out, cur = [], []
    for ln in open(path, encoding='utf-8').read().split('\n'):
        m = re.match(r'\s*#(.*)$', ln)
        if m and not ln.lstrip().startswith('#!'):
            cur.append(m.group(1))
        else:
            if cur: out.append((re.sub(r'\s+', ' ', ' '.join(cur)).strip(), ln)); cur = []
    if cur: out.append((re.sub(r'\s+', ' ', ' '.join(cur)).strip(), ''))
    return out
keys = [('9', 'beyond a limit the command is BLOCKED'), ('10', 'the WHOLE judged string, not its growth'), ('11', 'which is how a 4096-character list is refused'),
        ('12', 'Red when (21ag): the 36 KB dense copy passes'), ('13', 'Red when (21aj): such a segment is skipped'), ('14', 'Red when (21al): the braced 8193'),
        ('15', 'Red when (21ao): the 8193-character whole copy passes'), ('21', 'the copy limit holds for the braced form ${NAME} too'), ('22', 'whole-command mode (the command degrades because of a `(`)')]
B = runs(sys.argv[2]); W = runs(sys.argv[3])
for site, k in keys:
    b = [(t, n) for t, n in B if k in t]; w = [(t, n) for t, n in W if k in t]
    print(f'== site {site}: base runs {len(b)}, worktree runs {len(w)}, same text {b[0][0] == w[0][0] if b and w else None}; next line: {b[0][1][:60]!r}')
    for i, s in enumerate(re.split(r'(?<=[.;])\s+', b[0][0])): print(f'  {site}.{i+1} {s}')
