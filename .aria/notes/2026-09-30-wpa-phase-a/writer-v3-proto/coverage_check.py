#!/usr/bin/env python3
"""coverage_check.py FINAL_A_STDOUT -- every probe row that is NEW or REWRITTEN since v2 (v2/baseline-evidence.md) must be turned red by at least one bad implementation:
a block of a mutation plan (superseded first-pass blocks excluded, see work/equiv_reasons.py) or one of the manual runs listed in MANUAL below.  Prints the uncovered rows."""
import collections
import os
import re
import sys

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(EXP, "work"))
SUPERSEDED = {}
exec(open(os.path.join(EXP, "work", "equiv_reasons.py"), encoding="utf-8").read())


def rows(path, only_block=False):
    d = collections.OrderedDict()
    for l in open(path, encoding="utf-8"):
        m = re.match(r"^(SC-\d+) │ (\S+) │ (\S+) │ (.*) │ (.*) │ (.*) │ (yes|no|n/a)$", l.rstrip("\n"))
        if m:
            d[(m.group(1), m.group(2))] = (m.group(3), m.group(4), m.group(5))
    return d


old, new = rows(os.path.join(EXP, "v2", "baseline-evidence.md")), rows(sys.argv[1])
touched = [k for k in new if k not in old or old[k] != new[k]]
# manual runs (see work/archive/manual_runs.txt)
MANUAL = {
    "bad-sot / bad docs": {"26a", "26b", "26c", "26d", "26e", "26f", "26g", "26j", "26k", "28h", "28m"},
    "bad-layer docs": {"26i"}, "no-scope docs": {"28n"}, "no-selfcheck suite": {"27d"},
    "noentropy on a full tree (SC-33)": {"33a"}, "SC-15 negative control (nc15.py)": {"15g"},
}
manual = {r for v in MANUAL.values() for r in v}


def lookup(label, plan):
    for key in (plan + "/" + label, label):
        if key in SUPERSEDED:
            return True
    return any(k.endswith("*") and (plan + "/" + label).startswith(k[:-1]) for k in SUPERSEDED)


red = collections.defaultdict(set)
for plan in sorted(os.listdir(os.path.join(EXP, "mut"))):
    f = os.path.join(EXP, "mut", plan, "SUMMARY.txt")
    if not os.path.isfile(f):
        continue
    for b in re.split(r"(?m)^== ", open(f, encoding="utf-8").read())[1:]:
        label = b.split("\n", 1)[0].split(" ", 1)[0]
        if lookup(label, plan):
            continue
        for l in b.split("\n")[1:]:
            m = re.match(r"^   (SC-\d+) (\S+) \|", l)
            if m:
                red[(m.group(1), m.group(2))].add(plan + "/" + label)
unc = [k for k in touched if k not in red and k[1] not in manual]
print("rows new or rewritten since v2:", len(touched), "| red under >=1 plan bad implementation:", sum(1 for k in touched if k in red),
      "| covered only by a manual run:", sum(1 for k in touched if k not in red and k[1] in manual), "| uncovered:", len(unc))
for k in unc:
    print("  UNCOVERED", k[0], k[1], new[k][0], "|", new[k][1][:100])
