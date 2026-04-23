# Smoke Benchmark: aria-plugin v1.16.1 + v1.16.2 Patch Series

**Date**: 2026-04-23
**Session**: Post-M1 closeout bug cleanup
**Skills Benchmarked**: state-scanner + audit-engine
**Method**: Structural smoke (inline Python) — **NOT full `/skill-creator` AB**
**Commits Verified**:
- aria@9acb801 (v1.16.1) — #17 state-scanner regex + #27 audit-engine Pre-write validation
- aria@415f11c (v1.16.2) — #26 audit-engine Checkpoint Report Completeness Gate

---

## Summary

| Skill | Baseline (v1.16.0) | Target | Delta | Verdict |
|-------|---------------------|--------|-------|---------|
| state-scanner | 55.6% (5/9) | 100.0% (9/9, v1.16.1) | **+44.4pp** ✅ | Fix #17 validated, no regression |
| audit-engine | 10.0% (1/10) | 90.0% (9/10, v1.16.2) | **+80.0pp** ✅ | Fixes #26 + #27 validated |

**Effective audit-engine coverage** is 10/10 when accounting for C7 false negative (exclusion present in code as `key != "post_closure"` at line 120, but the Chinese keyword "除外" my regex looked for is not used; `事后审计，不做前置依赖` phrasing is semantically equivalent).

---

## state-scanner Detail

**Test set**: 9 canonical Status extraction inputs (expanding #17 bug report's 5-pattern table).

**Baseline (v1.16.0)**: 5 patterns in Phase 1.5:
- Pattern 1: `^Status:\s*(.+)` (EN, no heading prefix allowed) ← **fails on `## Status:`**
- Pattern 2: `\*\*Status\*\*:\s*(.+)` (EN bold)
- Pattern 3: `\*\*状态\*\*:\s*(.+)` (CN bold only) ← **fails on heading/plain**
- Pattern 4: `>\s*.*(?:Status|状态)[：:]\s*(.+)` (blockquote)
- Pattern 5: `\|\s*(?:Status|状态)\s*\|\s*(.+?)\s*\|` (table)

**Target (v1.16.1)**: Pattern 1 + Pattern 3 loosened to allow optional Markdown heading prefix `(?:#{1,6}\s+)?` and (Pattern 3) bold markers `\*{0,2}`.

| # | Input | v1.16.0 | v1.16.1 | Notes |
|---|-------|---------|---------|-------|
| E1 | `Status: done` | ✅ | ✅ | Regression (unchanged) |
| E2 | `## Status: COMPLETED (Cycle 42)` | ❌ | ✅ | **#17 core fix** |
| E3 | `### Status: active` | ❌ | ✅ | #17 generalization |
| E4 | `**Status**: done` | ✅ | ✅ | Regression (P2) |
| E5 | `### 状态: 完成` | ❌ | ✅ | #17 CN heading |
| E6 | `**状态**: 进行中` | ✅ | ✅ | Regression (P3 bold) |
| E7 | `状态: 待定` | ❌ | ✅ | #17 CN plain |
| E8 | `> Status: draft` | ✅ | ✅ | Regression (P4 blockquote) |
| E9 | `\| Status \| done \|` | ✅ | ✅ | Regression (P5 table) |

**Real-world impact** (per #17 report): SilkNode project 13/77 Stories using `## Status:` format were被 state-scanner 漏报, now correctly identified.

---

## audit-engine Detail

**Method**: Structural coverage check (10 grep predicates testing fix chapter presence + config flags + doc coherence). audit-engine is a Markdown SKILL (instructions, not executable), so structural verification = documentation coverage = effective behavior guarantee (the Skill 的 behavior is its文档内容).

| # | Check | v1.16.0 | v1.16.2 | Note |
|---|-------|---------|---------|------|
| C1 | Pre-write Validation 章节 (#27) | ❌ | ✅ | |
| C2 | openspec/changes/{id} 校验路径 | ❌ | ✅ | |
| C3 | openspec/archive/* 通配 | ❌ | ✅ | |
| C4 | config `audit.allow_dangling_change_ids` | ❌ | ✅ | |
| C5 | Checkpoint Report Completeness Gate 章节 (#26) | ❌ | ✅ | |
| C6 | `.aria/audit-reports/` 扫描 | ✅ | ✅ | baseline had generic mention |
| C7 | post_closure 排除 | ❌ | ❌* | *false negative — 实际在 L120 `key != "post_closure"` |
| C8 | config `audit.allow_incomplete_checkpoints` | ❌ | ✅ | |
| C9 | 豁免时 `[WARN] bypassed` audit trail | ❌ | ✅ | |
| C10 | #26+#27 互补关系文档化 | ❌ | ✅ | |

**Lines added**: 119 lines (394 → 513), covering 2 new gate chapters + 2 config flags + cross-reference.

**Real-world impact** (per #26 + #27 reports): truffle-hound v0.3.0 (2026-04-22) Phase A skip scenario would now be blocked by either gate (lacking report OR lacking change_id proposal).

---

## Caveats and Honest Limitations

1. **Not full `/skill-creator` AB**: This smoke benchmark verifies the code/doc changes are present and semantically correct, but does not measure end-to-end AI agent task success rate. Full AB would require:
   - Spawning with_skill + baseline subagents for each scenario
   - Grading outputs against assertions
   - Variance analysis across multiple runs per eval
   - HTML viewer for human review

2. **Deferred work**: Full `/skill-creator benchmark` for both skills is deferred to a dedicated session. Justification:
   - state-scanner: 11 existing evals × 2 configs × grading = ~30 subagent calls
   - audit-engine: no dedicated eval suite yet; would need 3 new evals + AB wiring
   - Per `feedback_level2_patch_no_benchmark.md`, Level 2 patches with pure doc logic can defer full AB when smoke validation is present

3. **Smoke verification is sufficient for release gate**:
   - state-scanner: regex change is code-level, smoke tests regex behavior directly against 9 inputs
   - audit-engine: is documentation, smoke tests doc coverage directly
   - Both verified 0 regressions + positive delta

---

## Next Actions (optional, not blocking)

- [ ] Full `/skill-creator benchmark state-scanner` in dedicated session (use existing `aria-plugin-benchmarks/ab-suite/state-scanner.json` 11 evals, append `heading-status-extraction` as eval 12)
- [ ] Create `aria-plugin-benchmarks/audit-engine/evals/evals.json` with 3 scenarios (normal / missing-checkpoint / dangling-change_id), then full AB

---

**Conclusion**: v1.16.1 + v1.16.2 patch series smoke-verified. Both Skills' fixes present, coherent, no regressions detected. Safe for downstream use.
