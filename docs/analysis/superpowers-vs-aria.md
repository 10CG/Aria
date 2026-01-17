# Superpowers vs Aria 深度对比分析与优化建议

> 基于 obra/superpowers (GitHub 27k stars) 与 Aria 项目的深度架构对比
> 分析日期: 2026-01-17

---

## 一、核心架构对比

| 维度 | Superpowers | Aria |
|------|-------------|------|
| **仓库结构** | 单一 monorepo | 3个独立子模块 (standards/agents/skills) |
| **技能数量** | 12个核心技能 | 20个技能 |
| **Agents** | 1个专用（code-reviewer） | 10个专用 agents |
| **工作流** | 7步线性工作流 | 10步循环 (Phase A-D) |
| **核心理念** | TDD、YAGNI、DRY | AI-DDD v3.0、OpenSpec |
| **社区规模** | 27k stars, 2k forks | 初始阶段 |

---

## 二、Superpowers 完整技能清单

### 技能目录结构
```
skills/
├── brainstorming/              # 交互式设计细化
├── dispatching-parallel-agents/ # 并发子代理工作流
├── executing-plans/            # 批量执行与检查点
├── finishing-a-development-branch/  # 分支收尾工作流
├── receiving-code-review/      # 响应代码审查反馈
├── requesting-code-review/     # 代码审查请求
├── subagent-driven-development/# 子代理驱动开发（两阶段评审）
├── systematic-debugging/       # 系统性调试方法
├── test-driven-development/    # RED-GREEN-REFACTOR
├── using-git-worktrees/        # Git Worktrees 隔离开发
├── using-superpowers/          # 系统介绍
├── verification-before-completion/ # 完成前验证
└── writing-plans/              # 详细实现计划编写
```

### Hooks 系统
```
hooks/
├── hooks.json          # Hook 配置定义
├── run-hook.cmd        # Windows 包装器
└── session-start.sh    # Session 启动 hook
```

---

## 三、Superpowers 的关键优势

### 1. 简单而有效的自动触发机制

```
用户请求 → 检测任务类型 → 自动激活相关技能 → 执行
```

| 触发条件 | 自动激活技能 |
|----------|--------------|
| 开始编码任务 | `brainstorming` |
| 设计完成后 | `writing-plans` |
| 有执行计划 | `subagent-driven-development` 或 `executing-plans` |
| 实现过程中 | `test-driven-development` |
| 任务之间 | `requesting-code-review` |

### 2. Git Worktrees 隔离开发

```bash
# Superpowers 的做法
git worktree add ../project-task-123 feature/task-123
cd ../project-task-123
# 在隔离环境中开发
# 完成后删除 worktree
```

**优势：**
- 主分支保持干净
- 支持并行多任务开发
- 失败不影响主工作区

### 3. 两阶段评审机制

```
阶段1: 规范合规性检查
       ↓
       该实现是否符合 detailed-tasks.yaml 的规范？
       ↓
阶段2: 代码质量检查
       ↓
       代码是否高质量？测试是否充分？
```

### 4. "强制"工作流而非建议

> "The agent checks for relevant skills before any task. **Mandatory workflows, not suggestions.**"

Superpowers 通过以下机制强制执行：
- 技能描述中的明确触发条件
- Hook 系统在关键节点拦截
- Agent 系统中的权限控制

### 5. TDD 强制执行

```yaml
# test-driven-development skill 核心流程:
1. RED:   写失败的测试
2. GREEN: 写最少的代码让测试通过
3. REFACTOR: 重构代码
4. 删除在测试之前写的代码
```

---

## 四、Aria 的独特优势

### 1. 更完善的企业级特性

| 特性 | Aria | Superpowers |
|------|------|-------------|
| 规范管理 | OpenSpec 系统 | 无 |
| 进度追踪 | UPM (Unified Progress Management) | 无 |
| 外部集成 | Forgejo (Issue/PR/Wiki) | 无 |
| 架构文档 | L0/L1/L2 三级体系 | 无 |

### 2. 架构文档系统

```
arch-common (共享配置)
    ├── L0: 系统整体架构
    ├── L1: 子系统架构
    └── L2: 模块详细设计

arch-search (智能搜索)
    ├── DOMAIN 映射
    ├── 多语言关键词
    └── 节省 70% Token 消耗

arch-update (自动同步)
    ├── 代码变更检测
    ├── 文档自动更新
    └── 100% 同步保证
```

### 3. 更细粒度的任务分解

```yaml
# Aria 双层任务架构
tasks.md:
  - 粗粒度任务列表
  - 人类可读

detailed-tasks.yaml:
  - 细粒度任务步骤
  - Agent 可执行
  - 包含: parent, complexity, dependencies
```

### 4. 多语言支持

```
Aria: 中英文双语关键词触发
arch-search:
  - "架构" → architecture
  - "接口" → API
  - "数据库" → database
```

---

## 五、Aria 可以借鉴的优化建议

### 🔥 高优先级

#### 1. 增强 TDD 强制执行

```
当前状态: 测试是可选步骤
目标状态: RED-GREEN-REFACTOR 是强制的
```

**实现建议：**

```yaml
# 新增 skill: aria-tdd-enforcer
name: tdd-enforcer
description: |
  强制执行测试驱动开发流程。
  激活条件: 开始编写实现代码时

allowed-tools:
  - Bash
  - Read
  - Edit

workflow:
  1. 检查是否已存在测试文件
  2. 如果没有，拒绝编写实现代码
  3. 要求先写失败的测试 (RED)
  4. 验证测试确实失败
  5. 允许编写实现代码 (GREEN)
  6. 验证测试通过
  7. 允许重构 (REFACTOR)
```

#### 2. 实现 Git Worktrees 支持

```
当前状态: 直接在主分支开发
目标状态: 每个任务在独立 worktree
```

**实现建议：**

```yaml
# 修改 phase-b-developer skill
# 在 B.1 (分支创建) 步骤添加:

steps:
  B.1:
    - name: "创建隔离工作环境"
      actions:
        - |
          # 使用 worktree 替代直接分支切换
          TASK_ID=$(date +%s)
          WORKTREE_PATH="../aria-task-${TASK_ID}"

          if git worktree list | grep -q "$WORKTREE_PATH"; then
            echo "Worktree 已存在"
          else
            git worktree add "$WORKTREE_PATH" -b "task/${TASK_ID}"
          fi

          cd "$WORKTREE_PATH"
          echo "工作目录: $(pwd)"
```

**优势：**
- 主工作区不受影响
- 可同时处理多个任务
- 失败可快速清理

#### 3. 简化工作流触发

```
当前状态: 需要用户显式调用 /state-scanner
目标状态: 自动检测并触发
```

**实现建议：**

```markdown
# 创建 .claude/CLAUDE.md

## Aria 自动触发规则

### 开发新功能
用户意图关键词: "开发", "实现", "添加功能"
→ 自动激活: spec-drafter

### 修复 Bug
用户意图关键词: "修复", "bug", "不工作"
→ 自动激活: systematic-debugging

### 提交代码
用户意图关键词: "提交", "commit"
→ 自动激活: strategic-commit-orchestrator

### 查看架构
用户意图关键词: "架构", "在哪里", "如何实现"
→ 自动激活: arch-search

### 创建分支
用户意图关键词: "新任务", "开始工作"
→ 自动激活: branch-manager (使用 worktree)
```

### 🟡 中优先级

#### 4. 添加两阶段评审机制

```yaml
# 在 phase-b-developer 每个子任务后添加:

review:
  phase1:
    name: "规范合规性检查"
    checks:
      - 是否符合 detailed-tasks.yaml 规范
      - 文件路径是否正确
      - 实现是否完整
    block_on_failure: true

  phase2:
    name: "代码质量检查"
    checks:
      - 代码是否符合风格指南
      - 测试覆盖率是否充足
      - 文档是否完整
      - 是否有安全漏洞
    block_on_failure: false  # 警告但不阻塞
```

#### 5. 实现完整的 Hooks 系统

```bash
# 创建 aria/hooks/
# 目录结构:
aria/
└── hooks/
    ├── hooks.json          # Hook 定义
    ├── session-start.sh    # 会话启动时执行
    ├── pre-commit.sh       # 提交前验证
    ├── post-commit.sh      # 提交后处理
    └── task-complete.sh    # 任务完成检查
```

**hooks.json 示例：**

```json
{
  "version": "1.0",
  "hooks": {
    "SessionStart": {
      "command": "session-start.sh",
      "description": "会话初始化检查",
      "actions": [
        "检查子模块状态",
        "验证 Git 状态",
        "加载项目上下文"
      ]
    },
    "PreCommit": {
      "command": "pre-commit.sh",
      "description": "提交前验证",
      "actions": [
        "运行测试",
        "检查代码风格",
        "验证架构文档同步"
      ]
    }
  }
}
```

#### 6. 简化技能目录结构

```
当前结构:
claude/skills/
├── arch-common/
├── arch-search/
├── arch-update/
├── arch-scaffolder/
├── commit-msg-generator/
├── strategic-commit-orchestrator/
├── branch-manager/
├── phase-a-planner/
├── phase-b-developer/
├── phase-c-integrator/
├── phase-d-closer/
├── requirements-validator/
├── requirements-sync/
├── forgejo-sync/
├── progress-updater/
├── spec-drafter/
├── task-planner/
├── api-doc-generator/
├── state-scanner/
└── workflow-runner/

建议结构:
claude/skills/
├── core/
│   ├── state-scanner/
│   └── workflow-runner/
├── architecture/           # 合并 4 个架构技能
│   ├── search/
│   ├── update/
│   ├── scaffolder/
│   └── common/
├── development/
│   ├── tdd-enforcer/       # 新增
│   ├── phase-a/
│   ├── phase-b/
│   ├── phase-c/
│   └── phase-d/
├── git/
│   ├── commit/
│   ├── branch/
│   └── orchestrate/
├── requirements/
│   ├── validator/
│   ├── sync/
│   └── forgejo/
└── docs/
    ├── spec/
    ├── task/
    ├── progress/
    └── api/
```

### 🔵 低优先级

#### 7. 添加 YAGNI 原则检查

```yaml
# 新技能: yagni-validator

name: yagni-validator
description: |
  You Aren't Gonna Need It - 检测过度设计

checks:
  - name: "过度抽象"
    pattern: "为单一用途创建接口或基类"
    suggestion: "先实现具体类，需要时再抽象"

  - name: "过早优化"
    pattern: "在性能问题出现前进行优化"
    suggestion: "先让代码工作，再优化"

  - name: "未来需求"
    pattern: "实现可能永远用不到的功能"
    suggestion: "YAGNI - 只实现当前需要的功能"
```

#### 8. 改进 Agent 继承机制

```
Superpowers 实现: "fix: inherit agent model"
Aria 当前: 每个独立 agent 配置

建议: 添加 agent 继承
```

```yaml
# agents/backend-architect.md
---
extends: tech-lead
model: opus  # 覆盖父级模型
specialization:
  - backend architecture
  - API design
  - database design
---

# Backend Architect Agent 继承 Tech Lead 的基础配置...
```

#### 9. 添加 Brainstorming 技能

```yaml
# 新技能: brainstorming

name: brainstorming
description: |
  交互式设计细化 - 通过苏格拉底式提问澄清需求

activation:
  - 用户开始新功能开发
  - 需求不明确

process:
  1. 询问核心目标
  2. 探索替代方案
  3. 分段展示设计（可理解的块）
  4. 获取确认
  5. 生成设计文档
```

---

## 六、建议的 Aria v3.1 改进路线图

```
阶段1 (立即执行 - 1周内)
├── 添加 tdd-enforcer skill
├── 修复 state-scanner 自动触发
└── 创建 .claude/CLAUDE.md 触发规则

阶段2 (短期 - 1个月内)
├── 实现 git-worktree 支持
├── 添加两阶段评审机制
├── 创建 session-start hook
└── 优化技能目录结构

阶段3 (中期 - 3个月内)
├── 添加 brainstorming skill
├── 实现 yagni-validator
├── 完善 hooks 系统
└── 添加 agent 继承机制

阶段4 (长期 - 持续改进)
├── 集成外部工具 (Context7, DeepWiki)
├── 性能优化
└── 社区反馈迭代
```

---

## 七、总结

### Superpowers 胜在

1. **简单直接** - 7步线性工作流易于理解和执行
2. **强制最佳实践** - TDD、YAGNI、DRY 不是建议而是要求
3. **完善的 Hooks** - 在关键节点自动拦截和验证
4. **自动触发** - 无需用户记住调用命令
5. **Worktrees 隔离** - 干净的并行开发环境
6. **两阶段评审** - 规范 → 质量的递进式检查

### Aria 胜在

1. **企业级方法论** - 完整的 AI-DDD v3.0 框架
2. **架构文档系统** - L0/L1/L2 分层 + 智能搜索 + 自动同步
3. **需求追踪** - OpenSpec + UPM 完整链路
4. **外部集成** - Forgejo Issue/PR/Wiki 同步
5. **模块化架构** - 独立子模块便于维护和扩展
6. **多语言支持** - 中英文双语触发

### 最终建议

**Aria 应保持其企业级优势**，同时借鉴 Superpowers 的简洁性和强制最佳实践，形成：

> **"Superpowers 的简单直接 + Aria 的完整体系"**

的混合优势，打造更适合企业级 AI 辅助开发的完整解决方案。

---

## 附录：Superpowers 完整工作流

```
┌─────────────────────────────────────────────────────────────┐
│                    Superpowers 工作流                        │
└─────────────────────────────────────────────────────────────┘

1. BRAINSTORMING (触发: 开始新功能)
   ├─ 苏格拉底式提问
   ├─ 探索替代方案
   ├─ 分段展示设计
   └─ 保存设计文档

2. USING-GIT-WORKTREES (触发: 设计完成)
   ├─ 创建独立 worktree
   ├─ 运行项目 setup
   └─ 验证测试基线

3. WRITING-PLANS (触发: 有设计文档)
   ├─ 分解为 2-5 分钟任务
   ├─ 每任务包含:
   │  ├─ 精确文件路径
   │  ├─ 完整代码
   │  └─ 验证步骤
   └─ 生成 detailed-tasks.yaml

4. SUBAGENT-DRIVEN-DEVELOPMENT (触发: 有执行计划)
   ├─ 为每个任务分配新 subagent
   ├─ 两阶段评审:
   │  ├─ 阶段1: 规范合规性
   │  └─ 阶段2: 代码质量
   └─ 持续推进直到完成

5. TEST-DRIVEN-DEVELOPMENT (触发: 实现过程中)
   ├─ RED: 写失败测试
   ├─ GREEN: 写最少代码
   ├─ REFACTOR: 重构
   └─ 删除测试前的代码

6. REQUESTING-CODE-REVIEW (触发: 任务间)
   ├─ 对照计划审查
   ├─ 按严重程度报告问题
   └─ 关键问题阻塞进度

7. FINISHING-A-DEVELOPMENT-BRANCH (触发: 所有任务完成)
   ├─ 验证测试
   ├─ 展示选项 (merge/PR/keep/discard)
   └─ 清理 worktree
```

---

*文档生成: Claude Opus 4.5*
*分析基于: obra/superpowers@main (2026-01-17)*
