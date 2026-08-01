---
verdict: REVISE
agent: tech-lead
round: R1
critical_count: 0
major_count: 2
minor_count: 5
---

# post_spec R1 · tech-lead 视角审计

审计对象: `openspec/changes/session-closer-autofill-yaml-datasource/proposal.md` (aria-plugin #121, Level 2)
视角: 架构 / 决策合理性 — 跨 skill 耦合方向、5 条关键决策、scope 大小、是否漏了更简方案。

逐行核对的真实代码:

- `aria/skills/session-closer/scripts/handoff_autofill.py` (全文 392 行)
- `aria/skills/state-scanner/scripts/lib/detailed_tasks.py` (全文 274 行)
- `aria/skills/state-scanner/scripts/lib/spec_complete.py` L120-360
- `aria/skills/state-scanner/scripts/collectors/openspec.py` L1-40 + L200-300
- `aria/skills/state-scanner/scripts/lib/carry_forward.py` / `frontmatter_block.py` (docstring 的 acyclic 论证)
- `aria/skills/session-closer/tests/test_handoff_autofill.py` L225-255
- `.aria/triage-report.json` (#121 triage 证据)
- 本仓 `openspec/changes/*` 全部 7 个 active spec 的 datasource 形态实测

---

## Major

### M-1 `parse_ok=False` 未处理 — 直接复刻本 issue 要杀的静默假绿

严重度: Major
位置: proposal §What 第 2 条 + 第 4 条 (降级方向) + Success Criteria 全表

主张: proposal 只写「`parse_detailed_tasks(text)` 逐 task 取 `{id, raw_status, title}`」, 从未提到返回值里的 `parse_ok` / `reason`。按字面实施 = 解析失败时拿到空 `tasks` 列表 → 报 0 条 → **与 #121 的病症字节级同构**。而第 4 条把 sentinel 降级**只**绑定在「跨 skill 导入失败」一种失败模式上, 漏掉了更常见的一种。

真代码证据 (`lib/detailed_tasks.py` L225-259): `parse_detailed_tasks` 有四条 file-level 失败路径, 每条都 `return` 一个 `{"parse_ok": False, "tasks": [], "reason": ...}`:

- L237-240 无单一无歧义的顶层 `tasks:` (缺失**或重复**)
- L246-247 `tasks:` 下零个 `- id:` 条目
- L254-259 结构自洽性不符 (base-indent 列表项数 ≠ `- id:` 匹配数 — 即 `id` 不是第一个字段 / dash-id 跨行, 这是「隐藏条目」类, 现实里最容易撞)

这三种都不是异常, 是**正常返回**, 空 `tasks` 一路静默流到 `items` 为空。

同 SOT 的另外两个消费方都显式分流, 先例齐备, 唯独本 spec 没写:

- `lib/spec_complete.py` L207-212: `if not parsed["parse_ok"]: return (False, f"...unparseable ({parsed['reason']})")` — 不放行, 且带 reason
- `collectors/openspec.py` L280-284: 读失败走 `r.soft_error(error_kind, ...)`, 不静默

要求: §What 第 4 条的 sentinel 规则改成覆盖「yaml 存在但拿不到可信 task 列表」的**全部**分支 (导入失败 / `parse_ok=False`), sentinel 文案带上 `parsed["reason"]`; Success Criteria 补一条 SC (例如结构自洽性不符的 fixture → 出 sentinel 而非 0)。这条不是加需求, 是让实现别在同一个 PR 里重开同一个洞。

### M-2 scope 声称的「第四处消费方」封闭性不成立 — 第三种 datasource 形态未命名, 且本 spec 自己就是那个形态

严重度: Major
位置: proposal §Why (「本处是跨 skill 的第四处」) + §Impact

主张: 根因是「消费方只认固定文件名, 遇到别的形态即静默 0」。proposal 把根因面收敛成 `tasks.md` 与 `detailed-tasks.yaml` 二元, 但真实存在第三种形态: **Level 2 spec 把任务清单内联写在 `proposal.md`**(CLAUDE.md 定义 Level 2 = 只有 `proposal.md`)。修完之后这类 spec 依然报 0。

实测证据 (本仓当前 7 个 active change 的形态扫描):

```
aria-2.0-m6-cost-model-telemetry        tasks.md=yes yaml=no   proposal `- [ ]`=12
aria-2.0-m6-dispatch-input-delivery     tasks.md=yes yaml=yes  proposal `- [ ]`=12
aria-2.0-m6-e2e-resilience              tasks.md=yes yaml=no
aria-2.0-m6-release-closeout            tasks.md=yes yaml=no
aria-2.0-m7-agent-lifecycle             tasks.md=yes yaml=no
aria-2.0-m7-fleet-aggregation           tasks.md=yes yaml=no
session-closer-autofill-yaml-datasource tasks.md=no  yaml=no   proposal `- [ ]`=10
```

也就是: 本仓当下**唯一**命中新分支的目录数是 0 (没有 yaml-only spec), 而**唯一**报 0 的 spec 是本 spec 自己 —— 它有 10 个未勾选项, `grep_unchecked_tasks` 修完照样看不见。issue #121 引用的那个真实案例 `state-scanner-gate-yaml-datasource` 已归档 (`openspec/archive/2026-07-22-...`), 不再在 active 面上。这不否定修复价值 (yaml-only 形态会复现), 但「第四处 = 收口」的叙述与实测不符。

顺带一个正向发现: `aria-2.0-m6-dispatch-input-delivery` 同时有 `tasks.md` 和 `detailed-tasks.yaml`, 是 SC-2 优先级断言的现成真实语料, 建议 SC-2 除 tempdir fixture 外在本仓真实目录上跑一次。

要求 (二选一, 都不需要写代码):

- 在 §Impact 显式 scope-out, 并写出真实理由 —— `proposal.md` 里的 `- [ ]` 混着 Success Criteria 与 Tasks 两类语义, 无差别扫会把验收标准当未完成任务, 是噪音而非信号; 因此需要独立设计而非顺手加个分支;
- 且开 follow-up issue 挂住, 否则「第五处消费方」会以 #121 完全相同的方式重开。

---

## Minor

### m-1 行号引用漂移 (关键决策表「import 路径」行)

位置: proposal §关键决策 表格第 3 行 + §What 第 3 条

- 表格写「spec_complete L342 同款先例」。真代码 `spec_complete.py` L342 是 `_CODE_EXT_RE = re.compile(...)`, 与 import 无关。真正的 `detailed_tasks` 裸模块 dual-context 先例在 **L350-356**。
- 正文写「`spec_complete.py` L342-356」, 是包含真区间的松散超集, 不算错但精度不足。
- 正文写 `owner_container()` (L317-321), 表格写「本文件 L319-321」, 两处自相不一致。真代码: `def owner_container()` 在 L305, sys.path 计算/插入在 L318-320, `from lib.identity import get_identity` 在 L321 (L317 是注释)。

建议统一成 `spec_complete.py:350-356` 与 `handoff_autofill.py:305-326 (绑定发生在 318-321)`。

### m-2 `lib` 顶层名毒化的论证选错了证据, 且该毒化是条件性的 — 实施者按图索骥会把它证伪

位置: proposal §What 第 3 条 + 关键决策表「import 路径」行的「本文件 L319-321 实锤」

结论 (禁用 `from lib.detailed_tasks import ...`) 我同意, 但**理由站不住**, 而错误的理由比没有理由危险: 实施者一验证发现不成立, 很可能退回去用 `lib.` 前缀。

真代码证据: 两个不同的 `lib` 目录并存 (memory `feedback_state_scanner_dual_lib_package_shadow`):

- `state-scanner/lib/` — Layer L (identity / claim_* / worktree_manager), **没有** `detailed_tasks.py`
- `state-scanner/scripts/lib/` — `detailed_tasks.py` / `spec_complete.py` / `carry_forward.py` 在这里

`owner_container()` L318 插的是 `state-scanner` skill root ⇒ `lib` = 前者 ⇒ `lib.detailed_tasks` 必然 ImportError。**但**在默认编排路径上它不是先跑的那个: `assemble_from_snapshot` L355-362 的 dict 字面量先算 `"sync"` ⇒ `fill_sync_section` ⇒ `_benign_unconditional_reasons()` (L48-50) 先把 `state-scanner/scripts` 插进 sys.path 并 import `collectors.multi_remote`, 而 `collectors/__init__` 链路会绑定 `lib` = `scripts/lib` —— 那里**有** `detailed_tasks`。也就是最常见路径上 `lib.detailed_tasks` 反而能通; 只有 `--owner-container` CLI 分支或 phase-d-closer 先调 `owner_container()` 时才炸。

真正该引的权威论证已经成文, 在 `collectors/openspec.py` L18-30 的 header note:

> Deliberately NOT `from lib.carry_forward import ...`: the top-level name `lib` may already be bound to state-scanner/lib (skill root) by handoff_multibranch.py's `_SS_ROOT` sys.path insertion.

建议把理由改写成「`lib` 绑到哪个目录**取决于进程内的调用顺序**(两个同名不同内容的 `lib` 目录 + 至少三处 sys.path 插入方), 顺序敏感的导入是不确定行为, 因此一律走裸模块名」, 并引 `collectors/openspec.py:18-30` 作先例。

### m-3 yaml 读失败 (OSError) 的处置未规定

位置: proposal §What 第 2 条

现行 `tasks.md` 分支 L168-172 的 OSError 处置是 `continue` (静默丢)。若 yaml 分支照抄, 得到的又是静默 0 —— 与 M-1 同一类。同 SOT 的 `collectors/openspec.py` L280-284 先例是 `soft_error` 而非静默; `spec_complete.py` L204-205 也把 unreadable 编成显式 reason。建议与 M-1 的 sentinel 规则合并成一条: 「yaml 在场 ⇒ 要么给出真实条目, 要么给出 sentinel, 不存在返回空的路径」。(`tasks.md` 分支的既有静默 continue 属存量问题, 不要求本 PR 改, 但值得在 §Impact 记一笔。)

### m-4 SC-6 引的 memory 方向反了; 真实的跨 skill 风险没被覆盖

位置: proposal §Success Criteria SC-6

SC-6 引 `feedback_test_runner_scope_blind_to_cross_skill_consumers` 说「跨 skill 消费方, 两边都跑」。那条 memory 讲的是**改共享 lib 时漏检下游消费方**; 本次改的恰是消费方, state-scanner 侧零改动 (proposal §Impact 自己也这么写), 方向反了。跑 state-scanner 测试无害 (保险成本近零), 但依据要写对。

真实的跨 skill 风险是反向的: session-closer 从此把 `state-scanner/scripts/lib/detailed_tasks.py` 的**物理路径**硬编码进 sys.path 计算, 而 state-scanner 自己的测试永远不会失败 —— 将来 lib 迁移/改名只会让 session-closer 静默降级成 sentinel(比假绿好, 但仍是能力丢失)。低成本对策 (任选): 在 `lib/detailed_tasks.py` docstring 增一行 external-consumer 契约注记 (该文件已有此类注记惯例, 见其 L4-17), 或 SC 里明确 SC-1 必须在**真实仓库布局**下跑 (不 mock import), 使路径断裂即红。

### m-5 `item` 文本拼接在 title 缺失时未定义

位置: proposal §What 第 2 条 (`"item": "<id> <title>"`)

`detailed_tasks._extract_block_title` L191-195 在 `title:` 缺失时返回空串 `""`(不是 None), 于是 item 会是 `"TASK-001 "` 带尾空格。下游 `cross_check_unfilled` 的 `_item_key` (L243-245) 会归一化掉, 不产生功能问题, 但输出给人看的 handoff 里是脏字符。建议 spec 直接写死: title 为空时只输出 id。

---

## 核对通过、无 finding 的部分 (逐条记录, 避免下一轮重开)

1. **耦合方向正确**。`session-closer → state-scanner/scripts/lib/detailed_tasks` 是消费方指向 SOT 的单向只读边, 目标是 leaf 模块 (`detailed_tasks.py` L33-35 只有 `from __future__` + `import re`, 零回边), 与 `frontmatter_block.py` docstring 的 acyclic 论证同型。proposal §What 第 3 条「零循环风险」成立。且 `handoff_autofill.py` 已有两处同形态跨 skill import (L42-59 / L305-326), 这是第三处, 拓扑一致、无新范式。
2. **不双写 parser 的决策正确**。`parse_detailed_tasks` / `is_done_status` 都是无下划线公开 API (L104-111 / L225-273), 复用合法; 第二次实现 yaml 解析会立刻分叉 range-bounded + indent-anchored + 字段列锚定三层不变量 (L177 的字段列锚定尤其反直觉, 重写必丢)。
3. **决策 2 (并存优先级) 与 #113 决策 6 逐条同型**。对照 `collectors/openspec.py` L272-277: `if tasks_file.is_file(): ... elif (d/"detailed-tasks.yaml").is_file(): ...` —— proposal 的「tasks.md 在场 ⇒ yaml 不看」与之字面一致, 防陈旧 A.3 期 yaml 双计的理由也一致。
4. **输出 schema 兼容性成立**。`assemble_unfinished` L235 是 `out.extend(unchecked_tasks or [])` 直通, 不解析 `source`; 全仓 grep 确认无任何消费方解析 `"tasks.md:"` 前缀 (唯一命中是测试 L227 的 fixture 字面量)。新前缀零改动兼容成立。
5. **决策 5 (`not is_done_status(...)`) 正确**。done-family 白名单 `_DONE_FAMILY = {"done","completed"}` 在 L83, `is_done_status(None) → False` (L109-111), 所以 SC-4 列的 deferred/blocked/in_progress/未知/缺失全部落残留, 与 SOT 同源, 不另写字面量。
6. **Rule #6 substitute 判定正确**。`handoff_autofill.py` 是 deterministic 机械脚本, SKILL.md / description 零变动 (SKILL.md 只在 L94-95 有调用行, 命令面不变), 符合 CLAUDE.md Rule #6 表「描述性 / deterministic ⇒ substitute: SC 级 baseline-failing 结构化测试」与 memory `feedback_deterministic_structural_skill_rule6_substitute`。SC-1 已写明 baseline 必 FAIL, 防真空绿。
7. **PATCH 定级与 ship 同步面正确**, 与 CLAUDE.md 版本管理段一致。
8. **triage 证据与 §Why 数字一致**: `.aria/triage-report.json` verdict=confirmed / severity=major / repro 2/2, case-1 fixture 就是 2 task 全 pending → 返回 `[]`, case-2 对照组 tasks.md 正常 2 条。proposal 的「实测 2 pending → 报 0; 对照组 2/2」逐字对得上。(注: issue 正文里的 10 pending 是另一个真实案例, 两个数字不冲突。)
9. **§Why 引用的 L160-175 与 §What 引用的 L46-50 均准确**。
10. **更简方案是否被忽略**: 考虑过「不做跨 skill import, 改由 state-scanner 在 snapshot 里多输出一个 per-change 残留计数字段, session-closer 只读 snapshot」。该路线更解耦, 但 (a) 要改 state-scanner + snapshot schema, 爆炸半径远大于 PATCH; (b) 违背 `grep_unchecked_tasks` 的设计意图 —— 其 docstring L161 明写「新增轻量 grep(非既有 collector)」, 它作为 backstop 的价值正在于**不与 collector 共享失败模式**(AD-2 的 backstop 定位, 文件 docstring L10-12)。所以 proposal 选的路线是对的。**但 proposal 没有记录这个被否决的替代方案**, 建议在 §关键决策 补一行, 否则后续 review 会重开同一讨论。
