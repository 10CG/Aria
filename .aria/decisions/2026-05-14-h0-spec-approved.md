# Phase A.3 Approval — aria-ten-step-session-handoff-stage (H0)

**Date**: 2026-05-14
**Decision**: Approve Spec for Phase B implementation
**Status transition**: Draft → **Approved**
**Cycle**: H0 (Forgejo Aria #92 — ten-step cycle + session-handoff stage)
**Target release**: aria-plugin v1.21.0 MINOR

---

## Approval criteria checklist

- [x] **Phase A.1 Spec drafted** — proposal.md + tasks.md created at `openspec/changes/aria-ten-step-session-handoff-stage/`
- [x] **Phase A.2 R1 audit completed** — 3 agents parallel (backend-architect / knowledge-manager / qa-engineer)
  - 1 Critical (schema bump), 8 Major, 4 Minor, 4 Observations aggregated
  - 10 inline-fixes applied (F1-F10): schema bump dropped, D.3 trigger fallback hierarchy, hook absolute-path regex, 9-section template (added §8 Memory entries), Rule #9 ship-time activation, CLAUDE.md 信息地图 update, hook shell subprocess test, benchmark restructured to structural metrics, migration idempotency + rollback, T8 estimate corrected 1h → 3h
- [x] **Phase A.2 R2 verify completed** — same 3 agents re-audited
  - 0 new Critical, 4 new Major (all editorial 1-line fixes), no oscillation
  - knowledge-manager: CONVERGED ✅
  - backend / qa: PASS_WITH_WARNINGS, no R3 needed
  - 4 editorial fixes applied (G1-G4): 3 stale "schema 1.1" prose corrected, regex Windows backslash compat, hook exit-code mechanism clarified (JSON deny preferred + exit-2 fallback), `git restore -SW` flags added
- [x] **Convergence verdict**: SCOPE_OK_R2 per Aria pragmatic convergence (memory `feedback_post_spec_audit_pragmatic_convergence.md` — unanimous PASS + verdict 改善 + 无振荡 = 实质收敛, 严格 4-tuple set equality 仅 R3+ 振荡检测时关键)

## Spec final state

```
Location:        openspec/changes/aria-ten-step-session-handoff-stage/
Level:           2 (Minimal — multi-file structural, ~20h)
Status:          Approved 2026-05-14
Effort baseline: 20h (corrected from 17h per R1 qa-M4 estimate)
PERT:            optimistic 17h / likely 20h / pessimistic 24h
OD trigger:      24h (20h × 1.20 reforecast trigger)

8 tasks (T1-T8):
  T1 collectors/handoff.py + snapshot.handoff field (L2)         ~4h
  T2 phase-d-closer D.3 + 9-section template (L5)                ~4h
  T3 PreToolUse hook (L1)                                        ~2h
  T4 RECOMMENDATION_RULES.md handoff_drift rule (L3)             ~1h
  T5 standards/conventions/session-handoff.md (L4)
     + CLAUDE.md Rule #9 activation + 信息地图 update             ~2.5h
  T6 migrate 6 .aria/handoff/*.md → docs/handoff/                ~1.5h
  T7 tests + Phase D dogfood                                     ~2h
  T8 pre-merge audit + benchmark + 3-repo ship + v1.21.0 release ~3h
                                                                 ─────
                                                                 ~20h

5-layer defense matrix:
  L1 PreToolUse hook (block .aria/handoff/*.md writes)
  L2 scan.py collectors/handoff.py (detect misplaced_files)
  L3 RECOMMENDATION_RULES.md handoff_drift (推荐迁移工作流)
  L4 standards/conventions/session-handoff.md (Convention SOT)
  L5 phase-d-closer template hardcode docs/handoff/ (写入侧)

Source incidents (4 dogfood):
  - SilkNode 2026-05-09 (#92 原文,跨 session 漏读 handoff)
  - Aria self 2026-05-13 ×3 (含本 session — state-scanner 推荐未读 handoff,
    .aria/handoff/ vs docs/handoff/ 双 dir 漂移 self-evident)

CLAUDE.md 不可协商规则 — Rule #9 ship-time 同步激活:
  与 Rule #7 (secret-hygiene 2 incidents) / #8 (pre-merge 1 incident) 一致 ship 即激活
  本 cycle dogfood 数 (4) > Rule #7/#8,无延迟观察依据
```

## Phase B entry conditions

- [x] Spec approved (此 doc 签收)
- [ ] Feature branch `feature/aria-ten-step-session-handoff-stage` 创建 (Phase B.1, 待执行)
- [ ] 3 repo branches dual-pushed (Aria main + aria submodule + standards submodule)

## Risks acknowledged at approval time

| Risk | Mitigation |
|------|------------|
| 20h Level 2 上限附近 — 若 Phase B 出 scope creep 推 21h+ | OD trigger 24h, 24h+ 时拆 sub-cycle 推 v1.22.0 |
| Rule #9 ship-time 激活可能 churn | 4 dogfood 实证 > Rule #7/#8, 风险低 |
| PreToolUse hook 跨平台兼容 (Windows backslash) | G2 fix 加 `[/\\]` char class, T3.4 smoke test cover |
| 本 cycle Phase D dogfood bootstrap | T7.4 已澄清: v1.21.0 ship 后手动模拟 D.3 流程,plugin update 不是 pre-req |

## Audit reports archived

R1:
- `.aria/audit-reports/post_spec-R1-2026-05-14T0000Z-aria-ten-step-session-handoff-stage-backend.md`
- `.aria/audit-reports/post_spec-R1-2026-05-14T0000Z-aria-ten-step-session-handoff-stage-knowledge.md`
- `.aria/audit-reports/post_spec-R1-2026-05-14T0000Z-aria-ten-step-session-handoff-stage-qa.md`

R2:
- `.aria/audit-reports/post_spec-R2-2026-05-14T0030Z-aria-ten-step-session-handoff-stage-backend.md`
- `.aria/audit-reports/post_spec-R2-2026-05-14T0030Z-aria-ten-step-session-handoff-stage-knowledge.md`
- `.aria/audit-reports/post_spec-R2-2026-05-14T0030Z-aria-ten-step-session-handoff-stage-qa.md`

## References

- Trigger: Forgejo Aria [#92](https://forgejo.10cg.pub/10CG/Aria/issues/92) (triage [#6170](https://forgejo.10cg.pub/10CG/Aria/issues/92#issuecomment-6170))
- Triage report: `.aria/triage-92.json`
- Proposal: `openspec/changes/aria-ten-step-session-handoff-stage/proposal.md`
- Tasks: `openspec/changes/aria-ten-step-session-handoff-stage/tasks.md`
- Precedent (Rule #7 structure): `standards/conventions/secret-hygiene.md`
- Convergence convention: memory `feedback_post_spec_audit_pragmatic_convergence.md`
- Predecessor handoff: `.aria/handoff/2026-05-13-issue-101-cycle-closeout.md` §3 H0

---

**Approved by**: User (Phase A.3 signoff, 2026-05-14)
**Next phase**: Phase B.1 — create `feature/aria-ten-step-session-handoff-stage` branch on Aria main + aria submodule + standards submodule, dual-push
