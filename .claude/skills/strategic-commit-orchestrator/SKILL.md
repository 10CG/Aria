---
name: strategic-commit-orchestrator
description: |
  基于AI-DDD v3.0.0的战略提交编排器，智能分析项目变更设计分组提交计划，
  支持多模块(mobile/backend/frontend/shared)协同提交和阶段性成果提交。

  使用场景：需要分组提交多个变更、跨模块协同开发、阶段性成果提交、大规模重构。

  依赖: commit-msg-generator
  推荐Agent: tech-lead
---

# Strategic Commit Orchestrator

## 🚀 快速开始

### 我应该使用这个 Skill 吗？

**决策树**:
```
有多个提交需要分组？
  ├─ 是 → 使用本 skill
  │   └─ 主项目 + 子模块都有变更？
  │       ├─ 是 → 类型E 全项目流程
  │       └─ 否 → 跨多个模块？
  │           ├─ 是 → 跨模块流程
  │           └─ 否 → 单模块分组流程
  └─ 否 → 使用 commit-msg-generator
```

**快速场景匹配**:

| 场景 | 使用? | 类型 | 说明 |
|------|------|------|------|
| 📁 创建多个架构文档 | ✅ | B | 文档批量提交 |
| 🔄 Backend + Mobile 协同开发 | ✅ | D | 跨模块提交 |
| 🎯 Phase/Cycle 结束里程碑 | ✅ | B/D | 阶段成果提交 |
| 🔧 大规模重构 | ✅ | A/B | 多文件分组 |
| 🌐 OpenSpec + Skills + Standards | ✅ | **E** | 全项目变更 |
| 📦 主项目 + 子模块同时变更 | ✅ | **E** | 全项目变更 |
| 📝 单文件修改 | ❌ | - | 直接用 commit-msg-generator |
| 🐛 单个 Bug 修复 | ❌ | - | 直接用 commit-msg-generator |

### 快速示例

```yaml
场景: Backend架构文档批量提交

步骤:
1. 分析变更 → 3个架构文档 (L0 + 2个L1)
2. 分组策略 → Group 1: L0, Group 2: L1文档
3. Subagent分配 → knowledge-manager
4. 执行策略 → 串行 (L0 → L1)
5. 并行执行提交
```

完整示例: [EXAMPLES.md](./EXAMPLES.md)

---

## 🎯 核心价值

作为 **Tech-Lead 级别** 的战略提交编排工具，在复杂多模块变更场景下，提供智能的提交分组规划、Subagent 并行编排和项目进度感知能力。

**核心能力**:
- ✅ 支持 mobile/backend/frontend/shared 所有模块
- ✅ 基于AI-DDD v3.0.0核心标准
- ✅ 自动识别变更文件所属模块
- ✅ 智能分配专业 Subagent
- ✅ 并行执行提交，提升效率

---

## 📋 五种变更类型（核心）

**✅ 使用前必读**: 根据变更类型选择正确的处理方式

| 类型 | 特征 | UPM处理 | Phase/Cycle | 示例 |
|------|------|---------|-------------|------|
| **类型A** | 业务功能子模块变更 | 读取子模块UPM | 使用实际进度 | `mobile/**`, `backend/**` |
| **类型B** | 主项目变更 | 读取主模块UPM | 使用主模块进度 | `docs/**`, `.claude/skills/**`, `scripts/**` |
| **类型C** | 跨项目共享基础设施 | 无UPM | 使用逻辑阶段 | `standards/**`, `.claude/agents/**` |
| **类型D** | 跨模块协同变更 | 读取主模块UPM | 使用主模块进度 | Backend + Mobile + API契约 |
| **类型E** | 全项目变更 | 混合策略 | 各自处理 | 主项目 + 子模块同时变更 |

**详细识别规则**: [CHANGE_TYPES.md](./CHANGE_TYPES.md)

---

## 🔄 基本使用流程

```yaml
1. 识别变更类型 → A / B / C / D / E

2. 读取项目状态
   → 类型A: 读取子模块UPM
   → 类型B/D: 读取主模块UPM
   → 类型C: 跳过UPM，使用逻辑阶段
   → 类型E: 混合策略 (见下方说明)

3. 分析变更并分组
   → 按职责、依赖关系分组文件
   → 类型E: 先扫描所有子模块变更

4. 分配 Subagent
   → knowledge-manager / backend-architect / mobile-developer 等

5. 执行提交
   → 使用 Task 工具并行/串行执行

6. 验证结果
   → 检查 git log，确认提交成功
```

**详细流程**: [ADVANCED_GUIDE.md - 标准工作流程](./ADVANCED_GUIDE.md#标准工作流程详解)

---

## 🤖 可用 Subagent

| Subagent | 专长领域 | 适用场景 |
|----------|---------|----------|
| **knowledge-manager** | 架构文档、知识库 | *_ARCHITECTURE.md, docs/* |
| **backend-architect** | 后端系统、API | backend/**/*.py, API实现 |
| **mobile-developer** | Flutter/Dart、UI | mobile/lib/**/*.dart |
| **api-documenter** | API文档、OpenAPI | shared/contracts/*.yaml |
| **qa-engineer** | 测试、质量保证 | test/**/*_test.* |
| **tech-lead** | 技术决策、重构 | Skill开发, 重大重构 |
| **general-purpose** | 通用任务 | 配置修改, 简单更新 |

**详细能力映射**: [ADVANCED_GUIDE.md - Subagent分配](./ADVANCED_GUIDE.md#phase-4-subagent-智能分配)

---

## ⚙️ 执行策略

### 全并行 (Fast Track)
- **条件**: 所有分组完全独立，无依赖
- **示例**: 3个不同 Skill 的独立更新

### 阶段并行 (Phased)
- **条件**: 存在阶段性依赖
- **示例**: Phase 1: [A || B], Phase 2: [C]

### 串行 (Sequential)
- **条件**: 强依赖关系，必须顺序执行
- **示例**: API定义 → 实现 → 测试

### 混合 (Hybrid) ⭐ 最常用
- **条件**: 部分并行 + 部分串行
- **执行**: 灵活组合

**详细策略**: [ADVANCED_GUIDE.md - 并行执行编排](./ADVANCED_GUIDE.md#phase-5-并行执行编排)

---

## 📝 提交消息增强

### 基础格式

```
<type>(<scope>): <中文描述> / <English description>

<Body>

🤖 Executed-By: {subagent_type} subagent
📋 Context: {Phase}-{Cycle} {context}
🔗 Module: {module_name}

<Footer>
```

### Phase/Cycle来源

```yaml
类型A (业务功能子模块):
  → 从子模块 UPM 读取实际进度
  → 示例: Phase4-Cycle9

类型B (主项目变更):
  → 从主模块 UPM 读取实际进度
  → 示例: Phase2-Cycle3

类型C (跨项目共享基础设施):
  → 使用逻辑阶段描述（无UPM）
  → 示例: Phase1-Cycle1 standards-unification

类型D (跨模块协同变更):
  → 从主模块 UPM 读取
  → 示例: Phase3-Cycle7

类型E (全项目变更):
  → 子模块: 各自策略 (A/C)
  → 主项目: 读取主模块UPM
  → 示例: 主项目 Phase2-Cycle3 + standards Phase1-Cycle1
```

**增强标记格式**: [commit-msg-generator/ENHANCED_MARKERS_SPEC.md](../commit-msg-generator/ENHANCED_MARKERS_SPEC.md)

---

## 💡 最佳实践

### 分组原则
- ✅ 职责单一、大小适中（3-8文件）
- ✅ 逻辑完整、依赖清晰
- ❌ 避免过大分组（20+文件）
- ❌ 避免职责混杂

### Agent选择
- ✅ 文档 → knowledge-manager
- ✅ 技术领域匹配 → 对应技术栈 agent
- ✅ 测试 → qa-engineer
- ❌ 避免全用 general-purpose

### 并行策略
- ✅ 不同端的独立功能可并行
- ❌ 同一文件的多次修改不可并行
- ❌ 有明确依赖关系的变更需串行

### 提交粒度
- **合适**: 3-15个文件，单一变更类型
- **太粗**: >50个文件，混合类型
- **太细**: 每个文件单独提交

**完整实践**: [ADVANCED_GUIDE.md - 最佳实践](./ADVANCED_GUIDE.md#最佳实践)

---

## 🚨 故障处理

### 常见问题

| 问题 | 症状 | 快速解决 |
|------|------|---------|
| **Git冲突** | 多个Task同时修改同一文件 | 暂停 → 解决冲突 → 重启 |
| **Task失败** | Subagent超时/失败 | AgentOutputTool查看输出 |
| **格式错误** | Git hook拒绝提交 | git commit --amend 修正 |

**详细处理**: [ADVANCED_GUIDE.md - 故障处理](./ADVANCED_GUIDE.md#故障处理)

---

## ✅ 快速检查清单

### 执行前
- [ ] 识别变更类型 (A/B/C/D/E)
- [ ] 类型E: 扫描所有子模块变更
- [ ] 读取 UPM (类型A/B/D/E需要)
- [ ] git status 确认所有变更
- [ ] 分组逻辑清晰
- [ ] Subagent分配合理

### 执行后
- [ ] git log 确认所有提交
- [ ] 提交消息格式正确
- [ ] 分支状态正常

**完整清单**: [TROUBLESHOOTING.md - 检查清单](./TROUBLESHOOTING.md#检查清单)

---

## 📚 相关文档

### Skill 文档（按需加载）
| 文档 | 职责 | 加载场景 |
|------|------|---------|
| [CHANGE_TYPES.md](./CHANGE_TYPES.md) | 变更类型识别 | 确定A/B/C/D/E类型 |
| [WORKFLOW_CORE.md](./WORKFLOW_CORE.md) | 通用流程 (Phase 2-6) | 每次提交 |
| [WORKFLOW_TYPE_A.md](./WORKFLOW_TYPE_A.md) | 子模块变更流程 | 类型A |
| [WORKFLOW_TYPE_B.md](./WORKFLOW_TYPE_B.md) | 主项目变更流程 | 类型B |
| [WORKFLOW_TYPE_C.md](./WORKFLOW_TYPE_C.md) | 跨项目共享流程 | 类型C |
| [WORKFLOW_TYPE_D.md](./WORKFLOW_TYPE_D.md) | 跨模块协同流程 | 类型D |
| [WORKFLOW_TYPE_E.md](./WORKFLOW_TYPE_E.md) | 全项目变更流程 | 类型E (v2.2.0新增) |
| [SUBMODULE_GUIDE.md](./SUBMODULE_GUIDE.md) | 子模块处理指南 | 类型E (v2.2.0新增) |
| [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) | 故障处理+最佳实践 | 遇到问题时 |
| [EXAMPLES.md](./EXAMPLES.md) | 完整工作流示例 | 学习参考 |
| [CHANGELOG.md](./CHANGELOG.md) | 版本历史 | 了解变更 |

### 依赖 Skill
- **commit-msg-generator** - v2.0.0

### 核心规范
- Git提交消息: `@standards/conventions/git-commit.md`
- AI-DDD进度管理: `@standards/core/progress-management/ai-ddd-progress-management-core.md` v1.0.0
- UPM文档路径: `@{module}/[docs/]project-planning/unified-progress-management.md`

### 外部资源
- [Conventional Commits](https://www.conventionalcommits.org/)

---

## 💡 使用提示

1. **首次使用**: 阅读本文档了解决策树和变更类型
2. **识别类型**: [CHANGE_TYPES.md](./CHANGE_TYPES.md) 确定变更类型
3. **执行流程**: 加载对应 WORKFLOW_TYPE_*.md + WORKFLOW_CORE.md
4. **查看示例**: [EXAMPLES.md](./EXAMPLES.md) 查看完整工作流
5. **遇到问题**: [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)

---

**版本**: 2.2.0
**最后更新**: 2026-01-01
**Skill版本**: 2.2.0 (新增类型E全项目变更支持)
