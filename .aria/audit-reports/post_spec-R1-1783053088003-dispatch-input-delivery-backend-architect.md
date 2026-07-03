---
checkpoint: post_spec
mode: convergence
round: 1
agent: backend-architect
verdict: REVISE
spec_id: aria-2.0-m6-dispatch-input-delivery
timestamp: 1783053088003
converged: false
---

# post_spec R1 — aria-2.0-m6-dispatch-input-delivery (backend-architect)

## Scope of this review

Verified every file:line assertion in `proposal.md` / `tasks.md` against `aria-orchestrator` HEAD
`daf7c79` with a backend-architect lens (fetch/Forgejo API contract, base_branch derivation,
title/body sanitization pipeline, data model / composite-key migration, Nomad META field
extension + size limits). Confirmed hard-requirement checks (a)-(d) from the audit brief.

## Findings

### [MAJOR][data-model:extension.py][gap] ISSUE_URL construction is not actually fixed — B.2's "already number today" is unverified/false, and the composite issue_id will break the URL post-fix

**Summary**: Proposal §What B.2 says: *"fix `ISSUE_URL` to use issue **number** (already number today at
`extension.py:2149`, but re-verify against new id scheme)"*. Recon shows this claim does not hold:

1. **Today**: `_handle_s4_launch` builds `issue_url` from the `issue_id` variable
   (`ctx.dispatch_row.get("issue_id", "")`, `extension.py:2108`), which is populated at seed time by
   `extension.py:1176`: `issue_id = str(issue.get("id") or issue.get("number") or "")`. Forgejo's
   issue API returns both `id` (a global, cross-repo unique identifier shared with PRs) and `number`
   (the per-repo display index the REST API path actually expects). Because `issue.get("id")` is
   truthy for every real issue, the `or` never falls through to `number` — so **today's `issue_url`
   is built from the internal `id`, not the issue number**, contradicting "already number today."
2. **After B.1/D.1 land**: `issue_id` (the same variable) becomes the composite
   `ARIA-<repo>-<number>` string. `extension.py:2149-2151` still does
   `f"/{forgejo_org}/{forgejo_repo}/issues/{issue_id}"` — i.e. it will literally interpolate
   `ARIA-Aria-147` into the URL path (`.../issues/ARIA-Aria-147`). Forgejo's issue GET endpoint
   requires a bare per-repo integer index; this is not a valid Forgejo issue reference and the fetch
   will 404 (or hit an unrelated resource). This breaks the **single most important AC-1 E2E gate**
   (autonomous dispatch → S9_CLOSE) because the entire C' architecture is built on `ISSUE_URL` being
   the authoritative fetch target for title/body (§What A, A.3).
3. Compounding gap: `extension.py:2147-2148` hardcodes `forgejo_org`/`forgejo_repo` from
   `FORGEJO_ORG`/`FORGEJO_REPO` env vars (defaulting to `"10CG"`/`"Aria"`), not from the new
   `target_repo` field B.2 itself proposes to add. Given decision-point 2's own rationale ("Forgejo
   issue number is per-repo unique, not global → `<repo>` component required"), a real cross-repo
   dispatch would build a `target_repo`-scoped `issue_id` but still fetch against the
   hardcoded single-repo env vars — wrong repo in the URL for any repo other than the default.

**Fix**: The spec's B.2 / TG-2.2 must be made an explicit, unambiguous decision instead of a
"re-verify" hedge: Layer 1 must retain the **raw Forgejo issue number as a value distinct from the
composite `issue_id`** (e.g. carry it alongside `dispatch_row` or re-derive it by parsing the
`ARIA-<repo>-<number>` string with a documented, tested delimiter/format), and build `ISSUE_URL`
from `{target_repo}/issues/{raw_number}` — not from `{issue_id}` and not from the hardcoded
`FORGEJO_ORG`/`FORGEJO_REPO` env vars. This should be added as an explicit AC/task item, not left
implicit inside "verify ISSUE_URL uses issue number under new id scheme" (tasks.md TG-2.2).

---

### [MAJOR][data-model:META-size][factual-error] Alternatives table cites "R7 64KB" as the reason to reject C-meta, but R7 itself documents that 64KB was a debunked myth — real limit is materially larger

**Summary**: Proposal §Alternatives: *"C-meta ... ❌ META size limit (long body overflows R7 64KB)"*.
This directly contradicts the R7 finding it cites. `docs/m0-report.md` §1.2 **R7 — Nomad meta 限制数值修正**
explicitly states: *"原陈述: 'Nomad meta 64KB 限制' [WRONG] ... 实测: 限制来自 Linux kernel
`MAX_ARG_STRLEN` = 131072 (128 KiB) per env string ... 阈值从 64KB 改为 100KB per field"*. The
codebase's own constants confirm the corrected number: `prompt_render.py:41-42`
(`PROMPT_SIZE_CAP_BYTES` / `META_VALUE_CAP_BYTES` = `100 * 1024`) and `extension.py:2033`'s comment
*"Meta payload size guard: assert len(meta) < 100 KB"*. Citing "R7 64KB" inverts what R7 actually
says (R7 is the correction *away* from 64KB, not evidence *for* it).

**Materiality**: this does not change the C' selection outcome — `target_repo`/`base_branch`/
`files_hint` are all tiny strings, comfortably within either 64KB or the real 100KB/field budget.
But it is a verifiable factual error at exactly the numeric constraint the audit brief flagged for
verification (hard requirement (d)), and it risks propagating a debunked number into future
size-budget decisions (e.g. a future engineer reading this Spec could wrongly treat 64KB as the
authoritative ceiling, or conversely distrust a legitimate ~90KB field that is actually within the
real 100KB margin).

**Fix**: Correct the Alternatives-table citation to "R7 100KB/field (128 KiB kernel hard limit)" and
drop the "64KB" figure, or cite it explicitly as "the debunked pre-R7 number, real limit is 100KB."

## Confirmed-accurate assertions (no discrepancy found)

- **(a)** `compute-assertions.sh:94-120` — confirmed: `FILE_HIT=true`/`DIFF_HIT=true` initialized
  unconditionally (lines 96, 113) and only flip inside `while` loops over `$EXPECTED_FILES` /
  `$EXPECTED_PATTERNS`; when those are empty strings the loop body never executes (empty-string
  continue guard at lines 98/115), so both stay `true`. Confirmed the false-green is real and exactly
  as described.
- **(b)** `schema.sql` — confirmed single `issue_id TEXT NOT NULL` column (line 61), composite
  `PRIMARY KEY (issue_id, dispatch_id)` (line 245, exact), and `CREATE UNIQUE INDEX
  uq_issue_active_partial ON dispatches (issue_id) WHERE state NOT IN (...)` (lines 271-273; spec
  cites line 273 which is the `WHERE` clause of the same statement — within-statement citation, not
  a discrepancy). D.1's "value reformat, not structural migration" framing is correct.
- **(c)** `initial.sh:286` — confirmed exact whitelist: `$ARIA_ISSUE_ID $ARIA_ISSUE_TITLE
  $ARIA_ISSUE_DESCRIPTION $ARIA_FILES_LISTING $ARIA_EXPECTED_CHANGES`. Body flows through
  `$ARIA_ISSUE_DESCRIPTION` only, no second `envsubst` pass exists in the file. A.4/A.7's
  "not re-expanded" claim holds against current code.
- **`initial.sh:106`** regex `^[A-Z][A-Z0-9-]+$` — confirmed exact.
- **`initial.sh:145`** `ISSUE_YAML="${ISSUE_INPUT_DIR}/issue.yaml"` — confirmed exact, keyed by
  `ISSUE_ID` not `dispatch_id`, matching the mismatch narrative in §Why.
- **`host-volume.hcl:26-28`** — confirmed `aria-runner-inputs` is `read_only=true`, local path
  `/opt/aether-volumes/aria-runner/inputs`, no NFS declaration in this file — Option D rejection is
  honest.
- **`extension.py:2989`** `head_branch = f"aria/{issue_id}"` — confirmed exact line and value;
  self-consistent with container `BRANCH="aria/${ISSUE_ID}"` (`initial.sh:266`) since both consume
  the same `dispatch_row.issue_id` string end-to-end (once B.1 lands). B.3's unify claim is sound.
- **`alloc_status_provider.py:259-267`** — confirmed the node-agnostic stderr-marker / Nomad-logs-API
  precedent used to justify the C' input-side symmetry argument.
- **`db.py` audit_extra / json_extract path** — confirmed `dispatch_audit_log` stores
  `issue_type_hint` via `audit_extra` (comment at `db.py:623`, spec cites 622 — one-line drift, not
  substantive), and the only `json_extract('$.issue_type_hint')` consumer
  (`acceptance/check-m6-e2e-acceptance.py:254`) has **zero** `issue_id`-keyed queries in that file —
  D.2's "narrower impact than DEC feared" correction is verified true.
- `initial.sh:233-234` today hardcodes `BASE_BRANCH="${BASE_BRANCH:-master}"` — confirmed this is the
  *current* (to-be-fixed) behavior A.5 targets; not a discrepancy, it's the baseline the Spec
  proposes to change.

## Verdict

**REVISE** — 2 Major findings, both squarely in backend-architect's assigned lens (Forgejo API fetch
contract / composite-key-vs-URL interaction, META size-limit citation). Finding 1 is the more urgent:
as written, the spec's own text ("already number today ... re-verify") would let a Phase B
implementer skip the one code change that keeps the fetch mechanism — the architectural centerpiece
of this Spec — from breaking on every real (non-single-issue) autonomous dispatch. Finding 2 is a
lower-materiality citation-accuracy issue but is directly on the exact numeric fact the audit was
asked to verify, and inverts the meaning of its own cited source.

All other file:line assertions in the proposal (checks (a)-(c) plus the additional citations
verified above) held up against `daf7c79` recon.
