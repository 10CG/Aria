# w9diff.py <new W9> <old W9>: for each impl entry that differs from the prototype round, show the differing check lines (old vs new), cut to 230 chars
import re, sys, difflib
def ent(f):
    out, sec, cur = [], None, None
    for l in open(f).read().split("\n"):
        if l.startswith("## "): sec = l[3:].strip(); continue
        if sec != "impl": continue
        if l.startswith("  FAIL "): cur = [l[7:], []]; out.append(cur)
        elif l.startswith("     ") and cur: cur[1].append(l.strip())
    return out
n, o = ent(sys.argv[1]), ent(sys.argv[2])
print("impl entry names identical and in the same order:", [a for a, _ in n] == [a for a, _ in o])
for (na, nc), (oa, oc) in zip(n, o):
    if (na, nc) != (oa, oc):
        print("ENTRY:", na[:110], "| checks old", len(oc), "new", len(nc))
        for d in difflib.unified_diff(oc, nc, "old", "new", n=0, lineterm=""):
            if not d.startswith(("---", "+++")): print("  ", d[:230])
