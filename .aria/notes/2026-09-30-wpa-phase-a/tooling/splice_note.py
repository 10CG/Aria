#!/usr/bin/env python3
"""Replace the placeholder controller section of an aggregated audit report with a note file.

usage: splice_note.py <aggregated.md> <note.md>
"""
import sys
from pathlib import Path

agg, note = Path(sys.argv[1]), Path(sys.argv[2])
placeholder = "## 主控记录\n\n(主控在落盘后追加)\n"
s = agg.read_text(encoding="utf-8")
if placeholder not in s:
    sys.exit("placeholder not found (already spliced?)")
s = s.replace(placeholder, note.read_text(encoding="utf-8"))
agg.write_text(s, encoding="utf-8")
print("spliced", agg.name, len(s))
