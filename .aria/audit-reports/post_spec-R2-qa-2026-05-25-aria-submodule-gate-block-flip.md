# post_spec R2 audit — aria-submodule-gate-block-flip (qa-engineer)

**Date**: 2026-05-25
**Auditor**: qa-engineer agent (R2)
**R1 verdict**: REVISE (2 Critical, 4 Important, 6 Minor)
**R2 verdict**: PASS_WITH_WARNINGS
**Convergence judgment**: 两个 Critical 均已实质性关闭。Rev1 对 C-1 和 C-2 的修复是 substance-level 而非 paper-fix——C-1 不仅替换了关键词，还在 schema 中增加了 `total_gate_executions` 字段并提供了清晰的数据来源推算路径；C-2 新增了完整的 §标注操作流程 sub-section，覆盖了标注时机 / owner / 操作方式 / 判定依据 / null-pending 处理，满足 Level 2 R2 unanimous PASS_WITH_WARNINGS baseline。所有 4 条 Important 也已处理（I-3 / I-4 为完整修复，I-1 / I-2 以 schema + 框架修改充分覆盖）。引入 1 条新 Minor，不影响收敛判定。

---

## R1 Critical issue closure verification

### C-1 minimum-observation guard 语义歧义

**Rev1 changes observed**:
1. §决策框架 trigger B 条件从 `WOULD-BLOCK events >= 3` 改为 **`total_gate_executions >= 3`**，并在括号中明确注释 `NOT WOULD-BLOCK events — per R1 QA C-1 + parent L234 原文`，直接锚定了修复依据。
2. trigger C 对应条件从 `WOULD-BLOCK events < 3` 改为 **`total_gate_executions < 3`**，逻辑对称一致。
3. §观察期数据 schema 新增 **`total_gate_executions: <int>`** 字段，位置在 `total_would_block` 之前（即 CRITICAL fields 首位），并附带了完整的数据来源注释：
   - 数据来源：`warns.jsonl 行数 + blocks.jsonl 行数 + overrides.jsonl 行数 + misses.jsonl 行数 + (total_pr_merges_in_window - 已 telemetry PR count) 推算 PASS 数`
   - 明确标注 `触发 trigger B/C minimum-observation guard 条件`
4. §Why 第一段 inline 文本也同步更新，括号注明 `不是 WOULD-BLOCK events — 详见 §决策框架 trigger B note`，形成 Why→What→How 三处一致性。
5. Phase B step 0 计算说明同步改为 `计算 total_gate_executions (= 上述 4 个 jsonl 行数总和 + 无事件 PR 推算 fallback)`。

**Paper-fix antipattern 验证**:
不是关键词替换。逻辑变化是实质性的：
- 修复前：trigger B 在 Aria 低频 PR 场景下（codebase 健康，WOULD-BLOCK = 0）永远落入 trigger C → 推荐无数据翻转。等价于"把无 regression 的正常运行误判为观测不足"。
- 修复后：trigger B 基于 `total_gate_executions >= 3`，gate 运行 3 次（无论是否触发 WOULD-BLOCK）即可满足 minimum-observation guard，逻辑回归 parent Spec 意图（验证 gate infrastructure liveness）。
- `total_gate_executions` 的数据来源路径清晰：4 个 jsonl 汇总 + PR merge log 推算 PASS 数。推算路径的"PASS 推算"部分（`total_pr_merges_in_window - 已 telemetry PR count`）使用了代理计数（proxy count via Forgejo PR merge log），这是 parent Spec B.2 step 0 已确立的合理 fallback，不引入新歧义。

**Verdict**: **CLOSED**

---

### C-2 D+0→D+14 FP labeling workflow 未定义

**Rev1 changes observed**:
在 §决策框架 和 §观察期数据 之间新增了完整的 **§标注操作流程 (FP labeling workflow, D+0 → D+14)** sub-section（proposal.md L178-190），结构为表格，覆盖 5 个维度：

| 维度 | Rev1 内容 |
|------|-----------|
| **标注时机** | 每次 WOULD-BLOCK 事件发生后 24h 内；D+14 当天批量回顾 null 条目 |
| **标注 owner** | simonfishgit（与 parent §FP labeling L237 一致） |
| **标注操作方式** | (a) JSONL 在 `aria/metrics/`（.gitignore 内）；(b) 手工编辑 append `human_reviewed_as_fp` 字段；(c) 决策 doc §2 记录标注结果含 PR URL + 判定理由 |
| **判定依据** | 对每个 event cross-ref PR merge commit + intent：legitimate rollback → `true`（FP）；actual regression → `false`；under investigation → `null`（pending） |
| **D+14 null 条目处理** | (a) 默认保守视为 `false`（not FP，不计入 FP rate 分子）；(b) 备选延迟 1-2 天；(c) 决策 doc §3 必须显式记录 null-pending 处理方式 |

同时在 §观察期数据 schema 中：
- `human_reviewed_as_fp_null: <int>` 字段增加注释 `D+14 默认按保守 false 处理 per §标注操作流程`，与新 section 形成双向锚定。

**Paper-fix antipattern 验证**:
不是表面修复。新增 section 解决了 C-2 识别的三个可执行性缺口：
1. **标注时机**：明确 24h SLA + D+14 批量回顾，不再是 vague "monthly review"。
2. **JSONL 在 .gitignore 的操作路径**：(b) 手工编辑说明了访问方式，(c) 在决策 doc 记录了可追踪的 audit trail。
3. **null 处理 fallback**：默认保守 `false` + 备选延迟 1-2 天 + 决策 doc 必须显式记录，三层兜底，不再是空白。

**一个微小的残余**：§标注操作流程 表格定义了"24h 内标注"，但未说明 owner 忘记在 24h 内标注时的 recovery path（即"24h 后但 D+14 前"的时间窗口的标注是否仍有效）。然而 D+14 批量回顾条款已经覆盖了这个场景——未在 24h 内标注的条目在 D+14 批量回顾中补打，仍属 `null` 的才走 fallback。这个隐含逻辑可被合理推导，不构成新 Critical。

**Verdict**: **CLOSED**

---

## R1 Important issue closure

| R1 ID | Status | Comment |
|-------|--------|---------|
| **I-1** (gate executions counter) | **CLOSED** | 与 C-1 同步修复。`total_gate_executions` 字段已加入 schema CRITICAL fields 首位，数据来源路径（4 jsonl + PR merge proxy）已定义。可观测性缺口已填补，D+14 时 owner 有明确计算路径。|
| **I-2** (trigger B "no FPs requiring redesign" 无量化边界) | **CLOSED** | trigger D 条件新增 `intermediate 3-19 events 区间出现 FP rate > 2% (e.g., 5 events / 1 FP = 20% — 视为 requiring redesign, 转入此 trigger 处理)`，明确覆盖了 R1 I-2 识别的中间地带（3~19 events，>0 FP）。触发逻辑现在在所有事件数范围内完备闭合：<3 → trigger C；3-19 且 FP > 2% → trigger D；3-19 且 FP ≤ 2% → trigger B；≥20 → trigger A。|
| **I-3** (fallback 默认推荐由 (b) 改为 (a)) | **CLOSED** | R1 Risk R1 mitigation 修正：`默认推荐 (a) extend` 附带完整推理 `gate executions 不可知 / 极少时, (b) 风险接受路径无证据基础, 保守 extend 路径优先`。trigger C 表格也同步标注 `默认推荐 (a) extend per R1 QA I-3`，形成一致性。|
| **I-4** (max defer outer bound 缺失) | **CLOSED** | R1 Risk R1 mitigation 新增：`最大延迟上界 (max defer outer bound): D+42 (= D+28 for fallback-a 20-PR window + D+14 buffer)。超过此日期若仍无足够数据，默认执行 (b) flip with risk-acceptance 并记录`，且 pre-ship Checklist 也有对应条目。|

---

## New issues introduced by Rev1 (paper-fix antipattern guard)

| ID | Severity | Issue | Fix |
|----|----------|-------|-----|
| **N-1** | Minor | `total_gate_executions` PASS 推算路径依赖 `total_pr_merges_in_window - 已 telemetry PR count` 的口径精确性，但两者来源不同（PR merge log vs 4 jsonl 文件），可能因 jsonl 记录遗漏（如 gate 被 phase-c-integrator bypass 时）造成负数或虚高的 PASS 推算。Spec 在 Phase B step 0 的计算说明中未说明 "推算值为负时的 fallback 处理"（即 `total_pr_merges_in_window < 已 telemetry PR count` 的异常情况）。| 在 §观察期数据 schema 的 `total_gate_executions` 注释中补充一行：`若推算 PASS 数为负（telemetry 行数 > PR merge 总数），则 PASS 推算改为 0，并在 decision_rationale 中说明口径异常原因`。不影响 D+14 决策流程，仅需补充 edge case 说明。|

**无重大新问题**。Rev1 整体是 substance-level 修复，新增内容有机衔接，未引入逻辑断层或新的 Critical 缺陷。

---

## Strengths of Rev1

**1. §标注操作流程 的结构设计规范**  
新 section 采用表格格式，每行对应"是什么 / 谁 / 怎么做 / 判定依据 / 边缘 fallback"的五维标准，是对 parent Spec "monthly review" 模糊承诺的有效具体化。尤其是 `D+14 null 条目处理` 三路选项（默认保守 false / 延迟 1-2 天 / 显式记录）构成了合理的决策弹性。

**2. C-1 修复的传播一致性**  
trigger B/C 文字修正、§Why 第一段 inline 注释、Phase B step 0 计算说明、schema CRITICAL fields 四处同步更新，而非只改 §决策框架 表格。体现了对"paper-fix antipattern"（仅改一处 verdict 数）的主动防御。

**3. trigger D 的中间地带覆盖**  
I-2 的修复方式采用了带具体数值的示例（`5 events / 1 FP = 20%`），使 "requiring redesign" 的抽象判据转化为可操作的量化规则，降低了 D+14 决策时的主观性。

**4. max defer outer bound 的 D+42 设计合理**  
D+28（fallback-a 20-PR window）+ D+14（buffer）= D+42 设计兼顾了 Aria 项目 PR 频次低的现实约束（20 PR merges 在低频项目可能需要 3-4 周），同时对 warn-only 永久状态设定了硬性终止线，与 parent Spec §Risk R2 "gate 形同虚设"风险对应。

---

## R2 verdict reasoning

**收敛判定依据** (per `feedback_post_spec_audit_pragmatic_convergence` + Level 2 baseline):

1. **Verdict 改善方向正确**: R1 REVISE → R2 PASS_WITH_WARNINGS，无振荡迹象。
2. **2 Critical 均实质性关闭**: C-1 和 C-2 的修复均为 substance-level（逻辑变化 + 新 section + schema 扩展），不是关键词替换。
3. **4 Important 全部处理**: I-1 随 C-1 同步修复；I-2 通过 trigger D 条件扩展覆盖中间地带；I-3 / I-4 直接文字修正。
4. **新增 issue 仅 1 条 Minor (N-1)**: PASS 推算路径负数边缘 case 未说明，属于 schema edge case 文档不足，不影响决策框架核心逻辑。Minor 级别不触发 REVISE。
5. **6 条 R1 Minor**:
   - m-1（gate_errors 字段）：Rev1 中 schema 新增了 `gate_errors: {fetch_failure_count, origin_rewrite_count}` 子结构，已关闭。
   - m-2（dogfood 测试命令具体化）：Phase B step 6 中已增加明确命令片段 `unset ARIA_SUBMODULE_GATE_MODE && ./submodule_gate.sh`，已关闭。
   - m-3（replay test T-replay-14）：Phase B step 6 注释 `若 13 现有 assertions 未覆盖 default-block path → 新增 T-replay-14`，已关闭（条件式处理，可接受）。
   - m-4（per_pr_breakdown pr_url 构造）：schema note 中增加了 `pr_url` 构造模板 `https://forgejo.10cg.pub/10CG/Aria/pulls/<NUM>` 及 `unknown` 时手动 cross-ref 说明，已关闭。
   - m-5（B.4 step 6 post-merge 验证具体化）：`step 6` 改为 `在 aria-plugin 或 standards submodule 有变更的下一次 PR merge 中，确认 §C.2.4.5 workflow 输出包含 MODE=block`，已关闭。
   - m-6（`.aria/decisions/` canonical 路径确认）：Rev1 未显式处理，但 R1 报告本身已记录"`.aria/decisions/` 目录已存在，是该项目已建立的 decisions 存储约定"，属于 owner 确认事项而非 Spec 文字问题。可视为 accepted risk，不重开。

**综合判定**: R2 verdict = **PASS_WITH_WARNINGS**

遗留 warning（写入决策 doc，无需 R3）:
- **W-1 (from N-1)**: Phase B step 0 执行时，若 `total_gate_executions` PASS 推算出现负数（telemetry 行数超过 PR merge 总数），需在 `decision_rationale` 字段显式记录口径异常，PASS 推算改为 0。
- **W-2 (from C-2 残余)**: §标注操作流程 的 24h SLA 是最佳实践约束，D+14 批量回顾覆盖了"24h 内遗漏"的 recovery path（视为 pending → null → fallback 保守 false），建议在决策 doc §2 中对每个 null 条目注明"批量回顾补标 vs 真实 pending"的区别。

Level 2 R1+R2 两轮审计均已完成（R1: tech-lead PASS_WITH_WARNINGS / qa REVISE / code-reviewer PASS_WITH_WARNINGS；R2: qa PASS_WITH_WARNINGS）。三 agent 方向收敛，满足 Level 2 baseline unanimous PASS_WITH_WARNINGS 条件。建议 Spec Status 更新为 **Approved**，进入 Phase A.2 完成 → Phase B 待命（2026-06-07）。
