---
type: deferred_acceptance_waiver
spec_id: aria-2.0-silknode-integration-contract
expires_at: 2026-08-05T23:59:59Z
sign_off_mechanism: pr_approval
approved_by: solo-lab (uni.concept.wzfq@gmail.com) via archive commit
status: deferred
audit_loop_rounds: 3
audit_loop_outcome: converged
---

# Owner Decision — silknode-integration-contract Archived with Explicit Waiver

> **Date**: 2026-05-07
> **Decider**: solo-lab (uni.concept.wzfq@gmail.com)
> **Type**: Governance disposition (Spec lifecycle closure with deferred acceptance)
> **Trigger**: 3-round multi-agent Spec discussion loop converged 2026-05-07 (4 agents: legal-advisor + tech-lead [discussion] / backend-architect + qa-engineer [challenge])
> **Status**: Active deferral until 2026-08-05 (90-day hard cap matching `2026-05-02-secret-rotation-deferred.md` precedent)

---

## 决策

将 `openspec/changes/aria-2.0-silknode-integration-contract/` (Draft 2026-04-14) 归档为 `openspec/archive/2026-05-07-aria-2.0-silknode-integration-contract/`, Status 改 Draft → Complete (Archived-with-Waiver), **接受其 4 项 acceptance criteria 中 3+4 项为 deferred-acceptance 状态** (非 silent drop)。

**Contract 2 (业务数据分类约束) was never mechanically enforced in M2 development and carries explicit waiver until 2026-08-05.**

## Acceptance Criteria 逐项判定

| # | Acceptance | 判定 | 证据 |
|---|------------|------|------|
| (a) | US-022 起草时 proposal.md 含 §契约 1 原文 | ✅ **MET** | `openspec/archive/2026-05-03-aria-2.0-m2-layer1-state-machine/proposal.md` L223-230 verbatim 引用 §契约 1 (line 31-40 of source Spec); 10 grep hits 累计 (含 acceptance §E + tasks T8/T9/T10 inheritance) |
| (b) | US-023 起草时 fallback 路径含 §契约 1 | ✅ **MET (retroactively confirmed)** | `openspec/archive/2026-05-06-aria-2.0-m3-cycle-close-glm-routing-recovery/proposal.md` L132 OD-3d **generalize** 契约 1 至所有 LLM provider (含 ZhipuClient direct-connect); marker `(deprecated)` at L369 reflects superseded-by-generalization, NOT abandonment. R3 owner ack: see `.aria/decisions/2026-05-02-od-9-luxeno-reframe.md` retroactive ack section appended 2026-05-07 |
| (c) | US-025 起草时 tasks.md 含 `silknode_storage_check` + `business_data_classification_check` | 🟡 **DEFERRED with detection stub** | US-025 not yet kicked off. Minimum-viable detection stub added in same commit as this waiver: `.aria/state-checks.yaml::silknode-contract-deferral-expiry` (WARN-on-expiry-or-trigger-met). Full audit checks remain US-025 scope when started |
| (d) | PRD v2.0 / CLAUDE.md 修订时 §契约 2 原文写入 | 🟡 **WAIVED until 2026-08-05** | grep against `CLAUDE.md` + `docs/requirements/prd-aria-v2.md` returns 0 hits for "silknode" / "no-storage" / "business_data_classification". US-026 not yet scoped. **Contract 2 was never mechanically enforced in M2; explicit waiver applies until 2026-08-05 hard cap or US-026 kickoff (whichever first)** |

## 触发条件 (强制 — 任一命中即重新评估)

仿 `2026-05-02-secret-rotation-deferred.md` §触发条件 4 项 pattern:

1. **US-025 kickoff** (Phase A.1 起 Spec, 包含 audit-engine `silknode_storage_check` + `business_data_classification_check` 实施任务)
2. **M5 production launch milestone 评审** (Aria 2.0 production launch 决议时点)
3. **r1-legal-memo expires_at 到期** 或 **业务范围变化** (Aria 2.0 处理类别从"技术工单/代码/方法论"扩展至 PII/支付/医疗/重要数据等任一)
4. **2026-08-05 硬时限护栏** (90 天, dev 期不无限拖延; 即使 1/2/3 都未触发也强制重审)

## 决策理由

| 因素 | 说明 |
|------|------|
| Discussion loop convergence | 3-round 4-agent Spec discussion 最终 R3 CONSENSUS REACHED (challenge group 0 objections); direction ALIGNED 全 3 rounds |
| Memo v1.1 audit chain | 保持完整 (Memo → Spec waiver → Code US-022/023 → Audit detection stub) — 不 sever bidirectional binding |
| Aria 小步迭代原则 | US-025 / US-026 设计深度需独立 Spec; 本 waiver 不强制设计这些 Spec |
| 1-人 lab 资源 | per AD-M0-9, owner = decision authority = PR approver; pr_approval 即 sign-off mechanism |
| Detection stub feasibility | `.aria/state-checks.yaml` 探针 ~15 行 YAML, 当前 commit 落地, 防 scaffold-helpers-drift 反 pattern (`feedback_scaffold_helpers_drift_without_callers`) |
| 90-day vs 180-day | 选 90d 与 secret-rotation precedent 对称 (`feedback_audit_driven_fix_conventions` 治理一致性优先于 Memo 年度 cadence) |

## 落地工件 (本 commit)

1. **本文件** `.aria/decisions/2026-05-07-silknode-contract-archive-with-deferred-acceptance.md`
2. **新增 state-scanner 探针** `.aria/state-checks.yaml::silknode-contract-deferral-expiry` (WARN if `expires_at < now()` OR 触发条件命中)
3. **OD-9 retroactive owner ack** 段追加 (resolves acceptance #(b) Phase A.2 conditional)
4. **Spec 归档** `openspec/changes/aria-2.0-silknode-integration-contract/` → `openspec/archive/2026-05-07-aria-2.0-silknode-integration-contract/` + Status: Draft → Complete (Archived-with-Waiver)

## 重新评估时 SOP (任一触发条件命中后)

1. 读取本文件 §Acceptance Criteria 逐项判定表
2. 检查 deferred items (c+d) 当前状态:
   - (c) US-025 是否已 kickoff? 若是 → 验证 `silknode_storage_check` + `business_data_classification_check` 任务已写入 US-025 tasks.md
   - (d) US-026 / PRD v2.0 / CLAUDE.md 是否含 §契约 2 原文? grep 验证
3. 决定: 关闭 waiver (acceptance 全 MET) / 续期 waiver (新文件, 新 expires_at) / upgrade 至 standards/governance/silknode-no-storage.md
4. 更新本文件 `status` 字段 + 写 closure 段

---

## 2026-08-05 到期重评 — 核实结果与两条前提质疑 (**待 owner 裁决, 本段不做决定**)

> 触发方式: `.aria/state-checks.yaml::silknode-contract-deferral-expiry` 于 2026-08-05 转红 (custom checks 8/8 → 7/8), 由 session 收尾的机械检查捕获。执行 §重新评估 SOP 第 1-2 步, 第 3-4 步 (决定 + status 变更) **留给 owner**。

### 触发条件命中情况: 4 条中 3 条

| # | 条件 | 状态 |
|---|------|------|
| 1 | US-025 kickoff | ✅ **早已命中** — US-025 不仅 kickoff, 已于 **2026-05-23 done** (M5 Phase D.2 close) |
| 2 | M5 production launch 评审 | ✅ **已命中** — M5 已 close |
| 3 | r1-legal-memo 到期 / 业务范围变化 | ❌ 未命中 — memo `expires_at: 2026-10-14`, 尚余约 70 天 |
| 4 | 2026-08-05 硬时限 | ✅ **今日命中** |

**值得记录的治理事实**: 条件 1 在 **2 个多月前**就已命中, 但无人回到本文件重评 —— 最终是靠条件 4 (90 天硬顶) 兜住的。这印证了 R2 阶段 backend-architect 坚持「90 天而非 180 天」的价值: 没有那道硬顶, 该 waiver 至今仍在无声延期。

### (c) 核实: 不是「还没做」, 是**做完了但漏了**

原判定假设「US-025 尚未 kickoff, 两个 check 留待启动时实现」。实测:

- US-025 已 **done (2026-05-23)**, 846 Python + 57 bash 测试全绿归档;
- 全仓 grep `silknode_storage_check` / `business_data_classification_check` → **仅命中本文件与归档源 Spec**, US-025 全文 **0 处提及**。

⇒ 这两个 check 的**唯一实施窗口 (US-025 的 Phase A.1) 已经过去且未被利用**。继续标 "DEFERRED with detection stub" 已不准确 —— 现状是 **MISSED**。

### (d) 核实: 与 90 天前**逐字相同**

复现原判定的同一组 grep (对 `CLAUDE.md` + `docs/requirements/prd-aria-v2.md`):

| 词 | 2026-05-07 | 2026-08-05 |
|----|-----------|-----------|
| `silknode` | 0 | **0** |
| `no-storage` | 0 | **0** |
| `business_data_classification` | 0 | **0** |

而 US-026 (契约 2 的指定消费方) 状态为 `in_progress`, 4 个 sub-Spec 已归档 2 个 —— **它一直在推进, 只是没带上这条**。

### owner 前提质疑一: 契约 1 越界 (约束的是别人的代码)

owner 2026-08-05 提出: 「silknode 的东西为什么要在 aria 里处理?」

核实后确认该质疑成立, 但要害在于**本 Spec 混装了两件性质不同的东西**:

| | 约束对象 | Aria 的实际能力 | 归属 |
|---|---|---|---|
| 契约 1 | silknode/Luxeno **的实现行为** (不许加 cache/落盘) | 只能纸面继承 + 静态扫描, **无写权限** | ⚠️ 越界 |
| 契约 2 | **Aria 自己**的业务数据范围 | 自己的 PRD/CLAUDE.md | ✅ 本属 Aria |

契约 1 的两个 enforcement 手段都很弱 (下游 Spec 逐字抄 = 纸面; `silknode_storage_check` = 从外部扫别人仓库找持久化痕迹)。**后者 90 天从未实现, 恐非偶然 —— 它本身就是个越界的活儿。** 更合理的归属是: 该约束在 silknode/Luxeno 侧成文并自测, Aria 这边只保留「假设失效 ⇒ 触发 r1-legal-memo 重评」的记录。

### owner 前提质疑二: 契约 2 与 Aria 的产品定位自相矛盾 (**本次最重要的发现**)

owner 追问: 「aria 是负责管理 AI 开发的, 为什么就不处理 PII/支付/医疗? 如果开发的项目需要这方面的数据呢?」

**该质疑成立, 且 2026-05-07 的 3 轮 4-agent 审计未曾触及。** 问题在于契约 2 混淆了两个层次:

| | 是什么 | 由谁决定 |
|---|---|---|
| 数据**载体** | issue body / code diff / prompt | Aria 固定, 永远这三样 |
| 数据**内容** | 那些 issue 与 diff **里装着什么** | **完全取决于用 Aria 开发的是什么项目** |

契约 2 声称限制第一列, 但 r1-legal-memo 的 IS-4 结论真正依赖的是第二列 (memo 原文: 「Aria issue/code 内容**通常**不含个人信息」)。

具体反例 — 用 Aria 开发一个医疗系统时: issue 讨论病历字段 / code diff 含病历处理逻辑 / 测试 fixture 塞样例病历 / 排障时贴了脱敏不彻底的日志。**载体类型未变, 内容分类彻底变了, 而这些全会流经 Luxeno 发往 GLM。**

而 Aria 的定位 (CLAUDE.md 首行) 是「AI-DDD 方法论的定义与端到端参考实现」——**通用**开发方法论工具。通用工具无法预先承诺「我管理的所有项目都不碰敏感数据」。故契约 2 原文存在三种读法, 均不成立:

- 读法 A「Aria 不得用于开发涉及 PII/支付/医疗的项目」→ 与「通用方法论」定位直接冲突;
- 读法 B「Aria 的 issue/prompt 中不应出现真实 PII」→ 合理, 但那是**数据卫生纪律** (与 Rule #7 secret-hygiene 同类), 不是「业务数据范围」;
- 读法 C「10CG Lab 目前的项目不涉及这些」→ 属**当下事实快照**而非可执行约束, 一旦接入相关领域客户即失效。

原文「判定权由产品负责人在 PRD 修订时判定分类归属; 工程师不得自行扩展业务数据范围」的措辞指向读法 A 或 C。

**这解释了 (d) 为何 90 天零进展**: acceptance (d) 要求「逐字抄进 CLAUDE.md」, 而只要真的动笔, 第一句「Aria 2.0 的业务数据范围仅限于……」写进一个通用方法论工具的 CLAUDE.md 就会立刻自相矛盾。**该条 acceptance 可能不是被遗忘, 而是写不出来。** 到期探针只盯日期, 盯不出「要求本身有问题」—— 与 memory `feedback_perpetual_red_check_may_encode_stale_convention` 同型。

### 供裁决参考的拆分建议 (非决定)

原 SOP 第 3 步的三个选项 (关闭 / 续期 / upgrade) 均建立在「契约 1+2 作为一个整体」之上。基于上述两条质疑, 建议先拆再选:

- **契约 2 → 重写而非照抄**, 拆成两条可执行的:
  - **数据卫生纪律** (Aria 自己可保证): 送入 LLM 的 issue/diff/prompt 不得含真实 PII / 支付凭据 / 医疗记录; 需样例时用合成数据。与 Rule #7 同类, 可有 hook 层 enforcement。
  - **法务结论的适用范围声明** (Aria 只能声明): r1-legal-memo v1.1 的 IS-4 结论**以「当前 10CG Lab 自身项目场景」为条件**; 若某个使用 Aria 的项目其领域数据本身属 PII/重要数据类别, 该结论对该项目不适用, 需单独评估。—— 把判断下放到具体项目, 而非让通用工具做全局承诺。
- **契约 1 → 归属迁移**: 在 silknode/Luxeno 侧成文并自测; Aria 侧仅保留失效触发记录, 不假装能 enforce 外部代码。

**以上均为分析与建议, 不构成决定。** `status` 字段维持 `deferred` 未改动 —— 关闭 / 续期 / upgrade / 重写 的裁决权归 owner (per AD-M0-9)。

---

## Audit Trajectory (3-round convergence)

| Round | Discussion group (legal-advisor + tech-lead) | Challenge group (backend-architect + qa-engineer) | Outcome |
|-------|----------------------------------------------|-------------------------------------------------|---------|
| **R1** | archive-as-absorbed (US-022 verbatim consumed + US-023 OD-3d generalized) | backend-architect: PARTIAL CONCUR (demand explicit waiver in `.aria/decisions/`); qa-engineer: OBJECTION (#d FAIL grep 0, #c UNTESTABLE, counter-proposal HOLD OPEN) | NOT_CONVERGED → R2 |
| **R2** | archive-with-explicit-waiver (legal-advisor: granular PASS/DEFER/WAIVE per criterion; tech-lead: 4 trigger conditions + 180-day hard cap) | backend-architect: BLOCKING — 90d not 180d + verbatim language + sign_off_mechanism field; qa-engineer: 4 OBJECTIONS (Phase A.2 papered over / #c stub commitment / expires_at machine-readable / explicit owner sig) | NOT_CONVERGED → R3 |
| **R3** | unified: 90d (concede to backend-architect) + verbatim "never mechanically enforced" + sign_off_mechanism: pr_approval + #b retroactive OD-9 ack + #c detection stub in-scope + expires_at YAML + audit trajectory | backend-architect: CONSENSUS REACHED 0 objections; qa-engineer: CONSENSUS REACHED 0 objections | **CONVERGED** |

Per `feedback_audit_convergence_pattern.md` strict definition: discussion group internally consistent across R3 + challenge group 0 objections + direction ALIGNED 4/4 全 3 rounds = 收敛达成.

## 跨引用

- `r1-legal-memo.md` v1.1 (`aria-orchestrator/docs/r1-legal-memo.md`) — 本 Spec 的源头依据
- `openspec/archive/2026-05-03-aria-2.0-m2-layer1-state-machine/proposal.md` — Acceptance (a) 证据
- `openspec/archive/2026-05-06-aria-2.0-m3-cycle-close-glm-routing-recovery/proposal.md` L132 + L369 — Acceptance (b) 证据 (OD-3d generalize)
- `.aria/decisions/2026-05-02-od-9-luxeno-reframe.md` — retroactive owner ack 段 (本 commit 追加, resolves Acceptance (b) Phase A.2 conditional)
- `.aria/decisions/2026-05-02-secret-rotation-deferred.md` — waiver 模板先例
- `.aria/state-checks.yaml::silknode-contract-deferral-expiry` — 机械检测探针 (本 commit 落地)
- `feedback_audit_convergence_pattern.md` / `feedback_audit_driven_fix_conventions.md` / `feedback_ad_slot_backfill_checkpoint.md` / `feedback_scaffold_helpers_drift_without_callers.md` — 方法论 anchors

## 版本历史

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-05-07 | 初版. 3-round Spec discussion loop converged. Acceptance (a)+(b) MET, (c)+(d) deferred-with-waiver until 2026-08-05. Detection stub `.aria/state-checks.yaml::silknode-contract-deferral-expiry` 同 commit 落地. |
| 1.1 | 2026-08-05 | **到期重评输入段追加** (SOP 第 1-2 步, 未做决定, `status` 维持 `deferred`). 核实: 触发条件 4 中 3 命中 (条件 1 早在 2026-05-23 即命中却无人回看, 靠 90 天硬顶兜住); (c) 由 DEFERRED 实为 **MISSED** (US-025 已 done 但零提及两 check, 实施窗口已过); (d) 三个 grep 与 90 天前逐字相同 (全 0). 记录 owner 两条前提质疑: 契约 1 **越界** (约束外部代码, Aria 无写权限, 故其扫描器 90 天未实现恐非偶然); 契约 2 **与 Aria 通用方法论定位自相矛盾** (混淆数据载体与数据内容; 用 Aria 开发医疗/支付项目时敏感内容仍会经 issue/diff 流经 Luxeno) —— 后者为 2026-05-07 三轮四席审计**未曾触及**的盲区, 并解释了 (d) 90 天零进展的可能真因 (不是遗忘, 是写不出来). 附拆分建议供裁决. |
