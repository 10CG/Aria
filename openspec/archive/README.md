# OpenSpec Archive

> Aria 方法论已归档的变更规范

## 说明

此目录包含 Aria 方法论框架演进过程中已完成并归档的变更规范。

## 目录结构

```
openspec/
├── changes/          # 活跃的变更
│   └── aria-workflow-enhancement/
├── archive/          # 已归档的变更 ← 当前目录
│   └── {date}-{feature}/
└── specs/            (未来创建 - 当前真理)
```

## 归档内容

### Aria 框架演进 (21 个)

| 日期 | 变更 | 类型 |
|------|------|------|
| 2025-12-16 | spec-drafter | Skill |
| 2025-12-16 | task-planner | Skill |
| 2025-12-17 | branch-manager | Skill |
| 2025-12-17 | progress-query-assistant | Skill |
| 2025-12-17 | progress-updater | Skill |
| 2025-12-19 | clarify-phase-a-task-pipeline | 工作流 |
| 2025-12-19 | phase-a-integration | 工作流 |
| 2025-12-22 | optimize-phase-a-with-dual-layer-architecture | 核心 |
| 2025-12-23 | git-commit-convention | 约定 |
| 2025-12-23 | reduce-context-token-overhead | 优化 |
| 2025-12-23 | refactor-skill-structure | 架构 |
| 2025-12-23 | ten-step-restructure | 核心 |
| 2025-12-24 | add-composite-skills | 架构 |
| 2025-12-24 | add-test-verification-skill | Skill |
| 2025-12-24 | refactor-workflow-architecture | 架构 |
| 2025-12-25 | update-composite-workflow-v2 | 工作流 |
| 2025-12-27 | validate-documentation-integrity | 工具 |
| 2025-12-28 | architecture-docs-separation | 文档 |
| 2026-01-01 | enhance-submodule-commit-orchestration | 工具 |
| 2026-01-01 | evolve-ai-ddd-system | 核心 |
| 2026-01-03 | fix-aria-requirements-model | 核心 |

## 命名规范

**格式**: `YYYY-MM-DD-{feature-name}/`

## 归档流程

变更满足以下条件时应归档：

| 条件 | 说明 |
|------|------|
| **Status = Implemented** | 核心功能已实施 |
| **Success Criteria 达成** | 验收标准通过 |
| **无活跃任务** | tasks.md 无进行中任务 |

---

**维护**: 10CG Lab
**迁移**: 2026-01-18 (从 aria-standards/openspec/archive)
