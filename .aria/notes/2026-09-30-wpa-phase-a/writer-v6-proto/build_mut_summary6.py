#!/usr/bin/env python3
"""build_mut_summary6.py -- write out/mut_summary_v6.txt from mut/final6/*/SUMMARY.txt (the final campaign, run_final_campaign6.sh).

Part A   this round's bad implementations: plans work/plans6/*.tsv (L3 / L1 / hooks.json variants) and the document variants (patch_docs.py flags): every block, with the rows it turns red.
         Every bad implementation must turn at least one row red, or carry a reason below (EQUIV): a timing-class bad implementation is caught by a time tier, an equivalent mutant is argued.
Part B   regression of the earlier rounds' bad implementations (work/plans_v5, work/plans_v4, work/plans_v3) on THIS prototype.  Reference = the previous round's FINAL campaign result of the same
         plan and label (a copy of that round's mut/final5/<plan>/SUMMARY.txt; every row that was red there must still be red now).  A row that is red now and was not red then is reported as `+ more rows`.
Exit 1 on any regression, patch / probe error, unexplained zero-red bad implementation or missing plan."""
import os
import re
import sys

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREV = os.environ.get("WPA_PREV_CAMPAIGN", "/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v5/mut/final5")
FIN = os.path.join(EXP, "mut", "final6")
EQUIV, SUPERSEDED = {}, {}
exec(open(os.path.join(EXP, "proto", "equiv_reasons6.py"), encoding="utf-8").read())

SUPERSEDED_PREFIX = {"drop_extreader_": ("An earlier design gave the extension a reader table of its own (29 print readers + python3 -c + node -e), so 'a member is missing from the extension's reader table' was a bad "
                                         "implementation of its own.  The present design has no such table: the extension judges the substituted copy with the BUILT-IN app.ini rows, so there is nothing to drop.  "
                                         "The same drop in the built-in reader set is `drop_reader:*` (previous rounds' plan_v5_l1), which turns 16q AND 19u red for every member.")}
A_PLANS = ["plan_v6_l3", "plan_v6_hj", "plan_v6_l1"]
B_PLANS = [("v5", ["plan_v5_l3", "plan_v5_l1", "plan_v5_l1b", "plan_v5_l1c", "plan_v5_b32"]),
           ("v4", ["plan_v4_l3", "plan_v4_l1_w9w10w12", "plan_v4_l1_w11w8", "plan_v4_l1_charsem", "plan_v4_l1_w12", "plan_v4_l1_evals", "plan_v4_l1_redo", "plan_v4_b32"]),
           ("v3", ["v3r_plan_l3_wl", "v3r_plan_l3_w4w5", "v3r_plan_l3_enum", "v3r_plan_l1_w8w9w10", "v3r_plan_l1_w11", "v3r_plan_extra", "v3r_plan_repeat", "v3r_plan_extra4", "v3r_plan_vsym",
                  "v3r_plan_extra2_b32"])]
ROW = re.compile(r"(?m)^   (SC-\d+) (\S+) \|")


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
        label = head.split(" (variant ", 1)[0]
        red = {(m.group(1), m.group(2)) for m in ROW.finditer(b)}
        err = "PATCH-FAILED" in b or "PROBE-ERROR" in b or "BUILD-FAILED" in b
        m = re.search(r"\(rows not yes: (\d+)\)", b)
        out.append((label, head, b, red, err, int(m.group(1)) if m else -1))
    return out


fmt = lambda s: " ".join(f"{sc[3:]}:{r}" for sc, r in sorted(s, key=lambda t: (int(t[0][3:]), t[1]))) or "-"
problems, lines_a, lines_b = [], [], []
sup_count = {}
a_total = a_zero = 0
zero = []
for p in A_PLANS + ["doc"]:
    f = os.path.join(FIN, p, "SUMMARY.txt")
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
    lines_a.append(f"##### {p}  ({len(bl)} bad implementations, {len(bl) - len(z)} turn at least one row red, {len(z)} turn none)\n")
    lines_a.extend("== " + b[2].rstrip("\n") + "\n" for b in bl)
    for b in z:
        zero.append((p, b[0]))
        if p == "doc":
            if b[0] not in ("doc_none",):
                problems.append(("document variant turned no row red", p, b[0]))
        elif lookup(b[0]) is None:
            problems.append(("UNEXPLAINED zero-red", p, b[0]))
# ---------------------------------------------------------------- B: regression against the previous round's final campaign
stat = {}
for rnd, plans in B_PLANS:
    tot = kept = lost = equiv = more = nowred = 0
    for p in plans:
        f_now, f_prev = os.path.join(FIN, p, "SUMMARY.txt"), os.path.join(PREV, p, "SUMMARY.txt")
        if not os.path.isfile(f_now):
            print("MISSING", f_now)
            sys.exit(2)
        if not os.path.isfile(f_prev):
            print("MISSING reference", f_prev)
            sys.exit(2)
        prev = {b[0]: b for b in blocks_of(f_prev)}
        for label, head, b, red, err, cnt in blocks_of(f_now):
            tot += 1
            if err or cnt < 0:
                problems.append(("ERROR RESULT", p, label))
                continue
            pref = next((k for k in SUPERSEDED_PREFIX if label.startswith(k)), None)
            if pref:
                sup_count[pref] = sup_count.get(pref, 0) + 1
                tot -= 1
                continue
            old = prev.get(label)
            if old is None:
                problems.append(("NO REFERENCE BLOCK", p, label))
                continue
            was = old[3]
            if was:
                missing = was - red
                if missing:
                    lost += 1
                    problems.append(("REGRESSION", p, label + " lost " + fmt(missing)))
                    status = "REGRESSION"
                else:
                    kept += 1
                    status = "preserved" + ("" if red == was else " (+ more rows)")
                    more += int(red != was)
                lines_b.append(f"  {p:22s} {label:36s} red now: {fmt(red)[:110]:110s} | red before: {fmt(was)[:110]}  [{status}]")
            else:
                equiv += 1
                nowred += int(bool(red))
                if not red and lookup(label) is None:
                    problems.append(("UNEXPLAINED zero-red (equivalent before)", p, label))
                if not red:
                    zero.append((p, label))
                lines_b.append(f"  {p:22s} {label:36s} red now: {fmt(red)[:110]:110s} | red before: -  [equivalent before{'; still no row red' if not red else '; NOW RED (more discriminating)'}]")
    stat[rnd] = (tot, kept, lost, equiv, more, nowred)
hdr = [
    "mut_summary_v6 -- the bad implementations of this round and the regression runs of the earlier rounds' bad implementations, on the final prototype",
    "",
    "Method: each bad implementation = the full final target prototype tree (work/t6) with ONE hook replaced by a variant produced by patch_l3.py / patch_l1.py (--variant), or with hooks.json produced by",
    "patch_hooks_json.py (--variant), or with the DOCUMENTS patched by a patch_docs.py flag; only the SC groups / rows named for it are run (proto/mutbatch.py, proto/docvariants6.py); a listed row is a row whose match",
    "is not `yes`.  The prototype is a text-substituted copy of the baseline, not the implementation (see README.md).  Regression reference = the previous round's final campaign result of the same plan and label.",
    "",
    f"PART A  -- this round: {a_total} bad implementations; {a_total - a_zero} turn at least one row red; {a_zero} turn no row red (reasons below).",
]
for rnd, label in (("v5", "the previous round's"), ("v4", "the round before's"), ("v3", "the rounds before that")):
    t = stat[rnd]
    hdr.append(f"PART B ({rnd}) -- regression of {label} bad implementations: {t[0]} re-run; {t[1]} keep every row that was red before ({t[4]} of them with more rows red than before); {t[2]} lose a row (regressions); {t[3]} were equivalent before ({t[5]} of them are red now).")
hdr += ["", "Superseded (no counterpart in the present design; listed, not judged):"]
hdr += [f"  {k}* ({sup_count.get(k, 0)} bad implementations): {v}" for k, v in SUPERSEDED_PREFIX.items()]
hdr += ["", "Bad implementations that turned NO row red:"]
for p, label in zero:
    hdr.append(f"  {p} / {label}: {lookup(label) or '!!! NO REASON GIVEN !!!'}")
if not zero:
    hdr.append("  (none)")
hdr += ["", "=" * 100, "", "PART A -- blocks", ""]
body = ("\n".join(hdr) + "\n" + "".join(lines_a) + "\n" + "=" * 100 + "\n\nPART B -- one line per bad implementation of the earlier rounds (rows are `SC-number:row`)\n\n" + "\n".join(lines_b) + "\n")
os.makedirs(os.path.join(EXP, "out"), exist_ok=True)
open(os.path.join(EXP, "out", "mut_summary_v6.txt"), "w", encoding="utf-8").write(body)
print("written out/mut_summary_v6.txt; PART A:", a_total, "run,", a_total - a_zero, "red,", a_zero, "no-row-red |", " | ".join(f"PART B {r}: {s[0]} run, {s[1]} preserved ({s[4]} with more rows), {s[2]} regressions, {s[3]} equivalent-before ({s[5]} red now)" for r, s in stat.items()))
for pr in problems:
    print("  PROBLEM", pr)
sys.exit(1 if problems else 0)
