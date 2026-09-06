# PREDICTION — Rule #6 AB `phase-a-planner` (母 Spec a1-entry-claim-duplicate-work-guard → v1.70.0)

> 写于八臂 (6 eval × 2 arm) 派出**之前**, memory `predict-then-measure`。事后不改本文件, 只在 RESULT.md 里对账。

## 臂与基线

- `with_skill` = aria `feature/a1-entry-claim-duplicate-work-guard` @ `ab3dbd0` 工作树
- `old_skill` = aria master `7dd0135` (v1.69.1) 快照 → `ab-workspace/2026-09-05-a1-entry-rule6/skill-snapshot/skills/phase-a-planner`
- 会话以 `ARIA_COORDINATION_NO_PUSH=1` 启动 (已核: 子进程 `no_push_requested_by_env() == True`); 协调 ref 基线 `539d231`

## 本 skill 的 hunk 与落档 (Spec rule6_note #1 / #3)

- **#1 frontmatter `allowed-tools` 加 `Bash, AskUserQuestion`** — 能力面, 判据表第二行「照跑 AB, 零裁量」⇒ eval 1/2 是回归臂
- **#3 正文新增「前置: REQUIRE claim (A.1, MUST)」块 + A.1 的 `precondition:` 指针** — 处方性 · 套件覆盖外 ⇒ eval 3-6 是本批新建的定向 fixture (7.5)

## 已知污染面 (memory `ab-baseline-leaks-via-repo-corpus`)

old 臂只是 SKILL.md 换成旧版, **仓是同一个真仓**: `openspec/changes/a1-entry-claim-duplicate-work-guard/proposal.md` 里逐字写着这些行为, 项目 CLAUDE.md 也照常加载。⇒ old 臂若去 grep 仓内在制 proposal, 可能学到目标行为。**这是本次预测最大的不确定源**, 下面每条 old 预测都按「不 grep proposal」给主值, 并标出 grep 命中时的上界。

## 逐 eval 预测

| eval | 断言数 | with | old (不 grep) | old (grep 到 proposal) | 依据 |
|---|---|---|---|---|---|
| 1 full-cycle-execution | 4 | **4/4** | **4/4** | 4/4 | 回归臂。A.1→A.2→A.3 编排两版逐字相同; 新块只是在 A.1 前多一步前置。**预期零区分度** —— 它的职责是证明没回归, 不是证明有增益 |
| 2 error-recovery | 3 | **3/3** | **3/3** | 3/3 | 同上, 该面未动 |
| 3 claim-derivation + linked-issue | 9 | **9/9** | **3/9** | 7/9 | with 臂新块逐字给了 slug+uuid 拼法、「不是 label」、哨兵一律省略整个参数、truthy 理由、Level1/enabled=false 零调用、release 义务。old 臂 SKILL.md **完全没有这个块**, 只能靠通识猜; 「不用 label」与「省略整个参数而非传哨兵」是反直觉点, 通识多半答成「传 label 也行」/「传空串」 |
| 4 overlap 按 status 请裁 | 6 | **6/6** | **2/6** | 5/6 | with 臂有四档表 + 「不要释放对方 claim」+ 「abandoned 可能是 GC 产物」。old 臂大概率能想到「问一下人」(1 条), 但 `unknown` 视同 active、`abandoned` 的 GC 来源这两条是本 Spec 独有推理 |
| 5 degraded 说「未能核实」 | 5 | **5/5** | **2/5** | 4/5 | 「两者不是同一个意思」从 JSON 本身可推 (给 old 1-2 条); 但「未能核实」这个**措辞字面**与「不得用 `.get(k,0)` 读」是 with 臂独有 |
| 6 unattended 零 AskUserQuestion | 5 | **5/5** | **1/5** | 4/5 | 最反直觉的一条: 判据取自 config 字段而**不是**运行期探测「AskUserQuestion 可不可用」。old 臂几乎必然答成后者 |

## 汇总预测

- 断言总数 **32** (4+3+9+6+5+5)
- `with_skill` **32/32 = 100%**
- `old_skill` **15/32 ≈ 47%** (不 grep) / 上界 **27/32 ≈ 84%** (grep 到在制 proposal)
- **delta 预测 +0.53**, 污染情形下可能压到 **+0.16**

## 可证伪的失败预期 (若实测与此不符, 说明预测错了, 照记不改 eval)

1. **with 臂任一 eval 3-6 的 [承重] 断言 FAIL** ⇒ 新块写了但 AI 没照做 ⇒ 是指令面缺陷, 不是 eval 问题, 须回改 SKILL.md 而非改断言
2. **old 臂 eval 6 ≥ 3/5** ⇒ 说明「config 字段 vs 运行期探测」这条通识就能答出, 该 fixture 区分度不足, 记入套件缺口 (aria-plugin#117 同族)
3. **eval 1/2 任一臂 FAIL** ⇒ 回归! `allowed-tools` 扩权或新块挤占了编排注意力, 必须查
4. **delta ≤ 0** ⇒ 不改 expectations 迁就、不降级, 原样上呈 owner (Rule #10)

## 与 AB 手册的验收挂钩

跑完须核 (手册 §场景 1 第 2 条): 任一臂 transcript 里若出现 `phase1_gate` / `release_gate` 的 JSON, 必须含 `"push_skipped": true, "push_skipped_reason": "env_var"`; 见到 `false` ⇒ 该 run 作废。另: 全部跑完后 `git ls-remote origin refs/aria/coordination` 必须仍等于基线 `539d231`。
