# Tasks: 两阶段代码审查实现 (Superpowers Two-Phase Review)

> **Spec**: changes/superpowers-two-phase-review/proposal.md
> **Level**: Full (Level 3)
> **Status**: Approved
> **Created**: 2026-02-06
> **Approved**: 2026-02-06
> **Estimated**: 32-40h

---

## 1. Phase 1: 核心 Agent 和 Skill 创建

- [ ] 1.1 创建 `aria:code-reviewer` Agent
  - 定义两阶段审查流程
  - 实现 Phase 1 规范合规性检查逻辑
  - 实现 Phase 2 代码质量检查逻辑
  - 定义 Critical/Important/Minor 输出格式

- [ ] 1.2 创建 `requesting-code-review` Skill
  - 编写 SKILL.md 规格说明
  - 定义使用场景和触发条件
  - 编写调用 aria:code-reviewer 的示例
  - 中英双语支持

- [ ] 1.3 创建 Agent 模板文件
  - 编写 code-reviewer.md 模板
  - 定义占位符变量 (WHAT_WAS_IMPLEMENTED, PLAN_OR_REQUIREMENTS, BASE_SHA, HEAD_SHA)
  - 编写输出格式示例

---

## 2. Phase 2: 集成与文档

- [ ] 2.1 更新 `subagent-driver` Skill 集成
  - 添加两阶段审查调用选项
  - 更新工作流文档
  - 保持向后兼容 (现有审查机制保留)

- [ ] 2.2 编写使用文档和示例
  - 创建 examples/ 目录结构
  - 编写 Phase 1 PASS 场景示例
  - 编写 Phase 1 FAIL 场景示例
  - 编写 Phase 2 FAIL 场景示例
  - 编写最佳实践指南

- [ ] 2.3 手动集成测试
  - 编写测试场景清单 (7 个场景)
  - 执行场景 1: Phase 1 PASS + Phase 2 PASS
  - 执行场景 2: Phase 1 FAIL (阻塞)
  - 执行场景 3: Phase 1 PASS + Phase 2 FAIL
  - 执行场景 4: 无计划文件时的降级处理
  - 执行场景 5: 大变更集的分批检查
  - 执行场景 6: Skill 调用流程
  - 执行场景 7: 直接 Agent 调用流程
  - 生成测试执行报告

---

## 3. Phase 3: 验证与发布

- [ ] 3.1 文档完善
  - 更新 aria/CHANGELOG.md
  - 更新 aria/README.md (Skills 数量 +1)
  - 更新系统架构文档 (docs/architecture/system-architecture.md)
  - 更新插件清单 (aria/.claude-plugin/plugin.json)

- [ ] 3.2 版本发布准备
  - 更新版本号至 v1.4.0
  - 更新 aria/VERSION 文件
  - 编写 Release Notes
  - 验证所有文件版本号一致性

---

## Summary

| Phase | Tasks | Estimated Hours |
|-------|-------|-----------------|
| 1. Phase 1: 核心 Agent 和 Skill 创建 | 3 | 12-16h |
| 2. Phase 2: 集成与文档 | 3 | 12-16h |
| 3. Phase 3: 验证与发布 | 2 | 8h |
| **Total** | **8** | **32-40h** |

---

## Dependencies

```
Phase 1 ──┬──> Phase 2 ──┬──> Phase 3
          │              │
          └──> [依赖: proposal.md 评审通过]
```

**关键依赖**:
- 1.1 (Agent) 和 1.2 (Skill) 可以并行开发
- 1.3 (模板) 依赖 1.1 完成
- 2.1 (集成) 依赖 1.1 和 1.2 完成
- 2.3 (测试) 依赖 2.1 和 2.2 完成

---

## Notes

1. **Numbering Immutability**: 任务编号 (1.1, 1.2, etc.) 确立后不得变更
   - 新增任务: 使用新编号 (如 1.4, 2.4)
   - 删除任务: 标记为 ~~cancelled~~ 而非删除
   - 重新编号: 禁止 - 会破坏 detailed-tasks.yaml 中的 parent 引用

2. **Task Granularity**: 每个任务代表一个粗粒度的功能交付物
   - 聚焦 "what" 而非 "how"
   - 每个复选框对应一个交付物
   - 保持描述简洁清晰

3. **手动测试说明**: 任务 2.3 采用手动测试方案
   - 真实环境中执行测试场景
   - 记录测试结果和问题
   - 作为文档示例的一部分

4. **向后兼容**: 任务 2.1 需确保现有功能不受影响
   - subagent-driver 现有审查机制保留
   - 新功能为可选启用
   - 不破坏现有用户工作流

5. **中英双语**: 所有新文件需支持中英双语
   - Agent 提示词双语
   - Skill 描述双语
   - 示例代码双语

---

## Dual-Layer Architecture

本 tasks.md 文件是双层架构中的 Layer 1 (粗粒度):

- **Layer 1** (本文件): 人类可读的进度跟踪, OpenSpec CLI 兼容
- **Layer 2** (detailed-tasks.yaml): AI 可执行的任务规格, 带 TASK-{NNN} ID

`task-planner` skill 将:
1. 解析本 tasks.md 文件
2. 生成带 parent 字段链接的 detailed-tasks.yaml
3. 为每个复选框创建原子化 TASK-{NNN} 项
4. 维护双向同步

---

## 详细交付物清单

### 1.1 aria:code-reviewer Agent 交付物
- [ ] `aria/agents/code-reviewer.md`
  - Agent 前置元数据 (name, description, model, tools)
  - Phase 1 审查逻辑
  - Phase 2 审查逻辑
  - 输出格式定义
  - 中英双语支持

### 1.2 requesting-code-review Skill 交付物
- [ ] `aria/skills/requesting-code-review/SKILL.md`
  - Skill 前置元数据
  - 使用场景定义
  - 触发条件
  - 调用示例
  - 中英双语

### 1.3 Agent 模板交付物
- [ ] `aria/skills/requesting-code-review/code-reviewer.md`
  - 占位符变量定义
  - Phase 1 检查清单
  - Phase 2 检查清单
  - 输出格式模板

### 2.1 subagent-driver 集成交付物
- [ ] `aria/skills/subagent-driver/SKILL.md` 更新
  - 新增两阶段审查选项
  - 更新工作流图
  - 向后兼容说明

### 2.2 文档和示例交付物
- [ ] `aria/skills/requesting-code-review/examples/` 目录
  - `phase1-pass-phase2-pass.md`
  - `phase1-fail-blocking.md`
  - `phase2-fail-with-warnings.md`
  - `no-plan-fallback.md`
  - `large-changeset-batching.md`
  - `skill-invocation.md`
  - `direct-agent-call.md`
  - `best-practices.md`

### 2.3 测试交付物
- [ ] `aria/skills/requesting-code-review/testing/test-scenarios.md`
  - 7 个测试场景定义
  - 预期结果
  - 执行步骤
- [ ] 测试执行报告 (markdown)
  - 实际执行结果
  - 发现的问题
  - 修复记录

### 3.1 文档更新交付物
- [ ] `aria/CHANGELOG.md` 更新
- [ ] `aria/README.md` 更新
- [ ] `docs/architecture/system-architecture.md` 更新
- [ ] `aria/.claude-plugin/plugin.json` 更新

### 3.2 发布交付物
- [ ] `aria/VERSION` 更新 (v1.4.0)
- [ ] Release Notes 编写
- [ ] 版本号一致性验证

---

**模板版本**: OpenSpec v2.1.0
**文档维护**: Aria 项目组
**更新日期**: 2026-02-06
