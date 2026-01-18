# Aria System Architecture

> **Version**: 1.0.0
> **Status**: Active
> **Created**: 2026-01-18
> **Project Type**: Methodology Research

---

## 1. Executive Summary

Aria 是一个**方法论研究项目**，探索 AI Agent 在软件工程全流程中的深度集成模式。它不是软件框架，而是一套规范、约定和工作流定义。

**核心架构模式**: 规范驱动的 AI 协作 (Spec-Driven AI Collaboration)

**关键特征**:
- 规范先行 (Spec First) - OpenSpot 需求规范
- 结构化工作流 (Ten-Step Cycle) - 可重现的 AI 协作流程
- 子模块化组织 (Modular Standards) - 方法论定义与工具分离

---

## 2. System Overview

### 2.1 系统目标

```
目标: 让 AI 成为理解项目意图的协作者，而非被动工具

手段:
├── 标准化需求描述 (OpenSpec)
├── 结构化工作流程 (十步循环)
└── 规范化交互接口 (Skills + Agents)
```

### 2.2 关键利益相关者

| 角色 | 关注点 |
|------|--------|
| **研究者** | 方法论有效性、可重现性 |
| **开发者** | 工作流效率、学习曲线 |
| **AI Agent** | 上下文完整性、指令清晰度 |

### 2.3 质量属性

| 属性 | 目标 |
|------|------|
| **可理解性** | 新人 30 分钟内理解核心概念 |
| **可操作性** | 每个步骤都有明确输入输出 |
| **可扩展性** | 支持新增 Skill 和 Agent |
| **兼容性** | 与 Claude Code 无缝集成 |

---

## 3. Architecture Diagram

### 3.1 项目结构

```
┌─────────────────────────────────────────────────────────────────┐
│                         Aria 项目                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   CLAUDE.md   │    │  README.md   │    │ .claude/     │      │
│  │  (AI 认知)    │    │  (人类文档)   │    │  (AI 配置)   │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                     standards/ (子模块)                      │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │  │
│  │  │  core   │  │openspec │  │ workflow │  │conventions│  │  │
│  │  │方法论核心│  │需求规范 │  │工作流定义│  │格式约定  │   │  │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                    .claude/ (子模块)                        │  │
│  │  ┌─────────┐  ┌─────────┐                                 │  │
│  │  │ agents/ │  │ skills/ │                                 │  │
│  │  │专业代理 │  │工作流单元│                                 │  │
│  │  └─────────┘  └─────────┘                                 │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │    docs/     │    │    tests/    │    │    aria/     │      │
│  │  研究文档     │    │   测试用例    │    │  辅助工具     │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 概念架构

```
┌─────────────────────────────────────────────────────────────────┐
│                     AI-DDD 方法论层级                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  L0: 业务需求 (PRD / User Stories)                              │
│      "做什么 & 为什么"                                          │
│                           │                                     │
│                           ▼                                     │
│  L1: 系统架构 (System Architecture)                              │
│      "技术组织方式"                                              │
│                           │                                     │
│                           ▼                                     │
│  L2: 模块架构 (Module Architecture + OpenSpec)                    │
│      "具体实现方案"                                              │
│                           │                                     │
│                           ▼                                     │
│  L3: 代码实现 (Implementation)                                   │
│      "可执行代码"                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Module Boundaries

| 模块 | 职责 | 拥有 | 使用 |
|------|------|------|------|
| **standards/** | 方法论定义 | 核心规范、OpenSpec、约定 | - |
| **.claude/skills/** | 工作流执行单元 | 十步循环实现 | standards/ 规范 |
| **.claude/agents/** | 专业领域代理 | 特定领域知识 | skills/ 触发 |
| **docs/** | 研究文档 | 分析、设计、记录 | standards/ 格式 |
| **tests/** | 验证用例 | 集成测试、验收测试 | standards/ 测试规范 |
| **aria/** | 辅助工具 | Hooks、脚本 | .claude/ 配置 |

### 模块交互规则

```
1. skills/ 只读取 standards/，不修改
2. agents/ 可被 skills/ 调用
3. docs/ 遵循 standards/ 的文档规范
4. tests/ 验证 standards/ 的规范有效性
```

---

## 5. Technology Decisions

### TD-001: 使用 Markdown 作为主要文档格式

**上下文**: 需要人类和 AI 都能轻松阅读的文档格式

**决策**: 使用 Markdown (GitHub Flavored)

**理由**:
- Claude Code 原生支持
- 版本控制友好 (diff 清晰)
- 可渲染为多种格式 (HTML, PDF)
- 支持代码块和图表

**后果**:
- ✅ AI 可直接读取和理解
- ✅ 易于协作编辑
- ⚠️ 复杂图表需要 ASCII/Mermaid

### TD-002: 子模块化组织规范

**上下文**: 规范可能独立演进

**决策**: 使用 Git 子模块管理 standards/、agents/、skills/

**理由**:
- 规范可跨项目复用
- 独立版本控制
- 降低主仓库复杂度

**后果**:
- ✅ 规范可单独更新
- ⚠️ 需要协调子模块指针
- ⚠️ 新手需要学习子模块操作

### TD-003: 不使用传统编程语言

**上下文**: Aria 是方法论，非软件框架

**决策**: 不提供 Python/Java/JavaScript SDK

**理由**:
- 方法论本质是"知识"而非"代码"
- 避免绑定特定技术栈
- 聚焦 Claude Code 生态

**后果**:
- ✅ 技术栈无关
- ✅ 长期稳定
- ⚠️ 无法直接"运行"

---

## 6. Cross-Cutting Concerns

### 6.1 文档一致性

```
规则: 代码和架构文档必须同步

检查点:
- Phase B.3: 代码评审时检查架构文档
- Phase D.2: 归档时验证文档完整性

工具:
- arch-update: 自动更新架构文档
- requirements-validator: 验证文档链路
```

### 6.2 向后兼容

```
原则: 新版本不得破坏现有工作流

保证:
- 所有变更有 migration guide
- 旧格式至少保留 2 个版本
- 弃用功能有明显的 deprecation 警告
```

### 6.3 可测试性

```
要求: 每个规范变更都有验证方法

实现:
- standards/openspec/: OpenSpec validator
- skills/: SKILL.md lint check
- conventions/: 格式验证脚本
```

---

## 7. Data Architecture

### 7.1 数据类型

| 数据 | 格式 | 位置 | 更新频率 |
|------|------|------|----------|
| **项目变更** | **OpenSpec (Markdown)** | **{project}/openspec/changes/** | **按功能** |
| 进度状态 | UPM (Markdown) | 各模块 docs/project-planning/ | 每周期 |
| 技能定义 | SKILL.md | .claude/skills/*/ | 按需 |
| 架构文档 | System Arch (Markdown) | docs/architecture/ | 按架构变更 |

### 7.1.1 变更位置边界 (OpenSpec 兼容)

```
┌─────────────────────────────────────────────────────────────────┐
│  重要: 职责分离原则 (OpenSpec 标准结构)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  aria-standards/openspec/changes/  → 已废弃 (v2.0)              │
│                                                                 │
│  项目/openspec/changes/            ← 正确位置 (OpenSpec 兼容)   │
│  ├── Aria/openspec/changes/        → Aria 项目自身的变更        │
│  │   └── aria-workflow-enhancement/                           │
│  └── your-project/openspec/changes/ → 用户项目的变更            │
│      └── your-feature/                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

原因:
1. aria-standards 是共享子模块，变更应属于各自项目
2. Git 子模块特性导致变更被追踪到错误的仓库
3. 与 OpenSpec CLI 工具的标准结构保持一致
```

### 7.2 数据流

```
┌─────────────┐
│  PRD /      │ 需求输入
│  User Story │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  OpenSpec   │ 技术方案 (L2)
│  proposal   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Implementation │ 代码实现 (L3)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    UPM      │ 进度追踪
└─────────────┘
```

---

## 8. Integration Patterns

### 8.1 Claude Code 集成

```
集成方式: 文档即配置

触发机制:
├── 自动: 关键词匹配 (.claude/local.md 定义)
└── 手动: /skill-name 命令

上下文加载:
├── CLAUDE.md (根目录) - 项目心智模型
├── .claude/local.md - 工作流配置
└── .claude/skills/*/SKILL.md - 技能定义
```

### 8.2 Forgejo 集成

```
同步对象: User Story ↔ Forgejo Issue

工具: forgejo-sync Skill

触发:
- Phase C.2: PR 创建后
- Phase D.1: 进度更新时

方向: 双向同步
```

### 8.3 跨项目复用

```
复用单元: standards/ 子模块

模式:
1. Fork aria-standards 仓库
2. 自定义规范内容
3. 在项目中引用 fork 版本

约束:
- 保持核心规范兼容
- 记录自定义差异
```

---

## 9. Evolution Roadmap

### 9.1 当前阶段 (v1.0)

```
状态: 核心流程已验证

✅ 完成:
  - 十步循环定义
  - OpenSpec 格式
  - Skills 框架
  - 文档架构

🚧 进行中:
  - 实际项目验证
  - 工具链完善
```

### 9.2 未来方向

| 阶段 | 目标 | 时间线 |
|------|------|--------|
| v1.1 | 增强工作流自动化 | Q2 2026 |
| v1.2 | 扩展到更多 AI 平台 | Q3 2026 |
| v2.0 | 企业级功能支持 | Q4 2026 |

---

## 10. Related Documents

| 文档 | 位置 | 说明 |
|------|------|------|
| 十步循环概览 | standards/core/ten-step-cycle/ | 核心工作流 |
| OpenSpec 项目定义 | standards/openspec/project.md | 需求规范格式 |
| UPM 进度管理 | standards/core/progress-management/ | 进度追踪 |
| System Architecture 规范 | standards/core/documentation/system-architecture-spec.md | 本文档格式定义 |

---

## Version History

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-01-18 | 初始版本 |

---

**维护**: 10CG Lab
**仓库**: https://forgejo.10cg.pub/10CG/Aria
**许可**: MIT License
