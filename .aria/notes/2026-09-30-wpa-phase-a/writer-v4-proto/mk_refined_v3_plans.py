#!/usr/bin/env python3
"""mk_refined_v3_plans.py -- regression plans for the bad implementations of the PREVIOUS round (v3), re-run on the v4 prototype.

For every v3 plan row (work/plans_v3/*.tsv) that has a block in the v3 summary (mut_summary_v3.txt; superseded first-pass blocks have none), write a plan row that runs
ONLY the rows that turned red in v3.  The regression criterion is then exact: every row that was red under that bad implementation in v3 must still be red under it on the
v4 prototype.  A bad implementation that turned no row red in v3 (an equivalent mutant) keeps its original SC list so that it is re-run in full.
Output: work/plans_v3r/<plan>.tsv  (same columns as plans/*.tsv)."""
import os
import re
import sys

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUMMARY = sys.argv[1] if len(sys.argv) > 1 else "/home/dev/Aria/.aria/notes/2026-09-30-wpa-phase-a/writer-v3-proto/mut_summary_v3.txt"
text = open(SUMMARY, encoding="utf-8").read()
blocks = {}                # (plan, label) -> list of red (sc, row)
cur_plan = None
for chunk in re.split(r"(?m)^(?=##### |== )", text):
    if chunk.startswith("##### "):
        cur_plan = chunk.split()[1]
    elif chunk.startswith("== ") and cur_plan:
        label = chunk[3:].split(" ", 1)[0]
        red = [(m.group(1), m.group(2)) for m in re.finditer(r"(?m)^   (SC-\d+) (\S+) \|", chunk)]
        blocks[(cur_plan, label)] = red
out = os.path.join(EXP, "work", "plans_v3r")
os.makedirs(out, exist_ok=True)
tot = kept = skipped = 0
for fn in sorted(os.listdir(os.path.join(EXP, "work", "plans_v3"))):
    plan = fn[:-4]
    rows_out = []
    for line in open(os.path.join(EXP, "work", "plans_v3", fn), encoding="utf-8"):
        f = line.rstrip("\n").split("\t")
        if len(f) < 4:
            continue
        tot += 1
        label, kind, variant, scs = f[0], f[1], f[2], f[3]
        orig_rows = f[4] if len(f) > 4 else ""
        key = (plan, label)
        if key not in blocks:
            skipped += 1                      # superseded first-pass block: its replacing run sits in another plan
            continue
        red = blocks[key]
        if red and any(r in ("32c", "32d", "29h", "29i") for _sc, r in red):
            rows_out.append((label, kind, variant, scs, orig_rows))      # a differential row compares the hook-direct rows that ran in the same process: keep the original SC list
        elif red:
            sc_list = ",".join(sorted({sc for sc, _r in red}, key=lambda s: int(s[3:])))
            row_list = ",".join(sorted({r for _sc, r in red}))
            rows_out.append((label, kind, variant, sc_list, row_list))
        else:
            rows_out.append((label, kind, variant, scs, orig_rows))
        kept += 1
    with open(os.path.join(out, fn), "w", encoding="utf-8") as fh:
        for r in rows_out:
            fh.write("\t".join(r) + "\n")
print("v3 plan rows:", tot, "| refined rows written:", kept, "| superseded (no block in the v3 summary):", skipped)
