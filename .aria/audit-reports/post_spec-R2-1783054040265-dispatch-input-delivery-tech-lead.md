---
checkpoint: post_spec
mode: convergence
round: 2
agent: tech-lead
verdict: PASS
spec_id: aria-2.0-m6-dispatch-input-delivery
timestamp: 1783054040265
converged: false
---

# post_spec R2 (convergence) — tech-lead — dispatch-input-delivery

**Verdict: PASS** (0 Critical / 0 Major). Vote: **PASS**.

R1 findings verified truly landed (code-grounded, not paper-fix); the fix-introduced-regression
surface (three-outcome model + AD-M1-4 amend + AD-M6-10 loading) is internally consistent with the
existing state machine / AD set. No new blocker.

---

## R1 finding verification (each traced to landed spec text + live code)

### C1 (Critical) AD-M0-5 misattribution → **FIXED, verified against code**
The R1 correction is factually correct and fully propagated:
- **Code ground truth**: `docs/architecture-decisions.md:384` (AD4 risk-table row #2) literally reads
  `AD-M0-5 约定: prompt 写 bind mount 文件, meta 只传 ISSUE_ID + 小参数` — this is the *only* home of
  the bind-mount premise, and it **mislabels** it. `docs/architecture-decisions.md:1035` (AD-M0-5
  body) is `m0-handoff.yaml schema 锁定 12 字段` — genuinely unrelated. The spec's diagnosis holds
  byte-for-byte.
- **Propagation complete** — `grep AD-M0-5` across proposal+tasks shows **zero** residual
  "amend/订正 AD-M0-5": frontmatter `:12`, §What F.2 `:185-188`, §How table `:203`, AC-10 `:276-279`,
  tasks TG-5.2 `:61` all say "correct AD4 risk-table cell (`:384`)" + "leave AD-M0-5 body (`:1035`)
  untouched". Constraints `:246` lists "AD4-cell correction" (no AD-M0-5 amend).
- **Nice**: `:203` explicitly notes "DEC line 22 carried the same misattribution — corrected here",
  so the spec correctly supersedes the upstream DEC error and documents the divergence rather than
  silently inheriting it. Correct downstream-authority handling.

### M1 (Major) ISSUE_URL / id-first → **FIXED, verified against code**
- **Code ground truth**: `extension.py:1176` = `issue_id = str(issue.get("id") or issue.get("number") or "")`
  → id-first, confirmed. ISSUE_URL at `:2147-2153` uses `FORGEJO_ORG`/`FORGEJO_REPO` env (default
  `10CG`/`Aria`, hardcoded) + interpolates `issue_id`. Both defects (internal-id + hardcoded repo)
  are real.
- §What B.3 `:105-111` faithfully restates this current state and prescribes the fix (retain raw
  **number** as a separate field, not parsed back from the composite `issue_id`; build
  `ISSUE_URL = {forgejo_base}/{target_repo}/issues/{raw_number}`). AC-11 `:280-282` requires
  verification on an `id != number` / non-Aria `target_repo` issue (defeats the early `id==number`
  masking). TG-2.3 `:43` mechanizes it. Substance complete; the raw-number-retention living in B.3
  (rather than a separate B.4) is immaterial — B.4 `:112-114` is head_branch unification, correct.

### M2 (Major) retry classification → **FIXED**
§What A.3 `:80-86`: retriable (timeout/5xx/429) → bounded exponential backoff (finite) then give up;
non-retriable (404/401/pseudo-success/empty) → immediate `INPUT_FETCH_FAILED`; "never `|| true`,
never silent continue"; both surface as `INPUT_FETCH_FAILED` but logged distinctly. AC-3 `:257-259`
and TG-1.4 `:31` mirror it. Matches DEC decision-point 6. Landed.

### minor TG-4 gate → **FIXED**
Overview note `:22` "TG-4 (image build) gates on TG-1 only" + TG-4.1 `:55` (only container-side code
baked; TG-2/TG-3 deploy to Hermes/light-1 separately). Correct.

---

## Fix-introduced-regression surface (the R2 focus) — clean

### Three-outcome model vs state machine → consistent
- **Code ground truth**: `initial.sh:524-536` = the AD-M1-4 5-AND gate (PENDING → SUCCESS else
  `ASSERTION_MISMATCH`); `:591-596` maps **only** `SUCCESS→exit 0`, else `exit 1`. The spec's §What C
  premise (a naive empty-guard forces fetch-mode into ASSERTION_MISMATCH→exit 1→S_FAIL, reproducing
  100% S_FAIL in a new form) is byte-accurate.
- The fix routes fetch mode through a **distinct** terminal `AUTONOMOUS_COMPLETED` (C.2 `:142-148`,
  three-condition `claude_exit==0 AND commit AND PR`, no file/diff hits) → **exit 0** branch (TG-1.9
  `:36`, must be added at the `:591-596` mapping so it is not swept into `else exit 1`). C.1 keeps
  file-mode 5-AND but hardens empty lists to `unknown`/`skip`. This does **not** re-break the state
  machine: the RED-test requirement is pinned to the **real `initial.sh` call-site** (C.2 `:143-145`,
  AC-4a `:260-264`), which is exactly what prevents the isolated-script masking that R1 flagged.
  Internally consistent, no new dead-end.

### AD-M1-4 amend → scopes, does not replace
§How table `:202` + F.5 `:189-190`: 5-AND `SUCCESS` scoped to file mode; adds the distinct
`AUTONOMOUS_COMPLETED` (`assertion_verified:false`, excluded from verified-SUCCESS corpus, C.3
`:149-154`) + `INPUT_FETCH_FAILED`. This narrows an existing decision rather than contradicting it —
consistent with the `initial.sh:526` "per AD-M1-4: 5 AND" anchor. No conflict.

### AD-M6-10 loading (C' + single-node bind-mount scope) → **not over-loaded**
The reviewer's over-load concern resolves cleanly: the single-node bind-mount scope is the *root-cause
background* for why C' dual-channel exists (bind mount only works single-node → node-agnostic channel
needed). Placing it in AD-M6-10's 六段 "背景" section (F.1 `:182-183`, §How `:201`) is its natural
home; the AD4 risk-table cell is merely a risk row that should not carry a full decision, so it
cross-references AD-M6-10 for the fuller treatment. One decision, one background statement — coherent,
not two unrelated concerns crammed together.

### `FailReason.INPUT_FETCH_FAILED` addition → consistent with enum design
`interfaces.py:67-90` is an explicit 11-value enum (M3 9 + M4 2) documented as "additive
non-collision, no implicit fallthrough". Adding a 12th value for input-fetch is exactly the
sanctioned extension pattern; the spec's "closed enum with no fetch/input value" claim (`:118`,
`:228-229`) is accurate. TG-2.5 `:45` + AC-6 `:267-270` route it distinct from `CONTAINER_CRASH`.

---

## Observations (non-blocking, Phase-B detail)

- **[minor][design:layer1]** The enum already has a generic `INFRASTRUCTURE` value. `INPUT_FETCH_FAILED`
  is justified (AC-6 corpus attribution needs a *dedicated* infra-fetch reason distinguishable from
  container-crash), but Phase B should note in the AD-M1-4 amend / interfaces docstring **why**
  `INPUT_FETCH_FAILED ≠ INFRASTRUCTURE` (fetch-fail is an input-delivery infra sub-class Layer 1
  attributes separately) so a future reader does not collapse them. → cover in TG-2.5 / TG-5.3 doc
  text. Does not affect the spec's correctness.

## Rationale for PASS

All four R1 findings (1 Critical, 2 Major, 1 minor) are landed with the fix text traceable to the
exact code lines it claims to correct (`architecture-decisions.md:384/1035`, `extension.py:1176/2147-2153`,
`initial.sh:524-536/591-596`, `interfaces.py:67-90`) — no paper-fix, no over-claim. The R2-specific
regression surface (three-outcome model, AD-M1-4 amend, AD-M6-10 loading, enum extension) is
internally consistent with the deployed state machine and AD set; the new `AUTONOMOUS_COMPLETED`
branch is an explicit distinct terminal, not a byproduct of the 5-AND, which is precisely what R1
demanded. The single remaining item is a minor Phase-B documentation nicety, not a spec defect.
0 Critical / 0 Major → PASS.
