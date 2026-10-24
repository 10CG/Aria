# compare.py <new W9> <old W9> <new W11> <old W11> <W11 table out> : the acceptance 3 and 4 comparisons; prints only judgment lines
import re, sys
def w9(f):
    secs, cur, ent = {}, None, None
    for l in open(f).read().split("\n"):
        if l.startswith("## "): cur = secs.setdefault(l[3:].strip(), {"counts": [], "ent": []}); continue
        if cur is None or l.startswith("#"): continue
        if re.match(r"^(PASS|FAIL): ", l): cur["counts"].append(l)
        elif l.startswith("  FAIL "): ent = [l[7:], []]; cur["ent"].append(ent)
        elif l.startswith("     ") and ent is not None: ent[1].append(l.strip())
    return {k: {"counts": v["counts"], "ent": [(n, tuple(c)) for n, c in v["ent"]]} for k, v in secs.items()}
nw, ow = w9(sys.argv[1]), w9(sys.argv[2])
grp = lambda n: (re.search(r"SC-(\d+[a-z]*)", n) or re.search(r"(\S+)", n)).group(1)
print("W9 sections new", sorted(nw), "old", sorted(ow))
for s in ("base", "impl"):
    print(f"W9 {s}: new == old (prototype round): counts {nw[s]['counts'] == ow[s]['counts']} entries {nw[s]['ent'] == ow[s]['ent']} | new {' / '.join(nw[s]['counts'])}")
def changes(w):
    b, i = set(w["base"]["ent"]), set(w["impl"]["ent"])
    return sorted({grp(n) for n, _ in i ^ b}), [e for e in w["impl"]["ent"] if e not in b], [e for e in w["base"]["ent"] if e not in i]
for tag, w in (("new", nw), ("old", ow)):
    g, onlyi, onlyb = changes(w); print(f"W9 {tag}: impl vs base changed groups {g}; entries only in impl {len(onlyi)}, only in base {len(onlyb)}")
g, onlyi, onlyb = changes(nw); oi = set(ow["impl"]["ent"])
print(f"W9 every changed entry (name + checks) equal to the prototype round: {sum(e in oi for e in onlyi)}/{len(onlyi)}")
sc13 = {f"{t}-{s}": [e for e in w[s]["ent"] if "SC-13" in e[0]] for t, w in (("new", nw), ("old", ow)) for s in ("base", "impl")}
print("W9 SC-13 entries:", {k: len(v) for k, v in sc13.items()}, "| all four identical:", len({repr(v) for v in sc13.values()}) == 1)
def w11(f):
    d, part, sec = {}, 1, None
    for l in open(f).read().split("\n"):
        if l.startswith("# extension project"): part = 2; continue
        if l.startswith("## "): sec = l[3:].strip(); continue
        m = re.match(r"^(\S+)\s+rc=(\d+)\s+wall=\s*([\d.]+)s\s+(.*)$", l)
        if m and sec: d[(part, sec, m[1])] = (m[2], m[4].rstrip(), m[3])
    return d
n11, o11 = w11(sys.argv[3]), w11(sys.argv[4]); bad = 0
with open(sys.argv[5], "w") as out:
    for k in sorted(set(n11) | set(o11)):
        a, b = o11.get(k), n11.get(k); same = bool(a and b and a[:2] == b[:2]); bad += not same
        out.write(f"{'main' if k[0] == 1 else 'ext'}\t{k[1]}\t{k[2]}\told rc={a[0] if a else '-'} {a[1] if a else '-'} wall={a[2] if a else '-'}\tnew rc={b[0] if b else '-'} {b[1] if b else '-'} wall={b[2] if b else '-'}\t{'same' if same else 'DIFF'}\n")
print(f"W11 shapes: old {len(o11)} new {len(n11)}; rc+kind differ: {bad}")
