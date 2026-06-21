## Triage 复核更新 (re-triage @ v1.47.0)

承接上方 2026-06-13 triage (verdict `partial-repro` / `major` / `next-cycle`)。本次在当前 **aria v1.47.0** (`281388d`) 复核,结论不变,补两点新信息:

### 1. 断裂在 v1.47.0 仍持续 (8 天无修复)
- v1.47.0 的 issue-sweep **改动了** `agent-team-audit` (cycle B `#54/#95` 加 data-availability + framework-convention 检查;cycle C `#79` 加 mid_post_spec 检查点),但 **selection-matrix 对 `.aria/agents/` / capabilities 路由仍零支持** (`grep -rn '.aria/agents|capabilities|项目级' skills/agent-team-audit/` 零命中)。
- 无 in-flight 分支 / 无修复 commit。核心断裂 (agent-team-audit 永不发现/唤醒项目专属 audit agent) **CONFIRMED 持续**。

### 2. ⚠️ 本 issue 核心诉求 **不** 被 M7 agent-lifecycle 覆盖
M7 agent-lifecycle Spec (已 Approved 2026-06-18) 引用了 `#145`,但**仅用于 "重启生效" caveat (CAVEAT #3)** 与 "git 集合库 vs marketplace" 决策依据。

M7 解决的是 **"项目 agent 如何物化进 `.claude/agents/` 原生加载"**;本 issue 要的是 **"agent-team-audit selection-matrix 按 capabilities 动态选项目 audit agent"** —— **两者正交**。即使 M7 ship 后项目 agent 被物化进原生目录,`agent-team-audit` 写死的 selection-matrix 仍不会按能力把它们选进审计检查点。

**结论**: `#145` 核心诉求需**独立 cycle** (brainstorm 收敛 selection-matrix capabilities 路由设计,可复用 agent-router 的 `.aria/agents/` 发现范式),不能寄望 M7 自动解决。优先级受 `agent-team-audit` = experimental (默认关闭) 影响,适合等待期/M7 立项时一并排期。

---
*Re-triaged by `/issue-triage` v1.47.0 — Ref: 10CG/Aria#145 · 复核 @ aria `281388d`*
