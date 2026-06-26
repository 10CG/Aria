# AB Benchmark — session-closer (Rule #6, TASK-009)

> **Date**: 2026-06-25 | **Skill**: session-closer v1.0.0 (session-closer-synthesis)
> **Type**: capability AB (process/leaf skill) | **Runner**: /skill-creator

## 结果

| 配置 | pass_rate | evals |
|------|-----------|-------|
| **with_skill** | **15/15 = 100.0%** | explore-session-no-cycle 7/7 + multi-thread-session 8/8 |
| without_skill (baseline) | 13/15 = 86.7% | 6/7 + 7/8 |
| **delta** | **+13.3 pp** | |

## 判别性 finding

唯一 with/without 分野 = **step2 结构标记 `[候选 memory]` / `[未写下经验]`** (AC-5b):
- with_skill: 两 eval 均产出结构标记 (机械可 grep) → 经验固化可验证
- without_skill: 均无结构标记 (经验写进 prose, 不可机械确认是否提炼)

其余 assertion (未完成线程 / 四维一致 / leaf 不触发 Phase D / 同步告警) **baseline 也大多命中** —— 因 eval 场景显式描述了 closeout-worthy 内容 + agent 能力强。这是 **process skill in-repo AB 的保守下界** ([[feedback_process_vs_content_skills]]): 真实第三方使用中 (场景不显式 spell out), skill 的系统化 step1/2/3 + leaf 框架 delta 会更大。

## Rule #6 分层 (per [[feedback_rule6_framing_differs_by_skill_type]])

- **deterministic 核心** (3 脚本): 49 单测 + 真 snapshot 集成测试 = structural substitute ([[feedback_deterministic_structural_skill_rule6_substitute]])。**非 AB**。
- **deterministic 触发命中率** (AC-10a): description 工程满足 AC-9 (phase-d 删「写 session handoff」+裸「收尾」; session-closer 强绑会话词; standards §1.3 消歧矩阵)。
- **capability** (AC-10b): 本 AB, delta +13.3pp 正向。**in-repo delta>0 非硬门, owner sign-off 为准** (delta≤0 仍可 ship per AC-10b)。

## Owner sign-off

- [x] owner 审阅: capability delta 正向 (+13.3pp) + 判别项 (经验固化结构化) 有真实价值
- [x] 确认 ship v1.50.0 (owner A 2026-06-25)
