# Write every Bash tool_use command > 4096 bytes from local transcripts to cmds/<n>.txt (raw bytes, no newline added) + index.tsv (n, project, bytes). No text printed.
import json, pathlib
import os
root = pathlib.Path("/home/dev/.claude/projects"); W = pathlib.Path(os.environ.get("TRAFFIC_DIR", "/tmp/r1traffic")); out = W / "cmds"; out.mkdir(parents=True, exist_ok=True)  # real command text: keep OUTSIDE the repo
idx = []; seen = set(); n = 0
for f in sorted(root.rglob("*.jsonl")):
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
                if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("name") == "Bash":
                    cmd = (c.get("input") or {}).get("command")
                    if not isinstance(cmd, str):
                        continue
                    b = cmd.encode("utf-8")
                    if len(b) <= 4096 or b in seen or b"\x00" in b:
                        continue
                    seen.add(b); n += 1
                    (out / f"{n}.txt").write_bytes(b)
                    idx.append(f"{n}\t{f.relative_to(root).parts[0]}\t{len(b)}")
(W / "index.tsv").write_text("\n".join(idx) + "\n")
print(f"unique commands over 4096 bytes: {n}")
