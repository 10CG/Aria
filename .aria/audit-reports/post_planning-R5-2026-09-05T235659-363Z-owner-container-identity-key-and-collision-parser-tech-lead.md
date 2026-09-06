---
checkpoint: post_planning
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-05T23:56:59.363Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R5 (max_rounds, 最后一轮) — tech-lead 席

审计对象: `proposal.md` v11 + `tasks.md` v5 + `detailed-tasks.yaml` v5 @ master `984c4e9`, v4→v5 / v10→v11 diff 逐 hunk 实读。未修改仓内任何文件; 只跑只读命令与 scratchpad 脚本。

本轮镜头 (按席位职责): 1 = R4 我的 M-1 (a)(b)(c) 是否逐一闭合且新措辞不引入新矛盾; 2 = 三向一致性终审 + TASK-018 新机械锁与 S2-1 注释翻转的配对性; 3 = 计划结构是否被 v5 扰动。

## v5 的实际改动面 (diff 实读, 三处)

| 文件 | hunk | 性质 |
|---|---|---|
| `proposal.md` | Status 行 v11 + `:120` T11 + `:132` SC-7 + `:134` SC-9 | 四行文本 (三行是 R4 M-1 处置) |
| `tasks.md` | 头 3 行版本/审计指针 + `:62` (2.7) + `:98` (S2-1 行) | 文本 |
| `detailed-tasks.yaml` | `:2` / `:16` 头注 + `:45-46` (TASK-027 预留项) + `:361` (TASK-018 verification) | 文本 |

零 `dependencies` / 零 `parent` / 零 id / 零 checkbox 改动 —— 与 `tasks.md:5` 自述「计划结构不变」一致, 我用机械实算复核 (下节)。

---

## R4 处置核对

### 我的 M-1 三处 — 三处全部 closed

| 支 | v10 原文 (R4 证据) | v11 现文 (实读) | 判定 |
|---|---|---|---|
| **(a)** SC-9 `:134` 尾句 | 「`RECOMMENDATION_RULES.md:31` 今日无取值字面, **加 `identity_advisories` 一句后满足**」— 与同行首句的两 token 要求互否 | 「`RECOMMENDATION_RULES.md:31` **今日两 token 均无, 须同时补 `cross_owner` 与 `identity_advisories` 才满足首句**」 | **closed**。事实前提我重跑核实: `sed -n '31p' aria/skills/state-scanner/RECOMMENDATION_RULES.md` 对 `cross_owner` / `identity_advisories` 的 `grep -c` 均为 **0**, 「两 token 均无」成立; 「才满足首句」把门槛显式绑回首句, 行内矛盾消失。与 `tasks.md:71` (3.4)「与 SC-9 首句对齐」、`yaml:442` deliverable 注、`yaml:447` TASK-024 verification 四处同文 |
| **(b)** T11 `:120` 时点 | 尾括注「merge 后、归档前执行」覆盖整行, 把 `#174` 征求 ack 也写成 merge 后 ⇒ 与 `:104` 的 S2 激活条件 (ack 在 merge 前) 互否 | 「两个时点: **B.1 起手** (tasks.md 0.2) #174 留言…征求 ack (S2 激活前提之一, 见上表 :104 行); **merge 后、归档前** (tasks.md 5.5) 回帖 #193 / aria-plugin#135…关 #193」 | **closed**。映射逐条实核: `tasks.md:38` = 0.2 征求 ack ↔ `yaml:84-97` **TASK-040 `parent: "0.2"`**, `dependencies: [TASK-000]`, notes「ack 是 S2 激活前置」; `tasks.md:87` = 5.5 merge 后回帖 ↔ `yaml:614-626` **TASK-038 `parent: "5.5"`**, `dependencies: [TASK-039, TASK-040]`。`:120` 新引的自指行号 `:104` 我实核为 proposal 第 104 行 = 「与 a1-entry 的边界与两种 ship 形态」行, 指向正确 |
| **(c)** SC-7 `:132` 「文件」限定 | 「本 Spec 新建测试**一律**写 TestCase」(无 carve-out) ⇒ 与 `yaml:32` / `tasks.md:78` 的 `test_collision.py` pytest carve-out 互斥 | 「本 Spec 新建测试**文件**一律写 TestCase 以归 (a) 覆盖; 对 `test_collision.py` 的新增用例沿用该文件的 pytest 风格, **计入 (b) 的 passed 基数**」 | **closed**, 且比我建议的更严 —— 末半句把 carve-out 直接接到 `TASK-032` verification 的 (b) 门槛「`passed ≥ 16 + 本 Spec 在该文件新增数`」(`yaml:502`) 上, 三层 (SC / tasks.md `:78` / yaml `:32`+`:502`) 现在读法唯一 |

### R4 其余 finding 的三态

| finding | 三态 | 依据 |
|---|---|---|
| 我的 m-1 (TASK-018 反向 grep 锁字面不可执行) | **closed (语义腿) / 残留见 m-1** | `yaml:361` 改为两条正向锁, 我用候选注释串实跑验证: 建议原句「label 当前仍参与协调身份 (设了会换身份), 后续版本改为仅展示; 建议留空」下, `grep -c 当前仍参与协调身份` = 1 (第一条过), `grep -c 仅展示` = 1 == `grep -cE "仅展示.*(后续|将)|(后续|将).*仅展示"` = 1 (第二条过)。**不再自我命中**, R4 假红问题解决。残留只在括注的字面 shell 形态 (本轮 m-1) |
| CR R4 m-3 (S2-1 未含 `identity.py` 注释翻转) | **partial** | `yaml:45-46` / `tasks.md:98` 已加「同 PR 改写注释为『label 仅展示』(撤销 TASK-018 的 S1 措辞与机械锁)」+ verification「注释区间不再含『当前仍参与协调身份』」—— **注释这一半对上了**, 但同一个 S1/S2 翻转还有第二半 (`test_identity_label.py` 的 S1 lock-in **测试**断言) 未配对 ⇒ 本轮 M-1 |
| 我的 m-2 (发布顺序导读行漏 5.4 / 5.8) | **open (连续第二轮未处置)** | `tasks.md:81` 与 `yaml:520` 实读仍是七项序, 5.4 / 5.8 仍缺; R4 聚合的 minor 处置表未收录本条 (m4 行把我的两条 minor 记成了别的内容) ⇒ 判为漏进 rework 清单而非被否 |
| KM R4 carry (S2 激活 handoff 记录未绑 TASK-027) | **open (设计如此)** | `tasks.md:103` 仍为「并在 handoff 记录激活时点」, 与 R4 处置意图一致 |

三态计数: **closed 4 · partial 1 · open 2 (1 条设计如此)**。

---

## 三向一致性终审 (proposal v11 ↔ tasks.md v5 ↔ yaml v5)

| 同步点 | proposal v11 | tasks.md v5 | yaml v5 | 判定 |
|---|---|---|---|---|
| SC-9 rule 1.54 门槛 | `:134` 首句两 token / 尾句「须同时补齐才满足首句」 | `:71` (3.4) 两 token「与首句对齐」 | `:442` / `:447` 两 token | **一致** |
| SC-9 文档面基数 | `:134` 「六处取值文档」(七处减 `templates/session-handoff.md`) | `:71` 列五个可改文件 + `SKILL.md` 不改动 | `TASK-024` 五 deliverable + 「`SKILL.md:149-154` diff 零」 | **一致**。第六处 = `SKILL.md`, 其交集非空**无须改动**即成立: 我实读 `SKILL.md:149` 含 `self_multi_container` (与 `cross-owner` 连字符形), 交集非空判据先天为真 |
| T11 两时点 | `:120` B.1 起手 / merge 后归档前 | `:38` (0.2) / `:87` (5.5) | TASK-040 `parent 0.2` / TASK-038 `parent 5.5` | **一致** |
| T11 与 S2 激活前提 | `:120` 指 `:104`; `:104` = S2-candidate + ack + merge 前 | `:103` 激活规则同三条件 | `metadata.s2_followup.activation` 同三条件 | **一致** |
| 双跑法 carve-out | `:132` 文件级 + `test_collision.py` pytest, 计入 (b) 基数 | `:78` (4.2) 文件级 + 两条命令 + 双基数 | `:32` `metadata.test_runner` + `:502` TASK-032 双基数 | **一致** |
| TASK-018 机械锁 | (SC 层不写 grep, 只有 T3 `:111` 「注释改写」) | `:62` (2.7) 两条 grep 同文 | `:361` 两条 grep 同文 | **一致** (SC 层松于任务层, 不矛盾) |
| S2-1 注释翻转 | SC-3 `:128` **仅 S2** 臂只写 flip / #135 时间线 / 发布门, **无注释子句** | `:98` S2-1 含注释翻转, 验收列注「不再含『当前仍参与协调身份』」, 但列头写「验收 (proposal SC-3 S2 臂)」 | TASK-027 title/verification 同 `tasks.md:98` | **可接受的单向超集**: SC-3 的 S2 臂没有「恰/仅/一律」等全称词, 加一条断言不构成互否; 但列头把该列冠名为「proposal SC-3 S2 臂」而实际是其真超集 —— 记为下方 M-1 的附带面, 与 M-1 同一处修法一并解决 |
| S1 lock-in ↔ S2 flip | `:128` **仅 S1** 「`get_container_id()` 在 label 非空时**仍**返回 label」/ **仅 S2** 「返回 uuid」 | `:49` (1.8) 「label accessor + S1 lock-in」; S2 表零提及 | `TASK-008:219` lock-in 断言; `TASK-018:360` 「S1 lock-in 仍绿」; TASK-027..030 零提及 | **不配对** ⇒ **M-1** |
| 发布顺序导读 | (proposal 不写序) | `:81` 七项 | `:520` 七项 | **与拓扑实算不一致** (漏 5.4 / 5.8) ⇒ m-2 (carry) |

除 M-1 外, 本轮未发现 v5/v11 新引入的读法冲突。

---

## 计划结构 (与 R4 同口径机械实算; 确认 v5 未改动结构)

scratchpad `dag5.py` 对 v5 实跑:

- 任务 39 / id 唯一 39 / `metadata.total_tasks: 39` 三方相等; `parent` 唯一无重复
- 依赖全部可解析 (unresolved = 空); 拓扑 len 39 ⇒ **无环**
- 总工时 **83.0h**; agent 实计 `backend-architect 15 · qa-engineer 15 · knowledge-manager 9` == `metadata.agents`
- `tasks.md` checkbox 实测 **39**, 与 yaml `parent` 集合**双向零差** (对称差为空)
- 预留 id `TASK-027..030` 零占用
- 传递闭包: `closure(TASK-034)` = **32**, 含 `TASK-000` 与 `TASK-040` (S2 激活「判定与留言必须在 merge 前」的机械承载仍在); `closure(TASK-039)` = **36**, 闭包外恰 `TASK-038` / `TASK-042` 两个 merge 后动作
- 三文件带圈数字 / 希腊字母命中集合均为空

全部数字与 R4 (v4) 逐项相同 ⇒ **v5 未扰动 DAG / 闭包 / 计数 / 编号**, 自述属实。发布顺序与激活/回退条款的结论与 R4 相同, 不重复展开 (CLAUDE.md 多远程硬约束 1+2 由 `tasks.md:83` / `:85` 承载; 4.3 排在 5.7 之后是结构必需, 非对闸门改序; 回退条款与 Rule #10 同向不冲突)。

---

## Findings

### M-1 (major · issue · testing) — S1/S2 翻转只配对了「注释」这一半: `test_identity_label.py` 的 S1 lock-in 断言在 S2 下必红, 且 flip 后无强制重跑回归的边

- **scope**: `detailed-tasks.yaml:43-46` (`s2_followup.items` TASK-027) · `tasks.md:98` (S2-1 行) · `detailed-tasks.yaml:41` (`activation`) · 对照面 `proposal.md:128` (SC-3) · `detailed-tasks.yaml:219` (TASK-008 verification) · `detailed-tasks.yaml:498` (TASK-032 dependencies)
- **summary**: v5 按 R4 CR m-3 给 S2-1 补了「同 PR 改写注释 + 撤销 TASK-018 机械锁」。但 S1→S2 翻转在计划里锁了**两处**同一事实, 不是一处: 注释 (TASK-018) 与**测试断言** (TASK-008 的 lock-in)。v5 只写了注释那处。测试那处在 S2 下与 flip 直接互斥, 且没有任何 DAG 边保证 flip 之后重跑回归。
- **evidence** (全部实读, 已 grep 全仓三文件确认无第二处提及):
  - `proposal.md:128` SC-3 把两臂写成互斥的同一函数断言: 「**仅 S1**: lock-in 断言 `get_container_id()` 在 label 非空时**仍**返回 label (S1 不得偷 flip, 否则 a1-entry SC-3 静默恒绿)」/「**仅 S2**: `get_container_id()` 返回 uuid」。
  - 该 lock-in 的落点是 `TASK-008` (`parent 1.8`), `yaml:219` verification: 「SC-3 S1: label 非空时 `get_container_label()` 返回 label **且 `get_container_id()` 仍返回 label (lock-in)**」, 交付物 `tests/test_identity_label.py` (`yaml:216`)。它是**基础 39 项之一**, S1/S2 两形态都会执行并勾选。
  - S2 侧全部四项 (`yaml:43-58` TASK-027..030) 与 `tasks.md:98-101` 逐字实读: 只有 TASK-027 提到 `identity.py:126-140` **注释**, 无一处提到 `test_identity_label.py` / lock-in 用例。`grep -n "lock-in\|test_identity_label" proposal.md tasks.md detailed-tasks.yaml` 命中 6 行, 全部在 S1 侧 (`tasks.md:49` / `proposal.md:128` / `yaml:209,216,219,360`), S2 侧零命中。
  - 顺序面: `TASK-032` (4.2 全套回归, SC-7「零失败」) `dependencies: [TASK-020, TASK-017, TASK-019, TASK-011, TASK-016]` (`yaml:498`) —— 不含 TASK-027..030。激活规则 (`yaml:41`) 只说「追加 TASK-027..030 (**接入 TASK-034 前置**)」, 即 flip 与回归并列挂在 merge 之下、**彼此无序**。
- **两种执行后果 (均为坏)**: (1) 回归先跑、flip 后落 ⇒ merge 时 `run_tests.py` 的真实状态未被任何门检验过, SC-7「零失败」拿的是 flip 前的证据 —— 属 memory `feedback_completion_signals_vs_runtime_invocation` 那一类假绿; (2) flip 先落、回归后跑 ⇒ `test_identity_label.py` 稳定红, 而计划没告诉执笔者「这条红是预期的、该怎么改」, 执笔者要么临场删断言 (删的正是 `proposal.md:128` 明写用来防「偷 flip」的守卫, 且删除动作无 owner 留痕), 要么误判为回归而回退 flip。
- **为何是 major 而非 minor** (与 R4 把注释那一半判 minor 的口径对齐后仍升一档): 注释锁失配的后果是一条 grep 假红, 人读即知; 这一条的后果是**测试套件真红或回归证据失效**, 且触到的是本 Spec 自己写明的防伪守卫。R4 的 M-1(b) 判 major 的理由是「让 S2 分支在结构上不可达」, 本条同类 —— 让 S2 分支在结构上**不可绿**。
- **为何不是 critical**: S2 当前不可达 ——`proposal.md:11` 实读 a1-entry「待 B.1」, 故 `TASK-000` 大概率判 S1, S2 表整体转为 `5.8` 的 tracker issue。不阻断 B.1 起手, 也不影响 S1 形态下任何 checkbox。
- **但不能留到 B 期**: `tasks.md:90` (5.8) 明写 tracker issue「含激活条件与 **S2-1..S2-4 原文**」—— 缺口会被原样复制进那张长期 issue, 成为跨 cycle 的遗留。修在这里是两行, 修在 tracker 上要重开一轮。
- **建议** (两处定点编辑, 零 DAG / 零编号 / 零 checkbox 影响):
  1. `yaml:45` TASK-027 title 末尾 + `tasks.md:98` S2-1 内容列末尾补: 「并改写 `tests/test_identity_label.py` 的 S1 lock-in 用例 (断言由『`get_container_id()` 仍返回 label』翻为『返回 uuid』), 撤销 SC-3 仅 S1 臂」; `yaml:46` verification 补「`test_identity_label.py` 在 flip 后全绿」。
  2. `yaml:41` `activation` 末尾补一句顺序约束: 「TASK-027 落地后必须重跑 TASK-032 (4.2 两跑法) 并以重跑结果作为 SC-7 证据」; `tasks.md:103` 同文。
  3. 顺带把 `tasks.md:96` S2 表列头「验收 (proposal SC-3 S2 臂)」改为「验收 (proposal SC-3 S2 臂 + 本表附加)」, 使冠名与实际内容 (已含注释与测试两条 SC-3 之外的断言) 相符。

### m-1 (minor · issue · documentation) — TASK-018 机械锁的括注 grep 表达式按字面不可执行 (缺引号与 `-E`)

- **scope**: `detailed-tasks.yaml:361`
- **summary**: 两条锁的**散文腿**已可机械执行 (我实跑验证, 见上文 R4 处置表), R4 m-1 实质关闭。残留的是同一条 verification 尾部那个「即 …」括注: 写作 `grep -c 仅展示 == grep -c 仅展示.*(后续|将)|(后续|将).*仅展示`, 逐字丢进 shell 会被当成管道 + 子 shell。
- **evidence**: 实跑 `bash -c 'grep -c 仅展示.*(后续|将)|(后续|将).*仅展示 cand.txt'` → `bash: -c: line 1: syntax error near unexpected token '('`。正确形态需引号 + `-E`: `a=$(grep -c "仅展示" F); b=$(grep -cE "仅展示.*(后续|将)|(后续|将).*仅展示" F); [ "$a" = "$b" ]` —— 这条我实跑得 `a=1 b=1 equal=yes`, 语义无误。
- **为何仍是 minor**: 括注以「即」引出, 是对散文腿的记法说明, 不是待执行命令行; 散文腿本身无歧义, B 期照它写出的 grep 就是对的。但它落在 memory `feedback_sot_example_commands_are_never_executed` 点名的形态 (写进文档的示例命令从未实跑), 一行可清。
- **建议**: 把括注换成上面实跑过的带引号 `-E` 形, 或直接删括注只留散文腿。

### m-2 (minor · issue · documentation · carry) — 发布顺序导读行 (两处) 仍漏 5.4 与 5.8, R3 提出、R4 重申, v5 第二轮未动

- **scope**: `tasks.md:81` · `detailed-tasks.yaml:520`
- **summary**: 两处导读仍为「5.2 bump → 5.1 merge+tag → 5.3 → 5.7 → 4.3 → 5.6 PR → 5.5 回帖」, 而 v5 拓扑实跑序是 `… 5.2 → **5.4** → 5.1 → 5.3 → 5.7 → 4.3 → 5.6 → 5.5 → **5.8**`。漏的两项一个是外发前的公开性闸 (`TASK-037` fixture 无邮箱/token/内网地址), 一个是 R2 M-1 整个处置的落点 (`TASK-042` S2 tracker 承载体)。
- **evidence**: 两行实读原文如上; 拓扑序取自本轮 `dag5.py` 对 v5 的实算 (与 v4 逐项相同)。R4 聚合的 minor 处置表未收录本条 —— 我核对了 R4 聚合 m4 行, 它把我的两条 minor 概括成了「proposal :104 与 T11 交叉引用措辞 / SC-7 括注长度」, 与我 R4 报告的 m-1/m-2 原文不符, 故本条属**漏进 rework 清单**, 不是被判为不必改。
- **为何仍是 minor**: `tasks.md:33` 明写「顺序由 yaml deps 定」, deps 是 SOT, 导读行不参与任何机械判定。
- **建议**: 两行各补两项与拓扑序对齐 (B.1 首个提交顺手带走)。

---

## Counts

**0C / 1M / 2m** (Critical 0 · Major 1 · Minor 2)。

明确回答席位职责的收束问题: **无 Critical**; **有 1 个 Major** (新, 非 R4 carry) —— 故不能写「无 Major」。R4 的三支 M-1 全部闭合, 且闭合未引入新的读法冲突; 本轮 Major 是 v5 对 R4 CR m-3 的**半幅处置**暴露出的另一半, 属同一处翻转的配对缺口。

## Vote

**PASS**

理由:

1. **R4 的全部 Major 已实证闭合**, 且是靠可核事实闭合的, 不是靠措辞: (a) 的事实前提我重跑 `grep -c` = 0/0; (b) 的两时点我逐条比对到 `TASK-040 parent 0.2` / `TASK-038 parent 5.5`; (c) 的 carve-out 现在接到了 `TASK-032` (b) 的门槛公式上。
2. **计划结构连续第三轮零缺陷**, 且本轮实算与 v4 逐项相同 (39 / 83.0h / topo 39 / closure 32 与 36 / checkbox 双向零差 / 预留 id 干净 / 禁用符号零)。v5 声称的「计划结构不变」经机械核实属实。
3. **本轮 Major 不阻断 B.1**: 它落在 S2 分支, 而 `proposal.md:11` 实读 a1-entry 仍「待 B.1」⇒ `TASK-000` 大概率判 S1, S2 表整体走 `5.8` tracker; S1 形态下 39 个 checkbox 无一受影响。修法是两行定点编辑 + 一处列头冠名, 零 DAG / 零编号影响, 可随 B.1 首个提交带走 —— 与 R4 三支的处置成本同量级。
4. **不建议再加轮**: 本轮唯一 Major 的根因不是「计划没想清楚」, 而是「同一处翻转的第二半没被点名」; 它已被点名并给出逐字修法。R5 是 max_rounds, 按算法呈 owner 三选一时, 我的执笔建议是**接受 (option 1) 并把 M-1 与两条 minor 列为 B.1 入口的 rework 清单**, 不再开 R6: 再开一轮的期望产出是又一份「三行定点编辑」清单, 收益低于流程成本, 且第五轮已连续三轮无结构性缺陷。

---

## 轮次记录

| 轮次 | 席位 | 结论 | 备注 |
|------|------|------|------|
| R1 | tech-lead | FAIL (2C / 5M / 2m) | 归档门 `deferred-s2` 机制不存在 + `plugin-cache-currency` 不可绿 |
| R2 | tech-lead | PASS_WITH_WARNINGS (0C / 4M / 4m) | Critical 归零; v2 引入两个新结构面 |
| R3 | tech-lead | PASS_WITH_WARNINGS (0C / 1M / 4m) | 计划层首次零结构性缺陷; vote REVISE |
| R4 | tech-lead | PASS_WITH_WARNINGS (0C / 1M / 2m) | 命令逐字实跑关闭 PP3-C1; Major = v10 三处新措辞内部矛盾; vote PASS |
| R5 | tech-lead | PASS_WITH_WARNINGS (0C / 1M / 2m) | R4 M-1 三支全 closed (含事实前提重跑); 结构实算与 v4 逐项相同。Major = S1/S2 翻转只配了注释半幅, `test_identity_label.py` lock-in 与 flip 后回归重跑未配对 (新, 非 carry)。minor: TASK-018 括注 grep 字面不可执行 (实跑 syntax error) / 发布导读行漏 5.4+5.8 (连续第二轮 carry)。严格判据集合 R5 ≠ R4 (Major 从 documentation 簇变为 testing 簇) ⇒ 预期 MAX_ROUNDS_EXHAUSTED, `converged=null` 交编排层判。全部 finding 附实读 file:line 或实跑输出; 未触碰任何仓内文件 |

**B 期顺手项 (不构成 finding, 与 R4 同, 未被 v5 处置且不必在计划里处置)**:
- S2 若激活, 除追加 6.1-6.4 / TASK-027..030 外还须同步 `metadata.total_tasks` (39→43) 与 `metadata.agents` 三个计数。
- `TASK-033` 两条 verification 都依赖 handoff 内容, 在其自身时点不可自验; 按「记入待写 handoff 的 owner action 清单」处理。
- `tasks.md:46` (1.5) 的 `` `aaaa1111` `` 仍是 backtick 形, D.2 gate 符号 liveness 会稳定给一条 `ambiguous` unverified_claim (warn, 不 block)。
- `TASK-016` (2.5) 与 `TASK-020` (2.9) 编辑 `track_board.py` 相邻区域且 DAG 无先后约束; 并行分派需注意落地顺序。
- `TASK-018` 规定的注释措辞是中文, 而 `lib/identity.py:126-140` 现有模板文本 (`# Aria container identity …` / `# Edit the \`label\` line …`) 全英文, 该文件仅 `:183` 一行含中文。机械锁的 token 是中文字面 ⇒ B 期照锁写就会在这段生成给用户的 `~/.aria/container-id` 头注里混入中文。不构成 finding (锁本身自洽, 本仓多个 lib 文件亦有中文), 但落地时值得决定是中文、英文还是双语 —— 若改英文, 两条 grep 的 token 需同步换。
