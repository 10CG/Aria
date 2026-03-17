# Aria - AI-DDD Methodology

> **项目本质**: AI 辅助的领域驱动设计方法论研究
> **核心假设**: AI 不是工具，而是理解项目意图的协作者
> **版本**: 1.0.0

---

## 文档边界

| 文档 | 受众 | 目的 |
|------|------|------|
| **README.md** | 人类用户 | 项目介绍、快速开始、使用指南 |
| **CLAUDE.md** | AI 助手 | 项目定位、上下文地图、不可协商规则 |

**README.md** = "用户如何使用 Aria"
**CLAUDE.md** = "AI 如何理解 Aria 项目"

---

## 项目定位

Aria 是一个**方法论研究项目**，而非框架实现。它探索如何让 AI Agent 深度参与软件工程全流程，从需求到交付的完整协作模式。

### 核心假设

```
传统模式: 人类主导 → AI 辅助
Aria 模式: AI 理解 → 人类确认 → 协作交付
```

### 研究目标

1. **可重现的 AI 协作流程** - 不同项目、不同 AI 都能获得一致结果
2. **最小化的上下文传递成本** - AI 能快速理解项目状态
3. **结构化的决策记录** - 每个"为什么"都有据可查

---

## 核心概念

### AI-DDD (AI-Assisted Domain-Driven Design)

领域驱动设计的 AI 增强版，强调 AI 对业务领域的理解和建模能力。

### 十步循环 (Ten-Step Cycle)

```
A. 规划 (Spec & Planning)
├── A.0 状态扫描    → 理解当前在哪
├── A.1 规范创建    → 定义要去哪
├── A.2 任务规划    → 规划怎么去
└── A.3 Agent 分配  → 谁去执行

B. 开发 (Development)
├── B.1 分支创建    → 隔离工作空间
├── B.2 执行验证    → 开发+评审

C. 集成 (Integration)
├── C.1 提交        → 记录变更
└── C.2 合并        → 集成到主干

D. 收尾 (Closure)
├── D.1 进度更新    → 同步状态
└── D.2 归档        → 完成闭环
```

### OpenSpec 需求规范

标准化的需求描述格式，让 AI 和人类对"做什么"达成共识。

- **Level 1**: Skip - 简单修复，无需规范
- **Level 2**: Minimal - `proposal.md`
- **Level 3**: Full - `proposal.md` + `tasks.md`

---

## 认知框架

理解 Aria 项目的四个原则:

### 1. 规范先行 (Spec First)

```
❌ 先写代码，后补文档
✅ 先写规范，后写代码

原因: AI 需要理解"为什么"才能给出好的建议
```

### 2. 小步迭代 (Incremental)

```
❌ 大爆炸式重构
✅ 每个任务 4-8 小时可完成

原因: 小步快跑，风险可控，AI 容易验证
```

### 3. 文档同步 (Docs in Sync)

```
❌ 代码和文档分离维护
✅ 架构文档与代码同步演进

原因: AI 通过文档理解结构，文档过时 = AI 误解
```

### 4. 向后兼容 (Backward Compatible)

```
❌ 破坏性变更
✅ 所有变更保持兼容

原因: 方法论需要稳定性，频繁弃用会破坏信任
```

---

## 信息地图

### 子模块职责

| 子模块 | 职责 | 关键内容 |
|--------|------|----------|
| `standards/` | 方法论定义 | 十步循环、OpenSpec、约定 |
| `aria/` | 工具集 (Plugin) | Skills + Agents + Hooks 配置 |

### 目录导航

```
需要理解 X? 找这里:

├── 项目定位       → standards/openspec/changes/aria-proposal.md
├── 工作流程       → standards/core/ten-step-cycle/
├── 需求规范       → standards/openspec/project.md
├── 提交规范       → standards/conventions/git-commit.md
├── 进度管理       → standards/core/progress-management/
└── 研究文档       → docs/
```

### Plugin 调用方式 (Aria 项目内部)

在 Aria 项目内部，Skills 和 Agents 可以直接调用：

```
Skills:
  /state-scanner
  /spec-drafter
  /workflow-runner

Agents:
  /tech-lead
  /backend-architect
  /knowledge-manager
```

其他项目通过 Plugin 安装后使用 `/aria:` 前缀。

---

## 技术约束

### Aria 不做什么

- ❌ 不提供代码生成模板
- ❌ 不强制特定编程语言
- ❌ 不绑定特定 AI 模型
- ❌ 不提供 CI/CD 配置

### Aria 的边界

```
┌─────────────────────────────────────────────────────────┐
│                   Aria 的边界                           │
├─────────────────────────────────────────────────────────┤
│  ✅ 定义: 如何思考、如何协作、如何决策                 │
│  ✅ 规范: 文档格式、工作流程、命名约定                 │
│  ❌ 实现: 具体代码、工具配置、部署脚本                 │
└─────────────────────────────────────────────────────────┘
```

---

## 版本管理规范

### 版本号语义

遵循 [Semantic Versioning 2.0.0](https://semver.org/):

```
MAJOR.MINOR.PATCH

MAJOR: 破坏性变更 / 架构重构
MINOR: 新功能 / 向后兼容
PATCH: Bug 修复 / 小改进
```

### Aria 特殊约定

| 变更类型 | 版本变更 | 示例 |
|----------|----------|------|
| 新增 Skill | MINOR+ | 1.2.0 → 1.3.0 |
| Skill 架构重构 | MINOR+ | 1.2.0 → 1.3.0 |
| 文档更新 | PATCH | 1.3.0 → 1.3.1 |
| Bug 修复 | PATCH | 1.3.0 → 1.3.1 |
| 破坏性变更 | MAJOR+ | 1.x → 2.0 |

### 版本信息文件架构

```
aria/
├── .claude-plugin/
│   ├── plugin.json       # 主版本文件 (真理来源 Source of Truth)
│   ├── marketplace.json   # 市场发布配置
│   └── hooks.json        # Hooks 配置
├── VERSION               # 人类可读版本快照
├── CHANGELOG.md          # 版本变更记录
└── README.md             # 包含版本号
```

### 版本发布检查清单

每次发布新版本时，必须更新以下文件：

```yaml
真理来源 (Source of Truth):
  - [ ] aria/.claude-plugin/plugin.json (version 字段)

派生文件 (必须同步):
  - [ ] aria/.claude-plugin/marketplace.json (version, plugins[].version)
  - [ ] aria/.claude-plugin/hooks.json (version 字段)
  - [ ] aria/VERSION (创建或更新)
  - [ ] aria/CHANGELOG.md (添加新版本条目)
  - [ ] aria/README.md (更新版本号和 Skills 数量)

主项目:
  - [ ] 更新子模块指针 (git add aria)
  - [ ] 主项目/VERSION 更新插件版本记录
```

### 版本信息一致性

所有版本信息文件必须保持一致：

| 文件 | 字段 | 示例 |
|------|------|------|
| plugin.json | `version` | `"1.3.0"` |
| marketplace.json | `version`, `plugins[].version` | `"1.3.0"` |
| hooks.json | `version` | `"1.3.0"` |
| VERSION | `版本` | `1.3.0` |
| CHANGELOG.md | `## [X.Y.Z]` | `## [1.3.0]` |
| README.md | `**Version**: X.Y.Z` | `**Version**: 1.3.0` |

**重要**: `plugin.json` 是版本号的**真理来源 (Source of Truth)**，其他文件必须与其保持一致。

---

## 与其他方法论的关系

```
                    DDD (领域驱动设计)
                           │
                           │ 延伸
                           ▼
                    AI-DDD (本项目的核心)
                           │
                           │ 具体化
                           ▼
                  十步循环 (工作流)
                           │
                           │ 形式化
                           ▼
                 OpenSpec (需求规范)
```

---

## 不可协商规则

这些规则是 Aria 的基石，违背它们就不符合 Aria 方法论:

1. **所有需求变更必须有 OpenSpec** - Level 2 或 Level 3
2. **十步循环不能跳过 Phase A** - 必须先理解现状再行动
3. **文档与代码必须同步更新** - 架构文档与代码一致
4. **每个提交必须遵循规范** - Conventional Commits 格式
5. **项目变更必须在项目的 openspec/changes/ 目录** - 不得放在 `standards/openspec/changes/`

```
┌─────────────────────────────────────────────────────────────────┐
│  规则 #5: 变更位置边界 (OpenSpec 兼容)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  aria-standards/openspec/changes/  → 已废弃，不应使用           │
│                                                                 │
│  项目/openspec/changes/            ← 正确位置                   │
│  ├── Aria/openspec/changes/        → Aria 自身的变更            │
│  └── your-project/openspec/changes/ → 用户项目的变更            │
│                                                                 │
│  原因: aria-standards 是共享子模块，变更应属于项目自身           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 项目状态

```
当前阶段: 研究中
成熟度:   0.7 (核心流程已验证)
插件版本: v1.5.1 (aria-plugin)
主项目版本: v1.0.2
```

---

**更新**: 2026-02-06
**维护**: 10CG Lab
**主仓库**: https://forgejo.10cg.pub/10CG/Aria
**插件仓库**: https://forgejo.10cg.pub/10CG/aria-plugin
**规范仓库**: https://forgejo.10cg.pub/10CG/aria-standards
