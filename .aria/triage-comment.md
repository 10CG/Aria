## Triage Report

**Verdict**: `partial-repro` | **Severity**: `minor` | **Recommended Action**: `next-cycle`

---

### Version

| Field | Value |
|-------|-------|
| Reported | `1.17.3` |
| Current | `1.19.0` |
| Gap | `behind` (+2 minor versions) |

Issue was filed against v1.17.3; current release is v1.19.0. The bug is present in both versions — this is not an outdated report. The `_normalize_status` logic has not changed between these versions (Step 4 git log confirms no relevant fix commits).

### Code Path

`aria/skills/state-scanner/scripts/collectors/_status.py` (prose citation, L58-60):

- File exists at path `aria/skills/state-scanner/scripts/collectors/_status.py` — confirmed present
- Line 58-60 snippet retrieved: `for token in ("done", "complete"): if token in low: return "done"` — matches issue description exactly
- Note: the issue also uses bare `skills/state-scanner/scripts/collectors/_status.py` (without `aria/` prefix) — that path does not exist; the full path with `aria/` prefix is the correct citation

The code path verification confirms: `"done"` and `"complete"` substring checks execute at lines 58-60, **before** the `"approved"` check at line 64. Any Status string containing the substring `"done"` will short-circuit and return `"done"` regardless of other tokens in the string.

### Git History

`git log -n 20 --oneline -- aria/skills/state-scanner/scripts/collectors/_status.py` returned:

- `47c9a57` feat(state-scanner): i18n status regex — fullwidth colon + inline blockquote
- `b8db9a0` refactor(state-scanner): T3 prep — split scan.py into collectors/ package

**No recent commits matched fix-related keywords** (`fix`, `resolve`, `normalize`, `bugfix`). `likely_fix_candidates: []`. The substring matching order logic has not been patched.

### In-flight

| Category | Matches |
|----------|---------|
| Remote PRs | none (0 open PRs keyword-matched on `101` / `normalize` / `_status`) |
| Local branches | none |
| Worktrees | `feature/aria-issue-triage-sop` (current worktree — unrelated to bug fix) |

No in-flight fix work found. Starting a new fix cycle will not create duplicate work.

### Reproduction

**Mode**: `auto` | **Hit rate**: `2/4`

Executed: `python3 -c "from _status import _normalize_status; ..."` against current `aria/skills/state-scanner/scripts/collectors/_status.py`.

| case_id | Input (Status raw string) | Expected behavior | Actual behavior | Match | Notes |
|---------|--------------------------|-------------------|-----------------|-------|-------|
| case-1-docs-marketplace | `Approved (Rev2 CONVERGED) — Phase A done, ready for Phase B` | `approved` (Phase B not started) | `done` (substring hit) | false | PRIMARY BUG — "done" token at L58 evaluated before "approved" at L64; `done` substring wins |
| case-2-existing-data-migration | `Implemented (Phase B PR-A merged 2026-05-10 main fce87bc) — post-deploy 验证后归档` | `done` (issue claims pending_archive hit) | `unknown` | false | SECONDARY BUG — `Implemented` not in any token list; returns `unknown` not `done`; different root cause than issue describes |
| case-3-pricing-marketplace-redo | `Implemented (Phase B PR-A merged 2026-05-10 main 6160d18) — UAT PASS; post-monitoring 后归档` | `done` (issue claims pending_archive hit) | `unknown` | false | SECONDARY BUG — same as case-2; `Implemented` missing from token dict |
| case-4-terms-of-service | `⏸ DRAFT pending lawyer review — Phase B PR-A done 2026-05-09 commit eb49e77` | `pending` or `draft` (lawyer-blocked, not done) | `done` (substring hit) | false | PRIMARY BUG — "done" token at L58 evaluated before "pending"/"draft" at L72; `done` substring wins |

**Summary**: cases 1 and 4 reproduce the primary substring-ordering bug exactly as described. Cases 2 and 3 hit a *different* bug (`Implemented` not mapped in the token dictionary → `unknown`), which the issue does not describe and which is a secondary/adjacent defect.

**Deviation from issue claim**: Issue reports all 4 cases as `pending_archive` hits via the `done` substring bug. Actual repro: 2/4 confirm the primary `done` substring ordering bug; 2/4 (`Implemented` cases) hit a secondary `unknown` mapping gap that the issue does not describe.

### Verdict Rationale

Verdict is **`partial-repro`** because:

1. The core bug is real and reproducible (2/4 confirmed: `"done"` token checked before `"approved"` and `"pending"` — substring `done` in Status narrative overrides intended semantic). This is a genuine defect requiring a fix.
2. However, the issue self-reports 4/4 hit rate for the `done` substring mechanism. The actual mechanism for cases 2 and 3 is different (`Implemented` not in token dictionary → `unknown`, not `done`). These cases end up in `pending_archive` for a *different* reason or may not appear there at all depending on scanner logic.
3. The `partial-repro` verdict forces the fix scope to cover both the primary (substring ordering) and secondary (missing `Implemented` token) bugs, rather than narrowly patching only what was described.

**deviation_note**: Issue self-reports 4/4 hit rate for the `done` substring ordering bug. Actual repro: 2/4 confirm primary bug (`done` token fires before `approved`/`pending` — cases 1 and 4). 2/4 (`existing-data-migration`, `pricing-status-marketplace-redo`) hit a secondary bug: `Implemented` is not in any token list and returns `unknown`, not `done`. Both are real defects in `_normalize_status` but they have different root causes. Fix scope must cover both (a) substring ordering/word-boundary for `done`, and (b) missing `Implemented` lifecycle token mapping.

---

*Generated by `/issue-triage` v1.19.0 — Ref: 10CG/Aria#101*
*Step 6 performed by AI (auto mode) — 2026-05-13*
