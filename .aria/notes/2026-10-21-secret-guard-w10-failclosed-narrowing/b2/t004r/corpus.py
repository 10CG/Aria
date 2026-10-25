# corpus.py MANIFEST CMDS : bytes + sha256 of every manifest row vs CMDS/<n>.txt; prints counts and ids only, never text
import sys, os, hashlib
man, cmds = sys.argv[1], sys.argv[2]
c = {'ok': 0, 'missing': 0, 'size': 0, 'sha': 0}; bad = []; names = set()
for ln in open(man, encoding='utf-8'):
    p = ln.rstrip('\n').split('\t')
    if len(p) < 3: continue
    n, size, sha = p[0], p[1], p[2]; names.add(n + '.txt'); f = os.path.join(cmds, n + '.txt')
    if not os.path.isfile(f): c['missing'] += 1; bad.append(n); continue
    b = open(f, 'rb').read()
    if len(b) != int(size): c['size'] += 1; bad.append(n); continue
    if hashlib.sha256(b).hexdigest() != sha: c['sha'] += 1; bad.append(n); continue
    c['ok'] += 1
extra = len(set(os.listdir(cmds)) - names)
print('corpus rows %d ok %d missing %d size-mismatch %d sha-mismatch %d extra-files %d bad: %s' % (sum(c.values()), c['ok'], c['missing'], c['size'], c['sha'], extra, ' '.join(bad[:20])))
sys.exit(0 if c['ok'] == sum(c.values()) else 1)
