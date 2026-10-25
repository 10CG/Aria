import re
R = '/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/T005f4-report.md'
rd = lambda p: open(p, encoding='utf-8').read()
def parts(diff):
    out = {}; cur = None
    for l in diff.splitlines(True):
        m = re.match(r'diff --git a/(\S+) ', l)
        if m: cur = m.group(1); out[cur] = ''
        if cur: out[cur] += l
    return out
w = parts(rd('diffs/wt.diff')); v = parts(rd('diffs/v31.diff'))
pre = '.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/'
nl = lambda s: s if s.endswith('\n') else s + '\n'
sub = {'HOOKDIFF': w['hooks/secret-guard.sh'], 'HELPERDIFF': w['hooks/tests/lib/secret-guard-w10-direct.sh'], 'PROVE': rd('prove5f4.out'),
       'TABLE': rd('criteria-table.md'), 'STEPS': rd('runs/steps.log'), 'FINAL': rd('final-state.txt'),
       'OTHERDIFF': w['hooks/tests/secret-guard.test.sh'] + v[pre + 'sc-cases.sh'] + v[pre + 'impl/w14-mutants.py']}
t = rd('tmpl.md')
for k, s in sub.items():
    assert t.count('@@%s@@' % k) == 1, k; t = t.replace('@@%s@@' % k, nl(s))
assert not re.search(r'@@[A-Z]+@@', t), 'placeholder left'
open(R, 'w', encoding='utf-8').write(t); print('written', len(t.encode('utf-8')), 'bytes,', t.count('\n'), 'lines; v31 diff files:', sorted(x.split('/')[-1] for x in v))
