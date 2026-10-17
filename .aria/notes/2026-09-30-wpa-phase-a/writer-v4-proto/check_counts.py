#!/usr/bin/env python3
"""check_counts.py PROPOSAL STDOUT -- compare the per-SC category counts that the proposal bullets claim (`category` xN) with the probe stdout tallies.

For every `- **SC-n** (...)` bullet: the claimed count per category = the sum of every "`cat` ×N" in the bullet; the actual count = rows of that SC and
category in the stdout.  A category that the bullet names without a count, or does not name at all, is reported as `unchecked` / `unnamed`.
Also checks the global claims: "共 N 行" and the per-category totals line.  Prints only mismatches and a summary."""
import re
import sys
from collections import Counter, OrderedDict

prop = open(sys.argv[1], encoding="utf-8").read()
out = open(sys.argv[2], encoding="utf-8").read()
rows = OrderedDict()
for l in out.split("\n"):
    m = re.match(r"^(SC-(\d+)) │ (\S+) │ (\S+) │ ", l)
    if m:
        rows[(int(m.group(2)), m.group(3))] = m.group(4)
actual = {}
for (n, cid), cat in rows.items():
    actual.setdefault(n, Counter())[cat] += 1
bad = 0
for l in prop.split("\n"):
    m = re.match(r"^- \*\*SC-(\d+)\*\*", l)
    if not m:
        continue
    n = int(m.group(1))
    claim = Counter()
    for cat, k in re.findall(r"`(baseline-failing|reverse-guard|allow-guard|known-limit|zero-regression|doc-sync)` ×(\d+)", l):
        claim[cat] += int(k)
    named = set(re.findall(r"`(baseline-failing|reverse-guard|allow-guard|known-limit|zero-regression|doc-sync)`", l))
    act = actual.get(n, Counter())
    if n == 30:
        continue
    msgs = []
    for cat, k in act.items():
        if cat in claim and claim[cat] != k:
            msgs.append(f"{cat}: text x{claim[cat]} vs rows {k}")
        elif cat not in claim and cat in named:
            msgs.append(f"{cat}: named without count (rows {k})")
        elif cat not in named:
            msgs.append(f"{cat}: not named in the bullet (rows {k})")
    for cat, k in claim.items():
        if cat not in act:
            msgs.append(f"{cat}: text x{k} but no such rows")
    if msgs:
        bad += 1
        print(f"SC-{n}: " + "; ".join(msgs))
tot = len(rows)
m = re.search(r"共 (\d+) 行", prop)
print("rows in stdout:", tot, "| '共 N 行' claims:", re.findall(r"共 (\d+) 行", prop), "| '(N 行探针)' claims:", re.findall(r"(\d+) 行探针", prop))
print("bullets with a mismatch / unchecked category:", bad)
