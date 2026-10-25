import re, sys
diff_path, prop_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
P = open(prop_path, encoding='utf-8').read().split('\n')
def find(pat):
    for i, l in enumerate(P):
        if re.search(pat, l): return i
    sys.exit('anchor not found: ' + pat)
a1 = find(r'^\*\*What 1 补充：'); a12 = find(r'^\*\*What 1 补充 2：'); a2 = find(r'^### 2\. ')
a6 = find(r'^### 6\. '); a7 = find(r'^### 7\. '); a7s = find(r'^\*\*What 7 补充：'); a7s2 = find(r'^\*\*What 7 补充 2：'); aref = find(r'^### 参考实现')
secs = {'W1S': (a1, a12), 'W1S2': (a12, a2), 'W6': (a6, a7), 'W7S': (a7s, a7s2), 'W7S2': (a7s2, aref)}
text = {k: '\n'.join(P[s:e]) for k, (s, e) in secs.items()}
alltext = '\n'.join(P)
def where(c):
    w = [k for k, t in text.items() if c in t or c.replace('|', '\\|') in t]
    return w or ['ELSEWHERE' if (c in alltext or c.replace('|', '\\|') in alltext) else 'NONE']
hunks, cur = [], None
for ln in open(diff_path, encoding='utf-8'):
    ln = ln.rstrip('\n')
    if ln.startswith('@@'): cur = {'h': ln, 'l': []}; hunks.append(cur); continue
    if cur is None or ln.startswith('+++') or ln.startswith('---'): continue
    if ln[:1] in '+-': cur['l'].append((ln[0], ln[1:]))
summ, det = [], []
for i, h in enumerate(hunks, 1):
    cp, cm = set(), set(); nb = 0
    for sg, body in h['l']:
        c = body.strip()
        if not c: nb += 1; det.append('h%d %s blank' % (i, sg)); continue
        w = where(c); (cp if sg == '+' else cm).update(w); det.append('h%d %s %-16s %s' % (i, sg, ','.join(w), c[:90]))
    summ.append('hunk %d %s | +%d -%d (blank %d) | added found in: %s | removed found in: %s' % (i, h['h'], sum(s == '+' for s, _ in h['l']), sum(s == '-' for s, _ in h['l']), nb, ' '.join(sorted(cp)) or '-', ' '.join(sorted(cm)) or '-'))
open(out_path, 'w').write('\n'.join(summ) + '\n#### per line\n' + '\n'.join(det) + '\n')
print('\n'.join(summ))
