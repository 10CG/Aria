#!/usr/bin/env python3
"""cap_probe.py -- the smallest per-process CPU cap (`ulimit -t N`, whole seconds) under which a secret-scan.sh copy still reports the expected tag on one long shape.
That N is the largest CPU time of any single process of the hook (the hook's own bash for the quadratic value code, grep / sed for the patterns): the quantity the probe's SC-34 rows judge.

usage: python3 cap_probe.py <hook> <shape> <size_kb> [<hook> ...]
shapes: kv-eq kv-export kv-yaml kv-blank-before-eq kv-export-blank json-blank-before-colon envline-long-key pg-long-password pg-long-user basicauth-long json-old-blank-before-colon"""
import json
import os
import re
import secrets
import string
import subprocess
import sys
import tempfile

shape, kb = sys.argv[2], int(sys.argv[3])
hooks = [os.path.abspath(sys.argv[1])] + [os.path.abspath(h) for h in sys.argv[4:]]
n = kb * 1000
work = tempfile.mkdtemp(prefix="cap-")
home = os.path.join(work, "home")
os.makedirs(home)
A = string.ascii_letters + string.digits


def alnum(k):
    while True:
        v = "".join(secrets.choice(A) for _ in range(k))
        if any(c.islower() for c in v) and any(c.isupper() for c in v) and any(c.isdigit() for c in v) and not any(b in v for b in ("AK", "gh", "sk", "eyJ", "LT")):
            return v


TOK, PW = "TO" + "KEN", "PASS" + "WORD"
U = "aA1" * (n // 3)
v24 = alnum(24)
CASES = {
    "kv-eq": ("SVC_" + TOK + " = " + U, "kv-secret-assign"),
    "kv-export": ("export SVC_" + TOK + "=" + U, "kv-secret-assign"),
    "kv-yaml": ("  SVC_" + TOK + ": " + U, "kv-secret-assign"),
    "kv-blank-before-eq": ("SVC_" + TOK + " " * n + "=" + v24, "kv-secret-assign"),
    "kv-export-blank": ("export" + " " * n + "SVC_" + TOK + "=" + v24, "kv-secret-assign"),
    "json-blank-before-colon": ('{"' + "tok" + 'en"' + " " * n + ':"' + v24 + '"}', "json-credential-field"),
    "json-old-blank-before-colon": ('{"pass' + 'word"' + " " * n + ':"' + v24 + '"}', "json-secret-field"),
    "envline-long-key": ("A" * n + "_" + TOK + "=" + v24, "env-line-secret-keyword"),
    "pg-long-password": ("postgres://u:" + "p" * n + "@h", "postgres-url"),
    "pg-long-user": ("postgres://" + "u" * n + ":" + alnum(8) + "@h", "postgres-url"),
    "basicauth-long": ("https://u:" + "p" * n + "@host", "basic-auth-url"),
}
text, tag = CASES[shape]
env_obj = {"tool_name": "Bash", "tool_input": {"command": "x"}, "tool_response": {"stdout": text, "stderr": "", "interrupted": False, "isImage": False, "noOutputExpected": False}}
payload = json.dumps(env_obj).encode()
ENV = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": home, "TMPDIR": work, "USER": "probe", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}


def detects(hook, cap):
    p = subprocess.run(["sh", "-c", 'ulimit -t "$0"; exec "$@"', str(cap), "bash", hook], input=payload, capture_output=True, env=ENV, cwd=work, timeout=600)
    if not p.stdout.strip():
        return False
    try:
        j = json.loads(p.stdout)
    except Exception:
        return False
    return (tag + "=1") in j.get("systemMessage", "")


for h in hooks:
    found = None
    for cap in (1, 2, 3, 4, 5, 6, 8, 10, 13, 17, 22, 30):
        if detects(h, cap):
            found = cap
            break
    print(f"{shape:30s} {kb:4d} KB  {os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(h)))):6s}  smallest per-process cap that still detects: {found}")
