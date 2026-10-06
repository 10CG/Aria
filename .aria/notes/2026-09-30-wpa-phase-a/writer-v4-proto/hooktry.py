#!/usr/bin/env python3
"""hooktry.py HOOK CASES.py [HOOK2 ...]  -- run L1 hook(s) over (tool, payload[, want]) cases defined in CASES.py (variable CASES)
and print exit codes side by side; a case with `want` is flagged when a hook disagrees.  Commands are only fed to the hook
on stdin, never executed.  HOME / TMPDIR are private."""
import json
import os
import subprocess
import sys
import tempfile

hooks = [sys.argv[1]] + sys.argv[3:]
ns = {}
exec(open(sys.argv[2], encoding="utf-8").read(), ns)
cases = ns["CASES"]
extra_env = ns.get("ENV", {})
home = tempfile.mkdtemp(prefix="ht-")


def run(hook, tool, payload, env_extra=None):
    ti = {"command": payload} if tool == "Bash" else {"file_path": payload}
    env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": home, "TMPDIR": home, "USER": "probe", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    env.update(extra_env)
    if env_extra:
        env.update(env_extra)
    p = subprocess.run(["bash", hook], input=json.dumps({"tool_name": tool, "tool_input": ti}).encode(), capture_output=True, env=env, timeout=120)
    return p.returncode


bad = 0
for c in cases:
    tool, payload = c[0], c[1]
    want = c[2] if len(c) > 2 else None
    rcs = [run(h, tool, payload) for h in hooks]
    flag = ""
    if want is not None and any(r != want for r in rcs[-1:]):
        flag = "   <== MISMATCH (want %s)" % want
        bad += 1
    shown = payload if tool == "Bash" else tool + " " + payload
    print(" ".join(str(r) for r in rcs), "|", shown[:150].replace("\n", "\\n"), flag)
print("mismatches:", bad)
