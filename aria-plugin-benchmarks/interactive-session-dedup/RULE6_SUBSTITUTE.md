# Rule #6 Substitute — Interactive Session Dedup (TASK-018)

> **Spec**: `openspec/changes/interactive-session-dedup-coordination` (DEC-20260704-002)
> **Skill type**: deterministic / structural (a git-backed coordination gate),
> NOT a capability skill. Per `feedback_rule6_framing_differs_by_skill_type` +
> `feedback_deterministic_structural_skill_rule6_substitute`, the Rule #6
> obligation is satisfied by **structural fixtures + unit tests + runtime-invocation
> probe + dogfood**, NOT by an LLM with/without AB comparison.

## Why not with/without AB

Rule #6's LLM with/without AB answers "does the Skill improve output *quality*".
That question is meaningful for capability skills (the model reasons differently
with the skill loaded). The dedup gate is **deterministic mechanism code**:
`run_gate` produces the same GateResult for the same claim state regardless of
any model. There is no "quality delta" to measure — there is only **"does the
wired mechanism actually run in production, and does it behave correctly"**. That
is exactly what structural tests + a runtime probe assert.

This mirrors the substitute already accepted for collector/parser/detector-class
skills (state-scanner collectors, audit-engine determinism).

## Structural test evidence (all green)

| concern | test artifact | what it locks |
|---------|---------------|---------------|
| advisory outcome mapping (occupied / clock_skew / push_fail → proceed + write claim + surface) | `aria/skills/state-scanner/tests/test_phase1_gate_advisory.py` (10) | TASK-003 — first-ever direct run_gate test |
| block-mode preserved; default-mode = advisory (flip lock) | same file, `TestDefaultModeLockIn` | TASK-005(f) `feedback_default_value_flip_needs_lock_in_test` |
| CLI stitch (argparse → run_gate → JSON contract) | same file, `TestCliStitch` | TASK-002 — the编排层↔run_gate coupling point |
| telemetry partition anti-spoof (harness/library NEVER touch production partition) | `tests/test_phase1_gate_telemetry.py` (10) | TASK-011/012 — R2-Major-C structural anti-spoof |
| probe reads only production partition; ignores harness/library records | same file, `TestCoordinationProbe` | TASK-012 — #95 anti-dead-code |
| §6 carry-id doesn't degrade frontmatter; carry-id normalization; per-container identity | `tests/test_dedup_backcompat.py` (6) | TASK-010 — back-compat |
| synthetic dual-session collision detection + falsifiable control arm | `aria-plugin-benchmarks/interactive-session-dedup/dedup_harness.py` | TASK-013 — control arm misses 20/20 (falsifiable) |

## Runtime-invocation probe (the part a test cannot fake)

Structural tests prove the mechanism *can* behave correctly. They do NOT prove it
is *actually invoked in production* — the exact gap that turned the mother-spec's
Layer L into dead code (aria-plugin #95). The **runtime probe**
(`coordination_probe.py`, wired as the `coordination-gate-invocation`
custom-check) closes that gap: it asserts the *production* telemetry partition has
≥1 `source=production` record. A test cannot satisfy it — only a real CLI
invocation (source="production") can, and the anti-spoof partition guarantees
harness/library calls cannot forge it.

This is the load-bearing difference from "勾选完成 ≠ 运行现实": the probe flips to
FAIL if the wired gate ever silently stops being called.

## Human review checkpoint

- [ ] Owner confirms the structural test suite (32 dedicated tests, all green) is
      the accepted Rule #6 evidence for this deterministic skill.
- [ ] Owner confirms the runtime probe is the accepted anti-dead-code guarantee
      (dogfood TASK-019 supplies the first production record).

> No `/skill-creator` with/without AB run is required or meaningful here (Rule #6
> is satisfied by the structural + runtime substitute above). Recording this
> explicitly per Rule #6's "不需要 OpenSpec / 验证活动" note — running these tests
> is a verification activity, not a spec change.
