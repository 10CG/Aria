#!/usr/bin/env python3
"""grade_reports.py — layer-l-sweep-safety AB iteration-1 机械评分 (锚定决策字段)。"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
IT = Path(__file__).resolve().parent

CASES = [
    ("eval-0-claim-swept-signal", "with_skill",
     [r"interpretation:\s*非\s*benign", r"claim_swept", r"--restore"], []),
    ("eval-0-claim-swept-signal", "old_skill",
     [r"benign|claim_not_found|等价"], []),
    ("eval-1-routine-sweep-neighbor", "with_skill",
     [r"disposition:\s*保持不动|disposition:\s*untouched", r"7d|SWEEP_TTL_CROSS|168"], []),
    ("eval-1-routine-sweep-neighbor", "old_skill",
     [r"disposition:\s*会被改写|disposition:\s*swept|abandoned", r"24h|STALE_TTL"], []),
    ("eval-2-long-session-heartbeat", "with_skill",
     [r"12h", r"--heartbeat-only", r"claim_swept|--restore"], []),
    ("eval-2-long-session-heartbeat", "old_skill",
     [r"仅入口刷|入口.{0,6}唯一|唯一.{0,12}入口"],
     [r"12h"]),  # 旧文无 ≤12h 周期义务 (12h 是新义务专属数值, 不应出现)
]

def grade(rd, must, forbid):
    rpt = rd / "outputs" / "report.md"
    exps = []
    if not rpt.exists():
        return False, [{"text": "report.md exists", "passed": False, "evidence": "missing"}]
    text = rpt.read_text(encoding="utf-8")
    ok = True
    for pat in must:
        hit = re.search(pat, text, re.I) is not None
        ok &= hit
        exps.append({"text": f"must: {pat}", "passed": hit, "evidence": "found" if hit else "not found"})
    for pat in forbid:
        hit = re.search(pat, text, re.I) is not None
        ok &= not hit
        exps.append({"text": f"must NOT: {pat}", "passed": not hit, "evidence": "absent" if not hit else "present"})
    return ok, exps

fails = 0
for evdir, arm, must, forbid in CASES:
    rd = IT / evdir / arm
    ok, exps = grade(rd, must, forbid)
    json.dump({"expectations": exps}, (rd / "grading.json").open("w"), ensure_ascii=False, indent=2)
    fails += 0 if ok else 1
    print(("PASS" if ok else "FAIL"), evdir, arm)
print(f"{len(CASES)-fails}/{len(CASES)} pass")
sys.exit(1 if fails else 0)
