#!/usr/bin/env python3
"""coverage_check.py V3_STDOUT V4_BASELINE_STDOUT -- every probe row that is NEW or REWRITTEN since v3 (any column but the match flag differs from the v3 baseline output) must be
turned red by at least one bad implementation: a block of this round's mutation plans (mut/final/plan_v4_*/SUMMARY.txt) or of the regression run of the previous round's bad implementations (mut/final/v3r_*/SUMMARY.txt) or one of the manual runs listed in MANUAL below (their
results are in work/archive/manual_runs.txt).  Prints the uncovered rows.  Exit 1 if any is uncovered."""
import collections
import os
import re
import sys

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rows(path):
    d = collections.OrderedDict()
    for l in open(path, encoding="utf-8"):
        m = re.match(r"^(SC-\d+) │ (\S+) │ (\S+) │ (.*) │ (.*) │ (.*) │ (yes|no|n/a)$", l.rstrip("\n"))
        if m:
            d[(m.group(1), m.group(2))] = (m.group(3), m.group(4), m.group(5), m.group(6))
    return d


old, new = rows(sys.argv[1]), rows(sys.argv[2])
touched = [k for k in new if k not in old or old[k] != new[k]]
# manual runs (work/run_manual_runs.py -> work/archive/manual_runs.txt): the documentation bad implementations (patch_docs.py flags), the secret-scan suite without the self-check
# assertion, the SC-33 census with the entropy floor removed, and the SC-15 negative control
MANUAL = {
    "doc bad implementations (--hdr-half-a / --hdr-argon / --hdr-topcontent / --hdr-count / --hdr-half-l / --hdr-dangling / --hdr-nohist; --bad for 28k)": {"28a", "28b", "28c", "28d", "28e", "28f", "28j", "28k", "28l"},
    "no-selfcheck suite": {"27d"}, "noentropy on a full tree (SC-33)": {"33a"}, "SC-15 negative control (nc15.py)": {"15g"},
}
manual = {r for v in MANUAL.values() for r in v}
red = collections.defaultdict(set)
base = os.path.join(EXP, "mut", "final")
for plan in sorted(os.listdir(base)):
    f = os.path.join(base, plan, "SUMMARY.txt")
    if not plan.startswith(("plan_v4_", "v3r_")) or not os.path.isfile(f):
        continue
    for b in re.split(r"(?m)^== ", open(f, encoding="utf-8").read())[1:]:
        label = b.split("\n", 1)[0].split(" ", 1)[0]
        for l in b.split("\n")[1:]:
            m = re.match(r"^   (SC-\d+) (\S+) \|", l)
            if m:
                red[(m.group(1), m.group(2))].add(plan + "/" + label)
unc = [k for k in touched if k not in red and k[1] not in manual]
print("rows new or rewritten since v3:", len(touched), "| red under >=1 plan bad implementation:", sum(1 for k in touched if k in red),
      "| covered only by a manual run:", sum(1 for k in touched if k not in red and k[1] in manual), "| uncovered:", len(unc))
for k in touched:
    who = sorted(red.get(k, ()))
    tag = ("%d plan bad impl(s), e.g. %s" % (len(who), who[0])) if who else ("manual run" if k[1] in manual else "UNCOVERED")
    print("  %-6s %-5s %-16s %s" % (k[0], k[1], new[k][0], tag))
for k in unc:
    print("  UNCOVERED", k[0], k[1], new[k][0], "|", new[k][1][:100])
sys.exit(1 if unc else 0)
