# recompute.py <aria notes dir> <sc-base.txt of the run> <W13 of 95cf1de7>: the main loop's recomputation of the TASK-004 second segment from the raw outputs
import math, re, subprocess, sys
N, scbase, w13old = sys.argv[1:4]
I = N + '/v31/impl/'
def load(p):
    d = {}
    for ln in open(p, encoding='utf-8'):
        if ln.startswith('#') or not ln.strip(): continue
        f = ln.rstrip('\n').split('\t'); d[f[0]] = f
    return d
im, ba = load(I + 'W12-replay-138.tsv'), load(I + 'W12-replay-138-base.tsv')
over = 0; out = {}
for n, f in im.items():
    w = float(f[3]); t = float(f[5]) if f[5] != '-' else w; over += w > max(t, 3.0) + 0.3; out[f[2]] = out.get(f[2], 0) + 1
ex = sorted(float(im[n][3]) - float(ba[n][3]) for n in im if im[n][5] != '-' and im[n][2] == 'allow')
nr = lambda a, q: a[max(0, math.ceil(q * len(a)) - 1)]
print('W12 rows', len(im), 'outcomes', out, 'over', over)
print('1b allowed after rerun n', len(ex), 'p50 %.3f p90 %.3f max %.3f' % (nr(ex, .5), nr(ex, .9), ex[-1]))
print('1b fallback to the baseline kind', sum(1 for n in im if im[n][5] != '-' and im[n][1] == '2' and im[n][2] == ba[n][2]))
print('1b other rerun outcomes', [(n, im[n][2], ba[n][2]) for n in im if im[n][5] != '-' and im[n][2] not in ('allow',) and not (im[n][1] == '2' and im[n][2] == ba[n][2])], 'no rerun', [(n, im[n][2]) for n in im if im[n][5] == '-'])
old = open(w13old, encoding='utf-8').read()
red = re.search(r'^  red: +(.*)$', old, re.M).group(1).split(); green = re.search(r'^  green: +(.*)$', old, re.M).group(1).split()
olds = {i: 'FAIL' for i in red}; olds.update({i: 'PASS' for i in green}); new = {}
for ln in open(scbase, encoding='utf-8', errors='replace'):
    m = re.match(r'^(PASS|FAIL|MISSING|SETUP|SKIP) (\S+)', ln)
    if m and m.group(2) not in new: new[m.group(2)] = m.group(1)
common = sorted(set(olds) & set(new))
print('W13 base red set: 95cf1de7 red', len(red), 'green', len(green), '| now', {k: sum(1 for v in new.values() if v == k) for k in sorted(set(new.values()))})
print('  common', len(common), 'differences (MISSING as FAIL)', [(i, olds[i], new[i]) for i in common if not (olds[i] == new[i] or (olds[i] == 'FAIL' and new[i] == 'MISSING'))])
print('  only in 95cf1de7', sorted(set(olds) - set(new)), '| only now', len(set(new) - set(olds)))
