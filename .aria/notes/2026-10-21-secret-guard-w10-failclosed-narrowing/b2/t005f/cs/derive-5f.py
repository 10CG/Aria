import sys, re
cs, d, newhook, newsuite = sys.argv[1:5]
src = open(cs, encoding='utf-8').read()
sys.argv = ['x', 'h', 's', 'target']; g = {}
exec(src[:src.index('\ndef say(')], g)
runs, site_run, HOOK_TEXT, SUITE_TEXT = g['runs'], g['site_run'], g['HOOK_TEXT'], g['SUITE_TEXT']
split = lambda r: [u for u in re.split(r'(?<=[.;])\s+', r or '') if u]
J = lambda R: '\n'.join(t for t, _ in R)
H = {k: runs(p) for k, p in (('b', f'{d}/hook-59e333c.sh'), ('p', f'{d}/hook-proto.sh'), ('o', f'{d}/hook-2893bcc.sh'), ('n', newhook))}
S = {k: runs(p) for k, p in (('b', f'{d}/suite-59e333c.sh'), ('o', f'{d}/suite-2893bcc.sh'), ('n', newsuite))}
log, FH, FS = [], [], []
def diff(R, site, loc):
    o, n = site_run(R['o'], loc), site_run(R['n'], loc)
    if o == n: return None
    ou, nu = split(o), split(n)
    return [u for u in ou if u not in nu], [u for u in nu if u not in ou]
for site, loc, untrue, new in HOOK_TEXT:
    r = diff(H, site, loc)
    if not r: continue
    rem, add = r; old5, new5 = [], []
    for u in rem:
        if J(H['n']).count(u): log.append(f'hook {site}: retracted unit still in the target comments, left out: {u!r}'); continue
        f = ('b' if u in (site_run(H['b'], loc) or '') else '') + ('p' if u in (site_run(H['p'], loc) or '') else '')
        if not f and (J(H['b']).count(u) or J(H['p']).count(u)): log.append(f'hook {site}: retracted unit elsewhere in baseline/prototype, left out: {u!r}'); continue
        old5.append((f or 'i', u))
    for u in add:
        if u in (site_run(H['b'], loc) or '') or u in (site_run(H['p'], loc) or ''): log.append(f'hook {site}: new unit already in the baseline/prototype run, left out: {u!r}'); continue
        new5.append(u)
    FH.append((site, old5, new5))
for site, loc, untrue, new in SUITE_TEXT:
    r = diff(S, site, loc)
    if not r: continue
    rem, add = r
    old5 = [u for u in rem if not J(S['n']).count(u) and not J(S['b']).count(u)]
    new5 = [u for u in add if not J(S['b']).count(u)]
    log += [f'suite {site}: unit left out: {u!r}' for u in rem + add if u not in old5 + new5]
    FS.append((site, old5, new5))
covered = {site_run(H['n'], loc) for _, loc, _, _ in HOOK_TEXT} | {site_run(S['n'], loc) for _, loc, _, _ in SUITE_TEXT}
for k, R in (('hook', H), ('suite', S)):
    on = {t for t, _ in R['o']}
    for t, _ in R['n']:
        if t not in on and t not in covered: log.append(f'{k}: a changed comment run outside every site: {t[:90]!r}')
out = ['# TASK-005 fix round (What 7 supplement 2, 2026-10-25): sentence units derived mechanically by derive-5f.py (split after \'.\' and \';\'; old run = aria 2893bcc,',
       '# new run = the fix round; flags against 59e333c and the mkv31.py prototype), not typed. Per site: the retracted units leave the site\'s new list and must occur 0 times',
       '# in the target (hook: flag b / p as above, i = written only by this change before the fix round; suite: 0 times in every mode); the new units must be in the site\'s run.',
       'FIX5_HOOK = ' + repr(FH), 'FIX5_SUITE = ' + repr(FS),
       'for _s, _old, _new in FIX5_HOOK:',
       '    _e = next(e for e in HOOK_TEXT if e[0] == _s); _gone = {u for _, u in _old}',
       '    _e[3][:] = [x for x in _e[3] if x[1] not in _gone]; _e[2].extend(_old); _e[3].extend(("s", u) for u in _new)',
       'SUITE_RETRACT = {}',
       'for _s, _old, _new in FIX5_SUITE:',
       '    _e = next(e for e in SUITE_TEXT if e[0] == _s)',
       '    _e[3][:] = [x for x in _e[3] if x not in set(_old)]; _e[3].extend(_new); SUITE_RETRACT[_s] = list(_old)']
assert 'FIX5_HOOK' not in src
src = src.replace('\ndef say(', '\n' + '\n'.join(out) + '\ndef say(', 1)
a = "        for u in new:\n            n = joined.count(u) if mode == 'baseline' else (run or '').count(u)\n            say((n == 0) if mode == 'baseline' else (n >= 1), 'new', site, n, u)\n"
assert src.count(a) == 1
src = src.replace(a, a + "        for u in SUITE_RETRACT.get(site, []):   # TASK-005 fix round: retracted sentences of the implementation, 0 times in every mode\n            n = joined.count(u); say(n == 0, 'old', site, n, u)\n")
open(cs, 'w', encoding='utf-8').write(src)
print('hook sites', [(s, len(o), len(n)) for s, o, n in FH], 'suite sites', [(s, len(o), len(n)) for s, o, n in FS])
print('\n'.join(log) or 'no unit left out, no uncovered run')
