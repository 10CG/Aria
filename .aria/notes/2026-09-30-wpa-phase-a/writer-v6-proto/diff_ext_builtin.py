#!/usr/bin/env python3
"""diff_ext_builtin.py HOOK [--show-all]  -- differential: the project extension entry vs the built-in `app.ini` row, command shape by command shape.

For every command template (`{P}` = the path) the hook is run twice: with the built-in name `/etc/gitea/app.ini` as {P} (no extension file in play), and with the
extension entry `/srv/billing/conf/prod.toml` as {P} (CLAUDE_PROJECT_DIR points at a project whose `.aria/secret-guard.paths` lists exactly that entry).  The two exit codes
must be equal for every shape (the extension reuses the built-in judgement, so the shapes where the built-in row over- or under-blocks are inherited on purpose).
Commands are only fed to the hook on stdin, never executed.  The template table is a larger, independent battery (93 shapes) that overlaps the 73 shapes of probe row 19af (the probe table is the one the Spec cites; this battery has 22 more shapes and
different labels for two of the probe's); the probe row is the criterion, this script is the wider cross-check."""
import json
import os
import subprocess
import sys
import tempfile

hook = sys.argv[1]
BUILTIN = "/etc/gitea/app.ini"
ENTRY = "/srv/billing/conf/prod.toml"

# (label, template).  Templates holding a newline are written with \n.
SHAPES = [
    # --- plain readers, credit pipes
    ("cat", "cat {P}"),
    ("sed-n", "sed -n '1,80p' {P}"),
    ("grep-n", "grep -n key {P}"),
    ("head", "head -n 5 {P}"),
    ("cat-wc", "cat {P} | wc -l"),
    ("cat-sha", "cat {P} | sha256sum"),
    ("cat-grep-v", "cat {P} | grep -v '^#'"),
    ("cat-grep-anch", "cat {P} | grep '^KEY'"),
    ("cat-head-pipe", "cat {P} | head -n 3"),
    ("cat-devnull", "cat {P} >/dev/null"),
    ("cat-2devnull", "cat {P} 2>/dev/null"),
    # --- separators
    ("semi-before", "echo hi; cat {P}"),
    ("semi-after", "cat {P}; echo hi"),
    ("and-and", "true && cat {P}"),
    ("or-or", "false || cat {P}"),
    ("or-or-pipe", "cat {P} || echo bad | wc -l"),
    ("pipe-first", "ls | grep y; echo {P}"),
    ("bare-mention", "echo {P}"),
    ("reader-then-mention", "cat x; echo {P}"),
    ("mention-then-reader", "echo {P}; cat {P}"),
    ("newline-sep", "cat x\necho {P}"),
    ("newline-reader", "echo hi\ncat {P}"),
    ("background-amp", "cat x & echo {P}"),
    ("background-reader", "echo hi & cat {P}"),
    ("pipe-reader-later", "cat x | echo {P}"),
    # --- line continuation
    ("cont-cat", "cat \\\n  {P}"),
    ("cont-sed", "sed -n '1,80p' \\\n  {P}"),
    ("cont-after-pipe", "cat {P} \\\n  | wc -l"),
    ("cont-mid", "cat \\\n  -n \\\n  {P}"),
    # --- redirections with &
    ("redir-2to1-wc", "cat {P} 2>&1 | wc -l"),
    ("redir-2to1-sha", "cat {P} 2>&1 | sha256sum"),
    ("redir-amp-gt", "cat {P} &>/dev/null"),
    ("redir-2to1-devnull", "cat {P} 2>&1 >/dev/null"),
    ("redir-1to2-wc", "cat {P} 1>&2 | wc -c"),
    ("redir-pipe-amp", "cat {P} |& wc -l"),
    ("redir-2to1-plain", "cat {P} 2>&1"),
    ("redir-2to1-cont", "cat {P} \\\n  2>&1 | wc -l"),
    # --- quoting and escapes
    ("dq-path", 'cat "{P}"'),
    ("sq-path", "cat '{P}'"),
    ("quoted-semicolon-after", 'cat {P} ";" | wc -l'),
    ("quoted-semicolon-before", 'echo ";" && cat {P}'),
    ("escaped-semicolon", "cat x\\; cat {P}"),
    ("escaped-amp", "cat x\\& {P}"),
    ("py-semi", "python3 -c \"import os; print(open('{P}').read())\""),
    ("py-two-semi", "python3 -c \"x=1; y=2; print(open('{P}').read())\""),
    ("py-escaped-dq", "python3 -c \"print(\\\"a\\\"); print(open('{P}').read())\""),
    ("py-escaped-dq-semi", "python3 -c \"print(\\\"a;b\\\"); print(open('{P}').read())\""),
    ("py-ansi-c", "python3 -c $'import os; print(\\'x\\'); print(open(\\'{P}\\').read())'"),
    ("node-ansi-c", "node -e $'const fs=require(\\'fs\\'); console.log(fs.readFileSync(\\'{P}\\'))'"),
    ("node-semi", "node -e \"const fs=require('fs'); console.log(fs.readFileSync('{P}','utf8'))\""),
    ("awk-semi", "awk 'BEGIN{x=1; while ((getline l < \"{P}\") > 0) print l}'"),
    ("py-newline", "python3 -c \"import os\nprint(open('{P}').read())\""),
    ("py-amp", "python3 -c \"a=1 & 2; print(open('{P}').read())\""),
    ("py-quoted-pipe", "python3 -c \"print(1|2); print(open('{P}').read())\""),
    ("grep-quoted-pipe", "grep -E 'A|B' {P}"),
    ("py-inner-pipe-wc", "bash -c 'cat {P} | wc -l'"),
    ("py-dq-in-sq", "python3 -c '\"; print(open(\"{P}\").read())'"),
    ("sq-in-dq", "echo \"it's\"; cat {P}"),
    # --- degraded (whole-command) judgement: block characters, keywords, background, heredoc
    ("cmdsubst", "x=$(cat {P})"),
    ("cmdsubst-wc", "x=$(cat {P} | wc -l)"),
    ("backticks", "x=`cat {P}`"),
    ("subshell", "(cat {P})"),
    ("brace-group", "{ cat {P}; }"),
    ("heredoc", "cat <<EOF\n{P}\nEOF"),
    ("heredoc-reader", "cat {P} <<EOF\nx\nEOF"),
    ("dbl-bracket", "[[ -f {P} ]] && cat {P}"),
    ("if-block", "if true; then cat {P}; fi"),
    ("for-block", "for i in 1 2; do cat {P}; done"),
    ("while-block", "while true; do cat {P}; break; done"),
    ("degraded-semicolon", "x=$(true); echo hi; cat x; echo {P}"),
    ("degraded-mention", "x=$(true); echo {P}"),
    ("exec-prefix", "exec cat {P}"),
    ("time-prefix", "time cat {P}"),
    # --- wrappers
    ("ssh-quoted", "ssh host 'cat {P}'"),
    ("docker-exec", "docker exec c cat {P}"),
    ("sh-c", "sh -c 'cat {P}'"),
    ("sudo", "sudo cat {P}"),
    ("xargs", "echo {P} | xargs cat"),
    ("find-exec", "find /srv -name x -exec cat {P} \\;"),
    # --- variable indirection (W10) and others
    ("var-indirect", "f={P}; cat \"$f\""),
    ("var-indirect-wc", "f={P}; cat \"$f\" | wc -l"),
    ("ls-l", "ls -l {P}"),
    ("chmod", "chmod 600 {P}"),
    ("cp", "cp {P} /tmp/x"),
    ("cat-then-mention-wc", "cat x | wc -l; echo {P}"),
    ("tee-redirect", "tee < {P}"),
    ("while-read", "while IFS= read -r l; do echo \"$l\"; done < {P}"),
    ("source", "source {P}"),
    ("diff", "diff {P} /tmp/y"),
    ("sort-uniq", "sort {P} | uniq"),
    ("nl-pipe-cut", "nl {P} | cut -d= -f1"),
    ("cat-multi-occurrence", "cat {P} {P}"),
    ("cat-then-ls-occurrence", "ls {P}; cat {P}"),
]


def run(path_value, proj, cmd):
    home = tempfile.mkdtemp(prefix="de-")
    env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": home, "TMPDIR": home, "USER": "probe", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    if proj:
        env["CLAUDE_PROJECT_DIR"] = proj
    p = subprocess.run(["bash", hook], input=json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}}).encode(), capture_output=True, env=env, timeout=120)
    return p.returncode


proj = tempfile.mkdtemp(prefix="dp-")
os.makedirs(os.path.join(proj, ".aria"))
open(os.path.join(proj, ".aria", "secret-guard.paths"), "w").write(ENTRY + "\n")
bad = 0
n_block = 0
for lab, tpl in SHAPES:
    b = run(BUILTIN, None, tpl.replace("{P}", BUILTIN))
    e = run(ENTRY, proj, tpl.replace("{P}", ENTRY))
    n_block += (b == 2)
    flag = "" if b == e else "   <== DIVERGES"
    bad += (b != e)
    if flag or "--show-all" in sys.argv:
        print(f"builtin={b} ext={e} | {lab:24s} | {tpl[:90]!r}{flag}")
print(f"shapes={len(SHAPES)} builtin-blocked={n_block} diverging={bad}")
