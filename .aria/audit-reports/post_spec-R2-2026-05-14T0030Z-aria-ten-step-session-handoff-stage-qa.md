---
checkpoint: post_spec
mode: convergence
round: 2
change_id: aria-ten-step-session-handoff-stage
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
vote: PASS_WITH_WARNINGS
timestamp: 2026-05-14T00:30Z
context: openspec/changes/aria-ten-step-session-handoff-stage/
agent: aria:qa-engineer
r1_findings_total: 9
r1_critical: 1
r1_major: 4
r1_minor: 4
r2_verified_resolved: 6
r2_partially_resolved: 1
r2_new_major: 2
r2_new_minor: 3
adaptive_level: 2
---

# aria-ten-step-session-handoff-stage post_spec R2 (QA) — 2026-05-14T00:30Z

> **Agent**: aria:qa-engineer
> **Vote**: PASS_WITH_WARNINGS
> **Focus**: Verify F1-F10 inline fixes resolve R1 findings; probe six R2 sharpening scenarios; identify any new Critical/Major
> **Next**: Two inline fixes required before Phase B kickoff (R2-M1 stale schema refs + R2-M2 hook response format); no R3 required if applied as editorial gate

---

## Vote

PASS_WITH_WARNINGS — QA-C1 fully resolved by F1 (schema never bumps, ordering risk eliminated). QA-M1/M2/M3/M4 substantially resolved with one residual gap each in F7 (hook exit code spec) and F9 (rollback partial-state correctness). Two new Major findings: R2-M1 (stale "schema 1.1" in proposal.md Success Criteria + T8.3 commit template) and R2-M2 (hook test asserts exit code 2 but exit code 2 causes Claude to ignore stderr; correct blocking mechanism is exit 0 + JSON deny). Three new Minor findings. No Critical introduced. All fixes are editorial or one-line corrections; no redesign needed. Treat as pre-Phase-B editorial gate, not a mandatory R3 trigger.

---

## R1 Findings Verification Table

| ID | R1 Finding | Fix | R2 Verdict | Notes |
|----|-----------|-----|-----------|-------|
| QA-C1 | Schema version lockout regression — T1.2 emitting "1.1" before T1.4 SKILL.md update creates hard abort | F1: Removed schema bump entirely; "1.0" forever | ✅ Resolved | T1.1 "No version bump", T1.2 "不修改 `snapshot_schema_version` — 保持 `"1.0"`", T1.5 "不修改阶段 2 入口断言" — the ordering risk is gone because there is nothing to order. Additive field precedent from v1.18.0 G2/G3/G4 correctly cited. |
| QA-M1 | Hook smoke test untestable — no PreToolUse unittest infra | F7: Shell subprocess + synthetic event JSON; new file `tests/test_handoff_hook.sh`; exit code 2 + stderr assert; no Python unittest | ⚠️ Partially resolved | Direction is correct (shell subprocess IS the right approach). However, exit code 2 is specified as success criterion but Claude Code docs confirm exit code 2 causes harness to ignore stdout and feed stderr to Claude as error — it does NOT require JSON output. Test assertion "assert exit code 2 + stderr contains 'must use docs/handoff/'" is technically valid for a hook that uses exit-code-only blocking. But the hook spec (T3.1) is ambiguous: it says "exit code 2 per Claude Code hook spec" without specifying whether the hook emits stderr text or a JSON deny payload. The test and the hook spec need to agree. See R2-M2 for full analysis. |
| QA-M2 | T8.2 benchmark tautological — "field present with/without collector" = trivially +100% | F8: Redefined to structural deterministic metrics: (1) mtime sort accuracy on 5-file fixture; (2) misplaced detection precision/recall on 3 synthetic project fixtures | ✅ Resolved | Tautological metric removed. Replacement metrics are deterministic and meaningful: mtime sort accuracy tests actual ranking logic, misplaced detection precision/recall tests the classification boundary. Both metrics have defined ground truth (fixture files with known mtimes; known dir populations). The benchmark is now a genuine quality signal rather than a smoke check. |
| QA-M3 | Migration idempotency + rollback unspecified | F9: T6.0 pre-check (skip if `.aria/handoff/*.md` empty + collision detect); T6.6 rollback via `git restore --source=HEAD` | ⚠️ Partially resolved | Pre-check and rollback are now present. However, the rollback command `git restore --source=HEAD .aria/handoff/ docs/handoff/` has a correctness issue in the partial-completion scenario. See R2-S4 analysis below. The intent is correct but the command is wrong for the git state at failure time. |
| QA-M4 | T8 effort estimate 1h severely under-estimated | F10: T8 bumped from 1h to 3h; total 17h → 20h | ✅ Resolved | 3h for T8 (pre-merge audit + benchmark + 3-repo Phase C + 3 PRs with gate checks + D.2 archive + v1.21.0 5+1 SOT release + dogfood handoff) is realistic. The PERT table now shows optimistic 17h / likely 20h / pessimistic 24h with a named R3-oscillation trigger. Mid-impl checkpoint at 13h threshold is well-placed. |
| QA-m1 | age_hours timezone unspecified | F8 (minor): T1.1 now explicitly specifies `time.time() - mtime` (UTC epoch float; "F8 minor — 不用 `datetime.now()` 防 timezone/DST") | ✅ Resolved | Implementation guidance is explicit. T7.1 test case "Test age_hours computation (mock `time.time()`, 确认 epoch float 输出)" covers the verification. |
| QA-m2 | L3 recommendation acceptance criterion subjective — "展示 handoff path 与 age" | Not explicitly updated in proposal.md Success Criteria | ⚠️ Partially resolved | proposal.md Success Criteria §Functional still reads "state-scanner Phase 2 推荐展示 handoff path 与 age (output-formats.md 文档化)". The parenthetical "(output-formats.md 文档化)" chains to T4.2 which creates the binding reference document. This is an improvement over the original but "展示" remains the operative verb. The criterion is now document-backed (T4.2) rather than subjective display-only. Acceptable as-is; T4.2's output-formats.md will provide the binding assertion text. Low residual risk. |
| QA-m3 | Non-UTF-8 filenames not handled | F8 (minor): T7.1 test case "non-UTF-8 filename in `docs/handoff/` → 跳过 file, emit warning to `errors[]`" added | ✅ Resolved | Both the implementation guidance (T1.1 edge cases) and the test case are present. The `errors[]` emission pattern aligns with existing collector error handling. |
| QA-m4 | T7.4 dogfood bootstrap paradox — D.3 not deployed when Phase D runs | F8 (minor): T7.4 clarified: "本 cycle 期间手动模拟 D.3 step, 因为 plugin 尚未 ship to local cache; D.3 流程 deployment 是 v1.21.0 ship 的副作用, not pre-req for dogfood" | ✅ Resolved | The temporal sequence is now explicit: T1-T8 land + PR merged + v1.21.0 tagged → then dogfood. Manual simulation during B-phase is acknowledged as the pre-release validation path. |

---

## R2 Sharpening Analysis — Six Scenarios

### Scenario 1 (F1 schema fix): Commit ordering walk-through

**Scenario**: T1.1 (new `handoff.py` file, returns plain dict) and T1.2 (scan.py imports + invokes `collectors.handoff`, adds `handoff` key to snapshot) — are these truly independent commits or does import order matter?

**Analysis**: T1.1 creates a new standalone file. T1.2 edits `scan.py` to import and invoke it. There is no circular import: `scan.py` imports `collectors.handoff`; `collectors.handoff` imports nothing from `scan.py`. If T1.2 lands before T1.1 (unlikely in a single-developer context but possible in a multi-agent Phase B scenario where backend-architect implements both), `scan.py` would have an unresolvable import and fail at runtime.

**Verdict**: The spec does not specify "T1.1 must commit before T1.2" but in practice they will be in the same branch and likely the same commit or consecutive commits. Since schema version is not changing, there is no harness-level abort risk. The ordering risk from QA-C1 is fully eliminated. The remaining import-order constraint is a standard Python dependency that any competent implementer handles naturally. No new finding; QA-C1 resolution holds.

### Scenario 2 (F7 shell subprocess test): Does Claude Code pass tool_input as JSON to the hook script?

**Verification**: WebFetch of official Claude Code hooks documentation (https://code.claude.com/docs/en/hooks) confirms:

- PreToolUse hook commands receive JSON via **stdin** (not environment variables, not argv)
- The JSON payload structure includes `tool_name`, `tool_input`, `hook_event_name`, `session_id`, `cwd`, `tool_use_id`
- For the Write tool: `tool_input = {"file_path": "/path/to/file", "content": "..."}`
- For the Edit tool: `tool_input = {"file_path": "/path/to/file", "old_string": "...", "new_string": "...", "replace_all": false}`

**Assessment of F7**: The shell test `test_handoff_hook.sh` constructs a synthetic JSON payload and pipes it to the hook script. This is the correct mechanism. The test's assumption that `tool_input.file_path` contains the path for both Write and Edit tools is verified correct.

**However**: The blocking mechanism in T3.1 and T3.4 specifies "exit code 2". Claude Code docs confirm exit code 2 for PreToolUse blocks the tool call AND causes the harness to ignore stdout, feeding stderr to Claude as an error message. This means:
- If the hook uses exit code 2: stderr text reaches Claude; JSON on stdout is ignored.
- If the hook uses exit 0 + JSON `{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "..."}}`: structured deny with reason text.

The existing `session-start-check.sh` hook uses exit 0 and emits JSON to stdout (SessionStart, not PreToolUse). This is a different event type. There are no existing PreToolUse shell hooks in the repo to compare against.

**The test in T3.4 asserts**: "exit code 2 + stderr contains 'must use docs/handoff/'". This assertion is internally consistent IF the hook script is implemented with exit code 2 + stderr output. But T3.1 says "exit code 2 per Claude Code hook spec" as if exit code 2 is the formally prescribed mechanism, when the docs show exit 0 + JSON deny is the preferred structured approach. The T3.2 error message block will work as stderr text under the exit-code-2 approach.

**Conclusion**: F7 is structurally sound (stdin JSON piping is correct) but the hook blocking mechanism is underspecified. The test and hook can be implemented consistently with either approach, but the spec does not commit to one. This creates ambiguity for the Phase B implementer. Raised as R2-M2.

### Scenario 3 (F8 benchmark fixtures): Real filesystem touch -t or in-memory mock?

**Analysis**: T8.2 specifies "fixture set 含 5 个 dated handoff files with known mtimes → assert latest detected == newest mtime". The spec does not clarify whether the fixture uses `touch -t YYYYMMDDHHmm` on a real filesystem or an in-memory mock.

The T7.1 unit test ("Test mtime sort DESC (3 fixture files, 不同 mtime → latest 正确)") uses Python and would naturally use `os.utime()` or `tempfile.NamedTemporaryFile` with explicit mtime patching via `unittest.mock.patch` on `os.stat`. This is reliable and timezone-independent.

The T8.2 benchmark, however, is a Rule #6 `/skill-creator` benchmark, not a Python unit test. The benchmark exercises the LLM (with/without skill) against fixture projects. For the structural deterministic metrics in the redefined T8.2, the benchmark fixture should be filesystem-based (real temp directories with `touch -t` or Python `os.utime()`) to test the actual collector against real `stat()` calls, not mocked.

**Risk**: If the benchmark fixture uses `touch -t` at benchmark run time, mtime resolution is second-granularity and fragile only if two files are created in the same second — unlikely with 5 pre-staged files. If the benchmark fixture uses `os.utime()` with pre-assigned epoch values (e.g., distinct POSIX timestamps days apart), this is robust. The spec does not specify which approach.

**Verdict**: Minor gap. The unit tests in T7.1 will exercise the mtime logic with mocked `time.time()`. The T8.2 benchmark fixture approach should be clarified in T8.2 to avoid timing-fragility. Raised as R2-m1.

### Scenario 4 (F9 rollback): Does `git restore --source=HEAD` work after partial `git mv`?

**Analysis**: The T6.6 rollback plan specifies: "If `git mv` partial fails (某 file 冲突): `git restore --source=HEAD .aria/handoff/ docs/handoff/`"

Walkthrough of what `git mv source dest` does internally:
1. Copies the file from source to dest (filesystem level)
2. Runs `git rm source` (stages the deletion)
3. Runs `git add dest` (stages the addition)

After a partial `git mv .aria/handoff/*.md docs/handoff/` that moves 3 of 6 files before failing:
- The git index (staging area) has: 3 files deleted from `.aria/handoff/`, 3 files added to `docs/handoff/`
- The working tree has: 3 files present in `docs/handoff/`, 3 files remaining in `.aria/handoff/`
- HEAD still has: all 6 files in `.aria/handoff/`, none in `docs/handoff/` (migration not committed)

`git restore --source=HEAD .aria/handoff/ docs/handoff/` behavior:
- `--source=HEAD` restores working tree AND index to HEAD state
- For `.aria/handoff/`: restores the 3 deleted files (unstages the `git rm`, recreates files in working tree)
- For `docs/handoff/`: removes the 3 added files (unstages the `git add`, deletes them from working tree)

**Verdict**: The rollback DOES work correctly in this scenario. `git restore --source=HEAD` with both paths specified returns both directories to their HEAD state, effectively undoing the partial `git mv` across both index and working tree. The concern raised in the prompt is valid to analyze but the command is actually correct. However, `git restore --source=HEAD` without `-W` (working tree) and `-S` (staged) flags defaults to working tree only. If the command does not restore the index, the staged deletions remain. The correct command is `git restore --source=HEAD -SW .aria/handoff/ docs/handoff/` to restore both working tree and staged changes.

**Verdict**: The rollback command in T6.6 is missing the `-SW` flags. `git restore --source=HEAD .aria/handoff/ docs/handoff/` (without `-SW`) only restores the working tree but leaves the staged deletions/additions in the index. A subsequent `git status` would still show 3 staged deletions and 3 staged additions. This is a Minor correctness gap. Raised as R2-m2.

### Scenario 5 (F10 20h estimate): Level 2 or Level 3?

**CLAUDE.md levels**:
- Level 2: Minimal — `proposal.md` (sometimes `tasks.md`)
- Level 3: Full — `proposal.md` + `tasks.md`

The spec already includes both `proposal.md` and `tasks.md`, making it Level 3 by document structure. The header reads "**Level**: 2 (Minimal — multi-file structural change, +/-doc-heavy, ~19h)" which is contradicted by the presence of `tasks.md`.

At 20h with 8 tasks, 5 layers of enforcement, 6 file changes in CLAUDE.md alone, Rule #9 activation, and a multi-repo release cycle, this spec is clearly Level 3 by any reasonable interpretation of "Full". The Level 2 label in the proposal header is stale/incorrect regardless of the effort estimate.

**Impact**: The level designation matters for process compliance. Level 2 Minimal under CLAUDE.md methodology is "proposal.md sometimes only". Level 3 Full requires both documents — which this spec has. The label mismatch does not block implementation but is a spec-internal inconsistency. The methodology compliance note in proposal.md ("Level 2 (Minimal...)") should read "Level 3 (Full)".

This was present before the fixes and is not introduced by F10. It is a pre-existing observation elevated to a Minor finding for the record.

### Scenario 6 (Bootstrap paradox T7.4): Temporal sequence trace

**Trace**:
1. Phase B: T1-T7 implemented on feature branch
2. Phase C.1: Commits created (3 repos)
3. Phase C.2: 3 PRs created + pre-merge gate verified + PRs merged
4. Phase D.2: `openspec archive aria-ten-step-session-handoff-stage`
5. T8.6: v1.21.0 5+1 SOT atomic bump + tag + multi-remote push (origin + github)
6. **At this point**: `phase-d-closer` SKILL.md with D.3 is live in the published plugin
7. T8.7 / T7.4 dogfood: Phase D.3 runs → writes `docs/handoff/2026-05-XX-h0-cycle-done.md`

**Assessment**: The F8 clarification in T7.4 is accurate: "本 cycle 期间手动模拟 D.3 step". The D.3 step in `phase-d-closer/SKILL.md` is authored in T2 and merged to aria-plugin in Phase C.2. It is "live" in the local checked-out aria submodule immediately after the aria-plugin PR merges, even before `claude plugin update aria` is run by external users. The Aria repo itself uses the submodule pointer, so Phase D of this cycle runs against the freshly-merged D.3-enabled SKILL.md.

**Conclusion**: The bootstrap paradox is correctly resolved. There is no circular dependency because: (a) the SKILL.md edit is local code authored in Phase B, merged in Phase C.2; (b) Phase D executes after Phase C.2 merge; (c) the Aria project uses the aria submodule directly (not a published plugin tarball); (d) the "third party claude plugin update" scenario applies to external users, not Aria's own development cycle. T7.4's "manual simulation" caveat is therefore overly conservative for Aria's own development — the D.3 step IS available post-merge. The caveat is correct in spirit (document the pre-release window) but slightly misleading for the primary user (Aria itself). Minor note, no action needed.

---

## New Findings (R2)

### Major (2)

#### R2-M1: Stale "schema 1.1" references in proposal.md contradict F1 fix

**Location**: `proposal.md` Success Criteria line 179; `proposal.md` Impact/Risk row; `tasks.md` T8.3 commit message template

**Problem**: F1 correctly removed the schema bump in the normative task text (T1.1, T1.2, T1.4, T1.5). However, three stale references remain:

1. `proposal.md` line 179: "输出 snapshot 含顶层 `handoff` 字段, 符合 schema 1.1"
2. `proposal.md` line 153 (Impact/Risk): "Schema 1.0 → 1.1 是 additive, 但下游 consumer 若严格 schema validate 需升级"
3. `tasks.md` line 161 (T8.3 commit message): "`feat(state-scanner): add handoff collector + snapshot.handoff field (schema 1.1)`"

A Phase B implementer following the Success Criteria will attempt to verify `snapshot_schema_version == "1.1"` — which will FAIL against a correctly-implemented T1 that preserves `"1.0"`. The T8.3 commit message template will produce misleading git history. This was also identified by the backend-architect R2 agent as R2-M1.

**Required fix** (3 text substitutions, no structural change):
- `proposal.md` line 179: replace "符合 schema 1.1" → "符合 schema 1.0 (additive field, no bump per F1 fix)"
- `proposal.md` line 153: replace Risk row text → "handoff field 是 additive top-level key, schema 保持 1.0; 已有 SKILL.md 契约无需改动, 下游无破坏性变更"
- `tasks.md` line 161: replace "schema 1.1" → "schema 1.0 (additive)"

#### R2-M2: Hook blocking mechanism underspecified — exit code 2 vs exit 0 + JSON deny conflict

**Location**: `tasks.md` T3.1, T3.4; `proposal.md` §Enforcement Success Criteria L1

**Problem**: T3.1 specifies "Action: block (exit code 2 per Claude Code hook spec)". T3.4 specifies "assert exit code 2 + stderr 含 'must use docs/handoff/'". The Success Criteria §Enforcement states "L1 hook: blocked, error message 包含 'must use docs/handoff/'".

Claude Code hook documentation (https://code.claude.com/docs/en/hooks) confirms two distinct blocking mechanisms for PreToolUse:

**Mechanism A — Exit code 2 (stdout ignored)**:
- Hook exits 2 → harness blocks the tool call
- Harness ignores ALL stdout (any JSON is discarded)
- Harness feeds stderr text to Claude as the error message
- T3.2 error message block works via stderr

**Mechanism B — Exit 0 + JSON deny (preferred structured approach)**:
- Hook exits 0 and prints to stdout: `{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "..."}}`
- Harness reads JSON, applies deny decision with reason
- stderr is irrelevant

T3.1 specifies exit code 2 (Mechanism A). T3.4 test asserts "exit code 2 + stderr text" — consistent with Mechanism A. This is internally consistent IF the hook is implemented as Mechanism A. However, T3.1 does not clarify:
- Whether the hook also emits stderr text (required for Claude to see the error message under Mechanism A)
- Whether the T3.2 error message block goes to stderr or is part of a JSON deny payload

**Additionally**: There is an open GitHub issue (#24327 in the search results) noting "PreToolUse hook exit code 2 causes Claude to stop instead of acting on error feedback" — suggesting that in some Claude Code versions, exit code 2 may cause Claude to halt entirely rather than retry with corrected path. The preferred Mechanism B (exit 0 + JSON deny) provides more predictable behavior: Claude receives the reason and redirects the write to `docs/handoff/`.

**Required fix**: T3.1 must explicitly specify which blocking mechanism is used AND how the error message is delivered. Recommended: adopt Mechanism B (exit 0 + JSON deny) as it provides structured feedback and is the documented preferred approach. Update T3.4 test to assert: exit code 0 + stdout JSON contains `"permissionDecision": "deny"` + `"permissionDecisionReason"` contains "must use docs/handoff/". If Mechanism A (exit 2) is intentionally retained, add to T3.1: "emit T3.2 error text to stderr (not stdout); stdout must be empty on exit 2".

### Minor (3)

#### R2-m1: T8.2 benchmark fixture mtime approach unspecified — timing fragility risk

**Location**: `tasks.md` T8.2

**Problem**: "fixture set 含 5 个 dated handoff files with known mtimes" does not specify whether the benchmark runner creates real filesystem files with `os.utime()` (robust) or `touch -t YYYYMMDDHHmm` (second-granularity, potentially fragile if files created in burst). The T7.1 Python unit test uses mock for mtime, which is correct for unit testing but separate from the benchmark fixture.

**Required fix**: Add to T8.2: "Fixture creation method: `os.utime(path, (ts, ts))` with distinct epoch timestamps ≥3600s apart (e.g., `[now-4d, now-3d, now-2d, now-1d, now-30m]`). Do not rely on creation-time mtime — set explicitly via utime to ensure deterministic ordering regardless of benchmark run speed."

#### R2-m2: T6.6 rollback command missing `-SW` flags — restores working tree only, not index

**Location**: `tasks.md` T6.6

**Problem**: `git restore --source=HEAD .aria/handoff/ docs/handoff/` without flags defaults to `--worktree` only. After a partial `git mv` (which stages deletions + additions in the index), this command restores the working tree files but leaves the staged index changes intact. A `git status` post-rollback would still show the partial `git mv` as staged changes.

**Required fix**: Change T6.6 rollback command to `git restore --source=HEAD -SW .aria/handoff/ docs/handoff/` (`-S` = staged/index, `-W` = working tree). This restores both the index and working tree to HEAD state, fully undoing the partial `git mv`.

#### R2-m3: proposal.md Level 2 label is incorrect — spec has both proposal.md and tasks.md (Level 3)

**Location**: `proposal.md` header line 3: "**Level**: 2 (Minimal..."

**Problem**: CLAUDE.md defines Level 2 as "Minimal — `proposal.md`" and Level 3 as "Full — `proposal.md` + `tasks.md`". This spec has both `proposal.md` and `tasks.md` with 8 tasks, 225 lines of task detail, and a 20h estimate. This is unambiguously Level 3 by document structure. The "Level 2" label was carried from the pre-fix state and not updated with the effort correction.

**Required fix**: Update header to "**Level**: 3 (Full — proposal.md + tasks.md, multi-file structural change, ~20h)". Pre-existing issue, not introduced by fixes; corrected here for spec accuracy.

---

## Observations (R2)

**OBS-R2-1**: The backend-architect R2 report (already filed as `post_spec-R2-2026-05-14T0030Z-aria-ten-step-session-handoff-stage-backend.md`) independently identifies the "schema 1.1" stale reference as R2-M1 and the Windows backslash separator gap as R2-M2. The QA-R2-M1 finding is convergent. The Windows separator finding (backend R2-M2) is out of scope for the QA engineer's hook-testability focus but is acknowledged; it targets a different aspect of T3.1 (regex character class, not blocking mechanism). Both findings must be addressed before Phase B.

**OBS-R2-2**: The `latest.md` file count discrepancy between R1 (OBS-2: "14 count = 8 + 6 is consistent including latest.md") and T6.5 ("== 15 (8 原有 含 latest.md + 6 迁移 + 1 dogfood...)") is now explained: the T6.5 count of 15 includes the dogfood handoff written in Phase D (T8.7). The pre-dogfood count of 14 is stated explicitly. This is internally consistent. No action needed.

**OBS-R2-3**: T7.4 states "本 cycle 期间手动模拟 D.3 step". Per Scenario 6 analysis, this is overly conservative for Aria's own development cycle — the D.3-enabled SKILL.md is live in the local submodule immediately after Phase C.2 merge, before any external `claude plugin update`. Suggest softening T7.4 language to: "After aria-plugin PR merges (Phase C.2), D.3 step is active in the local submodule. External users require `claude plugin update aria` after v1.21.0 tag. Dogfood executes post-merge using the live SKILL.md."

**OBS-R2-4**: T3.4 places the hook test under `aria/skills/state-scanner/tests/test_handoff_hook.sh`. This is a reasonable location given state-scanner's existing test structure, but the hook itself lives in `aria/hooks/`. If the Aria project ever adds a dedicated `aria/hooks/tests/` directory (following the single-responsibility principle of the test suite), this file should be relocated. Note for future cycle.

---

## Convergence Vote

- [ ] SCOPE_OK_R2 (all R1 resolved, 0 new Critical, R3 unnecessary — upgrade here if spec author applies R2-M1 + R2-M2 inline before Phase B)
- [x] PASS_WITH_WARNINGS (R3 not required as formal round if R2-M1 + R2-M2 applied as pre-Phase-B editorial fixes)
- [ ] FAIL

**Qualification**: If the spec author applies R2-M1 (3 text substitutions in proposal.md + tasks.md) and R2-M2 (hook blocking mechanism specification in T3.1 + T3.4 test assertion) before Phase B kickoff, this vote upgrades to SCOPE_OK_R2 with no R3. The Minor findings (R2-m1 fixture utime, R2-m2 git restore flags, R2-m3 Level label) can be addressed as editorial fixes without blocking Phase B.

All findings are editorial or single-line corrections. No architectural concerns, no redesign required. The spec is implementable.

---

## Summary Table

| Category | Count | Items |
|----------|-------|-------|
| R1 Critical verified resolved | 1 | QA-C1 (schema ordering) |
| R1 Major resolved | 2 | QA-M2 (benchmark), QA-M4 (estimate) |
| R1 Major partially resolved | 2 | QA-M1 (hook test direction correct; mechanism ambiguous), QA-M3 (pre-check added; rollback command incomplete) |
| R1 Minor resolved | 3 | QA-m1 (timezone), QA-m3 (UTF-8), QA-m4 (bootstrap) |
| R1 Minor partially resolved | 1 | QA-m2 (output-formats.md chain improves but "展示" remains) |
| New Major (R2) | 2 | R2-M1 (stale schema 1.1 refs), R2-M2 (hook blocking mechanism underspecified) |
| New Minor (R2) | 3 | R2-m1 (fixture utime), R2-m2 (git restore -SW), R2-m3 (Level label) |
| New Critical (R2) | 0 | — |
