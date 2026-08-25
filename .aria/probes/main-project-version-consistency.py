#!/usr/bin/env python3
"""主项目版本 (root VERSION 头部) 与其全部当前值引用点的一致性。

背景 (owner 2026-08-25 裁定): root `VERSION` 头部 `> **版本**: X` 是主项目版本的
SOT (`standards/conventions/version-management.md` §4.3 meta-repo: "VERSION 文件即
SOT, 不打 tag")。但该值在 2026-08-16 两次 bump (1.7.3→1.7.4→1.7.5) 时**只改了头部**,
其余 8 个当前值引用点全部留在 1.7.3 / 1.7.0, 漂移存活 9 天无人察觉。

根因 = Aria#177 点名的类级问题: CLAUDE.md 的「发布同步面」14 点清单**全部是
aria-plugin 版本**, 主项目版本这条线**从来没有同步面清单**, 每次靠改的人顺手。
两条 custom check (m6-version-badge-match / i18n-readme-translation-currency) 同样
只比插件版本 ⇒ 主项目版本漂移在机械层完全不可见。

⚠️ 一处易被当成"死条目"的落点: `VERSION` 的 `## 版本号` 裸 semver 代码块。它看起来
与头部重复, 但**任何 `_read_version_file()` 式解析器 (首个裸 semver 行胜) 读到的是
它而不是头部** —— 例如 aria issue-triage 的 5 路链 path 3。本仓因 path 1
(`aria/.claude-plugin/plugin.json`) 先命中而暂未受害, 但该块是机械入口不是装饰,
必须同步而不是删除。

判据 (全分割, 互斥且全覆盖):
  VERSION 缺失 / 头部不可解析            → FAIL (fail-closed, SOT 不可读不静默放行)
  任一引用点文件缺失                      → FAIL (清单与仓库结构脱节)
  任一引用点值 != SOT                     → FAIL 列出全部漂移点
  全部一致                                → PASS

新增引用点时须同步加进下方 POINTS —— 本 check 的覆盖面等于该清单, 不多不少
(它自己就是"同步面清单"的机读形态)。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# (相对路径, 正则, 说明). 正则须恰含一个捕获组 = 该点声称的主项目版本。
POINTS: list[tuple[str, str, str]] = [
    ("VERSION", r"^## 版本号\n\n```\n(\d+\.\d+\.\d+)\n```", "VERSION `## 版本号` 裸 semver 块 (机械解析入口)"),
    ("VERSION", r"^## 对应 Tag\n\n```\nv(\d+\.\d+\.\d+)\n```", "VERSION `## 对应 Tag` 块"),
    ("CLAUDE.md", r"主项目 v(\d+\.\d+\.\d+)", "CLAUDE.md 项目状态段"),
    ("README.md", r"Project Version:\s+(\d+\.\d+\.\d+)", "README.md Project Status"),
    ("README.zh.md", r"Project Version:\s+(\d+\.\d+\.\d+)", "README.zh.md Project Status"),
    ("README.ja.md", r"Project Version:\s+(\d+\.\d+\.\d+)", "README.ja.md Project Status"),
    ("README.ko.md", r"Project Version:\s+(\d+\.\d+\.\d+)", "README.ko.md Project Status"),
    ("docs/architecture/system-architecture.md", r"\| Aria main repo \| v(\d+\.\d+\.\d+) \|", "系统架构 版本流表"),
    ("docs/architecture/version-scheme.md", r"\| \*\*Aria main repo\*\* \| `/home/dev/Aria/` \| v(\d+\.\d+\.\d+) \|", "版本方案 版本流表"),
]

HEADER_RE = re.compile(r"^> \*\*版本\*\*:\s*(\d+\.\d+\.\d+)\s*$", re.MULTILINE)


def _fail(msg: str) -> int:
    print(f"FAIL {msg}")
    return 1


def main() -> int:
    vf = ROOT / "VERSION"
    if not vf.is_file():
        return _fail("root VERSION 缺失 — 主项目版本 SOT 不存在")
    try:
        text = vf.read_text(encoding="utf-8")
    except OSError as exc:
        return _fail(f"root VERSION 读取失败: {exc}")

    m = HEADER_RE.search(text)
    if not m:
        return _fail("root VERSION 头部 `> **版本**: X.Y.Z` 不可解析 — SOT 形态已变, 判据须同步更新")
    sot = m.group(1)

    drift: list[str] = []
    missing: list[str] = []
    for rel, pattern, label in POINTS:
        p = ROOT / rel
        if not p.is_file():
            missing.append(f"{rel} ({label})")
            continue
        body = p.read_text(encoding="utf-8")
        hit = re.search(pattern, body, re.MULTILINE)
        if not hit:
            missing.append(f"{rel}:{label} — 匹配不到版本声明 (格式漂移或该点已被删)")
            continue
        if hit.group(1) != sot:
            drift.append(f"{rel} ({label}) = {hit.group(1)}")

    if missing:
        return _fail(f"SOT={sot}; {len(missing)} 个引用点不可读: " + " · ".join(missing))
    if drift:
        return _fail(
            f"SOT={sot} (root VERSION 头部), 但 {len(drift)}/{len(POINTS)} 个引用点漂移: "
            + " · ".join(drift)
        )
    print(f"OK 主项目版本 {sot} — {len(POINTS)} 个引用点全部一致")
    return 0


if __name__ == "__main__":
    sys.exit(main())
