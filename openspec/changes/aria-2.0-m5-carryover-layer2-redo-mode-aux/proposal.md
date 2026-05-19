# Aria 2.0 M5 Carryover — Layer 2 redo-mode + aux (close-old-PR + spec_drift + commit-lint)

> **Level**: 3 (Full — Layer 2 image extension + Layer 1 PR-state-machine + Forgejo state PATCH + audit log + tests)
> **Status**: **Approved** (R3 stability audit 2026-05-17T03Z 3-agent unanimous PASS — 7/7 R1+R2-NEW CRIT closed + 17/17 R2 HIGH closed + 4 minor doc-polish surgical-fixed; see audit chain `.aria/audit-reports/post_spec-{R1-2026-05-16T0530Z,R2-2026-05-16T2242Z,R3-2026-05-17T03Z}-aria-2.0-m5-carryover-layer2-redo-mode-aux-summary.md`)
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

## R2 → v3 fixes (body+tasks propagation pass; 1 new CRIT)

R2 verify (2026-05-16T2242Z, 3-agent consensus: tech-lead + qa-engineer + code-reviewer) found:
- **1/6 R1 CRIT fully closed** (CRIT-3 REWORK_ROUND); 5/6 PARTIAL — decision table correct, body/tasks not propagated
- **1 new CRIT R2-NEW-1**: schema version target collision (current state already at v4.1 per `schema_migrate.py:_LATEST_SCHEMA_VERSION="4.1"`; migration 006 must bump to **v4.2** else no-op silent skip)
- **~10 new HIGH**: linked_spec_id field missing / T5 dup numbering / T3 order not reversed / T4.4 4-tuple still / test-type mismatch / SQLite syntax / cost row missing / dispatcher claim false / PR title template missing / T-pre scope undeclared

| R2 finding | v3 fix |
|------------|--------|
| **R2-NEW-1** schema v4.1 collision | Migration **006_schema_v4.2_add_spec_id.sql** (renamed); from_version="4.1", to_version="4.2"; `schema_migrate.py` add entry + bump `_LATEST_SCHEMA_VERSION="4.2"`; all body/tasks references v4.1 → v4.2 |
| **CRIT-1 propagation** | Body §A/§B + tasks T3.1 all `_handle_s5_pr_created` → `_handle_s5_await` terminal path |
| **CRIT-2 propagation** | Body §D code block rewrite: `bash /opt/aria-runner/lib/commit-lint-validate.sh` (no Python); remove "Python module already shipped" caption |
| **CRIT-4 propagation** | tasks T4.4 return `(spec_what, spec_acceptance, pr_diff)` 3-tuple matching `reconciler.py:1014` unpack |
| **CRIT-5 propagation** | tasks T7.2 add literal guard "append BELOW existing 2026-05-16 line — DO NOT replace; immutable append-only per Spec X R2 C2" |
| **CRIT-6 propagation** | Body §C + 验收 + 风险与回滚 all `005_schema_v4.1_additive.sql` → `006_schema_v4.2_add_spec_id.sql` |
| **R2-NEW-2** linked_spec_id missing | NEW task T1.0 (~0.3h): extend M1 issue validator schema with optional `linked_spec_id: string` field, regex `^[a-z0-9-]+$`, backward-compat |
| **R2-NEW-3** T5 dup numbering | Renumber T5.1/5.2/5.3/5.4/5.5 sequential |
| **R2-NEW-4** T3 order | T3 sub-task order **reversed**: 3.1 detect → 3.2 read parent → 3.3 PATCH state=closed (with retries) → 3.4 POST Superseded comment → 3.5 audit; per backend-H1 v2 |
| **R2-NEW-6** test-type mismatch | Add `tests/changes-mode/commit-lint-validate.sh` bash test (4 cases); Python test repurposed to retry-loop integration |
| **R2-NEW-7** SQLite syntax | Drop `IF NOT EXISTS` mention; mandate migration-version guard per 004 precedent |
| **R2-NEW-8** ai-4 cost row | Add risk-table row: "commit-lint retry × N dispatches × Opus rate → ~$0.01/failure; 3-retry hard cap" |
| **R2-NEW-9** T2.9 dead field | Remove `spec_id` from T2.9 result.json field list (Layer 1 S1_SCAN writes per T1) |
| **R2-NEW-10** dispatcher claim | Body §A L73 rewrite: "Spec Y replaces `redo) ... exit 1` branch in entrypoint.sh with `redo) exec /opt/aria-runner/modes/redo.sh \"$@\" ;;`" (matches T2.1) |
| **R2-NEW-11** PR title template | tasks T2.8 literal title template per below |
| **R2-NEW-12** T-pre scope | NEW proposal subsection §Out of Scope contrast: "Spec X retro-fix scope (T-pre.4/.5/.6 modify archived Spec X test files + AD-M5-3 contract section — legitimate per CRIT-3 retro-fix; not full Spec X re-archive)" |
| **HIGH ai-3** AD-M5-3 narrowing | tasks T7.2 append narrowing literal: "Spec Y narrows: redo mode = 3 sections (no diff); changes mode = 4 sections per original lock" |
| **HIGH ai-5** char caps | tasks T2.5 add explicit caps: feedback ≤4KB / issue ≤10K / supersedes ref ≤500 / total ≤15KB; overflow → S_FAIL(prompt_overflow) |
| **HIGH ai-7** commit_message directive | tasks T2.5 prompt appendix literal `IMPORTANT` directive (per Spec X T4.3 R2 F1) |
| **HIGH backend-H2 body** | Body §C rewrite: spec_id sourced at S1_SCAN via issue.yaml linked_spec_id (NOT Layer 2 result.json + _handle_s5_pr_created) |
| **HIGH qa-H6 tasks** | tasks T4.2: try `openspec/changes/<id>/proposal.md` first; on 404 fall back to `openspec/archive/*-<id>/proposal.md` via Forgejo `/contents` directory listing |
| **HIGH qa-H7 commands** | tasks T6.9 enumerate executable bash + Python commands per Spec X T6.3 pattern |
| **HIGH C9 Conv Commits** | tasks T8.1 enumerate Spec Y commit examples (T-pre/T0/T1/T2/T3/T4/T5/T7 each) |
| **HIGH C10 lib/forgejo** | tasks T2.3 "always extract `lib/forgejo-helpers.sh`" (drop "consider...>50 lines" guard) |
| **MEDIUM count drift** | All test count refs → ≥28 (enumeration: 3+5+4+2+3+5+4+2 plus new bash commit-lint 4 = 32) |
| **MEDIUM estimate** | Reconcile: ~20h AI-runnable (19h core OS + 1h T-pre retro-fix) + T1.0 (0.3h) + bookkeeping ~5h = **~25.3h gross** |
| **MEDIUM HCL validate** | tasks T6.10 "HCL changed by T-pre (REWORK_ROUND 5th key); MUST run `nomad job validate aria-layer2-runner.hcl` per `feedback_nomad_hcl_validate_early`" |
| **MEDIUM T6.4 rename** | `close-old-pr-layer2.sh` → `redo-result-pr.sh` (Layer 2 only writes new_pr_id; closure logic Layer 1) |
| **LOW status line** | tasks "当前 Phase" → "A.2 (R2 verified, v3 applied, R3 stability pending)" |
| **LOW T7 numbering** | tasks add T7.5: extend `validate-m5-handoff.py::check_m6_carryover_to_us_026_present` to verify Spec Y absorption (per proposal §G T7.4) |
| **LOW memory refs** | proposal Cross-references add `feedback_agent_team_for_level1` + `feedback_submodule_pointer_post_merge_bump` |

**R3 stability audit** (next, 3-agent, ~30min): verify v3 propagation complete; target 0 CRIT + ≤3 HIGH + ≤6 MEDIUM/LOW residual.

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
2. **OS-3 close-old-PR + Superseded-by comment**: Layer 1 `_handle_s5_await` terminal-path extension (per CRIT-1 v2 — handler `_handle_s5_pr_created` does NOT exist) — when `rework_of IS NOT NULL AND rework_mode='redo' AND parent_pr_id IS NOT NULL`, after new PR created (Layer 2 wrote new_pr_id to result.json) → **PATCH parent PR state=closed FIRST, then POST Superseded comment** (per backend-H1 v2 reversed sequence)
3. **OS-4 spec_drift_input_fetcher full impl**: per AD-M5-5 — dispatch_id → spec_id (from S1_SCAN write per backend-H2) + read `openspec/changes/<spec_id>/proposal.md` (with archive-path fallback per qa-H6) + Forgejo PR diff API; returns 3-tuple `(spec_what, spec_acceptance, pr_diff)` matching reconciler.py:1014 unpack (per CRIT-4)
4. **OS-5 commit-lint Layer 2 retry hook**: max 3 retries + S_FAIL on 3rd failure (per Spec 5.3 + BA-16); shell-port via `lib/commit-lint-validate.sh` (per CRIT-2 — NO Python in Layer 2 image); leverages Spec X T4.3 commit_message extraction + fallback pattern

**Scope rationale** (per brainstorm D2): bundling OS-2/3/4/5 into one Spec Y avoids 4 separate Phase A/B/C/D cycles for related Layer 2 follow-up work. OS-2 is the majority (~63% of effort); OS-3/4/5 are small auxiliary that share Layer 2 image + tests + audit overhead.

**Why bash (not Python)** (R1 lessons from Spec X C1): Same reality alignment — Layer 2 is Node base + bash entrypoint per Dockerfile + `modes/initial.sh`. mode_redo.sh follows Spec X bash patterns: curl + jq + envsubst + claude -p positional + git ops.

---

## What

### In scope (Spec Y must deliver, ~19h)

#### A. OS-2 modes/redo.sh (~12h)

**Bash mode handler**. Spec X currently has `redo) ... exit 1` branch in `entrypoint.sh` (case statement, NOT an associative-array dispatcher) emitting `redo_mode_unimplemented`. Spec Y replaces that branch with `redo) exec /opt/aria-runner/modes/redo.sh "$@" ;;` (per T2.1).

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
- Forgejo create new PR via API: `POST /repos/<org>/<repo>/pulls -d '{"title": "Aria redo: PR-${PARENT_PR_ID} round ${REWORK_ROUND}", "head":"<new_branch>", "base":"<base_branch>", "body": "Supersedes #${PARENT_PR_ID} (Aria redo mode)"}'` (literal template; T2.8 elaborates)
- result.json includes `new_pr_id` (Layer 1 reads this in `_handle_s5_await` terminal path per CRIT-1 fix for OS-3 close-old-PR; see T1.5)

#### B. OS-3 close-old-PR + Superseded-by comment (~2h)

**Layer 1 `_handle_s5_await` terminal-path extension** (extension.py; reuses existing handler at terminal `exit_code=0` branch — see T1.5):
- When dispatch_row `rework_mode='redo' AND rework_of IS NOT NULL AND new_pr_id from result.json`:
  - Read NEW pr_id from this dispatch's result.json (after S5 alloc terminates code=0; per CRIT-1 fix)
  - UPDATE dispatches SET pr_id=<new> WHERE dispatch_id=? (replaces find_or_create_pr path for redo dispatches)
  - Read PARENT pr_id from `rework_of` chain (parent dispatch row.pr_id; guard NULL → audit warn + skip close)
  - **Sequence (PATCH-first per backend-H1 v2)**:
    1. Forgejo API: PATCH `/repos/<org>/<repo>/issues/<parent_pr_id> {state: "closed"}` (3 retries on 5xx; success outcome = primary state goal)
    2. On PATCH success: Forgejo API POST comment on parent PR: `_Superseded by #<new>_ (Aria redo mode round <round>)` (round from dispatch.rework_round)
    3. On PATCH success + comment fail → audit `comment_only_succeeded` (acceptable; old PR closed)
    4. On PATCH fail after retries → audit `close_failed` + emit warn (don't block new PR; owner can manually close)
  - Emit audit event `rework_cycle` with payload outcome=`old_pr_closed` | `comment_only_succeeded` | `close_failed`
- Failure handling (enumerated per qa-H5): parent PR already closed (409/422) → treat as success + still post comment; null parent pr_id → audit warn + skip; network timeout vs 4xx/5xx distinct retry policy (network → retry; 4xx → no retry, audit; 5xx → 3 retries)

#### C. OS-4 spec_drift_input_fetcher full impl (~3h)

Per Spec X §Out of Scope cross-ref + AD-M5-5: M5 ships stub returning empty inputs. Spec Y full impl requires:

**T0 schema migration** (Layer 1, **v4.1 → v4.2 additive** — current state already at v4.1 per `schema_migrate.py:_LATEST_SCHEMA_VERSION`; per R2-NEW-1 fix):
- ALTER TABLE dispatches ADD COLUMN `spec_id TEXT` (nullable, no default; idempotency via migration-version guard pattern matching existing 004 migration — SQLite has no `ADD COLUMN IF NOT EXISTS`)
- Migration script `aria_layer1/migrations/006_schema_v4.2_add_spec_id.sql`
- `schema_migrate.py` add entry `("006", "006_schema_v4.2_add_spec_id.sql", "4.1", "4.2")` + bump `_LATEST_SCHEMA_VERSION="4.2"`
- DB triggers untouched (audit log immutability preserved per AD-M5-10 #1)

**Layer 1 write at S1_SCAN** (per backend-H2 v2 fix; NOT Layer 2 result.json):
- New T1.0: extend M1 issue body validator schema with optional `linked_spec_id: string` field (regex `^[a-z0-9-]+$`, nullable, backward-compat)
- T1.1: in `extension.py::_handle_s1_scan`, when issue.yaml `linked_spec_id` present → `UPDATE dispatches SET spec_id=? WHERE dispatch_id=? AND spec_id IS NULL` (CAS guard)
- Layer 2 result.json does NOT carry spec_id (removed per T1.4)

**Layer 1 spec_drift_input_fetcher** (replace M5 stub):
- Input: dispatch_id → query dispatches row → spec_id + pr_id (internal lookup keys)
- Read `openspec/changes/<spec_id>/proposal.md` from Aria main repo via Forgejo raw content API; **on 404 fall back to `openspec/archive/*-<spec_id>/proposal.md`** (per qa-H6 v2 fix; Forgejo `/contents` directory listing for prefix match)
- Read PR diff via Forgejo API `/repos/<org>/<repo>/pulls/<pr_id>.diff`
- Internally call `extract_spec_sections(proposal_text)` from existing `spec_drift.py:104-128` to slice §What + §验收
- Return `(spec_what, spec_acceptance, pr_diff)` **3-tuple matching `reconciler.py:1014` unpack** (per CRIT-4 v2 fix; NOT a 4-field named tuple — spec_id/pr_id are internal lookup, NOT output)

#### D. OS-5 Commit-lint Layer 2 retry hook (~2h)

Per Spec 5.3 + BA-16 + Spec X T4.3 commit_validator interaction. **Shell-port** per CRIT-2 v2 fix (Spec X R1 C1 reality drift precedent: Layer 2 is Node-base + bash, NO Python).

**lib/commit-lint-validate.sh** (~30 lines) — pure bash Conventional Commits validator:
- Regex per `standards/conventions/git-commit.md:40-53` valid types `{feat|fix|chore|refactor|test|docs|style|perf|build|ci}` + subject ≤72 chars
- Exit 0 if valid, exit 1 if invalid
- NO Python dependency (no `python3 -m aria_layer1.commit_validator`)

**lib/commit-lint-retry.sh** — shared retry loop helper invoked from both modes/changes.sh + modes/redo.sh:

```bash
# After git commit, before git push:
COMMIT_MSG=$(git log -1 --pretty=%s)
RETRY=0
MAX_RETRY=3
while ! bash /opt/aria-runner/lib/commit-lint-validate.sh "${COMMIT_MSG}" >/dev/null 2>&1; do
    RETRY=$((RETRY + 1))
    if [[ ${RETRY} -ge ${MAX_RETRY} ]]; then
        fail_with "commit_lint_exhausted" "3 invalid msgs"
    fi
    # Re-invoke claude (same ${ARIA_MODEL} as code-gen per HIGH ai-4 v2) to fix commit msg
    NEW_MSG=$(timeout -k 10s "${CLAUDE_TIMEOUT_S:-60}" claude -p "Rewrite this commit message to follow Conventional Commits format per standards/conventions/git-commit.md. Original: '${COMMIT_MSG}'. Output only the new message, single line.")
    git commit --amend -m "${NEW_MSG}"
    COMMIT_MSG="${NEW_MSG}"
done
```

`aria_layer1/commit_validator.py` library remains in M5 for Layer 1 use; Spec Y bash hook independently re-implements the regex contract per same Conventional Commits spec (single SoT: `standards/conventions/git-commit.md`).

**Note**: this hook applies to BOTH modes/changes.sh AND modes/redo.sh (shared via `lib/commit-lint-retry.sh` helper).

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
- `tests/changes-mode/redo-result-pr.sh` — Layer 2 result.json writes new_pr_id (2 cases: success / fail-to-create-new-PR no close action) — renamed per R2 MEDIUM
- `tests/changes-mode/commit-lint-validate.sh` — **NEW per R2-NEW-6** bash validator regex (4 cases: valid CC format / invalid format / 72-char boundary / type prefix CJK)
- `test_t_close_old_pr.py` — Python Layer 1 S5_AWAIT handler (3 cases: redo dispatch detected + PATCH+comment sequence / 4xx fallback / parent PR already closed graceful)
- `test_t_spec_drift_fetcher.py` — Python (5 cases: stub→full impl + missing spec_id graceful + proposal.md fetch + PR diff fetch + 3-tuple return)
- `test_t_commit_lint_retry.py` — Python **retry-loop integration** (4 cases: valid first try / invalid then valid retry / 3-retry exhaust → S_FAIL / claude rewrite fixture); validator regex correctness covered by bash test above
- `test_t_schema_v4_2_migration.py` — Python (3 cases: migration adds spec_id to v4.1 DB → v4.2 / idempotent re-run / drift-guard cumulative 003+004+005+006 per T0.6)
- `test_t_spec_id_write.py` — Python (2 cases: issue.yaml linked_spec_id present → UPDATE applied; absent → spec_id stays NULL graceful)

**Total: ≥35 new test cases enumerated** (18 bash + 17 Python; enumeration in tasks T6.1-T6.10 sums to 3+5+4+2+4+3+5+4+3+2 = 35; case-counted per Spec X R2 NEW-1 fix; commands verifiable per qa-H7 + tasks T6.11)

**Regression**: all Spec X tests must continue passing (modes/changes.sh + dispatcher.sh + Spec X Python tests).

#### G. Side-effect patches (~1h)

(Note: T7 sub-task numbering is canonical in tasks.md T7.1-T7.6; below is high-level body listing organized by purpose, not sub-task number)

- US-025 footer Spec Y status row (M5 Carryover Sub-Specs table) → done
- `aria-orchestrator/docs/m5-handoff.yaml::open_issues_for_m6` mark M5-OS-2/3/4/5 `absorbed_by: aria-2.0-m5-carryover-layer2-redo-mode-aux`
- `aria-orchestrator/docs/architecture-decisions.md::AD-M5-3` **APPEND BELOW** existing 2026-05-16 Spec X line (immutable per Spec X R2 C2; literal guard in tasks T7.2): "Spec Y impl complete; redo + close-old-PR + spec_drift + commit-lint shipped; **5-key contract** (REWORK_ROUND added); **prompt narrowing** (redo=3 sections / changes=4 sections)"
- `aria-orchestrator/docs/validate-m5-handoff.py` — extend `check_m6_carryover_to_us_026_present` (which Spec X T7.4 deferred) to also verify Spec Y absorption fields
- `docs/handoff/2026-05-15-us025-m5-c2-d1-done.md` — add Addendum 3 noting Spec Y cycle complete

---

### Out of Scope (deferred or rejected)

- **T-deploy image build** (image bump `claude-m5-carry-<sha>-v11`): owner-deferred per AD-M1-7 dispatch-time pin pattern (same as Spec X T5)
- **risk-tier algorithm** → M7+ per D6
- **Schema v5 / non-additive migration**: Spec Y only adds spec_id column (v4.1 → v4.2 additive per R2-NEW-1)
- **Spec Y full Tier-2 path coverage** (≥10 dispatches): absorbed to US-026 M6b per D7
- **claude -p invocation upgrades**: Layer 2 model + provider chain unchanged
- **Multi-iteration redo** (`/aria redo` round 2/3/4): rework_round cap=3 already enforced in M5 Layer 1; Spec Y doesn't change cap semantics

### Spec X retro-fix scope (in scope per R2-NEW-12, T-pre tasks 4-6)

T-pre.4/.5/.6 modify Spec X archived test files (`tests/test_t_changes_mode_meta.py` assertion 4→5 keys + `tests/changes-mode/mode_changes-prompt.sh` add REWORK_ROUND env case) and AD-M5-3 contract section (4-key → 5-key bump). This is **legitimate retro-fix scope** per CRIT-3 fix (REWORK_ROUND silent bug latent in Spec X master; modes/changes.sh:174,256 fallback `${REWORK_ROUND:-1}` always renders round 1). NOT a Spec X re-archive — Spec Y commits include these Spec X file edits because the bug was discovered while drafting Spec Y. Audit-engine treats this as Spec Y deliverable (per `feedback_sister_spec_r1_latent_catch`).

---

## Key Decisions (cross-ref brainstorm + Spec X precedent)

| 决策 | 锁定项 | Source |
|------|--------|--------|
| D1-D7 | All 7 brainstorm decisions inherited from Spec X | brainstorm 2026-05-15 |
| Bash mode handler | Same pattern as Spec X modes/changes.sh (per Spec X R1 C1 reality drift fix) | Spec X archived |
| `chore(redo-N)` commit msg | Same valid Conventional Commits type as Spec X chore(rework-N) | git-commit.md:40-53 |
| spec_id schema v4.1 → v4.2 | Additive ALTER TABLE only (v4.2 is target; current state v4.1 per `_LATEST_SCHEMA_VERSION` — R2-NEW-1 fix); preserves AD-M5-10 #1 audit immutability | AD-M5-10 |
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

### Phase B 验收 (R1+R2+R3 fixes refined)
- [ ] T-pre + T0-T8 全部 `[x]` complete (T1.0 NEW for M1 schema extension per R2-NEW-2)
- [ ] ≥35 new test cases PASS (mirror Spec X §F structure; case-counted per Spec X R2 NEW-1 fix; enumeration in tasks T6.1-T6.10)
- [ ] Spec X regression: 51 bash + 812 Python all still PASS (T6.9 enumerates executable commands per qa-H7)
- [ ] `nomad job validate aria-layer2-runner.hcl` PASS (HCL changed by T-pre adding REWORK_ROUND 5th key per `feedback_nomad_hcl_validate_early`)
- [ ] `aria_layer1` migration 006_schema_v4.2_add_spec_id.sql adds spec_id column to v4.1 DB (target v4.2) + idempotent re-run
- [ ] `_LATEST_SCHEMA_VERSION` bumped 4.1→4.2 in `schema_migrate.py`
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
| Schema v4.1 → v4.2 migration breaks existing dispatches | Medium | Additive-only (ALTER TABLE ADD COLUMN nullable); idempotent via migration-version guard (existing 004 precedent — SQLite has no ADD COLUMN IF NOT EXISTS); existing rows have spec_id=NULL (fetcher treats NULL as "no spec linked"); migration unit test verifies v4.1→v4.2 transition |
| Forgejo PATCH /issues/<id>/state has unintended effects | Medium | Best-effort fallback: if PATCH 5xx after 3 retries, audit warn + don't block new PR; if PATCH success + comment fails → audit `comment_only_succeeded` (old PR closed = primary goal achieved) |
| OS-3 timing — close-old-PR before new PR created → 漏更新 | Low | Sequence locked: new PR creation in modes/redo.sh MUST succeed before close-old-PR fires (in `_handle_s5_await` terminal handler reading new pr_id from result.json per CRIT-1) |
| OS-4 stale proposal.md content (Aria main repo branch lag) | Low | Fetch latest master via Forgejo raw API; archive-path fallback per qa-H6; document as "snapshot at S5 time" semantic; OS-4 audit log records sha |
| OS-5 commit-lint retry loop infinite | Low | Hard cap 3 retries + S_FAIL(commit_lint_exhausted); each retry has 60s claude timeout |
| OS-5 retry cost runaway | Low | Per HIGH ai-4: 3 retries × 2 modes × ~500 token input × ~50 token output × Opus rate = **~$0.01 per failed dispatch** (negligible); 3-retry hard cap prevents unbounded spend |
| Layer 2 image bump (v10 → v11) breaks Spec X (changes-mode) | Low | Same Dockerfile + chmod + modes/ structure; adds redo.sh + lib/commit-lint-validate.sh + lib/commit-lint-retry.sh; Spec X modes/initial.sh + modes/changes.sh unchanged (modes/changes.sh receives T-pre REWORK_ROUND env now) |
| spec_id write race condition (multiple Layer 2 allocs) | Low | Single-alloc-per-dispatch per Nomad parameterized job (same as M5 baseline); CAS UPDATE WHERE spec_id IS NULL guard at S1_SCAN (Layer 1 single-threaded write) |
| `linked_spec_id` issue field NULL/missing | Low | T1.0 makes field optional + backward-compat; absent → spec_id stays NULL → spec_drift fetcher treats as "no spec linked" → returns empty 3-tuple (existing M5 stub behavior preserved) |

**回滚路径**:
1. **Code-only revert**: revert Spec Y commits → Layer 2 dispatcher 'redo' branch reverts to exit 1 + redo_mode_unimplemented (Spec X behavior)
2. **Schema rollback**: spec_id column nullable + no FK → can be ignored if Spec Y reverted (column still in schema but unused)
3. **Forgejo state**: if PATCH close-old-PR caused real production issue, owner re-opens PR manually (low blast radius — only redo mode dispatches affected, all sourced from owner intent)

---

## 排序依赖

```
T-pre REWORK_ROUND 5-key contract ─┐
  (Layer 1 extra_meta + HCL + AD)  │
                                   ↓
                          T2 modes/redo.sh impl (writes new_pr_id to result.json)
                                   │
T0 schema 006 v4.1→v4.2 ──┐        │
                          ↓        │
T1.0 M1 issue schema +   T1 Layer 1│
linked_spec_id field      spec_id  │
                          @S1_SCAN │
                                   │
                                   ↓
T4 OS-4 spec_drift           T3 OS-3 close-old-PR Layer 1
fetcher (independent)──→─┐      `_handle_s5_await` terminal-path
                          │      (T3.1 reads result.json for new_pr_id
T5 OS-5 commit-lint       │       per CRIT-1, then PATCH-first per backend-H1)
shell-port lib/  ─────────┤
(commit-lint-validate.sh   │
 + commit-lint-retry.sh)   │
                           ↓
                  T6 Synthetic acceptance (≥35 cases)
                           │
                           ↓
                  T7 Side-effect patches (US-025 footer / m5-handoff / AD-M5-3 / validate-m5-handoff / handoff Addendum)
                           │
                           ↓
                  T8 Phase C+D (dual-repo merge + archive)
```

**Parallelism**: T-pre + T0 + T1.0 + T2 + T4 + T5 can run in parallel (different files). T1 depends on T0 + T1.0. T3 depends on T2 (T1.5 merged into T3.1 per CRIT-1 — both fire in `_handle_s5_await` terminal-path). T6 depends on T2-T5. T7 doc-only.

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
- Memory references: same as Spec X plus per R2 (`feedback_phase_a_depth_drives_b_velocity` / `feedback_git_force_with_lease_shallow_clone` / `feedback_audit_convergence_pattern` / `feedback_nomad_hcl_validate_early` / `feedback_validator_repo_drift_guard_test` / `feedback_pre_draft_bug_hunt_discipline` / `feedback_agent_team_for_level1` / `feedback_submodule_pointer_post_merge_bump` / `feedback_sister_spec_r1_latent_catch` / `feedback_per_spec_assumption_recheck`)
