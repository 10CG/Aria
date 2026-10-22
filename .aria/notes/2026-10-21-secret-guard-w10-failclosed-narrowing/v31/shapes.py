#!/usr/bin/env python3
"""shapes.py <shape> <out file>: command texts for the 10CG/aria-plugin#217 v3.1 cases (sc-cases.sh). No credential VALUES anywhere; the
credential-shaped PATHS are assembled at run time (the hook only judges text, nothing is ever read). Each shape names what it is for."""
import sys
shape, out = sys.argv[1], sys.argv[2]
DOT = "."
CRED = "~/" + DOT + "aw" + "s/cred" + "entials"          # a credential file path
APPINI = "/etc/forg" + "ejo/app" + DOT + "ini"         # a credential-bearing config path
EXT = "/srv/billing/conf/prod.toml"                     # the path listed by the test extension file
X4000 = "x" * 4000

def filler(n, word=" y"):
    return word * (n // len(word))

S = {}
# allow path, light: whole-command mode (a parenthesis makes the command unsafe to split, so the first pass is cheap); the copy is one line of about 16 KB
# (> 8192, growth about 8000 <= 8192), no reader -> rows only (line > _SGV_LMAX), nothing matches -> allowed; the job takes well under 0.3 s
S["benign-big"] = f"(true); x={X4000}; : $x $x" + filler(4200)
# the same with a credential-path read through a variable: the rerun blocks with the longline text -> with the sed shim the job stalls in that emission
S["stall-read"] = f"(true); C={CRED}; x={X4000}; : $x $x" + filler(4200) + "; cat $C"
# count axis (post_planning R1 TL-F1): 8 references, then the read through the 9th; about 9.4 KB of short benign lines (whole mode: braces)
S["count-axis"] = f"F={APPINI}; {{ echo" + " $F" * 8 + "; cat $F; }\n" + "".join("echo " + "0" * 60 + "\n" for _ in range(140))
# the same read through the 1st reference: a multi-line copy over 8192 with no line over 8192 -> the normal finding text, never longline
S["count-axis-ctl"] = f"F={APPINI}; {{ cat $F; echo" + " $F" * 8 + "; }\n" + "".join("echo " + "0" * 60 + "\n" for _ in range(140))
# a line longer than 8192 that exists only after expansion (every raw line is short): the copy's longest line routes to rows only -> longline text
S["longline-expansion"] = f"(true)\np={X4000}\nf={APPINI}\n: $p$p" + filler(300) + "\ncat $f"
# many short lines after expansion (copy over 8192, no line over 8192) and a read with a value-redacting filter -> credit -> allowed, as in the normal judgement
S["multiline-credit"] = f"(true)\nx={'x' * 2000}\n" + "".join(": $x\n" for _ in range(4)) + "".join("echo line\n" for _ in range(40)) + f"F={APPINI}; cat $F | wc -c"
# a value over 4096 characters (VMAX): blocked in the baseline pass before any trigger point -> byte-identical to the baseline
S["vmax"] = f"v={'v' * 4097}; echo $v"
# TMAX inside the rerun (segment mode, short raw segments): each copy is 8200 characters (> 8192, growth 8188 <= 8192); the 8th brings the total over 65536
S["tmax-rerun"] = f"x={X4000}; y={'y' * 196}" + "; : $x $x $y" * 8
# extension project: the big command reads the path the extension lists (CLAUDE_PROJECT_DIR is set to a project with that entry)
S["ext-read"] = "(x=1; : $x\n" + "A" * 24000 + f"\ncat {EXT})"
# P1 sampler: commands that never reach a trigger point (each must be byte-identical to the baseline)
S["p1-small-benign"] = "ls -la /tmp && echo done"
S["p1-small-read"] = f"cat {APPINI}"
S["p1-small-read-filter"] = f"cat {APPINI} | wc -c"
S["p1-var-read"] = f"F={APPINI}; cat $F"
S["p1-var-mid"] = f"x={'x' * 1000}; : $x $x $x; echo ok"
S["p1-var-mid-read"] = f"x={'x' * 1000}; F={APPINI}; : $x $x $x; cat $F"
if shape == "list":
    print(" ".join(sorted(S))); sys.exit(0)
if shape not in S:
    raise SystemExit("unknown shape " + shape)
with open(out, "w", encoding="utf-8") as f:
    f.write(S[shape])
