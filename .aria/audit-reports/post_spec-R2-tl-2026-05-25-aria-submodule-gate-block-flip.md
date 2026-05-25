# post_spec R2 audit — aria-submodule-gate-block-flip (tech-lead)

**Date**: 2026-05-25
**Auditor**: tech-lead agent (Claude Opus 4.7 1M context, R2)
**Spec under review**: `openspec/changes/aria-submodule-gate-block-flip/proposal.md` (Rev1 applied 2026-05-25T~13:30Z)
**Level**: 2 (Minimal — proposal.md only)
**R1 verdict**: PASS_WITH_WARNINGS (0 Critical, 7 Important, 10 Minor, 5 Q-NEW)
**R2 verdict**: **CONVERGED** (PASS_WITH_WARNINGS)
**Convergence judgment**: R1 全部 7 项 Important (I-tl-1 ~ I-tl-7) 在 Rev1 中已 substantively 解决,均为同根因 + 同机制的实质修复,非 surface keyword match。Rev1 同时吸收 qa + code-reviewer R1 issues (Spec 自述 2 Critical + 13 Important + 8 Minor fixed),整体结构紧致度显著提升。无新 Critical 引入,无 architectural regression,符合 Level 2 R1+R2 unanimous PASS_WITH_WARNINGS 收敛模式 (per [[feedback_post_spec_audit_two_round_pragmatic_for_l2]])。

---

## R1 issue closure status

| R1 ID | Issue summary | Fixed in Rev1? | Comment |
|-------|---------------|----------------|---------|
| **I-tl-1** | §A 默认值位置应明确 3 处 (script + inline doc-Bash + config table),而非二选一 | **CLOSED** | §A 重构为 A1/A2/A3 三段并列结构 (L38-55),A1 明确 `submodule_gate.sh L33` 为 runtime SOT,A2 明确 SKILL.md L378 为 doc-illustrative SOT,A3 明确 config table 多行 + grep batch-review 方法。L38 标题"Default flip in **3 places**"+ inline 注释"(per R1 I-tl-1 — script + inline doc-Bash + config table 三处并行存在, 必须同步翻转)"实质表达三者 parallel + must-sync 关系。Drift 风险消除。 |
| **I-tl-2** | §F CHANGELOG immutability — v1.28.0 entry 不应原地改写,应在 v1.29.0 new entry 记录 + 旧 entry 加可选 inline 注释 | **CLOSED** | §F 表格 L102 改为 "v1.28.0 entry L32 'v1.29.0 (planned, ...)' **保留原文** + 可选 inline 注释 `<!-- shipped <ship-date> see [1.29.0] -->`",§C 表格 L73 同步加 `<!-- shipped 2026-06-07 see [1.29.0] -->` 注释格式。Keep-a-Changelog convention 已正确内化,v1.28.0 historical state 保持 immutable。 |
| **I-tl-3** | §R5 M6 T-B0.10 关系是 dual-layer strengthening,非 hard block | **CLOSED** | §Why L30 + §R5 L280 + §Cross-references L344 全部重写为 dual-layer defense 表述:"M6 sub-Spec `aria-2.0-m6-docs` 的 `T-B0.10` 是 **inline self-contained gate** ..., **不依赖** 本 Spec ship。但 M6 整体 PR 走 phase-c-integrator merge 时会被 §C.2.4.5 二次验证 — 形成 **dual-layer defense**"。`§Cross-references` 旧 "Downstream blocked" 段亦改为 "Downstream strengthened (dual-layer defense, NOT blocked)"。3 处修订口径完全一致,无残留歧义。 |
| **I-tl-4** | 缺 R7 "stale-branch-first-merge-after-flip" risk | **CLOSED** | §Risk 新增 R7 行 (L282),含 Likelihood (LOW-MEDIUM, Aria 项目 PR 频次低) + 3-prong mitigation (ship 当天 open PRs ping / BLOCK override hint / 决策 doc §6 记录)。§E 决策记录 doc 同步新增 §6 段 (L95) "ship 当天 open PRs 审查结果"。§Validation Checklist L305 同步新增 "ship 前审 open PR 列表" 项。三处链式 surfacing,执行路径完整。 |
| **I-tl-5** | Effort baseline ~1.5h 严重低估,realistic ~5h | **CLOSED** | L10 effort baseline 已改为 "~5-6h end-to-end (Phase A.1 ~1h skeleton + A.2 audit ~1h + 2026-06-07 当天 §观察期数据汇总 ~1.5h + Phase B 实施 ~1.5h + Phase C dual-PR sequenced merge ~1h + Phase D archive + handoff ~0.5h)"。§How B.2 step 0 (data analysis ~1h) 显式新增 (L122-131),B.2/B.3/B.4 + Phase D 时间估算分别 ~1.5h / ~0.5h / ~0.5h / ~0.5h 加和与 L10 一致。Cognitive load 全部 surface。 |
| **I-tl-6** | §观察期数据 schema 漏 tripwire health 字段 | **CLOSED** | §观察期数据 YAML schema L258-262 新增 `tripwire_health` subsection,含 `workflow_dispatch_runs_in_window` / `last_manual_run_timestamp` / `ready_for_schedule_enable` / `notes` 4 字段。§Validation Checklist L306 "tripwire workflow 至少手工 dispatch 触发 1 次, 确认 ready for schedule cron enable" 同步落点。`(per R1 I-tl-6 — parent §R9 NEW Rev1 R1-qa M-qa-3)` inline 注释明确 trace。 |
| **I-tl-7** | §决策框架 缺 override_rate > 15% 触发条件 (Trigger F) | **CLOSED** | §决策框架 表格新增 Trigger F 行 (L204):"`override_rate = (trailer + label) / total_PR_merges_in_window > 15%` → 不翻转;file 新 OpenSpec 重审"。Trigger F 优先级 > A/B (高 override 表明合理 rollback 频繁) 显式声明。§观察期数据 YAML `override_usage.override_rate` 字段 (L255) 注释 "**>15% triggers §决策框架 Trigger F deferral**"。Default-on policy L206 同步加 "AND override rate ≤ 15% (trigger F not triggered)" 约束。三处链式 enforcement。 |

**Summary**: 7 / 7 Important CLOSED, 0 PARTIAL, 0 OPEN。

---

## New issues introduced by Rev1 (if any)

| ID | Severity | Issue | Fix |
|----|----------|-------|-----|
| _(none Critical)_ | | | |
| n-tl-1 | Minor | §How B.4 step 4 chicken-and-egg 注释 (L157) 描述清晰但 step 6 "post-merge 验证 — 在 aria-plugin 或 standards submodule 有变更的**下一次** PR merge 中..." 与 m-tl-3 R1 修订一致, 但未明确该 "下一次 PR" 若 14d 内无任何 submodule-touching PR 出现,acceptance criteria 何时算最终满足? 建议加 "acceptance window outer bound: ship 后 30d 内任一 submodule-touching PR 即可" 兜底。 | 非阻塞,可在 Phase B step 6 ship 当天 inline 决策。建议 Rev2 (若有) 或直接在 `.aria/decisions/<ship-date>-v1.29.0-block-flip.md` §6 记录 acceptance window。 |
| n-tl-2 | Minor | §标注操作流程 表格 (L182-189) 与 §观察期数据 schema 之间字段 `human_reviewed_as_fp_null` 处理细节正确,但 "保守视为 false (not FP)" 的 implication 是 fp_rate 公式 `true / (true + false)` 中 null 不进分母 — 与 parent §FP labeling L237 "排除 null" 一致,但 §决策框架 Trigger D "FP rate ≥ 2% sustained over ≥20 events" 中 "≥20 events" 是 (true + false) 还是 total (含 null)? 当前文本未显式说明。 | 非阻塞。建议在 §标注操作流程 末尾或 §决策框架 Trigger A/D 注释加一行 "events 口径 = (true + false), 不含 null"。Phase B step 0 数据汇总时 owner 可现场补订。 |

**Rev1 整体未引入新 Critical 或 Important**。2 项 Minor 均为 acceptance criteria / 字段口径的细节澄清,不阻塞 R2 CONVERGED,可在 Phase B ship-day 落地阶段 inline 处理。

---

## Paper-fix antipattern check

per `[[feedback_paper_fix_antipattern.md]]` — 多 agent 收敛验证必须 substance-level (同根因 + 同机制),非 surface-level (verdict 数 / 关键词匹配)。R2 逐项核查:

| R1 Issue | Surface keyword | Substance fix check |
|----------|-----------------|---------------------|
| I-tl-1 | "3 places" | ✅ Substance: A1/A2/A3 三段独立小节, 每段含具体 file path + line + 验证命令; A3 多行场景配 `grep -nE` batch-review 方法; runtime SOT vs doc-illustrative SOT vs config doc SOT 三层 SOT taxonomy 显式建立。非仅替换 "或" → "和"。 |
| I-tl-2 | "immutable" | ✅ Substance: §F 表格 v1.29.0 NEW entry 与 v1.28.0 historical entry 分离 (两行表格), inline 注释 `<!-- shipped see [1.29.0] -->` 是 Keep-a-Changelog 标准做法 而非自创格式; §C 表格 L73 同步 (一致性约束)。CHANGELOG 真值流向 (v1.29.0 自身 entry 是 ship 事件 SOT) 修复。 |
| I-tl-3 | "dual-layer" | ✅ Substance: §Why L30 + §R5 L280 + §Cross-references L344 三处独立修订, 每处都说明 "M6 T-B0.10 inline self-contained, 不依赖 v1.29.0 ship" + "PR 走 phase-c-integrator merge 时 dual-layer 都生效" + Layer L claim 防止 race。机制描述对齐 M6 tasks.md L180-218 实际实现 (3-zone ancestry check)。非仅把 "blocks" → "strengthens" 关键词替换。 |
| I-tl-4 | "R7 stale branch" | ✅ Substance: 不是单纯加一行 risk, 而是 Risk + Mitigation + Validation Checklist + 决策 doc §6 四处链式 surfacing。Mitigation 三勺设计 (open PR scan ping / BLOCK output override hint / 决策 doc 记录) 三层防御独立有效。 |
| I-tl-5 | "~5-6h" | ✅ Substance: 不是单纯把 "~1.5h" 改成 "~5-6h", 而是 L10 总估算 + §How B.2 step 0 新增 ~1h 子步 + B.2/B.3/B.4/Phase D 4 段时间估算分别 surface, 加和与总估算一致。data analysis + decision doc owner signoff 作为 explicit step 而非 implicit overhead。 |
| I-tl-6 | "tripwire_health" | ✅ Substance: schema 4 字段 (runs_in_window / last_manual_run_timestamp / ready_for_schedule_enable / notes) 对应 parent Spec §R9 cron health signal 真实需求 (workflow_dispatch 期手工触发 verify); checklist 同步加 "至少手工 dispatch 触发 1 次" — execution-grounded, 非仅 schema 加字段。 |
| I-tl-7 | "Trigger F >15%" | ✅ Substance: 不仅 §决策框架 表格加行, 同时在 §观察期数据 YAML override_rate 字段注释 + Default-on policy 末句加 "AND override rate ≤ 15%" 三处链式 enforcement; Trigger F 优先级 > A/B 显式声明 (因高 override 表明 rollback 频繁, block 翻转会引发 friction) — 与 root cause (override usage 是 gate sensitivity proxy) 对齐。 |

**Paper-fix check 结论**: 7 / 7 Important 均为 substance-level fix (同根因 + 同机制 + 多 surface 链式 enforcement),无 surface keyword 替换 antipattern。

---

## Strengths of Rev1

- **Multi-issue batch-fix 一致性极强**: Rev1 同时吸收 tech-lead 7 Important + qa 2 Critical + 13 Important + code-reviewer 8 Minor (共 30 项 fix),无 fix-互相冲突的痕迹。
- **§A 三段重构 (A1/A2/A3)** 是 Rev1 最大架构改善 — 把单一 "默认值翻转" 拆为三层 SOT taxonomy (runtime / doc-illustrative / config doc),为 ship 当天三处同步翻转提供机械化清单 + grep batch-review 方法,执行风险显著降低。
- **§标注操作流程 (L178-189) 新增** (per R1 QA C-2) 是 Rev1 最重要的 process-level 补充 — 把 parent Spec L237 的抽象 "human_reviewed_as_fp" 字段 转化为 5 行可执行表格 (标注时机 / owner / 操作方式 / 判定依据 / D+14 null 处理 / owner sign-off),消除 ship-day 数据汇总盲区。
- **§决策框架 Trigger C "Insufficient warm observation" 与 §Risk R1 fallback 一致性强化** — Trigger C 推荐默认 (a) extend per R1 QA I-3,与 R1 fallback 默认推荐一致,Trigger D "中间地带覆盖" (5 events / 1 FP = 20% 视为 requiring redesign) 也 surface — 决策表格的 corner case 完备度显著提升。
- **§Risk R1 max defer outer bound (D+42)** 是 Rev1 新增的硬约束 (per R1 QA I-4),防止 fallback (a) extend 无限延后 — 设置 D+42 = D+28 (20-PR window) + D+14 (buffer),并在超过此日期时 fallback 到 (b) flip with risk-acceptance。决策路径 well-bounded。
- **Phase B step 0 ~1h data analysis 显式列出 4 jsonl 文件读取 + Forgejo API cross-ref + 计算公式** — execution-grounded, 非抽象 "汇总数据"。`forgejo GET /repos/10CG/Aria/pulls?state=closed&base=master&merged=true` 命令直接给出, ship 当天可零思考执行。
- **§观察期数据 YAML schema 完备**:critical fields (drive decision) / gate health diagnostics / per_pr_breakdown / override_usage / tripwire_health 五组字段分离, 各组职责清晰 — 比 R1 时单一 flat schema 可读性 + 可执行性显著提升。
- **Cross-references "Rule references" 5 行 + "Memory references" 7 行** — 把 Aria CLAUDE.md §不可协商规则 #6/#7/#8/#9 + §版本管理规范 + 6 个 memory 全部 cross-ref, traceability 完整。
- **Validation Checklist 三段 (Phase A.1 / Phase A.2 / 2026-06-07 当天)** 显式分离, ship 当天 11 项 pre-ship checklist 覆盖 R1 全部修订点 (R7 open PR ping / tripwire 手工 dispatch / FP labeling D+14 null 处理 / Trigger override_rate ≤ 15% verify) — 是 R1+R2 修订的 enforcement 落点。

---

## R2 verdict reasoning

本 R2 audit 判定 **CONVERGED** (verdict = PASS_WITH_WARNINGS, 与 R1 同级别但实质改善)。判定依据:

1. **R1 Important 7 项全部 CLOSED, 无 PARTIAL / OPEN**:逐项核查 substance-level (同根因 + 同机制),非 surface keyword 替换。Paper-fix antipattern guard 通过。

2. **无新 Critical 或 Important 引入**:Rev1 30 项 batch-fix 内部一致, 未出现 fix-互相冲突 (e.g., §F immutability fix 与 §C v1.29.0 entry 同步, §R5 dual-layer 三处口径完全一致, §决策框架 Trigger F 与 §观察期数据 YAML override_rate 字段三处链式 enforcement)。仅 2 项 Minor (n-tl-1 acceptance window outer bound / n-tl-2 events 口径含义) 可在 ship-day inline 处理, 不阻塞。

3. **Verdict 改善显著**:虽然 R1+R2 均为 PASS_WITH_WARNINGS, 但 R2 issue count 大幅下降 (R1: 7 Important + 10 Minor → R2: 0 Important + 2 Minor)。符合 [[feedback_post_spec_audit_pragmatic_convergence]] "unanimous PASS + verdict 改善 + 无振荡" 实质收敛标准。

4. **Level 2 baseline 完全契合**:per [[feedback_post_spec_audit_two_round_pragmatic_for_l2]], Level 2 R1+R2 unanimous PASS_WITH_WARNINGS = 收敛 (单 session ~1h 跑完),与 4-round Level 3 baseline 互补。本 Spec 作为 parent v1.28.0 ship 的 follow-up flip Spec, mechanism 零新增, 严格符合 Level 2 "Minimal" 定位 — Rev1 后已达到 ship-ready 状态。

5. **架构 soundness 二次确认**:R2 通读 Rev1 全文 (369 lines), 关键架构判定均无 regression:
   - 5+1 SOT bump (§C) 完整, aria-plugin v1.29.0 + Aria main v1.7.1 双轨 separate-bump 设计合理
   - dual-PR sequenced merge (§How B.3 → B.4) 符合 [[feedback_sequenced_multirepo_gitlink_bump]] 三段式
   - chicken-and-egg 注释 (B.4 step 4) 正确描述 main repo PR 自身仍跑 v1.28.0 warn-mode, 首个 real block dogfood 是 D+15 next PR
   - Layer L claim (§How B.1) 防止与 M6 共改 standards/ race
   - Risk R6 区分 Spec doc immutable vs SKILL.md code mutable, drift surface 路径明确 (ship-day step 0 数据汇总会暴露 hotfix SHA)

6. **ship readiness**:Spec 已具备 ship-day execution 所需全部信息 — file paths + line numbers + 验证命令 + 时间估算 + 决策 trigger 表格 + acceptance criteria + fallback paths + max defer outer bound。Phase B ship-day owner 可零思考执行。

**建议 owner 操作**: 批准 Rev1 → Spec Status 更新为 **Approved** → 进入等待期 (D+1 ~ D+14) → 2026-06-07 ship。R2 verdict 不阻塞 Approved。2 项 n-tl Minor 可在 ship-day 落地阶段 inline 处理或写入决策 doc §3 rationale 中, 无需 Rev2。

---

**Audit completed**: 2026-05-25
**Convergence outcome**: R1 PASS_WITH_WARNINGS + R2 PASS_WITH_WARNINGS unanimous (tech-lead 维度) — 符合 Level 2 baseline。等待 qa + code-reviewer R2 verdict 聚合 unanimous 后, Phase A.2 完结, Spec Approved。
**Report path**: `.aria/audit-reports/post_spec-R2-tl-2026-05-25-aria-submodule-gate-block-flip.md`
