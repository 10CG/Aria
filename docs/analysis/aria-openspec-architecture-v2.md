# Aria OpenSpec 架构重构方案 v2.0

> **Created**: 2026-01-18
> **Status**: Proposal
> **Type**: Architecture Decision

---

## 问题陈述

### 当前错误

```
aria-standards/openspec/changes/
├── backend-api-development/        ❌ 属于用户项目
├── complete-requirements-chain/   ❌ 属于用户项目
└── aria-workflow-enhancement/     ✅ 属于 Aria
```

**根本问题**: aria-standards 子模块被误用为"用户项目的变更容器"。

### 为什么发生?

1. Git 子模块的工作目录特性
2. 用户在子模块内创建变更
3. 变更被追踪到子模块仓库
4. 混淆了"方法论定义"和"项目变更"的边界

---

## 正确架构

### 原则

```
┌─────────────────────────────────────────────────────────────────┐
│  核心原则: 职责分离                                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  aria-standards:     方法论定义 (格式、模板、规范)                │
│  用户项目:           具体变更 (specs/ 或 openspec/changes/)      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 目录结构

```
aria-standards (子模块):
├── openspec/
│   ├── project.md              ✅ OpenSpec 格式定义
│   ├── templates/              ✅ 模板 (proposal-minimal.md, etc.)
│   ├── examples/               ✅ 示例 (仅供学习参考)
│   │   ├── feature-example/
│   │   └── bugfix-example/
│   ├── archive/                ✅ Aria 自身的方法论变更归档
│   │   ├── 2025-12-23-ten-step-restructure/
│   │   └── 2026-01-18-aria-workflow-enhancement/
│   └── README.md               ✅ 使用说明
│
└── ❌ 删除 changes/ 目录 (用户不应在此创建变更)

用户项目 (如 todo-app):
├── standards/                  → aria-standards (子模块)
├── specs/                      或 openspec/changes/
│   ├── user-auth-feature/
│   │   ├── proposal.md
│   │   └── tasks.md
│   └── api-refactoring/
│       └── proposal.md
└── docs/
    └── requirements/
        ├── prd.md
        └── user-stories/
```

---

## 行动计划

### Phase 1: 立即清理

#### 1.1 移除不属于 Aria 的变更

```bash
# 在 aria-standards 子模块中
cd standards/

# 移动到 examples/ (作为参考示例)
mkdir -p openspec/examples/user-projects
mv openspec/changes/backend-api-development openspec/examples/user-projects/
mv openspec/changes/complete-requirements-chain openspec/examples/user-projects/

# 保留 Aria 自身的变更
# openspec/changes/aria-workflow-enhancement/ 保留
```

#### 1.2 更新 aria-standards README

在 `standards/openspec/README.md` 添加:

```markdown
## 用户项目规范位置

⚠️ **重要**: 请勿在 `standards/openspec/changes/` 中创建项目变更。

用户项目应在自己的仓库中创建 `specs/` 或 `openspec/changes/` 目录:

```
your-project/
├── standards/          → aria-standards 子模块
├── specs/              ← 你的项目变更在这里
│   └── your-feature/
│       └── proposal.md
```

本仓库的 `changes/` 目录仅用于 Aria 自身的方法论改进。
```

### Phase 2: 文档更新

#### 2.1 更新 Aria System Architecture

在 `docs/architecture/system-architecture.md` 中明确:

```yaml
Data Architecture:
  用户项目变更:
    格式: OpenSpec (Markdown)
    位置: {project}/specs/ 或 openspec/changes/
    追踪: 用户项目的 Git 仓库

  Aria 方法论变更:
    格式: OpenSpec (Markdown)
    位置: standards/openspec/changes/
    追踪: aria-standards 仓库
    约束: 仅限 Aria 自身的方法论改进
```

#### 2.2 更新 CLAUDE.md

添加不可协商规则:

```markdown
## 不可协商规则

5. **项目变更位置**: 用户项目变更必须在 `specs/` 目录，不得放在 `standards/openspec/changes/`
```

### Phase 3: 长期演进 (可选)

#### 选项 A: CLI 工具模式 (类似 OpenSpec)

```bash
# 安装 Aria CLI
npm install -g @aria/cli

# 初始化项目
aria init
# 创建:
# - .aria/ (配置)
# - specs/ (变更目录)
# - CLAUDE.md (AI 配置模板)
```

**优势**:
- 完全避免子模块混淆
- 用户项目独立
- 更易于分发

**劣势**:
- 需要额外开发
- 从子模块迁移成本

#### 选项 B: 保持子模块 + 强化边界

```yaml
当前模式优化:
  1. 文档强化边界说明
  2. 添加 pre-commit hook 检测
  3. examples/ 提供清晰参考
```

**优势**:
- 无需重构
- 向后兼容

**劣势**:
- 依赖用户自觉遵守

---

## 与 Superpowers/OpenSpec 的对比

| 项目 | OpenSpec 集成 | 变更存储 | 分发方式 |
|------|--------------|---------|---------|
| **OpenSpec** | 自身 | 用户项目 | npm CLI |
| **Superpowers** | ❌ 无 | 用户项目 | npm marketplace |
| **Aria (v1)** | ✅ 深度绑定 | ❌ 混淆 | Git submodule |
| **Aria (v2)** | ✅ 深度绑定 | ✅ 分离 | Git submodule |

### 关键洞察

**Superpowers 不需要 OpenSpec**，因为:
- 工作流是 "brainstorm → plan → execute"
- 强调灵活性和迭代
- 无需严格的需求追溯

**Aria 必须 OpenSpec**，因为:
- 工作流是 "Phase A (规范) → Phase B (开发) → ..."
- 核心价值是可追溯性和规范性
- AI-DDD 方法论的基石

**因此**: Aria 不能简单地模仿 Superpowers 的去中心化模式。
相反，Aria 应该:
1. 保持与 OpenSpec 的深度绑定
2. 明确"方法论定义"与"项目变更"的边界
3. 借鉴 OpenSpec 的 CLI 分发模式 (长期)

---

## 决策建议

### 立即执行 (Phase 1 + 2)
- [ ] 移动 `backend-api-development` 到 `examples/user-projects/`
- [ ] 移动 `complete-requirements-chain` 到 `examples/user-projects/`
- [ ] 更新 `standards/openspec/README.md`
- [ ] 更新 `docs/architecture/system-architecture.md`
- [ ] 更新 `CLAUDE.md` 不可协商规则

### 考虑 (Phase 3)
- [ ] 评估 CLI 工具模式的可行性
- [ ] 设计 pre-commit hook 防护
- [ ] 收集用户反馈

---

## 结论

Aria 的核心价值在于 **"规范驱动的 AI 协作"**，这决定了它必须使用 OpenSpec。
但当前架构混淆了"方法论定义"和"项目变更"的边界。

解决方案不是放弃 OpenSpec (像 Superpowers)，而是：
1. **明确边界**: aria-standards 只存方法论，用户项目存变更
2. **强化文档**: 在关键位置添加使用说明
3. **长期演进**: 考虑 CLI 工具模式

---

**维护**: 10CG Lab
**相关**: [Superpowers](https://github.com/obra/superpowers) | [OpenSpec](https://github.com/Fission-AI/OpenSpec)
