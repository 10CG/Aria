# Pre-merge Audit R1 — H0 aria-ten-step-session-handoff-stage (backend-architect)

**Date**: 2026-05-14
**Round**: R1
**Auditor role**: backend-architect
**Branch**: feature/aria-ten-step-session-handoff-stage
**Target**: aria-plugin v1.21.0 MINOR
**Verdict**: PASS_WITH_WARNINGS

---

## Findings

### Critical

None.

---

### Major

**M1 — Double stat() on `latest` in handoff.py creates unnecessary TOCTOU window**

File: `aria/skills/state-scanner/scripts/collectors/handoff.py:85-86`

```python
latest = max(canonical_files, key=lambda p: p.stat().st_mtime)  # line 85
mtime = latest.stat().st_mtime                                   # line 86 — second call
```

`max()` already calls `p.stat()` on every candidate including the winner, but the result is discarded. Line 86 re-stats the same file. If the file is deleted between lines 85 and 86, the OSError is caught correctly (line 87) — so this is not a correctness bug. However, the window is gratuitous. The cache-free pattern is an efficiency and clarity issue that becomes a real race if filesystems are slow or networked. Prefer:

```python
# Cache the StatResult inside max()
stat_cache: dict = {}
def _stat_cached(p: Path) -> float:
    stat_cache[p] = p.stat()
    return stat_cache[p].st_mtime

latest = max(canonical_files, key=_stat_cached)
mtime = stat_cache[latest].st_mtime
```

Or more simply, use a single try/except around just line 85 and derive mtime from `latest.stat()` once. Rating: Major because it is confusing to reviewers and could silently produce a stale mtime if the OS returns cached metadata inconsistently between two calls (edge case on distributed filesystems). Not a correctness regression in current test environment.

---

**M2 — `stat -c '%Y'` in D.3 `trigger_level_2` command_hint is Linux-only (macOS incompatible)**

File: `aria/skills/phase-d-closer/SKILL.md:367`

```bash
last_handoff_mtime=$(stat -c '%Y' $(ls -t docs/handoff/*.md | head -1))
```

`stat -c` is GNU coreutils syntax. macOS/BSD `stat` uses `stat -f '%m'`. This command_hint is executed by AI agents when evaluating D.3 trigger level 2. On macOS dev environments or macOS-hosted CI, the command will fail silently (exit non-zero) and the fallback chain descends to level 3. This is tolerable because the 4-level fallback is explicitly designed for signal-missing scenarios. However, the hint should document the macOS alternative or use a portable Python fallback:

```bash
# GNU/Linux
last_handoff_mtime=$(stat -c '%Y' "$(ls -t docs/handoff/*.md | head -1)")
# macOS/BSD: stat -f '%m' "$(ls -t docs/handoff/*.md | head -1)"
# Portable: python3 -c "import os,glob; f=max(glob.glob('docs/handoff/*.md'),key=os.path.getmtime); print(int(os.path.getmtime(f)))"
```

Additionally, the `ls -t docs/handoff/*.md` expansion is unquoted and will break on filenames with spaces (low-risk given current naming convention). Rating: Major because it silently degrades D.3 trigger detection on non-Linux platforms without surfacing an error.

---

### Minor

**m1 — `_scan_md_files` UnicodeError guard fires on `UnicodeEncodeError`, not `UnicodeDecodeError` — comment is misleading**

File: `aria/skills/state-scanner/scripts/collectors/handoff.py:39-51`

The docstring says "Skips files whose names cannot be decoded as UTF-8." The guard is:

```python
_ = entry.name.encode("utf-8")
```

On Linux, `Path.iterdir()` uses `sys.getfilesystemencodeerrors() = 'surrogateescape'`, so non-UTF-8 filenames arrive as Python `str` objects containing surrogate escape characters (`\udcXX`). Calling `.encode("utf-8")` on such a string raises `UnicodeEncodeError` (not `UnicodeDecodeError`). The except clause catches the parent class `UnicodeError`, which covers both. The behavior is correct but the docstring says "UnicodeDecodeError" implicitly when the actual exception is `UnicodeEncodeError`. Verified empirically:

```
$ python3 -c "bad='file\udcff.md'; bad.encode('utf-8')"
UnicodeEncodeError: surrogates not allowed
```

Fix: update docstring to "Skips files whose names contain non-UTF-8 bytes (raises UnicodeEncodeError via surrogate escape encoding)."

---

**m2 — `collectors/__init__.py` import of `_common` is not alphabetically sorted relative to other imports**

File: `aria/skills/state-scanner/scripts/collectors/__init__.py:14`

```python
from ._common import CollectorResult, log       # line 14 — underscore sorts before 'a'
from .architecture import collect_architecture  # line 15
```

Underscore prefix `_common` sorts before alphabetic names in Python convention and in ASCII order, so this is actually already correctly sorted. However, the pre-existing style in this file places `_common` first explicitly (consistent with its role as shared infrastructure). `handoff` is inserted at line 21 between `git` and `interrupt`, which is alphabetically correct. No action needed — confirmed correct.

---

**m3 — Hook `EVENT_JSON` passed via env var: no size guard for very large tool events**

File: `aria/hooks/handoff-location-guard.sh:25,33`

```bash
EVENT_JSON="$(cat || true)"
export ARIA_HOOK_EVENT="$EVENT_JSON"
```

Linux `ARG_MAX` is ~3.2 MB total (confirmed: `getconf ARG_MAX` = 3200000). Individual env var values are bounded by `MAX_ARG_STRLEN` (~128 KB on this kernel). A PreToolUse event for a `Write` tool with a large `content` field could exceed this limit, causing `export` to fail or be silently truncated. In practice, Claude Code likely splits large writes, but this is unverified. The fallback is safe: if `ARIA_HOOK_EVENT` is empty or truncated, the Python block falls through to `PASS`. However, truncation without error is harder to diagnose.

Recommendation: add a size guard in the shell script before the export:

```bash
if [ "${#EVENT_JSON}" -gt 65536 ]; then
  # Event too large to pass via env var safely; pass-through (no path match possible)
  exit 0
fi
```

Rating: Minor — real risk is very low given typical PreToolUse event sizes, and failure mode is safe (defaults to PASS, not DENY).

---

**m4 — `hooks.json` PreToolUse matcher `"Write|Edit|NotebookEdit"` — regex alternation not confirmed by Claude Code spec**

File: `aria/hooks/hooks.json:17`

```json
"matcher": "Write|Edit|NotebookEdit"
```

The hooks.json `matcher` field for PreToolUse tool name matching — it is unclear from available documentation whether Claude Code interprets this as a regex alternation or a literal string match. The `SessionStart` matcher uses `"*"` (glob). The `PreToolUse` matcher may use exact tool name matching, regex, or glob, depending on Claude Code's internal routing. If interpreted as a literal string, the hook would never fire (no tool is literally named `"Write|Edit|NotebookEdit"`).

This is a previously-audited item (referenced in hook comment as "G2 audit fix per R2 backend-M2") suggesting prior validation has occurred. However, no test in the current T7 suite validates that the hook actually fires on a real Claude Code `Write` event. If the matcher syntax is wrong, the entire L1 defense layer silently fails.

Recommend: add a smoke test or document the validated behavior (e.g., link to Claude Code hook documentation confirming regex alternation for `matcher`).

---

**m5 — Migration: `latest.md` pointer correctness relies on filesystem mtime, not commit order**

File: `docs/handoff/latest.md`

The migration commit (1de5159) correctly identifies `2026-05-13-issue-101-cycle-closeout.md` as the newest file by mtime (confirmed: `Modify: 2026-05-13 20:31:35` vs `2026-05-13-us025-m5-phase-a-b1-done.md` at `00:26:52`). The Phase 1.15 collector will also surface this file correctly via `max(..., key=lambda p: p.stat().st_mtime)`. Pointer is semantically correct.

Minor note: `latest.md` table is missing the migrated `2026-05-13-issue-101-cycle-closeout.md` in the historical rows (it IS listed as "Active (Latest)" correctly), but the 6 migrated April-era files are shown as "archived" rows at the bottom. Table formatting is consistent. No action needed.

---

### Observations

**O1 — Regex correctness confirmed across all documented cases**

The FORBIDDEN_RE regex `(?:^|[/\\])\.aria[/\\]handoff[/\\][^/\\]+\.md$` with `re.IGNORECASE` was tested against 8 cases. All passed. Notably: `prefix-.aria/handoff/foo.md` correctly does NOT match (hyphen is not a path separator — the `.aria` dir is not reached via a non-separator prefix). Windows backslash paths match correctly. The resolved-path approach (`Path.resolve(strict=False)`) removes symlink-based circumvention.

**O2 — Migration integrity: all 6 renames are R100**

`git log --diff-filter=R` confirms all 6 `.aria/handoff/*.md` → `docs/handoff/*.md` renames at 100% similarity. `.aria/handoff/` directory is absent from filesystem. Migration is clean.

**O3 — Schema version 1.0 unchanged**

`scan.py:69` `SNAPSHOT_SCHEMA_VERSION = "1.0"` — confirmed unchanged. The `handoff` field is additive (new top-level key in snapshot dict). No breaking change.

**O4 — collect_handoff is always-on (not opt-in)**

Unlike `issue_status` (which is gated by `enabled` flag), `handoff` is unconditionally emitted in the snapshot dict. This is correct for Layer 2 drift detection — opt-in would defeat the purpose.

**O5 — Test suite: 11/11 passing, covers all specified edge cases**

`test_handoff.py` covers: mtime DESC sort, age_hours epoch math, misplaced detection, non-.md exclusion, schema keys, UTC ISO suffix, empty dir, missing dir, drift state (both populated). Ran successfully with `python3 -m unittest`. No regression detected.

**O6 — exit2 deny path is correctly exclusive of JSON path**

`handoff-location-guard.sh:106-117` — when `DENY_MODE=exit2`, the script executes `echo "$MESSAGE" >&2; exit 2` and never reaches the `printf | python3` JSON block. The two paths are mutually exclusive. No double-emit bug.

---

## Convergence vote

- [x] **PASS_WITH_WARNINGS** — M1 (double stat) and M2 (stat -c portability) are inline-fixable before merge; m3-m5 are doc/comment clarifications. No Critical findings. No regression detected. L1 hook regex confirmed correct. Migration is clean. Tests pass 11/11.
- [ ] READY_TO_MERGE (0 Critical, 0 Major)
- [ ] FAIL (regression)

**Recommended before merge**:
1. Fix M1: cache stat result from `max()` to eliminate second `p.stat()` call on line 86
2. Fix M2: add macOS-compatible `stat` alternative to D.3 `trigger_level_2` command_hint comment
3. Fix m1: correct docstring in `_scan_md_files` from "UnicodeDecodeError" to "UnicodeEncodeError (via surrogateescape)"

M1+M2+m1 are all single-line doc/code fixes, no test changes required.

---

## Summary

The H0 implementation is structurally sound across all five audit scope areas. Collector correctness is strong: mtime sort, age_hours math, misplaced detection, OSError soft-error path, and schema-1.0 invariant all verified. The hook regex correctly matches all intended paths including Windows separators, and the exit2/json deny paths are mutually exclusive. Migration integrity is confirmed: 6 R100 renames, `.aria/handoff/` directory removed, `latest.md` pointer semantically correct by mtime comparison. The `handoff` key is always-on in the snapshot dict and correctly appended to errors aggregation. Two Major findings require inline fixes before merge: a double stat() call on lines 85-86 that creates a gratuitous TOCTOU window, and a Linux-only `stat -c '%Y'` command_hint in D.3 that silently degrades trigger detection on macOS. Neither is a correctness regression in the target Linux environment but both should be addressed. Three minor findings (docstring accuracy, env var size guard, hooks.json matcher documentation) are advisory. Tests 11/11 pass.
