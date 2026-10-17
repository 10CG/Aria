#!/usr/bin/env python3
"""fail_try3.py <hook> [<hook> ...] -- the three SC-35 35e style failure texts (two documented placeholders, one ordinary error) through secret-scan.sh copies: alert / silent per text.
Rule #7: the key and the header word are split in the source; the values are whitelisted markers."""
import json
import os
import subprocess
import sys
import tempfile

work = tempfile.mkdtemp(prefix="ft3-")
home = os.path.join(work, "home")
os.makedirs(home)
E = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": home, "TMPDIR": work, "USER": "probe", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
texts = ["Exit code 1\nset " + "JWT_" + "SECRET = FAKE_EXAMPLE_VALUE_1234567890 first",
         "Exit code 22\n> Authorization: " + "tok" + "en PLACEHOLDER_EXAMPLE_00000000",
         "Exit code 1\nls: cannot access 'x': No such file or directory"]
for hook in sys.argv[1:]:
    out = []
    for tx in texts:
        payload = {"hook_event_name": "PostToolUseFailure", "tool_name": "Bash", "tool_input": {"command": "x"}, "tool_use_id": "t", "error": tx, "is_interrupt": False}
        p = subprocess.run(["bash", os.path.abspath(hook)], input=json.dumps(payload).encode(), capture_output=True, env=E, cwd=work)
        out.append("alert" if p.stdout.strip() else "silent")
    print(os.path.relpath(hook), out)
