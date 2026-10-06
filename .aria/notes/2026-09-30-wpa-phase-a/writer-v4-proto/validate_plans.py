#!/usr/bin/env python3
"""validate_plans.py PLAN.tsv ... -- apply every variant of every plan row to the baseline hook (output discarded): reports rows the v4 patch scripts reject."""
import os
import subprocess
import sys

EXP = "/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v4"
bad = 0
n = 0
for plan in sys.argv[1:]:
    for line in open(plan, encoding="utf-8"):
        f = line.rstrip("\n").split("\t")
        if len(f) < 4:
            continue
        label, kind, variant = f[0], f[1], f[2]
        n += 1
        if kind == "l3":
            cmd = ["python3", EXP + "/proto/patch_l3.py", EXP + "/base/aria/hooks/secret-scan.sh", "/dev/null", "--variant", variant]
        else:
            cmd = ["python3", EXP + "/proto/patch_l1.py", EXP + "/base/aria/hooks/secret-guard.sh", "/dev/null", "--variant", variant]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            bad += 1
            print("REJECTED", os.path.basename(plan), label, kind, variant, "::", (r.stderr.strip().splitlines() or ["?"])[-1][:140])
print("rows:", n, "rejected:", bad)
