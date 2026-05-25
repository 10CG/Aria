# post_spec R1 audit — aria-submodule-gate-block-flip (tech-lead)

**Date**: 2026-05-25
**Auditor**: tech-lead agent (Claude Opus 4.7 1M context)
**Spec under review**: `openspec/changes/aria-submodule-gate-block-flip/proposal.md`
**Level**: 2 (Minimal — proposal.md only, mechanism inherited from parent Spec)
**Parent Spec**: `openspec/archive/2026-05-24-aria-submodule-pointer-regression-gate/` (Approved 2026-05-24)
**Verdict**: **PASS_WITH_WARNINGS**
**Reasoning summary**: Spec 结构合理、cross-Spec sequencing 思路正确、5+1 SOT bump 清单完整且引用 [[feedback_release_phase_d_5_files_synchronization]]。但 §A1 默认值翻转位置存在 architectural placement 歧义 (第 3 处 SKILL.md L378 inline Bash 与 script L33 是 **parallel** 而非 "或" 的关系, 必须同步翻转), §观察期数据 schema 漏 `last_run_timestamp` (parent R9 NEW), Phase B+C+D ~1.5h 估时与 parent ~9h 实证不符, 缺 "stale-branch-after-flip" 风险条目。无 Critical 阻塞, Important 7 项可在 Rev1 一次性 batch-fix。

---

## Critical issues (must fix before Approved)

| ID | Issue | File / Section | Fix |
|----|-------|----------------|-----|
| _(none)_ | | | |

> Tech-lead 维度无 Critical。Spec 整体架构判断正确、ship 顺序基本合理、SOT bump 完整。下方 Important 列出的均为 quality / completeness 提升项, 不是 architectural soundness gap。

---

## Important issues (should fix before Approved)

| ID | Issue | File / Section | Fix |
|----|-------|----------------|-----|
| I-tl-1 | **§A1 默认值位置严重低估 — 实际有 3 处 (script + inline SKILL.md doc-Bash + config table), proposal 措辞 "或" 暗示二选一**。`submodule_gate.sh` L33 `MODE="${ARIA_SUBMODULE_GATE_MODE:-warn}"` 是 runtime 真理来源; `aria/skills/phase-c-integrator/SKILL.md` L378 同样的 `MODE="${ARIA_SUBMODULE_GATE_MODE:-warn}"` 是 doc-illustrative Bash 段 — **两者必须同步翻转**, 否则 doc/code drift。 | `proposal.md §A1` L40 措辞 "或 inline SKILL.md 代码块,取实际 implementation 位置" | 改 §A1 标题为 "Default flip in 3 places", 明确列出: (a) `aria/skills/phase-c-integrator/scripts/submodule_gate.sh` L33 (runtime SOT); (b) `aria/skills/phase-c-integrator/SKILL.md` L378 (doc-illustrative Bash); (c) `aria/skills/phase-c-integrator/SKILL.md` L47 + L184 + L307 + L443 (config table / 触发条件 / 配置参数 default 列, **§F 已含但 §A 未列**)。§A 应做 source-of-truth flip 清单 (代码 + config doc 默认值); §F 做 cross-reference / wording sync 清单 (历史叙述 / 说明文档)。 |
| I-tl-2 | **§F CHANGELOG 历史 entry 不应原地改写** — proposal §F 表格行 "aria/CHANGELOG.md v1.28.0 entry L32 'v1.29.0 (planned, ...)' 改为 'v1.29.0 shipped 2026-06-07'" 违反 CHANGELOG immutability 原则 (历史 entry 反映 release-time state, 不应回写未来事件)。Keep-a-Changelog convention: 在 v1.29.0 **新 entry** 中记 "shipped per v1.28.0 §Two-phase rollout 承诺", v1.28.0 entry 保留 "(planned)" 历史措辞 + 可选追加注释 "(see [1.29.0] for actual ship)"。 | `proposal.md §F` 表格第 2 行 | 改 §F 该行为: "aria/CHANGELOG.md v1.29.0 **NEW entry** L? 包含 'flips v1.28.0 warn→block per Two-phase rollout 承诺, observation 数据见 .aria/decisions/2026-06-07-v1.29.0-block-flip.md'; v1.28.0 entry L32 'v1.29.0 (planned, ...)' **保留原文** + 可选 inline 注释 `<!-- shipped 2026-06-07 see [1.29.0] -->`。" |
| I-tl-3 | **R5 跨 Spec sequencing 描述 over-states M6 T-B0.10 对本 Spec 的依赖**。审阅 `openspec/changes/aria-2.0-m6-docs/tasks.md` L180-218 后, T-B0.10 是 **inline self-contained gate** (3-zone ancestry check, PASS/REGRESSION/DIVERGENT), 不依赖 phase-c-integrator §C.2.4.5 runtime — 它是 v1.29.0 block-mode 行为的**人工预演**, 而非消费 v1.29.0 已 ship 的 gate。真正的 cross-Spec 影响是: M6 整体 PR 走 phase-c-integrator merge 时会被 §C.2.4.5 block-mode 拦截 (若 standards pointer 不是 forward) — 这是 **dual-layer**: T-B0.10 inline check (caller-side pre-stage gate) + §C.2.4.5 (PR-side merge gate)。 | `proposal.md §Risk R5` + §Why "Why blocks downstream" 段 | 改 R5 描述: "(a) M6 T-B0.10 inline ancestry check 已 self-contained, **不依赖** v1.29.0 ship; (b) 但 M6 整体 PR 走 phase-c-integrator merge 时会被 §C.2.4.5 block-mode gate 二次验证 (dual-layer defense)。若 M6 PR 在 v1.29.0 ship **之前** 合 master, 则只有 T-B0.10 inline check 生效; 若在 v1.29.0 ship **之后**, 则 dual-layer 都生效。**实际 sequencing 推荐**: 本 Spec v1.29.0 先 ship → M6 PR 享受 dual-layer。Layer L claim 协调避免共改 standards/。" 同步修订 §Why L30 "v1.29.0 ship → unblock M6 T-B0.10" wording, 改为 "v1.29.0 ship → strengthen M6 T-B0.10 defense to dual-layer"。 |
| I-tl-4 | **缺 Risk R7 (NEW): "stale-branch-first-merge-after-flip" — long-lived feature branch 在 v1.28.0 warn-only 期间最后 push, 但 v1.29.0 ship 后才走 merge 的场景**。若该 branch 含 legitimate submodule rollback (e.g., revert v1.24.1 bug), v1.28.0 期间只 log WOULD-BLOCK 未告知 owner 加 override; 翻转后首次 merge 直接 exit 1 → owner 需临时学习 override 机制。R3 提及 "override 已 14d 教育期" 但教育覆盖度依赖 owner 在 v1.28.0 期间 **观察了 warns.jsonl**, 没有保证。 | `proposal.md §Risk + Mitigations` 表格 | 新增 R7: "**stale-branch-first-merge-after-flip** — Likelihood: LOW-MEDIUM (Aria 项目 PR 频次低, long-lived branch 少). Mitigation: (a) ship 当天审 open PRs 列表 (`forgejo GET /repos/10CG/Aria/pulls?state=open`), 对涉及 submodule pointer 改动的 PR 主动 ping owner 提醒 override; (b) BLOCK 输出已含 override hint (parent ship); (c) 决策记录 doc §6 (NEW section) 记录 ship 当天 open PRs 审查结果 + 是否触发 ping。" 同步在 §Validation Checklist 2026-06-07 当天加 checklist "[ ] ship 前审 open PR 列表, identify submodule-touching PRs"。 |
| I-tl-5 | **Phase B+C+D ~1.5h 估时与 parent ~9h 实证不符**。Spec L10 声称 "2026-06-07 当天 §观察期数据填充 ~0.5h + Phase B+C+D ~1.5h SOT bump + flip flag + tripwire cron + CHANGELOG + PR ship" = 总 2h。但 (a) §观察期 14d FP 数据汇总 + 决策 trigger 选择 + 决策 doc 起草 + owner signoff ~1.5h 起 (parent qa R3 FP labeling 流程是 manual); (b) 6 项 deliverable (A1 + A2 + B + C + D + E + F 措辞同步) 实际 ~1-2h; (c) replay test 13 assertions 重跑 ~0.5h; (d) 2 个 PR sequenced merge (aria-plugin → 主项目 gitlink re-bump per [[feedback_sequenced_multirepo_gitlink_bump]]) + multi-remote push ~0.5-1h; (e) Phase D handoff + archive ~0.5h。**realistic 总估时 ~4-5h**。低估会导致 ship 当天压力 → cut corners (如跳过决策 doc owner signoff)。 | `proposal.md` L10 + §Effort baseline + §How "实现序列" | 改 L10 effort baseline 为: "~5-6h end-to-end (Phase A.1 ~1h skeleton + A.2 audit ~1h + 2026-06-07 当天 §观察期数据汇总 ~1.5h + Phase B 实施 ~1.5h + Phase C dual-PR sequenced merge ~1h + Phase D archive + handoff ~0.5h)"。同步在 §How B.2 加 step 0 "data analysis ~1h" 并展开 step 3-8 时间估算。Load-bearing assumption: parent ship 已建立 mechanism, **B 阶段 zero new code**, 仅 default flip + cron append + measure update。这个 assumption **正确**, 但 data analysis + decision doc owner signoff 是新增 cognitive load, 不能 ignore。 |
| I-tl-6 | **§观察期数据 schema 漏 tripwire `last_run_timestamp` 字段 (parent Spec §R9 NEW Rev1 R1-qa M-qa-3 引入)**。parent Spec 明确要求 tripwire cron 每次 run 都写 `last_run_timestamp` 到 `misses.jsonl`, 用作 cron 失活的 health signal。观察期数据 (`§观察期数据` L175-207 YAML schema) 应预留 tripwire health subsection (即使 v1.28.0 期 tripwire 是 workflow_dispatch only, owner 仍可手动触发 ≥1 次验证 cron 在 ship 后 enable 时可工作)。 | `proposal.md §观察期数据` YAML schema L175-207 | 在 YAML schema 追加 subsection: `tripwire_health: { workflow_dispatch_runs_in_window: <int>, last_manual_run_timestamp: "...", ready_for_schedule_enable: true|false, notes: "..." }`。同步在 §Validation Checklist 2026-06-07 当天加项: "[ ] tripwire workflow 至少手工 dispatch 触发 1 次, 确认 ready for schedule cron enable"。 |
| I-tl-7 | **§决策框架 缺 override_rate 判断分支** (parent Spec qa R1 metric "override usage rate >15% 触发 re-calibration")。当前决策表只看 FP rate + event count + hard date, 没有把 override usage rate 纳入翻转判定。若 v1.28.0 期间 override rate 已 >15% (合理 rollback 频繁), block 模式翻转会引发更多 friction → 应延后翻转 + 重审 gate sensitivity。Risk R4 提及 monthly review 但未纳入 ship-day decision criteria。 | `proposal.md §决策框架` 表格 + §观察期数据 YAML | 在 §决策框架 表格新增 Trigger F: "**F. High override-usage (>15%)** — `override_rate (trailer+label)/total_PR_merges_in_window > 15%` → **不翻转**; file 新 OpenSpec 重审 gate 灵敏度 + 是否扩展 override 机制 (e.g., persistent label class)。" 同步在 §观察期数据 YAML `override_usage.override_rate` 字段下方加注释 "**>15% triggers Trigger F deferral**"。 |

---

## Minor issues (nice-to-have polish)

| ID | Issue | File / Section | Fix |
|----|-------|----------------|-----|
| m-tl-1 | §F 文件列表 L97 "行 47/180/192/229-230/300-301/378-381/414-415/443/450 等" 列举不全且 fragile (line number 在 R2 rev 后可能 drift); L184 (新发现的 "warn (v1.28.0 default) / block (v1.29.0 default)" 描述行) 未列。 | proposal.md §F L97 | 改为半结构化清单: "所有 v1.28.0/v1.29.0 时态说明行 (含但不限于 L47/L180/L184/L192/L229-230/L300-301/L307/L378-381/L414-415/L443/L450); ship 当天用 `grep -nE 'v1\\.28\\.0\\|v1\\.29\\.0' aria/skills/phase-c-integrator/SKILL.md` 取全集再 review"。 |
| m-tl-2 | §观察期数据 YAML `total_pr_merges_in_window` 字段需明确口径 — 是 master 所有 merge 还是仅 phase-c-integrator-触发的 merge? 决定 override_rate 分母。 | proposal.md §观察期数据 L203 | 加注释 "// 口径: 主项目 + aria-plugin + standards 三仓 master 在 window 内所有 merge commits (forgejo API: `pulls?state=closed&base=master&merged=true`); 不计 dev/feature 分支 merge"。 |
| m-tl-3 | §How B.4 step 4 "本次是首次真正 cross-validate: aria submodule 从 v1.28.0 SHA → v1.29.0 SHA, 应是 forward 关系 → verdict=pass" — 但**此时 §C.2.4.5 mode 仍是 warn** (主项目 PR 此时 aria-plugin 已 ship v1.29.0 但**主项目仍嵌着旧 aria 子模块**, 主项目运行的 phase-c-integrator 是子模块 commit 时刻的版本)。chicken-and-egg 需澄清 — 实际 dogfood block-mode 需要 v1.29.0 已 active 在 phase-c-integrator runtime 里。 | proposal.md §How B.4 step 4-6 | 加 clarification: "**重要**: 主项目 PR 跑 §C.2.4.5 时, 嵌入主项目的 aria submodule **尚未** 翻 v1.29.0 (此 PR 的目的就是 bump 它)。phase-c-integrator runtime 仍是 v1.28.0 warn-mode。主项目 PR merge 完成后, 下一个 PR (D+15 或更晚) 才是 first real block-mode dogfood。Validation Checklist '[ ] post-merge dogfood' 措辞改为 'next PR after main-repo merge 触发 §C.2.4.5 mode default = block'。" |
| m-tl-4 | §Cross-references "Downstream blocked" L271 措辞 "blocked on v1.29.0 ship" 与 I-tl-3 修订冲突 — 实际是 "strengthen to dual-layer", 不是 hard block。 | proposal.md L271 | 同 I-tl-3 一并改为 "Downstream strengthened by v1.29.0 (dual-layer defense)"。 |
| m-tl-5 | §How B.3 step 2 "C.2.4.5 (Rule #X submodule gate, 本次是首个 cross-validate dogfood — 本 PR 不动 submodule,gate 应 verdict=pass; 翻转后下次 PR 才真正验证 block 行为)" — "Rule #X" 占位符未替换 (parent Spec 决定 **NOT** 加 numbered Rule, 仅 convention SOT)。 | proposal.md §How B.3 step 2 L125 | 改 "Rule #X submodule gate" 为 "§C.2.4.5 submodule gate (per `standards/conventions/submodule-pointer-hygiene.md` convention, NOT numbered Rule per parent AD-FOLLOWUP-4)"。 |
| m-tl-6 | §Risk R6 "13 days won't change parent" — parent Spec **已 archived** (`openspec/archive/2026-05-24-...`), spec doc immutable; 但 `aria/skills/phase-c-integrator/SKILL.md` §C.2.4.5 本身可能在 13 天内被 hotfix (e.g., 若发现 bug)。R6 应区分 "Spec doc immutable" vs "Skill code mutable"。 | proposal.md §Risk R6 | 加注释 "Spec doc immutable; SKILL.md §C.2.4.5 code 仍可 hotfix — 但任何 hotfix 都会反映在 §观察期数据 (新版本 SHA + 行为变化), 在 ship 当天 step 1 数据汇总时会 surface, 不会 silent drift。" |
| m-tl-7 | proposal.md L7 "Parent Forgejo issue: Aria #124 (closed on parent ship)" — 应验证 issue 实际是否已 close (parent Spec §Acceptance L412 "Forgejo Aria #124 closed with PR reference" 是 mechanical D.2 step, 可能漏执行)。 | proposal.md L7 | Phase A.2 audit 期间 owner 用 `forgejo GET /repos/10CG/Aria/issues/124` 验证 state=closed; 若 still open, 在本 Spec ship 当天 D.2 一并 close (或主动 backfill close 在 D+1 ~ D+13 之间)。无需 spec 文本变化, 仅 audit checklist item。 |
| m-tl-8 | proposal.md §Why "(per qa R3 + code-reviewer R3 in parent audit)" L28 — 引用 parent audit agent verdict 时无 audit report 路径 cross-ref。 | proposal.md §Why L28 | 在第一处引用加 footnote-style cross-ref: "(per qa R3 + code-reviewer R3 in parent R2 audit, see `.aria/audit-reports/post_spec-R2-2026-05-24T1515Z-aria-submodule-pointer-regression-gate.md`)"。 |
| m-tl-9 | §Validation Checklist Phase A.2 "[ ] post_spec R1 audit (3-4 agents) — Level 2 baseline" — 3 vs 4 agent count 不一致 ([[feedback_post_spec_audit_two_round_pragmatic_for_l2]] 提示 Level 2 = 3 agents)。 | proposal.md §Validation Checklist L236 | 改为 "[ ] post_spec R1 audit (3 agents per Level 2 baseline: tech-lead + qa + code-reviewer) — per [[feedback_post_spec_audit_two_round_pragmatic_for_l2]]"。 |
| m-tl-10 | proposal.md L289 "Ship target: 2026-06-07 (D+14 hard date from parent v1.28.0 ship 2026-05-24)" — 2026-05-24 + 14d = 2026-06-07 (Sunday); ship 落在周日, owner availability 是否有保证? 若有 fallback (e.g., 顺延周一 06-08) 应明示。 | proposal.md L289 | 加 footnote: "*若 2026-06-07 (Sunday) owner 不在线, 顺延至 06-08 Monday; 不视为 deferral, 不需要 OpenSpec defer。*" |

---

## Strengths (what's done well)

- **5+1 SOT bump 清单完整** (§C 表格 + §D Aria main repo patch bump 分离) 直接引用 `[[feedback_release_phase_d_5_files_synchronization]]` 实证教训, 避免 v1.11.1 类型遗漏。
- **零新机制声明清晰** (Spec L36 "全部为 minimal-cascade") + §How "Mechanism 引用" L145-150 明确委托 parent Spec, 不重复 mechanism 描述 — 符合 Level 2 "Minimal" 定位。
- **§决策框架 5-trigger 表格清晰** (A FP-threshold preferred / B hard-date fallback / C insufficient / D high-FP / E explicit-defer), 涵盖 brainstorm 期间所有 surface 出来的边界条件, 与 parent Spec §Two-phase rollout L229-238 + R2 严格对齐。
- **§观察期数据 schema-as-placeholder 模式** 是结构早期固化 + 数据 ship 当天填的优雅折中, 避免 D+1 起草无数据 vs D+14 紧急起草两难。
- **Phase B+C+D 串行编排** (§How L106-141) 符合 [[feedback_sequenced_multirepo_gitlink_bump]] 三段式 (aria-plugin merge → re-bump → main repo merge), 不会 race-merge。
- **memory cross-ref 完整** (§Cross-references L279-284 引用 4 个 relevant memory, 含 [[feedback_dec_ship_target_staleness_verify]] 表明已做 A.0 version stake-out)。
- **R1 fallback 三路径设计周全** (extend / risk-accept / explicit-defer with 推荐默认), 符合 parent Spec Rev1 R1-qa-3 zero-activity guard 精神。
- **§Why "Why now (D+1) draft skeleton" 论证 4 条具体收益**, 不是泛泛 "提前规划好", 体现 [[feedback_dec_ship_target_staleness_verify]] 教训内化。

---

## Q-NEW (questions for owner, do not block PASS)

| ID | Question |
|----|----------|
| Q-tl-1 | M6 `aria-2.0-m6-docs` Spec 当前 ship target 是否仍是 v1.29.0 之后? 若 M6 提前 (e.g., 在 v1.28.0 期间 ship), 本 Spec §Why "blocks downstream" 段需要重写 — M6 不再被 "unblocked", 而是 v1.29.0 ship 后被 "strengthened to dual-layer"。owner 需明确 M6 当前 timeline 与本 Spec ship 日 (2026-06-07) 的先后关系。 |
| Q-tl-2 | 2026-05-24 ~ 2026-06-07 14d 内, 是否有 in-flight aria-plugin OpenSpec changes (除 M6 / 本 Spec 外) 可能影响 SKILL.md §C.2.4.5 行为? 若有, 本 Spec ship 时需 rebase + 重新审视 §A1 默认值翻转位置 (line numbers 会变)。 |
| Q-tl-3 | 决策框架 Trigger B "hard date + ≥3 events" 中, 若 D+14 时 events 数恰好 = 0 (Aria PR 频次低), §Risk R1 三 fallback 中 owner 倾向哪个? (a) extend 20-PR window 推迟到 D+30~60 ; (b) risk-accept + flip; (c) explicit-defer 1-2 周。proposal 当前推荐 (b) 但理由仅 "13/13 replay PASS" — owner 是否接受这是 sufficient 证据? |
| Q-tl-4 | `aria/metrics/submodule-gate-warns.jsonl` 在 Aria 项目根 vs aria-plugin 内 — parent ship 实际写到哪里? (script L42-47 自适应: `aria/metrics/` 优先 / `metrics/` fallback / `ARIA_METRICS_DIR` 覆盖) 数据汇总 ship 当天 owner 需明确指定路径, 否则可能漏汇总 (e.g., 一部分 events 在 `aria/metrics/`, 另一部分在 `metrics/` 因为不同上下文 invocation)。 |
| Q-tl-5 | 若 ship 当天发现 §观察期数据 提示 mechanism 有缺陷 (e.g., 一个 PR 误判 REGRESSION 但实际是 forward), 是否倾向 (a) v1.29.0 仍 flip + 同时 file v1.30.0 hotfix; (b) 不 flip + file 新 OpenSpec 重设计 (Trigger D)? proposal §决策框架 Trigger D 选 (b), 但与 (a) "ship-then-hotfix" 文化对比, owner 决策原则需明示。 |

---

## Verdict reasoning

本 Spec 作为 Level 2 follow-up 设计合理：parent Spec 已 ship 完整机制 (script + SKILL.md + 测试 + telemetry + convention doc + tripwire workflow draft), 本 Spec 仅承担 "default flag flip + cron enable + SOT bump + 决策记录" 4 类 minimal-cascade 操作, 符合 OpenSpec Level 2 "minimal" 定位。

**架构判断正确性**: 6 项 deliverable (A-F) 覆盖 parent §Two-phase rollout L229-238 的所有承诺 — default flip + cron enable + hard-date + minimum-observation guard + FP labeling + decision doc。Cross-Spec 与 M6 T-B0.10 的关系思路 (R5) 方向正确但**描述过度**了 "blocks" 关系 (I-tl-3), 实际是 dual-layer strengthening。Layer L claim 协调点出 (R5 末句 "Layer L claim 协调避免 race") 正确。

**Important issues 集中在三类**: (a) **§A 默认值位置盲点** (I-tl-1) — 必须明确 3 处 source-of-truth (script + inline doc-Bash + config table), proposal 当前 "或" 措辞会让 Phase B 执行者只改一处导致 doc/code drift; (b) **CHANGELOG immutability + override-rate 决策完整性** (I-tl-2, I-tl-7) — 影响 ship 当天决策框架严密性; (c) **estimation realism + risk completeness** (I-tl-4, I-tl-5, I-tl-6) — 影响 ship-day execution 顺畅度。所有 7 项 Important 都可在 Rev1 一次性 batch-fix (~30-45 min), 不需要重新结构 Spec。

**Risk completeness gap (I-tl-4)**: "stale-branch-first-merge-after-flip" 是 v1.28.0 → v1.29.0 跨版本交互的真实风险类别, parent Spec R3 提及 override 教育但未具体到此场景。本 Spec 应继承 + 显式列出。

**Estimation realism (I-tl-5)**: parent Phase B ~9h 是 from-scratch impl + replay test infrastructure; 本 Spec ~1.5h Phase B+C+D 假设 "zero new code" 是对的, 但忽略了 data analysis + decision doc owner signoff + dual-PR sequenced merge 的认知 + 操作开销。realistic ~4-5h, 仍是 single-session work, 但 ship 当天的时间预算应明示。

**No Critical**: 无架构 soundness gap, 无 SOT 文件遗漏, 无 cross-Spec hard conflict, 无 rule violation。Q-NEW 5 项均为 owner 政策决策 (M6 timeline / fallback 倾向 / metrics dir 口径 / ship-then-hotfix 文化), 不阻塞 PASS。

**Convergence outlook**: 按 [[feedback_post_spec_audit_two_round_pragmatic_for_l2]] Level 2 baseline (R1 REVISE-or-PASS_WITH_WARNINGS → Rev1 → R2 PASS_WITH_WARNINGS unanimous), 预期 R2 应能 CONVERGED。tech-lead 维度本 R1 verdict = **PASS_WITH_WARNINGS** (0 Critical, 7 Important), 在 Level 2 baseline 容忍域内 (Level 2 R1 允许 3-10 Important, 见 rubric)。建议 owner 批 Rev1 后直接进 R2, 无需 Phase A.2 卡顿。

---

**Audit completed**: 2026-05-25
**Next step**: 等待 backend-architect / qa / code-reviewer agent R1 verdict, owner 聚合后决定是否 Rev1 + R2。
**Report path**: `.aria/audit-reports/post_spec-R1-tl-2026-05-25-aria-submodule-gate-block-flip.md`
