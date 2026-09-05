#!/usr/bin/env python3
"""`handoff-current-state-scan.py` 的拒绝能力测试 (2026-09-04).

来源: PR #190 pre_merge R5 的两条 finding —— `d61b5fc9` (code-reviewer / tech-lead,
「扫描器不是 fail-CLOSED, 三形态」) 与 `d711ce91` (knowledge-manager, 三条合成对抗
输入全部 MISSED)。R4 把这个扫描器写进决策单当作 `a3bfd693` 不再复发的判据, 但当时
只验了「真实文档 residual = 0」这一个正例, **没验坏输入**
(memory `check-runs-at-baseline-first` / `adversarial-fixture`)。

跑法: `python3 .aria/repro/test_handoff_current_state_scan.py`

每条测试的「它怎么会红」写在 docstring 里。R5 点名的三条对抗输入逐字固化在
`_R5_ADVERSARIAL` 里 —— 改扫描器时若把它们放跑了, 这里立刻红。
"""
from __future__ import annotations

import importlib.util
import pathlib
import subprocess
import sys
import tempfile
import unittest

_HERE = pathlib.Path(__file__).resolve().parent
_SCANNER = _HERE / "handoff-current-state-scan.py"

_spec = importlib.util.spec_from_file_location("hcss", _SCANNER)
assert _spec and _spec.loader
scanner = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(scanner)

# R5 / knowledge-manager `d711ce91` 逐字给出的三条 —— 当时三条全部 MISSED。
# 共同形状: 一个真陈旧的轮次声称, 与一个**无关的**白名单词同行 (但不同子句)。
_R5_ADVERSARIAL = [
    "H1 四处推送已完成; PR #190 pre_merge 收敛审计 R3/R4 稳定性确认后合并",
    "推送授权已于同日给出, R1/R2 已清账 剩 R3/R4 待跑",
    "H1 (a)-(d) 已完成, R4 稳定性确认",
]

# `d61b5fc9` (ii): 旧 STALE 正向枚举只到 R4, R5 期措辞天然 fail-OPEN。
_R5_ERA_STALE = [
    "R6 稳定性确认后合并",
    "R5 = max_rounds 最后一轮, 若仍不满足 ⇒ 降级三选一",
]

# 必须**不**被误报的真实历史记述 (拆子句后仍应豁免) —— 拒绝能力不能靠提高误报换。
_MUST_STAY_EXEMPT = [
    "| 08: H1 四处推送完成 | `fe32441` | 前一 tag v1.68.0 |",
    "> **2026-09-02 更新 #2 (simonfish/023236f2, PR #190 审计中)**: owner 授权 → H1 四处推送完成",
    "轮次与结果以 `.aria/audit-reports/pre_merge-R*-…-aggregated.md` 最新一份为准",
    "推送授权已于同日给出并执行",
    "### PR #190 pre_merge 收敛审计 R3 清账 (2026-09-02; 四席 0C / 1M)",
]


class TestRejectsStaleClaims(unittest.TestCase):
    def test_r5_three_adversarial_inputs_are_caught(self):
        """R5 点名的三条必须全部 CAUGHT。

        它怎么会红: 把 HIST_OK 改回整行求值 ⇒ 同行的 `已完成` / `推送授权已于`
        会把另一子句里的 `R3/R4` / `R4 稳定性确认` 一起赦免 ⇒ 三条全 MISSED ⇒ 红。
        这正是 v1.69.0 及之前的行为。
        """
        for text in _R5_ADVERSARIAL:
            with self.subTest(text=text):
                self.assertTrue(scanner.scan_text("synthetic", text), f"MISSED: {text}")

    def test_r5_era_wording_is_caught(self):
        """R5–R9 期措辞必须被 STALE 认出。

        它怎么会红: STALE 枚举退回只到 R4 ⇒ 这两条 STALE=0 ⇒ 空结果 ⇒ 红。
        """
        for text in _R5_ERA_STALE:
            with self.subTest(text=text):
                self.assertTrue(scanner.scan_text("synthetic", text), f"MISSED: {text}")

    def test_genuine_historical_lines_stay_exempt(self):
        """真实历史记述不得被误报 —— 否则「提高拒绝能力」只是把假绿换成假红。

        它怎么会红: 子句窗口取得过窄 / 结构性白名单漏掉某种行首形态 ⇒ 这些行被
        flag ⇒ 红。修的时候要加**精确**的白名单条目, 不要放宽 STALE。
        """
        for text in _MUST_STAY_EXEMPT:
            with self.subTest(text=text):
                self.assertEqual(scanner.scan_text("synthetic", text), [], f"误报: {text}")


class TestFailClosedExitCodes(unittest.TestCase):
    def test_unreadable_input_file_exits_2_and_prints_no_residual(self):
        """输入文件不可读 ⇒ exit 2, 且**不得**打印 `residual = 0`。

        它怎么会红: 回到旧版 (读失败直接抛 / 或吞掉继续) ⇒ 要么 traceback,
        要么 exit 0 + `residual = 0` —— 「没扫成」被读成「零残余」⇒ 红。
        """
        with tempfile.TemporaryDirectory() as td:
            missing = str(pathlib.Path(td) / "nope.md")
            proc = subprocess.run(
                [sys.executable, str(_SCANNER), missing],
                capture_output=True, text=True, timeout=60,
            )
            self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
            self.assertNotIn("residual =", proc.stdout)
            self.assertNotIn("Traceback", proc.stderr)

    def test_pr_body_unreadable_exits_2(self):
        """`--pr` 取不到 body ⇒ exit 2, 不打 `residual = 0` (d61b5fc9 形态 iii)。

        用一个假的 `forgejo` (回 `{}`, 没有 `body` 键) 顶替 PATH 上的真 CLI ——
        与 R5 code-reviewer 的复现手法相同, 不打真网络。
        它怎么会红: 回到旧版 ⇒ 仅 stderr 一行, 仍 `residual = 0` + exit 0 ⇒ 红。
        """
        with tempfile.TemporaryDirectory() as td:
            tdp = pathlib.Path(td)
            (tdp / "clean.md").write_text("# 干净文档\n无陈旧陈述。\n", encoding="utf-8")
            fake = tdp / "bin" / "forgejo"
            fake.parent.mkdir()
            fake.write_text("#!/bin/sh\necho '{}'\n", encoding="utf-8")
            fake.chmod(0o755)
            import os
            env = dict(os.environ, PATH=f"{fake.parent}:{os.environ.get('PATH', '')}")
            proc = subprocess.run(
                [sys.executable, str(_SCANNER), str(tdp / "clean.md"), "--pr", "190"],
                capture_output=True, text=True, timeout=60, env=env,
            )
            self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
            self.assertNotIn("residual =", proc.stdout)
            self.assertIn("扫描未完成", proc.stderr)

    def test_clean_document_exits_0(self):
        """正控: 干净文档 ⇒ exit 0 + `residual = 0` (三态里的第三态)。"""
        with tempfile.TemporaryDirectory() as td:
            f = pathlib.Path(td) / "clean.md"
            f.write_text("# 干净文档\n\n本 cycle 已归档, 无未闭合项。\n", encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(_SCANNER), str(f)],
                capture_output=True, text=True, timeout=60,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("residual = 0", proc.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
