# corpus_check.py <manifest.tsv> <frozen TRAFFIC_DIR> name,path,col ... : counts and ids only, never command text
import sys, hashlib, pathlib
man, frozen = sys.argv[1], pathlib.Path(sys.argv[2]) / "cmds"
m = {}
for ln in open(man):
    p = ln.rstrip("\n").split("\t")
    if len(p) >= 3 and p[0].isdigit(): m[int(p[0])] = (int(p[1]), p[2])
def check(ids):
    ok, miss, bad = [], [], []
    for n in ids:
        f = frozen / f"{n}.txt"
        if not f.exists(): miss.append(n); continue
        b = f.read_bytes()
        if n not in m or len(b) != m[n][0] or hashlib.sha256(b).hexdigest() != m[n][1]: bad.append(n)
        else: ok.append(n)
    return ok, miss, bad
ok, miss, bad = check(sorted(m))
print(f"manifest: entries {len(m)} found+hash-ok {len(ok)} missing {len(miss)} hash-mismatch {len(bad)} files-in-frozen {len(list(frozen.glob('*.txt')))}")
for spec in sys.argv[3:]:
    name, path, col = spec.split(",")
    ids = [int(p[int(col)]) for p in (l.rstrip("\n").split("\t") for l in open(path)) if len(p) > int(col) and p[int(col)].strip().isdigit()]
    ok, miss, bad = check(ids)
    print(f"{name}: listed {len(ids)} unique {len(set(ids))} found+hash-ok {len(ok)} missing {len(miss)} ids={miss[:60]} hash-mismatch {len(bad)} ids={bad[:60]}")
