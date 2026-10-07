#!/usr/bin/env python3
"""timing.py BASE_HOOK_DIR TARGET_HOOK_DIR [tiers] [--pairs N] [--gsize B] [--nrefs N] [--vlen N] [--hsegs N] [--nvars N] [--judge]

Interleaved A/B timing of the baseline hook (A) and a target hook (B) on the W14 time-budget inputs.
With --judge every bounded tier also prints `verdict=PASS|FAIL` (the W14 bounds: f <= 3.0 as a pure ratio; f0 target <= 1.5 x max(base, 100 ms); fh-a / fh-b <= 3.0; g-a / g-b <= 2.5; h2 <= 1.5; i1 / i2 <= 2.0;
i3-a..e <= 2.5; i3-f / g / h (300 KB unquoted kv value) <= 5.0; a failed liveness assertion fails the tier) and the exit code is 1 if any bounded tier fails (the unbounded ones -- h1, fh-0, w1 -- are informational).  Per run it records the CPU time
(user+sys, via RUSAGE_CHILDREN deltas -- all descendants of the hook process) and the wall time; the statistic per hook is the MINIMUM over
N interleaved runs, the verdict statistic is the CPU ratio B/A.  Values are generated at run time, nothing is printed except numbers.
tiers: f (200-entry extension, one benign segment, Bash and Read faces) / f0 (no extension file, Bash and Read faces) /
       g (W14 tier (g-a): one string of --gsize bytes [4000], --nvars assignments [8] of --vlen bytes [300], --nrefs references [40]) /
       gmax (W14 tier (g-b), the W10 caps: --gsize [4000], --nvars [16] assignments of --vlen [100] bytes, --nrefs [128] references = 16 assignments x 8 references) /
       h (16 assignments, then --hsegs ref-bearing benign segments [150], with a 200-entry extension: h1 all allowed, h2 + a last dotenv read, must stay exit 2) /
       i (dense L3 inputs: ~900 KB of bearer lines; ~600 KB of JSON password lines)
       w1 (a Read result through the L3 hook: 4 KB and 60 KB of clean prose, 180 KB of dense INI-style assignment lines; the baseline hook does not extract file.content, so A is the process-start floor)
       fhit (v5: the extension's HIT path, 200 entries, the command mentions a listed path: fh-a a 4 KB single line with one occurrence at the end, fh-b a 4 KB single line
             with 64 occurrences behind the padding; plus a no-hit control; liveness: the built-in judgement runs TWICE (the command and its substituted copy), once in the control)
       i3 (long single-line L3 inputs -- 8 KB header value, 60 KB and 100 KB runs in front of a flag / key, 8 KB blank runs, and a 300 KB UNQUOTED kv value in the three forms; ratio against the
             baseline hook, liveness = the new tag is counted by the target hook)
"""
import json
import os
import re
import resource
import secrets
import string
import subprocess
import sys
import tempfile
import time

base_dir, tgt_dir = sys.argv[1], sys.argv[2]


def opt(name, default):
    return int(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


skip_vals = {str(opt(n, -1)) for n in ("--pairs", "--gsize", "--nrefs", "--vlen", "--hsegs", "--nvars")}
args = []
for k, a in enumerate(sys.argv[3:], start=3):
    if a.startswith("--"):
        continue
    if sys.argv[k - 1].startswith("--") and a in skip_vals:
        continue
    args.append(a)
tiers = args[0].split(",") if args else ["f", "f0", "g", "gmax", "h", "i"]
pairs = opt("--pairs", 5)
gsize, hsegs = opt("--gsize", 4000), opt("--hsegs", 150)
G_A = (opt("--nvars", 8), opt("--vlen", 300), opt("--nrefs", 40))          # W14 (g-a)
G_B = (opt("--nvars", 16), opt("--vlen", 100), opt("--nrefs", 128))        # W14 (g-b): the W10 caps
hrefs = "--hrefs" in sys.argv
ALNUM = string.ascii_letters + string.digits
home = tempfile.mkdtemp(prefix="tm-")
ENV = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": home, "TMPDIR": home, "USER": "probe", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}


def alnum(n):
    return "".join(secrets.choice(ALNUM) for _ in range(n))


def run(hook, payload, env_extra=None):
    env = dict(ENV)
    if env_extra:
        env.update(env_extra)
    r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    t0 = time.time()
    p = subprocess.run(["bash", hook], input=payload, capture_output=True, env=env, timeout=900)
    wall = time.time() - t0
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    return (r1.ru_utime - r0.ru_utime) + (r1.ru_stime - r0.ru_stime), wall, p.returncode, p.stdout


def instrumented(hook_path, funcs):
    """copy of a hook with `echo FUNCNAME >> $WPA_MARKER` as the first statement of each named function (the probe's 20l / 20m / 21v / 21w technique)"""
    src = open(hook_path, encoding="utf-8").read()
    for f in funcs:
        pat = re.compile(r"^(%s\(\) \{)" % re.escape(f), re.M)
        assert pat.search(src), f
        src = pat.sub(lambda m: m.group(1) + ' echo "${FUNCNAME[0]}" >> "${WPA_MARKER:-/dev/null}";', src, count=1)
    d = tempfile.mkdtemp(prefix="live-")
    path = os.path.join(d, os.path.basename(hook_path))
    open(path, "w", encoding="utf-8").write(src)
    return path


def live_check(hook_name, payload, env_extra, funcs, expect):
    """liveness (a no-op would pass the ratio): ONE untimed run of the instrumented target hook on the same input; the set of instrumented functions that were called must equal `expect`"""
    mk = os.path.join(tempfile.mkdtemp(prefix="mk-"), "marker")
    open(mk, "w").close()
    hook = instrumented(os.path.join(tgt_dir, hook_name), funcs)
    env = dict(env_extra or {}, WPA_MARKER=mk)
    run(hook, payload, env)
    calls = set(open(mk).read().split())
    return ("ok" if calls == set(expect) else "FAIL") + "(" + ",".join(sorted(calls)) + ")"


JUDGE = "--judge" in sys.argv
JUDGED = []          # (name, passed)
BOUNDS = [("f  200", lambda b, t, r: r <= 3.0), ("f0 ", lambda b, t, r: t <= 1.5 * max(b, 0.100)), ("fh-a", lambda b, t, r: r <= 3.0), ("fh-b", lambda b, t, r: r <= 3.0),
          ("g-a", lambda b, t, r: r <= 2.5), ("g-b", lambda b, t, r: r <= 2.5), ("h2", lambda b, t, r: r <= 1.5), ("i1", lambda b, t, r: r <= 2.0), ("i2", lambda b, t, r: r <= 2.0),
          ("i3-f", lambda b, t, r: r <= 5.0), ("i3-g", lambda b, t, r: r <= 5.0), ("i3-h", lambda b, t, r: r <= 5.0), ("i3-", lambda b, t, r: r <= 2.5)]


def judge(name, base_min, tgt_min, live_text):
    """-> ' verdict=PASS|FAIL' for a bounded tier (and records it), '' for an informational tier"""
    for pre, fn in BOUNDS:
        if name.startswith(pre):
            ok = fn(base_min, tgt_min, tgt_min / max(base_min, 1e-6)) and "FAIL" not in live_text
            if name.startswith("i3-"):
                want = (True, True) if "baseline tag" in name else (False, True)
                ok = ok and ("live=" + str(want)) in live_text
            if name[:2] in ("i1", "i2"):
                ok = ok and "live=(True, True)" in live_text
            JUDGED.append((name, ok))
            return " verdict=" + ("PASS" if ok else "FAIL")
    return ""


def ab(name, hook_name, payload, env_extra=None, check=None, live=None):
    a_h, b_h = os.path.join(base_dir, hook_name), os.path.join(tgt_dir, hook_name)
    ca, cb, wa, wb, rcs = [], [], [], [], set()
    out = out2 = b""
    for _ in range(pairs):
        c, w, rc, out = run(a_h, payload, env_extra); ca.append(c); wa.append(w); rcs.add(("A", rc))
        c, w, rc, out2 = run(b_h, payload, env_extra); cb.append(c); wb.append(w); rcs.add(("B", rc))
    lv = ""
    if check:
        lv = " live=" + str(check(out, out2))
    if live:
        lv += " live-calls=" + live_check(hook_name, payload, env_extra, live[0], live[1])
    verdict = judge(name, min(ca), min(cb), lv) if JUDGE else ""
    print(f"{name:44s} CPU min base {min(ca):6.3f}s target {min(cb):6.3f}s ratio {min(cb) / max(min(ca), 1e-6):5.2f} | wall min base {min(wa):6.3f}s target {min(wb):6.3f}s | rc {sorted(rcs)}{lv}{verdict}", flush=True)


G, S = "secret-guard.sh", "secret-scan.sh"


def bash_payload(cmd):
    return json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}}).encode()


def read_payload(path):
    return json.dumps({"tool_name": "Read", "tool_input": {"file_path": path}}).encode()


if "h" in tiers:
    dot = "." + "env"
    projh = tempfile.mkdtemp(prefix="ph-")
    os.makedirs(os.path.join(projh, ".aria"))
    open(os.path.join(projh, ".aria", "secret-guard.paths"), "w").write("".join("/srv/filler/entry-%03d.conf\n" % i for i in range(200)))
    body = "; ".join(f"v{k}=/srv/data/{alnum(20)}" for k in range(16)) + "; " + "; ".join(f"echo $v{k % 16}" for k in range(hsegs))
    ab(f"h1 {hsegs} ref-bearing segments, all allowed", G, bash_payload(body), {"CLAUDE_PROJECT_DIR": projh}, live=(["_sg_vx_pass", "_sg_ext_pass"], ["_sg_vx_pass", "_sg_ext_pass"]))
    ab(f"h2 {hsegs} ref-bearing segments + dotenv read", G, bash_payload(body + "; cat " + dot), {"CLAUDE_PROJECT_DIR": projh}, live=(["_sg_vx_pass", "_sg_ext_pass"], []))
for _t, (nvars, vlen, nrefs) in (("g", G_A), ("gmax", G_B)):
    if _t not in tiers:
        continue
    names = [f"v{i}" for i in range(nvars)]
    assigns = "; ".join(f"{n}=/srv/data/{alnum(vlen)}" for n in names)
    refs = " ".join("$" + names[i % nvars] for i in range(nrefs))
    cmd = assigns + "; echo " + refs + " " + "pad " * (gsize // 4)
    cmd = cmd[:gsize]
    ab(f"{'g-a' if _t == 'g' else 'g-b'} {gsize} B string, {nvars} assign(len {vlen}), {nrefs} refs", G, bash_payload(cmd), live=(["_sg_vx_pass"], ["_sg_vx_pass"]))
if "f" in tiers or "f0" in tiers:
    proj = tempfile.mkdtemp(prefix="pj-")
    os.makedirs(os.path.join(proj, ".aria"))
    open(os.path.join(proj, ".aria", "secret-guard.paths"), "w").write("".join("/srv/filler/entry-%03d.conf\n" % i for i in range(200)))
    empty = tempfile.mkdtemp(prefix="pe-")
    if "f" in tiers:
        ab("f  200 entries, Bash benign", G, bash_payload("ls -la"), {"CLAUDE_PROJECT_DIR": proj}, live=(["_sg_ext_pass"], ["_sg_ext_pass"]))
        ab("f  200 entries, Read benign", G, read_payload("/x/README.md"), {"CLAUDE_PROJECT_DIR": proj}, live=(["_sg_ext_path_pass"], ["_sg_ext_path_pass"]))
    if "f0" in tiers:
        ab("f0 no extension, Bash benign", G, bash_payload("ls -la"), {"CLAUDE_PROJECT_DIR": empty})
        ab("f0 no extension, Read benign", G, read_payload("/x/README.md"), {"CLAUDE_PROJECT_DIR": empty})
if "fhit" in tiers:
    projf = tempfile.mkdtemp(prefix="pf-")
    os.makedirs(os.path.join(projf, ".aria"))
    HITP = "/srv/data/hit.conf"
    open(os.path.join(projf, ".aria", "secret-guard.paths"), "w").write("".join("/srv/filler/entry-%03d.conf\n" % i for i in range(199)) + HITP + "\n")
    pad = "padding-text " * 320
    def live_count(cmd, expect_calls):
        mk = os.path.join(tempfile.mkdtemp(prefix="mk-"), "marker")
        open(mk, "w").close()
        hook = instrumented(os.path.join(tgt_dir, G), ["_sg_core_eval"])
        run(hook, bash_payload(cmd), {"CLAUDE_PROJECT_DIR": projf, "WPA_MARKER": mk})
        n = open(mk).read().split().count("_sg_core_eval")
        return ("ok" if n == expect_calls else "FAIL") + "(_sg_core_eval x%d)" % n
    for name, cmd, calls in (("fh-a 4 KB single line, one occurrence at the end", "echo " + pad + "; ls " + HITP, 2),
                             ("fh-b 4 KB single line, 64 occurrences after the padding", "echo " + pad + " " + " ".join([HITP] * 64), 2),
                             ("fh-0 4 KB single line, no occurrence (control)", "echo " + pad + "; ls /x/y.conf", 1)):
        ab(name, G, bash_payload(cmd), {"CLAUDE_PROJECT_DIR": projf})
        lc = live_count(cmd, calls)
        print("   liveness:", lc, flush=True)
        if JUDGE and "FAIL" in lc and JUDGED and JUDGED[-1][0] == name:
            JUDGED[-1] = (name, False)
            print("   verdict=FAIL (liveness)", flush=True)
if "i3" in tiers:
    def scan_payload3(text):
        return json.dumps({"tool_name": "Bash", "tool_input": {"command": "x"}, "tool_response": {"stdout": text, "stderr": "", "interrupted": False, "isImage": False, "noOutputExpected": False}}).encode()
    t_ = "tok" + "en"
    unit = "aA1" * 2700
    for name, text, tag in (("i3-a 8 KB header value (auth-header-token)", "Authorization: " + t_ + " " + unit, b"auth-header-token"),
                            ("i3-b 60 KB `-` run + flag (cli-secret-flag)", "-" * 60000 + " -" + t_ + "=" + alnum(24), b"cli-secret-flag"),
                            ("i3-c 100 KB upper-case run + key (kv-secret-assign)", "A" * 100000 + " JWT_" + "SECRET=" + alnum(24), b"kv-secret-assign"),
                            ("i3-d 8 KB blank run, export form (kv-secret-assign)", "export" + " " * 8000 + "SVC_" + "TOKEN=" + alnum(24), b"kv-secret-assign"),
                            ("i3-e 8 KB bearer value (baseline tag)", "Authorization: " + "Bear" + "er " + unit, b"bearer-token"),
                            ("i3-f 300 KB unquoted value, `KEY = v` (kv-secret-assign)", "SVC_" + "TOKEN" + " = " + "aA1" * 100000, b"kv-secret-assign"),
                            ("i3-g 300 KB unquoted value, `export KEY=v` (kv-secret-assign)", "export SVC_" + "TOKEN" + "=" + "aA1" * 100000, b"kv-secret-assign"),
                            ("i3-h 300 KB unquoted value, YAML `  KEY: v` (kv-secret-assign)", "  SVC_" + "TOKEN" + ": " + "aA1" * 100000, b"kv-secret-assign")):
        ab(name, S, scan_payload3(text), check=lambda a, b, tag=tag: (tag in a, tag in b))
if "i" in tiers:
    def scan_payload(text):
        return json.dumps({"tool_name": "Bash", "tool_input": {"command": "x"}, "tool_response": {"stdout": text, "stderr": "", "interrupted": False, "isImage": False, "noOutputExpected": False}}).encode()
    hdr = "Authorization: " + "Bear" + "er "
    bearer = "".join(hdr + alnum(32) + "\n" for _ in range(16000))[:900_000]
    ab("i1 ~900 KB dense bearer lines", S, scan_payload(bearer), check=lambda a, b: (b"DETECTED" in a, b"DETECTED" in b))
    pw = "".join('{"pass' + 'word":"' + alnum(12) + '"}\n' for _ in range(24000))[:600_000]
    ab("i2 ~600 KB dense json password lines", S, scan_payload(pw), check=lambda a, b: (b"DETECTED" in a, b"DETECTED" in b))

if "w1" in tiers:
    def read_scan_payload(text):
        return json.dumps({"tool_name": "Read", "tool_input": {"file_path": "/x/doc.txt"}, "tool_response": {"type": "text", "file": {"filePath": "/x/doc.txt", "content": text, "numLines": text.count("\n") + 1, "startLine": 1, "totalLines": text.count("\n") + 1}}}).encode()
    words = ["alpha", "beta", "gamma", "delta", "config", "service", "restart", "value", "enabled", "timeout"]
    def prose(n):
        out = []
        size = 0
        while size < n:
            line = " ".join(secrets.choice(words) for _ in range(12)) + "\n"
            out.append(line)
            size += len(line)
        return "".join(out)[:n]
    ab("w1 Read 4 KB clean prose", S, read_scan_payload(prose(4_000)), check=lambda a, b: (b"DETECTED" in a, b"DETECTED" in b))
    ab("w1 Read 60 KB clean prose", S, read_scan_payload(prose(60_000)), check=lambda a, b: (b"DETECTED" in a, b"DETECTED" in b))
    ini = "".join("[sec%d]\n%s = %s\n" % (i, "SVC" + str(i) + "_SEC" + "RET", alnum(40)) for i in range(4000))[:180_000]
    ab("w1 Read 180 KB dense INI assignments", S, read_scan_payload(ini), check=lambda a, b: (b"DETECTED" in a, b"DETECTED" in b))
if JUDGE:
    bad = [n for n, ok in JUDGED if not ok]
    print(f"judge: {len(JUDGED)} bounded tiers, {len(bad)} failed" + (": " + "; ".join(bad) if bad else ""))
    sys.exit(1 if bad else 0)
