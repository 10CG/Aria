---
checkpoint: post_spec
round: R1
agent: aria:backend-architect
spec: aria-ten-step-session-handoff-stage
verdict: PASS_WITH_WARNINGS
converged: false
timestamp: 2026-05-14T00:00Z
---

# R1 Audit — H0 aria-ten-step-session-handoff-stage (backend-architect)

**Date**: 2026-05-14
**Round**: R1
**Agent**: aria:backend-architect
**Spec under review**: `openspec/changes/aria-ten-step-session-handoff-stage/`
**Verdict**: PASS_WITH_WARNINGS

---

## Findings

### Critical (must-fix before approval)

**C1 — Schema version bump will break SKILL.md Phase 2 entry assertion**

`aria/skills/state-scanner/SKILL.md` line 155 contains a hardcoded equality check:

```
值 != "1.0" → abort, 提示 "scan.py schema 版本 (X.Y) 与 SKILL.md 契约 (1.0) 不兼Compatible..."
```

The proposal (T1.2) bumps `SNAPSHOT_SCHEMA_VERSION` in `scan.py` from `"1.0"` to `"1.1"`. This will immediately trigger the abort path in every SKILL.md Phase 2 entry the moment the new `scan.py` runs — breaking state-scanner entirely until SKILL.md is also updated.

The schema doc (`state-snapshot-schema.md` §Additive-change policy, lines 43-44) explicitly states: _"SKILL.md Phase 2 asserts `snapshot_schema_version == "1.0"` literal. To preserve this without rewriting SKILL.md for every addition, new fields MUST be additive-compatible and preserve `"1.0"`."_

T1.4 (tasks.md line 24) says SKILL.md Phase 2 entry assertion should "accept `1.0` OR `1.1` (transition period soft accept)" — but this is listed as a task step, not a pre-condition. The ordering risk is real: if T1.2 lands before T1.4, any scan produces a broken snapshot.

**Recommendation**: Either (a) keep `SNAPSHOT_SCHEMA_VERSION = "1.0"` — the `handoff` field is additive per the existing policy; there is no semantic need to bump to 1.1 for an additive top-level key, which is the precedent set by all G2/G3/G4 additions in v1.18.0. Or (b) if bumping to 1.1 is intentional to signal the new field to consumers, then T1.4 MUST be implemented atomically in the same commit as T1.2 (not sequentially) AND the schema-doc additive-change policy table needs updating to declare this change as a "Minor" bump rather than "Additive". Option (a) is strongly preferred — it avoids a breaking change entirely, follows established precedent, and eliminates C1.

---

### Major (should-fix this round)

**M1 — T2 trigger condition "session > 4h" has no measurable signal in current code**

The trigger condition for D.3 includes `session > 4h`. No existing runtime field tracks session wall-clock duration. `interrupt.session_age_seconds` is explicitly `null` (deferred, `scan.py` line 61: `# T1.2 defers session-age calc to later patch`). The `workflow-state.json` schema (`workflow-state-schema.md` lines 17-20) has `session.started_at` and `session.last_active_at` fields, but these are only populated when a `workflow-state.json` is present — which is not the case for most handoff scenarios (user ends a session without an active workflow).

Without a concrete signal, the D.3 skill must fall back to asking the user to self-report session duration, which is ad-hoc and defeats the automation intent.

**Recommendation**: Tasks.md should explicitly specify the evaluation order: (1) check `interrupt.raw.session.started_at` if workflow-state exists → compute duration; (2) if no workflow-state, fall back to heuristic "AI estimates based on context length / timestamps in conversation"; (3) if unable to determine, prompt user. Document the fallback hierarchy explicitly in T2.2. Alternatively, scope this trigger to the other two measurable conditions (≥2 cycles/US, ≥2 phases from phase_results) and demote "session > 4h" to a user-confirmed prompt ("Has this session lasted more than 4 hours?").

**M2 — T3 hook path-pattern does not distinguish relative vs. absolute path forms**

T3.1 specifies matching `path matches .aria/handoff/*.md` but `tasks.md` line 46 notes "incl. relative + absolute forms" without specifying how the hook framework disambiguates them. In Claude Code's PreToolUse hook system, the `file_path` parameter for Write/Edit tools is typically the absolute path as passed by the tool. However, if the AI issues `Write` with a relative path like `../.aria/handoff/foo.md` from inside `docs/`, the glob pattern `.aria/handoff/*.md` would fail to match because the hook sees the resolved absolute path.

The `aria/hooks/hooks.json` existing hook uses a simple command-execution pattern (not a path-pattern hook). The spec does not clarify whether `handoff-location-guard.json` uses a regex or glob on the absolute path or the raw tool input. T3.1 says "path matches `.aria/handoff/*.md`" — this is ambiguous and fragile. For symlinks, if `.aria/handoff` is a symlink to another directory, the resolved path will not match `.aria/handoff/`.

**Recommendation**: T3.1 should specify that the match pattern is applied against the resolved absolute path, and use a regex that matches `[/\\].aria[/\\]handoff[/\\][^/\\]+\.md$` rather than a glob. Also note explicitly that symlinks are out-of-scope (acceptable given T6 removes the directory). Add to T3.4 smoke test: test with both absolute and relative path inputs.

**M3 — `misplaced_files` false-positive guard not specified for non-handoff `.md` in `.aria/handoff/`**

The proposal (T1.1) detects `.aria/handoff/*.md` as misplaced. But after T6 migration, the spec says "`.aria/handoff/` dir not exist" — so in steady state, the dir is gone and L2 detection is moot. The concern is pre-migration behavior: if `.aria/handoff/README.md` or `.aria/handoff/NOTES.md` existed as legitimate documentation (e.g. a future project team puts a README there), the collector would flag it as a misplaced handoff doc.

The spec's "misplaced_files: [paths]" field does not distinguish between handoff docs (`.md` files matching handoff naming conventions) and arbitrary `.md` files in that path.

**Recommendation**: Add a check in `collectors/handoff.py` that either (a) only flags files whose names match the handoff naming pattern (e.g., `YYYY-MM-DD-*.md` or files containing "handoff" / "session" / "closeout" in the name), or (b) flags all `.md` files but includes a `misplaced_file_type: "unknown"` vs `"handoff_pattern"` field. Alternatively, document explicitly in T1.1 that any `.md` in `.aria/handoff/` is treated as misplaced regardless — since the canonical decision is that `.aria/handoff/` is forbidden entirely.

---

### Minor (polish, can defer)

**m1 — mtime-based latest-detection is not deterministic across `git clone` (fat-clone vs. shallow)**

The `audit.py` collector (line 22) uses the same `key=lambda p: p.stat().st_mtime` sort pattern. However, `git clone` without `--no-checkout` or `git reset --hard` often sets all file mtimes to the checkout timestamp, not the original commit timestamp. On a fresh clone, all `docs/handoff/*.md` files would have the same mtime, making the sort non-deterministic (tie-breaking falls to directory enumeration order, which varies by filesystem).

The existing `requirements.py` `priority_items` sort handles this with a three-level stable tie-break (status → mtime DESC → path LEX ASC per schema-doc lines 255-258). The handoff collector should adopt the same pattern: mtime DESC with filename LEX ASC tiebreak.

**m2 — T3 typo: "Match tool_name: Write OR Edit OR Write" (tasks.md line 46)**

`tasks.md` line 46: `Match tool_name: Write OR Edit OR Write` — "Write" is duplicated. Should be `Write OR Edit` (and potentially `MultiEdit` if that tool exists in the framework).

**m3 — "30 days" CLAUDE.md Rule #9 deferral window may be over-conservative given 4 existing dogfoods**

The proposal defers Rule #9 activation pending "ship + 3 dogfood reuse + 0 drift for 30 days." With 4 incidents already documented (SilkNode + Aria self x3) and the 5-layer defense-in-depth providing strong enforcement, a 30-day observation window post-ship seems conservative. This is not blocking, but the 30-day figure is arbitrary and could be tightened to 14 days given the dogfood evidence already cited in the proposal itself. Acceptable to defer as stated.

**m4 — T6 migration: `git mv` across project boundary note needed**

The migration (T6) operates on files in the Aria main repo — not inside the `aria` submodule. `tasks.md` T6.2 says "verify mtime preserved (git history follows mv, blame preserved)" but `git mv` preserves history via rename-detection at diff time, not at commit time. `git log --follow` will work; `git blame` on the moved file will show the move commit as the origin unless `--follow` is used. This is standard behavior but worth explicitly documenting in T6.2 so the dogfood verifier knows to use `git log --follow docs/handoff/<file>` for history check. Not a blocker.

---

### Observations (no action needed, just noted)

**O1 — Collector API shape is consistent with existing pattern**

`collectors/audit.py` is the closest analog: scans `.aria/audit-reports/` by mtime, picks latest, returns `CollectorResult`. The proposed `collectors/handoff.py` follows the same pattern (scan dir by mtime, return structured dict). Return shape using `CollectorResult` dataclass from `_common.py` is correct. The stdlib-only constraint (`pathlib`, `datetime`, `os`) is satisfied — no external deps needed.

**O2 — `issue_status` opt-in precedent suggests `handoff` field should always be emitted**

Unlike `issue_status` (Phase 1.13) which is opt-in and conditionally emitted, the `handoff` collector is unconditional. This is the right design — the `docs/handoff/` path is deterministic and the collector should always emit the `handoff` block (with `exists: false` when the dir is empty), matching the `audit` collector's pattern. The spec is correct on this.

**O3 — Layer interaction order is sound**

L1 hook fires at PreToolUse (write attempt) → L2 collector fires at scan time (read-only) → L3 recommendation fires at Phase 2 (after scan). These three layers are non-conflicting. The concern about "hook blocking the migration" is correctly addressed in the proposal: `git mv` via Bash tool is unaffected by Write/Edit PreToolUse hooks. The spec does not need to add explicit text for this — it's a property of the tool framework.

**O4 — `__init__.py` registration step absent from tasks**

`tasks.md` T1.2 covers editing `scan.py` to import the new collector, but does not mention updating `collectors/__init__.py` to export `collect_handoff`. Looking at `__init__.py`, every collector must be added to both the import list and `__all__`. This is a small but mandatory step. It could be added as T1.2.a or noted in T1.2 body text.

---

## Verdict rationale

The spec is structurally sound and the layered defense approach is well-designed. The collector pattern is consistent with existing code. The primary blocker is **C1**: bumping `snapshot_schema_version` to `"1.1"` while `SKILL.md` has a hardcoded `!= "1.0"` abort will break state-scanner. The simplest fix — keeping the version at `"1.0"` per the existing additive-change policy — eliminates this risk entirely, following the exact same precedent established by the G2/G3/G4 additions in v1.18.0.

**M1** (session duration signal) is real but manageable: the spec should document the three-tier fallback hierarchy for the 4h trigger condition rather than leaving it as an undefined signal. **M2** (hook path pattern ambiguity) needs a concrete regex specification. If C1 is resolved by dropping the version bump (option a), and M1/M2 are addressed inline in tasks.md, this spec can proceed to approval without an R2.

## Convergence vote

- [ ] PASS — spec ready for approval
- [x] PASS_WITH_WARNINGS — Critical=1 (C1 resolvable inline by dropping version bump), Major=2 (M1/M2 inline-fixable in tasks.md)
- [ ] FAIL — needs R2
