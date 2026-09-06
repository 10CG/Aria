# Rule #6 substitute 台账 — owner-container-identity-key-and-collision-parser (TASK-031 汇总)

> 改前基线: aria 7dd0135 (v1.69.1) | 采集 2026-09-06T07:18:32Z | 跑法 (a) run_tests.py 全套 TestCase / (b) pytest tests/test_collision.py

## RED (改前, 7dd0135 + 新测试)

### (b) pytest tests/test_collision.py
```
FAILED tests/test_collision.py::test_split_owner_container_variants - Asserti...
FAILED tests/test_collision.py::test_arm_same_container_two_owners_is_none - ...
FAILED tests/test_collision.py::test_arm_two_people_two_machines_is_cross_owner
FAILED tests/test_collision.py::test_arm_same_person_two_machines_is_self_multi_container
FAILED tests/test_collision.py::test_arm_drift_without_cooccurrence_is_cross_owner
FAILED tests/test_collision.py::test_advisory_same_container_two_owners_yields_exactly_one
FAILED tests/test_collision.py::test_advisory_three_owners_same_uuid_lists_three
FAILED tests/test_collision.py::test_advisory_ignores_legacy_unknown_and_hostname_containers
FAILED tests/test_collision.py::test_advisory_no_input_is_empty_list - Attrib...
FAILED tests/test_collision.py::test_family_key_two_uuid_suffixed_tracks_collide
FAILED tests/test_collision.py::test_family_key_strip_rules - AssertionError:...
FAILED tests/test_collision.py::test_real_collector_emits_cross_owner_collision
FAILED tests/test_collision.py::test_real_collector_no_collision_is_none - As...
13 failed, 15 passed in 0.72s
```

### (a) unittest tests.test_handoff_multibranch_collision_dedupe
```
FAIL: test_owner_segment_participates_in_grouping_key (tests.test_handoff_multibranch_collision_dedupe.TestDedupeRound3Residuals.test_owner_segment_participates_in_grouping_key)
FAIL: test_both_latest_active_same_owner_is_self_multi_container (tests.test_handoff_multibranch_collision_dedupe.TestSelfMultiContainerRealCollisionSurvivesDedupe.test_both_latest_active_same_owner_is_self_multi_container)
FAIL: test_both_latest_active_still_reports_self_multi_container (tests.test_handoff_multibranch_collision_dedupe.TestSelfMultiContainerRealCollisionSurvivesDedupe.test_both_latest_active_still_reports_self_multi_container)
FAIL: test_advisory_wired_before_dedupe_same_track_two_owner_strings (tests.test_handoff_multibranch_collision_dedupe.TestTwoPartBoardEchoAndAdvisoryWiring.test_advisory_wired_before_dedupe_same_track_two_owner_strings)
FAIL: test_board_echoes_original_two_part_strings (tests.test_handoff_multibranch_collision_dedupe.TestTwoPartBoardEchoAndAdvisoryWiring.test_board_echoes_original_two_part_strings)
FAIL: test_real_two_part_two_people_two_machines_is_cross_owner (tests.test_handoff_multibranch_collision_dedupe.TestTwoPartBoardEchoAndAdvisoryWiring.test_real_two_part_two_people_two_machines_is_cross_owner)
Ran 21 tests in 0.800s
FAILED (failures=6)
```

映射: SC-1 ← test_split_owner_container_variants · SC-2 判定臂 ← test_arm_* (zero_segment / unknown_owner 两条改前即绿, 为 lock-in) · SC-2 advisory ← test_advisory_* · SC-2 族键 ← test_family_key_* · SC-8 ← test_real_collector_* keys · SC-4 ← test_owner_segment_participates_in_grouping_key (A 臂红) / test_both_latest_active_* / test_board_echoes_original_two_part_strings · SC-2 端到端 ← test_advisory_wired_before_dedupe_* / test_real_two_part_two_people_*

### (a) unittest tests.test_collision_frozen_corpus tests.test_track_board_advisories (TASK-006 / TASK-004 / TASK-019)
```
ERROR: test_collision_frozen_corpus (unittest.loader._FailedTest.test_collision_frozen_corpus)
ImportError: cannot import name 'LAYER_H_ACTIVE_WINDOW_DAYS' from 'lib.constants' (/home/dev/Aria/aria/skills/state-scanner/lib/constants.py)
ERROR: test_counterfactual_deduped_rows_yield_zero_advisories (tests.test_track_board_advisories.TestAdvisoryRendering.test_counterfactual_deduped_rows_yield_ze
AttributeError: module 'lib.collision' has no attribute 'identity_drift_advisories'
FAIL: test_fixture_renders_exactly_two_advisory_lines (tests.test_track_board_advisories.TestAdvisoryRendering.test_fixture_renders_exactly_two_advisory_lines)
AssertionError: 0 != 2 : e    D.3    2026-05-20    107d ago  🔴 abandoned? 可接管
Ran 6 tests in 0.033s
FAILED (failures=1, errors=2)
```
映射: SC-6/SC-11 ← test_collision_frozen_corpus (整模块 ImportError: LAYER_H_ACTIVE_WINDOW_DAYS 不存在) · SC-10 ← test_fixture_renders_exactly_two_advisory_lines (0≠2) / test_counterfactual_* (AttributeError) · SC-8 容错两条改前即绿 (lock-in)

### (a) unittest tests.test_identity_label tests.test_migration_inventory (TASK-008)
```
ERROR: test_identity_label (unittest.loader._FailedTest.test_identity_label)
ImportError: cannot import name 'get_container_label' from 'lib.identity' (/home/dev/Aria/aria/skills/state-scanner/lib/identity.py)
ERROR: test_migration_inventory (unittest.loader._FailedTest.test_migration_inventory)
ImportError: cannot import name 'label_migration_inventory' from 'lib.claim_lifecycle' (/home/dev/Aria/aria/skills/state-scanner/lib/claim_lifecycle.py)
Ran 2 tests in 0.002s
FAILED (errors=2)
```
映射: SC-3 S1 臂 ← test_identity_label (ImportError: get_container_label) · SC-3 共同臂 ← test_migration_inventory (ImportError: label_migration_inventory)

## GREEN (改后, aria feature 分支, 2026-09-06T07:32:47Z)
```
(b) pytest tests/test_collision.py: 28 passed in 0.45s
(a) run_tests.py: Ran 1505 tests in 111.166s OK OK (1 recent production run_gate invocation(s) recorded) OK (coordination gate disabled) 
phase-d-closer test_fetch_gate.py (pytest 风格): 11 passed in 0.02s
session-closer run_tests.py: Ran 74 tests OK
```
语料归因表 (2026-09-05 fixture, 无窗口 2 组): [simonfish/dev-claude, simonfish/dev-claude2] @ aria-2-0-m5-replay-reconciler-drift-review-loop-audit (2026-05-20/23) → stale(#182); [dev-claude, simonfishgit/dev-claude] @ aria-submodule-gate-block-flip (2026-05-25/28) → stale(#182); 有窗口 → 0 组; 注入 2026-09-05 合成组 → true-collision。

## 提交落点
- aria feature/owner-container-identity-key-and-collision-parser: 4603fcc (组 1 RED) → 5fbb974 (组 2 impl, GREEN) → f2e4231 (组 3 docs + fetch_gate 断言)
- standards feature/owner-container-identity-key-and-collision-parser: c955783 (§2.3.1 / §2.3.5 / §2.3.9)
- fixture 公开性 (5.4 / TASK-037): 八字段扫描 emails 0 / tokens 0 / 内网 IP 0 / /home/ 0 (见 freeze 时输出)
