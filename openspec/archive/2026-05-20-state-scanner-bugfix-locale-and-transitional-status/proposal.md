# state-scanner v1.21.4 — sister-bug bundle: locale crash + transitional status mis-classification

> **Level**: 2 (Minimal — proposal-only; 2 file-scoped fixes + regression tests)
> **Status**: **Complete** (Phase A+B+C+D shipped 2026-05-20; merged via aria-plugin PR #51; closes #61 + #73)
> **Change ID**: `state-scanner-bugfix-locale-and-transitional-status`
> **Trigger**: Forgejo Aria [#61](https://forgejo.10cg.pub/10CG/Aria/issues/61) + [#73](https://forgejo.10cg.pub/10CG/Aria/issues/73) — bundled per `feedback_sister_bug_bundling` (same module surface: `aria/skills/state-scanner/scripts/collectors/`)
> **Plugin version**: 1.21.3 → 1.21.4 (PATCH per CLAUDE.md SemVer)
> **Predecessor patch**: `2026-05-13-aria-issue-101-status-normalize` (v1.20.0; same module — `_status.py` shared author)
> **Effort baseline**: ~2h actual (single-session ship: A→B→C→D)
> **Created**: 2026-05-20

---

## Why

Two independent state-scanner bugs share the same module surface (`scripts/collectors/`), satisfying the sister-bug bundling discipline. Both are confirmed in current code (post-v1.21.3); both have low blast radius (file-scoped fix); both have natural regression-test homes (existing test suite or new stdlib test).

### Bug 1 (#61): `scan.py` crashes on Windows CJK locale

```
File "scripts/collectors/_common.py", line 37 in _run:
  p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, ...)
                                                              ^^^^^^^^^^
UnicodeDecodeError: 'gbk' codec can't decode byte 0xaf in position 17: illegal multibyte sequence
```

**Root cause**: `subprocess.run(..., text=True)` without explicit `encoding=` falls back to `locale.getpreferredencoding()`, which is `gbk` on Chinese Windows. Git output of commit messages containing CJK characters or emoji (mandated by aria-standards `git-commit.md` 双语规范) is UTF-8, so decode fails. Bug surface = every git subprocess call (commits / status / submodule / branch / etc.) — effectively 100% of `scan.py` runs on Chinese Windows.

**Secondary failure**: when `UnicodeDecodeError` escapes the reader thread, `subprocess.run` returns with `stdout=None`. Downstream callers (e.g. `_collect_recent_commits` at `git.py:187`) call `.splitlines()` on None → `AttributeError` → scan.py exit 30.

**Blast radius**: Windows owners cannot use state-scanner at all in CJK locale. Cross-platform regression first reported 2026-05-02 (`#61`); incidentally untouched by intervening v1.20.0 #101 fix because #101 modified `_status.py`, not `_common.py`.

### Bug 2 (#73): transitional status mis-classifies to `pending`, causing secondary false-positives

Original report (2026-05-04, against v1.20.0 pre-#101) was `Implementation-Complete-Pending-Obs → done → false-positive pending_archive`. The v1.20.0 #101 fix incidentally moved `pending` family above `done` fallback in priority order, so the symptom now reads:

```python
_normalize_status("Implementation-Complete-Pending-Obs") → "pending"
```

`pending_archive` rule no longer fires (the original reported false-positive is gone), **but a different downstream consumer breaks**: `requirements.py:56` filters `status ∈ {in_progress, ready, pending}` to surface user-facing "待处理 Story" lists. A transitional spec/story labeled `Implementation-Complete-Pending-Obs` will now appear as a **待开始/待启动 work item** — wrong category, misleading recommendation surface.

**Root cause**: `_normalize_status` has no rule for transitional states. SKILL.md token dictionary already declares `implemented` as the canonical lifecycle slot for *"post-merge, awaiting verify/archive"* — the exact semantic of `Implementation-Complete-Pending-Obs`. But the current token regex matches only `\bimplemented\b`, which doesn't match the `Implementation-` prefix variant.

**Real-world hit** (Aether 2026-05-04, per `#73` body): `migrate-docker-data-root-to-local-ssd` Spec with 24h observation window — should surface as `implemented` (waiting for obs PASS → archive), not `pending` (which would suggest restarting work).

---

## What

### In scope

1. **Fix Bug 1** (`scripts/collectors/_common.py:_run`):
   - Add `encoding="utf-8"` + `errors="replace"` to the `subprocess.run` call (matches the defensive pattern already used at `openspec.py:38`, `readme.py:30`, `upm.py:335`)
   - Add `UnicodeDecodeError` to the `except` chain (returns `(125, "", f"decode error: {e}")`, mirrors `TimeoutExpired` / `FileNotFoundError` softening — never raises out of `_run`)

2. **Fix Bug 2** (`scripts/collectors/_status.py:_normalize_status`):
   - Add transitional-state recognition: tokens `implementation-complete` / `implementation-done` map to `implemented` (already an existing lifecycle state, no schema change)
   - Priority position: AFTER `pending` family (preserves `Draft pending lawyer review` semantics) but BEFORE in-progress family (so `Implementation-Complete-Pending-Obs` resolves before `Pending-Obs` could match `pending` family)
   - Implementation hint: extend the `_has_token` check for `implemented` to also try multi-word variants `implementation-complete` and `implementation-done` (hyphenated literal, treated as a phrase)

3. **Regression tests** (`aria/skills/state-scanner/tests/test_openspec.py::TestStatusNormalizationIssue101Fix` extension):
   - `test_issue73_implementation_complete_pending_obs → implemented`
   - `test_issue73_implementation_done_with_narrative → implemented`
   - `test_issue73_does_not_collide_with_unimplemented` (shadow guard)
   - `test_issue73_pending_archive_does_not_fire_for_implemented` (downstream invariant)

4. **Smoke for #61** (new stdlib test or in-line behavioral assertion):
   - Direct call to `_run(["echo", "中文测试"], cwd=Path("."))` with environment forced to GBK if possible (or `LC_ALL=zh_CN.GBK` if test runner supports); verify rc=0 + stdout decodes cleanly
   - Per `feedback_python_script_importlib_smoke`: importlib dynamic load + direct invocation

5. **Plugin version bump** (5 files per CLAUDE.md SoT discipline):
   - `aria/.claude-plugin/plugin.json` (1.21.3 → 1.21.4, SOURCE OF TRUTH)
   - `aria/.claude-plugin/marketplace.json` (version + plugins[].version)
   - `aria/VERSION`
   - `aria/CHANGELOG.md` (new `## [1.21.4]` entry)
   - `aria/README.md` (version-string reference)

### Out of scope

- New lifecycle states beyond `implemented` (no `verifying` / `monitoring` — those were out-of-scope in #101 too; same boundary)
- Refactor of `_run` signature beyond minimal fix (the existing `tuple[int, str, str]` contract is preserved)
- Cross-collector encoding sweep (only `_run` is the locale-sensitive surface — other readers already specify `encoding="utf-8"`)
- Windows-specific test runner (mocking GBK is sufficient — no CI matrix expansion)
- AB benchmark (per `feedback_level2_patch_no_benchmark` — Level 2 + Skill logic change → smoke benchmark suffices, not full `/skill-creator` AB)
- Touching `aria-orchestrator` / `standards` submodules — fix is fully contained in `aria/`

### Fix sketch

#### Bug 1 fix (`_common.py:_run`)

```python
def _run(cmd: list[str], cwd: Path, timeout: int = 5) -> tuple[int, str, str]:
    """subprocess wrapper: returns (rc, stdout, stderr). Never raises on non-zero rc."""
    try:
        p = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            encoding="utf-8",        # NEW: force UTF-8 (matches git output);
            errors="replace",        # NEW: never raise on partial bytes
            timeout=timeout,
            check=False,
        )
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        return 124, "", f"timeout after {timeout}s: {e}"
    except FileNotFoundError as e:
        return 127, "", f"command not found: {e}"
    except UnicodeDecodeError as e:  # NEW: defensive — shouldn't fire with errors="replace"
        return 125, "", f"decode error: {e}"
```

#### Bug 2 fix (`_status.py:_normalize_status`)

```python
# Pending family (existing — unchanged)
for token in ("draft", "pending", "placeholder"):
    if _has_token(low, token):
        # NEW: but check transitional override first — Implementation-Complete-Pending-Obs
        # is semantically `implemented`, not `pending`. Hyphenated phrase variants
        # (`implementation-complete`, `implementation-done`) take precedence over
        # naked `pending` token match in the same string.
        if "implementation-complete" in low or "implementation-done" in low:
            return "implemented"
        return "pending"

# ... unchanged through `approved`, `implemented` (single-token), etc.
```

Alternative (cleaner): introduce a separate transitional check ahead of pending family:

```python
# Transitional family — hyphenated multi-word, semantically `implemented`
# (post-merge, awaiting obs window / verify / archive). #73 fix 2026-05-20.
for phrase in ("implementation-complete", "implementation-done"):
    if phrase in low:
        return "implemented"

# Pending family (unchanged)
for token in ("draft", "pending", "placeholder"):
    ...
```

Preferred: the alternative (cleaner separation of concerns, matches existing `in_progress` multi-word pattern at lines 92-94).

---

## Acceptance (Phase B complete when)

- [ ] `_run` accepts UTF-8 git output without `UnicodeDecodeError`; mock test passes
- [ ] `_normalize_status('Implementation-Complete-Pending-Obs')` returns `'implemented'` (not `'pending'` and not `'done'`)
- [ ] `_normalize_status('Implementation-Done (24h obs PASS)')` returns `'implemented'`
- [ ] Shadow guards: `_normalize_status('Unimplemented')` and similar negative cases still resolve correctly
- [ ] `pending_archive` rule does NOT fire for `implemented` status (already true per #101 fix; verified by regression test)
- [ ] `requirements.py` surfacing rules do NOT include `implemented` specs in "待处理" surfaces (already true per existing filter `status ∈ {in_progress, ready, pending}`; verified by smoke)
- [ ] All existing 13+ tests in `TestStatusNormalizationIssue101Fix` still pass
- [ ] Plugin 5-file version bump consistency check (every file shows `1.21.4`)
- [ ] aria-plugin PR merged + Aria main submodule pointer bumped
- [ ] Forgejo issues #61 + #73 closed with release reference

---

## Rollback

| Failure | Rollback |
|---|---|
| #61 fix breaks non-CJK locale tests | Revert `_common.py` only (Bug 2 fix independent; ship Bug 2 in v1.21.5 separately) |
| #73 fix breaks existing #101 tests | Revert `_status.py` only (Bug 1 fix independent) |
| Both fixes pass but version-bump mismatch | Re-run version bump checklist; revert mismatched files |

---

## Cross-references

- Bug source: [#61](https://forgejo.10cg.pub/10CG/Aria/issues/61), [#73](https://forgejo.10cg.pub/10CG/Aria/issues/73)
- Predecessor: [openspec/archive/2026-05-13-aria-issue-101-status-normalize/](../../archive/2026-05-13-aria-issue-101-status-normalize/) (v1.20.0 #101 fix — same `_status.py` module; incidentally migrated #73 symptom from `done` to `pending` but did not close the semantic gap)
- Sister patches (precedent for sister-bug bundle pattern):
  - `2026-04-26-aria-v1.17.4-validator-i18n-and-audit-filename-uniqueness/`
  - `2026-04-26-aria-v1.17.5-finding-id-hash-and-stability-gate/`
- Feedback memories applied:
  - `feedback_sister_bug_bundling` — bundle rationale
  - `feedback_level2_patch_no_benchmark` — Level 2 + smoke (not full AB)
  - `feedback_python_script_importlib_smoke` — smoke pattern
  - `feedback_smoke_vs_full_ab_benchmark` — smoke sufficient for code change
  - `feedback_validator_repo_drift_guard_test` — regression test pairs with fix
- SKILL.md token dictionary: `aria/skills/state-scanner/SKILL.md` §"Status 字段最佳实践"
- Downstream consumers verified:
  - `pending_archive` rule (`openspec.py`)
  - `requirements.py:56` priority items filter

---

**Drafter**: AI (Phase A.1 single-session draft, 2026-05-20)
**Owner OD pending**: Approve to proceed Phase B (or amend scope)
