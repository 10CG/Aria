"""gen-table.py <t002g dir> : per-id table (v31 mut-summary vs suite mode first run vs low-load rerun) -> <dir>/table.md; prints a short summary."""
import re, sys
out = sys.argv[1]
MUT = '/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/b2/t002b-verify/mut-summary.txt'
RM = '/home/dev/Aria/.aria/notes/2026-10-21-secret-guard-w10-failclosed-narrowing/v31/run-mutants.sh'
refids = set(' '.join(re.findall(r"^REFIDS\+?='([^']*)'", open(RM, encoding='utf-8').read(), re.M)).split())


def parse(p):
    d = {}
    for line in open(p, encoding='utf-8', errors='replace'):
        m = re.match(r'^((?:BI|P)-\S+)\s+(\S+)', line)
        if not m:
            continue
        toks = re.findall(r'\s(V\d+-[A-Z]\d+\S*?)=(\S+)', line)
        b = re.search(r'timing batch: ([^|]*?)\s*(?:\||$)', line)
        ls = re.search(r'load start (\S+)', line)
        d[m.group(1)] = (m.group(2), toks, b.group(1).strip() if b else '', ls.group(1) if ls else '')
    return d


a = parse(MUT)
s = parse(out + '/all.txt')
r = parse(out + '/rerun-load.txt')
r.update(parse(out + '/p0-rerun.txt'))
rows = ['| 编号 | v31 判定 (mut-summary) | 套件首跑判定 | 首跑计时批 (起始一分钟负载) | 低负载重跑 (计时批, 起始负载) | 指定用例 = 套件首跑状态 (\\* = 走关门臂) | 与 v31 |',
        '|---|---|---|---|---|---|---|']
nref = []
void = []
for i in a:
    va, ta, _, _ = a[i]
    vs, ts, bs, ls = s.get(i, ('absent', [], '', ''))
    rr = r.get(i)
    if bs.startswith('void'):
        void.append(i)
    rerun = f'{rr[0]} ({rr[2]}, {rr[3]})' if rr else '—'
    star = '\\*'
    cases = ' '.join(f'`{c}`{star if c in refids else ""}={st}' for c, st in ts) or '（全部移植用例）'
    if any(c in refids for c, _ in ts):
        nref.append(i)
    if va == vs and ta == ts:
        same = '同'
    elif va == vs and [(c, st.replace('[reference]', '')) for c, st in ts] == ta:
        same = '判定同；原因由 [reference] 认定'
    elif rr and rr[0] == va and rr[1] == ta:
        same = '首跑因负载不同，重跑同'
    else:
        same = '**不同**'
    rows.append(f'| {i} | {va} | {vs} | {bs} ({ls}) | {rerun} | {cases} | {same} |')
open(out + '/table.md', 'w', encoding='utf-8').write('\n'.join(rows) + '\n')
print(f'{len(rows) - 2} rows; differ: {[x.split(" | ")[0][2:] for x in rows[2:] if "**不同**" in x]}; [reference]: {[x.split(" | ")[0][2:] for x in rows[2:] if "[reference]" in x]}')
print(f'ids with a designated case of the gate-closed arm: {len(nref)}: {" ".join(nref)}')
print(f'first-run batch void: {void}')
