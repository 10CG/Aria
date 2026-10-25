import sys, os, hashlib
man, cmds = sys.argv[1], sys.argv[2]
names = {os.path.splitext(f)[0]: os.path.join(cmds, f) for f in os.listdir(cmds)}
ok = miss = badlen = badsha = 0; bad = []
for ln in open(man):
    n, b, h = ln.rstrip('\n').split('\t')[:3]
    p = names.get(n)
    if p is None: miss += 1; bad.append(n); continue
    d = open(p, 'rb').read()
    if len(d) != int(b): badlen += 1; bad.append(n); continue
    if hashlib.sha256(d).hexdigest() != h: badsha += 1; bad.append(n); continue
    ok += 1
print("corpus: ok %d missing %d size-mismatch %d sha-mismatch %d | files in cmds %d | bad ids: %s" % (ok, miss, badlen, badsha, len(names), " ".join(bad[:20])))
