#!/usr/bin/env python3
"""nc15.py ARIA_TREE -- negative control for SC-15 15e / 15f / 15g: append ONE runtime-assembled credential-shaped line to a private copy of each of the
three files (proposal.md, baseline_probe.py, baseline-evidence.md), run the copy of the probe on the SC-15 rows, print only the row status.
The shape is assembled from pieces here; nothing credential-shaped is printed or stored in the repository tree."""
import os
import re
import secrets
import shutil
import subprocess
import sys

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tree = sys.argv[1]
d = os.path.join(EXP, "work", "nc15")
shutil.rmtree(d, ignore_errors=True)
os.makedirs(d)
for f in ("baseline_probe.py", "proposal.md", "baseline-evidence.md"):
    shutil.copy(os.path.join(EXP, "spec", f), d)
line = '{"' + "tok" + 'en":"' + secrets.token_hex(20) + '"}\n'
for f in ("proposal.md", "baseline-evidence.md"):
    with open(os.path.join(d, f), "a", encoding="utf-8") as fh:
        fh.write("\n" + line)
with open(os.path.join(d, "baseline_probe.py"), "a", encoding="utf-8") as fh:
    fh.write("\n# " + line)
env = dict(os.environ, HOME=os.path.join(EXP, "home"), TMPDIR=os.path.join(EXP, "tmp"), WPA_ONLY="SC-15")
p = subprocess.run(["python3", os.path.join(d, "baseline_probe.py"), tree], capture_output=True, text=True, env=env, cwd=d)
for l in p.stdout.split("\n"):
    m = re.match(r"^SC-15 │ (15[efg]) │ (\S+) │ .* │ (.*) │ (yes|no|n/a)$", l)
    if m:
        print(m.group(1), m.group(2), "|", re.sub(r"\{[^}]*\}", "{tags}", m.group(3))[:60], "|", m.group(4))
print("rc", p.returncode, "stderr bytes", len(p.stderr))
shutil.rmtree(d, ignore_errors=True)
