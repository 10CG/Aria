---
type: owner_decision_sheet
subject: 10CG/Aria#199 Phase B 组 1 (1.3 fixture 矩阵审查) 的 spec 漂移裁定 (SC-2 的 F-b 样本 / SC-7(b) 的集合 C / SC-22(2) 的 WARN 文案) 与三处执行口径
spec_ids: [pre-merge-completeness-gate-change-scope]
status: decided
decided_by: owner
decided_at: 2026-09-30
created: 2026-09-30
container: simonfish/bfe8285d
---

# 决策单 — 2026-09-30: 10CG/Aria#199 组 1 的 spec 漂移 (等待点 3)

> **来由**: owner `/goal` 直驱本轨 Phase B。1.3 (TASK-003) fixture 矩阵经只读审查 (21 条意见) 后, 修正实例逐条核实: 19 条成立并落进矩阵, 2 条判为 spec 漂移 (hard_constraints 第 13 条 / `owner_gates` 第 3 项), 另留 3 处执行口径给主控。主控对照 proposal 原文与冻结语料独立核实后, 经 AskUserQuestion 两次呈报 (第 1 – 4 项; 矩阵第三轮审查后的第 5 项) (选项由 AI 列出并逐项写明代价, 推荐项标明为 AI 推荐)。本单是这些裁定的权威记录。
> **授权范围**: 本单只含裁定, 不含外向动作。

---

## 1. SC-2 的 F-b 样本 —— 按 SC-2 自带兜底规则 (c) 降下界

- **事实 (主控核实)**: `corpus-freeze.md` §3.1 为 id `state-scanner-inter-cycle-surfacing` 冻结的 3 份 F-b 样本, 文件名全以 `pre_merge-` 开头; `pre_merge` 是 Step 3 的固定排除项 (裁定 1 的五项之一), 门的纳入集与统计面都不含它 ⇒ 这 3 份经命令行在 `results` 与两个计数里结构上都观测不到, SC-2 (i) 对 F-b 的归属断言在正确实现上必红。换 id 重采走不通: 对冻结语料 (F = 主仓 `8d2ff8b`) 按「可纳入 checkpoint + 两列一致」统计, 同一 id 同时有 F-a 与 F-b 的 **0 个** (连各 ≥1 的都没有)。
- **裁定**: 走 SC-2 原文的兜底 (「若 Phase B 发现某族仍不足下界, 走规则 (c) 兜底, 不得自造样本」): 这 3 份标为「不可用 —— pre_merge 属固定排除项, 门结构上不报告」并记名; F-b 下界按实测上限降为 **0**; SC-2 (i) 用 F-a / F-c / F-d 验归属判定, (ii) 照旧验 F-e / F-f 三桶两两不交。
- **依据**: SC-2 原文的两条反事实 (规则 2 退回纯中缀 ⇒ F-a 少计; 按第 4 段取 spec_id ⇒ `A1-` 与 `R5.5` 形态少计) 分别由 F-a 与 F-d 承载, 不依赖 F-b。
- **代价**: 真实语料里的 role 后缀形态不进 SC-2; 同形的「`-<id>-`」中缀由 F-c (`…-<id>-aggregated.md`) 与其余 SC 的手造 fixture 覆盖。`corpus-freeze.md` 要补一节记录本裁定 (由未参与实现的实例执笔), 原标注保留作溯源。

## 2. SC-7(b) 的集合 C —— 在 C 里再加 `aria-orchestrator`

- **事实 (主控核实)**: SC-7(b) 原文「`C` 含 `aria-orchestrator-divestiture` 而不含 `orchestrator`, `--change-id orchestrator` → exit 2 `change_id_unanchored`; 反事实: 用 `pre-write-validation.md:25` 的裸 glob `archive/*-orchestrator/` → 判有锚 → 落 `missing` → 红」。C 若只含 `aria-orchestrator-divestiture`, 裸 glob `*-orchestrator` 同样匹配不到 (目录名以 `-divestiture` 结尾), 反事实实现也判无锚 ⇒ 该格对它自己写的反事实没有区分力。§1.1 S1 自己举的命中例子是 `2026-…-aria-orchestrator`。
- **裁定**: fixture 的 C 同时含 `aria-orchestrator-divestiture` 与 `aria-orchestrator` (后者按 S1 的例子放在 `openspec/archive/<日期>-aria-orchestrator/` 下并带 `proposal.md`)。原文「C 含 `aria-orchestrator-divestiture` 而不含 `orchestrator`」仍逐字成立, 期望值不变; 裸 glob 实现会命中 `aria-orchestrator` 而判有锚, 反事实由此可测。
- **代价**: fixture 多一个归档目录。

## 3. 三处执行口径 —— 照主控口径

主控按原文定, owner 确认 (不属漂移; 作为主控判断记入台账, 周期 handoff 列入待复议清单):

1. **SC-4 截断格**: 构造 unattributed 总数**恰为 22** 的 fixture。原文「同一 fixture 另造 22 份」的另一读法 (在主 fixture 已有的 1 份上再加 22 份, 共 23 份) 与同句期望值 `unattributed_count == 22`、「全 22 项」、「其余 2 份」冲突, 不成立。
2. **SC-9(2) 第一跑**: 原文两处给了两份字面 config —— R4 的「两跑」那份 (`checkpoints: {post_spec: 'convergence', post_planning: 'off'}`, 同旗标即 `allow_incomplete_checkpoints: true`) 与 R5「锁短路」逐字给的那份 (`checkpoints: {post_spec: 'convergence'}`, `allow_incomplete_checkpoints: true`); 两份都在格 `SC-9.2-S4-bypassed-manual` 内跑, 期望相同 (`verdict == 'bypassed'`、`error_kind is None`、exit 0、`checked_checkpoints == ['post_spec']`)。只跑后一份会丢掉前一份才测得到的「值为 off 的键不收」。
3. **SC-15(5)**: 保留原文「每条 `results` 的 `enabled_by == 'mode:convergence'`」断言。读前必看第 6 条只把 checkpoint 列表、`len(results)` 与 missing 对数由四改为三, 并写明 fixture 不变, 没有删这条; TASK-006 第 2 条的摘要漏写了它, 以 proposal 原文为准。

## 4. 落档方式 —— 记本决策单与台账, 计划不出新版

- **裁定**: 本单为权威记录; 台账「停下与上报」一节引用本单; 之后组 1–4 的派单直接带上本单。计划 (`tasks.md` / `detailed-tasks.yaml`) 不出 v2.11。
- **代价**: `tasks.md` 读前必看里没有这几条, 后续执行者须同时读本单。
- **执行注**: `.aria/decisions/` 在 `metadata.commit_attribution` 里属他轨路径, 本单的提交到 5.8 会被判 `foreign`、停在 `owner_gates` 第 16 项请 owner 确认一次 (fail-closed, 预期内)。

## 5. SC-22(2) 的 WARN 文案 —— 按 §1.4 全文断言 (第二次呈报, 同日)

- **事实 (主控核实)**: 1.3 矩阵第三轮只读审查指出: SC-22(2) 原文写 stderr 含「`[WARN] .aria/audit-reports/ 不存在`」, 同句括注称「与 §1.4『报告目录不存在』的 WARN 全文对齐」; §1.4 (proposal `:281`) 与 TASK-012 第 2 条规定的实际输出是「`[WARN] completeness gate: .aria/audit-reports/ 不存在, 按零报告评估`」—— 前者不是后者的子串, 按字面写子串断言会让正确实现误红。
- **裁定**: 测试断言 stderr 含 §1.4 的整行 WARN (`[WARN] completeness gate: .aria/audit-reports/ 不存在, 按零报告评估`)。SC 原文那段读作 §1.4 那一行的简写 —— 它的括注本就指向 §1.4 全文; 期望值仍取 spec 字面, 只是取 SC 自己点名的那份全文。
- **代价**: SC-22(2) 原文那段简写不按字面使用。

## 落地记录 (2026-09-30)

| 项 | 落地 | 核验 |
|---|---|---|
| 1 | `corpus-freeze.md` 补记本裁定 (未参与实现的新实例执笔); 矩阵 SC-2 行改写 | 矩阵第二轮只读审查 |
| 2 | 矩阵 SC-7.b 行改写; 1.5 测试按此造 fixture | 同上; RED 审查 |
| 3 | 矩阵相应三行按上文改写 | 同上 |
| 4 | 本单 + 台账「停下与上报」 | — |
| 5 | 矩阵 SC-22.2 行按 §1.4 全文改写; 1.6 测试按此断言 | RED 审查 |
