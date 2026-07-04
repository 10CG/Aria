# Aria 2.0 M6 — Layer1→Layer2 Dispatch Input Delivery (C' dual-channel)

> **Level**: 3 (Full — cross-cuts container entrypoint + Layer 1 dispatch + acceptance assertions + boundary contract; new immutable image build; 4 internal task groups)
> **Status**: ✅ **Approved** (owner sign-off 2026-07-03; Phase A.2 post_spec CONVERGED via R3 unanimous PASS; **Phase A.3 agent 分配 LOCKED 2026-07-04** — `detailed-tasks.yaml` 30 tasks [backend-architect 21 / qa-engineer 4 / knowledge-manager 5], 1:1 对 tasks.md 30 项 + verification↔AC 映射; 经 mid_post_spec dogfood 修正; owner 全权归本侧后采用此细粒度版 supersede 早前 20-task; **post_planning R1→R2 CONVERGED 2026-07-04** [6 Major+minors fixed, R2 5/5 PASS; 首个 post_planning gate per DEC-20260704-001]; ready for Phase B.1)
> **Audit trajectory** (convergence mode, 5-agent team, code-grounded against `aria-orchestrator` daf7c79):
>   - R1 (2026-07-03): **5/5 REVISE** — 3 Critical (AD-M0-5 misattribution [2-agent] / fetch-outcome↔state-machine dead-end [qa] / AC-6 fetch-fail indistinguishable [qa]) + 4 Major (ISSUE_URL not fixed [4-agent] / retry classification dropped / META "R7 64KB" factual error / compute-assertions call-site) + 1 Minor. All landed.
>   - R2 (2026-07-03): **4 PASS + 1 REVISE** — backend-architect found 2 fix-introduced Criticals (corpus-exclusion label stranded on cross-node-unreadable `result.json` / B.3-vs-D.1 raw-number contradiction). Both landed (outcome-class stderr-marker → DB persistence → acceptance stratify; seed additive columns).
>   - R3 (2026-07-03): **5/5 unanimous PASS** — both R2 Criticals verified CLOSED against live code; no fix-introduced regressions. Non-blocking findings (fail-closed marker default / base_branch seed-availability wording / single-carrier) folded in. **CONVERGED.**
> **Change ID**: `aria-2.0-m6-dispatch-input-delivery`
> **Parent US**: [US-026](../../../docs/requirements/user-stories/US-026.md) (Aria 2.0 M6 — autonomous E2E closure umbrella)
> **Parent PRD**: [prd-aria-v2.md §M6](../../../docs/requirements/prd-aria-v2.md) (Week 26-30, E2E testing + release)
> **Decision Source**: [DEC-20260702-001](../../../docs/decisions/DEC-20260702-001-layer2-input-delivery-architecture.md) (technical brainstorm → 4-agent post_brainstorm 审议: 1 OBJECTION + 3 CONCERNS 全折入 C')
> **Discovered by**: M6 168h-run pre-flight ([Aria #147](https://forgejo.10cg.pub/10CG/Aria/issues/147) Blocker 3, comments #14260/#14265/#14270) — 数据铁证: 唯一 S9_CLOSE = 字母前缀 manual dispatch; 所有数字-id 自主 dispatch 100% S_FAIL
> **Sibling Spec (not a dependency, but load-bearing sequencing)**: [aria-2.0-m6-e2e-resilience](../aria-2.0-m6-e2e-resilience/proposal.md) — Spec #2's 168h autonomous run (AC-5/AC-6 corpus) is **not valid** until this Spec ships (autonomous dispatch never closed the loop; Spec #2's corpus would be either empty or false-green polluted). This Spec is a **precondition to Spec #2's operational run**, not to its code (Spec #2 code already shipped 2026-06-02).
> **Downstream dependency edge (explicit)**: A **separate** telemetry Spec (container → Layer 1 cost/model reporting via logs marker) is required before the 168h run is scorable for AC-6 cost gate. **This Spec fixes input delivery only** — shipping it does NOT make the 168h run scorable on its own (see §Out of Scope).
> **AD allocation**: **AD-M6-10** reserved for this Spec (next available; AD-M6-1/2/4/5/6/7/9 used, AD-M6-8 Retired, AD-M6-3 skipped). Amends **AD-M1-4** (file-mode 5-AND + fetch-mode outcome). Corrects the **AD4 risk-table cell** (`:384`) that mislabels the bind-mount assumption as "AD-M0-5 约定" (AD-M0-5 body left untouched). Adds **§5** to `layer-boundary-contract.md`.
> **Scope**: `aria-orchestrator` (v2.0 runtime). Spec lands in main-repo `openspec/changes/` per Rule #5 (project change, not shared submodule).
> **Recon provenance**: all §What line-references verified against `aria-orchestrator` HEAD `daf7c79` (2026-07-02); the 4 DEC §待核实 items resolved by code recon (see §Prerequisite Verification).

---

## Why

Aria 2.0 M6's "verified autonomous" claim rests on a sustained 168-hour autonomous dispatch run
(Spec #2 AC-5/AC-6). M6 pre-flight (2026-07-02) proved that **the autonomous dispatch path has never
closed end-to-end**: the only `S9_CLOSE` in the `dispatches` table is a letter-prefixed *manual*
dispatch (`smoke-m4-pr97`); **every numeric-id autonomous dispatch is `S_FAIL`**. Starting the 168h
run against this system would produce zero valid cycles — or worse, false-green cycles that silently
pollute the AC-5/AC-6 corpus.

The root cause is a **two-dimension contract mismatch** between the layers, plus a downstream
false-green hazard:

**1. Cross-node input-delivery gap.** Layer 1's tick runs on `light-1` (local `ext4`); Layer 2's
container runs on the `heavy` node pool (`heavy-1..4`, docker). The container reads task input from
`inputs/<ISSUE_ID>/issue.yaml` on host_volume `aria-runner-inputs`, which is a **per-heavy-node local
volume** (`/opt/aether-volumes/aria-runner/inputs`, verified not NFS). `light-1` has no such directory
— **Layer 1 physically cannot write to a location the container can read**. Compounding this, autonomous
Layer 1 writes `prompt.txt` keyed by `dispatch_id` (`/opt/aria-inputs/<dispatch_id>/prompt.txt`,
`extension.py:2143`), while the container reads `issue.yaml` keyed by `ISSUE_ID` (`initial.sh:145`) —
**both the filename and the key are mismatched**.

**2. ISSUE_ID regex rejects autonomous ids.** The container entrypoint enforces
`^[A-Z][A-Z0-9-]+$` (`initial.sh:106`) **before** input loading. Autonomous dispatch passes the numeric
Forgejo id (`extension.py:1176`) → Step 1 `die` (FATAL) before Step 2 ever runs.

**3. Empty-`expected_changes` false-green (corpus poisoning).** `compute-assertions.sh:94-120`
initializes `FILE_HIT=true`/`DIFF_HIT=true` and only flips them to `false` inside a loop over
`expected_file_touched[]`/`expected_diff_contains[]`. When those lists are **empty**, the loops never
iterate and both stay `true` → the 5-AND SUCCESS gate (`initial.sh:524-536`, AD-M1-4) passes on *any*
commit+PR. Today this is masked because `RENDERING_CONTRACT.md:76` promises `expected_file_touched[]`
is "always non-empty (validator enforces)" — **but that validator runs only in the file/authored path**.
A fetch-based autonomous dispatch derives no `expected_changes` and would therefore mark **every**
dispatch that produces any commit as SUCCESS, silently corrupting the 168h AC-5/AC-6 evidence.

The existing codebase already solved the *output* side of the cross-node problem with a
**node-agnostic channel**: host volumes are unreachable across nodes, so the container echoes markers
to stderr and Layer 1 greps them via the Nomad logs API (`alloc_status_provider.py:259`). Dispatch
already carries small parameters via **Nomad META (env)** (AD-M3-1). This Spec applies the same
node-agnostic principle to the *input* side.

## What

**C' dual-channel input delivery** (per DEC-20260702-001, folding in all 4 audit findings):

- Large human-authored content (**title / body**) → container **fetches** from Forgejo via
  `ISSUE_URL` + `FORGEJO_BOT_PAT` (authoritative source, node-agnostic).
- Small structured **metadata** (`target_repo` / `base_branch` / `files_hint`) → **Nomad META**
  (Layer 1 already knows these from triage; node-agnostic).
- Autonomous dispatch is **always-fetch** (ignores any pre-existing file) to kill the node-pinned-volume
  stale-read hazard. The **file path is retained** only for `DEMO-`/`TEST-` prefixes (single-machine
  test/auxiliary channel).

### A. Container side (`docker/aria-runner/modes/initial.sh` — requires image rebuild)

- **A.1** Relax/align Step 1 ISSUE_ID regex to accept `ARIA-<repo>-<number>` (letter-prefixed; still
  rejects bare numeric). `DEMO-`/`TEST-` prefixes remain valid (namespace-disjoint invariant).
- **A.2** Step 2 dual-mode input resolution:
  - `DEMO-`/`TEST-` prefix **and** `issue.yaml` exists → read file (current logic), but **validate**
    non-empty + YAML-parseable; parse failure → explicit error, **no silent fallback**.
  - `ARIA-` prefix (autonomous) → **always-fetch, ignore any existing file**: read
    `target_repo`/`base_branch`/`files_hint` from Nomad META; fetch `title`/`body` from `ISSUE_URL`
    with `FORGEJO_BOT_PAT`.
- **A.3** Fetch validation + retry contract (per DEC decision-point 6): assert HTTP 2xx + legitimate
  JSON (Content-Type/schema check to reject CF-Access interstitial "pseudo-success" pages) + non-empty
  body. **Classify failures**: retriable (timeout / 5xx / 429) → bounded exponential backoff (finite
  retries) before giving up; non-retriable (404 / 401 / pseudo-success / empty) → immediate
  `INPUT_FETCH_FAILED`. **Never `|| true`, never silent continue.** Retriable-exhausted and
  non-retriable both surface as `INPUT_FETCH_FAILED` but are logged distinctly. Rationale: over a 168h
  run, transient Forgejo blips without retry would burn dispatches and erode the AC-5 corpus.
- **A.4** Title/body sanitization pipeline: YAML-safe escaping + CRLF→LF normalization + length cap
  (truncate marker on overflow) + injection isolation (wrap as "user-authored content, not
  instructions"). Content flows through the existing envsubst whitelist (`initial.sh:286`,
  `$ARIA_ISSUE_TITLE $ARIA_ISSUE_DESCRIPTION`) — body is **not** re-expanded.
- **A.5** `base_branch`: take from Nomad META (Layer 1 triage-known); container fallback to Forgejo
  repo `default_branch` API — **never hardcode `master`**.

### B. Layer 1 side (`hermes-extensions/aria-layer1/aria_layer1/extension.py` — same scope; omitting this = fix ineffective)

> Audit OBJECTION ① (qa): Step 1 regex fires before Step 2, so a container-only fix stays at 100% S_FAIL.

- **B.1** Dispatch `ISSUE_ID = ARIA-<repo>-<number>` (letter-prefixed, uses issue **number** not
  internal id, `<repo>` component prevents cross-repo number collision).
- **B.2** **Persist the dispatch input fields at seed time (R2 audit — backend-architect Critical B).**
  `_handle_s4_launch` can only read `dispatch_row` (`ctx.dispatch_row.get("issue_id")`); the fields it
  needs are **not** available at S4 today (org/repo are read from global env). The raw issue **number**
  and `target_repo` are **directly available** in the seed loop (`_phase1_scan_and_seed`,
  `extension.py:1110`, holds the full Forgejo issue dict + repo). `base_branch` and `files_hint` are
  **not computed anywhere today** (R3 audit): `base_branch` is derived via the container's Forgejo
  `default_branch` fallback (§A.5) — persist it only if Layer 1 computes it, else leave NULL and let the
  container resolve; `files_hint` is **optional** prompt context (nullable, unused by the skipped
  fetch-mode assertion path). Add these as **additive nullable columns** on `dispatches` following the established
  `migrations/00N_schema_vN_additive.sql` pattern (M3 v2 / M4 v3 / M5 all added forensic columns this
  way — this is the codebase's standard additive migration, **not** a key restructure; see D.1). Seed
  writes them; `_handle_s4_launch` reads them. This resolves the B.3-vs-D.1 tension (no composite parsing,
  no key change) and supplies the META/URL builders below.
- **B.3** Extend the Nomad META builder (`_handle_s4_launch` / `build_nomad_meta`) with the persisted
  `target_repo` / `base_branch` / `files_hint` (each tiny — well within the 100 KB/field META cap).
- **B.4** **Fix `ISSUE_URL` construction (R1 audit — 4-agent Major).** Current state
  (`extension.py:2149-2152`) interpolates `issue_id` directly, and `issue_id` (`extension.py:1176`) is
  `str(issue.get("id") or issue.get("number"))` — Forgejo issues always carry a truthy `id`, so today's
  URL uses the **internal cross-repo id, not the per-repo number** (early Aria issues where `id==number`
  masked this). Org/repo are also hardcoded from `FORGEJO_ORG`/`FORGEJO_REPO` env
  (`extension.py:2147-2148`), not `target_repo`. After B.1/D.1 make `issue_id` the composite
  `ARIA-<repo>-<number>`, direct interpolation yields an invalid path (`/issues/ARIA-Aria-147` → 404,
  breaking the fetch that is this Spec's centerpiece). **Fix**: build `ISSUE_URL =
  {forgejo_base}/{target_repo}/issues/{raw_number}` from the **persisted** `raw_issue_number` +
  `target_repo` columns (B.2) — no composite parsing, no hardcoded env. Per DEC decision-point 5.
- **B.5** Unify the `head_branch` formula: `aria/{issue_id}` (`extension.py:2989`) must match the
  container's `BRANCH="aria/${ISSUE_ID}"` under the new `ARIA-<repo>-<number>` scheme (else S6_REVIEW
  PR binding breaks).
- **B.6** **Consume the container outcome-class marker (R1 qa Critical + R2 backend-architect Critical A
  — makes AC-6 implementable AND the AUTONOMOUS_COMPLETED label load-bearing).** `_handle_s5_await`
  (`extension.py:2593-2640`) today reads **only** the Nomad alloc `exit_code`: `==0 → S6_REVIEW`, else
  `S_FAIL(CONTAINER_CRASH)` (closed enum, `interfaces.py:67-86`); it **never reads `result.json`** (which
  is on the cross-node-unreadable host volume this Spec's §Why cites, and has "no downstream consumer",
  `extension.py:2596-2599`). So the container's outcome **class** must cross to Layer 1 via the
  **stderr-marker channel Layer 1 actually reads** (`get_alloc_logs()`, `alloc_status_provider.py:251`,
  the same channel `redo.sh` markers use), **not** `result.json`:
  - On `exit_code != 0`: read the marker; add `FailReason.INPUT_FETCH_FAILED` and route it distinctly
    from `CONTAINER_CRASH` (infra-fail vs agent/exec-fail → AC-6).
  - On `exit_code == 0`: read the marker to distinguish `AUTONOMOUS_COMPLETED` (assertion-unverified)
    from a file-mode 5-AND `SUCCESS`, and **persist the outcome class into the DB** — either an additive
    `outcome_class` column (B.2 migration) or `dispatch_audit_log` payload (reusing the #147 B4
    `issue_type_hint` `json_extract` pattern, `db.py:622`). Both advance to S6_REVIEW→S9; the persisted
    class is what lets acceptance stratify (§C.3). This is the mechanism that makes the label
    load-bearing — a flag written only to `result.json` (as R1 had it) would be written to a file no one
    reads. **Fail-closed default (R3 qa Important):** if the marker is **absent or malformed** on
    `exit_code == 0`, do **not** default to a verified `SUCCESS` — record a distinct
    `outcome_class=UNKNOWN` (excluded from verified-SUCCESS metrics, same as `AUTONOMOUS_COMPLETED`), so a
    missing marker cannot reopen ② in a third form. Fixture test covers marker-absent + malformed.
  - **Detailed-tasks note (R3 tech-lead M-1):** A.2 should pick **one** carrier (`outcome_class` column
    *or* audit payload), not both, to avoid an implementation fork — both satisfy "DB-persisted,
    queryable, not `result.json`"; the column is simpler to stratify in the acceptance SQL.

### C. Acceptance outcome — three-outcome model (`initial.sh` + `compute-assertions.sh` — false-green fix, RED-first)

> Audit OBJECTION ② (qa): empty `expected_changes` →恒真 → corpus poisoning.
> Audit R1 (qa Critical): a *naive* empty-guard collides with the state machine — making empty hits
> non-`true` forces fetch-mode to `ASSERTION_MISMATCH` → `exit 1` → `S_FAIL(container_crash)`
> (`initial.sh:526-596` + `_handle_s5_await:2620-2640`), **reproducing 100% S_FAIL in a new form**.
> The fetch-mode outcome must therefore be a *distinct, explicit* branch, not a byproduct of the 5-AND.

The current pipeline (`compute-assertions.sh:37-39` dies if `issue.yaml` absent; `initial.sh:513`
calls it unconditionally with `$ISSUE_YAML`; `initial.sh:526-535` 5-AND → `SUCCESS` else
`ASSERTION_MISMATCH`; `:591-596` maps `SUCCESS→exit 0`, else `exit 1`) assumes `expected_changes`
always exist. This Spec introduces a **three-outcome model** (amends AD-M1-4, see §How):

- **C.1 (file mode — `DEMO-`/`TEST-`):** keep the AD-M1-4 5-AND `SUCCESS`. Harden it: empty
  `expected_file_touched[]`/`expected_diff_contains[]` must **not** default to `true` — emit
  `unknown`/`skip`, never a passing hit. **RED test first** reproducing the current false-green
  (`compute-assertions.sh:94-120`, both `HIT` init `true`, loops skip on empty → any commit reads
  SUCCESS). In file mode the upstream validator enforces non-empty, so this is a defense-in-depth guard.
- **C.2 (fetch mode — `ARIA-`):** fetch dispatches carry **no** `expected_changes` and never write
  `issue.yaml`, so the `compute-assertions.sh` call must be **skipped** (not fed a stub) — the RED test
  must exercise the **real `initial.sh` call-site** in fetch mode, not just the script in isolation
  (else it masks that the call-site can't reach the fix). Define a distinct terminal outcome
  **`AUTONOMOUS_COMPLETED`** = `claude_exit==0 AND commit AND PR` (the **three** verifiable conditions;
  **no** file/diff hits, since there is nothing to assert against). Map `AUTONOMOUS_COMPLETED → exit 0`
  so the dispatch advances to S6_REVIEW→S9 (resolves the C2 dead-end).
- **C.3 (honest labelling — resolves ② without re-breaking; R2 backend-architect Critical A).**
  `AUTONOMOUS_COMPLETED` must be distinguishable from a verified `SUCCESS` **in the channel acceptance
  actually queries**, not merely in `result.json`. Both reach `S9_CLOSE`, and the sibling Spec #2
  acceptance gate counts `total_s9 = COUNT(*) WHERE state='S9_CLOSE'` (`check-m6-e2e-acceptance.py`) — on
  `state` alone the two are **indistinguishable**, so a `result.json` flag (which Layer 1 never reads)
  would let ② reappear at the acceptance-query layer. Therefore: the container reports the outcome class
  via the stderr marker (§B.6); Layer 1 **persists it in the DB** (additive `outcome_class` column or
  `dispatch_audit_log` payload, #147 B4 pattern); and **Spec #2's acceptance queries are made
  outcome-class-aware** — `AUTONOMOUS_COMPLETED` rows are excluded from any "verified-SUCCESS" corpus
  metric and stratified separately (cross-Spec coordination item, see §Out of Scope + AC-4). The entry is
  honestly marked not-diff-verified rather than silently masquerading as a verified SUCCESS. (AC-5 scores
  humanized-command quality by owner, not assertions, so an unverified-but-completed dispatch is a valid
  AC-5 corpus member **once labelled** — and S6_REVIEW LLM review + S7 human gate still run before any
  merge, an independent safety net.)
- **C.4 (fetch failure):** if title/body fetch fails (§A.3), emit the stderr marker Layer 1 consumes
  (§B.6) and `exit 1` — routed to `S_FAIL(INPUT_FETCH_FAILED)`, distinct from both completion and crash.

### D. Key format + migration (`schema.sql` / acceptance queries)

- **D.1** `issue_id` becomes `ARIA-<repo>-<number>`. **Recon correction (vs DEC decision-point 8):**
  the schema already stores `issue_id` as a single `TEXT` column with composite PK `(issue_id,
  dispatch_id)` + partial-unique index `uq_issue_active_partial` on `issue_id`. The "(repo, number)
  composite" is achieved by **embedding repo+number into the `issue_id` string value** — the **key
  itself is not restructured** (no PK/index change); the partial-unique-active-dispatch invariant
  continues to hold on the string. **Clarification (R2 audit):** "no key restructure" does **not**
  forbid the *additive input columns* of B.2 (`raw_issue_number` / `target_repo` / `base_branch` /
  `files_hint` / optional `outcome_class`) — those follow the codebase's established
  `migrations/00N_schema_vN_additive.sql` pattern (M3 v2 / M4 v3 / M5 precedent) and are how the raw
  number + repo reach `_handle_s4_launch` without parsing the composite.
- **D.2** Migration = **value reformat**, not schema change. Survey every acceptance query that
  **filters/groups by `issue_id`** and confirm it tolerates the new format. **Recon correction (vs DEC
  decision-point 8):** AC-2 issue_type stratification reads `json_extract('$.issue_type_hint')` from
  `dispatch_audit_log.payload_json` — it is **not** a SQL join on `dispatches.issue_id`, so it is more
  robust than the DEC feared; but audit-log and dispatches rows still carry the reformatted `issue_id`
  value, so any query keying on it must be surveyed (#147 join-impact).

### E. Image build + freeze

- **E.1** Rebuild `aria-runner` via `aether-build-container` after A/C land; push to internal registry;
  capture the immutable `image_sha256`.
- **E.2** **Freeze a single `IMAGE_SHA` for the entire 168h run** — a mid-run hotfix would confound the
  AC-5/AC-6 corpus.

### F. Contract + doc sync (Rule #3 — delivery items, not optional)

- **F.1** Add **AD-M6-10** (six-section format) documenting the C' dual-channel decision + the
  single-node scope of the bind-mount input assumption.
- **F.2** **Correct the AD4 risk-table cell** at `architecture-decisions.md:384` (R1 audit — the
  bind-mount assumption is **not** an AD-M0-5 decision; that cell mislabels it). Fix the mislabel +
  scope the "prompt → bind mount, meta → small params" premise to **single-node** + cross-reference
  AD-M6-10. **Leave the AD-M0-5 body (`:1035`, m0-handoff schema) untouched** — amending it would
  corrupt an unrelated decision.
- **F.5** **Amend AD-M1-4** (5-AND SUCCESS) — scope it to file mode; document the `AUTONOMOUS_COMPLETED`
  fetch-mode outcome (`assertion_verified:false`) + `INPUT_FETCH_FAILED`.
- **F.3** Add **layer-boundary-contract.md §5 "Task Content Delivery Mechanism"** — field-level schema
  table for both channels (file vs fetch) + file-mode lifecycle declaration (this contract currently
  says *nothing* about how the container obtains full issue content — a pre-existing gap).
- **F.4** Update CLAUDE.md M6 status section to record the input-delivery ↔ telemetry dependency chain
  (high-contention region — fetch before edit per `[[feedback_claude_md_project_status_high_contention]]`).

## How — Architecture Decisions

| AD | Type | Summary |
|----|------|---------|
| **AD-M6-10** | New | C' dual-channel input delivery: title/body via Forgejo fetch; structured metadata via Nomad META; autonomous = always-fetch; file mode retained for `DEMO-`/`TEST-` only. Also states the single-node scope of the bind-mount input assumption (see AD4 correction below). |
| **AD-M1-4** | Amend | Scope the 5-AND `SUCCESS` to file/authored mode; add the distinct `AUTONOMOUS_COMPLETED` (three-condition, `assertion_verified:false`) fetch-mode outcome + `INPUT_FETCH_FAILED` failure. |
| **AD4 risk-table cell** (`architecture-decisions.md:384`) | Correct | **R1 audit — 2-agent Critical/Major.** The "prompt→bind mount, meta→small params" assumption lives **only** in this AD4 risk-table row, which mislabels it "AD-M0-5 约定". `AD-M0-5` (`:1035`) is actually "m0-handoff.yaml schema 12 字段" and is **left untouched**. Correct the mislabel here + scope the bind-mount premise to single-node + cross-reference AD-M6-10. (DEC line 22 carried the same misattribution — corrected here.) |
| `layer-boundary-contract.md §5` | New section | Task content delivery mechanism (dual-channel field schema + file-mode lifecycle) |

## Alternatives Considered

| Option | Description | Verdict |
|--------|-------------|---------|
| **C' dual-channel** | title/body → fetch; metadata → META; always-fetch | ✅ **Selected** |
| C-fetch (original) | all via fetch + derive metadata from URL + file-first dual-mode | ⚠️ Upgraded to C': deriving metadata from URL removes cross-repo decoupling; file-first = stale-read hazard |
| C-meta | full issue content in META env | ❌ Long body risks the per-field META cap (`META_VALUE_CAP_BYTES = 100 KB`, `prompt_render.py:42`; the real ceiling is Linux `MAX_ARG_STRLEN` 128 KiB — R7 in `m0-report.md` §1.2 **debunked** the old "64 KB" myth) + content double-write. (C' metadata fields are tiny, so no cap concern; C-meta rejected on double-write + unbounded-body grounds, not the debunked number.) |
| D shared storage | make `aria-runner-inputs` an NFS/cluster volume | ❌ **Honestly rejected (recon-confirmed):** `host-volume.hcl:26` shows `path=/opt/aether-volumes/aria-runner/inputs`, `read_only`, **local, not NFS**. AD4 mentions heavy nodes mounting `nfs-fastpool-aether`, but the *writer* (`light-1`) is confirmed local `ext4` — Option D would additionally require `light-1` to mount NFS (infra change) + inverts the node-agnostic philosophy + introduces a shared-volume single point |
| E node-pin + push | Layer 1 `scp` to target heavy node + dispatch node constraint | ❌ Most bespoke/fragile (per-dispatch scp + reschedule-to-same-node coupling) |

## Prerequisite Verification (DEC §待核实, resolved by code recon @ `daf7c79`)

| # | DEC prerequisite | Verification result |
|---|-----------------|---------------------|
| 1 | heavy `/opt/aria-inputs` mount type (NFS?) → honestly reject D | **Local, not NFS** (`nomad/client-config/host-volume.hcl:26-29`). D correctly rejected. |
| 2 | envsubst whitelist + body handling (byte-level) | **5 vars** `$ARIA_ISSUE_ID $ARIA_ISSUE_TITLE $ARIA_ISSUE_DESCRIPTION $ARIA_FILES_LISTING $ARIA_EXPECTED_CHANGES` (`initial.sh:286`); body via `$ARIA_ISSUE_DESCRIPTION`, no double-expansion. Container has **no** issue-content fetch code today (PAT used only for clone `:251` + PR API `:396`). |
| 3 | `RENDERING_CONTRACT` expected_changes structure + compute-assertions empty behavior (RED-repro) | `expected_file_touched[]` (non-empty by file-mode validator) + `expected_diff_contains[]` (`RENDERING_CONTRACT.md:61-78`). **False-green confirmed** at `compute-assertions.sh:94-120`; guard is upstream-validator-only (file mode) → fetch mode unguarded → concern valid. |
| 4 | DB key migration impact on #147 AC-2 join | `issue_id TEXT`, PK `(issue_id, dispatch_id)`, partial-unique on `issue_id` (`schema.sql:61,245,273`). AC-2 reads `json_extract('$.issue_type_hint')` from audit payload (`db.py:622`), **not** an `issue_id` join → narrower impact; still survey issue_id-keyed queries. |

**Additional code facts verified during R1 audit** (drove the §What B.5 / §What C rework): the state
machine maps `FINAL_OUTCOME==SUCCESS→exit 0`, else `exit 1` (`initial.sh:591-596`);
`_handle_s5_await` (`extension.py:2620-2640`) reads **only** the Nomad `exit_code` and routes any
non-zero to `S_FAIL(CONTAINER_CRASH)` — `FailReason` is a closed enum with no fetch/input value
(`interfaces.py:67-86`); `compute-assertions.sh:37-39` dies if `issue.yaml` is absent; the per-field
META cap is `META_VALUE_CAP_BYTES = 100 KB` (`prompt_render.py:42`), and R7 (`m0-report.md §1.2`)
**debunked** the "64 KB" figure (real ceiling `MAX_ARG_STRLEN` 128 KiB).

## Impact

| Type | Description |
|------|-------------|
| **Positive** | Autonomous numeric-id dispatch closes S0→S9 for the first time; 168h run becomes runnable; corpus false-green eliminated |
| **Positive** | Node-agnostic input channel — no per-node volume placement, no scp, no shared-storage single point |
| **Risk** | Fetch adds a new container outbound dependency on heavy-node Forgejo egress/auth — **must be live-tested pre-run** (mitigation: §Risks) |
| **Risk** | Image rebuild + id-format migration touch acceptance queries — surveyed per D.2; frozen IMAGE_SHA per E.2 |
| **Backward-compat** | Rule #4: file mode (`DEMO-`/`TEST-`) preserved as auxiliary channel. This is **not** "preserve shipped behavior" — autonomous never worked; it is preservation of the single-machine test path. |

## Constraints

- **Framework Constraints**: N/A (aria-orchestrator is a Python/bash runtime, not a web framework project).
- **Rule #3** doc sync (AD-M6-10 + AD4-cell correction + AD-M1-4 amend + §5 + CLAUDE.md) are delivery items.
- **Rule #5**: Spec in main-repo `openspec/changes/` (not `standards/`).
- **Rule #4**: `DEMO-`/`TEST-` file mode retained; namespace-disjoint from `ARIA-`.
- ISSUE_ID must be letter-prefixed (container regex is in the deployed M5 image, byte-confirmed).
- Forgejo issue **number** is per-repo unique, not global → `<repo>` component required in id.

## Acceptance Criteria

- [ ] **AC-1** Autonomous dispatch of a real numeric Forgejo issue reaches **S9_CLOSE with a merged PR**
      (E2E dogfood, not unit-only) — the single most important gate.
- [ ] **AC-2** Container Step 1 accepts `ARIA-<repo>-<number>` and still rejects bare numeric (regression test).
- [ ] **AC-3** Fetch path: title/body retrieved from `ISSUE_URL`; **failure classification tested** —
      retriable (timeout/5xx/429) retries with bounded backoff then gives up; non-retriable
      (404/401/CF-Access pseudo-success/empty JSON) → immediate `INPUT_FETCH_FAILED`; **no silent continue**.
- [ ] **AC-4** Three-outcome model verified: (a) **RED test at the real `initial.sh` call-site** proves
      the pre-fix empty-`expected_changes` false-green, then passes — file mode empty → `unknown`/`skip`,
      never SUCCESS; (b) fetch mode reaches `AUTONOMOUS_COMPLETED`→`exit 0`→S6_REVIEW→S9 (does **not**
      dead-end at `ASSERTION_MISMATCH`/S_FAIL); (c) the `AUTONOMOUS_COMPLETED` outcome class crosses to
      Layer 1 via the stderr marker (§B.6), is **persisted in the DB** (additive `outcome_class` column or
      audit payload — **not** `result.json`, which Layer 1 never reads), and Spec #2's acceptance queries
      are **outcome-class-aware** so it is excluded from any verified-SUCCESS corpus metric (query on
      `state='S9_CLOSE'` alone must not conflate it with verified `SUCCESS`); (d) **fail-closed** —
      marker absent/malformed on `exit 0` → `outcome_class=UNKNOWN` (not `SUCCESS`), fixture-tested.
- [ ] **AC-5** Layer 1 emits `ARIA-<repo>-<number>` + `target_repo`/`base_branch`/`files_hint` META (read
      from the persisted seed columns, B.2) + matching `head_branch`; S6_REVIEW PR binding intact.
- [ ] **AC-6** Fetch failure distinguishable to Layer 1: container emits stderr marker → `get_alloc_logs`
      → `_handle_s5_await` routes `FailReason.INPUT_FETCH_FAILED` (infra-fail) **distinct from**
      `CONTAINER_CRASH` (agent/exec-fail); fixture test covers both branches so infra failures do not
      pollute AC-5 corpus attribution.
- [ ] **AC-7** Title/body sanitization: YAML-safe + CRLF→LF + length cap + injection isolation;
      body not re-expanded by envsubst (whitelist-verified).
- [ ] **AC-8** `issue_id` value reformat surveyed: every acceptance query keying on `issue_id`
      tolerates the new format; #147 issue_type_hint stratification unaffected (json_extract path).
- [ ] **AC-9** Single frozen `IMAGE_SHA` recorded for the 168h run; rollback path (old sha) documented.
- [ ] **AC-10** Doc sync complete: AD-M6-10 written (C' + single-node bind-mount scope), **AD4
      risk-table cell (`:384`) corrected** (mislabel fixed, AD-M0-5 body untouched), **AD-M1-4 amended**
      (file-mode 5-AND + `AUTONOMOUS_COMPLETED` + `INPUT_FETCH_FAILED`), layer-boundary-contract §5
      added, CLAUDE.md M6 dependency chain updated.
- [ ] **AC-11** `ISSUE_URL` built from `{target_repo}/issues/{raw_number}` using the **persisted**
      `raw_issue_number` + `target_repo` columns (B.2 — not parsed from the composite `issue_id`, not from
      hardcoded env); verified on an issue where `id != number` (proves the fix isn't masked by early
      `id==number` cases). Cross-repo (non-Aria `target_repo`) is verified structurally by unit test; a
      live cross-repo dispatch is **deferred** if the 168h seed pipeline runs single-repo (honestly
      scoped — `_phase1_scan_and_seed` reads one `FORGEJO_REPO` today).
- [ ] **AC-12** Seed persists `raw_issue_number` / `target_repo` / `base_branch` / `files_hint` (+ optional
      `outcome_class`) as additive nullable columns (established `migrations/00N_additive.sql` pattern);
      `_handle_s4_launch` reads them from `dispatch_row`; historical rows (NULL) degrade gracefully.

## Cross-Spec coordination (in scope — delivered here, touches Spec #2's file)

The outcome-class-aware acceptance query (§C.3, AC-4) edits Spec #2's `check-m6-e2e-acceptance.py` — the
`total_s9 = COUNT(*) WHERE state='S9_CLOSE'` gate must be taught to stratify `AUTONOMOUS_COMPLETED` out of
verified-SUCCESS counts. This edit is **delivered by this Spec** (it is the mechanism that makes the label
load-bearing), coordinated with Spec #2 which is not yet archived. Without it, R2 Critical A recurs at the
acceptance layer.

## Out of Scope

- **Telemetry Spec (separate, explicit dependency edge):** how the container reports `cost`/`model`
  back to Layer 1 via logs markers (needed for AC-6 cost gate of Spec #2). Input (this Spec) and output
  (telemetry) are disjoint, per the sub-PR splitting philosophy. **Shipping this Spec alone does NOT
  make the 168h run scorable** — the run's AC-5/AC-6 scoring still depends on the telemetry Spec.
- **Blocker 4 (Luxeno/GLM backend latency):** owner/infra/SilkNode side (#147 / SilkNode #830). Not code.
- **manual dispatch tool-chain repair** (checklist Menu A): owner chose the autonomous path (Menu B).

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| fetch hits CF-Access pseudo-success page (silent empty) | Live-test heavy-node Forgejo egress/auth **before the run** + post-fetch legitimate-JSON validation (Content-Type/schema) + ISSUE_URL constrained to internal-reachable host |
| false-green pollutes corpus (②) | compute-assertions empty-expected禁恒真 + fetch independent outcome + RED-repro first |
| fix ineffective (①) | Layer 1 changes in same scope + E2E dogfood to real numeric-id S9/merged-PR (not unit-only) |
| cross-repo number collision | `<repo>` component in id + volume path |
| body injection / overflow / CRLF | sanitization pipeline (A.4) |
| 168h corpus confound | freeze IMAGE_SHA (E.2) |

## Rollback

Immutable IMAGE_SHA: old image sha retained; point dispatch META back to old sha to roll back the
container side. Layer 1 changes are `git revert`. File mode (`DEMO-`/`TEST-`) is unaffected — the
single-machine test path always works.

## References

- Decision: [DEC-20260702-001](../../../docs/decisions/DEC-20260702-001-layer2-input-delivery-architecture.md)
- Blocker chain: [Aria #147](https://forgejo.10cg.pub/10CG/Aria/issues/147) (comments #14260/#14265/#14270)
- Handoff: [2026-07-02-m6-preflight-luxeno-blocker.md](../../../docs/handoff/2026-07-02-m6-preflight-luxeno-blocker.md)
- Sibling: [aria-2.0-m6-e2e-resilience](../aria-2.0-m6-e2e-resilience/proposal.md)
- Disambiguation: AD-M6-5 is pre-flight fixture provenance (test-side) — a *different* decision from this Spec.
