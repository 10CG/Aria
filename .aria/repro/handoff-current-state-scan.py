#!/usr/bin/env python3
"""handoff / 派生文档「当前态陈述」陈旧扫描 (PR #190 pre_merge 审计 R3/R4 教训: 同一事实在 handoff /
latest.md / proposal / tasks.md / yaml / PR body 多处复述, 逐轮修实例必残余; memory `fix-the-class` /
`no-code-host-no-assertion`).

用法 (主仓根):
  python3 .aria/repro/handoff-current-state-scan.py <handoff.md> [--pr 190] [--extra file ...]
判据: 每行若命中 STALE (推送授权类 / 轮次进度类 / 旧版本·计数类 token) 且不命中 HIST_OK (历史记述白名单)
  ⇒ 残余, 打印 `<file>:<line>: <text>`; 有残余 exit 1, 否则 exit 0。
白名单是显式枚举 (fail-CLOSED): 新增历史写法须加进 HIST_OK, 不得放宽 STALE。
"""
from __future__ import annotations
import argparse, json, re, subprocess, sys, pathlib

STALE = re.compile(
    r"未推|推送授权|待授权|待 owner merge|待 owner 一句"          # 推送授权类
    r"|R1/R2 已清账|R3/R4|R3 \(\+R4\)|R1–R3 已清账|R4 稳定性确认|R[1-5] 待"  # 轮次进度类 (派生文档不得写轮次数字)
    r"|22/25|48/48|\b1457\b|\b1889\b|48 条 RED|1\.68\.0|fe32441|fad8b4b"      # 旧版本 / 计数类
)
HIST_OK = re.compile(
    r"^\| (0[678]:|1[0-9]:)"            # §1 时间线表行 (历史)
    r"|前一|原文保留|历史|已完成|亦在两端|→ v1\.68\.1|→ 清账|v1\.68\.0 → |ab-results/2026-09-02-v1\.68\.0"
    r"|1\.68\.0 `fe32441` 亦|\(fe32441\)|R1 清账|前一 fe32441|前一 fad8b4b|d1caa66 ⊇ fe32441|两 tag"
    r"|tag v1\.68\.0 / standards `fad8b4b` / 主仓 PR #190|aria `fe32441`\+tag v1\.68\.0|1\.68\.0 \+ 1\.68\.1|1\.68\.0\]"
    r"|已推|类推自授权|以「通过后合并」|推送授权已于|不再推|B9-补|\(R[1-4]\)|R[1-4] [a-z-]+ (major|minor)|第[三四]轮"
    r"|^\| \*\*H1\*\* ✅|^#+ .*(R1|R2|R3|R4) |aggregated|决策单 [BC][0-9]"
    r"|^> \*\*2026-0[0-9]-[0-9]{2} 更新|^> \*\*2026-0[0-9]-[0-9]{2} 补记|^> \*\*2026-0[0-9]-[0-9]{2} 会话收尾"  # latest.md 历史更新段
    r"|<vNEXT>|占位|外向, 待授权|均已双推|Tags published"                                   # A.2 历史 / carry 项 / 正确当前陈述
)

def scan_text(name: str, text: str) -> list[tuple[str, int, str]]:
    out = []
    for i, line in enumerate(text.split("\n"), 1):
        if STALE.search(line) and not HIST_OK.search(line):
            out.append((name, i, line.strip()[:170]))
    return out

def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("handoff"); ap.add_argument("--pr", type=int); ap.add_argument("--extra", nargs="*", default=[])
    a = ap.parse_args(argv)
    residual = []
    for f in [a.handoff, *a.extra]:
        residual += scan_text(f, pathlib.Path(f).read_text(encoding="utf-8"))
    if a.pr:
        r = subprocess.run(["forgejo", "GET", f"/repos/10CG/Aria/pulls/{a.pr}"], capture_output=True, text=True)
        try:
            residual += scan_text(f"PR#{a.pr}/body", json.loads(r.stdout)["body"])
        except Exception as exc:  # noqa: BLE001
            print(f"PR#{a.pr} body 不可读: {exc}", file=sys.stderr)
    for name, i, line in residual:
        print(f"{name}:{i}: {line}")
    print(f"residual = {len(residual)}")
    return 1 if residual else 0

if __name__ == "__main__":
    sys.exit(main())
