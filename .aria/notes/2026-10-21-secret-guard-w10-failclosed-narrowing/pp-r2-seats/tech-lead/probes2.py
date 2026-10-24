#!/usr/bin/env python3
# probes2.py OUTDIR : indirect read + a quoted metacharacter value (spliced as syntax in the copy, three plain arguments in bash); small and big multi-line
import sys, os, json
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
DOT = "."; APPINI = "/etc/forg" + "ejo/app" + DOT + "ini"
X4 = "x" * 4000
lines = "".join("echo " + "0" * 60 + "\n" for _ in range(40))
P = {
  "splice-indirect-small": "F=" + APPINI + "; G='| jq keys'; cat $F $G",
  "splice-indirect-big": "(true)\nF=" + APPINI + "\nG='| jq keys'\nx=" + X4 + "\n: $x\n: $x\n" + lines + "cat $F $G",
  "reassign-big-multiline": "(true)\nf=/tmp/x\nx=" + X4 + "\n: $x\n: $x\n" + lines + "f=" + APPINI + "\ncat $f",
}
for k, cmd in P.items():
    open(os.path.join(out, k + ".json"), "w", encoding="utf-8").write(json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}}))
print(" ".join(P))
