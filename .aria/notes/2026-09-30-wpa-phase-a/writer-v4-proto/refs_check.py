#!/usr/bin/env python3
"""refs_check.py -- the mechanical closing-keyword check of the proposal's Impact section (v4), with the three states clean / violating / did-not-run.

1. the keyword regex: positives must match (rc 0, output), negatives must not (rc 1, no output)  [unchanged since v3]
2. the v4 procedure, run for real in a temporary git repository (all in a private temp dir, nothing outside is touched):
     step 1  git -C <repo> rev-list --count <start>..HEAD; echo "rc=$?"          -> must print an integer >= 1 and rc=0, else NOT-RUN
     step 2  git -C <repo> log --format=%B <start>..HEAD | grep -niE '...'; echo "rc=${PIPESTATUS[0]},${PIPESTATUS[1]}"
     step 3  [ -n "$text" ] && printf '%s' "$text" | grep -niE '...'; echo "rc=${PIPESTATUS[0]},${PIPESTATUS[1]}"       (PR title / description drafts)
   criterion (steps 2 and 3): last line exactly `rc=0,1` and no output before it = PASS; `rc=0,0` or any output before the rc line = VIOLATION; anything else = NOT-RUN
3. the v3 criterion (grep exit code only, `rc=${PIPESTATUS[1]}`, `rc=1` and no output = pass) on the same scenarios: it calls the NOT-RUN scenarios a pass (vacuous)
Every scenario prints: scenario | v4 verdict | v3 verdict.  A scenario whose v4 verdict differs from the expected one makes the script exit 1."""
import os
import shutil
import subprocess
import sys
import tempfile

RX = r"(^|[^[:alnum:]_])(close[sd]?|fix(e[sd])?|resolve[sd]?)[[:space:]:]+(https?://[^[:space:]]*/issues/|[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+#|#)(154|203|221)([^0-9]|$)"
POS = ["Closes #154", "closes #203", "Fixes 10CG/aria-plugin#154", "fixed: #221", "Resolves 10CG/Aria#221", "close https://forgejo.example/10CG/Aria/issues/221",
       "fix #154.", "Closed #203", "RESOLVED #221", "Closes: 10CG/aria-plugin#203", "feat: x\n\nCloses #154\n"]
NEG = ["Refs 10CG/aria-plugin#154", "Refs #203", "see #154", "Closes #1540", "Closes #15", "refs: 10CG/Aria#221", "closest to #154", "prefix #154 mentioned",
       "Closes #12345", "Fixes #2210", "Closes 10CG/Aria#999", ""]
bad = 0
for t in POS + NEG:
    hit = subprocess.run(["grep", "-niE", RX], input=t.encode(), capture_output=True).returncode == 0
    if hit != (t in POS):
        bad += 1
        print("REGEX WRONG:", repr(t))
print("regex samples: %d positives, %d negatives, wrong: %d" % (len(POS), len(NEG), bad))

TMP = tempfile.mkdtemp(prefix="refs-", dir=os.environ.get("TMPDIR"))
ENV = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": TMP, "GIT_CONFIG_GLOBAL": os.path.join(TMP, "gitconfig"), "GIT_CONFIG_SYSTEM": "/dev/null",
       "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid"}


def sh(script, cwd=None):
    p = subprocess.run(["bash", "-c", script], capture_output=True, text=True, env=ENV, cwd=cwd, timeout=120)
    return p.stdout


def mk_repo(msgs):
    d = tempfile.mkdtemp(prefix="repo-", dir=TMP)
    sh("git init -q -b main . && git commit -q --allow-empty -m base && git checkout -q -b work", d)
    for i, m in enumerate(msgs):
        open(os.path.join(TMP, "msg%d" % i), "w").write(m)
        sh("git commit -q --allow-empty -F %s" % os.path.join(TMP, "msg%d" % i), d)
    return d


def run_v4(repo, start, text=None):
    """-> (verdict, transcript)"""
    GREP = "grep -niE '%s'" % RX
    if text is None:
        s1 = sh('git -C %s rev-list --count %s..HEAD; echo "rc=$?"' % (repo, start))
        lines = [l for l in s1.splitlines() if l]
        n_ok = len(lines) == 2 and lines[0].isdigit() and int(lines[0]) >= 1 and lines[1] == "rc=0"
        if not n_ok:
            return "NOT-RUN", s1
        out = sh('git -C %s log --format=%%B %s..HEAD | %s; echo "rc=${PIPESTATUS[0]},${PIPESTATUS[1]}"' % (repo, start, GREP))
    else:
        open(os.path.join(TMP, "draft.txt"), "w").write(text)
        out = sh('t="$(cat %s)"; [ -n "$t" ] && printf \'%%s\' "$t" | %s; echo "rc=${PIPESTATUS[0]},${PIPESTATUS[1]}"' % (os.path.join(TMP, "draft.txt"), GREP))
    lines = out.rstrip("\n").split("\n")
    last, before = lines[-1], [l for l in lines[:-1] if l]
    if last == "rc=0,1" and not before:
        return "PASS", out
    if last == "rc=0,0" or before:
        return ("VIOLATION" if last in ("rc=0,0", "rc=0,1") else "NOT-RUN"), out
    return "NOT-RUN", out


def run_v3(repo, start, text=None):
    """the v3 criterion: grep's exit code only; no output and rc=1 = pass; output = violation; other rc = did not run"""
    GREP = "grep -niE '%s'" % RX
    if text is None:
        out = sh('git -C %s log --format=%%B %s..HEAD | %s; echo "rc=${PIPESTATUS[1]}"' % (repo, start, GREP))
    else:
        out = sh('printf \'%%s\' "$(cat %s)" | %s; echo "rc=${PIPESTATUS[1]}"' % (os.path.join(TMP, "draft.txt"), GREP))
    lines = out.rstrip("\n").split("\n")
    last, before = lines[-1], [l for l in lines[:-1] if l]
    if last == "rc=1" and not before:
        return "PASS"
    if before:
        return "VIOLATION"
    return "NOT-RUN"


clean = mk_repo(["feat: a\n\nRefs 10CG/aria-plugin#154\n", "fix: b\n\nRefs 10CG/Aria#221\n"])
viol = mk_repo(["feat: a\n\nRefs 10CG/aria-plugin#154\n", "fix: b\n\nCloses #221\n"])
SC = [("clean range, real merge-base", clean, "main", None, "PASS"),
      ("violating commit (Closes #221) in range", viol, "main", None, "VIOLATION"),
      ("start ref mistyped (does not resolve)", clean, "mastr", None, "NOT-RUN"),
      ("start empty (range is ..HEAD, no commit checked)", clean, "", None, "NOT-RUN"),
      ("repository root is not a repository", "/nonexistent-wpa-refs-check", "main", None, "NOT-RUN"),
      ("violating commit AND start mistyped", viol, "mastr", None, "NOT-RUN"),
      ("PR text clean", clean, "main", "Implements the hook changes. Refs 10CG/aria-plugin#154", "PASS"),
      ("PR text violating", clean, "main", "Closes 10CG/aria-plugin#203", "VIOLATION"),
      ("PR text empty", clean, "main", "", "NOT-RUN")]
fail = 0
print("%-52s %-10s %-10s %s" % ("scenario", "v4", "v3", ""))
for name, repo, start, text, want in SC:
    v4, _ = run_v4(repo, start, text)
    v3 = run_v3(repo, start, text)
    flag = "" if v4 == want else "   <== v4 WRONG (want %s)" % want
    fail += (v4 != want)
    note = "   (v3: vacuous pass)" if (want == "NOT-RUN" and v3 == "PASS") else ""
    print("%-52s %-10s %-10s%s%s" % (name, v4, v3, flag, note))
shutil.rmtree(TMP, ignore_errors=True)
print("v4 wrong:", fail)
sys.exit(1 if (fail or bad) else 0)
