#!/usr/bin/env python3
"""build_mut_summary.py -- write work/archive/mut_summary_v4.txt from mut/final/*/SUMMARY.txt.

Part A  this round's bad implementations (plans/): every block, with the rows it turns red.
Part B  regression run of the PREVIOUS round's bad implementations on the v4 prototype (plans_v3r/: only the rows that were red in v3 are run; see work/mk_refined_v3_plans.py):
        one line per bad implementation: rows red now / rows red in v3 / status, and the per-plan tally.
Every bad implementation that turned NO row red must carry an equivalence reason from EQUIV (work/equiv_reasons.py), otherwise the script exits 1.
Exit 1 also on any regression (a row red in v3 that is no longer red), any patch / probe error, or a missing plan."""
import os
import re
import sys

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V3 = "/home/dev/Aria/.aria/notes/2026-09-30-wpa-phase-a/writer-v3-proto/mut_summary_v3.txt"
EQUIV, SUPERSEDED = {}, {}
exec(open(os.path.join(EXP, "work", "equiv_reasons.py"), encoding="utf-8").read())
A_PLANS = ["plan_v4_l3", "plan_v4_l1_w9w10w12", "plan_v4_l1_charsem", "plan_v4_l1_w11w8", "plan_v4_b32"]
B_PLANS = ["plan_extra", "plan_extra4", "plan_repeat", "plan_vsym", "plan_l3_wl", "plan_l3_w4w5", "plan_l3_enum", "plan_l1_w8w9w10", "plan_l1_w11", "plan_extra2_b32"]


def lookup(label):
    if label in EQUIV:
        return EQUIV[label]
    for k, v in EQUIV.items():
        if k.endswith("*") and label.startswith(k[:-1]):
            return v
    return None


def blocks_of(path):
    text = open(path, encoding="utf-8").read()
    out = []
    for b in re.split(r"(?m)^== ", text)[1:]:
        head = b.split("\n", 1)[0]
        label = head.split(" ", 1)[0]
        red = [(m.group(1), m.group(2)) for m in re.finditer(r"(?m)^   (SC-\d+) (\S+) \|", b)]
        err = "PATCH-FAILED" in b or "PROBE-ERROR" in b
        m = re.search(r"\(rows not yes: (\d+)\)", b)
        out.append((label, head, b, red, err, int(m.group(1)) if m else -1))
    return out


problems = []
txt = []
# ---------------------------------------------------------------- Part A
a_total = a_zero = 0
a_lines = []
for p in A_PLANS:
    f = os.path.join(EXP, "mut", "final", p, "SUMMARY.txt")
    if not os.path.isfile(f):
        print("MISSING", f)
        sys.exit(2)
    bl = blocks_of(f)
    z = [b for b in bl if b[5] == 0]
    for b in bl:
        if b[4] or b[5] < 0:
            problems.append(("ERROR RESULT", p, b[0]))
    a_total += len(bl)
    a_zero += len(z)
    a_lines.append(f"##### {p}  ({len(bl)} bad implementations, {len(bl) - len(z)} turn at least one row red, {len(z)} turn none)\n")
    a_lines.extend("== " + b[2].rstrip("\n") + "\n" for b in bl)
    for b in z:
        if lookup(b[0]) is None:
            problems.append(("UNEXPLAINED zero-red", p, b[0]))
# ---------------------------------------------------------------- Part B
v3 = {}
plan = None
for chunk in re.split(r"(?m)^(?=##### |== )", open(V3, encoding="utf-8").read()):
    if chunk.startswith("##### "):
        plan = chunk.split()[1]
    elif chunk.startswith("== ") and plan:
        label = chunk[3:].split(" ", 1)[0]
        v3[(plan, label)] = sorted({(m.group(1), m.group(2)) for m in re.finditer(r"(?m)^   (SC-\d+) (\S+) \|", chunk)}, key=lambda t: (int(t[0][3:]), t[1]))
b_total = b_pres = b_reg = b_zero = 0
b_lines, b_tally = [], []
for p in B_PLANS:
    f = os.path.join(EXP, "mut", "final", "v3r_" + p, "SUMMARY.txt")
    if not os.path.isfile(f):
        print("MISSING", f)
        sys.exit(2)
    n = pres = reg = zero = 0
    for label, head, b, red, err, cnt in blocks_of(f):
        n += 1
        if err or cnt < 0:
            problems.append(("ERROR RESULT", "v3r_" + p, label))
            continue
        old = v3.get((p, label))
        if old is None:
            problems.append(("NO v3 BLOCK", "v3r_" + p, label))
            continue
        now = set(red)
        fmt = lambda s: " ".join(f"{sc[3:]}:{r}" for sc, r in sorted(s, key=lambda t: (int(t[0][3:]), t[1]))) or "-"
        if old:
            missing = set(old) - now
            if missing:
                reg += 1
                problems.append(("REGRESSION", "v3r_" + p, label + " lost " + fmt(missing)))
                status = "REGRESSION"
            else:
                pres += 1
                status = "preserved" + ("" if now == set(old) else " (+ more rows)")
            b_lines.append(f"  {p:16s} {label:42s} red now: {fmt(now)[:110]:110s} | red in v3: {fmt(old)[:110]}  [{status}]")
        else:
            zero += 1
            why = lookup(label)
            if why is None:
                problems.append(("UNEXPLAINED zero-red (v3 equivalent)", "v3r_" + p, label))
            b_lines.append(f"  {p:16s} {label:42s} red now: {fmt(now)[:110]:110s} | red in v3: -  [equivalent in v3{'; still no row red' if not now else '; NOW RED (more discriminating)'}]")
    b_tally.append((p, n, pres, reg, zero))
    b_total += n
    b_pres += pres
    b_reg += reg
    b_zero += zero
hdr = [
    "mut_summary_v4 -- the bad implementations of the v4 round and the regression run of the v3 bad implementations, on the v4 prototype",
    "",
    "Method: each bad implementation = the full v4 target prototype tree (work/t4f) with ONE hook replaced by a variant produced by patch_l3.py / patch_l1.py (--variant);",
    "only the SC groups / rows named for it are run (proto/mutbatch.py); a listed row is a row whose match is not `yes`.  The prototype is a text-substituted copy of the",
    "baseline, not the implementation (see README.md).  Plans: plans/*.tsv (this round), plans_v3r/*.tsv (the previous round's, refined to the rows that were red in v3).",
    "",
    f"PART A -- this round: {a_total} bad implementations; {a_total - a_zero} turn at least one row red; {a_zero} turn no row red (equivalent mutants, reasons below).",
    "PART B -- regression: %d bad implementations of the previous round re-run on the v4 prototype; %d keep every row that was red in v3; %d lose a row (regressions); %d were equivalent in v3 (reasons below)."
    % (b_total, b_pres, b_reg, b_zero),
    "",
    "PART B tally:  %-16s %5s %9s %11s %12s" % ("plan", "run", "preserved", "regressions", "zero-red(v3)"),
]
for p, n, pres, reg, zero in b_tally:
    hdr.append("               %-16s %5d %9d %11d %12d" % (p, n, pres, reg, zero))
hdr += ["", "Bad implementations that turned NO row red (equivalent mutants: the mutated program behaves exactly like the correct one on every input the rows can build, so there is nothing to catch):", ""]
seen = set()
for plan_name, lines in (("A", a_lines), ("B", b_lines)):
    pass
zero_list = []
for p in A_PLANS:
    for b in blocks_of(os.path.join(EXP, "mut", "final", p, "SUMMARY.txt")):
        if b[5] == 0:
            zero_list.append((p, b[0]))
for p in B_PLANS:
    for label, head, b, red, err, cnt in blocks_of(os.path.join(EXP, "mut", "final", "v3r_" + p, "SUMMARY.txt")):
        if cnt == 0 and not v3.get((p, label)):
            zero_list.append(("v3r_" + p, label))
for p, label in zero_list:
    hdr.append(f"  {p} / {label}: {lookup(label) or '!!! NO REASON GIVEN !!!'}")
if not zero_list:
    hdr.append("  (none)")
hdr += ["", "=" * 100, "", "PART A -- blocks", ""]
body = "\n".join(hdr) + "\n" + "".join(a_lines) + "\n" + "=" * 100 + "\n\nPART B -- one line per bad implementation of the previous round (rows are `SC-number:row`)\n\n" + "\n".join(b_lines) + "\n"
os.makedirs(os.path.join(EXP, "work", "archive"), exist_ok=True)
open(os.path.join(EXP, "work", "archive", "mut_summary_v4.txt"), "w", encoding="utf-8").write(body)
print("written; PART A:", a_total, "run,", a_total - a_zero, "red,", a_zero, "no-row-red | PART B:", b_total, "run,", b_pres, "preserved,", b_reg, "regressions,", b_zero, "zero-red (v3 equivalents)")
for pr in problems:
    print("  PROBLEM", pr)
sys.exit(1 if problems else 0)
