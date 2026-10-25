import re, collections
vs = ['3.2.57', '5.0.18', '5.1.16', '5.2.15', '5.3.20']; rows = collections.OrderedDict()
for v in vs:
    for l in open('proofs/cmp-%s.txt' % v, encoding='utf-8'):
        m = re.match(r'(\S+)\s+hook=(\S+) \(want (\S+)\) stderr=(\S+) \| helper=(\S+) scdirect=(\S+) suite=(\S+) sccases=(\S+)\s+(\S+)', l)
        if m: rows.setdefault(m.group(1), []).append((v,) + m.groups()[1:])
out = ['| 情形 | 期望 hook | hook（3.2.57/5.0.18/5.1.16/5.2.15/5.3.20） | stderr 字节 | helper | sc-direct | suite | sc-cases | 判定 |', '|---|---|---|---|---|---|---|---|---|']
for k, r in rows.items():
    col = lambda i: '/'.join(x[i] for x in r)
    out.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (k, r[0][2], col(1), col(3), col(4), col(5), col(6), col(7), ','.join(sorted(set(x[8] for x in r)))))
open('criteria-table.md', 'w', encoding='utf-8').write('\n'.join(out) + '\n'); print(len(rows), 'rows;', sum(len(r) for r in rows.values()), 'cells')
