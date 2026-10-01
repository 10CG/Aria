#!/usr/bin/env python3
"""Build a round config JSON for gen_dispatch.py.

usage: mk_round_cfg.py <sp> <checkpoint> <round> <version> <sha> <sibling.json> <writer_report> <writer_note_file> <round_context_file> <roles.json> <primary_goal_file> <out.json>
"""
import json
import sys
from pathlib import Path

(sp, checkpoint, rnd, version, sha, sib_path, writer_report, note_file, ctx_file, roles_file, goal_file, out) = sys.argv[1:13]
sib = json.loads(Path(sib_path).read_text(encoding="utf-8"))
remotes = " / ".join(
    "{} {} 份".format(r.get("name"), r.get("proposals_scanned") or r.get("scanned")) for r in sib.get("remotes", [])
)
if sib.get("status") == "ok" and sib.get("verdict") == "no_sibling_found":
    sibling = "`sibling_spec_probe.py` status=ok / verdict=no_sibling_found, {} proposal 完整扫描, caps={}; 本轮已完整扫描, 未发现同 issue 竞品。".format(remotes, sib.get("caps_applied"))
elif sib.get("verdict") == "sibling_found":
    sibling = "🔴 `sibling_spec_probe.py` verdict=sibling_found: 检测到 {} 份同 issue 的竞品 Spec (详见 hits)。".format(len(sib.get("hits", [])))
else:
    sibling = "未能核实 (status={}, reason={})".format(sib.get("status"), sib.get("reason"))
cfg = {
    "CHECKPOINT": checkpoint,
    "ROUND": int(rnd),
    "PREV_ROUND": int(rnd) - 1,
    "VERSION": version,
    "SHA": sha,
    "PRIMARY_GOAL": Path(goal_file).read_text(encoding="utf-8").strip(),
    "SIBLING": sibling,
    "WRITER_REPORT": writer_report,
    "WRITER_NOTE": Path(note_file).read_text(encoding="utf-8").strip(),
    "ROUND_CONTEXT": Path(ctx_file).read_text(encoding="utf-8").rstrip("\n"),
    "SP": sp,
    "roles": json.loads(Path(roles_file).read_text(encoding="utf-8")),
}
Path(out).write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
print("cfg ok", out)
