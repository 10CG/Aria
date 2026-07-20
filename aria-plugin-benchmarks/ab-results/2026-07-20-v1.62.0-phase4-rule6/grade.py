#!/usr/bin/env python3
"""AB 评分辅助 — 机械可查的信号先跑脚本, 语义判定留人工/grader agent。

设计原则 (skill-creator 的建议 + 本仓教训): 能程序化查的就别肉眼看 —— 脚本快、
可复现、跨 iteration 可复用。但**不要**把语义断言硬塞进正则: 那会造出恒真断言,
正是本 cycle 反复在打的假绿。所以这里只产出「证据锚点」(某个概念是否在文中出现过、
出现在哪行), 由 grader 结合上下文判定 passed。
"""
from __future__ import annotations

import json
import pathlib
import re

WS = pathlib.Path(__file__).resolve().parent

# 每条断言的证据锚点 (正则, 大小写不敏感)。命中 != 通过 —— 命中只说明"提到了",
# 是否真的按该语义作答由 grader 读上下文定。
ANCHORS = {
    "A1": [r"per-remote|逐\s*remote|每个\s*remote|按 remote"],
    "A2": [r"origin", r"github"],
    "A3": [r"behind_count|落后\s*\d+|behind\s*[:=]\s*\d+"],
    "A4": [r"Everything up-to-date|已是最新|全部同步"],  # 反向锚: 命中需看是否被批判
    "A5": [r"multi_remote_drift", r"1\.35"],
    "A6": [r"git -C .* push"],
    "A7": [r"has_pending_push"],
    "A8": [r"blocking_unknown|benign|二分"],
    "A9": [r"evidence_grade", r"fresh"],
    "A10": [r"gitlink", r"clone --recursive|递归 clone|断裂"],
    "A11": [r"degrade|降级|离线|has_unreachable_remote"],
    "B1": [r"github.*落后|落后.*github|未推送"],
    "B2": [r"origin.*github|两个.*轴|本地.*origin"],
    "B3": [r"git -C aria push github"],
    "B4": [r"gitlink", r"clone --recursive|断裂"],
    "B5": [r"fetch_ok|evidence_grade"],
    "C1": [r"ahead|behind"],
    "C2": [r"pull", r"push"],
    "C3": [r"workdir_vs_tree|tree_vs_remote|工作目录.*记录"],
    "C4": [r"reason"],
}

EVAL_ASSERTIONS = {
    "eval-10-multi-remote-parity-drift": [f"A{i}" for i in range(1, 12)],
    "eval-11-submodule-push-github-sync-miss": [f"B{i}" for i in range(1, 6)],
    "eval-06-upstream-behind-control": [f"C{i}" for i in range(1, 5)],
}


def anchors_for(text: str, aid: str) -> dict:
    pats = ANCHORS.get(aid, [])
    hits = {}
    for pat in pats:
        m = [i + 1 for i, line in enumerate(text.splitlines()) if re.search(pat, line, re.I)]
        hits[pat] = m[:5]
    all_hit = all(v for v in hits.values()) if pats else False
    return {"all_patterns_hit": all_hit, "per_pattern_lines": hits}


def main() -> None:
    report: dict = {}
    for eval_dir, aids in EVAL_ASSERTIONS.items():
        d = WS / eval_dir
        if not d.exists():
            continue
        report[eval_dir] = {}
        for arm_dir in sorted(d.iterdir()):
            res = arm_dir / "outputs" / "result.md"
            if not res.is_file():
                report[eval_dir][arm_dir.name] = {"status": "MISSING"}
                continue
            text = res.read_text(encoding="utf-8", errors="replace")
            report[eval_dir][arm_dir.name] = {
                "status": "present",
                "chars": len(text),
                "anchors": {aid: anchors_for(text, aid) for aid in aids},
            }
    out = WS / "anchors.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=1))

    # 人类可读摘要
    for eval_dir, arms in report.items():
        print(f"\n=== {eval_dir} ===")
        aids = EVAL_ASSERTIONS[eval_dir]
        armnames = [a for a in arms if arms[a].get("status") == "present"]
        print("assertion  " + "  ".join(f"{a[:12]:>12}" for a in armnames))
        for aid in aids:
            row = []
            for a in armnames:
                hit = arms[a]["anchors"][aid]["all_patterns_hit"]
                row.append(f"{'HIT' if hit else '—':>12}")
            print(f"{aid:<10} " + "  ".join(row))
    print(f"\n锚点明细 -> {out}")


if __name__ == "__main__":
    main()
