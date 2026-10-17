#!/usr/bin/env python3
"""apply_edits.py V4_PROPOSAL OUT [--numbers numbers.json] [--allow-unresolved]

Builds the v5 proposal from the v4 text by applying every edit script in proposal_edits/ (part1 ... part6, in file-name order).
An edit is ("sub", old, new, count) = replace an exact substring that must occur exactly `count` times, ("line", prefix, new, 1) = replace the whole line that starts with
`prefix` (exactly one such line), ("after", prefix, new, 1) = insert `new` as extra line(s) after the one line that starts with `prefix`.  A part-1 style 3-tuple is a "sub".
Every anchor must match: a missing / ambiguous anchor stops the script.  Placeholders @NAME@ are filled from numbers.json; unresolved ones are an error unless --allow-unresolved."""
import glob
import json
import os
import re
import sys

src_path, out_path = sys.argv[1], sys.argv[2]
numbers = {}
if "--numbers" in sys.argv:
    numbers = json.load(open(sys.argv[sys.argv.index("--numbers") + 1], encoding="utf-8"))
allow = "--allow-unresolved" in sys.argv
here = os.path.dirname(os.path.abspath(__file__))
text = open(src_path, encoding="utf-8").read()
n_edits = 0
for part in sorted(glob.glob(os.path.join(here, "proposal_edits", "part*.py"))):
    ns = {"__file__": part}
    exec(compile(open(part, encoding="utf-8").read(), part, "exec"), ns)
    for i, e in enumerate(ns["EDITS"]):
        if e is None:
            continue
        if len(e) == 3:
            e = ("sub",) + tuple(e)
        kind = e[0]
        tag = f"{os.path.basename(part)}#{i}"
        if kind == "sub":
            _k, old, new, count = e
            n = text.count(old)
            if n != count:
                sys.exit(f"{tag}: anchor occurs {n} times, expected {count}: {old[:100]!r}")
            text = text.replace(old, new)
        elif kind in ("line", "after"):
            _k, prefix, new, _c = e
            lines = text.split("\n")
            idx = [j for j, l in enumerate(lines) if l.startswith(prefix)]
            if len(idx) != 1:
                sys.exit(f"{tag}: {len(idx)} lines start with {prefix[:80]!r}")
            j = idx[0]
            if kind == "line":
                lines[j] = new
            else:
                lines[j + 1:j + 1] = new.split("\n")
            text = "\n".join(lines)
        else:
            sys.exit(f"{tag}: unknown edit kind {kind!r}")
        n_edits += 1


def fill(m):
    k = m.group(1)
    return str(numbers[k]) if k in numbers else m.group(0)


text = re.sub(r"@([A-Z0-9_]+)@", fill, text)
left = sorted(set(re.findall(r"@[A-Z0-9_]+@", text)))
if left and not allow:
    sys.exit("unresolved placeholders: " + " ".join(left))
open(out_path, "w", encoding="utf-8", newline="\n").write(text)
print(f"applied {n_edits} edits; unresolved placeholders: {' '.join(left) if left else 'none'}; wrote {out_path} ({len(text.encode('utf-8'))} bytes)")
