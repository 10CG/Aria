#!/usr/bin/env python3
"""mk_timing_summary6.py -- compose out/timing_summary_v6.txt and out/gitcopy_summary_v6.txt from the raw outputs (out/timing_t6_main.txt, timing_t6_f15.txt, timing_bad6.txt, bad_cost500.txt,
member_matrix.txt, cap_lin.txt, gitcopy_*.txt / *.meta).  Only concatenation and headers: every number in the body is the raw output."""
import os
import re

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(EXP, "out")


def rd(name):
    p = os.path.join(OUT, name)
    return open(p, encoding="utf-8").read().rstrip("\n") if os.path.exists(p) else f"(missing: {name})"


hdr = """timing_summary_v6 -- W14 time tiers on the target prototype and on the bad implementations of the tiers; the SC-34 per-process CPU caps (proposal W14 item 5, SC-30, SC-34)

Method (proto/timing.py): the baseline hook (aria 268da8f) and the target hook run INTERLEAVED (A/B/A/B...) on the same input on the same host; per run the CPU time (user+sys, via RUSAGE_CHILDREN
deltas, i.e. the whole process tree of the hook) and the wall time are recorded; the statistic per hook is the MINIMUM over N interleaved runs, the verdict statistic is the CPU ratio
target / baseline.  Wall time and load average are recorded, never judged.  `--judge` prints verdict=PASS|FAIL per bounded tier against the W14 bounds:
(f) <= 3.0 as a pure ratio; (f0) target <= 1.5 x max(baseline, 100 ms); (f-hit) <= 3.0; (g-a) / (g-b) <= 2.5; (h2) <= 1.5; (i1) / (i2) <= 2.0; (i3-a..e) <= 2.5; (i3-f / g / h) <= 5.0.
A failed liveness assertion fails the tier.  w1 (a Read result through the L3 hook; the baseline hook does not extract file.content and exits early) and h1 / fh-0 are informational.
Host: Linux 6.17.9-1-pve, 4 cores, shared (other tenants); the 1-minute load average is printed in the headers of the runs below.  Numbers move with the host; only ratios are judged.
Bad implementations: every one exceeds its bound or fails its liveness check (rows below).  The quadratic value-extraction idioms are also measured on the 500 KB SC-34 members (bad_cost500) and the
linear members under the probe's own cap (cap_lin: the smallest whole-second `ulimit -t` under which each member is still detected; member_matrix: which members each bad implementation fails).
"""
parts = [hdr,
         "################ target prototype (good): all tiers, 5 pairs, --judge ################\n$ proto/run_timing_good6.sh  (python3 proto/timing.py base/aria/hooks work/t6/aria/hooks f,f0,g,gmax,h,i,w1,fhit,i3 --pairs 5 --judge)\n" + rd("timing_t6_main.txt"),
         "################ target prototype (good): tiers f f0, 15 pairs (the 5-pair run above shows the spread: f / f0 minima move by +-10 ms with the host) ################\n" + rd("timing_t6_f15.txt"),
         "################ bad implementations, each on the tier meant to catch it (3 pairs; the slow ones 1 pair) ################\n$ proto/run_timing_variants6.sh 3 1\n" + rd("timing_bad6.txt"),
         "################ the 500 KB SC-34 members: TOTAL cpu of the quadratic value-extraction variants vs the target ################\n" + rd("bad_cost500.txt"),
         "################ the linear members under the probe's own cap: smallest whole-second per-process CPU cap that still detects (cap_lin.py) ################\n" + rd("cap_lin.txt"),
         "################ which SC-34 members each bad implementation fails under the 4 s cap (member_matrix.py, final probe members) ################\n" + rd("member_matrix.txt"),
         "################ the same matrix with the export-blank member at 400 KB, three jobs on a busy host: the TARGET itself fails that member (why it is 100 KB) ################\n" + rd("member_matrix.400KB_under_load.txt")]
open(os.path.join(OUT, "timing_summary_v6.txt"), "w", encoding="utf-8").write("\n\n".join(parts) + "\n")
print("written out/timing_summary_v6.txt")

g = """gitcopy_summary_v6 -- the existing hook suites on a git copy of the aria repository (history present: the suite's SC-8 latency benchmark and SC-9a pre-change comparison reach their reference commit af87cae)

Method (proto/run_gitcopy_suite.sh): `git clone` of /home/dev/Aria/.git/modules/aria (read-only source) into the experiment directory; `git checkout 268da8f` (the baseline); `baseline` = that working tree untouched,
`proto` = the same working tree with the prototype's hooks / hooks.json / suites copied over (uncommitted, like an implementer's tree before the commit).  Then `bash hooks/tests/secret-guard.test.sh` and
`bash hooks/tests/secret-scan.test.sh` with HOME redirected to a private directory.  The five SC-8 tiers are measured INSIDE the suite (EPOCHREALTIME, 20 rounds of 10 calls, min of rounds); the ceiling per tier is
max(100 ms, old x 1.5) per call and is not changed.  The load average printed at the start of the SC-8 block is the host state for the tier numbers.
"""
body = [g]
for which in ("baseline", "proto", "proto_header_unsynced", "core_below_gate"):
    mp = os.path.join(OUT, f"gitcopy_{which}.meta")
    gp = os.path.join(OUT, f"gitcopy_{which}_guard.txt")
    sp = os.path.join(OUT, f"gitcopy_{which}_scan.txt")
    if not os.path.exists(mp):
        continue
    gtxt = open(gp, encoding="utf-8").read() if os.path.exists(gp) else ""
    keep = [l for l in gtxt.split("\n") if re.search(r"\[SC-8\]|\[SKIP\]|^PASS:|^FAIL:|^  FAIL ", l)]
    stxt = open(sp, encoding="utf-8").read() if os.path.exists(sp) else ""
    keep_s = [l for l in stxt.split("\n") if re.search(r"^PASS:|^FAIL:|^  FAIL ", l)]
    body.append(f"################ {which} ################\n" + rd(f"gitcopy_{which}.meta") + "\n-- secret-guard.test.sh (selected lines)\n" + "\n".join(keep) + "\n-- secret-scan.test.sh (selected lines)\n" + "\n".join(keep_s))
open(os.path.join(OUT, "gitcopy_summary_v6.txt"), "w", encoding="utf-8").write("\n\n".join(body) + "\n")
print("written out/gitcopy_summary_v6.txt")
