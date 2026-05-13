# Tasks — Aria Issue #101 status normalize fix

> Parent: [proposal.md](./proposal.md) | **Status**: Phase A.2 R1 SCOPE_OK_R1 (2 agent PASS_WITH_WARNINGS unanimous, 4 Major inline-fixed), ready for Phase B

## Phase B Tasks (按依赖顺序)

### T1 — Fix `_normalize_status` (~30min)

- [x] **T1.1** Edit `aria/skills/state-scanner/scripts/collectors/_status.py`:
  - Reorder check priority: terminal (archived/deprecated) → explicit (pending/in_progress/implemented/approved/reviewed/active/ready) → done fallback
  - Add `implemented` token → new lifecycle state `implemented`
  - Preserve i18n patterns (Pattern 6 fullwidth colon etc.) — DO NOT touch `_STATUS_PATTERNS`
- [x] **T1.2** Update docstring on `_normalize_status` to reflect priority ordering rationale (cite #101)

### T2 — Unit tests (~1h)

- [x] **T2.1** Add `aria/skills/state-scanner/tests/test_status_normalize.py` (new file)
- [x] **T2.2** Test cases (R1 audit refined — 3 categories):
  - **Bug 1+2 fix verification** (4 issue #101 strings, proposal §Success Criteria 列出)
  - **Shadow guards** (R1 BA-M1 / BA-m2 / QA-M1):
    - `"Inactive — superseded"` → `unknown` (NOT `active`)
    - `"Unimplemented stubs"` → `unknown` (NOT `implemented`)
    - `"Incomplete (missing sections)"` → `unknown` (NOT `done`)
    - `"Approved (Implemented by PR-A)"` → `approved` (BA-M2: ordering: approved BEFORE implemented)
  - **Positive regression** (R1 BA-m4 / QA-m5 — confirm reorder didn't break happy path):
    - `"Active"` / `"Reviewed"` / `"Ready"` 单 token → respective states
    - `"In Progress (50% done)"` → `in_progress` (multi-word phrase + shadow inside)
    - `"ready (Phase A done)"` → `ready` (shadow inside narrative)
  - **Existing happy path**:
    - `"Done"` 单 token → `done` (fallback still works)
    - `"Implemented"` 单 token → `implemented` (new state)
    - `"Archived 2026-01-01"` → `archived` (terminal precedence)
    - `None` / 空字符串 → `unknown`
- [x] **T2.3** Run state-scanner 整体 test suite, 确认无 regression (pre-fix all green, post-fix all green)
- [x] **T2.4** Live verify: `python3 aria/skills/state-scanner/scripts/scan.py --output /tmp/scan-after-fix.json` → 检查 `openspec.pending_archive` 在 Aria 当前所有 `openspec/changes/` 内 spec 上为空 (R1 QA-m1: 不写死 4 个,以当前内容为准)

### T3 — Doc update (~30min)

- [x] **T3.1** `aria/skills/state-scanner/SKILL.md` 加 "Status 字段最佳实践" 小节:
  - Status 行格式建议: `<single-token>` 或 `<token> — <narrative>` (token 在 token 字典首位才安全)
  - 列出 supported token set: archived / deprecated / pending / in_progress / implemented / approved / reviewed / active / ready / done / complete
  - 反面教材: "Approved Phase A done" 不安全 (因 narrative 含 done 子串)
  - 推荐: "Approved — Phase A done" 安全 (em-dash 后任意内容,首 token 决定语义)
- [x] **T3.2** 在 `references/state-snapshot-schema.md` 添加 `implemented` 到 `openspec.active[].status` 枚举说明

### T4 — Rule #6 skill-creator benchmark (~1h)

- [x] **T4.1** Run `/skill-creator benchmark state-scanner` (Rule #6 不可协商 — modifying Skill logic)
- [x] **T4.2** Eval prompts (3 cases):
  - Scan Aria itself (current 4 active specs should NOT be in pending_archive post-fix)
  - Scan a synthetic project with mixed "Approved/Implemented/Done" Status
  - Edge case: spec with Status containing both "Implemented" AND "done" in narrative
- [x] **T4.3** Acceptance: delta > 0 on accuracy (pre-fix has false positives on 4/4 Aria spec; post-fix should have 0)
- [x] **T4.4** Store results in `aria-plugin-benchmarks/ab-results/2026-05-13-state-scanner-issue-101-fix/`

### T5 — Phase C ship (~30min)

- [x] **T5.1** Commit T1+T2+T3 to aria submodule on `feature/aria-issue-101-status-normalize`
- [x] **T5.2** Create 2 PRs (aria-plugin + Aria main) referencing #101
- [x] **T5.3** Rule #8 pre-merge gate (aether 1.8.5 fallback `skip_with_warning` applies, same as triage-sop cycle)
- [x] **T5.4** Merge submodule PR first → bump main pointer → merge main PR
- [x] **T5.5** Multi-remote parity verify (origin = github for both repos)
- [x] **T5.6** Close Forgejo Aria #101 (`Closes #101` in PR body or post-merge comment)

### T6 — Phase D archive (~15min)

- [x] **T6.1** Update proposal Status: Draft → Complete
- [x] **T6.2** `openspec archive aria-issue-101-status-normalize --yes`
- [x] **T6.3** Auto-fix CLI bug (move openspec/changes/archive/ → openspec/archive/)
- [x] **T6.4** Commit archive move to main

---

## Phase A.3 Agent Assignment

| Task | Primary agent | Rationale |
|------|---------------|-----------|
| T1 fix | `aria:backend-architect` | Token chain logic, deterministic code |
| T2 tests | `aria:qa-engineer` | Regression + edge case design |
| T3 docs | `aria:knowledge-manager` | SKILL.md best-practices doc |
| T4 benchmark | owner manual `/skill-creator` | Rule #6 不可协商 |
| T5 ship | `phase-c-integrator` skill | standard ship flow |
| T6 archive | `openspec-archive` skill | standard archive flow |

---

## Effort baseline

| Task | Optimistic | Pessimistic |
|---|---|---|
| T1 fix | 0.5h | 1h |
| T2 tests | 1h | 1.5h |
| T3 docs | 0.5h | 1h |
| T4 benchmark | 1h | 1.5h |
| T5 ship | 0.5h | 1h |
| T6 archive | 0.25h | 0.5h |
| **Total** | **~3.75h** | **~6.5h** |

Level 2 minimal scope, ~0.5 day。

---

## Phase B 入口条件 (Phase A.2 audit 通过后)

- ✅ Spec Approved (post_spec R1 or R1+R2)
- ✅ tasks.md well-formed
- ✅ Open Questions resolved (none, scope is clear from triage)
- ✅ Trigger triage evidence cited (issuecomment-5972 + #6019)
