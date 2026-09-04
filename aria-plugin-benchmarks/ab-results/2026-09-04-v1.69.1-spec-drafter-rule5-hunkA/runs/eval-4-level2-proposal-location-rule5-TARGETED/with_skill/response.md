用 `spec-drafter` (A.1 Spec 管理) 为 todo-web 起草这份 Level 2 proposal。产出形态为描述性推演 —— 下面只推演落点与内容，不实际创建文件、不跑 git/脚本。

---

## 0. Skill 执行轨迹 (descriptive)

| 步骤 | 结论 |
|------|------|
| A.1.0 头脑风暴检查 | 未见 `docs/decisions/technical-*.md` 相关决策记录。需求边界清楚 (单一排序选项)，判定无需先跑 `brainstorm.technical`，直接起草 —— 交互模式下这里会给【1】先头脑风暴 /【2】直接创建 /【3】取消 三选一 |
| A.1.1 需求信息收集 | Why / What / Deliverables / Constraints 见下方全文；Framework Constraints 为可选项，见第 4 节待确认事项 |
| A.1.2 Level 判断 | 关键词「加一个…选项」= add / feature，命中 Level 2 触发词；无 refactor / breaking / migration / 跨模块 等 Level 3 触发词；影响范围为任务列表单模块。综合评分落在 `3 <= score < 7` → **Level 2 (Minimal)** |
| A.1.3 模块检测 | todo-web 前端任务列表模块 (单模块，非 shared / 非 standards) |
| A.1.4 生成 Spec | Level 2 只产 `proposal.md`，**不生成 tasks.md** (那是 Level 3 的产出；细粒度任务由 A.2 `task-planner` 产 `detailed-tasks.yaml`) |
| A.1.5 交互确认 | 逐章节确认：Level → Why → What → Deliverables → Impact → Tasks → Success Criteria |
| A.1.6 验证提示 | 建议 `openspec validate sort-tasks-by-due-date --strict` |

---

## 1. 这份 proposal.md 应该落在哪个完整相对路径

```
openspec/changes/sort-tasks-by-due-date/proposal.md
```

相对 **todo-web 仓库根**。展开即 `todo-web/openspec/changes/sort-tasks-by-due-date/proposal.md`。

Level 2 只有这一个文件，同目录下不建 `tasks.md`。

---

## 2. 为什么是那个路径而不是另一个候选

最容易误落的候选是把它写进共享子模块：

```
standards/openspec/changes/sort-tasks-by-due-date/proposal.md   ← 错
```

不选它的理由，按重要性排：

【1】**Aria 不可协商规则 #5 直接禁止**：「项目变更放本项目 `openspec/changes/`，不放 `standards/openspec/changes/`」。spec-drafter 的 A.1.4 也把这条写进了路径落点约束：路径落点 = **消费方项目自己的** `openspec/changes/`。

【2】**所有权判据**：`standards/` 是从 aria-standards 引入的**共享子模块**，是所有采用 Aria 方法论的项目共读的规范 SOT。把 todo-web 的一个产品功能写进去，这份变更会对**所有采用方可见且无人拥有** —— 别的项目在自己仓里看到一份和自己无关的「按截止日期排序」proposal，既无法验收也无法归档。

【3】**机械后果**：`standards` 作为子模块，指针由 `git submodule update --remote` 推进。写在子模块工作区里的项目级变更要么在下次更新时被冲掉，要么被迫推进共享 repo 的 master —— 前者丢工作，后者污染共享规范的变更历史。

【4】**分界线怎么划**：判据是「这个变更的**对象**是谁」。改十步循环、改 `proposal-minimal.md` 模板、改 conventions —— 变更对象是规范本身，那才落 standards 仓自己的 `openspec/changes/`。按截止日期排序的对象是 todo-web 的任务列表功能，属于项目自身 ⇒ 落 todo-web 的 `openspec/`。

另外两个次要误落点，一并排除：

- `openspec/specs/…` —— 那是已归档、代表**当前能力基线**的目录，in-flight 变更不进这里。
- `openspec/archive/…` —— 那是十步循环 D.2 归档之后才进的位置，Draft 阶段不能预先落在这里。

所以 in-flight 的 Level 2 变更，位置恒为本项目仓的 `openspec/changes/{feature}/proposal.md`。

---

## 3. proposal.md 全文

```markdown
# Sort Task List by Due Date

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-09-04
> **Linked Issue**: `none`

## Why

当前任务列表只有一种默认排序 (创建时间)，带截止日期的任务不会因为「临期」而上浮，用户必须逐条扫读整个列表才能判断接下来该做什么。加一个按截止日期排序的选项，让最紧急的任务在首屏可见，是任务类产品的基础预期，也是当前最常见的用户反馈。

## What

在任务列表增加一种排序方式 `dueDate`，与现有默认排序并列，用户可在列表头部的排序控件中切换，并可在升序 / 降序间翻转；所选排序方式随用户偏好持久化，刷新与重新进入后保持。本变更只影响列表的读取与展示路径，不改动任务数据模型，不新增字段。

### Key Deliverables
- 列表排序控件新增「按截止日期」选项，含升序 / 降序切换
- 排序逻辑：有截止日期的任务按日期排序；无截止日期的任务恒定排在末尾，不参与升降序翻转
- 排序偏好持久化与恢复 (跨会话保持)
- 排序逻辑单元测试 + 列表交互测试

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 用户可一眼定位临期任务，减少人工扫读；纯读取路径变更，不触碰任务数据模型，回滚成本低 |
| **Risk** | 空 `dueDate` 与时区边界容易产生不稳定排序 (同日任务顺序抖动、跨时区跨日)。缓解：排序键定义为三元组 `(has_due_date, due_date, created_at)` 保证全序且稳定；日期比较统一在同一时区基准下进行，本地化只发生在展示层 |

## Tasks

- [ ] 定义排序键与空值语义 (无截止日期恒末尾；三元组保证稳定全序)
- [ ] 实现 dueDate 排序函数并接入列表数据层
- [ ] 排序控件 UI 增加选项与升降序切换
- [ ] 排序偏好持久化与恢复
- [ ] 补齐测试：空值 / 同截止日期 / 跨时区 / 升降序 / 空列表
- [ ] 同步更新用户文档与架构文档中任务列表模块的说明

## Success Criteria

- [ ] 选择「按截止日期」后，有截止日期的任务按日期升序排列，无截止日期的任务全部位于列表末尾
- [ ] 切换降序时只翻转有截止日期的部分，无截止日期的任务仍在末尾
- [ ] 同一截止日期的多个任务顺序稳定 —— 重复渲染 / 刷新 / 重新进入结果一致
- [ ] 排序偏好在刷新和重新进入后保持
- [ ] 新增排序逻辑单元测试全部通过，任务列表模块测试覆盖率不低于变更前
- [ ] 默认排序行为不变 (未主动切换的用户看到的列表与变更前一致)
```

---

## 4. 起草后的三项待确认 / 后续动作

【1】**Linked Issue 字段**。头部按 SOT 模板 `standards/openspec/templates/proposal-minimal.md` 的顺序写 (`Level` → `Status` → `Created` → `Linked Issue`)。这里先填哨兵 `` `none` ``，含义是「已核实无关联 issue」。如果 todo-web 在 tracker 里已有对应条目，把值替换成 inline code span 形的 `` `<org>/todo-web#<n>` ``；多个 issue 写在同一个 code span 内用 `, ` 分隔。三条硬性写法：不留空、不删行；`N/A` / `TBD` / `-` 都不是合法哨兵；不要写成 markdown 链接形。

【2】**Framework Constraints (A.1.1 可选项，Aria #95)**。todo-web 若跑在 Next.js / Astro / SvelteKit / Vue / Remix 之类 framework 上，proposal 里应补一段该 framework 的已知 convention / anti-pattern (例如 `use client` / server 边界、route handler export 限制)，供 post_spec 与 post_implementation 的审计 agent 直接对照。当前信息不足以判断 todo-web 用的是哪个 framework，这一段先留空 —— 交互确认时补，别凭空编。

【3】**下一步**。确认本 proposal 后运行 `openspec validate sort-tasks-by-due-date --strict` 验证格式，然后进入 A.2 `task-planner` 做任务分解与 Agent 分配 (`detailed-tasks.yaml`)，再进 B.1 建分支。
