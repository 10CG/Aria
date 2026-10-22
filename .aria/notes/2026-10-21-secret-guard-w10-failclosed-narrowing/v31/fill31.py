#!/usr/bin/env python3
"""fill31.py <proposal template> <v3.1 hook> <evidence dir (v31/)> <out> : fills the proposal's placeholders from the evidence, so every quoted block and number
equals the prototype and the runs. Asserts that EVERY hunk of W8-v31.diff is either quoted in <<<CODE-LOGIC>>> or a comment-only hunk (What 7 lists those by
site): post_planning R1 PP1-A30 found a logic line that v3's fill.py had silently dropped."""
import re, sys, os, csv, subprocess, tempfile
tpl, hook, ev, out = sys.argv[1:5]
t = open(tpl, encoding='utf-8').read(); H = open(hook, encoding='utf-8').read()
P = lambda n: os.path.join(ev, n)
D = open(P('W8-v31.diff'), encoding='utf-8').read()
hunks = re.split(r'(?m)^(?=@@ )', D.split('\n', 2)[2])
def comment_only(h):
    ch = [l[1:] for l in h.split('\n')[1:] if l[:1] in '+-']
    return all((not c.strip()) or c.lstrip().startswith('#') for c in ch)
logic = [h.rstrip('\n') for h in hunks if not comment_only(h)]
comm = [h for h in hunks if comment_only(h)]
assert logic and len(logic) + len(comm) == len(hunks)
code_logic = '```diff\n' + '\n'.join(logic) + '\n```\n\n（共 %d 个 hunk：%d 个逻辑 hunk 全部列在上面，%d 个只改注释的 hunk 见 What 7。）' % (len(hunks), len(logic), len(comm))
added = sum(1 for l in D.split('\n') if l.startswith('+') and not l.startswith('+++'))
blank = sum(1 for l in D.split('\n') if l == '+')
removed = sum(1 for l in D.split('\n') if l.startswith('-') and not l.startswith('---'))
w8count = f'+{added} / −{removed} 行，新增里 {blank} 行空行'
s = H.index('  if [[ "$kind" == longline ]]; then\n    cat >&2 <<EOF\n') + len('  if [[ "$kind" == longline ]]; then\n    cat >&2 <<EOF\n')
code_long = '```\n' + H[s:H.index('\nEOF\n', s)] + '\n```'
ns = {}; src = open(P('commentsync.py'), encoding='utf-8').read()
exec(src[src.index('HOOK_SITES = ['):src.index('bad = 0')], ns)
rows = ['| 处 | 位置（基线） | 定位用的锚点短语（改后 0 次） |', '|---|---|---|']
for site, h, anchors in ns['HOOK_SITES'] + ns['SUITE_SITES']:
    n, where = site.split(' ', 1)
    rows.append(f'| {n} | {where} | ' + '；'.join('`' + a.replace('|', '\\|') + '`' for a, _ in anchors) + ' |')
for site, title, _ in ns['SUITE_TITLES']:
    n, where = site.split(' ', 1)
    rows.append(f'| {n} | {where}（用例标题，整句） | `' + title.replace('|', '\\|') + '` |')
table = '\n'.join(rows) + '\n\n「应出现」的词（改后至少 1 次，基线 0 次）——hook：' + '、'.join('`%s`' % w for w in ns['ADD_HOOK']) + '；套件：' + '、'.join('`%s`' % w for w in ns['ADD_SUITE']) + '。'
W12 = open(P('W12-real-traffic.txt'), encoding='utf-8').read()
def g(rx, txt=W12): m = re.search(rx, txt); assert m, rx; return m
oc = dict((k, int(v)) for k, v in re.findall(r'outcome (\S+)\s+(\d+)', W12))
wall = g(r'allow wall \(s\): n=(\d+) p50=([\d.]+) p90=([\d.]+) p99=([\d.]+) max=([\d.]+)')
over = g(r'every outcome within max\(trigger, 3 s\) \+ 0\.3 s: (\d+) of (\d+) over the bound')
ident = g(r'## 2\..*?identical=(\d+) different=(\d+)', re.sub(r'\n', ' ', W12)); ident32 = g(r'## 3\..*?identical=(\d+) different=(\d+)', re.sub(r'\n', ' ', W12))
load = re.findall(r'load ([\d.]+ [\d.]+ [\d.]+)', W12)
others = '、'.join(f'{k} {v} 条' for k, v in sorted(oc.items()) if k != 'allow')
w12rows = (f"| v3.1 原型逐条回放这 138 条（GNU/Linux、bash 5.2、无扩展；负载见 W12 页眉 {load[0]} → {load[-1]}） | "
           f"放行 {oc.get('allow', 0)} 条，其余 {others}；放行的墙钟中位 {wall.group(2)} s、p90 {wall.group(3)} s、p99 {wall.group(4)} s、最慢 {wall.group(5)} s。"
           f"138 条的每一种结局都核对了上界 max(触发时刻, 3 s) + 0.3 s：超出 {over.group(1)} 条 | W12 第 1 节 |\n"
           f"| 放宽类之外 | 抽样 300 条退出码与 stderr 逐字节相同（{ident.group(1)} / 300）；bash 3.2 下 W1 抽 40 条逐字节相同（{ident32.group(1)} / 40） | W12 第 2、3 节 |")
W13 = open(P('W13-sc-cases.txt'), encoding='utf-8').read()
sec = re.split(r'(?m)^## ', W13)
r1 = [l for l in sec[1].split('\n')[1:] if l.startswith('bash ')]
r2 = g(r'# totals: PASS (\d+)\s+FAIL (\d+)\s+SKIP (\d+)', sec[2])
mres = {m.group(1): m for m in re.finditer(r'(?m)^(BI-\d+)\s+(CAUGHT|MISSED)\s+(.*?) \| designated: (.*?) \| other red: (.*)$', sec[3])}
msum = g(r'# (\d+) caught, (\d+) missed \(of (\d+)\)', sec[3])
lines = ['| 被测 hook × bash | 结果 |', '|---|---|']
for l in r1:
    ver = l.split()[1]; tot = g(r'PASS (\d+)\s+FAIL (\d+)\s+SKIP (\d+)', l); rel = g(r'relaxation expected: (\w+)', l).group(1)
    lines.append(f"| v3.1 原型 × bash {ver.split('(')[0]}（期望放宽：{'是' if rel == 'yes' else '否'}） | PASS {tot.group(1)}、FAIL {tot.group(2)}、SKIP {tot.group(3)} |")
lines.append(f"| 基线 × bash 5.2（基线作为被测 hook） | PASS {r2.group(1)}、FAIL {r2.group(2)}：FAIL 的即基线红集，PASS 的是回归闸（P1 抽样、VMAX、基线那一遍的计数上限等），明细见 W13 第 2 节 |")
lines.append(f"| {msum.group(3)} 个坏实现 × bash 5.2 | {msum.group(1)} 个被各自的指定用例全部抓住，{msum.group(2)} 个漏网（下表） |")
sc_results = '\n'.join(lines)
bi = ['| BI | 坏实现（v3.1 + 一处改动） | 指定用例（须全部变红） | W13 | 连带变红的其他用例 |', '|---|---|---|---|---|']
TMP = tempfile.mkdtemp()   # the BI list with its designated cases comes from mutants.py itself, built against the same hook
subprocess.run([sys.executable, P('mutants.py'), hook, TMP], check=True, capture_output=True)
for i, cases, desc in csv.reader(open(os.path.join(TMP, 'designated.tsv'), encoding='utf-8'), delimiter='\t'):
    m = mres[i]
    other = m.group(5).strip()
    bi.append(f"| {i} | {desc} | {'、'.join('`%s`' % c for c in cases.split())} | {'抓住' if m.group(2) == 'CAUGHT' else '**漏网**'} | {'—' if other == 'none' else len(other.split())} |")
bi_table = '\n'.join(bi)
for k, v in (('<<<CODE-LOGIC>>>', code_logic), ('<<<CODE-LONGLINE>>>', code_long), ('<<<COMMENT-TABLE>>>', table), ('<<<W12-ROWS>>>', w12rows),
             ('<<<W8-COUNT>>>', w8count), ('<<<SC-RESULTS>>>', sc_results), ('<<<BI-TABLE>>>', bi_table)):
    assert t.count(k) == 1, k
    t = t.replace(k, v)
assert not re.search(r'<<<[A-Z0-9-]+>>>', t), 'unfilled placeholder'
with open(out, 'w', encoding='utf-8') as f: f.write(t)
print('filled', len(t.encode()), 'bytes;', len(logic), 'logic hunks quoted,', len(comm), 'comment-only hunks')
