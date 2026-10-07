#!/usr/bin/env python3
"""manifest6.py -- (re)write deliver/MANIFEST.sha256 (sha256sum format, relative paths, every file under deliver/ except the manifest itself)."""
import hashlib
import os

DEL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "deliver")
lines = []
for r, _d, fs in os.walk(DEL):
    for f in fs:
        if f == "MANIFEST.sha256":
            continue
        p = os.path.join(r, f)
        lines.append(f"{hashlib.sha256(open(p, 'rb').read()).hexdigest()}  {os.path.relpath(p, DEL)}")
lines.sort(key=lambda s: s.split("  ", 1)[1])
open(os.path.join(DEL, "MANIFEST.sha256"), "w").write("\n".join(lines) + "\n")
print("MANIFEST.sha256:", len(lines), "files")
