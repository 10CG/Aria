#!/usr/bin/env python3
"""w_scan.py -- W-cluster experiment: CPU cost of the L3 value-extraction code on long single-line shapes.

usage: python3 w_scan.py <hook secret-scan.sh> [size_kb ...] [--only NAME,NAME]

Every credential-shaped value is generated in-process with `secrets` and fed to the hook on stdin; only exit code, alert tag counts and CPU seconds are printed.
CPU = user+sys of the hook and every process it starts (the shell builtin `times`), each run capped at 40 CPU seconds.
Rule #7: no credential-shaped literal in this file (key names are assembled from pieces)."""
import json
import os
import re
import secrets
import string
import subprocess
import sys
import tempfile

HOOK = os.path.abspath(sys.argv[1])
args = [a for a in sys.argv[2:] if not a.startswith("--")]
SIZES = [int(a) for a in args] or [100, 300]
ONLY = None
if "--only" in sys.argv:
    ONLY = set(sys.argv[sys.argv.index("--only") + 1].split(","))
    SIZES = [int(a) for a in args if a.isdigit() and a != sys.argv[sys.argv.index("--only") + 1]] or [100, 300]

ALNUM = string.ascii_letters + string.digits
WORK = tempfile.mkdtemp(prefix="wscan-")
HOME = os.path.join(WORK, "home")
os.makedirs(HOME)
_TIMES = re.compile(r"(\d+)m([0-9.]+)s\s+(\d+)m([0-9.]+)s")


def alnum(n):
    while True:
        v = "".join(secrets.choice(ALNUM) for _ in range(n))
        if any(c.islower() for c in v) and any(c.isupper() for c in v) and any(c.isdigit() for c in v) and "gh" not in v and "sk" not in v and "AK" not in v and "eyJ" not in v and "LT" not in v:
            return v


def long(unit, n):
    return unit * (n // len(unit))


TOK = "TO" + "KEN"
SEC = "SE" + "CRET"
PW = "PASS" + "WORD"


def envelope(c):
    return {"tool_name": "Bash", "tool_input": {"command": "cat /x/out.txt"},
            "tool_response": {"stdout": c, "stderr": "", "interrupted": False, "isImage": False, "noOutputExpected": False}}


def run(content, cap=40):
    wrapper = 'ulimit -t "$0"; bash "$@" >"$OUT" 2>/dev/null; rc=$?; times >&2; exit $rc'
    out = os.path.join(WORK, "out.json")
    env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": HOME, "TMPDIR": WORK, "USER": "probe", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "OUT": out}
    p = subprocess.run(["sh", "-c", wrapper, str(cap), HOOK], input=json.dumps(envelope(content)).encode(), capture_output=True, env=env, cwd=WORK, timeout=600)
    ms = _TIMES.findall(p.stderr.decode("utf-8", "replace"))
    cpu = (int(ms[-1][0]) * 60 + float(ms[-1][1]) + int(ms[-1][2]) * 60 + float(ms[-1][3])) if ms else -1.0
    tags = {}
    try:
        j = json.loads(open(out).read() or "{}")
        m = re.search(r"\(([^)]*)\); rotate", j.get("systemMessage", ""))
        if m:
            tags = {t: int(c) for t, c in re.findall(r"([a-z0-9-]+)=(\d+)", m.group(1))}
    except Exception:
        pass
    return p.returncode, cpu, tags


def cases(n):
    """name -> content builder.  n = size in bytes of the long part"""
    v24 = alnum(24)
    U = long("aA1", n)             # a long run of value-class characters, three classes, no quote, no blank
    return {
        # --- kv, the tl/M2 shapes: long UNQUOTED value
        "kv-eq-spaced-long-value": lambda: "SVC_" + TOK + " = " + U,
        "kv-export-long-value": lambda: "export SVC_" + TOK + "=" + U,
        "kv-yaml-long-value": lambda: "  SVC_" + TOK + ": " + U,
        "kv-quoted-long-value": lambda: "SVC_" + TOK + '="' + U + '"',
        # --- kv, blank runs around the delimiters
        "kv-blank-before-eq": lambda: "SVC_" + TOK + " " * n + "=" + v24,
        "kv-blank-after-eq": lambda: "SVC_" + TOK + "=" + " " * n + v24,
        "kv-export-blank": lambda: "export" + " " * n + "SVC_" + TOK + "=" + v24,
        "kv-long-key-prefix": lambda: "A" * n + " JWT_" + SEC + "=" + v24,
        # --- json
        "json-long-value": lambda: '{"token":"' + U + '"}',
        "json-blank-before-colon": lambda: '{"token"' + " " * n + ':"' + v24 + '"}',
        "json-blank-after-colon": lambda: '{"token":' + " " * n + '"' + v24 + '"}',
        "json-old-long-value": lambda: '{"pass' + 'word":"' + U + '"}',
        "json-old-blank-before-colon": lambda: '{"pass' + 'word"' + " " * n + ':"' + v24 + '"}',
        "json-env-long-key": lambda: '{"' + "A" * n + "_" + TOK + '":"' + v24 + '"}',
        # --- headers, flags
        "auth-long-value": lambda: "Authorization: token " + U,
        "auth-blank-run": lambda: "Authorization:" + " " * n + "token " + v24,
        "cf-long-value": lambda: "CF-Access-Client-" + "Secret: " + U,
        "cli-long-value": lambda: "--token=" + U,
        # --- baseline tags (the extraction code runs for them too)
        "bearer-long-value": lambda: "Authorization: Bear" + "er " + U,
        "xapikey-long-value": lambda: "X-Api-" + "Key: " + U,
        "env-line-long-value": lambda: "DB_" + PW + "=" + U,
        "env-line-long-key": lambda: "A" * n + "_" + TOK + "=" + v24,
        "postgres-long-password": lambda: "postgres://u:" + "p" * n + "@h",
        "postgres-long-user": lambda: "postgres://" + "u" * n + ":" + alnum(8) + "@h",
        "basic-auth-long": lambda: "https://u:" + "p" * n + "@host",
    }


names = None
for kb in SIZES:
    n = kb * 1000
    cs = cases(n)
    print(f"== size {kb} KB ==")
    for name, b in cs.items():
        if ONLY and name not in ONLY:
            continue
        rc, cpu, tags = run(b())
        print(f"{name:34s} rc={rc:<4d} cpu={cpu:7.2f}s tags={tags}")
