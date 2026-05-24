# Rule #6 Substitute — Submodule Pointer Regression Gate Structural Benchmark

> **Type**: Deterministic structural Skill — Rule #6 substitute (per `feedback_deterministic_structural_skill_rule6_substitute`)
> **NOT for LLM AB testing** via `/skill-creator` (wrong instrument for deterministic git plumbing)
> **Spec**: `openspec/changes/aria-submodule-pointer-regression-gate/proposal.md` (Approved 2026-05-24)
> **Created**: 2026-05-24 as part of Phase B

---

## Why structural substitute and not LLM AB?

Rule #6 normally requires `/skill-creator benchmark` AB comparison of Skill with vs without LLM gates. But this Skill (Phase C.2.4.5 submodule pointer regression gate) is **purely deterministic** — git plumbing + `merge-base --is-ancestor` exit codes. There is no LLM judgment in the loop. LLM AB would measure noise, not signal.

Per `feedback_deterministic_structural_skill_rule6_substitute` memory, the substitute for deterministic Skills is:
1. **Structural fixture README** (this file)
2. **Unit tests covering known failure modes** (`aria/skills/phase-c-integrator/tests/test_submodule_gate.sh`)
3. **Dogfood evidence** (deliberate regression PR validated by real gate run, captured below)
4. **Atomicity guard test** (race scenario coverage in test suite scenario 9)

This substitute pattern was used in v1.24.0 (aria-secret-guard) and v1.23.0 (state-scanner-status-extraction) and is established Aria precedent.

---

## Structural fixtures

### 10 replay scenarios (test_submodule_gate.sh)

| # | Scenario | Expected verdict | Asserts |
|---|----------|------------------|---------|
| 1 | Happy path forward bump | PASS (exit 0) | "forward bump" in output |
| 2 | Pure regression (block mode) | BLOCK (exit 1) | "REGRESSION" + "submodule=" + SHAs in stderr |
| 2 | Pure regression (warn mode) | warn (exit 0) | "WOULD-BLOCK" in stderr + telemetry append |
| 3 | Divergent history | BLOCK (exit 1) | "DIVERGENT" + NOT "REGRESSION" |
| 4 | Stale-ref fetch recovery (clean) | PASS (exit 0) | mandatory fetch refreshes ref |
| 4 | Stale-ref fetch failure | BLOCK (exit 2) | "BLOCK: git fetch origin failed" |
| 5 | Legitimate revert with valid trailer | ALLOW (exit 0) | "ALLOW" + "overridden by per-PR marker" + audit log |
| 5 | Mismatched SHAs in trailer | BLOCK (exit 1) | trailer rejected, gate blocks |
| 6 | No-change (same pointer) | PASS (exit 0) | "unchanged" in output |
| 7 | First-time submodule (nil-SHA) — **CRITICAL** | PASS (exit 0) | "first introduced" INFO log |
| 8 | Submodule removed from feature | PASS (exit 0) | gate exits 0 (no .gitmodules entry) |
| 9 | Concurrent force-push race | BLOCK (exit 3) | "origin/master rewritten" detected via refspec assertion |
| 10 | Detached HEAD submodule | PASS (exit 0) | ancestry check works on raw SHAs |

**Verdict**: 13 assertions across 10 scenarios. All must PASS for Phase B exit.

### Atomicity guard (race scenario 9)

Scenario 9 specifically tests the race where `origin/master` is force-pushed BETWEEN the gate's BEFORE-fetch rev-parse and AFTER-fetch rev-parse. The deterministic pre-stage approach (rather than real concurrency) validates the refspec assertion's detection logic without flakiness. Per backend-architect R3 NEW finding + qa R3 N-qa-1 trade-off documentation.

---

## Dogfood evidence

### Local run 2026-05-24 (Phase B execution)

```
$ bash aria/skills/phase-c-integrator/tests/test_submodule_gate.sh
... [scenarios 1-10 executed] ...
════════════════════════════════════════════════════════════
  Results: 13 PASS / 0 FAIL / 0 skipped
════════════════════════════════════════════════════════════
```

13/13 assertions PASS at v1.28.0 ship time. No false positives in fixture suite.

### Real-world PR validation (deferred to Phase C dogfood)

The gate ships in v1.28.0 warn-only mode. The 14-day observation window collects telemetry from real PR merges to:
1. Validate zero false-positive rate on legitimate forward bumps
2. Surface any edge cases not covered by the 10 fixture scenarios
3. Inform v1.29.0 block-mode flip decision per Spec §What E

Telemetry file paths:
- `aria/metrics/submodule-gate-warns.jsonl` — WOULD-BLOCK events in warn mode
- `aria/metrics/submodule-gate-blocks.jsonl` — BLOCK events in block mode (post v1.29.0)
- `aria/metrics/submodule-gate-overrides.jsonl` — override usage (trailer or label)
- `aria/metrics/submodule-gate-misses.jsonl` — tripwire detections (post-merge regressions that escaped gate)

---

## Why this fits Aria methodology

- **Rule #6**: deterministic substitute documented + validated
- **Rule #8 pattern**: extends pre-merge gate (Rule #8 is `aether ci status`; this is submodule pointer ancestry)
- **向后兼容**: 2-phase rollout warn → block honors backward compat
- **小步迭代**: 9.8h Phase B with per-task granularity ~0.1-3.5h

---

## Cross-references

- Spec proposal: `openspec/changes/aria-submodule-pointer-regression-gate/proposal.md`
- Spec tasks: `openspec/changes/aria-submodule-pointer-regression-gate/tasks.md`
- Gate implementation: `aria/skills/phase-c-integrator/SKILL.md §C.2.4.5`
- Gate helper script: `aria/skills/phase-c-integrator/scripts/submodule_gate.sh`
- Replay tests: `aria/skills/phase-c-integrator/tests/test_submodule_gate.sh`
- Convention doc: `standards/conventions/submodule-pointer-hygiene.md`
- Tripwire workflow: `.forgejo/workflows/submodule-gate-tripwire.yml`
- Memory: `feedback_deterministic_structural_skill_rule6_substitute`
- DEC: `.aria/decisions/2026-05-24-aria-124-submodule-pointer-regression-gate.md`
- Forgejo issue: Aria #124
