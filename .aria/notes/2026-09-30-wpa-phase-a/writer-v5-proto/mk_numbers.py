#!/usr/bin/env python3
"""mk_numbers.py -- parse the timing / cost outputs (out/timing_main.txt, out/timing_bad.txt, out/occ_2k.txt, out/occ_8k.txt, out/probe_times.txt) into out/numbers.json and print them.

Every number that proposal.md quotes about time comes from here (the texts that hold them are composed by apply_edits.py from these values); nothing is typed by hand."""
import json
import os
import re
import sys

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(EXP, "out")
LINE = re.compile(r"^(?P<name>\S.*?)\s+CPU min base\s+(?P<base>[0-9.]+)s target\s+(?P<tgt>[0-9.]+)s ratio\s+(?P<ratio>[0-9.]+)")
N = {}


def put(k, v):
    N[k] = v


def parse_timing(path, prefix):
    cur = None
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
            res.setdefault(cur or "", []).append((m.group("name"), float(m.group("base")), float(m.group("tgt")), float(m.group("ratio"))))
    return res


main = parse_timing(os.path.join(OUT, "timing_main.txt"), "")[""]
key = {
    "h1": "h1 ", "h2": "h2 ", "ga": "g-a ", "gb": "g-b ", "fB": "f  200 entries, Bash", "fR": "f  200 entries, Read", "f0B": "f0 no extension, Bash", "f0R": "f0 no extension, Read",
    "fha": "fh-a ", "fhb": "fh-b ", "fh0": "fh-0 ", "i3a": "i3-a ", "i3b": "i3-b ", "i3c": "i3-c ", "i3d": "i3-d ", "i3e": "i3-e ", "i1": "i1 ", "i2": "i2 ",
    "w1a": "w1 Read 4 KB", "w1b": "w1 Read 60 KB", "w1c": "w1 Read 180 KB",
}
for k, pre in key.items():
    hit = [r for r in main if r[0].startswith(pre)]
    if hit:
        _n, b, t, r = hit[-1]
        put(k + "_b", f"{b:.3f}")
        put(k + "_t", f"{t:.3f}")
        put(k + "_r", f"{r:.2f}")
# the i3-c time tier may be re-measured separately (out/timing_i3.txt) after the size change: that file wins
p3 = os.path.join(OUT, "timing_i3.txt")
if os.path.exists(p3):
    for l in open(p3, encoding="utf-8"):
        m = LINE.match(l.rstrip("\n"))
        if m:
            for k in ("i3a", "i3b", "i3c", "i3d", "i3e"):
                if m.group("name").startswith(key[k].strip()):
                    put(k + "_b", f"{float(m.group('base')):.3f}")
                    put(k + "_t", f"{float(m.group('tgt')):.3f}")
                    put(k + "_r", f"{float(m.group('ratio')):.2f}")

bad = parse_timing(os.path.join(OUT, "timing_bad.txt"), "")
p3b = os.path.join(OUT, "timing_i3_bad.txt")
if os.path.exists(p3b):                 # the i3 tier was re-measured after its sizes changed: those numbers win for the variants it covers
    for variant, rows in parse_timing(p3b, "").items():
        bad[variant] = rows
for variant, rows in bad.items():
    for name, b, t, r in rows:
        tag = name.split(" ")[0] + ("B" if "Bash" in name else "R" if "Read" in name else "")
        put(f"bad_{variant}_{tag}_r", f"{r:.1f}")
        put(f"bad_{variant}_{tag}_t", f"{t:.2f}")
# occurrence cost (occ_cost.py): ratio to the baseline hook
for sz, f in (("2k", "occ_2k.txt"), ("8k", "occ_8k.txt")):
    p = os.path.join(OUT, f)
    if not os.path.exists(p):
        continue
    for l in open(p, encoding="utf-8"):
        m = re.match(r"size=\s*(\d+) B\s+(\S+)\s+cpu=\s*([0-9.]+) s\s+ratio-to-baseline=\s*([0-9.]+)", l)
        if m:
            put(f"occ{sz}_{m.group(2)}_r", f"{float(m.group(4)):.1f}")
            put(f"occ{sz}_{m.group(2)}_cpu", f"{float(m.group(3)):.2f}")
# placeholders of proposal.md that are filled by apply_edits.py (names as written in the edit scripts)
probe_out = next((p for p in (os.path.join(EXP, "logs", "final_T.out"), os.path.join(EXP, "logs", "t5_full.out")) if os.path.exists(p)), None)
if probe_out:
    t = open(probe_out, encoding="utf-8").read()
    put("ROWS", len(re.findall(r"(?m)^SC-\d+ │ ", t)))
    m = re.search(r"differential against the built-in app.ini row over (\d+) command shapes", t)
    if m:
        put("NDIFF", m.group(1))
    m = re.search(r"identical over (\d+) hook-direct rows", t)
    if m:
        put("HOOKROWS", m.group(1))
for dst, src in (("W1_BASE", "w1a_b"), ("W1_4K", "w1a_t"), ("W1_60K", "w1b_t"), ("W1_180K", "w1c_t"), ("V4_2K", "occ2k_ext_v4stage_r"), ("V4_8K", "occ8k_ext_v4stage_r")):
    if src in N:
        put(dst, N[src])
# W2's linear-time paragraph: grep -oE CPU of the target and bad patterns (ere_claims.py) and the 16 KB prefix-removal measurement (out/val_quadratic_16k.txt)
pe = os.path.join(OUT, "ere_claims.txt")
if os.path.exists(pe):
    for l in open(pe, encoding="utf-8"):
        m = re.match(r"(\S+)\s+(target|kv_unbounded|cli_unbounded|cli_noleft)\b.*grep -oE CPU\s+([0-9.]+) s", l)
        if m:
            key = {("kv-secret-assign", "target"): "ERE_KV_B", ("kv-secret-assign", "kv_unbounded"): "ERE_KV_UNB", ("cli-secret-flag", "target"): "ERE_CLI_B",
                   ("cli-secret-flag", "cli_unbounded"): "ERE_CLI_UNB", ("cli-secret-flag", "cli_noleft"): "ERE_CLI_NOLEFT"}[(m.group(1), m.group(2))]
            v = float(m.group(3))
            put(key, f"{v:.2f}" if v < 1 else f"{v:.0f}" if v >= 10 else f"{v:.1f}")
pv = os.path.join(OUT, "val_quadratic_16k.txt")
if os.path.exists(pv):
    m = re.search(r"val_quadratic.*CPU ([0-9.]+) s", open(pv, encoding="utf-8").read())
    if m:
        put("VAL16K", f"{float(m.group(1)):.0f}")
pt = os.path.join(OUT, "probe_times.txt")
if os.path.exists(pt):
    m = re.search(r"SC-34 seconds (\d+)", open(pt, encoding="utf-8").read())
    if m:
        put("SC34SEC", m.group(1))
json.dump(N, open(os.path.join(OUT, "numbers.json"), "w"), indent=1, sort_keys=True)
for k in sorted(N):
    print(f"{k:34s} {N[k]}")
