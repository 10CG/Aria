#!/usr/bin/env python3
"""build_deliver5.py -- assemble deliver/ from the final files and write MANIFEST.sha256.

Preconditions (all asserted):
  * spec/proposal.md, spec/baseline_probe.py, spec/baseline-evidence.md are byte-equal to the snapshots that the stage-2 runs (final_T / final_TN / final_C) used, and the stage-1 runs
    (final_A / final_B / final_N) snapshotted the same probe
  * final_A, final_B and final_C stdout are byte-equal (reproducibility, and independence from the evidence file), every run rc 0 with empty stderr
  * final_T: every row `yes` except the by-design 30a, target shape `holds`
  * the evidence file embeds final_A's stdout verbatim
Copies: the three files, dispositions.json (from proto/dispositions_data.py), the probe stdout files and the other evidence outputs (logs/ and out/), and the archive directory
writer-v5-proto/ (scripts, plans, summaries, README).  MANIFEST.sha256 covers every file under deliver/ except itself.  No report .md file is written: the repair report is returned as
text in the structured output."""
import hashlib
import json
import os
import re
import shutil
import sys

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(EXP, "proto"))
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
# stage 1 runs the baseline: its stdout does not depend on the text of proposal.md (row 15e is silent for any text); only the PROBE must be the final one.  The independence is proved by
# final_C (stage 2, final proposal + final evidence in place) being byte-equal to final_A.
for f in ("baseline_probe.py",):
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
shutil.copy2(os.path.join(L, "final.log"), os.path.join(DEL, "logs", "final.log"))
for f in sorted(os.listdir(L)):
    if f.startswith(("evidence_", "check_counts", "xref_check", "refs_check", "scan_all", "ere_battery", "diff_ext_builtin", "fuzz_ext_builtin", "fuzz_value_of", "readface_check", "format_lint", "probe_diff", "mutation_")) \
            and f.endswith((".out", ".txt")):
        shutil.copy2(os.path.join(L, f), os.path.join(DEL, "logs", f))
OUT = os.path.join(EXP, "out")
for f in ("occ_2k.txt", "occ_8k.txt", "timing_main.txt", "timing_bad.txt", "timing_i3_bad.txt", "ere_claims.txt", "val_quadratic_16k.txt", "numbers.json", "probe_times.txt", "mut_summary_v5.txt"):
    src = os.path.join(OUT, f)
    assert os.path.exists(src), src
    shutil.copy2(src, os.path.join(DEL, "logs", f))
cl = os.path.join(EXP, "mut", "final5", "campaign.log")
if os.path.exists(cl):
    shutil.copy2(cl, os.path.join(DEL, "logs", "campaign.log"))

P = os.path.join(DEL, "writer-v5-proto")
os.makedirs(P)
PROTO = ["patch_l3.py", "patch_l1.py", "patch_docs.py", "patch_tests.py", "patch_probe_v5.py", "build_full.sh", "build_docvariant.sh", "build_noselfcheck.sh", "runprobe.sh", "final_runs.sh",
         "run_final_campaign5.sh", "run_docvariants5.sh", "docvariants5.py", "mutbatch.py", "onemut.sh", "validate_plans.py", "build_mut_summary5.py", "equiv_reasons.py",
         "timing.py", "run_timing_variants5.sh", "occ_cost.py", "ere_battery.py", "diff_ext_builtin.py", "fuzz_ext_builtin.py", "fuzz_value_of.py", "readface_check.py", "refs_check.py", "scan_all.py", "scan_file.py",
         "check_counts.py", "xref_check.py", "format_lint.py", "ere_claims.py", "mk_numbers.py", "mk_evidence.py", "apply_edits.py", "build_deliver5.py", "dispositions_data.py", "mk_report.py", "report_text.py", "README.md"]
for f in PROTO:
    src = os.path.join(EXP, "proto", f)
    assert os.path.exists(src), src
    shutil.copy2(src, os.path.join(P, f))
os.makedirs(os.path.join(P, "proposal_edits"))
for f in sorted(os.listdir(os.path.join(EXP, "proto", "proposal_edits"))):
    if f.endswith(".py"):
        shutil.copy2(os.path.join(EXP, "proto", "proposal_edits", f), os.path.join(P, "proposal_edits", f))
shutil.copytree(os.path.join(EXP, "work", "plans5"), os.path.join(P, "plans_v5"))
shutil.copytree(os.path.join(EXP, "work", "plans"), os.path.join(P, "plans_v4"))
shutil.copytree(os.path.join(EXP, "work", "plans_v3"), os.path.join(P, "plans_v3"))
for f in ("mut_summary_v5.txt",):
    shutil.copy2(os.path.join(OUT, f), os.path.join(P, f))

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
