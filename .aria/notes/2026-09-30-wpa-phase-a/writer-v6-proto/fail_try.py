#!/usr/bin/env python3
"""fail_try.py -- feed PostToolUseFailure / PostToolUse envelopes to secret-scan.sh copies; print exit code, event name of the output, tags.

usage: python3 fail_try.py <hook> [<hook> ...]
Values are generated at run time and never printed (Rule #7)."""
import json
import os
import re
import secrets
import string
import subprocess
import sys
import tempfile

hooks = [os.path.abspath(h) for h in sys.argv[1:]]
ALNUM = string.ascii_letters + string.digits
work = tempfile.mkdtemp(prefix="failtry-")
home = os.path.join(work, "home")
os.makedirs(home)


def alnum(n):
    while True:
        v = "".join(secrets.choice(ALNUM) for _ in range(n))
        if any(c.islower() for c in v) and any(c.isupper() for c in v) and any(c.isdigit() for c in v) and not any(b in v for b in ("AK", "gh", "sk", "eyJ", "LT")):
            return v


def failure(text):
    return {"session_id": "s", "transcript_path": "/x/t.jsonl", "cwd": "/x", "permission_mode": "default", "hook_event_name": "PostToolUseFailure",
            "tool_name": "Bash", "tool_input": {"command": "false"}, "tool_use_id": "toolu_1", "error": text, "is_interrupt": False, "duration_ms": 12}


def success(text, event="PostToolUse"):
    return {"session_id": "s", "transcript_path": "/x/t.jsonl", "cwd": "/x", "permission_mode": "default", "hook_event_name": event,
            "tool_name": "Bash", "tool_input": {"command": "cat x"}, "tool_use_id": "toolu_2",
            "tool_response": {"stdout": text, "stderr": "", "interrupted": False, "isImage": False, "noOutputExpected": False}, "duration_ms": 5}


AKIA = "AK" + "IA" + "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16))
cases = [
    ("failure: aws key id line", failure("Exit code 22\n" + AKIA)),
    ("failure: JWT_SECRET kv line", failure("Exit code 3\nJWT_" + "SECRET = " + alnum(43))),
    ("failure: curl -v echoed Authorization", failure("Exit code 22\n> Authorization: " + "tok" + "en " + "".join(secrets.choice("0123456789abcdef") for _ in range(40)))),
    ("failure: clean text", failure("Exit code 1\nls: cannot access 'x': No such file or directory")),
    ("failure: interrupted (is_interrupt true) + aws line", dict(failure("Exit code 130\n" + AKIA), is_interrupt=True)),
    ("failure: Read tool + aws line", dict(failure("File does not exist.\n" + AKIA), tool_name="Read", tool_input={"file_path": "/x/y"})),
    ("failure: NUL-delimited env records in error", failure("Exit code 2\nHOME=/x\u0000JWT_" + "SECRET=" + alnum(43) + "\u0000PATH=/bin")),
    ("failure: error text names the event + aws line", failure("hook_event_name PostToolUseFailure " + AKIA)),
    ("success: aws key id line", success(AKIA)),
    ("success: text MENTIONING the event name + aws line", success("hook_event_name\":\"PostToolUseFailure\" " + AKIA)),
]
for label, env in cases:
    row = []
    for h in hooks:
        p = subprocess.run(["bash", h], input=json.dumps(env).encode(), capture_output=True,
                           env={"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": home, "TMPDIR": work, "USER": "probe", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}, cwd=work, timeout=120)
        ev, tags = "-", "-"
        if p.stdout.strip():
            try:
                j = json.loads(p.stdout)
                ev = j["hookSpecificOutput"]["hookEventName"]
                m = re.search(r"\(([^)]*)\); rotate", j.get("systemMessage", ""))
                tags = m.group(1) if m else "?"
            except Exception as e:
                ev = "unparsable"
        row.append(f"rc={p.returncode} event={ev} tags={tags}")
    print(f"{label:52s} | " + " | ".join(row))
