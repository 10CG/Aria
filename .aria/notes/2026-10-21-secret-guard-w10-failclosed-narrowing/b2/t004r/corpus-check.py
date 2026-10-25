import sys, hashlib, pathlib
man, td = sys.argv[1], pathlib.Path(sys.argv[2]) / "cmds"
ok = miss = bad = 0; badn = []
for line in open(man, encoding="utf-8"):
    f = line.rstrip("\n").split("\t")
    if len(f) < 3 or not f[0].isdigit(): continue
    p = td / (f[0] + ".txt")
    if not p.exists(): miss += 1; badn.append(f[0]); continue
    b = p.read_bytes()
    if len(b) == int(f[1]) and hashlib.sha256(b).hexdigest() == f[2]: ok += 1
    else: bad += 1; badn.append(f[0])
extra = len(list(td.glob("*.txt")))
print("corpus: ok %d missing %d mismatch %d | files in cmds %d | bad ids %s" % (ok, miss, bad, extra, " ".join(badn[:20])))
