#!/usr/bin/env python3
"""Generate per-seat audit dispatch files from a template + a round config JSON.

usage: gen_dispatch.py <template.md> <round-config.json> <out-dir>

round-config.json keys:
  ROUND, VERSION, SHA, PRIMARY_GOAL, SIBLING, WRITER_NOTE, ROUND_CONTEXT, SP,
  roles: {role: focus_text}
Writes <out-dir>/<checkpoint>-R<ROUND>-<role>.md and prints "<role> <sha256[:16]> <path>".
Every {PLACEHOLDER} left unfilled is a hard error (no silent half-filled dispatch).
"""
import hashlib
import json
import re
import sys
from pathlib import Path

tpl_path, cfg_path, out_dir = sys.argv[1:4]
tpl = Path(tpl_path).read_text(encoding="utf-8")
cfg = json.loads(Path(cfg_path).read_text(encoding="utf-8"))
checkpoint = cfg.get("CHECKPOINT", "post_spec")
out = Path(out_dir)
out.mkdir(parents=True, exist_ok=True)

KEYS = ["ROUND", "VERSION", "SHA", "PRIMARY_GOAL", "SIBLING", "WRITER_NOTE", "ROUND_CONTEXT", "SP"]
for role, focus in cfg["roles"].items():
    text = tpl
    for k in KEYS:
        text = text.replace("{" + k + "}", str(cfg[k]))
    text = text.replace("{ROLE}", role).replace("{FOCUS}", focus)
    # the finding-id recipe legitimately contains {category} etc.; only flag our upper-case placeholders
    left = sorted(set(re.findall(r"\{[A-Z_]{3,}\}", text)))
    if left:
        sys.exit(f"unfilled placeholders for {role}: {left}")
    p = out / f"{checkpoint}-R{cfg['ROUND']}-{role}.md"
    p.write_text(text, encoding="utf-8")
    print(role, hashlib.sha256(text.encode("utf-8")).hexdigest()[:16], p)
