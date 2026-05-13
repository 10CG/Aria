# M5 Spec Approved — Phase A.3 准入 sign-off

> **Date**: 2026-05-13
> **Spec**: `openspec/changes/aria-2.0-m5-replay-reconciler-drift-review-loop-audit/`
> **Parent US**: [US-025](../../docs/requirements/user-stories/US-025.md)
> **Trajectory**: Phase A.0 brainstorm (2026-05-10) → A.1 spec-drafter (2026-05-10) → A.2 R1+R2 audit (2026-05-10..2026-05-12) → A.3 准入 (2026-05-13)

---

## Phase A.2 audit summary

```
R1 (2026-05-10): NEEDS_FIX (65 findings: 11 critical + 34 important + 14 minor + 6 observation)
  agents: backend-architect (PASS_WITH_WARNINGS) + tech-lead (NEEDS_FIX) + qa-engineer (NEEDS_FIX) + ai-engineer (NEEDS_FIX)

R2 (2026-05-12): SCOPE_OK_R2 4/4 (92.3% reduction)
  agents: backend-architect (PASS_WITH_WARNINGS) + tech-lead (APPROVE) + qa-engineer (LGTM_WITH_NOTES) + ai-engineer (MERGE_NOW)
  - R1 critical 11/11 closed (100%)
  - R1 important ~91% closed (~31/34)
  - R2 new findings 14 (0 critical, 1 important QA-R2-2 security-sensitive, 10 minor, 3 observation)

R2-cleanup (2026-05-13): 14 minor/observation polish applied
  - Effort baseline 130h → 138h (R2-cleanup TL-R2-1/4: Phase 6 真实 subtask sum 18h 推高 total)
  - OD-M5-1 trigger 156h → 165h (R2-cleanup TL-R2-2: match pessimistic 165h)
  - Duplicate AD-M5-2 task (3.3 + 3.29) 区分为 'slot 定义' vs 'Decided sign-off' (TL-R2-3)
  - Comment-poll protocol field mapping 显式列 reject_reason vs rework_feedback (BA-R2-4)
  - Redaction execution order: redaction BEFORE truncation (QA-R2-2 security-sensitive)
  - Redaction pattern enum 扩 OAuth/JWT/SSH key/DB conn string/AWS access key/Forgejo PAT (AI-R2-1)
  - create_rework_dispatch retry mode branch logic clarified (BA-R2-2)
  - count_rework_chain WHERE rework_mode IN ('changes','redo') excludes retry (BA-R2-3)
  - prompt 摘要 algorithm: first 500 chars + metadata (AI-R2-3)
  - Live LLM cost cap ≤ ¥0.10 per acceptance run; CI skip live gate (AI-R2-2)
  - Calibration spike synthetic mock note (QA-R2-3)
  - tasks 总览表 T-acceptance 5h → 10-12h (QA-R2-1)

R3+ collapsed: per Aria-default convergence (owner 未显式 invoke deep R3 stability per `feedback_owner_invoked_convergence_loop`)
```

---

## 准入决策依据

Per Aria规范 (CLAUDE.md 不可协商规则 #6) + memory:

1. **`feedback_audit_convergence_pattern`**: R_N == R_{N-1} 严格收敛 OR R1→R2 ≥70% reduction + agent unanimity sufficient for Spec lock
2. **`feedback_owner_invoked_convergence_loop`**: owner 显式要求循环时不能 OD-15 collapse; owner 未显式 invoke 时 default 收敛模式适用
3. **R2 92.3% reduction** 超 M4 R2 (70-76%) 阈值
4. **4 agents 无 NEEDS_FIX vote** (PASS-level unanimity)
5. **0 R2 critical, 1 R2 important** (security-sensitive QA-R2-2 已 inline closed)

---

## Spec final state (Approved 2026-05-13)

```
openspec/changes/aria-2.0-m5-replay-reconciler-drift-review-loop-audit/
├── proposal.md  (~370 lines after R2-cleanup, Status: Approved)
└── tasks.md     (~290 lines after R2-cleanup, Status: Approved)

Effort baseline:    138h (AI portion, T-deploy owner-runnable not counted)
OD-M5-1 trigger:    165h (= 138 × 1.20)
PERT 三点估算:       optimistic 117h / likely 138h / pessimistic 165h

7 scope items lock:  A Replay (10h) + B Failure analysis (15h) + C Drift defense (12h)
                     + D Review loop hybrid (52h) + E Audit log immutable (15h)
                     + F Risk-tier dual-write (5h) + G cron direct (6h)
                     Phase 6 总收: ~18h (acceptance + docs + prd-reframe)
推 M6:              H aria-layer2-runner deploy / F.algorithm / A.advanced /
                     B.advanced / C.advanced
11 AD-M5 slots:     M5-1..M5-11 全 reserved (Phase B 实施期回填)
abi_compat hard:    4 promises from m4-handoff (M5 不可违反; validate-m5-handoff.py
                     6 checks enforce)
```

---

## 准入 sign-off

- [x] Owner authorize via "遵循aria规范进行决策和选择,往下推进" (2026-05-13)
- [x] AI execute per Aria规范 default convergence (per `feedback_owner_invoked_convergence_loop` 未 owner-invoke)
- [x] Phase A.0 brainstorm Q0-Q9 全 locked
- [x] Phase A.1 spec-drafter proposal + tasks complete
- [x] Phase A.2 R1+R2 audit 4/4 SCOPE_OK_R2
- [x] R2-cleanup 14 polish applied
- [x] Spec frontmatter Status: Draft → Approved (proposal + tasks)
- [x] Audit trajectory documented in proposal frontmatter
- [x] Effort baseline reconciled (138h) + OD trigger raised (165h)
- [x] R2-cleanup 14 findings 全部 addressed inline OR explicit deferral rationale

---

## ▶️ Next: Phase B.1 分支创建

Per ten-step-cycle Phase B.1 (per `aria/skills/branch-manager/SKILL.md`):

```bash
# Aria 主仓
git checkout -b feature/aria-2.0-m5 master

# aria-orchestrator submodule
git -C aria-orchestrator checkout -b feature/aria-2.0-m5 master
```

Phase B.2 实施按 proposal §How total strategy 6 Phase 顺序:
1. Phase 1 Schema + Foundation (~25h)
2. Phase 2 G cron direct + B failure analysis (~21h, 可并行)
3. Phase 3 D Review loop hybrid (~52h, 含 mid-checkpoint after schema+protocol ~15h)
4. Phase 4 A Replay (~10h)
5. Phase 5 C Drift defense (~12h)
6. Phase 6 acceptance + docs + prd-reframe + T-deploy (~18h AI + owner-runnable deploy)

每 Phase 内部串行, Phase 2/3 + Phase 4/5 之间可视情况并行 (per §dependency graph)。

---

## Cross-references

- [Brainstorm decision](2026-05-10-us025-m5-brainstorm.md) — Q0-Q9 全 locked
- [OD-M4-2 retrospective](2026-05-09-od-m4-2-underbaseline-retrospective.md) — M5 application guidance
- [R1 audit report](../audit-reports/post_spec-R1-2026-05-10T1506Z-aria-2.0-m5.md)
- [R2 audit report](../audit-reports/post_spec-R2-2026-05-12T2351Z-aria-2.0-m5.md)
- [US-025](../../docs/requirements/user-stories/US-025.md) — parent User Story
- [PRD §M5](../../docs/requirements/prd-aria-v2.md) — milestone roadmap (待 Phase 6 同步 actual scope)
- [m4-handoff.yaml::abi_compat_promises](../../aria-orchestrator/docs/m4-handoff.yaml) — 4 forward-binding hard constraints

---

**Status**: Approved 2026-05-13 — Ready for Phase B.1 分支创建
