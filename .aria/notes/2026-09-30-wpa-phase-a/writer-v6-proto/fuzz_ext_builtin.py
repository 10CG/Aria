#!/usr/bin/env python3
"""fuzz_ext_builtin.py HOOK [--n 1500] [--seed S]  -- random differential: a command built from fragments (readers, separators, redirections, quoting, escapes, sub-shells, heredocs, credit pipes)
with 1-3 slots `{P}`; the hook is run once with the built-in name `/etc/gitea/app.ini` in the slots (no extension file) and once with the listed entry `/srv/billing/conf/prod.toml` in the
slots (CLAUDE_PROJECT_DIR points at a project whose `.aria/secret-guard.paths` lists exactly that entry).  The two exit codes must be equal for EVERY command (the extension judges the substituted copy with the
built-in function).  Commands are only fed to the hook on stdin, never executed.  Prints the number of commands, how many the built-in blocks, and every divergence (the command text is made of fragments only)."""
import json
import os
import random
import subprocess
import sys
import tempfile
import concurrent.futures as cf

hook = os.path.abspath(sys.argv[1])
n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 1500
seed = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 20261007
rnd = random.Random(seed)
BUILTIN = "/etc/gitea/app.ini"
ENTRY = "/srv/billing/conf/prod.toml"
proj = tempfile.mkdtemp(prefix="fz-")
os.makedirs(os.path.join(proj, ".aria"))
open(os.path.join(proj, ".aria", "secret-guard.paths"), "w").write(ENTRY + "\n")
home = tempfile.mkdtemp(prefix="fzh-")
ENV = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": home, "TMPDIR": home, "USER": "fuzz", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}

READERS = ["cat {P}", "head -n 5 {P}", "tail {P}", "sed -n '1,80p' {P}", "grep -n key {P}", "awk '{{print}}' {P}", "less {P}", "cat -n {P}", "strings {P}", "cut -d= -f1 {P}",
           "python3 -c \"print(open('{P}').read())\"", "node -e \"console.log(require('fs').readFileSync('{P}','utf8'))\"", "xargs cat < {P}", "cat < {P}", "sort {P}",
           "sudo cat {P}", "env cat {P}", "time cat {P}", "nohup cat {P}", "ssh host 'cat {P}'", "docker exec c cat {P}", "bash -c 'cat {P}'", "sh -c \"cat {P}\"", "watch 'cat {P}'"]
NONREAD = ["echo {P}", "ls {P}", "ls -l {P}", "test -f {P}", "stat {P}", "chmod 600 {P}", "touch {P}", "echo hi", "true", "ls", "pwd", "echo 'see {P}'", "echo \"see {P}\"", "cd /tmp"]
SEPS = [" ; ", " && ", " || ", " | ", " & ", "\n", " ;\n", " \\\n  && "]
TAILS = ["", "", "", " | wc -l", " | sha256sum", " >/dev/null", " 2>/dev/null", " 2>&1", " 2>&1 | wc -l", " &>/dev/null", " | grep -v '^#'", " | grep '^KEY'", " | head -c 0", " \";\" | wc -l", " ';' | wc -l"]
WRAP = ["{c}", "{c}", "{c}", "( {c} )", "{{ {c}; }}", "x=$( {c} )", "x=`{c}`", "if true; then {c}; fi", "for i in 1 2; do {c}; done", "while true; do {c}; break; done", "echo ok; {c}",
        "echo \"a;b\"; {c}", "echo 'a|b'; {c}", "echo $'a\\'b;c'; {c}", "echo \"\\\";\" ; {c}", "cat <<EOF\n{P}\nEOF\n{c}", "f={P}; {c}", "[[ -f {P} ]] && {c}"]


def command():
    parts = []
    for _ in range(rnd.randint(1, 3)):
        c = rnd.choice(READERS if rnd.random() < 0.8 else NONREAD)
        c = c + (rnd.choice(TAILS) if rnd.random() < 0.25 else "")
        parts.append(rnd.choice(WRAP).replace("{c}", c))
    cmd = rnd.choice(SEPS).join(parts)
    return cmd.replace("{{", "{").replace("}}", "}")


def run(cmd, entry):
    env = dict(ENV)
    if entry:
        env["CLAUDE_PROJECT_DIR"] = proj
    p = subprocess.run(["bash", hook], input=json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}}).encode(), capture_output=True, env=env, cwd=home, timeout=120)
    return p.returncode


def one(cmd):
    return cmd, run(cmd.replace("{P}", BUILTIN), False), run(cmd.replace("{P}", ENTRY), True)


cmds = []
while len(cmds) < n:
    c = command()
    if "{P}" in c:
        cmds.append(c)
bad = []
blocked = 0
with cf.ThreadPoolExecutor(max_workers=3) as ex:
    for cmd, b, e in ex.map(one, cmds):
        blocked += (b == 2)
        if b != e:
            bad.append((cmd, b, e))
print(f"commands={len(cmds)} builtin-blocked={blocked} diverging={len(bad)} seed={seed}")
for cmd, b, e in bad[:40]:
    print(f"builtin={b} ext={e} | {cmd!r}")
