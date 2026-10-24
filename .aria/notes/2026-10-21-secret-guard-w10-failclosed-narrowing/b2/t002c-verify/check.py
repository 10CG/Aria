# check.py <verify dir> : compares the verification outputs with PREDICT.md's items (numbers and ids only)
import sys, re, os
O = sys.argv[1]
def rows(path):   # v31 / SG_W10_LOG lines: STATUS id detail
    d = {}
    for ln in open(path, encoding='utf-8', errors='replace'):
        m = re.match(r'^(PASS|FAIL|SKIP|MISSING|SETUP) (\S+) ?(.*)$', ln.rstrip('\n'))
        if m: d.setdefault(m.group(2), []).append((m.group(1), m.group(3)))
    return d
print('== R1 W10-only rounds')
for v in ('5.2', '5.0', '5.1', '5.3', '3.2'):
    p = f'{O}/w10-{v}.txt'
    if not os.path.exists(p): print(v, 'missing'); continue
    t = open(p, encoding='utf-8', errors='replace').read()
    s = {k: re.search(k + r': (\d+) / (\d+)', t) for k in ('PASS', 'FAIL', 'SKIP')}
    tb = re.search(r'relaxation expected: (\w+) \| load start (\S+) .* end (\S+) .*\| timing batch: (.*)', t)
    lg = rows(f'{O}/w10-{v}.log'); dup = [i for i, x in lg.items() if len(x) > 1]
    print(v, ' '.join(f"{k} {m.group(1)}/{m.group(2)}" if m else f'{k} ?' for k, m in s.items()), '| relax', tb.group(1) if tb else '?',
          '| load', tb.group(2) if tb else '?', '->', tb.group(3) if tb else '?', '| batch', tb.group(4) if tb else '?', '| log ids', len(lg), 'dup', len(dup),
          '| skip reasons', sorted({x[0][1].split(']')[0] + ']' for x in lg.values() if x[0][0] == 'SKIP'}))
print('== R2 / R5 equivalence (5.2)')
a = rows(f'{O}/sc-cases-5.2.txt'); b = rows(f'{O}/w10-5.2.log')
print('sc-cases ids', len(a), 'statuses', {s: sum(1 for x in a.values() if x[0][0] == s) for s in ('PASS', 'FAIL', 'SKIP', 'MISSING', 'SETUP')})
tbl = re.search(r'timing batch: .*', open(f'{O}/sc-cases-5.2.txt', encoding='utf-8', errors='replace').read()); print('sc-cases', tbl.group(0) if tbl else 'no batch line')
only_a = sorted(set(a) - set(b)); only_b = sorted(set(b) - set(a)); diff = sorted(i for i in set(a) & set(b) if a[i][0][0] != b[i][0][0])
print('common', len(set(a) & set(b)), '| only sc-cases', only_a, '| only suite', only_b, '| status differs', diff)
print('== R4 bad implementations')
rs = {}
for ln in open(f'{O}/mut/reasons.tsv', encoding='utf-8'):
    f = ln.rstrip('\n').split('\t')
    if len(f) >= 3: rs[(f[0], f[1])] = f[2]
des = {}
for ln in open(f'{O}/mut/designated.tsv', encoding='utf-8'):
    f = ln.rstrip('\n').split('\t'); des[f[0]] = f[1].split()
for bi in ('BI-8', 'BI-5', 'BI-45', 'BI-24', 'BI-7', 'BI-11'):
    p = f'{O}/mut-{bi}.log'
    if not os.path.exists(p): print(bi, 'no log'); continue
    lg = rows(p); out = []
    for c in des[bi]:
        st, det = (lg.get(c) or [('absent', '')])[0]; rx = rs.get((bi, c), '')
        verdict = 'red' if st == 'FAIL' and re.search(rx, det) else ('red-other-reason' if st == 'FAIL' else st.lower())
        out.append(f'{c}={verdict}' + ('' if verdict == 'red' else f' [{det[:150]}]'))
    hd = open(f'{O}/mut-{bi}.txt', encoding='utf-8', errors='replace').readline().strip()[:150]
    print(bi, '|', ' ; '.join(out), '|', re.sub(r'.*\| hook ', 'hook ', hd)[:40])
lg = rows(f'{O}/ctl-impl.log'); print('ctl impl:', {i: x[0][0] for i, x in lg.items()})
print('== R3 full round 5.2')
p = f'{O}/full-5.2.txt'
if os.path.exists(p):
    t = open(p, encoding='utf-8', errors='replace').read()
    for k in ('PASS', 'FAIL', 'SKIP'):
        m = re.search(k + r': (\d+) / (\d+)', t); print(k, m.group(0) if m else '?')
    print(re.search(r'W10 ported cases: .*', t).group(0)[:260] if re.search(r'W10 ported cases: .*', t) else 'no W10 line')
    print('FAIL titles:', [x[:60] for x in re.findall(r'^  FAIL[^\n]*', t, re.M)][:12])
    print('SC-13 lines:', [x[:120] for x in re.findall(r'^.*SC-13[^\n]*', t, re.M)][:4])
