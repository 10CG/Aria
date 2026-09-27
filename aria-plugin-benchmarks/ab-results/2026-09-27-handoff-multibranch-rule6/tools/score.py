"""从两臂 grading.json 直接汇总 (不经人工转述)。delta.pass_rate = mean(with 臂 pass_rate) - mean(old 臂 pass_rate), 只算主样本 (不含 -rep2/-rep3)。"""
import json, glob, os, re, statistics
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'state-scanner', 'runs')
rows = []
for d in sorted(glob.glob(os.path.join(root, 'eval-*')), key=lambda p: (int(re.search(r'eval-(\d+)', p).group(1)), p)):
    g = {}
    for arm in ('with_skill', 'old_skill'):
        e = json.load(open(os.path.join(d, arm, 'grading.json')))['expectations']
        g[arm] = (sum(1 for x in e if x['passed']), len(e))
    rows.append((os.path.basename(d), g))
print('| eval | 类别 | with | old | with − old |'); print('|---|---|---|---|---|')
for name, g in rows:
    kind = '复跑' if re.search(r'-rep\d$', name) else '主样本'
    w, o = g['with_skill'], g['old_skill']
    print(f'| {name} | {kind} | {w[0]}/{w[1]} | {o[0]}/{o[1]} | {w[0]-o[0]:+d} |')
main = [g for n, g in rows if not re.search(r'-rep\d$', n)]
wr = [g['with_skill'][0] / g['with_skill'][1] for g in main]
orr = [g['old_skill'][0] / g['old_skill'][1] for g in main]
W = sum(g['with_skill'][0] for g in main); O = sum(g['old_skill'][0] for g in main); T = sum(g['with_skill'][1] for g in main)
print()
print(f'主样本 eval 数 = {len(main)}; 断言合计 with {W}/{T} · old {O}/{T}')
print(f'mean(with pass_rate) = {statistics.mean(wr):.4f}; mean(old pass_rate) = {statistics.mean(orr):.4f}')
print(f'delta.pass_rate = {statistics.mean(wr) - statistics.mean(orr):+.4f}')
lower = [n for n, g in rows if g['with_skill'][0] < g['old_skill'][0] and not re.search(r'-rep\d$', n)]
print('主样本中 with < old 的 eval:', lower or '无')
for n in lower:
    samples = [g for m, g in rows if m == n or m.startswith(n + '-rep')]
    k = sum(1 for g in samples if g['with_skill'][0] < g['old_skill'][0])
    print(f'  {n}: 样本 {len(samples)} 个, 其中 with < old 的 {k} 个 ⇒ {"判回归" if k >= 2 else "不判回归"}')
