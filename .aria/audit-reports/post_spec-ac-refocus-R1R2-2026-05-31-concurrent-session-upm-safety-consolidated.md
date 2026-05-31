---
checkpoint: post_spec (focused re-audit, (a)/(c) portions)
mode: convergence
rounds: 2
converged: true
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-05-31T02:40:00Z
context: openspec/changes/concurrent-session-upm-safety/ (proposal.md + tasks.md) — (a)/(c) absorbed-from-sister portions
agents: [tech-lead, qa-engineer, code-reviewer]
---

# post_spec (a)/(c) focused re-audit — concurrent-session-upm-safety (CONVERGED)

> **Scope**: 仅审合并 Spec 从 sister `concurrent-track-proactive-coordination` 吸收的 **(a) 检测 / (c) fetch + collision 持久化前置** 部分是否收敛 sister R2-CARRY。(b) convention backbone 已在合并 Spec 自身 R1/R2 CONVERGED (见 `post_spec-R2-2026-05-30-concurrent-session-upm-safety-consolidated.md`)。
> **Panel**: 沿用 sister R2-CARRY 提出方 (tech-lead/qa/code-reviewer), 由其验闭合。**全程对真代码 verify (created_at-class 纪律)**。

## Verdict

**PASS** (converged, 2 rounds, no oscillation)。R1 拦截 2 Critical + 1 Important citation 缺陷 (sister R2-CARRY "修 3 citation" 合并时未真修)。

## 收敛轨迹

| Round | tech-lead | qa-engineer | code-reviewer | 结果 |
|-------|-----------|-------------|---------------|------|
| R1 | CONVERGED (C1/I3/N2/N3 CLOSED) | CONVERGED (5 qa CLOSED) | **NEEDS-FIX** (I1/I2 Critical + C1 Important citation 引错真代码) | NEEDS-FIX |
| Rev | — | — | — | 修 citation + 真签名 + coordination 全路径 + groups schema + 自身 error_kind 误述 |
| R2 | CONVERGED | CONVERGED | **CONVERGED** | **CONVERGED — 0 Critical/Important** |

## R1 关键拦截 (created_at-class citation 缺陷, code-reviewer 对真代码)

- **I1 (Critical)**: proposal 称 default-branch "沿用 `sync.py:36-41` symbolic-ref" → 真代码 `git symbolic-ref` **全 state-scanner 不存在** (grep 零命中); sync.py:37-41 是 `_ORIGIN_HEAD_REFS` ref-name 常量。**闭合**: 改为"复用常量作 fallback 顺序 + 解析机制**新实现**, 非沿用"。
- **I2 (Critical)**: 称"复用 git.py:167 ahead/behind 手法" → :167 是 `@{u}`-锁定解包行不通用。**闭合**: 改"复用 `rev-list --left-right --count HEAD...origin/<default>` pattern (sync.py:146 同手法对 @{u}, 本处对 origin/<default>), 不复用 git.py:167"。
- **C1 (Important)**: 复用表写 `_classify_collision` 输入 `tracks[]` → 真签名 `(claims: list[ClaimRecord]) -> tuple` (track_board.py:331)。**闭合**: 标真签名 + 明确"不 promote, 新写 `classify(tracks)->{kind,groups}` 避开 reconcile 链"。

## R1 Important (qa + tech-lead, 全 Rev 吸收)

- coordination.enabled 全路径锚定 `state_scanner.coordination.enabled` (DEFAULTS.json 无此 key = opt-in by design; 误读静默 false 破 disjointness)
- AC-1 切口1 source_file null-guard 显式 (upm.py:326 无 UPM 为 null → 静默)
- renderer 双轨: 读持久化 kind 供切口1/2 + 保留 reconcile 路径渲染胜负/时钟偏移行 (不回归)
- groups schema `list[{owner_container, track_ids}]` (Phase B state-snapshot-schema.md additive)

## R2-CARRY 全条复核 (sister 6 项 + N3)

| sister R2-CARRY | R2 状态 |
|-----------------|---------|
| C1 collision 迁移 (真输入 ClaimRecord 非 tracks) | CLOSED (新写 classify(tracks) 避链) |
| I3 phase1_gate 共享字段 (独立 claim-ref 源) | CLOSED (删共享说法, enabled 互斥 disjointness) |
| N2 scope 拆子 Spec | CLOSED (defer Phase B 可接受 — implementation-time partition, 契约已定) |
| N3 _track_to_claim_record lossy | CLOSED (新函数避链, lossy 不入持久化字段) |
| 3 citation (I1/I2/C1) | CLOSED (本轮 R1 拦 → Rev 修 → R2 逐行核验) |
| qa null-guard + enabled==true fixture + 中间态 smoke | CLOSED |
| AC-4 out-of-scope | CLOSED |

## 结论

(a)/(c) 已收敛, 与 (b) backbone 合并后**整体 audit 收敛** → 可进 A.2 task-planner / Phase B。核心价值: 本轮把 sister R2-CARRY "修 3 citation" 的遗漏 (合并时未真修) 对真代码逐行揪出并修复 —— 正是本 Spec 自身要治的 created_at-class 病 (引用未读码就假设的数据形状), audit 在写码前再次拦下。advisory-over-hardlock 哲学 (DEC-20260519-001) 全程保留。

**Phase B 入口提示**: TASK-000 (collision 持久化) deps=[] 可先行; step 0 评估是否拆独立 prereq Spec (实测 diff 体量) + 复核 version。
