# Tasks: Enforcement Mechanism Redesign

> **Spec**: changes/enforcement-mechanism-redesign/proposal.md
> **Level**: Full (Level 3)
> **Status**: Draft
> **Created**: 2026-01-20
> **Updated**: 2026-01-20
> **Estimated**: 16-24h
> **Version**: 2.0 (单一入口架构)

---

## 1. branch-manager 技能增强

- [x] 1.1 设计并实现模式决策逻辑 (评分系统)
- [x] 1.2 实现模式 A: 常规分支创建流程
- [x] 1.3 实现模式 B: Worktree 创建流程
- [x] 1.4 实现目录优先级选择逻辑
- [x] 1.5 实现 .gitignore 强制验证和自动修复
- [x] 1.6 实现环境验证 (npm/cargo/pnpm + 测试基线)
- [x] 1.7 更新 SKILL.md 文档 (包含两种模式说明)
- [x] 1.8 添加 Red Flags 和职责边界章节
- [x] 1.9 更新 hooks.json 配置

## 2. subagent-driver 技能实现

- [x] 2.1 创建 subagent-driver/SKILL.md 主文档
- [x] 2.2 实现计划加载功能 (tasks.md/detailed-tasks.yaml)
- [x] 2.3 实现 TodoWrite 创建和维护逻辑
- [x] 2.4 实现 fresh subagent 调用机制
- [x] 2.5 实现逐任务执行流程
- [x] 2.6 实现任务间代码审查机制
- [x] 2.7 实现问题优先级分类 (Critical/Major/Minor)
- [x] 2.8 实现 Critical 问题阻塞逻辑
- [x] 2.9 实现最终审查流程
- [x] 2.10 配置 REQUIRED branch-finisher 调用
- [x] 2.11 实现与 branch-manager 的输入输出集成
- [x] 2.12 添加公告模式文档

## 3. branch-finisher 技能实现

- [x] 3.1 创建 branch-finisher/SKILL.md 主文档
- [x] 3.2 实现测试前置验证逻辑
- [x] 3.3 实现 4 选项完成流程 UI
- [x] 3.4 实现 worktree 清理决策逻辑
- [x] 3.5 实现与 subagent-driver 的输入集成
- [x] 3.6 添加 Red Flags 和职责边界章节

## 4. 现有技能集成更新

- [x] 4.1 更新 phase-b-developer 与新技能集成
- [x] 4.2 更新 phase-c-integrator 与 branch-finisher 集成
- [x] 4.3 更新 strategic-commit-orchestrator 协作逻辑
- [x] 4.4 验证与 tdd-enforcer 无冲突

## 5. 文档和对比分析

- [x] 5.1 创建 superpowers-vs-aria.md 对比文档
- [x] 5.2 创建 dual-isolation-strategy.md 策略文档
- [x] 5.3 更新 AGENTS_ARCHITECTURE.md 添加 SDD 模式
- [x] 5.4 更新 system-architecture.md 添加强制执行章节
- [x] 5.5 创建渐进式隔离策略图示

## 6. 验证和测试

- [x] 6.1 验证 branch-manager 模式决策正确性
- [x] 6.2 验证 worktree 创建和清理流程
- [x] 6.3 验证 subagent-driver 任务执行链
- [x] 6.4 验证技能间数据传递
- [x] 6.5 端到端测试 Level 2-4 工作流
- [x] 6.6 验证与现有 tdd-enforcer 兼容性

---

## Summary

| Phase | Tasks | Estimated Hours |
|-------|-------|-----------------|
| 1. branch-manager 增强 | 9 | 4-6h |
| 2. subagent-driver | 12 | 6-8h |
| 3. branch-finisher | 6 | 2-3h |
| 4. 现有技能集成 | 4 | 2-3h |
| 5. 文档和对比 | 5 | 2-3h |
| 6. 验证和测试 | 6 | 3-4h |
| **Total** | **42** | **19-27h** |

---

## Dependencies

```
Phase 1 (branch-manager) ──┬──> Phase 2 (subagent-driver)
                          │        │
                          │        └──> Phase 3 (branch-finisher)
                          │              │
                          └──> Phase 4 (集成更新)
                                 │
                                 ▼
                          Phase 5 (文档)
                                 │
                                 ▼
                          Phase 6 (验证)
```

**关键依赖**:
- Phase 2 依赖 Phase 1 完成 (subagent-driver 需要 branch-manager 的输出)
- Phase 3 依赖 Phase 2 完成 (branch-finisher 需要 subagent-driver 的输出)
- Phase 4 依赖 Phase 1,2,3 完成 (集成需要所有新技能就绪)

---

## Notes

1. **编号不可变性**: 一旦建立编号 (1.1, 1.2 等)，必须不得更改
   - 添加新任务: 使用新编号 (如 1.10, 1.11)
   - 删除任务: 标记为 ~~cancelled~~ 而非删除
   - 重新编号: 禁止 - 破坏 detailed-tasks.yaml 中的 parent 引用

2. **任务粒度**: 每项代表粗粒度的功能交付物
   - 聚焦"做什么"而非"怎么做"
   - 保持描述简明扼要
   - 每个复选框首选单一交付物

3. **阶段组织**:
   - 在逻辑阶段下对相关任务进行分组
   - 保持每个阶段内的顺序编号
   - 阶段名称应反映主要工作领域

4. **架构变更 (v2.0)**:
   - 取消独立的 worktree-manager 技能
   - 功能合并到 branch-manager 增强版
   - 采用单一入口原则
   - 内部自动模式决策

---

## Dual-Layer Architecture

此 tasks.md 文件作为双层架构中的第 1 层（粗粒度）:

- **第 1 层** (本文件): 人类可读的进度跟踪，OpenSpec CLI 兼容
- **第 2 层** (detailed-tasks.yaml): AI 可执行的任务规范，含 TASK-{NNN} ID

`task-planner` 技能将:
1. 解析此 tasks.md 文件
2. 生成 detailed-tasks.yaml，含 parent 字段链接 (如 parent: "1.1")
3. 为每个复选框创建原子化 TASK-{NNN} 项
4. 维护双向同步

---

## Version History

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.0 | 2026-01-20 | 重构为单一入口架构，取消 worktree-manager |
| 1.0 | 2026-01-20 | 初始版本 (两个独立技能) |

---

**Created**: 2026-01-20
**Maintained By**: 10CG Lab
