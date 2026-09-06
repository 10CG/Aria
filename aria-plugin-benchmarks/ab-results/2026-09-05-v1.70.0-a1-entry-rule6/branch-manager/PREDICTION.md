# PREDICTION — Rule #6 AB `branch-manager` (母 Spec a1-entry-claim-duplicate-work-guard → v1.70.0)

> 写于四臂派出**之前**。事后不改本文件, 只在 RESULT.md 对账。

## 本 skill 的 hunk 与落档

rule6_note **#8**: `branch-manager/SKILL.md:149` 命令行占位串同步 (标题 `Part A1` **不改** —— 那是已 ship Spec 的部件名, 非 Phase A.1)

**实读 diff**: **单行改动**: `<carry-id>` → `<A.1 认领时派生的那一串>`

## 臂与基线

- `with_skill` = aria `feature/a1-entry-claim-duplicate-work-guard` @ `ab3dbd0`
- `old_skill` = aria master `7dd0135` (v1.69.1) 快照
- `ARIA_COORDINATION_NO_PUSH=1` 已核; 协调 ref 基线 `539d231`

## ⚠️ 预测的核心: 本套件**结构上测不到**本轮改动

判据表把这类 hunk 落在第二行「处方性 · 运行时指令面 / **能** / 照跑 AB, 零裁量」, 所以**必须跑** —— 这是义务, 不是为了拿分。但跑之前就能看出: 改动面与 eval 覆盖面**不相交**。

⇒ **预测 delta = 0, 且这不是失败**。它是「照跑」义务被履行完毕后得到的一个真实结论: **该套件对本类改动零敏感**。这条要写进套件缺口 issue, 而不是被解读成「改动没用」。

**若实测 delta ≠ 0**, 说明我这个「不相交」判断错了, 要回头查是哪条断言意外碰到了改动面 —— 那反而是有信息量的意外。

## 逐 eval 预测

| eval | 断言 | with | old | 依据 |
|---|---|---|---|---|
| 1 simple-feature-branch-creation | 2 | **2/2** | **2/2** | 测的是 feature 分支创建, 与 claim 命令行占位串无交集 |
| 2 module-identifier-validation | 1 | **1/1** | **1/1** | 测的是模块标识符枚举, 更加无关 |

## 汇总预测

- 断言总数 **3**
- `with_skill` **3/3 (100%)** · `old_skill` **3/3 (100%)**
- **delta 预测 0.000** —— 见上方「结构上测不到」

## 可证伪的失败预期

1. **任一臂 FAIL** ⇒ 与本轮改动无关的既有缺陷 (或采样波动), 照记并查, **不改断言**
2. **delta ≠ 0** ⇒ 我的「不相交」判断错了, 回查是哪条断言碰到了改动面
3. **两臂都低分** ⇒ 该 eval 本身有问题 (恒假断言 / 语料不匹配), 进套件缺口
