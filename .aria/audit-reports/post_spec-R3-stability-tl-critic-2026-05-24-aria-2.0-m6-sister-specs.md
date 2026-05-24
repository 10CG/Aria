# Post_Spec R3 Stability Check (combined sister-Specs) — tech-lead-critic

> **Auditor**: tech-lead-critic
> **Round**: R3 stability (Phase A.2 post_spec) — scope-limited to 3 R2 fixes
> **Specs**: aria-2.0-m6-e2e-resilience + aria-2.0-m6-docs
> **Spec status**: Draft post-R3-fix (commit c0e9d79)
> **DEC references**: DEC-20260524-001 (brainstorm) + DEC-20260524-002 (Aria #124 gate)
> **Vote**: **R3_STABLE**

---

## Summary

All 3 R2-fix items verified CLOSED via byte-level evidence (grep counts, sed-extracted bash `bash -n` syntax check, cross-reference to dev-claude2 SoT). Zero new Critical and zero new Important issues introduced by the R3 fix-pass. Convergence trajectory R1 (~25 raw → 10 themes + 5 X-Critical) → R2 (3 NEW Critical, all TRUE-positive) → R3 (0 new) is monotonically converging. Specs #2 + #3 are ready for Phase A.3 → Approved status flip.

---

## R2 fix verification matrix

| R2 ID | Closure | Evidence | Note |
|-------|---------|----------|------|
| NC-tl-R2-1 (migration rename 006 → 007) | **CLOSED** | Spec #2 `proposal.md` (2 hits) + `tasks.md` (3 hits) of canonical name `007_schema_v4.3_add_is_synthetic.sql`; grep `006_schema\|migration 006\|Migration 006\|m006\|006_schema_v5` returns 0 matches across both files. Filesystem confirms slot 006 occupied by M5's `006_schema_v4.2_add_spec_id.sql` (untouched, 2149 bytes, May 19), slot 007 empty (to be created by M6). Schema progression v3→v4→v4(uq-drop)→v4.2→v4.3 additive contract preserved. Python variable `m007` consistently used at tasks.md:323-326. | No collision risk. R-M6E-PR-1 risk row (line 1038-1039) updated to reference slot 007. |
| NC-tl-R2-2 (Spec #3 T-B0.10 gate args inversion) | **CLOSED** | Spec #3 `tasks.md` lines 195-220: replaced single-call gate with 3-zone branching (PASS forward / REGRESSION / DIVERGENT). PASS check uses `git merge-base --is-ancestor "$MASTER_PTR" "$FEATURE_PTR"` (line 207) — bit-exact match to dev-claude2 SoT `aria-submodule-pointer-regression-gate/tasks.md:86` ("Primary: `git -C "$SUB" merge-base --is-ancestor "$MASTER_PTR" "$FEATURE_PTR"` → exit 0 = PASS forward"). Reverse check at line 210 (`FEATURE_PTR` first) emits REGRESSION + exit 1 — matches SoT:87. DIVERGENT branch (else) emits exit 1 with explanatory message. `bash -n /tmp/r3_gate.sh` returns clean. Inline R3 fix-trail comment present at tasks.md:197-200. | Semantic now matches Aria #124 DEC-20260524-002 §4 (B+) "block mode" gate design v1.29.0. |
| C-tl-#3-1 paper-fix (Rule #1-#6 → Rule #1-#9 propagation) | **CLOSED** | Spec #3 grep for forbidden patterns `Rule #1-#6\|Rules #1-#6\|规则 #\[1-6\]\|6 条规则\|6 rule bodies\|the 6 rules\|不修改现有 6 条` returns 0 matches. Only 2 residual `1-6` occurrences exist: (a) proposal.md:80 historical fix-trail `R1-T3-1 fix: original Diff 6 said "Rules #1-#6 FROZEN"...` — intentional per checklist exemption; (b) tasks.md:59 historical fix-trail `R1-I3-1: The Rule freeze scope extends to all 9 rules (not just #1-#6)` — also intentional fix-trail. New `Rule #1-#9` / `规则 #[1-9]` text confirmed at 12 sites across proposal.md (lines 59, 79, 81, 82, 101, 388, 390, 451, 460, 596) + tasks.md (lines 39, 51, 57, 58, 60, 512). AC-1 freeze regex at proposal.md:455 (`grep -c "Rule #" CLAUDE.md  # must return ≥ 9`) + tasks.md:39 (`grep -E "规则 #[1-9]"`) both updated. R-M6D-1 risk row at line 596 reads "Rules #1-#9 text (AD11 violation)" + threshold "≥ 9". | No over-replacement: standalone references to Rule #6, Rule #7, Rule #8, Rule #9, Rule #8 individually (e.g., proposal.md:95 "Rule #8 §exception", line 96 "Rule #9 §2.3", line 93 "Rules #7/8/9") preserved verbatim. |

---

## New findings (R3-introduced; should be 0)

### Critical
*(empty — no new Critical findings introduced)*

### Important
*(empty — no new Important findings introduced)*

---

## Convergence trajectory

- **R1 (4-agent combined audit)**: NEEDS_FIX 4/4. ~25 raw Critical findings de-duped to 10 themes + 5 X-Critical (cross-Spec dependency) findings.
- **R1-fix (commit 8a5fdc4)**: 10 themes + 5 X-Critical addressed across both Spec proposals + tasks.
- **R2 (3-agent challenge)**: split verdict — cr SCOPE_OK_R2 (23/23 R1 items closed) + ai SCOPE_OK_R2 (6/6) + **tl-critic NEEDS_FIX (2 NEW Critical self-spotted via cross-Spec verification + 1 paper-fix flagged)**. Independent verify (ls/grep on live filesystem) confirmed all 3 tl-critic findings TRUE.
- **R2-fix (commit c0e9d79)**: 2 NEW Critical (migration rename + gate args inversion) + 1 paper-fix completion. 4 proposal/tasks files modified, +106 / -45 net per diff stat.
- **R3 (this round, stability check)**: **0 new Critical + 0 new Important**. All 3 R2 fixes verified byte-for-byte CLOSED.

Net reduction R1 → R3: 25 raw + 5 X-Critical → 0. Convergence ratio 100%.

---

## Vote rationale

**R3_STABLE.** All three R2 fixes pass byte-level verification:

1. **Migration rename**: Zero stale `006_schema_v5` / `m006` / `Migration 006` references across both Spec #2 files. Filesystem-grounded check confirms slot 006 (M5's `006_schema_v4.2_add_spec_id.sql`, 2149 bytes) is untouched and slot 007 is empty (open for M6 creation). Additive schema progression v3 → v4 → v4 (drop_inline_uq) → v4.2 → v4.3 preserved. abi_compat contract intact.

2. **Gate args inversion**: Spec #3 T-B0.10 now uses 3-zone branching (PASS / REGRESSION / DIVERGENT) with explicit exit codes. PASS condition `git merge-base --is-ancestor "$MASTER_PTR" "$FEATURE_PTR"` is bit-exact match to dev-claude2 SoT line 86. Bash syntax validated (`bash -n` returns clean). Inline R3 fix-trail comment explains the inversion correction for future maintainers. Eliminates the false-negative pass-on-regression failure mode that would have silently rolled back the standards submodule pointer.

3. **Paper-fix propagation**: 12 sites updated from `#1-#6` / `6 条规则` to `#1-#9` / `9 条规则` across Spec #3 proposal.md + tasks.md. AC-1 freeze regex updated to `[1-9]` + threshold `≥ 9`. R-M6D-1 risk row reflects #1-#9. Two remaining `1-6` matches are both intentional historical fix-trail comments (proposal.md:80 R1-T3-1 + tasks.md:59 R1-I3-1) — both explicitly explain the prior `#1-#6` → `#1-#9` correction and must remain for audit trail accuracy. No over-replacement detected: standalone Rule #6, Rule #7, Rule #8, Rule #9 references (where each digit is a Rule identifier, not a range endpoint) preserved verbatim.

No new Critical or Important findings introduced by the R3 fix-pass. The "verify byte-for-byte" anti-paper-fix discipline (committed at R2) is upheld — every claimed closure has filesystem-grounded evidence (grep counts, line numbers, sed/diff extraction). The R2 split-verdict pattern (cr + ai already SCOPE_OK, only tl-critic NEEDS_FIX) does not regenerate at R3: zero new issues from any of the 3 agents' perspectives based on the focused R3 scope.

**Specs #2 (`aria-2.0-m6-e2e-resilience`) + #3 (`aria-2.0-m6-docs`) are ready for Phase A.3 → Approved status flip.** No further fix rounds required for these two sister Specs in the post_spec convergence audit.

---

## Files inspected

- `/home/dev/Aria/openspec/changes/aria-2.0-m6-e2e-resilience/proposal.md` (post-R3-fix)
- `/home/dev/Aria/openspec/changes/aria-2.0-m6-e2e-resilience/tasks.md` (post-R3-fix)
- `/home/dev/Aria/openspec/changes/aria-2.0-m6-docs/proposal.md` (post-R3-fix)
- `/home/dev/Aria/openspec/changes/aria-2.0-m6-docs/tasks.md` (post-R3-fix)
- `/home/dev/Aria/openspec/changes/aria-submodule-pointer-regression-gate/tasks.md` lines 78-95 (dev-claude2 SoT cross-ref)
- `/home/dev/Aria/aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/migrations/` (live filesystem state)
- `/home/dev/Aria/.aria/audit-reports/post_spec-R2-tl-critic-2026-05-24-aria-2.0-m6-sister-specs.md`
- `git diff 8a5fdc4..c0e9d79 --stat` (R2-fix commit, 4 spec files + 4 audit reports)
