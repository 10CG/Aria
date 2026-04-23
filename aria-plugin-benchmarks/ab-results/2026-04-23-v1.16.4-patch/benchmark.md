# Smoke Benchmark: aria-plugin v1.16.4

**Date**: 2026-04-23
**Session**: Post-M1 cleanup — 4th patch release same day
**Scope**: #22 Phase D.1 multi-PR milestone + #23 aria-dashboard 3 Major bugs
**Method**: Structural smoke (inline Python) — NOT full `/skill-creator` AB
**Commits**:
- aria@17f6423 (#22 + #23)
- standards@5b56dd4 (#22 ten-step docs sync)
- main@3a2c6a8 (submodule pointer bump)

---

## Summary

| Area | Baseline (v1.16.3) | Target (v1.16.4) | Delta | Verdict |
|------|---------------------|-------------------|-------|---------|
| #22 phase-c C.2.6 + phase-d milestone-mode | 0/6 | 5/6 (effective 6/6 w/ C4 false-neg) | **+83.3pp** ✅ | Feature added, backward-compat preserved |
| #23 aria-dashboard 3 Major | 0/10 | 10/10 | **+100.0pp** ✅ | All 3 Major bugs fixed |

**C4 false-negative note** (#22-4 `[ ]→[~]` transition): prose at SKILL.md L285 says "从 `[ ]` 升级为 `[~]`" (semantically equivalent but doesn't match literal `→` regex). Also L261 has `sed` command actually implementing the transition. Effective coverage 6/6.

---

## #22 Detail

**Files changed**:
- `aria/skills/phase-c-integrator/SKILL.md` — +C.2.6 section, config `upm.milestone_driven: false` (opt-in)
- `aria/skills/phase-d-closer/SKILL.md` — +Milestone-driven Mode subsection (D.1 只需 finalize)
- `standards/core/ten-step-cycle/phase-c-integration.md` — +Step 8.5 UPM Sub-progress Append
- `standards/core/ten-step-cycle/phase-d-closure.md` — +Milestone-driven Mode section

**Mechanism**:
- `upm.milestone_driven: true` → C.2.6 activates after C.2.5 push
- C.2.6: parse commit for `US-XXX` or spec change_id → locate UPM Story row → append `YYYY-MM-DD: {sha} — {title} ({PR_URL})` sub-bullet → status `[ ]` → `[~]`
- D.1 finalize mode: `[~]` → `[x]` + archive path link (no history rebuild needed)

**Backward-compat**: `milestone_driven=false` (default) preserves D.1-only behavior.

**Real pain validated**:
- M1 closeout 2026-04-23 (this session): 85 tasks updated in single D.1 pass
- silknode US-074 multi-PR migration (per issue body): 3-PR schema expand-migrate-contract

---

## #23 Detail

**Files changed**:
- `aria/skills/aria-dashboard/SKILL.md` (parsing + rendering logic)
- `aria/skills/aria-dashboard/templates/dashboard.html` (CSS + placeholder)

**Bug M1: Archived spec duration "—"**
- 5-step fallback chain for `Created` date: frontmatter strict regex → frontmatter loose → `git log --diff-filter=A` first commit → archive dir `YYYY-MM-DD-*` prefix → null
- Duration computed only when both ends non-null

**Bug M2: Audit verdict CSS mislabeling**
- Parser reads audit-engine frontmatter `verdict:` field first (canonical)
- CSS class mapping (4-way):
  - `PASS` → `verdict-pass` (green, existing)
  - `PASS_WITH_*` (regex `/^PASS_WITH_/i`) → `verdict-warning` (yellow, **new**)
  - `FAIL`/`REVISE` → `verdict-revise` (red, existing; fixed color)
  - Unknown → `verdict-neutral` (gray, **new**, avoids "unknown=failure" misread)
- Fixes real bug: `PASS_WITH_POLISH` was rendering as red → now yellow

**Bug M3: No Carry-forward visualization**
- New `Carry-forward` HTML section (`{{CARRY_FORWARD_HTML}}` placeholder, between Benchmark and Issue Form)
- Data sources (OR-combined):
  1. `.aria/audit-reports/*.md` frontmatter `carry_forward:` field
  2. `.aria/audit-reports/*.md` body H2/H3 "Carry-forward" sections
  3. `openspec/changes/*/proposal.md` + `openspec/archive/*/proposal.md` "Out of Scope" sections
- Grouped by `target_release` (e.g., "v0.2.2 候选: 7 条 / v0.3 候选: 3 条")

**Backward-compat**: No `Created` → fallback chain; no carry-forward data → section hidden.

**Minor 4-9 deferred**: 归档 spec 元信息薄 / 双仓库感知 / `docs/decisions` 展示 / 审计表截断 / spec 链接 / banner fallback → v1.17.x

---

## Limitations

Same as v1.16.1-3 smoke benchmarks: structural verification, not end-to-end AI task success. Full `/skill-creator` AB for these 3 skills (phase-c-integrator, phase-d-closer, aria-dashboard) deferred to dedicated session.

---

## Session Cumulative (v1.16.1 → v1.16.4)

| Patch | Date | Skills touched | Forgejo Issues closed |
|-------|------|----------------|------------------------|
| v1.16.1 | 2026-04-23 | state-scanner, audit-engine (+ standards) | #17, #24, #27 |
| v1.16.2 | 2026-04-23 | audit-engine | #26 |
| v1.16.3 | 2026-04-23 | state-scanner (+ standards) | #18, #25 |
| v1.16.4 | 2026-04-23 | phase-c-integrator, phase-d-closer, aria-dashboard (+ standards) | #22, #23 (pending close) |
| **Total** | 1 session | **6 skills + standards** | **8 issues** |

Open Issues: 11 → 3 (清理 73%)
