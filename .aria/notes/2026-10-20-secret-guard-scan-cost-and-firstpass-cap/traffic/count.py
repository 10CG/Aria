# Count Bash tool_use commands in local Claude Code transcripts by byte size (aggregates only; no command text printed).
import json, pathlib, sys
root = pathlib.Path("/home/dev/.claude/projects")
files = [p for p in root.rglob("*.jsonl")]
tot = 0; big = 0; sizes = []; sess = set(); bigsess = set(); per_proj = {}
for f in files:
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
            msg = o.get("message") or {}
            for c in msg.get("content") or []:
                if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("name") == "Bash":
                    cmd = (c.get("input") or {}).get("command")
                    if not isinstance(cmd, str):
                        continue
                    n = len(cmd.encode("utf-8")); tot += 1; sess.add(str(f))
                    proj = f.relative_to(root).parts[0]; per_proj.setdefault(proj, [0, 0]); per_proj[proj][0] += 1
                    if n > 4096:
                        big += 1; sizes.append(n); bigsess.add(str(f)); per_proj[proj][1] += 1
sizes.sort()
print(f"transcript files={len(files)} with-bash={len(sess)} bash-commands={tot} over-4096-bytes={big} ({100*big/max(tot,1):.2f}%) in {len(bigsess)} files")
if sizes:
    q = lambda p: sizes[min(len(sizes)-1, int(p*len(sizes)))]
    print(f"over-4096 sizes: min={sizes[0]} p50={q(.5)} p90={q(.9)} max={sizes[-1]}; >14KB={sum(1 for s in sizes if s>14000)} >32KB={sum(1 for s in sizes if s>32000)}")
for k, (a, b) in sorted(per_proj.items(), key=lambda kv: -kv[1][0])[:8]:
    print(f"  {k[:60]:60s} bash={a:6d} over4096={b}")
