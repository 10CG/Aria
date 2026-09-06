# SCORES — Rule #6 AB `a1-entry-claim-duplicate-work-guard` → v1.70.0

> 脚本从各臂 `grading.json` 直接汇总, **不经人工转述**。`-rep2/-rep3` 是采样稳定性复跑, 不计入总分。

> ⚠️ **回归臂的分数没有效度** —— 见 `DEFECTS.md` A 节: 89 条回归断言中大量恒真, 另有 4 处**奖励错误 / 惩罚正确**, 1 处单侧承重污染。该列数字**不可**读作「已验证无回归」或「新版略差」。

## phase-a-planner

| eval | 类别 | with | old |
|---|---|---|---|
| eval-1-full-cycle-execution | 回归 | 4/4 | 4/4 |
| eval-2-error-recovery | 回归 | 3/3 | 3/3 |
| eval-3-a1-claim-derivation-and-linked-issue-TA | **定向** | 9/9 | 3/9 |
| eval-4-a1-overlap-ask-user-by-status-TARGETED | **定向** | 6/6 | 3/6 |
| eval-5-a1-degraded-says-unverified-TARGETED | **定向** | 5/5 | 3/5 |
| eval-6-a1-unattended-no-ask-TARGETED | **定向** | 5/5 | 4/5 |

## spec-drafter

| eval | 类别 | with | old |
|---|---|---|---|
| eval-1-level-judgment | 回归 | 2/2 | 2/2 |
| eval-2-bilingual-support | 回归 | 5/5 | 5/5 |
| eval-3-linked-issue-field-authoring-TARGETED | 回归 | 5/5 | 5/5 |
| eval-4-level2-proposal-location-rule5-TARGETED | 回归 | 4/4 | 4/4 |
| eval-5-a1-claim-derivation-and-linked-issue-TA | **定向** | 8/8 | 0/8 |
| eval-6-a1-overlap-ask-user-by-status-TARGETED | **定向** | 6/6 | 1/6 |

## state-scanner

| eval | 类别 | with | old |
|---|---|---|---|
| eval-1-basic-state-collection | 回归 | 3/3 | 3/3 |
| eval-10-multi-remote-parity-drift | 回归 | 9/12 | 7/12 |
| eval-11-submodule-push-github-sync-miss | 回归 | 5/9 | 3/9 |
| eval-12-unnamed-12 | 回归 | 5/5 | 5/5 |
| eval-13-a1-heartbeat-on-entry-TARGETED | **定向** | 6/6 | 2/6 |
| eval-2-user-options-display | 回归 | 2/2 | 2/2 |
| eval-3-readme-sync-detection | 回归 | 3/3 | 2/3 |
| eval-3-readme-sync-detection-rep2 | 复跑 | 3/3 | 2/3 |
| eval-3-readme-sync-detection-rep3 | 复跑 | 3/3 | 2/3 |
| eval-4-config-awareness | 回归 | 3/3 | 3/3 |
| eval-5-submodule-sync-detection-new | 回归 | 3/6 | 3/6 |
| eval-6-upstream-behind-detection-new | 回归 | 2/6 | 4/6 |
| eval-7-issue-awareness-opt-in-new | 回归 | 4/8 | 4/8 |
| eval-8-readme-skill-count-badge-check | 回归 | 5/8 | 5/8 |
| eval-9-forgejo-config-detection | 回归 | 6/7 | 7/7 |

## phase-b-developer

| eval | 类别 | with | old |
|---|---|---|---|
| eval-1-branch-creation-flow | 回归 | 3/3 | 1/3 |
| eval-2-test-verification | 回归 | 3/3 | 1/3 |

## branch-manager

| eval | 类别 | with | old |
|---|---|---|---|
| eval-1-simple-feature-branch-creation | 回归 | 2/2 | 2/2 |
| eval-2-module-identifier-validation | 回归 | 1/1 | 1/1 |

## phase-d-closer

| eval | 类别 | with | old |
|---|---|---|---|
| eval-1-progress-update-execution | 回归 | 0/3 | 3/3 |
| eval-2-status-summary-output | 回归 | 3/3 | 3/3 |

## 汇总 (不含复跑)

| 分组 | with | old | delta | 效度 |
|---|---|---|---|---|
| **定向 fixture (7 条)** | **45/45** (100%) | 16/45 (36%) | **+0.644** | ✅ 断言含否定/字面串, 有牙齿 |
| 回归臂 | 85/110 (77%) | 82/110 (75%) | +0.027 | ❌ **无效度**, 见上方警告 |
| 合计 (仅供存档) | 130/155 | 98/155 | +0.206 | ⚠️ 混合了有效与无效度两部分 |

## 结论

**唯一可援引的数字: 定向 fixture delta = +0.644** (with 45/45 vs old 16/45)。
三个套件各自成立 (phase-a-planner / spec-drafter / state-scanner), 不靠单条撑起。

**回归判定**: 无回归**迹象**, 但**未被有效测试**。依据是主控手工横向比对 (五 eval 输出特征对照 + eval 3 七样本), 非断言产出。两者的区别写死在此。
