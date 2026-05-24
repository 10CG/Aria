# Post_Spec R2 Audit — tech-lead-critic (CHALLENGE position) — aria-2.0-m6-cost-acceptance

> **Auditor**: tech-lead-critic (R2 CHALLENGE seat)
> **Round**: R2 (Phase A.2 post_spec, CHALLENGE mode)
> **Spec**: aria-2.0-m6-cost-acceptance (Spec #1 of M6 four sub-Specs)
> **Spec status at audit time**: Draft, R1 fixes applied (commit `0d4a317`)
> **Audit baseline**: R1 commit `6e58b75` → R1-fix commit `0d4a317` (8-file diff, +2363/-176)
> **R1 verdict baseline (mine)**: NEEDS_FIX — 3 Critical + 5 Important + 4 minor + 5 obs
> **DEC reference**: DEC-20260524-001
> **R2 Verdict**: **SCOPE_OK_R2 — convergence reached with 1 new Critical (PATH-RESOLUTION REGRESSION, MUST FIX before Phase A.3)**

---

## Executive summary (3 lines)

R1 Critical findings substantively closed (C1 schema column, C2 Luxeno dual-layer, C3 path discipline at task-level). C3 fix introduced a **NEW Critical: REPO_ROOT path expression is wrong** (`Path(__file__).parent.parent.parent` resolves to `/home/dev/Aria/`, NOT `aria-orchestrator/`). Spec body §Why narrative for C3 is paper-light (substantive AC layer, but the originally-flagged "Attributing cost_usd=0 is a silent false-positive" sentence retained verbatim instead of reframing per R1 suggestion); not blocking — AC-3 carries the truth. Cross-Spec coordination (Q4 AD-M6-1/2/3) landed cleanly in both DEC and Spec frontmatter; bidirectional cross-ref verified.

---

## R1 finding closure verification

### tl C-tl-1 (validate-m6-handoff.py grep targets) — **SUBSTANTIVE (with regression)**

Tasks T5.2–T5.6 now cite the canonical paths verbatim (`REPO_ROOT / "hermes-extensions/aria-layer1/aria_layer1/<file>"`). Proposal §What F lines 232-236 mirror the path-construction pattern. C-tl-1 narrowly closed.

**BUT**: introduces **NEW Critical C-tl-N1** — see §New Critical below. The path expression `REPO_ROOT = Path(__file__).parent.parent.parent` is wrong; sibling `validate-m5-handoff.py` uses `HERE.parent` (single level, REPO_ROOT = `aria-orchestrator/`). A Phase B implementer reading the Spec literally will create a `validate-m6-handoff.py` whose REPO_ROOT resolves to `/home/dev/Aria/` (project root), then resolve `REPO_ROOT / "hermes-extensions"` to `/home/dev/Aria/hermes-extensions/` — **a non-existent path** — and produce silent FileNotFoundError or empty-grep PASS, exactly the failure mode C-tl-1 was supposed to prevent. This is the `[[feedback_paper_fix_antipattern]]` shape: text was rewritten but the path arithmetic was not actually verified against the sibling.

### tl C-tl-2 (Zhipu cost SQL filter column) — **SUBSTANTIVE**

All callsites converted: proposal §How diagram, §What A field semantics block, §What D.iii volume floor SQL, AC-3 verification query, Dependencies row — all 9 occurrences now use `provider_cost_model='metered'` or `'subscription_flat'`. tasks.md T1.1 / T1.2 / T3.7 align. Inline `<!-- R1-C1 fix: -->` traces left for audit traceability per `[[feedback_audit_driven_fix_conventions]]`. Effort baseline accounting: SQL is now slightly more explicit (~10 extra characters per query) — does NOT materially shift T1.x estimate. Sane.

### tl C-tl-3 (AC-3 evidence + §Why narrative) — **SUBSTANTIVE at AC layer, PARTIAL at §Why**

**AC layer (lines 461-481)**: properly two-layered. "Layer 1 — Code path (primary)" verifies the snapshot script's null guard via T3.5 unit test (mock `cost_usd=null` → `feishu_send` NOT called for Luxeno). "Layer 2 — Schema invariant note" explicitly states `token_cost_usd REAL NOT NULL DEFAULT 0.0` per schema.sql:101 and clarifies the cost.json `null` is a **snapshot-script transformation** distinct from the schema-stored 0.0. This is the elegant fix I recommended. Architecture-clean.

**§Why narrative (line 34)**: original sentence "Attributing `cost_usd=0` per dispatch is a silent false-positive that would prevent alarms from firing" retained verbatim. R1 suggestion was to rewrite as "the existing dispatches.token_cost_usd column contains 0.0 for Luxeno rows by M2 T10 contract; merging these into cost.json metered_usd would understate metered cost". Current text frames the failure mode prospectively (hypothetical attribution), not as describing the existing schema state. **This is the anti-paper-fix discipline trigger**: I explicitly flagged this prose; the patch did not invert the narrative — it added correct AC text below, but left the upstream §Why prose intact.

Verdict on C-tl-3: **PARTIAL** — substantive at the binary-falsifiable evidence layer (which is what gates Phase B), light-touch at the §Why narrative layer (cosmetic, not Phase B blocking). Flagging as **I-tl-2-residual** below, not as blocker.

### tl I-tl-1 (.aria/config.json location) — **SUBSTANTIVE**

§What B opening sentence specifies `/home/dev/Aria/.aria/config.json` (project-root); tasks.md T2.1 same; Dependencies row §What B / config path consistent. Phase B implementer has no path ambiguity.

### tl I-tl-2 (`check_cost_measurement_method_enum` helper-without-caller) — **SUBSTANTIVE**

§What F lines 257-276 now: field is treated as optional in M6 (warning-only if absent) + advisory promotion to FAIL in M7+. Additional zhipu_client.py `_post_chat` no-`cost_usd`-key assertion grounds the validator in a real production code path. The validator now has TWO real callers (cost.json field check + zhipu_client.py contract enforcement). `[[feedback_scaffold_helpers_drift_without_callers]]` violation closed.

### tl I-tl-3 (Cross-Spec DAG P-15) — **PARTIAL**

§Dependencies adds Spec #2 downstream row (gates on AC-7); §Cross-references explicitly lists sibling Specs with relationship notes. **However**: Spec #4 release-closeout RED gate consumer relationship is mentioned in DEC §2 Spec #4 scope but NOT cross-referenced from Spec #1's §Dependencies. If Spec #1 renames `m6.cost_thresholds.zhipu_30d_usd` during Phase B (low probability but possible), Spec #4 would silently break. This is a forward-binding contract leak. Flagging as **I-tl-3-residual** but non-blocking (Spec #4 isn't drafted yet; the field name is locked by AC-4 evidence Python literal so a rename would also break Spec #1's own AC).

### tl I-tl-4 (freshness_ts ISO format) — **SUBSTANTIVE**

§What A line 106 mandates `datetime.now(timezone.utc).isoformat()` (produces `+00:00`); AC-1 evidence Python (lines 420-435) uses `datetime.fromisoformat(d['freshness_ts'])` + `datetime.now(timezone.utc)` (tz-aware throughout) + tzinfo assert + `age < 0` clock-skew guard + strict `age < 86400` boundary. All four R1 sub-failure modes addressed.

### tl I-tl-5 (T7.1 PRD verify mis-scoped) — **NOT FIXED**

tasks.md T7.1 (lines 293-295) still reads as a verify task with the original wording ("Verify PRD §M6 lines 638-646 already reflect... if not yet patched, note for owner action"). My R1 suggested rewriting to a grep-based drift sentinel. Was not addressed in the R1 fix pass. Non-blocking — the task is a 0.5h no-op at worst; not Phase B path. Defer to D.3 polish or close as minor here.

### Minors m-tl-1..m-tl-4 — partially closed

- m-tl-1 (today vs today-1 ambiguity): §What G + AC-7 lines 295-302 now lock "Today" as `datetime.now(timezone.utc).date()` and "most recent date >= today - 1 day". Closed.
- m-tl-2 (action_url helper-without-caller): still listed in §What D card fields; no clarification of what URL. Open (minor).
- m-tl-3 (AD-M6-1 punt language premature): AD table reads "Python (same as aria_layer1 runtime; enables unittest mocking)" — language decided inline. Closed.
- m-tl-4 (m5-handoff.yaml stable anchor): not addressed. Open (cosmetic).

### Observations O-tl-1..O-tl-5 — informational, no action expected

O-tl-1 (extract AC evidence patterns to standards/) deferred. O-tl-4 (effort baseline) revised ~10h → ~12h per `[[feedback_phase_budget_compounding]]` — math: 38 leaf tasks at ~18min each = 11.4h ≈ 12h. Sane. O-tl-5 (validate-m6-handoff.py self-referencing contract) not addressed; deferral OK.

---

## Architecture-level R2 inspection (new lens)

### Sequencing / boundary integrity

§How "Technical approach" diagram (lines 360-396) cleanly partitions cost data pipeline (dispatches → metered_usd ∪ subscription_usd → cost.json → check-m6-cost-acceptance.py / validate-m6-handoff.py). Alarm path partition (Feishu via `ARIA_FEISHU_WEBHOOK_URL`) explicit. Volume floor partition (D.iii subscription_flat 7-day average) independent of 80% cost alarm. Three concerns are properly orthogonalized — Phase B can implement T-schema, T-alarm, T-validate in parallel with declared T-acceptance dependency only on T-schema + T-config. Ordering dependency section in tasks.md (lines 304-320) consistent with this DAG.

### Phase B handoff readiness

Read tasks.md as if I am the Phase B implementer. Open questions:
- Q-prov: **`SUM(token_cost_usd)` cast handling**: T1.5 covers stringified cost_usd from API path, but **what if the SQLite aggregate is `None` (zero matching rows)?** T1.4 mentions "zero Zhipu rows in fixture → assert `metered_usd.cost_usd == 0.0`" — implicitly the snapshot script does `float(cursor.fetchone()[0] or 0.0)` (proposal line 105 explicit). OK.
- Q-cron: T3.6 says "add or extend existing `aria-layer1-cron` job (or create new `aria-layer1-cost-sentinel` periodic job)". This is a binary decision deferred to Phase B with no AD slot. AD-M6-1 says "integrated with existing aria-layer1-cron as a new sub-command" — but T3.6 still gives the implementer the "extend OR create new" choice. **Minor ambiguity**, flag as **N1-minor**.
- Q-script-exec: Acceptance script file is `aria-orchestrator/acceptance/check-m6-cost-acceptance.py` — the **directory does not exist yet** (`find aria-orchestrator -maxdepth 2 -type d` confirms). Spec does not mention `mkdir -p` step. Phase B implementer will trivially handle this, but it's worth a **N3-trivial** mention.
- Q-py-interpreter: AC evidence shell commands use `python3` consistently (proposal line 528, 544, 561, 570, 581; tasks.md T5.1 CLI). Aria-layer1 container runtime is Python 3.9+ per §Constraints "Platform" line 351. Consistent. No `chmod +x` mentioned — but the AC examples invoke `python3 path/to/script.py`, so executable bit is not load-bearing. Worth a one-line note in T1.1 / T4.1 to clarify; trivial.

### §Risks R-M6-1..R-M6-6 — relevance + completeness

R-M6-1 through R-M6-6 all remain relevant post-fix. NEW risks surfaced by R1 fixes that should be added:
- **R-M6-7 candidate**: REPO_ROOT path expression error in validate-m6-handoff.py would silently produce PASS on grep targets that file-not-found. Already partially covered by R-M6-4 ("grep patterns stale") — could extend that risk to include "REPO_ROOT misresolution". Defer to D.3 polish.
- **R-M6-8 candidate (NEW Critical surface)**: SQLite aggregate return type drift. `SUM(token_cost_usd)` returns `Decimal` in some SQLite Python bindings and `float` in others; T1.5 covers stringified type but not Decimal type. Out of scope flag — float cast handles all numeric coercions. No new risk needed.

### Cross-Spec coordination (Q4) — bidirectional verify

**Forward direction (DEC → Spec #1 frontmatter)**: DEC-20260524-001 §2 lines 125-129 explicitly reserve AD-M6-1/2/3 for Spec #1 with rationale ("Spec #1 ships first, claims earliest AD slots"). Cross-Spec coordination enforced by state-scanner audit-engine R1+R2 cross-ref check.

**Reverse direction (Spec #1 → DEC reference)**: Spec #1 frontmatter line 17-18 declares "AD allocation reservation: AD-M6-1 / AD-M6-2 / AD-M6-3 are reserved for **this Spec #1** only. Specs #2 / #3 / #4 must start from AD-M6-4 onwards. (per Q4, 2026-05-24)". Cleanly cross-linked.

Multi-terminal collision risk (parallel dev-claude2 drafting Spec #2/#3/#4): `aria-orchestrator/docs/architecture-decisions.md` is the AD slot file. tasks.md T6.1 / T6.2 add AD-M6-1 / AD-M6-2. If dev-claude2 simultaneously drafts Spec #2 and tries to write AD-M6-4, the file would have concurrent appends — a merge conflict, not a silent collision. Track G+ coordinator (state-scanner Phase 1.16/1.17) would surface this on next status check. Acceptable.

Other potential collisions: validate-m6-handoff.py file itself — Spec #2 would extend the same script with new check functions. **Potential issue**: Spec #2 proposal hasn't landed yet, so we cannot verify the extension pattern is forward-compatible. Recommend flagging in §Risks R-M6-4: "Phase A.1 for Spec #2 must verify the validate-m6-handoff.py CLI surface designed in Spec #1 T5.1 supports new --check-* flags additively." Minor enhancement; non-blocking.

### Plugin version compat (aria-plugin v1.27.0)

Spec #1 runs inside aria-orchestrator (not aria-plugin). Plugin runtime not on critical path — Spec #1 ships Python scripts under aria-orchestrator/acceptance/ and aria-orchestrator/docs/ that execute via cron (Nomad job) + manual invocation. **No plugin upgrade needed**. v1.27.0 capable.

### Effort baseline accounting (~10h → ~12h)

R1 deltas:
- D group +1h (T3.7/T3.8 volume floor tasks)
- E group +0.5h (T4.5/T4.6 infra failure unit tests)
- F group +0.5h (T5.11 pricing freshness check)
- Sub-total +2h

Net: 10h → 12h (~13h with R1 review integration overhead per `[[feedback_phase_budget_compounding]]`). Task count: 32 → 38 leaf tasks. Math: 38 × ~18min = 11.4h ≈ 12h. **Math is sound. No hidden +3-4h cascade.**

Per `[[feedback_phase_budget_compounding]]` empirical record: single-phase Spec budgets at this size actualize at ×0.5-0.7 of estimate = ~6-9h AI time. Aligns with M5 Phase 1 (~13h vs 25h, ×0.52). No under-estimation cascade risk.

---

## New Critical (R2-surfaced; gates Phase A.3)

### **C-tl-N1 — REPO_ROOT path expression error in proposal + tasks.md** *(BLOCKING for Phase B)*

- **Location**: `proposal.md` line 232 (§What F: `REPO_ROOT = Path(__file__).parent.parent.parent`) + `tasks.md` line 33 (T1.1) + line 190 (T5.1).
- **Why critical**: The R1 fix says "mirrors `validate-m5-handoff.py::REPO_ROOT` resolution" — but the sibling actually uses **`HERE = Path(__file__).resolve().parent`** then **`REPO_ROOT = HERE.parent`** (single `.parent`, REPO_ROOT = `aria-orchestrator/`). The Spec's expression `Path(__file__).parent.parent.parent` is THREE levels up: from `aria-orchestrator/docs/validate-m6-handoff.py` that resolves to `/home/dev/Aria/` (project root). Then `REPO_ROOT / "hermes-extensions"` becomes `/home/dev/Aria/hermes-extensions/` — does not exist. Phase B implementer who reads tasks.md literally will produce code that **either FileNotFoundError on first run OR silently empty-grep-PASS** — the exact failure mode C-tl-1 was supposed to prevent. This is `[[feedback_paper_fix_antipattern]]` in textbook form: text was changed, semantics were not verified.
- **Verification evidence**: `grep -n "REPO_ROOT" aria-orchestrator/docs/validate-m5-handoff.py` line 41: `REPO_ROOT = HERE.parent  # aria-orchestrator/`. The comment is explicit. Spec must mirror this expression verbatim.
- **Suggested fix** (2-pass per `[[feedback_spec_v2_body_propagation_2pass]]`):
  1. **proposal.md line 232**: Change `REPO_ROOT = Path(__file__).parent.parent.parent (mirrors validate-m5-handoff.py::REPO_ROOT resolution)` to `HERE = Path(__file__).resolve().parent; REPO_ROOT = HERE.parent (mirrors validate-m5-handoff.py lines 40-41, REPO_ROOT = aria-orchestrator/)`.
  2. **tasks.md line 33**: Same change in T1.1 description.
  3. **tasks.md line 190**: Same change in T5.1 description.
  4. Add T5.9-bis unit assert: `assert REPO_ROOT.name == 'aria-orchestrator'` to fail-fast if the path expression is wrong in Phase B implementation. This is the canonical instance test pattern from `[[feedback_validator_repo_drift_guard_test]]`.
- **Severity**: CRITICAL (blocks Phase B T5.1-T5.6 + T1.1 — every grep target resolves wrong).

---

## Residual Important (non-blocking R2 verdict)

### I-tl-2-residual — §Why narrative not inverted (C-tl-3 partial)

- **Location**: `proposal.md` line 34 (§Why bullet 1).
- **Issue**: R1 explicitly flagged this sentence as factually inverted. R1 fix updated AC-3 evidence (substantive) but did not edit the §Why narrative (light-touch). Anti-paper-fix discipline trigger satisfied at AC layer (the binary-falsifiable contract is correct), but the §Why narrative remains imprecise.
- **Suggested fix**: Rewrite §Why line 33-34 to: "**Layer 1 (Luxeno)**: flat monthly subscription. The schema stores `token_cost_usd=0.0` per Luxeno dispatch (M2 T10 contract); but cost.json must NOT carry that 0.0 forward as a metered cost — the snapshot script transforms it to `subscription_usd.cost_usd=null` to prevent the Luxeno=0 silent false-positive failure mode (DEC brainstorm R2 ai-CH-3)."
- **Severity**: Important (not Critical) — AC layer is correct; narrative is cosmetic.

### I-tl-3-residual — Spec #4 RED gate consumer not declared in §Dependencies

- **Location**: `proposal.md` §Dependencies (lines 629-637) + §Cross-references "Sibling Specs" (lines 647-650).
- **Issue**: Spec #4 release-closeout consumes `m6.cost_thresholds.{zhipu_30d_usd, luxeno_monthly_usd}` as RED gate evaluation. This forward-binding contract is implicit (per DEC §2 Spec #4 scope) but not declared in Spec #1's Dependencies "Downstream contract" sub-section. If a Phase B Spec #1 implementer renames a threshold key, Spec #4 silently breaks.
- **Mitigation**: AC-4's evidence Python literal (`t['zhipu_30d_usd']`, `t['luxeno_monthly_usd']`) acts as a soft contract anchor — any rename would also break Spec #1's own AC-4, providing implicit guard. So risk is bounded.
- **Suggested fix**: Add to §Dependencies a one-row "Downstream consumers" entry: "Spec #4 `aria-2.0-m6-release-closeout` reads `metered_usd.cost_usd`, `subscription_usd.cost_usd` (null-aware), `freshness_ts`, `m6.cost_thresholds.zhipu_30d_usd`, `m6.cost_thresholds.luxeno_monthly_usd` for RED pre-release gate. Field rename in Phase B requires updating Spec #4 proposal."
- **Severity**: Important (not Critical) — forward-binding has soft mitigation via AC-4.

---

## New Minor / Trivial (R2-surfaced)

- **N1-minor**: T3.6 "extend existing aria-layer1-cron job OR create new aria-layer1-cost-sentinel" — but AD-M6-1 already locks "integrated with existing aria-layer1-cron as new sub-command". Edit T3.6 to remove the "OR create new" option (force consistency with AD-M6-1 decision).
- **N2-trivial**: Spec invokes `python3 aria-orchestrator/acceptance/check-m6-cost-acceptance.py` (cwd-dependent path). On Phase B implementation, ensure script is invoked from project root OR use absolute path. T1.1 should clarify.
- **N3-trivial**: `aria-orchestrator/acceptance/` directory does not exist yet (`find aria-orchestrator -maxdepth 2 -type d` confirms). T1.1 should include `mkdir -p aria-orchestrator/acceptance/` step (or implicit via `Path.mkdir(parents=True, exist_ok=True)` in the snapshot script).
- **N4-trivial**: `.aria/cost-snapshots/` directory also does not exist; snapshot script must create it on first run. T1.1 should mention.

---

## Convergence vote

**SCOPE_OK_R2** with the following gates:

| Item | Status | Phase A.3 gate |
|------|--------|----------------|
| C-tl-1 (grep paths) | SUBSTANTIVE | OK |
| C-tl-2 (SQL column) | SUBSTANTIVE | OK |
| C-tl-3 (AC-3) | SUBSTANTIVE at AC, PARTIAL at §Why | OK (AC carries truth) |
| I-tl-1 / I-tl-2 / I-tl-4 | SUBSTANTIVE | OK |
| I-tl-3 / I-tl-5 / minors | PARTIAL or DEFERRED | OK (non-blocking) |
| Q4 AD-M6-* memo (cross-link both ways) | SUBSTANTIVE | OK |
| Effort baseline (~12h) | SANE | OK |
| Cross-Spec DAG (P-15) | PARTIAL | OK (DAG is constructible from Spec #1 alone) |
| **C-tl-N1 (REPO_ROOT path expression)** | **NEW CRITICAL** | **MUST FIX before Phase A.3** |

**Vote**: **CONVERGED conditional on C-tl-N1 closure** — Phase A.3 may proceed after a single targeted Edit pass (proposal.md line 232 + tasks.md line 33 + line 190) without invoking R3. Per `[[feedback_audit_r2_collapse_default_vs_owner_invoked]]`, default R2 collapse with 1 new Critical of trivial fix scope (single grep-and-replace pattern, no architecture rethink) qualifies as SCOPE_OK_R2 + targeted-patch-then-merge. No need for full R3.

R3 would be appropriate if: (a) C-tl-N1 fix introduces another regression, OR (b) multiple new Critical surfaced (only 1 new). Single targeted Edit is the minimum sufficient response.

---

## Stability heuristic check (per `[[feedback_premerge_iteration_pattern]]`)

R1 → R2 trajectory:
- R1: 11 Critical (aggregate) + 20 Important
- R2 (this report): 0 carry-over Critical (all 3 of mine closed substantively) + 1 new Critical (regression from C3 fix)
- Reduction: 91% on Critical (11 → 1)

Per `[[feedback_premerge_iteration_pattern]]` ≥70% reduction + ≤1 new Critical + scoped fix → R2 collapse is the default verdict. **First-stability-round confidence**: medium — the new Critical is a textbook regression, easy to verify-and-fix. Recommend single Phase A.2.5 micro-pass (Edit + 1-line diff verify) before Phase A.3 kickoff.

---

## What unblocks Phase A.3 from my seat (priority-ordered)

1. **C-tl-N1 patched** (1 Edit, ~5min): proposal.md line 232 + tasks.md line 33 + line 190 — change `Path(__file__).parent.parent.parent` to `HERE = Path(__file__).resolve().parent; REPO_ROOT = HERE.parent` pattern verbatim mirroring `validate-m5-handoff.py:40-41`.
2. **I-tl-2-residual addressed** (1 Edit, ~5min, OPTIONAL): proposal.md §Why line 33-34 reframe to reflect production schema reality (anti-paper-fix discipline cleanup).
3. I-tl-3-residual / N1-N4 / m-tl-2 / m-tl-4 / T7.1 — DEFER to Phase D.3 polish.

After (1) lands, Phase A.3 agent assignment proceeds: backend-architect agent for T-schema / T-config / T-alarm / T-acceptance / T-validate / T-docs / T-prd (single-agent Spec per §Spec drafter handoff in DEC §6 — "backend-architect (10h baseline)" now ~12h).

---

## Memory refs cited

- `[[feedback_audit_convergence_pattern]]` — 5-round convergence model; this Spec at R2 with 1 new Critical of trivial fix scope qualifies for default R2 collapse (per `[[feedback_audit_r2_collapse_default_vs_owner_invoked]]`).
- `[[feedback_premerge_iteration_pattern]]` — R1→R2 91% Critical reduction satisfies stability heuristic; first-stability-round confidence medium.
- `[[feedback_phase_budget_compounding]]` — effort baseline ~12h passes math check (38 leaf × 18min).
- `[[feedback_audit_driven_fix_conventions]]` — Inline R1-C*/R1-I-* traces consistently applied; auditable.
- `[[feedback_paper_fix_antipattern]]` — C-tl-N1 (REPO_ROOT path expression) is textbook example: text rewritten, semantics not verified against sibling.
- `[[feedback_validator_repo_drift_guard_test]]` — recommend adding `assert REPO_ROOT.name == 'aria-orchestrator'` to T5.9 as drift sentinel.
- `[[feedback_spec_v2_body_propagation_2pass]]` — C-tl-N1 fix touches 3 surfaces (1 proposal + 2 tasks); 2-pass discipline applies.

---

## Verdict summary

**SCOPE_OK_R2** with **1 new Critical (C-tl-N1) requiring targeted patch before Phase A.3 kickoff**. R3 not warranted; default R2 collapse applies. After C-tl-N1 patched, this Spec is Phase B-ready from the tech-lead-critic seat: SQL filter columns correct, path discipline correct (post-patch), AC-3 truthful at the binary-falsifiable layer, cross-Spec coordination clean both directions, effort baseline sound, risk register relevant. No architecture-level rethink needed.

**R2 → Phase A.3 entry conditional on**: 5-minute Edit pass on REPO_ROOT expression (3 occurrences) + verification grep confirms 0 remaining `Path(__file__).parent.parent.parent` in proposal.md/tasks.md.
