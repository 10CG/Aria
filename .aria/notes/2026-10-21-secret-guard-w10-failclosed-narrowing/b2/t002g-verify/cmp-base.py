# compare the suite's statuses on 59e333c (SG_W10_LOG) with v31's base-5.2.15.txt, id by id; prints counts and differences only
import sys, re
def load(p):
    d = {}
    for ln in open(p, encoding='utf-8', errors='replace'):
        m = re.match(r'^(PASS|FAIL|MISSING|SKIP|SETUP|TIMED) (\S+)(.*)$', ln.rstrip('\n'))
        if m and m.group(2) not in d: d[m.group(2)] = (m.group(1), m.group(3))
    return d
v31, suite = load(sys.argv[1]), load(sys.argv[2])
cnt = {}
for st, det in suite.values(): cnt[st] = cnt.get(st, 0) + 1
print('suite', dict(sorted(cnt.items())), 'missing-tag', sum(1 for st, det in suite.values() if st == 'FAIL' and '[missing]' in det),
      'reference-tag', sum(1 for st, det in suite.values() if '[reference]' in det))
only_v31 = sorted(set(v31) - set(suite)); only_suite = sorted(set(suite) - set(v31))
print('ids: v31', len(v31), 'suite', len(suite), 'common', len(set(v31) & set(suite)), 'only v31', only_v31, 'only suite', only_suite)
diff = []
for i in sorted(set(v31) & set(suite)):
    a, b = v31[i][0], suite[i][0]
    want = 'FAIL' if a == 'MISSING' else a
    if b != want or (a == 'MISSING' and '[missing]' not in suite[i][1]): diff.append((i, a, b))
print('status differences', len(diff)); [print(' ', *x) for x in diff[:20]]
