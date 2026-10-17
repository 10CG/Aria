#!/usr/bin/env python3
"""member_matrix.py [--jobs N] [--cap N] VARIANT [VARIANT ...] -- which member of the probe's SC-34 lists (LIN_BASE 9 + LIN_NEW 14) each bad L3 implementation fails.
For `target` the final prototype's hook is used; for any other name patch_l3.py builds the variant from the baseline hook and the rest of the tree is the final prototype's.
Every member runs once under `ulimit -t CAP` (default 4, the probe's cap) through the probe's own machinery; the output is one line per variant: `name: <members that are NOT detected>`.
Rule #7: this file holds no credential-shaped literal (the probe builds its values at run time)."""
import concurrent.futures as cf
import contextlib
import io
import os
import shutil
import subprocess
import sys
import threading

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[1:]
jobs, cap = 3, 4
if "--jobs" in args:
    i = args.index("--jobs")
    jobs = int(args[i + 1])
    del args[i:i + 2]
if "--cap" in args:
    i = args.index("--cap")
    cap = int(args[i + 1])
    del args[i:i + 2]
variants = args
probe = os.path.join(EXP, "spec", "baseline_probe.py")
src = open(probe, encoding="utf-8").read()
cut = src.index('row("SC-34", "34a"')


def build(variant):
    root = os.path.join(EXP, "work", "capv", variant)
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root + "/aria")
    shutil.copytree(EXP + "/work/t6/aria/hooks", root + "/aria/hooks")
    if variant != "target":
        r = subprocess.run(["python3", EXP + "/proto/patch_l3.py", EXP + "/base/aria/hooks/secret-scan.sh", root + "/aria/hooks/secret-scan.sh", "--variant", variant], capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
    return root + "/aria"


LOCK = threading.Lock()


def one(variant):
    aria = build(variant)
    g = {"__name__": "probe_prefix", "__file__": probe}
    with LOCK:                                   # sys.argv and sys.stdout are process-wide: the exec of the probe prefix is serialised
        sys.argv = [probe, aria]
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src[:cut], probe, "exec"), g)
    bad = []
    for name in ("LIN_BASE", "LIN_NEW"):
        for label, builder, want in g[name]:
            r = g["run_scan"](g["envelope"](g["BR"], builder()), cpu=cap)
            if not g["_scan_ok"](r, want):
                bad.append(label)
    return variant, bad


with cf.ThreadPoolExecutor(max_workers=jobs) as ex:
    for variant, bad in ex.map(one, variants):
        print(f"{variant}: {len(bad)} not detected under {cap} s: {', '.join(bad) if bad else '-'}", flush=True)
