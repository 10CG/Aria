明白, 按 descriptive 模式推演 —— 下面只出内容, 不落盘、不跑脚本、不碰 git。

---

## 0. 先交代两个被跳过的 A.1 前置 (descriptive 模式声明)

这两步在真实会话里是要真跑的, 这里只描述, 请知悉这不是「判定它们不适用」:

**A.1 REQUIRE claim (MUST)**: 起草前必须先认领, 防的是「远端已有人在做同一件事」—— 十步循环那 10 轮闸门审的都是「这份产物做得对不对」, 没有一条问过「它该不该存在」。真实路径下会是:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
  --raw-track-id "task-list-due-date-sort-<container_uuid>" \
  --phase A.1 --mode advisory \
  --include-terminal \
  --repo-path "<todo-web 仓根>"
```

- `--raw-track-id` = 逐字 `<spec-slug>-<container_uuid>`, slug 取 Spec 目录名 `task-list-due-date-sort` (不预归一), uuid 段取 `~/.aria/container-id` 的 **`uuid` 字段**而非 `label`。
- `--linked-issue` 这里**整个省略**: 目前没拿到 todo-web 侧的关联 issue, 而哨兵 (`none` / `NO_TOKEN` / `NO_FIELD`) 绝不可当值传 —— 任何非空字符串都 truthy, 两份毫无关系的 Spec 只要都写哨兵就会互相命中。
- 读结果时注意四态互不相同: 键缺席 = 「本轮未检测」; `linked_issue_overlap == []` = 「无碰撞」; `unknown_schema_claims > 0` = 「已检测到 N 条无法解析的 claim, 按存在处理」; `overlap == null` 且 `overlap_error` 非空 = 「**未能核实, 建议重试**」—— 最后这条绝不能渲染成「无碰撞」, 零证据不是正证据。
- 退出义务两条: Spec 目录改名 ⇒ release 旧 + acquire 新; 放弃方向 ⇒ `release_gate.py --raw-track-id <同一串> --status abandoned`。

**A.1.0 头脑风暴检查**: 真实路径下会扫 `docs/decisions/technical-*.md` 看有没有可预填充的技术决策。这个需求边界清晰 (单一交互选项 + 一个排序键), 即使没有决策记录也不必先走 brainstorm.technical; 若 todo-web 仓里已有相关 DEC, 起草时应在头部加 `> **决策来源**: [DEC-00x](../../docs/decisions/technical-00x.md)` 并预填「技术方案 / 约束条件」两节。

**Level 判断 (A.1.2)**: 关键词「加一个…选项」= 功能开发词 (add / feature), 影响范围单模块 (前端任务列表的排序逻辑 + 一个 UI 控件), 无 breaking / 无跨模块 / 无 schema 契约变更 ⇒ **Level 2 (Minimal), 只出 `proposal.md`, 不出 `tasks.md`**。符合模板自陈的 Level 2 画像 (1-3 天、2-5 个文件)。

---

## 1. 这份 proposal.md 应该落在哪个完整相对路径

```
openspec/changes/task-list-due-date-sort/proposal.md
```

相对于 **`todo-web` 仓库根**。也就是绝对形态是 `<todo-web 仓根>/openspec/changes/task-list-due-date-sort/proposal.md`。

Level 2 到此为止 —— 同目录下**不**生成 `tasks.md` (那是 Level 3 的产出物), 任务粒度的 `detailed-tasks.yaml` 也不在这一步, 归 A.2 `task-planner`。

---

## 2. 为什么是这个路径, 而不是另一个候选

另一个候选是 `standards/openspec/changes/task-list-due-date-sort/proposal.md` —— 它看上去很像, 因为 `standards/` 子模块里确实**也**有一个 `openspec/` 目录结构。这正是这个坑的诱因。它是错的, 理由三层:

**(a) 直接判据 —— Aria 不可协商规则 #5**: 「项目变更放本项目 `openspec/changes/`, 不放 `standards/openspec/changes/`」。这条是硬规则, 不是风格偏好。

**(b) 归属语义 —— `standards/` 是共享子模块, 不是本项目的一部分**: `standards/` 是从 aria-standards 引入的**共享**规范仓, todo-web 只是它的一个采用方 (consumer)。把「todo-web 的任务列表加排序选项」写进 `standards/openspec/changes/`, 后果是这份变更对**所有**采用 aria-standards 的项目可见, 却**没有任何一个项目拥有它** —— 它既不是 standards 自己的规范演进, 也不再由 todo-web 独立管辖。变更的所有权和它的可见范围就此错配。

**(c) 机械后果**: `standards/` 是 submodule, 在它里面新增文件会污染子模块工作区, 产生一次与 todo-web 功能无关的子模块提交 + 主仓 gitlink bump; 后续 `git submodule update --remote` 又会让这份 Spec 与上游 standards 打架。而 todo-web 自己的 `openspec/changes/` 就在主仓工作树里, 跟着功能分支一起走, 与 B.1 分支 / C.1 提交 / D.2 归档 (`openspec/changes/archive/`) 全流程对齐。

**边界另一侧**: 什么时候才该落 `standards/openspec/changes/`? 只有当变更的对象**就是共享规范本身**时 —— 比如「修改十步循环 Phase A 的定义」「给 proposal-minimal 模板加一个必填字段」。判据一句话: **问「这次变更交付完成后, 谁的行为改变了」**。答案是 todo-web ⇒ 落 todo-web; 答案是「所有采用 Aria 的项目」⇒ 才落 standards。本例答案显然是前者。

---

## 3. proposal.md 全文

```
╔══════════════════════════════════════════════════════════╗
║           SPEC DRAFT PREVIEW (Level 2)                   ║
╚══════════════════════════════════════════════════════════╝

Feature: task-list-due-date-sort
Module: web (前端任务列表; 单模块, 无跨模块)
Location: openspec/changes/task-list-due-date-sort/proposal.md
```

---

```markdown
# Task List Due Date Sort

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft
> **Created**: 2026-09-05
> **Linked Issue**: `none`

## Why

当前任务列表只有单一固定排序, 用户无法把「快到期」的任务顶到视野内, 只能靠肉眼在整列表里扫截止日期。任务量一多, 临期任务被淹没, 直接削弱待办清单的核心价值 —— 提醒「接下来该做什么」。加一个按截止日期排序的选项, 用最小改动补上这个缺口。

## What

在任务列表上新增一个「排序方式」选项, 允许用户在现有默认排序与「按截止日期」之间切换, 并支持升序 (最早到期在前) / 降序。排序在客户端对已加载的任务集合进行, 不改动任务数据模型, 不引入新的后端接口。用户的选择在会话内保持 (刷新后回落到默认排序, 持久化留作后续增强)。

无截止日期的任务统一排在有截止日期的任务之后, 且在升序/降序两个方向上都保持该位置 —— 避免降序时一堆空值抢占列表头部。

### Key Deliverables

- 任务列表组件: 新增排序方式选择控件 (默认排序 / 按截止日期), 含升降序切换
- 排序逻辑模块: 纯函数 `sortTasks(tasks, sortKey, direction)`, 集中处理截止日期比较与空值归位规则
- 排序选择的会话内状态管理 (列表组件本地状态或既有 store, 依 todo-web 现状择一)
- 单元测试: 覆盖升序 / 降序 / 空截止日期 / 同日期并列 / 空列表五类输入

> 上述交付物按「一个 UI 控件 + 一个排序纯函数 + 状态 + 测试」的形态描述; 具体文件路径以 todo-web 实际目录结构为准, 由 A.2 任务规划阶段落到具体 file path (本 Level 2 proposal 不写死路径)。

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 用户可主动把临期任务置顶, 提升待办清单的实际可用性; 排序逻辑抽为纯函数, 后续新增排序键 (优先级 / 创建时间) 可直接复用同一入口 |
| **Risk** | 空截止日期与同日期并列的处理若不明确, 会出现列表顺序抖动 (同一份数据两次渲染顺序不同)。缓解: 排序实现为稳定排序, 并把空值归位与并列时的次级比较键 (任务 id) 写死进 `sortTasks`, 由单元测试锁定 |
| **Risk** | 排序控件挤占列表头部空间, 在窄屏下可能压缩任务标题显示。缓解: 窄屏下控件折叠为图标按钮, 交付前在移动端宽度实测一次 |

## Tasks

- [ ] 确认现有任务列表的默认排序规则与截止日期字段的实际类型/可空性
- [ ] 实现 `sortTasks` 纯函数 (截止日期升降序 + 空值归位 + 稳定并列)
- [ ] 为 `sortTasks` 编写单元测试 (升序/降序/空值/并列/空列表)
- [ ] 在任务列表组件接入排序方式选择控件与会话内状态
- [ ] 窄屏与空列表两种边界状态的手工核验

## Success Criteria

- [ ] 选择「按截止日期 · 升序」后, 列表顺序与按截止日期升序排列的期望序列逐项一致 (含并列项的稳定顺序)
- [ ] 无截止日期的任务在升序与降序两个方向下均位于列表末尾
- [ ] 切换排序方式不触发任何数据重新请求 (排序全部在客户端完成)
- [ ] `sortTasks` 单元测试五类输入全部通过, 且测试对错误实现可证伪 (故意反转比较方向时测试必须变红)
- [ ] 空列表 / 全部任务无截止日期两种边界下不报错、不出现空白页
```

---

## 4. 两处需要你确认的地方 (不确认不影响起草, 但影响定稿)

1. **`Linked Issue` 值**: 我按「未核实到关联 issue」逐字写了哨兵 `` `none` ``。这个字段是 Level 2/3 的**必填**项 —— 不留空、不删行 (空值与「忘了写」不可区分), 且 `N/A` / `TBD` / `-` 都不是被接受的哨兵、会判不合规。如果 todo-web 侧已经有对应 issue, 请把它换成 `` `<org>/<repo>#<n>` `` 形式 (例 `` `10CG/todo-web#42` ``), 多个 issue 写在**同一个** code span 内用 `, ` 分隔; 别写成 markdown 链接形 (`[repo#42](url)` 会被判 `NO_TOKEN`)。

2. **Framework Constraints 段 (Aria #95, 可选)**: todo-web 若是 Next.js / Astro / SvelteKit / Remix 一类 framework 项目, proposal 里应再加一段已知 framework convention / anti-pattern (例如 `use client` 边界 —— 排序控件带交互状态就必须是客户端组件, 别不小心塞进 server component), 供 post_spec / post_implementation 的审计 agent 直接对照。我目前不知道 todo-web 用的是什么栈, 所以先没加; 告诉我栈, 我补这一段。

---

## 5. 下一步

- 落盘后建议跑 `openspec validate task-list-due-date-sort --strict` 验证格式。
- Level 2 到此结束, 接着进 **A.2 `task-planner`** 把 Tasks 拆成带文件路径与估算的 `detailed-tasks.yaml`, 再由 A.3 分配 Agent, 然后 B.1 建分支。
