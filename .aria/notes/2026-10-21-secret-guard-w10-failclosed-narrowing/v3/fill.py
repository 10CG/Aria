#!/usr/bin/env python3
"""fill.py <proposal draft> <v3 hook> <W8 diff> <W12 txt> <out>: fills the proposal's code / table placeholders from the evidence, so every quoted block equals the prototype."""
import re, sys, importlib.util, os
draft, hook, w8, w12, out = sys.argv[1:6]
t = open(draft, encoding='utf-8').read()
H = open(hook, encoding='utf-8').read()
D = open(w8, encoding='utf-8').read()
hunks = re.split(r'(?m)^(?=@@ )', D.split('\n', 2)[2])           # drop the --- / +++ header
def pick(pred):
    sel = [h.rstrip('\n') for h in hunks if pred(h)]
    assert sel, 'no hunk'
    return '```diff\n' + '\n'.join(sel) + '\n```'
is_funcs = lambda h: '_sg_relax_run() {' in h
is_long = lambda h: 'kind" == longline' in h
is_eval = lambda h: '_sg_relax_run "$cmd"' in h
code_pass = pick(lambda h: not (is_funcs(h) or is_long(h) or is_eval(h)))
code_eval = pick(is_eval)
s = H.index('# #217 relaxed rerun. When the relaxation'); e = H.index('\n# W9 -- project-level extension')
code_funcs = '```bash\n' + H[s:e].strip('\n') + '\n```'
s = H.index('  if [[ "$kind" == longline ]]; then\n    cat >&2 <<EOF\n') + len('  if [[ "$kind" == longline ]]; then\n    cat >&2 <<EOF\n')
e = H.index('\nEOF\n', s)
code_long = '```\n' + H[s:e] + '\n```'
spec = importlib.util.spec_from_file_location('cs', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'commentsync.py'))
src = open(spec.origin, encoding='utf-8').read()
RETIRE = re.findall(r"\('(\d+ [a-z]+ :[0-9-]+ [^']*)', [HT], '((?:[^'\\]|\\.)*)'\)", src)
ADD = re.findall(r"\('(hook|test)', [HT], w\) for w in \(([^)]*)\)", src)
rows = ['| 处 | 位置（基线） | 退役短语（改后 0 次） |', '|---|---|---|']
for site, ph in RETIRE:
    n, f, rng = site.split(' ', 3)[:3]
    where = site.split(' ', 1)[1]
    rows.append(f'| {n} | {where} | `' + ph.replace('|', '\\|') + '` |')
adds = []
for f, ws in ADD:
    adds.append(f"{'hook' if f=='hook' else '套件'}：" + '、'.join('`%s`' % w.strip().strip("'") for w in ws.split(',') if w.strip()))
table = '\n'.join(rows) + '\n\n「应出现」的词（改后至少 1 次，基线 0 次）——' + '；'.join(adds) + '。这一半只核对出现，不核对位置，位置由 TASK-005 的代码审查把关。'
W = open(w12, encoding='utf-8').read()
def g(rx): m = re.search(rx, W); assert m, rx; return m
allow = int(g(r'outcome allow\s+(\d+)').group(1)); over = int(g(r'outcome oversize\s+(\d+)').group(1))
wall = g(r'allow wall \(s\): n=(\d+) p50=([\d.]+) p90=([\d.]+) p99=([\d.]+) max=([\d.]+)')
ident = g(r'identical=(\d+) different=(\d+)'); ident32 = re.findall(r'identical=(\d+) different=(\d+)', W)[-1]
load = re.findall(r'load ([\d.]+ [\d.]+ [\d.]+)', W)
def res(name):
    p = os.path.join(os.path.dirname(w12), name)
    rows = [l.rstrip('\n').split('\t') for l in open(p, encoding='utf-8')]
    a = sum(1 for r in rows if r[2] == 'allow'); r = [r for r in rows if r[0] == '172'][0]
    return a, ('放行 %s s' % r[3]) if r[2] == 'allow' else ('回落为基线拦截 %s s' % r[3])
a1, n1 = res('W12-replay-138.tsv'); a2, n2 = res('W12b-replay-138.tsv')
w12rows = (f"| v3 原型逐条回放这 138 条（Linux、bash 5.2、无扩展；负载见 W12 页眉 {load[0]} → {load[-1]}） | "
           f"放行 {allow} 条，按尺寸拦 {over} 条（{'即' if over == 1 else '含'} VMAX 那 1 条）；放行的墙钟中位 {wall.group(2)} s、p90 {wall.group(3)} s、p99 {wall.group(4)} s、最慢 {wall.group(5)} s。"
           f"同一原型独立回放两次，放行 {a1} 条与 {a2} 条；判定最慢的 n=172（W1 判定 0.97 s）离截止最近，两次分别为「{n1}」与「{n2}」。截止前判不完的命令按 P3、P6 回落为基线拦截，不会放行 | W12 第 1 节；W12b |\n"
           f"| 放宽类之外 | 抽样 300 条退出码与 stderr 逐字节相同（{ident.group(1)} / 300）；bash 3.2 下 W1 抽 40 条逐字节相同（{ident32[0]} / 40） | W12 第 2、3 节 |")
for k, v in (('<<<CODE-PASS>>>', code_pass), ('<<<CODE-EVAL>>>', code_eval), ('<<<CODE-FUNCS>>>', code_funcs), ('<<<CODE-LONGLINE>>>', code_long), ('<<<COMMENT-TABLE>>>', table), ('<<<W12-ROWS>>>', w12rows)):
    assert t.count(k) == 1, k
    t = t.replace(k, v)
assert not re.search(r'<<<[A-Z0-9-]+>>>', t), 'unfilled placeholder'
open(out, 'w', encoding='utf-8').write(t)
print('filled', len(t.encode()))
