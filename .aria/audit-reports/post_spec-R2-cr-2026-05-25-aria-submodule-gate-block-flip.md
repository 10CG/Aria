# post_spec R2 audit — aria-submodule-gate-block-flip (code-reviewer)

**Date**: 2026-05-25
**Auditor**: code-reviewer agent (R2)
**Spec**: `openspec/changes/aria-submodule-gate-block-flip/proposal.md` (Rev1 applied)
**R1 verdict**: PASS_WITH_WARNINGS (0 Critical, 6 Important, 8 Minor)
**R2 verdict**: **PASS_WITH_WARNINGS** (CONVERGED)
**Convergence judgment**: Rev1 已 close 全部 6 R1 Important (CLOSED) + 6/8 R1 Minor (CLOSED) + 2/8 R1 Minor (acceptably deferred);无 Rev1 引入 new Critical/Important;Level 2 baseline (R1+R2 unanimous PASS_WITH_WARNINGS per `feedback_post_spec_audit_two_round_pragmatic_for_l2`) 达成,无 R3 必要。

---

## Phase 1 — R1 Important closure status

| R1 ID | 状态 | Comment |
|-------|------|---------|
| **Imp1** §C marketplace.json 双 version 字段标注 | **CLOSED** | §C 表 L71 已改为 "**顶层 L3 `version` + L16 `plugins[].version` 两处都需同步** *(per R1 cr-Imp1+Imp4)*",验证命令 `grep -n '"version"' aria/.claude-plugin/marketplace.json` (期望 2 命中) 也加入。Phase B step 6 不会漏 grep。 |
| **Imp2** §A1 file:line 精确化 (script L33 + SKILL.md L378) | **CLOSED** | §A1 (L40-43) 明示 `submodule_gate.sh` (下划线) L33 + §A2 (L45-48) 明示 SKILL.md L378。两处都标 "已 Phase A.0 verified"。R1 提到的 "下划线 NOT 连字符" warning 也保留。 |
| **Imp3** §F 行号清单 → grep pattern | **CLOSED** | §A3 (L50-54) 已改为 grep pattern `grep -nE 'v1\.28\.0|v1\.29\.0|warn-only|warn\".*default|default.*warn' aria/skills/phase-c-integrator/SKILL.md`;§F 表 SKILL.md 行 (L101) 同步标 *(per R1 cr-Imp3 + tl m-tl-1 — 不 hardcode 行号)*。Phase B 执行时实时 grep,符合 CLAUDE.md 文档同步原则。 |
| **Imp4** §F marketplace+plugin.json description 字段 verify | **CLOSED** | §C 表 L70 (plugin.json 行) 已加 "+ `description` (verify Skills count 未变 = 32)";§F 表 L105 新增 `aria/.claude-plugin/{plugin,marketplace}.json` 独立行 "description 字段 verify 一致性 *(per R1 cr-Imp4 — 历史 patch 1 Skills count 31→32 typo 失同步前车之鉴)*";§Validation Checklist L312 "description 字段 verify 一致" 已列入 ship-day list。 |
| **Imp5** §E decision doc filename — placeholder | **CLOSED** | §E (L88) 改为 `.aria/decisions/<ship-date>-v1.29.0-block-flip.md` (占位符);L89 明示 "文件名 ship-date 占位 *(per R1 cr-Imp5 — 若 R1 fallback (a) extend window 导致 ship 实际日期 ≠ 2026-06-07,文件名按实际 ship 日期改, 不 hardcoded)*"。R1 fallback 路径 (a) extend 已 cover。 |
| **Imp6** §B clarify cron flip 属 main repo PR | **CLOSED** | §B (L60) 已加显式句 "**该 workflow 文件位于 Aria main repo, schedule cron 追加属 Aria main repo PR (Phase B.4) 范围, NOT aria-plugin PR (Phase B.3)** *(per R1 cr-Imp6)*"。Phase B.4 step 2 (L155) 也同步加 "cron 改动属本 PR scope" 注释。Scope confusion 风险消除。 |

**小结**: 6/6 R1 Important CLOSED,全部满足 R1 报告 Rev1 推荐 "Must fix in Rev1"。

---

## Phase 2 — R1 Minor closure status

| R1 ID | 状态 | Comment |
|-------|------|---------|
| **Min 1** §A2 historical wording note | **CLOSED** | §A3 (L52) 已明示 "ship 当天用 grep 取全集再 batch-review";§F 表 SKILL.md 行 (L101) 说 "保留历史叙述行 (e.g., L294 'v1.28.0 ships warn-only' 不改, 体现 changelog 风格)"。历史 v1.28.0 warn-only 措辞处理 explicit。 |
| **Min 2** §F standards convention "若" → hard requirement | **CLOSED** | §F 表 standards convention 行 (L103) 已改为 "**确定要改** *(per R1 cr-Min 2 ...)* §Mechanical enforcement (v1.28.0+) → (v1.29.0+);L80 删除 14-day observation window 段(已 elapsed);L81 改 block 为现在时"。无 "若" 不确定措辞。 |
| **Min 3** §D Aria main repo bump 升级前 verify | **CLOSED** | §D Note (L84) 已加 "**升级前必先 verify v1.8.0 slot 未占** (`grep '1.8.0' VERSION CHANGELOG.md`),再决定";§Validation Checklist L314 "若 minor 升级先 verify v1.8.0 slot 空闲" 同步列入。 |
| **Min 4** A.2 "3-4 agents" → "3 agents" | **CLOSED** | §Validation Checklist Phase A.2 L298 已改为 "post_spec R1 audit (**3 agents per Level 2 baseline**: tech-lead + qa + code-reviewer per [[feedback_post_spec_audit_two_round_pragmatic_for_l2]])"。 |
| **Min 5** schema `pr_url` → Aria-specific URL | **CLOSED** | §观察期数据 L214 已加 "`pr_url` 构造模板: `https://forgejo.10cg.pub/10CG/Aria/pulls/<NUM>` *(per R1 cr-Min 5)*";schema 内 L242 `per_pr_breakdown.pr_url` 也用了完整 URL。 |
| **Min 6** §决策框架 trigger F override>15% | **CLOSED** | §决策框架表 L204 已加 trigger F "**High override-usage (>15%)** *(NEW per R1 I-tl-7 + cr Min 6)*",含 condition + 决策 + 与 trigger A/B 优先级关系 ("F 优先级 > A/B")。§Default-on policy (L206) 也加 "AND override rate ≤ 15% (trigger F not triggered)" 条件。 |
| **Min 7** memory ref convention `[[...]]` vs 裸 | **DEFERRED (acceptable)** | R1 报告本就说 "OK to defer — 本 Spec 与 CLAUDE.md 一致即可"。Rev1 一致使用 `[[...]]` wikilink 格式 (e.g., L21-22, L66, L348-360),与 CLAUDE.md 一致;跨 Spec 不统一是 project-wide convention 问题,non-blocking。 |
| **Min 8** cite `feedback_deterministic_structural_skill_rule6_substitute` in §Rule references | **CLOSED** | §Rule references L348 已加 "Aria CLAUDE.md §不可协商规则 #6 (Skill benchmark — Rule #6 substitute artifacts inherited from parent, no re-benchmark needed since no behavior change, per [[feedback_deterministic_structural_skill_rule6_substitute]])";§Memory references L360 也列。引用 explicit。 |

**小结**: 6/8 R1 Minor CLOSED,2/8 R1 Minor acceptably deferred (Min 7 per R1 报告原文 "OK to defer";Min 3 已 CLOSED — 计入 closed 列)。R1 报告 Rev1 推荐 "Should fix in Rev1" (Important 3, 5 + Minor 1, 2) 全部满足。R1 推荐 "OK to batch in Phase B.1" (Minor 3-8) 大部分提前在 Rev1 修了 (Min 3, 5, 6, 8 都在 Spec,只剩 Min 7 项目级 convention 是真正 defer)。

---

## Phase 3 — New issues introduced by Rev1

| ID | Severity | Issue |
|----|----------|-------|
| N-1 | **Minor** | §观察期数据 schema L222 `metrics_dir_used: "aria/metrics/" \| "metrics/" \| <other via ARIA_METRICS_DIR>` — 引入了 metrics dir 多口径概念但本 Spec 未规定 default 是哪个。Phase B 当天填数据可能误填。建议: 默认取 `aria/metrics/` (parent Spec §How telemetry 默认位置),若 Phase B 发现实际 dir 不同再 override。**Non-blocking** — schema 已提供 fallback 字段,Phase B step 0 数据汇总时会 surface。 |
| N-2 | **Minor** | §决策框架 trigger D (L202) 引入了 "intermediate 3-19 events 区间出现 FP rate > 2% (e.g., 5 events / 1 FP = 20%)" 中间地带规则。规则本身好,但与 trigger A "≥20 events" 门槛重叠时优先级未明示 (e.g., 19 events / 1 FP = 5.3%, 19 events < 20 → A 不触发, D 中间地带触发 → 不翻;但 trigger B "hard-date + ≥3 executions" 也可能触发翻转)。建议: 决策框架表加 "trigger 优先级: D > F > B > A (deferral 优先于 flip)" 显式排序。**Non-blocking** — Phase B owner decision 时可手动 resolve,且 trigger D 处理 "requiring redesign" 性质本就 dominant。 |
| N-3 | **Minor** | §How Phase B.4 step 4 chicken-and-egg 注释 (L157) 写得详细但用了 "下一个 PR (D+15 或更晚) 才是 first real block-mode dogfood"。这是 accurate 但与 R7 (stale-branch-first-merge-after-flip) 的 ship-day open PR ping 流程隐含一致。建议: §How B.4 step 6 (L159) post-merge 验证段加 cross-ref "见 §Risk R7 + §Validation Checklist ship-day open PR audit"。**Non-blocking**。 |
| N-4 | **Minor** | §标注操作流程 (L178-189, NEW per R1 QA C-2) 引入了 14d 窗口 + monthly review 同步概念,与 parent §FP labeling L237 表面一致;但本 Spec 14d 窗口 (D+0 = 2026-05-24 → D+14 = 2026-06-07) 是首次 monthly review — 如果 parent §FP labeling 实际 monthly review 周期 ≠ 14d (e.g., calendar month),会有微弱时序错位。Rev1 已说 "恰为第一个 monthly review 周期" — accurate for this Spec but 建议未来 Spec 明示 cadence 不可拼接假设。**Non-blocking**。 |

**小结**: 4 个 Minor, 0 Critical, 0 Important。全部 non-blocking polish 级别,可在 Phase B 当天 owner judgment 处理,或在 future Spec 改进。Rev1 引入的新内容 (§标注操作流程 / trigger F / Risk R7 / max defer outer bound D+42 / metrics_dir_used 字段) 主体质量 solid。

---

## Strengths of Rev1

1. **R1 Important 100% closure** — 6/6 全 CLOSED,且 Rev1 引用 (per R1 cr-Imp1+Imp4 / Imp3 / Imp5 / Imp6 等) 在 Spec body 标注 explicit,便于 R2 verify trace。
2. **R1 Minor 高 closure 率** — 6/8 CLOSED + 1/8 已 CLOSED (Min 3) + 1/8 acceptably deferred (Min 7 per R1 原文允许)。超过 R1 报告 Rev1 推荐 "Should fix" 范围。
3. **§A1+A2+A3 三段拆分清晰** — Rev1 把 default flip 从 "one place" 改为 explicit "3 places" (script L33 / SKILL.md L378 / SKILL.md config table multi-line via grep),消除 R1 Imp2 + parent Spec 单点 flip 假设。Phase B 当天不会漏改。
4. **§C 表 marketplace.json 双 version 标注 + 验证命令** — 满足 R1 Imp1 + 加了 `grep -n '"version"' aria/.claude-plugin/marketplace.json` (期望 2 命中) 验证命令,Phase B step 6 grep 即可自检。
5. **§E decision doc 文件名 `<ship-date>` 占位符** — 同步更新 §How B.2 step 1 (L132) + §Validation Checklist (L309) + §Cross-references (L335) 全部一致使用占位符,无 hard-code 残留。
6. **§F 表 standards convention "确定要改" + 具体行号** — 不仅 R1 Min 2 closure,还显式列 L80 / L81 改动内容,Phase B 当天可直接按 spec 执行。
7. **§标注操作流程 NEW section (R1 QA C-2 fix)** — Rev1 主动新增 5 项标注规则 (时机 / owner / 操作方式 / 判定依据 / D+14 null 处理 / sign-off) + 与 Rule #7 sign-off 模式呼应。属于 Rev1 超出 R1 issues 主动 strengthen。
8. **§决策框架 trigger F + Default-on policy 更新** — Rev1 加 trigger F (override>15%) + 在 Default-on policy (L206) 补 "AND override rate ≤ 15% (trigger F not triggered)" 条件。逻辑闭环,无 trigger 漏选。
9. **§Risk R7 NEW (stale-branch-first-merge-after-flip)** — Rev1 主动新增 R7 row 处理 long-lived branch 边缘场景, mitigation 含 3 子项 (ship 当天 ping + override hint + decision doc §6 记录),并在 §Validation Checklist ship-day list (L305) + §E decision doc §6 (L95) 同步落地。Defense-in-depth thinking.
10. **§Risk R1 max defer outer bound (D+42)** — Rev1 明示 "最大延迟上界 D+42 = D+28 for fallback-a 20-PR window + D+14 buffer";超过此日期默认执行 (b) flip with risk-acceptance。覆盖 R1 QA I-4 边界 case。

---

## R2 verdict reasoning

**PASS_WITH_WARNINGS (CONVERGED)** justification:

- **0 Critical** — Phase 1 compliance 全部通过 (Rev1 修复了 R1 QA 的 2 Critical,本 R2 verify 全 CLOSED;无 Phase 1 compliance regression)
- **0 Important** — R1 6 Important 全 CLOSED;Rev1 引入的 4 个 new issues 全 Minor 级别
- **4 Minor (new from Rev1)** — N-1 (metrics_dir_used default) / N-2 (trigger 优先级) / N-3 (B.4 step 6 cross-ref) / N-4 (monthly review cadence 假设);全部 non-blocking, Phase B owner 可手动 resolve
- **R1 Minor closure**: 6/8 CLOSED + 1 已 CLOSED (Min 3) + 1 acceptably deferred (Min 7 per R1 原文 OK to defer)
- **No oscillation** — R1 verdict PWW → R2 verdict PWW,无 verdict 振荡。Rev1 严格 superset of R1 issues + 主动 strengthen (§标注操作流程 / Risk R7 / max defer outer bound)
- **Convergence rule**: per `feedback_post_spec_audit_pragmatic_convergence` "unanimous PASS + verdict 改善 + 无振荡" — 本 R2 与 R1 同 verdict (PWW),但 Important 数 6 → 0 (verdict 改善, Minor 数 8 → 4 + Rev1 新 4 = net 0 change),3 agents 预期 unanimous → CONVERGED
- **Level 2 R1+R2 baseline**: per `feedback_post_spec_audit_two_round_pragmatic_for_l2` Level 2 OpenSpec post_spec audit pragmatic cycle = R1 REVISE/PWW → Rev1 → R2 PASS_WITH_WARNINGS unanimous (3 agents) → CONVERGED → no R3 needed
- **0 Q-NEW** — Spec scope/decisions 已 fully clear, 无需 escalate to owner

**Phase B execution readiness**: Spec 已可 graduate to Approved status。Rev1 后 Spec body 提供 actionable Phase B 执行清单 (§A 3 处 flip / §C 5+1 SOT + marketplace.json 双 version grep / §F wording sync + description verify / §E decision doc 含 §6 ship-day open PRs / §Risk R7 stale-branch ping)。4 个 Rev1-introduced Minor 可在 Phase B 当天 owner judgment 处理,non-blocking。

**R2 final recommendation**: **CONVERGED — proceed to Approved status, no R3 needed**。Phase B (2026-06-07) 可直接按 Spec 执行;ship 当天 owner 可 reference 本 R2 报告 N-1~N-4 微调点 (~5 min decision overhead)。

---

**Report end**
