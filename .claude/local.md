# Aria - AI-DDD Methodology

> **版本**: 1.1.0
> **更新**: 2026-01-18
> **性质**: 方法论研究项目

---

## 项目定位

Aria 是一个基于 AI 辅助的领域驱动设计 (AI-DDD) 方法论研究项目，旨在探索 AI Agent 在软件工程全流程中的深度集成模式。

### 核心特征

| 特征 | 说明 |
|------|------|
| **方法论优先** | 定义规范而非实现框架 |
| **AI-Native** | 设计 AI Agent 协作模式 |
| **十步循环** | 结构化开发工作流 |
| **OpenSpec** | 标准化需求规范格式 |

---

## 项目结构

```
Aria/
├── .claude/
│   ├── local.md              # 本配置文件
│   ├── agents/               # AI-DDD 专用 Agents (子模块)
│   ├── skills/               # 十步循环 Skills (子模块)
│   └── trigger-rules.json    # 自动触发规则
├── standards/                # AI-DDD 规范体系 (子模块)
│   ├── core/                 # 核心方法论
│   ├── openspec/             # 需求规范标准
│   ├── workflow/             # 工作流定义
│   └── conventions/          # 约定和格式
├── docs/                     # 研究文档
└── aria/                     # 辅助工具 (hooks)
```

---

## 核心概念

### 十步循环 (Ten-Step Cycle)

```
A. 规划阶段 (Spec & Planning)
├── A.0 状态扫描      → state-scanner
├── A.1 规范创建      → spec-drafter
├── A.2 任务规划      → task-planner
└── A.3 Agent 分配    → task-planner

B. 开发阶段 (Development)
├── B.1 分支创建      → branch-manager
├── B.2 执行验证      → phase-b-developer
└── B.Review 两阶段评审

C. 集成阶段 (Integration)
├── C.1 Git 提交      → commit-msg-generator
└── C.2 PR 创建       → branch-manager

D. 收尾阶段 (Closure)
├── D.1 进度更新      → progress-updater
└── D.2 归档          → phase-d-closer
```

### OpenSpec 需求规范

- **Level 1**: Skip - 简单修复，无需规范
- **Level 2**: Minimal - 中等功能，proposal.md
- **Level 3**: Full - 架构变更，proposal.md + tasks.md

---

## AI-DDD 工作流

### 状态感知入口

任何开发任务从 **A.0 状态扫描** 开始：

```
用户: "我要开发一个新功能"
   ↓
state-scanner: 分析当前状态 → 推荐工作流
   ↓
用户确认 → 执行相应 Phase
```

### 自动触发规则

| 用户意图关键词 | 推荐技能 |
|----------------|----------|
| 状态、进度、扫描 | state-scanner |
| 规范、提案、spec | spec-drafter |
| 任务、规划、分解 | task-planner |
| 分支、worktree | branch-manager |
| 测试、tdd | tdd-enforcer |
| 提交、commit | commit-msg-generator |
| 架构、设计文档 | arch-search / arch-update |
| 进度更新 | progress-updater |

```
禁用自动触发: 请求前加 NO_AUTO_TRIGGER
```

---

## 子模块说明

### standards (规范子模块)

AI-DDD 方法论的核心定义，包含：

- `core/` - 十步循环、进度管理、Agent 规范
- `openspec/` - 需求规范格式和模板
- `workflow/` - 工作流定义和最佳实践
- `conventions/` - Git commit、changelog 等格式约定

### skills (技能子模块)

十步循环的执行单元，每个 Phase 对应一个或多个 Skill。

### agents (代理子模块)

专业领域的 AI Agent 定义。

---

## 开发原则

1. **规范先行** - 需求变更先写 OpenSpec
2. **小步提交** - 每个任务独立提交
3. **文档同步** - 代码与架构文档同步更新
4. **向后兼容** - 所有变更保持兼容性

---

## 相关文档

- [十步循环概览](standards/core/ten-step-cycle/README.md)
- [OpenSpec 项目定义](standards/openspec/project.md)
- [AI-DDD 进度管理](standards/core/progress-management/)

---

**维护**: 10CG Lab
**仓库**: https://forgejo.10cg.pub/10CG/Aria
