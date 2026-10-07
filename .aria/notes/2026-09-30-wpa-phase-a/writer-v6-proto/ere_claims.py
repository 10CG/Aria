#!/usr/bin/env python3
"""ere_claims.py -- the measurements behind the numbers that W2's linear-time paragraph quotes: the CPU time of `grep -oE -- <pattern>` (exactly the hook's call) on one long single line, for the
target pattern and for the bad-implementation patterns (unbounded affix / no left boundary), read from the hook files themselves.

  kv   : 320 KB run of one upper-case letter + ` JWT_SECRET=<value>`       target (bounded {0,64} + left boundary) vs kv_unbounded
  cli  : 300 KB run of `-`           + ` -token=<value>`                  target (boundary + {0,40}) vs cli_unbounded (boundary, unbounded prefix) vs cli_noleft (bounded, no left boundary)

usage: ere_claims.py TARGET_SCAN VARIANT_DIR_ROOT     (VARIANT_DIR_ROOT/<variant>/secret-scan.sh for kv_unbounded cli_unbounded cli_noleft)
Values are generated at run time; nothing credential-shaped is printed (only sizes, seconds)."""
import os
import re
import resource
import secrets
import string
import subprocess
import sys

target, vroot = sys.argv[1], sys.argv[2]
AL = string.ascii_letters + string.digits
val = "".join(secrets.choice(AL) for _ in range(24))


def pattern_of(hook, tag):
    src = open(hook, encoding="utf-8").read()
    m = re.search(r"^  '" + re.escape(tag) + r"\|(.*)'$", src, re.M)
    assert m, (hook, tag)
    return m.group(1).replace("'\"'\"'", "'")


def cpu_of(pat, line):
    r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    p = subprocess.run(["grep", "-oE", "--", pat], input=line.encode(), capture_output=True, env={"PATH": "/usr/local/bin:/usr/bin:/bin", "LC_ALL": "C.UTF-8"}, timeout=900)
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    return (r1.ru_utime - r0.ru_utime) + (r1.ru_stime - r0.ru_stime), bool(p.stdout.strip())


KV_LINE = "A" * 320000 + " JWT_" + "SEC" + "RET=" + val
CLI_LINE = "-" * 300000 + " -" + "tok" + "en=" + val
rows = [("kv-secret-assign", "target (bounded {0,64}, left boundary)", target, KV_LINE, "320 KB upper-case run"),
        ("kv-secret-assign", "kv_unbounded (unbounded key affixes)", os.path.join(vroot, "kv_unbounded", "secret-scan.sh"), KV_LINE, "320 KB upper-case run"),
        ("cli-secret-flag", "target (left boundary, {0,40})", target, CLI_LINE, "300 KB dash run"),
        ("cli-secret-flag", "cli_unbounded (left boundary, unbounded prefix)", os.path.join(vroot, "cli_unbounded", "secret-scan.sh"), CLI_LINE, "300 KB dash run"),
        ("cli-secret-flag", "cli_noleft (bounded, no left boundary)", os.path.join(vroot, "cli_noleft", "secret-scan.sh"), CLI_LINE, "300 KB dash run")]
for tag, name, hook, line, shape in rows:
    t, hit = cpu_of(pattern_of(hook, tag), line)
    print(f"{tag:18s} {name:52s} {shape:24s} grep -oE CPU {t:7.2f} s  hit={'yes' if hit else 'NO'}", flush=True)
