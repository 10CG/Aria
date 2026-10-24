#!/usr/bin/env python3
# probes3.py OUTDIR : Decision 14's "reverse case" -- a redirect value behind the 9th reference (whole mode); small vs big; plus within-bounds small
import sys, os, json
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
DOT = "."; APPINI = "/etc/forg" + "ejo/app" + DOT + "ini"
lines = "".join("echo " + "0" * 60 + "\n" for _ in range(140))
head = "F=" + APPINI + "; G='>/dev/null'; { echo" + " $G" * 8 + "; cat $F $G; }"
P = {
  "rev9-small": head,
  "rev9-big": head + "\n" + lines,
  "rev1-small": "F=" + APPINI + "; G='>/dev/null'; { cat $F $G; }",
}
for k, cmd in P.items():
    open(os.path.join(out, k + ".json"), "w", encoding="utf-8").write(json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}}))
print(" ".join(P))
