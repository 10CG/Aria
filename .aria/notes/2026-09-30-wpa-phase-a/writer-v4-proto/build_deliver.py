#!/usr/bin/env python3
"""build_deliver.py -- assemble deliver/ from the final files and write MANIFEST.sha256.

Preconditions (all asserted):
  * spec/proposal.md, spec/baseline_probe.py, spec/baseline-evidence.md are byte-equal to the snapshots that the stage-2 runs (final_T / final_TN / final_C) used, and the stage-1 runs
    (final_A / final_B / final_N) snapshotted the same proposal + probe
  * final_A, final_B and final_C stdout are byte-equal (reproducibility, and independence from the evidence file), every run rc 0 with empty stderr
  * final_T: every row `yes` except the by-design 30a, target shape `holds`
  * the evidence file embeds final_A's stdout verbatim
Copies: proposal.md, baseline_probe.py, baseline-evidence.md, dispositions.json (from work/dispositions_data.py), the probe stdout files used for the evidence (logs/final_*.out / .rc / .err)
and the other evidence logs, and the archive directory writer-v4-proto/ (scripts, plans, summaries).  MANIFEST.sha256 covers every file under deliver/ except itself.
No report .md file is written: the repair report is returned as text in the structured output."""
import hashlib
import json
import os
import re
import shutil
import sys

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(EXP, "work"))
from dispositions_data import D  # noqa: E402

DEL = os.path.join(EXP, "deliver")


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def same(a, b):
    return open(a, "rb").read() == open(b, "rb").read()


spec = os.path.join(EXP, "spec")
for f in ("proposal.md", "baseline_probe.py", "baseline-evidence.md"):
    for lab in ("final_T", "final_TN", "final_C"):
        s = os.path.join(EXP, "work", "snap", lab, f)
        assert os.path.exists(s) and same(s, os.path.join(spec, f)), f"{lab}/{f} differs from spec/{f}"
for f in ("proposal.md", "baseline_probe.py"):
    for lab in ("final_A", "final_B", "final_N"):
        s = os.path.join(EXP, "work", "snap", lab, f)
        assert os.path.exists(s) and same(s, os.path.join(spec, f)), f"{lab}/{f} differs from spec/{f}"
L = os.path.join(EXP, "logs")
assert same(os.path.join(L, "final_A.out"), os.path.join(L, "final_B.out")), "final_A and final_B stdout differ"
assert same(os.path.join(L, "final_A.out"), os.path.join(L, "final_C.out")), "final_A and final_C stdout differ"
for lab in ("final_A", "final_B", "final_N", "final_T", "final_TN", "final_C"):
    assert open(os.path.join(L, lab + ".err")).read() == "", lab + " stderr not empty"
    assert open(os.path.join(L, lab + ".rc")).read().strip() == "rc=0", lab + " rc not 0"
    print(lab, open(os.path.join(L, lab + ".rc")).read().strip(), os.path.getsize(os.path.join(L, lab + ".out")), "bytes")
t = open(os.path.join(L, "final_T.out"), encoding="utf-8").read()
bad_rows = [l for l in t.split("\n") if re.match(r"^SC-\d+ │ ", l) and not l.endswith("│ yes") and "│ 30a │" not in l]
assert not bad_rows, bad_rows[:3]
assert "target shape (every row 'yes' and no leg row left unrun): holds" in t, "target shape does not hold"
ev = open(os.path.join(spec, "baseline-evidence.md"), encoding="utf-8").read()
a = open(os.path.join(L, "final_A.out"), encoding="utf-8").read().rstrip("\n")
assert a in ev, "evidence does not embed final_A stdout verbatim"

shutil.rmtree(DEL, ignore_errors=True)
os.makedirs(os.path.join(DEL, "logs"))
for f in ("proposal.md", "baseline_probe.py", "baseline-evidence.md"):
    shutil.copy2(os.path.join(spec, f), os.path.join(DEL, f))
json.dump(D, open(os.path.join(DEL, "dispositions.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(os.path.join(DEL, "dispositions.json"), "a").write("\n")
for lab in ("final_A", "final_B", "final_N", "final_T", "final_TN", "final_C"):
    for ext in (".out", ".rc", ".err"):
        shutil.copy2(os.path.join(L, lab + ext), os.path.join(DEL, "logs", lab + ext))
for f in sorted(os.listdir(L)):
    if f.startswith(("refs_check", "plugin_cache_currency", "fuzz_mask", "timing_", "mask_cost", "check_counts", "xref_check", "nc15", "coverage_check", "probe_diff", "regress_compare")) and f.endswith((".out", ".txt")):
        shutil.copy2(os.path.join(L, f), os.path.join(DEL, "logs", f))

P = os.path.join(DEL, "writer-v4-proto")
os.makedirs(P)
PROTO = ["patch_l3.py", "patch_l1.py", "patch_docs.py", "patch_tests.py", "build_full.sh", "build_docvariant.sh", "build_noselfcheck.sh", "runprobe.sh", "final_runs.sh",
         "run_final_campaign.sh", "run_v3_regression.sh", "run_timing_variants.sh", "onemut.sh", "mutbatch.py", "timing.py", "hooktry.py", "mk_evidence.py"]
for f in PROTO:
    shutil.copy2(os.path.join(EXP, "proto", f), os.path.join(P, f))
WORK = ["mkplan_v4.py", "mk_refined_v3_plans.py", "validate_plans.py", "regress_compare.py", "build_mut_summary.py", "equiv_reasons.py", "coverage_check.py", "refs_check.py",
        "check_counts.py", "xref_check.py", "sc_counts.py", "scan_all.py", "scan_file.py", "nc15.py", "fuzz_mask.py", "mask_cost.py", "run_manual_runs.py", "build_deliver.py",
        "dispositions_data.py", "l3try.py", "cases_m5.py"]
for f in WORK:
    src = os.path.join(EXP, "work", f)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(P, f))
    else:
        print("note: not present:", f)
for f in sorted(os.listdir(os.path.join(EXP, "work"))):
    if f.startswith("cases_") and f.endswith(".py") and f not in WORK:
        shutil.copy2(os.path.join(EXP, "work", f), os.path.join(P, f))
shutil.copytree(os.path.join(EXP, "work", "plans"), os.path.join(P, "plans"))
shutil.copytree(os.path.join(EXP, "work", "plans_v3r"), os.path.join(P, "plans_v3r"))
for f in ("mut_summary_v4.txt", "timing_summary.txt", "manual_runs.txt", "README.md"):
    src = os.path.join(EXP, "work", "archive", f)
    assert os.path.exists(src), src
    shutil.copy2(src, os.path.join(P, f))

lines = []
for r, _d, fs in os.walk(DEL):
    for f in fs:
        if f == "MANIFEST.sha256":
            continue
        p = os.path.join(r, f)
        lines.append(f"{sha(p)}  {os.path.relpath(p, DEL)}")
lines.sort(key=lambda s: s.split("  ", 1)[1])
open(os.path.join(DEL, "MANIFEST.sha256"), "w").write("\n".join(lines) + "\n")
print("deliver/ assembled:", len(lines), "files")
for k in ("proposal.md", "baseline_probe.py", "baseline-evidence.md", "dispositions.json"):
    p = os.path.join(DEL, k)
    print(k, sha(p)[:16], os.path.getsize(p), "bytes")
