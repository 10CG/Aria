---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: false
oscillation: false
overridden_by_user: true
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-13T02:30:00.000Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

> ## 🔴 owner override (2026-08-16)
>
> **owner 明确裁定「接受当前结论, 直接进 A.2」** ⇒ `overridden_by_user: true`。
> `converged` 保持 **false** (它是事实, 不因 override 改变); `degraded` 保持 false
> (按 audit-engine SOT, `degraded: true` 是降级路径 [3] 被选中后的结果, 本次不是)。
>
> **override 时 A 侧仍未闭合 4 条 `blocks_phase_b`** (M-4 Level 条件① 与 M-5 版本定档
> 已由 [DEC-20260816-002](../../docs/decisions/DEC-20260816-002-fix-first-outcome-oriented.md) 的定档方向解决, 余 4 条):
> M-1 `CLAUDE.md:113` 规则 #8 同步归属 (回到未裁) · M-2 B 的 `TASK-013` 与 A 的 hunk ②③ 是同一份交付物 ·
> code-reviewer M-2 `SC-A-doc` 锚点定位规则未推广 · knowledge-manager 一条。
> **这 4 条被带进 A.2**, 须在任务清单里显式承接或显式声明不承接。
>
> **max_rounds 6 仍余 1 轮未用** —— override 不消耗它; 若 A.2 之后需要, 该轮仍在。

# post_spec R5 汇总 — Spec A (owner 加轮后的第 1 轮, max_rounds 6 已用 5)

## 投票

**5 REVISE / 0 PASS** · 五席 verdict 全 `PASS_WITH_WARNINGS` · 原始 **0C + 16M + 10m = 26** ·
6 条 `blocks_phase_b` · R4-fix 引入 **19/26 = 73%**。

| 席位 | C+M+m | 阻塞B | 引入 |
|---|---|---|---|
| tech-lead | 0+6+4 = 10 | 4 | 7 |
| code-reviewer | 0+3+3 = 6 | 1 | 5 |
| knowledge-manager | 0+3+2 = 5 | 1 | 4 |
| backend-architect | 0+2+1 = 3 | 0 | 2 |
| qa-engineer | 0+2+0 = 2 | 0 | 1 |

## ⭐ 「少改」策略的实测效果 — 执笔方预测的记分卡

| 量 | 预测 | 实际 | |
|---|---|---|---|
| **引入率** | 70–85% | **73%** | ✅ **命中** |
| Critical | 0 | **0** | ✅ 命中 |
| 总数 | 14–20 (点估 17) | **26** | ❌ 低估 |
| Major | 5–8 | **16** | ❌ **低估一倍** |

**⇒ 结论有两半**:
1. **「少改」确实把引入率从 93% 压到 73%** —— 触点 25→12 的效果**可测且如预测**;
2. **但总数没降** —— 因为席位这轮**挖到了更深的结构层**: **7/26 (27%) 是非自生成的**,
   且其中两条动摇的是本 Spec 的**定档根基**(见下)。

⇒ **前四轮的高引入率掩盖了一批更深的既存问题**; 少改让它们浮出来了。这不是坏事, 但它意味着
**"条数"这个量在策略变化时不可跨轮比较** —— 该比的是**引入率**与**非自生成条数**。

## 🔴 两条动摇定档根基的发现 (均非自生成)

### 1. 版本定档 MINOR **全程未过成文 SOT**, 而 owner 的选项集被 AI 预先收窄

A §版本 全节理由逐字只有「全部为 additive … API 形状层零破坏面」, **零引用** `CLAUDE.md:79`
与 `standards/conventions/version-management.md`。

`CLAUDE.md:79` 逐字:「新增 Skill / Skill 架构重构 = **MINOR+**; 文档更新 / **bug 修复 = PATCH**」
—— A **既非新增 Skill**, 又已在 Level (a) 腿**自答「架构变更 = NO」** ⇒ **落不到 MINOR+ 桶,
逐字落进 PATCH 桶**。`version-management.md:52-55`/:67-70 两条触发条件**同时命中且 SOT 无优先级规则**。

⚠️ 而 A `:165` 逐字规定「**先版本 (MINOR vs MAJOR), 后 Level**」—— **题面只有两个选项**,
任何照 SOT 逐字求值的裁定者得到的是**第三个选项 PATCH, 它不在选项集里**
⇒ **owner 在被 AI 预先收窄的选项集上作第一顺位裁定**。

> 对照: B 侧 `detailed-tasks.yaml` 的 `ship_target` 字段**做了字段级对账**
> (「CLAUDE.md:35 与 :79 两条下界求交唯一解」), **A 没做**。

### 2. Level 条件 ①「涉及 2 个及以上模块」的求值也是自造谓词

A `:18` 逐字「① = NO (代码面全在 phase-c-integrator **一个 skill** 内)」。
而 `LEVEL_GUIDE.md:127-151` 的模块映射是 **mobile / backend / shared / standards 四模块**,
「**skill**」一个字都不在里面。逐字求值: 路径侧 `aria/skills/**` 对五个前缀**零命中 ⇒ 不可判**;
关键词侧**同时命中 standards** (Skill/规范/文档) **与 backend** (Python/API) ⇒ **≥2 模块**
⇒ 条件① **YES** ⇒ `:162` 逐字「**自动提升为 Level 3**」。

⇒ **D-c 的题面应是「条件① 与 ③ 两条待裁」而非一条** —— A 自己为条件③ 立的规矩逐字是
「成文条件的解释问题, **不是 AI 的裁量空间**」, **同一规矩未施于 ①**。

## 🔴 「改法欠定」这个不修理由被证伪

R4-fix 拒修 `SC-A-step (a)(b)` 的核心理由是「**新步骤锚 token 今日不存在, 改法欠定**」——
而**同一 Spec 的 `SC-A-step (c-含)` 已钉死一个必然出现在新步骤正文里的 token: `#137`**。
实跑: `grep -c '#137' SKILL.md` = **0** (今日零命中 ⇒ A ship 后唯一, **baseline-failing 成立**);
`grep -c '#137' B/proposal.md` = 9 但**逐行实读全部是 issue 归属讨论, 无一要求写进 SKILL.md**
⇒ B 正确落地**也不引入第二个**。另两锚在 §C.2.4 内唯一。

⇒ **今日即可写成确定形式**: 按出现位置断言 `resolve_ci_backend < #137 < evaluate_path_coverage`,
配「§C.2.4 内首个匹配」—— **该规则本轮刚由 `SC-A-note` 现成写下**。

⇒ 三条理由里**只有一条属「欠定」而那一条不成立**, 实际支撑不修的**只剩两条价值/风险评估**
—— 正是它声明自己**没有**在做的那件事。

## 🔴 编排层第 17 条错误 (主 loop 自陈, 已补执行)

我为 DEC §5.3 把 B 的 6 条标 `cancelled`, **但没处理指向它们的依赖边**:
实测 `TASK-011→003` (B 的承重 D1) · `012→009` · `013→009` · `016→008` · `020→009` ·
`021→[008,009]` (终局全量收口) **共 6 条悬空边**。
⇒ 「依赖已 cancelled」在 B 的执行编排里**无定义** ⇒ 两个独立执行者得相反结果。

✅ **已补执行**: 6 条 pending 任务就地声明调度语义 ——
「**cancelled 前置视同已满足**(不阻塞调度, 因交付物由 A 承接), 但**不得据此认为该前置的内容已在 B 内可用**」。

**另一条同源**: `TASK-013` (pending, deliverables=`SKILL.md`) 与 A 的 hunk ②③ **是同一份交付物**
—— 我的过户普查总体是「规格**整体**过户的六条」, **TASK-013 是部分重叠, 未被覆盖**。

## 处置

`max_rounds` **6 (owner 加轮), 已用 5, 余 1**。`converged: false` (5 REVISE)。
A 侧 Phase B 仍被阻断 (6 条 `blocks_phase_b`)。

### ⚠️ 建议在用掉最后一轮之前先裁两件事

R5 表明 **D-c/版本定档的题面本身是错的**:
- 版本选项集缺 **PATCH** (SOT 逐字可达);
- Level 条件 **①** 与 ③ 同样是「成文条件的解释」, 却只上呈了 ③。

**在这两件被裁定之前跑 R6, 审的是一个定档前提可能被推翻的对象** ——
若裁 PATCH 或 Level 3, R6 与 R5 的条数不可比, 且 §Impact/发版同步面/O-1 整段推导都要重来。
