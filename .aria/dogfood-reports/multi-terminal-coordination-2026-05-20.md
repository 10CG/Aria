# Dogfood Report — multi-terminal-coordination (Pending Execution)

> **Report type**: dogfood-pending (organic evidence captured; full execution gated on master merge)
> **Date**: 2026-05-20
> **Cycle ID**: `organic-spec-authoring-2026-05-20`
> **Layer L deployed**: No — `feature/multi-terminal-coordination` not yet merged to master
> **Verdict**: **PENDING** (coordination_ref not bootstrapped; Layer L awaits merge)
> **Task**: TASK-028 (tasks.md §3.6, detailed-tasks.yaml TASK-028)
> **Spec**: `openspec/changes/multi-terminal-coordination/`

---

## §1 Status Declaration

Layer L (`refs/aria/coordination`, claim CRUD, phase1_gate, reconcile) is complete and
tested on `feature/multi-terminal-coordination` but has not been merged to master. The
coordination orphan ref cannot be bootstrapped until at least one real post-merge session
calls `acquire_claim()` via the `phase1_gate` integration point.

**This report serves two purposes:**

1. **Organic dogfood evidence** — the spec authoring sessions (2026-05-19 to 2026-05-20)
   directly collided with the three race conditions that motivated this Spec. These are
   real, unscripted, production-traffic events, not synthetic tests. They constitute
   genuine dogfood evidence even though Layer L was not deployed to prevent them.

2. **Pending execution scaffold** — §5 documents the exact command to run after merge,
   the thresholds to measure against, and which table cells to fill in.

Per tasks.md §3.6 (c): dogfood reports MUST contain actual measured values. The section
§4 below contains the dry-run metric output from the instrumentation library run against
the current worktree state (2026-05-20T04:xx UTC).

---

## §2 Organic Dogfood Evidence — Three Real Race Events

The following three events occurred during the Spec authoring and P1/P2 implementation
sessions (2026-05-19 to 2026-05-20). Each maps 1:1 to a §Why item in `proposal.md` and
to a specific Layer in this Spec.

### Event 1 — Wrong-Baton Pickup (handoff branch-local siloing)

**What happened**: This session started on `master`. `docs/handoff/latest.md` at that
point pointed to `2026-05-16-spec-x-shipped-spec-y-kickoff.md` (Spec Y kickoff, 2 days
prior). However, the true most-recent handoff was
`docs/handoff/2026-05-17-evening-spec-y-phase-b-core-5-tasks.md`, committed on
`feature/spec-y-layer2-redo-mode-aux` at `2026-05-17T21:46:14Z` (git commit
`a2b6eaf`). That file existed only on the feature branch — master could not see it.

**Discovery method**: Manual `git show origin/feature/spec-y-layer2-redo-mode-aux:docs/handoff/2026-05-17-evening-spec-y-phase-b-core-5-tasks.md`
after noticing that "latest" handoff on master seemed 2 days stale relative to known
activity.

**Evidence in repo**:
- File `docs/handoff/2026-05-17-evening-spec-y-phase-b-core-5-tasks.md` — git log shows
  `a2b6eaf` commit at `2026-05-17T21:46:14+00:00` on `feature/spec-y-layer2-redo-mode-aux`.
- `docs/handoff/latest.md` on master at session start: pointed to 2026-05-16 doc.

**Layer H counterfactual**: With Layer H deployed, state-scanner Phase 1 collector would
have run `git fetch refs/heads/*` and scanned `docs/handoff/*.md` frontmatter on ALL
remote branches. The `feature/spec-y-layer2-redo-mode-aux` handoff would appear in the
track board as a separate track with `status: active`, `updated-at: 2026-05-17T21:46:14Z`,
`phase: B`. The session would have started with full situational awareness rather than a
2-day-old picture.

**Maps to**: proposal.md §Why #1, tasks.md §1.x (Layer H), tasks.md §3.6 (b) metric.

---

### Event 2 — Cross-Container Race + Push Reject (non-fast-forward)

**What happened**: This session ran Phase A commit + push for the multi-terminal-coordination
Spec. The first push attempt was rejected by origin with a non-fast-forward error. The cause:
another terminal had concurrently completed an entire Spec Y full Phase A→D cycle
(T2-T8 + 5 findings closed + Phase D archive) and pushed multiple commits to master. The
two terminals ran zero coordination; there was no claim, no awareness of parallel activity,
and no warning until the push rejection.

**Evidence in repo**:
- Commit `ce8ff55` (`2026-05-19T11:48:47Z`) — "docs(session): 2026-05-19 closeout — Spec Y
  full Phase A→D cycle COMPLETE" — was the commit that caused the non-fast-forward.
- The multi-terminal-coordination session's first push encountered this and had to
  fetch-rebase before re-pushing.

**Layer L counterfactual**: With Layer L deployed and `phase1_gate` active, the session
that picked up the Spec Y work would have called `acquire_claim(track_id="spec-y-...",
claimed_at=T1)`. When the multi-terminal-coordination session started, the Phase 1
state-scanner board would have shown `spec-y-layer2-redo-mode-aux: status=active,
owner=<other-container>, claimed_at=T1`. The multi-terminal-coordination session would
have known immediately that a parallel session was active on a different track.  The push
rejection would still have occurred (Layer L does not prevent pushes), but `failure_handlers.
resilient_push()` would have automatically executed the fetch-replay-repush retry protocol
(tasks.md §2.9(a)) rather than requiring manual intervention.

**Maps to**: proposal.md §Why #2, tasks.md §2.9 (a), tasks.md §3.6 (a) metric.

---

### Event 3 — Submodule Worktree Contamination (aria-orchestrator detached)

**What happened**: At session start, `aria-orchestrator` submodule was in a detached HEAD
state at commit `834c313`. This commit was neither on `master` nor on the
`feature/spec-y-layer2-redo-mode-aux` branch — it was from a prior stale checkout state
(identified from git submodule status as an older m4 commit). Work on the main worktree
with a detached submodule creates the risk of accidentally operating on stale submodule
code without realizing it.

**Mitigation taken**: A dedicated worktree was created at
`/home/dev/Aria/.git/worktrees/multi-terminal-coordination/` for P3 work, isolating it
from the main worktree state. This manual worktree creation is exactly what Design A
automates.

**Current submodule state** (after P2 bump): `aria-orchestrator` is now at
`962cb56` (`heads/master`), as confirmed by `git submodule status aria-orchestrator`.

**Design A counterfactual**: With Design A deployed, `count_concurrent_tracks()` detecting
≥2 active tracks in the same container would trigger `create_worktree(track_id=...)` with
an independent submodule checkout. The contamination scenario structurally cannot occur
within Design A's scope (same-container only — cross-container is out of scope per
DEC-20260519-001 #5).

**Maps to**: proposal.md §Why #3, tasks.md §3.1-§3.3 (Design A), tasks.md §3.6 context.

---

## §3 Counterfactual Analysis

If Layer L had been deployed to master before this session:

| Scenario | Without Layer L (observed) | With Layer L (counterfactual) |
|----------|---------------------------|-------------------------------|
| Session start — handoff orientation | Read 2-day-old `latest.md`; manually found real handoff via git show | state-scanner board shows all remote-branch tracks; `feature/spec-y-layer2-redo-mode-aux` track visible immediately |
| Parallel session awareness | None until push rejection | Phase 1 board shows `spec-y` track as `active` by other container; operator sees collision row if concurrent |
| Push non-fast-forward | Manual fetch-rebase required | `resilient_push()` executes fetch-replay-repush automatically (up to `NON_FF_MAX_RETRIES`) |
| Submodule detached state | Manual worktree creation required | Design A triggers `create_worktree()` when concurrent ≥2 tracks detected; isolated submodule checkout |
| Metric (a) — duplicate claims | Not measurable (no claim mechanism) | `coordination_ref.read_claims()` shows active_count per track_id; any >1 is immediately visible |
| Metric (b) — handoff freshness | All 24 existing files lack frontmatter; `delta_seconds=null` for all | Post-merge sessions write frontmatter; delta measured in seconds, not days |

**Summary**: Layer L compresses the race detection window from hours (push rejection) to
seconds (second fetch after claim push). Layer H eliminates the class of orientation error
where a session starts from a stale master-visible snapshot.

---

## §4 Measured Values (Dry Run — 2026-05-20)

The instrumentation library (`measure_multi_terminal.py`) was run against the current
worktree (`feature/multi-terminal-coordination`, HEAD `ce1032a`) at 2026-05-20 UTC.

### Metric (a) — Duplicate Active Claims

**Result**: BLOCKED — `coordination_ref_not_bootstrapped`

```
error: coordination_ref_not_bootstrapped: no claims to measure;
       run at least one real session that calls acquire_claim() first
per_track: {}
duplicates: []
max_active_per_track: null
```

**Interpretation**: refs/aria/coordination does not yet exist on this branch because no
session has run `phase1_gate` → `acquire_claim()` against it. This is the expected
pre-deployment state. The metric CANNOT be falsified until at least one real post-merge
session runs the gate. See §5 for the pending execution plan.

**NOT a failure**: absence of a coordination ref is the correct pre-merge state.

---

### Metric (b) — Handoff Freshness (frontmatter vs git log delta)

**Result**: Measured — 24 files scanned; 0 stale; all `delta=null` (no frontmatter)

```
per_file: 24 files scanned
files with git_last_commit_at: 24 (all files have git history)
files without frontmatter updated-at: 24 (all pre-Layer-H, expected)
files where delta_seconds >= 60: 0
max_delta_seconds: null (no frontmatter to compare against)
stale_files: []
```

**Interpretation**: All 24 existing handoff files predate Layer H (frontmatter schema
introduced in TASK-001/TASK-002, on `feature/multi-terminal-coordination`). They do not
have `updated-at` frontmatter, so `delta_seconds=null` for all. This is correct behavior:
the spec design says files without frontmatter are tagged as `legacy` and do not fail the
freshness check. The first handoff written by a session running on a post-merge master
(using the updated `aria/templates/session-handoff.md`) will be the first file with
measurable `delta_seconds`.

**Verification**: The script correctly identified all 24 files via git log, and all show
`git_last_commit_at` in the range `2026-04-23` to `2026-05-19`. No false positives.

---

### Metric (c) — Measurement Completeness

**Result**: PENDING (Layer L not yet deployed)

```
metric_c_complete: false
reason: metric_a blocked: coordination_ref_not_bootstrapped
```

Per tasks.md §3.6 (c): "dogfood report MUST contain actual measured values; 'absence of
failure' not acceptable as PASS evidence." The metric (b) dry-run above constitutes real
numeric measurement (24 files, 0 stale, max_delta=null). Metric (a) requires a bootstrapped
coordination ref. See §5.

---

### Metrics Framework Thresholds

| Metric | What is measured | Pass threshold | Fail condition |
|--------|-----------------|:--------------:|:--------------|
| (a) duplicate active claims | `status=active` claim count per `track_id` in `refs/aria/coordination` | ≤ 1 per track_id | Any track_id with count > 1 |
| (b) handoff freshness | `|frontmatter updated-at − git log latest commit time|` per `docs/handoff/*.md` | < 60s | Any file ≥ 60s |
| (c) completeness | Both (a) and (b) returned numeric data (not blocked) | Both produce non-null measurements | Either metric blocked by import/ref error |

**Constants source of truth**: `aria/skills/state-scanner/lib/constants.py`
(Finding #3 SOT: `HEARTBEAT_INTERVAL=600`, `STALE_TTL=1800`, `CLOCK_SKEW_WARN_THRESHOLD=30`).

The 60s threshold for metric (b) is chosen to be 2× the typical git push + clock rounding
margin while still catching the multi-minute-to-multi-day staleness that the wrong-baton
problem produces.

---

## §5 Pending Execution — Post-Merge Instructions

**Trigger**: After `feature/multi-terminal-coordination` merges to master and the first
real session runs `phase1_gate` → `acquire_claim()`.

**Step 1 — Bootstrap verification**

```bash
git -C /path/to/Aria fetch origin refs/aria/coordination:refs/aria/coordination
git -C /path/to/Aria cat-file -t refs/aria/coordination  # should print "commit"
```

If `refs/aria/coordination` exists, at least one session has run the gate. Proceed.

**Step 2 — Run instrumentation**

```bash
# From Aria main repo root:
python3 .aria/scripts/dogfood/measure_multi_terminal.py \
    --repo-path /path/to/Aria \
    --cycle-id  post-p3-merge-$(date -u +%Y-%m-%d) \
    --output    .aria/dogfood-reports/multi-terminal-coordination-$(date -u +%Y-%m-%d).md \
    --json-output .aria/dogfood-reports/multi-terminal-coordination-$(date -u +%Y-%m-%d).json
```

Exit code 0 = metric_c_complete (measurements ran; see report for PASS/FAIL).
Exit code 1 = still PENDING (coordination ref not bootstrapped).

**Step 3 — Fill in this table** (copy to the output report or update §4 in a new report):

| Metric | Pending value | Post-run value | Pass? |
|--------|:-------------:|:--------------:|:-----:|
| (a) max_active_per_track | `null` | _______ | _____ |
| (a) duplicates | `[]` | _______ | _____ |
| (b) max_delta_seconds | `null` | _______ | _____ |
| (b) stale_files | `[]` | _______ | _____ |
| (c) metric_c_complete | `false` | _______ | _____ |
| Overall verdict | PENDING | _______ | _____ |

**Step 4 — Acceptance criterion** (from tasks.md §3.6):

- ≥1 dogfood cycle complete (a real session ran `phase1_gate`)
- Actual measured values appear in report (not absent-of-failure)
- No duplicate claims (`duplicates == []` in metric_a)
- No stale handoffs (`stale_files == []` in metric_b, or all stale entries have explanations)

---

## §6 References

| Item | Path |
|------|------|
| Spec proposal | `openspec/changes/multi-terminal-coordination/proposal.md` |
| Spec tasks | `openspec/changes/multi-terminal-coordination/tasks.md §3.6` |
| Detailed tasks | `openspec/changes/multi-terminal-coordination/detailed-tasks.yaml TASK-028` |
| TASK-027 benchmark result | `aria-plugin-benchmarks/ab-results/2026-05-20T042320Z-multi-terminal-coordination/benchmark-result.json` |
| P1 closeout | `.aria/notes/multi-terminal-coordination-p1-closeout.md` |
| P2 closeout | `.aria/notes/multi-terminal-coordination-p2-closeout.md` |
| Instrumentation library | `.aria/scripts/dogfood/measure_multi_terminal.py` |
| Shadowed handoff (Event 1 evidence) | `docs/handoff/2026-05-17-evening-spec-y-phase-b-core-5-tasks.md` |
| Concurrent push commit (Event 2 evidence) | git commit `ce8ff55` on `feature/spec-y-layer2-redo-mode-aux` |
| constants SOT (Finding #3) | `aria/skills/state-scanner/lib/constants.py` |
| Decision record | `docs/decisions/DEC-20260519-001-multi-terminal-coordination.md` |

---

*Report generated: 2026-05-20. Layer L on `feature/multi-terminal-coordination` (HEAD `ce1032a`).
Instrumentation dry-run confirms metric-b correctly handles 24 pre-Layer-H legacy handoff files
(all delta=null, 0 false stale). Metric-a requires post-merge session execution.*
