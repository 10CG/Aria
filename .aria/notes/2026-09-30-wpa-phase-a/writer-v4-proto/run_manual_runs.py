#!/usr/bin/env python3
"""run_manual_runs.py -- the bad implementations and controls that cannot be written as a mutbatch plan entry (they need a FULL tree, a repeat count, or the shape lines).
Writes work/archive/manual_runs.txt (and prints it).  Everything runs in private directories (HOME / TMPDIR under the experiment dir); `python3 baseline_probe.py <tree>/aria`
is run from a private snapshot of the spec directory with WPA_ONLY / WPA_ROWS narrowing.  Only exit codes / row ids / counts / tag names are printed."""
import os
import re
import shutil
import subprocess
import sys

EXP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(EXP, "work", "archive"), exist_ok=True)
SNAP = os.path.join(EXP, "work", "manual_spec")
shutil.rmtree(SNAP, ignore_errors=True)
os.makedirs(SNAP)
for f in ("baseline_probe.py", "proposal.md", "baseline-evidence.md"):
    shutil.copy(os.path.join(EXP, "spec", f), SNAP)
ENV = dict(os.environ, HOME=os.path.join(EXP, "home"), TMPDIR=os.path.join(EXP, "tmp"))
ENV.pop("WPA_BASH32", None)
ENV.pop("WPA_REQUIRE_ALL", None)
B32 = os.path.join(EXP, "bash32", "bash")
out = []


def log(s=""):
    out.append(s)
    print(s, flush=True)


def probe(tree, only, rows="", extra=None):
    env = dict(ENV, WPA_ONLY=only)
    if rows:
        env["WPA_ROWS"] = rows
    if extra:
        env.update(extra)
    p = subprocess.run(["python3", os.path.join(SNAP, "baseline_probe.py"), os.path.join(tree, "aria")], capture_output=True, text=True, env=env, cwd=SNAP)
    res = {}
    for l in p.stdout.split("\n"):
        m = re.match(r"^(SC-\d+) │ (\S+) │ (\S+) │ (.*) │ (.*) │ (.*) │ (yes|no|n/a)$", l)
        if m:
            res[m.group(2)] = (m.group(7), m.group(6))
    return p, res


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, env=ENV)


log("manual_runs -- bad implementations and controls that cannot be expressed as a mutbatch plan entry, with their results (written by work/run_manual_runs.py)")
log()
log("Why these are manual: proto/mutbatch.py builds each bad implementation as a tree that holds only aria/hooks (the replaced hook next to the unchanged target hooks) and")
log("symlinks standards; rows that read documents, test suites or the whole aria tree (SC-26 / 27 / 28 / 33) need a full tree, rows that need a repeat count need a loop.")
log("All commands: HOME / TMPDIR = private directories; `python3 baseline_probe.py <tree>/aria` run from the spec directory with WPA_ONLY / WPA_ROWS narrowing.")
log()
log("1. Documentation bad implementations (SC-26 / SC-28, proto/patch_docs.py flags on a full prototype tree; hooks and suites are the v4 prototype)")
DOC = [("--bad-sot", "facts only in the SOT version-history row; README / CHANGELOG / hook headers / VERSION patched normally"),
       ("--bad", "facts only in the SOT version-history row; no other document patched"),
       ("--bad-layer", "everything patched normally, but the new SOT clause says `L1 / L3`"),
       ("--no-scope", "everything patched normally, but the secret-scan.sh header Scope list does not name the 6 new tags"),
       ("--hdr-count", "everything patched normally, but the secret-scan.sh header gains a NEW count literal (`37 patterns, ~12 key-shape forms, 6 new tags`)"),
       ("--hdr-half-l", "everything patched normally, but the secret-scan.sh header keeps the first half of the stale sentence (`Claude Code exposes no field to replace tool_response`)"),
       ("--hdr-dangling", "everything patched normally, but the secret-guard.sh header re-points the dangling runbook reference at the non-existent `§1.3` of secret-hygiene.md"),
       ("--hdr-half-a", "everything patched normally, but the secret-guard.sh header only rewrites the FIRST line of the stale three-line sentence (keeps `style env lines + redacts`)"),
       ("--hdr-argon", "everything patched normally, but the secret-scan.sh header still claims argon2 in other words (`bcrypt password hashes, argon2 too`)"),
       ("--hdr-topcontent", "everything patched normally, but the secret-scan.sh contract keeps a top-level `\"content\"` key line and only names file.content in its comment"),
       ("--hdr-nohist", "everything patched normally, but the secret-guard.sh History block gets no entry (the change-id appears only in a code comment of the prototype)")]
target_tree = os.path.join(EXP, "work", "t4f")
p, res = probe(target_tree, "SC-26,SC-28")
log("   target tree (reference): not-yes rows = " + (", ".join(k for k, v in sorted(res.items()) if v[0] != "yes") or "none") + "   [%d SC-26 / SC-28 rows]" % len(res))
for flag, what in DOC:
    d = os.path.join(EXP, "work", "dv" + flag)
    r = sh(["bash", os.path.join(EXP, "proto", "build_docvariant.sh"), d, flag])
    p, res = probe(d, "SC-26,SC-28")
    red = sorted(k for k, v in res.items() if v[0] != "yes")
    log("   %-16s (%s)" % (flag, what))
    log("       red: %s ;  every other SC-26 / SC-28 row yes" % (", ".join(red) or "none"))
log()
log("2. SC-27 27d, secret-scan suite with the header comment but WITHOUT the self-check assertion (proto/patch_tests.py --no-selfcheck)")
d = os.path.join(EXP, "work", "t4_noselfcheck")
r = sh(["bash", os.path.join(EXP, "proto", "build_noselfcheck.sh"), d])
p, res = probe(target_tree, "SC-27", "27a,27b,27c,27d")
log("   target tree:           " + "  ".join("%s %s (%s)" % (k, v[0], v[1][:60]) for k, v in sorted(res.items())))
p, res = probe(d, "SC-27", "27a,27b,27c,27d")
log("   header-only variant:   " + "  ".join("%s %s (%s)" % (k, v[0], v[1][:60]) for k, v in sorted(res.items())))
log()
log("3. Path-form character class, the three bad implementations of rows 4n / 5l, 10 probe runs each (the padded generator excludes '+', the unpadded one excludes '=')")
for var, what in (("path_eq", "class admits '='"), ("path_plus", "class admits '+'"), ("loosepath", "any '/'-led value")):
    n4 = n5 = 0
    for i in range(10):
        w = os.path.join(EXP, "work", "pf_" + var)
        shutil.rmtree(w, ignore_errors=True)
        os.makedirs(os.path.join(w, "aria"))
        shutil.copytree(os.path.join(target_tree, "aria", "hooks"), os.path.join(w, "aria", "hooks"), symlinks=True)
        subprocess.run(["python3", os.path.join(EXP, "proto", "patch_l3.py"), os.path.join(EXP, "base", "aria", "hooks", "secret-scan.sh"),
                        os.path.join(w, "aria", "hooks", "secret-scan.sh"), "--variant", var], capture_output=True)
        p, res = probe(w, "SC-4,SC-5", "4n,5l")
        n4 += res.get("4n", ("?",))[0] == "no"
        n5 += res.get("5l", ("?",))[0] == "no"
    log("   %-10s (%s): 4n red %d/10, 5l red %d/10" % (var, what, n4, n5))
n4 = n5 = 0
for i in range(10):
    p, res = probe(target_tree, "SC-4,SC-5", "4n,5l")
    n4 += res.get("4n", ("?",))[0] == "no"
    n5 += res.get("5l", ("?",))[0] == "no"
log("   target prototype:           4n red %d/10, 5l red %d/10" % (n4, n5))
log()
log("4. SC-33 census, noentropy bad implementation (entropy floor removed) on a FULL copy of the target tree")
p, res = probe(target_tree, "SC-33")
log("   target tree:    33a %s  %s" % (res.get("33a", ("?", "?"))[0], res.get("33a", ("?", "?"))[1][:200]))
d = os.path.join(EXP, "work", "t4_noentropy")
sh(["bash", os.path.join(EXP, "proto", "build_full.sh"), d, "64", "noentropy", "v4"])
p, res = probe(d, "SC-33")
log("   noentropy:      33a %s  %s" % (res.get("33a", ("?", "?"))[0], res.get("33a", ("?", "?"))[1][:300]))
log()
log("5. Negative controls of the probe")
for lab, extra in (("a. shape lines (target tree, WPA_ONLY=SC-32, no WPA_BASH32)", {}),
                   ("   same with WPA_REQUIRE_ALL=1", {"WPA_REQUIRE_ALL": "1"})):
    env = dict(ENV, WPA_ONLY="SC-32")
    env.update(extra)
    p = subprocess.run(["python3", os.path.join(SNAP, "baseline_probe.py"), os.path.join(target_tree, "aria")], capture_output=True, text=True, env=env, cwd=SNAP)
    lines = [l for l in p.stdout.split("\n") if l.startswith(("rows not run", "baseline shape", "target shape"))]
    log("   %s: rc %d" % (lab, p.returncode))
    for l in lines:
        log("      " + l[:230])
env = dict(ENV, WPA_ONLY="SC-1", WPA_REQUIRE_ALL="1")
p = subprocess.run(["python3", os.path.join(SNAP, "baseline_probe.py"), os.path.join(target_tree, "aria")], capture_output=True, text=True, env=env, cwd=SNAP)
log("   WPA_ONLY=SC-1 (no leg rows) with WPA_REQUIRE_ALL=1: rc %d; %s" % (p.returncode, next((l[:120] for l in p.stdout.split("\n") if l.startswith("target shape")), "?")))
r = sh(["python3", os.path.join(EXP, "work", "nc15.py"), os.path.join(target_tree, "aria")])
log("   b. SC-15 (work/nc15.py: one runtime-assembled credential-shaped line appended to private copies of proposal.md, baseline_probe.py, baseline-evidence.md)")
log("      target hooks:   " + "; ".join(l for l in r.stdout.split("\n") if l.startswith("15")))
base_tree = os.path.join(EXP, "base")
r = sh(["python3", os.path.join(EXP, "work", "nc15.py"), os.path.join(base_tree, "aria")])
log("      baseline hooks: " + "; ".join(l for l in r.stdout.split("\n") if l.startswith("15")) + "   (the baseline L3 cannot see that key form -- the 2026-08-20 hole itself)")
log("   c. Impact keyword check (work/refs_check.py): see logs/refs_check.out (regex samples, 3-state scenarios, v3 criterion for contrast)")
log()
open(os.path.join(EXP, "work", "archive", "manual_runs.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
