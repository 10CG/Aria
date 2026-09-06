# PREDICTION — Rule #6 AB `spec-drafter` (母 Spec a1-entry-claim-duplicate-work-guard → v1.70.0)

> 写于十二臂 (6 eval × 2 arm) 派出**之前**。事后不改本文件, 只在 RESULT.md 对账。

## 臂与基线

- `with_skill` = aria `feature/a1-entry-claim-duplicate-work-guard` @ `ab3dbd0`
- `old_skill` = aria master `7dd0135` (v1.69.1) 快照
- 会话 `ARIA_COORDINATION_NO_PUSH=1` (已核 `no_push_requested_by_env() == True`); 协调 ref 基线 `539d231`

## 本 skill 的 hunk 与落档 (Spec rule6_note #2 / #4)

- **#2 frontmatter `allowed-tools` 加 `Bash`** — 能力面, 第二行「照跑 AB, 零裁量」⇒ eval 1-4 是回归臂
- **#4 正文新增「前置: REQUIRE claim (A.1, MUST)」块** (59 行) — 处方性 · 套件覆盖外 ⇒ eval 5-6 是定向 fixture (7.5(b))

**与 phase-a-planner 版的实质差异 (实读 diff, 非照抄 Spec)**: spec-drafter 版**没有 Level 1 例外** —— 块内逐字写「直调路径没有 Level 判定, 因此本块无 Level 1 例外」, 并多一段「幂等分工」说明只在 (a) 未经 phase-a-planner 直调 或 (b) 上游 skip 时才生效。⇒ eval 5 是 8 断言 (phase-a-planner eval 3 是 9, 多的那条正是 Level 1 零调用)。

## 逐 eval 预测

| eval | 断言数 | with | old | 依据 |
|---|---|---|---|---|
| 1 level-judgment | 2 | **2/2** | **2/2** | 回归臂, Level 判定段两版逐字相同。**预期零区分度** |
| 2 bilingual-support | 5 | **5/5** | **5/5** | 回归臂。含 `Linked Issue` 字段两条 —— 那是上一 cycle 已 ship 的面, 两版都有 |
| 3 linked-issue-field-authoring | 5 | **5/5** | **5/5** | 回归臂 (字段 Spec 的 fixture)。本 cycle 未动该面 |
| 4 level2-location-rule5 | 4 | **4/4** | **4/4** | 回归臂 (Level 1 批次的 fixture)。本 cycle 未动 |
| 5 claim-derivation + linked-issue | 8 | **8/8** | **3/8** | 与 phase-a-planner eval 3 同题少一问。old 臂无该块, 「不用 label」「哨兵省略整个参数」两处反直觉点大概率失手 |
| 6 overlap 按 status 请裁 | 6 | **6/6** | **2/6** | 同 phase-a-planner eval 4。`unknown` 视同 active + `abandoned` 可能是 GC 产物, 是本 Spec 独有推理 |

## 汇总预测

- 断言总数 **30** (2+5+5+4+8+6)
- `with_skill` **30/30 = 100%**
- `old_skill` **21/30 = 70%** —— 注意基数高是因为 4 个回归 eval 两臂都该满分; **区分力全部集中在 eval 5/6 的 14 条**上 (old 预测 5/14)
- **delta 预测 +0.30**
- 污染上界 (old 去 grep 在制 proposal): old 可达 26/30 ⇒ delta 压到 +0.13

## 可证伪的失败预期

1. **eval 1-4 任一臂 FAIL** ⇒ 回归! 新块或 `allowed-tools` 扩权挤占了起草注意力, 必须查而不是记账了事
2. **with 臂 eval 5/6 任一 [承重] FAIL** ⇒ 指令面缺陷, 回改 SKILL.md, **不改断言**
3. **old 臂 eval 5/6 ≥ 9/14** ⇒ 区分度不足, 记套件缺口 (aria-plugin#117 同族)
4. **delta ≤ 0** ⇒ 原样上呈 owner, 不降级不迁就 (Rule #10)

## 一个本套件独有的观察点 (非断言, 但要在 RESULT 里记)

with 臂 eval 5 若答出「本块无 Level 1 例外」这层, 说明它读到了「幂等分工」那段而不只是复制命令行 —— 这是 phase-a-planner 版**没有**的信息, 可用来判两个落点是否被当成同一块囫囵处理。
