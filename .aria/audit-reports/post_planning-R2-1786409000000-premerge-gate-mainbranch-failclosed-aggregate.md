---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-11T00:35:00.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_planning R2 汇总 — premerge-gate-mainbranch-failclosed

> 被审对象 = R1-fix 后的 A.2 产物 (commit `6818773`)。R1-fix 由 **非原作者执笔** (tech-lead),
> 主 loop 只核验 —— 这是 owner 在并发轨验证过的处方, 本轮首次在本轨施用并**量化其效果**。

## 投票

| 席位 | VOTE | VERDICT | C+M+m | 阻塞 B | 由 R1-fix 引入 |
|---|---|---|---|---|---|
| tech-lead | REVISE | FAIL | 1+8+3 = 12 | **8** | 6 |
| backend-architect | REVISE | FAIL | 1+2+0 = 3 | — | 2 |
| code-reviewer | REVISE | PASS_WITH_WARNINGS | 0+5+6 = 11 | 4 | 4 |
| qa-engineer | REVISE | PASS_WITH_WARNINGS | 0+1+1 = 2 | 0 | 2 |
| **knowledge-manager** | **PASS** | PASS_WITH_WARNINGS | 0+1+1 = 2 | 0 | 2 |

**4 REVISE / 1 PASS** · verdict **FAIL** · `converged: false` · 零 spawn 失败。
原始 **2C + 17M + 11m = 30**; 去重后 **1C + ~13M**。

## ⭐ 本轮最重要的产出: 换人执笔的量化效果

本轮脚本**显式统计** `introduced_by_r1fix`, 用于实测本 Spec 五轮量化出的规律是否被打断:

| 轮次 | 执笔方 | 本轮 fix 引入的新缺陷占比 |
|---|---|---|
| post_spec R1→R5 (5 轮) | **主 loop (原作者)** | **73–100%** |
| **post_planning R1→R2** | **tech-lead (非原作者)** | **53%** (16/30) |

⇒ **规律被显著削弱, 但未被打断。**
53% 仍在 memory `feedback_audit_marginal_return_goes_negative` 的判据线上
(「本轮 fix 引入的 major 占比 > 1/2 即到拐点」)。

**且 Major 数持平** (R1 去重 12 → R2 去重 ~13), 命中 memory
`feedback_stop_adding_rounds_when_major_count_flattens`:「加轮判据是 major 数是否还在降;
major 持平 = 每轮 fix 引入约等量同形状缺陷 = 不收敛」。
**Critical 在降** (3 → 1), 这是唯一的正向信号。

## 一条 Critical (两席独立命中同一缺陷)

**TASK-020 的 fail-CLOSED 既无插入点规定, 又与 D9/§6/SC-M10 在同一输入上要求相反结果。**

- 实测 `pre_merge_gate.py`: `_normalize_config()` 是 `gate_check` 的**第一条可执行语句**,
  在 `enabled` 早退**之前**;
- Spec 为 `_verify_branch_exists` 写了 D9 + §6 + SC-M10 **三重插入点保护**, 对 TASK-020 的硬失败**零规定**;
- ⇒ 实施者把硬失败放 `_normalize_config` ⇒ `enabled=false` + legacy key 的输入按 SC-M10 应 green, 实得 fail ⇒ SC-M10 红;
  放 `enabled` 之后 ⇒ TASK-020 自己的用例红。**两个独立实施者得相反结果**;
- 受影响的正是 TASK-020 点名要保护的人群 (从 `config.template.json` 复制 legacy key 的采用方) 中
  `enabled=false` 的那部分 —— **他们的每次合并被 BLOCK**。
- backend-architect 从另一角度命中同一处: 该机制**无信号传播设计**, 最自然的实现会让 **CLI 崩溃**而非产出 `verdict=fail`
  (呼应 R1 复核已指出的「`gate_error` 全仓零消费者 / workflow-runner 只有四条臂, 无异常臂」)。

## 失效的两个形状 (tech-lead 席位的诊断, 主 loop 认可)

R2 的 fix **方向全部正确**, 失效集中在两处:

1. **只修实例不修类** —— A 条款修好了, 但它对 B 的隐含前提 (依赖边 / 插入点 / 求值时点 / 交付面) 没同步;
2. **移交给没核过的下游** —— 写「移交 TASK-X」前没去 X 核它是否真会做
   (memory `feedback_delegation_must_verify_target_actually_does_it`)。

典型实例:
- `TASK-010` 把「全量收口」移交 `TASK-008`, 而**实测 TASK-008 不传递依赖 TASK-010**
  ⇒ 合法拓扑序下 TASK-006 已把参数改必填、TASK-010 尚未补参 ⇒ 24 条 TypeError ⇒ TASK-008 的「重跑全量」必红;
- `TASK-014` 第三版验收量是**行号集合 `{:610}`**, 与同任务「行号必然位移, 不得按行号核」的禁令**自相矛盾**
  —— 该量已被换过两次, 这是第三次 (memory `redfix-change-quantity`: 换量而不是在同一个不稳定的量上打补丁);
- `TASK-015` (Rule #6 AB) 排在 `TASK-020` **之前**, 而 TASK-020 会改 `SKILL.md` 七行
  ⇒ AB 跑的 SHA ≠ ship 的 SHA; 且新入 scope 的 `config-loader` 这个 skill **没有 AB 套件、无 rule6_note、无 substitute SC**。

## 两条与 R1 无关、但阻塞 Phase B 的既存缺口

- **MAJOR 的落地面无人承接**: 发版同步 8 文件 (`plugin.json` / `marketplace.json` / `VERSION` ×2 /
  `CHANGELOG.md` / `README.md` badge / 3 份 i18n README) **全不在 `scope_repos.paths`, 全无 task**
  ⇒ 20 条任务做完后 `plugin.json` 仍是 1.65.5, 而代码里的 `will be removed in v2.0` 已被执行
  ⇒ 一个 1.65.x 版本违背了自己的承诺。且 `m6-version-badge-match` 检查比的是 badge ↔ plugin.json, 两边都没动 ⇒ **对该失效方向 fail-OPEN**。
- **SC-M12 仍只挂 spike**: 真正写进 `SKILL.md` 的那条调用**从未跨五 cwd 复跑**
  ⇒ spike 定稿正确而 TASK-011 抄错 (少候选 / 引号错位) 时, 现有断言集 (全是全文件 grep 计数) **全绿**。

## ⚠️ 编排层本轮的一处结构性错误 (主 loop 自陈)

**R1-fix 的执笔方 `tech-lead` 同时是 R2 的审计席位** —— 即**它审了自己写的东西**。

这与 owner 裁定「换人执笔」所依据的 memory
`feedback_author_and_verifier_must_differ_for_corrections` **直接冲突**。
成因: R2 席位编制取自 `config.audit.teams.post_planning` (5 席固定), 而我从同一名单里选了执笔方。

**实际结果与担心相反** —— tech-lead 席位是本轮最严厉的一席 (12 findings / 8 阻塞 /
**主动把 6 条归因为自己 R1-fix 引入**)。但**结构性冲突不因结果好而消失**:
下一轮的执笔方必须从 R2 席位之外选, 或明确记录该席位在下一轮回避。

## 轮次记录

| 轮 | 席位 | vote | 去重 | 阻塞 B | fix 引入占比 | converged |
|---|---|---|---|---|---|---|
| R1 | 5 | 4 REVISE / 1 PASS | 3C + 12M + 8m = 23 | 6 | — | false |
| R2 | 5 | 4 REVISE / 1 PASS | **1C + ~13M** | **12** | **53%** | **false** |

`max_rounds` = 4, 已用 **2**。

## 处置建议 (须 owner 裁)

三条数据指向同一结论: **继续「fix → 审计」同形循环不会收敛。**
(Critical 3→1 在降 · Major 12→13 持平 · fix 引入占比 53% 仍过半)

tech-lead 席位的处方值得采纳且与 memory `feedback_fixes_contradict_each_other_across_clusters` 一致:
> **不是再换人, 而是在 fix 后加一道机械的条款间交叉检查。**

⇒ 建议 R2-fix 采取两点结构性改变 (而非再来一轮同形 fix):
1. **换非 R2 席位的执笔方** (修上述结构性冲突);
2. **fix 后强制跑一遍机械交叉检查** —— 至少覆盖: DAG 依赖边 vs verification 里点名的移交对象 ·
   每条 SC 的 owning task 是否交付测试文件 · 每条断言的量是否随实施位移 · 插入点是否被多条条款同时管辖。

**Phase B 当前被本闸门阻断** (12 条 `blocks_phase_b: true`, 含一条两个实施者得相反结果的 Critical)。
按 Rule #10, AI 不得自行豁免该阻断。
