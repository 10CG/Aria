# post_spec R1 audit — aria-submodule-gate-block-flip (qa-engineer)

**Date**: 2026-05-25
**Auditor**: qa-engineer agent
**Verdict**: REVISE
**Reasoning summary**: Spec 在两个维度存在 Critical 问题：(1) 最关键的决策判据"最小观测数"在 child Spec 与 parent Spec 之间存在语义不一致（gate executions vs WOULD-BLOCK events），会直接误导 D+14 决策流程；(2) `human_reviewed_as_fp` 字段的标注工作流在 D+0→D+14 窗口内完全未定义，导致 §观察期数据 schema 填充时存在盲操作风险。其余 4 条 Important 问题包括可观测性缺口（无 PASS 计数器）、fallback 默认推荐争议、0-event null state 显式处理缺失、以及 trigger B "no FPs requiring redesign" 判据无量化边界。

---

## Critical issues

### C-1: minimum-observation guard 语义歧义（child Spec 与 parent Spec 不一致）

**位置**: `proposal.md` §决策框架 trigger B + trigger C，与 parent Spec L234 冲突

**问题描述**:

parent Spec L234 的原文:

> `14d hard date elapsed since v1.28.0 ship WITH **≥3 minimum gate executions observed in warn-only window**`

child Spec (本 Spec) §决策框架的条件:

> trigger B: `WOULD-BLOCK events >= 3`
> trigger C: `now >= 2026-06-07 AND WOULD-BLOCK events < 3`

"gate executions"（gate 每次 PR merge 运行一次）与 "WOULD-BLOCK events"（gate 运行中实际检测到 regression/divergence 的次数）是截然不同的两个量:

- 在健康 codebase 中，gate 跑 19 次（对应 19 次 PR merge），WOULD-BLOCK events 可能 = 0（所有 PR 的 submodule pointer 都是 forward bump 或 no-change）
- 代码验证（`submodule_gate.sh` L258 `log_telemetry "$WARNS_FILE"`）：PASS 路径无 telemetry 写入，`warns.jsonl` 行数 == 0 无法区分"gate 从未运行"vs"gate 运行 N 次但无 regression 事件"
- 若按 child Spec 语义（"WOULD-BLOCK events >= 3"），即使 gate 健康运行了 19 次，正常运作的 codebase 永远不会触发 trigger B，永远落入 trigger C → 默认推荐 fallback (b) 无数据翻转

**风险**: D+14 决策框架实质上失去了"观测充足"的保障。parent Spec 的 "gate executions" 意图是验证 gate 真的在跑（infrastructure liveness），而非等待 regression 出现。child Spec 的替换改变了这个意图。

**修复建议**:
1. 将 trigger B/C 条件改回 parent Spec 语义：`gate executions >= 3`（即 warns.jsonl + blocks.jsonl + 所有 PASS 的 gate runs 总数）
2. 或在 `submodule_gate.sh` 中增加 PASS telemetry（写入单独 `submodule-gate-runs.jsonl` 或 `submodule-gate-stats.jsonl`），使 `total_gate_executions` 可观测
3. §观察期数据 schema 中明确区分 `total_gate_executions` vs `total_would_block`，两者均作为 trigger B 判断依据

---

### C-2: D+0→D+14 FP 标注工作流未定义

**位置**: `proposal.md` §观察期数据 schema，parent Spec L237

**问题描述**:

parent Spec L237 定义:

> `human_reviewed_as_fp: true|false|null` field. **Monthly review** (named owner: simonfishgit per Rev1 M-qa-6 fix) sets the field by examining each WOULD-BLOCK event against PR intent

本 Spec 在 D+1 起草，D+14 ship。观察窗口 D+0→D+14 恰好是 parent 所定义"monthly review"的第一个周期。但:

1. **标注工作流在 D+0→D+14 期间无文档化操作指引**: 谁在什么时机触发标注？是每次 WOULD-BLOCK 事件发生后立即标注，还是 D+14 当天批量标注？如何访问和编辑 `warns.jsonl` 中的 `human_reviewed_as_fp` 字段（该文件在 `.gitignore` 中，不随 PR 提交）？
2. **schema 字段 `human_reviewed_as_fp_null` 的含义含糊**: "未审查 (pending)" 在 D+14 决策时如何处理？FP rate 公式 `= true / (true + false)` 排除 null，但如果所有事件都是 null（simonfishgit 未来得及标注），rate = undefined，决策无法执行 trigger A 或 B。
3. **D+14 当天 ship 的时间序列问题**: Phase B step 1 先收集数据再起草决策 doc，但若 WOULD-BLOCK 事件在 D+13 发生且未标注，D+14 会用 null 值做决策。Spec 未说明 null 的处理方式在决策当天如何 fallback。

**风险**: 标注流程的缺失意味着 §观察期数据 section 在 D+14 可能被随意填充，丧失了"观察期数据"的可信度，进而使整个 §决策框架 失去数据支撑。

**修复建议**:
1. 在 §观察期数据 section 前增加 "标注操作流程" 段落（1-2 句），说明：D+14 当天 Phase B step 1 执行 `cat aria/metrics/submodule-gate-warns.jsonl` 后，对每个 null 条目逐一 cross-ref 对应 PR 的 merge commit message + PR intent，在决策 doc 中记录标注结果
2. 明确 null-pending 处理规则：若 D+14 存在 null 条目 → 视为"未审查 true block（保守）"或"延迟 1-2 天待标注完成再决策"
3. 参照 Rule #7 `secret-leak-ok-explicit` 模式，标注操作须有 owner sign-off 记录

---

## Important issues

### I-1: 可观测性缺口 — 无法区分"gate 从未运行"vs"gate 运行且无事件"

**位置**: `proposal.md` §观察期数据 schema + `submodule_gate.sh`

**问题描述**:

代码验证确认：`submodule_gate.sh` 只在 WOULD-BLOCK（warn 模式）、BLOCK（block 模式）、override 和 fetch/fetch-incomplete 错误时写 JSONL。PASS 路径（forward bump / no-change / first-time）无任何 telemetry 输出。

`warns.jsonl` 行数 = 0 在语义上有两种完全不同的情况：
- (a) gate 跑了 N 次，所有 PR 的 submodule 都是 forward bump → gate 运转正常，codebase 健康
- (b) gate 完全没有被 phase-c-integrator 调用（configuration 未对接、脚本路径错误）

Spec 的 §观察期数据 schema 中 `total_would_block: <int>` 无法区分这两种情况。decision maker 在 D+14 面对 `total_would_block: 0` 时，无法判断是情况 (a) 还是 (b)。

**QA 影响**: D+14 若 `total_would_block: 0` 且无独立的 `total_gate_executions` 字段，owner 必须手动 cross-ref git log（PR 数）与 gate 调用日志来证明 gate 在运行，这是未文档化的人工验证步骤。

**修复建议**:
1. 在 schema 中增加 `total_gate_executions: <int>` 字段，注释说明来源（phase-c-integrator 调用 submodule_gate.sh 的次数，可从 CI/workflow 日志或 gate 启动时追加 run-log 计数）
2. 或在 `submodule_gate.sh` 中增加 PASS 事件简要 telemetry（仅 `{timestamp, pr_id, verdict: "PASS", submodule_count}`），使 runs.jsonl 成为真实的 gate execution counter

---

### I-2: trigger B 条件 "no FPs requiring redesign" 无量化边界，与 trigger D / Risk R2 边界不清

**位置**: `proposal.md` §决策框架 trigger B + trigger D，Risk R2

**问题描述**:

trigger B 条件之一是 `no FPs requiring redesign`，但 "requiring redesign" 从未被量化定义。与之相关：
- trigger D（High FP rate ≥ 2%）基于 `FP_count / total_WOULD-BLOCK_events` 且要求 ≥20 events（分母门槛）
- trigger B 适用于 WOULD-BLOCK events 在 3~19 之间（不够触发 trigger A）

**未定义场景**：若 `total_would_block = 5`，`human_reviewed_as_fp_true = 1`（FP rate = 20%），此时：
- trigger A 不适用（events < 20）
- trigger D 不适用（events < 20，"sustained over ≥20"条件未满足）
- trigger B 条件 "WOULD-BLOCK events >= 3" 满足，但 "no FPs requiring redesign" 如何判断？20% FP rate 是否 "requiring redesign"？

Spec 没有给出这个中间地带（3-19 events，>0 FP）的处理规则。owner 在 D+14 可能面对完全主观的判断。

**修复建议**:
在 §决策框架 表格后增加一段注释，明确 trigger B 的 "no FPs requiring redesign" 等价条件：例如 "若 <20 events 但 FP rate 超过 2%，视为 requiring redesign，转入 trigger D 处理"。使触发逻辑在所有事件数范围内完备覆盖。

---

### I-3: R1 fallback (b) 被设为默认推荐——逻辑合理性存疑，存在"零数据翻转"风险

**位置**: `proposal.md` Risk R1 fallback 策略，"默认推荐 (b)"

**问题描述**:

R1 fallback 三路径：
- (a) extend warm-up window（下一 20 PR merges，新 hard date）
- (b) flip with explicit risk-acceptance note（默认推荐）
- (c) 延迟 1-2 周 file 显式 OpenSpec defer

Spec 将 (b) 设为默认推荐，理由是"parent Spec replay test 13/13 PASS 已提供 mechanism confidence"。但这一推荐有两个质量问题：

**问题 1**: 如 C-1 所述，若 `total_would_block = 0` 且无独立 gate execution counter，owner 无法验证 gate 是否在实际运行。在 gate 可能根本未被调用的情况下，用"机制经过测试，放心翻转"的论据是危险的。

**问题 2**: (b) 路径与 (c) 路径不是真正独立：(b) "owner 显式签字接受零数据风险" 本质上就是一种显式的 defer/skip，与 (c) "file 显式 OpenSpec defer" 的区别仅在于是否新建 Spec。若 (b) 和 (c) 的实际风险效果相同（都是在无数据情况下翻转或延期），为何不推荐风险更低的 (a)（延长至有数据）？

**QA 推荐**: 若 `total_gate_executions` 可观测（解决 I-1 后），且 `total_gate_executions >= 3` 但 `total_would_block = 0`（gate 健康运转，无 regression），则推荐 (b) flip 是完全合理的（机制有效，0 事件 = 零 regression）。但若 `total_gate_executions` 不可知，建议将默认推荐改为 (a)（保守路径）而非 (b)。

---

### I-4: R1 fallback 缺少最大延迟上界（max defer outer bound）

**位置**: `proposal.md` Risk R1 fallback (a) + (c) 路径

**问题描述**:

R1 fallback (a) 描述 "extend warm-up window 下一 20 PR merges，新 hard date 写决策 doc"，(c) 描述 "延迟 1-2 周 file 显式 OpenSpec defer"。两条路径都缺少：
- 硬性最大延迟上界（例如"无论如何，D+30 或 D+42 必须翻转或放弃"）
- 如果 (a) 延期后的 20 PR merges 仍 0 WOULD-BLOCK events，是否再次 fallback？

parent Spec §Risk R2 明确指出"warn-only 模式无 trigger 翻转 = MEDIUM 风险（gate 形同虚设）"。若 fallback 路径可无限期延伸（(a) → (a) → (a)），则 warn-only 永久状态风险被低估。

**修复建议**:
在 R1 mitigation 中增加一行：`最大延迟上界: D+42 (D+28 for fallback-a 20-PR window + D+14 buffer)。超过此日期若仍无足够数据，默认执行 flip with risk-acceptance note (b) 并记录到决策 doc。`

---

## Minor issues

### m-1: §观察期数据 schema 缺少 gate 网络故障计数字段

`fetch_failure_count` 和 `origin_rewrite_count` 未在 schema 中出现。这两类事件（exit code 2、3）在 `submodule-gate-blocks.jsonl` 中有记录，但 §观察期数据 没有对应聚合字段。对于 D+14 决策，了解"14d 内 gate 是否曾因 fetch 失败降级"是有价值的诊断信息。建议在 schema 中增加 `gate_errors: {fetch_failure: <int>, origin_rewrite: <int>}` 可选字段。

---

### m-2: §Validation Checklist Phase B step 7 dogfood 测试不够具体

step 7 描述：`ARIA_SUBMODULE_GATE_MODE 未显式设置时，新代码 fallback 到 "block"`

但现有测试套件（`test_submodule_gate.sh`）中所有 13 个 assertion 都显式传入 `env ARIA_SUBMODULE_GATE_MODE=block`，没有测试"不设 env var"时 default 的行为。

建议：Phase B step 7 dogfood 应包含一个明确的命令片段：
```bash
unset ARIA_SUBMODULE_GATE_MODE
./submodule_gate.sh  # 预期行为: MODE="block" (从 L33 ${:-block} 读取)
```
并在 Validation Checklist 中记录预期输出（BLOCK or PASS，取决于当前 repo 的 submodule 状态）。

---

### m-3: replay test suite 未计划为 v1.29.0 扩展新 test case

§Validation Checklist step 8 描述 "replay test (parent Spec 13 assertions × 10 scenarios) 重跑确认未 regress"，但未说明是否需要新增针对 v1.29.0 default-block 行为的测试用例（例如"无 env var override，PR 有 regression，预期 exit 1"）。

建议在 Checklist 中增加说明：`若 Phase B self-review 发现 default-block path 未被现有 13 assertions 覆盖，须新增 T-replay-14: default mode=block (no env var), regression PR, expect exit 1`。

---

### m-4: per_pr_breakdown 数据来源未明确

§观察期数据 schema 的 `per_pr_breakdown` array 中，每个条目包含 `pr_url`、`timestamp`、`master_ptr`、`feature_ptr` 等字段，但 schema note 仅说明"数据源: warns.jsonl + Forgejo PR merge log"。

实际上，`warns.jsonl` 不包含 `pr_url`（仅有 `pr_id = ARIA_PR_NUMBER`），`pr_url` 需要通过 `ARIA_FORGEJO_REPO` + `pr_id` 构造。若 `ARIA_PR_NUMBER` 未设置（gate 在非标准调用路径运行），则 `pr_id = "unknown"` → `per_pr_breakdown` 无法构造有效条目。

建议：schema note 中明确 `pr_url` 的构造方式：`https://forgejo.10cg.pub/{ARIA_FORGEJO_REPO}/pulls/{pr_id}`，并说明若 `pr_id = "unknown"` 时手动 cross-ref git log 的操作步骤。

---

### m-5: B.4 step 6 "post-merge 验证"描述过于模糊

`step 6: post-merge 验证: 下一次 PR 触发 §C.2.4.5 时 mode default 已为 block`

这个验证步骤没有说明：
- "下一次 PR" 需要是有 submodule 变更的 PR（才能看到 gate 路径区别）
- 接受标准是什么（看到 `MODE=block` 日志输出？看到 BLOCK 拦截？还是看到 PASS 且 gate 正常运行？）

建议改为：`step 6: post-merge 验证: 在 aria-plugin 或 standards submodule 有变更的下一次 PR merge 中，确认 §C.2.4.5 workflow 输出包含 mode=block（无论 verdict 是 PASS / BLOCK）`

---

### m-6: 翻转决策文档路径使用 `.aria/decisions/`，但 Rule #9 规定 prose 应在 `docs/`

`proposal.md §What E` 创建 `.aria/decisions/2026-06-07-v1.29.0-block-flip.md`。按照 CLAUDE.md Rule #9 精神（`.aria/` 是机器状态 namespace，`docs/` 是 human/AI readable prose namespace），Flip Decision Record 属于 prose/decision 文档，其位置是否符合项目命名空间约定值得确认。

注：`.aria/decisions/` 目录已存在（验证：`ls /home/dev/Aria/.aria/decisions/` 输出多个决策文档），表明这是该项目已建立的 decisions 存储约定，与 Rule #9（handoff 路径约束）没有直接冲突。此条 minor 仅为提示，请 owner 确认 `.aria/decisions/` 是该类文档的 canonical 路径。

---

## Strengths

1. **Spec 结构清晰，继承设计合理**: Level 2 minimal 定位准确，零新机制的声明贯穿全文，deliverables 6 项全部有具体文件路径和前后版本对比，减少了 Phase B 实施时的歧义。

2. **§决策框架 表格设计良好**: 5 个 trigger（A/B/C/D/E）覆盖了主要决策路径，每个 trigger 的前提条件和决策动作都有明确记录。Decision Record 的起草要求（`.aria/decisions/` 文件，含 5 个必要 section）提供了足够的结构化约束。

3. **Risk R5 跨 Spec 时序冲突识别准确**: 明确指出本 Spec 与 M6 sub-Spec `aria-2.0-m6-docs` T-B0.10 的先后依赖关系（DEC-20260524-002 R1-X-T2 fix），并通过 Layer L claim 协调避免 race，符合 `feedback_concurrency_advisory_over_hardlock` 约定。

4. **§观察期数据 schema 结构合理（框架层面）**: YAML schema 在 Phase A 给出占位模板的思路可取，`override_usage` 子结构包含 `override_rate` 并指向父 Spec 15% 再校准阈值，schema 与 parent Spec §R4 联动设计清晰。

5. **backward compatibility 路径完整**: `mode="warn"` legacy opt-out + `mode="off"` emergency bypass 均已保留，env-var override 优先级不变，符合 Aria `向后兼容` 原则。

6. **Cross-reference 完整性高**: 引用了 parent Spec / 决策文档 / 审计报告 / M6 依赖 / Rule #6 substitute 继承 / memory references，有效降低了读者需要二次查阅的成本。

---

## Q-NEW

**Q-NEW-1 (owner only)**: C-1 修复方向的选择 — 你倾向于 (X1) 修正 child Spec 的语言，将 trigger B/C 改为"gate executions >= 3"并在 schema 增加 `total_gate_executions` 字段，还是 (X2) 在 `submodule_gate.sh` 增加 PASS telemetry 写入（更侵入但更完整）？两者影响 Phase B 的实施范围。

**Q-NEW-2 (owner only)**: I-3 推荐将默认 fallback 从 (b) 改为 (a)（如 C-1/I-1 修复后 gate executions 可观测）。你是否认可这个调整？还是坚持"机制 confidence 已足够，允许零 WOULD-BLOCK 事件时直接翻转"？

---

## Verdict reasoning

**总计**: 2 Critical + 4 Important + 6 Minor

**按 Rubric 判定**: 1-2 Critical → **REVISE**

两个 Critical 均与 D+14 核心决策流程直接相关：

- **C-1** 是 Spec 继承错误——child Spec 在翻译 parent Spec 的 minimum-observation guard 时引入了语义替换（"gate executions" → "WOULD-BLOCK events"），使得在正常运作的 codebase 中该 guard 永远不会被满足，实质上使 trigger B 变成了死代码，所有正常情况下都落入 trigger C → fallback (b)。这不是措辞问题，而是决策逻辑错误。

- **C-2** 是可执行性缺口——D+14 当天的数据填充依赖 `human_reviewed_as_fp` 字段，但整个 14 天观察期内没有定义标注时机、标注操作方式（JSONL 在 .gitignore 内，不随 PR 可追踪），以及 null 条目在决策当天的 fallback 处理。这会导致 D+14 fillout 存在操作空白。

4 条 Important 问题均可在 Rev1 中通过 Spec 文本修改解决，不需要 mechanism 变更。Rev1 后预计可达到 PASS_WITH_WARNINGS（per `feedback_post_spec_audit_two_round_pragmatic_for_l2` Level 2 baseline）。

**不升级到 FAIL 的理由**: 两个 Critical 均为文档/判据层面缺陷，不涉及 mechanism 错误（gate 代码本身已验证正确）；Spec 整体结构和 deliverable 清单无质量风险；现有 13 个 replay test 对 gate 行为的覆盖有效。
