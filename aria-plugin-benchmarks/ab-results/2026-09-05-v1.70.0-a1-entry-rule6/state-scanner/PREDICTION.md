# PREDICTION — Rule #6 AB `state-scanner` (母 Spec a1-entry-claim-duplicate-work-guard → v1.70.0)

> 写于 26 臂 (13 eval × 2 arm) 派出**之前**。事后不改本文件, 只在 RESULT.md 对账。

## 臂与基线

- `with_skill` = aria `feature/a1-entry-claim-duplicate-work-guard` @ `ab3dbd0`
- `old_skill` = aria master `7dd0135` (v1.69.1) 快照
- `ARIA_COORDINATION_NO_PUSH=1` 已核; 协调 ref 基线 `539d231`

## 本 skill 的 hunk 与落档 (Spec rule6_note #5 / #10b / #12)

- **#5 `SKILL.md` 新增「Layer L A.1 heartbeat 集成」小节** (触发条件一句 + CLI 一行 + fail-soft 一句 + 指针) — 处方性 · 运行时指令面 ⇒ 第二行「照跑 AB, 零裁量」+ **在既有套件内新增 1 个 eval (id 13)** 钉点名行为 (d)
- **#12 `:168` 输出键集补 `push_skipped` / `push_skipped_reason`** — 描述性 ⇒ substitute 走结构化断言 (Group 6 已做), 不指望 AB 测出
- **#10b `references/layer-l-integration.md` 新增设计段** — 处方性, 与 #5 同一次照跑覆盖

## ⚠️ 本套件的结构性特点 (必须先说, 否则会误读结果)

**13 个 eval 里只有 eval 13 能区分两臂。** 其余 12 个 (78 断言里的 **72 条**) 覆盖的是 collector / 输出区块 / 同步检测等本 cycle **完全没动**的面 —— 它们是**回归臂**, 职责是证明没坏, 不是证明有增益。

⇒ 即使 eval 13 满分横扫, **聚合 delta 的理论上限也只有 6/78 ≈ +0.077**。**不能**因为 delta 小就说「这次改动没用」; 判据要落到 **eval 13 单独的 6 条**上。这一点写在跑之前, 免得事后拿聚合数字做任何方向的文章。

## 逐 eval 预测

| eval | 断言数 | with | old | 依据 |
|---|---|---|---|---|
| 1 basic-state-collection | 3 | 3/3 | 3/3 | 回归臂, 未动 |
| 2 user-options-display | 2 | 2/2 | 2/2 | 同上 |
| 3 readme-sync-detection | 3 | 3/3 | 3/3 | 同上 |
| 4 config-awareness | 3 | 3/3 | 3/3 | 同上 |
| 5 submodule-sync-detection | 6 | 6/6 | 6/6 | 同上 |
| 6 upstream-behind-detection | 6 | 6/6 | 6/6 | 同上 |
| 7 issue-awareness-opt-in | 8 | 8/8 | 8/8 | 同上 |
| 8 readme-skill-count-badge | 8 | 8/8 | 8/8 | 同上 |
| 9 forgejo-config-detection | 7 | 7/7 | 7/7 | 同上 |
| 10 multi-remote-parity-drift | 12 | 12/12 | 12/12 | 同上 (最大的一条, 也最可能出现随机波动) |
| 11 submodule-push-github-sync-miss | 9 | 9/9 | 9/9 | 同上 |
| 12 (未命名) | 5 | 5/5 | 5/5 | 同上 |
| **13 a1-heartbeat-on-entry (新)** | **6** | **6/6** | **1/6** | with 臂新小节逐字给了 `--heartbeat-only` 命令行、「刷新既有 claim 而非新认领」、`enabled==false` 零调用、遥测走独立分区。old 臂 SKILL.md **完全没有这一节** —— 它大概率会答成「跑 phase1_gate 认领」或「跑完整闸门」, 那正好命中第 5 条负向断言 |

## 汇总预测

- 断言总数 **78**
- `with_skill` **78/78 = 100%**
- `old_skill` **73/78 ≈ 94%**
- **delta 预测 +0.064** (= 5/78) —— 小, 但**这是设计使然**, 见上面的结构性说明
- **真正的判据: eval 13 = with 6/6 vs old 1/6**

## 可证伪的失败预期

1. **eval 1-12 任一臂 FAIL** ⇒ **回归**! 新小节挤占了扫描/展示的注意力, 必须查根因, 不能记账了事
2. **with 臂 eval 13 任一 [承重] FAIL** ⇒ 新小节写了但 AI 没照做 ⇒ 指令面缺陷, 回改 SKILL.md, **不改断言**
3. **old 臂 eval 13 ≥ 4/6** ⇒ 该行为通识就能答出, fixture 区分度不足, 记套件缺口
4. **两臂在 eval 10 (12 断言) 出现不对称波动** ⇒ 优先怀疑 flaky 而非真实差异, 需复跑该条再下结论
