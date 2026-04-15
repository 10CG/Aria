# Round 1 Aggregate Audit Report — PR #19 state-scanner-submodule-issue-scan

**Date**: 2026-04-15
**Checkpoint**: pre_merge (challenge mode)
**Agent Team**: tech-lead + backend-architect + qa-engineer + code-reviewer + knowledge-manager (5 agents)
**Overall Verdict**: **FAIL** (2 CRITICAL blocks merge)

## Per-Agent Verdicts

| Agent | Verdict | CRIT | IMP | MIN |
|---|---|---|---|---|
| backend-architect | **FAIL** | 2 | 2 | 1 |
| code-reviewer | PASS_WITH_WARNINGS | 0 | 3 | 3 |
| qa-engineer | PASS_WITH_WARNINGS | 0 | 3 | 2 |
| tech-lead | PASS_WITH_WARNINGS | 0 | 1 | 2 |
| knowledge-manager | PASS_WITH_WARNINGS | 0 | 2 | 3 |
| **Total** | **FAIL** | **2** | **11** | **11** |

## Findings by Severity

### CRITICAL (2) — blocks merge

| # | Type | Area | Fix target |
|---|---|---|---|
| C1 | cache_schema_migration_gap | issue-scanning.md §Step 5 + live cache | Add schema version guard; invalidate pre-v1.16 caches |
| C2 | per_repo_fetched_at_missing_in_write | issue-scanning.md §Step 3.6 vs §Step 5 | Write per-repo fetched_at OR remove per-repo TTL check |

### IMPORTANT (11)

| # | Agent | Type | Area | Fix target |
|---|---|---|---|---|
| I1 | backend-architect | output_schema_key_rename_is_breaking | SKILL.md output schema | Retain `open_issues` alias OR add schema_version |
| I2 | backend-architect | timeout_not_scaling_with_n | D3 + SKILL.md stage_timeout | Auto-compute OR doc warning on N>3 |
| I3 | tech-lead | non-opt-in-side-effect | D3 timeout 12→20s unconditional | Gate on scan_submodules=true OR doc side effect |
| I4 | code-reviewer | submodule_path_with_spaces | issue-scanning.md §Step 3 for-loop | `while IFS= read -r` or mapfile |
| I5 | code-reviewer | date_d_GNU_only | issue-scanning.md §Step 3.6 | POSIX alternative or documented limitation |
| I6 | code-reviewer | cd_vs_gh_C | issue-scanning.md §Step 3.7 github branch | Use `gh -C` or subshell |
| I7 | qa-engineer | benchmark_metadata_inconsistency | benchmark.json runs_per_configuration=3 | Correct to 1 |
| I8 | qa-engineer | false_positive_assertion | eval-meta-repo assertion "4 repos scanned" | Replace with discriminating assertion |
| I9 | qa-engineer | eval_coverage_gap_backward_compat | benchmark eval suite | Add eval-backward-compat for scan_submodules=false |
| I10 | knowledge-manager | version-drift | RECOMMENDATION_RULES.md footer + changelog | Append v2.10.0 entry + update date |
| I11 | knowledge-manager | schema-mismatch | issue-scanning.md §Output Schema (top, lines 25-46) | Update to v1.1.0 双视图 |

### MINOR (11)

| # | Agent | Type | Area | Action |
|---|---|---|---|---|
| M1 | backend-architect | label_summary_opacity | SKILL.md label_summary | **Skip** — accepted, no per-repo breakdown needed |
| M2 | code-reviewer | ambiguity_now_ts_undefined | issue-scanning.md §Step 3.6 | Define now_ts init |
| M3 | code-reviewer | failsoft_inconsistency | SKILL.md vs fail-soft matrix (uninitialized submodule) | Unify to record fetch_error |
| M4 | code-reviewer | all_repos_json_undefined | issue-scanning.md §Step 3-4 variable | Define construction |
| M5 | tech-lead | decision-gap_limit_aggregation | proposal.md D-records | Add D13 limit semantics |
| M6 | tech-lead | benchmark-report-format | benchmark.md sign convention + per-eval breakdown | Regenerate/expand |
| M7 | qa-engineer | rollback_level1_gap | proposal.md §Rollback L1 | Add shared-path caveat |
| M8 | qa-engineer | ac_not_mechanically_verifiable | proposal.md AC-5/AC-6 | Flag as live-data dependent |
| M9 | knowledge-manager | broken-link_parent_spec_naming | proposal.md frontmatter | Split Parent vs Sister |
| M10 | knowledge-manager | changelog-gap | aria/CHANGELOG.md | Add [1.16.0] TBD entry |
| M11 | knowledge-manager | memory-alignment | CLAUDE.md + memory | **Skip** — positive alignment confirmed |

## Summary

Round 1 exposed **2 CRITICAL schema integrity bugs** that would cause silent cache corruption on upgrade paths, plus **11 IMPORTANT issues** spanning bash portability, benchmark methodology, version drift, and non-opt-in side effects. The Spec is architecturally sound (D1-D12 cover main trade-offs, opt-in design correct, sister-spec separation justified), but the reference implementation has material gaps that must be closed before merge.

**Decision**: Apply all fixes except M1 and M11 (accepted as no-action). Total 22 fixes to apply across 7 files + 1 new eval.

## Convergence Tracking

Findings fingerprint (for diff against Round 2):

```
CRIT: C1, C2
IMP:  I1, I2, I3, I4, I5, I6, I7, I8, I9, I10, I11
MIN:  M2, M3, M4, M5, M6, M7, M8, M9, M10
```

Round 2 expectation: all 22 findings resolved → 0 findings. But per `feedback_premerge_iteration_pattern`, need Round 3 stability confirmation before declaring convergence.
