# ai-native-estimator — Rule #6 deterministic structural substitute (#18 v1)

> internal data-layer 逻辑, 不适用 LLM AB (per `feedback_deterministic_structural_skill_rule6_substitute`)。
> Rule #6 由确定性单测 + inline fixtures 替代 with/without AB。

## 测试套件 (39 deterministic tests, 0 LLM)

| 文件 | tests | 覆盖 |
|------|-------|------|
| `aria/skills/ai-native-estimator/tests/test_estimator.py` | 20 | capture 增量/空区间幂等/uuid-miss fallback/wall_clock 派生+null/raw 全存/no-transcript skip/enabled:false/spec_level null + forecast 3 态(uncalibrated 断言)/cross-level 隔离/forecast(None)/velocity window+空/forecast 不含 wall_clock + portability |
| `aria/skills/aria-token-telemetry/tests/test_token_telemetry.py` | 19 | 15 existing (zero regression) + 4 new `iter_transcript_usage` (per-turn meta / skip-corrupt / missing-file / null-timestamp) |

## fixture 策略

测试用 inline temp transcript (`_turn()` helper 生成含 uuid/timestamp/sessionId 的 JSONL) +
temp project root + 直接 variance 写入 (forecast unit-isolation)。覆盖错误路径:
partial transcript / null timestamp / empty+missing variance / mixed-level / session 切换 (uuid-miss)。

## 11 Success Criteria ↔ test 映射

全部 11 条 proposal Success Criteria 均有对应 test (见 test_estimator.py 类/方法名)。
NEW-C-1 (empty-range 幂等) 实证: `test_idempotent_empty_range_skip` + live smoke (capture #2 → skipped, variance count=1)。

## 运行

```bash
python3 aria/skills/ai-native-estimator/tests/test_estimator.py
python3 aria/skills/aria-token-telemetry/tests/test_token_telemetry.py
```

## post_spec audit

CONVERGED R1 (3/3 REVISE, 3 convergent Critical) → Rev1 → R2 (2 PWW + 1 NEW Critical:
cycle_id idempotency) → Rev2 → R3 (2/2 PWW, 0 new Critical)。详见 proposal Rev1/Rev2 changelog。
