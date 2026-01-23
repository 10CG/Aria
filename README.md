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

### 方式一: 使用 Plugin (推荐，用于其他项目)

```bash
# 添加 marketplace
/plugin marketplace add https://github.com/10CG/aria-plugin

# 安装 Skills
/plugin install aria@10cg-aria-plugin

# 安装 Agents (手动复制)
# Linux/macOS
git clone https://github.com/10CG/aria-plugin.git /tmp/aria-plugin
cp -r /tmp/aria-plugin/agents/* ~/.claude/agents/
rm -rf /tmp/aria-plugin

# Windows
git clone https://github.com/10CG/aria-plugin.git %TEMP%\aria-plugin
xcopy /E /I %TEMP%\aria-plugin\agents %USERPROFILE%\.claude\agents
rmdir /S /Q %TEMP%\aria-plugin

# 使用
/aria:state-scanner    # 扫描项目状态
/aria:spec-drafter     # 创建需求规范
# 直接调用 Agent
请使用 tech-lead 规划这个功能的架构
```

### 方式二: 使用 Submodule (用于 Aria 项目自身)

```bash
# 克隆 Aria 仓库
git clone ssh://forgejo@forgejo.10cg.pub/10CG/Aria.git
cd Aria
git submodule update --init --recursive

# 使用
/state-scanner              # 扫描项目状态
/spec-drafter              # 创建需求规范
请使用 tech-lead 规划这个功能的架构
```

### 配置项目

编辑 `.claude/local.md`，添加你的项目信息：

```markdown
# 你的项目

> 项目描述...

## 技术栈
- Backend: Python/FastAPI
- Frontend: React/Vue
```

---

## 项目结构

```
Aria/                          # Aria 主项目 (方法论研究)
├── CLAUDE.md                  # AI 项目上下文
├── README.md                  # 本文档
├── .claude/
│   └── local.md               # AI 工作流配置
├── standards/                 # 方法论规范 (子模块)
│   ├── core/                  # 核心定义
│   ├── openspec/              # 需求规范
│   └── workflow/              # 工作流
├── aria/                      # Aria 插件 (子模块)
│   ├── skills/                # 23 个 Skills
│   ├── agents/                # 9 个 Agents
│   └── .claude-plugin/        # Plugin 配置
└── docs/                      # 研究文档
```

### 使用方式对比

| | Aria 项目自身 | 其他项目 |
|---|--------------|----------|
| **安装方式** | Git Submodule | Plugin Marketplace |
| **来源** | `aria/` 子模块 | `/plugin install aria@10cg-aria-plugin` |
| **调用格式** | `/state-scanner` 或 `aria/skills/state-scanner` | `/aria:state-scanner` |
| **更新方式** | `git submodule update --remote` | `/plugin marketplace update` |

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

- **主仓库**: https://forgejo.10cg.pub/10CG/Aria
- **插件仓库**: https://forgejo.10cg.pub/10CG/aria-plugin
- **规范仓库**: https://forgejo.10cg.pub/10CG/aria-standards
- **维护**: 10CG Lab

---

**让 AI 成为你的软件开发伙伴 🚀**
