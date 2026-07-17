---
track-id: reconcile-yielded-terminal-fix
linked-issue: 10CG/aria-plugin#111
owner-container: aria-runner-bot/023236f2
phase: D-shipped
status: done
updated-at: 2026-07-17
---

# Session Handoff — reconcile clock-skew #111 fix ship v1.59.1 (含诊断纠正)

> 承接同 session 的 v1.59.0 Phase 0 ship (`docs/handoff/2026-07-17-mainspec-phase0-v1.59.0-ship.md`)。本 cycle: 修 aria-plugin #111 (Layer-L reconcile clock_skew 误报) → ship v1.59.1。**核心不是"修了个 bug", 而是"初始诊断锁定对的现象、错的修复层, TDD 的 RED-前影响面分析在实现前拦下破坏性修复"。**

## §0 入口 (新 session 优先读)

- **本 cycle 已闭环** (A→D + ship v1.59.1)。aria `19dad0b` / 主仓 gitlink `3e209d3`, 四仓双远程 parity ✓, #111 已 close, claim done。
- **无 carry-forward**。主 spec Phase 1 (core) 仍是唯一剩的大开发线 (专门 session), 见 Phase 0 handoff §6。

## §1 已完成 — reconcile clock-skew #111 fix (v1.59.1)

**现象**: phase1_gate acquire 报 clock_skew_conflict 20663s, 但容器时钟准 (vs forgejo 1s)。

**诊断纠正 (本 cycle 关键)**:
- **初始 #111 诊断**: "yielded ∉ terminal → 被当 candidate → clock_skew; 修法: 两处 `_TERMINAL_STATUSES` 加 yielded"。
- **TDD RED-前影响面分析 + 现有 golden 测试推翻它**:
  - `yielded = voluntarily paused` (concurrent_tracks.py:30), 5 个现有测试 (`test_yielded_yielded_earlier_wins` 等) 断言 yielded 是**可竞争 winner 的 active candidate**。加 terminal 破坏设计 (实测 5 测试回归)。
  - `worktree_manager.py:1068-69` 注释 "Active / yielded — do not touch": yielded worktree 被**故意保护** (暂停可恢复)。盲目加 yielded 会误删暂停 session 工作树 —— 破坏性。
- **真正根因**: clock_skew 检测 (reconcile Rule 5.1) 对**全部 candidate** (含 heartbeat 3 天前、早 stale 的历史 claim) 算 claimed_at 跨度。stale claim 的 claimed_at 是历史工作时长, 非并发时钟读数。
- **真正修复**: clock_skew 只在 **fresh (非 stale) candidate** 间算; < 2 fresh → skew undefined (None) 永不 conflict。winner 选择不变 (stale winner 由 Rule 6 stale-takeover 兜)。yielded 保持 candidate。

**产出**:
- reconcile.py Rule 5.1 fresh-only skew + 2 处 doc 同步 (review Minor)
- 3 新回归测试 (stale 排除 / 单-fresh-amid-stale #111 复现 / **genuine fresh-pair skew 仍检测**守卫)
- reconcile 58 绿 / 全量 1074 绿 (1 预存 flaky `test_two_consecutive_runs_diff_zero`, master 也 fail, 因果隔离 — reconcile 不在 scan.py 链)
- code-review PASS (0C/0I): 单调性保证 fresh⊆all → 只能抑制 conflict 不引入 false-positive; 消费者 None-safe 由不变量 `conflict⟹skew≠None` 保证
- ship v1.59.1: aria `19dad0b` / 主仓 gitlink `3e209d3` (badge/i18n/VERSION/CLAUDE.md 同步; Phase 0 SHIPPED v1.59.0 历史事实保留)
- #111 close + 诊断纠正评论 (诚实留痕)

## §3 关键教训

- 🔴 **初始诊断可能锁定对的现象、错的修复层**。#111 现象对 (yielded claim 触发 clock_skew), 但修复层错 (candidate 分类 vs skew 计算)。**修复前必做影响面分析: 读所有使用点 + 现有测试 (它们是设计意图的 SOT)。** TDD 的 RED-前分析在写production代码前拦下了破坏性修复 (加 yielded terminal 会误删 worktree + 破坏 yielded-can-win)。→ memory `feedback_impact_analysis_before_fix_existing_tests_are_design_sot`
- **同名常量语义可不同**: reconcile 与 worktree_manager 各有 `_TERMINAL_STATUSES`, 一个管"竞争 ownership", 一个管"worktree 可清理"。yielded 对前者非 terminal (可恢复竞争), 对后者也非 (保护 worktree) —— 但若为"修 bug"统一它们会双重破坏。
- **stale flaky 因果隔离取证**: `test_two_consecutive_runs_diff_zero` 在我改动 + 干净 master (stash 后) 都 fail → 预存环境 flaky (跑真 scan 打真网络, 本对话并发活跃)。用 stash 对照 + 因果链 (reconcile ∉ scan.py) 双证, 不假装全绿。

## §5 同步状态

| 维度 | 状态 |
|------|------|
| aria-plugin master | `19dad0b` **v1.59.1** 双远程 parity ✓ |
| 主仓 | `3e209d3` 双远程 parity ✓ (F10″ gitlink 全可达) |
| #111 | closed (诊断纠正 + fix) |
| 协调 ref | reconcile-yielded-terminal-fix claim **done** |
| 测试 | reconcile 58 / 全量 1074 绿 (1 预存 flaky) |

## §6 Next

同 Phase 0 handoff §6: 主 spec Phase 1 (core, 专门 session) / #165 (建议并入 Phase 2 F10″) / owner 门。本 cycle 无新增 carry。

## §8 Memory

- **[候选]** `feedback_impact_analysis_before_fix_existing_tests_are_design_sot` — 修复前必做影响面分析; 现有测试是设计意图 SOT, 会推翻"合理但错层"的诊断。**落** (与 `feedback_review_catches_critical_despite_green_tests` 相邻但正交: 那条是 review 抓 critical, 本条是 RED-前影响面拦破坏性修复)。

## Cross-references
- 同 session 前序: `docs/handoff/2026-07-17-mainspec-phase0-v1.59.0-ship.md` (v1.59.0 Phase 0 ship)
- Issue: aria-plugin #111 (closed) — 发现于查 clock_skew 告警 (查 NTP 时挖出)
- fix commit: aria `19dad0b` (v1.59.1) / 主仓 `3e209d3`
