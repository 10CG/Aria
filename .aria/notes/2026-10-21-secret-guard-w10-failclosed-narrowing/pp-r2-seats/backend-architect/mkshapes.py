#!/usr/bin/env python3
"""mkshapes.py <outdir>: extra e2e command texts for the demonstrations of the non-author mutants (no credential VALUES; the credential-shaped
path is assembled at run time, the hook only judges text, nothing is ever executed)."""
import sys, os, json
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
DOT = "."
APPINI = "/etc/forg" + "ejo/app" + DOT + "ini"
CRED = "~/" + DOT + "aw" + "s/cred" + "entials"
X4000 = "x" * 4000
def filler(n, word=" y"):
    return word * (n // len(word))
S = {}
# growth > 8192 in whole mode (parenthesis => whole): 4 references of 4000 characters => growth 15992
S["growth-whole"] = f"(true); f={APPINI}; a={X4000}; : $a $a $a $a; cat $f"
# growth > 8192 in segment mode (no parenthesis / brace): same, split by ;
S["growth-seg"] = f"f={APPINI}; a={X4000}; : $a $a $a $a; cat $f"
# segment mode, ONE segment whose copy is a single line over 8192 characters, reads a credential-bearing file, WITH a value-redacting filter (| wc -c)
S["seg-longline-filtered"] = f"f={APPINI}; p={X4000}; cat $f $p $p" + filler(280) + " | wc -c"
# the same unfiltered
S["seg-longline-plain"] = f"f={APPINI}; p={X4000}; cat $f $p $p" + filler(280)
# whole mode, single copy line over 8192, read WITH a filter
S["whole-longline-filtered"] = f"(true); f={APPINI}; p={X4000}; cat $f $p $p" + filler(280) + " | wc -c"
# segment-mode stall: segment 3 is the big copy; the reader is the last segment, so the job stalls in the first block text (sed shim)
S["stall-read-seg"] = f"C={CRED}; x={X4000}; : $x $x" + filler(4200) + "; cat $C"
# LMAX boundary: whole mode, the copy has exactly one line of 8192 (L=8192) or 8193 characters and an unfiltered read
def boundary(n):
    # line 2 of the COPY is "cat <APPINI> <4000 x> " + 'y' * k and has exactly n characters; the reader is hidden behind $f in the raw command
    k = n - (4 + len(APPINI) + 1 + 4000 + 1)
    return f"(true); f={APPINI}; p={X4000}\ncat $f $p " + "y" * k
S["lmax-8192"] = boundary(8192)
S["lmax-8193"] = boundary(8193)
for k, v in S.items():
    with open(os.path.join(out, k + ".txt"), "w", encoding="utf-8") as f:
        f.write(v)
    with open(os.path.join(out, k + ".json"), "w", encoding="utf-8") as f:
        json.dump({"tool_name": "Bash", "tool_input": {"command": v}}, f)
print(" ".join(sorted(S)))
