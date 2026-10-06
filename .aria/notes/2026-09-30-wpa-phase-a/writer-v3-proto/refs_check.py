#!/usr/bin/env python3
"""exercise the keyword check of the Impact section: positives must match (rc 0, output), negatives must not (rc 1, no output)"""
import subprocess

RX = r"(^|[^[:alnum:]_])(close[sd]?|fix(e[sd])?|resolve[sd]?)[[:space:]:]+(https?://[^[:space:]]*/issues/|[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+#|#)(154|203|221)([^0-9]|$)"
POS = ["Closes #154", "closes #203", "Fixes 10CG/aria-plugin#154", "fixed: #221", "Resolves 10CG/Aria#221", "close https://forgejo.example/10CG/Aria/issues/221",
       "fix #154.", "Closed #203", "RESOLVED #221", "Closes: 10CG/aria-plugin#203", "feat: x\n\nCloses #154\n"]
NEG = ["Refs 10CG/aria-plugin#154", "Refs #203", "see #154", "Closes #1540", "Closes #15", "refs: 10CG/Aria#221", "closest to #154", "prefix #154 mentioned",
       "Closes #12345", "Fixes #2210", "Closes 10CG/Aria#999", ""]
bad = 0
for t in POS + NEG:
    p = subprocess.run(["grep", "-niE", RX], input=t.encode(), capture_output=True)
    hit = p.returncode == 0
    want = t in POS
    flag = "" if hit == want else "   <== WRONG"
    bad += (hit != want)
    print(("MATCH " if hit else "no    "), repr(t)[:70], flag)
print("wrong:", bad)
