#!/usr/bin/env python3
"""ratio_try.py -- CPU ratio target/baseline of secret-scan.sh copies on one long single-line shape (the W14 (i3) idea), minimum over N interleaved pairs.

usage: python3 ratio_try.py <base hook> <hook> [<hook> ...] --sizes 30,100,300 --shape kv-eq|kv-export|kv-yaml|kv-quoted|header --pairs 3"""
import json
import os
import resource
import secrets
import string
import subprocess
import sys
import tempfile
import time

args = sys.argv[1:]


def opt(name, default):
    return args[args.index(name) + 1] if name in args else default


sizes = [int(x) for x in opt("--sizes", "30,100,300").split(",")]
shape = opt("--shape", "kv-eq")
pairs = int(opt("--pairs", "3"))
hooks = [os.path.abspath(a) for a in args if a.endswith(".sh")]
home = tempfile.mkdtemp(prefix="ratio-")
ENV = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": home, "TMPDIR": home, "USER": "probe", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
TOK = "TO" + "KEN"


def payload(text):
    return json.dumps({"tool_name": "Bash", "tool_input": {"command": "x"}, "tool_response": {"stdout": text, "stderr": "", "interrupted": False, "isImage": False, "noOutputExpected": False}}).encode()


def build(n):
    u = "aA1" * (n // 3)
    return {"kv-eq": "SVC_" + TOK + " = " + u, "kv-export": "export SVC_" + TOK + "=" + u, "kv-yaml": "  SVC_" + TOK + ": " + u,
            "kv-quoted": "SVC_" + TOK + '="' + u + '"', "header": "Authorization: " + "tok" + "en " + u}[shape]


def run(h, p):
    r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    subprocess.run(["bash", h], input=p, capture_output=True, env=ENV, timeout=900)
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    return (r1.ru_utime - r0.ru_utime) + (r1.ru_stime - r0.ru_stime)


for kb in sizes:
    p = payload(build(kb * 1000))
    best = {h: 1e9 for h in hooks}
    for _ in range(pairs):
        for h in hooks:
            best[h] = min(best[h], run(h, p))
    base = best[hooks[0]]
    print(f"{shape} {kb:4d} KB  " + "  ".join(f"{os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(h))))}:{best[h]:6.2f}s({best[h] / max(base, 1e-6):4.1f}x)" for h in hooks))
