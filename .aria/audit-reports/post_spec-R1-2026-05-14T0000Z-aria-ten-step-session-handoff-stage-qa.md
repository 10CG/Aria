---
checkpoint: post_spec
mode: convergence
round: 1
change_id: aria-ten-step-session-handoff-stage
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
vote: PASS_WITH_WARNINGS
timestamp: 2026-05-14T00:00Z
context: openspec/changes/aria-ten-step-session-handoff-stage/
agent: aria:qa-engineer
r1_findings_total: 9
r1_critical: 1
r1_major: 4
r1_minor: 4
adaptive_level: 2
---

# aria-ten-step-session-handoff-stage post_spec R1 (QA) — 2026-05-14T00:00Z

> **Agent**: aria:qa-engineer
> **Vote**: PASS_WITH_WARNINGS
> **Focus**: test coverage, acceptance criteria measurability, edge cases, risk surface
> **Next**: Apply Critical + Major findings before A.3 agent assignment

---

## Vote

PASS_WITH_WARNINGS — 1 Critical (schema version lockout regression, blocks T1.4 as written), 4 Major (hook testability gap, benchmark tautology, migration idempotency unspecified, T8 severely under-estimated). No showstopper architectural concerns. Spec is structurally sound; findings are scoped corrections, not redesigns.

---

## Critical (1)

### QA-C1: SKILL.md schema version assertion creates hard lockout regression during rollout

**Location**: `aria/skills/state-scanner/SKILL.md` line 155 (current) + `tasks.md` T1.4

**Problem**: The current SKILL.md Phase 2 entry assertion is:

> 值 != `"1.0"` → abort, 提示 "scan.py schema 版本 (X.Y) 与 SKILL.md 契约 (1.0) 不兼容, 请升级 aria-plugin"

T1.4 proposes updating this to "accept `"1.0"` OR `"1.1"`". However, the spec treats this as a soft documentation edit without specifying the **temporal ordering risk**:

- If `scan.py` is updated to emit `"1.1"` (T1.2) before `SKILL.md` receives its assertion update (T1.4), any invocation of `/state-scanner` during the B-phase window will hit the hard abort. This is a real risk in multi-repo releases where aria-plugin submodule and SKILL.md update in separate commits across a multi-hour development window.
- Conversely, if SKILL.md accepts `"1.0"` OR `"1.1"` before `scan.py` emits `"1.1"`, the assertion change is a safe no-op. But the tasks do not specify this ordering constraint.
- T1.2 and T1.4 are listed under the same task (T1), but there is no explicit "T1.4 must land in the same commit as or before T1.2" guard anywhere in tasks.md.

**Additional concern**: T1.4 says "transition period soft accept" but there is no deprecation plan for when `"1.0"` acceptance is removed. Without a tracking mechanism (comment in SKILL.md, follow-up issue, or explicit date), this "soft accept" can persist indefinitely and the schema version gate becomes permanently weakened.

**Required fix**:
1. Add ordering note to T1: "T1.4 SKILL.md assertion update must be committed in the same commit as or before T1.2 scan.py version bump."
2. Add a tracking stub to T1.3 (schema doc): document the `"1.0"` deprecation timeline, e.g., "1.0 deprecated at v1.21.0; removal target v1.23.0 or after 60 days with zero `"1.0"` reports."

---

## Major (4)

### QA-M1: Hook smoke test (T3.4 / T7.3) is not unit-testable as specified; no testing framework exists for PreToolUse hooks

**Location**: `tasks.md` T3.4, T7.3

**Problem**: T3.4 specifies "temp test that attempts Write `.aria/handoff/test.md` → expect hook block." T7.3 adds "in sandboxed test repo." PreToolUse hooks are runtime events dispatched by the Claude Code harness to a running hook subprocess — they are not callable from Python `unittest` or any in-process test framework.

Examination of existing hooks shows: `aria/hooks/hooks.json` contains only a `SessionStart` shell hook (`session-start-check.sh`). There are no existing PreToolUse hooks, and no test infrastructure for hooks anywhere in `aria/skills/state-scanner/tests/` or `aria/hooks/`. The AB_TEST_OPERATIONS.md §Hook 型 Skill describes a LLM with/without approach for hooks (e.g., tdd-enforcer), not unit test simulation.

The `tdd-enforcer` SKILL.md references PreToolUse but has no test files under `aria/skills/tdd-enforcer/` that unit-test the hook intercept itself.

**What "smoke test" actually means for PreToolUse**: Either (a) a shell script that calls the hook subprocess directly with a synthesized event JSON payload, or (b) an LLM eval (via `/skill-creator`) that simulates the write attempt. Neither is specified.

**Required fix**:
1. T3.4 / T7.3: Replace "unit test / sandboxed test repo" framing with an explicit hook integration test approach: either a shell script (`tests/test_hook_handoff_guard.sh`) that invokes the hook handler with a synthetic `{"tool_name":"Write","tool_input":{"file_path":".aria/handoff/test.md"}}` payload, or acknowledge that hook behavior is validated via LLM eval (Rule #6 benchmark T8.2).
2. Clarify what the success criterion actually asserts: does the exit code of the hook subprocess block the write? Document the expected hook response format (JSON `{"decision":"block","reason":"..."}` vs non-zero exit code).

### QA-M2: T8.2 benchmark is tautological as a structural metric — measuring field presence when the collector added the field

**Location**: `tasks.md` T8.2; `proposal.md` §Tests & Dogfood

**Problem**: T8.2 specifies:

> Structural metric: snapshot 含 `handoff` 字段 (with collector) vs 不含 (without collector) — deterministic +100%

This is tautological. The question "does adding the `handoff.py` collector add the `handoff` field to the snapshot?" has a deterministic answer of yes by construction — it is not a quality measure, it is a smoke check that scan.py imports and invokes the new module. The `feedback_rule6_framing_differs_by_skill_type` memory establishes that structural Skills need structural metrics, but the metric must measure meaningful improvement, not tautological field presence.

The meaningful quality questions for this collector are:
- Does `latest_path` correctly identify the most-recently-modified file when multiple files exist with equal-second mtime? (accuracy)
- Does `age_hours` match the expected value within tolerance? (correctness)
- Does `misplaced_files` detect `.aria/handoff/*.md` correctly when the directory contains a mix of `.json` and `.md` files? (precision/recall)
- Does state-scanner Phase 2 correctly surface a handoff-drift recommendation when `misplaced_files != []`? (end-to-end integration)

The "with collector vs without collector" framing is only meaningful if the eval cases include fixture projects where `misplaced_files != []` and the recommendation output is compared — measuring whether the AI's Phase 2 recommendation correctly includes a drift-migration workflow vs. missing it entirely.

**Required fix**: Reframe T8.2:
- Keep: deterministic pre/post unit test pass rate (T7.1 test suite), as precedent from `2026-05-13-state-scanner-issue-101-fix` benchmark.
- Replace "field presence +100%" with: "collector accuracy on mtime sort correctness + misplaced detection precision (all T7.1 cases passing = +100% from 0 baseline)".
- For LLM component: if Phase 2 recommendation accuracy is the metric, specify 2-3 eval cases (one with `misplaced_files != []`, one without) and the expected recommendation output.

### QA-M3: Migration is not specified to be idempotent; partial failure has no rollback plan

**Location**: `tasks.md` T6; `proposal.md` §Migration success criteria

**Problem**: T6.1 specifies `git mv .aria/handoff/*.md docs/handoff/` as a shell glob. This is not idempotent. If run twice (e.g., after a partially-applied migration where some files moved and the command was interrupted), the glob will fail because `.aria/handoff/` no longer exists, but there is no verification that the first run completed cleanly.

More specifically:
- T6.5 verifies `wc -l == 14`. This count assumes exactly 8 pre-existing + 6 migrated files. If `docs/handoff/` already contains files named identically to any of the 6 migrated files (unlikely but possible after a partial run), `git mv` will conflict and abort. There is no spec for what to do if the count is not 14.
- `docs/handoff/latest.md` is a pointer file, not a `.md` handoff doc. T6.5 counts it in the 14. If `latest.md` is included in the `wc -l` count, then the math is: 7 handoff docs + 1 `latest.md` in `docs/handoff/` + 6 migrated = 14. If `latest.md` is excluded, the count is 13. The spec does not clarify whether `latest.md` is a `.md` counted by `ls docs/handoff/*.md | wc -l`.
- No rollback plan is specified for partial migration failure (e.g., 3 of 6 files migrated, command interrupted).

**Required fix**:
1. Add idempotency note to T6: verify `.aria/handoff/` exists before running `git mv`, and add a check that no destination file already exists.
2. Clarify the `wc -l == 14` count in T6.5: does it include `latest.md`? Expected breakdown: `{7 docs/handoff docs} + {latest.md} + {6 migrated}`. If `latest.md` is `.md`, count is 14. Confirm.
3. Add a one-line rollback: "If migration partially fails: `git checkout HEAD -- .aria/handoff/` to restore source, then `git rm docs/handoff/<migrated-files>` to clean target."

### QA-M4: T8 effort estimate (1h) is severely under-estimated; multi-repo release cycle is 2-4h alone

**Location**: `tasks.md` §Estimated effort, T8 row

**Problem**: T8 covers: pre-merge audit (T8.1), Rule #6 benchmark execution (T8.2), Phase C.1 commits across 3 repos (T8.3), Phase C.2 3 PRs with pre-merge gate checks (T8.4), Phase D.2 archive (T8.5), v1.21.0 release with 5+1 SOT file updates + tag + multi-remote push (T8.6), and Phase D.3 dogfood handoff (T8.7).

Evidence from CLAUDE.md: "v1.11.1 发版后未推送 GitHub, 市场停留在 v1.11.0" — the multi-remote push alone has been a source of production incidents. The 5+1 SOT file atomic bump + tag + multi-remote push across 3 repos (standards + aria + main Aria) historically takes 2-3h in Phase C alone. Pre-merge gate with aether fallback adds uncertainty. T8.2 benchmark execution via `/skill-creator` requires LLM invocations with result storage. T8.7 dogfood is already listed separately in T7.4 (duplication, adds confusion).

The current 1h estimate makes the cumulative total ~17h appear correct, but masks that T8 is realistically 3-4h. The PERT pessimistic estimate of 20h does not account for T8 expansion.

**Required fix**:
1. Re-estimate T8 at 3h minimum (not 1h). Update cumulative total to 19h, PERT pessimistic to 22h.
2. Note overlap between T7.4 and T8.7 (both describe "write closeout handoff as dogfood"). Deduplicate: T7.4 is the functional verification of D.3 template; T8.7 is the actual cycle closeout handoff. Keep both but clarify the distinction to avoid double-counting in effort estimate.

---

## Minor (4)

### QA-m1: age_hours timezone not specified — UTC vs local creates inconsistent drift detection

**Location**: `tasks.md` T1.1; `proposal.md` §Functional success criteria

**Problem**: `age_hours = (now - mtime) / 3600` — the proposal does not specify whether `now` is `time.time()` (UTC epoch, timezone-agnostic) or `datetime.now()` (local time). Python's `os.stat().st_mtime` returns a POSIX timestamp (UTC epoch seconds), so if `now` is also `time.time()`, the arithmetic is correct and timezone-independent. However, if a developer uses `datetime.now()` without `tz=timezone.utc`, DST transitions can introduce a 1-hour error in `age_hours`, which is material for a "session > 4h" trigger condition threshold.

**Required fix**: Specify in T1.1 explicitly: "use `time.time() - mtime` (POSIX float arithmetic, timezone-agnostic)." Add a test case in T7.1 that mocks `time.time()` to a known value and asserts `age_hours` is correct to 2 decimal places.

### QA-m2: L3 recommendation acceptance criterion uses subjective "展示" — not deterministically verifiable

**Location**: `proposal.md` §Functional success criteria, line 167: "state-scanner Phase 2 推荐展示 handoff path 与 age"

**Problem**: "展示 handoff path 与 age" is a human-judgment criterion. There is no assertion on what substring must appear in Phase 2 output, which field value must be present, or which comparison point establishes pass/fail. This is in the Functional section of Success Criteria, which should be deterministic.

**Required fix**: Replace with: "state-scanner Phase 2 output includes `handoff.latest_path` value and `handoff.age_hours` value as documented in `references/output-formats.md`." The `output-formats.md` update (T4.2) then becomes the binding acceptance criterion. This converts a subjective display check into a document-reference check.

### QA-m3: Non-UTF-8 filenames in docs/handoff/ not handled by collector

**Location**: `tasks.md` T1.1; no edge case test specified

**Problem**: `os.listdir()` or `Path.glob()` on Linux returns raw bytes for filenames not decodable as UTF-8. If `docs/handoff/` contains a file with a non-UTF-8 name (e.g., from an OS copy that mangled encoding), `Path.glob("*.md")` will skip it silently on some Python versions or raise `UnicodeDecodeError` on others. The collector uses `pathlib.Path`, which on Linux raises `UnicodeDecodeError` for truly malformed surrogate filenames in some Python 3.x versions.

This is low-probability in practice (handoff files are human-created), but the existing collector pattern (e.g., `collectors/openspec.py` line 38: `errors="replace"` for file content) shows the project does handle encoding defensively for file reads. Filename encoding is not handled.

**Required fix**: Add to T7.1 edge cases: "non-UTF-8 filename in `docs/handoff/` — expect `soft_error` appended, not exception propagation." Add `errors="surrogateescape"` or `try/except OSError` around the glob iteration in T1.1 implementation guidance.

### QA-m4: T7.4 / dogfood bootstrap paradox — D.3 not deployed when this cycle's Phase D runs

**Location**: `tasks.md` T7.4; `proposal.md` §Tests & Dogfood

**Problem**: T7.4 says "本 cycle Phase D 执行 D.3 流程,写 handoff." But D.3 step is added to `phase-d-closer` SKILL.md in T2 — which is implemented in Phase B of this cycle, not deployed to production until Phase C merge + v1.21.0 release. The Phase D of this cycle runs after Phase C, at which point D.3 would be deployed (assuming the cycle completes before the session ends).

This creates a sequencing dependency the spec does not document: T7.4 / T8.7 dogfood can only validate D.3 if the aria-plugin PR has merged and the new `phase-d-closer` SKILL.md is active when Phase D runs. If Phase D runs using the pre-release SKILL.md (e.g., from a cached version), the D.3 step would not be present and the dogfood would produce a false negative.

The trigger condition check: "本 session 跨 ≥ 2 phases" — this session (H0) covers A+B+C+D, satisfying the trigger. No bootstrap concern on trigger. The concern is deployment timing.

**Required fix**: Add to T7.4: "Prerequisite: aria-plugin PR merged and v1.21.0 released (T8.6 complete) before Phase D.3 execution. If Phase D runs pre-release, manually invoke D.3 template as manual dogfood and note in handoff as 'pre-release manual validation'."

---

## Observations

**OBS-1**: T3.1 duplicates "Write OR Edit OR Write" (Write appears twice) — likely copy-paste error. Fix in T3.1 before implementation: "Match tool_name: Write OR Edit."

**OBS-2**: The `proposal.md` §Success Criteria Migration section says `wc -l == 14` but the migration uses `git mv *.md` which would include `latest.md` from `.aria/handoff/` if it exists. Current `.aria/handoff/` contains 6 files (none named `latest.md`). `docs/handoff/` contains 8 files including `latest.md`. So the 14 count (8 + 6) correctly includes `latest.md` from the existing `docs/handoff/` set. This is consistent but should be explicitly stated.

**OBS-3**: The layered defense matrix shows L1 fires on Write/Edit to `.aria/handoff/*.md`. After T6 migration, `.aria/handoff/` does not exist. A new `mkdir .aria/handoff/ && touch .aria/handoff/test.md` would be Bash tool calls (not Write/Edit), so L1 would not fire. L2 (collector) would detect the new file on next scan. The spec correctly notes this in the §Impact Risk row but the enforcement matrix should note that L1 fires on AI write tools only, not on shell tool creates.

**OBS-4**: `tasks.md` T8.3 lists commit messages for `aria` (plugin) as 4 separate commits, but T8.4 creates 3 PRs. If all 4 commits go into one PR for the aria submodule, the PR title will be ambiguous. If they go into separate branches/PRs, that is not stated. Clarify PR-to-commit grouping in T8.4.

---

## Verdict

**PASS_WITH_WARNINGS** — QA engineer vote.

The spec has one Critical finding (QA-C1, schema version ordering creates hard lockout regression risk) and four Major findings. None require architecture redesign. The Critical and Majors are all in the "specification gap" category — missing ordering constraints, missing test infrastructure clarity, mis-estimated effort — not fundamental design problems.

The spec is implementable as written with these corrections applied. Recommend proceeding to R2 only if another audit agent raises additional Critical findings; otherwise apply inline fixes to tasks.md and advance to A.3.

**Convergence vote**: NO (Critical open, Major QA-M2 requires benchmark reframe before T8.2 implementation)
