# Aria 2.0 M5 Carryover — Layer 2 redo-mode + aux (close-old-PR + spec_drift + commit-lint)

> **Level**: 3 (Full — Layer 2 image extension + Layer 1 PR-state-machine + Forgejo state PATCH + audit log + tests)
> **Status**: Draft v2 (R1 fixes applied 2026-05-16; addresses 6 CRITICAL + key HIGH reality-drift findings; R2 verification audit deferred to next session per context budget — see `.aria/audit-reports/post_spec-R1-2026-05-16T0530Z-*.md`)
> **Change ID**: `aria-2.0-m5-carryover-layer2-redo-mode-aux`
> **Parent US**: US-025 (M5 carryover; second of the carryover trio after Spec X, mirror M3 precedent per brainstorm D4)
> **Sibling Spec**: `openspec/archive/2026-05-16-aria-2.0-m5-carryover-layer2-changes-mode/` (Spec X — shipped 2026-05-16, archived; established bash mode dispatcher + changes handler that Spec Y drops 'redo' handler into per D5 A2 skeleton-then-fill)
> **Brainstorm source**: [`.aria/decisions/2026-05-15-m6-brainstorm.md`](../../../.aria/decisions/2026-05-15-m6-brainstorm.md) D1-D7 (same as Spec X)
> **Estimate**: ~19h AI-runnable
>   - OS-2 mode_redo.sh (~12h)
>   - OS-3 close-old-PR + Superseded comment (~2h)
>   - OS-4 spec_drift_input_fetcher full impl (~3h)
>   - OS-5 commit-lint Layer 2 retry hook (~2h)
> **Created**: 2026-05-16

---

## R1 → v2 fixes (architectural decisions locked + reality alignment)

| R1 finding | Decision / Fix |
|------------|---------------|
| **CRIT-1** `_handle_s5_pr_created` doesn't exist | **Decision**: extend existing `_handle_s5_await` terminal path (alloc exit_code=0) to read result.json + extract new_pr_id when `rework_mode='redo'`. NEW Layer 1 task T1.5 reads result.json (location `${OUTPUTS_DIR}/result.json` mounted via host volume, same as M5 alloc result). NO new state machine state; minimal change. T3 OS-3 fires AFTER S5_AWAIT terminal handler stores new_pr_id on dispatch row. |
| **CRIT-2** commit_validator Python not in Layer 2 image | **Decision**: **shell-port** validator regex (Aria precedent: Spec X R1 C4 chose bash + curl+jq over Python). New `lib/commit-lint-validate.sh` (~30 lines) implements Conv Commits regex per `standards/conventions/git-commit.md`. NO Python pkg added to Dockerfile. T5.1 invokes `bash /opt/aria-runner/lib/commit-lint-validate.sh "${COMMIT_MSG}"` instead of python3 -m. |
| **CRIT-3** REWORK_ROUND env never propagated | **Decision**: extend Layer 1 `_handle_s4_launch` extra_meta dict + HCL meta_optional to **5 keys** (add `REWORK_ROUND` 5th key). NEW Spec Y task T-pre (0.5h): aria-orchestrator Layer 1 patch + HCL update. **Also retro-fixes Spec X latent bug** (changes mode round display always 1). Updates AD-M5-3 contract from 4-key to 5-key. |
| **CRIT-4** spec_drift_input_fetcher signature wrong | **Fix**: T4.4 return `(spec_what, spec_acceptance, pr_diff)` 3-tuple matching `reconciler.py:1014` unpack. Fetcher internally calls `extract_spec_sections(proposal_text)` from existing `spec_drift.py:104-128`. spec_id/pr_id are internal lookup keys, NOT output. |
| **CRIT-5** T7.2 AD-M5-3 append guard missing | **Fix**: T7.2 explicit literal guard: "**append BELOW existing 2026-05-16 line** preserving Spec X's previous update line; AD = immutable per Spec X R2 C2 convention". |
| **CRIT-6** Migration 005 already occupied | **Fix**: renumber to **006_schema_v4.1_add_spec_id.sql** (T0.1). Update drift-guard test T0.5 to apply cumulative 003+004+005+006. |
| **HIGH backend-H2** spec_id derivation undefined | **Decision**: spec_id sourced from **issue.yaml** `linked_spec_id` field if present (Layer 1 already parses issue.yaml during S1_SCAN). NEW: Layer 1 writes spec_id to dispatch row at S1_SCAN time (not S5). Removes T1.1 result.json dependency on Layer 2 for spec_id. |
| **HIGH backend-H1** OS-3 partial state risk | **Fix**: T3 sequence reverses to PATCH-first then comment: (1) PATCH state=closed; (2) on success, POST Superseded comment; (3) on PATCH failure 5xx → 3 retries; (4) on PATCH success + comment fail → audit `comment_only` outcome (acceptable — old PR is closed which is the primary state goal). |
| **HIGH ai-3** AD-M5-3 narrowing | **Fix**: T7.3 AD-M5-3 append also adds narrowing note: "Spec Y 2026-05-16 narrows: redo mode = 3 sections (no diff); changes mode = 4 sections per original lock". |
| **HIGH ai-4** T5.1 LLM cost | **Decision**: commit-lint retry uses **same `${ARIA_MODEL}` (claude-opus-4-5)** as main code-gen for consistency. Add cost row to risk table: "3 retries × 2 modes × ~500 token input × ~50 token output × opus rate = ~$0.01 per failed dispatch — negligible". |
| **HIGH ai-5** Redo prompt char budget | **Fix**: T2.5 explicit per-section caps: feedback ≤4KB (Layer 1 truncated, inherited), issue body ≤10K chars (head -c), supersedes ref ≤500 chars (literal). Total ≤15KB hard cap; overflow → `S_FAIL(prompt_overflow)` per Spec X precedent. |
| **HIGH ai-7** commit_message extraction directive | **Fix**: T2.5 prompt template appendix: literal directive `IMPORTANT: After your code changes, output a single final line in plain text: 'commit_message: <type>(<scope>): <description>'` per Spec X T4.3 R2 F1 pattern. |
| **HIGH qa-H4 → CRIT-6** | Migration renumber 005 → 006 (covered in CRIT-6 fix). |
| **HIGH qa-H6** OS-4 archived spec path | **Fix**: T4.2 fetch logic: try `openspec/changes/<spec_id>/proposal.md` first; on 404 fall back to `openspec/archive/*-<spec_id>/proposal.md` (Forgejo content API supports directory listing via `/contents` endpoint). Audit log records which path used. |
| **HIGH qa-H7** Regression count not enumerated | **Fix**: T6.9 explicit commands listed (mirror Spec X T6.3 pattern). |
| **HIGH code-reviewer C1-C10** | Bundled fixes: D5 bash explicit / §What add T0+T1 preamble / AD line ranges added / T8.1 Conv Commits 9 examples enumerated / Level header layer placement clarified / image v11 task explicit / Out of Scope inheritance line / lib/forgejo-helpers.sh extraction confirmed (extract always). |

**Remaining R1 findings deferred to R2 verification next session** (~10 MEDIUM + ~8 LOW): non-blocking refinements (race conditions / over-cap defensive sizing / end-to-end test gaps / etc).

---

---

## Why

Spec X (M5 carryover, archived 2026-05-16) shipped:
- Bash mode dispatcher (`entrypoint.sh` → `modes/initial.sh|changes.sh|redo→exit_1|unknown→exit_1`)
- changes-mode handler (`modes/changes.sh`) — Forgejo fetch + prompt + force-push to existing PR branch
- Layer 1 `_handle_s4_launch` writes 4 meta_optional keys for `rework_mode ∈ {changes, redo}` (per AD-M5-3 + brainstorm D3)
- HCL meta_optional declared 4 keys

**Current gap** (after Spec X ship): owner `/aria redo:` still fails with `redo_mode_unimplemented` exit 1 (`entrypoint.sh` dispatcher returns FAIL for redo branch). Per AD-M5-3 §"M5 期间观察行为" + Spec X §C, this is the known limitation that Spec Y closes.

**Spec Y delivers**:
1. **OS-2 redo mode container**: `modes/redo.sh` — fresh checkout from base branch + feedback prompt context + new branch + new PR (no force-push, distinct from changes-mode)
2. **OS-3 close-old-PR + Superseded-by comment**: Layer 1 S5_PR_CREATED handler — when `rework_of IS NOT NULL AND rework_mode='redo' AND parent_pr_id IS NOT NULL`, after new PR created → POST comment `_Superseded by #<new>_` on parent PR + PATCH parent PR state=closed (per Spec 3.22 + BA-9)
4. **OS-4 spec_drift_input_fetcher full impl**: per AD-M5-5 — dispatch_id → spec_id mapping + read `openspec/changes/<spec_id>/proposal.md` + Forgejo PR diff API (Spec X T1 placeholder `spec_id` schema column needed; Spec Y adds via T0 schema migration sub-task)
5. **OS-5 commit-lint Layer 2 retry hook**: max 3 retries + S_FAIL on 3rd failure (per Spec 5.3 + BA-16); leverages Spec X T4.3 commit_message extraction + fallback pattern

**Scope rationale** (per brainstorm D2): bundling OS-2/3/4/5 into one Spec Y avoids 4 separate Phase A/B/C/D cycles for related Layer 2 follow-up work. OS-2 is the majority (~63% of effort); OS-3/4/5 are small auxiliary that share Layer 2 image + tests + audit overhead.

**Why bash (not Python)** (R1 lessons from Spec X C1): Same reality alignment — Layer 2 is Node base + bash entrypoint per Dockerfile + `modes/initial.sh`. mode_redo.sh follows Spec X bash patterns: curl + jq + envsubst + claude -p positional + git ops.

---

## What

### In scope (Spec Y must deliver, ~19h)

#### A. OS-2 modes/redo.sh (~12h)

**Bash mode handler**, drop-in to `MODE_HANDLERS['redo']` slot (per Spec X T3.1 dispatcher already routes `redo` to `modes/redo.sh`). Spec X currently has the `redo` branch in `entrypoint.sh` exit 1 with `redo_mode_unimplemented`; Spec Y replaces that branch with `exec /opt/aria-runner/modes/redo.sh`.

**modes/redo.sh logic** (~250 lines bash, similar shape to modes/changes.sh):
- Read env: `NOMAD_META_REWORK_FEEDBACK`, `NOMAD_META_PARENT_PR_ID`, `NOMAD_META_REWORK_OF`, FORGEJO_BOT_PAT
- Empty feedback guard → S_FAIL(empty_feedback) (mirror Spec X T4.4 case 1)
- Forgejo PR fetch for parent PR (curl + jq, 4xx/5xx error mapping mirror Spec X)
- **Diff from changes-mode**: fresh checkout from **base branch (master/main per PR's `base.ref`)**, not head branch:
  - `git clone --depth 1 --branch <base_branch> <clone_url> work/`
  - Generate NEW branch name: `aria/redo-${PARENT_PR_ID}-${REWORK_ROUND:-1}-$(date +%Y%m%dT%H%M%S)`
  - `git checkout -b <new_branch>`
- Prompt assemble (per AD-M5-3 prompt strategy; subset of Spec X — redo mode DOES NOT include "original PR diff" since we discard previous work):
  - Section 1: feedback (must)
  - Section 2: issue body (must, from `${INPUTS_DIR}/issue.yaml`)
  - Section 3: brief reference to parent PR ("This redo supersedes PR #${PARENT_PR_ID} — owner wants fresh approach.")
  - (NO Section 4 diff — redo intentionally discards prior implementation)
- claude -p positional (per Spec X T4.3, `timeout -k 10s ${CLAUDE_TIMEOUT_S}`)
- Extract commit_message OR fallback `chore(redo-${PARENT_PR_ID}): redo PR-${PARENT_PR_ID} round ${REWORK_ROUND:-1}` (per Spec X T4.3 conventional commits)
- `git push origin <new_branch>` (regular push, not force-push)
- Forgejo create new PR via API: `POST /repos/<org>/<repo>/pulls -d '{"title":..., "head":"<new_branch>", "base":"<base_branch>"}'`
- result.json includes `new_pr_id` (Layer 1 reads this in S5_PR_CREATED handler for OS-3 close-old-PR)

#### B. OS-3 close-old-PR + Superseded-by comment (~2h)

**Layer 1 `_handle_s5_pr_created`** extension (extension.py):
- When dispatch_row `rework_mode='redo' AND rework_of IS NOT NULL`:
  - Read NEW pr_id from this dispatch's result.json (after S5 alloc terminates code=0)
  - Read PARENT pr_id from `rework_of` chain (parent dispatch row.pr_id)
  - Forgejo API: POST comment on parent PR: `_Superseded by #<new>_ (Aria redo mode round <round>)`
  - Forgejo API: PATCH `/repos/<org>/<repo>/issues/<parent_pr_id> {state: "closed"}`
  - Emit audit event `rework_cycle` with payload outcome=`old_pr_closed`
- Failure handling: Forgejo 4xx/5xx → audit warn + don't block new PR creation (best-effort)

#### C. OS-4 spec_drift_input_fetcher full impl (~3h)

Per Spec X §Out of Scope cross-ref + AD-M5-5: M5 ships stub returning empty inputs. Spec Y full impl requires:

**T0 schema migration** (Layer 1, v4 → v4.1 additive):
- ALTER TABLE dispatches ADD COLUMN `spec_id TEXT` (nullable, no default)
- Migration script `aria_layer1/migrations/005_schema_v4.1_additive.sql`
- DB triggers untouched (audit log immutability preserved per AD-M5-10 #1)

**Layer 1 write**: when Layer 2 dispatch creates new branch/PR with linked Spec, store `spec_id` on dispatch row (NEW T1: Layer 2 result.json includes `spec_id` if available; Layer 1 _handle_s5_pr_created reads + UPDATE dispatches SET spec_id=...).

**Layer 1 spec_drift_input_fetcher** (replace M5 stub):
- Input: dispatch_id → query dispatches row → spec_id + pr_id
- Read `openspec/changes/<spec_id>/proposal.md` from Aria main repo (Forgejo raw content API or git fetch)
- Read PR diff via Forgejo API `/repos/<org>/<repo>/pulls/<pr_id>.diff`
- Return both as input to spec_drift LLM analysis (existing M5 spec_drift.py logic, just replace empty-input stub)

#### D. OS-5 Commit-lint Layer 2 retry hook (~2h)

Per Spec 5.3 + BA-16 + Spec X T4.3 commit_validator interaction:

**modes/changes.sh + modes/redo.sh** add post-commit pre-push hook:
```bash
# After git commit, before git push:
COMMIT_MSG=$(git log -1 --pretty=%s)
RETRY=0
MAX_RETRY=3
while ! python3 -m aria_layer1.commit_validator validate "${COMMIT_MSG}" 2>/dev/null; do
    RETRY=$((RETRY + 1))
    if [[ ${RETRY} -ge ${MAX_RETRY} ]]; then
        fail_with "commit_lint_exhausted" "3 invalid msgs"
    fi
    # Re-invoke claude to fix commit msg
    NEW_MSG=$(timeout -k 10s 60 claude -p "Rewrite this commit message to follow Conventional Commits format per standards/conventions/git-commit.md. Original: '${COMMIT_MSG}'. Output only the new message, single line.")
    git commit --amend -m "${NEW_MSG}"
    COMMIT_MSG="${NEW_MSG}"
done
```

`commit_validator` Python module already shipped in M5 (Spec 5.3); Spec Y adds Layer 2 hook invocation.

**Note**: this hook applies to BOTH modes/changes.sh AND modes/redo.sh (shared infrastructure refactored into `lib/commit-lint-retry.sh` helper).

#### E. Layer 2 entrypoint dispatcher update (~0.5h)

`entrypoint.sh` (currently in master at `b197f26`): replace `redo)` branch:
```bash
# BEFORE (Spec X ship):
redo)
    echo "ERR: redo mode not implemented (Spec Y carryover)" >&2
    ...
    exit 1 ;;
# AFTER (Spec Y):
redo) exec /opt/aria-runner/modes/redo.sh "$@" ;;
```

#### F. Synthetic acceptance (~2h, mirror Spec X §F)

Test files (under existing `docker/aria-runner/tests/` + `hermes-extensions/aria-layer1/tests/`):
- `tests/changes-mode/redo-dispatcher.sh` — verify dispatcher routes 'redo' to modes/redo.sh (3 cases: redo→exec / unknown still fails / initial still works)
- `tests/changes-mode/mode_redo-prompt.sh` — prompt assembly (5 cases: feedback/issue body/no diff section/CJK/boundary)
- `tests/changes-mode/mode_redo-git.sh` — git ops (4 cases: fresh checkout / new branch creation / regular push / new PR creation)
- `tests/changes-mode/close-old-pr.sh` — bash tests for Layer 2-side; Python test for Layer 1 S5 handler in test_t_close_old_pr.py
- `test_t_spec_drift_fetcher.py` — Python (5 cases: stub→full impl + missing spec_id + proposal.md fetch + PR diff fetch + integration)
- `test_t_commit_lint_retry.py` — Python (4 cases: valid first try / invalid then valid retry / 3-retry exhaust → S_FAIL / claude rewrite fixture)
- `test_t_schema_v4_1_migration.py` — Python (2 cases: migration adds spec_id column / idempotent re-run)

**Total: ~23 new test cases** (~12 bash + ~11 Python)

**Regression**: all Spec X tests must continue passing (modes/changes.sh + dispatcher.sh + Spec X Python tests).

#### G. Side-effect patches (~1h)

- T7.1: `docs/requirements/user-stories/US-025.md` footer — add Spec Y status row to M5 Carryover Sub-Specs table (mark Spec Y in_progress → done)
- T7.2: `aria-orchestrator/docs/m5-handoff.yaml::open_issues_for_m6` — mark M5-OS-2/3/4/5 `absorbed_by: aria-2.0-m5-carryover-layer2-redo-mode-aux`
- T7.3: `aria-orchestrator/docs/architecture-decisions.md::AD-M5-3` append "2026-05-XX Spec Y impl complete; redo + close-old-PR + spec_drift + commit-lint shipped"
- T7.4: `aria-orchestrator/docs/validate-m5-handoff.py` — extend `check_m6_carryover_to_us_026_present` (which Spec X T7.4 deferred) to also verify Spec Y absorption fields if appropriate

---

### Out of Scope (deferred or rejected)

- **T-deploy image build** (image bump `claude-m5-carry-<sha>-v11`): owner-deferred per AD-M1-7 dispatch-time pin pattern (same as Spec X T5)
- **risk-tier algorithm** → M7+ per D6
- **Schema v5 / non-additive migration**: Spec Y only adds spec_id column (v4.1 additive)
- **Spec Y full Tier-2 path coverage** (≥10 dispatches): absorbed to US-026 M6b per D7
- **claude -p invocation upgrades**: Layer 2 model + provider chain unchanged
- **Multi-iteration redo** (`/aria redo` round 2/3/4): rework_round cap=3 already enforced in M5 Layer 1; Spec Y doesn't change cap semantics

---

## Key Decisions (cross-ref brainstorm + Spec X precedent)

| 决策 | 锁定项 | Source |
|------|--------|--------|
| D1-D7 | All 7 brainstorm decisions inherited from Spec X | brainstorm 2026-05-15 |
| Bash mode handler | Same pattern as Spec X modes/changes.sh (per Spec X R1 C1 reality drift fix) | Spec X archived |
| `chore(redo-N)` commit msg | Same valid Conventional Commits type as Spec X chore(rework-N) | git-commit.md:40-53 |
| spec_id schema v4.1 | Additive ALTER TABLE only; preserves AD-M5-10 #1 audit immutability | AD-M5-10 |
| OS-3 close-old-PR via Forgejo API | Forgejo PATCH `/issues/<id>/state` (issues API covers PRs in Forgejo) | per Spec 3.22 |
| Forgejo PAT secret-hygiene | Same Nomad Variables injection pattern as Spec X §I | standards/conventions/secret-hygiene.md Rule #7 |

---

## 验收

### A.1 Phase 完成
- [ ] proposal.md + tasks.md (Level 3) created
- [ ] cross-ref Spec X archived correctly

### A.2 audit 收敛
- [ ] R1 audit (3-5 agents per proportionality) finding count
- [ ] R2 audit fixes; ≥80% reduction
- [ ] R3 stability if needed
- [ ] Spec Status → Approved

### Phase B 验收 (R1+R2 fixes will refine)
- [ ] T1-T8 全部 `[x]` complete
- [ ] ~23 new test cases PASS (mirror Spec X §F structure)
- [ ] Spec X regression: 51 bash + 812 Python all still PASS
- [ ] `nomad job validate aria-layer2-runner.hcl` PASS (HCL unchanged but smoke verify)
- [ ] `aria_layer1` migration 005 adds spec_id column + idempotent
- [ ] Approximate test count ≥ 23 new (case-counted, not file-counted per Spec X R2 NEW-1 fix)
- [ ] Rule #6 benchmark exemption explicit (no Skill changes)

### Phase C merge (dual-repo, Rule #8 per repo)
- [ ] aria-orchestrator PR merged (`aether ci status` gate or skip_with_warning fallback)
- [ ] Aria 主 repo PR merged (submodule bump + side-effect patches)
- [ ] Both repos master parity (4-way: Forgejo origin + GitHub)

### Phase D archive (Spec Y archived → US-025 unblocks owner T-deploy + Tier-1 live)
- [ ] `openspec/archive/2026-XX-XX-aria-2.0-m5-carryover-layer2-redo-mode-aux/`
- [ ] US-025 status: Spec Y row marked done; awaiting only T-deploy + Tier-1 live
- [ ] (Rule #9) per-session phase-d-closer D.3 trigger evaluation

---

## 价值

| 维度 | 解锁 |
|------|------|
| Owner UX | `/aria redo:` 高频用法 live (currently fails with `redo_mode_unimplemented` exit 1 in Spec X-shipped master) |
| US-025 close path | Spec Y archive 是 D.2 close 第 2 个 AI 前置(after Spec X) |
| spec_drift production-ready | M5 stub → full impl unblocks AD-M5-5 production usage |
| commit-lint Layer 2 | Spec 5.3 / BA-16 closes M5 known gap (Layer 2 fallback commit msg validation) |
| close-old-PR cleanliness | Owner sees explicit "Superseded by #N" trail; no orphan PRs |
| Aria methodology | M5 carryover trio second of two Specs complete; mirror M3 trio pattern fully validated |

---

## 风险与回滚

| 风险 | Severity | Mitigation |
|------|----------|-----------|
| Schema v4 → v4.1 migration breaks existing dispatches | Medium | Additive-only (ALTER TABLE ADD COLUMN nullable); idempotent re-run; existing rows have spec_id=NULL (fetcher treats NULL as "no spec linked"); migration unit test |
| Forgejo PATCH /issues/<id>/state has unintended effects | Medium | Best-effort fallback: if PATCH 5xx, log + don't block new PR; mark old PR as Superseded via comment regardless |
| OS-3 timing — close-old-PR before new PR created → 漏更新 | Low | Sequence locked: new PR creation MUST succeed before close-old-PR fires (in S5_PR_CREATED handler reading new pr_id from result.json) |
| OS-4 stale proposal.md content (Aria main repo branch lag) | Low | Fetch latest master via Forgejo raw API; document as "snapshot at S5 time" semantic; OS-4 audit log records sha |
| OS-5 commit-lint retry loop infinite | Low | Hard cap 3 retries + S_FAIL(commit_lint_exhausted); each retry has 60s claude timeout |
| Layer 2 image bump (v10 → v11) breaks Spec X (changes-mode) | Low | Same Dockerfile + chmod + modes/ structure; just adds redo.sh + lib/commit-lint-retry.sh; Spec X modes/initial.sh + modes/changes.sh unchanged |
| spec_id write race condition (multiple Layer 2 allocs) | Low | Single-alloc-per-dispatch per Nomad parameterized job (same as M5 baseline); CAS UPDATE WHERE spec_id IS NULL guard |

**回滚路径**:
1. **Code-only revert**: revert Spec Y commits → Layer 2 dispatcher 'redo' branch reverts to exit 1 + redo_mode_unimplemented (Spec X behavior)
2. **Schema rollback**: spec_id column nullable + no FK → can be ignored if Spec Y reverted (column still in schema but unused)
3. **Forgejo state**: if PATCH close-old-PR caused real production issue, owner re-opens PR manually (low blast radius — only redo mode dispatches affected, all sourced from owner intent)

---

## 排序依赖

```
T0 schema migration (v4.1) ─┐
                            ├─→ T1 Layer 1 spec_id write
                            │
T2 modes/redo.sh impl ──────┼─→ T3 OS-3 Layer 1 S5_PR_CREATED close-old-PR
                            │
T4 OS-4 spec_drift_input_fetcher full impl ─→ (independent)
                            │
T5 OS-5 commit-lint Layer 2 retry hook (shared lib) ──→ updates modes/changes.sh + modes/redo.sh
                            │
                            ↓
                    T6 Synthetic acceptance (~23 cases)
                            │
                            ↓
                    T7 Side-effect patches
                            │
                            ↓
                    T8 Phase C+D (dual-repo merge + archive)
```

**Parallelism**: T0+T2+T4+T5 can run in parallel (different files). T1 depends on T0. T3 depends on T2. T6 depends on T2-T5. T7 doc-only.

---

## Cross-references

- Sibling: [Spec X archived](../../archive/2026-05-16-aria-2.0-m5-carryover-layer2-changes-mode/) (proposal + tasks + R1/R2/R3 audit pattern)
- Brainstorm: [`.aria/decisions/2026-05-15-m6-brainstorm.md`](../../../.aria/decisions/2026-05-15-m6-brainstorm.md)
- AD-M5-3 (Layer 1↔Layer 2 contract): `aria-orchestrator/docs/architecture-decisions.md` §AD-M5-3 (already has "2026-05-16 update via Spec X" append; Spec Y will add second update line)
- AD-M5-5 (spec_drift threshold + input fetcher): same file §AD-M5-5
- AD-M5-10 (forward-binding promises): same file §AD-M5-10 (Spec Y must preserve all 5)
- M5 handoff: `aria-orchestrator/docs/m5-handoff.yaml::open_issues_for_m6` (M5-OS-2/3/4/5)
- US-025: `docs/requirements/user-stories/US-025.md` (close gate per D7)
- PRD §588 US row: M6 stays `US-026` per D4
- Spec X precedents (mirror these in Spec Y): bash dispatcher pattern + tests/changes-mode/ + R1+R2+R3 audit convergence + per-task-group commits
- Memory references: same as Spec X (`feedback_phase_a_depth_drives_b_velocity` / `feedback_git_force_with_lease_shallow_clone` / `feedback_audit_convergence_pattern` / `feedback_nomad_hcl_validate_early` / `feedback_validator_repo_drift_guard_test` / `feedback_pre_draft_bug_hunt_discipline`)
