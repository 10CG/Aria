# M6 Dispatch Input Delivery — Tasks (C' dual-channel)

> **Spec**: [proposal.md](./proposal.md)
> **Level**: 3 (Full)
> **Status**: ✅ Approved (owner sign-off 2026-07-03; Phase A.2 post_spec CONVERGED). Task granularity is functional; A.2 task-planner adds detailed-tasks.yaml with paths/estimates, A.3 assigns agents.
> **Decision Source**: [DEC-20260702-001](../../../docs/decisions/DEC-20260702-001-layer2-input-delivery-architecture.md)
> **Ordering rationale (DEC §落地)**: container code + assertion fix (RED-first) → Layer 1 code (same scope, else ineffective) → key migration → image build/freeze → contract-doc sync → E2E dogfood. Layer 1 (TG-2) and container (TG-1) must ship together; assertion fix (TG-1.C) is RED-first before container fetch is exercised.

---

## Task Group Overview

| Group | Topic | Scope ref |
|-------|-------|-----------|
| TG-1 | Container side: regex + dual-mode input + fetch + sanitization + three-outcome model | §What A + §What C |
| TG-2 | Layer 1 side: additive seed columns + id format + META + ISSUE_URL rebuild + head_branch + outcome-class/INPUT_FETCH_FAILED consumption + acceptance stratify | §What B + §What C.3 |
| TG-3 | Key format value migration + acceptance-query survey | §What D |
| TG-4 | Image rebuild + freeze | §What E |
| TG-5 | Contract + doc sync (AD-M6-10 / AD4-cell correction / AD-M1-4 amend / §5 / CLAUDE.md) | §What F |
| TG-6 | E2E dogfood + pre-run egress live-test | §Acceptance AC-1/AC-3/AC-6 |

> TG-1 and TG-2 are **co-dependent** (regex fires before input load — a container-only ship stays 100% S_FAIL). They land in one integrated change; TG-3/TG-5 can proceed in parallel; **TG-4 (image build) gates on TG-1 only** (only container-side code is baked in; TG-2/TG-3 deploy to Hermes/light-1 separately); TG-6 E2E dogfood gates on TG-1+TG-2+TG-3+TG-4 all deployed.

---

## TG-1 — Container side (initial.sh + compute-assertions.sh)

- [ ] 1.1 Align Step 1 ISSUE_ID regex to accept `ARIA-<repo>-<number>` (still reject bare numeric; `DEMO-`/`TEST-` preserved)
- [ ] 1.2 Step 2 dual-mode resolution: `DEMO-`/`TEST-` + file-exists → validated file read (non-empty + YAML-parseable, no silent fallback); `ARIA-` → always-fetch (ignore existing file)
- [ ] 1.3 Fetch title/body from `ISSUE_URL` with `FORGEJO_BOT_PAT`; read `target_repo`/`base_branch`/`files_hint` from Nomad META
- [ ] 1.4 Fetch validation + retry classification: HTTP 2xx + legitimate JSON (reject CF-Access pseudo-success) + non-empty; retriable (timeout/5xx/429) → bounded backoff; non-retriable (404/401/pseudo-success/empty) → immediate fail (no `|| true`)
- [ ] 1.5 Title/body sanitization pipeline: YAML-safe escape + CRLF→LF + length cap + injection isolation; route through existing envsubst whitelist (body not re-expanded)
- [ ] 1.6 `base_branch` from META with Forgejo `default_branch` fallback (never hardcode `master`)
- [ ] 1.7 **RED-first** at the real `initial.sh` call-site: reproduce current empty-`expected_changes` false-green; fix compute-assertions to emit `unknown`/`skip` (not `true`) on empty lists (file-mode defense-in-depth)
- [ ] 1.8 Fetch mode **skips** the `compute-assertions.sh` call entirely; wire the skip at `initial.sh:513-515`. (Mechanism, corrected by mid_post_spec dogfood 2026-07-04: the call at `:514` has `| tail -5 || true` under `set -euo pipefail` — compute-assertions.sh's `exit 1` at `:37` is **swallowed**, container does NOT die there; real dead-end is `FILE_TOUCHED_HIT`/`DIFF_CONTAINS_HIT` defaulting `false` at `:517-518` → 5-AND fail → `ASSERTION_MISMATCH` `:534` → `exit 1` `:595` → `S_FAIL`. Skip avoids this dead-end.)
- [ ] 1.9 Define `AUTONOMOUS_COMPLETED` outcome (fetch mode) = `claude_exit==0 AND commit AND PR` (no file/diff hits); map to `exit 0`
- [ ] 1.10 Emit the outcome-**class** stderr marker on the channel Layer 1 reads (cf. `redo.sh` precedent, consumed via `get_alloc_logs`): on success distinguish `AUTONOMOUS_COMPLETED` vs file-mode `SUCCESS`; on fetch failure emit `INPUT_FETCH_FAILED` + `exit 1`. (Do **not** rely on `result.json` — Layer 1 never reads it and it is on cross-node-unreadable storage.)

## TG-2 — Layer 1 side (extension.py + schema migration)

- [ ] 2.1 Add additive nullable columns (`migrations/00N_schema_vN_additive.sql` pattern, M3/M4/M5 precedent): `raw_issue_number` / `target_repo` / `base_branch` / `files_hint` (+ optional `outcome_class`); seed (`_phase1_scan_and_seed`) writes them
- [ ] 2.2 Dispatch `ISSUE_ID = ARIA-<repo>-<number>` (letter-prefixed, issue number not internal id, repo component anti-collision)
- [ ] 2.3 Extend Nomad META builder with `target_repo` / `base_branch` / `files_hint` read from the persisted columns (2.1) via `dispatch_row` — not global env
- [ ] 2.4 **Rebuild `ISSUE_URL`** = `{target_repo}/issues/{raw_issue_number}` from the persisted columns (do NOT parse the composite `issue_id`, do NOT use hardcoded `FORGEJO_ORG`/`FORGEJO_REPO`); fixes the current internal-id + hardcoded-repo construction (`extension.py:1176/2147-2152`)
- [ ] 2.5 Unify `head_branch = aria/{issue_id}` with container `BRANCH` under new scheme (preserve S6_REVIEW PR binding)
- [ ] 2.6 Add `FailReason.INPUT_FETCH_FAILED` (`interfaces.py`); in `_handle_s5_await` (`extension.py:2593-2640`) consume the container outcome-class marker via `get_alloc_logs()`: `exit_code!=0` → route `INPUT_FETCH_FAILED` distinct from `CONTAINER_CRASH`; `exit_code==0` → record `outcome_class` (`AUTONOMOUS_COMPLETED` vs `SUCCESS`) into DB (**single carrier** — additive column preferred over audit payload). **Fail-closed**: marker absent/malformed on `exit 0` → `outcome_class=UNKNOWN` (not `SUCCESS`); fixture covers absent + malformed
- [ ] 2.7 Make Spec #2's acceptance query (`check-m6-e2e-acceptance.py`) outcome-class-aware: `AUTONOMOUS_COMPLETED` excluded from verified-SUCCESS counts / stratified (cross-Spec coordination)

## TG-3 — Key format migration + query survey

- [ ] 3.1 Reformat `issue_id` **value** to `ARIA-<repo>-<number>` (value-level; the **key** is not restructured — composite embedded in TEXT, partial-unique-active invariant preserved). Distinct from the additive input columns of TG-2.1 (those are separate additive migrations, not a key change).
- [ ] 3.2 Decide + document clean-DB vs historical-migration for existing `issue_id` rows
- [ ] 3.3 Survey every acceptance/dispatch query keying on `issue_id`; confirm new-format tolerance; verify #147 issue_type_hint stratification (json_extract path) unaffected

## TG-4 — Image rebuild + freeze

- [ ] 4.1 Rebuild `aria-runner` via `aether-build-container` after **TG-1** lands (only container-side code is baked into the image; TG-2/TG-3 are Hermes/light-1 side, deployed separately); push to internal registry
- [ ] 4.2 Capture immutable `image_sha256`; freeze single `IMAGE_SHA` for the 168h run; record rollback (old sha)

## TG-5 — Contract + doc sync (Rule #3)

- [ ] 5.1 Write **AD-M6-10** (six-section: decision/background/alternatives/rationale/risks/rollback); include single-node scope of the bind-mount input assumption
- [ ] 5.2 **Correct the AD4 risk-table cell** (`architecture-decisions.md:384`): fix the "AD-M0-5 约定" mislabel + scope bind-mount premise to single-node + xref AD-M6-10. **Do NOT touch the AD-M0-5 body** (`:1035`, m0-handoff schema — unrelated)
- [ ] 5.3 **Amend AD-M1-4**: scope 5-AND SUCCESS to file mode; document `AUTONOMOUS_COMPLETED` + `INPUT_FETCH_FAILED`. **Caveat (R2 km):** the AD-M1-4 body (`architecture-decisions.md:1360`) has pre-existing doc/code drift (records a 9-enum/6-AND `entrypoint-m1.sh` version vs the current 5-AND `initial.sh:524`) — verify the AD's current literal content before editing to avoid conflating the two generations.
- [ ] 5.4 Add `layer-boundary-contract.md §5 "Task Content Delivery Mechanism"` (dual-channel field schema + file-mode lifecycle)
- [ ] 5.5 Update CLAUDE.md M6 status section: record input-delivery ↔ telemetry dependency chain (fetch-before-edit; high-contention region)

## TG-6 — E2E dogfood + pre-run verification

- [ ] 6.1 Live-test heavy-node Forgejo egress/auth (fetch reachability) before any run
- [ ] 6.2 E2E dogfood: real numeric-id autonomous dispatch → S9_CLOSE with merged PR (AC-1)
- [ ] 6.3 Verify fetch-failure classes distinguishable to Layer 1 as infra-fail vs agent-fail (AC-6)

---

## Notes

- **Not in this Spec** (explicit dependency edge): container → Layer 1 cost/model telemetry (separate Spec; the 168h run is not scorable for AC-6 until that ships).
- **Sequencing**: this Spec is a precondition to Spec #2's *operational* 168h run, not to Spec #2's code (already shipped 2026-06-02).
- **Phase A.3** will assign agents (no new agent expected — existing roster: backend-architect / qa-engineer / knowledge-manager cover container/assertion/contract-doc work).
