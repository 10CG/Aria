#!/usr/bin/env python3
"""scan_file.py HOOK FILE [LINE_FROM LINE_TO] -- feed a file's text to a secret-scan hook as a Bash stdout envelope and print ONLY the tag breakdown
(no values).  With a line range, scan only those lines; with `--bisect` print the line numbers whose single-line scan alerts."""
import json
import os
import re
import subprocess
import sys

hook, path = sys.argv[1], sys.argv[2]
bisect = "--bisect" in sys.argv
args = [a for a in sys.argv[3:] if a != "--bisect"]
text = open(path, encoding="utf-8", errors="replace").read()
lines = text.split("\n")
if len(args) == 2:
    lo, hi = int(args[0]), int(args[1])
    text = "\n".join(lines[lo - 1:hi])
home = os.environ.get("HOME", "/tmp")
env = {"PATH": os.environ["PATH"], "HOME": home, "TMPDIR": os.environ.get("TMPDIR", "/tmp"), "LC_ALL": "C.UTF-8"}


def run(t):
    env_json = json.dumps({"tool_name": "Bash", "tool_input": {"command": "x"}, "tool_response": {"stdout": t, "stderr": "", "interrupted": False, "isImage": False, "noOutputExpected": False}})
    p = subprocess.run(["bash", hook], input=env_json, capture_output=True, text=True, env=env)
    msg = ""
    try:
        msg = json.loads(p.stdout).get("systemMessage", "") if p.stdout.strip() else ""
    except Exception:
        msg = "unparsed"
    m = re.search(r"\(([^)]*)\)\s*$", msg)
    return p.returncode, msg if not m else m.group(1), bool(p.stdout.strip())


if bisect:
    hits = []
    for i, l in enumerate(lines, 1):
        if not l.strip():
            continue
        rc, tags, alert = run(l)
        if alert:
            hits.append((i, tags))
    print("alerting lines:", hits)
else:
    print(run(text))
