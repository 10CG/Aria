#!/usr/bin/env python3
"""docvariants5.py -- document-sync bad implementations: for every patch_docs.py flag build a full tree (hooks / suites of the final prototype, DOCUMENTS patched with the flag) and run the probe on SC-26 / SC-27 / SC-28;
the rows that are not `yes` are the rows that catch the bad implementation.  Results in mut/final5/doc/SUMMARY.txt (same block format as mutbatch.py).
usage: docvariants5.py [--jobs N] [--only FLAG[;FLAG...]]     (--only re-runs the listed flags and merges them into the existing SUMMARY.txt)"""
import concurrent.futures as cf
import os
import re
import shutil
import subprocess
import sys

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(EXP, "mut", "final5", "doc")
os.makedirs(OUT, exist_ok=True)
jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 3
MARKERS = ["rule6_note", ".aria/secret-guard.paths", "ps aux", "/proc", "app.ini", "file.content", "kv-secret-assign", "placeholder", "os.environ", "keys_unsorted", "fp=", "CPU", "partial"]
FLAGS = ["--bad", "--bad-sot", "--bad-layer", "--no-scope", "--hdr-count", "--hdr-half-l", "--hdr-dangling", "--hdr-half-a", "--hdr-argon", "--hdr-topcontent", "--hdr-nohist"] + ["--cl-drop=" + m for m in MARKERS]
ENVV = dict(os.environ, HOME=EXP + "/home", TMPDIR=EXP + "/tmp")
snap = EXP + "/work/mutspec_doc"
shutil.rmtree(snap, ignore_errors=True)
os.makedirs(snap)
for f in ("baseline_probe.py", "proposal.md", "baseline-evidence.md"):
    if os.path.exists(os.path.join(EXP, "spec", f)):
        shutil.copy(os.path.join(EXP, "spec", f), snap)


def one(flag):
    safe = re.sub(r"[^A-Za-z0-9_.=-]", "_", flag).replace("=", "_").strip("_-") or "ctl"
    tree = f"{EXP}/work/dv_{safe}"
    if flag == "--no-selfcheck":
        r = subprocess.run(["bash", EXP + "/proto/build_noselfcheck.sh", tree], capture_output=True, text=True, env=ENVV)
    else:
        r = subprocess.run(["bash", EXP + "/proto/build_docvariant.sh", tree, flag], capture_output=True, text=True, env=ENVV)
    if r.returncode != 0:
        return flag, [f"BUILD-FAILED: {r.stderr.strip()[-200:]}"]
    e2 = dict(ENVV, WPA_ONLY="SC-26,SC-27,SC-28")
    e2.pop("WPA_BASH32", None)
    p = subprocess.run(["python3", snap + "/baseline_probe.py", tree + "/aria"], capture_output=True, text=True, env=e2, cwd=snap)
    red = []
    for l in p.stdout.split("\n"):
        m = re.match(r"^(SC-\d+) │ (\S+) │ (\S+) │ .* │ (.*) │ (yes|no|n/a)$", l)
        if m and m.group(5) == "no":
            parts = l.split(" │ ")
            red.append(f"{m.group(1)} {m.group(2)} | {parts[-2][:120]}")
    if p.returncode not in (0, 3):
        red.append(f"PROBE-ERROR rc={p.returncode}: {p.stderr.strip()[-200:]}")
    shutil.rmtree(tree, ignore_errors=True)
    return flag, red


ALL = FLAGS + ["--no-selfcheck"]
only = sys.argv[sys.argv.index("--only") + 1].split(";") if "--only" in sys.argv else None
res = {}
SUMM = os.path.join(OUT, "SUMMARY.txt")
if only and os.path.exists(SUMM):          # merge: keep the blocks of the flags that are not re-run
    for blk in re.split(r"(?m)^== ", open(SUMM, encoding="utf-8").read())[1:]:
        head = blk.split("\n", 1)[0]
        name = re.match(r"doc(.*?) \(patch_docs\.py ", head).group(1)
        fl = "--" + name[1:] if name.startswith("_") else name
        fl = fl.replace(":", "=") if fl.startswith("--cl-drop") else fl      # the header spelling turned every `=` of the flag into `:` (the marker `fp=` holds one)
        res[fl] = [l[3:] for l in blk.split("\n")[1:] if l.startswith("   SC-") or l.startswith("   PROBE") or l.startswith("   BUILD")]
todo = only if only else ALL
with cf.ThreadPoolExecutor(max_workers=jobs) as ex:
    for flag, red in ex.map(one, todo):
        res[flag] = red
        print(f"{flag}: {len(red)} red", flush=True)
with open(SUMM, "w", encoding="utf-8") as f:
    for flag in ALL:
        f.write(f"== doc{flag.replace('--', '_').replace('=', ':')} (patch_docs.py {flag}; WPA_ONLY=SC-26,SC-27,SC-28)\n")
        for l in res.get(flag, []):
            f.write("   " + l + "\n")
        f.write(f"   (rows not yes: {len(res.get(flag, []))})\n")
