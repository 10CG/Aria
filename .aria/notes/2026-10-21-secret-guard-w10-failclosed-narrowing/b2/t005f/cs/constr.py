import sys, re
cs, d = sys.argv[1], sys.argv[2]
src = open(cs, encoding='utf-8').read(); sys.argv = ['x', 'h', 's', 'target']; g = {}
exec(src[:src.index('\ndef say(')], g)
for kind, base, SITES, ADD in (('hook', f'{d}/hook-59e333c.sh', g['HOOK_SITES'], g['ADD_HOOK']), ('suite', f'{d}/suite-59e333c.sh', g['SUITE_SITES'], g['ADD_SUITE'])):
    t = open(base, encoding='utf-8').read(); anchors = [a for _, _, al in SITES for a, _ in al]
    ins = t
    for a in anchors: ins = ins.replace(a, a[0] + 'x' + a[1:])
    addl = '\n# ' + ' '.join(ADD) + '\n'
    open(f'{d}/{kind}-c1-insert.sh', 'w', encoding='utf-8').write(ins + addl)
    L = t.split('\n'); kill = set(); i = 0
    while i < len(L):   # whole comment runs that hold an anchor
        if re.match(r'\s*#', L[i]) and not L[i].lstrip().startswith('#!'):
            j = i
            while j < len(L) and re.match(r'\s*#', L[j]): j += 1
            if any(a in ' '.join(L[i:j]) or a in re.sub(r'\s+', ' ', ' '.join(re.sub(r'^\s*#', '', x) for x in L[i:j])) for a in anchors): kill.update(range(i, j))
            i = j
        else: i += 1
    open(f'{d}/{kind}-c2-delete.sh', 'w', encoding='utf-8').write('\n'.join(x for k, x in enumerate(L) if k not in kill) + addl)
    print(kind, 'anchors', len(anchors), 'insert: anchors left', sum(ins.count(a) for a in anchors), '| delete: lines removed', len(kill))
