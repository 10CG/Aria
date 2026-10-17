#!/usr/bin/env python3
"""family_scan.py -- the mechanical part of the same-family scan of the repair report (out/family_scan.txt):

  A. every place of the proposal that hands a residual risk to L3 ("交给 L3", "L3 兜底", "输出侧", "事后兜底" ...): does the sentence say that failed calls are covered too (`失败`)?
  B. every `#` / `##` / `%` / `%%` parameter-expansion deletion in the L3 prototype and in the L1 prototype (beyond the baseline), with the line number
  C. every place that names the SC-8 / SC-9a test blocks (the extraction assembly belongs to SC-8 only)
  D. every `基线 N/M` count of the proposal's Why table and W11 现状 against the probe's own tally (rows of the category `baseline-failing` per SC)
Only text and counts are printed."""
import collections
import os
import re
import sys

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
prop = open(os.path.join(EXP, "spec", "proposal.md"), encoding="utf-8").read()
out = []

out.append("== A. residual risk handed to L3")
pat = re.compile(r"交给 L3|L3 兜底|输出侧由|输出侧兜底|事后兜底|由 L3 (?:检出|兜底)|L3 在输出侧")
for m in pat.finditer(prop):
    line_no = prop.count("\n", 0, m.start()) + 1
    s = prop[max(0, m.start() - 70):m.end() + 90].replace("\n", " ")
    ctx = prop[max(0, m.start() - 160):m.end() + 160]
    out.append(f"  line {line_no:3d} [{'covers failed calls' if ('失败' in ctx) else 'no mention of failed calls'}] ...{s}...")

out.append("")
out.append("== B. parameter-expansion deletions (`#` `##` `%` `%%`) in the prototype hooks (comment lines skipped)")
rx = re.compile(r"\$\{[A-Za-z_][A-Za-z0-9_]*(?:#|##|%|%%)[^}]*\}")
for name, rel in (("L3 baseline", "base/aria/hooks/secret-scan.sh"), ("L3 target", "work/t6/aria/hooks/secret-scan.sh"), ("L1 baseline", "base/aria/hooks/secret-guard.sh"), ("L1 target", "work/t6/aria/hooks/secret-guard.sh")):
    sites = []
    for i, l in enumerate(open(os.path.join(EXP, rel), encoding="utf-8").read().split("\n"), 1):
        if l.lstrip().startswith("#"):
            continue
        for m in rx.finditer(l):
            sites.append((i, m.group(0)))
    out.append(f"  {name}: {len(sites)} site(s)")
    for i, e in sites:
        out.append(f"      {i:5d}: {e}")

out.append("")
out.append("== C. SC-8 / SC-9a")
for m in re.finditer(r"SC-8 / SC-9a|SC-9a / SC-8|SC-9a", prop):
    line_no = prop.count("\n", 0, m.start()) + 1
    out.append(f"  line {line_no:3d} ...{prop[max(0, m.start() - 50):m.end() + 60]}...".replace("\n", " "))

out.append("")
out.append("== D. baseline-failing row counts per SC against the probe's tally")
tally = collections.Counter()
po = os.path.join(EXP, "out", "probe_target.out")
if os.path.exists(po):
    for l in open(po, encoding="utf-8"):
        m = re.match(r"^(SC-\d+) │ (\S+) │ (\S+) │", l)
        if m and m.group(3) == "baseline-failing":
            tally[m.group(1)] += 1
    for sc in sorted(tally, key=lambda s: int(s[3:])):
        m = re.search(r"\*\*" + re.escape(sc) + r"\*\* \((?:W[0-9 /,]+\)?: )?\(?`baseline-failing` ×(\d+)", prop) or re.search(r"\*\*" + re.escape(sc) + r"\*\*[^\n]{0,60}?`baseline-failing` ×(\d+)", prop)
        out.append(f"  {sc}: probe {tally[sc]} | proposal bullet {m.group(1) if m else '(no x-count in the bullet head)'}")
else:
    out.append("  (out/probe_target.out missing)")
txt = "\n".join(out) + "\n"
open(os.path.join(EXP, "out", "family_scan.txt"), "w", encoding="utf-8").write(txt)
print(txt)
