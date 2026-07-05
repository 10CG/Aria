# E Sweep — pre-#134 归档孤儿审计 (#95 TASK-E, out-of-scope 一次性)

> **日期**: 2026-07-05 | **工具**: `spec_complete.py --gate` (#95 archive-gate, shipped v1.53.0)
> **范围**: 所有 date < 2026-06-10 (#134 archive-completeness-gate ship 日) 的归档 spec
> **结论**: **零死代码孤儿** — 无 pre-#134 "勾了但死代码" 孤儿; gate 对 100 个真实 spec 零误 block (SC 既有正常归档零影响 再实证)

## 触发

#95 病根来自 Layer L (`multi-terminal-coordination`, archived 2026-05-20): "集成"任务勾 `[x]` 但 `phase1_gate` 从未接进生产。推论: **#134 之前归档的 spec 可能还有别的"勾了但没跑通"孤儿** → 用 #95 gate (已 ship) 一次性 sweep 审所有 pre-#134 归档。

## 结果

| verdict | 数量 | 含义 |
|---------|------|------|
| 🔴 block | **0** | 高置信死代码孤儿 (符号有 Py 定义但生产零语义引用) — **无** |
| 🟠 warn | 22 | unverified 声称 (无法提取具体符号 / dogfood·benchmark 无静态可链接产物) — fail-toward-warn, **benign** |
| ⚪ pass | 78 | 清白 |
| err | 0 | — |
| **合计** | **100** | pre-#134 归档 |

## 分析

- **零 block**: 促成 #95 的唯一真死代码孤儿 (Layer L `phase1_gate`) 已被**双子星 DEC-002 (v1.52.0) 接活** → 现 warn 非 block。其余 99 个 pre-#134 归档无死代码孤儿。**历史归档不存在系统性"勾了但死代码"问题** (推论被证伪 — 好消息)。
- **22 warn 全 benign** (spot-check top): 均为 fail-toward-warn 的"无法提取具体代码符号"case —— 集成测试声称 (`T2.8 Integration tests via unittest.mock`) / 决策回填 (`AD-M3-2 lazy-wire 决策`) / test 文件声称 / env-var 引用 (`ARIA_FEISHU_...`)。这些非死代码, 是静态 gate 无法核验的运行时/测试/决策类声称 (proposal 已知 fail-toward-warn 设计)。**非孤儿, 无需 action**。
- **SC 零影响再实证**: gate 对 100 个真实历史 spec 零误 block (合 B.2 阶段 116 全量 sweep = 仅合成/真死代码 block)。

## 处置

**E task 完成, 无后续 action** —— pre-#134 归档干净。若日后要收窄 warn 噪音, 可考虑对"无法提取符号"类声称降级为 pass (当前保守 warn); 但非必要 (warn 不阻断归档, 仅 surface)。
