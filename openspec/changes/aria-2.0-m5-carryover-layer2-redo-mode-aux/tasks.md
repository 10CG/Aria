# Spec Y Tasks — Aria 2.0 M5 Carryover Layer 2 redo-mode + aux

> **Change ID**: `aria-2.0-m5-carryover-layer2-redo-mode-aux`
> **Parent**: US-025 (M5 carryover, second of trio after Spec X)
> **Estimate v2**: ~20h AI-runnable (T-pre+T0+T1+T2+T3+T4+T5+T6+T7 = 0.5+1+1+12+2+3+2+2+1 = 24.5h post-overhead; OS line items 12+2+3+2 = 19h core + 1h CRIT-3 REWORK_ROUND retro-fix)
> **Sibling Spec X**: archived at `openspec/archive/2026-05-16-aria-2.0-m5-carryover-layer2-changes-mode/`
> **Phase B sequencing**: T-pre + T0 + T2 + T4 + T5 parallel-able; T1 ⏸ T0 + S1_SCAN spec_id write; T3 ⏸ T2 + S5_AWAIT result.json read; T6 ⏸ T2-T5; T7 doc only
> **R1→v2 fix manifest**: 6 CRIT + ~13 HIGH applied (see proposal.md §"R1 → v2 fixes"); ~10 MED + ~8 LOW deferred to R2 verification next session

---

## Task Group 总览 (v2 post-R1 fixes)

| ID | 标题 | 工时 | 阻塞 |
|----|------|------|------|
| **T-pre** | **NEW (CRIT-3)** REWORK_ROUND propagation: Layer 1 extra_meta + HCL meta_optional 5th key + retro-fix Spec X latent | 0.5h | — |
| T0 | Schema v4.1 migration **006_schema_v4.1_add_spec_id.sql** (renumbered per CRIT-6) | 1h | — |
| T1 | Layer 1 spec_id write **at S1_SCAN** (per HIGH backend-H2 — read issue.yaml linked_spec_id) | 1h | T0 |
| T2 | modes/redo.sh impl (OS-2) + entrypoint.sh swap redo branch | 12h | T-pre |
| T3 | OS-3 close-old-PR via **PATCH-first then comment** (per HIGH backend-H1 reversed sequence) + Layer 1 S5_AWAIT terminal handler reads result.json for new_pr_id (per CRIT-1) | 2h | T2 |
| T4 | OS-4 spec_drift_input_fetcher full impl — return **3-tuple** matching reconciler unpack (per CRIT-4); archive-path fallback per HIGH qa-H6 | 3h | T0 + T1 |
| T5 | OS-5 commit-lint Layer 2 retry — **shell-port** via lib/commit-lint-validate.sh (per CRIT-2); same ${ARIA_MODEL} for retry calls per HIGH ai-4 | 2h | T2 |
| T6 | Synthetic acceptance tests (~25 cases, enumerated per HIGH qa-H7) | 2h | T2-T5 |
| T7 | Side-effect patches — T7.2 explicit "preserve Spec X 2026-05-16 line" guard per CRIT-5 + AD-M5-3 narrowing note per HIGH ai-3 | 1h | T2 (parallel) |
| T8 | Phase C+D (dual-repo merge + archive + Rule #9 handoff trigger) | (standard) | T6+T7 |

总: ~24h with bookkeeping; core OS items ~19h

---

## Phase 0 — T-pre REWORK_ROUND propagation (CRIT-3 retro-fix, 0.5h)

### T-pre — Add 5th meta_optional key REWORK_ROUND

- [ ] pre.1 Extend `aria_layer1/extension.py::_handle_s4_launch` extra_meta when `rework_mode IN ('changes','redo')`: add `"REWORK_ROUND": str(dispatch.get("rework_round") or 1)`
- [ ] pre.2 Update HCL `nomad/jobs/aria-layer2-runner.hcl` meta_optional list: add 5th key `"REWORK_ROUND"`
- [ ] pre.3 Update existing audit `meta_optional_written` payload `rework_keys_written` list to include `REWORK_ROUND` (5 keys total)
- [ ] pre.4 Update Spec X test `tests/test_t_changes_mode_meta.py` (modify existing assertions): REWORK_ROUND key present in meta + value matches dispatch.rework_round
- [ ] pre.5 Update Spec X bash test `tests/changes-mode/mode_changes-prompt.sh` to verify NOMAD_META_REWORK_ROUND env consumed (modes/changes.sh:174 fallback `${REWORK_ROUND:-1}` now correctly resolves)
- [ ] pre.6 Update AD-M5-3 contract section: 4-key → **5-key** Layer 1↔Layer 2 meta contract (architecture-decisions.md:3585-3596 append note)

---

## Phase 1 — Schema + Layer 1 (T0+T1, 2h, T0 unblocks T1+T4)

### T0 — Schema v4 → v4.1 additive migration (~1h)

- [ ] 0.1 Create `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/migrations/006_schema_v4.1_add_spec_id.sql` (**renumbered from 005 per CRIT-6** — 005 already occupied by M5 T1.5 005_schema_v4_drop_inline_uq.sql):
  - `ALTER TABLE dispatches ADD COLUMN spec_id TEXT;` (nullable, no default; idempotent via `IF NOT EXISTS` pattern OR migration-version guard)
  - Update `schema_meta` row inserting v4.1 marker
- [ ] 0.2 Update `aria_layer1/schema.sql` (canonical):
  - Add `spec_id TEXT` to `CREATE TABLE dispatches` column list (between `pr_id` and `fail_reason` per existing ordering convention)
  - Update header version comment v4.0 → v4.1
- [ ] 0.3 Update `aria_layer1/db.py` `DispatchRepository.create_dispatch` + helpers to optionally accept/read `spec_id` (default None)
- [ ] 0.4 Unit test `test_t_schema_v4_1_migration.py`:
  - Migration adds spec_id column to v4.0 DB
  - Re-run idempotent (no error on existing v4.1 DB)
  - Existing dispatches rows have spec_id=NULL after migration
- [ ] 0.5 Drift-guard test (per `feedback_validator_repo_drift_guard_test`): committed `schema.sql` matches migration **004 + 005 + 006** cumulative result

### T1 — Layer 1 spec_id write **at S1_SCAN** (per HIGH backend-H2 fix, ~1h)

- [ ] 1.1 In `extension.py::_handle_s1_scan` (or equivalent S1_SCAN handler): when issue.yaml has `linked_spec_id` field, `UPDATE dispatches SET spec_id=? WHERE dispatch_id=? AND spec_id IS NULL` (CAS guard)
- [ ] 1.2 Audit event: emit `rework_cycle` with payload `outcome=spec_id_written`, `spec_id=<value>` at S1_SCAN time (not S5)
- [ ] 1.3 Unit test in new `test_t_spec_id_write.py`: seed dispatch + issue.yaml with linked_spec_id → verify UPDATE applied
- [ ] 1.4 Document: spec_id sourced from issue.yaml `linked_spec_id` field (e.g. user pre-fills when creating issue from Spec template). Layer 2 result.json does NOT need to include spec_id (removes T2.9 dependency on Layer 2 deriving).

### T1.5 — Layer 1 S5_AWAIT result.json read for new_pr_id (CRIT-1 fix, included in T3 effort)

- [ ] 1.5.1 In `extension.py::_handle_s5_await` terminal path (alloc exit_code=0): when `rework_mode='redo' AND new_pr_id in result.json`, extract new_pr_id + UPDATE dispatches SET pr_id=<new> WHERE dispatch_id=? (replaces find_or_create_pr path for redo dispatches)
- [ ] 1.5.2 Audit event: `state_transition` payload `new_pr_id_from_result_json=true`
- [ ] 1.5.3 Unit test: redo dispatch alloc terminates with result.json containing new_pr_id → Layer 1 binds pr_id correctly

---

## Phase 2 — Layer 2 redo handler + dispatcher swap (T2, 12h, Spec Y main body)

### T2 — modes/redo.sh + entrypoint.sh redo branch swap

- [ ] 2.1 (~0.5h) entrypoint.sh: replace `redo) exit 1 ...` with `redo) exec /opt/aria-runner/modes/redo.sh "$@" ;;`
- [ ] 2.2 (~2h) modes/redo.sh skeleton + globals (mirror modes/changes.sh §"Globals" section; same defaults, same env var consumption)
- [ ] 2.3 (~1.5h) Forgejo PR fetch (curl + jq; reuse modes/changes.sh `forgejo_get_retry` pattern; consider extracting to `lib/forgejo-helpers.sh` if duplication > 50 lines)
- [ ] 2.4 (~2h) Fresh-checkout from `base.ref` (NOT head.ref): `git clone --depth 1 --branch ${BASE_BRANCH} ...` + create new branch via `git checkout -b aria/redo-${PARENT_PR_ID}-${REWORK_ROUND:-1}-$(date +%Y%m%dT%H%M%S)`
- [ ] 2.5 (~2h) Prompt assemble — redo-specific (3 sections only, NO diff section):
  - Section 1: feedback
  - Section 2: issue body (`${INPUTS_DIR}/<dispatch_id>/issue.yaml`)
  - Section 3: "supersedes PR #<id>" reference (deliberately discards prior diff)
- [ ] 2.6 (~1.5h) claude -p positional + parse output + extract commit_message OR fallback `chore(redo-${PARENT_PR_ID}): redo PR-${PARENT_PR_ID} round ${REWORK_ROUND:-1}`
- [ ] 2.7 (~1h) `git push origin <new_branch>` (regular push, NOT force-push)
- [ ] 2.8 (~1.5h) Forgejo create new PR: `POST /repos/<org>/<repo>/pulls -d '{title, head, base}'`; parse response for new pr_id
- [ ] 2.9 (~0.5h) result.json write with `new_pr_id`, `parent_pr_id`, `spec_id` (if can derive from issue body or env)

---

## Phase 3 — OS-3 close-old-PR (T3, 2h)

### T3 — Layer 1 S5_PR_CREATED close-old-PR

- [ ] 3.1 (~0.5h) In `extension.py::_handle_s5_pr_created`: detect redo dispatch (`rework_mode='redo' AND rework_of IS NOT NULL`)
- [ ] 3.2 (~0.5h) Read parent dispatch row via `rework_of` → parent.pr_id
- [ ] 3.3 (~0.5h) Forgejo POST comment on parent PR: `_Superseded by #<new>_ (Aria redo round <N>)`
- [ ] 3.4 (~0.3h) Forgejo PATCH `/issues/<parent_pr_id> {state: "closed"}` (Forgejo PR is issue subtype)
- [ ] 3.5 (~0.2h) Audit event `rework_cycle` outcome=`old_pr_closed`, payload=`{parent_pr_id, new_pr_id, superseded_comment_id}`
- [ ] 3.6 Error handling: 4xx/5xx → audit warn + don't block new PR (best-effort per Spec §B risk mitigation)

---

## Phase 4 — OS-4 spec_drift full impl (T4, 3h, independent)

### T4 — spec_drift_input_fetcher production impl

- [ ] 4.1 (~0.5h) Replace M5 stub `spec_drift_input_fetcher` empty-return with full impl
- [ ] 4.2 (~1h) Read `openspec/changes/<spec_id>/proposal.md` from Aria main repo (Forgejo raw content API: `GET /repos/<aria_org>/<aria_repo>/raw/branch/<branch>/<path>`)
- [ ] 4.3 (~1h) Read PR diff via `GET /repos/<org>/<repo>/pulls/<pr_id>.diff` (Forgejo diff endpoint)
- [ ] 4.4 (~0.5h) Return both as `SpecDriftInputs(proposal_text, pr_diff, spec_id, pr_id)` named tuple
- [ ] 4.5 Unit tests `test_t_spec_drift_fetcher.py`:
  - 5 cases (stub→full, missing spec_id graceful, proposal.md fetch success, PR diff fetch success, both fetch + return tuple)

---

## Phase 5 — OS-5 commit-lint retry (T5, 2h, shared lib)

### T5 — Commit-lint Layer 2 retry hook (CRIT-2 fix: **shell-port**, not Python)

- [ ] 5.1 (~0.7h, +0.2h vs v1) Create `docker/aria-runner/lib/commit-lint-validate.sh` (~30 lines): bash regex validator per `standards/conventions/git-commit.md:40-53` valid types `{feat|fix|chore|refactor|test|docs|style|perf|build|ci}` + subject line ≤72 chars. Exit 0 if valid, exit 1 if invalid. NO Python dependency.
- [ ] 5.2 (~0.5h) Create `docker/aria-runner/lib/commit-lint-retry.sh` shared helper:
  - Function `commit_lint_retry_loop()` taking COMMIT_MSG + MAX_RETRY (default 3)
  - Calls `bash /opt/aria-runner/lib/commit-lint-validate.sh "$msg"` (NOT Python)
  - Loop: validate → if fail, `timeout -k 10s ${CLAUDE_TIMEOUT_S:-60} claude -p` rewrite (using `${ARIA_MODEL}` opus per HIGH ai-4 decision) → git commit --amend → retry (max 3)
  - On 3rd fail: exit with S_FAIL(commit_lint_exhausted) — write result.json + exit 1
- [ ] 5.2 (~0.5h) Update modes/changes.sh: call `commit_lint_retry_loop` after `git commit` before `git push`
- [ ] 5.3 (~0.5h) Update modes/redo.sh: same call pattern
- [ ] 5.4 Unit test `test_t_commit_lint_retry.py`:
  - 4 cases (valid first try / invalid then valid after retry / 3-retry exhaust / claude rewrite fixture)

---

## Phase 6 — Acceptance (T6, 2h)

### T6 — Synthetic tests (~23 cases total)

- [ ] 6.1 `tests/changes-mode/redo-dispatcher.sh` (3 cases): redo→modes/redo.sh / unknown still fails / initial still works (regression for Spec X T3.5 backward compat)
- [ ] 6.2 `tests/changes-mode/mode_redo-prompt.sh` (5 cases): feedback/issue body/no diff section/CJK/boundary
- [ ] 6.3 `tests/changes-mode/mode_redo-git.sh` (4 cases): fresh checkout base / new branch creation / regular push / new PR creation
- [ ] 6.4 `tests/changes-mode/close-old-pr-layer2.sh` (2 cases): Layer 2 result.json includes new_pr_id / fail to create new PR → no close action
- [ ] 6.5 Python `test_t_close_old_pr.py` (3 cases): S5 handler detects redo dispatch / Forgejo PATCH + comment / 4xx fallback
- [ ] 6.6 Python `test_t_spec_drift_fetcher.py` (5 cases per T4.5)
- [ ] 6.7 Python `test_t_commit_lint_retry.py` (4 cases per T5.4)
- [ ] 6.8 Python `test_t_schema_v4_1_migration.py` (2 cases per T0.4)
- [ ] 6.9 Spec X regression — all 51 bash + 812 Python from Spec X archived state still PASS
- [ ] 6.10 nomad job validate (HCL unchanged but smoke verify)
- [ ] 6.11 Test count target: ≥23 new behavioral cases (case-counted per Spec X R2 NEW-1 fix)

---

## Phase 7 — Side-effect Patches (T7, 1h, parallel with T2+)

### T7 — Doc patches

- [ ] 7.1 `aria-orchestrator/docs/m5-handoff.yaml::open_issues_for_m6`:
  - M5-OS-2 `absorbed_by: aria-2.0-m5-carryover-layer2-redo-mode-aux` (Spec Y)
  - M5-OS-3 `absorbed_by: aria-2.0-m5-carryover-layer2-redo-mode-aux`
  - M5-OS-4 `absorbed_by: aria-2.0-m5-carryover-layer2-redo-mode-aux`
  - M5-OS-5 `absorbed_by: aria-2.0-m5-carryover-layer2-redo-mode-aux`
- [ ] 7.2 `aria-orchestrator/docs/architecture-decisions.md::AD-M5-3` append: `> **更新 2026-05-XX**: Spec Y (redo + close-old-PR + spec_drift + commit-lint) shipped; M5 carryover trio complete`
- [ ] 7.3 `docs/requirements/user-stories/US-025.md` footer "M5 Carryover Sub-Specs" table — mark Spec Y row done
- [ ] 7.4 `docs/handoff/2026-05-15-us025-m5-c2-d1-done.md` — add Addendum 3 noting Spec Y cycle complete
- [ ] 7.5 NOT touching `prd-aria-v2.md` (per D4)

---

## Phase 8 — Phase C+D bookkeeping (T8)

### T8 — Standard 10-step + R1 fixes carry-forward from Spec X

- [ ] 8.1 Per-task-group commits with Conventional Commits format (Spec X T8.1 examples reused)
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
- [ ] T0 Phase A.2 audit (3-agent proportional R1 expected; convergence likely faster than Spec X since architecture pattern established)
- [ ] T0 Spec Status → Approved
- [ ] T1-T7 Phase B (~19h AI-runnable)
- [ ] T8 Phase C+D

**当前 Phase**: A.1 (Spec drafted, awaiting R1 audit)
