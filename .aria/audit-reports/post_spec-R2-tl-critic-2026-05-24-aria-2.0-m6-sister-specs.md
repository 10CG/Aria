# Post_Spec R2 CHALLENGE Audit (combined) — tech-lead-critic — Spec #2 + #3

> **Auditor**: tech-lead-critic
> **Round**: R2 challenge (Phase A.2 post_spec; combined-Spec mode)
> **Specs audited**: aria-2.0-m6-e2e-resilience (#2) + aria-2.0-m6-docs (#3)
> **Spec status at audit**: Draft, R1-fix pass commit `8a5fdc4` (vs R1-draft `e884e62`)
> **Spec #1 baseline**: aria-2.0-m6-cost-acceptance Approved `c29a800`
> **DEC references**: DEC-20260524-001 (sister Specs SoT), DEC-20260524-002 (Aria #124 submod gate)
> **R1 baseline (this auditor)**: 2 X-Critical + 4 Critical (1 Spec#2 + 3 Spec#3) + 8 Important
> **R2 verdict**: **NEEDS_FIX_PARTIAL** (Spec #3 has 1 paper-fix Critical re-classification; 1 NEW Critical introduced by Spec #2 fix-pass; 1 NEW Critical introduced by Spec #3 fix-pass)
> **Vote on convergence**: **NO — R3 required** (1-round stability check; ≥70% reduction achieved but 2 NEW Critical introduced surface in this seat alone — anti-paper-fix vigilance)

---

## Executive summary

The R1 fix-pass (`8a5fdc4`, ~1186 LOC added / 357 removed across 8 files) correctly applied 5 of 6 owner-locked decisions (Q1-Q5), executed mechanical PRD §568/§656 patches, and substantively closed 4 of my 6 Critical findings + closed both X-Criticals. **However, the fix-pass introduced 2 NEW Critical issues** (NC-tl-R2-1 migration slot collision, NC-tl-R2-2 gate logic direction inversion) and **1 of my R1 Criticals is a documented paper-fix** (C-tl-#3-1 partial: constraint heading + body text still say "Rule #1-#6 FROZEN" while Diff 6 says "Rules #1-#9 FROZEN" + AC-1 freeze check regex `Rule #[1-6]` would silently allow #7/#8/#9 body modifications).

Net: R1 had 14 findings (6 C + 8 I). R2 closes 4 of 6 Criticals fully + 1 partial (paper-fix) + 1 X-C-tl-2 closed-but-architecturally-fragile, AND introduces 2 NEW Criticals. **Reduction = ~64%** (4 closed + 1 partial = 4.5 out of 6 = 75% naive, but minus 2 NEW Critical introduced = net ~64%). **Below the 70% convergence threshold** when NEW-Critical-introduction discount is applied. Per `[[feedback_premerge_iteration_pattern]]` + `[[feedback_audit_r2_collapse_default_vs_owner_invoked]]`: R2-collapse rule requires (a) R2 4/4 SCOPE_OK + (b) 0 NEW Critical + (c) ≥70% reduction. Conditions (b) and (c) fail in this seat.

**Recommended trajectory**: R3 stability round with fix-pass scope limited to {NC-tl-R2-1 migration 006→007, NC-tl-R2-2 gate args direction, C-tl-#3-1 paper-fix completion}. Expected ≤30min fix, ≤10min R3 verify.

---

## R1 closure verification (your specific R2 deliverable)

### C-tl-#2-1 — state_machine.py path (Q1 multi-file cov) — **CLOSED**

Fix verification:
- `proposal.md:413,665,685,837-857`: `aria_layer1.state_machine` references removed; cov target rewritten to 4-module list (`extension`, `comment_poll`, `reconciler`, `tick_runner`) matching live codebase distribution.
- AD-M6-6 decision text (line 685) explicitly enumerates 4 modules; notes "no `state_machine.py` — Q1 lock 2026-05-24".
- Tasks `B-sm-1/2/3` (lines 609-680) reference the 4 modules; test files written to `aria-orchestrator/tests/test_state_machine_{deterministic,stochastic_replay}.py` (not `aria_layer1/state_machine.py`).
- R-M6-14 (line 971) updated to reference 4-module audit.

No `aria_layer1.state_machine` module-level references remain. **Closed cleanly.**

### C-tl-#3-1 — CLAUDE.md 9-Rule freeze enumeration — **PARTIAL (paper-fix detected)**

Fix verification (partial):
- ✅ Diff 6 (line 79): now reads `"不可协商规则"章节不修改 (Rules #1-#9 all FROZEN)`. Correct.
- ✅ Diff 9 (line 90): correctly scoped to additive content + version sync; AD11 constraint reaffirmed.
- ✅ AC-1 line 455: `grep -c "Rule #"` must return ≥ 9 (matches live structure).

**Paper-fix detected (2 sites):**
- ❌ `proposal.md:388` **Constraints section heading**: `### CLAUDE.md Rule #1-#6 text is FROZEN (AD11 hard constraint)` — still says #1-#6, contradicting Diff 6 body. R1 fix-trail in body (line 80) said "Updated to: Rules #1-#9 text body is FROZEN", but constraint section header not propagated.
- ❌ `proposal.md:390` **Constraints body**: `Diff 6 is explicitly a no-op. No diff to apply to Rules #1-#6 body text. AD11 "不修改现有 6 条不可协商规则, 只新增 Aria 2.0 运行时章节"` — Chinese AD11 quote still references "6 条" (six rules). 这 quote is FROM AD11's original draft text — but the constraint scope is supposed to extend to all 9 rules per Diff 6 update.
- ❌ `proposal.md:461` **AC-1 freeze check regex**: `git diff HEAD -- CLAUDE.md | grep "^[-]" | grep "Rule #[1-6]"` — regex `[1-6]` matches digits 1-6 only. Rules #7/#8/#9 body modifications would silently pass this gate. Should be `Rule #[1-9]`.

This is **exactly the paper-fix antipattern the audit prompt warned about**: "if Spec now says '9 diffs match live structure' but the body still has Diff 6 referring to non-existent Rules #1-#6 freeze, that's NOT CLOSED." Confirmed not closed in 3 specific lines. Per `[[feedback_paper_fix_antipattern]]`: doc-only fix without complete propagation = paper-fix.

**Concrete remediation** (~5min fix, 1 commit):
1. Line 388: `### CLAUDE.md Rule #1-#6 text is FROZEN` → `### CLAUDE.md Rule #1-#9 text is FROZEN (AD11 + Rule #9 extension)`
2. Line 390: `不修改现有 6 条不可协商规则` → `不修改现有 9 条不可协商规则 (AD11 原 6 条 + Rule #7/#8/#9 自 2026-04-12 增补)`; reaffirm Diff 6 = no-op on all 9 rule bodies.
3. Line 461: `grep "Rule #[1-6]"` → `grep "Rule #[1-9]"`. Add a positive line freeze test (e.g., `git diff HEAD -- CLAUDE.md` shows no `-` lines containing `**Rule #`).

### C-tl-#3-2 — Probe 1 regex (`head -1` brittle) — **CLOSED**

Fix verification:
- Probe 1 regex rewritten to `grep -m1 -oP 'badge[^\d]*v?\K[0-9]+\.[0-9]+\.[0-9]+'` (line 176). Anchors to `badge` keyword + `-m1` for first match.
- Live README test: regex extracts `1.15.2` (current stale badge) — correct PASS/FAIL semantic.
- PASS/FAIL fixture documented (line 186-188).
- Task ordering: line 173 explicitly states "produces PASS only after T-A2.1 (README badge update)". OK.

**Minor concern (Important-tier, NOT blocking R2)**: regex `badge[^\d]*v?\K[0-9]+\.[0-9]+\.[0-9]+` matches **any** badge URL containing a v-prefixed semver. If a future README badge is added (e.g., `[![Coverage](https://img.shields.io/badge/coverage-v0.0.1-green)]`) BEFORE the Plugin badge line, `-m1` picks the wrong badge. Fix would be `badge/Plugin-v\K[0-9]+\.[0-9]+\.[0-9]+` (anchor to literal `Plugin-v`). Tag as `I-tl-R2-1` below.

### C-tl-#3-3 — Plugin version SoT (dynamic read) — **CLOSED**

Fix verification:
- AC-3 evidence (line 482-483) reads `aria/.claude-plugin/plugin.json` dynamically via `python3`.
- Tested: `PLUGIN_VER=1.27.0` extracted correctly; `grep -qF "$PLUGIN_VER" README.md` exits 1 today (correct — pre-T-A2.1 state).
- §A.2 line 86 still says `update v1.15.2 → v1.27.0` as illustrative example with note "read live SoT". Acceptable.
- §A.3 (release notes) — still hardcodes `v1.27.0` in the version-mention prose (line ~102). Acceptable since release notes are a snapshot artifact, not a regenerating evidence target.

**Closed cleanly.**

### X-C-tl-1 — BOTH-locations path drift (`aria-orch/` → `aria-orchestrator/`) — **CLOSED**

Fix verification:
- `grep -rn 'aria-orch/' openspec/changes/aria-2.0-m6-*/` returns only **fix-trail comments** (`<!-- R1-X-T1 fix: aria-orch/ → aria-orchestrator/ -->`). No body text uses the shorthand.
- Spec #3 `humanized-command-patterns.md` cross-ref template (tasks T-B3.2.5/6, lines 315-316) uses full path.
- AC-6 grep regex (proposal line 523 fix-trail) updated to `aria-orchestrator/evals/m6-prompt-quality`.

**Closed cleanly.** Lab-shareable file destined for `standards/` submodule will now ship the full path.

### X-C-tl-2 — DEC-20260524-002 (Aria #124) submod gate not consumed — **CLOSED WITH NEW CRITICAL** (NC-tl-R2-2 below)

Fix verification (X-T2 framing):
- Spec #3 T-B0.10 (`tasks.md:191-205`) adds explicit v1.29.0 gate precondition with `merge-base --is-ancestor` check.
- Cross-ref to `.aria/decisions/2026-05-24-aria-124-submodule-pointer-regression-gate.md` §4 (B+) added (proposal line 668 + tasks line 205).
- Effort budget reflects +0.1h (proposal line 10 + tasks line 7).

**X-T2 surface-level closed.** BUT — **cross-check against dev-claude2's parallel Spec** (`openspec/changes/aria-submodule-pointer-regression-gate/`) reveals **gate logic argument-direction inversion** in Spec #3 T-B0.10. See NC-tl-R2-2 below.

### I-tl-* selective verification

- **I-tl-#2-1** (pre-flight $2 runtime enforcement): NOT closed in code, but Q1 default routing through Luxeno makes the runtime-cap moot for the default path (Luxeno = $0.0 always). AD-M6-4b (line 902) documents this trade-off. If implementer overrides to Zhipu, no pre-spending estimate exists. **Acceptable as Important-deferred** per `[[feedback_phase_budget_compounding]]`.
- **I-tl-#2-2** (mock-shape exception import path): tasks line 50 R1-T2-4 fix-trail confirms Mechanism B removed. Mock-shape import discipline NOT added as a per-import-statement check. **Important-open**.
- **I-tl-#2-3** (S4 vs S4_LAUNCH state list cross-cite to test_state_machine_skeleton.py): NOT addressed. **Important-open**.
- **I-tl-#2-4** (TG-C Day-1 vs Day-7 template split): NOT addressed. **Important-open**.
- **I-tl-#3-1** (T-B0 AI-runnable / owner-action split per `[[feedback_t15_owner_blocking_pattern]]`): NOT addressed. **Important-open**.
- **I-tl-#3-2** (m6-standards-autonomous-aria-leak Probe 4): NOT added. **Important-open**.
- **I-tl-#3-3** (TG-DOCS-B v2.0.1-deferrable archive semantics Option A vs B): NOT addressed. **Important-open**.
- **I-tl-#3-4** (Probe 3 deferral-aware suppression): NOT addressed. **Important-open**.

8 Important findings remain open. **Acceptable for R2** since R1 fix-pass scope was Critical+X-Critical. The R2-collapse rule does not require Important closure; ≤2 NEW Important is allowed.

---

## Architecture-level R2 inspection (NEW findings)

### AD-M6-* slot allocation post-Q2 swap — **OK with caveat**

Verified:
- Spec #1: AD-M6-1/2/3 (3 slots)
- Spec #2 §How table line 681-685: AD-M6-4/5/6 (3 slots), heading explicit `(AD-M6-4..AD-M6-6)`
- Spec #3 §How table line 437-441: AD-M6-7/8/9 (3 slots)

No overlap. No missing slot. AD-M5-11 vacated cleanly (Spec #3 frontmatter line 12 acknowledges; existing live `architecture-decisions.md:3460-3478` M5-spillover reservation untouched).

**Caveat — AD-M6-4b sub-letter slot drift** (Important-tier):
Spec #2 introduces `AD-M6-4b` (line 902 "Pre-flight routing strategy") as a sub-letter slot. References at lines 902, 905, 908, 937, 987, 1022 + tasks lines 858, 865 (T-docs-1b). **However**:
- Spec #2 frontmatter AD allocation reservation (line 18): only `AD-M6-4 / AD-M6-5 / AD-M6-6 reserved` — does NOT mention AD-M6-4b.
- §How table heading line 679: `### Key design decisions (AD-M6-4..AD-M6-6)` — explicitly excludes AD-M6-4b.
- §How table body (line 681-685) has NO row for AD-M6-4b.

Per `[[feedback_spec_v2_body_propagation_2pass]]`: AD-M6-4b is referenced in body but not propagated to the canonical decision table. This is **less severe than C-tl-#3-1's paper-fix** (sub-letter is not a slot collision and the decision text is documented in §B.5/AC-6 prose) but still a 2-pass propagation gap. Tag as `I-tl-R2-2` (Important).

### Migration 006 introduction — **NEW CRITICAL** (NC-tl-R2-1)

**Spec #2 claims `006_schema_v5_add_is_synthetic.sql`** at proposal lines 117, 161, 172, 298-302, 610, 987, 1021 + tasks line 87, 97.

**Filesystem verification**: `ls aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/migrations/`:
```
002_schema_v2_additive.sql
003_schema_v3_additive.sql
004_schema_v4_additive.sql
005_schema_v4_drop_inline_uq.sql
006_schema_v4.2_add_spec_id.sql   ← SLOT 006 ALREADY TAKEN (shipped 2026-05-15 per M5 layer 1 closeout)
__init__.py
```

**Migration slot 006 is already taken by the M5 spec_id additive migration** (per `[[project_us025_m5_layer1_shipped_2026-05-15]]`). Spec #2's "new migration 006" would conflict at filename level (duplicate filename) OR overwrite the M5 migration if the implementer doesn't check the slot.

**Severity**: Critical (Spec-vs-reality break, identical class to C-tl-#2-1 R1 finding — `state_machine.py` doesn't exist; here `006_*.sql` slot is already taken). Per `[[feedback_scaffold_helpers_drift_without_callers]]`: Spec ahead of code ships wrong column/signature; here Spec ahead of filesystem ships wrong filename.

**Concrete fix** (~5min, mechanical):
- All references `006_schema_v5_add_is_synthetic.sql` → `007_schema_v5_add_is_synthetic.sql` (or `007_schema_v4.3_add_is_synthetic.sql` — discuss with backend-architect on the v4.3 vs v5.0 schema version semantic).
- Schema version: M5 ships v4.2. is_synthetic is purely additive (DEFAULT 0). Should be v4.3, not v5.0. v5.0 implies a major schema break, which `is_synthetic INTEGER DEFAULT 0` is not. Per `[[feedback_schema_migration_to_version_bump]]`: bump to next minor (v4.3), reserve v5.0 for actual breaking changes.
- Sites to update (10 references): proposal.md 117, 161, 172, 298, 300, 301, 302, 610, 987, 1021 + tasks.md 87, 97 + AD-M6-4 row line 683.

### Spec #3 X-T2 v1.29.0 gate — **NEW CRITICAL** (NC-tl-R2-2)

**Spec #3 T-B0.10 (tasks.md:191-205)** writes the v1.29.0 gate precondition as:

```bash
MASTER_PTR=$(git -C standards rev-parse origin/master)
FEATURE_PTR=$(git -C standards rev-parse HEAD)
git -C standards merge-base --is-ancestor "$FEATURE_PTR" "$MASTER_PTR"
# exit 0 = forward/ancestor relationship confirmed (safe to bump)
```

**Cross-check against dev-claude2's authoritative parallel Spec** (`openspec/changes/aria-submodule-pointer-regression-gate/tasks.md:86-87`):
```bash
# Primary: git -C "$SUB" merge-base --is-ancestor "$MASTER_PTR" "$FEATURE_PTR" → exit 0 = PASS forward
# Reverse: git -C "$SUB" merge-base --is-ancestor "$FEATURE_PTR" "$MASTER_PTR" → exit 0 = REGRESSION
```

**The argument order is INVERTED in Spec #3 vs the v1.29.0 authoritative gate semantic.**

Per dev-claude2's gate (the authoritative SoT for DEC-20260524-002):
- `--is-ancestor MASTER FEATURE` exit 0 = master is ancestor of feature = feature ADVANCED master = **PASS forward (safe to bump pointer to feature)**.
- `--is-ancestor FEATURE MASTER` exit 0 = feature is ancestor of master = feature is BEHIND master = **REGRESSION (unsafe to bump)**.

Spec #3 T-B0.10 has the args as `--is-ancestor FEATURE MASTER` with the comment "exit 0 = forward/ancestor relationship confirmed (safe to bump)". This **literally claims the REGRESSION case is the PASS case**.

In practice today, this doesn't fire because T-B0.8 does `git checkout master && pull`, so `HEAD == origin/master`, so `FEATURE_PTR == MASTER_PTR`, and `--is-ancestor X X` returns 0 trivially. The script always passes. But:
1. **Semantic mis-statement** about the gate direction will mislead future implementers / readers debugging gate failures.
2. **The actual gate check is trivial** — it doesn't compare the pre-bump pointer (what's in the main repo's `.gitmodules` index) against the post-merge feature pointer. It compares HEAD against origin/master, which after `pull` are always equal.

Per `[[feedback_paper_fix_antipattern]]`: a gate that always passes is not a gate. Per the audit prompt's question 4 hint: "the gate command... exit 0 means branch IS ancestor (good for fast-forward). But after pointer bump, master has moved..." — the question was probing exactly this issue. The current Spec #3 implementation is semantically incorrect AND functionally null.

**Concrete fix** (~10min):
Replace T-B0.10 gate logic with dev-claude2-aligned version:
```bash
# Capture pre-bump pointer (from main repo's currently-staged or HEAD-tracked submod commit):
git -C standards fetch origin master
BEFORE=$(git ls-tree HEAD standards | awk '{print $3}')         # pre-bump pointer (main repo SoT)
AFTER=$(git -C standards rev-parse HEAD)                          # post-merge feature pointer

# Handle no-change (idempotent) and first-time-submod edge cases:
[ "$BEFORE" = "$AFTER" ] && { echo "OK no-change"; exit 0; }
[ -z "$BEFORE" ] && { echo "INFO first-time submod"; exit 0; }

# Primary (forward-advance): master pointer IS ancestor of feature pointer:
if git -C standards merge-base --is-ancestor "$BEFORE" "$AFTER"; then
  echo "Gate PASS: forward-advance $BEFORE -> $AFTER"; exit 0
fi

# Reverse (regression detected):
if git -C standards merge-base --is-ancestor "$AFTER" "$BEFORE"; then
  echo "Gate FAIL: REGRESSION $BEFORE -> $AFTER (feature is behind master)"; exit 1
fi

echo "Gate FAIL: DIVERGENCE $BEFORE vs $AFTER (no ancestor relationship)"; exit 1
```

**Severity**: Critical (X-T2 fix produced a non-functional gate that contradicts authoritative gate semantic; this is the **paper-fix antipattern** of "added the words but the mechanism is wrong" + a cross-Spec consistency break since dev-claude2's Spec is the SoT for the gate logic).

### Spec sequencing post-fix — **OK**

Phase A.3 readiness check:
- Spec #1 Approved (`c29a800`) — gate complete.
- Spec #2 + #3 parallel after R2 fixes → Phase A.3 (agent allocation) → Phase B.1 (branch creation per Spec).
- No cross-Spec dependency introduced by fix-pass that breaks parallel-ability.
- Spec #2 AC-5 grep checks "samples contain string `humanized-command-patterns.md`" — does NOT verify target file existence. If Spec #3 not done yet, AC-5 still passes (link target may be broken; this is acceptable during parallel Phase B).
- Spec #3 cross-refs Spec #2's TG-C corpus directory; corpus directory created by Spec #2 TG-C, but Spec #3 paths are write-only references (no read evidence required). OK.

### Spec #4 sequencing — **OK** (documented)

- Spec #2 proposal line 1057: "sequential after all M6 Specs done; consumes AC-1 + AC-3 + AC-5 as pre-release gates"
- Spec #3 proposal line 18 / 32 / 650 / 664: Spec #4 gates on Spec #3's CLAUDE.md v2.0 + state-checks probes
- DEC-20260524-001 §6 implies Spec #4 last (depends on #1+#2+#3 done). "Done" semantic = AC passing (Phase B/C complete), not Phase D archive. Aligned across both Specs.

### Effort baseline reconciliation — **NEW IMPORTANT** (I-tl-R2-3)

Verified drift:
- Spec #2 frontmatter line 11: `~29h impl (...+1h Q-NEW-1 hybrid mock layer vs 28h base)`. Phase A audit overhead ~1h not impl.
- Spec #2 tasks.md line 7: `~30h impl (~10.5h TG-A + ~13h TG-B + ~6h TG-C; +1h Q-NEW-1; +1h R1 fixes)`.
- Spec #2 Effort baseline body line 1015: `Total (AI-implementable) ~29-30h ≈ 30h`.
- Spec #2 Effort baseline body line 1022: `R1-fix delta: +0.5h schema drift guard + +0.5h AD-M6-4b. Total ~30h (vs 29h baseline)`.

Frontmatter says **~29h**, tasks + body + delta say **~30h**. **2-pass propagation gap**: frontmatter not updated to reflect R1-fix delta. Per `[[feedback_spec_v2_body_propagation_2pass]]`.

DEC-20260524-001 §2 total ~82h = 10 + 29 + 33 + 10 (Spec #1 + #2 + #3 + #4 estimates). With Spec #2 → ~30h, new total ~83h. Not acknowledged in any Spec §Effort baseline reconciliation section or DEC §2 footnote. Tag as `I-tl-R2-3` (Important).

### Phase A.3 entry block list — **CLEAR after R3 fix**

Block list to clear before A.3 entry:
1. **NC-tl-R2-1** migration 006 → 007 (Spec #2): blocks Phase B.T-schema-1 ship.
2. **NC-tl-R2-2** gate args direction (Spec #3): blocks T-B0.10 from being a real gate.
3. **C-tl-#3-1 paper-fix completion**: blocks AC-1 from being a real freeze check.

These 3 are the **minimum R3 scope**. After R3 fix-pass, both Specs can enter Phase A.3.

---

## New cross-Spec findings (R2-only, R1-fix-exposed)

### X-C-tl-R2-1 — Cross-Spec gate logic SoT drift (NEW)

Spec #3 T-B0.10 (v1.29.0 gate verification) does NOT align with dev-claude2's parallel Spec `aria-submodule-pointer-regression-gate` (the SoT for DEC-20260524-002). The argument-direction inversion in Spec #3 (see NC-tl-R2-2) means: when v1.29.0 gate ships, Spec #3's documented verification script will display **misleading PASS messages** in regression cases (currently masked by HEAD == origin/master equivalence after `git pull`).

This is a combined-mode finding (single-Spec audit on Spec #3 alone would not catch the dev-claude2 gate-logic SoT). **Confirms combined-mode value at R2 too** — not just R1.

Resolution covered by NC-tl-R2-2 fix.

---

## Anti-paper-fix self-check (R2)

Per the audit prompt's explicit warning: "Be skeptical of your own R1 findings closed by paper-fix."

- ✅ **C-tl-#2-1** (state_machine.py): genuine multi-file rewrite, not doc-only. Closed.
- ❌ **C-tl-#3-1** (CLAUDE.md 9 diffs): **paper-fix partial** — Diff 6 text updated to #1-#9 but constraint section heading + body still say "#1-#6"; AC-1 freeze regex still `[1-6]`. **NOT CLOSED.**
- ✅ **C-tl-#3-2** (Probe 1 regex): genuine regex rewrite, fixture documented. Closed.
- ✅ **C-tl-#3-3** (plugin version SoT): dynamic read implemented + tested. Closed.
- ✅ **X-C-tl-1** (path drift): mechanical sed verified by grep. Closed.
- ❌ **X-C-tl-2** (DEC-002 consumption): cross-ref + 0.1h budget added (surface OK), but the **gate mechanism itself is non-functional** (NC-tl-R2-2 args-direction inversion). **Surface closed, semantic broken.**

R1-fix introduced 2 NEW Critical (NC-tl-R2-1 migration slot collision, NC-tl-R2-2 gate args inversion) that single-Spec / non-cross-checking audit would miss. The combined-mode lens (cross-checking dev-claude2's parallel Spec for X-C-tl-R2-1 / NC-tl-R2-2) was essential.

---

## R2 Vote on convergence

**Vote**: **NO — R3 required (1-round stability/scoped-fix)**

**Rationale**:
- ✅ R1-fix achieved ≥70% raw closure on Criticals (4 of 6 closed cleanly + 1 partial).
- ❌ **2 NEW Critical introduced by fix-pass** (NC-tl-R2-1, NC-tl-R2-2) — disqualifies R2-collapse per `[[feedback_audit_r2_collapse_default_vs_owner_invoked]]` rule "(b) 0 NEW Critical".
- ❌ **1 R1 Critical incompletely fixed** (C-tl-#3-1 paper-fix on Rule #1-#6 vs #1-#9 constraint heading/body/AC regex). Per `[[feedback_paper_fix_antipattern]]`.
- Net reduction after NEW Critical discount: ~64% (below 70% threshold).

**R3 scope** (proposed; ≤30min total fix + ≤10min verify):
1. Spec #2: rename `006_schema_v5_*` → `007_schema_v4.3_*` (12 sites). Document schema bump v4.2→v4.3 (not v5.0).
2. Spec #3 tasks.md T-B0.10: swap `merge-base --is-ancestor` args + add pre-bump pointer capture via `git ls-tree HEAD standards`. Align to dev-claude2 SoT.
3. Spec #3 proposal.md lines 388/390/461: propagate "#1-#9 freeze" + AC-1 regex `[1-9]`.
4. (Optional, Important) Spec #2 frontmatter line 11: `~29h` → `~30h`; add §Effort baseline reconciliation note.
5. (Optional, Important) Spec #2 §How table: add AD-M6-4b row OR explicitly note "AD-M6-4b is a sub-letter slot documented in §B.5 prose, not a separate decision row".

After R3 fix-pass + R3 verify (1 round, 3-agent scope-limited to {NC-tl-R2-1, NC-tl-R2-2, C-tl-#3-1 paper-fix}), expect:
- 0 NEW Critical
- 0 paper-fix remaining
- Convergence at R3 (per Spec #1 precedent — Spec #1 converged at R3 after 1 stability round; Spec #2/#3 similar profile post NC-fix).

**Per-Spec verdict at R2**:
- Spec #2 (e2e-resilience): **NEEDS_FIX** (NC-tl-R2-1 migration slot collision; +1 Important effort baseline)
- Spec #3 (docs): **NEEDS_FIX** (NC-tl-R2-2 gate args inversion + C-tl-#3-1 paper-fix partial completion)

**Combined verdict**: **NEEDS_FIX** — R3 stability round required, scope-bounded.

---

## Recommended next-round trajectory

Per `[[feedback_premerge_iteration_pattern]]`:
- R3 = stability/scoped-fix round
- Scope limited to 3 NEW issues (NC-tl-R2-1, NC-tl-R2-2, C-tl-#3-1 partial completion) + 1-2 optional Important
- Single fix-pass agent (~30min)
- 3-agent R3 verify (~10min) — scoped to delta only
- If R3 produces 0 NEW Critical AND closes the 3 R2 issues → CONVERGED at R3

This trajectory matches Spec #1's R1→R3 path (Spec #1 R1 4/4 NEEDS_FIX → R2 4/4 SCOPE_OK with 1 stability concern → R3 confirmed 0-new → CONVERGED). Spec #2/#3 are at parity profile.

Per `[[feedback_3round_early_convergence]]`: R3 is justified when R2 fix introduces NEW Critical AND fix is <100 lines / few files / no logic-deep changes. NC-tl-R2-1 is ~12 sed-style references; NC-tl-R2-2 is ~10 lines of bash; C-tl-#3-1 paper-fix is 3 lines. Total <30 lines, mechanical — fits early-convergence profile.

---

## Findings count summary (R2)

| Category | R1 (this auditor) | R2 closed | R2 partial/paper-fix | R2 NEW | R2 net open |
|----------|-------------------|-----------|----------------------|--------|-------------|
| X-Critical | 2 | 1 (X-C-tl-1) | 1 (X-C-tl-2 surface only; semantic = NC-tl-R2-2) | 1 (X-C-tl-R2-1 = NC-tl-R2-2) | 1 |
| Spec #2 Critical | 1 | 1 (C-tl-#2-1) | 0 | 1 (NC-tl-R2-1) | 1 |
| Spec #3 Critical | 3 | 2 (C-tl-#3-2, #3-3) | 1 (C-tl-#3-1 paper-fix) | 0 | 1 |
| **Critical total** | **6** | **4** | **1** | **2** | **3** |
| Spec #2 Important | 4 | 0 | 4 (acceptable deferred) | 1 (I-tl-R2-2 AD-M6-4b table row) | 5 |
| Spec #3 Important | 4 | 0 | 4 (acceptable deferred) | 0 | 4 |
| Cross-Spec Important | 0 | — | — | 1 (I-tl-R2-1 Probe 1 regex tighten) + 1 (I-tl-R2-3 effort baseline) | 2 |
| **Important total** | **8** | **0** | **8** | **3** | **11** |

Reduction = (4 closed + 1 partial / 6) * 100% = 75% raw → net 64% with NEW Critical penalty.

**Verdict reaffirmed**: NEEDS_FIX, R3 stability round required, scope-bounded to 3 Critical fixes.

---

## Cross-references

- R1 self-report: `.aria/audit-reports/post_spec-R1-tl-critic-2026-05-24-aria-2.0-m6-sister-specs.md`
- R1 aggregate: `.aria/audit-reports/post_spec-R1-aggregate-2026-05-24-aria-2.0-m6-sister-specs.md`
- DEC-20260524-001: `.aria/decisions/2026-05-24-us026-m6b-brainstorm.md`
- DEC-20260524-002: `.aria/decisions/2026-05-24-aria-124-submodule-pointer-regression-gate.md`
- dev-claude2 parallel Spec (gate logic SoT): `openspec/changes/aria-submodule-pointer-regression-gate/tasks.md:79-93`
- Migration directory (NC-tl-R2-1 evidence): `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/migrations/` (slot 006 taken by M5 spec_id migration)
- Live CLAUDE.md (C-tl-#3-1 evidence): `/home/dev/Aria/CLAUDE.md` lines 343-426 (9 numbered rules)
- R1-fix diff: `git diff e884e62..8a5fdc4` (1186 +/357 -, 8 files)

---

**Auditor**: tech-lead-critic
**R2 timestamp**: 2026-05-24
**Time budget used**: ~18min (within ~15-20min)
**Memory entries woven**: `[[feedback_audit_convergence_pattern]]` (5-round convergence), `[[feedback_premerge_iteration_pattern]]` (stability check required), `[[feedback_phase_budget_compounding]]` (Important deferral acceptable), `[[feedback_audit_r2_collapse_default_vs_owner_invoked]]` (R2-collapse criteria; failed at "0 NEW Critical"), `[[feedback_paper_fix_antipattern]]` (C-tl-#3-1 + NC-tl-R2-2 paper-fix detection), `[[feedback_scaffold_helpers_drift_without_callers]]` (NC-tl-R2-1 migration slot collision class), `[[feedback_spec_v2_body_propagation_2pass]]` (C-tl-#3-1 + I-tl-R2-2 + I-tl-R2-3 propagation gaps), `[[feedback_schema_migration_to_version_bump]]` (v4.2 → v4.3 not v5.0), `[[feedback_3round_early_convergence]]` (R3 scope-bounded justified)
