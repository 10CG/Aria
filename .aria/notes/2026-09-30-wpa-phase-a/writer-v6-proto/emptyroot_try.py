#!/usr/bin/env python3
"""emptyroot_try.py <hook> [<hook> ...] -- CLAUDE_PROJECT_DIR unset / empty / set, stdin cwd = a project holding an entry file: exit codes of `cat <listed path>` per hook.
Only exit codes are printed; the command text is stdin only, never executed."""
import json
import os
import subprocess
import sys
import tempfile

work = tempfile.mkdtemp(prefix="er-")
proj = os.path.join(work, "proj")
os.makedirs(os.path.join(proj, ".aria"))
LISTED = "/srv/data/hit-me.conf"
open(os.path.join(proj, ".aria", "secret-guard.paths"), "w").write(LISTED + "\n")
home = os.path.join(work, "home")
os.makedirs(home)
base = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": home, "TMPDIR": work, "USER": "probe", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": "cat " + LISTED}, "cwd": proj}).encode()
for hook in sys.argv[1:]:
    res = []
    for label, extra in (("unset", {}), ("empty", {"CLAUDE_PROJECT_DIR": ""}), ("set", {"CLAUDE_PROJECT_DIR": proj}), ("set-other", {"CLAUDE_PROJECT_DIR": work})):
        env = dict(base)
        env.update(extra)
        p = subprocess.run(["bash", os.path.abspath(hook)], input=payload, capture_output=True, env=env, cwd=work)
        res.append(f"{label}={p.returncode}")
    print(" ".join(res), "::", os.path.relpath(hook))
