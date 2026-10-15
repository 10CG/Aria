#!/usr/bin/env python3
"""build_mut_summary5.py -- write out/mut_summary_v5.txt from mut/final5/*/SUMMARY.txt (the final campaign, run_final_campaign5.sh).

Part A   this round's bad implementations: plans work/plans5/*.tsv (hook variants) and the document variants (patch_docs.py flags): every block, with the rows it turns red.
Part B1  regression of the PREVIOUS round's bad implementations (work/plans/plan_v4_*.tsv) on this prototype: every row that was red under the previous prototype must still be red now
         (reference = the previous round's summary, proto/mut_summary_v4.txt, Part A blocks).  The 7 whose design no longer exists are listed as superseded, with the variant that replaces them.
Part B2  regression of the rounds before (work/plans_v3/*.tsv, refined to the rows that were red then): same rule, reference = the v3 summary (full blocks).
Every bad implementation that turned NO row red must carry a reason (EQUIV below / equiv_reasons.py), otherwise the script exits 1.  Exit 1 also on any regression, patch / probe error or missing plan."""
import os
import re
import sys

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V4 = os.path.join(EXP, "proto", "mut_summary_v4.txt")
V3 = "/home/dev/Aria/.aria/notes/2026-09-30-wpa-phase-a/writer-v3-proto/mut_summary_v3.txt"
if not os.path.exists(V3):
    V3 = os.path.join(EXP, "proto", "mut_summary_v3.txt")
EQUIV, SUPERSEDED = {}, {}
exec(open(os.path.join(EXP, "proto", "equiv_reasons.py"), encoding="utf-8").read())

_ENVWRAP5 = ("The mutated program behaves exactly like the correct one: the baseline already has its own, older rules that block `<this wrapper> ... env` / `... printenv` (docker / kubectl / podman / lxc exec) "
             "WITH the default credit (an anchored `grep` / `cut` / `wc` after the dump is a filter), and the wrapped-dump alternative of this change uses the same credit, so removing the wrapper from the NEW "
             "alternation changes the verdict of no input -- not on the plain dump (22bo), not with the legitimate filters (22br) and not with `grep -v` (22bs).  The wrappers whose removal IS observable "
             "(ssh, sh -c / bash -c, watch, nomad alloc exec, pct exec) are the ones the baseline misses, and each turns 22bo red.")
EQUIV.update({"remote_env_split_docker": _ENVWRAP5, "remote_env_split_kubectl": _ENVWRAP5, "remote_env_split_podman": _ENVWRAP5, "remote_env_split_lxc": _ENVWRAP5,
              "ext_perentry": ("A TIMING-class bad implementation: one grep process per extension entry computes exactly the same verdicts as the single `grep -f` pass, so no functional row can be red; "
                                              "it is caught by the time tier (f) (see out/timing_bad.txt: the ratio is about ten times the bound) and by nothing else.")})
SUPERSEDED.update({k: ("The previous design put a hand-written quote mask in front of a hand-written stage cut; this design has neither (the extension substitutes the built-in app.ini name and calls the built-in "
                       "`_sg_core_eval`), so a bad implementation OF THE MASK has no counterpart.  The class stays alive as `ext_v4stage` and its five sub-variants (:noesc_q :noesc_all :noansi :nopipe :nonl): "
                       "each turns 19af red (19z too for :nonl), see Part A.") for k in ("ext_nomask", "ext_mask_nosemi", "ext_mask_noamp", "ext_mask_nopipe", "ext_mask_nonl", "ext_mask_all")})
SUPERSEDED["ext_uniclass"] = ("The previous entry rule needed a letter or digit of the caller's locale class; the entry rule now is 'an ASCII letter or digit, or any non-ASCII byte' under an exported LC_ALL=C.  "
                              "The locale-dependent classes are covered by `ext_noc`, `ext_charlen`, `ext_ascii_only` and `ext_localnoexp` (19ad 19ae 19ag 19ah 19am), see Part A.")

SUPERSEDED_PREFIX = {"drop_extreader_": ("The previous design gave the extension a reader table of its own (29 print readers + python3 -c + node -e), so 'a member is missing from the extension's reader table' was a bad "
                                         "implementation of its own.  This design has no such table: the extension judges the substituted copy with the BUILT-IN app.ini rows, so there is nothing to drop.  "
                                         "The same drop in the built-in reader set is `drop_reader:*` (same plan), which turns 16q AND 19u red for every member (19u runs the 31 readers through the extension).")}
A_PLANS = ["plan_v5_l3", "plan_v5_l1", "plan_v5_l1b", "plan_v5_l1c", "plan_v5_b32"]
B1_PLANS = ["plan_v4_l3", "plan_v4_l1_w9w10w12", "plan_v4_l1_charsem", "plan_v4_l1_w11w8", "plan_v4_b32"]
B2_PLANS = ["plan_extra", "plan_extra4", "plan_repeat", "plan_vsym", "plan_l3_wl", "plan_l3_w4w5", "plan_l3_enum", "plan_l1_w8w9w10", "plan_l1_w11", "plan_extra2_b32"]
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
        label = head.split(" ", 1)[0]
        red = [(m.group(1), m.group(2)) for m in ROW.finditer(b)]
        err = "PATCH-FAILED" in b or "PROBE-ERROR" in b or "BUILD-FAILED" in b
        m = re.search(r"\(rows not yes: (\d+)\)", b)
        out.append((label, head, b, red, err, int(m.group(1)) if m else -1))
    return out


def old_blocks(text, with_plan=True):
    out, plan = {}, None
    for chunk in re.split(r"(?m)^(?=##### |== )", text):
        if chunk.startswith("##### "):
            plan = chunk.split()[1]
        elif chunk.startswith("== ") and plan:
            label = chunk[3:].split(" ", 1)[0]
            out[(plan, label)] = {(m.group(1), m.group(2)) for m in ROW.finditer(chunk)}
    return out


fmt = lambda s: " ".join(f"{sc[3:]}:{r}" for sc, r in sorted(s, key=lambda t: (int(t[0][3:]), t[1]))) or "-"
problems, lines_a, lines_b1, lines_b2 = [], [], [], []
a_total = a_zero = 0
for p in A_PLANS + ["doc"]:
    f = os.path.join(EXP, "mut", "final5", p, "SUMMARY.txt")
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
        if lookup(b[0]) is None and p != "doc":
            problems.append(("UNEXPLAINED zero-red", p, b[0]))
        if p == "doc" and b[0] not in ("doc_none",):
            problems.append(("document variant turned no row red", p, b[0]))
# ---------------------------------------------------------------- B1: previous round
v4 = old_blocks(open(V4, encoding="utf-8").read().split("PART B -- one line per bad implementation")[0])
b1 = [0, 0, 0, 0]
for p in B1_PLANS:
    f = os.path.join(EXP, "mut", "final5", p, "SUMMARY.txt")
    if not os.path.isfile(f):
        print("MISSING", f)
        sys.exit(2)
    for label, head, b, red, err, cnt in blocks_of(f):
        b1[0] += 1
        if err or cnt < 0:
            problems.append(("ERROR RESULT", p, label))
            continue
        old = v4.get((p, label))
        if old is None:
            problems.append(("NO v4 BLOCK", p, label))
            continue
        now = set(red)
        if old:
            missing = old - now
            if missing:
                b1[2] += 1
                problems.append(("REGRESSION", p, label + " lost " + fmt(missing)))
                status = "REGRESSION"
            else:
                b1[1] += 1
                status = "preserved" + ("" if now == old else " (+ more rows)")
            lines_b1.append(f"  {p:22s} {label:36s} red now: {fmt(now)[:100]:100s} | red before: {fmt(old)[:100]}  [{status}]")
        else:
            b1[3] += 1
            why = lookup(label)
            if why is None:
                problems.append(("UNEXPLAINED zero-red (equivalent before)", p, label))
            lines_b1.append(f"  {p:22s} {label:36s} red now: {fmt(now)[:100]:100s} | red before: -  [equivalent before{'; still no row red' if not now else '; NOW RED (more discriminating)'}]")
sup = sorted(SUPERSEDED)
# ---------------------------------------------------------------- B2: rounds before
v3 = old_blocks(open(V3, encoding="utf-8").read())
b2 = [0, 0, 0, 0]
sup_prefix_count = {}
for p in B2_PLANS:
    f = os.path.join(EXP, "mut", "final5", "v3r_" + p, "SUMMARY.txt")
    if not os.path.isfile(f):
        print("MISSING", f)
        sys.exit(2)
    for label, head, b, red, err, cnt in blocks_of(f):
        b2[0] += 1
        if err or cnt < 0:
            problems.append(("ERROR RESULT", "v3r_" + p, label))
            continue
        old = v3.get((p, label))
        if old is None:
            problems.append(("NO v3 BLOCK", "v3r_" + p, label))
            continue
        pref = next((k for k in SUPERSEDED_PREFIX if label.startswith(k)), None)
        if pref:
            sup_prefix_count[pref] = sup_prefix_count.get(pref, 0) + 1
            b2[0] -= 1
            continue
        now = set(red)
        if old:
            missing = old - now
            if missing:
                b2[2] += 1
                problems.append(("REGRESSION", "v3r_" + p, label + " lost " + fmt(missing)))
                status = "REGRESSION"
            else:
                b2[1] += 1
                status = "preserved" + ("" if now == old else " (+ more rows)")
            lines_b2.append(f"  {p:16s} {label:42s} red now: {fmt(now)[:100]:100s} | red in v3: {fmt(old)[:100]}  [{status}]")
        else:
            b2[3] += 1
            why = lookup(label)
            if why is None:
                problems.append(("UNEXPLAINED zero-red (v3 equivalent)", "v3r_" + p, label))
            lines_b2.append(f"  {p:16s} {label:42s} red now: {fmt(now)[:100]:100s} | red in v3: -  [equivalent in v3{'; still no row red' if not now else '; NOW RED (more discriminating)'}]")
hdr = [
    "mut_summary_v5 -- the bad implementations of this round and the regression runs of the earlier rounds' bad implementations, on the final prototype",
    "",
    "Method: each bad implementation = the full final target prototype tree (work/t5f) with ONE hook replaced by a variant produced by patch_l3.py / patch_l1.py (--variant), or with the DOCUMENTS patched",
    "by a patch_docs.py flag; only the SC groups / rows named for it are run (proto/mutbatch.py, proto/docvariants5.py); a listed row is a row whose match is not `yes`.  The prototype is a text-substituted",
    "copy of the baseline, not the implementation (see README.md).",
    "",
    f"PART A  -- this round: {a_total} bad implementations; {a_total - a_zero} turn at least one row red; {a_zero} turn no row red (equivalent mutants / timing-class: reasons below).",
    f"PART B1 -- regression of the previous round's bad implementations: {b1[0]} re-run; {b1[1]} keep every row that was red before; {b1[2]} lose a row (regressions); {b1[3]} were equivalent before; {len(sup)} superseded (below).",
    f"PART B2 -- regression of the rounds before: {b2[0]} re-run; {b2[1]} keep every row that was red in v3; {b2[2]} lose a row (regressions); {b2[3]} were equivalent in v3; {sum(sup_prefix_count.values())} superseded (below).",
    "",
    "Bad implementations that turned NO row red:",
]
zero = []
for p in A_PLANS:
    for b in blocks_of(os.path.join(EXP, "mut", "final5", p, "SUMMARY.txt")):
        if b[5] == 0:
            zero.append((p, b[0]))
for p in B1_PLANS:
    for label, head, b, red, err, cnt in blocks_of(os.path.join(EXP, "mut", "final5", p, "SUMMARY.txt")):
        if cnt == 0:
            zero.append((p, label))
for p in B2_PLANS:
    for label, head, b, red, err, cnt in blocks_of(os.path.join(EXP, "mut", "final5", "v3r_" + p, "SUMMARY.txt")):
        if cnt == 0 and not v3.get((p, label)):
            zero.append(("v3r_" + p, label))
for p, label in zero:
    hdr.append(f"  {p} / {label}: {lookup(label) or '!!! NO REASON GIVEN !!!'}")
if not zero:
    hdr.append("  (none)")
hdr += ["", "Superseded (the bad implementation of the previous design has no counterpart in this design; removed from the regression run, replacement named):"]
hdr += [f"  {k}: {SUPERSEDED[k]}" for k in sup]
hdr += [f"  {k}* ({sup_prefix_count.get(k, 0)} bad implementations): {v}" for k, v in SUPERSEDED_PREFIX.items()]
hdr += ["", "=" * 100, "", "PART A -- blocks", ""]
body = ("\n".join(hdr) + "\n" + "".join(lines_a) + "\n" + "=" * 100 + "\n\nPART B1 -- one line per bad implementation of the previous round (rows are `SC-number:row`)\n\n" + "\n".join(lines_b1)
        + "\n\n" + "=" * 100 + "\n\nPART B2 -- one line per bad implementation of the rounds before (rows are `SC-number:row`)\n\n" + "\n".join(lines_b2) + "\n")
os.makedirs(os.path.join(EXP, "out"), exist_ok=True)
open(os.path.join(EXP, "out", "mut_summary_v5.txt"), "w", encoding="utf-8").write(body)
print("written out/mut_summary_v5.txt; PART A:", a_total, "run,", a_total - a_zero, "red,", a_zero, "no-row-red | PART B1:", b1[0], "run,", b1[1], "preserved,", b1[2], "regressions,", b1[3], "equivalent-before |",
      "PART B2:", b2[0], "run,", b2[1], "preserved,", b2[2], "regressions,", b2[3], "equivalent-in-v3 | superseded:", len(sup))
for pr in problems:
    print("  PROBLEM", pr)
sys.exit(1 if problems else 0)
