#!/usr/bin/env python3
"""mk_numbers6.py -- parse the timing / cap / probe outputs into out/numbers.json (every number the proposal quotes about time or counts comes from here; nothing typed by hand).

inputs (all under out/):
  timing_t6_main.txt        good prototype, all tiers, 5 pairs, --judge (run_timing_good6.sh)
  timing_t6_f15.txt         good prototype, tiers f / f0, 15 pairs (only used for the stability line of the report, not for the proposal)
  timing_bad6.txt           bad implementations on the tiers meant to catch them (run_timing_variants6.sh)
  cap_lin.txt               smallest whole-second per-process CPU cap under which each linear member of SC-34 is still detected (cap_lin.py), one `list member N` per line
  probe_target.out          stdout of the probe on the target prototype (row / group counts)
  probe_baseline.out        stdout of the probe on the baseline (baseline counts)
usage: python3 mk_numbers6.py
"""
import json
import os
import re

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(EXP, "out")
LINE = re.compile(r"^(?P<name>\S.*?)\s+CPU min base\s+(?P<base>[0-9.]+)s target\s+(?P<tgt>[0-9.]+)s ratio\s+(?P<ratio>[0-9.]+)")
N = {}


def put(k, v):
    N[k] = v


def parse_timing(path):
    cur = ""
    res = {}
    for l in open(path, encoding="utf-8"):
        l = l.rstrip("\n")
        if l.startswith("-- "):
            cur = l[3:].split(" ")[0]
            continue
        if l.startswith("   [") and l.rstrip().endswith("]"):
            cur = l.strip()[1:-1]
            continue
        m = LINE.match(l)
        if m:
            res.setdefault(cur, []).append((m.group("name"), float(m.group("base")), float(m.group("tgt")), float(m.group("ratio"))))
    return res


main = parse_timing(os.path.join(OUT, "timing_t6_main.txt"))[""]
key = {
    "h1": "h1 ", "h2": "h2 ", "ga": "g-a ", "gb": "g-b ", "fB": "f  200 entries, Bash", "fR": "f  200 entries, Read", "f0B": "f0 no extension, Bash", "f0R": "f0 no extension, Read",
    "fha": "fh-a ", "fhb": "fh-b ", "fh0": "fh-0 ", "i3a": "i3-a ", "i3b": "i3-b ", "i3c": "i3-c ", "i3d": "i3-d ", "i3e": "i3-e ", "i3f": "i3-f ", "i3g": "i3-g ", "i3h": "i3-h ",
    "i1": "i1 ", "i2": "i2 ", "w1a": "w1 Read 4 KB", "w1b": "w1 Read 60 KB", "w1c": "w1 Read 180 KB",
}
for k, pre in key.items():
    hit = [r for r in main if r[0].startswith(pre)]
    assert len(hit) == 1, (k, pre, len(hit))
    _n, b, t, r = hit[0]
    put(k + "_b", f"{b:.3f}")
    put(k + "_t", f"{t:.3f}")
    put(k + "_r", f"{r:.2f}")

# the Impact sentence: the percentage / millisecond cost of the extension-free and the 200-entry paths (same 5-pair run as W14 item 5)
def fl(k):
    return float(N[k])


put("PCT_F0B", f"{(fl('f0B_t') / fl('f0B_b') - 1) * 100:.0f}")
put("PCT_F0R", f"{(fl('f0R_t') / fl('f0R_b') - 1) * 100:.0f}")
put("MS_FB", f"{(fl('fB_t') - fl('fB_b')) * 1000:.0f}")
put("MS_FR", f"{(fl('fR_t') - fl('fR_b')) * 1000:.0f}")
for dst, src in (("W1_BASE", "w1a_b"), ("W1_4K", "w1a_t"), ("W1_60K", "w1b_t"), ("W1_180K", "w1c_t")):
    put(dst, N[src])

# load average at the start / end of the main run
txt = open(os.path.join(OUT, "timing_t6_main.txt"), encoding="utf-8").read()
loads = [float(x) for x in re.findall(r"load\((?:start|end)\)=([0-9.]+) ", txt)]
lo, hi = min(loads), max(loads)
put("LOAD_TIMING", f"{lo:.1f}" if f"{lo:.1f}" == f"{hi:.1f}" else f"{lo:.1f}–{hi:.1f}")

# bad implementations
pb = os.path.join(OUT, "timing_bad6.txt")
if os.path.exists(pb):
    for variant, rows in parse_timing(pb).items():
        for name, b, t, r in rows:
            tag = name.split(" ")[0] + ("B" if "Bash" in name else "R" if "Read" in name else "")
            put(f"bad_{variant}_{tag}_r", f"{r:.1f}")
            put(f"bad_{variant}_{tag}_t", f"{t:.2f}")

# the 500 KB members: total CPU of the quadratic value-extraction variants (bad_cost500.sh): the first val_quote_strip entry stands for the quote-strip class
pc5 = os.path.join(OUT, "bad_cost500.txt")
if os.path.exists(pc5):
    cur, vals = None, {}
    for l in open(pc5, encoding="utf-8"):
        if l.startswith("-- "):
            cur = l[3:].split()[0]
            continue
        m = re.match(r"^(\S+)\s+500 KB\s+cpu\s+([0-9.]+) s", l)
        if m and cur and cur != "target":
            vals.setdefault(cur, []).append(float(m.group(2)))
    put("BAD500_QS", f"{vals['val_quote_strip'][0]:.0f}")
    put("BAD500_MIN", f"{min(min(v) for v in vals.values()):.0f}")

# W2's linear-time paragraph: grep -oE CPU of the target and the bad patterns (ere_claims.py)
pe = os.path.join(OUT, "ere_claims.txt")
if os.path.exists(pe):
    names = {("kv-secret-assign", "target"): "ERE_KV_B", ("kv-secret-assign", "kv_unbounded"): "ERE_KV_UNB", ("cli-secret-flag", "target"): "ERE_CLI_B",
             ("cli-secret-flag", "cli_unbounded"): "ERE_CLI_UNB", ("cli-secret-flag", "cli_noleft"): "ERE_CLI_NOLEFT"}
    for l in open(pe, encoding="utf-8"):
        m = re.match(r"(\S+)\s+(target|kv_unbounded|cli_unbounded|cli_noleft)\b.*grep -oE CPU\s+([0-9.]+) s", l)
        if m:
            v = float(m.group(3))
            put(names[(m.group(1), m.group(2))], f"{v:.2f}" if v < 1 else f"{v:.0f}" if v >= 10 else f"{v:.1f}")

# W9's matching-cost sentence: the per-occurrence stage cut (ext_v4stage) against the baseline on a 64-occurrence command of about 2 KB and 8 KB (occ_cost.py)
po = os.path.join(OUT, "occ.txt")
if os.path.exists(po):
    for l in open(po, encoding="utf-8"):
        m = re.match(r"size=\s*(\d+) B\s+ext_v4stage\s+cpu=\s*([0-9.]+) s\s+ratio-to-baseline=\s*([0-9.]+)", l)
        if m:
            put("V4_2K" if int(m.group(1)) < 4000 else "V4_8K", f"{float(m.group(3)):.1f}")

# SC-34 linear members: the largest single-process CPU of the target prototype
pc = os.path.join(OUT, "cap_lin.txt")
if os.path.exists(pc):
    vals = [float(l.split()[-1]) for l in open(pc, encoding="utf-8") if l.strip() and not l.startswith("#")]
    put("CAP_LIN_MAX", str(int(max(vals))))                       # whole seconds: the smallest `ulimit -t N` under which every linear member is still detected

# probe-derived counts (target stdout)
pt = os.path.join(OUT, "probe_target.out")
if os.path.exists(pt):
    t = open(pt, encoding="utf-8").read()
    rows = re.findall(r"(?m)^SC-(\d+) │ ", t)
    put("ROWS", len(rows))
    put("SC_GROUPS", len(set(rows)))
    put("SC22_N", len(re.findall(r"(?m)^SC-22 │ \S+ │ baseline-failing │", t)))
    m17 = re.search(r"(?m)^SC-17 │ 17d │.* │ (\d+)/(\d+) as expected[^│]*│ [^│]* │ (?:yes|no|n/a)$", t)
    assert m17 and m17.group(1) == m17.group(2), "17d member count"
    put("N17D", int(m17.group(1)))
pbase = os.path.join(OUT, "probe_baseline.out")
if os.path.exists(pbase):
    t = open(pbase, encoding="utf-8").read()
    tot = blocked = 0
    for rid in ("23a", "23b", "23j"):
        mm = re.search(r"(?m)^SC-23 │ " + rid + r" │ [^│]* │ .* │ ([^│]*) │ ([^│]*) │ (?:yes|no|n/a)$", t)
        assert mm, rid
        toks = [x for x in mm.group(2).replace("exit=", "").split(",") if x]
        tot += len(toks)
        blocked += sum(1 for x in toks if x == "2")
    put("SC23_BASE", f"{blocked}/{tot}")
json.dump(N, open(os.path.join(OUT, "numbers.json"), "w"), indent=1, sort_keys=True)
for k in sorted(N):
    print(f"{k:34s} {N[k]}")
