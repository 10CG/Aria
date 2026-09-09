# AB 结果 — phase-d-closer (E-0b, SC-11 分支 b 补跑)

| 字段 | 值 |
|---|---|
| 跑于 | 2026-09-08 |
| 为什么跑 | SC-11 的分支 (b) 要求「补跑 phase-d-closer / state-scanner 套件」。主控**无条件**执行了该分支里唯一能产生信息的那一半 —— 依据 SOT §2 决策表第四行「拿不准 ⇒ **照跑** (宁跑勿豁)」 |
| 两臂 | v_new = 本 Spec 落地后 · v_old = `aria` `301641b` (= v1.71.1, 跑时的 `origin/master`; `git -C aria show 301641b:skills/phase-d-closer/SKILL.md` sha256 `550f33b7dfc5d50dd441507df1b24aa6131671e45b8a888daba072ce211ab547`) — 2026-09-09 由可变 ref 勘正为不可变 SHA |
| 两版 SKILL.md 差异 | **2+/2−** (B-15 那一行) |

## 记分

| eval | v_new | v_old | delta | discriminating |
|---|---|---|---|---|
| 1 `progress-update-execution` | **1/3** | **3/3** | **−2** | 2 |
| 2 `status-summary-output` | 3/3 | 3/3 | 0 | 0 |
| **合计** | **4/6** | **6/6** | **−2** | 2 |

## ⚠️ delta 为负 —— 按 E-3 的「`WITHOUT_BETTER` 逐条解释或回退」, 这里是**解释**, 不回退

### 三重独立验证: 那 2 行改动**不可能**是成因

1. **被改文本对本套件结构不可见 (最硬的一条)**: 四份答卷 grep `cli bug|cli_bug|自动修正|auto-fix|修正 CLI` —— **全部 0 命中**, 包括**仍然持有该声称**的 v_old 臂。v_old 从未把「自动修正 CLI bug」复述进输出, 所以删掉它不可能改变任何一条 expectation 的取值。
2. **prompt 只点名 D.1, 而被改的是 D.2 表格行**: 两臂都据此声明 D.2 不跑 (v_old L8 / v_new L9) —— 被改文本**连进入输出的激发条件都不具备**。
3. **两条 discriminating 的分歧维度与改动正交**: 它们是「PR/commit info 归 D.1 还是 D.2」与「未核实输入要不要采信」, 依据的是两版**逐字相同、未被 diff 触及**的 `SKILL.md L183`。

### 负 delta 的真实成因 = 已在册的 P0 断言缺陷

- v_new: `tasks_claimed: 6  # 无 tasks.md 可核, **未采信**为 completedTasks` / 「我**没有**编造 `TASK-001 ~ TASK-006` 填进去」 ⇒ **fail**
- v_old: `| completedTasks | +6 (oauth2-social-login 全部 6 项) | 按你给的 "All 6 tasks complete" |` ⇒ **pass**

即: **断言在奖励「采信用户口述的未核实输入」, 惩罚「拒绝编造」。**

这**正是** `10CG/aria-plugin#172` 已开的 P0 单: 「[P0][AB套件] phase-d-closer eval 1 断言奖励虚构 —— 拒绝编造进度的臂 0/3, 用 TASK-001~006 占位编记录的臂 3/3」。**同一个 eval, 同一个形状**, 本次为它提供了一份新的实证。

### 为什么不回退

回退 B-15 = 把「openspec-archive 会自动修正 CLI bug」这个**已不成立的跨 Skill 声称**装回 `phase-d-closer/SKILL.md`。而本 Spec 存在的理由就是删掉它 (openspec-archive 本轮改走 `git mv`, 且本仓从未安装那个 CLI)。据一条已知坏掉的断言去回退一个正确的事实订正, 是 memory `author-to-match-checker`「让内容去迁就检查器」的反面形态。

⇒ **不回退**, 逐条解释已在上, 并把本次实证追进 `10CG/aria-plugin#172`。

## 与 SC-11 的关系

SC-11 的分支 (b) 要求补跑两个套件。实测三套件矩阵:

| 套件 | v_old SKILL.md sha256 | v_new sha256 | `--numstat` | 处置 |
|---|---|---|---|---|
| `openspec-archive` | `5593508c…` | `edba8c5e…` | 63+/34− | ✅ 已跑 (E-2/E-3) |
| `phase-d-closer` | `550f33b7…` | `4b432573…` | 2+/2− | ✅ **本文** |
| `state-scanner` | `cf5257599672ee04…` | `cf5257599672ee04…` | **0+/0−** | ⛔ **两臂逐字节相同 ⇒ 结构上零信息** |

`state-scanner` 那一行**不是成本判断**: 两版 SKILL.md 逐字节相同、`description` 亦零变动 ⇒ 它的 AB 会是**两个完全一样的臂**, 跑它是 SOT §3 点名的测量剧场 (同 memory `false_green_dual_is_permanent_red`)。本 Spec 对该 Skill 只加了两个**不被其自身流程调用**的新脚本, 没动它任何一行运行时指令面。

⇒ **分支 (b) 已被满足到它物理上能产生信息的极限**; 分支 (a) 则是多做了。**无论 owner 怎么裁, Rule #6 的完备性问题都已由测量闭合。**
