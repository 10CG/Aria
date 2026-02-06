# Tasks: TDD 执行严格度增强 (文档驱动重构)

> **Spec**: changes/2026-02-05-tdd-strictness-enhancement/proposal.md
> **Level**: Full (Level 3)
> **Status**: Draft
> **Created**: 2026-02-05
> **Updated**: 2026-02-06 (设计重构：文档驱动)
> **Estimated**: 8-16h

---

## 设计重构说明 (v2.0)

> **重要变更**: 从代码驱动转向文档驱动设计
>
> **旧设计 (v1.x)**: 17+ Python 模块实现
> - test_runners/, validators/, hooks/, tests/
> - 问题: AI 不会执行这些 Python 代码
>
> **新设计 (v2.0)**: 文档描述，AI 理解执行
> - SKILL.md 描述工作流
> - AI 读取并执行检查规则
> - 参考 Superpowers 的实现方式

---

## 1. Phase 1: 文档重构

- [ ] 1.1 重写 SKILL.md (文档驱动设计)
- [ ] 1.2 更新 EXAMPLES.md (使用示例)
- [ ] 1.3 编写 references/strictness-levels.md (严格度级别详解)
- [ ] 1.4 编写 references/red-state-detection.md (RED 状态检测说明)
- [ ] 1.5 编写 references/green-phase-check.md (GREEN 阶段检查说明)
- [ ] 1.6 编写 references/migration-guide.md (v1.x → v2.0 迁移指南)
- [ ] 1.7 更新 tdd-config-schema.json (配置 JSON Schema)

## 2. Phase 2: 清理旧实现

- [ ] 2.1 删除 cache.py
- [ ] 2.2 删除 config.py
- [ ] 2.3 删除 diff_analyzer.py
- [ ] 2.4 删除 state_persistence.py
- [ ] 2.5 删除 state_tracker.py
- [ ] 2.6 删除 test_runners/ 目录
- [ ] 2.7 删除 validators/ 目录
- [ ] 2.8 删除 hooks/pre_tool_use_hook.py
- [ ] 2.9 删除 tests/ 目录 (Python 单元测试)

## 3. Phase 3: 示例更新

- [ ] 3.1 更新 Python 示例 (配置 + README)
- [ ] 3.2 更新 JavaScript 示例 (配置 + README)
- [ ] 3.3 更新 Dart 示例 (配置 + README)
- [ ] 3.4 添加配置文件示例 (.claude/tdd-config.json)

## 4. Phase 4: 验证和发布

- [ ] 4.1 文档格式验证 (SKILL.md 符合规范)
- [ ] 4.2 示例项目可运行性测试
- [ ] 4.3 v2.0.0 发布准备

---

## Summary

| Phase | Tasks | Estimated Hours |
|-------|-------|-----------------|
| 1. Phase 1: 文档重构 | 7 | 4-6h |
| 2. Phase 2: 清理旧实现 | 9 | 1-2h |
| 3. Phase 3: 示例更新 | 4 | 2-4h |
| 4. Phase 4: 验证和发布 | 3 | 1-2h |
| **Total** | **23** | **8-16h** |

---

## Dependencies

```
Phase 1 ──────────────────────────────────────────────────────────────┐
      │                                                              │
      ├──▶ 1.1 SKILL.md 重写                                         │
      │     │                                                        │
      │     ├──▶ 1.2 EXAMPLES.md                                     │
      │     ├──▶ 1.3 strictness-levels.md ──────────────────────┐    │
      │     ├──▶ 1.4 red-state-detection.md ────────────────────┤    │
      │     ├──▶ 1.5 green-phase-check.md ──────────────────────┤    │
      │     ├──▶ 1.6 migration-guide.md ────────────────────────┤    │
      │     └──▶ 1.7 tdd-config-schema.json ─────────────────────┤    │
      │                                                        │    │
Phase 2 ──────────────────────────────────────────────────────│────│
      │ (可并行)                                              │    │
      ├──▶ 2.1-2.5 删除 Python 模块                           │    │
      ├──▶ 2.6 删除 test_runners/                             │    │
      ├──▶ 2.7 删除 validators/                               │    │
      ├──▶ 2.8 删除 hooks/                                    │    │
      └──▶ 2.9 删除 tests/                                    │    │
                                                            │    │
Phase 3 ─────────────────────────────────────────────────────┘    │
      │ (依赖 Phase 1 完成)                                       │
      ├──▶ 3.1 Python 示例 ─────────────────────────────────────┐  │
      ├──▶ 3.2 JavaScript 示例 ─────────────────────────────────┤  │
      ├──▶ 3.3 Dart 示例 ────────────────────────────────────────┤  │
      └──▶ 3.4 配置文件示例 ─────────────────────────────────────┤  │
                                                                 │  │
Phase 4 ─────────────────────────────────────────────────────────┘  │
      │ (依赖 Phase 1-3 完成)                                      │
      ├──▶ 4.1 文档格式验证                                         │
      ├──▶ 4.2 示例可运行性测试                                      │
      └──▶ 4.3 v2.0.0 发布                                          │
                                                                    │
Phase 1 完成 ───────────────────────────────────────────────────────┘
     │
     ├──▶ Phase 2 (可并行)
     └──▶ Phase 3 (依赖 Phase 1)
            │
            └──▶ Phase 4
```

---

## Notes

### Numbering Immutability

Once numbering (1.1, 1.2, etc.) is established, it MUST NOT be changed:
- Adding new tasks: Use new numbers (1.8, 2.10, etc.)
- Removing tasks: Mark as ~~cancelled~~ instead of deleting
- Renumbering: Forbidden - breaks parent references in detailed-tasks.yaml

### Task Granularity

Each item represents a coarse-grained functional deliverable:
- Focus on "what" not "how"
- Keep descriptions brief and clear
- One deliverable per checkbox preferred

### Phase Organization

- **Phase 1**: 核心文档重写 (SKILL.md + references/)
- **Phase 2**: 删除不再需要的 Python 代码
- **Phase 3**: 更新示例项目
- **Phase 4**: 验证和发布

---

## Dual-Layer Architecture

This tasks.md file serves as Layer 1 (coarse-grained) in the dual-layer architecture:

- **Layer 1** (this file): Human-readable progress tracking, OpenSpec CLI compatible
- **Layer 2** (detailed-tasks.yaml): AI-executable task specifications with TASK-{NNN} IDs

The `task-planner` skill will:
1. Parse this tasks.md file
2. Generate detailed-tasks.yaml with parent field linking (e.g., parent: "1.1")
3. Create atomic TASK-{NNN} items for each checkbox
4. Maintain bidirectional synchronization

---

## Agent Assignments (预分配)

| Phase | 推荐 Agent | 理由 |
|-------|-----------|------|
| 1.1-1.7 | knowledge-manager | 文档编写，设计描述 |
| 2.1-2.9 | knowledge-manager | 清理工作，文档整理 |
| 3.1-3.4 | backend-architect | 示例项目配置 |
| 4.1-4.3 | qa-engineer | 验证和测试 |

---

## Milestones

| 里程碑 | 标准 | 预计日期 |
|--------|------|---------|
| **M1: 文档重构完成** | Phase 1 所有文档编写完成 | Day 1 |
| **M2: 清理完成** | 旧代码全部删除 | Day 1 |
| **M3: 示例更新完成** | 所有示例可运行 | Day 2 |
| **M4: v2.0.0 发布** | 验证通过，准备发布 | Day 2 |

---

## 与 v1.x 的差异

| 项目 | v1.x (旧设计) | v2.0 (新设计) |
|------|-------------|--------------|
| 实现方式 | Python 代码 | 文档描述 |
| 文件数量 | 17+ Python 模块 | 1 SKILL.md + 5 references/ |
| 测试 | Python 单元测试 | 示例项目验证 |
| 工作量 | 80-120h | 8-16h |
| AI 执行方式 | Hook 调用 Python | AI 读取文档理解 |

---

**Version**: 2.0 (设计重构)
**Last Updated**: 2026-02-06
