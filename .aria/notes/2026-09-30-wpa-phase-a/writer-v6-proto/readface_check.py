#!/usr/bin/env python3
"""readface_check.py -- SC-18 18j / 18k path table: every path must match EXACTLY ONE of the 32 alternatives of the baseline Read / Edit path regex
(secret-guard.sh, the `grep -qE` on the lower-cased file_path), and it must be the one it is listed for.  Reads the regex from the baseline hook and the
(label, path) table from the probe source, so the two cannot drift."""
import re
import subprocess
import sys

hook, probe = sys.argv[1], sys.argv[2]
src = open(hook, encoding="utf-8").read()
m = re.search(r"grep -qE '(\\\.env\(.*?)'; then", src)
alts = m.group(1).split("|")
assert len(alts) == 32, len(alts)
ptxt = open(probe, encoding="utf-8").read()
tab = re.search(r"READ_ALT_PATHS = \[(.*?)\n\]", ptxt, re.S).group(1)
rows = re.findall(r'\("([a-z0-9_-]+)", "([^"]+)"\)', tab)
assert len(rows) == 32, len(rows)
bad = 0
for i, (lab, path) in enumerate(rows):
    lp = path.lower()
    hits = [j for j, a in enumerate(alts) if subprocess.run(["grep", "-qE", "--", a], input=lp.encode()).returncode == 0]
    ok = hits == [i]
    bad += not ok
    if not ok:
        print(f"MISMATCH alt#{i + 1} {lab} {path}: matches alternatives {[h + 1 for h in hits]}")
print(f"{len(rows)} paths, {bad} not unique/in-place")
sys.exit(1 if bad else 0)
