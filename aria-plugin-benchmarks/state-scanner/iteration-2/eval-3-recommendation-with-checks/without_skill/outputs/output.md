# Aria 项目状态检查报告

> 扫描时间: 2026-04-03
> 当前分支: feature/us-006-custom-health-checks (2 commits ahead of master)
> 主项目版本: v1.3.0 | 插件版本: v1.10.0

---

## 1. 总体状态概览

| 维度 | 状态 | 说明 |
|------|------|------|
| Git 工作区 | 干净 | 无未提交变更（仅有 untracked eval 目录） |
| 当前分支 | 功能分支 | feature/us-006-custom-health-checks，US-006 开发进行中 |
| 子模块同步 | OK | aria 和 standards 子模块与当前指针一致 |
| 版本一致性 | OK | plugin.json (1.10.0) 与 CHANGELOG (1.10.0) 匹配 |

---

## 2. 发现的问题

### 问题 1: PRD User Story 表严重过时 [严重]

**位置**: `docs/requirements/prd-aria-v1.md` 第 140-144 行

PRD 中的 User Story 表仅列出 3 个 Story（US-001 到 US-003），且状态全部标记为 `pending`，但实际情况：

| Story | PRD 中状态 | 实际状态 | 偏差 |
|-------|-----------|---------|------|
| US-001 | pending | done | 过时 |
| US-002 | pending | done | 过时 |
| US-003 | pending | pending | 一致 |
| US-004 | 未记录 | done | 缺失 |
| US-005 | 未记录 | in_progress | 缺失 |
| US-006 | 未记录 | in_progress | 缺失 |

PRD 的成功标准中也有条目仍标记为未完成，但对应 Story 已经完成（如"跨项目验证"标记为 v1.1.0 目标，但 US-002 已 done）。

**影响**: 违反 Aria 认知框架第 3 条"文档同步"原则。AI 和人类通过 PRD 了解全局状态时会获得错误信息。

---

### 问题 2: US-005 aria-dashboard 未完成但主项目已发版 v1.3.0 [中等]

US-005 的 Target Version 是 v1.3.0，目前状态为 `in_progress`。git 历史显示：
- Phase 1（看板生成）已完成并合并
- Phase 2（Issue 提交 + 存储）已完成并合并
- Phase 3（心跳 Agent 自动开发）尚未开始

主项目已发布 v1.3.0 (`release: v1.3.0 — aria-dashboard Phase 1 + version sync`)，但 US-005 仍有未完成的验收标准（Phase 3）。这意味着要么 Phase 3 需要推迟到 v1.4.0，要么 US-005 的 Target Version 需要更新。

---

### 问题 3: OpenSpec aria-dashboard 未归档 [轻微]

`openspec/changes/aria-dashboard/` 仍在 changes 目录中，但 Phase 1 和 Phase 2 已完成并合并到 master。如果 Phase 3 推迟到未来版本，已完成部分的 OpenSpec 状态应该更新反映进展。

---

### 问题 4: v1.3.0 未打 Git Tag [轻微]

VERSION 文件记录当前版本为 v1.3.0，git log 中有 release commit，但 `git tag -l 'v1.3*'` 返回空。前序版本的 tag 可能存在，但 v1.3.0 的 tag 缺失。

---

## 3. 自定义健康检查结果

基于 `.aria/state-checks.yaml` 中定义的 2 项检查：

| 检查项 | 结果 | 严重度 |
|--------|------|--------|
| submodule-freshness | OK - 子模块同步 | warning |
| changelog-version-match | OK - plugin.json 与 CHANGELOG 版本一致 | error |

两项自定义检查均通过。

---

## 4. User Story 总览

| Story | 标题 | 状态 | 说明 |
|-------|------|------|------|
| US-001 | 增强工作流自动化 | done | v1.1.0 已交付 |
| US-002 | 跨项目方法论验证 | done | Kairos 试点完成 |
| US-003 | 多 AI 平台兼容性 | pending | 无 OpenSpec，优先级 LOW |
| US-004 | 十步循环自动审计系统 | done | v1.2.0 已交付 |
| US-005 | 项目进度看板 | in_progress | Phase 1-2 完成，Phase 3 待做 |
| US-006 | 自定义健康检查 | in_progress | OpenSpec 已批准，功能分支开发中 |

---

## 5. AB Benchmark 摘要

- 28 个 Skills 已测试
- 24 个 WITH_BETTER（Skill 确实提升了质量）
- 3 个 EQUAL（api-doc-generator, phase-a-planner, spec-drafter）
- 1 个 MIXED（forgejo-sync）
- 平均 delta: +0.56
- 100% with_skill 通过率

近期新增的 Skills（aria-dashboard 等）可能尚未纳入 AB baseline。

---

## 6. 推荐下一步

### 推荐 A: 完成 US-006 当前开发（最高优先级）

**理由**: 你当前在 `feature/us-006-custom-health-checks` 分支上，已有 2 个 commit。US-006 是一个 Level 2 Spec（4-6 小时工作量），继续完成它是最自然的下一步。

**具体行动**:
1. 验证 state-scanner SKILL.md 中已添加阶段 1.11 定义
2. 确认 RECOMMENDATION_RULES.md 中已新增 `custom_check_failed` 规则
3. 运行 AB benchmark 验证 delta 为正值（Rule #6 要求）
4. 创建 PR 合并到 master

---

### 推荐 B: 修复 PRD 文档同步问题（高优先级）

**理由**: PRD 是项目的顶层需求文档，当前严重过时。这违反了 Aria 的"文档同步"核心原则。修复工作量小（约 30 分钟），属于 PATCH 级别变更。

**具体行动**:
1. 更新 PRD User Story 表，添加 US-004、US-005、US-006
2. 更新各 Story 的状态（done/in_progress/pending）
3. 更新成功标准的勾选状态
4. 更新 Skills/Agents 计数（当前 33 Skills + 11 Agents）

---

### 推荐 C: 决定 US-005 Phase 3 的排期

**理由**: US-005 Phase 3（心跳 Agent 自动开发）是一个复杂功能，依赖 Claude Code `/schedule` 能力。需要明确决定：是继续在 v1.3.x 中完成，还是推迟到 v1.4.0 或更晚。

**具体行动**:
1. 评估 Phase 3 是否技术可行（`/schedule` 能力是否就绪）
2. 如果推迟：更新 US-005 Target Version，将 Phase 3 拆分为独立 Story
3. 如果继续：在 US-006 完成后排入开发计划

---

### 推荐 D: 补打 v1.3.0 Git Tag

**理由**: 版本发布应有对应的 Git Tag，方便回溯和引用。

**具体行动**:
```
git tag v1.3.0 b12aa2b   # 在 release commit 上打 tag
git push origin v1.3.0
```

---

## 7. 建议的行动优先级

| 优先级 | 行动 | 预计工作量 | 类型 |
|--------|------|-----------|------|
| 1 | 完成 US-006 开发 + AB benchmark + 合并 | 2-4 小时 | 功能开发 |
| 2 | 修复 PRD 文档同步 | 30 分钟 | 文档维护 |
| 3 | 补打 v1.3.0 Tag | 5 分钟 | 版本管理 |
| 4 | 决定 US-005 Phase 3 排期 | 决策讨论 | 规划 |
