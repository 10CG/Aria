#!/usr/bin/env python3
"""ere_battery.py HOOK_SCAN_SH [--sizes 5000,10000,20000,40000] [--only TAG[,TAG]]  -- scaling of the 6 new key-shape patterns on adversarial SINGLE lines.

The patterns are read from the hook's PATTERNS array (the `'tag|ere'` lines of the 6 new tags), so the battery times exactly what the hook runs (`grep -oE -- ere`, and the
`sed -E` counting substitution when something matched).  For every (pattern, line shape) it runs the line at the sizes given (n, 2n, 4n, 8n) and prints the CPU time of
`grep -oE` and the ratio t(2n)/t(n): about 2 = linear, about 4 = quadratic.  A line is a run of one adversarial construction followed (where the construction needs it) by a
real hit, so the hit is found at the very end (the worst place for a backtracking engine).  Values are generated at run time; nothing credential-shaped is printed."""
import os
import re
import resource
import secrets
import string
import subprocess
import sys

hook = sys.argv[1]
sizes = [int(x) for x in (sys.argv[sys.argv.index("--sizes") + 1] if "--sizes" in sys.argv else "5000,10000,20000,40000").split(",")]
only = set((sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else "").split(",")) - {""}
src = open(hook, encoding="utf-8").read()
NEW = ["json-credential-field", "json-env-secret-key", "kv-secret-assign", "auth-header-token", "cf-access-client-secret", "cli-secret-flag"]
pats = {}
for m in re.finditer(r"^  '([a-z0-9-]+)\|(.*)'$", src, re.M):
    if m.group(1) in NEW:
        pats[m.group(1)] = m.group(2).replace("'\"'\"'", "'")
assert set(pats) == set(NEW), set(NEW) - set(pats)
AL = string.ascii_letters + string.digits


def val(n=24):
    return "".join(secrets.choice(AL) for _ in range(n))


def shapes(n):
    t = "tok" + "en"
    kw = "TO" + "KEN"
    return {
        "dashes + ` -token=`": "-" * n + " -" + t + "=" + val(),
        "a- repeated + ` --token=`": "a-" * (n // 2) + " --" + t + "=" + val(),
        "1a2b3c4d- repeated + flag": "1a2b3c4d-" * (n // 9) + " --" + t + "=" + val(),
        "A1 repeated + ` X_TOKEN=`": "A1" * (n // 2) + " X_" + kw + "=" + val(),
        "TOKEN repeated (keyword-rich)": kw * (n // 5) + "=" + val(),
        "TOKEN repeated, no `=`": kw * (n // 5),
        "uppercase run + ` JWT_SECRET=`": "A" * n + " JWT_SEC" + "RET=" + val(),
        "underscore run + key": "_" * n + "X_" + kw + "=" + val(),
        "`=` run": "KEY_" + kw + "=" * n,
        "`--token=` repeated": ("--" + t + "=") * (n // 8),
        "`export ` repeated": "export " * (n // 7) + kw + "=" + val(),
        "json key, unclosed value": '{"' + t + '":"' + "x" * n,
        "json key repeated, unclosed": ('"' + t + '":"abc') * (n // 12),
        "quotes run": '"' * n,
        "auth header repeated": "Authorization: " * (n // 15),
        "auth header + long value": "Authorization: " + t + " " + "a" * n,
        "cf header repeated": "CF-Access-Client-Secret:" * (n // 24),
        "env-json key, long upper run": '{"' + "A" * n + kw + '":"' + val() + '"}',
        "spaces run": "KEY_" + kw + " " * n + "=" + val(),
        "colon run": "KEY_" + kw + ":" * n,
        # --- shapes for the value-extraction code of every tag family (baseline tags included: the fingerprint code runs on them too)
        "env-line (baseline) long key": "A" * n + "_" + kw + "=" + val(),
        "env-line (baseline) long value": "DB_" + kw + "=" + "aA1" * (n // 3),
        "bearer (baseline) long value": "Authorization: " + "Bear" + "er " + "aA1" * (n // 3),
        "x-api-key (baseline) long value": "X-Api-Key: " + "aA1" * (n // 3),
        "x-api-key + spaces + value": "X-Api-Key:" + " " * n + val(),
        "postgres url, long user": "postgres://" + "u" * n + ":" + val(8) + "@h",
        "postgres url, long password": "postgres://u:" + "p" * n + "@h",
        "basic-auth url, long user": "https://" + "u" * n + ":" + val(8) + "@h",
        "kv value dotted chain": "SVC_" + kw + "=" + "aA1." * (n // 4),
        "kv value long mixed": "SVC_" + kw + "=" + "aA1" * (n // 3),
        "kv export + spaces": "export" + " " * n + "SVC_" + kw + "=" + val(),
        "kv value spaces after =": "SVC_" + kw + "=" + " " * n + val(),
        "json value long": '{"' + t + '":"' + "aA1" * (n // 3) + '"}',
        "json value spaces": '{"' + t + '":"' + " " * n + val() + '"}',
        "json key + spaces before colon": '{"' + t + '"' + " " * n + ':"' + val() + '"}',
        "auth header spaces + value": "Authorization:" + " " * n + t + " " + val(),
        "auth header token + spaces + value": "Authorization: " + t + " " * n + val(),
        "cf header spaces + value": "CF-Access-Client-Secret:" + " " * n + val(),
        "cli long value": "--" + t + "=" + "aA1" * (n // 3),
        "cli long flag name 41": "--" + "x" * 41 + t + "=" + val(),
    }


def cpu(args, text):
    r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    p = subprocess.run(args, input=text.encode(), capture_output=True, timeout=600)
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    return (r1.ru_utime - r0.ru_utime) + (r1.ru_stime - r0.ru_stime), len(p.stdout.splitlines())


import json
if "--hook" in sys.argv:
    home = os.environ.get("TMPDIR", "/tmp")
    ENV = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": home, "TMPDIR": home, "USER": "probe", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    def hook_cpu(line):
        pay = json.dumps({"tool_name": "Bash", "tool_input": {"command": "x"}, "tool_response": {"stdout": line, "stderr": "", "interrupted": False, "isImage": False, "noOutputExpected": False}})
        r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
        p = subprocess.run(["bash", hook], input=pay.encode(), capture_output=True, env=ENV, timeout=900)
        r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
        return (r1.ru_utime - r0.ru_utime) + (r1.ru_stime - r0.ru_stime), p.stdout.decode()[:0]
    names = list(shapes(100).keys())
    for name in names:
        res = []
        for n in sizes:
            line = shapes(n)[name]
            c, _ = hook_cpu(line)
            res.append((n, c))
        ratios = [res[i + 1][1] / max(res[i][1], 0.05) for i in range(len(res) - 1)]
        flag = "   <== SUPERLINEAR" if res[-1][1] > 2.0 and ratios[-1] > 3.0 else ""
        print(f"HOOK | {name:34s} | " + " ".join(f"{n}:{c:6.3f}s" for n, c in res) + " | last ratio " + f"{ratios[-1]:4.1f}" + flag, flush=True)
    sys.exit(0)
worst = {}
for tag in NEW:
    if only and tag not in only:
        continue
    pat = pats[tag]
    names = list(shapes(100).keys())
    for name in names:
        res = []
        for n in sizes:
            line = shapes(n)[name]
            best = min(cpu(["grep", "-oE", "--", pat], line)[0] for _ in range(2))
            hits = cpu(["grep", "-oE", "--", pat], line)[1]
            res.append((n, best, hits))
        ratios = [res[i + 1][1] / max(res[i][1], 0.004) for i in range(len(res) - 1)]
        big = res[-1]
        flag = ""
        if big[1] > 1.0 and ratios[-1] > 3.0:
            flag = "   <== SUPERLINEAR"
        print(f"{tag:24s} | {name:34s} | " + " ".join(f"{n}:{c:6.3f}s" for n, c, _h in res) + " | last ratio " + f"{ratios[-1]:4.1f}" + f" | hits {big[2]}" + flag, flush=True)
        worst[(tag, name)] = (big[1], ratios[-1])
print("max CPU at the largest size: %.3fs" % max(v[0] for v in worst.values()))
