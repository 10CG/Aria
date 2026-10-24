#!/usr/bin/env python3
# probes.py OUTDIR EXTDIR : writes OUTDIR/<name>.json hook inputs. Credential-shaped paths assembled at run time; nothing is ever executed, the hook only judges text.
import sys, os, json
out, ext = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
DOT = "."
APPINI = "/etc/forg" + "ejo/app" + DOT + "ini"
CRED = "~/" + DOT + "aw" + "s/cred" + "entials"
EXTP = "/srv/billing/conf/prod.toml"
X4 = "x" * 4000
def fill(n, w=" y"): return w * (n // len(w))
P = {}
# ruling C, whole mode: a line > 8192 only after expansion, a credential read, and a value-redacting filter on another line (#139 whole-mode credit)
P["C-whole-filter-elsewhere"] = ("(true)\np=" + X4 + "\nf=" + APPINI + "\ncat $f $p$p" + fill(300) + "\necho done >/dev/null", None)
# ruling C, segment mode: the read segment's copy has a > 8192 line and a value-redacting pipe in the same segment
P["C-segment-filter"] = ("p=" + X4 + "; f=" + APPINI + "; cat $f $p$p" + fill(300) + " | wc -c", None)
# ruling C, whole mode, leading blanks: the long line is mostly blanks that exist only after expansion
P["C-whole-leading-blanks"] = ("(true)\np=\"" + " " * 4000 + "\"\nf=" + APPINI + "\n" + " " * 300 + "$p$p cat $f\necho done >/dev/null", None)
# extension project known only through the stdin cwd (no CLAUDE_PROJECT_DIR): the big command reads the listed path
P["ext-via-cwd"] = ("(x=" + X4 + "; : $x $x" + fill(4200) + "\ncat " + EXTP + ")", ext)
# count axis on the for-statement bound: the read sits in the 9th for statement of a big whole-mode command
fors = "".join("for a%d in %d; do :; done\n" % (i, i) for i in range(1, 9))
P["count-axis-for9"] = ("(true)\n" + fors + "for F in " + APPINI + "; do cat $F; done\nx=" + X4 + "\n: $x $x" + fill(4200), None)
P["count-axis-for1-ctl"] = ("(true)\nfor F in " + APPINI + "; do cat $F; done\n" + fors + "x=" + X4 + "\n: $x $x" + fill(4200), None)
# re-assignment: the later value of a re-assigned variable is never substituted (first value wins), small and big
P["reassign-small"] = ("f=/tmp/x; f=" + CRED + "; cat $f", None)
P["reassign-big"] = ("(true); f=/tmp/x; x=" + X4 + "; : $x $x" + fill(4200) + "; f=" + CRED + "; cat $f", None)
# a quoted metacharacter value spliced as syntax: in bash $G is three arguments to cat, in the copy it is a pipe (small and big)
P["splice-small"] = ("G='| wc -c'; cat " + APPINI + " $G", None)
P["splice-big"] = ("(true); G='| wc -c'; x=" + X4 + "; : $x $x" + fill(4200) + "; cat " + APPINI + " $G", None)
for k, (cmd, cwd) in P.items():
    d = {"tool_name": "Bash", "tool_input": {"command": cmd}}
    if cwd: d["cwd"] = cwd
    open(os.path.join(out, k + ".json"), "w", encoding="utf-8").write(json.dumps(d))
print(" ".join(P))
