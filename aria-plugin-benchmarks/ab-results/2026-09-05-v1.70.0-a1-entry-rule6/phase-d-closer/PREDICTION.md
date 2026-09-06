# PREDICTION — Rule #6 AB `phase-d-closer` (母 Spec a1-entry-claim-duplicate-work-guard → v1.70.0)

> 写于四臂派出**之前**。事后不改本文件, 只在 RESULT.md 对账。

## 本 skill 的 hunk 与落档

rule6_note **#9**: `phase-d-closer/SKILL.md:51-52` 调用模板 + `:55` 说明句的 carry-id 口径 (`:56` 的 `STALE_TTL` 误写属既有缺陷, **不在本 Spec 改**, 已开 aria-plugin#163)

**实读 diff**: 占位串 `<本 cycle 的 carry-id 原始串>` → `<A.1 认领时派生的那一串>`, 说明句同步

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
| 1 progress-update-execution | 3 | **3/3** | **3/3** | 测的是 D.1 进度更新, 与 D.2b release 的占位串无交集 |
| 2 status-summary-output | 3 | **3/3** | **3/3** | 测的是收尾摘要格式, 同样无交集 |

## 汇总预测

- 断言总数 **6**
- `with_skill` **6/6 (100%)** · `old_skill` **6/6 (100%)**
- **delta 预测 0.000** —— 见上方「结构上测不到」

## 可证伪的失败预期

1. **任一臂 FAIL** ⇒ 与本轮改动无关的既有缺陷 (或采样波动), 照记并查, **不改断言**
2. **delta ≠ 0** ⇒ 我的「不相交」判断错了, 回查是哪条断言碰到了改动面
3. **两臂都低分** ⇒ 该 eval 本身有问题 (恒假断言 / 语料不匹配), 进套件缺口
