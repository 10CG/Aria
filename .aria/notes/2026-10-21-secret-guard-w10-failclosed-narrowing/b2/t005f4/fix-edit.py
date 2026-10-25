p = 'edit5f4.py'; t = open(p, encoding='utf-8').read()
a = """hb = T['helper'].split('\\n'); sb = T['scdirect'].split('\\n')
print('B2 helper vs sc-direct after the edit: helper tail from line 11 == sc-direct tail from line 5:', hb[10:] == sb[4:])
"""
b = """def dd(x, y): return [l for l in difflib.unified_diff(x.split('\\n'), y.split('\\n'), lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('+++', '---')]
P0 = {k: open(O + '/pre/' + k + '-' + os.path.basename(F[k]), encoding='utf-8', newline='').read() for k in ('helper', 'scdirect')}
print('B2 helper vs sc-direct: the differing lines are the same before and after the edit (INV-2):', dd(P0['helper'], P0['scdirect']) == dd(T['helper'], T['scdirect']), '| differing lines', len(dd(T['helper'], T['scdirect'])))
"""
assert t.count(a) == 1; t = t.replace(a, b)
a2 = """T['suite'] = once(T['suite'], 'V15-W1l-unlistable-directory-with-wslinterop-late V15-W1m-mount-table-read-only-after-platform-and-time\\n',
                  'V15-W1l-unlistable-directory-with-wslinterop-late V15-W1m-mount-table-read-only-after-platform-and-time ' + W1O + '\\n', 'SGW_EXP_DIRECT')"""
b2 = """T['suite'] = once(T['suite'], 'V15-W1l-unlistable-directory-with-wslinterop-late V15-W1m-mount-table-read-only-after-platform-and-time',
                  'V15-W1l-unlistable-directory-with-wslinterop-late V15-W1m-mount-table-read-only-after-platform-and-time ' + W1O, 'SGW_EXP_DIRECT')"""
assert t.count(a2) == 1; t = t.replace(a2, b2); open(p, 'w', encoding='utf-8').write(t); print('patched')
