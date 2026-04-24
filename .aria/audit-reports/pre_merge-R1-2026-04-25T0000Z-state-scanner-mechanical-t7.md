---
checkpoint: pre_merge
spec: state-scanner-mechanical-enforcement
task_group: T7.0+T7.1+T7.2
round: R1
timestamp: 2026-04-25T00:00Z
verdict: MERGE_WITH_FIXES
converged: true
agents:
  - aria:code-reviewer
---

# Pre_merge R1 — T7 canonical normalizer + snapshot stability

**Scope**: aria PR #26 (1a875d5): 4 new files +1305 行
**Mode**: 1 agent × 1 round (Level 2 doc+code, proportionate)

## Phase 1: Spec Compliance
- T7.0 doc covers CF-2 (sort/float/null/timestamp): PASS
- T7.0 code 10 rules: PASS_WITH_WARNING → RESOLVED (IF-1 fixed)
- T7.1 baseline: PASS_WITH_WARNING (不 wired 到 auto test, doc 已澄清 manual-compare)
- T7.2 stability test: PASS (live dogfood DIFF_EXIT=0)
- Reframe (v2.9 → v3.0 stability): PASS (doc §reframe + commit message + tasks.md 注记)

## Phase 2: Code Quality
- Tests pass: PASS (215/215, 1.6s)
- Stdlib-only: PASS (AD-SSME-1 aligned)
- Baseline hygiene: PASS (0 absolute paths 泄漏, 0 full SHA, 0 wall-clock)
- Refresh workflow: PASS (doc 明确)

## Phase 3: Hazards
- Rule 5 SHA 40-char anchor: PASS (无 URL/content 误伤)
- Rule 2 abs path (conservative prefix): PASS (零 false-positive)
- Test flake: PASS (tempdir 隔离, 无网络/并发)
- Baseline private info: PASS (仅 public hostname forgejo.10cg.pub)

## Findings Resolved in this Round
- IF-1 Rule 2 spec↔code divergence: RESOLVED 同 session (doc 收紧到 prefix-only + 移除 dead `_ABS_PATH_RE` 常量 + 增补 conservative rationale)
- MN-1 fixture filename drift (`reference-snapshot.json` → `reference-snapshot-aria.json`): RESOLVED 同 session
- MN-2 consumer filename drift (`test_snapshot_stability.py` → `test_normalize_snapshot.py::TestStabilityIntegration`): RESOLVED 同 session

## Findings Deferred
- MN-3 baseline 未被自动 test 消费: doc §Consumers 已澄清 (manual-compare reference); 未来 T8/T10 可以加 `test_live_scan_matches_committed_baseline` wiring

## Verdict
**MERGE_WITH_FIXES** — 1 Important + 2 Minor doc drift 全部同 session 修复, 215 tests 绿, T7.2 live dogfood DIFF_EXIT=0 充分证明机械断言满足.
