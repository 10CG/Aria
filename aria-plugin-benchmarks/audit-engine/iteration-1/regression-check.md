# Backward Compatibility Regression Check

> **Date**: 2026-03-27
> **Scope**: Phase Skills modified for audit-engine integration
> **Type**: Code review (not AB benchmark)
> **Verdict**: 7 PASS / 1 CONDITIONAL PASS

---

## Summary

| # | Skill | Version | audit.enabled=false guard | Existing steps unmodified | allowed-tools updated | No breaking output changes | Verdict |
|---|-------|---------|:------------------------:|:------------------------:|:---------------------:|:--------------------------:|:-------:|
| 1 | phase-a-planner | 1.1.0 | PASS | PASS | PASS | PASS | **PASS** |
| 2 | phase-b-developer | 1.4.0 | PASS | PASS | PASS | PASS | **PASS** |
| 3 | phase-c-integrator | 1.2.0 | PASS | PASS | PASS | PASS | **PASS** |
| 4 | phase-d-closer | 1.0.0 | PASS | PASS | N/A | PASS | **PASS** |
| 5 | brainstorm | 2.0.0 | PASS | PASS | N/A | PASS | **PASS** |
| 6 | task-planner | 2.0.0 | PASS | PASS | N/A | PASS | **PASS** |
| 7 | state-scanner | 2.7.0 | PASS | PASS | PASS | PASS | **PASS** |
| 8 | config-loader | 1.0.0 | PASS | PASS | N/A | PASS | **COND. PASS** |

---

## Detailed Analysis

### 1. phase-a-planner/SKILL.md (v1.1.0) -- PASS

**audit.enabled=false guard**: PASS
- Line 158-160: Explicit guard `audit.enabled == true AND checkpoints.post_spec != "off"` as condition for `A.post` block.
- Line 170: `backward_compat` section explicitly states: `audit.enabled=false: 完全跳过，Phase A 行为与之前完全相同`.

**Existing steps unmodified**: PASS
- Original steps A.1, A.2, A.3 (lines 63-99) are untouched.
- Audit block is added as a new section `A.post` (lines 147-182), positioned between A.1 completion and A.2 execution. It does not modify the existing A.1/A.2/A.3 step definitions.

**allowed-tools**: PASS
- Frontmatter (line 9): `allowed-tools: Read, Write, Glob, Grep, Task, Skill`. `Skill` tool is present, which is needed to call audit-engine.

**No breaking output changes**: PASS
- Core output format (lines 103-120) is unchanged.
- Audit fields (`audit_verdict`, `audit_report`) are only emitted when audit is enabled (lines 180-181). When disabled, output schema is identical to pre-integration.

---

### 2. phase-b-developer/SKILL.md (v1.4.0) -- PASS

**audit.enabled=false guard**: PASS
- Configuration table (lines 41-43): `audit.enabled` defaults to `false`.
- Line 46: Trigger condition explicitly requires `audit.enabled=true` AND checkpoint != `"off"`.
- `B.mid` block (lines 124-152): Condition at line 127-128: `audit.enabled == true AND audit.checkpoints.mid_implementation != "off"`.
- `B.post` block (lines 157-190): Condition at line 162: `audit.enabled == true AND checkpoints.post_implementation != "off"`.
- Line 177: `backward_compat` section: `audit.enabled=false: 完全跳过，Phase B 行为与之前完全相同`.
- Legacy compat (line 178-179): Old `experiments.agent_team_audit` mapped by audit-engine internally.

**Existing steps unmodified**: PASS
- B.1 (lines 83-92), B.2 (lines 94-107), B.3 (lines 109-118) are unchanged from pre-audit versions.
- Audit blocks `B.mid` and `B.post` are additive-only sections.

**allowed-tools**: PASS
- Frontmatter (line 10): `allowed-tools: Bash, Read, Write, Glob, Grep, Task, Skill`. `Skill` tool present.

**No breaking output changes**: PASS
- Core output (lines 194-213) is unchanged.
- Audit fields only appear when audit is enabled. When `audit.enabled=false`, the output structure is identical to v1.2.0/v1.3.0.

---

### 3. phase-c-integrator/SKILL.md (v1.2.0) -- PASS

**audit.enabled=false guard**: PASS
- Configuration table (lines 40-43): `audit.enabled` defaults to `false`.
- Line 119: Guard condition: `audit.enabled — false 则跳过，保持现有行为不变`.
- Line 129: `backward_compat` section: `audit.enabled=false: 完全跳过，Phase C 行为与之前完全相同`.
- Legacy compat (line 130): Old config `experiments.agent_team_audit` handled by audit-engine.

**Existing steps unmodified**: PASS
- C.1 (lines 91-106) and C.2 action/output (lines 108-148) maintain original structure.
- Audit logic is embedded as a `pre_hook` within C.2 (lines 114-135), not modifying C.2's core flow. When disabled, the pre_hook is skipped entirely (line 135: `on_skip: 继续合并 (审计未启用)`).

**allowed-tools**: PASS
- Frontmatter (line 10): `allowed-tools: Bash, Read, Write, Glob, Grep, Task, Skill`. `Skill` tool present.

**No breaking output changes**: PASS
- Core output (lines 153-168) is unchanged.
- `audit_verdict` and `audit_report` (lines 144-145) are conditional fields, only present when audit is enabled.

---

### 4. phase-d-closer/SKILL.md (v1.0.0) -- PASS

**audit.enabled=false guard**: PASS
- Lines 81-82: `D.post` checkpoint condition: `audit.enabled == true AND audit.checkpoints.post_closure != "off"`.
- Line 92: `不阻塞: 无论 verdict 结果如何，均继续执行 D.2` -- even when enabled, this checkpoint is non-blocking (experience extraction only).
- Line 95: `on_fail: 记录审计报告但不阻塞，继续 D.2`.
- Line 96: `on_skip: 直接进入 D.2`.

**Existing steps unmodified**: PASS
- D.1 (lines 64-76) and D.2 (lines 98-109) are unchanged.
- `D.post` (lines 78-96) is inserted as a new section between D.1 and D.2, with explicit skip behavior when disabled.

**allowed-tools**: N/A (acceptable)
- Frontmatter (line 9): `allowed-tools: Read, Write, Glob, Grep, Bash, Task`. Does NOT include `Skill`.
- **Note**: This is acceptable because `D.post` is non-blocking and the Phase D Skill can invoke audit-engine via `Task` tool (subagent dispatch). However, if direct Skill invocation is intended, `Skill` should be added. This is non-breaking since the checkpoint is purely advisory and non-blocking.

**No breaking output changes**: PASS
- Core output (lines 114-127) is unchanged. `context_for_next: null` remains.
- No new fields are added to the output when audit is disabled.

---

### 5. brainstorm/SKILL.md (v2.0.0) -- PASS

**audit.enabled=false guard**: PASS
- Line 141: Trigger condition: `audit.enabled == true AND audit.checkpoints.post_brainstorm != "off"`.
- When `audit.enabled=false` (the default per DEFAULTS.json line 30), the entire "post_brainstorm" section (lines 138-153) is skipped.

**Existing steps unmodified**: PASS
- The three core phases (Understanding lines 47-73, Exploring lines 75-106, Presenting lines 108-136) are completely unchanged.
- The audit checkpoint (lines 138-153) is appended after Phase 3, not modifying any existing phase logic.

**allowed-tools**: N/A
- Brainstorm SKILL.md frontmatter does not list `allowed-tools` -- it inherits defaults. The audit section is descriptive (calling audit-engine conceptually). No frontmatter change needed as this is a prompt-based Skill without explicit tool restrictions.

**No breaking output changes**: PASS
- Output specs (lines 179-229) are unchanged.
- The audit checkpoint only gates file write (line 150-152: if FAIL, blocks output file; else continues). When disabled, brainstorm writes files exactly as before.

---

### 6. task-planner/SKILL.md (v2.0.0) -- PASS

**audit.enabled=false guard**: PASS
- Line 123: Trigger condition: `audit.enabled == true AND audit.checkpoints.post_planning != "off"`.
- When disabled, the entire A.2.7 section (lines 120-137) is skipped and task-planner proceeds directly to completion.

**Existing steps unmodified**: PASS
- Steps A.2.1 through A.2.6 (lines 53-118) are completely unchanged.
- A.2.7 (lines 120-137) is appended as a new step after the existing flow.

**allowed-tools**: N/A
- Frontmatter (line 10): `allowed-tools: Read, Write, Glob, Grep, AskUserQuestion`. Does not include `Skill`.
- Same observation as Phase D: `Skill` tool may be needed if direct invocation of audit-engine is intended. However, since task-planner is orchestrated by phase-a-planner (which has `Skill`), the audit call may be delegated. Non-breaking.

**No breaking output changes**: PASS
- Output format (lines 152-203) is unchanged.
- No new fields in the output when audit is disabled.

---

### 7. state-scanner/SKILL.md (v2.7.0) -- PASS

**audit.enabled=false guard**: PASS
- Phase 1.10 (lines 370-417): Explicit step 1 checks `audit.enabled == false` or field missing, outputs `enabled: false` and skips subsequent steps.
- When `audit.enabled=false`: output is simply `audit_status: { enabled: false }` (line 416-417).
- State-scanner does not execute any audit; it only reads and reports audit configuration state.

**Existing steps unmodified**: PASS
- Phases 1 through 1.9 (lines 61-368) are untouched.
- Phase 1.10 (lines 370-417) is additive -- a new scan phase appended to the existing sequence.
- Phase 2 (recommendation rules, line 421) adds `audit_unconverged` as a new rule alongside existing rules, not replacing any.
- Phase 3-4 (lines 435-467) are unchanged.

**allowed-tools**: PASS
- Frontmatter (line 11): `allowed-tools: Read, Glob, Grep, Bash`. Sufficient for reading config and scanning audit report directory. State-scanner does not call audit-engine, only reads its outputs.

**No breaking output changes**: PASS
- New `audit` section in Phase 1 output (lines 96-108) and new `audit_status` in Phase 1.10 output are additive fields.
- Existing fields (`git`, `project`, `changes`, `requirements`) are unchanged.
- Phase 4 output (line 463-466) adds optional `audit` context field, only when `audit.enabled=true`.

---

### 8. config-loader/SKILL.md (v1.0.0) -- CONDITIONAL PASS

**audit.enabled=false guard**: PASS
- DEFAULTS.json (line 30-31): `audit.enabled: false` is the default. All checkpoints default to `"off"` (lines 52-58).
- When no `audit` block exists in user config AND `experiments.agent_team_audit` is false/missing, audit remains fully disabled.

**Existing steps unmodified**: PASS
- Original loading flow (lines 23-29) is unchanged: find -> parse -> validate -> merge.
- Legacy compat layer (lines 111-157) is inserted at step 3 (before validation), which is a standard extension point.
- Original field validation rules (lines 43-87) for `workflow.*`, `state_scanner.*`, `tdd.*`, `benchmarks.*`, `experiments.*` are all preserved.

**allowed-tools**: N/A
- Config-loader is internal infrastructure (`user-invocable: false`). Its `allowed-tools: Read, Glob` is appropriate -- it only reads configuration files.

**No breaking output changes**: PASS
- Config-loader's contract is: return a config object with defaults merged. New `audit.*` fields (lines 89-109) are additive to the config object.
- Existing consumers reading `experiments.*`, `workflow.*`, etc. are unaffected.

**Conditional note**: The legacy compat layer (lines 116-121) triggers ONLY when `experiments.agent_team_audit === true` AND no `audit` block exists. This means:
- Users with `experiments.agent_team_audit: false` (default): No change.
- Users with `experiments.agent_team_audit: true` but no `audit` block: Auto-mapped to `audit.enabled: true` with `mode: "manual"`. This is intentional migration behavior, not a breaking change, but deserves a CONDITIONAL PASS because it changes effective behavior for those users (from direct agent-team-audit calls to audit-engine orchestration).

---

## Cross-Cutting Findings

### 1. Default Safety (PASS)

DEFAULTS.json confirms `audit.enabled: false` and all 7 checkpoints default to `"off"`. A project with no `.aria/config.json` or with an empty audit block will have zero audit behavior -- identical to pre-integration.

### 2. Legacy Config Compatibility (PASS)

The `experiments.agent_team_audit` to `audit.*` mapping is:
- Only triggered when both conditions are met (old config true + no new audit block).
- Maps to `mode: "manual"` (most conservative).
- Produces a user-visible migration prompt.
- Does not delete or modify the old fields.

### 3. Output Schema Compatibility (PASS)

All audit-related output fields (`audit_verdict`, `audit_report`, `mid_audit_verdict`, `audit_status`) are:
- Conditional (only present when audit is enabled).
- Additive (no existing fields removed or renamed).
- Consumers that do not read these fields are unaffected.

### 4. allowed-tools Coverage (ADVISORY)

Two Skills lack `Skill` in their `allowed-tools` frontmatter:
- **phase-d-closer**: Has `Task` but not `Skill`. Acceptable because D.post is non-blocking.
- **task-planner**: Has `AskUserQuestion` but not `Skill`. Acceptable because orchestrated by phase-a-planner.

**Recommendation**: Consider adding `Skill` to both for direct audit-engine invocation capability. This is non-blocking for current functionality.

---

## Final Verdict

**7/8 PASS, 1/8 CONDITIONAL PASS**

All 8 files maintain backward compatibility when `audit.enabled=false` (the default). No existing workflow steps are modified. No existing output formats are broken. The conditional pass on config-loader is due to intentional migration behavior for legacy `experiments.agent_team_audit` users, which is well-documented and non-destructive.

**No regressions detected.**
