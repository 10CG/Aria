#!/usr/bin/env python3
"""scale_try.py <hook secret-scan.sh> <shape> <kb> [<kb> ...] -- total CPU (user+sys of the hook and all its children, via RUSAGE_CHILDREN) of one run per size, for the shapes of cap_probe.py.
Only numbers are printed.  Rule #7: values are generated at run time."""
import json
import os
import resource
import subprocess
import sys
import tempfile

hook = os.path.abspath(sys.argv[1])
shape = sys.argv[2]
sizes = [int(a) for a in sys.argv[3:]]
sys.argv = ["cap_probe.py", hook, shape, "1"]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cap_probe.py"), encoding="utf-8").read()
# reuse the case table of cap_probe.py (it builds the payload at import time for size 1 KB; rebuilt below per size)
work = tempfile.mkdtemp(prefix="sc-")
home = os.path.join(work, "home")
os.makedirs(home)
ENV = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": home, "TMPDIR": work, "USER": "probe", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
cut = src.index("text, tag = CASES[shape]")
for kb in sizes:
    sys.argv = ["cap_probe.py", hook, shape, str(kb)]
    g = {"__name__": "capprobe_prefix"}
    exec(compile(src[:cut], "cap_probe.py", "exec"), g)
    text, tag = g["CASES"][shape]
    env_obj = {"tool_name": "Bash", "tool_input": {"command": "x"}, "tool_response": {"stdout": text, "stderr": "", "interrupted": False, "isImage": False, "noOutputExpected": False}}
    payload = json.dumps(env_obj).encode()
    r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    p = subprocess.run(["bash", hook], input=payload, capture_output=True, env=ENV, cwd=work, timeout=900)
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    cpu = (r1.ru_utime - r0.ru_utime) + (r1.ru_stime - r0.ru_stime)
    seen = tag.encode() in p.stdout
    print(f"{shape:28s} {kb:5d} KB  cpu {cpu:6.2f} s  tag={'yes' if seen else 'NO'}", flush=True)
