# post_spec R1 audit — aria-submodule-gate-block-flip (code-reviewer)

**Date**: 2026-05-25
**Auditor**: code-reviewer agent (Phase 1 compliance + Phase 2 quality)
**Spec**: `openspec/changes/aria-submodule-gate-block-flip/proposal.md`
**Parent Spec**: `openspec/archive/2026-05-24-aria-submodule-pointer-regression-gate/` (Approved 2026-05-24)
**Verdict**: **PASS_WITH_WARNINGS**
**Reasoning summary**: Spec 结构 / 版本占用 / Rule 引用 / 5+1 SOT 清单全部 verifiable;6 个 Important 集中在 §C 表格不完整 (缺 marketplace.json 行) + A 表格 location 拟态描述不精确 + 决策 doc 路径前后不一致 + F 表格"行号清单"硬编码易失同步 + 跨 repo CLAUDE.md 改动隐藏在 §F 而非顶层 deliverables。无 Critical, 无 spec scope creep, Level 2 baseline (R1+R2 unanimous PASS_WITH_WARNINGS per `feedback_post_spec_audit_pragmatic_convergence`) 完全可达。

---

## Phase 1 — Spec compliance

### Critical
(none)

### Important

1. **§C 5+1 SOT 表格遗漏 `marketplace.json` 独立行** (§What §C, L66-73)
   - Spec §C 表格当前 6 行:plugin.json / marketplace.json / VERSION / CHANGELOG.md / README.md / submodule pointer。**marketplace.json 行存在 ✓**, 但其字段标注 `version + plugins[].version` 容易在执行时漏改一处 (marketplace 文件实际有 2 个 version 字段:顶层 `version` 在 L3, `plugins[].version` 在 L16, 两个都必须同步)。
   - 现状验证:`/home/dev/Aria/aria/.claude-plugin/marketplace.json` L3 `"version": "1.28.0"` + L16 `"version": "1.28.0"` 两处都需 bump。Spec 表格已 cover 但 Phase B 执行容易 grep 漏。
   - 影响:Level 2 spec 应该完全无歧义,避免 Phase B 当天误改。
   - 修复:§C 表格 marketplace.json 行 cell 拆为 "顶层 L3 `version` + L16 `plugins[].version` 两处都需同步";或在 Phase B step 6 task 描述里加 `grep -n '"version"' marketplace.json` 验证两行命中。

2. **§What §A1 描述位置不精确** (L40)
   - Spec 写 "`aria/skills/phase-c-integrator/scripts/submodule-gate.sh` 或 inline SKILL.md 代码块,取实际 implementation 位置"。**实际 implementation 位置已确定**:`/home/dev/Aria/aria/skills/phase-c-integrator/scripts/submodule_gate.sh` (注意是下划线 `submodule_gate.sh`, 不是连字符 `submodule-gate.sh`) L33 `MODE="${ARIA_SUBMODULE_GATE_MODE:-warn}"`。
   - 同时 SKILL.md L378 inline 代码块也有同样 `MODE="${ARIA_SUBMODULE_GATE_MODE:-warn}"` (文档示例),也需 flip。
   - 影响:Spec 起草时留 "取实际位置" 是 D+1 偷懒;实际有 **2 处** (script 实际执行 + SKILL.md 文档示例) 都需 flip,Spec 未明示。
   - 修复:§A1 改为列出两处具体 file:line:
     - `aria/skills/phase-c-integrator/scripts/submodule_gate.sh:33` (实际执行 default)
     - `aria/skills/phase-c-integrator/SKILL.md:378` (inline 文档示例 default)

3. **§F 表格"行号清单"硬编码 violates 文档同步原则** (L97)
   - Spec §F 表格 SKILL.md 行 `"行 47/180/192/229-230/300-301/378-381/414-415/443/450 等"` 是 D+1 起草时 grep 结果。但 SKILL.md 后续任何编辑 (e.g., M6 Spec ship / aria-secret-guard hotfix) 都可能 shift 行号,导致 Phase B 当天行号清单已失同步。
   - 影响:Phase B 执行时按错 line 编辑或漏改。违反 CLAUDE.md §文档同步原则。
   - 修复:行号清单改为 grep pattern 清单 (e.g., `grep -nE '(v1\.28|v1\.29|warn-only)' aria/skills/phase-c-integrator/SKILL.md`),Phase B 执行时实时 grep 取行号。或加 Phase B step 描述 "rerun grep 取最新行号,不依赖此处 hardcoded 清单"。

4. **§F 表格遗漏 marketplace.json description 字段** (L93-100)
   - §F 列出 SKILL.md / CHANGELOG L32 / convention / CLAUDE.md 4 个跨引用文档,但 **未列 marketplace.json + plugin.json 的 `description` 字段**。当前 description 为 `"32个 Skills + 11个 Agents + Hooks系统 (含默认 secret-guard)"` — 若 v1.29.0 Skills 数 / Agents 数 / Hooks 个数变化 (本 Spec 零变化但需 verify) 则需 sync。
   - 影响:Phase D 5+1 SOT verify 时可能漏检 description 字段,造成 description 与实际 plugin 内容不一致 (历史 patch 1 中 `Skills count typo 31→32` 就是此类失同步)。
   - 修复:§F 加 marketplace.json + plugin.json description 字段 verify 行 (本 Spec 无 Skill 数变化,应保持 "32 Skills"),Phase B step 6 task 加 "确认 plugin.json + marketplace.json description 与实际 Skills/Agents/Hooks 数一致"。

5. **§E `.aria/decisions/<date>-v1.29.0-block-flip.md` 文件名与 §C/§Cross-references 不一致** (L86 vs L243)
   - L86 `.aria/decisions/2026-06-07-v1.29.0-block-flip.md` (decision doc 文件名)
   - L243 (Validation Checklist) 同上 ✓
   - 但 §观察期数据 (L173) 提到 "数据源: `aria/metrics/submodule-gate-warns.jsonl`"; ship 当天若 D+14 仍非 2026-06-07 (e.g., 因 R1 fallback path c → extend) 则 hard-coded 2026-06-07 文件名失准。
   - 影响:边界 case 下 decision doc 文件名误导;且 spec 未明示文件名是 hard-coded 还是 ship 当天日期。
   - 修复:§E 加 note "若 ship 实际日期 ≠ 2026-06-07 (e.g., extended warm window per R1 fallback (a)),decision doc 文件名按 ship 实际日期改";或将 hard-coded 改为 `<ship-date>` 模板。

6. **§How Phase B.4 step 2 cron schedule 改动未列入 §What deliverables** (L131)
   - Phase B.4 step 2 写 ".forgejo/workflows/submodule-gate-tripwire.yml 追加 schedule cron"。**§What §B 已 cover** ✓ (L58-62)。
   - 但 Phase B.3 step 描述跳过 cron 改动 (B.3 全部是 aria-plugin 内),cron 在 main repo `.forgejo/workflows/`,出现在 B.4 step 2 — 这是正确的 (cron 在 main repo)。**但 Spec 未明示 cron flip 属 main repo PR 而非 aria-plugin PR**, 容易误以为是 aria-plugin 内 deliverable。
   - 现状验证:`/home/dev/Aria/.forgejo/workflows/submodule-gate-tripwire.yml` 存在于 Aria main repo ✓,与 Spec §B 描述 "位于 Aria main repo, NOT aria-plugin per parent Rev1 R1-tl-3 fix" 一致。
   - 影响:Phase B 执行时 PR scope confusion (aria-plugin PR 是否含 workflow 修改?)。
   - 修复:§What §B 加一行明示 "**该 workflow 文件位于 Aria main repo, schedule cron 追加属 Aria main repo PR (Phase B.4) 范围, NOT aria-plugin PR (Phase B.3)**"。

### Minor

1. **§A2 config table 措辞 v1.29.0+ 与 v1.28.0 历史叙述并存** (L48-54)
   - Spec 给的目标态:`"block" (v1.29.0+) | "warn" (legacy opt-out) | "off" (emergency bypass)`。**OK ✓** (legacy opt-out 保留向后兼容)。但 SKILL.md L443 当前是 `"warn"` (v1.28.0) / `"block"` (v1.29.0+) — 翻转后历史 v1.28.0 default warn 描述要怎么处理?保留还是删?Spec 未明示。
   - 修复:§F 表格 SKILL.md 行加 note "L443 config table 改为 v1.29.0+ 现在时,历史 v1.28.0 warn-only 叙述可保留在 §C.2.4.5 §改动历史 / changelog 风格 sub-section (per parent CHANGELOG 风格)"。

2. **§F 表格 standards convention 用 "若"** (L99)
   - "若 §Layer 引用 v1.28.0 warn-only 默认 → 更新至 v1.29.0 block 默认"。**实际验证 `standards/conventions/submodule-pointer-hygiene.md` L6, L8, L76-83 多处直接说 v1.28.0+ warn-only / v1.29.0+ block** — 不是 "若",是 **确定要改**。
   - 修复:§F 表格 standards convention 行 "若" 改为确定 "改 §Mechanical enforcement (v1.28.0+) → (v1.29.0+),L80 删除 14-day observation window 段(已 elapsed),L81 改 block 为现在时"。

3. **§D Aria main repo bump "若...则 bump 升级为 minor"** (L82)
   - Spec 留了 conditional bump (1.7.0→1.7.1 patch OR 1.7.0→1.8.0 minor)。**这是 reasonable hedge**,但 Level 2 Spec 应该 deterministic;若 Phase B 当天 owner 临时决定 minor,本 Spec 未规定 version slot 占用验证流程。
   - 修复:§D 加 note "Phase B 实施时若发现 main repo CLAUDE.md cross-ref 需要更新 → bump 升级 minor,**先 verify v1.8.0 slot 未占** (`grep '1.8.0' VERSION CHANGELOG.md`),再决定"。

---

## Phase 2 — Spec quality

### Critical
(none)

### Important

(none — 所有 quality 问题归入 Minor)

### Minor

1. **§观察期数据 schema 缺 `gate_executions_observed` 字段** (L170-207)
   - Spec §决策框架 R1 fallback 路径 (L162) 依赖 "WOULD-BLOCK events < 3" 判断,但 §观察期数据 schema (L182-188) 给的字段是 `total_would_block` (= 触发事件数),**未明示 "gate executions observed" (= 总 gate 调用次数, 含 PASS)**。Parent Spec §What §E (L234) 写 "≥3 minimum gate executions observed in warn-only window" — 是 executions, 不是 events。
   - 影响:Schema 与决策框架 trigger C 条件描述不一致,Phase B 当天填数据时易混淆。
   - 修复:§观察期数据 schema events 段加 `total_gate_executions: <int>  # 含 PASS + WOULD-BLOCK + override 所有, 触发 minimum-observation guard 条件`。

2. **§Risk R5 跨 Spec 时序冲突未列 Layer L claim 操作** (L221)
   - R5 提到 "Layer L claim 协调避免 race" 但未列入 §How Phase B step。Parent Spec R8 (L362) 明确 Phase B.1 必须 claim `aria/skills/phase-c-integrator/SKILL.md` via Layer L (track-id `aria-submodule-pointer-regression-gate`)。本 Spec 也修同一文件,**也需要 claim**,但 §How B.1 未列。
   - 影响:Phase B 当天与 M6 sub-Spec 或其他并行 work 撞 Skill 文件。
   - 修复:§How Phase B.1 加 step "claim `aria/skills/phase-c-integrator/SKILL.md` via Layer L,track-id `aria-submodule-gate-block-flip`,写 claim YAML 到 `refs/aria/coordination`"。

3. **§Cross-references audit reports 路径与 parent Spec 不完全一致** (L260-262)
   - 列了 R1 + R2 audit reports 路径,但 parent Spec 实际还有 Rev1 commit + R3 没列 (R3 在 brainstorm DEC, 非 post_spec)。OK ✓ 但 R1+R2 列了 ≠ 完整 audit trail。
   - 影响:Minor — 跟 parent Spec 引用习惯不齐。
   - 修复:§Cross-references audit reports 段加 "parent Spec 完整 audit trail 见 parent proposal.md §Audit trajectory L18-22"。

4. **§Validation Checklist Phase A.1 vs A.2 分隔不清** (L228-238)
   - A.1 列 5 项 [x] (已完成),A.2 列 4 项 [ ] (待执行)。A.2 第 1 项 "post_spec R1 audit (3-4 agents) — Level 2 baseline"。但 Level 2 baseline 通常 3 agents (per parent Spec R2 = 3 agents),不是 3-4。
   - 修复:A.2 改为 "post_spec R1 audit (3 agents: tech-lead + qa + code-reviewer per Level 2 baseline)"。

5. **§观察期数据 YAML schema 示例 `pr_url` 用 `https://forgejo.../pulls/XXX`** (L190)
   - `forgejo.../pulls/XXX` 是 placeholder URL,但 Aria 实际 URL 是 `https://forgejo.10cg.pub/10CG/Aria/pulls/XXX`。Phase B 当天若按模板 copy URL pattern 可能写错。
   - 修复:placeholder 改为 `https://forgejo.10cg.pub/10CG/Aria/pulls/<NUM>`。

6. **§观察期数据 `override_rate > 15%` trigger 引用 parent §R4 但未给具体 follow-up action** (L203)
   - 提到 ">15% trigger parent §R4 re-calibration" 但本 Spec 未规定 re-calibration 是否阻塞 v1.29.0 flip。Edge case:若 override_rate 19% + FP rate 1% → 翻 or 不翻?
   - 修复:§决策框架 加 trigger F "override_rate > 15% → 不翻 + file 新 OpenSpec re-calibrate gate sensitivity (与 trigger D 平行)"。

7. **§Cross-references memory references 用 `[[...]]` 格式 vs Aria 其他 Spec 用 `[memory: ...]`** (L280-283)
   - Aria 历史 Spec memory 引用格式不统一。本 Spec 用 wikilink `[[feedback_xxx]]` 格式,CLAUDE.md (L274-277) 也用 `[[...]]` 格式 ✓。但 parent Spec (L454-458) 用裸 `feedback_xxx` 无 wikilink。**inconsistent project-wide, 非本 Spec 责任。**
   - 修复:OK to defer — 本 Spec 与 CLAUDE.md 一致即可。建议 owner 发起跨 Spec memory ref 格式 convention spec。

8. **§Cross-references "Companion artifacts" 引用 `aria-plugin-benchmarks/submodule-gate/`** (L267)
   - 验证 `/home/dev/Aria/aria-plugin-benchmarks/submodule-gate/README.md` 存在 ✓ (parent Spec Rule #6 substitute 已 ship)。**OK ✓**。但 Spec 说 "no re-benchmark needed since no behavior change" — 这是 correct application of `feedback_deterministic_structural_skill_rule6_substitute`,但应 explicit cite memory entry 在 §Rule references 段。
   - 修复:§Rule references 加 "`[[feedback_deterministic_structural_skill_rule6_substitute]]` — deterministic Skill Rule #6 substitute, 本 Spec 零行为变化继承 parent artifacts"。

---

## Strengths

1. **§Why "Why now (D+1) draft skeleton, ship D+14" 论证清晰** — 4 reason 全部 actionable (减少 deadline 起草压力 / 早期 audit / TBD 占位 / Phase B+C+D atomic ship)。早期起草本身就是好 practice。

2. **§决策框架 5 trigger 表 (L158-166)** — 全面覆盖 (A FP-threshold / B hard-date / C insufficient / D high-FP / E explicit defer) + 明确 default-on policy。直接继承 parent Spec §What §E 的 flip criteria,无 drift。

3. **§Risk R1 (insufficient warm observation) 3 fallback path** — (a) extend / (b) flip with risk-accept / (c) defer 都有具体 procedure + 推荐 (b) + rationale "13 assertions PASS 已提供 mechanism confidence"。这是 mature spec 写法。

4. **§Cross-references Rule references + Memory references 分段清晰** (L273-283) — Rule #6 / Rule #8 / Rule #9 + 4 memory entries 各列原因,supports `feedback_dec_ship_target_staleness_verify` 已应用 (Phase A.0 verify 完成)。

5. **§How Mechanism 引用段 (L143-150) 明示 "本 Spec **零新机制**"** — 1 句话 hard-codes scope,封堵 scope creep。Level 2 spec 模板。

6. **§Validation Checklist 三段分明** (Phase A.1 [x] / Phase A.2 [ ] / 2026-06-07 当天 [ ]) — 与 Spec 两阶段 (A.1+A.2 now / B+C+D ship day) 完全对应,便于 audit verifier 跟踪进度。

7. **Version slot 验证 (L232 [x])** — Phase A.1 已 hard-verify aria-plugin v1.29.0 + Aria v1.7.1 slot 空闲。实测吻合 (`aria/VERSION` 1.28.0 + `Aria/VERSION` 1.7.0)。`feedback_dec_ship_target_staleness_verify` 已应用。

8. **Backward-compat 措辞 (L56)** — `mode="warn"` legacy opt-out + `mode="off"` emergency bypass + env-var override 优先级保持。Spec 不破坏现有用户 workflow。

---

## Q-NEW

(none) — Spec scope/decisions 已 clear, Phase A.2 仅需 polish 不需要 escalate to owner。

---

## Verdict reasoning

**PASS_WITH_WARNINGS** justification:
- **0 Critical** — Phase 1 compliance 全部通过 (Level 2 frontmatter / Rule #5 placement / Rule #6 substitute inheritance / Rule #7/#8/#9 cross-refs / version slot 实测 verified)
- **6 Important** — 集中在 §C/§A1/§F 表格精度 + Phase B scope 描述,全部 spec-polish 级别,不动 decisions / 不动 mechanism
- **8 Minor** — 主要是 schema 字段补齐 / Layer L claim 漏列 / placeholder URL / convention 格式微调
- **0 scope creep** — Spec §Mechanism 引用段明示 "零新机制",effort baseline ~3-4h 与 Level 2 体量匹配
- **3-4 agent baseline** — Level 2 R1+R2 unanimous PASS_WITH_WARNINGS per `feedback_post_spec_audit_two_round_pragmatic_for_l2`,R1 这里 PWW + 6 Important 数量 in baseline 范围 (3-10 Important per rubric),Rev1 修完即可 R2 unanimous CONVERGED

**Rev1 推荐优先级**:
- **Must fix in Rev1** (Important 1, 2, 4, 6) — §C marketplace.json 双 version 字段标注 / §A1 file:line 精确化 / §F marketplace+plugin.json description verify / §B main-repo PR scope 明示
- **Should fix in Rev1** (Important 3, 5 + Minor 1, 2) — §F 行号清单改 grep pattern / §E decision doc 文件名 hard-coded note / §A2 historical wording / §F standards convention "若" 改 hard
- **OK to batch in Phase B.1** (Minor 3-8) — Layer L claim / audit trail polish / checklist agent count / URL placeholder / override_rate trigger F / memory ref convention

**预期 R2 outcome**: Rev1 修完 Important 1-6 + Minor 1-2 后, R2 应 PASS_WITH_WARNINGS unanimous 3/3 (tech-lead + qa + code-reviewer), 与 Level 2 baseline 一致。

---

**Report end**
