#!/usr/bin/env python3
"""build_mut_summary.py -- concatenate mut/plan_*/SUMMARY.txt into work/archive/mut_summary_v3.txt.

* blocks whose label is in SUPERSEDED (stale first-pass results: the variant, the probe or the harness was fixed afterwards) are NOT part of the totals and are
  replaced by a one-line note naming the run that supersedes them;
* every remaining bad implementation that turned NO row red must carry an equivalence reason from EQUIV (work/equiv_reasons.py), otherwise the script exits 1."""
import os
import re
import sys

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLANS = ["plan_l3_wl", "plan_l3_w4w5", "plan_l3_enum", "plan_l1_w8w9w10", "plan_l1_w11", "plan_extra", "plan_extra_b32", "plan_repeat", "plan_extra2_b32", "plan_vsym", "plan_extra4"]
EQUIV = {}
SUPERSEDED = {}
exec(open(os.path.join(EXP, "work", "equiv_reasons.py"), encoding="utf-8").read())


def lookup(table, label, plan=""):
    for key in ((plan + "/" + label), label):
        if key in table:
            return table[key]
    for k, v in table.items():
        pre = k[:-1] if k.endswith("*") else None
        if pre is not None and ((plan + "/" + label).startswith(pre) or label.startswith(pre)):
            return v
    return None


out = []
tot = zero_n = 0
zeros, perplan, dropped = [], [], []
for p in PLANS:
    f = os.path.join(EXP, "mut", p, "SUMMARY.txt")
    if not os.path.exists(f):
        print("MISSING", f)
        sys.exit(2)
    text = open(f, encoding="utf-8").read()
    blocks = re.split(r"(?m)^== ", text)[1:]
    n = z = 0
    kept = []
    for b in blocks:
        head = b.split("\n", 1)[0]
        label = head.split(" ", 1)[0]
        why_sup = lookup(SUPERSEDED, label, p)
        if why_sup is not None:
            dropped.append((p, label, why_sup))
            continue
        m = re.search(r"\(rows not yes: (\d+)\)", b)
        if not m:
            print("NO COUNT LINE in", p, label)
            sys.exit(2)
        if "PATCH-FAILED" in b or "PROBE-ERROR" in b:
            print("ERROR RESULT in", p, label)
            sys.exit(2)
        n += 1
        if int(m.group(1)) == 0:
            z += 1
            zeros.append((p, label))
        kept.append("== " + b.rstrip("\n") + "\n")
    perplan.append((p, n, n - z, z))
    tot += n
    zero_n += z
    out.append(f"##### {p}  ({n} bad implementations, {n - z} turn at least one row red, {z} turn none)\n")
    out.extend(kept)
hdr = [
    "mut_summary_v3 -- every bad implementation of the v3 mutation campaign and the probe rows it turns red",
    "",
    "Method: each bad implementation = the full v3 target prototype with ONE hook replaced by a variant produced by patch_l3.py / patch_l1.py (--variant);",
    "only the SC groups / rows named for it are run (proto/mutbatch.py, plans in plans/*.tsv); a listed row is a row whose match is not `yes`.",
    "Variant families: boundary (prefix / suffix / loose / no end anchor), missing-member (drop one member of an enumeration), over-reach (a removed or wider class re-added),",
    "off-by-one (every upper bound with N-1 / N+1).  The prototype is a text-substituted copy of the baseline, not the implementation (see README.md).",
    "",
    f"Totals (superseded first-pass blocks excluded): {tot} bad implementations; {tot - zero_n} turn at least one row red; {zero_n} turn no row red (equivalent mutants, listed below).",
]
for p, n, r, z in perplan:
    hdr.append(f"  {p:18s} {n:4d} run, {r:4d} red, {z:3d} no row red")
hdr += ["", f"Superseded first-pass results ({len(dropped)} blocks left out of the totals and of the text below; the replacing run is named):", ""]
_by_reason = {}
for p, label, why in dropped:
    _by_reason.setdefault(why, []).append(f"{p}/{label}")
for why, labels in _by_reason.items():
    hdr.append(f"  - {why}")
    hdr.append(f"    labels ({len(labels)}): " + ", ".join(labels))
hdr += ["", "Bad implementations that turned NO row red (equivalent mutants: the mutated program behaves exactly like the correct one on every input the rows can build, so there is nothing to catch):", ""]
missing = []
for p, label in zeros:
    why = lookup(EQUIV, label, p)
    if why is None:
        missing.append((p, label))
        why = "!!! NO REASON GIVEN !!!"
    hdr.append(f"  {p} / {label}: {why}")
if not zeros:
    hdr.append("  (none)")
hdr += ["", "=" * 100, ""]
open(os.path.join(EXP, "work", "archive", "mut_summary_v3.txt"), "w", encoding="utf-8").write("\n".join(hdr) + "\n".join(out))
print("written; totals:", tot, "run,", tot - zero_n, "red,", zero_n, "no-row-red; superseded blocks:", len(dropped), "; unexplained:", len(missing))
for m in missing:
    print("  UNEXPLAINED", m)
sys.exit(1 if missing else 0)
