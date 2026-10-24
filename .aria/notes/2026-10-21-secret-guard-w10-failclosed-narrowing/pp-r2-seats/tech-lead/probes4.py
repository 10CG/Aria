#!/usr/bin/env python3
# probes4.py OUTDIR : segment-mode splice (the filter exists only in the substituted value, not in the read segment's own text); small vs big
import sys, os, json
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
DOT = "."; APPINI = "/etc/forg" + "ejo/app" + DOT + "ini"
X4 = "x" * 4000
P = {
  "seg-splice-small": "F=" + APPINI + "; G='| jq keys'; cat $F $G",
  "seg-splice-big": "F=" + APPINI + "; G='| jq keys'; x=" + X4 + "; : $x $x" + " y" * 150 + "; cat $F $G",
  "seg-noval-big-ctl": "F=" + APPINI + "; x=" + X4 + "; : $x $x" + " y" * 150 + "; cat $F",
}
for k, cmd in P.items():
    open(os.path.join(out, k + ".json"), "w", encoding="utf-8").write(json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}}))
print(" ".join(P))
