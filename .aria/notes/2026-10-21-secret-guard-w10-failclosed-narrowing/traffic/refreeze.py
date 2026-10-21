# refreeze.py <manifest.tsv> <fresh TRAFFIC_DIR> <out dir> -- copy each frozen command found in a fresh extraction to <out dir>/cmds/<frozen n>.txt, matched by sha256
# Prints counts only (found / missing), never text; missing ones are listed by n, and a replay must report them as not judged
import hashlib, pathlib, sys
man, fresh, out = sys.argv[1], pathlib.Path(sys.argv[2]) / "cmds", pathlib.Path(sys.argv[3]) / "cmds"
want = {}
for line in open(man, encoding="utf-8"):
    n, ln, h = line.rstrip("\n").split("\t"); want[h] = int(n)
out.mkdir(parents=True, exist_ok=True); found = set()
for p in fresh.glob("*.txt"):
    b = p.read_bytes(); h = hashlib.sha256(b).hexdigest()
    if h in want and want[h] not in found:
        (out / f"{want[h]}.txt").write_bytes(b); found.add(want[h])
missing = sorted(set(want.values()) - found)
print(f"frozen={len(want)} found={len(found)} missing={len(missing)}" + (f" missing_n={','.join(map(str, missing[:50]))}" if missing else ""))
