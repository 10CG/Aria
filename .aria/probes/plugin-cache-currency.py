#!/usr/bin/env python3
"""Aria #172 probe — 本仓运行时加载的 aria-plugin 版本 vs 仓内 SOT 版本。

背景 (Aria #172): 2026-08-04 实测发现 Claude Code 加载的 plugin cache 停在
1.63.0, 而 `aria/.claude-plugin/plugin.json` (版本 SOT) 已是 1.65.5 ——
v1.64.x/v1.65.x 的全部 hook 修复在 Aria 自己的运行时从未生效, 导致仓内一切
hook/skill dogfood 验收失真 ("ship 了" ≠ "本仓用上了")。

根因是两层滞后, 本探针检测其**后果**(cache 落后 SOT), 因此两层任一断裂都会红:
  第 1 层  marketplace clone 落后上游 → Claude Code 根本不知道有新版可升
  第 2 层  plugin cache 落后 marketplace → 知道有新版但没装

判据 (全分割, 互斥且全覆盖):
  SOT 缺失/不可解析                      → SKIP  (非 meta-repo 布局, 判据不适用)
  installed_plugins.json 缺失/无 aria 记录 → SKIP  (非 marketplace 安装; 零证据
                                                   不当正证据)
  版本串不可解析                          → FAIL  (fail-closed, 不静默放行)
  min(已装版本) <  SOT                    → FAIL  STALE  ← #172 本体
  min(已装版本) == SOT                    → PASS
  min(已装版本) >  SOT                    → FAIL  AHEAD (本地子模块 checkout 陈旧)

取 min: 多条安装记录 (user/project scope) 时, 最旧的那份可能就是实际被加载的,
最坏情形governs。
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

SKIP_MARKER = "##SKIP##"
PLUGIN_KEY_SUFFIX = "@10CG-aria-plugin"
PLUGIN_NAME = "aria"
SOT_PATH = Path("aria/.claude-plugin/plugin.json")

_SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)")


def _skip(msg: str) -> int:
    print(f"{SKIP_MARKER} {msg}")
    return 0


def _fail(msg: str) -> int:
    print(msg)
    return 1


def _parse_version(raw: str):
    """'1.65.5' -> (1, 65, 5); 不匹配返回 None (调用方 fail-closed)。"""
    m = _SEMVER_RE.match((raw or "").strip().lstrip("v"))
    return tuple(int(g) for g in m.groups()) if m else None


def _config_dir() -> Path:
    env = os.environ.get("CLAUDE_CONFIG_DIR")
    return Path(env) if env else Path.home() / ".claude"


def _read_json(path: Path):
    try:
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def _marketplace_declared_version(cfg: Path) -> str | None:
    """marketplace clone 自称的版本 —— 用于分辨滞后落在第 1 层还是第 2 层。

    纯诊断信息, 不参与判决 (拿不到就不打印)。
    """
    known = _read_json(cfg / "plugins" / "known_marketplaces.json") or {}
    entry = known.get(PLUGIN_KEY_SUFFIX.lstrip("@"))
    if not isinstance(entry, dict):
        return None
    loc = entry.get("installLocation")
    if not loc:
        return None
    mf = _read_json(Path(loc) / ".claude-plugin" / "marketplace.json") or {}
    for plugin in mf.get("plugins", []) or []:
        if isinstance(plugin, dict) and plugin.get("name") == PLUGIN_NAME:
            v = plugin.get("version")
            if isinstance(v, str):
                return v
    v = mf.get("version")
    return v if isinstance(v, str) else None


def main() -> int:
    sot_raw = (_read_json(SOT_PATH) or {}).get("version")
    if not isinstance(sot_raw, str):
        return _skip(f"SOT 缺失/不可解析 ({SOT_PATH}) — 非 Aria meta-repo 布局, 判据不适用")
    sot = _parse_version(sot_raw)
    if sot is None:
        return _fail(f"MALFORMED SOT 版本串 {sot_raw!r} @ {SOT_PATH}")

    cfg = _config_dir()
    installed = _read_json(cfg / "plugins" / "installed_plugins.json")
    if not isinstance(installed, dict):
        return _skip(f"installed_plugins.json 缺失/不可解析 @ {cfg}/plugins/ — 无法判定运行时版本")

    records = []
    for key, entries in (installed.get("plugins") or {}).items():
        if not key.endswith(PLUGIN_KEY_SUFFIX):
            continue
        for e in entries if isinstance(entries, list) else []:
            if isinstance(e, dict) and isinstance(e.get("version"), str):
                records.append((e["version"], e.get("scope", "?")))
    if not records:
        return _skip(f"installed_plugins.json 无 *{PLUGIN_KEY_SUFFIX} 记录 — 非 marketplace 安装")

    bad = [v for v, _ in records if _parse_version(v) is None]
    if bad:
        return _fail(f"MALFORMED 已装版本串 {bad!r} (installed_plugins.json)")
    parsed = [(_parse_version(v) or (), v, scope) for v, scope in records]

    worst, worst_raw, worst_scope = min(parsed, key=lambda t: t[0])
    detail = f"installed={worst_raw} (scope={worst_scope}) sot={sot_raw}"
    if len(parsed) > 1:
        detail += f" [{len(parsed)} 条记录, 取最旧]"

    if worst == sot:
        print(f"OK {detail}")
        return 0

    mp = _marketplace_declared_version(cfg)
    if worst < sot:
        mp_parsed = _parse_version(mp) if mp else None
        if mp is None:
            layer = "marketplace 自称版本读取失败"
        elif mp_parsed is not None and mp_parsed < sot:
            layer = f"marketplace clone 自称 {mp} — 第 1 层滞后, 需先刷新 marketplace"
        else:
            layer = f"marketplace clone 自称 {mp} — 第 2 层滞后, marketplace 已新, 装即可"
        return _fail(f"STALE {detail} — 运行时落后 SOT; {layer} (Aria #172)")
    return _fail(f"AHEAD {detail} — 已装版本新于仓内子模块 checkout, 本地 aria/ 陈旧")


if __name__ == "__main__":
    sys.exit(main())
