#!/usr/bin/env python3
"""mutbatch.py PLAN.tsv [--jobs N] [--out DIR] [--tree TREE]

PLAN.tsv lines:  label <TAB> kind(l3|l1|hj) <TAB> variant <TAB> SC list (WPA_ONLY) <TAB> rows (WPA_ROWS, optional)
Every mutant = the full target prototype (TREE, default work/t6) with ONE hook replaced by a bad implementation produced by
patch_l3.py / patch_l1.py --variant; the probe rows that are not `yes` are the rows that catch it.  Results: OUT/<label>.txt
(one line per red row, plus the wrong-label text of the row) and OUT/SUMMARY.txt."""
import concurrent.futures as cf
import hashlib
import os
import re
import shutil
import subprocess
import sys

EXP = "/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v6"
plan = sys.argv[1]
jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 3
outdir = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else EXP + "/mut"
tree = sys.argv[sys.argv.index("--tree") + 1] if "--tree" in sys.argv else EXP + "/work/t6"
spec = sys.argv[sys.argv.index("--spec") + 1] if "--spec" in sys.argv else EXP + "/spec"
b32 = "--b32" in sys.argv
os.makedirs(outdir, exist_ok=True)
snap_spec = EXP + "/work/mutspec"
shutil.rmtree(snap_spec, ignore_errors=True)
os.makedirs(snap_spec)
for f in ("baseline_probe.py", "proposal.md", "baseline-evidence.md"):
    if os.path.exists(os.path.join(spec, f)):
        shutil.copy(os.path.join(spec, f), snap_spec)


def one(line):
    label, kind, variant, scs = line[:4]
    rows = line[4] if len(line) > 4 else ""
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", label)
    if safe != label:                      # a sanitised name can collide with another label (e.g. `+` and `/` both become `_`): make it unique
        safe += "_" + hashlib.sha1(label.encode()).hexdigest()[:6]
    work = f"{EXP}/work/mutwork/{safe}"
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work + "/aria")
    shutil.copytree(tree + "/aria/hooks", work + "/aria/hooks", symlinks=True)
    if os.path.isdir(tree + "/standards"):
        os.symlink(tree + "/standards", work + "/standards")
    base = EXP + "/base/aria/hooks/"
    if kind == "l3":
        r = subprocess.run(["python3", EXP + "/proto/patch_l3.py", base + "secret-scan.sh", work + "/aria/hooks/secret-scan.sh", "--variant", variant], capture_output=True, text=True)
    elif kind == "hj":                      # hooks.json variant: regenerate hooks.json from the baseline copy
        shutil.copy(base + "hooks.json", work + "/aria/hooks/hooks.json")
        r = subprocess.run(["python3", EXP + "/proto/patch_hooks_json.py", work, "--variant", variant], capture_output=True, text=True)
    else:
        r = subprocess.run(["python3", EXP + "/proto/patch_l1.py", base + "secret-guard.sh", work + "/aria/hooks/secret-guard.sh", "--variant", variant], capture_output=True, text=True)
    if r.returncode != 0:
        res = f"PATCH-FAILED: {r.stderr.strip()[-300:]}"
        open(f"{outdir}/{safe}.txt", "w").write(res + "\n")
        return label, variant, [res]
    env = dict(os.environ, HOME=EXP + "/home", TMPDIR=EXP + "/tmp", WPA_ONLY=scs)
    env.pop("WPA_BASH32", None)
    if rows:
        env["WPA_ROWS"] = rows
    if b32:
        env["WPA_BASH32"] = "/tmp/claude-1000/-home-dev-Aria/261f53cc-4e83-410e-bb33-9a99debc3b55/scratchpad/exp/writer-v6/bash32/bash"
    p = subprocess.run(["python3", snap_spec + "/baseline_probe.py", work + "/aria"], capture_output=True, text=True, env=env, cwd=snap_spec)
    red = []
    for l in p.stdout.split("\n"):
        m = re.match(r"^(SC-\d+) │ (\S+) │ (\S+) │ .* │ (.*) │ (yes|no|n/a)$", l)
        if m and m.group(5) == "no":
            parts = l.split(" │ ")
            red.append(f"{m.group(1)} {m.group(2)} | {parts[-2][:150]}")
    if p.returncode not in (0, 3):
        red.append(f"PROBE-ERROR rc={p.returncode}: {p.stderr.strip()[-200:]}")
    open(f"{outdir}/{safe}.txt", "w").write("\n".join(red) + ("\n" if red else ""))
    shutil.rmtree(work, ignore_errors=True)
    return label, variant, red


lines = [l.rstrip("\n").split("\t") for l in open(plan, encoding="utf-8") if l.strip() and not l.startswith("#")]
results = {}
with cf.ThreadPoolExecutor(max_workers=jobs) as ex:
    futs = {ex.submit(one, ln): ln[0] for ln in lines}
    for f in cf.as_completed(futs):
        label, variant, red = f.result()
        results[label] = (variant, red)
        print(f"{label}: {len(red)} red", flush=True)
with open(f"{outdir}/SUMMARY.txt", "w") as fh:
    for ln in lines:
        label = ln[0]
        variant, red = results[label]
        fh.write(f"== {label} (variant {variant}; WPA_ONLY={ln[3]}{'; WPA_ROWS=' + ln[4] if len(ln) > 4 else ''})\n")
        for r in red:
            fh.write("   " + r + "\n")
        fh.write(f"   (rows not yes: {len(red)})\n")
