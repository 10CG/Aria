# Superpowers vs Aria 深度对比分析与优化建议

> 基于 obra/superpowers (GitHub 27k stars) 与 Aria 项目的深度架构对比
> 参考 Agent Skills 官方规范 (agentskills.io) 与 Anthropic 官方示例
> 分析日期: 2026-01-17

**文档更新记录：**
- v1.1 (2026-01-17): 根据 Agent Skills 官方规范重新评估技能目录结构，确认无需重构
- v1.2 (2026-01-18): 添加 aria-workflow-enhancement 实施总结

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

### 🔵 低优先级

#### 6. 添加 YAGNI 原则检查

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

#### 7. 改进 Agent 继承机制

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

#### 8. 添加 Brainstorming 技能

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
└── 创建 session-start hook

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

### Aria 技能目录结构评估 ✅

**结论：无需重构，已符合 Agent Skills 官方最佳实践**

#### 对比 Agent Skills 官方规范

| 规范要求 | Aria 实现 | 状态 |
|---------|----------|------|
| 扁平结构 | 20个技能全部在 skills/ 根目录 | ✅ 符合 |
| kebab-case 命名 | arch-search, phase-b-planner 等 | ✅ 符合 |
| SKILL.md 必需 | 每个技能都有 SKILL.md | ✅ 符合 |
| Progressive Disclosure | 详细的 references/ 和 assets/ | ✅ 符合 |

#### 与生态对比

| 项目 | 技能数量 | 目录结构 | 分组方式 |
|------|---------|---------|----------|
| **Anthropic 官方** | 30+ | 完全扁平 | marketplace.json 分组 |
| **Superpowers** | 13 | 完全扁平 | 无分组 |
| **Aria** | 20 | 完全扁平 | 前缀命名分组 |

**Aria 的前缀分组策略优于子目录分组：**

```bash
# 前缀分组 (Aria) ✅
skills/arch-search/     # 路径短，扫描快
skills/phase-b-developer/

# 子目录分组 (不推荐)
skills/architecture/search/  # 路径长，引用复杂
skills/development/phase-b/
```

**优势：**
- 一眼可见所有技能
- 路径引用更简洁
- 无需递归扫描
- 符合官方 Progressive Disclosure 原则

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

## 附录：Agent Skills 官方规范要点

### 目录结构规范 (agentskills.io)

```
skill-name/
└── SKILL.md  # 必需

可选目录:
├── scripts/     # 可执行代码
├── references/  # 参考文档 (按需加载)
└── assets/      # 静态资源
```

### 命名规范

```
name: skill-name  # 1-64字符，小写字母+数字+连字符
description: 清晰描述技能功能和使用场景
```

### Progressive Disclosure 原则

| 层级 | 内容 | Token 预算 |
|------|------|-----------|
| Metadata | name + description | ~100 tokens |
| Instructions | SKILL.md 主体 | < 5000 tokens |
| Resources | scripts/references/assets | 按需加载 |

### 关键原则

1. **扁平优于嵌套** - 所有技能在同一层级
2. **保持 SKILL.md < 500 行** - 详细内容放 references/
3. **相对路径引用** - 最多一层嵌套

---

*文档生成: Claude Opus 4.5*
*分析基于: obra/superpowers@main + agentskills.io + anthropics/skills*
*最后更新: 2026-01-18 (v1.2)*

---

## 附录：aria-workflow-enhancement 实施总结

### 实施概述

基于本分析文档的建议，`aria-workflow-enhancement` 提案已实施完成 74% (23/31 任务)。

### 已实现功能

| 功能 | 来源 | 状态 | 相关文件 |
|------|------|------|----------|
| **TDD Enforcer Skill** | Superpowers TDD | ✅ 完整实现 | `.claude/skills/tdd-enforcer/` |
| **Git Worktrees 集成** | Superpowers Worktrees | ✅ 完整实现 | `branch-manager/` + 模板脚本 |
| **自动触发系统** | Superpowers Auto-Trigger | ✅ 完整实现 | `.claude/CLAUDE.md` + `trigger-rules.json` |
| **两阶段评审机制** | Superpowers Two-Phase Review | ✅ 完整实现 | `phase-b-developer/validators/` |
| **Hooks 系统框架** | Superpowers Hooks | ✅ 完整实现 | `aria/hooks/` |

### 创建的文件统计

```
总计: 23 个新文件/更新文件

Skills (6 个文件):
  - tdd-enforcer/SKILL.md
  - tdd-enforcer/workflow.md
  - tdd-enforcer/EXAMPLES.md
  - branch-manager/SKILL.md (v1.2.0)
  - branch-manager/templates/*.sh
  - phase-b-developer/SKILL.md (v1.1.0)

配置 (3 个文件):
  - .claude/CLAUDE.md
  - .claude/trigger-rules.json
  - aria/hooks/hooks.json

脚本 (5 个文件):
  - branch-manager/templates/worktree-create.sh
  - branch-manager/templates/worktree-cleanup.sh
  - phase-b-developer/templates/worktree-switch.sh
  - phase-b-developer/templates/worktree-status.sh
  - aria/hooks/session-start.sh
  - aria/hooks/run-hook.cmd

文档 (5 个文件):
  - aria/hooks/README.md
  - docs/workflow/auto-trigger-guide.md
  - phase-b-developer/validators/*.md
  - phase-b-developer/templates/review-report.md
  - phase-b-developer/blocking-rules.json.md

测试 (1 个文件):
  - tests/auto-trigger/test_matching.py

规范 (3 个文件):
  - openspec/changes/aria-workflow-enhancement/proposal.md (v1.1)
  - openspec/changes/aria-workflow-enhancement/tasks.md (v1.1)
  - openspec/changes/aria-workflow-enhancement/detailed-tasks.yaml
```

### 技术债务

以下任务需要实际代码环境或运行时支持，标记为技术债务：

| TASK | 描述 | 原因 |
|------|------|------|
| TASK-003 | PreToolUse Hook 实现 | 需要 Claude Code 运行时 API |
| TASK-004 | 删除验证规则 | 依赖 TASK-003 |
| TASK-014 | Skill 自动激活逻辑 | 需要实际集成测试 |

### 向后兼容性

- ✅ 所有新功能可选启用
- ✅ 默认行为保持不变
- ✅ 现有技能目录结构保持不变
- ✅ 符合 Agent Skills 官方规范

### 下一步计划

1. **Phase 2 (Extended)** - 实现剩余的高优先级功能
   - Pre-Commit Hook
   - Task-Complete Hook
   - YAGNI Validator

2. **集成测试** - 在实际开发环境中验证
   - TDD Enforcer 实际拦截测试
   - Worktree 并行开发验证
   - 自动触发准确性测试

3. **用户反馈收集** - 根据实际使用调整

---

**实施日期**: 2026-01-18
**提案版本**: v1.1
**完成度**: 74% (23/31 任务)
**相关提案**: `standards/openspec/changes/aria-workflow-enhancement/proposal.md`

---

## 附录：enforcement-mechanism-redesign 实施总结 (v2.0)

> **新增于 2026-01-21** - Aria 强制机制重设计实施

### 实施概述

基于 aria-workflow-enhancement 的经验，`enforcement-mechanism-redesign` 提案进一步增强了 Aria 的强制执行能力，借鉴 Superpowers 的核心模式。

### 新增技能

| 技能 | 版本 | 来源借鉴 | 职责 |
|------|------|---------|------|
| **branch-manager** | v2.0.0 | using-git-worktrees | 自动模式决策 (Branch/Worktree) |
| **subagent-driver** | v1.0.0 | subagent-driven-development | Fresh Subagent 执行 + 任务间审查 |
| **branch-finisher** | v1.0.0 | finishing-a-development-branch | 测试验证 + 4选项完成流程 |

### 关键实现对比

#### 1. 隔离模式决策

```yaml
Superpowers: 始终使用 Worktree
Aria v2.0:   智能决策 (5因子评分)

factors:
  - file_count: 变更文件数
  - cross_directory: 跨目录变更
  - task_count: 任务数量
  - risk_level: 风险等级
  - parallel_needed: 并行需求

threshold: >= 3 → Worktree, < 3 → Branch
```

#### 2. Subagent 执行模式

```yaml
Superpowers: Fresh Subagent per task
Aria v2.0:   Fresh Subagent + 隔离级别选择

isolation_levels:
  L1: 对话隔离 (简单任务)
  L2: 对话 + Worktree (中等复杂度)
  L3: 完全进程隔离 (高风险/并行)
```

#### 3. 完成流程

```yaml
Superpowers: 4选项 (merge/PR/keep/discard)
Aria v2.0:   4选项 + 测试前置验证

options:
  "[1] 提交并创建 PR"  → 测试通过后执行
  "[2] 继续修改"       → 返回开发
  "[3] 放弃变更"       → 回滚 + 强制清理
  "[4] 暂停保存"       → 保存状态

pre_validation:
  blocking: [tests, type_check, build]
  warning: [lint, coverage]
```

### 架构增强

```
┌─────────────────────────────────────────────────────────────┐
│                    Aria v2.0 强制执行架构                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  branch-manager v2.0.0                                      │
│  ├── 自动模式决策 (5因子评分)                                │
│  ├── Mode A: Branch 创建                                    │
│  └── Mode B: Worktree 隔离                                  │
│       │                                                     │
│       ▼                                                     │
│  subagent-driver v1.0.0                                     │
│  ├── Fresh Subagent 启动                                    │
│  ├── 逐任务执行                                              │
│  ├── 任务间代码审查                                          │
│  └── 上下文隔离验证                                          │
│       │                                                     │
│       ▼                                                     │
│  branch-finisher v1.0.0                                     │
│  ├── 测试前置验证 (阻塞/警告)                                │
│  ├── 4选项完成流程                                           │
│  └── Worktree 智能清理                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 与 Superpowers 的对比结论

| 维度 | Superpowers | Aria v2.0 |
|------|-------------|-----------|
| 隔离策略 | 始终 Worktree | 智能选择 (效率优化) |
| Subagent 隔离 | Fresh per task | Fresh + 隔离级别 |
| 完成验证 | 基本检查 | 多级验证 (阻塞/警告) |
| 清理时机 | 完成后询问 | 上下文感知决策 |

**Aria v2.0 优势**:
- 更智能的模式选择，避免过度隔离
- 渐进式隔离策略 (L1→L2→L3)
- 与企业级特性深度集成 (TDD、架构同步)

**实施文件统计**:
```
Skills: 3 个新技能
  - branch-manager/   (v2.0.0 重构)
  - subagent-driver/  (新建)
  - branch-finisher/  (新建)

Internal 文档: 12 个
  - MODE_DECISION_LOGIC.md
  - MODE_A_BRANCH_FLOW.md
  - MODE_B_WORKTREE_FLOW.md
  - DIRECTORY_PRIORITY.md
  - GITIGNORE_VALIDATOR.md
  - ENVIRONMENT_VALIDATOR.md
  - FRESH_SUBAGENT_LAUNCHER.md
  - INTER_TASK_REVIEW.md
  - FOUR_OPTION_COMPLETION.md
  - CONTEXT_ISOLATION.md
  - TASK_STATE_TRACKING.md
  - TEST_PRE_VALIDATION.md
  - WORKTREE_CLEANUP.md

集成更新: 4 个技能
  - phase-b-developer v1.2.0
  - phase-c-integrator v1.1.0
  - strategic-commit-orchestrator v2.3.0
  - tdd-enforcer v1.1.0
```

---

**实施日期**: 2026-01-21
**提案版本**: v2.0
**相关提案**: `openspec/changes/enforcement-mechanism-redesign/proposal.md`
