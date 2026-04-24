---
checkpoint: post_implementation
spec: state-scanner-mechanical-enforcement
phase: B.2 T3 (T3.2-T3.5 parallel impl)
round: 1
timestamp: 2026-04-24T10:00Z
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer]
converged: false
verdict: PASS_WITH_WARNINGS
proceed_recommendation: iterate_then_integrate
critical_count: 2
important_count: 14
minor_count: 12
---

# T3.2-T3.5 Post-Implementation Audit — Round 1

## Scope

4 new collectors produced by parallel impl agents (T3.2-T3.5):
- `collectors/sync.py` (430 lines) — Phase 1.12 local/remote sync
- `collectors/multi_remote.py` (504 lines) — Phase 1.12 multi-remote parity
- `collectors/issue_scan.py` (801 lines) — Phase 1.13 Issue awareness
- `collectors/forgejo_config.py` (127 lines) — Phase 1.14 Forgejo config detection

Plus integration into `scan.py` + `collectors/__init__.py`.

Pre-audit smoke test: rc=0, 0 soft errors, snapshot parseable.

## Verdict Convergence

| Agent | Verdict | Vote | Critical | Important | Minor |
|---|---|---|---|---|---|
| tech-lead | PASS_WITH_WARNINGS | approve_with_revisions | 0 | 4 | 3 |
| backend-architect | PASS_WITH_WARNINGS | approve_with_revisions | 0 | 5 | 4 |
| qa-engineer | PASS_WITH_WARNINGS | approve_with_revisions | **2** | 5 | 4 |
| code-reviewer | PASS_WITH_WARNINGS | approve_with_revisions | 0 | 4 | 5 |

**Convergence**: 3/4 vote iterate_then_integrate, 1/4 (code-reviewer) votes integrate_now.
Any critical finding blocks integrate_now per pre_merge template.

## Critical Findings (must-fix before integrate)

### QA-C1: multi_remote `overall_parity=True` when all remotes `parity=unknown`
- **File**: `collectors/multi_remote.py` `_aggregate_flags()`
- **Reproduced** on `/tmp/scan-T3-integrated.json`: main_repo has 2 remotes both `parity: unknown, reason: no_local_tracking_ref` (feature branch without upstream), `overall_parity: true`.
- **Consequence**: Downstream recommender reads has_pending_push=false + overall_parity=true, suppresses push reminders for an unpushed feature branch.
- **Fix applied (R2)**: `overall_parity = has_equal_evidence AND not blocks_parity`. At least one remote must confirm `equal` for True; zero positive evidence → False.

### QA-C2: Forgejo `/issues` endpoint returns PRs mixed with issues
- **File**: `collectors/issue_scan.py` `_fetch_forgejo` + `_normalize_items`
- **Reproduced** on live fetch: `#30 .../pulls/30` appeared in `issue_status.items`. Direct API probe confirmed Forgejo returns PRs even with `type=issues` query (carry `pull_request: True` field).
- **Consequence**: open_count inflated, heuristic linker runs over PR titles (false openspec matches), state-scanner loses "X open issues" precision.
- **Fix applied (R2)**: (1) `&type=issues` added to Forgejo URL (defense-in-depth — unreliable on this version). (2) `_normalize_items` skips any raw item with `pull_request` key OR URL containing `/pulls/`. GitHub `gh issue list` already filters server-side.

## Important Findings — Fixed in R2

### QA-I1: `ls-remote` empty output sets `reachable=False` for never-pushed branch
- **File**: `collectors/multi_remote.py` `_remote_parity_ls_remote()`
- **Fix applied (R2)**: empty stdout with rc=0 → `reason="remote_branch_missing", reachable=True`. Unparseable output → `reason="parse_error", reachable=True`. Prior logic conflated "branch not on remote" with "remote unreachable".

### QA-I3: `forgejo:` inside fenced code block gives false-positive `configured`
- **File**: `collectors/forgejo_config.py` `_has_forgejo_block()`
- **Fix applied (R2)**: Added `_FENCED_BLOCK = re.compile(r"```[\s\S]*?```", re.MULTILINE)` mask; strip fenced blocks before running YAML-key and heading heuristics.

### BA-I1: Aligned submodules emit `behind_count=null, ahead_count=null` instead of `0`
- **File**: `collectors/sync.py` `_collect_submodule_entry()`
- **Fix applied (R2)**: When `tree_commit == remote_commit`, explicitly emit `behind_count=0, ahead_count=0`. Reserves `null` for the fail-soft paths per SKILL.md §1.12 `int | null` contract semantic ("null = unable to measure").

### CR-M1: `collect_forgejo_config` missing function docstring
- **Fix applied (R2)**: Added 6-line docstring documenting the 4-state output contract.

## Important Findings — Deferred (not blockers)

### 4-agent consensus: Helper duplication (TL-I2 / BA-M1 / QA-I5 / CR-I1 / CR-I2)
- `_current_branch`, `_is_shallow`, `_enumerate_submodule_paths` (gitmodules parser) duplicated across `sync.py`, `multi_remote.py`, `issue_scan.py`.
- **Rationale for defer**: Correctness-safe (each version works). Consolidation requires cross-file refactor touching 4 files + test harness. Scheduling as `T3.6 — helper consolidation` follow-up commit to keep R2 focused on correctness bugs.

### TL-I1 / BA-I3 / BA-I4 / BA-I5: `state-snapshot-schema.md` lags implementation
- 4 new top-level keys (`custom_checks`, `sync_status`, `forgejo_config`, `issue_status`) + nested additive fields (`main_repo.path`, `items[].heuristic`) not documented in the schema reference.
- **Rationale for defer**: T4.1 is the explicit task for schema.md authoring. Deferring keeps T3 scope bounded; T4.1 will backfill with complete field enumeration.

### TL-I4 / CR-I3: `issue_scan.py` 801 lines approaches TL-1 threshold (was 1106 for scan.py)
- `collect_issue_scan` function 205 lines; natural extraction points: `_scan_main_repo`, `_scan_one_submodule`, `_aggregate_issue_status`.
- **Rationale for defer**: No correctness issue. Future T6/T7 refactor candidate.

### BA-I2: `auth_missing` enum value defined but never emitted (9/10 reachable)
- **Rationale for defer**: Not a runtime crash; mis-triaged as `auth_failed` at worst. Fix options: (a) implement token-probe call before API, (b) mark enum as reserved in references. Chose (b) for T4 schema reference doc.

### QA-I2 / QA-I4 / various Minor: documentation/observability polish
- Scheduled for T6 test harness + hardening phase.

## Retest

Post-R2 fixes re-ran end-to-end scan:
- `overall_parity`: correctly False for all-unknown (unit regression test passes 6/6 scenarios).
- `issue_status.open_count`: 0 (down from inflated 6), confirming PR filter works. Direct Forgejo API probe confirms their server-side filter is broken on this version; client-side filter is the real defense.
- Aligned submodules now emit `behind_count=0, ahead_count=0` instead of `null`.
- Scan rc=0, 0 soft errors.

## Decision

**iterate_then_integrate was executed in R2**. All 2 Critical + 3 Important (Fixed in R2 list) resolved. Remaining findings are all documentation/quality debt, not correctness blockers. Proceeding to commit + integrate.

Follow-up tasks filed:
- T3.6 — Helper consolidation (4-agent consensus, mechanical refactor)
- T4.1 — schema.md SoT backfill (TL-I1 + BA-I3/I4/I5)
- T6 — Test harness with missing fixtures (QA test_strategy_gaps)
