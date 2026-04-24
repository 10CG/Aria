# Smoke Benchmark: aria-plugin v1.17.0

**Date**: 2026-04-25
**Session**: state-scanner-mechanical-enforcement Spec closeout (T10 release gate)
**Scope**: state-scanner v2.10.1 → v3.0.0 (mechanical mode)
**Method**: Structural smoke (deterministic Python assertions) — Full `/skill-creator` AB **deferred** (see §"Why smoke not full AB" below)

**Commits going into v1.17.0**:
- aria@1a875d5 (PR #20+#21+#22+#23+#24+#25+#26 — 6 partial merges of state-scanner-mechanical Spec T1-T7+T9.1-T9.2)
- main@eb8d042 (submodule pointer + R1-M1 cleanup + audit reports for each PR)

---

## Summary

| Metric | Result |
|---|---|
| ab-suite/state-scanner.json eval cases covered | 11 / 11 |
| Structural assertions passed | **35 / 35 (100%)** |
| Schema version | `1.0` (snapshot_schema_version) |
| scan.py exit code | 0 (clean) |
| Test suite (T6) | 215 / 215 passed (1.6s) |
| T7 stability dogfood | DIFF_EXIT=0 (two consecutive scan.py runs byte-identical post-normalize) |

**Verdict**: PASS — release gate satisfied via mechanical evidence; full `/skill-creator` AB scheduled as v1.17.x post-release validation.

---

## Per-eval breakdown

| ID | Eval | Pass | Total | Status |
|----|------|------|-------|--------|
| 1  | basic-state-collection | 4 | 4 | 100% ✅ |
| 2  | user-options-display | 2 | 2 | 100% ✅ |
| 3  | readme-sync-detection | 4 | 4 | 100% ✅ |
| 4  | config-awareness | 2 | 2 | 100% ✅ |
| 5  | submodule-sync-detection | 5 | 5 | 100% ✅ |
| 6  | upstream-behind-detection | 3 | 3 | 100% ✅ |
| 7  | issue-awareness-opt-in | 4 | 4 | 100% ✅ |
| 8  | readme-skill-count-badge | 2 | 2 | 100% ✅ |
| 9  | forgejo-config-detection | 3 | 3 | 100% ✅ |
| 10 | multi-remote-parity-drift | 3 | 3 | 100% ✅ |
| 11 | submodule-push-github-sync-miss | 3 | 3 | 100% ✅ |

Raw assertion log: `state-scanner/smoke-results.json`.

---

## Why smoke not full AB

Per `feedback_smoke_vs_full_ab_benchmark.md` and v1.16.2/3/4 precedent, smoke benchmark is acceptable when:

1. The Skill change is doc-dominant (SKILL.md is the AI contract surface)
2. Stronger mechanical evidence exists than typical AB would produce
3. Field-level correctness is testable structurally without LLM stochasticity

For v1.17.0 state-scanner v3.0:

- **Doc-dominant**: SKILL.md was reduced 1178 → 454 lines, prose contract migrated to schema.md (T5). All 17 top-level snapshot keys are versioned at `snapshot_schema_version=1.0`.
- **Stronger evidence**: 215 unit tests (T6) + live DIFF_EXIT=0 (T7.2) + 8 successful merge cycles with audits across 6 partial PRs. AB benchmark would re-test what the mechanical evidence already proves: scan.py outputs deterministic, schema-consistent fields.
- **Field-level testable**: 35 structural assertions exercise every `expectations[]` clause from the 11 ab-suite eval cases without requiring LLM invocation.

**Caveat**: Smoke benchmark cannot validate description-triggering accuracy or AI prose-path quality on the opt-out branch (`mechanical_mode=false`). These are deferred:

- **Description triggering**: covered by `/skill-creator` benchmark in any future session (post-release validation; not blocking v1.17.0)
- **Opt-out prose path quality**: opt-out flag is documented as transitional (removed v1.18.0 per AD-SSME-5); zero-usage observability over v1.17.x cycle is the green-light signal for removal

---

## v1.17.0 Release Contents

### Skill changes (state-scanner v3.0.0)
- **Step 0 hard constraint**: `python3 scan.py` is now the only legitimate Phase 1 data path
- **17 top-level snapshot keys** at `snapshot_schema_version=1.0`
- **Exit code contract**: 0 (ok) / 10 (soft) / 20 (hard precondition) / 30 (uncaught)
- **D1-D5 intentional divergences** (Approved/Reviewed/TBD-rejection/block-scalar/Active preservation)
- **Opt-out** `state_scanner.mechanical_mode=false` (AI-prose contract, not runtime switch) — removed v1.18.0

### Infrastructure
- 17 collectors under `scripts/collectors/` (stdlib-only)
- `scripts/normalize_snapshot.py` (T7.0 canonical normalizer, 10 rules)
- `scripts/validate_schema_doc.py` (live ↔ schema.md consistency)
- `tests/run_tests.py` + 215 stdlib unittest tests
- `references/state-snapshot-schema.md` (source-of-truth, 18 documented keys)
- `references/json-diff-normalizer.md` (canonical projection spec)
- `references/migration-v2.9-to-v3.0.md` (upgrade + rollback guide)
- `tests/fixtures/reference-snapshot-aria.json` (golden baseline)

### Spec closure
- `state-scanner-mechanical-enforcement` Spec: 39 tasks done, 5 deferred to T6.5-followup or T8 (cross-project / coverage)
- Spec status remains Approved through v1.17.0 cycle; archive triggered when all post-merge action items close

---

## Post-release validation (T8 + T6.5-followup)

These do not block v1.17.0:

- **T8 Kairos cross-project**: run scan.py on Kairos (TypeScript/Node project), verify field collection works across non-Aria stacks
- **T6.5-followup**: subprocess mocking layer to lift sync (18%) / multi_remote (33%) / issue_scan (44%) coverage to ≥70%
- **Full `/skill-creator` AB**: dedicated benchmark session against v1.16.4 → v1.17.0 to capture description-trigger accuracy delta

---

## References

- ab-suite: `aria-plugin-benchmarks/ab-suite/state-scanner.json` (v1.4.0, 11 evals)
- T6 test suite: `aria/skills/state-scanner/tests/` (215 tests)
- T7 stability: `aria/skills/state-scanner/tests/test_normalize_snapshot.py::TestStabilityIntegration`
- Spec: `openspec/changes/state-scanner-mechanical-enforcement/`
- Audit reports: `.aria/audit-reports/pre_merge-*-state-scanner-mechanical-*.md` (8 reports across T1-T9)
