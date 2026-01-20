# Enforcement Mechanism Redesign

> **Level**: Full (Level 3 Spec)
> **Status**: Draft
> **Created**: 2026-01-20
> **Updated**: 2026-01-20
> **Reference**: [Superpowers](https://github.com/obra/superpowers)

---

## Why

### 核心问题：双重隔离需求

Aria 目前实现了子代理驱动开发 (SDD) 和 Git Worktrees 隔离开发，但这两个特性是**可选**而非**强制执行**的。这导致：

1. **子代理复用污染上下文** - 同一子代理处理多个任务会累积上下文，影响专注度
2. **任务间代码审查缺失** - 传统做法是在所有任务完成后才审查，无法及时发现和修复问题
3. **文件系统隔离不足** - 缺少强制的 worktree 使用规范和验证

### 核心洞察：两种隔离是正交的

```
┌─────────────────────────────────────────────────────────────┐
│                    双重隔离需求                              │
├─────────────────────────────────────────────────────────────┤
│                                                                  │
│  文件系统隔离            上下文隔离                     │
│  ┌─────────────┐        ┌─────────────┐                        │
│  │ Worktree    │        │ Subagent    │                        │
│  │ - 物理目录   │        │ - AI 上下文  │                        │
│  │ - Git 引用   │        │ - 任务专注  │                        │
│  │ - 并行开发   │        │ - 代码审查  │                        │
│  └─────────────┘        └─────────────┘                        │
│         │                      │                               │
│         └──────────┬───────────┘                                │
│                    │                                            │
│                    ▼                                            │
│           ┌───────────────┐                                     │
│           │ 完全隔离开发  │  ← Aria 目标                        │
│           └───────────────┘                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────┘

关键: 这两个隔离机制是**正交但互补**的，不应混淆绑定
```

### 传统分支管理 vs AI 需求的差异

| 需求类型 | 传统方案 | AI 特有需求 |
|----------|----------|-------------|
| **代码隔离** | git branch | ✅ worktree 增强隔离 |
| **并行开发** | git branch (切换麻烦) | ✅ worktree 天然支持 |
| **协作审查** | GitHub PR | ⚠️ PR 平台解决 |
| **历史追溯** | git log | ✅ worktree 不影响 |
| **上下文隔离** | ❌ 不适用 | ✅ **只有 subagent 解决** |
| **任务专注度** | ❌ 不适用 | ✅ **只有 subagent 解决** |
| **任务间审查** | ❌ 不适用 | ✅ **只有 subagent 解决** |

**结论**: Worktree 解决传统需求（文件隔离），Subagent 解决 AI 特有需求（上下文隔离）。两者应分离但可组合。

---

## What

重写 Aria 的执行机制，采用**单一入口原则**，增强现有 branch-manager，新增两个核心技能：

### 核心变更

| 技能 | 类型 | 说明 |
|------|------|------|
| **branch-manager** | 增强 | 统一工作环境入口，内部选择常规分支或 worktree |
| **subagent-driver** | 新增 | 实现 SDD 工作流，每个任务使用全新子代理 |
| **branch-finisher** | 新增 | 完成分支时的验证和清理流程 |

### 架构决策

#### 决策 1: 单一入口原则

```
❌ 错误方案: 两个独立技能
  worktree-manager → 只能创建 worktree
  branch-manager   → 只能创建常规分支
  → 用户需要选择，AI 需要判断，复杂度高

✅ 正确方案: 统一入口，内部决策
  branch-manager (增强)
    ├─ 模式 A: 常规分支 (简单任务)
    └─ 模式 B: Worktree (复杂任务)
    → 用户只说"开始开发"，AI 自动选择模式
```

#### 决策 2: 渐进式复杂度

```
Level 1: 直接修改
  → 无 Git 追踪，文档 typo

Level 2: 常规分支
  → branch-manager 模式 A
  → 简单 bugfix，小功能

Level 3: Worktree 隔离
  → branch-manager 模式 B
  → 中等功能，需要保持主分支干净

Level 4: Worktree + Subagent
  → branch-manager → subagent-driver → branch-finisher
  → 复杂功能，架构重构
```

#### 决策 3: 职责分离

| 技能 | 职责 | 不负责 |
|------|------|--------|
| **branch-manager** | 工作环境创建、分支生命周期 | Subagent 调用、任务分发 |
| **subagent-driver** | 任务执行、上下文隔离、代码审查 | Git 操作、Worktree 创建 |
| **branch-finisher** | 完成验证、清理决策 | 任务执行逻辑 |

### 工作流链示意图

```
┌─────────────────────────────────────────────────────────────┐
│                    Aria 隔离技能体系                          │
└─────────────────────────────────────────────────────────────┘

                    branch-manager (增强)
                    ┌─────────────────────┐
                    │  B.1 工作环境创建    │
                    │  - 自动模式选择      │
                    │  - 常规 │ worktree │
                    │  - .gitignore 验证  │
                    │  - 环境检查         │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                              ▼
        subagent-driver                  branch-finisher
        ┌──────────────────┐              ┌──────────────────┐
        │ B.2 任务执行      │              │ C.2 完成          │
        │ - Fresh subagent │              │ - 测试验证        │
        │ - 任务间审查      │              │ - 4选项          │
        │ - 进度跟踪        │              │ - worktree清理   │
        └──────────────────┘              └──────────────────┘
```

---

## 1. branch-manager 技能规范 (增强)

### 1.1 核心职责

```yaml
单一入口:
  - 为开发任务创建合适的工作环境
  - 管理分支生命周期
  - 处理 PR 和合并

内部模式:
  - 模式 A: 常规分支 (git checkout -b)
  - 模式 B: Worktree (git worktree add)
```

### 1.2 模式决策逻辑

```yaml
auto_mode_decision:
  评分因素:
    file_count:
      1-3:     → branch (0分)
      4-10:    → worktree (+1)
      10+:     → worktree (+3)

    cross_directory:
      no:      → branch (0分)
      yes:     → worktree (+2)

    task_count:
      1-3:     → branch (0分)
      4-8:     → worktree (+1)
      8+:      → worktree (+3)

    risk_level:
      low:     → branch (0分)
      medium:  → worktree (+1)
      high:    → worktree (+3)

    parallel_needed:
      no:      → branch (0分)
      yes:     → worktree (+5)  # 必须用 worktree

  阈值: 3分
    score >= 3 → worktree
    score < 3  → branch
```

### 1.3 模式 A: 常规分支

```yaml
操作流程:
  1. 验证工作目录干净 (或 stash)
  2. git checkout -b {branch_name}
  3. git push -u origin {branch_name}

适用场景:
  - 简单 bugfix
  - 小功能开发
  - 单文件修改

输出:
  { mode: "branch", branch_name: "...", cleanup_required: false }
```

### 1.4 模式 B: Worktree

```yaml
操作流程:
  1. 目录优先级选择
     .worktrees/ > worktrees/ > CLAUDE.md > 询问

  2. .gitignore 强制验证
     - 检查是否包含 .worktrees/ 和 worktrees/
     - 缺失 → 立即修复 (不询问)

  3. 环境验证
     - npm install / cargo build / pnpm install
     - 测试基线检查

  4. 创建 worktree
     git worktree add -b {branch_name} {directory}

适用场景:
  - 中大型功能
  - 跨目录开发
  - 需要保持主分支可用
  - 并行开发多个功能

输出:
  {
    mode: "worktree",
    worktree_path: "../{feature}",
    branch_name: "...",
    cleanup_required: true
  }
```

### 1.5 输入参数

```yaml
mode: auto | branch | worktree  # 新增
    auto:    自动选择 (默认)
    branch:  强制使用常规分支
    worktree: 强制使用 worktree

base_branch: develop
feature_name: oauth-refactor
directory: ../worktrees       # worktree 目录 (仅 worktree 模式)
verify_env: true
```

### 1.6 Red Flags

```
永远不要:
  - 在 .gitignore 缺失时继续创建 worktree
  - 在测试失败时创建 worktree
  - 强制用户选择模式（让 auto 决定，用户可覆盖）
  - 同时管理多个 worktree（用户自己决定）
```

---

## 2. subagent-driver 技能规范

### 2.1 核心原则

```yaml
Fresh Subagent 规则:
  - 每个任务使用全新的子代理
  - 不复用之前的子代理
  - 理由: 避免上下文污染，保持专注

公告模式:
  - 开始时: "I'm using the subagent-driven-development skill"
  - 每任务: "Dispatching fresh subagent for TASK-{NNN}"
```

### 2.2 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│                     Subagent-Driven Development             │
└─────────────────────────────────────────────────────────────┘

  1. 接收工作环境信息
     └─ from branch-manager: { mode, worktree_path, branch_name }

  2. 加载计划
     └─ 读取 detailed-tasks.yaml 或 tasks.md

  3. 创建 TodoWrite
     └─ 将任务转换为可跟踪的 checklist

  4. 逐任务执行
     │
     ├─▶ Dispatch FRESH subagent
     │   └─ 每次使用 Task(subagent_type="xxx")
     │
     ├─▶ Subagent 执行
     │   └─ 完成后返回
     │
     ├─▶ 代码审查 (关键!)
     │   └─ 检查代码质量、测试覆盖
     │
     ├─▶ 发现 Critical 问题?
     │   ├─ Yes → 立即修复，重新审查
     │   └─ No → 标记任务完成
     │
     └─▶ 继续下一个任务

  5. 所有任务完成后
     └─ 最终审查

  6. REQUIRED 调用 branch-finisher
     └─ 不跳过，不询问
```

### 2.3 问题优先级

| 级别 | 含义 | 处理方式 |
|------|------|----------|
| **Critical** | 必须立即修复 | 阻塞下一个任务 |
| **Major** | 应该修复 | 记录，继续，最终审查前修复 |
| **Minor** | 可选优化 | 建议记录 |

### 2.4 Red Flags

```
永不执行:
  - 复用之前的子代理处理新任务
  - 跳过任务间代码审查
  - 在 Critical 问题未修复时继续下一个任务
  - 跳过 branch-finisher 调用
```

### 2.5 与 branch-manager 的协作

```yaml
输入来源:
  - 接收 branch-manager 的输出
  - worktree_path: 如果是 worktree 模式，在指定目录执行
  - mode: 影响是否需要清理

输出去向:
  - 将执行摘要传递给 branch-finisher
  - worktree_path 用于清理决策
```

---

## 3. branch-finisher 技能规范

### 3.1 验证前置条件

```yaml
选项前验证:
  - [ ] 运行完整测试套件
  - [ ] 所有测试通过
  - [ ] 代码审查无 Critical 问题
```

### 3.2 四选项流程

```
╔══════════════════════════════════════════════════════════════╗
║                    分支完成选项                                ║
╠══════════════════════════════════════════════════════════════╣
║                                                                ║
║  [1] Merge to target branch    - 合并到目标分支               ║
║  [2] Create Pull Request       - 创建 PR 等待审批             ║
║  [3] Keep working              - 继续在此分支工作             ║
║  [4] Discard changes           - 丢弃变更                     ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝
```

### 3.3 Worktree 清理规则

```yaml
需要清理 worktree:
  - 选项 [1] (Merge): 删除 worktree
  - 选项 [4] (Discard): 删除 worktree
  - 选项 [2] (PR): 保留，等待 PR 合并
  - 选项 [3] (Keep): 保留

清理命令:
  git worktree remove {worktree_path}
```

### 3.4 输入参数

```yaml
worktree_path: string | null  # 来自 branch-manager
mode: "branch" | "worktree"   # 来自 branch-manager
test_required: true           # 是否要求测试通过
execution_summary: object     # 来自 subagent-driver
```

---

## 4. 现有技能集成

### 4.1 更新 phase-b-developer

```yaml
phase-b-developer (更新):
  B.1: branch-manager (增强版)
    → 内部自动选择模式
    → 返回工作环境信息

  B.2: subagent-driver
    → 接收 B.1 的输出
    → 在工作环境中执行任务

  B.3: 架构同步 (保留)
```

### 4.2 更新 phase-c-integrator

```yaml
phase-c-integrator (更新):
  C.1: commit-msg-generator (保留)

  C.2: branch-finisher
    → 接收 worktree_path
    → 验证测试
    → 4选项完成
    → 清理 worktree
```

### 4.3 文档规范

所有相关技能添加章节:
- **Red Flags**: 永不执行的操作
- **Common Mistakes**: 常见错误及避免方法
- **Integration**: 与其他技能的协作
- **职责边界**: 负责 vs 不负责

---

## 5. 渐进式隔离策略

```
┌─────────────────────────────────────────────────────────────┐
│                    决策树                                    │
└─────────────────────────────────────────────────────────────┘

用户发起开发任务
        │
        ▼
   是否需要 Git 追踪?
        │
   ┌────┴────┐
   │ No      │ Yes
   ▼         ▼
直接修改   branch-manager (auto 模式)
         │
         ▼
    内部分数 < 3?
         │
    ┌────┴────┐
    │ Yes     │ No
    ▼         ▼
  常规分支   Worktree
         │
         ▼
   是否需要任务间审查?
         │
    ┌────┴────┐
    │ No      │ Yes
    ▼         ▼
  手动开发   subagent-driver
             │
             ▼
        branch-finisher
```

### 完整工作流示例

#### 场景 1: 简单 Bugfix

```
用户: "修复登录页面的 typo"

branch-manager (auto):
  分析: 文件数=1, 复杂度=S, 风险=低
  评分: 0分
  决策: 常规分支模式

执行:
  1. git checkout -b fix/typo
  2. [手动修复]
  3. git commit
  4. 无需 subagent-driver, 无需 branch-finisher
```

#### 场景 2: 中等功能

```
用户: "添加用户资料编辑功能"

branch-manager (auto):
  分析: 文件数=5, 跨目录=是, 任务数=3
  评分: 3分
  决策: Worktree 模式

执行:
  1. branch-manager 创建 worktree
  2. [手动开发]
  3. branch-finisher 完成
```

#### 场景 3: 复杂功能

```
用户: "重构认证系统，添加 OAuth 支持"

branch-manager (auto):
  分析: 文件数=15+, 跨模块=是, 任务数=10+, 风险=高
  评分: 12分
  决策: Worktree 模式

执行:
  1. branch-manager 创建 worktree
  2. subagent-driver 执行任务
     → 逐任务 fresh subagent
     → 任务间代码审查
  3. branch-finisher 完成
```

---

## 6. Superpowers 设计模式借鉴

| 模式 | 来源 | 应用 |
|------|------|------|
| **Fresh subagent per task** | subagent-driven-development | 每任务新子代理 |
| **Code review BETWEEN tasks** | subagent-driven-development | 任务间审查 |
| **Directory priority** | using-git-worktrees | 优先级选择 |
| **Fix immediately if missing** | using-git-worktrees | .gitignore 缺失立即修复 |
| **4-option completion** | finishing-a-development-branch | 合并/PR/保留/丢弃 |
| **Announcement pattern** | 多个技能 | "I'm using the X skill..." |
| **Single entry point** | Aria 设计 | **branch-manager 统一入口** |

---

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 单一入口简化使用，渐进式复杂度，双重隔离质量保证 |
| **Risk** | branch-manager 增加复杂度 | 缓解: 内部自动决策，用户无需关心细节 |

---

## Key Deliverables

```
.claude/skills/
├── branch-manager/ (增强)
│   ├── SKILL.md (重写)
│   │   ├── 模式决策逻辑
│   │   ├── 常规分支模式
│   │   └── Worktree 模式
│   ├── hooks.json (更新)
│   └── scripts/
│       ├── worktree-create.sh
│       └── worktree-cleanup.sh
├── subagent-driver/ (新增)
│   ├── SKILL.md
│   └── tasks-template.md
├── branch-finisher/ (新增)
│   └── SKILL.md
└── (existing skills updated)
    ├── phase-b-developer/
    ├── phase-c-integrator/
    └── strategic-commit-orchestrator/

.claude/agents/
└── AGENTS_ARCHITECTURE.md (更新 SDD 模式)

docs/
└── analysis/
    ├── superpowers-vs-aria.md (对比)
    └── dual-isolation-strategy.md (双重隔离策略)
```

---

## Success Criteria

- [ ] branch-manager 自动选择常规分支或 worktree 模式
- [ ] branch-manager .gitignore 强制验证和自动修复
- [ ] subagent-driver 每任务使用全新子代理
- [ ] subagent-driver 在任务间执行代码审查
- [ ] branch-finisher 验证测试后显示 4 选项
- [ ] branch-finisher 正确清理 worktree
- [ ] 所有技能包含 Red Flags 和职责边界章节
- [ ] 与现有 tdd-enforcer 无冲突
- [ ] 渐进式复杂度策略文档完整

---

## References

- [Superpowers - subagent-driven-development](https://github.com/obra/superpowers/tree/main/skills/subagent-driven-development)
- [Superpowers - using-git-worktrees](https://github.com/obra/superpowers/tree/main/skills/using-git-worktrees)
- [Superpowers - finishing-a-development-branch](https://github.com/obra/superpowers/tree/main/skills/finishing-a-development-branch)
- [Aria TDD Enforcer](.claude/skills/tdd-enforcer/SKILL.md)
- [Aria Agents Architecture](.claude/agents/AGENTS_ARCHITECTURE.md)
- [Aria System Architecture](docs/architecture/system-architecture.md)

---

**Maintained By**: 10CG Lab
**Spec Level**: Full (Level 3)
**Estimate**: 16-24h
**Version**: 2.0 (单一入口架构)
