#!/usr/bin/env python3
"""apply_edits_v6.py -- build the proposal of the current revision from the previous one by anchored, asserting edits.

usage: python3 apply_edits_v6.py <previous proposal.md> <numbers.json | -> <out proposal.md>

Every edit asserts that its anchor occurs the expected number of times.  `@NAME@` placeholders are filled from numbers.json (produced by mk_numbers6.py from raw outputs, not typed by hand);
an unfilled placeholder stops the run.  Rule #7: no credential-shaped literal in this file."""
import json
import re
import sys

src_path, num_path, out_path = sys.argv[1:4]
t = open(src_path, encoding="utf-8").read()
NUM = json.load(open(num_path, encoding="utf-8")) if num_path != "-" else {}


FAILS = []


def sub1(old, new, count=1):
    global t
    n = t.count(old)
    if n != count:
        FAILS.append(f"anchor count {n} != {count}: {old[:140]!r}")
        return
    t = t.replace(old, new)


def after(anchor, add, count=1):
    sub1(anchor, anchor + add, count)


exec(open(__file__.replace("apply_edits_v6.py", "edits_v6_a.py"), encoding="utf-8").read())      # header, Why, W1, W2, W4
exec(open(__file__.replace("apply_edits_v6.py", "edits_v6_b.py"), encoding="utf-8").read())      # W8, W9, W10, W11, W14, Out of scope
exec(open(__file__.replace("apply_edits_v6.py", "edits_v6_c.py"), encoding="utf-8").read())      # Success Criteria
exec(open(__file__.replace("apply_edits_v6.py", "edits_v6_d.py"), encoding="utf-8").read())      # rule6_note, Impact, Tasks, open questions

if FAILS:
    print("ANCHOR FAILURES:", len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)

benign = set(re.findall(r"@[A-Za-z0-9_-]+@", open(src_path, encoding="utf-8").read()))      # tokens the previous text already holds (e.g. `p1 @f1 >/dev/null; ... @f2`): not placeholders
pending = []
for k in sorted(set(re.findall(r"@[A-Za-z0-9_-]+@", t)) - benign):
    key = k.strip("@")
    if key not in NUM:
        pending.append(key)
        continue
    t = t.replace(k, str(NUM[key]))
if pending:
    if num_path == "-":
        print("UNRESOLVED PLACEHOLDERS (list mode):", len(pending))
        print(" ".join(pending))
    else:
        print("UNRESOLVED PLACEHOLDERS:", len(pending))
        print(" ".join(pending))
        sys.exit(1)
open(out_path, "w", encoding="utf-8", newline="").write(t)
print("proposal written:", out_path, len(t.encode()), "bytes")
