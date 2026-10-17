#!/usr/bin/env python3
"""l3try.py HOOK_SCAN_SH -- run a few accepted-false-positive texts through a secret-scan hook (Bash envelope), print only tag breakdown.
The key names are assembled at run time (no contiguous credential-key literal in this source)."""
import json
import os
import re
import subprocess
import sys

hook = sys.argv[1]
home = os.environ.get("HOME", "/tmp")
env = {"PATH": os.environ["PATH"], "HOME": home, "TMPDIR": os.environ.get("TMPDIR", "/tmp"), "LC_ALL": "C.UTF-8"}
K = lambda *p: "".join(p)
cases = [
    ("env-key json, URL value", '{"' + K("TOK", "EN_URL") + '":"https://login.example.com/oauth2/v2.0/token"}'),
    ("env-key json, resource name", '{"' + K("SEC", "RET_NAME") + '":"prod/payments/db-credentials-v2"}'),
    ("env-key json, policy name", '{"' + K("PASS", "WORD_POLICY") + '":"min-length-12-with-symbols-required"}'),
    ("kv, relative path value", K("PASS", "WORD_RESET_PATH") + " = auth/reset/Confirm2Step"),
    ("kv yaml colon, resource path", K("SEC", "RET_NAME") + ": prod/payments/db-credentials-v2"),
]
for name, text in cases:
    env_json = json.dumps({"tool_name": "Bash", "tool_input": {"command": "x"}, "tool_response": {"stdout": text, "stderr": "", "interrupted": False, "isImage": False, "noOutputExpected": False}})
    p = subprocess.run(["bash", hook], input=env_json, capture_output=True, text=True, env=env)
    tags = "silent"
    if p.stdout.strip():
        try:
            msg = json.loads(p.stdout).get("systemMessage", "")
            ms = re.findall(r"\(([^)]*)\)", msg)
            tg = [g for g in ms if "=" in g]
            tags = tg[-1] if tg else msg[:80]
        except Exception:
            tags = "unparsed"
    print(f"{name:34s} | rc={p.returncode} | {tags}")
