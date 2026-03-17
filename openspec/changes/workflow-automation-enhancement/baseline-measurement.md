# Baseline Measurement: Manual Steps in Level 2 Feature Workflow

> **Date**: 2026-03-16
> **Workflow**: feature-dev (A.0 → D.2)
> **Methodology**: Count each distinct human input as one step
> **Scope**: Level 2 feature, full end-to-end cycle including Phase D

## Assumptions

- **Level 2 feature**: Requires proposal.md but not tasks.md (Minimal spec)
- **No pre-existing OpenSpec**: User starts from scratch (no skip of A.1)
- **No pre-existing detailed-tasks.yaml**: Full planning required
- **Standard branch mode**: Not worktree (simple feature)
- **Multiple tasks**: Assume 3 tasks executed via subagent-driver (SDD)
- **PR required**: Feature branch merged via PR
- **UPM configured**: Progress tracking is active
- **Brainstorm not triggered**: No fuzziness detection (standard flow)

## Step-by-Step Trace

| # | Phase | Step | Human Action | Type |
|---|-------|------|-------------|------|
| 1 | A.0 | State scan | Invoke `/state-scanner` (or describe intent) | command |
| 2 | A.0 | Wait for scan | Read status output (no input, but attention required) | passive |
| 3 | A.0 | Choose workflow | Select `[1] feature-dev` from recommended options | confirmation |
| 4 | - | Workflow plan | Review execution plan displayed by workflow-runner | passive |
| 5 | - | Confirm workflow | Confirm "Execute this workflow? [Yes/No]" | gate |
| 6 | A.1 | Spec drafter invoked | Provide feature requirement description to spec-drafter | input |
| 7 | A.1 | Level confirmation | Review auto-detected Level 2 and confirm or override | confirmation |
| 8 | A.1 | Module confirmation | Review auto-detected module and confirm or override | confirmation |
| 9 | A.1 | Spec preview review | Review generated proposal.md preview content | passive |
| 10 | A.1 | Approve spec creation | Confirm "Create this file? [Yes/No/Edit]" | gate |
| 11 | A.1 | Interactive chapter review (Why) | Confirm or edit the "Why" section | confirmation |
| 12 | A.1 | Interactive chapter review (What) | Confirm or edit the "What" section | confirmation |
| 13 | A.1 | Interactive chapter review (Deliverables) | Confirm or edit deliverables | confirmation |
| 14 | A.1 | Interactive chapter review (Success Criteria) | Confirm or edit success criteria | confirmation |
| 15 | A.2 | Task planning output | Review generated task list from task-planner | passive |
| 16 | A.2 | Approve task plan | Confirm task decomposition is acceptable | gate |
| 17 | A.3 | Agent assignment output | Review agent-to-task mapping | passive |
| 18 | A.3 | Approve agent assignment | Confirm agent assignments are acceptable | gate |
| 19 | B.1 | Branch creation | Review branch name and mode decision (auto/branch/worktree) | passive |
| 20 | B.1 | Confirm branch | Confirm branch creation (or accept auto-created branch) | confirmation |
| 21 | B.1 | Environment validation | Review .gitignore and environment check results | passive |
| 22 | B.1 | Fix environment issues (if any) | Approve auto-fix for .gitignore or dependency issues | confirmation |
| 23 | B.2 | Subagent Task 1 start | Observe subagent-driver launching Fresh Subagent for TASK-001 | passive |
| 24 | B.2 | Agent routing (Task 1) | Select agent from recommended list (if not auto-matched) | confirmation |
| 25 | B.2 | Task 1 completion review | Review change summary and code review results for TASK-001 | passive |
| 26 | B.2 | Task 1 completion choice | Select from 4 options: [1] Continue / [2] Modify / [3] Reset / [4] Pause | confirmation |
| 27 | B.2 | Agent routing (Task 2) | Select agent from recommended list (if not auto-matched) | confirmation |
| 28 | B.2 | Task 2 completion review | Review change summary and code review results for TASK-002 | passive |
| 29 | B.2 | Task 2 completion choice | Select from 4 options: [1] Continue / [2] Modify / [3] Reset / [4] Pause | confirmation |
| 30 | B.2 | Agent routing (Task 3) | Select agent from recommended list (if not auto-matched) | confirmation |
| 31 | B.2 | Task 3 completion review | Review change summary and code review results for TASK-003 | passive |
| 32 | B.2 | Task 3 completion choice | Select from 4 options (final task, typically [1]) | confirmation |
| 33 | B.3 | Branch finisher validation | Review test pre-validation results (unit, build, lint, coverage) | passive |
| 34 | B.3 | Branch finisher completion | Select from 4 options: [1] Commit+PR / [2] Continue / [3] Abandon / [4] Pause | gate |
| 35 | C.1 | Commit message review | Review generated commit message from commit-msg-generator | passive |
| 36 | C.1 | Approve commit | Confirm commit message and execute `git commit` | gate |
| 37 | C.2 | PR creation review | Review generated PR title and body | passive |
| 38 | C.2 | Approve PR creation | Confirm PR creation | gate |
| 39 | C.2 | PR merge wait | Wait for PR review / approval (external) | external-wait |
| 40 | C.2 | Confirm merge | Confirm merge of PR (or approve auto-merge) | gate |
| 41 | C.2 | Worktree cleanup (if applicable) | Select cleanup option: [1] Clean / [2] Preserve | confirmation |
| 42 | D.1 | Progress update review | Review UPM progress update summary | passive |
| 43 | D.1 | Approve progress update | Confirm UPM state write | confirmation |
| 44 | D.2 | Spec archive review | Review spec archive action (move to archive/) | passive |
| 45 | D.2 | Approve spec archive | Confirm OpenSpec archival | gate |

## Summary

| Metric | Count |
|--------|-------|
| **Total manual steps** | **45** |
| **Active input steps** (commands, confirmations, gates) | **30** |
| **Passive review steps** (reading output, no input) | **14** |
| **External wait steps** | **1** |

### Breakdown by Type

| Type | Count | Description |
|------|-------|-------------|
| `command` | 1 | User initiates a skill invocation |
| `input` | 1 | User provides substantive content (requirement text) |
| `confirmation` | 16 | User selects an option or confirms a recommendation |
| `gate` | 9 | User approves a critical action (spec creation, commit, PR, merge, archive) |
| `passive` | 14 | User reads output but provides no input |
| `external-wait` | 1 | Waiting for external action (PR review) |

### Breakdown by Phase

| Phase | Active Steps | Passive Steps | Total |
|-------|-------------|---------------|-------|
| A.0 (State scan) | 2 | 1 | 3 |
| Workflow confirm | 1 | 1 | 2 |
| A.1 (Spec management) | 6 | 1 | 7 |
| A.2 (Task planning) | 1 | 1 | 2 |
| A.3 (Agent assignment) | 1 | 1 | 2 |
| B.1 (Branch creation) | 2 | 2 | 4 |
| B.2 (Execution - 3 tasks) | 6 | 3 | 9 |
| B.3 (Branch finisher) | 1 | 1 | 2 |
| C.1 (Git commit) | 1 | 1 | 2 |
| C.2 (PR/merge) | 3 | 1 | 4 |
| C.2 (Worktree cleanup) | 1 | 0 | 1 |
| D.1 (Progress update) | 1 | 1 | 2 |
| D.2 (Spec archive) | 1 | 1 | 2 |
| **External wait** | 0 | 0 | 1 |
| **TOTAL** | **27** | **14** | **45** |

### Gate Confirmations (Critical Decision Points)

These are steps where the user must approve a significant, potentially irreversible action:

| # | Phase | Gate Description |
|---|-------|-----------------|
| 5 | - | Confirm workflow execution plan |
| 10 | A.1 | Approve spec file creation |
| 16 | A.2 | Approve task decomposition |
| 18 | A.3 | Approve agent assignments |
| 34 | B.3 | Approve branch completion option |
| 36 | C.1 | Approve commit execution |
| 38 | C.2 | Approve PR creation |
| 40 | C.2 | Approve PR merge |
| 45 | D.2 | Approve spec archival |

**Total gate confirmations: 9**

### Automation Target Calculation

```
Total manual steps:                      45
  Minus external wait (not automatable):  -1
  Minus gates (must remain manual):       -9
  ─────────────────────────────────────────
  Non-gate, automatable steps:            35

50% reduction target for non-gate steps: 35 * 0.5 = ~18 steps eliminated

Post-automation expected total:
  Gates (kept):                            9
  Non-gate steps after 50% reduction:     17
  External wait:                           1
  ─────────────────────────────────────────
  Target total:                           27
```

## Scaling Note

The B.2 (execution) phase scales linearly with task count. For each additional task:
- +1 agent routing confirmation (if not auto-matched)
- +1 passive review of results
- +1 completion choice (4-option selection)

With N tasks, B.2 contributes 3N steps (N=3 in this baseline = 9 steps).

## Sources

- `/home/dev/Aria/aria/skills/state-scanner/SKILL.md` (v2.4.0)
- `/home/dev/Aria/aria/skills/workflow-runner/SKILL.md` (v2.2.0)
- `/home/dev/Aria/aria/skills/workflow-runner/WORKFLOWS.md` (v2.0.0)
- `/home/dev/Aria/standards/core/ten-step-cycle/README.md` (v2.3.0)
- `/home/dev/Aria/aria/skills/phase-a-planner/SKILL.md` (v1.0.0)
- `/home/dev/Aria/aria/skills/phase-b-developer/SKILL.md` (v1.3.0)
- `/home/dev/Aria/aria/skills/phase-c-integrator/SKILL.md` (v1.1.0)
- `/home/dev/Aria/aria/skills/phase-d-closer/SKILL.md` (v1.0.0)
- `/home/dev/Aria/aria/skills/spec-drafter/SKILL.md` (v2.1.0)
- `/home/dev/Aria/aria/skills/subagent-driver/SKILL.md` (v1.3.0)
- `/home/dev/Aria/aria/skills/commit-msg-generator/SKILL.md` (v2.0.0)
- `/home/dev/Aria/aria/skills/branch-manager/SKILL.md` (v2.0.0)
- `/home/dev/Aria/aria/skills/branch-finisher/SKILL.md` (v1.0.0)
