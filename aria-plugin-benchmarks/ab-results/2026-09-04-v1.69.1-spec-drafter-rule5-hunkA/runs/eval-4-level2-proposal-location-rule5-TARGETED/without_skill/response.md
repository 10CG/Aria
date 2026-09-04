# spec-drafter A.1 推演 — todo-web「任务列表按截止日期排序」Level 2 Proposal

> 产出形态: **descriptive (描述性推演)**。以下内容**未落盘**、未执行 git、未运行任何脚本。
> 这是 A.1 (Spec 管理) 的 draft preview, 相当于 spec-drafter 交互流程停在 `🤔 Create this file? [Yes/No/Edit]` 那一步。

---

## 0. 前置: A.1.0 / A.1.2 / A.1.3 判断过程

**A.1.0 头脑风暴检查**: 本次推演未扫描 `docs/decisions/technical-*.md`。若 todo-web 下已有相关技术决策记录, 应在 proposal 头部补 `> **决策来源**: [DEC-xxx](...)` 并据其预填充「技术方案 / 约束条件」两节。目前按「无决策记录」处理 —— 需求本身足够收敛 (单一交互选项), 不强制先跑 brainstorm。

**A.1.2 Level 判断** (与用户指定的 Level 2 一致):

| 因素 | 观察 | 判定倾向 |
|------|------|----------|
| 关键词匹配 | 「加一个……选项」= `add` / `option`, 属 Level 2 功能开发词; 无 `重构` / `迁移` / `breaking` / `跨模块` 等 Level 3 触发词 | Level 2 |
| 文件影响范围 | 单模块 (前端任务列表视图 + 一个排序纯函数), 不动 `shared/` 契约 | Level 2 |
| 变更类型 | 增量新增, 非 breaking; 默认排序行为保持不变 | Level 2 |
| 综合 | 未触发跨模块自动提升规则 | **Level 2 (Minimal), 产出物 = `proposal.md` only** |

> 边界提醒: 这个 Level 2 结论有一个**前提** —— 任务数据模型里 `due_date` 字段**已经存在**。若还需要新增该字段 (涉及 schema / API 契约 / 迁移), 按「跨模块 + migration」规则应提升为 Level 3 (`proposal.md` + `tasks.md`)。执笔前请先确认这一条。

**A.1.3 模块检测**: 用户界面 + 列表渲染逻辑 → 单一前端模块 (todo-web 自身应用代码), 非 `standards`。

---

## 1. 这份 proposal.md 应该落在哪个完整相对路径

```
standards/openspec/changes/task-list-due-date-sort/proposal.md
```

(相对 todo-web 仓库根目录; feature slug 取 `task-list-due-date-sort`, kebab-case, 与 proposal 标题对应)

---

## 2. 为什么是那个路径, 而不是另一个候选

另一个候选是仓库根目录下的 `openspec/changes/task-list-due-date-sort/proposal.md`。

选择 `standards/openspec/changes/...` 的理由:

【1】**spec-drafter A.1.4 的产出位置就是这么定义的**。SKILL.md 执行流程 A.1.4「生成 Spec 文档」逐字写着:

- `Level 2: standards/openspec/changes/{feature}/proposal.md`
- `Level 3: proposal.md + tasks.md`

Level 2 只有这一个落点, 没有分支条件。

【2】**Skill 的输出预览与 LEVEL_GUIDE 的示例全部一致地指向同一处**。SKILL.md 的「Level 2 预览」区块里 `Location:` 行是 `standards/openspec/changes/user-authentication/proposal.md`; LEVEL_GUIDE.md 的示例 1 (Level 2) 输出 `path: standards/openspec/changes/test-report-skill/proposal.md`, 示例 2 (Level 3) 输出 `standards/openspec/changes/progress-refactor/{proposal,tasks}.md`。三处独立位置口径一致, 不是笔误。

【3】**OpenSpec 的规范定义与模板都挂在 `standards/` 下**。proposal 要对齐的模板是 `standards/openspec/templates/proposal-minimal.md`, 项目定义是 `standards/openspec/project.md` —— todo-web 既然从 aria-standards 引入了 `standards/` 子模块, `openspec/` 这套目录结构的宿主就在该子模块内, changes 与它的模板/项目定义同处一棵树, 引用路径 (`../../../standards/...` 这类相对链接) 和 `openspec validate` 的解析基准才成立。

【4】**根目录 `openspec/` 落点在本 Skill 的执行流程里没有任何出处**。SKILL.md 与 LEVEL_GUIDE.md 全篇没有一处把 Level 2 产出指向仓库根的 `openspec/changes/`; 在两个候选之间, 只有 `standards/openspec/changes/` 有明文依据, 因此按 Skill 执行。

> **执笔者留痕 (需 owner 确认)**: todo-web 仓库根**本身也有**一个 `openspec/` 目录, 而 `standards/` 是从 aria-standards 引入的**共享子模块**。「项目自身的变更该放共享子模块内, 还是放项目自己的 `openspec/`」这一点, 本次仅依据 spec-drafter 的 A.1.4 明文作出选择; 如果 todo-web 的项目级规范对此另有约定 (例如要求项目变更留在本仓、不写入共享子模块), 请在创建文件前推翻上述路径, 改落 `openspec/changes/task-list-due-date-sort/proposal.md`。这属于流程判断分歧, 应写进 handoff 请复议, 不由执笔方单方定案。

---

## 3. proposal.md 全文

```markdown
# Task List Due Date Sort

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-09-04
> **Linked Issue**: `none`

## Why

任务量增长后, 当前任务列表只按创建顺序 (或手动顺序) 呈现, 用户无法一眼看出哪些任务临近截止。
临期任务被埋在列表中部是典型的漏做诱因 —— 用户被迫逐条扫读 `due date` 才能自行排序, 这既慢又不可靠。

给列表补一个「按截止日期排序」的选项, 用一次点击把最紧迫的任务顶到可视区顶部, 是成本最低、
不改数据模型、也不改默认行为的解法。

## What

在任务列表视图新增**排序方式选择器**, 并在其中新增「按截止日期」一项。

行为契约 (承重, 实现零裁量):

1. 排序方向: 升序 —— 截止日期**早**的排在前。
2. 缺失值: `due_date` 为空的任务恒排在**所有**有 `due_date` 的任务之后 (null-last), 与排序方向无关。
3. 稳定性: 截止日期相同 (或同为空) 的任务, 保持切换排序前的相对顺序 (稳定排序)。
4. 默认值: 默认排序方式**保持现状不变**; 用户不主动切换时, 列表与本变更前逐条一致。
5. 持久化: 用户选中的排序方式在本设备上保留, 刷新页面后仍生效。

### Key Deliverables

- `src/lib/sortTasks.ts` — 排序纯函数 (排序方式枚举 + null-last + 稳定排序)
- `src/components/TaskList/SortSelector.tsx` — 排序方式选择器 UI
- `src/components/TaskList/TaskList.tsx` — 接入选择器, 渲染前套用排序
- `src/store/preferences.ts` — 排序偏好读写与恢复
- `src/lib/__tests__/sortTasks.test.ts` — 排序纯函数单元测试

## Tasks

- [ ] 定义排序方式枚举与「缺失 due_date」的排序契约 (null-last, 稳定)
- [ ] 实现 `sortTasks` 纯函数并覆盖单元测试
- [ ] 任务列表视图接入排序方式选择器 UI
- [ ] 排序偏好持久化与页面加载时恢复
- [ ] 回归验证默认排序路径未变

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 临期任务可一键置顶, 减少漏做; 排序逻辑收敛到单个纯函数, 后续加排序维度成本低 |
| **Risk** | 缺失 `due_date` 的任务位置若处理不当会「消失」在列表尾部之外 —— 由契约第 2 条 + 专项测试兜住 |
| **Risk** | 排序偏好持久化引入的本地状态可能与既有偏好存储冲突, 需复用现有 preferences 通道而非另起一套 |
| **Compatibility** | 向后兼容: 不改任务数据模型, 不改 API, 默认排序行为不变 |

## Constraints

| 类型 | 约束 |
|------|------|
| technical | 复用已有 `due_date` 字段, 本 Spec **不含** schema / API 变更; 若该字段尚不存在, 本 Spec 作废并按 Level 3 重开 |
| technical | 排序在客户端完成, 不新增后端排序参数 |
| product | 默认排序方式不变, 避免对现有用户造成无预期的列表重排 |

## Success Criteria

- [ ] 用户可在任务列表切换到「按截止日期」, 列表即时按截止日期升序重排
- [ ] 无 `due_date` 的任务恒排在有 `due_date` 的任务之后 (混合列表实测)
- [ ] 截止日期相同的任务保持切换前的相对顺序 (稳定排序实测)
- [ ] 排序选择在页面刷新后仍然生效
- [ ] `sortTasks` 单元测试覆盖四类输入并全绿: 空列表 / 全部无 due_date / 混合 / 同日多条
- [ ] 未主动切换排序的用户, 列表顺序与本变更前逐条一致 (默认路径回归)
```

---

## 4. A.1.6 验证提示 / 下一步

- 建议运行 `openspec validate task-list-due-date-sort --strict` 验证格式。
- `Linked Issue` 当前填的是哨兵值 `` `none` ``。若 todo-web 侧已有对应 issue, 创建文件前替换为 `` `<org>/<repo>#<n>` `` 形 (inline code span, 不要写成 markdown 链接形, 也不要用 `N/A` / `TBD` / `-`)。
- 若 todo-web 是 framework 项目 (Next.js / Astro / SvelteKit / Vue / Remix 等), 按 A.1.1 在 proposal 里补一段 Framework Constraints (已知 convention / anti-pattern), 供 post_spec / post_implementation 审计 agent 直接对照。本次因未确认框架而留空。
- 确认无误后进入 **A.2 任务规划** (`task-planner`), 由它产出 `detailed-tasks.yaml` (时间估算 / 文件路径) 与 A.3 Agent 分配 —— 这些内容按分工**不写进** proposal.md。
