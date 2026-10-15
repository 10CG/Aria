#!/usr/bin/env python3
"""sc_counts.py OUT [OUT ...] -- per SC and category: row count and `yes` count, parsed from probe stdout files (rows are keyed by SC / case id; later files win)"""
import re
import sys
from collections import OrderedDict

rows = OrderedDict()
for path in sys.argv[1:]:
    for l in open(path, encoding="utf-8"):
        m = re.match(r"^(SC-\d+) │ (\S+) │ (\S+) │ .* │ (yes|no|n/a)$", l.rstrip("\n"))
        if m:
            rows[(m.group(1), m.group(2))] = (m.group(3), m.group(4))
per = OrderedDict()
for (sc, cid), (cat, ok) in rows.items():
    d = per.setdefault(sc, OrderedDict())
    t = d.setdefault(cat, [0, 0])
    t[1] += 1
    t[0] += (ok == "yes")
for sc in sorted(per, key=lambda s: int(s.split("-")[1])):
    parts = ", ".join(f"{cat} {y}/{n}" for cat, (y, n) in per[sc].items())
    print(f"{sc}: {parts}")
print("total rows:", len(rows))
cat_tot = {}
for (sc, cid), (cat, ok) in rows.items():
    cat_tot[cat] = cat_tot.get(cat, 0) + 1
print(cat_tot)
