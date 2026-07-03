---
checkpoint: post_spec
mode: convergence
round: 1
agent: tech-lead
verdict: REVISE
spec_id: aria-2.0-m6-dispatch-input-delivery
timestamp: 1783053088003
converged: false
---

# post_spec R1 — tech-lead audit: aria-2.0-m6-dispatch-input-delivery

**Scope of my lens**: architecture-decision completeness / cross-system task decomposition
(Layer1 + container + assertion + image) / explicit dependency edges / AD allocation / 11
decision-point coverage / TG co-dependency / altitude-level structural gaps. Every `file:line`
assertion opened against `aria-orchestrator` HEAD `daf7c79`.

**Verdict: REVISE** (1 critical + 2 major). The spec is largely faithful and well-recon'd — the
core C' architecture, cross-node rationale, false-green root cause, TG ordering, and AD-M6-10
allocation are all correct and code-verified. But it inherited one **wrong AD-target** from the
DEC (never re-verified against the AD body) and dropped/under-specified two load-bearing details.

---

## Findings

### F1 [CRITICAL][architecture:docs/architecture-decisions.md] `AD-M0-5` amend targets the WRONG AD — the doc-sync deliverable (F.2/TG-5.2/AC-10) is unexecutable as written

- **type**: issue
- **Evidence**: Spec §What F.2, §How table, tasks TG-5.2, AC-10 all say "**Amend AD-M0-5** —
  scope the 'prompt → bind mount, meta → small params' assumption to single-node." The spec cites
  `architecture-decisions.md:384` as the "old wording" — that citation is correct: line 384 is a
  **risk-table cell** reading `AD-M0-5 约定: prompt 写 bind mount 文件, meta 只传 ISSUE_ID + 小参数`.
  **But the actual AD-M0-5 body (`architecture-decisions.md:1035`) is titled
  `AD-M0-5 — m0-handoff.yaml schema 锁定 12 字段`** and decides an entirely unrelated thing (the
  12-field M0→M1 handoff schema). There is **no formal AD** anywhere that decides "prompt → bind
  mount / meta → small params" (grep of all AD headers confirms: the phrase exists only in the
  line-384 risk cell, which mis-labels it "AD-M0-5 约定"). AD-M1-10 is prompt *template engine*
  selection, not delivery mechanism.
- **Why critical**: As written, an implementer executing TG-5.2 "amend AD-M0-5 to scope
  single-node bind-mount" would either (a) edit the m0-handoff-schema AD-M0-5 with unrelated
  single-node/bind-mount language → **corrupts an unrelated decision record**, or (b) find no
  amendable anchor text inside AD-M0-5 and produce a malformed deliverable. Either way AC-10
  ("AD-M0-5 amended") cannot be satisfied honestly. The spec's own "Recon provenance" header
  claims "all §What line-references verified" — this attribution was **not** verified (only the
  line-384 citation was, not the AD body it points to). This is exactly the altitude-miss the
  hard-recon requirement targets.
- **Fix**: Retarget the amend. The bind-mount "prompt→file, meta→small-params" convention is not a
  formal AD — it is an informal mitigation note in the AD4 risk table (line 384) that
  mis-references AD-M0-5. Correct F.2 / §How table / TG-5.2 / AC-10 to: (1) **fix/annotate the
  line-384 risk-table cell** to scope the "bind-mount reachable by both sides" assumption to
  single-node and cross-reference the new AD-M6-10; (2) **do NOT edit the AD-M0-5 body**
  (m0-handoff schema — untouched); (3) if formal scoping is desired, put the single-node caveat in
  the new **AD-M6-10** and have line 384 point to it. Propagate the wording correction through the
  DEC-derived language everywhere it says "amend AD-M0-5". (Note: the DEC-20260702-001 itself
  carries the same misattribution at line 22 — flag for the decision record too, but the spec is
  the deliverable that must be corrected.)

### F2 [MAJOR][implementation:extension.py] `ISSUE_URL` recon claim "already number today" is FALSE; also built from hardcoded org/repo, not `target_repo`

- **type**: issue
- **Evidence**: Spec B.2 says "fix `ISSUE_URL` to use issue **number** (already number today at
  `extension.py:2149`, but re-verify against new id scheme)". Real code
  (`extension.py:2150-2153`): `issue_url = f"{base}/{forgejo_org}/{forgejo_repo}/issues/{issue_id}"`
  where `issue_id = ctx.dispatch_row.get("issue_id")` (line 2109) and the DB `issue_id` is seeded in
  the S0 loop as `str(issue.get("id") or issue.get("number") or "")` (`extension.py:1176`) —
  **internal id first, NOT number**. So today the URL resolves to `/issues/{internal_global_id}`,
  which is the wrong Forgejo path (issue URLs are keyed by per-repo **number**). The parenthetical
  "already number today" is factually wrong and *understates the fix*.
- **Second gap**: `forgejo_org`/`forgejo_repo` come from env `FORGEJO_ORG`/`FORGEJO_REPO` (defaults
  `10CG`/`Aria`) — they are **not** derived from the new `target_repo` metadata field. The entire C'
  design introduces `target_repo` for cross-repo decoupling, but the URL the container fetches would
  still point at the hardcoded single repo. For the 168h run (single-repo `10CG/Aria` aria-auto
  issues) reachability is limited, but it silently breaks the cross-repo promise the id scheme
  (`ARIA-<repo>-<number>`) exists to support.
- **Fix**: Correct B.2 / D.2 / TG-2.2 premise: ISSUE_URL today uses the **internal id, not the
  number** — under the new `ARIA-<repo>-<number>` scheme the URL must be built from the **bare
  extracted number** (decoupled from `issue_id`, since `issue_id` will now be the composite string),
  and `org/repo` must be **derived from `target_repo`** (or the issue's actual repo), not the
  hardcoded `FORGEJO_ORG/FORGEJO_REPO` env, for the fetch to hit the correct repo. Add an AC/task
  line asserting URL org/repo consistency with `target_repo`.

### F3 [MAJOR][architecture:proposal §What A.3 / AC-3 / AC-6] DEC decision-point 6 retry/backoff classification is dropped — transient fetch failures burn dispatches

- **type**: issue
- **Evidence**: DEC decision-point 6 requires "fetch 失败契约: **可重试 (超时/5xx/429, 有限退避)** vs
  **不可重试 (404/401)** 分类; 显式检 HTTP status; 不 `|| true`; 失败对 Layer 1 可区分". The spec
  captures three of these (explicit HTTP-status check → A.3; no `|| true` → A.3/AC-3;
  infra-fail-vs-agent-fail distinguishability → AC-6), but **omits the retriable-vs-non-retriable
  classification with bounded backoff entirely**. A.3 goes straight from "non-2xx / pseudo-success /
  empty → explicit FETCH_FAILED" with no retry for transient 超时/5xx/429.
- **Why major**: The audit brief asks whether all 11 decision points landed. This one is only
  partially landed. Operationally: during a 168h run, a transient Forgejo hiccup (5xx/429/timeout)
  would immediately mark the dispatch `FETCH_FAILED` with no retry → a recoverable infra blip is
  counted as a hard failure, eroding AC-5 corpus yield. The infra-fail-vs-agent-fail split (AC-6)
  presumes the classification exists to route retriable cases — but the spec never defines it.
- **Fix**: Add to A.3 (and a TG-1.4 sub-item + AC-3): classify fetch failures into **retriable
  (timeout / 5xx / 429 → bounded exponential backoff, capped attempts)** vs **non-retriable
  (404 / 401 → immediate FETCH_FAILED)**, per DEC decision-point 6. Tie the retriable class to the
  "infra-fail" outcome of AC-6.

### F4 [MINOR][implementation:tasks TG-4 gate] Image-build gate over-broad — TG-2/TG-3 are Hermes-side, not baked into the container image

- **type**: risk
- **Evidence**: tasks.md overview line: "TG-4 gates on TG-1+TG-2+TG-3". But the `aria-runner` image
  only contains container-side artifacts (`docker/aria-runner/**` — `initial.sh` +
  `compute-assertions.sh`, i.e. TG-1). TG-2 (`extension.py`) and TG-3 (`schema.sql`) are Hermes-Layer-1
  code deployed separately to `light-1`, **not** in the container image. TG-4.1's own body correctly
  says "after TG-1/TG-3 land" (still lists TG-3 unnecessarily; TG-3 is schema, also Hermes-side).
- **Why minor**: Not wrong-direction (conservative serialization is harmless), but it implies a
  false build dependency that could unnecessarily block the image rebuild on Layer-1 work. The real
  minimal gate for TG-4 is **TG-1 only** (container code + assertion). The full-system E2E (TG-6)
  correctly gates on everything.
- **Fix**: Change the overview to "TG-4 (image build) gates on **TG-1 only**; TG-6 (E2E) gates on
  TG-1+TG-2+TG-3+TG-4 deployed together". Align TG-4.1 wording (drop TG-3 from its precondition).

---

## Verified-correct (no action) — recorded so convergence can trust the recon

- Regex `^[A-Z][A-Z0-9-]+$` @ `initial.sh:106`; file-mode key mismatch (`issue.yaml`/ISSUE_ID @
  `initial.sh:143-145` vs `prompt.txt`/dispatch_id @ `extension.py:2144`) — root-cause narrative accurate.
- envsubst 5-var whitelist @ `initial.sh:286` (`$ARIA_ISSUE_ID $ARIA_ISSUE_TITLE
  $ARIA_ISSUE_DESCRIPTION $ARIA_FILES_LISTING $ARIA_EXPECTED_CHANGES`); body via `$ARIA_ISSUE_DESCRIPTION`,
  no double-expansion — A.4/AC-7 accurate. Container has no issue-fetch code today (PAT only for clone
  `:251` + PR API `:396`) — accurate.
- 5-AND SUCCESS gate @ `initial.sh:525-534`; `compute-assertions.sh` FILE_HIT/DIFF_HIT init `true`
  with empty-list loop-skip → false-green — root cause C.1/AC-4 accurate; `RENDERING_CONTRACT.md:76`
  "always non-empty (validator enforces)" is file-mode-only — accurate.
- `host-volume.hcl` `aria-runner-inputs` = local `read_only` host_volume (not NFS) → Option D
  honest rejection is correct.
- `schema.sql` `issue_id TEXT` / PK `(issue_id, dispatch_id)` / partial-unique `uq_issue_active_partial`
  — D.1 recon-correction (value-reformat, no structural migration) is **accurate and a genuine
  improvement over the DEC's "(repo,number) composite column" framing**.
- AC-2 stratification via `json_extract('$.issue_type_hint')` from audit payload (`db.py` audit_extra),
  not an `issue_id` join — D.2 recon-correction accurate.
- **AD-M6-10 is genuinely the next-available number** (headers present: M6-1/2/4/5/6/7/8-Retired/9;
  M6-3 skipped; M6-10 unused). Allocation correct.
- `layer-boundary-contract.md` ends at §4 + Appendix → §5 is the correct next section; the "no
  description of how the container obtains issue content" gap is real. F.3 correct.
- Explicit dependency edges (telemetry Spec out-of-scope; Spec #2 operational-precondition-not-code)
  are clearly and correctly stated.
