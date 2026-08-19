#!/usr/bin/env python3
"""config-template-key-currency — Aria #181 的机械兜底.

断言 `.aria/config.template.json` 的 `phase_c_integrator.pre_merge_gate` 段:
  (a) 经 `_normalize_config` 归一化时 **零 DeprecationWarning**
      (模板分发弃用键 = 把 deprecation 警告直接发给新采用方 — #181 本体);
  (b) 全部键 ∈ `DEFAULT_CONFIG ∪ {_comment}`
      (代码改键名而模板没跟时, 在 alias 存在前就先红 — 类级根因).

作用域声明 (knob-granularity): 只覆盖 pre_merge_gate 段 — 它是事故发生段, 且是
仓内唯一有单一 DEFAULT_CONFIG 注册表可机械比对的段; 其他段无统一 schema 注册表,
无法 fail-closed 全模板断言 (硬编全模板白名单只会造恒红/恒绿)。若未来其他段出现
同类注册表, 应扩展本探针而非另起一个.

判据分割 (零证据不当正证据):
  模板缺失 / 段缺失 / pre_merge_gate 模块导入失败 → ##SKIP## (可见, 非 PASS 非 FAIL)
  DeprecationWarning ≥ 1 或未知键 ≥ 1                → FAIL (exit 1)
  否则                                                → OK (exit 0)

用法: python3 .aria/probes/config-template-key-currency.py [--template PATH]
      (--template 供 FAIL 路径的拒绝能力测试注入合成坏模板)
"""
from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

SKIP = "##SKIP##"
TEMPLATE = ".aria/config.template.json"
PMG_SCRIPTS = "aria/skills/phase-c-integrator/scripts"


def main() -> int:
    template = TEMPLATE
    argv = sys.argv[1:]
    if len(argv) == 2 and argv[0] == "--template":
        template = argv[1]
    elif argv:
        print(f"{SKIP} usage: config-template-key-currency.py [--template PATH]")
        return 0

    tpl_path = Path(template)
    if not tpl_path.is_file():
        print(f"{SKIP} template absent: {template}")
        return 0

    try:
        tpl = json.loads(tpl_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"FAIL template unreadable/invalid JSON: {e}")
        return 1

    sec = (tpl.get("phase_c_integrator") or {}).get("pre_merge_gate")
    if not isinstance(sec, dict):
        print(f"{SKIP} template has no phase_c_integrator.pre_merge_gate section")
        return 0

    sys.path.insert(0, PMG_SCRIPTS)
    try:
        import pre_merge_gate as pmg  # type: ignore[import]
    except Exception as e:  # submodule not initialized / moved
        print(f"{SKIP} cannot import pre_merge_gate ({e.__class__.__name__}: {e})")
        return 0

    problems: list[str] = []

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        pmg._normalize_config(dict(sec))
    dep = [str(w.message) for w in caught if issubclass(w.category, DeprecationWarning)]
    if dep:
        problems.append(f"{len(dep)} DeprecationWarning: " + " | ".join(dep))

    unknown = sorted(set(sec) - set(pmg.DEFAULT_CONFIG) - {"_comment"})
    if unknown:
        problems.append(f"unknown key(s) not in DEFAULT_CONFIG: {', '.join(unknown)}")

    if problems:
        print("FAIL " + " ;; ".join(problems))
        return 1

    print(f"OK ({len(sec)} keys, 0 deprecated, 0 unknown vs DEFAULT_CONFIG)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
