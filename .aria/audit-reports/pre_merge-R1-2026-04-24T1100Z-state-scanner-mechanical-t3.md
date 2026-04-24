---
checkpoint: pre_merge
spec: state-scanner-mechanical-enforcement
pr: [21, 34]
branch: feature/state-scanner-mechanical-t3
head_before_r2: e5693b8
head_after_r2: 730fba6
round: 1
timestamp: 2026-04-24T11:00Z
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer]
converged: false
verdict: PASS_WITH_WARNINGS
critical_count: 3
important_count: 11
minor_count: 8
proceed_consensus: 3/4 iterate_then_merge, 1/4 merge_now
---

# Pre-merge Audit Round 1 — state-scanner-mechanical-enforcement T3 scope-bounded

## PRs audited
- aria-plugin #21 — feature/state-scanner-mechanical-t3 @ e5693b8 (4 commits)
- Aria main #34 — submodule bump 3f05158→e5693b8 + tasks.md + audit reports

## Verdict Convergence

| Agent | Verdict | Vote | Critical | Important | Minor |
|---|---|---|---|---|---|
| tech-lead | PASS_WITH_WARNINGS | approve_with_revisions | 1 (TL-R1-C1 merge order) | 4 | 2 |
| backend-architect | PASS_WITH_WARNINGS | approve_with_revisions | 1 (BA-R1-C1 spec drift) | 3 | 2 |
| qa-engineer | PASS_WITH_WARNINGS | approve_with_revisions | 1 (QA-R1-C1 not_a_git_repo) | 4 | 3 |
| code-reviewer | PASS_WITH_WARNINGS | merge_now | 0 | 0 | 3 |

**3/4 iterate, 1/4 merge_now**. Any critical → must iterate per pre_merge rule.

## Critical Findings

### QA-R1-C1 / CR-R1-m1 / BA-R1-I1 — 3/4 agent consensus
- **Title**: `collect_multi_remote` not-a-git-repo fallback hardcodes `overall_parity=True`
- **Severity**: qa-engineer=critical, code-reviewer=minor, backend-architect=important. Classified CRITICAL by round aggregate (consensus on issue + one agent calls it critical).
- **Fix applied in 730fba6**: `multi_remote.py:454` flipped `True→False` with explicit audit-trail comment. Synthetic test confirms. QA-C1 regression test still passes.

### BA-R1-C1 — backend-architect independent
- **Title**: SKILL.md §1.12 `overall_parity` definition diverges from `_aggregate_flags` implementation
- **Impact**: Mixed equal+unknown topology (feature branch with origin+github, one pushed one not) would confuse spec consumers — code says True (has positive evidence), spec says False (not all equal). On paper the spec is stricter, but QA-C1 fix established the "positive-evidence" invariant.
- **Fix applied in 730fba6**: Rewrote SKILL.md §1.12 overall_parity definition with 4-bullet explicit rule + rationale paragraph. Module docstring synced. Spec now matches `_aggregate_flags` semantics literally.

### TL-R1-C1 — tech-lead (process constraint, NOT code)
- **Title**: PR merge order enforcement — PR #21 must merge before PR #34
- **Reason**: PR #34 bumps aria submodule pointer to a commit that lives only on the aria feature branch. Merging #34 first would leave a dangling submodule pointer (same bug class as `feedback_submodule_branch_before_archive.md`).
- **Action**: Process-level, not code. To be enforced at actual merge time.

## Important Findings (all deferred with rationale)

All 11 important findings across 4 agents are deferred under scope-bounded merge pattern:

- **TL-R1-I1** Spec un-archived during partial merge — consistent with PR #33 precedent
- **TL-R1-I2** SKILL.md v2.10 vs scan.py implementation drift — T5 rewrite deferred
- **TL-R1-I3** CLAUDE.md rule #6 benchmark at T10 release gate
- **TL-R1-I4** overall_parity 6-scenario test was manual — T6 fixture
- **QA-R1-I1** forgejo_config/issue_scan hardcode `origin` remote — T6/T8 docs
- **QA-R1-I2** issue_scan budget 1s floor under high N — documented fail-soft
- **QA-R1-I3** `_KNOWN_FORGEJO_HOSTS` not config-driven — T4 docs + future enhancement
- **QA-R1-I4** tests/ directory empty — T6 explicit task, blocks nothing today
- **BA-R1-I2** main_repo.path / items[].heuristic not in SKILL.md — T4.1 schema
- **BA-R1-I3** cache v1.0 fallback owner_repo mismatch — T6 hardening
- **BA-R1-I1** (subsumed by QA-R1-C1 fix above)

## Minor Findings (8 total, all post-merge follow-ups)

- docstring gaps on pre-T3 helpers (CR-R1-m3)
- module-level docstring drift (BA-R1-M1, now fixed with BA-R1-C1 SKILL.md update)
- `ERR_AUTH_MISSING` dead enum (BA-R1-M2) — T4 reserved label
- sync.py `time` import inside function body (QA-R1-M1) — 1-line follow-up
- issue_scan `_lookup_cached_repo` forward-reference layout (QA-R1-M2) — T4 cleanup
- multi_remote `_scan_repo` dead tuple return (QA-R1-M3) — T4 cleanup
- audit report location (TL-R1-M1) — no action, noted
- PR title em-dash (TL-R1-M2) — no action, noted

## R2 Plan (applied in commit 730fba6 on aria branch)

1. **Code fix**: `multi_remote.py:454` `overall_parity: True → False` (not_a_git_repo path)
2. **Doc fix**: SKILL.md §1.12 `overall_parity` definition rewritten + rationale paragraph
3. **Doc fix**: `multi_remote.py` module docstring synced with new semantics

Process constraint TL-R1-C1 addressed at merge time, not by commit.

## Expected R2 findings

- QA-R1-C1 / CR-R1-m1 / BA-R1-I1 (not_a_git_repo): RESOLVED — should not appear
- BA-R1-C1 (SKILL.md drift): RESOLVED — should not appear
- TL-R1-C1 (merge order): PERSISTS until actual merge happens
- All other important/minor: PERSIST (deferred intentionally)

R2 → R3 convergence expected when R2's findings set == R3's findings set (i.e., remaining deferred set is stable across two rounds).
