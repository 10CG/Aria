# #229 frequency in real traffic (all Bash commands, any size): for the three rows with a blank-or-EOL right boundary, count occurrences by the
# character that follows the token, and whether the occurrence sits in discussion text (inside a heredoc body or a backtick span). Aggregates only.
import json, pathlib, re, collections
root = pathlib.Path("/home/dev/.claude/projects")
ROWS = {
  "pat-tokens": re.compile(r"\b(forgejo|curl)\b[^|]*?/users/[^\s|/]+/tokens"),
  "cp-key":     re.compile(r"\bcp\s+[^|]*?(\.ssh/id_[A-Za-z0-9_]+|id_rsa|id_ed25519|id_ecdsa|\.pem|\.key)"),
  "nomad-put":  re.compile(r"nomad\s+var\s+put"),
}
OK = {"pat-tokens": set(" \t\n?/"), "cp-key": set(" \t\n"), "nomad-put": set(" \t\n")}
cnt = collections.Counter(); cmds = 0
for f in root.rglob("*.jsonl"):
    try:
        fh = f.open(encoding="utf-8", errors="replace")
    except OSError:
        continue
    with fh:
        for line in fh:
            if '"tool_use"' not in line or '"Bash"' not in line:
                continue
            try:
                o = json.loads(line)
            except Exception:
                continue
            for c in (o.get("message") or {}).get("content") or []:
                if not (isinstance(c, dict) and c.get("type") == "tool_use" and c.get("name") == "Bash"):
                    continue
                s = (c.get("input") or {}).get("command")
                if not isinstance(s, str):
                    continue
                cmds += 1
                hd = s.find("<<")
                for name, rx in ROWS.items():
                    for m in rx.finditer(s):
                        e = m.end(); nxt = s[e] if e < len(s) else "EOL"
                        disc = (hd != -1 and m.start() > hd) or (s.count("`", 0, m.start()) % 2 == 1)
                        kind = "caught" if (nxt == "EOL" or nxt in OK[name]) else f"missed[{nxt!r}]"
                        cnt[(name, "discussion" if disc else "command", kind)] += 1
print(f"bash commands scanned: {cmds}")
for (name, where, kind), n in sorted(cnt.items()):
    print(f"  {name:11s} {where:10s} {kind:14s} {n}")
