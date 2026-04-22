# Aria 方法论演化史料：前 Aria 时期的 Prompt 原稿

> **原始文件**：`F:/work2025/cursor/todo-app-开发提示词(临时).md`（已处理）
> **时间范围**：约 2025 Q2 – Q3（todo-app 项目开发期）
> **整理日期**：2026-04-23
> **整理目的**：保留 aria 方法论从"散文化 prompt"进化到"结构化 skill 系统"的演化痕迹
>
> 本文件已脱敏：
> - 移除 3 个 Google API keys（泄露风险）
> - 移除个人生辰八字等无关 QA 工作的内容
> - 保留所有与 aria 方法论原型直接相关的段落

---

## 一、七步循环的早期形态

> 这是今天 aria **十步循环** 的直接前身。注意当时是 `tech-lead` 作为入口角色。

```
>识别项目状态处于七步循环的位置
-@tech-lead,
-遵从 @docs\standards\ai-project-state-recognition-and-task-execution-system.md,
-识别现在的项目状态
```

### 今天的 aria 对应

| 前 Aria | 今日 aria |
|---|---|
| `识别项目状态处于七步循环的位置` | `aria:state-scanner` — 十步循环统一入口 |
| `ai-project-state-recognition-and-task-execution-system.md` | `aria-standards/` 子模块下的十步循环规范 |
| 入口 agent：`@tech-lead` | Skill-first，Agent 仅为 Skill 辅助（用于独立审查等高风险操作）|

---

## 二、AI-DDD 进度管理系统（step5 – step8）

> `ai-ddd` 一词在这时期已经定名。下方 step5/6/7/8 是完整的"开发闭环工作流"，对应今天 aria 的 Phase C + Phase D。

### step5 — 根据代码更新架构文档

```
>step5-根据代码更新架构文档
-@knowledge-manager,
-遵从 @docs\standards\architecture-documentation-management-system.md
-查看git状态和提交记录,获取所有项目目录中新增和修改的代码文件进入待检查代码文件列表,
-检查待检查代码文件列表的每个文件,判断是否需要更新相关的架构文件,或补全缺失的架构文档,
-确保移动端项目目录架构文档和代码文档 同步率100%, 覆盖率100%.
```

**今日对应**：`aria:arch-update` skill（L0/L1/L2 层级体系，同步率/覆盖率验证）

### step6 — git 分组提交

```
>step6-git提交
-@tech-lead,
-遵从 @.cursor/rules/git-rule.mdc git提交消息规范,
-遵从 @docs\standards\mobile-ai-ddd-progress-management-system.md,
-根据git更改的情况,和移动端项目开发推进情况,设计分组提交计划,
-根据不同的分组提交信息,指派不同subagent代理并行执行git提交(提交信息中需注明执行提交的subagent).
```

**今日对应**：`aria:strategic-commit-orchestrator` — 基于 AI-DDD v3.0.0 的战略提交编排器

### step7 — 代码更新进度文档

```
>step7-根据代码更新进度文档
-@knowledge-manager,
-遵从 @docs\standards\mobile-ai-ddd-progress-management-system.md,
-读取当前移动端进度文档记录的进度情况,识别对应的git提交记录点,
-完整了解当前移动端进度文档记录之后的所有git提交,
  确认移动端项目开发推进情况,更新移动端进度文档.
```

**今日对应**：`aria:progress-updater` skill（写入 UPM 文档的 UPMv2-STATE 机读区块）

### step8 — 分支管理

```
>step8-分支管理
-@tech-lead,
-遵从 @docs\standards\mobile-development-management-system.md,
-遵从 @docs\standards\mobile-ai-ddd-progress-management-system.md,
根据todo应用双规范协作流程,基于移动端项目开发进度,请进行分支操作.
```

**今日对应**：`aria:branch-manager` skill（支持 B.1 和 C.2，结合 Forgejo 集成）

---

## 三、任务分解与并行调度

> `shrimp` 是外部 MCP 工具，早期用它做任务列表管理。今天由 `aria:task-planner` 取代（双层任务架构 tasks.md + detailed-tasks.yaml）。

```
>连续串行执行
-@context-manager,
-使用shrimp工具, 获取最新的任务列表,
-根据子任务的信息,指派最合适的subagent连续执行规划的剩余待执行任务,
-可以并行执行任务的分组,直接启动并行的subagent来执行对应任务,
-直到所有任务都100%完成,否则不要停.
```

**今日对应**：
- 任务规划：`aria:task-planner`（A.2 + A.3，Agent 预分配）
- 执行编排：`aria:subagent-driver`（Fresh Subagent 管理、任务间代码审查）
- 决策矩阵：`aria:agent-router`（任务到 Agent 智能路由）

---

## 四、下一步任务规划

```
>根据文档规划任务
-@tech-lead,
-遵从 @docs\standards\mobile-ai-ddd-progress-management-system.md,
-判断下一步需要执行的阶段任务,
-遵从 @docs\standards\mobile-development-management-system.md,
-为下一步需要执行的阶段任务,创建最优的分支策略,
-给下一步需要执行的阶段任务清单的每个任务指派不同的最合适的subagent,
-连续执行任务清单,直到所有任务都100%完成,否则不要停.
```

**今日对应**：`aria:phase-a-planner`（编排 A.1-A.3：Spec 管理 → 任务规划 → Agent 分配）

---

## 五、架构文档初始化（独立场景）

```
>架构文档初始化
-@knowledge-manager,
遵从 @docs\standards\architecture-documentation-management-system.md
-为 @backend 创建完整的v3.0架构文档系统.

>架构文档索引
-@knowledge-manager,
遵从 @docs\standards\architecture-documentation-management-system.md
-为 @backend 创建或更新架构文档索引.
```

**今日对应**：
- `aria:arch-update` 负责日常同步
- `arch-scaffolder`（如已实现）负责首次初始化
- `arch-search`（L0/L1/L2 搜索）负责读取

---

## 六、演化洞察（今天回看）

### 已稳定继承的架构决策

1. **Agent 命名空间**：`@tech-lead` / `@knowledge-manager` / `@context-manager` 从那时开始一直沿用至今
2. **文档驱动**：`遵从 @docs\standards\...` 的模式今天变成 Skill 内部的 reference/standards 引用
3. **多 subagent 并行**：前 Aria 就有"可以并行执行任务的分组"概念 → 今天的 subagent-driver 多 Fresh instance
4. **同步率/覆盖率承诺**：架构文档"100%同步率、100%覆盖率" → 今天 arch-update 的验证器

### 已被替换/扬弃的模式

1. **散文化 prompt**：大量自然语言 prompt 链 → 结构化 Skill.md（frontmatter + body）
2. **shrimp 外部 MCP**：外部任务管理 → aria 内建 task-planner
3. **七步 → 十步**：扩展出了 Phase A 的 "理解现状"（state-scanner）和 Phase D 的 "归档" (openspec-archive)
4. **"否则不要停"式强制循环**：早期靠 prompt 语言强制，今天靠 hook/agent 机制结构化执行

### 仍可借鉴的早期 idea

1. **"提交信息中需注明执行提交的 subagent"**：调用链审计思路，今天 `aria:code-reviewer` 的 verdict 标注有类似精神，但**提交消息维度还没正式做**
2. **"--reporter=compact --concurrency=1" 作为测试规范**：早期就注意到 Agent 驱动测试时的输出冗余和并发问题，今天仍是值得写进 standards 的操作细节

---

## 附：原稿其他段落的去向

原稿还包含以下内容，**不纳入本史料**：

| 段落 | 去向 |
|---|---|
| 行 1-29：todo-app 早期 QA 测试 prompt（shrimp 主导） | 与具体项目强相关，价值已过期，不保留 |
| 行 133-135：3 个 Google API keys | **删除并要求 rotate**（敏感信息） |
| 行 145-151：个人生辰八字 + 金融软件命名请求 | 与 aria 方法论无关，已移除 |

---

**维护**：10CG Lab
**当前 aria 版本**：v1.16.0（对应 10cg-local-plugin 稳定期）
**下次演化节点**：`aria:audit-engine` challenge 模式（issue #17 Drift Guard）+ Token×Attention 估算（issue #18）
