#!/usr/bin/env python3
# gen-b.py -> rep-b.md: report sections 3 (comment and title sentences, before / after) and 4 (the rounds), generated from the files, not typed
import re, sys
T = '/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/r217impl/t002d'
WT = '/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad/wt217/aria'
sys.path.insert(0, T)
from apply3b import runs, site_run, LOCS
base, tgt = T + '/base-suite.sh', WT + '/hooks/tests/secret-guard.test.sh'
cut = lambda t: re.split(r'(?<=[.;])\s+', t)
out = ['', '## 3. 注释与标题改写前后对照 (只列句子)', '',
       '切句与 commentsync 相同 (连续 # 行去前缀连成一行, 在 `.` 与 `;` 之后切)。原句一字不改仍在改后段里的算 "保留", 不另列。由 `t002d/gen-b.py` 从两份套件生成。', '']
RB, RT = runs(base), runs(tgt)
for site, loc in LOCS:
    b, t = site_run(RB, loc), site_run(RT, loc)
    old = [s for s in cut(b) if s not in t]; new = [s for s in cut(t) if s not in b]
    out += [f'### 第 {site.split()[0]} 处 ({site.split(" ", 1)[1]}; 紧挨 `{loc[1]}` 的注释段; 保留 {len(cut(b)) - len(old)} 句)', '', '改写前 (删掉的句子):']
    out += [f'- {s}' for s in old] + ['', '改写后 (新句):'] + [f'- {s}' for s in new] + ['']
out += ['### 第 16-20 处 (用例标题, 整句)', '']
def title(p, n): return [re.match(r'wpa_begin_bash_case "([^"]*)"', l).group(1) for l in open(p, encoding='utf-8') if l.startswith(f'wpa_begin_bash_case "W10 SC-{n} ')][0]
for k, n in [('16', '21ab'), ('17', '21ag'), ('18', '21aj'), ('19', '21al'), ('20', '21ao')]:
    out += [f'- 第 {k} 处 {n} 改写前: {title(base, n)}', f'  - 改写后: {title(tgt, n)}']
out += ['', '## 4. 各轮结果与首尾负载', '',
        '每轮在 worktree 里跑 `taskset -c 0,1 nice -n 19 bash hooks/tests/secret-guard.test.sh` (PATH 上的 bash = /usr/bin/bash 5.2.15), 开跑前等一分钟负载 <= 1.2; 输出 `t002d/<轮>.out`、`<轮>.w10log`、`<轮>.meta`。',
        '"整轮负载" 是驱动在开跑前与结束后读的 /proc/loadavg; "计时批负载" 是套件在 W10 批首尾读的 (INV-7 判据, 门槛 2)。', '',
        '| 轮 | SC_BASH / 环境 | 整轮开跑 → 结束负载 | PASS / FAIL / SKIP / 总数 | SKIP 原因 | 放宽预期 | 计时批: 开始 → 结束负载, 结论 | 移植编号数 | 6 组 | SC-13 |',
        '|---|---|---|---|---|---|---|---|---|---|']
fails = []
for lb in ['b-usr', 'b-5.0.18', 'b-5.1.16', 'b-5.3.20', 'b-3.2.57', 'b-3.2.57-r2', 'wsl']:
    try: meta = open(f'{T}/{lb}.meta').read(); o = open(f'{T}/{lb}.out').read()
    except OSError: out.append(f'| {lb} | (未跑完) |'); continue
    g = lambda pat, s=o: (re.search(pat, s, re.M) or [None, '?'])
    st = re.search(r'^start \S+ loadavg (\S+ \S+ \S+)', meta, re.M); en = re.search(r'^end \S+ rc (\d+) loadavg (\S+ \S+ \S+)', meta, re.M)
    p = re.search(r'^PASS: (\d+) / (\d+)', o, re.M); f = re.search(r'^FAIL: (\d+)', o, re.M); sk = re.search(r'^SKIP: (\d+) / \d+ \((.*)\)', o, re.M)
    w = re.search(r'^W10 ported cases: SC_BASH (\S+) \((.*?)\) -> relaxation expected: (\w+) \| load start (\S+ \S+ \S+) end (\S+ \S+ \S+) \| timing batch: (.*)$', o, re.M)
    six = re.search(r'^W10 older groups [^:]*: (\w+ branch)', o, re.M)
    fl = [l.strip()[:200] for l in o.split('\n') if l.startswith('  FAIL')]
    fails += [f'{lb}: {l}' for l in fl]
    n = sum(1 for l in open(f'{T}/{lb}.w10log') if l.strip() and not l.startswith('#'))
    env = ' + WSL_DISTRO_NAME=Ubuntu' if lb == 'wsl' else ''
    out.append(f'| {lb} | {w.group(1) if w else "?"} ({w.group(2) if w else "?"}){env} | {st.group(1) if st else "?"} → {en.group(2) if en else "?"} (rc {en.group(1) if en else "?"}) | '
               f'{p.group(1) if p else "?"} / {f.group(1) if f else "?"} / {sk.group(1) if sk else "?"} / {p.group(2) if p else "?"} | {sk.group(2) if sk else "?"} | {w.group(3) if w else "?"} | '
               f'{w.group(4) if w else "?"} → {w.group(5) if w else "?"}, {w.group(6) if w else "?"} | {n} | {six.group(1) if six else "?"} | {"FAIL" if any("SC-13" in l for l in fl) else "绿"} |')
    waits = re.findall(r'^(wait .*|WAIT.*)$', meta, re.M)
    if waits: out.append(f'|  | 开跑前等待读数: {"; ".join(waits)} |')
out += ['', 'FAIL 行: ' + ('无' if not fails else '')] + [f'- {x}' for x in fails]
sixl = [re.search(r'^W10 older groups .*$', open(f'{T}/{lb}.out').read(), re.M) for lb in ['b-usr', 'wsl']]
out += ['', 'Summary 新行 (b-usr 与 wsl 两轮原文):'] + [f'- `{m.group(0)}`' for m in sixl if m]
open(T + '/rep-b.md', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('rep-b.md', len(out), 'lines; FAIL lines', len(fails))
