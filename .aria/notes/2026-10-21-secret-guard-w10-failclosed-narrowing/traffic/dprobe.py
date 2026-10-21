# D probe for one command: where the >4096 assignment sits and which indirection-ish constructs exist. Prints booleans/counts only, never text.
import re, sys
s = open(sys.argv[1], encoding="utf-8", errors="replace").read()
rx = re.compile(r"(^|[;&|\s(\"`'])((export|declare|local|readonly|typeset)\s+(-[a-zA-Z]+\s+)*)?([A-Za-z_][A-Za-z0-9_]*)=(\"([^\"]*)\"|'([^']*)'|\$\([^)]*\)|`[^`]*`|[^\s;&|]*)")
for m in rx.finditer(s):
    name = m.group(5); val = m.group(6)
    if len(val) <= 4096: continue
    a, b = m.start(5), m.end()
    rest = s[:a] + s[b:]
    hd = [h.start() for h in re.finditer(r"<<-?\s*['\"]?[A-Za-z_]+", s)]
    inside_heredoc = any(h < a for h in hd)
    nxt = s[b:b+40].lstrip(" \t")
    follow = "end" if not nxt else ("terminator" if nxt[0] in ";&|)\n" else "other")
    print(f"value_len={len(val)} kw={bool(m.group(3))} heredoc_before_assignment={inside_heredoc} heredocs={len(hd)} follow={follow}")
    print(f"bare_name_elsewhere={name in rest} dollar_ref={('$'+name) in rest} brace_ref={('${'+name) in rest}")
    for k, p in [("eval", r"\beval\b"), ("bang_indirect", r"\$\{!"), ("declare/typeset/local", r"\b(declare|typeset|local)\b"), ("export", r"\bexport\b"), ("source/dot", r"(\bsource\b|(^|[;&|\s])\.\s)"), ("set -a/allexport", r"(set\s+-[a-zA-Z]*a|allexport)"), ("trap", r"\btrap\b"), ("python/node", r"\b(python3?|node)\b")]:
        print(f"  {k}: {len(re.findall(p, s))}")
