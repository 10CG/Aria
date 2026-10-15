#!/usr/bin/env python3
"""scan_all.py FILE_OR_DIR [...] -- Rule #7 self-scan: every file (<= 2 MB text) is fed, as a Bash tool stdout and as a Read tool file.content, to the BASELINE secret-scan hook and to the
TARGET prototype secret-scan hook; prints one line per file with 'silent' / the tag breakdown (no values) for the four combinations.  Exit 1 if anything alerts."""
import json
import os
import re
import subprocess
import sys

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOKS = {"base": os.path.join(EXP, "base/aria/hooks/secret-scan.sh"), "target": os.path.join(EXP, "work/t5f/aria/hooks/secret-scan.sh")}
ENV = {"PATH": os.environ["PATH"], "HOME": os.path.join(EXP, "home"), "TMPDIR": os.path.join(EXP, "tmp"), "LC_ALL": "C.UTF-8"}


def envelope(kind, text):
    if kind == "bash":
        return {"tool_name": "Bash", "tool_input": {"command": "x"}, "tool_response": {"stdout": text, "stderr": "", "interrupted": False, "isImage": False, "noOutputExpected": False}}
    return {"tool_name": "Read", "tool_input": {"file_path": "/x/f"}, "tool_response": {"type": "text", "file": {"filePath": "/x/f", "content": text, "numLines": 1, "startLine": 1, "totalLines": 1}}}


def run(hook, kind, text):
    p = subprocess.run(["bash", hook], input=json.dumps(envelope(kind, text)), capture_output=True, text=True, env=ENV)
    if not p.stdout.strip():
        return "silent"
    try:
        msg = json.loads(p.stdout).get("systemMessage", "")
    except Exception:
        return "alert(unparsed)"
    tg = [g for g in re.findall(r"\(([^)]*)\)", msg) if "=" in g]
    return "ALERT " + (tg[-1] if tg else "?")


files = []
for a in sys.argv[1:]:
    if os.path.isdir(a):
        for r, _d, fs in os.walk(a):
            for f in sorted(fs):
                files.append(os.path.join(r, f))
    else:
        files.append(a)
bad = 0
for f in files:
    try:
        if os.path.getsize(f) > 2_000_000:
            print(f, "| skipped (>2 MB)")
            continue
        text = open(f, encoding="utf-8", errors="replace").read()
    except Exception as e:
        print(f, "| unreadable", type(e).__name__)
        continue
    res = {(h, k): run(HOOKS[h], k, text) for h in HOOKS for k in ("bash", "read")}
    flag = any(v != "silent" for v in res.values())
    bad += flag
    print(os.path.relpath(f, EXP), "|", " ; ".join(f"{h}/{k}: {v}" for (h, k), v in res.items()), "  <== ALERT" if flag else "")
print("files with an alert:", bad)
sys.exit(1 if bad else 0)
