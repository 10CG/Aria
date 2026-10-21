# For one command: list assignments whose value is > 4096 chars (name, value length) and whether $name / ${name} appears elsewhere. No text printed.
import re, sys
s = open(sys.argv[1], encoding="utf-8", errors="replace").read()
rx = re.compile(r"(^|[;&|\s(\"`'])((export|declare|local|readonly|typeset)\s+(-[a-zA-Z]+\s+)*)?([A-Za-z_][A-Za-z0-9_]*)=(\"([^\"]*)\"|'([^']*)'|\$\([^)]*\)|`[^`]*`|[^\s;&|]*)")
for m in rx.finditer(s):
    name = m.group(5); val = m.group(6)
    if len(val) > 4096:
        rest = s[:m.start()] + s[m.end():]
        ref = ("$" + name) in rest or ("${" + name + "}") in rest
        quoted = val[:1] in ("'", '"')
        hd = "<<" in s
        print(f"name_len={len(name)} value_len={len(val)} quoted={quoted} referenced={ref} heredoc_in_cmd={hd} cmd_bytes={len(s.encode())}")
