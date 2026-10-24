# classify_w8.py <proto> <impl> <diff -u proto impl> <proposal.md> : per-line classification of every hunk into the three INV-1 classes; prints <= 20 lines
import re, sys
proto, impl = [open(f).read().split("\n") for f in sys.argv[1:3]]
prop = open(sys.argv[4]).read().replace("\r", "").split("\n")
hunks, cur = [], None
for ln in open(sys.argv[3]).read().split("\n"):
    m = re.match(r"@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", ln)
    if m: cur = {"rem": [], "add": [], "p": int(m[1]), "i": int(m[2])}; hunks.append(cur); pl, il = cur["p"], cur["i"]; continue
    if cur is None or ln.startswith("\\"): continue
    if ln.startswith(" "): pl += 1; il += 1
    elif ln.startswith("-"): cur["rem"].append((pl, ln[1:])); pl += 1
    elif ln.startswith("+"): cur["add"].append((il, ln[1:])); il += 1
def sect(a, b):
    s = next(i for i, l in enumerate(prop) if l.startswith(a)); e = next(i for i in range(s + 1, len(prop)) if prop[i].startswith(b)); return s, e
def blocks(s, e):
    out, inb, c = [], False, []
    for l in prop[s:e]:
        if l.startswith("```"):
            if inb: out.append(c); c = []
            inb = not inb; continue
        if inb: c.append(l)
    return out
def find(lines, blk):
    hits = [i + 1 for i in range(len(lines) - len(blk) + 1) if lines[i:i + len(blk)] == blk]
    return hits
s1, e1 = sect("**What 1 补充", "### "); s7, e7 = sect("**What 7 补充", "### ")
B = {"W1S": blocks(s1, e1)[0]}
b7 = blocks(s7, e7); assert len(b7) == 4, len(b7)
for k in range(4): B[f"W7S-{k+1}"] = b7[k]
def fn(lines, name):
    s = next(i for i, l in enumerate(lines) if l.startswith(name + "() {")); e = next(i for i in range(s, len(lines)) if lines[i] == "}"); return (s + 1, e + 1)
PR = {"W1S": [fn(proto, "_sg_relax_ok"), fn(proto, "_sg_relax_platform")]}
items = [l for l in prop[s7:e7] if re.match(r"^[1-4]\. ", l)]; quotes = {}
for k, l in enumerate(items):
    a, b = map(int, re.search(r"原型 `:(\d+)-(\d+)`", l).groups()); PR[f"W7S-{k+1}"] = [(a, b)]; quotes[f"W7S-{k+1}"] = re.findall(r"「`(.+?)`」", l)
IR = {}
for k, blk in B.items():
    h = find(impl, blk); hp = find(proto, blk); IR[k] = (h[0], h[0] + len(blk) - 1) if len(h) == 1 else None
    print(f"block {k}: {len(blk)} lines, verbatim in impl at {h} (in proto: {hp})")
W6 = '[[ -z "${_SGV_V[j]}" ]] && continue'
print(f"What 6 line: proto {sum(l.strip() == W6 for l in proto)} impl {sum(l.strip() == W6 for l in impl)}; _sg_relax_ok defs impl {sum(l.startswith('_sg_relax_ok()') for l in impl)}, _sg_relax_platform defs impl {sum(l.startswith('_sg_relax_platform()') for l in impl)}")
other = 0; remq = {}
for n, h in enumerate(hunks, 1):
    cls = set()
    for (ln, t) in h["rem"]:
        c = "W6" if t.strip() == W6 else next((k for k, rs in PR.items() if any(a <= ln <= b for a, b in rs)), "OTHER"); cls.add("-" + c); remq.setdefault(c, []).append(t)
        other += c == "OTHER"
    for (ln, t) in h["add"]:
        c = next((k for k, r in IR.items() if r and r[0] <= ln <= r[1]), "OTHER"); cls.add("+" + c); other += c == "OTHER"
    pr = f"{h['rem'][0][0]}-{h['rem'][-1][0]}" if h["rem"] else "-"; ir = f"{h['add'][0][0]}-{h['add'][-1][0]}" if h["add"] else "-"
    print(f"H{n}: proto {pr} (-{len(h['rem'])}) impl {ir} (+{len(h['add'])}) classes {sorted(cls)}")
for k, q in quotes.items():
    if q: print(f"{k}: proposal quotes {len(q)} old line(s); equal to the removed lines: {q == [t[2:] if False else t for t in remq.get(k, [])]}")
print(f"OTHER lines: {other}; hunks {len(hunks)}; removed {sum(len(h['rem']) for h in hunks)} added {sum(len(h['add']) for h in hunks)}")
