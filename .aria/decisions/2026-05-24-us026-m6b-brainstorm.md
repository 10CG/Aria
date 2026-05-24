# Brainstorm: US-026 M6b kickoff (DEC-20260524-001)

> **Date**: 2026-05-24
> **Mode**: requirements + technical (per `aria:brainstorm` SKILL.md, owner-iterative convergence loop)
> **Scope**: M6/US-026 kickoff — 4 sub-Specs composition + scope + acceptance + sequencing + owner gates
> **Status**: **CONVERGED 2026-05-24** (R3 Discussion 4/4 ACCEPT + R3 Challenge 0 substantive blocking objections after Q-NEW-1 owner answer)
> **Author**: solo-lab (uni.concept.wzfq@gmail.com), drafted by Claude Opus 4.7 (1M context), owner-arbitrated 11 Qs total
> **Loop**: Q1-Q8 initial (single-question owner Q&A) → R1 Discussion (4-agent parallel) → R1 Challenge (3-agent) → R2 Discussion → R2 Challenge → R3 Discussion (orchestrator-forcing-function unified anchor) → R3 Challenge → 3 final owner Qs (Q-final-1 + Q-final-2 + Q-NEW-1) → CLOSED
> **Successor artifacts**: 4 sub-Specs Phase A.1 kickoff (aria-2.0-m6-* naming) — parallel spec-drafter dispatch

---

## §1 Owner decisions (locked Q1-Q11)

### Initial Q&A (single-question owner-interactive, ~30min)

| Q | Decision | Implication |
|---|----------|-------------|
| Q1 | Multi-Spec sub-tracks (not single Spec) | M6 拆 4 sub-Specs (post-R3 refinement, R1 推 5) |
| Q2 | Synthetic OK (混合 real + test issue 在 7d ≥10 dispatch) | dispatch supply 不依赖 organic Lab issue 节奏 |
| Q3 | Lightweight cost infra (SQL aggregator + cron) | M2 T9 token_usage schema 复用,无新 dashboard |
| Q4 | Standard docs scope (~25-35h pre-R3, post-R3 实 ~33h) | CLAUDE.md + 主 README + system-architecture v2.0 + standards/autonomous + AI-DDD 方法论 |
| Q5 | Standard release (~8-12h, Aria 主仓 v2.0.0 tag, aria-plugin **不**同 bump) | semantic boundary 明确 (aria-plugin = tools, Aria 2.0 = autonomous infra) |
| Q6 | Defer all carry-forward (M5-OS-PB-1 + 本 Track E 3 follow-up issues) | M6 scope discipline, 独立 hygiene cycles |
| Q7 | Crash recovery: Process + Node + Network (3 infra modes 显式 lock) | R3 内部 brainstorm 扩 6 modes (+3 LLM mocked: 429/invalid JSON/provider 5xx mid-transition) |
| Q8 | COST first → E2E + DOCS 并行 → RELEASE 最后 | 4-5 weeks single owner timeline |

### Final iterative-loop Qs (post-R3 convergence, ~5min)

| Q | Decision | Implication |
|---|----------|-------------|
| **Q-final-1** | **Menu C — Accept 4-5w slip + formal PRD §M6 timeline patch** | owner PR 改 PRD §M6 baseline 3w → 5w;全 4 sub-Specs ship, scope 完整;risk: secret rotation 8-2 buffer 压缩 ~36 days at 5w (RED threshold) |
| **Q-final-2** | **Path (a) — PRD §628-629 patch metered+subscription dual-track** | owner PR 改 PRD §628-629 文本: (i) Luxeno 月度账单 ≤ $X subscription + (ii) Zhipu/Z.AI metered 月度账单 ≤ $Y + (iii) dispatch volume ≥ 10/day under flat-rate;Spec #1 cost.json schema split 与之 align |
| **Q-NEW-1** | **Hybrid mock layer** — 4 modes SDK boundary + 2 modes (partial-stream/5xx) HTTP layer | TG-B per-mode rationale matrix +1h scope (~28h → ~29h);防 mock-shape-mismatch per `[[feedback_test_mock_pattern_hides_prod_bug]]` |

---

## §2 M6 sub-Spec composition (locked)

```yaml
M6 = 4 sub-Specs (aria-2.0-m6-* naming convention, Level 2/3 mix)

# Spec #1
aria-2.0-m6-cost-acceptance:
  estimated: ~10h
  level: 2-3 borderline
  scope:
    - 双行 cost.json schema:
        metered_usd: {provider: zhipu, model, input_tokens, output_tokens, cost_usd, note: "Additive per-dispatch."}
        subscription_usd: {provider: luxeno, model, cost_usd: null, attribution_disclaimer: "subscription billing, no per-dispatch attribution"}
    - owner-set thresholds in .aria/config.json m6.cost_thresholds.{zhipu_30d_usd, luxeno_monthly_usd}
    - freshness_ts 字段 (acceptance reject if now-freshness>24h)
    - cron sentinel + alarm path (Feishu webhook 80% threshold warn, reuse ARIA_FEISHU_WEBHOOK_URL)
    - acceptance SQL script (binary-falsifiable)
    - Luxeno=0 静默假阳性 prevention (R2 ai-CH-3 closure)
  acceptance:
    - cost.json fresh (24h gate) + 双行 schema 正确
    - threshold doc + SQL script binary-falsifiable
    - 3-day trending data 在 Spec #2 启动前 ready (cr-CH-9 closure)
  agent: backend-architect

# Spec #2
aria-2.0-m6-e2e-resilience:
  estimated: ~29h (28 + Q-NEW-1 hybrid +1)
  level: 3
  scope (internal TG split):
    TG-A runtime-observability (~10h):
      - 7d = 168h Nomad alloc uptime API query (per qa M-qa-R3 acceptance)
      - dispatch tracker SQL `GROUP BY rework_mode HAVING SUM>=10`
      - synthetic ≤70% + stratification (≥1 bug + ≥1 feature + ≥1 stale real)
      - daily snapshot `.aria/probes/m6-7d-day-{1..7}.md`
      - Day-3 mid-run health gate (≥1 完整 S0→S9 cycle, ≤50% S_FAIL, no stuck >4h)
      - Pre-flight ~3 dry-run dispatches (per ai R2CH-4, real LLM throwaway with $2 hard cap per dispatch, fixture source TBD per Phase A precision)
      - validate-m6-handoff.py + paired test triple (M5-handoff.yaml abi_compat_promises cross-check) per backend M-ba-R3-1c
      - is_synthetic tagging (schema column OR `[DEMO-M6-*]` title convention, per qa M-qa-R3-10)
      - cross-project Kairos/silknode dispatch evidence (conditional, per ai R2CH-3 + qa M-qa-R3-10)
    TG-B crash-recovery (~13h, +1 Q-NEW-1):
      - 6 modes mock-only (Q-NEW-1 Hybrid layer):
          Infra-1 (SDK): Hermes SIGKILL mid-transition (test_t12 existing)
          Infra-2 (SDK): Layer 2 alloc SIGKILL (light-1 不能 drain reframe)
          Infra-3 (SDK): SQLite WAL truncation 0-byte + integrity_check rejection
              (M-qa-R3-8 NEW: PRD §634 cov gap, commit shell script in acceptance/)
          LLM-4 (SDK): 429 rate-limit mid-transition mock
          LLM-5 (HTTP): invalid JSON malformed response (httpx_mock)
          LLM-6 (HTTP): provider 5xx mid-transition (httpx_mock)
      - Defer to v2.1: context-window overflow + safety/content refusal
      - State machine 100% cov: deterministic transitions only (S0/S1/S4/S5/S7/S8/S9 + S_FAIL from each);
          stochastic (S2/S3/S6) separate sub-task with mocked replay (zero live cost)
      - AdvancingClock DI (per `[[feedback_phase_b_velocity_patterns_2026-04-29]]`) 防 wall-clock flakiness
      - Mock-layer-per-mode matrix (Q-NEW-1 hybrid rationale doc)
    TG-C 拟人命令 samples (~6h):
      - 10 real samples collected from E2E run
      - PRD §639 rubric ≥7/10 median scoring
      - Corpus 文件 commit `aria-orch/evals/m6-prompt-quality/{rubric.md, corpus/sample-{01..10}.md, score-{01..10}-owner.md}`
      - Cross-ref Spec #3 TG-DOCS-B humanized-command-patterns.md (BOTH locations design)
  acceptance:
    - 7d 168h uptime PASS + ≥10 dispatch path-stratified + Day-3 gate PASS
    - 6 crash modes 全 test PASS (mock-only, zero live cost)
    - State machine deterministic transitions 100% cov verified by pytest --cov gate
    - 10 samples median score ≥7/10
  agent: backend-architect + qa-engineer (TG-A obs / TG-B crash) / knowledge-manager (TG-C samples)

# Spec #3
aria-2.0-m6-docs:
  estimated: ~33h
  level: 3
  scope (single Spec internal A+B TG split):
    TG-DOCS-A (release-blocker, ~11h):
      - CLAUDE.md v1.0.4 → v2.0 (草案 ready @ aria-orchestrator/docs/claude-md-revision-draft.md + Diff 9 增量: Rule #7/#8/#9 + 插件版本 catch-up v1.26.0)
      - 主 Aria README badge + 定位描述 + Aria 2.0 cross-link
      - Release notes v2.0.0 含 "Plugin Compatibility — aria-plugin 不随 Aria 2.0 同 bump" 段 (R1 cr-CH-8 closure)
      - aria/README.md cross-link 补充
      - Migration notes ("non-migration" 内部说明; cr-CH-8 closure)
      - Forgejo Discussion FAQ
    TG-DOCS-B (architecture, ~22h, can ship v2.0.1 if calendar slips per Menu C):
      - docs/architecture/system-architecture.md v2.0 (~8-12h, 三层架构 + Layer 1/2 + autonomy model)
      - docs/architecture/version-scheme.md 新建 (Aria 主仓 / aria-plugin / aria-orchestrator / Aria 2.0 PRD 四套版本号 disambiguation)
      - standards/autonomous/decision-autonomy-matrix.md (Lab-shareable, per PRD §553)
      - standards/autonomous/humanized-command-patterns.md (Lab-shareable, ≥10 curated samples + PRD §639 rubric;BOTH locations 与 Spec #2 TG-C 双向引用)
      - aria-orchestrator/docs/layer-boundary-contract.md (Aria-specific, **不**入 standards/ per km M-km-R2-005)
      - aria-orchestrator/README v2.0 update
      - .aria/state-checks.yaml 3 drift 探针 (version badge match / claude.md version match / arch doc stale warning ≥90d)
      - aria-orchestrator/docs/architecture-decisions.md §AD-M5-11 RESERVED slot 用于 M6 docs decisions

> **AD-M6-* allocation reservation (post-R1, lock 2026-05-24, per Spec #1 R1 audit aggregate Q4):**
> - **AD-M6-1 / AD-M6-2 / AD-M6-3**: reserved for **Spec #1 `aria-2.0-m6-cost-acceptance`** (snapshot script lang choice / cost-snapshots archive retention / [removed: was acceptance script exit code, lifted to Spec body per Q1])
> - **AD-M6-4+**: Specs #2 / #3 / #4 drafter must start from AD-M6-4
> - **AD-M5-11**: pre-existing M5 reserved slot for M6 docs (Spec #3 may use)
> - Rationale: Spec #1 ships first (cost-acceptance gates Spec #2 trending data), claims earliest AD slots. Cross-Spec coordination enforced by this memo + state-scanner audit-engine R1+R2 cross-ref check.
  acceptance:
    - TG-DOCS-A release-blocker: 4 files exist + state-checks 3 探针 ship + CLAUDE.md v2.0 grep verify
    - TG-DOCS-B architecture: 4 standards/autonomous files + system-architecture v2.0 + version-scheme + state-checks 探针 + drift 探针 yaml grep verify
  agent: knowledge-manager

# Spec #4
aria-2.0-m6-release-closeout:
  estimated: ~10h
  level: 2
  scope:
    - Aria 主仓 v1.7.0 → v2.0.0 git tag + 5+1 SOT bump (VERSION + CHANGELOG + README badge sync)
    - Pre-release checklist (RED/ABORT gates):
        * Secret rotation 2026-08-02 buffer:
            - <21d (RED): warning to owner, proceed with caution
            - <14d (ABORT): block release until rotation done
        * abi_compat_promises cross-check (per m5-handoff.yaml line 155 mandatory carry-forward)
        * 4-key set NEW exposure trigger check (per project_secret_rotation_deferred_2026-05-02 2026-05-20 update)
        * submodule branch verify (default branch on master not feature, per feedback_submodule_branch_before_archive)
    - Submodule pointer freeze + 3-way SHA parity verify (3 repos × 3 endpoints = 9-way)
    - Forgejo + GitHub release pages with notes
    - Feishu announcement
    - aria-plugin 不同步 bump (semantic boundary, comms section in Spec #3 TG-DOCS-A)
  acceptance:
    - git tag v2.0.0 exists + reachable from forgejo + github
    - 5+1 SOT files synced
    - Forgejo release page exists + GitHub release page exists
    - Feishu announcement posted (URL evidence)
    - Pre-release gate logs RED/ABORT decisions if any
  agent: tech-lead

# Total
Total estimated: ~82h (10 + 29 + 33 + 10)
Wall-clock: 4-5 weeks single owner (Spec #1 first, Spec #2 + Spec #3 parallel, Spec #4 last)
```

---

## §3 DROPPED proposals (explicit non-decisions to prevent re-litigation)

| Item | Source | Drop reason |
|------|--------|-------------|
| 5 sub-Specs (R1 tech-lead) | tech-lead R1 over-decomposition | Proportionality violation per tl2-CH-001 (M6 ~80h is Level 2-cluster, 5× spec-drafter+audit overhead 浪费);R3 锁 4 sub-Specs + internal TG split |
| INFRA sub-Spec (km R2) | km m6-infra Nomad docker auth fix | Track E (`aria-layer2-docker-auth-cold-pull-fix`) 2026-05-23 已完整修 F2 (HCL auth removed) + F3 (节点级 plugin auth.config wired) + cred sync;ghost work, drop confirmed by km R3 self-correction |
| M5-OS-PB-1 拉回 (backend-architect R1 D-03) | comment_poll_runner lazy-wire forgejo UX fix | owner Q6 决策 "defer all carry-forward";D-03 直接违 Q6;DROPPED 4/4 confirm in R3 |
| m6-core Spec (km R2) | km m6-core Layer 2 wiring | Content = M5-OS-PB-1 (与 Q6 矛盾);km R3 self-correction confirmed drop |
| PRD §628-629 release notes vacuous reframe (R2 default Path b) | tech-lead R2 default option | Path b 是 PRD compliance 实质降级 (per ai R2CH-2);R3 改 Path a PRD patch (Q-final-2 owner answer) |
| Stochastic LLM 测试 live cost (R2 qa) | qa R2 stochastic split sample N | mocked replay zero live cost 替代 (R3 qa-R3 revision per ai R2CH-1) |
| DOCS 独立 A + B Spec (km R2) | km double Spec proposal | R3 single Spec + internal A+B TG split (per km R3 self-correction) |

---

## §4 Phase A precision items (non-blocking, threaded into spec-drafter)

R3 Challenge 共 surfaced 8 Phase A precision items, by sub-Spec:

### Spec #1 cost-acceptance
- P-1: cost.json schema field semantics (subscription.tokens_used informational + window dates) per ai R3CH-2
- P-2: cost measurement oracle method explicit in validate-m6-handoff.py (`cost_measurement_method` enum) per qa M-qa-R3-3
- P-3: validate-m6-handoff.py cross-check m5-handoff.yaml line 155 mandatory promise per backend M-ba-R3-1c

### Spec #2 e2e-resilience
- P-4: Mock-layer-per-mode matrix (Q-NEW-1 hybrid 显式 4 SDK + 2 HTTP table)
- P-5: 4 WAL scenarios vs 3 enumeration (PRD §634 a/b sub-clauses 总 4) per backend M-ba-R3-1a
- P-6: TG-A → TG-B handoff checkpoint contract (TG-A content-complete checkpoint before TG-B) per backend M-ba-R3-4a
- P-7: is_synthetic tagging mechanism (schema column OR title prefix convention) per qa M-qa-R3-10
- P-8: Pre-flight dispatch fixture provenance (replay M5 O3 captures vs fresh synthetic vs cross-project) per ai R3CH-3
- P-9: Cross-project Kairos/silknode acceptance conditions per ai R3CH-4

### Spec #3 docs
- P-10: standards submodule operation sequence (feature branch → PR → bump pointer → 主仓 PR) per km M-km-R3-7
- P-11: prompt-templates.md (aria-orch) vs humanized-command-patterns.md (standards) content boundary disambiguation per km M-km-R3-4 + km R3 Q1 condition
- P-12: state-checks.yaml 3 probe scripts detailed logic (not just "add probe") per km M-km-R3-7 + feedback_pre_draft_bug_hunt_discipline
- P-13: CLAUDE.md 8 diffs 逐一列出 in proposal §What per km M-km-R3-7

### Spec #4 release-closeout
- P-14: standards/autonomous/ 目录是否已存在 verify (M0 推迟到 US-026) per km M-km-R3-8

### Cross-Spec
- P-15: Sub-Spec dependency DAG (Phase A.2 task-planner 必须显化) per tl2 R3CH-002

---

## §5 Convergence loop trace

```
R1 Discussion (4 agents parallel)
  - tech-lead: 推 5 sub-Specs + 5 refinements (R-tl-1..5)
  - backend-architect: 4 sub-Specs + 6 refinements (M-ba-D-01..06)
  - qa-engineer: 10 falsifiability findings (M-qa-2..11)
  - knowledge-manager: 8 docs scope refinements (M-km-D1..8)
R1 Challenge (3 agents parallel)
  - code-reviewer: 9 objections (4 CRITICAL/cross-cutting consensus with tl2)
  - ai-engineer: 8 objections + PRD §78/§639/§644 拟人命令 PRD compliance defect surfaced
  - tech-lead-critic (tl2): 7 objections (4 CRITICAL: 5 sub-Specs / 5w vs 3w / D-03 vs Q6 / NOT YET UNIFIED)
R1 → R2 cross-cutting consensus on revision (3 CRITICAL):
  - D-03 M5-OS-PB-1 拉回 violation of Q6
  - PRD §628-629 cost model vs Luxeno subscription mismatch
  - 5 sub-Specs over-engineering (4 better)
R2 Discussion (4 agents address R1 Challenge)
  - tech-lead R2: SIGNIFICANT_REVISION, 16/19 R1 findings addressed, 4 Q escalations
  - backend-architect R2: 7 R2 positions
  - qa-engineer R2: 8 R2 positions
  - knowledge-manager R2: 7 R2 positions + 2 new memory entries proposed
R2 Challenge (3 agents parallel)
  - code-reviewer: 6 new objections (4 sub-Specs paper-unified vs 4 different boundaries)
  - ai-engineer: 5 new objections (stochastic cost budget / Q10 default wrong / synthetic ≤70% 可行性 / pre-flight bracket / INFRA LLM-routing)
  - tech-lead-critic: 7 new objections (4 escalations 越界 / velocity math 不闭合 / R2 paper-fix antipattern 复现)
R2 → R3 cross-cutting consensus on FURTHER revision (3 CRITICAL):
  - 4 sub-Specs paper-unified 但 4 boundary proposals not converged
  - 4 owner escalations 越界 brainstorm 责任
  - velocity 数学 87h vs 79h drift 不闭合
R3 Discussion (4 agents validate orchestrator-forced unified anchor)
  - tech-lead R3: ACCEPT_WITH_MINOR_REFINEMENTS, CONVERGED, 12/14 R2 Challenge addressed
  - backend-architect R3: PASS_WITH_CLARIFICATIONS (3 Phase A precision)
  - qa-engineer R3: structurally sound + 3 binary falsifiability gaps
  - knowledge-manager R3: ACCEPT + 4 知识架构约束 Phase A 必写 + km self-correction (m6-core/m6-infra DROP)
R3 Challenge (3 agents verify)
  - code-reviewer: ACCEPT_R3, CONVERGED, 0 substantive new objections
  - ai-engineer: READY conditional on Q-NEW-1, 1 minor substantive (mock layer choice) + 3 precision
  - tech-lead-critic: CONVERGED_WITH_MINOR_NOTES, 0 substantive new, 3 advisory INFO

Final owner Qs (3 total):
  - Q-final-1 (timeline 3w vs 5w + 3 cut menus) → Menu C
  - Q-final-2 (PRD §628-629 patch) → Path (a)
  - Q-NEW-1 (mock layer) → Hybrid

CONVERGED 2026-05-24
```

---

## §6 Spec drafter handoff (Phase A.1 kickoff readiness)

**Parallel dispatch ready**:

- Spec #1 cost-acceptance — backend-architect (10h baseline)
- Spec #2 e2e-resilience — backend-architect (TG-A obs) + qa-engineer (TG-B crash) + knowledge-manager (TG-C 拟人 samples). Joint draft. (29h baseline)
- Spec #3 docs — knowledge-manager (33h baseline, internal A+B TG split)
- Spec #4 release-closeout — tech-lead (10h baseline)

**Sequencing for Phase A.1**:
1. Spec #1 first (gates Spec #2 cost trending data + cost gate threshold)
2. Spec #2 + Spec #3 parallel (independent)
3. Spec #4 last (depends on #1 + #2 + #3 done)

**Phase A.1 should produce**: 4 proposal.md files + 4 tasks.md files + 4 post_spec R1+R2 audits (single round per Spec or 2-agent vs 4-agent per scope) + 4 Approved status before any Phase B starts.

**PRD patches required (owner-action, parallel to Phase A.1)**:
- PRD §M6 timeline 3w → 5w (Q-final-1 Menu C)
- PRD §628-629 cost gate metered+subscription dual-track (Q-final-2 Path a)

---

## §7 Cross-references

- US-026: `docs/requirements/user-stories/US-026.md`
- PRD §M6: `docs/requirements/prd-aria-v2.md` line 414 + §625-647
- 2026-05-15 M6a brainstorm: `.aria/decisions/2026-05-15-m6-brainstorm.md` D1-D7
- M5 close: `docs/handoff/2026-05-23-m5-phase-c-o3-done-d2-close.md`
- Track E close (本 session 之前): `docs/handoff/2026-05-23-aria-layer2-docker-auth-cold-pull-fix-done.md`
- Secret rotation deferred: `.aria/decisions/2026-05-02-secret-rotation-deferred.md` + `.aria/decisions/2026-05-20-secret-rotation-during-m5-deploy.md`
- m5-handoff abi_compat_promises: `aria-orchestrator/docs/m5-handoff.yaml` line 155
- Memory references: `[[feedback_owner_invoked_convergence_loop]]`, `[[feedback_audit_convergence_pattern]]`, `[[feedback_paper_fix_antipattern]]`, `[[feedback_phase_a_depth_drives_b_velocity]]`, `[[project_glm_routing_luxeno]]`, `[[feedback_test_mock_pattern_hides_prod_bug]]`, `[[feedback_validator_repo_drift_guard_test]]`

---

## §8 Next session entry

```bash
/aria:state-scanner  # surface 本 brainstorm DEC + 推荐 Phase A.1 parallel kickoff
```

Recommended workflow: `/aria:phase-a-planner` per sub-Spec OR direct spec-drafter dispatch × 4 parallel。如 owner 选 parallel,可一 session 内完成 4 个 proposal.md 草案 (各 ~30-60min),然后逐 sub-Spec R1+R2 audit。

---

**Created**: 2026-05-24 (session continuation from 2026-05-23 ~22:00 UTC sister session)
**Convergence**: R3 + final owner Qs (11 owner decisions total)
**Status**: CLOSED — proceed to Phase A.1 × 4 parallel spec-drafter dispatch
