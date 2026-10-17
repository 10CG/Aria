#!/usr/bin/env python3
"""regress_compare.py -- compare the v3 regression run (mut/final/v3r_<plan>/SUMMARY.txt, v4 prototype) with the v3 summary (mut_summary_v3.txt).

For every bad implementation of the previous round: the set of rows that were red in v3 must still be red now (a superset is fine).  Prints one line per regression
(label, rows that stopped turning red) and a tally per plan.  Exit 1 if there is any regression or any block is missing / errored."""
import os
import re
import sys

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V3 = sys.argv[1] if len(sys.argv) > 1 else "/home/dev/Aria/.aria/notes/2026-09-30-wpa-phase-a/writer-v3-proto/mut_summary_v3.txt"


def parse(text, with_plan):
    out, plan = {}, None
    for chunk in re.split(r"(?m)^(?=##### |== )", text):
        if chunk.startswith("##### "):
            plan = chunk.split()[1]
        elif chunk.startswith("== "):
            label = chunk[3:].split(" ", 1)[0]
            red = {(m.group(1), m.group(2)) for m in re.finditer(r"(?m)^   (SC-\d+) (\S+) \|", chunk)}
            err = "PATCH-FAILED" in chunk or "PROBE-ERROR" in chunk
            out[(plan if with_plan else None, label)] = (red, err)
    return out


v3 = parse(open(V3, encoding="utf-8").read(), True)
bad = 0
tally = {}
for d in sorted(os.listdir(os.path.join(EXP, "mut", "final"))):
    if not d.startswith("v3r_") or not os.path.isfile(os.path.join(EXP, "mut", "final", d, "SUMMARY.txt")):
        continue
    plan = d[4:]
    now = parse(open(os.path.join(EXP, "mut", "final", d, "SUMMARY.txt"), encoding="utf-8").read(), False)
    t = tally.setdefault(plan, [0, 0, 0, 0, 0])     # run, preserved, regressions, zero-red (as in v3), errors
    for (_p, label), (red_now, err) in now.items():
        t[0] += 1
        old = v3.get((plan, label))
        if old is None:
            print("NO v3 BLOCK:", plan, label)
            bad += 1
            continue
        if err:
            t[4] += 1
            bad += 1
            print("ERROR RESULT:", plan, label)
            continue
        if not old[0]:
            t[3] += 1                                  # equivalent mutant in v3, still no row red (or newly red: fine either way)
            continue
        missing = old[0] - red_now
        if missing:
            t[2] += 1
            bad += 1
            print("REGRESSION:", plan, label, "stopped turning red:", sorted(missing))
        else:
            t[1] += 1
print("%-18s %5s %9s %11s %12s %6s" % ("plan", "run", "preserved", "regressions", "zero-red(v3)", "errors"))
for p, t in tally.items():
    print("%-18s %5d %9d %11d %12d %6d" % ((p,) + tuple(t)))
print("TOTAL run %d | preserved %d | regressions %d | zero-red in v3 and now %d | errors %d" % tuple(sum(t[i] for t in tally.values()) for i in range(5)))
sys.exit(1 if bad else 0)
