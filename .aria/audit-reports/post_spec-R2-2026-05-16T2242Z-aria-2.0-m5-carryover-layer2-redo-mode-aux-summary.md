---
checkpoint: post_spec
mode: convergence
round: R2
converged: false
oscillation: false
verdict: NEEDS_FIX
timestamp: 2026-05-16T22:42Z
spec_id: aria-2.0-m5-carryover-layer2-redo-mode-aux
context: openspec/changes/aria-2.0-m5-carryover-layer2-redo-mode-aux/
agents: [tech-lead, qa-engineer, code-reviewer]
agent_count: 3
proportionality_rationale: Spec X R3 stability 3-agent precedent + Spec Y verification (not stability) — 3 sufficient
spec_y_head_audited: 9de6f1f
predecessor_round: R1 (2026-05-16T05:30Z, 37 findings, 6 CRIT)
findings_total: ~22 distinct (cross-agent dedup)
findings_critical: 2 (R2-1 schema v4.2 collision NEW; CRIT-1/2/4/5/6 propagation PARTIAL)
findings_high: ~10
findings_medium: ~6
findings_low: ~4
convergence_prognosis: R3 needed after surgical body-propagation; estimated ~2-3h fix + 30min R3 stability audit
---

# R2 post_spec Verification Audit — Spec Y v2

## Verdict: NEEDS_FIX (3/3 agent consensus)

**Common diagnosis**: v2 commit `9de6f1f` correctly locks all 6 CRIT architectural decisions in proposal §"R1 → v2 fixes" table, but failed to **propagate** those decisions to the proposal body (§A-G + 验收 + 风险与回滚) and to tasks.md task entries. Result: an implementer reading the proposal body OR tasks.md (rather than the fix table) would reproduce the original CRIT-1/2/4/6 bugs. Additionally, **1 new CRITICAL** schema version collision and ~10 HIGH new findings surface.

**Architecturally sound** — no decision needs rework. **Mechanically incomplete** — body/tasks propagation pass missed.

---

## R1 CRITICAL closure — cross-agent consensus

| ID | R1 issue | v2 fix table claim | Tech-lead | qa-engineer | Code-reviewer | Consensus |
|----|----------|---------------------|-----------|-------------|---------------|-----------|
| **CRIT-1** | `_handle_s5_pr_created` doesn't exist | T1.5 extend `_handle_s5_await` terminal path | PARTIAL | PARTIAL | PARTIAL | **PARTIAL** — table+T1.5 correct; proposal §B L96-99, §A L92, risk row L261, tasks T3.1 L99 still reference `_handle_s5_pr_created` |
| **CRIT-2** | `python3 -m commit_validator` broken | Shell-port lib/commit-lint-validate.sh | PARTIAL | PARTIAL | PARTIAL | **PARTIAL** — table+T5 correct; proposal §D L127-141 code block STILL contains literal `python3 -m aria_layer1.commit_validator validate`; L144 caption still says "Python module already shipped" |
| **CRIT-3** | REWORK_ROUND not propagated | 5th meta_optional key | ✅ PASS | ✅ PASS | ✅ VERIFIED | **✅ PASS** — T-pre.1-pre.6 complete; HCL contract bump 4→5; Spec X latent bug retro-fix included |
| **CRIT-4** | spec_drift_input_fetcher 4-tuple wrong | Return 3-tuple `(spec_what, spec_acceptance, pr_diff)` matching reconciler:1014 | PARTIAL | FAIL | PARTIAL | **FAIL** — table says 3-tuple; tasks T4.4 L115 STILL says `SpecDriftInputs(proposal_text, pr_diff, spec_id, pr_id)` 4-field named tuple. Direct contradiction. Will crash reconciler:1014 unpack at runtime |
| **CRIT-5** | T7.2 AD-M5-3 append guard missing | Literal "append BELOW existing 2026-05-16 line preserving Spec X line" | ✅ (table) | PARTIAL | NOT VERIFIED | **PARTIAL** — fix table contains guard literal; tasks T7.2 L165 only has new append text, NO preserve guard. Phase B agent executing T7.2 from tasks.md has CRIT-5 still latent |
| **CRIT-6** | Migration 005 collision | Renumber to 006 | PARTIAL | PARTIAL | PARTIAL | **PARTIAL** — tasks T0.1/T0.5 correct (006); proposal §C L111 still says `005_schema_v4.1_additive.sql`; 验收 L226 still says "migration 005" |

**CRIT closure rate**: 1/6 fully closed (16%) vs R1 target ≥80%. Far below threshold.

---

## NEW CRITICAL (R2-raised, not in R1)

### R2-NEW-1: Schema version target collision (tech-lead R2-1 + qa-engineer NF-2 independent consensus)

**Severity**: CRITICAL — silent correctness bug

**Issue**: Migration 006 must declare a NEW target version, but tasks.md T0.1+T0.2 say "v4.0 → v4.1". Reality: `_LATEST_SCHEMA_VERSION = "4.1"` (schema_migrate.py:65); current state is **already** at v4.1 from M5 migration 005. schema_migrate.py compares `current_version == _LATEST_SCHEMA_VERSION` and returns no-op. Migration 006 will never run; `spec_id` column will never be added; T4 spec_drift_input_fetcher will fail to query spec_id from dispatches table.

**Evidence**: 
- `aria_layer1/schema.sql:37` schema_version 4.1
- `migrations/005_schema_v4_drop_inline_uq.sql:222` confirms 4.1 set
- `aria_layer1/schema_migrate.py:62-65` `_LATEST_SCHEMA_VERSION = "4.1"`
- tasks.md L48-50 says "Update schema_meta row inserting v4.1 marker"

**Fix**: 
- Rename `006_schema_v4.1_add_spec_id.sql` → `006_schema_v4.2_add_spec_id.sql`
- T0.1: from_version="4.1", to_version="4.2"
- T0.2: schema.sql header v4.1 → v4.2
- schema_migrate.py: add entry `("006", ..., "4.1", "4.2")` + bump `_LATEST_SCHEMA_VERSION = "4.2"`
- T0.4 baseline: "migration adds spec_id to v4.1 DB" (not v4.0)
- All references to "v4.1" in Spec Y → "v4.2"

---

## R1 HIGH closure — cross-agent consensus

| HIGH | Fix claim | tech-lead | qa-engineer | code-reviewer | Consensus |
|------|-----------|-----------|-------------|---------------|-----------|
| backend-H1 OS-3 partial state | PATCH-first then comment | ✅ table | ✅ table | NOT VERIFIED | **PARTIAL** — table reverses order; tasks T3.3 L101 still POST comment THEN T3.4 PATCH (old order preserved) |
| backend-H2 spec_id source | issue.yaml@S1_SCAN | NEEDS_FIX | PARTIAL | ✅ | **PARTIAL** — table+T1.1 correct; proposal §C L114 still says "Layer 2 result.json includes spec_id; Layer 1 _handle_s5_pr_created reads"; `linked_spec_id` field doesn't exist in M1 issue schema (NEW R2 finding R2-2) |
| qa-H6 archive path fallback | T4.2 try changes/ then archive/ | PARTIAL | ✅ | PARTIAL | **PARTIAL** — table claims fallback; T4.2 L113 only mentions `openspec/changes/`, no fallback code |
| qa-H7 regression commands | T6.9 enumerate executable | PARTIAL | PARTIAL | NOT VERIFIED | **PARTIAL** — counts correct (51 bash + 812 Python verified); commands not enumerated per Spec X T6.3 pattern |
| ai-3 AD-M5-3 narrowing note | T7.2/T7.3 narrowing | NOT VERIFIED | PARTIAL | NOT VERIFIED | **NOT VERIFIED** — tasks T7.2 L165 has no narrowing note text |
| ai-4 T5.1 LLM cost row | Risk table cost row | PARTIAL | — | PARTIAL | **PARTIAL** — ARIA_MODEL fix done; risk table L255-265 has NO cost row |
| ai-5 Redo prompt char budget | T2.5 explicit caps 4KB/10K/500/15KB | NOT VERIFIED | — | NOT VERIFIED | **NOT VERIFIED** — T2.5 L84-87 has no char caps |
| ai-7 commit_message directive | T2.5 literal IMPORTANT prompt | NOT VERIFIED | PARTIAL | NOT VERIFIED | **NOT VERIFIED** — T2.5/T2.6 no literal directive |
| C1-C10 bundle | Various | PARTIAL | — | PARTIAL | **PARTIAL** — Conv Commits examples not enumerated per Spec X (P1.8); lib/forgejo-helpers "consider" vs "always extract" drift (P1.9) |

**HIGH closure rate**: ~3/13 fully verified (~23%) — below R1 target ≥80%.

---

## NEW HIGH findings (R2-raised, ≥2-agent consensus or single-agent high-severity)

### R2-NEW-2: `linked_spec_id` issue field doesn't exist (tech-lead R2-2)
M1 issue body schema has no `linked_spec_id` field. Spec Y T1.1 assumes parseable, but grep across codebase → zero matches outside Spec Y itself. **Fix**: add T1.0 (~0.5h) to extend M1 issue validator schema with optional `linked_spec_id: string`, OR pick alternative source (PR branch name pattern / Forgejo label prefix `spec:<id>`).

### R2-NEW-3: T5 sub-task numbering duplicate (3-agent consensus)
Two distinct tasks labeled `5.2` (tasks.md L126 + L131). **Fix**: renumber sequentially 5.1/5.2/5.3/5.4/5.5.

### R2-NEW-4: T3 sequence still old order (code-reviewer P1.10)
tasks.md T3.3 (L101) POST comment → T3.4 (L102) PATCH state. backend-H1 v2 fix decision is **reversed**: PATCH-first then comment. Failure mode "PATCH succeeds + comment fails" outcome `comment_only` cannot fire in current order.

### R2-NEW-5: T4.4 4-tuple contradiction (3-agent consensus, supersedes CRIT-4 verdict)
tasks.md L115 STILL says 4-field named tuple. Will raise `ValueError: too many values to unpack` at reconciler.py:1014. **Fix**: rewrite T4.4 to `Return (spec_what, spec_acceptance, pr_diff) 3-tuple matching reconciler:1014 unpack`.

### R2-NEW-6: CRIT-2 test-type mismatch (qa-engineer NF-1)
`test_t_commit_lint_retry.py` is Python (T5.4, T6.7) but validator is now bash (`lib/commit-lint-validate.sh`). Python subprocess-testing bash reintroduces cross-language test fragility. **Fix**: add `tests/changes-mode/commit-lint-validate.sh` bash test (3-4 cases: valid format / invalid / 72-char boundary / type prefix); Python test repurposed to retry loop integration only.

### R2-NEW-7: SQLite `ADD COLUMN IF NOT EXISTS` invalid syntax (tech-lead R2-4)
T0.1 says "idempotent via `IF NOT EXISTS` pattern OR migration-version guard". First is not valid SQLite syntax. **Fix**: drop `IF NOT EXISTS` mention; mandate migration-version guard (matches existing 004 approach).

### R2-NEW-8: Missing risk row for ai-4 cost (tech-lead R2-5)
HIGH ai-4 fix claim "Add cost row to risk table" — unfulfilled. Risk table L255-265 unchanged. **Fix**: add row "commit-lint retry × N dispatches × Opus rate → ~$0.01/failure; mitigation: 3-retry hard cap".

### R2-NEW-9: T2.9 result.json spec_id field dead (code-reviewer MEDIUM)
T1.4 says Layer 2 result.json does NOT need spec_id (Layer 1 S1_SCAN writes); T2.9 L91 still says "result.json write with spec_id (if can derive from issue body or env)". Dead field; remove from T2.9.

### R2-NEW-10: MODE_HANDLERS / dispatcher claim false (code-reviewer HIGH)
proposal L73 says "Spec Y drops 'redo' handler into per D5 A2 skeleton-then-fill" + "Spec X currently has the redo branch in entrypoint.sh exit 1". Sentence structure misleads — `MODE_HANDLERS` is not a structure; dispatcher is `case` statement. Currently `redo) ... exit 1`. **Fix**: rewrite L73 to literal: "Spec Y replaces `redo) ... exit 1` branch with `redo) exec /opt/aria-runner/modes/redo.sh "$@" ;;`" (already matches T2.1).

### R2-NEW-11: New PR title template missing (code-reviewer HIGH)
proposal L91 `POST /pulls -d '{"title":..., "head":"<new_branch>"}'` — title elided. **Fix**: add T2.8 sub-bullet with literal title template e.g. `title="Aria redo: PR-${PARENT_PR_ID} round ${REWORK_ROUND}"` or "same as parent PR title + `[redo R<N>]` prefix".

### R2-NEW-12: T-pre Spec X retro-fix scope not declared (code-reviewer HIGH)
T-pre.4-pre.6 modify Spec X archived test files + AD-M5-3 contract section. Legitimate per CRIT-3, but proposal §Out of Scope contrast or 风险与回滚 has no explicit "Spec X retro-modification" statement. **Fix**: add proposal subsection or note in CRIT-3 fix row.

---

## MEDIUM / LOW findings (~10 items, deferred to v3 inclusive)

- **Status line outdated** (P1.11): tasks.md L197 "当前 Phase: A.1 (Spec drafted, awaiting R1 audit)" → should be "A.2 (R2 verified, v3 fix in progress)"
- **Test count drift** (P1.12): proposal ~23 / tasks table ~25 / actual sum 28 — reconcile to ≥28
- **Estimate drift** (P1.13): proposal 19h / tasks 20h / tasks L27 24.5h — reconcile to single statement
- **lib/forgejo-helpers decision drift** (P1.9): T2.3 "consider" vs R1 fix table "extract always"
- **Memory reference missing** (P2.7): `feedback_agent_team_for_level1` per R1 LOW not added; `feedback_submodule_pointer_post_merge_bump` in tasks but not in proposal index
- **HCL change validate gap** (P2.3): T6.10 says "HCL unchanged but smoke verify" — but T-pre changes HCL; per `feedback_nomad_hcl_validate_early` must validate, not smoke
- **T7 numbering proposal §G ↔ tasks.md mismatch** (P1.6): proposal §G T7.4 validate-m5-handoff.py task dropped from tasks.md T7
- **T6.4 test file naming** (LOW): `close-old-pr-layer2.sh` misleads (Layer 2 only writes; closure is Layer 1) — rename `redo-result-pr.sh`
- **T3.3 round source unspecified** (MEDIUM): `(Aria redo round <N>)` — query source not specified
- **HIGH qa-H5 dropped from fix table** (MEDIUM): OS-3 failure modes (parent PR already closed / null pr_id) not addressed
- **CRIT-3 audit-log payload variable length** (MEDIUM R2-6): historical 4-key + new 5-key rows — readers must use `len()` not equality

---

## R3 action plan (cross-agent consensus)

### Surgical body+tasks propagation pass (~2-3h, mechanical)

**Priority CRIT (must fix before B.2)**:
1. **R2-NEW-1**: Schema bump v4.1 → v4.2 — rename file, update T0.1/T0.2/T0.4, schema_migrate.py entry + `_LATEST_SCHEMA_VERSION`
2. **CRIT-1 body**: All `_handle_s5_pr_created` → `_handle_s5_await` (proposal L92/96/261, tasks T3.1 L99)
3. **CRIT-2 body**: Rewrite proposal §D L127-144 to bash invocation; remove "Python module already shipped" caption
4. **CRIT-4 body+tasks**: Rewrite T4.4 to 3-tuple
5. **CRIT-5 tasks**: Add literal guard to T7.2 "append BELOW existing 2026-05-16 line preserving Spec X line"
6. **CRIT-6 body**: All `005_schema_v4.1_additive.sql` → `006_schema_v4.2_add_spec_id.sql` (proposal §C L111, 验收 L226)

**Priority HIGH (target ≥80% closure)**:
7. **R2-NEW-2**: Add T1.0 M1 schema extension OR pick alternative spec_id source
8. **R2-NEW-3**: Renumber T5 sub-tasks
9. **R2-NEW-4**: Reverse T3.3/T3.4 to PATCH-first
10. **R2-NEW-6**: Add `tests/changes-mode/commit-lint-validate.sh` bash test
11. **R2-NEW-10**: Rewrite proposal L73 literal entrypoint swap
12. **R2-NEW-11**: Add literal new PR title template to T2.8
13. **R2-NEW-12**: Declare T-pre Spec X retro-fix scope
14. **HIGH ai-5**: Add T2.5 explicit char caps
15. **HIGH ai-7**: Add T2.5 commit_message extraction literal directive
16. **HIGH ai-3**: Add AD-M5-3 narrowing note literal to T7.2
17. **HIGH backend-H2 body**: Rewrite proposal §C L114 to S1_SCAN source
18. **HIGH qa-H6**: Add T4.2 archive-path fallback
19. **HIGH qa-H7**: Add T6.9 executable command enumeration

**MEDIUM/LOW (bundle)**: status line / test count / estimate / lib/forgejo helpers / memory refs / HCL validate / T7 numbering / T6.4 rename — all mechanical

### R3 audit (~30min)

3-agent **stability** mode (not convergence) on v3:
- Target: 0 CRITICAL, ≤3 HIGH, ≤6 MEDIUM/LOW
- Per `feedback_audit_convergence_pattern` 5-round template, R3 confirms 0-finding stability after R2 fix
- Spec Status → **Approved** if R3 stable; ready for Phase A.3 task-planner + B.1

---

## Convergence prognosis

Per `feedback_audit_convergence_pattern`:
- R1 (37 findings, 6 CRIT) → R2 (~22 findings, 6/22 = 27% **partial** + 1 new CRIT) — closure not at 73% reduction target
- Expected v3 (R3 stability): ≤5 findings, all LOW/MEDIUM doc polish
- Total Phase A.2 effort: v2→v3 surgical ~2-3h + R3 ~30min + Status flip = **~3.5h in next session**

**Per `feedback_phase_a_depth_drives_b_velocity`**: This R2 catch validates the principle — incomplete propagation in Phase A would have caused Phase B agent crashes at runtime (CRIT-4 reconciler unpack / R2-NEW-1 silent migration skip). 1-2h R2 invest avoids 5-10h Phase B debug.

---

## Cross-agent agentId references (for SendMessage continuation)
- tech-lead R2: a9f1233980a00b0e7
- qa-engineer R2: ab11a3a87763c247b
- code-reviewer R2: af0bb77acdf795365

## Files referenced
- `openspec/changes/aria-2.0-m5-carryover-layer2-redo-mode-aux/proposal.md` (lines 22-37 fix table; lines 73, 91-100, 109-120, 122-144, 261, 264, 287, 311 body)
- `openspec/changes/aria-2.0-m5-carryover-layer2-redo-mode-aux/tasks.md` (lines 5, 23-27, 82, 91, 99-102, 115, 125-134, 140, 152, 165, 197)
- `.aria/audit-reports/post_spec-R1-2026-05-16T0530Z-aria-2.0-m5-carryover-layer2-redo-mode-aux-summary.md` (R1 source-of-truth)
- `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/schema.sql:37` (already at v4.1)
- `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/schema_migrate.py:62-65` (`_LATEST_SCHEMA_VERSION="4.1"`)
- `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/extension.py` (no `_handle_s5_pr_created`)
- `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/reconciler.py:1014` (3-tuple unpack reality)
- `aria-orchestrator/docker/aria-runner/entrypoint.sh` (`redo) exit 1` current state)
- `aria-orchestrator/docker/aria-runner/modes/changes.sh:174,256` (REWORK_ROUND latent bug)
- `aria-orchestrator/nomad/jobs/aria-layer2-runner.hcl:89-97` (4-key meta_optional)
- `aria-orchestrator/docs/architecture-decisions.md:3574-3613` (AD-M5-3)
- `openspec/archive/2026-05-16-aria-2.0-m5-carryover-layer2-changes-mode/` (Spec X precedent)
- `standards/conventions/git-commit.md:40-53` (Conv Commits valid types)
