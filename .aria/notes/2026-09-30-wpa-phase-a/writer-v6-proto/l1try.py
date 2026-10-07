#!/usr/bin/env python3
"""l1try.py -- feed command texts (as stdin text only, never executed) to one or more secret-guard.sh copies and print the exit codes.

usage: python3 l1try.py <cmdfile> <hook> [<hook> ...] [--env K=V ...] [--tool Bash|Read|Edit]
  <cmdfile>: one command per line; the two-character sequence \\n inside a line stands for a newline, \\t for a tab; a line starting with # is a comment.
Output: one line per command: exit codes of the hooks in the order given, then the command."""
import json
import os
import subprocess
import sys
import tempfile

args = sys.argv[1:]
env_extra = {}
tool = "Bash"
if "--tool" in args:
    i = args.index("--tool")
    tool = args[i + 1]
    del args[i:i + 2]
while "--env" in args:
    i = args.index("--env")
    k, _, v = args[i + 1].partition("=")
    env_extra[k] = v
    del args[i:i + 2]
cmdfile, hooks = os.path.abspath(args[0]), [os.path.abspath(h) for h in args[1:]]
work = tempfile.mkdtemp(prefix="l1try-")
home = os.path.join(work, "home")
os.makedirs(home)
env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": home, "TMPDIR": work, "USER": "probe", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
env.update(env_extra)
for line in open(cmdfile, encoding="utf-8").read().split("\n"):
    if not line.strip() or line.startswith("#"):
        continue
    cmd = line.replace("\\n", "\n").replace("\\t", "\t")
    ti = {"command": cmd} if tool == "Bash" else {"file_path": cmd}
    rcs = []
    for h in hooks:
        p = subprocess.run(["bash", h], input=json.dumps({"tool_name": tool, "tool_input": ti}).encode(), capture_output=True, env=env, cwd=work, timeout=120)
        rcs.append(p.returncode)
    print(" ".join(str(r) for r in rcs), "::", line)
