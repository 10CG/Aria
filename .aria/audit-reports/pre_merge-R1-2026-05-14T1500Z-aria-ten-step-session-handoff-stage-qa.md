---
checkpoint: pre_merge
mode: convergence
round: 1
change_id: aria-ten-step-session-handoff-stage
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
vote: PASS_WITH_WARNINGS
timestamp: 2026-05-14T15:00Z
context: openspec/changes/aria-ten-step-session-handoff-stage/
agent: aria:qa-engineer
findings_critical: 0
findings_major: 3
findings_minor: 4
---

# aria-ten-step-session-handoff-stage pre_merge R1 (QA) — 2026-05-14T15:00Z

> **Agent**: aria:qa-engineer
> **Checkpoint**: pre_merge (Phase B.3, before T8 ship)
> **Vote**: PASS_WITH_WARNINGS
> **Focus**: Test coverage gaps, regression risk, bootstrap concerns, production readiness
> **Spec**: openspec/changes/aria-ten-step-session-handoff-stage/ (Approved 2026-05-14)
> **Target release**: aria-plugin v1.21.0 MINOR

---

## 150-Word Summary

The H0 implementation is functionally sound and all 10 shell tests pass (DENY_JSON / PASS_SILENT / DENY_EXIT2 modes verified). Python test suite shows 438/438 PASS with no regressions. Three Major findings require attention before or at T8 ship: (M1) the `soft_error` path for permission-denied on the canonical dir is silently swallowed — `exists=False` with no error emitted, no unit test covers this; (M2) `latest.md` pointer file wins the mtime sort whenever it is updated (as happened in T6 migration), causing the collector to surface a pointer file rather than the actual handoff document — not tested; (M3) the shell test suite (`test_handoff_hook.sh`) is excluded from the primary `run_tests.py` runner and must be invoked manually, creating a CI blind spot. Four Minor findings include un-tested stat() soft_error trigger, stale "exit code 2" text in tasks.md, missing `latest.md` exclusion documentation, and potential false-positive on case-insensitive path matching for Linux. No Critical findings. PASS_WITH_WARNINGS; M1 and M2 are fixable as test additions without blocking ship.

---

## Critical Findings

None.

---

## Major Findings

### M1: Permission-denied on canonical `docs/handoff/` silently produces `exists=False` with no error

**File**: `aria/skills/state-scanner/scripts/collectors/handoff.py`, `_scan_md_files()` lines 44-55

**Evidence**:
When `docs/handoff/` exists as a directory but has mode `000` (no read permission), `Path.is_dir()` returns `True` on Linux (directory presence does not require read permission). The subsequent `directory.iterdir()` raises `OSError` which is caught and swallowed, returning an empty list. `collect_handoff()` then emits `exists=False` with an empty `errors` list. The AI consumer receives a clean snapshot indicating no handoff files, which is factually incorrect.

Reproduction:
```python
os.chmod("docs/handoff", 0o000)
r = collect_handoff(root)
# r.data["exists"] == False, r.errors == []  # misleading
```

**Verified by**: live test run in this audit session.

**Impact**: AI reads `handoff.exists=False` → skips reading handoff → loses session carry-forward context. This is the primary user pain point (Issue #92) that H0 is designed to solve. Permission errors on the canonical dir would silently defeat the fix.

**Missing test**: No test case covers `docs/handoff/` existing but unreadable. The module docstring lists "soft_error on stat() failure" but this refers only to the stat() OSError on line 85-87; the `_scan_md_files` OSError (line 54) emits no soft_error at all.

**Recommendation**:
1. In `_scan_md_files`, change `except OSError: return []` to emit a soft_error via a callback or return a sentinel.
2. Add a test in `TestEdgeCases` that chmods `docs/handoff/` to 000, verifies `errors` is non-empty with key `handoff_dir_unreadable`, then restores permissions.

**Severity**: Major — silent false negative defeats the core collector contract.

---

### M2: `latest.md` pointer file wins mtime sort, surfacing a pointer not a handoff document

**File**: `aria/skills/state-scanner/scripts/collectors/handoff.py` lines 85-86; `docs/handoff/latest.md`

**Evidence**:
After the T6 migration commit (`1de5159`), `docs/handoff/latest.md` has mtime `2026-05-14 22:26:58 UTC` — newer than all actual handoff documents. The collector returns `latest_filename: "latest.md"` and `latest_path: "docs/handoff/latest.md"`. The AI reading this path gets the pointer file content (which links to the real handoff), not the actual handoff content directly. This creates a two-hop indirection: AI must parse the pointer, extract the referenced filename, then read the real document.

Verified via live `python3 scan.py` output:
```json
"latest_filename": "latest.md",
"latest_path": "docs/handoff/latest.md"
```

The spec's intent (proposal.md §T1) is to surface the most recent handoff _document_, not the pointer file. The `latest.md` pointer is updated on every migration or handoff write, making it structurally always the newest mtime.

**No test covers this scenario**: `TestHandoffMtimeSort` only tests filename/mtime combinations that do not include `latest.md` in the fixture.

**Recommendation**:
Option A (preferred): Exclude `latest.md` by name from `_scan_md_files` results: `if entry.name == "latest.md": continue`.
Option B: Document the two-hop behavior explicitly in the module docstring and SKILL.md, and add a test that asserts `latest.md` present in fixture → `latest_filename` equals something other than `latest.md` (i.e., confirm exclusion works) OR assert that AI is expected to follow the pointer.

The `latest.md` exclusion is a one-line change with minimal risk. If Option B is chosen, the RECOMMENDATION_RULES.md output format should document the pointer-following step.

**Severity**: Major — silent behavioral gap vs. spec intent; no test coverage.

---

### M3: Shell test suite excluded from primary test runner — CI blind spot

**File**: `aria/skills/state-scanner/tests/run_tests.py`; `tests/test_handoff_hook.sh`

**Evidence**:
`run_tests.py` uses `unittest.TestLoader().discover(pattern="test_*.py")` which matches only Python files. `test_handoff_hook.sh` is a shell script and is never invoked by `run_tests.py`. The reported "438/438 PASS" count does not include the 10 hook smoke tests.

The shell test must be invoked separately: `bash tests/test_handoff_hook.sh`. It passes cleanly when run manually, but there is no CI integration or automated gate that runs it as part of the standard test pipeline.

**Impact**: If the hook script (`handoff-location-guard.sh`) is modified in a future cycle, `run_tests.py` will not catch regressions. The 10 shell tests cover the primary blocking logic (L1 enforcement), making this a silent coverage gap in the automated pipeline.

**Recommendation**: Add a subprocess invocation to `run_tests.py` that calls `bash test_handoff_hook.sh` and treats non-zero exit as a test failure. Alternatively, document in `tests/README.md` (if one exists) that both `run_tests.py` and `test_handoff_hook.sh` must pass before ship. At minimum, the T8 ship checklist should explicitly include `bash tests/test_handoff_hook.sh`.

**Severity**: Major — active testing gap in the automated pipeline for the Layer 1 hook.

---

## Minor Findings

### m1: `stat()` soft_error path (lines 87-88) has no triggering test

**File**: `aria/skills/state-scanner/tests/test_handoff.py`

The docstring header lists "soft_error on stat() failure" as a covered scenario, and the `except OSError` block at lines 87-88 correctly calls `r.soft_error("handoff_stat_failed", ...)`. However, no test function exercises this code path. The `TestEdgeCases.test_no_errors_on_happy_path` only verifies the non-error branch. Triggering this requires a file that passes `_scan_md_files` then becomes unstateable between the `max()` call and the second `stat()` call (a race condition), or that triggers an OSError in the `max(key=lambda p: p.stat()...)` call.

**Recommendation**: Add `test_soft_error_on_stat_failure` using `unittest.mock.patch` to make `Path.stat` raise `OSError` after file listing succeeds. Assert `r.errors` contains one entry with `code == "handoff_stat_failed"` and `r.data["exists"] == True` (the block correctly sets exists=True even when stat fails).

**Severity**: Minor — the error path exists and is structurally correct; only the test coverage is absent.

---

### m2: tasks.md T7.3 and line 86 still specify "assert exit code 2" for DENY — stale after R2-M2 resolution

**File**: `openspec/changes/aria-ten-step-session-handoff-stage/tasks.md` lines 86 and 149

The R2 audit identified R2-M2 (hook blocking mechanism: exit 0 + JSON deny is correct, not exit code 2). The hook implementation correctly uses `exit 0 + JSON` as the default mode. The test (`test_handoff_hook.sh`) correctly uses `DENY_JSON` expected outcome (checks `rc==0` + JSON `decision: block`). However, tasks.md lines 86 and 149 still read "assert exit code 2" and "assert exit code 2 on `.aria/handoff/` path". These are stale and contradict both the implementation and the test.

**Impact**: Low (runtime unaffected; spec text only). Future cycle readers or agent-team-audit may flag these as inconsistencies.

**Recommendation**: Editorial fix — replace "assert exit code 2" with "assert exit 0 + JSON `{\"decision\": \"block\"}`" in tasks.md lines 86 and 149. Can be done as part of D.2 archive or T8.3 commit.

**Severity**: Minor — documentation-only staleness; no runtime impact.

---

### m3: `re.IGNORECASE` on Linux produces false-positive DENY for `.ARIA/HANDOFF/x.md`

**File**: `aria/hooks/handoff-location-guard.sh` (Python inline, line 76-79)

The regex `FORBIDDEN_RE` uses `re.IGNORECASE`. On Linux (case-sensitive filesystem), `.ARIA/HANDOFF/x.md` is a completely different path from `.aria/handoff/x.md` — the uppercase variant cannot be the forbidden directory (which does not exist). Blocking a write to `.ARIA/HANDOFF/x.md` is a false positive: the AI may legitimately want to create files in a `.ARIA/` directory on a case-sensitive system.

Verified: `echo '{"tool_name": "Write", "tool_input": {"file_path": ".ARIA/HANDOFF/x.md"}}' | bash handoff-location-guard.sh` → DENY.

**Impact**: Low probability in practice (`.ARIA/` directory is unlikely). But if a downstream project has a legitimate `.ARIA/` directory, the hook would incorrectly block writes to it.

**Recommendation**: Remove `re.IGNORECASE` and leave case-sensitive matching as Linux default. The Windows `[/\\]` separator handling (already present) is sufficient for cross-platform support without case folding. Alternatively, add a note in the hook comments explaining the intentional over-blocking rationale.

No test covers this case (test case 6 tests absolute path, not case-sensitivity).

**Severity**: Minor — false positive risk in edge deployment scenario.

---

### m4: `latest.md` not documented as a known pointer file — downstream consumers lack guidance

**File**: `aria/skills/state-scanner/scripts/collectors/handoff.py` (module docstring); `aria/skills/state-scanner/SKILL.md`

Neither the collector module docstring nor the SKILL.md Phase 1.15 section documents that `docs/handoff/latest.md` exists as a pointer file and may appear as `latest_filename` in snapshot output. Downstream consumers (AI agents reading the snapshot) will see `latest_path: "docs/handoff/latest.md"` and must know to follow the pointer link inside it to reach the actual handoff content.

The Phase 2 recommendation logic in RECOMMENDATION_RULES.md does not account for this pointer-following step either.

**Impact**: AI may read `latest.md` and stop, without reading the actual handoff document. This partially defeats the Phase 1.15 collector's purpose.

**Recommendation**: Add to the collector docstring: "Note: `docs/handoff/latest.md` (if present) is a pointer file — its content references the actual latest handoff. Consumers should follow the pointer link." Also add a Phase 2 recommendation note instructing AI to follow the pointer if `latest_filename == "latest.md"`. This is resolved by M2's recommended fix (exclusion), making m4 dependent on M2's resolution path.

**Severity**: Minor — behavioral guidance gap; AI can still reach the handoff via the pointer, just with one extra hop.

---

## Observations

### OBS-1: 438/438 Python tests pass cleanly with handoff collector addition

`run_tests.py` shows no regressions across all 26 Python test modules. The new `test_handoff.py` (11 tests) runs cleanly. The `test_normalize_snapshot.py` and `test_upm.py` files reference `docs/handoff/` paths only in string fixtures — no filesystem dependency — so they are unaffected by the T6 migration.

### OBS-2: Hook correctly handles `null` tool_input and malformed JSON

Live testing confirmed:
- `{"tool_name": "Write", "tool_input": null}` → `tool_input or {}` coerces null to `{}` → PASS (correct)
- `{"tool_name": "Write", "tool_input": {"file_path": null}}` → `file_path or ""` → empty string → PASS (correct)
- Malformed JSON → `json.JSONDecodeError` caught → PASS (correct)

No test cases cover these null/malformed scenarios in `test_handoff_hook.sh`. These are defensive paths that work correctly but could be tested for regression hardening.

### OBS-3: Double `stat()` call at lines 85-86 is inside the `try` block — TOCTOU is handled

Both `p.stat().st_mtime` (in the `max()` lambda) and `latest.stat().st_mtime` (line 86) are inside the same `try/except OSError` block. A concurrent file deletion between the two calls would raise OSError from line 86, which is caught and converted to `handoff_stat_failed` soft_error with `exists=True`. This is correct behavior.

### OBS-4: 5-layer enforcement matrix is coherent and all layers verified present

- L1 (hook): `aria/hooks/handoff-location-guard.sh` — present, tested, registered in `hooks.json`
- L2 (collector): `aria/skills/state-scanner/scripts/collectors/handoff.py` — present, 11 tests
- L3 (recommendation): `RECOMMENDATION_RULES.md` §1.91 `handoff_drift` rule — present
- L4 (convention SOT): `standards/conventions/session-handoff.md` — present (standards submodule on feature branch, pending merge)
- L5 (template hardcode): `aria/templates/session-handoff.md` + `phase-d-closer/SKILL.md §D.3` — present

### OBS-5: Version bump files are at 1.20.0 — 5+1 SOT files not yet updated for v1.21.0

Confirmed: `aria/.claude-plugin/plugin.json` = `"1.20.0"`, `aria/.claude-plugin/marketplace.json` = `"1.20.0"`, `aria/VERSION` = `1.20.0`, `aria/CHANGELOG.md` latest entry = `[1.20.0]`, `aria/README.md` = `"1.20.0"`, `aria/README.zh.md` = `"1.20.0"`. All six SOT files require atomic bump to `1.21.0` at T8 ship. This is expected pre-merge state; confirming readiness checklist is clean.

### OBS-6: T7.4 dogfood bootstrap sequence is achievable

The temporal sequence is: commits land → PR merge → v1.21.0 tag → multi-remote push → THEN write closeout handoff using `aria/templates/session-handoff.md` directly (bypassing D.3 plugin invocation which requires cache refresh). This is documented in tasks.md T7.4 and was confirmed as acceptable in the R2 audit (QA-m4 resolved). The closeout handoff written in this session counts as the 5th dogfood evidence. The plugin cache refresh is not required for template-based manual dogfood.

### OBS-7: `standards` submodule is on feature branch (not master) pre-merge

`git submodule status` shows `standards` at `+2f3b167` on `feature/aria-ten-step-session-handoff-stage` (commit `feat(conventions): add session-handoff.md`). The `+` prefix indicates the submodule is ahead of what the main project's index records. The T8 ship sequence must include merging the `standards` submodule PR before or simultaneously with the aria and main-project PRs. This is a 3-repo PR coordination requirement.

---

## R1 Findings Table

| ID | Severity | Area | Description | Resolution Path |
|----|----------|------|-------------|-----------------|
| M1 | Major | Test coverage + runtime | Permission-denied on canonical dir silently returns `exists=False`, no soft_error | Add `CannotReadDir` soft_error in `_scan_md_files`; add test |
| M2 | Major | Test coverage + runtime | `latest.md` pointer wins mtime sort — surfaces pointer file not handoff document | Exclude `latest.md` from `_scan_md_files` output; add test |
| M3 | Major | CI / pipeline | Shell hook test excluded from `run_tests.py` — 10 tests never run in automated pipeline | Add subprocess call in `run_tests.py` or document explicit manual gate |
| m1 | Minor | Test coverage | `stat()` soft_error path (lines 87-88) has no test | Add mock-based test |
| m2 | Minor | Docs (tasks.md) | tasks.md lines 86/149 say "exit code 2" — stale after R2-M2 hook fix | Editorial: update to "exit 0 + JSON deny" |
| m3 | Minor | Hook behavior | `re.IGNORECASE` false-positive DENY on `.ARIA/HANDOFF/x.md` (Linux case-sensitive FS) | Remove IGNORECASE or document rationale |
| m4 | Minor | Documentation | `latest.md` pointer file not documented; downstream consumers may not follow pointer | Add docstring note; resolved if M2 exclusion applied |

---

## Verdict

**PASS_WITH_WARNINGS**

The H0 implementation is structurally complete. All 5 enforcement layers are present. Both test suites pass (438/438 Python + 10/10 shell). The core handoff collector and hook logic are functionally correct.

Three Major findings exist: M1 (permission-denied silent false-negative), M2 (`latest.md` mtime contamination), and M3 (shell test excluded from automated pipeline). None of these block the current test execution, but M1 and M2 represent silent behavioral gaps that affect the collector's correctness contract. M3 creates a regression risk for future cycles.

**Recommended disposition for T8 ship**:
- M1 and M2 are one-line code fixes + one test each. They should be applied before or as part of T8 to avoid shipping known silent failure modes in the collector's most important output fields.
- M3 should be tracked as a follow-up issue (acceptable to defer if the T8 checklist explicitly requires `bash tests/test_handoff_hook.sh` as a manual gate step).
- m1-m4 can be deferred to a future cycle.

If M1 and M2 are fixed and a re-run confirms 440/440 (or equivalent) tests pass, this audit upgrades to **SCOPE_OK_R1** with no R2 required.

---

## Convergence Vote

- [x] PASS_WITH_WARNINGS (M1/M2 fixable pre-ship; M3 deferrable with explicit manual gate)
- [ ] SCOPE_OK_R1 (conditional: apply M1 + M2 fixes and confirm tests pass)
- [ ] FAIL (no critical findings; no blocking issues)

**Qualification**: If M1 (`_scan_md_files` OSError soft_error) and M2 (`latest.md` exclusion from mtime sort) are applied with corresponding tests before T8 ship execution, this vote upgrades to SCOPE_OK_R1. The three Major findings collectively do not represent a design flaw; they are implementation gaps amenable to targeted fixes.
