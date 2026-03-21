# Aria vs Superpowers 对比分析

> **分析日期**: 2026-02-05
> **Aria 版本**: v1.0.0
> **Superpowers 版本**: v3.3.0
> **目的**: 通过对比分析，为 Aria 方法论提供优化建议

---

## 执行摘要

Superpowers 是 obra 开发的 Claude Code 插件框架，拥有 501+ GitHub Stars，专注于 TDD 强制执行和子代理驱动开发。Aria 是基于 AI-DDD 方法论的企业级工作流框架。

**核心发现**:
- Superpowers 的 TDD 执行更严格（RED-GREEN-REFACTOR 完整循环）
- Superpowers 有独特的 brainstorming 交互式设计能力
- Aria 在企业级功能（多模块、架构同步、需求追踪）方面更全面
- Aria 有更完整的方法论体系（AI-DDD + 十步循环 + OpenSpec）

---

## 一、项目概览对比

| 维度 | Aria | Superpowers |
|------|------|-------------|
| **版本** | v1.0.0 | v3.3.0 |
| **GitHub Stars** | N/A (私有仓库) | 501+ |
| **核心理念** | AI-DDD (AI辅助领域驱动设计) | TDD + 子代理驱动开发 |
| **Skills 数量** | 23 | ~30 |
| **Agents 数量** | 10 | 0 (使用 Fresh Subagent) |
| **Hooks** | 4 (3启用) | 3 (全部启用) |
| **文档语言** | 中文 | 英文 |
| **企业支持** | 多模块、架构同步、需求追踪 | 单项目导向 |

---

## 二、功能对比

### 2.1 Skills 对比

#### Aria Skills (23个)

**十步循环核心** (9个):
- `state-scanner` - 项目状态扫描与智能工作流推荐
- `workflow-runner` - 十步循环轻量编排器
- `phase-a-planner` - Phase A 规划阶段执行器
- `phase-b-developer` - Phase B 开发阶段执行器
- `phase-c-integrator` - Phase C 集成阶段执行器
- `phase-d-closer` - Phase D 收尾阶段执行器
- `spec-drafter` - 创建 OpenSpec proposal.md
- `task-planner` - 将 OpenSpec 分解为可执行任务
- `progress-updater` - 更新项目进度状态

**Git 工作流** (4个):
- `commit-msg-generator` - Conventional Commits 消息生成
- `strategic-commit-orchestrator` - 跨模块/批量/里程碑提交编排
- `branch-manager` - 分支创建与 PR 管理
- `branch-finisher` - 分支完成收尾

**开发工具** (3个):
- `subagent-driver` - 子代理驱动开发 (SDD)
- `agent-router` - 任务到 Agent 的智能路由器
- `tdd-enforcer` - 强制执行 TDD 工作流

**架构文档** (5个):
- `arch-common` - 架构工具共享组件
- `arch-search` - 搜索架构文档
- `arch-update` - 更新架构文档
- `arch-scaffolder` - 从 PRD 生成架构骨架
- `api-doc-generator` - API 文档生成

**需求管理** (3个):
- `requirements-validator` - PRD/Story/Architecture 验证
- `requirements-sync` - Story <-> UPM 状态同步
- `forgejo-sync` - Story <-> Issue 同步

#### Superpowers Skills

**TDD 核心**:
- `tdd-mode` - TDD 模式开关，启用 RED-GREEN-REFACTOR 循环
- `red-skill` - 编写失败测试
- `green-skill` - 最小代码通过测试
- `refactor-skill` - 重构代码

**开发流程**:
- `subagent-skill` - Fresh Subagent 驱动开发
- `code-review-skill` - 两阶段代码审查（规范合规 + 代码质量）
- `commit-skill` - 自动化提交

**独特功能**:
- `brainstorm-skill` - 交互式设计完善，支持多轮讨论
- `worktree-skill` - Git worktree 隔离管理

### 2.2 Hooks 对比

| Hook 点 | Aria | Superpowers |
|--------|------|-------------|
| **SessionStart** | state-scanner | tdd-setup |
| **SessionEnd** | progress-updater | N/A |
| **PreToolUse** | tdd-enforcer | write-guard (TDD检查) |
| **PostToolUse** | (禁用) | N/A |

**关键差异**: Superpowers 的 `write-guard` 会在 Write/Edit 工具调用前检查测试文件是否存在且失败，确保 TDD 顺序不被违反。

---

## 三、工作流对比

### 3.1 Aria 十步循环

```
A. 规划 (Spec & Planning)
├── A.0 状态扫描    → 理解当前在哪
├── A.1 规范创建    → 定义要去哪 (OpenSpec)
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

### 3.2 Superpowers 工作流

```
1. Brainstorm (可选)
   └── 交互式设计讨论，完善需求理解

2. RED Phase
   └── 编写失败测试

3. GREEN Phase
   └── 最小代码通过测试

4. REFACTOR Phase
   └── 重构代码质量

5. Code Review
   ├── Spec 合规性检查
   └── 代码质量检查

6. Commit
   └── 自动化提交
```

**关键差异**:
- Superpowers 是**线性 TDD 循环**，Aria 是**四阶段方法论**
- Superpowers 强制 TDD 顺序，Aria 强调整体流程规范性
- Superpowers 有 brainstorming 交互环节，Aria 有 OpenSpec 文档规范

---

## 四、TDD 执行机制对比

### 4.1 Aria tdd-enforcer

```
触发时机: PreToolUse Hook
检查逻辑:
  1. 检测到 Write/Edit 操作
  2. 检查是否有对应测试文件
  3. 如果没有，警告用户

执行级别: 警告 (可绕过)
```

### 4.2 Superpowers write-guard

```
触发时机: PreToolUse Hook
检查逻辑:
  1. 检测到 Write/Edit 操作
  2. 确认 TDD 模式已启用
  3. 检查测试文件状态:
     - 必须存在
     - 必须处于失败状态 (RED)
  4. 如果不满足，阻止操作

执行级别: 强制 (不可绕过)
```

**关键差异**: Superpowers 的 TDD 检查更严格，要求测试必须处于失败状态（RED），而不仅仅是存在。

---

## 五、隔离策略对比

### 5.1 Aria 分支策略

```
Level 1: 本地分支
  └── feature/xxx, fix/xxx

Level 2: 功能分支 + PR
  └── 推送到远程，创建 Pull Request

Level 3: Git Worktree (可选)
  └── 多工作目录并行开发
```

### 5.2 Superpowers 隔离策略

```
Always: Git Worktree
  └── 每个任务使用独立 worktree
  └── 完全隔离的工作环境
  └── 完成后自动清理
```

**关键差异**: Superpowers 默认使用 Git Worktree，提供更强的隔离保证。Aria 将其作为可选方案。

---

## 六、优化建议

### 高优先级 (立即实施)

#### 1. 增强 TDD 执行严格度

**当前问题**: Aria 的 tdd-enforcer 只检查测试文件存在，不检查测试状态

**建议方案**:
```yaml
增强后的 tdd-enforcer:
  检查点:
    1. 测试文件是否存在
    2. 测试是否处于失败状态 (RED)
    3. 代码变更是否最小 (GREEN)

  执行级别:
    - Level 1: 警告 (当前)
    - Level 2: 强制 (可配置)
    - Level 3: Superpowers 模式 (不可绕过)
```

#### 2. 添加 Brainstorming Skill

**当前问题**: Aria 缺少交互式设计讨论能力

**建议方案**:
```yaml
新 Skill: design-brainstorm
  功能:
    - 引导多轮设计讨论
    - 记录设计决策
    - 生成 OpenSpec 草稿
    - 支持用户提出约束和偏好

  输出:
    - design-decisions.md
    - openspec/proposal.md (可选)
```

#### 3. 实现两阶段代码审查

**当前问题**: 代码审查没有明确的两阶段划分

**建议方案**:
```yaml
增强后的 code-review:
  Phase 1: Spec 合规性
    - 检查是否遵循 OpenSpec
    - 检查架构文档是否同步
    - 检查需求追踪状态

  Phase 2: 代码质量
    - 检查代码风格
    - 检查测试覆盖
    - 检查性能问题
```

### 中优先级 (近期规划)

#### 4. Git Worktree 深度集成

**建议方案**:
```yaml
新 Skill: worktree-manager
  功能:
    - 自动创建 worktree
    - 管理 worktree 生命周期
    - 自动清理完成的 worktree
    - worktree 状态追踪

  集成点:
    - B.1 分支创建 → 自动创建 worktree
    - D.2 归档 → 自动清理 worktree
```

#### 5. Fresh Subagent 模式

**当前问题**: Aria 使用固定 Agents，Superpowers 使用 Fresh Subagent

**建议方案**:
```yaml
增强后的 subagent-driver:
  模式选择:
    - Mode 1: Fixed Agents (当前 Aria)
    - Mode 2: Fresh Subagent (Superpowers 风格)
    - Mode 3: Hybrid (混合模式)

  Fresh Subagent 特性:
    - 每次启动新实例
    - 无历史上下文污染
    - 专注当前任务
```

#### 6. 开源社区策略

**当前问题**: Aria 是私有仓库，社区贡献受限

**建议方案**:
```yaml
开源计划:
  Phase 1: GitHub 公开仓库
    - 迁移主仓库到 GitHub
    - 建立 Contributor Guidelines
    - 设置 PR 模板

  Phase 2: 社区 Skills
    - 参考 superpowers-skills 模式
    - 允许社区贡献 Skills
    - 建立 Skill 审查流程
```

### 低优先级 (长期考虑)

#### 7. 英文文档支持

**建议方案**:
```yaml
文档国际化:
  - 核心文档中英双语
  - Skills 文档可选翻译
  - 使用 i18n 工具管理
```

#### 8. 性能优化

**建议方案**:
```yaml
优化方向:
  - Hooks 执行性能
  - Skills 加载缓存
  - 状态扫描增量更新
```

---

## 七、实施路线图

### Phase 1: 核心 TDD 增强 (1-2周)

```
Week 1:
  [ ] 增强 tdd-enforcer (RED 状态检查)
  [ ] 添加 TDD 严格度配置
  [ ] 编写测试和文档

Week 2:
  [ ] 实现两阶段代码审查
  [ ] 更新 code-review-skill
  [ ] 集成测试
```

### Phase 2: 新增核心 Skills (2-3周)

```
Week 3-4:
  [ ] 实现 design-brainstorm skill
  [ ] 实现 worktree-manager skill
  [ ] 更新 workflow-runner 集成

Week 5:
  [ ] 增强子代理驱动 (Fresh 模式)
  [ ] 文档更新
  [ ] 示例项目
```

### Phase 3: 社区与生态 (4-6周)

```
Week 6-8:
  [ ] GitHub 公开仓库准备
  [ ] Contributor Guidelines
  [ ] PR/Issue 模板

Week 9-10:
  [ ] 社区 Skills 机制设计
  [ ] Skill 审查流程
  [ ] v1.1.0 发布准备
```

---

## 八、结论

Aria 和 Superpowers 代表了两种不同的插件框架设计哲学：

| 维度 | Aria | Superpowers |
|------|------|-------------|
| **定位** | 企业级方法论 | 开发者工具集 |
| **优势** | 完整体系、多模块、架构同步 | TDD 严格、交互式设计 |
| **适用场景** | 大型项目、团队协作 | 个人开发、快速迭代 |

**最佳策略**: 不是二选一，而是取长补短：
- Aria 保持企业级优势（架构同步、需求追踪）
- 借鉴 Superpowers 的 TDD 严格度和交互式设计
- 逐步开源，建立社区生态

---

## 附录：资源链接

- **Aria**: https://github.com/10CG/Aria
- **Aria Plugin**: https://github.com/10CG/aria-plugin
- **Superpowers**: https://github.com/obra/superpowers
- **Superpowers Skills**: https://github.com/obra/superpowers-skills (archived)

---

**文档维护**: Aria 项目组
**更新日期**: 2026-02-05
