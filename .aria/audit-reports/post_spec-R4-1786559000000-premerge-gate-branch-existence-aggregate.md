---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-12T18:40:00.000Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_spec R4 汇总 — Spec A `premerge-gate-branch-existence` (**max_rounds 走满**)

## 投票

| 席位 | VOTE | VERDICT | C+M+m | 阻塞 B | R3-fix 引入 |
|---|---|---|---|---|---|
| tech-lead | REVISE | PASS_WITH_WARNINGS | 0+6+5 = 11 | 5 | 10 |
| code-reviewer | REVISE | PASS_WITH_WARNINGS | 0+4+7 = 11 | 2 | 10 |
| qa-engineer | REVISE | PASS_WITH_WARNINGS | 0+2+1 = 3 | 2 | 3 |
| knowledge-manager | **PASS** | PASS_WITH_WARNINGS | 0+0+3 = 3 | 0 | 3 |
| **backend-architect** | **PASS** | **PASS** | **0+0+0 = 0** | 0 | 0 |

**3 REVISE / 2 PASS** · 原始 **0C + 12M + 16m = 28** · 9 条 `blocks_phase_b` ·
R3-fix 引入 **26/28 = 93%**。**一席给出完整 `PASS` (零 findings)** —— 四轮首次。

## 四轮轨迹 — 最清晰的一张图

| 轮 | 投票 | 原始 | **Critical** | **fix 引入率** |
|---|---|---|---|---|
| R1 | 5R/0P | 26 | **6** | — |
| R2 | 3R/2P | 23 | **0** | 74% |
| R3 | 4R/1P | 24 | **0** | 79% |
| R4 | 3R/2P | 28 | **0** | **93%** |

**⇒ 两个同时为真的事实**:
1. **Critical 连续三轮为 0** —— B 侧 post_planning 四轮 (3→1→2→3) **从未做到**;
2. **引入率升到 93%** —— **28 条里 26 条是上一轮 fix 新造的**。这个循环现已**几乎纯自生成**。

Major 14 → 12 (略降), 但那是在 26/28 由自己新造的前提下的"降"。

## 与 B 侧并列 (八轮总数据)

| | Critical 轨迹 | 引入率轨迹 |
|---|---|---|
| **B 侧** post_planning R1-R4 | 3 → 1 → 2 → **3** | — → 53% → 70% → 71% |
| **A 侧** post_spec R1-R4 | 6 → **0 → 0 → 0** | — → 74% → 79% → **93%** |

**拆分买到了严重度天花板, 没买到收敛; 且引入率比 B 侧更高。**

## 🔴 R4 抓到一条编排层漏执行的 owner 裁定 (第 15 条错误)

**DEC-20260812-001 §5.3** (owner 裁定, 状态 Approved) 逐字:
> 「B 的 `detailed-tasks.yaml` 删去迁往 A 的任务时**须留 cancelled 痕迹, 不得静默删**」

实测: `grep -n 'cancelled' B/detailed-tasks.yaml` = 2 处, **均属 TASK-020 条件触发纪律, 与迁移无关**;
逐条解析 21 条 task ⇒ **全部 pending**, 其中 **TASK-003/004/005/007/008/009 六条的规格已整体过户给 A**。

而 A 的处置逐字是「A 本轮不改 B (跨轨改会撞车) ⇒ 列为 A 的 **D.2 handoff 必写项**」
—— **把 owner 裁定的 A.1 迁移动作自行降级成了 handoff 备忘**, 且 A 全文对 DEC **§5 零引用**
⇒ owner 在 D-a/D-b/D-c 三个待裁点上**看不到它**。

**后果 (席位逐字)**: B 的实施者拿到七条 pending 且规格已迁走的任务, 按 B `tasks.md:77` 去实现
⇒ **第二份 `_verify_branch_exists` 定义 / merge conflict** —— 正是 A 自己写下的那个后果。

✅ **已补执行** (owner 已批准的动作, 非新决定): B 的 6 条标 `status: cancelled` + 逐条 notes 留痕
(⛔ 不得再实现 + 指向 A 侧承接) + `metadata.audit_state` 追加拆分说明。
实测 status 分布: **pending 15 / cancelled 6**, 21 条一条未删, 字段数恒 12。

## 其余承重 Major (择要)

- **「移入 `## Success Criteria` ⇒ 路径 B 必然出六条 TASK」在 delegate 处不成立** ——
  `DUAL_LAYER_SPEC.md:90-93` 把三项**各带用途**分派, `## Success Criteria` 的落点是**每条 task 内的
  `verification:` 字段, 不是 task 本身**; 实跑 `grep -rn 'Success Criteria' task-planner/` = 仅 2 命中,
  **全 skill 无一句把 SC 条目转成 TASK**。且 A 实测 `^## What$` = 0 且 `^### Key Deliverables` = 0
  ⇒ **路径 B 文档化的两个任务源章节 A 一个都没有**。
  ⇒ 最小修法 = 删掉「必然」, 保留祈使句形态 (A.2 执行者义务, **无机械闸门**) ——
  才与 A 自己 O-1 列写的「有机械闸门吗: **没有**」自洽。
- **`§非目标:844` 仍逐字要求 R3 已作废的 landmine 标注** —— 同一陈述**四个落点只改了三个**
  (memory `fix-the-class`, **在它本轮诊断出同款病的同一轮里同时犯**)。
- **Level 定档的 (b)「跨模块」腿仍是自造判据** —— `LEVEL_GUIDE.md:153-163` 逐字给出**四条件 OR 列表**,
  A 评估的「落在几个文件/几个 skill」**一个字都不在四条里**; 其中条件 3「需要 API 契约变更」
  A 自己要给 `gate_check()`/`_build_output` 加形参、给 schema 加键 ⇒ **可能 YES**。
- **Level 的 (c)「Breaking」腿是版本定档的函数, 而 A 明文判两者「不得合并处理」** ⇒
  owner 分两次裁可能产出**违反 `LEVEL_GUIDE.md:29/:162` 的档位组合** (Breaking=YES 而 Level=2)。
  修法: D-c 加依赖声明 + 把「不得合并」收窄为「**不得混为一题, 但须按序裁: 先版本, 后 Level**」。
- **【复核执笔方预判 ①】只有 1/3 对** —— 「折叠后行首编号是否保留」确实不可断言 (诚实标注正确),
  但由此推出 `SC-A-step (a)(b)` **整体**无法断言, 是**把非承重量的不可测当成了承重量的不可测**:
  顺序有与折叠形态无关的测量点 (按出现位置断言三个内容锚的相对次序)。
  ⚠️ **这正是执笔方本轮在 (c-含) 上亲自走通的第三条路 —— 同一份文件同一轮里一处走通一处没走。**

## 处置 — `max_rounds` 结构性耗尽 (A 侧)

`max_rounds` = 4 **已用 4**。`converged: false` (3 REVISE; 收敛要求全席 PASS)。
⇒ 按 audit-engine §降级策略 **触发 `AskUserQuestion` 三路径选择**。
frontmatter 保持 `degraded: false` —— 那是路径 [3] 被选中后的结果, AI 不得预先落章。

**A 侧 Phase B 仍被本闸门阻断** (9 条 `blocks_phase_b`)。Rule #10: AI 不得自行豁免。

### 交给 owner 的判断材料

**八轮数据 (两条轨各四轮) 支持一个明确结论**:

> **拆分把「严重度」压住了 (A 侧 Critical 连续三轮 0, B 侧从未做到), 但没有改变「总量稳态」,
> 且 A 侧引入率 (93%) 比 B 侧 (71%) 更高。**

⇒ 若目标是「**不带 Critical 进 Phase B**」—— **A 已连续三轮达标**, 且本轮有一席给出完整 PASS;
⇒ 若目标是「**收敛 (全席 PASS)**」—— **四轮数据不支持"再加轮能到"**: 引入率 74→79→93% 单调上升,
   意味着**每一轮 fix 的产出几乎全部是它自己制造的新条目**。

---

## 🔨 owner 裁定 (2026-08-13, 经 `AskUserQuestion` 三路径选择)

**选定路径 [2] — 增加轮次: `max_rounds` 4 → 6。**

- AI 的建议是 **[1] 接受当前结论 → 进 Phase B** (依据: Critical 连续三轮 0, 一席完整 PASS);
- **owner 选 [2]**, 覆盖该建议。⇒ 继续 R4-fix → R5, 余 2 轮。
- 先例: 本 Spec 拆分前的 post_spec 亦曾由 owner 把 `max_rounds` 4→6 (用 5 余 1)。

⚠️ **AI 对该裁定的诚实提示 (已在选项里给出, 此处留痕)**: 四轮引入率 74%→79%→**93%** 单调上升,
R4 的 28 条里 **26 条是上一轮 fix 自己新造的**。**再加轮的预期产出是「换一批同量级 Major」而非收敛。**
若 R5 引入率仍 ≥ 90%, 建议届时重新评估路径 [1]/[3]。

**本轮 R4-fix 的重点据此调整**: 优先清 **9 条 `blocks_phase_b`** 与**非自生成的那 2 条**,
对「修了会引入更多」的条目**如实说不修并给理由** —— 在引入率已达 93% 的前提下,
少改比多改更可能降低下一轮的条数。
