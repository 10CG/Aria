# Phase A.2 post_spec R1 audit — code-reviewer position

> **Spec**: `aria-2.0-m6-cost-acceptance` (M6 Spec #1)
> **Phase**: A.2 post_spec R1
> **Position**: code-reviewer
> **Auditor**: Claude Opus 4.7 (1M context), 2026-05-24
> **Round budget**: ~10-15 min
> **Inputs read**: proposal.md (445 lines), tasks.md (210 lines), DEC-20260524-001 (303 lines), m5-handoff.yaml (full), PRD §M6 + §成功标准, M5 sibling Spec proposal.md frontmatter, CLAUDE.md Rule #5+#8, AD-M5-11 reservation note.

---

## Verdict

**NEEDS_FIX** — 1 Critical (file extension contract glitch in §What E vs AC-9 vs tasks T4.1), 4 Important (frontmatter line-number drift fragility, AD-M5-11 reservation conflict with AD-M6-* numbering, OOS-5 vs OOS-7 vs §Gate-role consistency, R2 Pre-Approved (R1 yet to render) signal in §Audit trajectory format), 5 Minor (memory ref cross-doc completeness, effort math vs proportionality, Status string vs OpenSpec enum), 0 observations material to convergence.

Spec is structurally sound, faithful to DEC-20260524-001 §2 scope, and binary-falsifiable per all 9 ACs. The contract glitch (Critical) and 2 fragility items (Important) are mechanical fixes per `[[feedback_spec_literal_surfaces_contract_glitch]]` — owner can ship R2 with concrete fixes propagated 2-pass per `[[feedback_spec_v2_body_propagation_2pass]]`.

---

## Critical findings (must fix before Phase A.3)

### CR-R1-C1 — Acceptance script file extension contract glitch (.sql vs .py) — 3 occurrences disagree

`[[feedback_spec_literal_surfaces_contract_glitch]]` applies: ≥2 surface locations cite contradictory filename.

| Location | Cite |
|---|---|
| proposal.md:147 (§What E) | "`aria-orchestrator/acceptance/check-m6-cost-acceptance.sql` (or Python wrapper calling SQLite)" |
| proposal.md:222 (§How data pipeline diagram) | "`check-m6-cost-acceptance.sql  →  PASS/FAIL per criterion`" |
| proposal.md:368 (AC-9 evidence bash) | "`python3 check-m6-cost-acceptance.py`" |
| tasks.md:91 (T4.1) | "Implement `aria-orchestrator/acceptance/check-m6-cost-acceptance.py`" |

**Why critical**: AC-9 evidence command literally invokes `python3 check-m6-cost-acceptance.py` (line 368). If implementer follows §What E + §How diagram literally, file is `.sql` — AC-9 unrunnable. If implementer follows AC-9 + T4.1, file is `.py` — §How data flow diagram references a non-existent `.sql` artifact. Either way, one Spec section silently lies post-implementation.

**Anti-paper-fix replacement** (propagate to all 4 surfaces in P1 2-pass):
- proposal.md:147 change `aria-orchestrator/acceptance/check-m6-cost-acceptance.sql` (or Python wrapper calling SQLite)` → `aria-orchestrator/acceptance/check-m6-cost-acceptance.py` (Python wrapper executing inline SQL against SQLite)`
- proposal.md:222 change `check-m6-cost-acceptance.sql` → `check-m6-cost-acceptance.py`
- proposal.md:368 (AC-9): already `.py` — keep
- tasks.md:91 (T4.1): already `.py` — keep

Rationale: AC-9 evidence is exec-bound (runs the file by literal path), so `.py` is the authoritative form. Convert §What E + §How to align with AC-9 (not vice-versa).

---

## Important findings (should fix before Approved)

### CR-R1-I1 — Frontmatter line-citation fragility on m5-handoff.yaml — drift risk if M5 handoff yaml grows

proposal.md:11-16 cites `m5-handoff.yaml line 151-172` and individual promise line ranges (line 152-155, 156-159, 160-163, 164-167, 168-171).

**Verification** (audited against actual `aria-orchestrator/docs/m5-handoff.yaml`, 323 lines total):
- Frontmatter says "line 151-172"; actual `abi_compat_promises:` keyword on line 151, last promise ends at line 171. Range citation `151-172` is **technically off by +1 at the end** (line 172 is blank). Strictly correct: `151-171` or `148-172` (148 = section header `# 4. abi_compat 承诺 ...`).
- Individual promise line cites are EXACTLY correct: promise#1 line 152-155 ✓, #2 line 156-159 ✓, #3 line 160-163 ✓, #4 line 164-167 ✓, #5 line 168-171 ✓.

**Why important** (not critical): hand-numbered line citations are fragile. If a future contributor inserts comments or reformats yaml whitespace above line 151, **all 6 frontmatter line cites drift simultaneously**, and validate-m6-handoff.py grep targets (which the Spec doesn't currently anchor on line numbers — it greps by promise ID) remain correct. So the fragility is **documentation-only**, but a doc-vs-code drift is exactly what `[[feedback_validator_repo_drift_guard_test]]` warns against.

**Anti-paper-fix replacement** (proposal.md:11):
- Change `source: aria-orchestrator/docs/m5-handoff.yaml line 151-172`
- To `source: aria-orchestrator/docs/m5-handoff.yaml § "4. abi_compat 承诺" (line ranges below are anchor-relative; if yaml above is reformatted, re-verify with grep -n abi_compat_promises)`
- And inside §Constraints table (proposal.md:249-253), replace each `m5-handoff.yaml line N-M` with `m5-handoff.yaml::abi_compat_promises[<id>]` (anchor by structured key, not line offset).

Same fix applies symmetrically to tasks.md (currently no line cites in tasks — fine).

### CR-R1-I2 — AD numbering namespace conflict: AD-M5-11 reserved-for-M6 vs new AD-M6-1..3 slots

DEC §2 Spec #3 (lines 122-123 of brainstorm) states: `"aria-orchestrator/docs/architecture-decisions.md §AD-M5-11 RESERVED slot 用于 M6 docs decisions"`.

But Spec #1 proposal §How (proposal.md:235-241) opens **three new AD-M6-1..AD-M6-3 slots** for Phase B decisions. Sibling Spec #3 (docs) will also want AD-M6-* slots (or claim AD-M5-11).

**Audit of architecture-decisions.md:3460-3478** confirms AD-M5-11 reserved but **explicitly notes**: "如 M6 期间发现 M5-spillover decision, 在此填充 ... 如 M6 也 unused, 转 'archived' status". So AD-M5-11 is for **M5-spillover** retroactive decisions, NOT M6 forward-decisions.

**Why important**: Convention is consistent (M5-spillover → AD-M5-11; M6 forward → AD-M6-*), but DEC brainstorm §2 Spec #3 line 123 mis-cites it ("`AD-M5-11 RESERVED slot 用于 M6 docs decisions`") — this is a brainstorm wording bug that Spec #1 has correctly **not** propagated. However:
1. Spec #3 (docs) will draft to the brainstorm wording, accidentally re-using AD-M5-11 for M6 docs decisions.
2. Spec #1 + Spec #3 will then both want different things from AD-M5-11.
3. AD-M6-1..3 in Spec #1 don't conflict with Spec #3's AD-M6-* claims yet, but **no numbering coordination contract exists across the 4 sub-Specs**.

**Anti-paper-fix replacement** (insert into proposal.md after line 241):
```
> **AD-M6-* numbering coordination**: This Spec claims slots AD-M6-1..AD-M6-3 for cost-acceptance scope.
> Sibling Specs (#2 e2e-resilience, #3 docs, #4 release-closeout) must claim subsequent slots starting
> from AD-M6-4 in their respective Phase A drafts. AD-M5-11 (reserved 2026-05-15 per
> architecture-decisions.md:3460) is for M5-spillover retroactive decisions only — not M6 forward
> decisions. The brainstorm DEC §2 Spec #3 line 123 should be read with this clarification.
```

Plus owner action: amend brainstorm DEC §2 Spec #3 line 123 to remove `AD-M5-11 RESERVED slot 用于 M6 docs decisions` (replace with `AD-M6-4..AD-M6-N (continuation)`). Optional — brainstorm is historical record, but uncorrected it will mis-cue Spec #3 drafter.

### CR-R1-I3 — OOS scope inconsistency: OOS-5 vs §Gate role vs AC-7 fold

- OOS-5 (proposal.md:194): `"3-day trending data production itself"` is marked OOS with reason "Spec #1 ships the schema + cron; owner manually runs cron daily ≥3 days before Spec #2 starts".
- §Gate role in M6 sequencing (proposal.md:53-55) AND §What G (proposal.md:176-184) AND AC-7 (proposal.md:344-354) all explicitly **require** the 3-day history check to be implemented (`check_3_day_rolling_history_exists`) and to GATE Spec #2 startup.

**Why important**: OOS-5 claims production of trending data is OOS, while §What G + AC-7 + tasks.md T5.8 all build the **mechanism to verify** it exists. The wording "3-day trending data production itself" is ambiguous — does it mean (a) writing the data (cron does this in scope) or (b) acquiring 3 calendar days of accumulated history (owner manual cron-run loop)?

Reading carefully, the intent is (b): owner-blocking accumulation step is OOS, but the cron writes daily ✓ AND the validator check is in scope ✓. The current OOS-5 wording invites future-reader misreading "trending data production is OOS" as "we don't write daily snapshots".

**Anti-paper-fix replacement** (proposal.md:194):
- Change `OOS-5 | 3-day trending data production itself | ...`
- To `OOS-5 | Owner-manual ≥3-day cron-run accumulation loop (cron infrastructure + per-day snapshot writes are in scope §What G; only the wall-clock 3-day waiting period and owner-action to run cron daily are out of scope) | Spec #1 ships the schema + cron + daily snapshot writes + AC-7 validator; owner manually triggers cron daily for ≥3 days OR waits for natural cadence before Spec #2 starts`

### CR-R1-I4 — Spec status string deviates from sibling M5 convention + state-scanner enum

proposal.md:4 + tasks.md:5 both use status `"Draft (Phase A.1; pending Phase A.2 post_spec audit)"`.

**Comparison vs sibling M5 archived Spec** (post-archive convention):
- M5 proposal.md:4 uses `"Complete (...)"` post-archive; pre-archive used `"Approved (Phase A.2 ... SCOPE_OK_R2 ...)"`.
- aria/skills/state-scanner/SKILL.md:574 shows `> **Status**: Approved` as canonical.
- standards/openspec/project.md:4 uses `Status: Active`.

**Why important**: not a hard block — "Draft" is acceptable for pre-approved status. But for downstream tooling (state-scanner Phase 1.x scans look for normalized status enum: Draft / Approved / Complete / Archived), the parenthetical suffix `(Phase A.1; pending Phase A.2 post_spec audit)` is informational and won't parse cleanly. M5 used trajectory in a SEPARATE frontmatter line (`Audit trajectory:`), which Spec #1 already does (proposal.md:17-19) — so the suffix is **redundant** with §Audit trajectory.

**Anti-paper-fix replacement** (proposal.md:4 + tasks.md:5):
- proposal.md:4: change `> **Status**: **Draft** (Phase A.1; pending Phase A.2 post_spec audit)` → `> **Status**: **Draft** (Phase A.1 complete; Phase A.2 R1 in progress)`
- tasks.md:5: same edit pattern.
- Keep §Audit trajectory block for detailed tracking — it's correctly placed in proposal.md:17-19.

---

## Minor findings (nice to have)

### CR-R1-M1 — Memory ref `[[feedback_audit_driven_fix_conventions]]` cited by R1 prompt but absent from Spec body

The R1 audit prompt mandates citing `[[feedback_audit_driven_fix_conventions]]` (R<N>-<ID> inline fix convention). Spec body (proposal.md + tasks.md) does **not** reference this memory ref — and arguably shouldn't, since it's an audit-process pattern, not a Spec deliverable.

**Action**: no Spec change. Audit reports (this file) cite the ref by convention. Confirmed CR-R1-C1 / I1-I4 / M1-M5 IDs follow `R<N>-<ID>` pattern per `[[feedback_audit_driven_fix_conventions]]`.

### CR-R1-M2 — Effort baseline: 32 tasks @ ~10h ≈ 18.75 min/task. Under-estimated per `[[feedback_phase_budget_compounding]]`?

Group breakdown:
- T-schema (4 tasks) @ ~2h = 30min/task ✓ reasonable
- T-config (3 tasks) @ ~1h = 20min/task — tight (T2.3 unit test alone could be 15-20min)
- T-alarm (6 tasks) @ ~2h = 20min/task — **tight**; T3.1 (Feishu logic + card fields wiring) realistically 30-45min
- T-acceptance (4 tasks) @ ~1.5h = 22.5min/task ✓ reasonable
- T-validate (10 tasks) @ ~2.5h = 15min/task — **very tight**; T5.2 (grep schema.sql + check both keywords + exit code semantics) realistically 20-30min
- T-docs (3 tasks) @ ~0.5h = 10min/task ✓ for stub slots
- T-prd (2 tasks) @ ~0.5h = 15min/task ✓ verify-only

**Why minor**: M5 ratio per `[[project_us025_m5_phase_1_done_2026-05-14]]` was ~0.52 (Phase 1: 13h actual vs 25h baseline). If Spec #1 follows M5 Phase 1 ratio it would be **5h actual**, not 10h. But `[[feedback_phase_budget_compounding]]` notes later phases drift higher. For this Level 2-3 borderline Spec with no novel architecture, central 10h is **plausible** but the per-task distribution is uneven. No fix required — risk is small, R-M6-2 captures threshold-set blocking.

### CR-R1-M3 — `or .py` ambiguity in T1.1 file path

tasks.md:28 says `aria-orchestrator/acceptance/m6-cost-snapshot.sh or .py`. This mirrors proposal §What A but T1.2 / T1.3 / T1.4 do not pin which extension. AD-M6-1 slot (proposal.md:239) is reserved for this decision.

**Why minor**: AD slot exists for the deferred decision (good Aria practice). Slight risk: if implementer drafts Phase B before AD-M6-1 is filled, both .sh and .py paths may end up half-written.

**Suggestion**: in T1.1, change `.sh or .py` to `.sh or .py (AD-M6-1 decision; pin to one before T1.2)`.

### CR-R1-M4 — `subscription_usd.model` field semantics unspecified

proposal.md:80 shows schema:
```
"subscription_usd": { "provider": "luxeno", "model": "<model_id>", "cost_usd": null, ... }
```

Luxeno is a flat subscription with multiple models routed under one bill. What does `subscription_usd.model` mean — primary model? Most-used model? Comma-separated list? Empty string?

**Why minor**: Phase B implementer may default to empty string or constant — acceptable. AC-2 (proposal.md:288) doesn't check `subscription_usd.model` content so it won't break acceptance. But `[[feedback_falsifiable_evidence_for_binary_acceptance]]` mandates concrete schema semantics for all fields — `model` field for subscription_usd is the one underspecified field.

**Suggestion**: add to proposal.md after line 86: `subscription_usd.model semantics: most-used model_id during the billing window (informational only; if billing API not exposing, use null or "mixed-subscription").`

### CR-R1-M5 — `cost_measurement_method` field optionally present in cost.json — schema spec gap

P-2 / AC-8 / T5.7 all describe a `cost_measurement_method` enum check. proposal.md:170-174 says **"if present in the schema"** the check validates the enum value; if absent, the check verifies a schema document. tasks.md:130-134 mirrors this conditional.

**Why minor**: this is a graceful fallback design (don't force schema change if doc covers it). But: §What A schema sample (proposal.md:68-89) **does not include** the field, so by default it WILL be absent — meaning the check always runs the documentation-grep branch. The "doc-only branch" risk is the paper-fix antipattern per `[[feedback_paper_fix_antipattern]]`.

**Suggestion**: pin the field as present (always-write) in §What A schema sample. Add per-row:
```
"metered_usd": {..., "cost_measurement_method": "local_token_count_x_unit_price"}
"subscription_usd": {..., "cost_measurement_method": "subscription_flat_no_attribution"}
```
Then T5.7 only needs the schema-validation branch (simpler, paper-fix-resistant).

---

## Observations (non-blocking)

### CR-R1-O1 — Cross-reference completeness commendable

proposal.md:421-444 (§Cross-references) and tasks.md:196-201 (Precision items cross-reference table) BOTH explicitly thread DEC §4 P-1/P-2/P-3 to §What sections AND task numbers. This is exactly the 2-pass propagation discipline from `[[feedback_spec_v2_body_propagation_2pass]]`. **Strength**: the table at tasks.md:198-201 is a model for future M6 sub-Spec audits.

### CR-R1-O2 — Predecessor Spec link path correctness verified

proposal.md:8 cites `[aria-2.0-m5-replay-reconciler-drift-review-loop-audit](../../archive/2026-05-23-aria-2.0-m5-replay-reconciler-drift-review-loop-audit/proposal.md)`. Path correctness verified: `openspec/changes/aria-2.0-m6-cost-acceptance/proposal.md` ../../ = `openspec/` + `archive/2026-05-23-...` = exists ✓.

### CR-R1-O3 — Rule #5 compliance verified

Spec lives in `/home/dev/Aria/openspec/changes/aria-2.0-m6-cost-acceptance/` — main repo `openspec/changes/` per Rule #5 ✓. Not in `standards/openspec/changes/` (correctly avoided).

### CR-R1-O4 — Rule #8 (pre-merge gate) not applicable to Spec #1 itself

Spec proposal/tasks does not mention Phase C merge specifics; phase-c-integrator C.2.4 gate is enforced at PR-merge time (not Spec-author time). No Rule #8 finding.

### CR-R1-O5 — DEC §3 vs §OOS reconciliation

DEC §3 has 7 explicit drops; proposal §OOS has 9 items. The extra 2 (OOS-6 reuse webhook, OOS-7 no schema migration) are **scope-creep prevention adds**, not contradictions. Both align with DEC §2 Spec #1 scope (which explicitly says "reuse ARIA_FEISHU_WEBHOOK_URL" and "M2 T9 token_usage schema 复用"). Healthy.

### CR-R1-O6 — Commit a786444 (PRD patch) exists; PRD §638-646 dual-track verified

`git log --oneline a786444` returns `a786444 docs(prd-v2): M6 reframe + cost gate dual-track patch (DEC-20260524-001)` ✓. PRD line 638-646 content verified: §638 "M6 验证 (发版前)" header; §642-646 contains dual-track (i)+(ii)+(iii) language matching Spec #1 schema. Cross-ref accurate.

### CR-R1-O7 — DEC §2 vs proposal §What scope mapping table

| DEC §2 Spec #1 scope item | proposal §What section |
|---|---|
| 双行 cost.json schema | §What A (lines 63-104) ✓ |
| owner-set thresholds .aria/config.json | §What B (lines 106-121) ✓ |
| freshness_ts 字段 | §What C (lines 123-129) ✓ |
| cron sentinel + alarm path | §What D (lines 131-143) ✓ |
| acceptance SQL script | §What E (lines 145-149) ✓ |
| Luxeno=0 静默假阳性 prevention | §What A (lines 91-95) + §What D (lines 137-141) ✓ |

All 6 DEC §2 scope items mapped. No missing items, no scope creep.

Additionally Spec #1 adds **§What F (validate-m6-handoff.py)** and **§What G (3-day rolling history)** — these come from DEC §4 P-3 (M-ba-R3-1c) and cr-CH-9 closure (cited in §Why). Justified additions.

---

## Cross-cutting consensus signals (for orchestrator)

- **C1 critical (file-extension contract glitch)** is mechanical, 4-line fix, propagation per `[[feedback_spec_v2_body_propagation_2pass]]` (P1 lock decision = `.py`, P2 propagate to §What E + §How diagram).
- **I1 (line-citation fragility)** is structural — recommend converting line-number citations to anchor-relative (`§ "4. abi_compat 承诺"`) + structured-key (`::abi_compat_promises[<id>]`) form. This is a **reusable pattern** for all 3 remaining M6 sub-Specs that will need to cite m5-handoff.yaml.
- **I2 (AD numbering coordination)** is a 4-sub-Spec contract not currently enforced. Recommend the orchestrator (Phase A.3 task-planner) emit a cross-Spec AD slot allocation note BEFORE Spec #2/#3/#4 Phase A.1 drafting starts.
- **I3 (OOS-5 wording)** is doc-only ambiguity; mechanical replacement provided.
- **I4 (Status string)** is convention drift; replace inline.

No issue rises to the level of blocking R2; all Critical + Important are mechanical and propagation-discipline-bound. Spec #1 is on track to converge in R2 with ~5-10 line changes plus the AD numbering cross-cut.

---

## Memory refs cited

- `[[feedback_audit_driven_fix_conventions]]` — used to ID-tag findings R<N>-<ID> for traceability
- `[[feedback_spec_v2_body_propagation_2pass]]` — basis for C1 propagation discipline + I1 structural anchor recommendation
- `[[feedback_validator_repo_drift_guard_test]]` — basis for I1 line-cite fragility framing
- `[[feedback_spec_literal_surfaces_contract_glitch]]` — basis for C1 (≥2 surface contradictory cite)
- `[[feedback_falsifiable_evidence_for_binary_acceptance]]` — Spec compliance verified (M4 references)
- `[[feedback_paper_fix_antipattern]]` — basis for M5 (cost_measurement_method always-write recommendation)
- `[[feedback_phase_budget_compounding]]` — basis for M2 effort sanity-check

---

## Verdict summary

| Severity | Count | IDs |
|---|---|---|
| Critical | 1 | CR-R1-C1 |
| Important | 4 | CR-R1-I1, I2, I3, I4 |
| Minor | 5 | CR-R1-M1, M2, M3, M4, M5 |
| Observation | 7 | CR-R1-O1..O7 |
| **Total** | **17** | — |

**Recommendation**: NEEDS_FIX — proceed to R2 after applying C1 + I1-I4 fixes (≤10 lines edits). Minor items can be folded into R2 as polish. Observations are non-blocking convergence signals.

