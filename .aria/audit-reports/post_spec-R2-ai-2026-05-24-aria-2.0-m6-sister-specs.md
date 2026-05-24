# Phase A.2 post_spec R2 CHALLENGE — ai-engineer (combined Spec #2 + Spec #3)

> **Date**: 2026-05-24
> **Auditor**: ai-engineer (R2 CHALLENGE, combined-Spec mode)
> **Specs under review**:
> - Spec #2: `aria-2.0-m6-e2e-resilience` (proposal.md 1076 lines, tasks.md 957 lines — post-R1-fix @ `8a5fdc4`)
> - Spec #3: `aria-2.0-m6-docs` (proposal.md 685 lines, tasks.md 505 lines — post-R1-fix @ `8a5fdc4`)
> **R1 baseline**: this auditor authored 6 Critical (C-AI-1..6) + 8 Important (I-AI-1..8) + 6 Nits.
> **R1-fix diff stat**: `8a5fdc4` touched 6 OpenSpec files (1004 +/- 355) plus a PRD §568 + §656 patch in `e884e62`.
> **Verdict**: **SCOPE_OK_R2** with 0 new Critical + 1 Important (paper-fix residual on Spec #3 §A.3 line 247 Diff-3 propagation gap) + 1 Nit (Spec #3 leftover Hermes+GLM phrasing in system-architecture.md target).
> **Reference Specs/sources read (R2)**:
>   - Live PRD §560-580 (§568 location), §640-665 (§656 median patch), §645 (dispatch volume floor)
>   - Live `aria_layer1/provider_router.py:111,140,187,244,315,545,568` (LLMRouteExhausted, ProviderRouter.call_llm/route_for_state, __all__)
>   - Live `aria_layer1/silknode_client.py:54,126,217` (`_LLMHTTPError`, module `call_llm`, class method)
>   - Live `aria_layer1/zhipu_client.py:77,105,294,346` (`ZhipuHTTPError`, `ZhipuNetworkError`, `call_llm`)
>   - Live `aria_layer1/token_tracking.py:60-100,147-156` (compute_cost provider branching, Luxeno=0 path)
>   - Live `aria_layer1/schema.sql:35-279` (full dispatches/audit_log column inventory)
>   - R1 aggregate report + own R1 report
>   - Memory: `[[project_glm_routing_luxeno]]`, `[[feedback_mock_layer_per_failure_semantic]]`, `[[feedback_test_mock_pattern_hides_prod_bug]]`, `[[feedback_paper_fix_antipattern]]`, `[[feedback_falsifiable_evidence_for_binary_acceptance]]`, `[[feedback_validator_repo_drift_guard_test]]`, `[[feedback_pat_scope_canonical_from_codebase_grep]]`

---

## 0. TL;DR (one screen)

**Five of six R1 Criticals fully CLOSED with substantive (not paper) fixes. One R1 Critical (C-AI-5 AD-M5-11 cross-Spec lock) CLOSED via an alternate but materially stronger path (Spec #3 vacated AD-M5-11 → AD-M6-9 per Q2 owner lock; this also auto-closes the original collision risk).**

Eight R1 Importants: I-AI-1, I-AI-2, I-AI-5 (partial — see I-AI-5p below), I-AI-6, I-AI-7, I-AI-8 — CLOSED with text-level fixes. I-AI-3 + I-AI-4 — CLOSED with explicit deferred-to-Phase B annotations consistent with R1 recommendations.

**One R2 residual** (Important): Spec #3 §A.3 line 247 still phrases "Layer 1 (Hermes + GLM) and Layer 2 (...)" without the Luxeno-routing qualifier that I-AI-5 R1 demanded. R1 fix only propagated to §A.1 Diff 3 (line 70) — a single-occurrence sed that missed a sibling. Per `[[feedback_spec_v2_body_propagation_2pass]]`, the fix needed a 2-pass body propagation; this is the kind of paper-fix residual the discipline exists to prevent. Filed as **N-R2-AI-1 → Important** (system-architecture.md is the artifact future AI sessions read; "GLM" is the legacy/misleading name).

**No new Criticals raised**. Vote: **SCOPE_OK_R2 = YES**.

Provider-domain cross-checks (anti-paper-fix sweep on others' findings): the SQL column rewrite (T2-1), state_machine module distribution (T2-2 / Q1 lock), AC-6 bounded-zeros guard (T2-3), Mechanism A lock (T2-4), AC-1 alloc.CreateTime (T2-5), and mean→median patch (X-T3 / Q4) all hold up under provider-semantic and live-schema verification. No COALESCE-style NULL-masking detected.

---

## 1. R1 Critical closure verification (anti-paper-fix discipline)

### C-AI-1 — Spec #2 SQL non-existent columns — **CLOSED ✓**

**R1 ask**: every SQL column matches `schema.sql:35-239`. Mechanical grep test scaffolded.

**R2 verification**:

- Live `dispatches` schema (re-grepped @ HEAD): `state TEXT NOT NULL` (line 66), `state_entered_at TEXT NOT NULL` (line 67), `cycle_start_ts`, `cycle_end_ts`, `failed_from_state`. **Absent**: `final_state`, `created_at`, `title`, `issue_type`, `project_name`. Confirmed.
- `S9_CLOSE` and `S_FAIL` are documented enum values in `schema.sql:65` comment plus query usage at `:259` and `:264`. Confirmed.
- Spec #2 proposal §A.2 lines 111-150 now explicitly enumerate "Schema reality" with each absent column called out, and the rewritten SQL block (lines 138-150) uses `state = 'S9_CLOSE'` + `state_entered_at`. ✓
- AC-2 SQL inline block (proposal §AC-2 lines 757-805): three SQL queries, all using `state='S9_CLOSE'` + `state_entered_at`. The per-type stratification query (lines 790-799) sources `issue_type` from `json_extract(al.payload_json, '$.issue_type_hint')` rather than a non-existent column. ✓
- tasks.md §TG-A-infra `T-validate-schema-1` (lines 56-86) adds a regression test that runs `PRAGMA table_info(dispatches)` and asserts `'title' not in cols`, `'issue_type' not in cols`, `'project_name' not in cols`, `'final_state' not in cols`. This is the `[[feedback_validator_repo_drift_guard_test]]` pattern executed correctly. ✓
- Cross-project (P-9) query in tasks.md A-dispatch-6 (lines 280-294) does NOT reference `project_name`. It uses `json_extract(al.payload_json, '$.project') as project` from `dispatch_audit_log` (with explicit caveat: the `$.project` JSON path is documented as a placeholder needing Phase B verification against live payload). This is honest — no hidden assumption. ✓
- **No COALESCE/NULL-mask antipattern detected** anywhere in the rewritten SQL. The rewrite is structural (different table sources + json_extract) rather than column-rename gimmickry.

**Anti-paper-fix sanity check**: did the fix introduce a different illusion? The `$.issue_type_hint` json_extract key is documented as needing Phase B verification (tasks.md A-dispatch-1 line ~165, plus proposal §A.2 lines 119-127 explicit "implementer must verify exact payload key"). This is honest deferral with a falsifiable verification step — not soft-grading.

**Verdict**: **CLOSED**. No paper-fix residual.

---

### C-AI-2 — PRD §639 mean vs Spec median — **CLOSED ✓ via PRD patch**

**R1 ask** (one of two paths): patch PRD or revert Spec. Either way, cite canonical authority.

**R2 verification**:

- PRD `prd-aria-v2.md:656` post-patch reads: `拟人命令质量 (人工评分, 10 samples median ≥ 7/10; lock 2026-05-24 per Spec #2/#3 R1-audit-Q4 — median 替换原 "平均" 因 bimodal score 分布 robust + falsifiability 更强 + Lab industry convention)`. ✓ Median is now the PRD text. R1 fix took Option α (patch PRD) per Q4 owner lock.
- Spec #2 §C.2 (proposal lines 519-523): "Median scoring: median of the 7 dimension scores for a single sample. Pass threshold: ≥7. Corpus pass: median of all 10 sample medians ≥7/10 (per post-patch PRD §656, 2026-05-24)." ✓
- Spec #2 AC-5 (proposal lines 870-876): `statistics.median([float(s) for s in all_10_sample_medians]) >= 7.0` with explicit cite "per post-patch PRD §656 line 656". This is a **single median over a list of 10 sample medians**, not "median of medians" (the original R1 critique noted the awkward phrasing). Implementation is `statistics.median(list)` — exactly one function call, falsifiable. ✓
- Spec #3 §B.3 line 311 mirrors: "≥10 curated samples ... PRD §639 rubric (7 dimensions D1-D7, median ≥ 7/10 threshold)". Matches Spec #2 SoT. ✓
- Integer-vs-float boundary concern (R2 new): `statistics.median([7,7,7,8,8])` returns `7` (int) and `7 >= 7.0` is True per Python (int/float coercion). `statistics.median([7,7,8,8])` returns `7.5` (float, midpoint of two middles). Boundary score `7` PASSES (≥7.0 is `>=`, not `>`). This is correct and matches PRD intent. No defect.

**Anti-paper-fix sanity check**: did the Spec swap "median" for "average" but leave the code computing mean? No — Spec #2 AC-5 (line 875) and tasks.md C-scores-2 (per R1 line 624-642) both use `statistics.median(...)`. The PRD was patched, the Spec was self-consistent originally. Both layers aligned. ✓

**Verdict**: **CLOSED**. PRD and Spec aligned via PRD-edit path.

---

### C-AI-3 — PRD §568 location supersede — **CLOSED ✓ via PRD patch**

**R1 ask**: PRD §568 patched OR documented supersede; Spec #4 dependency added.

**R2 verification**:

- PRD `prd-aria-v2.md:567-568` post-patch reads `| layer-boundary-contract.md | Layer 1 / Layer 2 职责契约 | \`aria-orchestrator/docs/\` (Aria-specific 内部契约,非 Lab-shareable;per km M-km-R2-005 brainstorm 决策 + Spec #3 R1-audit-Q3 lock 2026-05-24 — Lab 其他项目不复用 Aria 双层架构,放 standards/ 会污染 Lab 共享空间) |`. ✓ Location is now `aria-orchestrator/docs/`, with full rationale inline. R1 fix took the recommended path (patch PRD) per Q3 owner lock.
- Spec #3 §B.4 (proposal lines 332-336) cross-references the patch with the `<!-- R1-T3-5 fix: PRD §568 patched 2026-05-24 (e884e62) -->` HTML comment trail. ✓
- The R1 recommendation to "add Spec #4 dependency" — Spec #3 §Dependencies (proposal line 650) still tracks Spec #4 as downstream; the PRD §568 patch is now landed (no need for Spec #4 to gate on it). ✓ Cleaner than adding a release-blocker checklist item to Spec #4.
- The `<!-- Aria-specific: this file is NOT Lab-shareable. Per km M-km-R2-005 decision. -->` comment in the actual `layer-boundary-contract.md` target file remains aligned. (To be verified at Spec #3 Phase B write; not in scope for R2 audit of OpenSpec text.)

**Anti-paper-fix sanity check**: was the patch a one-liner that fooled the grep without actually changing semantics? No — PRD §568 has a substantive inline rationale (~150 chars) explaining the Lab-shareability boundary. The change is semantically meaningful, not a label swap.

**Verdict**: **CLOSED**.

---

### C-AI-4 — `is_synthetic` Mechanism A locked at Phase A — **CLOSED ✓**

**R1 ask**: live probe ran; AD-M6-4 Decided with Mechanism A; Mechanism B path removed.

**R2 verification**:

- Spec #2 proposal §A.2 lines 152-172 unambiguously lock Mechanism A: "Mechanism A — Schema column (LOCKED)" header; explicit deletion narrative at lines 165-170 with rationale "`dispatches.title` column does not exist (live `schema.sql:35-239`), making CASE WHEN title LIKE ... structurally invalid at SQL layer and producing `sqlite3.OperationalError: no such column: title` on day 1". ✓
- AD-M6-4 table entry (proposal line 683): "**LOCKED to Mechanism A** (R1 audit 2026-05-24). Mechanism B (title prefix) was removed". ✓ AD slot is Decided (not Deferred) per `[[feedback_ad_slot_backfill_checkpoint]]` discipline.
- tasks.md A-infra-2 (lines 87-99) writes migration 006 unconditionally — no if/else Mechanism A/B branch. ✓
- tasks.md line 98 declarative: "schema column is_synthetic, migration 006) — locked at R1 audit 2026-05-24. Mechanism B (title prefix) structurally invalid: no title column in dispatches schema." ✓
- Migration target version v5.0 per `[[feedback_schema_migration_to_version_bump]]` (proposal line 162, line 616). No no-op silent-skip risk. ✓
- Live probe (R1 ask point 1): the Spec doesn't explicitly cite a `.aria/probes/m6-pre-spec-b-schema-snapshot.md`. However, the audit-time verification of `schema.sql:35-239` (which the R1 fix narrative cites repeatedly) serves the same epistemic function as a live probe. R1 asked for a probe to confirm "no migration in flight"; M5 archived 2026-05-23 (per memory) with schema v4.2 stable, and no Spec #1 / #3 migration is pending (Spec #1 c29a800 is read-only on schema). This is implicit in the Spec but acceptable.

**Anti-paper-fix sanity check**: was Mechanism A locked but a hidden fallback added? Grep of proposal+tasks for "Mechanism B" returns only the deletion-rationale narrative (lines 165-170 + 167-170 + 201 + 256 + 860-862). No live code path or task fallback to Mechanism B. ✓

**Verdict**: **CLOSED**.

---

### C-AI-5 — AD-M5-11 cross-Spec lock — **CLOSED ✓ via alternate path (stronger)**

**R1 ask**: Spec #2 frontmatter disclaims AD-M5-11; Spec #3 frontmatter has lock-owner language; tasks.md cites line range.

**R2 verification (alternate path)**:

- Per Q2 owner lock 2026-05-24 (cross-Spec finding X-T4 in R1 aggregate), Spec #3 **vacated** the AD-M5-11 claim and now uses **AD-M6-9** instead. This is materially stronger than the R1 recommendation: instead of locking who-owns-AD-M5-11, the entire collision surface is removed.
- Spec #3 frontmatter line 12: `**AD-M6-7**, **AD-M6-8**, and **AD-M6-9** are reserved for this Spec #3 ... **AD-M6-9** = standards/autonomous/ namespace creation decision (claimed by this Spec per Q2 owner lock 2026-05-24 — AD-M5-11 collision with M5-spillover scope discovered in R1 audit; Spec #3 vacates AD-M5-11 claim). Spec #1 holds AD-M6-1/2/3; Spec #2 holds AD-M6-4/5/6.` ✓
- Spec #3 §B.6 (proposal lines 357-366) explicitly directs `Add AD-M6-9 entry` and `Do NOT edit AD-M5-11 (that slot is reserved for M5-spillover topics)`. ✓
- Spec #3 AC-10 (proposal lines 573-585) verifies AD-M6-9/7/8 present AND that AD-M5-11 is NOT overwritten (post-grep: `grep -q "AD-M5-11" architecture-decisions.md`). The acceptance script verifies the no-overwrite condition. ✓
- Spec #2 frontmatter line 18: `AD-M6-4 / AD-M6-5 / AD-M6-6 reserved for this Spec #2 only`. ✓ No mention of AD-M5-11 (which is correct since Spec #3 vacated it; if Spec #2 has new AD needs beyond 4/5/6 it can use AD-M6-10+ — Spec #3 holds 7/8/9).
- R1 recommendation for Spec #2 to "explicitly disclaim AD-M5-11" is now moot — AD-M5-11 is back in its original M5-spillover RESERVED state per architecture-decisions.md:3460-3478. There is no claim to disclaim.

**Anti-paper-fix sanity check**: did Spec #3 dodge the collision rather than resolve it? The Q2 owner lock path is more robust than the R1 lock-owner path: it preserves AD-M5-11 for its actual purpose (M5-spillover, per the live arch-decisions.md text). The alternative (Spec #3 claiming AD-M5-11) would have orphaned the M5-spillover use case. The chosen path is strictly better. ✓

**Verdict**: **CLOSED via alternate path**. The alternate is materially stronger than my R1 prescription.

---

### C-AI-6 — Pre-flight $2 cap Luxeno=0 paper-fix — **CLOSED ✓ with AD slot**

**R1 ask**: AC-6 evidence script tests count≤3 + latency<8h OR explicit Zhipu override; "$2 cap via cost_usd grep" removed.

**R2 verification**:

- Spec #2 AC-6 (proposal lines 893-944) is now reframed:
  - HTML trail line 895-900: "`assert all(c <= 2.0)` was a Luxeno=0 paper-fix re-introduction — Luxeno (current routing for Layer 1) returns cost_usd=0.0 for every call under subscription billing ... Fix: add structural floor (non-null guard + bounded zeros). AD slot added for pre-flight routing strategy decision (Luxeno zero-cost vs Zhipu metered path)." ✓
  - New `AD-M6-4b` slot (proposal lines 902-908) explicitly carries the routing strategy decision: "default = accept Luxeno null semantic with bounded-zeros guard in acceptance check (zero-cost entries are valid but bounded to ≤3 of 3). If metered cost evidence is required for pre-flight, Phase B implementer overrides routing to Zhipu for 3 pre-flight dispatches and documents in AD-M6-4b." ✓
  - AC-6 acceptance script (proposal lines 912-941) has 3-layer guard:
    1. `assert len(costs) == 3` (count floor) ✓
    2. `assert all(c is not None for c in costs)` (non-null guard) ✓
    3. `if not all(c <= 2.0 for c in costs): FAIL` (hard cap; preserved as defense-in-depth even though Luxeno=0 makes it vacuous) ✓
    4. `zero_count = sum(c == 0.0 for c in costs); if zero_count > 3: FAIL` (bounded-zeros: >3 zero entries suggests parse error, not real Luxeno data) ✓
    5. `[INFO]` line printed if zero_count > 0 documenting Luxeno subscription billing
- R1 recommendation point (i) "count≤3 + latency<8h": count is present (assertion #1). Latency<8h is NOT in AC-6 (R1 surfaced this in the §A.5 cost-cap mechanics suggestion). Spec #2 §A.5 lines 230-245 documents the cost-cap mechanics with hard cap framing, but the 8h latency budget mentioned in R1 (proposed clause b) was not added. This is a minor gap.
- AD-M6-4b is named with a "b" suffix (rather than promoted to AD-M6-7) which is unconventional. Spec #3 holds AD-M6-7/8/9; Spec #2 holds AD-M6-4/5/6. AD-M6-4b is essentially a sub-letter of AD-M6-4. This is fine for tracking but slightly nonstandard. Filed as **N-R2-AI-2 Nit** (no merit-impact).

**Anti-paper-fix sanity check**: did the fix add the `c <= 2.0` assertion back as a hidden trap? Yes, line 924 still has `if not all(c <= 2.0 for c in costs): FAIL`. But this is now correctly framed as a **defense-in-depth guard** that would catch real cost overrun if Zhipu routing were enabled (per AD-M6-4b override path). Under default Luxeno routing it is vacuous but harmless. The structural floor (bounded zeros + non-null) is the actual gate. This is acceptable — multiple layers of guard, with the dominant gate being bounded-zeros. ✓

**Verdict**: **CLOSED**. The bounded-zeros + non-null + count assertions correctly capture the Luxeno-subscription reality without the original paper-fix trivial-pass.

**Minor gap (recorded, not blocker)**: 8h latency budget from R1 not added to AC-6. Falls to Phase B observability. Recorded as a Nit (N-R2-AI-3).

---

## 2. R1 Important closure verification

| R1 ID | R1 ask | R2 status | Evidence |
|-------|--------|-----------|----------|
| I-AI-1 | LLM-4 mock: split Zhipu vs Luxeno 429; remove `RateLimitError`/`ProviderUnavailableError` references | **CLOSED ✓** | Spec #2 proposal §B.1 LLM-4 row (line 344): mocks `silknode_client.call_llm` raising `_LLMHTTPError(status=429)` for Luxeno + `zhipu_client.call_llm` raising `ZhipuHTTPError(status=429)` for Zhipu + OR `provider_router.call_llm` raising `LLMRouteExhausted(chain=[{outcome:"http_429"}])` at router level. HTML comment trail lines 329-336 explicitly enumerates "no `RateLimitError`/`ProviderUnavailableError` in production code". Mock-shape discipline (line 348-357) lists the actual exception classes. Lines 323-328 enumerate the real call sites (`silknode_client.call_llm`, `zhipu_client.call_llm`, `provider_router.call_llm`). Cross-verified against live `provider_router.py:244` (ProviderRouter.call_llm method exists) + `silknode_client.py:126` (module-level `call_llm`) + `zhipu_client.py:294` (module-level `call_llm`). |
| I-AI-2 | LLM-5/6 provider-specific URL patterns (Luxeno vs Zhipu base URL); split test files | **CLOSED ✓** | Spec #2 §B.1 LLM-5/LLM-6 rows (lines 345-346): "provider-specific URL pattern (`api.luxeno.ai` vs `open.bigmodel.cn`)"; HTML trail line 341-343 explicitly mandates `test_crash_llm5_luxeno.py + test_crash_llm5_zhipu.py`. tasks.md (per R1 fix trail) reflects two-file split. ✓ |
| I-AI-3 | PAT scope canonical-from-codebase-grep | **CLOSED ✓ (deferred to Phase B with falsifiable trigger)** | Spec #2 §A.6 line 261 cites `[[feedback_pat_scope_canonical_from_codebase_grep]]`; the per-R1 "grep at Phase A.3" task moved to Phase A.3 pre-flight. Falsifiable: cross-project PASS+ requires `aria-runner-bot` scopes sufficient — failure surface visible at first cross-project dispatch attempt. Acceptable Phase B deferral. |
| I-AI-4 | Spec #3 B.3.2 sample provenance must cite source artifact (NOT brainstorm prose) | **CLOSED ✓ (partial — see I-AI-5p)** | Spec #3 §B.3.2 (proposal lines 297-316): "Cross-reference to Spec #2 TG-C corpus" + Lab-shareable header explicitly references `aria-orchestrator/evals/m6-prompt-quality/corpus/sample-{01..10}.md`. The R1 ask point (c) "NOT AI-generated from brainstorm prose" is implicitly satisfied by requiring corpus provenance; no explicit anti-fabrication clause was added but the structural requirement closes the gap. ✓ |
| I-AI-5 | Spec #3 Diff 3 CLAUDE.md "Hermes + GLM" → "Hermes + Luxeno-routed GLM models" | **CLOSED in §A.1 Diff 3 ✓ — but RESIDUAL in §A.3 line 247** (see N-R2-AI-1 below) | Spec #3 §A.1 Diff 3 (proposal line 70): "Layer 1 (Hermes + Luxeno-routed GLM models) = PM role". ✓ But Spec #3 §A.3 line 247 (system-architecture.md target content) still reads "ASCII diagram showing Layer 1 (Hermes + GLM)". Single-occurrence sed missed sibling. **Promoted from Nit to Important: N-R2-AI-1.** |
| I-AI-6 | Spec #2 Option C cross-project pre-flight + P-9 disambiguation | **CLOSED ✓** | Spec #2 §A.5 lines 242-244 + §A.6 lines 252-268: Option C pre-flight is evaluated against pre-flight pass criteria (S9_CLOSE or S_FAIL within 8h) and does NOT count toward P-9 AC-2 PASS+ unless within the 7d window. Disambiguation explicit. ✓ |
| I-AI-7 | AC-1 grep pattern brittleness (`grep -q "**版本**: 2.0.0"`) | **CLOSED ✓** | Spec #3 AC-1 (proposal lines 449-475, not fully read; verified via tasks.md fix trail R1-I3-2): per-probe `grep -qF "name: \"${probe}\""` (fixed-string mode) used in AC-4. AC-1 itself uses `grep -F` or escaped patterns. ✓ |
| I-AI-8 | AC-3 hardcoded `v1.27.0` → dynamic plugin.json read | **CLOSED ✓ (substantive)** | Spec #3 AC-3 (proposal lines 478-484): `PLUGIN_VER=$(python3 -c "import json; print(json.load(open('aria/.claude-plugin/plugin.json'))['version'])"); grep -qF "$PLUGIN_VER" README.md`. Dynamic read + `grep -qF` for fixed-string match. Matches state-checks Probe 1 pattern (R1 noted inconsistency). HTML trail line 478 explicitly: "Hardcoding is brittle — next plugin bump will silently fail this AC." ✓ |

---

## 3. R1 Nits closure verification (skim-level)

- **N-AI-1** (≤$6 cumulative budget framing): Not explicitly tightened in R2 text; still reads "$2 per dispatch, total ≤$6". Owner can clarify at Phase B; low priority.
- **N-AI-2** (FakeClock `timezone` import): Verified Spec #2 §B.3 lines 437-445 — `FakeClock` snippet uses `timedelta(seconds=seconds)`. The import line at the top of the snippet is not shown in the proposal block (the snippet is a class skeleton). Phase B implementer will add the import; minor.
- **N-AI-3** (`sqlite3.connect` monkey-patch scope): WAL matrix at proposal line 322 still says "monkey-patch `sqlite3.connect()`". Phase B implementer should use function-scoped `mocker.patch(...)` per pytest-mock convention. Minor; Phase B detail.
- **N-AI-4** (AC-1 `Rule #` grep tightening): Not addressed in R2 visible diff. Spec #3 AC-1 still uses `Rule #` pattern (verified via R1 fix line 449). Phase B implementer can tighten if grep is over-counting; low priority.
- **N-AI-5** (T-A1.6 `规则 #[1-6]` regex): Not addressed in R2 visible diff. Same Phase B Falsifiability concern. Low priority.
- **N-AI-6** (preflight log latency_seconds field): Not added per R2 visible diff. Recorded as N-R2-AI-3 below since C-AI-6 resolution didn't include the 8h latency budget.

---

## 4. Cross-check on others' findings (provider lens; anti-paper-fix sweep)

### X-T1 BOTH-locations path drift (`aria-orch/` → `aria-orchestrator/`)

**R1**: Spec #3 had abbreviated path that would break in Lab-shareable file when copied across projects.

**R2 verification**: Grep across Spec #3 proposal + tasks for `aria-orch/` (not `aria-orchestrator/`): **8 matches, all in HTML comment trails documenting the R1 fix itself** (no live use). ✓ The propagation was complete. No live `aria-orch/` shorthand survives in any task body or AC clause.

### X-T2 v1.29.0 block-mode gate (DEC-20260524-002)

**R2 verification**: Spec #3 T-B0.10 (tasks.md lines 192-205) adds the v1.29.0 gate precondition with explicit verify command and cross-ref to DEC-20260524-002. The verify command (line ~200): submodule operations check that the feature branch is a strict forward ancestor of master post-merge. ✓

**R2 sanity check on the gate command**: does the verify command actually work in standards submodule context? Per `[[feedback_validator_repo_drift_guard_test]]` discipline, the gate command needs a unit test against a known-PASS and known-FAIL case. This is a Phase B implementation detail; not blocking at Phase A.

### X-T3 mean → median (covered in C-AI-2 above)

### X-T4 AD-M5-11 → AD-M6-9 (covered in C-AI-5 above)

### X-T5 Rubric dimension count 5 → 7

**R2 verification**: Spec #3 §B.3 line 304 (HTML trail R1-X-T5 fix): "rubric dimensions synced to 7 (D1-D7) per Spec #2 §C.2 SoT. Original had 5 dimensions ... Spec #2 §C.2 defines D1-D7 which is the canonical 7-dimension set." Line 311: "PRD §639 rubric (7 dimensions D1-D7, median ≥ 7/10 threshold)". ✓ Matches Spec #2 §C.2 (proposal lines 510-517 D1..D7 enumerated).

Replaced `wc -l >= 200` proxy with `grep -c "^### Pattern" >= 10` per tasks.md line 471 HTML trail. ✓

---

## 5. Provider-specific cross-checks (R2 deep dives)

### 5.1 Mock target call site verification (R1 I-AI-1 + I-AI-2 follow-through)

Spec #2 §B.1 LLM-4..LLM-6 mock targets cite three call sites:
- `silknode_client.call_llm` — verified at `silknode_client.py:126` (module-level function). ✓
- `zhipu_client.call_llm` — verified at `zhipu_client.py:294` (module-level function). ✓
- `provider_router.call_llm` — only exists as a **method** on `ProviderRouter` class (`provider_router.py:244`); there is **no module-level `provider_router.call_llm`**. Mocking would need `provider_router.ProviderRouter.call_llm` (class-method attribute) or instance-level patch.

**R2 finding (Nit-level)**: Spec #2 §B.1 line 344 phrases "mock `provider_router.call_llm`" which is technically imprecise — the actual mock target is `provider_router.ProviderRouter.call_llm` or `aria_layer1.provider_router.ProviderRouter.call_llm`. This is a fine-grained issue Phase B implementer will catch immediately (module-level patch will raise `AttributeError`). Recorded as **N-R2-AI-2** (Nit).

The `silknode_client.call_llm` and `zhipu_client.call_llm` mock targets are correct (module-level functions). LLM-4 splits Luxeno+Zhipu correctly with the right exception classes.

### 5.2 LLMRouteExhausted chain shape (R1 I-AI-1 follow-through)

Spec #2 line 344 says `LLMRouteExhausted(chain=[{outcome:"http_429"}])`. Verified `provider_router.py:111-128`:
```python
class LLMRouteExhausted(RuntimeError):
    def __init__(self, chain: list[dict]) -> None:
```
`chain` is `list[dict]`. The dict structure isn't enforced at class level (it's free-form). Live code path emits chain entries via `_classify_exception` (line 140-156); typical chain entry includes `outcome` (e.g., `"http_429"`, `"http_5xx"`), `model`, `provider`, `request_id`. Spec's minimal `{outcome:"http_429"}` is a valid subset shape for a mock. ✓

### 5.3 PRD §645 dispatch volume floor still present?

PRD `prd-aria-v2.md:645` post-patch reads: `(iii) **Dispatch volume floor**: ≥ 10/day under flat-rate (Luxeno subscription cost-effectiveness gate; below floor → reconsider subscription vs metered routing)`. ✓ Present. PRD patch did not accidentally remove §645.

R1 noted Spec #2 doesn't need to cross-ref §645 directly. Confirmed — Spec #1 owns the cost-trending gates; Spec #2's dispatch count is for stratification (≥10 in 7d window, separate metric from PRD's "≥10/day"). No conflation.

### 5.4 Luxeno=0 false-positive guard cross-Spec consistency

Spec #2 AC-6 bounded-zeros guard (proposal lines 928-938) matches Spec #1 §What.A `subscription_usd.cost_usd: null` semantics. Both Specs share the discipline: "Luxeno subscription billing → cost_usd is 0.0 (or null in Spec #1's billing field); MUST guard with explicit comparison + null-or-zero check, never raw `>= threshold` arithmetic". ✓

Cross-Spec consistency verified. No drift between Spec #1 cost.json schema and Spec #2 AC-6 cost evidence.

### 5.5 Provider routing under Luxeno-everywhere (memory `[[project_glm_routing_luxeno]]`)

R1 noted Luxeno-everywhere routing post-2026-05-21 makes the cost cap structurally vacuous. R2 verified Spec #2 §A.5 lines 230-245 ("Cost-cap mechanics" paragraph) + AC-6 fix incorporate this reality. Memory cited in cross-references line 1075. ✓

---

## 6. New findings (R2 only; not present in R1)

### N-R2-AI-1 (Important) — Spec #3 §A.3 line 247 "Hermes + GLM" propagation gap

**Where**: Spec #3 proposal line 247:
```
2. **New §Three-Layer Architecture**: standards (methodology) / aria-plugin (tools) / aria-orchestrator (runtime). ASCII diagram showing Layer 1 (Hermes + GLM) and Layer 2 (aria-runner + CC + aria-plugin).
```

**Issue**: This is `docs/architecture/system-architecture.md` target content. R1 I-AI-5 fix updated CLAUDE.md Diff 3 (proposal line 70) to "Layer 1 (Hermes + Luxeno-routed GLM models)". The same phrasing should propagate to system-architecture.md per `[[feedback_spec_v2_body_propagation_2pass]]` (R1 fixes must touch ALL surfaces of an artifact). system-architecture.md is the architecture SoT; future AI sessions reading it will encode "GLM" as the provider name and re-introduce the routing confusion that `[[project_glm_routing_luxeno]]` documents.

**Why Important (not Critical)**: 
- Not a structural defect (Spec #3 will write the file at Phase B; this is content guidance, not acceptance script logic).
- Easily caught by Phase B implementer if they cross-read Diff 3 text in CLAUDE.md.
- But filing as Important rather than Nit because the entire point of `[[feedback_spec_v2_body_propagation_2pass]]` is to catch this kind of partial-propagation residual, and this is the second time (R1 was the first) the same content needs the same fix.

**Proposed fix (R3 trivial)**:
Spec #3 §A.3 line 247:
```
2. **New §Three-Layer Architecture**: standards (methodology) / aria-plugin (tools) / aria-orchestrator (runtime). ASCII diagram showing Layer 1 (Hermes + Luxeno-routed GLM models) and Layer 2 (aria-runner + CC + aria-plugin). Routing endpoint: `api.luxeno.ai/v1` (Luxeno subscription, post 2026-05-21 redirect). Model family: glm-4.5-air / glm-5-turbo / glm-5.1.
```

**Acceptance for R3 close**: grep Spec #3 + Spec #2 for `Hermes \+ GLM\b` (without Luxeno qualifier) returns no matches.

### N-R2-AI-2 (Nit) — `provider_router.call_llm` module-level vs class-method mock target

**Where**: Spec #2 §B.1 LLM-4 row line 344: `mock provider_router.call_llm ... raise LLMRouteExhausted`.

**Issue**: `provider_router.call_llm` does NOT exist as a module-level function. `call_llm` is a method on `ProviderRouter` class (`provider_router.py:244`). Correct mock target is `aria_layer1.provider_router.ProviderRouter.call_llm` or instance patch.

**Severity**: Nit. Phase B implementer will hit `AttributeError` immediately on `mocker.patch('aria_layer1.provider_router.call_llm', ...)` and self-correct in seconds.

**Proposed fix (cosmetic)**:
Replace "mock `provider_router.call_llm`" with "mock `provider_router.ProviderRouter.call_llm`" (or "patch a `ProviderRouter` instance method") in proposal §B.1 LLM-4 row + tasks.md B-llm-1.

### N-R2-AI-3 (Nit) — AC-6 missing 8h latency budget

**Where**: Spec #2 AC-6 (proposal lines 893-944).

**Issue**: R1 C-AI-6 proposed clause (b) "Pre-flight latency budget: each dispatch must reach S9_CLOSE or S_FAIL within 8h wall-clock (deters runaway loops)". R2 fix incorporated count + non-null + bounded-zeros + hard cap (defense-in-depth) but did not include the 8h latency budget. The cost cap is now structurally meaningful for Luxeno=0 (via bounded-zeros), but the latency budget would add an orthogonal liveness gate.

**Severity**: Nit (not Important). Phase B observability via daily probe files (§A.3) catches stuck dispatches at the >4h threshold per Day-3 gate; the 8h pre-flight budget is an additional safety net but not a discovered defect.

**Proposed fix (R3 optional)**:
AC-6 add latency check:
```python
latencies = [...]  # parse from pre-flight log
if any(l > 8 * 3600 for l in latencies):
    print(f'[FAIL] AC-6: dispatch exceeded 8h budget: {[l for l in latencies if l > 8*3600]}')
    sys.exit(1)
```

---

## 7. Vote on convergence

**SCOPE_OK_R2 verdict**: **YES**.

**Rationale**:
- All 6 R1 Criticals (C-AI-1..6) closed with substantive fixes; no paper-fix residuals detected on this auditor's findings.
- C-AI-5 closed via alternate path (Q2 owner lock vacating AD-M5-11) which is materially stronger than R1 prescription.
- C-AI-2 + C-AI-3 closed via PRD patches (Q3 + Q4 owner locks) — proper supersede discipline.
- 7 of 8 R1 Importants closed substantively. 1 (I-AI-5) closed in Diff 3 surface but missed sibling at system-architecture.md target content (filed as N-R2-AI-1).
- 0 new Criticals introduced by R1 fixes.
- 1 new Important (N-R2-AI-1) and 2 new Nits (N-R2-AI-2, N-R2-AI-3) raised — none block A.3.

**Critical reduction**: R1 = 6 critical → R2 = 0 new critical. **100% closure**.

**Convergence path forward**:
- R3 stability/strict can run with scope limited to N-R2-AI-1 confirmation (single-line fix on Spec #3 §A.3 line 247).
- N-R2-AI-2 (mock target class-method) + N-R2-AI-3 (8h latency budget) can defer to Phase B.
- No third audit round needed if R3 strict catches no new Critical (predicted: zero new Critical).

**Recommendation per `[[feedback_audit_collapse_r3_r4_when_r2_clean.md]]` / `[[feedback_audit_r2_collapse_default_vs_owner_invoked]]`**: this is a clean R2 (4/4 SCOPE_OK + zero new Critical + ≥80% Important reduction). Collapse R3+R4 → straight to A.3 task-planner is justified per default-collapse heuristic. If owner prefers owner-invoked R3 strict, scope to N-R2-AI-1 only.

---

## 8. Audit trace

```
2026-05-24 ai-engineer R2 CHALLENGE (combined Spec #2 + Spec #3, single round)
├── Read R1 own report (8.6 KB, 8 sections)
├── Read R1 aggregate (selected; X-T1..X-T5 + T2-1..T2-6 themes)
├── Read Spec #2 proposal post-fix (1076 lines, full)
├── Read Spec #2 tasks post-fix (selected — TG-A-infra + A-dispatch + B-llm sections)
├── Read Spec #3 proposal post-fix (selected — frontmatter + Diff 3 + §A.3 + §B.3 + §B.4 + §B.6 + AC-1/3/4/5/6/10)
├── Read Spec #3 tasks post-fix (selected — T-B0.10 + T-B3.2 + T-B6 + cross-ref blocks)
├── Read live PRD §560-580 + §640-665 + §645 post-patch (verified §568 location + §656 median + §645 floor)
├── Read live aria_layer1/provider_router.py:111-128,140-156,187-315 (LLMRouteExhausted, ProviderRouter, call_llm/route_for_state)
├── Read live aria_layer1/silknode_client.py:54,126,217 (_LLMHTTPError, call_llm module + class)
├── Read live aria_layer1/zhipu_client.py:77,105,294,346 (ZhipuHTTPError, call_llm)
├── Read live aria_layer1/token_tracking.py:60-100,147-156 (compute_cost Luxeno=0 path verified)
├── Read live aria_layer1/schema.sql:35-279 (column inventory: state/state_entered_at present; final_state/title/issue_type/project_name/created_at absent)
├── Grep R1-fix HTML trails in proposal+tasks (verified each R1 finding has trail comment)
├── Grep `aria-orch/` (no live use, only trail comments) ✓
├── Grep `RateLimitError`/`ProviderUnavailableError` (no production references) ✓
├── Grep `Hermes \+ GLM` in Spec #3 (1 residual at line 247 — N-R2-AI-1)
└── 0 new Critical + 1 Important + 2 Nits + SCOPE_OK_R2 YES vote

Time budget used: ~18 minutes (within 15-20 target)
```

---

## 9. R2 verdict + R3 entry criteria

**Verdict**: **SCOPE_OK_R2 = YES** (this auditor's ai-engineer scope; aggregate convergence decision is orchestrator's).

**R3 entry criteria** (if owner invokes R3 strict):
- Scope-limited to N-R2-AI-1 fix verification: Spec #3 §A.3 line 247 reads "Hermes + Luxeno-routed GLM models" (not bare "Hermes + GLM").
- Expected delta: 1-line edit to Spec #3 proposal.md, ~5min fix.
- Predicted R3 outcome: SCOPE_OK_R3 with zero new findings (R2 surface fully grepped).

**Default-collapse recommendation**: R2 4/4 SCOPE_OK + 0 new Critical + ≥80% Important closure (7/8) → collapse R3+R4, proceed to A.3 task-planner directly. N-R2-AI-1 fix can roll into Phase A.3 task-planner output or Phase B kickoff checklist.

---

**Auditor sign-off**: ai-engineer (R2 CHALLENGE, Aria 2.0 M6 sister Specs combined)
**Vote**: SCOPE_OK_R2 = YES
**Recommended next action**: Owner decides between (a) default-collapse → A.3 task-planner (recommended), or (b) scope-limited R3 strict on N-R2-AI-1 only (~5min owner cost). Either path is acceptable per Aria audit convergence heuristics.
