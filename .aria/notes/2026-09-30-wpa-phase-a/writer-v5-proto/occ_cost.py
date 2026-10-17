#!/usr/bin/env python3
"""occ_cost.py BASE_GUARD TARGET_GUARD [BAD_GUARD ...] [--sizes 2000,8000] [--pairs N] [--cpu-cap S]

CPU cost of the extension's hit path as a function of the command length: a command of about SIZE bytes (a padding word run, then the listed path 64 times, the last one behind
`cat`; no separator character in the padding) through the baseline guard (no extension in the baseline), the target guard and any number of bad-implementation guards, each in a
private project with a one-entry `.aria/secret-guard.paths`.  Prints the minimum over --pairs interleaved runs of the total CPU time (user + sys of the hook and all its children)
and the ratio to the baseline hook on the same command.  A run killed by --cpu-cap prints `>cap`.  Numbers only."""
import json
import os
import resource
import subprocess
import sys
import tempfile
import time

args = [a for a in sys.argv[1:] if not a.startswith("--")]


def opt(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


skip = {opt(n, "") for n in ("--sizes", "--pairs", "--cpu-cap")} - {""}
args = [a for a in args if a not in skip]
base, tgt, bads = args[0], args[1], args[2:]
sizes = [int(x) for x in opt("--sizes", "2000,8000").split(",")]
pairs = int(opt("--pairs", "3"))
cap = int(opt("--cpu-cap", "300"))
P = "/srv/billing/conf/prod.toml"
root = tempfile.mkdtemp(prefix="occ-")
os.makedirs(os.path.join(root, "proj", ".aria"))
open(os.path.join(root, "proj", ".aria", "secret-guard.paths"), "w").write(P + "\n")
home = os.path.join(root, "home")
os.makedirs(home)
ENV = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": home, "TMPDIR": home, "USER": "probe", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
       "CLAUDE_PROJECT_DIR": os.path.join(root, "proj")}


def cmd_of(size):
    occ = " ".join([P] * 63)
    pad = "padding-text " * max(1, (size - len(occ) - 20) // 13)
    return "echo " + pad + occ + "; cat " + P


def run(hook, command):
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}}).encode()
    wrapper = 'ulimit -t "$0"; "$@" >/dev/null 2>&1; rc=$?; times >&2; exit $rc'
    t0 = time.time()
    p = subprocess.run(["sh", "-c", wrapper, str(cap), "bash", hook], input=payload, capture_output=True, env=ENV, timeout=cap * 4)
    wall = time.time() - t0
    import re
    ms = re.findall(r"(\d+)m([0-9.]+)s\s+(\d+)m([0-9.]+)s", p.stderr.decode("utf-8", "replace"))
    cpu = (int(ms[-1][0]) * 60 + float(ms[-1][1]) + int(ms[-1][2]) * 60 + float(ms[-1][3])) if ms else float("inf")
    return cpu, p.returncode, wall


hooks = [("baseline", base), ("target", tgt)] + [(os.path.basename(os.path.dirname(b)) or f"bad{i}", b) for i, b in enumerate(bads)]
for size in sizes:
    command = cmd_of(size)
    best = {name: (float("inf"), None) for name, _ in hooks}
    for _ in range(pairs):
        for name, h in hooks:
            cpu, rc, _w = run(h, command)
            if cpu < best[name][0]:
                best[name] = (cpu, rc)
    b0 = max(best["baseline"][0], 0.01)
    for name, _h in hooks:
        cpu, rc = best[name]
        rcs = "" if rc == 2 or name == "baseline" else f" exit={rc}"
        print(f"size={len(command):6d} B  {name:10s} cpu={cpu:8.3f} s  ratio-to-baseline={cpu / b0:7.1f}{rcs}" if cpu != float("inf") else f"size={len(command)} {name} >cap")
