---
checkpoint: post_spec
round: R2
agent: aria:backend-architect
spec: aria-ten-step-session-handoff-stage
verdict: PASS_WITH_WARNINGS
converged: false
timestamp: 2026-05-14T00:30Z
---

# R2 Audit — H0 aria-ten-step-session-handoff-stage (backend-architect)

**Date**: 2026-05-14
**Round**: R2
**Agent**: aria:backend-architect
**Spec under review**: `openspec/changes/aria-ten-step-session-handoff-stage/`
**Verdict**: PASS_WITH_WARNINGS

---

## R1 findings verification

| ID | R1 Finding | R2 Status | Notes |
|----|-----------|-----------|-------|
| C1 | Schema version bump 1.0 → 1.1 breaks SKILL.md hardcoded check | ⚠️ Partially resolved | T1.1, T1.2, T1.4 text correctly drops the bump. However, `proposal.md` Success Criteria line 179 still reads "符合 schema 1.1", and tasks.md T8.3 commit message still says "schema 1.1". These residual references contradict the fix and will cause confusion during Phase B implementation. Core logic is correct; docs are inconsistent. |
| M1 | D.3 trigger "session > 4h" has no measurable runtime signal | ✅ Resolved | T2.2 adds explicit 4-level fallback hierarchy: (1) `workflow-state.json::session.started_at` → elapsed; (2) `git log` cycle archive count; (3) phase markers in commit subjects; (4) prompt user with `yes` default if D.2 succeeded. Signal path is now fully specified. |
| M2 | Hook path-pattern ambiguous (relative vs absolute, symlinks) | ✅ Resolved | T3.1 replaces glob with absolute-path regex `^(?:.+/)?\.aria/handoff/[^/]+\.md$`, adds `realpath` resolution before match, and explicitly excludes Bash tool from interception scope. Pattern is unambiguous for the Linux/macOS deployment environment. |
| m2 | Typo "Write OR Edit OR Write" | ✅ Resolved | T3.1 now lists `{Write, Edit, NotebookEdit}` — no duplicate. |
| O4 | `collectors/__init__.py` registration absent from tasks | ✅ Resolved | T1.3 explicitly adds registration of new `handoff` module to `__init__.py` and `__all__`. The fix is consistent with the existing pattern (import from `.handoff` + export `collect_handoff` in `__all__`). |

---

## New findings (R2 introduced or missed in R1)

### Critical

None.

### Major

**R2-M1 — Residual "schema 1.1" references in proposal.md Success Criteria + tasks.md T8.3 commit message contradict the F1 fix**

`proposal.md` line 179 (Success Criteria) still reads:

```
- [ ] `python3 scripts/scan.py` 输出 snapshot 含顶层 `handoff` 字段,符合 schema 1.1
```

`tasks.md` line 161 (T8.3 commit message template) still reads:

```
`feat(state-scanner): add handoff collector + snapshot.handoff field (schema 1.1)`
```

Additionally, `proposal.md` line 153 (Impact / Risk row) still reads:

```
Schema 1.0 → 1.1 是 additive,但下游 consumer 若严格 schema validate 需升级
```

These three stale references directly contradict T1.1 "No version bump", T1.2 "不修改 `snapshot_schema_version` — 保持 `"1.0"`", and T1.4 "schema 仍 1.0". The F1 fix was applied to the task specifications but not propagated to all prose sections.

**Risk**: A Phase B implementer following the Success Criteria verbatim will attempt to verify `schema_version == "1.1"` — which will fail against a correctly implemented T1 that preserves `"1.0"`. The T8.3 commit message template also encodes `schema 1.1` which would generate misleading git history.

**Recommendation**: Before Phase B begins, update three locations in proposal.md:
- Line 179: replace "符合 schema 1.1" with "符合 schema 1.0 (additive field, no bump)"
- Line 153 Risk row: restate as "handoff field 是 additive top-level key, schema 保持 1.0; 已有 SKILL.md 契约无需改动"
And in tasks.md:
- Line 161: replace "schema 1.1" with "schema 1.0 (additive)" in the aria commit message template

This is a Major rather than Critical because the normative task text (T1.1, T1.2, T1.4) is correct — the stale prose cannot cause a runtime breakage on its own, only implementation confusion. However, it creates an inconsistent spec that violates the "文档与代码必须同步" principle (#3) and risks divergence in Phase B.

**R2-M2 — F3 regex does not handle Windows absolute paths (backslash separators)**

The F3 regex `^(?:.+/)?\.aria/handoff/[^/]+\.md$` exclusively uses forward-slash `/` as the path separator. On Windows, `os.path.realpath()` and `pathlib.Path.resolve()` return paths using backslash `\` as separator (e.g., `C:\Users\dev\project\.aria\handoff\foo.md`).

The hook spec states the resolved `realpath` is matched against this regex. On Windows the regex would never match — the hook silently stops enforcing the forbidden location.

Inspection of `scan.py` confirms stdlib-only usage with `pathlib.Path`, which is cross-platform. However, no scan.py contract document explicitly excludes Windows, and the `aria/skills/state-scanner/scripts/collectors/` directory uses `pathlib.Path` throughout (which emits OS-native separators on stat/glob operations).

**Assessment**: The M1 R1 recommendation specifically suggested `[/\\]` separators for this reason. The F3 fix adopted the more ergonomic forward-slash-only regex without addressing the Windows case.

**Recommendation** (two options):
- Option A (preferred): Update the regex to `^(?:.+[/\\])?\.aria[/\\]handoff[/\\][^/\\]+\.md$` in both T3.1 and proposal.md T3 description. Add a note in T3.1: "On Windows, `realpath()` returns backslash-separated paths; the regex must use `[/\\]` separators."
- Option B (scope boundary): Add an explicit Out-of-scope statement: "Hook enforcement on Windows is out of scope for v1.21.0. Windows paths with backslash separators are not matched." This is acceptable if Aria confirms Windows is not a supported deployment target, but the Out-of-scope section currently makes no mention of platform constraints.

This finding is Major because it causes a silent enforcement gap — not a crash, but complete bypass of Layer 1 on a supported OS variant. The issue was present in the pre-fix spec and explicitly flagged in R1 (though framed as a secondary concern within M2). The F3 fix resolved the relative/absolute ambiguity but did not address the separator issue.

### Minor

**R2-m1 — `__init__.py` registration in T1.3 specifies `__all__` update but does not name the export symbol**

T1.3 says "Register new `handoff` module in `__all__` (per existing collector convention)." The existing pattern in `collectors/__init__.py` requires both:
1. `from .handoff import collect_handoff` in the import block
2. `"collect_handoff"` added to the `__all__` list

The task text mentions only `__all__` registration, not the explicit import statement. A strict reading of T1.3 could lead an implementer to add only `"collect_handoff"` to `__all__` without the corresponding `from .handoff import collect_handoff` line, which would cause a `NameError` at scan time.

**Recommendation**: Expand T1.3 to read: "Add `from .handoff import collect_handoff` to the import block and `"collect_handoff"` to `__all__` in `collectors/__init__.py`." Low risk in practice (an implementer reading the existing pattern will do both), but the spec should be unambiguous.

**R2-m2 — F2 fallback level 4 ambiguity: "default yes if D.2 succeeded" interacts oddly with the 3 measurable conditions**

T2.2 fallback level 4: "prompt user... default `yes` if Phase D 执行到 D.2 archive 成功". If levels 1-3 are all absent/inconclusive (e.g., no workflow-state.json, no git log cycles, no phase markers — a first-ever session on a fresh project), the fallback fires and defaults to `yes`, triggering handoff creation after every D.2.

This is intentional per the spec (conservative design — better over-write than under-write), but it means every D.2 completion on a project with no handoff history will prompt D.3 with a `yes` default. The proposal notes this in the Impact/Risk table ("触发条件可能过于宽松"). This is accepted design, but T2.2 should note explicitly: "First-session edge case: all 3 signals absent → level 4 fires → default yes → D.3 triggers. This is intentional (first session likely warrants a handoff); document in T5 convention SOT."

This is a minor note, not a blocker.

---

## Convergence vote

- [ ] **SCOPE_OK_R2** (R2 PASS — all R1 fixed, 0 new Critical, R3 unnecessary)
- [x] **PASS_WITH_WARNINGS** (R3 recommended for R2-M1 + R2-M2 inline fixes; alternatively treat as pre-Phase-B editorial gate)
- [ ] FAIL (regression introduced)

**Qualification**: If the spec author treats R2-M1 and R2-M2 as inline fixes before Phase B kickoff (not requiring another audit round), both are editorial in nature and a formal R3 is unnecessary. R2-M1 is pure doc consistency (3 text replacements); R2-M2 regex fix is a one-line change to T3.1 and T3.1 description. In that case the convergence vote upgrades to SCOPE_OK_R2 post-fix, with no R3 required.

---

## Summary

All three R1 Critical/Major findings are substantially addressed: C1 (schema bump) is correctly dropped in the normative task text; M1 (4h trigger signal) now has an explicit 4-level fallback hierarchy; M2 (hook path ambiguity) is resolved via absolute-path regex with realpath resolution. Two new Major findings are introduced by the fixes: R2-M1 is a doc-consistency gap where three prose locations in proposal.md and tasks.md still reference "schema 1.1" despite the F1 fix — this creates an implementation trap in Success Criteria and commit message templates. R2-M2 is the Windows backslash separator gap in the F3 regex, which would cause the hook to silently fail on Windows deployments. Both are inline-fixable (3 text substitutions + 1 regex character class change) before Phase B begins, making a formal R3 unnecessary if treated as a pre-Phase-B editorial gate. Recommend resolving R2-M1 and R2-M2 inline and proceeding to Phase B.
