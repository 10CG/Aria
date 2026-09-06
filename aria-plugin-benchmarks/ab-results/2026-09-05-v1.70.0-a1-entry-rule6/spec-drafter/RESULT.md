# RESULT — Rule #6 AB `spec-drafter` (母 Spec a1-entry-claim-duplicate-work-guard → v1.70.0)

> 对账对象: 同目录 `PREDICTION.md` (八臂派出前写死, **全程未改**)。
> **本次没有改动任何一条 eval 断言。** 唯一的制品改动是给 SKILL.md **补入** Spec 已收敛但 A.2/A.3 漏抄的内容 (见下 §制品变更)。

## 臂与制品指纹 (逐 run 可核)

| 臂 | 来源 | `SKILL.md` blob |
|---|---|---|
| `with_skill` (eval 1-5) | aria `feature/a1-entry-claim-duplicate-work-guard` @ `ab3dbd0` | `85db2a1f9f52` |
| `with_skill` (eval 6, 重跑) | 同上 + 本轮补丁 | **`ef0082a0df8b`** |
| `with_skill_prefix` (eval 6, 归档不计分) | 补丁前 | `85db2a1f9f52` |
| `old_skill` (全部) | aria master `7dd0135` (v1.69.1) 快照 | 见 `ab-workspace/.../skill-snapshot` |

会话以 `ARIA_COORDINATION_NO_PUSH=1` 启动 (子进程实测 `no_push_requested_by_env() == True`)。

## 逐 eval 结果 vs 预测

| eval | 断言 | with (预测) | old (预测) | 偏离 |
|---|---|---|---|---|
| 1 level-judgment | 2 | 2/2 (2/2) | 2/2 (2/2) | — |
| 2 bilingual-support | 5 | 5/5 (5/5) | 5/5 (5/5) | — |
| 3 linked-issue-field-authoring | 5 | 5/5 (5/5) | 5/5 (5/5) | — |
| 4 level2-location-rule5 | 4 | 4/4 (4/4) | 4/4 (4/4) | — |
| **5 claim 派生 + linked-issue** | 8 | **8/8** (8/8) | **0/8** (预 3/8) | ⚠️ old 比预测**更弱** |
| **6 overlap 按 status 请裁** | 6 | **6/6** (6/6) | **1/6** (预 2/6) | ⚠️ old 略低于预测 |

## 汇总

| 分组 | with | old | delta |
|---|---|---|---|
| 全套件 | **30/30 (100%)** | 17/30 (57%) | **+0.433** (预测 +0.300) |
| 回归臂 (1-4) | 16/16 | 16/16 | **+0.000** |
| 定向 fixture (5-6) | **14/14** | **1/14** | **+0.929** |

**回归臂零区分度 + 定向臂近满格**, 分离干净。预测的四条可证伪条件: 第 1 条 (回归 FAIL) 未触发; 第 2 条 (with 承重 FAIL) **触发过一次并已处置**, 见下; 第 3 条 (old ≥ 9/14) 未触发; 第 4 条 (delta ≤ 0) 未触发。

## 制品变更 (预测第 2 条触发后的处置)

补丁前 eval 6 的 with 臂**整段 overlap 分档缺失**, 不只是缺一行。依据:
- `proposal.md:668` 要求本落点是「**同上的**『前置: REQUIRE claim』步骤块」, 而 phase-a-planner 版含 overlap 分档;
- `proposal.md:277` 另要求「告警须含 …**双方 `linked_issue` 原始串**…」。

⇒ 判为 **A.2/A.3 派生漏抄**(与本 cycle M4 那五处同族), 按跑前写死的规则「指令面缺陷 ⇒ 回改 SKILL.md, 不改断言」补入整段 (**纯增 +12/−0, CRLF 保持** 520→532), 重跑 eval 6 的 with 臂。补前那份归档为 `with_skill_prefix/` 并附 `NOTE.md`。

## grader 挖出的套件缺陷 (进套件缺口 issue, 不是本次结果的瑕疵)

1. **eval 3 的 5 条断言对本 cycle 结构性零区分度** —— `git diff 7dd0135 ab3dbd0 -- skills/spec-drafter/SKILL.md` 是 59+/1−, **没有一行触及 `Linked Issue`**; baseline `SKILL.md:344-354` 已逐字含全部五条判据。5/5 vs 5/5 是构造上注定的, **严格说不该计入 delta 分母**。
2. **eval 3 断言 3 是断言 2 的推论** (满足 `` `none` `` 即自动无链接形且非空), 零增量信息。建议改成「有 issue 时不得写链接形」的负控。
3. **eval 3 断言 5 的 grep 面宽于它点名的缺陷** —— 字面禁全文出现「关联 Issue」, 但 `SKILL.md:354` 明文允许读取侧 alias ⇒ 一个解释得更深的臂会被**误判 fail**。本轮靠运气未触发。
4. **eval 3 唯一有真牙齿的是断言 2** —— 两版骨架都逐字印着 `{<org>/<repo>#<n>}`, 照抄骨架即 fail; 两臂都正确替换。
5. **eval 3 没测到本 cycle 的真 delta** —— with 臂整段处理 A.1 REQUIRE claim, old 臂对 claim 零提及, 而 eval 3 一条都没覆盖。

## 污染判定 (memory `ab-baseline-leaks-via-repo-corpus`)

**两臂均无仓内语料污染。** grader 独立 grep, `a1-entry` 在所有臂的回答里**零命中**; with 臂内容逐条溯源到 SKILL.md 行号 (`:84`/`:97`/`:104`/`:115-129`/`:426`), 且 `depth-1` 等特征串在母 Spec 文档里零命中 ⇒ 是技能生效, 不是泄漏。

唯一边缘事实: with 臂写「slug 与现有 7 个 change 目录无碰撞」, 实测仓内恰 7 个且含本 Spec 目录 —— 即它**列了目录名**但未读内容, 对本 eval 无影响。

## 一条反向信号 (照记)

grader 指出 old 臂在 eval 3 的 SC-4 上**反而更强** (自带「先构造坏实现确认转红」的负控要求)。这不影响计分, 但说明新版在某个维度上没有全面压过旧版, 值得在下一轮 authoring 时留意。
