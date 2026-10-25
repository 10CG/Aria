#!/usr/bin/env python3
"""mkreport.py: assemble T005f-report.md from the narrative below and the mechanically extracted parts (diffs, before/after texts, run summaries)."""
import subprocess, re, os, glob
S = '/tmp/claude-1000/-home-dev-Aria/d97ed439-6e11-46f3-83bd-93caeddb60ff/scratchpad'
T = f'{S}/r217impl/t005f'; W = f'{S}/wt217/aria'; A = '/home/dev/Aria'
NV = '.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31'
OUT = f'{S}/r217impl/T005f-report.md'
sh = lambda *a, cwd=None: subprocess.run(a, cwd=cwd, capture_output=True, text=True).stdout
rd = lambda p: open(p, encoding='utf-8').read() if os.path.exists(p) else ''
def fence(t, lang='diff'): return f'```{lang}\n{t.rstrip()}\n```\n'
hookdiff = sh('git', 'diff', '2893bcc', '--', 'hooks/secret-guard.sh', cwd=W)
helperdiff = sh('git', 'diff', '--', 'hooks/tests/lib/secret-guard-w10-direct.sh', cwd=W)
suitediff = sh('git', 'diff', '--', 'hooks/tests/secret-guard.test.sh', cwd=W)
scddiff = sh('git', 'diff', '--', f'{NV}/sc-direct.sh', cwd=A)
sccdiff = sh('git', 'diff', '--', f'{NV}/sc-cases.sh', cwd=A)
w14diff = sh('git', 'diff', '--', f'{NV}/impl/w14-mutants.py', cwd=A)
csdiff = sh('git', 'diff', '--', f'{NV}/commentsync.py', cwd=A)
mutdiff = sh('git', 'diff', '--stat', '--', f'{NV}/mutants.py', cwd=A)
wtstat = sh('git', 'status', '--short', cwd=W); mainstat = sh('git', 'status', '--short', cwd=A)
sha = lambda p: sh('sha256sum', p)[:12]
# INV-2: the change lines of the helper and of v31/sc-direct.sh, compared (the helper alone also lists the relax ids in RELAX_IDS)
chg = lambda d: [l for l in d.split('\n') if l[:1] in '+-' and not l.startswith(('+++', '---'))]
hc, sc = chg(helperdiff), chg(scddiff)
only_h = [l for l in hc if l not in sc]; only_s = [l for l in sc if l not in hc]
# before / after of every changed comment place, verbatim, from the hunks of the hook diff and the suite diff
def hunks(d):
    out, cur = [], None
    for l in d.split('\n'):
        if l.startswith('@@'):
            cur = {'head': l, 'old': [], 'new': []}; out.append(cur)
        elif cur is not None and l[:1] == '-' and not l.startswith('---'): cur['old'].append(l[1:])
        elif cur is not None and l[:1] == '+' and not l.startswith('+++'): cur['new'].append(l[1:])
    return out
def joined(ls):
    return re.sub(r'\s+', ' ', ' '.join(re.sub(r'^\s*#', '', x) if re.match(r'\s*#', x) else x for x in ls)).strip()
places = []
for h in hunks(hookdiff) + [x for x in hunks(suitediff) if any('relaxation is not in effect' in y for y in x['old'])]:
    places.append(h)
ba = []
for i, h in enumerate(places, 1):
    ba.append(f'#### 片段 {i}  `{h["head"]}`\n\n改前（逐行）：\n\n' + fence('\n'.join(h['old']) or '(无)', 'text') + '\n改后（逐行）：\n\n' + fence('\n'.join(h['new']), 'text'))
    if all(re.match(r'\s*#', x) for x in h['old'] + h['new']) and h['old']:
        ba.append('读者所见（去掉 `#`、合并空白）：\n\n- 改前：' + joined(h['old']) + '\n- 改后：' + joined(h['new']) + '\n')
# run summaries
def runsum():
    o = []
    log = rd(f'{T}/runs/steps.log'); o.append('`runs/steps.log`（每步开跑前等一分钟负载 < 1.2；load0 / load1 = 开跑时与结束时的 1/5/15 分钟负载）：\n\n' + fence(log or '(尚无)', 'text'))
    for f in sorted(glob.glob(f'{T}/runs/*.txt')):
        n = os.path.basename(f); t = rd(f); keep = []
        for l in t.split('\n'):
            if re.match(r'^(PASS|FAIL|SKIP): ', l) or l.startswith(('W10 ported cases:', '# totals', '# load', '# perturbation round', '# end', '# designated round', '# sc-cases.sh')) or re.search(r'SC-13|V0-H2|FILTERED ROUND|branch \(', l):
                keep.append(l[:400])
        cnt = {}
        for l in t.split('\n'):
            m = re.match(r'^(BI-\S+|P-\S+|QA-\S+)\s+(\S+)', l)
            if m: cnt[m.group(2)] = cnt.get(m.group(2), 0) + 1
        if cnt: keep.append('verdict counts (column 2): ' + ', '.join(f'{k} {v}' for k, v in sorted(cnt.items())))
        fails = [l[:300] for l in t.split('\n') if re.match(r'^(FAIL|MISSING|SETUP)\b', l) or re.match(r'^\S+\s+(MISSED|WRONG-REASON|SETUP|NOT-JUDGED)\b', l)]
        o.append(f'**{n}**\n\n' + fence('\n'.join(keep[-14:] + fails[:12]) or '(无摘要行)', 'text'))
    return '\n'.join(o)
narr = rd(f'{T}/report-narrative.md')
rep = [narr,
 '\n## 附录 A：hook 完整 diff（`git diff 2893bcc -- hooks/secret-guard.sh`，sha256 前缀 ' + sha(f'{W}/hooks/secret-guard.sh') + '）\n\n' + fence(hookdiff),
 '\n## 附录 B：What 7 补充 2 各处与 WSL 两行的改前改后逐字文本（由附录 A 与套件 diff 的 hunk 机械抽出）\n\n' + '\n'.join(ba),
 '\n## 附录 C：helper diff（新用例代码在此；`hooks/tests/lib/secret-guard-w10-direct.sh`，sha256 前缀 ' + sha(f'{W}/hooks/tests/lib/secret-guard-w10-direct.sh') + '）\n\n' + fence(helperdiff),
 '\n## 附录 D：INV-2 —— helper 与 `v31/sc-direct.sh` 的改动行比对\n\n' + f'helper 改动行 {len(hc)}，sc-direct.sh 改动行 {len(sc)}；只在 helper 的：\n\n' + fence('\n'.join(only_h) or '(无)') + '\n只在 sc-direct.sh 的：\n\n' + fence('\n'.join(only_s) or '(无)'),
 '\n## 附录 E：套件、sc-cases.sh、w14-mutants.py、commentsync.py 的 diff；mutants.py 的 diffstat\n\n' + fence(suitediff) + fence(sccdiff) + fence(w14diff) + fence(csdiff) + fence(mutdiff or '(mutants.py 无改动)', 'text'),
 '\n## 附录 F：「能红」矩阵（`t005f/prove-helper.txt`，helper 直跑 SC_ONLY=^V15-）\n\n' + fence(rd(f'{T}/prove-helper.txt'), 'text'),
 '\n## 附录 G：各轮输出摘要（机械抽取，原文在 `t005f/runs/`）\n\n' + fence(rd(f'{T}/expect.md'), 'markdown') + runsum(),
 '\n## 附录 H：git status（worktree / 主仓）\n\n' + fence(wtstat, 'text') + fence(mainstat, 'text')]
open(OUT, 'w', encoding='utf-8').write('\n'.join(rep))
print(OUT, len('\n'.join(rep)), 'chars;', 'INV-2 only-helper', len(only_h), 'only-scd', len(only_s), '; places', len(places))
