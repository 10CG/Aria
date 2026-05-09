# State Scanner Recommendation — Bench Fixture (arm_B v1.17.7 + T5 fallback)

## Snapshot Summary (from `/tmp/bench-snapshot-v117t5.json`)

- **Project root**: `/tmp/state-scanner-bench-fixture`
- **Git**: branch `master`, working tree clean (0 staged / 0 unstaged / 0 untracked), no upstream configured
- **Recent commits**: `e40043e Fix US-042 status placement`, `8166d41 Initial bench fixture`
- **OpenSpec**: not configured (0 changes / 0 archive)
- **Architecture docs**: absent
- **Audit**: not enabled
- **Interrupt**: none
- **Requirements**: configured — 2 user stories
  - US-042 (in_progress)
  - US-043 (pending)
- **UPM**: configured; `current_phase=PhaseB`, `current_cycle=Cycle3`, `active_module=backend`
- **Snapshot completeness**: v1.17.7+T5 — no `upm.followups[]`, no `upm.handoff_doc`, no `requirements.stories.priority_items[]` collectors. Snapshot alone would point to "feature_new" (clean tree, no spec drafts) and miss the real backlog.

## T5 Fallback Triggered

All four conditions hold simultaneously:

1. `git.status_clean == true` (uncommitted_count=0; no staged/unstaged/untracked)
2. `audit.has_unconverged == false` (audit.enabled=null, no unconverged signals)
3. No `commit_only` / `quick_fix` rule matches (no diff to commit, no hotfix branch heuristic)
4. `requirements.upm.configured == true` and `requirements.upm.raw_block != null`

→ Per SKILL.md, must Read UPM full text + grep handoff regex before recommending. Did so.

## Surfaced via UPM Read (`docs/project-planning/unified-progress-management.md`)

**Pending Followups table (priority-ordered):**

| Priority | Item | Tracking | Next Action |
|----------|------|----------|-------------|
| P1 | Hotfix auth race condition | incident#9 (active) | deploy |
| P1 | Ship payment gateway integration | issue#42 (sprint-3) | review |
| P2 | Refactor user model | backlog | none |
| P2 | Improve test isolation | issue#67 (backlog) | scope |
| P3 | Doc update for new API | wiki | author |
| P3 | Cleanup deprecated endpoints | issue#88 (backlog) | review |

**Handoff regex hit** → `docs/handoff/2026-05-09-bench-handoff.md`:

- Last cycle: shipped TX.0 status_clean; started TX.1 schema doc
- Next session priorities (explicit):
  1. Review P1 followups (auth + payment)
  2. Continue US-042 implementation

## Top Priorities (T5-corrected, NOT raw snapshot)

1. **P1 — Hotfix auth race condition** (incident#9 active, next action: deploy). Highest urgency: active incident.
2. **P1 — Ship payment gateway integration** (issue#42 sprint-3, next action: review). Sprint-bound, review-ready.
3. **Continue US-042** (in_progress per snapshot + handoff doc). Already mid-flight; finishing avoids context loss.

P2/P3 items remain in backlog; defer until P1 + US-042 settle.

## Suggested Workflow

**NOT** `feature_new` (which raw snapshot would default to). Instead:

- **Phase A.0 → A.1 (Spec for auth hotfix)**: Treat incident#9 as the next change. Run `/spec-drafter` to author Level 2/3 OpenSpec for the auth race fix (criticality + handoff explicit "deploy" action warrants a spec for traceability, even on hotfix path).
- **Phase B (resume)**: After auth ships, resume **US-042 implementation** per handoff §"Next session priorities #2". Snapshot already shows US-042 in_progress; check existing branch/worktree state via `/branch-manager` before opening new work.
- **Parallel review track**: Payment gateway (issue#42) is review-stage — dispatch `/requesting-code-review` (aria:code-reviewer agent) on the existing PR rather than re-opening dev work.
- **Defer**: P2/P3 items, doc cleanup, deprecated endpoint removal — backlog until P1 closure.

**Why this differs from snapshot-only output**: Raw v1.17.7+T5 snapshot has clean tree + no specs + UPM PhaseB → naive rule would suggest `feature_new` or `phase_b_resume` against `active_module=backend` generically. T5 Read surfaces (a) an active incident requiring deploy, (b) a sprint-bound review-ready PR, and (c) explicit handoff-doc priority ordering — all invisible to the field-only view.
