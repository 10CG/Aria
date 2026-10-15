#!/usr/bin/env python3
"""pat_cost.py -- CPU seconds of `grep -oE` / `sed -E s` with the kv-secret-assign pattern of a secret-scan.sh on one adversarial single line, process by process.

usage: python3 pat_cost.py <secret-scan.sh> <shape> [size_kb]    shape: export-blank | key-prefix | blank-before-eq | long-value"""
import os
import re
import resource
import secrets
import string
import subprocess
import sys
import tempfile
import time

hook, shape = os.path.abspath(sys.argv[1]), sys.argv[2]
n = int(sys.argv[3]) * 1000 if len(sys.argv) > 3 else 300000
src = open(hook, encoding="utf-8").read()
m = re.search(r"^  '(kv-secret-assign)\|(.*)'$", src, re.M)
assert m, "kv pattern not found"
pat = m.group(2).replace("'\"'\"'", "'")
v24 = "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(24))
TOK = "TO" + "KEN"
shapes = {
    "export-blank": "export" + " " * n + "SVC_" + TOK + "=" + v24,
    "key-prefix": "A" * n + " JWT_" + "SEC" + "RET=" + v24,
    "blank-before-eq": "SVC_" + TOK + " " * n + "=" + v24,
    "long-value": "SVC_" + TOK + "=" + ("aA1" * (n // 3)),
}
text = shapes[shape]
d = tempfile.mkdtemp(prefix="patcost-")
f = os.path.join(d, "in.txt")
open(f, "w").write(text)


def cpu(argv, **kw):
    r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    t0 = time.time()
    p = subprocess.run(argv, capture_output=True, **kw)
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    return (r1.ru_utime - r0.ru_utime) + (r1.ru_stime - r0.ru_stime), time.time() - t0, p


env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
c, w, p = cpu(["grep", "-oE", "--", pat, f], env=env)
print(f"grep -oE : cpu {c:6.2f}s wall {w:6.2f}s matches {len(p.stdout.splitlines())}")
c, w, p = cpu(["sed", "-i", "-E", "s\x01" + pat + "\x01<counted>\x01g", f], env=env)
print(f"sed -i -E: cpu {c:6.2f}s wall {w:6.2f}s")
