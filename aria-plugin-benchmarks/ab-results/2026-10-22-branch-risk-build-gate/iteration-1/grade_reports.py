#!/usr/bin/env python3
"""grade_reports.py — branch-risk-build-gate AB iteration-1 机械评分。

断言全部程序化 (grep report.md 判定字段), 不需 LLM 评分。
判据 = evals.json 各 eval 的 expected_new / expected_old。
产物: 每 run 目录 grading.json {expectations:[{text,passed,evidence}]} +
汇总 pass 矩阵 stdout。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

IT = Path(__file__).resolve().parent

# (eval_dir, arm, must_match_patterns, forbid_patterns)
# must: 全部命中 (regex, ignore-case); forbid: 任一命中即 fail
CASES = [
    ("eval-0-api-mention-small-fix", "with_skill",
     [r"risk_level:\s*medium", r"mode:\s*Branch"],
     [r"risk_level:\s*high", r"mode:\s*Worktree"]),
    ("eval-0-api-mention-small-fix", "old_skill",
     [r"risk_level:\s*high", r"mode:\s*Worktree"], []),
    ("eval-1-api-change-real", "with_skill",
     [r"risk_level:\s*high", r"mode:\s*Worktree"], []),
    ("eval-1-api-change-real", "old_skill",
     [r"risk_level:\s*high", r"mode:\s*Worktree"], []),
    ("eval-2-refactor-core-module", "with_skill",
     [r"risk_level:\s*high", r"mode:\s*Worktree"], []),
    ("eval-2-refactor-core-module", "old_skill",
     [r"risk_level:\s*high", r"mode:\s*Worktree"], []),
    ("eval-3-keyword-override-empty", "with_skill",
     [r"risk_level:\s*medium", r"mode:\s*Branch",
      r"(覆盖|override|high_risk_keywords)"],
     [r"risk_level:\s*high"]),
    ("eval-3-keyword-override-empty", "old_skill",
     [r"risk_level:\s*high", r"mode:\s*Worktree"], []),
    ("eval-4-typo-low-regression", "with_skill",
     [r"risk_level:\s*low", r"mode:\s*Branch"], [r"risk_level:\s*high"]),
    ("eval-4-typo-low-regression", "old_skill",
     [r"risk_level:\s*low", r"mode:\s*Branch"], []),
    # branch-finisher: 锚定 build_verdict / overall 决策行 (非任意位置字样 —
    # 「非阻塞」「阻塞项: 空」与其他项的合法「跳过」不得误伤)
    ("eval-5-build-disabled-skip", "with_skill",
     [r"build_verdict:\s*跳过", r"overall:\s*可继续"], []),
    ("eval-5-build-disabled-skip", "old_skill",
     [r"build_verdict:\s*阻塞", r"overall:\s*不能继续"], []),
    ("eval-6-build-blocking-fail", "with_skill",
     [r"build_verdict:\s*阻塞", r"overall:\s*不能继续"], []),
    ("eval-6-build-blocking-fail", "old_skill",
     [r"build_verdict:\s*阻塞", r"overall:\s*不能继续"], []),
    ("eval-7-build-advisory-fail", "with_skill",
     [r"build_verdict:\s*警告", r"overall:\s*能继续"], []),
    ("eval-7-build-advisory-fail", "old_skill",
     [r"build_verdict:\s*阻塞", r"overall:\s*不能继续"], []),
]


def grade(run_dir: Path, must: list[str], forbid: list[str]) -> tuple[bool, list[dict]]:
    report = run_dir / "outputs" / "report.md"
    exps: list[dict] = []
    if not report.exists():
        return False, [{"text": "report.md exists", "passed": False, "evidence": "missing"}]
    text = report.read_text(encoding="utf-8")
    ok = True
    for pat in must:
        hit = re.search(pat, text, re.I) is not None
        ok &= hit
        exps.append({"text": f"must match: {pat}", "passed": hit,
                     "evidence": "found" if hit else "not found"})
    for pat in forbid:
        hit = re.search(pat, text, re.I) is not None
        ok &= not hit
        exps.append({"text": f"must NOT match: {pat}", "passed": not hit,
                     "evidence": "absent" if not hit else "unexpectedly present"})
    return ok, exps


def main() -> int:
    matrix: list[tuple[str, str, bool]] = []
    for evdir, arm, must, forbid in CASES:
        rd = IT / evdir / arm
        ok, exps = grade(rd, must, forbid)
        json.dump({"expectations": exps}, (rd / "grading.json").open("w"),
                  ensure_ascii=False, indent=2)
        matrix.append((evdir, arm, ok))
    fails = 0
    for evdir, arm, ok in matrix:
        mark = "PASS" if ok else "FAIL"
        fails += 0 if ok else 1
        print(f"{mark}  {evdir}/{arm}")
    print(f"\n{len(matrix) - fails}/{len(matrix)} runs pass")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
