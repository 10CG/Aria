#!/usr/bin/env python3
"""stage_cost.py <kb> -- where does the CPU of the kv-secret-assign member `export<blank run>KEY=value` go?  Runs the stages separately (grep -oE with the hook's own pattern; the bash regex cuts of the value code)
and prints CPU seconds per stage.  Rule #7: the key and the value are assembled at run time; nothing but numbers is printed."""
import os
import re
import resource
import secrets
import string
import subprocess
import sys
import tempfile

kb = int(sys.argv[1])
n = kb * 1000
hook = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "work", "t6", "aria", "hooks", "secret-scan.sh")
src = open(hook, encoding="utf-8").read()
pat = re.search(r"'kv-secret-assign\|(.*)'\n", src).group(1).replace("'\"'\"'", "'")
A = string.ascii_letters + string.digits
val = "".join(secrets.choice(A) for _ in range(24))
text = "export" + " " * n + "SVC_" + "TOKEN=" + val
work = tempfile.mkdtemp(prefix="stage-")
open(os.path.join(work, "in.txt"), "w").write(text + "\n")


def cpu(fn):
    r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    fn()
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    return (r1.ru_utime - r0.ru_utime) + (r1.ru_stime - r0.ru_stime)


def grep_stage():
    return subprocess.run(["grep", "-oE", "--", pat, os.path.join(work, "in.txt")], capture_output=True, env={"LC_ALL": "C.UTF-8", "PATH": "/usr/bin:/bin"})


out = {}
out["grep_oE_utf8"] = cpu(grep_stage)
span = grep_stage().stdout.decode().rstrip("\n")
open(os.path.join(work, "span.txt"), "w").write(span)
# bash stages on the span: prefix cut regex, trim regex
script = r'''
span="$(cat "$1")"
_AZ='ABCDEFGHIJKLMNOPQRSTUVWXYZ'; _09='0123456789'
_RE_PFX_KV="^[^${_AZ}${_09}_]*[${_AZ}${_09}_]*[[:space:]]*[=:]"
_RE_TRIM='^[[:space:]]*(.*[^[:space:]])[[:space:]]*$'
case "$2" in
  pfx) [[ "$span" =~ $_RE_PFX_KV ]] ;;
  trim) [[ "$span" =~ $_RE_TRIM ]] ;;
  nop) : ;;
esac
'''
open(os.path.join(work, "st.sh"), "w").write(script)
for stage in ("nop", "pfx", "trim"):
    out["bash_" + stage] = cpu(lambda s=stage: subprocess.run(["bash", os.path.join(work, "st.sh"), os.path.join(work, "span.txt"), s], capture_output=True, env={"LC_ALL": "C.UTF-8", "PATH": "/usr/bin:/bin"}))
print(f"{kb} KB span={len(span)}", " ".join(f"{k}={v:.2f}s" for k, v in out.items()))
