#!/usr/bin/env python3
"""b1_fn_audit.py HOOK [--lens 8,32] [--shapes A,B,C,D,E,F] [--kinds secret,benign] [--reps 3] [--topn 5]

Driver for b1_fn_audit.sh: writes one input file per (kind, shape, KB) with the b1_shapes definitions into a private temp
dir, runs the bash harness once (in-process timing, no fork noise), prints its TSV, and removes the inputs.
Read the ratio t(32 KB) / t(8 KB) per row: about 4 = linear, about 16 = quadratic.
"""
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from b1_shapes import build  # noqa: E402

hook = os.path.abspath(sys.argv[1])


def opt(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


lens = [int(x) for x in opt("--lens", "8,32").split(",")]
shapes = opt("--shapes", "A,B,C,D,E,F").split(",")
kinds = opt("--kinds", "secret,benign").split(",")
reps, topn = opt("--reps", "3"), opt("--topn", "5")

d = tempfile.mkdtemp(prefix="b1fa-")
try:
    for kind in kinds:
        for shape in shapes:
            for kb in lens:
                with open(os.path.join(d, "%s_%s_%02d.txt" % (kind, shape, kb)), "w", encoding="utf-8") as fh:
                    fh.write(build(kind, shape, kb))
    env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": d, "TMPDIR": d, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    sh = os.path.join(os.path.dirname(os.path.abspath(__file__)), "b1_fn_audit.sh")
    p = subprocess.run(["bash", sh, hook, d, reps, topn], env=env, cwd=d, capture_output=True, text=True)
    sys.stdout.write(p.stdout)
    if p.returncode != 0 or p.stderr.strip():
        sys.stdout.write("# harness rc=%d stderr_lines=%d\n" % (p.returncode, len(p.stderr.splitlines())))
finally:
    shutil.rmtree(d, ignore_errors=True)
