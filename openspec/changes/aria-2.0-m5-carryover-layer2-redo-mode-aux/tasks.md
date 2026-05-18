# Spec Y Tasks — Aria 2.0 M5 Carryover Layer 2 redo-mode + aux

> **Change ID**: `aria-2.0-m5-carryover-layer2-redo-mode-aux`
> **Parent**: US-025 (M5 carryover, second of trio after Spec X)
> **Estimate v3**: **~24.8h AI-runnable** (enumeration: T-pre 0.5 + T0 1 + T1.0 0.3 + T1 1 + T2 12 + T3 2 + T4 3 + T5 2 + T6 2 + T7 1 = 24.8h); **+~5h bookkeeping** (Phase C/D + audits) = **~29.8h gross**. Breakdown: 19h OS core (T2+T3+T4+T5) + 0.5h T-pre + 0.3h T1.0 + 1h T1 + 4h T6+T7 cumulative
> **Sibling Spec X**: archived at `openspec/archive/2026-05-16-aria-2.0-m5-carryover-layer2-changes-mode/`
> **Phase B sequencing**: T-pre + T0 + T1.0 + T2 + T4 + T5 parallel-able; T1 ⏸ T0 + T1.0; T3 ⏸ T2 + T3.1 binding (T1.5 merged into T3.1 per CRIT-1 fix — both fire in `_handle_s5_await` terminal-path); T6 ⏸ T2-T5; T7 doc only
> **R1→v2 fix manifest**: 6 CRIT + ~13 HIGH applied (see proposal.md §"R1 → v2 fixes")
> **R2→v3 fix manifest**: 5/6 R1 CRIT body+tasks propagation + 1 NEW CRIT R2-NEW-1 schema v4.2 + 10 HIGH (see proposal.md §"R2 → v3 fixes")

---

## Task Group 总览 (v3 post-R2 propagation)

| ID | 标题 | 工时 | 阻塞 |
|----|------|------|------|
| **T-pre** | **NEW (CRIT-3)** REWORK_ROUND propagation: Layer 1 extra_meta + HCL meta_optional 5th key + retro-fix Spec X latent (legit scope per R2-NEW-12) | 0.5h | — |
| T0 | Schema v4.1 → **v4.2** migration **006_schema_v4.2_add_spec_id.sql** (renumbered per CRIT-6 + version bump per R2-NEW-1; idempotent via migration-version guard NOT SQLite IF NOT EXISTS per R2-NEW-7) | 1h | — |
| **T1.0** | **NEW per R2-NEW-2**: extend M1 issue body validator schema with optional `linked_spec_id` field (regex `^[a-z0-9-]+$`, nullable, backward-compat) | 0.3h | — |
| T1 | Layer 1 spec_id write **at S1_SCAN** (per HIGH backend-H2 — read issue.yaml linked_spec_id from M1 schema) | 1h | T0 + T1.0 |
| T2 | modes/redo.sh impl (OS-2) + entrypoint.sh swap redo branch + lib/forgejo-helpers.sh (extract `forgejo_get_retry` from changes.sh + create new `forgejo_post_retry` + `forgejo_patch_retry`, per C10) | 12h | T-pre |
| T3 | OS-3 close-old-PR via **PATCH-first then comment** (per HIGH backend-H1 + R2-NEW-4) — T3.1 also binds new_pr_id from result.json in `_handle_s5_await` terminal-path (merged T1.5 per CRIT-1) | 2h | T2 |
| T4 | OS-4 spec_drift_input_fetcher full impl — return **3-tuple `(spec_what, spec_acceptance, pr_diff)`** matching reconciler.py:1014 unpack (per CRIT-4); archive-path fallback per HIGH qa-H6 | 3h | T0 + T1 |
| T5 | OS-5 commit-lint Layer 2 retry — **shell-port** via lib/commit-lint-validate.sh (per CRIT-2 + R2-NEW-6 add bash test); same ${ARIA_MODEL} for retry calls per HIGH ai-4 | 2h | T2 |
| T6 | Synthetic acceptance tests (~32 cases enumerated per HIGH qa-H7 + R2-NEW-6 bash validator test) + HCL validate (changed by T-pre per R2 MEDIUM) | 2h | T2-T5 |
| T7 | Side-effect patches — T7.2 explicit CRIT-5 guard + AD-M5-3 narrowing note per HIGH ai-3 + T7.5 validate-m5-handoff.py extension (per R2 LOW T7-numbering) | 1h | T2 (parallel) |
| T8 | Phase C+D (dual-repo merge + archive + Rule #9 handoff trigger + T8.1 Conv Commits enumerated per C9) | (standard) | T6+T7 |

总: ~29.8h gross (AI-runnable 24.8h + bookkeeping ~5h); core OS items ~19h (T2+T3+T4+T5)

---

## Phase 0 — T-pre REWORK_ROUND propagation (CRIT-3 retro-fix, 0.5h; in-scope Spec X retro-modification per R2-NEW-12 — see proposal §"Spec X retro-fix scope")

### T-pre — Add 5th meta_optional key REWORK_ROUND

- [x] pre.1 Extend `aria_layer1/extension.py::_handle_s4_launch` extra_meta when `rework_mode IN ('changes','redo')`: add `"REWORK_ROUND": str(dispatch.get("rework_round") or 1)`
- [x] pre.2 Update HCL `nomad/jobs/aria-layer2-runner.hcl` meta_optional list: add 5th key `"REWORK_ROUND"`. **Must run `nomad job validate aria-layer2-runner.hcl`** post-edit per `feedback_nomad_hcl_validate_early`
- [x] pre.3 Update existing audit `meta_optional_written` payload `rework_keys_written` list to include `REWORK_ROUND` (5 keys total; note: existing historical rows remain 4-key per AD-M5-10 #1 immutability — readers must use `len()` not equality)
- [x] pre.4 Update Spec X test `tests/test_t_changes_mode_meta.py` (modify existing assertions): add `REWORK_ROUND` to expected key list (5 keys total: REWORK_MODE / REWORK_FEEDBACK / PARENT_PR_ID / REWORK_OF / REWORK_ROUND); value matches dispatch.rework_round
- [x] pre.5 Update Spec X bash test `tests/changes-mode/mode_changes-prompt.sh` to add **new test case** verifying NOMAD_META_REWORK_ROUND env consumed (modes/changes.sh:174 fallback `${REWORK_ROUND:-1}` now correctly resolves to actual round when env present; test with REWORK_ROUND=2 → prompt section header says "round 2")
- [x] pre.6 Update AD-M5-3 contract section: 4-key → **5-key** Layer 1↔Layer 2 meta contract (architecture-decisions.md §AD-M5-3 contract sub-section ~L3585-3596; verify line range with grep before edit)

---

## Phase 1 — Schema + Layer 1 (T1.0 + T0+T1, 2.3h, T0+T1.0 unblock T1+T4)

### T1.0 — M1 issue schema extension (R2-NEW-2, ~0.3h)

- [x] 1.0.1 Locate M1 issue body validator (per `extension.py:1614` reference) — likely `aria_layer1/m1_issue_validator.py` or schema file
- [x] 1.0.2 Add optional field `linked_spec_id`: type `string`, regex `^[a-z0-9.-]+$` (H2 amend 2026-05-18: original `^[a-z0-9-]+$` rejected real change IDs like `aria-2.0-m5-…`; owner OD → add `.` per pre-archive amendment), nullable, backward-compat (absent → ignored, no validation error)
- [x] 1.0.3 Unit test extending existing M1 validator tests: present + valid format → passes; absent → passes; present + invalid format (uppercase/special chars) → validation error

### T0 — Schema **v4.1 → v4.2** additive migration (~1h, R2-NEW-1)

- [x] 0.1 Create `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/migrations/006_schema_v4.2_add_spec_id.sql` (renumbered from 005 per CRIT-6 + version bumped v4.1→v4.2 per R2-NEW-1 — current state already at v4.1 per `_LATEST_SCHEMA_VERSION`):
  - `ALTER TABLE dispatches ADD COLUMN spec_id TEXT;` (nullable, no default)
  - **NO** `ADD COLUMN IF NOT EXISTS` (per R2-NEW-7 — SQLite does NOT support this syntax); idempotency via migration-version guard pattern matching existing 004 precedent (runner skips applied migrations)
  - Update `schema_meta` row: insert/update v4.2 marker (NOT v4.1 — already there)
- [x] 0.2 Update `aria_layer1/schema.sql` (canonical):
  - Add `spec_id TEXT` to `CREATE TABLE dispatches` column list (between `pr_id` and `fail_reason` per existing ordering convention)
  - Update header version comment **v4.1 → v4.2** (NOT v4.0→v4.1 — current is v4.1)
- [x] 0.3 Update `aria_layer1/schema_migrate.py`:
  - Add migration registry entry `("006", "006_schema_v4.2_add_spec_id.sql", "4.1", "4.2")` (from_version, to_version)
  - Bump `_LATEST_SCHEMA_VERSION = "4.2"` (was "4.1")
- [x] 0.4 Update `aria_layer1/db.py` `DispatchRepository.create_dispatch` + helpers to optionally accept/read `spec_id` (default None)
- [x] 0.5 Unit test `test_t_schema_v4_2_migration.py`:
  - Migration adds spec_id column to **v4.1** DB (not v4.0 — current baseline is v4.1) → version becomes v4.2
  - Re-run idempotent (no error on existing v4.2 DB; migration-version guard skips)
  - Existing dispatches rows have spec_id=NULL after migration
- [x] 0.6 Drift-guard test (per `feedback_validator_repo_drift_guard_test`): committed `schema.sql` matches migrations **003 + 004 + 005 + 006** cumulative result

### T1 — Layer 1 spec_id write **at S1_SCAN** (per HIGH backend-H2 fix, ~1h; depends on T1.0)

- [x] 1.1 In `extension.py::_handle_s1_scan` (or equivalent S1_SCAN handler): when issue.yaml has `linked_spec_id` field (validated by T1.0 schema), `UPDATE dispatches SET spec_id=? WHERE dispatch_id=? AND spec_id IS NULL` (CAS guard)
- [x] 1.2 Audit event: emit `rework_cycle` with payload `outcome=spec_id_written`, `spec_id=<value>` at S1_SCAN time (not S5)
- [x] 1.3 Unit test in new `test_t_spec_id_write.py`: 2 cases — (a) seed dispatch + issue.yaml with linked_spec_id → verify UPDATE applied; (b) issue.yaml without linked_spec_id → spec_id stays NULL graceful skip
- [x] 1.4 Document: spec_id sourced from issue.yaml `linked_spec_id` field (e.g. user pre-fills when creating issue from Spec template). Layer 2 result.json does NOT carry spec_id (T2.9 has spec_id removed).

**Note**: T1.5 (Layer 1 S5_AWAIT result.json read for new_pr_id, CRIT-1 fix) merged into T3.1 since both fire in the same `_handle_s5_await` terminal-path branch. **T3.1 + T6.6** (`test_t_close_old_pr.py` — note T6.5 is the bash commit-lint-validate test, not the close-old-pr test) covers the unit test scenarios (redo dispatch alloc terminates with result.json → Layer 1 binds pr_id correctly + audit `state_transition` payload `new_pr_id_from_result_json=true`).

---

## Phase 2 — Layer 2 redo handler + dispatcher swap (T2, 12h, Spec Y main body)

### T2 — modes/redo.sh + entrypoint.sh redo branch swap

- [x] 2.1 (~0.5h) entrypoint.sh: replace `redo) ... exit 1` branch with `redo) exec /opt/aria-runner/modes/redo.sh "$@" ;;`
- [x] 2.2 (~2h) modes/redo.sh skeleton + globals (mirror modes/changes.sh §"Globals" section; same defaults, same env var consumption including NOMAD_META_REWORK_ROUND per T-pre.2)
- [x] 2.3 (~1.5h) Forgejo PR fetch (curl + jq). **Always create `lib/forgejo-helpers.sh`** (per C10 v2 decision; drop "if duplication > 50 lines" guard) — by (a) **extracting** existing `forgejo_get_retry` from `modes/changes.sh`; (b) **writing new** `forgejo_post_retry` + `forgejo_patch_retry` using same retry pattern. Both modes/changes.sh + modes/redo.sh source this helper
- [ ] 2.4 (~2h) Fresh-checkout from `base.ref` (NOT head.ref): `git clone --depth 1 --branch ${BASE_BRANCH} ...` + create new branch via `git checkout -b aria/redo-${PARENT_PR_ID}-${REWORK_ROUND}-$(date +%Y%m%dT%H%M%S)` (REWORK_ROUND now real env var from T-pre, no `:-1` fallback in branch name)
- [ ] 2.5 (~2h) Prompt assemble — redo-specific (3 sections only, NO diff section per AD-M5-3 narrowing). **Explicit char caps per HIGH ai-5**:
  - Section 1: feedback ≤4KB (Layer 1 truncated upstream, inherited from Spec X T4.4)
  - Section 2: issue body ≤10K chars (`head -c 10240 ${INPUTS_DIR}/<dispatch_id>/issue.yaml`)
  - Section 3: "supersedes PR #<id>" reference ≤500 chars (literal sentence; deliberately discards prior diff)
  - **Total hard cap ≤15KB**; overflow → `S_FAIL(prompt_overflow)` per Spec X T4.4 case 5 precedent
  - **Appendix literal directive per HIGH ai-7** (Spec X T4.3 R2 F1 pattern): append to prompt: `IMPORTANT: After your code changes, output a single final line in plain text: 'commit_message: <type>(<scope>): <description>'` — used by T2.6 extraction
- [ ] 2.6 (~1.5h) claude -p positional + parse output + extract `commit_message: ...` line (per T2.5 directive) OR fallback `chore(redo-${PARENT_PR_ID}): redo PR-${PARENT_PR_ID} round ${REWORK_ROUND}`
- [ ] 2.7 (~1h) `git push origin <new_branch>` (regular push, NOT force-push)
- [ ] 2.8 (~1.5h) Forgejo create new PR with **literal title template per R2-NEW-11**:
  ```bash
  forgejo_post_retry "/repos/${ORG}/${REPO}/pulls" \
    --data "$(jq -n \
      --arg title "Aria redo: PR-${PARENT_PR_ID} round ${REWORK_ROUND}" \
      --arg head "${NEW_BRANCH}" \
      --arg base "${BASE_BRANCH}" \
      --arg body "Supersedes #${PARENT_PR_ID} (Aria redo mode round ${REWORK_ROUND}); fresh checkout from \`${BASE_BRANCH}\`" \
      '{title: $title, head: $head, base: $base, body: $body}')"
  ```
  Parse response for new pr_id via `jq '.number'`
- [ ] 2.9 (~0.5h) result.json write with **only** `new_pr_id` + `parent_pr_id` (spec_id REMOVED per R2-NEW-9 — Layer 1 S1_SCAN writes spec_id from issue.yaml linked_spec_id per T1.1, NOT Layer 2)

---

## Phase 3 — OS-3 close-old-PR (T3, 2h; PATCH-first sequence per backend-H1 v2 + R2-NEW-4)

### T3 — Layer 1 `_handle_s5_await` terminal-path close-old-PR (per CRIT-1 fix — NOT `_handle_s5_pr_created` which doesn't exist)

- [ ] 3.1 (~0.5h) In `extension.py::_handle_s5_await` terminal branch (exit_code=0): detect redo dispatch (`rework_mode='redo' AND rework_of IS NOT NULL AND new_pr_id in result.json`); UPDATE dispatches SET pr_id=<new> WHERE dispatch_id=? (replaces find_or_create_pr for redo); audit event `state_transition` payload `new_pr_id_from_result_json=true`
- [ ] 3.2 (~0.3h) Read parent dispatch row via `rework_of` → parent.pr_id; **guard NULL parent pr_id** (audit warn `parent_no_pr` + skip close) per qa-H5
- [ ] 3.3 (~0.5h) **PATCH-FIRST per backend-H1 v2**: Forgejo PATCH `/repos/<org>/<repo>/issues/<parent_pr_id> {state: "closed"}` with **3 retries on 5xx** (Forgejo PR is issue subtype); on 409/422 (already closed) → treat as success continue to T3.4; on 4xx (not 409/422) → audit `close_failed_4xx` + skip comment; on 5xx exhausted → audit `close_failed_5xx` + skip comment + don't block new PR
- [ ] 3.4 (~0.3h) On PATCH success (incl. already-closed): Forgejo POST comment on parent PR: `_Superseded by #<new>_ (Aria redo round ${round})` — round from `dispatch.rework_round` query; on comment fail → audit `comment_only_succeeded` (acceptable; old PR is closed, primary goal achieved)
- [ ] 3.5 (~0.2h) Audit event `rework_cycle` outcome ∈ `{old_pr_closed | comment_only_succeeded | close_failed_4xx | close_failed_5xx | parent_no_pr}`, payload=`{parent_pr_id, new_pr_id, superseded_comment_id?, round, http_status?, retries?}`
- [ ] 3.6 Error handling matrix (enumerated per qa-H5):
  - Network timeout (distinct from HTTP error) → retry as 5xx (3 retries)
  - Parent PR already closed (409/422) → continue to comment (still post supersede note)
  - rework_of resolves to dispatch with pr_id=NULL → audit warn `parent_no_pr` + skip both PATCH+comment (don't fail dispatch)
  - PATCH success + comment 4xx/5xx → audit `comment_only_succeeded` (primary goal met)
  - PATCH fail after 3 retries → audit `close_failed_5xx` + skip comment + don't block new PR creation (owner can manually close)

---

## Phase 4 — OS-4 spec_drift full impl (T4, 3h, independent)

### T4 — spec_drift_input_fetcher production impl (per CRIT-4 + qa-H6 v2 fixes)

- [ ] 4.1 (~0.5h) Replace M5 stub `spec_drift_input_fetcher` empty-return (`reconcile_runner.py:213-221`) with full impl
- [ ] 4.2 (~1h) Read `openspec/changes/<spec_id>/proposal.md` from Aria main repo via Forgejo raw content API: `GET /repos/<aria_org>/<aria_repo>/raw/branch/<branch>/<path>`. **On 404 fall back per qa-H6**: try `openspec/archive/*-<spec_id>/proposal.md` — use Forgejo `GET /repos/<aria_org>/<aria_repo>/contents/openspec/archive` to list directory entries, find prefix-match `*-<spec_id>`, fetch from matched path. Audit log records which path used (`source: changes | archive | not_found`)
- [ ] 4.3 (~1h) Read PR diff via `GET /repos/<org>/<repo>/pulls/<pr_id>.diff` (Forgejo diff endpoint)
- [ ] 4.4 (~0.5h) Return **3-tuple `(spec_what, spec_acceptance, pr_diff)`** matching `reconciler.py:1014` unpack contract (per CRIT-4 v2 fix). Internally call `extract_spec_sections(proposal_text)` from existing `spec_drift.py:104-128` to slice §What + §验收 sections. spec_id and pr_id are **internal lookup keys**, NOT output fields. NOT a named tuple; plain 3-tuple
- [ ] 4.5 Unit tests `test_t_spec_drift_fetcher.py` (5 cases):
  - (a) stub-replaced (existing reconciler test still passes with full impl)
  - (b) missing spec_id (NULL in dispatch row) → return empty 3-tuple `("", "", "")` graceful
  - (c) proposal.md fetch success from `openspec/changes/<id>/`
  - (d) archive-path fallback: changes/ returns 404 → archive/ matched + fetched
  - (e) reconciler.py:1014 unpack contract test (assert `spec_what, spec_accept, pr_diff = fetcher_result` succeeds)

---

## Phase 5 — OS-5 commit-lint retry (T5, 2h, shared lib)

### T5 — Commit-lint Layer 2 retry hook (CRIT-2 fix: **shell-port**, not Python; renumbered per R2-NEW-3)

- [ ] 5.1 (~0.7h) Create `docker/aria-runner/lib/commit-lint-validate.sh` (~30 lines): bash regex validator per `standards/conventions/git-commit.md:40-53` valid types `{feat|fix|chore|refactor|test|docs|style|perf|build|ci}` + subject line ≤72 chars. Exit 0 if valid, exit 1 if invalid. NO Python dependency.
- [ ] 5.2 (~0.5h) Create `docker/aria-runner/lib/commit-lint-retry.sh` shared helper:
  - Function `commit_lint_retry_loop()` taking COMMIT_MSG + MAX_RETRY (default 3)
  - Calls `bash /opt/aria-runner/lib/commit-lint-validate.sh "$msg" >/dev/null 2>&1` (NOT Python)
  - Loop: validate → if fail, `timeout -k 10s ${CLAUDE_TIMEOUT_S:-60} claude -p` rewrite (using `${ARIA_MODEL}` opus per HIGH ai-4 decision) → git commit --amend → retry (max 3)
  - On 3rd fail: exit with S_FAIL(commit_lint_exhausted) — write result.json + exit 1
- [ ] 5.3 (~0.5h) Update modes/changes.sh: source `lib/commit-lint-retry.sh` + call `commit_lint_retry_loop` after `git commit` before `git push`
- [ ] 5.4 (~0.5h) Update modes/redo.sh: same source + call pattern
- [ ] 5.5 (~0.5h) Unit test `test_t_commit_lint_retry.py` (Python retry-loop integration only — validator regex correctness covered by separate bash test `tests/changes-mode/commit-lint-validate.sh` per R2-NEW-6):
  - 4 cases (valid first try / invalid then valid after retry / 3-retry exhaust → S_FAIL exit 1 + result.json written / claude rewrite fixture mocked)

---

## Phase 6 — Acceptance (T6, 2h)

### T6 — Synthetic tests (~32 cases total, enumerated per qa-H7)

- [ ] 6.1 `tests/changes-mode/redo-dispatcher.sh` (3 cases): redo→modes/redo.sh / unknown still fails / initial still works (regression for Spec X T3.5 backward compat)
- [ ] 6.2 `tests/changes-mode/mode_redo-prompt.sh` (5 cases): feedback / issue body / no diff section / CJK / boundary (overflow→S_FAIL prompt_overflow per T2.5 caps)
- [ ] 6.3 `tests/changes-mode/mode_redo-git.sh` (4 cases): fresh checkout from base.ref / new branch creation with timestamp / regular push (NOT force-push) / new PR creation with title template
- [ ] 6.4 `tests/changes-mode/redo-result-pr.sh` (2 cases; **renamed** from `close-old-pr-layer2.sh` per R2 MEDIUM — Layer 2 only writes new_pr_id, closure is Layer 1): Layer 2 result.json includes new_pr_id + parent_pr_id (no spec_id per R2-NEW-9) / fail-to-create-new-PR → no close action triggered
- [ ] 6.5 **NEW per R2-NEW-6** `tests/changes-mode/commit-lint-validate.sh` (4 cases): valid CC format (`feat(scope): desc`) → exit 0 / invalid format (`bad msg`) → exit 1 / 72-char boundary (exactly 72 → pass; 73 → fail) / CJK in description allowed
- [ ] 6.6 Python `test_t_close_old_pr.py` (3 cases): S5_AWAIT terminal-path handler detects redo dispatch + binds new_pr_id / PATCH-first then comment sequence (per R2-NEW-4) / 4xx fallback (audit `close_failed_4xx`) — additional graceful for parent PR already closed 409/422 covered inline
- [ ] 6.7 Python `test_t_spec_drift_fetcher.py` (5 cases per T4.5; includes archive-path fallback + 3-tuple unpack contract)
- [ ] 6.8 Python `test_t_commit_lint_retry.py` (4 cases per T5.5; retry-loop integration only — regex correctness in T6.5 bash test)
- [ ] 6.9 Python `test_t_schema_v4_2_migration.py` (3 cases per T0.5+T0.6; v4.1→v4.2 migration adds spec_id + idempotent + drift-guard cumulative 003+004+005+006)
- [ ] 6.10 Python `test_t_spec_id_write.py` (2 cases per T1.3)
- [ ] 6.11 Spec X regression enumerated commands (per qa-H7 + Spec X T6.3 pattern):
  ```bash
  bash docker/aria-runner/tests/changes-mode/dispatcher.sh
  bash docker/aria-runner/tests/changes-mode/mode_changes-prompt.sh   # T-pre.5 modified
  bash docker/aria-runner/tests/changes-mode/mode_changes-git.sh
  bash docker/aria-runner/tests/changes-mode/forgejo-errors.sh
  bash docker/aria-runner/tests/compute-assertions/test.sh
  bash docker/aria-runner/tests/parse-stream-json/test.sh
  bash docker/aria-runner/tests/push-classifier/test.sh
  # Total: 7 bash files = 51 cases (excl. t3-verify.sh which requires Docker image, owner-run)
  cd hermes-extensions/aria-layer1 && python3 -m unittest discover tests -v
  # Total Python: 812 tests (will become 812 + new T6.x cases after Spec Y impl)
  ```
- [ ] 6.12 **HCL validate** (per R2 MEDIUM + `feedback_nomad_hcl_validate_early`): HCL CHANGED by T-pre.2 (REWORK_ROUND 5th key); MUST run `nomad job validate nomad/jobs/aria-layer2-runner.hcl` post-edit — NOT smoke "unchanged" assumption
- [ ] 6.13 Test count target: **≥32 new behavioral cases** (case-counted per Spec X R2 NEW-1 fix; enumeration: 3+5+4+2+4+3+5+4+3+2 = 35 new cases including 4 bash commit-lint + 3 schema migration + 2 spec_id_write; rounding ~32 for buffer)

---

## Phase 7 — Side-effect Patches (T7, 1h, parallel with T2+)

### T7 — Doc patches

- [ ] 7.1 `aria-orchestrator/docs/m5-handoff.yaml::open_issues_for_m6`:
  - M5-OS-2 `absorbed_by: aria-2.0-m5-carryover-layer2-redo-mode-aux` (Spec Y)
  - M5-OS-3 `absorbed_by: aria-2.0-m5-carryover-layer2-redo-mode-aux`
  - M5-OS-4 `absorbed_by: aria-2.0-m5-carryover-layer2-redo-mode-aux`
  - M5-OS-5 `absorbed_by: aria-2.0-m5-carryover-layer2-redo-mode-aux`
- [ ] 7.2 `aria-orchestrator/docs/architecture-decisions.md::AD-M5-3` append (per CRIT-5 v2 + ai-3 narrowing):
  - **APPEND BELOW the existing 2026-05-16 Spec X line — DO NOT replace or delete it. AD is immutable append-only per Spec X R2 C2 convention.**
  - Literal text to append:
    ```
    > **更新 2026-05-XX (Spec Y)**: Spec Y (redo-mode + close-old-PR + spec_drift + commit-lint) shipped; M5 carryover trio complete. **Layer 1↔Layer 2 contract bumped 4→5 keys** (REWORK_ROUND added; per T-pre fix for changes-mode latent bug). **Prompt strategy narrowing**: redo mode = 3 sections (feedback + issue body + supersedes ref, NO diff section); changes mode = 4 sections per original AD-M5-3 lock.
    ```
- [ ] 7.3 `docs/requirements/user-stories/US-025.md` footer "M5 Carryover Sub-Specs" table — mark Spec Y row done
- [ ] 7.4 `docs/handoff/2026-05-15-us025-m5-c2-d1-done.md` — add Addendum 3 noting Spec Y cycle complete
- [ ] 7.5 `aria-orchestrator/docs/validate-m5-handoff.py` — extend `check_m6_carryover_to_us_026_present` (Spec X T7.4 deferred this) to also verify Spec Y absorption fields (M5-OS-2/3/4/5 `absorbed_by` set to spec-y change ID)
- [ ] 7.6 NOT touching `prd-aria-v2.md` (per D4)

---

## Phase 8 — Phase C+D bookkeeping (T8)

### T8 — Standard 10-step + R1+R2 fixes carry-forward from Spec X

- [ ] 8.1 Per-task-group commits with Conventional Commits format. **Enumerated Spec Y examples per C9 v2**:
  - T-pre: `chore(spec-y): T-pre REWORK_ROUND 5-key contract + Spec X latent bug retro-fix`
  - T0: `feat(spec-y): T0 schema 006 v4.1→v4.2 add spec_id column`
  - T1.0: `feat(spec-y): T1.0 M1 issue schema linked_spec_id optional field`
  - T1: `feat(spec-y): T1 Layer 1 spec_id write at S1_SCAN + T1.5 S5_AWAIT result.json read`
  - T2: `feat(spec-y): T2 modes/redo.sh + entrypoint redo branch swap`
  - T3: `feat(spec-y): T3 OS-3 close-old-PR via PATCH-first sequence`
  - T4: `feat(spec-y): T4 spec_drift_input_fetcher full impl + archive fallback`
  - T5: `feat(spec-y): T5 commit-lint Layer 2 retry shell-port`
  - T6: `test(spec-y): T6 synthetic acceptance ~32 cases`
  - T7: `docs(spec-y): T7 side-effect patches (AD-M5-3 append + US-025 + handoff Addendum 3 + validate-m5-handoff extension)`
- [ ] 8.2 Phase B.3 mid_implementation audit trigger eval (same proportionality as Spec X — defer to pre_merge)
- [ ] 8.3 Phase C.2 aria-orchestrator PR + dual-repo pre-merge gate per Rule #8 (skip_with_warning fallback if no aether)
- [ ] 8.4 aria-orchestrator merge → submodule bump in Aria main feature branch (post-merge master SHA, NOT feature branch HEAD per `feedback_submodule_pointer_post_merge_bump`)
- [ ] 8.5 Aria main repo PR + Rule #8 gate + merge
- [ ] 8.6 Dual-push 4-way SHA parity verify (Forgejo origin + GitHub for both repos)
- [ ] 8.7 Phase D.1: US-025 footer Spec Y row marked done (T7.3 already done in Phase B; verify still consistent)
- [ ] 8.8 Phase D.2: openspec archive `aria-2.0-m5-carryover-layer2-redo-mode-aux` → `openspec/archive/2026-XX-XX-...`
- [ ] 8.9 Rule #9 trigger evaluation per session
- [ ] 8.10 Verify US-025 close-gate progress: now `Spec X archived + Spec Y archived` = 2 of 4 AI/owner gates complete; remaining T-deploy + Tier-1 live LLM owner action

---

## Status

- [x] T0 Spec drafted v1 (Phase A.1 done 2026-05-16; concise via Spec X cross-ref)
- [x] Phase A.2 R1 audit (4-agent: backend-architect + qa-engineer + code-reviewer + ai-engineer; 37 findings 6 CRIT) — report `.aria/audit-reports/post_spec-R1-2026-05-16T0530Z-aria-2.0-m5-carryover-layer2-redo-mode-aux-summary.md`
- [x] v2 fixes applied 2026-05-16 (commit `9de6f1f`) — addresses 6 CRIT in fix table + key HIGH
- [x] Phase A.2 R2 verify audit (3-agent: tech-lead + qa-engineer + code-reviewer; ~22 findings, 1 NEW CRIT + ~10 HIGH; 5/6 R1 CRIT body+tasks propagation incomplete) — report `.aria/audit-reports/post_spec-R2-2026-05-16T2242Z-aria-2.0-m5-carryover-layer2-redo-mode-aux-summary.md`
- [x] v3 fixes applied 2026-05-17 — body+tasks propagation + R2-NEW-1 schema v4.2 + 10 HIGH (commit `7680da6`)
- [x] Phase A.2 R3 stability audit (3-agent unanimous PASS: tech-lead + qa-engineer + code-reviewer — 7/7 CRIT closed + 17/17 HIGH closed + 4 minor surgical-fixed) — report `.aria/audit-reports/post_spec-R3-2026-05-17T03Z-aria-2.0-m5-carryover-layer2-redo-mode-aux-summary.md`
- [x] Spec Status → **Approved** (2026-05-17)
- [ ] T-pre + T0 + T1.0 + T1-T7 Phase B (~24.8h AI-runnable)
- [ ] T8 Phase C+D

**当前 Phase**: **A.3** (Spec Approved, ready for task-planner + B.1 branch creation — feature branch already exists)
