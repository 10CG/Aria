#!/usr/bin/env python3
"""cap_lin.py <aria root> [--bad VARIANT_HOOK_DIR] -- for every member of the probe's SC-34 lists (LIN_BASE 9 + LIN_NEW 14) the smallest whole-second CPU cap per process (`ulimit -t N`,
N = 1..4) under which the L3 hook still reports the expected tag; `>4` = the member is not detected even under the probe's own cap (the quadratic bad implementations).
The machinery is the probe's own (the source above the SC-34 rows is executed with the aria root as argv[1]); nothing is printed except member names, caps and counts.
Rule #7: this file holds no credential-shaped literal (the probe builds its values at run time)."""
import os
import sys

aria = os.path.abspath(sys.argv[1])
probe = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "spec", "baseline_probe.py")
src = open(probe, encoding="utf-8").read()
cut = src.index('row("SC-34", "34a"')
sys.argv = [probe, aria]
g = {"__name__": "probe_prefix", "__file__": probe}
import contextlib
import io

with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:cut], probe, "exec"), g)
out = []
for name in ("LIN_BASE", "LIN_NEW"):
    for label, builder, want in g[name]:
        content = builder()
        got = ">4"
        for cap in (1, 2, 3, 4):
            r = g["run_scan"](g["envelope"](g["BR"], content), cpu=cap)
            if g["_scan_ok"](r, want):
                got = str(cap)
                break
        out.append((name, label, got))
        print(f"{name:9s} {label:36s} {got}", flush=True)
ok = [int(c) for _n, _l, c in out if c != ">4"]
print("# members:", len(out), "detected under the 4 s cap:", len(ok), "max minimal cap:", max(ok) if ok else "-")
