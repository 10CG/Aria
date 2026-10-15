#!/usr/bin/env python3
"""mask_cost.py: CPU cost of the quote mask (_sg_ext_mask), which runs only when the command mentions a listed path.
usage: python3 mask_cost.py <hook with mask> <hook without mask (ext_nomask)> <project dir>   -- interleaved, 5 pairs, minimum CPU (user+sys of all children)"""
import json
import os
import resource
import subprocess
import sys
import tempfile

hk_a, hk_b, proj = sys.argv[1:4]
home = tempfile.mkdtemp(prefix="mc-", dir=os.environ.get("TMPDIR"))
ENV = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": home, "TMPDIR": home, "USER": "probe", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "CLAUDE_PROJECT_DIR": proj}
P = "/srv/billing/conf/prod.toml"


def cpu(hook, cmd):
    r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    subprocess.run(["bash", hook], input=json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}}).encode(), capture_output=True, env=ENV, timeout=600)
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    return (r1.ru_utime - r0.ru_utime) + (r1.ru_stime - r0.ru_stime)


for n in (300, 1000, 4000):
    filler = ("echo 'filler text with a quote' ; " * 200)[: n - len(P) - 8]
    cmd = filler + " cat " + P
    a = [cpu(hk_a, cmd) for _ in range(1)]  # warm
    A, B = [], []
    for _ in range(5):
        A.append(cpu(hk_a, cmd))
        B.append(cpu(hk_b, cmd))
    print(f"command {len(cmd):5d} B with a listed path: CPU min  with mask {min(A):.3f}s  without {min(B):.3f}s  delta {min(A) - min(B):+.3f}s")
    cmd2 = filler + " cat /x/other.txt"
    A, B = [], []
    for _ in range(5):
        A.append(cpu(hk_a, cmd2))
        B.append(cpu(hk_b, cmd2))
    print(f"command {len(cmd2):5d} B WITHOUT a listed path: CPU min  with mask {min(A):.3f}s  without {min(B):.3f}s  delta {min(A) - min(B):+.3f}s")
