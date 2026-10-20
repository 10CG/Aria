#!/usr/bin/env python3
"""b1_curve.py HOOK [--lens 2,4,8,16,32] [--shapes A,B,C,D,E,F,S] [--kinds secret,benign] [--reps N] [--timeout S] [--bash BIN]

B.1 baseline for secret-guard-scan-cost-and-firstpass-cap (TASK-001): whole-process cost of the built-in FIRST pass
on ONE segment (no top-level ; && || or newline) of about L KB, per padding shape.
  kind=secret : the head is a credential-file read, so a risky pattern hits and _sg_compute_credit runs on the segment
  kind=benign : same shape and length, no credential-shaped token, so compute_credit is never reached (for-pat loop only)
  floor       : a trivial command (process start + jq + loop over a tiny string)
Padding shapes (appended to the head, the whole string stays one segment):
  A one long path token   B many short words   C a long `| cat` pipeline   D pipes inside one quoted grep -F argument
  E a jq program full of pipes (targets the jq credit regex)   F runs of 400 random alnum bytes (a W10-substitution-like copy)
Per run: CPU = user+sys of the hook process tree (RUSAGE_CHILDREN delta), wall = perf_counter; the exit code is kept as
liveness (secret must be 2, benign must be 0, floor must be 0). Statistic = MIN over N interleaved runs.
The credential path is assembled at run time; nothing is printed except labels and numbers (the hook's output is discarded).
"""
import json
import os
import random
import resource
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from b1_shapes import build  # noqa: E402  (the single source of the padding shapes)

hook = os.path.abspath(sys.argv[1])   # absolute: the hook runs with cwd=home (a relative path there is rc 127)


def opt(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


lens = [int(x) for x in opt("--lens", "2,4,8,16,32").split(",")]
shapes = opt("--shapes", "A,B,C,D,E,F").split(",")
kinds = opt("--kinds", "secret,benign").split(",")
reps = int(opt("--reps", "3"))
tmo = float(opt("--timeout", "40"))
bash = opt("--bash", "bash")                          # e.g. the bash-3.2.57 binary

home = tempfile.mkdtemp(prefix="b1-")
ENV = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": home, "TMPDIR": home, "USER": "probe",
       "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
def run_once(cmd):
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}}).encode()
    r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    t0 = time.perf_counter()
    try:
        p = subprocess.run([bash, hook], input=payload, env=ENV, cwd=home,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=tmo)
        rc = p.returncode
    except subprocess.TimeoutExpired:
        rc = "TMO"
    wall = time.perf_counter() - t0
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    cpu = (r1.ru_utime - r0.ru_utime) + (r1.ru_stime - r0.ru_stime)
    return cpu, wall, rc


configs = [("floor", "-", 0)]
for kind in kinds:
    for shape in shapes:
        for kb in lens:
            configs.append((kind, shape, kb))

res = {c: [] for c in configs}
for _ in range(reps):
    order = configs[:]
    random.shuffle(order)                      # interleave: spread host-load noise across configs
    for c in order:
        cmd = build(*c)
        cpu, wall, rc = run_once(cmd)
        res[c].append((cpu, wall, rc, len(cmd)))

print("kind\tshape\tKB\tbytes\tcpu_min_s\twall_min_s\texit_codes\tliveness")
for c in configs:
    rows = res[c]
    kind = c[0]
    want = 2 if kind == "secret" else 0
    rcs = sorted({str(r[2]) for r in rows})
    live = "ok" if all(r[2] == want for r in rows) else ("TIMEOUT" if any(r[2] == "TMO" for r in rows) else "FAIL")
    print("%s\t%s\t%s\t%d\t%.3f\t%.3f\t%s\t%s" % (kind, c[1], c[2], rows[0][3],
                                                 min(r[0] for r in rows), min(r[1] for r in rows), ",".join(rcs), live))
