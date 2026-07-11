# Proposal: 协调机制 3 缺陷修复 — claim 生命周期 + 语义重叠 + 认领强制

> **Status**: ✅ Shipped v1.56.0 (2026-07-11) — Phase B 全三部件实现 (aria PR#106 merge `504da89`); pre-merge 对抗 review R1 1 Critical (sweep TTL 误杀活 session → SWEEP_TTL=24h) + 5 Important 全修; 测试 968→1006; 一次性清理真协调 ref 完成 (唯一 active = 本 cycle claim, 收尾 D.2b 释放)。orchestrator follow-up (defect a Layer 2 维度) 另行开票。
> **Level**: 3 (Full — blast radius: 改 DEC-002 Layer L 协调机制, 影响多终端/多 session 撞车防护)
> **Created**: 2026-07-11
> **Source**: 2026-07-11 双子星撞车实战暴露 (aria-runner-bot 与 simonfish 并发做同一批 secret-guard, claim gate 未拦)
> **Recon**: Explore agent 全代码 recon (见下 §现状), 3 缺陷分档: (c) 可实现 / (a) 部分跨运行时 / (b) 需设计

## Why

DEC-002 Layer L advisory 协调本应防止两个 session 做同一件事。2026-07-11 实战暴露它没拦住 aria-runner-bot (自主运行时) 与 simonfish 交互 session 并发做同一批 secret-guard issue。根因 recon 出 **3 个独立缺陷**:

| 缺陷 | 现象 | recon 定位 | 可行性 |
|------|------|-----------|--------|
| **(a) 认领非强制** | 自主 bot 干活前根本没 claim | `enabled` 默认 false + `mode` advisory + 无 REQUIRE-claim 检查点 (`phase1_gate.py` 只被 AI 编排层 subprocess 可选调用, 无代码强制) | **部分** — config 翻默认 + hook 可做; 但强制自主 bot claim 跨 orchestrator/运行时 |
| **(b) track-id 字符串匹配** | 两个不同名字 (`secret-guard-bash3-multiline-hardening` vs `carry-secretguard-fieldparse-anchor`) 判不出同一件事 | 撞车检测 100% 精确归一 track-id 字符串相等 (`phase1_gate.py:485` + `reconcile.py:350-352`); schema 无 linked_issue/file_globs/branch 语义信号 | **需真设计** — schema 扩展 + 模糊匹配 |
| **(c) claim 从不释放** | ship 完的 claim 永远 active 累积 | `release_claim`/`heartbeat` **零生产调用**; `gc.archive_done_claims` 只处理 `done` 且 git 写入是 no-op stub (`gc.py:259-268`); reconcile 是纯函数不删 | **可实现** — release-on-ship 接线 + 补 GC stub |

实证 (本 session 协调 ref): aria-runner-bot `carry-runtime-probe-phase-b` (7-07 ship, 仍 active) + simonfish `carry-dec002-dedup-phase-b`/`carry-followup-99` (均 ship, 仍 active) —— 缺陷 (c) 的 stale 累积肉眼可见。

## What Changes

### 部件 C — claim 释放生命周期 (defect c, 可直接实现)

**设计决策 (release-by-track, 非 release-by-session)**: 现 `release_claim` 靠 `(container, session)` 定位, 而 `get_identity()` 每次 mint 新 session_id → phase-d-closer 后续调用找不到原 claim。改为**按 track_id + container 释放** (ship 上下文知道 carry-id/track-id, 不知道原 session):
- 新增 `release_claim_by_track(track_id, container, status="done")` (或给 `release_claim` 加 by-track 模式): 定位该 container 下匹配 track_id 的 active claim, 标 done。
- 新增 CLI 入口 (`phase1_gate.py` 或新 `release_gate.py`, 镜像 acquire 的 subprocess 契约)。
- **接线 phase-c-integrator (C.2 merge 后) 或 phase-d-closer (D.x ship 后)**: 传入本 cycle 的 carry-id → 释放 claim。advisory (释放失败不阻断 ship)。
- 补 `gc.archive_done_claims` 的 git 写入 stub (`gc.py:259-268`) + stale-active sweep (heartbeat 超 STALE_TTL 的 active → abandoned, 复用 `_is_stale`)。
- **一次性清理**: 现有 stale active claim (bot runtime-probe / dec002 / followup-99 等) 标 done/abandoned。

### 部件 A — 认领强制 (defect a, 部分可实现, 需 owner 决策边界)

选项 (owner 定):
- **A1 (插件内)**: `enabled` 默认 false→true + phase-b-developer/branch-manager 进 Phase B 前 REQUIRE 一条本 (container,session) 的 active claim, 无则强制先 claim。防交互 session 忘 claim。
- **A2 (跨运行时)**: 自主 bot (aria-runner-bot) 的 orchestrator workflow 在 dispatch 时强制 claim —— 这在 aria-orchestrator (Layer 2), 不在 aria-plugin。**本 spec 范围外, 需单独 orchestrator cycle**。
- **诚实边界**: 插件改不了"绕过 state-scanner 的自主 bot 不 claim"。A1 只能覆盖走 state-scanner/phase-b 的 session。

### 部件 B — 语义重叠检测 (defect b, 需设计, owner 决策是否做)

现无任何语义信号。选项:
- **B1 (轻)**: claim schema 加**可选** `linked_issue` 字段; 撞车检测在 track-id 相等**之外**追加 "同 linked_issue 不同 track-id" 告警 (advisory, 不阻断)。低成本, 覆盖"同 issue 两个名字"的常见撞车。
- **B2 (重)**: 加 `file_globs` + 文件重叠检测。成本高, 覆盖面广。
- **B3**: 接受现状 (纯字符串), 靠 handoff/carry-id 约定 + 部件 A/C 缓解。
- **recon 结论**: B 是三者中唯一"需真设计"的; 建议 B1 (linked_issue advisory) 性价比最高。

## Impact

- **版本**: aria-plugin MINOR (协调机制增强, 新 CLI + schema 可选字段); 具体号待 Phase B。
- **风险**: 改协调机制 = 改多终端撞车防护核心。部件 C 是纯增益 (释放泄漏的 claim); 部件 A1 翻 enabled 默认可能对未配置项目引入 claim 写入 (需 advisory 保证不阻断); 部件 B1 加字段是 additive。
- **Rule #6**: 协调是 deterministic 机制, structural test (release/GC/sweep golden table + CLI I/O 契约 + schema roundtrip)。

## Open Questions (owner 决策后进 Phase B)

1. **(a) 边界**: A1 (插件内 REQUIRE claim + 翻 enabled 默认) 做不做? A2 (orchestrator 强制 bot claim) 是否另开 aria-orchestrator cycle?
2. **(b) 范围**: B1 (linked_issue advisory) / B2 (file 重叠) / B3 (接受现状)?
3. **(c) 接线点**: release-on-ship 挂 phase-c-integrator (merge 后) 还是 phase-d-closer (归档后)? 建议 phase-d-closer D.x (cycle 真正结束点)。
4. 一次性清理现有 stale claim: 本 cycle 顺带做还是独立?

## Verification (Phase B)

- 部件 C: release_claim_by_track golden table + GC 写入 (非 no-op) + stale sweep + CLI I/O + 一次性清理验证 (协调 ref 无 stale active)。
- 部件 A1 (若做): 进 Phase B 无 claim → REQUIRE 拦; enabled 默认翻转 lock-in test。
- 部件 B1 (若做): 同 issue 不同 track-id → advisory 告警; schema roundtrip 向后兼容 (无 linked_issue 的旧 claim 正常)。
