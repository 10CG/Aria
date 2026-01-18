# Aria

> 让 AI 真正理解你的软件项目

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Forgejo](https://img.shields.io/badge/Forgejo-Aria-blue)](https://forgejo.10cg.pub/10CG/Aria)

---

## 什么是 Aria？

Aria 是一套 **AI-DDD (AI 辅助领域驱动设计) 方法论**，通过结构化的工作流让 Claude Code 这样的 AI 助手深度参与软件开发全过程。

与传统"AI 写代码"工具不同，Aria 关注的是：**如何让 AI 理解项目意图，成为有价值的协作者**。

```
┌─────────────────────────────────────────────────────────┐
│  传统模式: AI 是工具 (你问 → AI 答)                    │
│  Aria 模式: AI 是协作者 (AI 理解 → 你确认 → 共同交付)  │
└─────────────────────────────────────────────────────────┘
```

---

## 为什么需要 Aria？

### 问题

- AI 给的建议不符合项目规范
- 每次都要重新解释项目背景
- 代码和文档不同步
- 需求变更没有追溯记录

### 解决方案

| 特性 | 说明 |
|------|------|
| **🎯 状态感知** | AI 自动扫描项目，理解当前进度 |
| **📋 规范先行** | OpenSpec 标准化需求描述 |
| **🔄 十步循环** | 结构化的 AI 协作工作流 |
| **📄 文档同步** | 架构文档与代码共同演进 |

---

## 核心概念：十步循环

```
┌─────────────────────────────────────────────────────────┐
│                    十步循环 (Ten-Step Cycle)             │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  A. 规划阶段                                            │
│  └── A.0 状态扫描 → A.1 规范 → A.2 规划 → A.3 分配      │
│                                                          │
│  B. 开发阶段                                            │
│  └── B.1 分支 → B.2 开发 + 评审                         │
│                                                          │
│  C. 集成阶段                                            │
│  └── C.1 提交 → C.2 合并                                │
│                                                          │
│  D. 收尾阶段                                            │
│  └── D.1 进度更新 → D.2 归档                            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 快速开始

### 1. 复制项目文件

```bash
# 复制到你的项目根目录
git clone https://forgejo.10cg.pub/10CG/Aria.git
cp -r Aria/.claude your-project/
cp Aria/CLAUDE.md your-project/
```

### 2. 配置项目

编辑 `.claude/local.md`，添加你的项目信息：

```markdown
# 你的项目

> 项目描述...

## 技术栈
- Backend: Python/FastAPI
- Frontend: React/Vue
```

### 3. 开始使用

```bash
# 在 Claude Code 中
/state-scanner    # 扫描项目状态
```

---

## 项目结构

```
Aria/
├── CLAUDE.md              # AI 项目上下文
├── README.md              # 本文档
├── .claude/
│   ├── local.md           # AI 工作流配置
│   ├── agents/            # 专业 Agents
│   └── skills/            # 十步循环 Skills
├── standards/             # 方法论规范
│   ├── core/              # 核心定义
│   ├── openspec/          # 需求规范
│   └── workflow/          # 工作流
├── docs/                  # 研究文档
└── aria/                  # 辅助工具
```

---

## 核心组件

### OpenSpec 需求规范

标准化的需求描述格式：

| Level | 适用场景 | 产物 |
|-------|----------|------|
| 1 | 简单修复 | 无需规范 |
| 2 | 中等功能 | `proposal.md` |
| 3 | 架构变更 | `proposal.md` + `tasks.md` |

### Skills 工作流

每个 Phase 对应一个 Skill，确保流程标准化：

- `state-scanner` - 项目状态扫描
- `spec-drafter` - 需求规范生成
- `task-planner` - 任务分解
- `branch-manager` - 分支管理
- `phase-b-developer` - 开发执行
- `commit-msg-generator` - 提交消息
- `progress-updater` - 进度更新

---

## 适用场景

| 场景 | Aria 帮助你 |
|------|-------------|
| 新功能开发 | 从需求到代码的完整流程 |
| Bug 修复 | TDD 驱动的修复流程 |
| 重构 | 架构文档同步的代码演进 |
| 代码审查 | 规范合规性自动检查 |
| 知识传递 | 新人快速理解项目 |

---

## 项目状态

```
当前版本: 1.0.0
成熟度:   核心流程已验证
研究方向: AI 协作模式的可重现性
```

---

## 贡献指南

欢迎讨论和改进！

1. Fork 本项目
2. 创建你的分支 (`git checkout -b feature/AmazingFeature`)
3. 遵循十步循环流程
4. 提交 Pull Request

---

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 联系方式

- **仓库**: https://forgejo.10cg.pub/10CG/Aria
- **维护**: 10CG Lab

---

**让 AI 成为你的软件开发伙伴 🚀**
