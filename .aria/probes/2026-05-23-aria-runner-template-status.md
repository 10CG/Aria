# Probe: aria-runner-template status (T1.0 / DEC-20260523-001)

> **Date**: 2026-05-23 ~12:40 UTC
> **Branch**: feature/layer2-docker-auth-fix
> **Spec**: openspec/changes/aria-layer2-docker-auth-cold-pull-fix/proposal.md
> **Author**: solo-lab (uni.concept.wzfq@gmail.com), Claude Opus 4.7

---

## §1 决定 — 走分支 (b): registered 但无 recent dispatch

依据:
- 3 节点 nomad job status: registered (Submit Date 2026-04-23T04:07:06Z, batch/parameterized, status=running)
- nomad job allocs aria-runner-template: **0 placements**
- nomad job status -json grep 子 dispatch: **0 个 dispatch-* children**
- 自 2026-04-23 (M3 era) 注册以来无任何 dispatch invocation

不符合分支 (a) "active + 有 recent dispatch": 0 dispatch = 显然不是
不符合分支 (c) "未 registered": Nomad job 在 3 节点都 running, status registered = 不是

**分支 (b)** 决定:
- 删 task-level `auth { ... }` block (L78-81) — 与 aria-layer2-runner.hcl 保 parity
- 文件 header 加 deprecation 注释 (不删文件): `# DEPRECATED (DEC-20260523-001): M1 baseline 自 2026-04-23 注册无 dispatch; M3 后由 aria-layer2-runner.hcl supersede; 文件保留作 M1 historical reference, 不应 nomad job stop (避免误删 registered 但 dormant 的 job artifact)`
- commit message template: `feat(layer2): delete auth block from aria-layer2-runner; deprecate aria-runner-template (M1 baseline, no recent dispatch)`

---

## §2 调查证据

### nomad job status (3 nodes 一致)

```
ID            = aria-runner-template
Name          = aria-runner-template
Submit Date   = 2026-04-23T04:07:06Z
Type          = batch
Priority      = 50
```

### nomad job inspect (parameterized 验证)

```
Submit: 1776917226795567781 (= 2026-04-23 UTC)
ParameterizedJob: True
Status: running
StatusDescription: (empty)
```

### Allocation history

```
nomad job allocs aria-runner-template:
  No allocations placed
```

### Sub-dispatch children

```python
{matches: 0 dispatch children with name prefix 'aria-runner-template/dispatch-*'}
```

---

## §3 Repo references (grep audit)

### Active code paths (Tier 1 — 触发 actual nomad dispatch)

| File | Line | Context | 影响 |
|------|------|---------|------|
| `aria-orchestrator/scripts/dispatch-issue.sh` | 26 | `JOB_NAME="aria-runner-template"` | **active script**, 用户可能手动跑 |
| `aria-orchestrator/scripts/t5-run-demo.sh` | 118 | `nomad job dispatch ... aria-runner-template` | **active script** |
| `aria-orchestrator/scripts/tests/test-dispatch-idempotency.sh` | (TBD) | test reference | test 路径 |

→ 这些 script 在 M3 deprecation 后未跟进, 与 nomad job 0-dispatch 一致 = 假设 owner 不再手动用 (但还能用)。

### Doc references (Tier 2 — 不触发 nomad dispatch)

- `aria-orchestrator/nomad/jobs/aria-runner-template.hcl` (本 Spec 改它)
- `aria-orchestrator/nomad/jobs/aria-smoke-resources.hcl` (smoke test, 可能 reference)
- `aria-orchestrator/nomad/jobs/aria-smoke-env-probe.hcl` (smoke test)
- `aria-orchestrator/nomad/jobs/aria-layer2-runner.hcl` (M3 supersede 提到 forked from)
- `aria-orchestrator/nomad/README.md` (job inventory)
- `aria-orchestrator/scripts/README.md` (script doc)
- `aria-orchestrator/docs/m1-report.md` (M1 era report, 不动)
- `aria-orchestrator/docs/t2-2-job-register-dispatch-evidence.md` (M1 evidence, 不动)
- `aria-orchestrator/docs/architecture-decisions.md` (AD-M1-8 等, T3.2 加 Revised note)
- `aria-orchestrator/docs/bot-token-lifecycle-design.md` (设计文档)
- `aria-orchestrator/docker/aria-runner/modes/initial.sh` (docker container script)
- `aria-orchestrator/spikes/m1-registry-auth/spike-procedure.md` (M1 spike doc)
- `docs/handoff/2026-05-22-m5-phase-c-playbook.md` (M5 playbook, M5 era)
- `docs/handoff/2026-05-21-m5-phase-b-stabilization-hermes-luxeno.md` (M5 era)
- `docs/handoff/2026-05-09-track-a-deploy-done.md` (M4 era)
- `docs/requirements/user-stories/US-021.md` (US-021 M1 spec)
- `docs/requirements/prd-aria-v2.md` (PRD v2)

→ Tier-2 全部 archive / historical doc 不动 (per Spec out-of-scope: scope 限于本 Spec 改的文件)。

---

## §4 Follow-up Forgejo issue 草稿 (per R1 M-qa-M-2 enforcement)

**File new issue 时机**: T2.2 commit 时一起 file (或独立 ad-hoc)。

### Issue draft

**Title**: `tech-debt: dispatch-issue.sh + t5-run-demo.sh + test-dispatch-idempotency.sh 引用 deprecated job aria-runner-template`

**Labels**: `tech-debt`, `m1-baseline-cleanup`

**Body**:

```markdown
## Background

DEC-20260523-001 (Spec: aria-layer2-docker-auth-cold-pull-fix) 在 Phase B T2.2 把 `aria-orchestrator/nomad/jobs/aria-runner-template.hcl` 标记为 deprecated (M1 baseline, 自 2026-04-23 注册以来 0 个 dispatch, 已由 aria-layer2-runner.hcl 在 M3 era supersede)。

但以下 active scripts 仍引用 `JOB_NAME="aria-runner-template"`:

- `aria-orchestrator/scripts/dispatch-issue.sh:26`
- `aria-orchestrator/scripts/t5-run-demo.sh:118`
- `aria-orchestrator/scripts/tests/test-dispatch-idempotency.sh` (需 verify exact line)

这些 script 是 pre-existing M1-era drift, **不在 aria-layer2-docker-auth-cold-pull-fix Spec scope** (per proposal §Out of Scope), 但需要 follow-up 处理。

## Proposal

将上述 3 个 script 更新为引用 `aria-layer2-runner` (M3 supersedeing job), 或显式标记 deprecated 并 disable interactive run prompt。

## Acceptance

- [ ] `grep -rn 'aria-runner-template' aria-orchestrator/scripts/` 输出全是 `# DEPRECATED` 注释或已替换为 `aria-layer2-runner`
- [ ] 至少 1 test 验证 dispatch-issue.sh + t5-run-demo.sh 用 aria-layer2-runner 跑通

## References

- Parent Spec: openspec/changes/aria-layer2-docker-auth-cold-pull-fix/
- DEC: .aria/decisions/2026-05-23-layer2-docker-auth-cold-pull-fix.md
- Probe: .aria/probes/2026-05-23-aria-runner-template-status.md
```

---

## §5 决策 → 后续 task gating

- **T2.2** 走分支 (b) 实施:
  - 删 L78-81 task `auth { ... }` block
  - 文件 header (L1-L10 之间) 加 deprecation header banner
  - commit message: `feat(layer2): delete auth block from aria-layer2-runner; deprecate aria-runner-template (M1 baseline, no recent dispatch)` + reference 本 probe report

- **T11.4 (Phase D)** open Forgejo issue (内容 per §4 草稿)

- **Acceptance A** 不变: grep 双 HCL (`aria-layer2-runner.hcl` + `aria-runner-template.hcl`) 均 0 个 task-level `auth { ... }` block; deprecation 注释包整体 file header 不会增加 `auth\s*{` 匹配。

---

**Created**: 2026-05-23 ~12:40 UTC
**Author**: solo-lab (uni.concept.wzfq@gmail.com), drafted by Claude Opus 4.7
