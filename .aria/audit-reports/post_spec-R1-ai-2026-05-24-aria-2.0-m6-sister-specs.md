# Phase A.2 post_spec R1 — ai-engineer (combined Spec #2 + Spec #3)

> **Date**: 2026-05-24
> **Auditor**: ai-engineer (R1, combined-Spec mode)
> **Specs under review**:
> - Spec #2: `aria-2.0-m6-e2e-resilience` (proposal.md, tasks.md @ HEAD)
> - Spec #3: `aria-2.0-m6-docs` (proposal.md, tasks.md @ HEAD)
> **Verdict**: **NEEDS_FIX (both Specs)** — 6 Critical + 8 Important + 6 Nits
> **Reference Specs/docs read**: Spec #1 proposal (§A schema), brainstorm DEC-20260524-001, PRD §225-243 / §305 / §369 / §381 / §491-553 / §567-568 / §638-656, `token_tracking.py`, `provider_router.py`, `zhipu_pricing.py`, `schema.sql`, `architecture-decisions.md §AD-M5-11`, memory `[[project_glm_routing_luxeno]]` (verified live).
> **Convergence target (R2/R3)**: each Critical resolved with literal text-replacement clause (no advisory language).

---

## 0. TL;DR (one screen)

**Three blocker classes** that ai-engineer specifically owns:

1. **SCHEMA-vs-SQL mismatch in Spec #2 AC-2** — every TG-A SQL query references columns that **do not exist** in the live `dispatches` table (`final_state`, `issue_type`, `project_name`, `title`, `created_at`). Live schema uses `state` (with terminal value `S9_CLOSE`, not `'S9'`). This is a paper-fix antipattern: AC-2 will FAIL on day 1 at `sqlite3.OperationalError: no such column`. ⇒ **C-AI-1** (Spec #2).

2. **PRD §639 average-vs-median contradiction** — PRD verbatim says `10 samples **平均** ≥ 7/10` (mean). Spec #2 AC-5 and Spec #3 §C.2 + tasks.md T-A6 mandate **median** of seven-dimension medians. Mean ≠ median, and they diverge sharply on bimodal scoring. This is a falsifiability gap per `[[feedback_falsifiable_evidence_for_binary_acceptance]]`. ⇒ **C-AI-2** (cross-Spec).

3. **PRD §568 vs Spec #3 §B.4 location conflict on `layer-boundary-contract.md`** — PRD §568 places `layer-boundary-contract.md` in `standards/autonomous/`. Spec #3 §B.4 + Constraint + AD-M5-11 claim put it in `aria-orchestrator/docs/` and cite "km M-km-R2-005" as authority. Spec #3 amends PRD silently without PRD patch (Q-final-1/2 set a precedent that PRD patches are owner-action — this requires one too). ⇒ **C-AI-3** (Spec #3).

Two additional ai-domain blockers:

4. **`is_synthetic` defer pattern is paper-fix per `[[feedback_paper_fix_antipattern]]`** — Spec #2 §A.2 + tasks.md A-infra-2 say "Phase B implementer chooses Mechanism A or B". But the acceptance SQL (AC-2 §What and `A-dispatch-2`) hard-codes `WHERE is_synthetic=1` AND falls back to `title LIKE '[DEMO-M6-%]'` (mechanism B). Title column also does not exist. Decision must be **locked at Phase A** with a fully wired-through column choice or a different join strategy. ⇒ **C-AI-4** (Spec #2).

5. **AD-M5-11 over-claim collision** — Both Spec #2 frontmatter (line 18) and Spec #3 (line 12 + AD allocation table + §B.6) reserve "AD-M5-11 ... claimed". Spec #2 frontmatter line 18 says "AD-M6-4..6 reserved for this Spec only" but never explicitly cites AD-M5-11 — yet brainstorm DEC §2 line 128 says "AD-M5-11 ... Spec #3 may use". Need explicit cross-Spec lock so Phase B doesn't double-write AD-M5-11. ⇒ **C-AI-5** (cross-Spec).

6. **Pre-flight $2 cap pre/post-estimation gap** — Spec #2 §A.5 says "real LLM, ≤$2/dispatch" and AC-6 reads `cost_usd` from the log AFTER the dispatch. But the dispatch is irreversible — by the time you can see the actual `cost_usd` it's already been spent. There is no pre-flight estimation that ABORTS before the dispatch runs if estimated cost > $2. ⇒ **C-AI-6** (Spec #2).

---

## 1. Critical findings (must fix R1→R2)

### C-AI-1 — Spec #2: SQL queries reference non-existent columns (SCHEMA SoT violation)

**Where**:
- Spec #2 proposal §A.2 lines 91-106 (stratification SQL)
- Spec #2 proposal §AC-2 lines 591-628 (binary-falsifiable Python SQL)
- Spec #2 tasks.md A-dispatch-1 lines 156-161, A-dispatch-2 lines 168-176, A-dispatch-3 lines 179-185, A-dispatch-4 lines 187-189, A-dispatch-6 lines 207-218
- Spec #2 §Constraints "Schema column SoT" lines 475-481 (acknowledges no `provider` column, but misses the rest)

**Live schema (verified via `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/schema.sql` line 35-239 at HEAD)**:

| Spec #2 references | Reality in schema.sql |
|--------------------|-----------------------|
| `final_state` | **does not exist** — column is `state TEXT NOT NULL` (line 66) |
| value `'S9'` | **wrong sentinel** — terminal state is `S9_CLOSE` (line 65/123/259), and `S_FAIL` is the other terminal |
| `issue_type` | **does not exist** anywhere in the dispatches table |
| `project_name` | **does not exist** anywhere |
| `title` | **does not exist** anywhere |
| `created_at` (on dispatches) | **does not exist** — schema_meta has `created_at` key (line 40) but it's a meta row; dispatch rows have `state_entered_at` (line 67) and `cycle_start_ts` (line 125) |
| `is_synthetic` | does not exist yet (would be added by m6 migration 005 — see C-AI-4) |

**Why this is Critical**: When Phase B runs `python3 aria-orchestrator/acceptance/check-m6-e2e-acceptance.py --tg-a` against the real DB, every SELECT throws `sqlite3.OperationalError: no such column: final_state`. AC-2 cannot pass. This is the canonical paper-fix antipattern surfaced by `[[feedback_paper_fix_antipattern]]` and `[[feedback_test_mock_pattern_hides_prod_bug]]`: the SQL was written without grepping the live SoT.

**Proposed text-replacement (R2 fix, byte-faithful)**:

In Spec #2 §A.2 lines 91-106, replace the stratification gate SQL with:

```sql
-- Stratification gate: ≥10 dispatches at terminal S9_CLOSE, ≥1 per required category.
-- SoT: aria-layer1/schema.sql HEAD — column names verified.
SELECT
    json_extract(audit_log.payload_json, '$.issue_type') AS issue_type,
    COUNT(*) AS n
FROM dispatches d
LEFT JOIN dispatch_audit_log audit_log
    ON audit_log.dispatch_id = d.dispatch_id
   AND audit_log.event_type = 's0_issue_classified'
WHERE
    d.state = 'S9_CLOSE'
    AND d.state_entered_at BETWEEN :run_start AND :run_end
GROUP BY issue_type
HAVING COUNT(*) >= 1;
-- Required: rows include issue_type IN ('bug','feature','stale')
-- AND SUM(n) across all rows >= 10.
```

**Or**, if `issue_type` was always intended to be a new schema column, Spec #2 must declare a migration `006_m6_issue_type.sql` adding `issue_type TEXT` with backfill rules, and the abi_compat paired test triple in §A.7 must extend to migration 006 as well. The current text reads as if `issue_type` already exists, which it doesn't.

Add explicit clause to §Constraints "Schema column SoT" (after line 481):

> Additionally: the columns `final_state`, `title`, `created_at`, `project_name`, and `issue_type` are **not present** in the live dispatches schema as of M5 archive. Spec #2 SQL must use `state` (terminal value `'S9_CLOSE'`), `state_entered_at` (in lieu of `created_at`), and source `issue_type`/`project_name` either from a Phase B migration 006 or from `dispatch_audit_log.payload_json` via `json_extract()`. Phase A.3 task-planner must lock which option before Phase B branches.

Then update **every** SQL block in proposal §AC-2 and tasks.md A-dispatch-1..6 + AC-2 + cross-project query (A-dispatch-6 line 209-215 uses `project_name`) to match the chosen option. Cross-project query (P-9) needs the same fix — `project_name` does not exist.

**Acceptance for R2 close**: grep'd schema.sql for every column name in every SQL in Spec #2; all match. Add a one-line unit test scaffold in `aria-orchestrator/tests/test_m6_acceptance_sql_columns.py` that runs `PRAGMA table_info(dispatches)` and asserts each column referenced by the acceptance script exists (per `[[feedback_validator_repo_drift_guard_test]]`).

---

### C-AI-2 — Cross-Spec: PRD §639 "平均" (average) vs Spec mandate "median" — falsifiability gap

**Where**:
- PRD §656 verbatim: `拟人命令质量 (人工评分, 10 samples 平均 ≥ 7/10)`. `平均` is unambiguously "mean/average" in Chinese.
- Spec #2 proposal §C.2 line 400: `**Median scoring**: median of the 7 dimension scores for a single sample. Pass threshold: ≥7. **Corpus pass**: median(sample-01..10 medians) ≥7/10.`
- Spec #2 AC-5 (line 684): `stdout contains \`[PASS] AC-5: 10 samples scored, median=<N.N> >= 7.0\``
- Spec #2 tasks.md C-scores-2 (line 624-642): computes `statistics.median(scores)` per sample then `statistics.median(medians)` over the 10 samples.
- Spec #3 proposal §AC-6 line 446-455: line counts only, doesn't double-mandate, but §C.2.B.3.2 references the same rubric.

**Why this is Critical** (per `[[feedback_falsifiable_evidence_for_binary_acceptance]]`):

For 10 samples with per-sample scores: mean and median diverge meaningfully on outliers.
- Example A: `[10,10,10,10,10,4,4,4,4,4]` → mean=7.0 PASS, median=7.0 PASS (both pass).
- Example B: `[10,10,10,10,10,10,10,3,3,3]` → mean=7.7 PASS, median=10 PASS.
- Example C: `[8,8,8,8,8,8,6,6,6,6]` → mean=7.2 PASS, **median=7** PASS by exact tie.
- Example D: `[8,8,8,8,8,6,6,6,6,6]` → mean=7.0 borderline, **median=7** PASS, BUT if scores swap to `[7,7,7,7,7,6,6,6,6,6]` → mean=6.5 FAIL, median=6.5 FAIL.
- **Pathological**: `[10,10,10,10,10,5,5,5,5,5]` → mean=7.5 PASS, median=7.5 PASS but five samples scored unacceptably low. PRD likely intended "average ≥ 7" as a tolerance; "median ≥ 7" is a STRICTER claim that filters extreme tails but accepts up-to-4 sub-7 samples. The two threshold semantics are not interchangeable.

The Spec changed the PRD acceptance metric **without a PRD patch** (Q-final-1 Path a established that PRD §628-629 patches are owner-actioned; this should follow the same discipline).

**Proposed resolution** (one of two — owner Q escalation):

- **Option α (recommended)**: Patch PRD §656 to mirror Spec language: `拟人命令质量 (人工评分, 10 samples 各样本7维度评分的 median, 整体 median ≥ 7/10)`. Then Spec text stands. Add to Spec #2 §Cross-references a note: "PRD §656 to be patched in PRD patch series (parallel with Q-final-1 §M6 timeline patch)."
- **Option β**: Revert to PRD wording. Spec #2 §C.2 + AC-5 + tasks.md C-scores-2 compute mean of per-sample means. Tradeoff: less outlier-resistant; matches PRD text literally.

R2 must lock one option with rationale. Until then the Spec is internally consistent but PRD-divergent.

**Acceptance for R2 close**: PRD patch text drafted (Option α) OR Spec text reverted (Option β). Either way, AC-5 line in Spec #2 must cite the canonical authority (PRD §656 + commit SHA of patch, OR Spec-internal rationale).

---

### C-AI-3 — Spec #3 §B.4: `layer-boundary-contract.md` location conflicts with PRD §568

**Where**:
- PRD §568 (verbatim): `| layer-boundary-contract.md | Layer 1 / Layer 2 职责契约 | \`standards/autonomous/\` |`
- Spec #3 §B.4 lines 273-286: `**Target file**: \`/home/dev/Aria/aria-orchestrator/docs/layer-boundary-contract.md\`` + `<!-- Aria-specific: this file is NOT Lab-shareable. It belongs in aria-orchestrator/docs/, not in standards/. Per km M-km-R2-005 decision. -->`
- Spec #3 §AD-M5-11 (proposal line 374): rationalizes the split as Aria-internal contracts vs Lab-shareable.

**Why this is Critical**: PRD is the contract anchor. Spec #3 explicitly **contradicts** PRD §568 and replaces it with a per-km decision. Per Aria's Rule #3 (`文档与代码必须同步更新`) plus the implicit "PRD before Spec" hierarchy, this needs either a PRD patch or a documented PRD-supersede decision. The Spec's `<!-- km M-km-R2-005 -->` comment is **not** a sufficient supersede authority — km is a brainstorm agent voice, not a PRD editor.

The rationale Spec #3 gives (Aria-specific contracts shouldn't pollute the shared standards submodule) is **technically sound** — it aligns with `[[project_meta_repo_pattern]]` (standards as own git repo, importable by Kairos/SilkNode). But the procedural step (PRD patch or supersede note) is missing.

**Proposed resolution**:

1. Add PRD patch task to Spec #3 §Dependencies (parallel to Q-final-1 patch series): "PRD §568 line `layer-boundary-contract.md ... standards/autonomous/` to be patched → `aria-orchestrator/docs/`. Owner action; tracked alongside §M6 timeline and §628-629 cost-gate patches."

2. Add explicit cross-reference in Spec #3 §B.4 header (lines 273-280) citing the PRD patch:

```
**PRD supersede**: PRD §568 originally placed this file in `standards/autonomous/`. Per
km M-km-R2-005 (DEC-20260524-001 brainstorm), the file is reframed as Aria-specific.
PRD patch tracked in Spec #4 release-closeout pre-release checklist (alongside Q-final-1
§M6 timeline patch).
```

3. Spec #4 release-closeout pre-release checklist must add the PRD §568 patch as a release-blocker (otherwise Aria 2.0 ships with PRD claiming a location that doesn't exist).

**Acceptance for R2 close**: PRD §568 patch text drafted (one-liner: change `standards/autonomous/` → `aria-orchestrator/docs/`); Spec #3 §B.4 header cites it; Spec #4 dependency added.

---

### C-AI-4 — Spec #2: `is_synthetic` Phase B deferral is paper-fix; both mechanisms fail acceptance

**Where**:
- Spec #2 proposal §A.2 lines 109-129 (Mechanism A column vs Mechanism B title prefix)
- Spec #2 proposal §How AD-M6-4 line 550: "Deferred to Phase B"
- Spec #2 tasks.md A-infra-2 lines 57-69: "If column exists ... If absent ... If migration blocked".
- Spec #2 AC-2 SQL (line 605-614): hard-codes `WHERE is_synthetic=1`.
- Spec #2 tasks.md A-dispatch-2 line 177: `If Mechanism B (title prefix): replace \`is_synthetic=1\` with \`title LIKE '[DEMO-M6-%]'\`.`

**Why this is Critical** (per `[[feedback_paper_fix_antipattern]]` + `[[feedback_layered_od_resolution_with_live_probe]]`):

Mechanism B is **structurally non-viable** because:
1. `title` column does **not exist** on the dispatches table (verified — see C-AI-1).
2. Even if `title` existed via audit_log JSON, a fallback to title-prefix matching breaks abi_compat paired test triple §A.7 (which asserts migration 005 leaves audit triggers intact) — because Mechanism B writes no migration at all, the abi_compat test trivially passes but Mechanism B's column won't have an audit guard.
3. The Phase B chooser logic in A-infra-2 ("If migration blocked: use Mechanism B") has no falsifiable trigger. "Migration blocked" is not defined. Per `[[feedback_falsifiable_evidence_for_binary_acceptance]]` this gate is subjective.

A live probe in Phase A is needed (per `[[feedback_layered_od_resolution_with_live_probe]]`): does the live DB currently have any in-flight schema migration that 005 would conflict with? If no, Mechanism A is mandatory.

**Proposed resolution**:

1. Run live probe at Phase A.3 (before agent allocation): `PRAGMA user_version` and `SELECT key FROM schema_migrations ORDER BY applied_at DESC LIMIT 5;` — record in `.aria/probes/m6-pre-spec-b-schema-snapshot.md`.

2. If no migration in flight (overwhelming likely — M5 archived 2026-05-23 with schema v4.2): **lock Mechanism A** in AD-M6-4 at Phase A.2 R2 (not deferred to Phase B). Update proposal §A.2 lines 109-129 to delete Mechanism B path entirely. Update tasks.md A-infra-2 to drop the if/else branches and write migration 005 unconditionally.

3. If a migration is genuinely in flight: Spec #2 declares dependency on that other Spec's completion before Phase B can start. This is a real blocker, not "fallback to a column that doesn't exist."

4. Replace the "Phase B implementer chooses" language with a Phase A-locked decision; AD-M6-4 becomes a real Decided slot, not a Deferred one. This also matches `[[feedback_ad_slot_backfill_checkpoint]]` discipline (no Deferred AD slots at Phase A end).

**Acceptance for R2 close**: live probe ran; AD-M6-4 Decided with Mechanism A (or genuine in-flight dependency cited); Mechanism B path removed from Spec text and tasks.md.

---

### C-AI-5 — Cross-Spec: AD-M5-11 over-claim collision (Spec #2 vs Spec #3)

**Where**:
- Spec #2 frontmatter line 18: `**AD allocation reservation**: AD-M6-4 / AD-M6-5 / AD-M6-6 reserved for **this Spec #2** only.` (correctly disclaims AD-M5-11)
- Spec #3 frontmatter line 12: `**AD-M5-11** (pre-existing M5 RESERVED slot in \`aria-orchestrator/docs/architecture-decisions.md\`) is claimed by this Spec for M6 docs architectural decisions.`
- Spec #3 §B.6 line 296-301: claims AD-M5-11 for the standards/autonomous/ namespace creation decision.
- Live arch-decisions.md line 3478 (verified): `**AD-M5-11 reserved for**: M6 spec drafter 可在 M5 closeout 之后, M6 kickoff 前发现需补充的 M5-spillover decision`. Single claim — first-come-first-served.
- Brainstorm DEC §2 line 128: `**AD-M5-11**: pre-existing M5 reserved slot for M6 docs (Spec #3 may use)`.

**Status today**: Brainstorm gave it to Spec #3, and Spec #3 claims it. Spec #2 does not claim it. But Spec #2 §A.7 paired test triple (line 219-242) needs an AD slot for the `is_synthetic` migration 005 decision AND for the AdvancingClock DI decision (which Spec #2 has labelled AD-M6-6). The risk surface is:

- If Phase B of Spec #2 surfaces a new architectural decision beyond AD-M6-4/5/6 (very plausible — e.g., light-1 alloc drain reframe documented at §B.1 Infra-2 line 376-382 deserves its own AD), and the available AD slots in Spec #2's reservation are exhausted, the implementer may reach for AD-M5-11 not knowing Spec #3 claimed it.

**Why this is Critical now (not Phase B)**: Spec #3 ships in parallel with Spec #2 per brainstorm §6 (line 270-273). The two Specs may land in any order. If Spec #2 archives first (claiming AD-M5-11 informally), Spec #3 archive collides.

**Proposed resolution**:

1. Spec #2 frontmatter explicitly disclaims AD-M5-11: add to line 18-19 after the AD-M6-4/5/6 claim: `AD-M5-11 is reserved for Spec #3 (m6-docs) per brainstorm DEC §2 line 128. Spec #2 MUST NOT claim AD-M5-11; if a new AD slot is needed beyond AD-M6-4/5/6, Spec #2 reserves AD-M6-9 onwards (AD-M6-7/8 are Spec #3's).`

2. Spec #3 frontmatter (line 12) already correct; add a stronger phrasing: `AD-M5-11 lock owner = Spec #3 (this Spec). Spec #2 and Spec #4 MUST NOT claim AD-M5-11.`

3. Live architecture-decisions.md line 3478 RESERVED slot text — when Spec #3 ships, the file edit must change `**AD-M5-11 reserved for**: M6 spec drafter 可在 M5 closeout 之后` to `**AD-M5-11 状态: Decided** (claimed by aria-2.0-m6-docs T-B6, 2026-05-24)`. Spec #3 §B.6.1 currently directs this edit but the wording is slightly off — it says "Replace the RESERVED status with the Decided content" without specifying the file line range. Tighten to: "Edit `architecture-decisions.md` line 3460-3478: change frontmatter `状态: RESERVED` → `状态: Decided (2026-05-24, aria-2.0-m6-docs T-B6)`."

**Acceptance for R2 close**: Spec #2 frontmatter has explicit AD-M5-11 disclaim; Spec #3 has explicit lock-owner language; tasks.md T-B6.1 cites line range.

---

### C-AI-6 — Spec #2: Pre-flight $2 cap is post-hoc, not pre-flight

**Where**:
- Spec #2 proposal §A.5 line 178-179: "real LLM calls (real throwaway cost; hard cap: $2 per dispatch, total ≤$6 for 3 dispatches combined)"
- Spec #2 AC-6 line 707-714: `costs = [float(m) for m in re.findall(r'cost_usd:\s*([\d.]+)', content)]` and `assert all(c <= 2.0 for c in costs)` — reads after-the-fact log entries.
- Spec #2 tasks.md A-dispatch-5 line 195-205: same pattern.

**Why this is Critical** (ai-domain — provider semantics):

In a real Layer 1+Layer 2 dispatch:
- Layer 1 (Hermes via Luxeno subscription) cost per call = $0 by `compute_cost(..., provider="luxeno")` per `token_tracking.py:88-90` — Luxeno is flat-rate, attribution is null.
- Layer 2 (`aria-runner` container) cost is the bulk: it spawns Claude Code which makes many LLM calls. Owner mentioned anthropic deprecated (PRD §513), so Layer 2's LLM is also Luxeno-flat ($0 per-call attribution).
- Per `aria_layer1.token_tracking.compute_cost`: Luxeno path returns 0.0 always. Zhipu path returns metered.

**Implication**: under the current Luxeno-everywhere routing (post-2026-05-21 redirect, per `[[project_glm_routing_luxeno]]` memory), **`cost_usd` will be 0.0 for every pre-flight dispatch**. The `assert all(c <= 2.0 for c in costs)` will trivially pass with `[0.0, 0.0, 0.0]`. The $2 cap **does not actually cap** anything because attribution is null per subscription billing (per Spec #1's own `subscription_usd.cost_usd: null` rationale).

This is the same false-positive failure mode that Spec #1 §What.A explicitly warns against ("Any consumer that computes `month_to_date_cost >= 0.8 * threshold` for Luxeno MUST guard `if cost_usd is null: skip alarm logic` — Luxeno=0 false-positive prevention").

Either:
- The $2 cap claim is structurally meaningless and should be removed (and replaced with a different gate — e.g., dispatch count ≤ 3, latency budget ≤ 8h end-to-end).
- Or pre-flight must run via Zhipu (forcing `ZHIPU_API_KEY` set + `extension.py:879` gate path active), and the `cost_usd` value must come from Zhipu's metered response — requires a config override at Phase B kickoff.

**Proposed resolution**:

Add to Spec #2 §A.5 (after line 197) a "Cost-cap mechanics" paragraph:

```
**Cost-cap mechanics (P-8 sub-clause)**: Under current routing (Luxeno-everywhere post
2026-05-21, per [[project_glm_routing_luxeno]]), `cost_usd` for pre-flight dispatches will
report `0.0` because Luxeno is subscription_flat per `token_tracking.compute_cost`. The
$2/dispatch and $6 total caps are therefore NOT enforced by `cost_usd` comparison; they
are enforced by:
  (a) ≤3 pre-flight dispatches (hard count, AC-6).
  (b) Pre-flight latency budget: each dispatch must reach S9_CLOSE or S_FAIL within 8h
      wall-clock (deters runaway loops).
  (c) Owner-acknowledged subscription_usd disclaimer: pre-flight cost attribution is
      "subscription billing, no per-dispatch attribution" — same null semantics as
      Spec #1's `subscription_usd.cost_usd: null` field.

If owner wants real per-dispatch cost evidence, pre-flight MUST set `ZHIPU_API_KEY` env
in the aria-layer1 Nomad alloc and run with Zhipu provider override (config flip via
`extension.py:879` ZHIPU_API_KEY gate). This is an explicit Phase B opt-in; default
pre-flight runs under Luxeno-flat and AC-6 verifies (a)+(b) above instead of $2/dispatch.
```

Then update AC-6 (line 701-715) to verify count==3 + latency<8h per dispatch (instead of cost<$2). Or, if owner insists on real $2 attribution, add an AD-M6-? slot for "pre-flight provider override" and lock Zhipu routing for pre-flight only.

**Acceptance for R2 close**: AC-6 evidence script tests one of: (i) count≤3 + latency<8h, OR (ii) cost<$2 under explicit Zhipu override config. The current text claiming "$2 cap via cost_usd grep" is removed because Luxeno makes it vacuous.

---

## 2. Important findings (R2 strongly recommended; R3 acceptable)

### I-AI-1 — Spec #2 §B.1 LLM-4 mock semantics: Luxeno 429 is irrelevant

**Where**: Spec #2 §B.1 line 261, Infra-1 LLM-4 row: `LLM 429 rate-limit ... mock `RateLimitError` with `retry_after=30``.

**Issue**: Under Luxeno flat subscription, 429 rate-limit is **near-impossible** — Luxeno headroom is implicit in the subscription. Zhipu metered does see 429s (Insufficient balance per memory `project_glm_routing_luxeno`). The mock should specify which provider's 429 it emulates. Both `provider_router.py:90-92` (HTTP_429 enum) and `silknode_client.py` (Luxeno path) handle 429 differently from `zhipu_client.py`.

**Recommendation**: In Spec #2 §B.1 mock-layer-per-mode matrix LLM-4 row, change "Rate limit response mid-transition (S2/S3/S6 LLM call)" → "Zhipu 429 mid-transition (S2/S3/S6 LLM call when Zhipu route active). Mock target is `aria_layer1.zhipu_client.ZhipuClient.call_llm` raising `RateLimitError(retry_after=30)`; Luxeno path is excluded because Luxeno=flat-subscription has no per-call 429 semantics in this routing config." Add note: "If routing is Luxeno-only (current state per memory), LLM-4 test exercises the ProviderRouter's degrade-to-Zhipu path; if no Zhipu key configured, LLM-4 test is documented as `pytest.skip('no Zhipu route active; covered by upstream Spec #X when Zhipu routing re-enabled')` rather than masking the gap."

Also add to LLM-4 row in the matrix: `Mock layer = SDK boundary on \`zhipu_client.call_llm\`, NOT on a generic `llm_client.complete()`. The schema has no `llm_client` module; that is hand-wavy.` Grep confirms: there is no `llm_client.complete()` in `aria-layer1`. The actual call paths are `silknode_client.call_llm`, `zhipu_client.call_llm`, and `provider_router.ProviderRouter.call_with_routing`.

### I-AI-2 — Spec #2 §B.1 LLM-5/LLM-6: provider-typed body required, not generic

**Where**: Spec #2 §B.1 LLM-5/LLM-6 rows lines 262-263, tasks.md B-llm-2/B-llm-3 lines 449-479.

**Issue**: `httpx_mock.add_response(method="POST", url=re.compile(r"https://.*api.*"), status_code=200, content=b"{ bad json [")` is wildcard-URL. Luxeno (`api.luxeno.ai/v1`) and Zhipu (`open.bigmodel.cn/api/paas/v4`) have different response envelopes (OpenAI-compat vs Zhipu-native). LLM-5 invalid JSON differs by provider — Zhipu wraps errors in `{"error":{"code":...,"message":...}}` while OpenAI-compat (Luxeno) uses `{"error":{"type":...,"message":...}}`.

**Recommendation**: Add to Spec #2 §B.1 mock matrix a footnote: "LLM-5 and LLM-6 httpx_mock URL pattern MUST match the actual provider endpoint under test (Luxeno = `api.luxeno.ai/v1/chat/completions`; Zhipu = `open.bigmodel.cn/api/paas/v4/chat/completions`). Wildcard URL is a smell; use provider-specific test files: `test_crash_llm5_luxeno_invalid_json.py` and `test_crash_llm5_zhipu_invalid_json.py` (and same for LLM-6)." Per `[[feedback_mock_layer_per_failure_semantic]]` — HTTP-layer mock must reproduce real provider envelope.

In tasks.md B-llm-2 line 451-456, replace `url=re.compile(r"https://.*api.*")` with two test functions, one per provider URL. This grows the LLM-5/LLM-6 test count from 2 to 4 but matches real provider semantics.

### I-AI-3 — Spec #2 §A.6 cross-project (P-9) PAT scope assumption is unverified

**Where**: Spec #2 §A.6 line 209-211: condition #2 says `aria-runner-bot scopes sufficient — see [[feedback_pat_scope_canonical_from_codebase_grep]]`.

**Issue**: The memory cited (`[[feedback_pat_scope_canonical_from_codebase_grep]]`) says canonical scope comes from "codebase API grep reverse-inference, not from a single AD/decision partial list". Spec #2 cites the memory but doesn't actually do the grep. Cross-project dispatch will hit Kairos and SilkNode Forgejo repos; the required PAT scopes for those orgs may differ from Aria's. The text "existing scopes sufficient" is an unverified assumption.

**Recommendation**: Add Phase A.3 pre-flight task: `grep -rn "forgejo_client.\|forgejo\\.10cg\\.pub" aria-orchestrator/hermes-extensions/aria-layer1/ | grep -E "scope|token" | tee .aria/probes/m6-pat-scope-audit.md`. Lock the actual scope list in AD-M6-? (new slot) before Phase B. If cross-project hits new endpoints (e.g., `kairos-org` org reads), document the required scope additions and gate AC-2 P-9 evidence on owner confirming scope is granted.

### I-AI-4 — Spec #3 §B.3.2 humanized samples deferred while Spec #2 TG-C is upstream

**Where**: Spec #3 R-M6D-8 line 516 mitigation: "B.3.2 can be drafted from M5 E2E evidence and prior brainstorm examples, independent of Spec #2 TG-C corpus timeline."

**Issue**: Spec #2 §C.3 line 405-426 establishes BOTH-locations: Spec #2 = raw corpus, Spec #3 = curated abstractions distilled FROM the corpus. If Spec #3 ships first by drafting "from M5 evidence and brainstorm examples", the BOTH-locations design is hollow — Spec #3's "curated" samples have no actual abstraction-from-corpus provenance. The ai-domain risk is that "curated patterns" become AI fabrications presented as Lab patterns.

**Recommendation**: Add to Spec #3 §B.3.2 (after line 271) explicit ordering: "B.3.2 ≥10 curated samples MUST be drawn from one of:
  - (a) Spec #2 TG-C corpus (preferred — actual M6 E2E evidence)
  - (b) M5 archive corpus (`openspec/archive/2026-05-23-aria-2.0-m5-*/`) — if Spec #2 TG-C is not yet shipped at B.3.2 implementation time.
  - (c) **NOT** AI-generated from brainstorm prose (rejected — fabrication risk).
Each curated sample MUST cite its source artifact (dispatch_id or archive doc + line)."

Also remove the "prior brainstorm examples" phrasing from R-M6D-8 mitigation — brainstorm prose is meta-discussion, not humanized command samples.

### I-AI-5 — Spec #3 Diff 3 (CLAUDE.md two-layer split) does not cite live routing

**Where**: Spec #3 §A.1 Diff 3 line 54-56: "Layer 1 (Hermes + GLM) = PM role. Layer 2 (aria-runner + CC + aria-plugin) = engineering role."

**Issue**: This phrasing assumes Layer 1 = "GLM" (provider-neutral). Per `[[project_glm_routing_luxeno]]` (2026-05-21 corrected): Hermes path A uses `provider: zai` config name but **endpoint redirected to Luxeno** (`GLM_BASE_URL=https://api.luxeno.ai/v1`); aria-layer1 path B uses Luxeno explicitly. The "GLM" naming is **legacy** and misleading — it refers to the model family (`glm-4.5-air`, `glm-5.1`, etc.) not the routing endpoint. CLAUDE.md should reflect reality: Layer 1 calls go to **Luxeno endpoint** (api.luxeno.ai/v1) running GLM models.

**Recommendation**: In Spec #3 §A.1 Diff 3 (and the source draft `claude-md-revision-draft.md`), change "Layer 1 (Hermes + GLM) = PM role" to "Layer 1 (Hermes + Luxeno-routed GLM models) = PM role". Add a footnote: "Routing endpoint: `api.luxeno.ai/v1` (Luxeno subscription, post 2026-05-21 redirect). Model family: glm-4.5-air / glm-5-turbo / glm-5.1." This matches Spec #1 §What.A cost model (subscription_flat Luxeno) and prevents AI sessions from mis-routing future calls to a hypothetical "GLM" provider.

### I-AI-6 — Spec #2 §A.5 Option C cross-project pre-flight + §A.6 P-9 conditional confusion

**Where**: Spec #2 §A.5 line 190-193 (Option C "Cross-project Kairos/SilkNode issues") and §A.6 (P-9 conditional cross-project) seem to allow cross-project pre-flight separately from cross-project acceptance.

**Issue**: Option C reads "use ≥1 real Kairos or SilkNode issue as one of the 3 pre-flight dispatches (evidences cross-project capability in pre-flight log)." But §A.6 P-9 conditions say cross-project is only conditional acceptance (PASS+) and tagged `is_synthetic=0`. If pre-flight uses a real cross-project issue and the issue does not reach S9_CLOSE (because dispatch hits unmapped PAT scope per I-AI-3), pre-flight log shows a non-S9 cost entry — does that fail AC-6? Two interpretations are valid.

**Recommendation**: Spec #2 §A.5 clarify: "Option C pre-flight dispatch is evaluated against the same pre-flight pass criteria as Options A/B (reaches S9_CLOSE or S_FAIL within 8h; cost_usd grep present in log). It does NOT count toward AC-2 P-9 PASS+ unless it occurs DURING the 7d window (pre-flight is pre-window). Cross-project pre-flight evidences provider routing health; cross-project acceptance evidences sustained operation." Same clarification in tasks.md A-dispatch-5/A-dispatch-6.

### I-AI-7 — Spec #3 AC-1 grep pattern brittleness

**Where**: Spec #3 AC-1 line 388: `grep -q "**版本**: 2.0.0" CLAUDE.md`.

**Issue**: Shell expansion of `**` in unquoted grep pattern fails in many shells (bash globs `**` in interactive shells with globstar; sh treats it literally). The proposal also uses literal `**版本**: 2.0.0` in tasks.md T-A1.9 line 41 without escaping. Cross-platform test risk.

**Recommendation**: Change all such grep patterns to `grep -qF '**版本**: 2.0.0' CLAUDE.md` (fixed-string mode, single quotes prevent shell expansion). Apply globally to Spec #3 AC-1 + T-A1.9 + Spec #3 state-checks Probe 2 §A.6 line 167 (`grep -oP '(?<=\\*\\*版本\\*\\*: )[0-9]+\\.[0-9]+\\.[0-9]+'` — keep the regex but verify it handles markdown bold escapes).

### I-AI-8 — Spec #3 §AC-3 README badge claim assumes plugin.json version is v1.27.0

**Where**: Spec #3 AC-3 line 410-411: `grep -q "v1.27.0" README.md && grep -q "Aria 2.0" README.md && exit 0`.

**Issue**: Hardcodes `v1.27.0` as the badge target. Spec #3 ships in parallel with Spec #2 over weeks. If aria-plugin bumps to v1.27.1 or v1.28.0 mid-Spec (very likely given current cadence — 4 patches in 2026-04-23 session alone per `[[project_aria_v1_16_1_patch]]`), the AC-3 grep silently fails post-implementation. The AC should read the version from `plugin.json` not a literal.

**Recommendation**: Change AC-3 to:
```bash
PLUGIN_VER=$(python3 -c "import json; print(json.load(open('aria/.claude-plugin/plugin.json'))['version'])")
grep -q "v${PLUGIN_VER}" README.md && grep -q "Aria 2.0" README.md && exit 0
```

Same for tasks.md T-A2.1 and AC-1d. This matches the spirit of state-checks Probe 1 (which already does this dynamically — proposal §A.6 line 150-152). Internal inconsistency: Probe 1 reads plugin.json dynamically; AC-3 hard-codes. Make them consistent.

---

## 3. Nits (record, defer to Phase B unless trivial)

- **N-AI-1** (Spec #2): typo "≤$6 for 3 dispatches combined" but §A.5 line 179 also says "$2 per dispatch, total ≤$6" — but with 3 × $2 = $6 cap, the total ceiling is exact, not "≤$6" (could be exactly $6 if all 3 are at cap). Minor; clarify "≤$6 cumulative budget; per-dispatch ≤$2 hard cap, no per-dispatch under-cap rollover" to prevent ambiguity.

- **N-AI-2** (Spec #2): §B.3 `FakeClock` class (line 318-326) has no `timezone` import shown — risk of `datetime` naive vs aware mismatch. Add `from datetime import datetime, timezone, timedelta` to the class snippet for completeness.

- **N-AI-3** (Spec #2): mock-layer-per-mode matrix uses "monkey-patch `sqlite3.connect()`" for WAL-A/B/C (line 260). monkey-patching `sqlite3.connect` directly is a footgun — depending on test framework lifecycle, the patch can leak across tests. Should be `mocker.patch('aria_layer1.db.sqlite3.connect', ...)` (function-scoped) explicitly.

- **N-AI-4** (Spec #3): AC-1 grep for "Rule #" count ≥ 9 (line 388). The pattern matches any string starting "Rule #" including code samples discussing rules ("see Rule #X"). Tighter: `grep -cE '^[0-9]+\. \*\*' CLAUDE.md` for the numbered list pattern; or count `### Rule #` headings.

- **N-AI-5** (Spec #3): T-A1.6 (Diff 6 NO-OP verification line 38) uses `grep -E "规则 #[1-6]"` but rules are formatted as `1. **... Rule #X ...**` in CLAUDE.md (numbered list with bold), so `规则 #[1-6]` might not match. Verify the regex against live CLAUDE.md content before using.

- **N-AI-6** (Spec #2): tasks.md A-dispatch-5 line 200-201 says probe template fields include `dispatch_id`, `fixture_source`, `outcome`, `cost_usd`, but doesn't reference the 8h latency budget I-AI-6 surfaces. If C-AI-6 resolves with latency budget, add `latency_seconds` field to template too.

---

## 4. Cross-Spec consistency check (block #11-#14 from task prompt)

### #11 — Spec #1 cost.json schema cite in Spec #3 B.4

**Status**: PARTIAL. Spec #3 §B.4 line 282 says "cost.json schema (locked at Spec #1 c29a800): full schema reproduction including `metered_usd`, `subscription_usd`, `freshness_ts` fields". Spec #1 §What.A lines 75-95 has the actual JSON. Spec #3 §B.4 will "reproduce" the schema during Phase B B.4 — but the proposal does **not** yet inline the schema, so byte-identity can't be verified at Phase A. Risk: paraphrase drift during B.4 writing.

**Recommendation**: Add to Spec #3 tasks.md T-B4.2 (line 309-313) a literal copy-paste source: "Copy the exact JSON block from Spec #1 proposal §What.A lines 75-95 (between the ` ```jsonc ` fences). Do not re-type; use copy-paste from the canonical source. Verify with `diff <(jq . openspec/changes/aria-2.0-m6-cost-acceptance/proposal.md ...) <(jq . aria-orchestrator/docs/layer-boundary-contract.md ...)`." Or use a single SoT include pattern (e.g., a fenced code block in `aria-orchestrator/docs/cost-schema.json` that both Spec #1 and B.4 reference). Per `[[feedback_spec_v2_body_propagation_2pass]]`: copy-paste from canonical SoT prevents drift.

### #12 — Spec #2 TG-C corpus ↔ Spec #3 humanized-command-patterns.md content boundary

**Status**: Mostly OK. P-11 in brainstorm DEC §4 + Spec #3 §B.3.2 line 260-265 explicitly: "standards/ file = curated patterns + rubric guide; aria-orch/evals/ file = raw corpus samples. Cross-reference; no content duplication." Spec #2 §C.3 line 405-426 mirrors this with BOTH-locations design.

**Gap**: The abstraction-vs-instance boundary is asserted but not enforced. A reviewer in Phase C can't mechanically detect content duplication; they have to read both files and intuit. Without an explicit rule "no sample text appears verbatim in both files", drift is invited.

**Recommendation**: Add to Spec #2 §C.3 (after line 426) and Spec #3 §B.3.2 a falsifiable de-dup check:

```bash
# Verify no verbatim sample text duplication between locations.
# Each Spec #2 sample has a unique dispatch_id; Spec #3 patterns must NOT reference dispatch_ids.
grep -oP 'dispatch_id:\s*\S+' standards/autonomous/humanized-command-patterns.md | wc -l
# expected 0 (Spec #3 abstracts; doesn't cite specific dispatches)
```

Add this as a binary AC clause in both Specs.

### #13 — Spec #4 future references to Spec #2 AC-2

**Status**: Not in this audit's scope (Spec #4 separate). But Spec #2 AC-2 phrasing (line 593-628) is the Python SQL inline block. For Spec #4 to mechanically consume, AC-2 needs a callable interface, not just a Python snippet. Recommendation for Spec #2 R2: factor AC-2 into a CLI: `python3 aria-orchestrator/acceptance/check-m6-e2e-acceptance.py --tg-a --check-dispatch --json` emitting `{"ac2_passed": true, "total": N, "synthetic_ratio": X, "bug": N, "feature": N, "stale": N}`. Spec #4 then `jq '.ac2_passed' < output.json` — mechanical, falsifiable. The current Python block embedded in proposal is human-readable but not machine-consumable.

### #14 — PRD §M6 acceptance numerals coverage

PRD §640 = 7d / §641 = ≥10 issue / §654 = <10min approval / §655 = <20% drift / §656 = 平均 ≥7/10.

Coverage map:
- 7d uptime: Spec #2 AC-1 ✅
- ≥10 issue dispatch+merge: Spec #2 AC-2 ✅ (but `final_state='S9'` is wrong per C-AI-1; correct: `state='S9_CLOSE'`)
- <10min approval: **NOT in any of Spec #1/#2/#3**. Belongs to Spec #4 release-closeout or is dropped silently. Need to track explicitly.
- <20% drift detection error rate: **NOT in any of Spec #1/#2/#3**. M5 spec-drift threshold default 70 (abi_compat #3) is enforced as a code default; the <20% claim is a runtime metric. Spec #4 or carryover? Need owner Q.
- 平均/median ≥7/10: Spec #2 AC-5 ✅ (but median vs mean disagreement per C-AI-2).

**Recommendation**: Spec #2 §Out-of-scope explicit row "OOS-X: PRD §654 (<10min median approval time) and PRD §655 (<20% drift error rate) are owned by Spec #4 release-closeout pre-release checklist OR documented as carryover to v2.0.1 — not in Spec #2." Track in cross-Spec coverage matrix.

---

## 5. Provider-specific deep dives (block #15-#16 from task prompt)

### #15 — Anthropic deprecated check

**Status**: PASS. Grep of `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/*.py` returned **zero** matches for "Anthropic" or "anthropic". No new Anthropic mock scaffolding in Spec #2 §B.1 (matrix lines 258-263 use SDK-generic exception names like `RateLimitError` and `ProcessKilledError`).

**Minor caveat**: Spec #2 §B.1 LLM-4 row says "RateLimitError" — this exception class name needs binding to a real module. In Anthropic SDK it's `anthropic.RateLimitError`; in OpenAI-compat SDK (Luxeno uses OpenAI-compat per `silknode_client.py`) it's `openai.RateLimitError`; in Zhipu native it's a custom error class. Spec #2 should not import from `anthropic` even by class name — bind LLM-4 mock to `aria_layer1.zhipu_client.ZhipuClient` / `silknode_client.SilknodeClient` raising the project's existing exception types. Cross-ref I-AI-1.

### #16 — Zhipu/Luxeno binary routing

**Status**: PASS. Spec #2/#3 mention only Zhipu and Luxeno (+ "GLM" as model-family name, not provider name). No 3rd-provider scope creep detected.

**Minor caveat**: `provider_router.py:99-100` defines `PROVIDER_LUXENO`, `PROVIDER_ZHIPU`, plus synthetic `"router"` enum for routing entries. Spec #2 §B.1 LLM-6 says "SDK converts 5xx to `ProviderUnavailableError`" — that exception class doesn't exist in current `provider_router.py` (grep shows only outcome enums HTTP_5XX/HTTP_429/etc, no `ProviderUnavailableError` class). Either:
  - Add `ProviderUnavailableError` class to `provider_router.py` as part of Spec #2 §B (deserves an AD slot).
  - Or use the existing outcome-enum-based handling and rephrase Spec #2 §B.1 LLM-6 row.

**Recommendation**: Pick one path in Spec #2 R2. Don't reference a class name that doesn't exist in the codebase.

---

## 6. Memory entry recommendations (none new R1; verify existing)

Verified citations against live memory MEMORY.md:

- `[[project_glm_routing_luxeno]]` ✅ exists; cited correctly in Spec #2 cross-references line 842 and brainstorm DEC §7 line 292. **Action**: Use the 2026-05-21 corrected fact (Luxeno-everywhere routing) when revising Spec #2 §A.5 cost-cap mechanics (C-AI-6) and Spec #3 §A.1 Diff 3 (I-AI-5).
- `[[feedback_test_mock_pattern_hides_prod_bug]]` ✅ exists; cited correctly Spec #2 §B.1 line 265.
- `[[feedback_mock_layer_per_failure_semantic]]` ✅ exists; cited Spec #2 §B.1 line 492.
- `[[feedback_falsifiable_evidence_for_binary_acceptance]]` ✅ exists; cited Spec #2 line 558 + Spec #3 line 382.

No new memory entries needed at R1; defer to Phase C/D session-handoff if substantive learnings emerge during fixes.

---

## 7. R1 verdict + R2 entry criteria

**Verdict**: **NEEDS_FIX** (both Specs)

R2 must close **all 6 Critical** with literal text-replacement clauses. R2 reviewer (next ai-engineer pass) verifies:
1. C-AI-1: every SQL column in Spec #2 acceptance scripts matches live schema (mechanical grep test scaffolded).
2. C-AI-2: PRD §656 patch drafted OR Spec #2 reverted to mean. AC-5 cites canonical authority.
3. C-AI-3: PRD §568 patch drafted; Spec #3 §B.4 + §B.6 + Spec #4 dependency added.
4. C-AI-4: Mechanism A locked at Phase A.2 R2 (or genuine in-flight dependency cited); Mechanism B removed.
5. C-AI-5: AD-M5-11 lock-owner language in both Specs' frontmatter.
6. C-AI-6: Pre-flight $2 cap reframed as count+latency (or explicit Zhipu override AD slot).

R3 stability check expected to pass once R2 closes the Critical set. Important items I-AI-1..8 may slip to Phase B if R2 surfaces R3-blocking dependencies — owner decides at R2 close.

---

## 8. Audit trace

```
2026-05-24 ai-engineer R1 (combined Spec #2 + Spec #3, single round)
├── Read Spec #2 proposal.md (44 sections, ~46k bytes)
├── Read Spec #2 tasks.md (~38k bytes)
├── Read Spec #3 proposal.md (~42k bytes)
├── Read Spec #3 tasks.md (~30k bytes)
├── Read Spec #1 proposal.md §What.A (cost schema) for cross-ref verification
├── Read brainstorm DEC-20260524-001 (full)
├── Read PRD §225-243 (humanized command protocol), §305, §369, §381, §491-553 (provider routing), §567-568 (doc locations), §638-656 (M6 验证)
├── Read live token_tracking.py (compute_cost branching, Luxeno=0 false-positive surface)
├── Read live provider_router.py (provider/outcome enums, NO ProviderUnavailableError class)
├── Read live zhipu_pricing.py (snapshot vintage + owner-verify flag)
├── Verified schema.sql @ HEAD (line 35-239): dispatches columns enumerated
├── Verified architecture-decisions.md line 3460-3478 AD-M5-11 RESERVED text
├── Verified memory [[project_glm_routing_luxeno]] (2026-05-21 corrected fact)
└── 6 Critical + 8 Important + 6 Nits authored

Time budget used: ~22 minutes (within ~15-20 target; +2 min for live SoT verification grepping)
```

---

**Auditor sign-off**: ai-engineer (R1, Aria 2.0 M6 sister Specs)
**Recommended next action**: spec-drafter R2 fix pass (Spec #2 + Spec #3 in parallel; ~2h R2-fix overhead per Spec). After R2, schedule R3 stability with same ai-engineer scope-limited to Critical closure verification.
