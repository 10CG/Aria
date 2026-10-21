# Flags only (no command text): for each c-spaced command, does it look like discussion text (heredoc / commit message / issue-PR body / echo-printf of docs)?
import pathlib, re, sys
import os
T = pathlib.Path(os.environ.get("TRAFFIC_DIR", "/tmp/r1traffic"))
rows = [l.split("\t") for l in (T / "classes.tsv").read_text().splitlines()]
for n, mode, orow, srow, segrow, cls in rows:
    if cls != "c-spaced":
        continue
    s = (T / "cmds" / f"{n}.txt").read_text(encoding="utf-8", errors="replace")
    f = []
    if "<<" in s: f.append("heredoc")
    if re.search(r"\bgit\s+commit\b", s): f.append("git-commit")
    if re.search(r"--body|\"body\"|'body'|body:", s): f.append("body")
    if re.search(r"\b(forgejo|gh)\s+(POST|PATCH|api|issue|pr)\b", s): f.append("api-post")
    if "`" in s: f.append("backticks")
    proj = next((l.split("\t")[1] for l in (T / "index.tsv").read_text().splitlines() if l.split("\t")[0] == n), "?")
    print(f"n={n:>5} row={srow:>4} bytes={len(s.encode()):>6} project={proj[:22]:22} flags={','.join(f) or '-'}")
