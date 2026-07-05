# Interactive Session Dedup — Pre-Registered Decision Rules (TASK-014)

> **Spec**: `openspec/changes/interactive-session-dedup-coordination` (DEC-20260704-002)
> **Harness**: [`dedup_harness.py`](./dedup_harness.py) (TASK-013)
> **Pre-registration**: thresholds fixed BEFORE running the AB harness, per
> `feedback_static_benchmark_unfit_as_oneshot_selection_gate` — the harness result
> must not be able to retro-fit its own pass bar.

## Why pre-register

The dedup mechanism has **three candidate trigger arms** (how session B's Layer L
gate gets invoked). Only one is shipped live in Phase B; the others are adopted
(or dropped) based on the harness. Pre-registering the pass bar prevents
"harness-gaming" (tuning the bar to whatever the run produced).

## Trigger arms

| arm | how B's gate fires | Phase B status |
|-----|--------------------|----------------|
| **manual**  | AI/human calls the `phase1_gate` CLI at Phase-B entry (state-scanner 阶段 2 编排层) | **live** — shipped in Phase B; the runtime-probe (TASK-012) asserts this arm is actually invoked in production |
| **semi**    | gate invoked after B starts some work (later in the race window) | **pending** — adopt only if it clears the bar below |
| **auto**    | gate fires automatically at scan time | **pending** — adopt only if it clears the bar below |
| **control** | gate never called (the pre-DEC-002 #94 world) | **baseline** — must show missed collisions (falsifiability check) |

## Pass bar (fixed pre-run)

A candidate arm (semi / auto) is **adopted** iff ALL hold over the harness run:

| metric | threshold | rationale |
|--------|-----------|-----------|
| **detection rate** | ≥ **0.90** | `surfaced / (surfaced + missed)` — must catch ≥90% of genuine collisions |
| **false-positive rate** | ≤ **0.05** | surfacing a collision when none exists erodes trust (advisory fatigue) |
| **friction** | ≤ **500 tokens / claim** | the gate's cost per invocation must stay cheap enough not to deter use |

Plus the harness itself must be **falsifiable**: the `control` arm MUST report
≥1 `collision_missed`, otherwise a 100% detection headline is meaningless (the
harness can't tell a hit from a miss). `dedup_harness.py` exits non-zero if the
control arm misses zero collisions.

## Manual arm = the P1 live arm

`manual` is NOT gated on this harness — it is the arm shipped in Phase B and the
one the **runtime-invocation probe (TASK-012)** watches: the probe asserts the
production telemetry partition has ≥1 `source=production` record, i.e. the manual
arm is genuinely invoked in production, not just green in a test. This is the
anti-dead-code guarantee (aria-plugin #95): the mechanism cannot silently rot
back into dead code without the probe flipping to FAIL.

## Follow-up (post-AB)

- If `semi` and/or `auto` clear the bar → a follow-up task wires that arm's
  trigger into state-scanner and re-points the probe.
- If neither clears it → `manual` remains the sole live arm; auto/semi are
  dropped and the harness result is archived as the negative evidence.
- Either way the decision is recorded in the ship handoff + this file is updated
  with the observed numbers (kept append-only for auditability).

## Observed numbers (synthetic baseline, deterministic)

First deterministic run (`--trials 20`, ground-truth-known synthetic collisions):

First deterministic run (`--trials 20`, half the trials seed a genuine collision,
half do not — so the false-positive branch is actually exercised):

| arm | detection | false-positive | friction | status |
|-----|-----------|----------------|----------|--------|
| manual  | 1.00 | 0.00 | ~1 tok | **live** — real `run_gate_synthetic`, meets bar |
| semi    | 1.00 | 0.00 | ~1 tok | **stub** — code == manual; NOT differentiated |
| auto    | 1.00 | 0.00 | ~1 tok | **stub** — code == manual; NOT differentiated |
| control | 0.00 | 0.00 | 0 | **baseline** — 10/10 collisions missed (falsifiable ✅) |

> ⚠️ **Honest scope** (audit fix): these are **synthetic** numbers (mocked claim
> state, deterministic). `semi` and `auto` share `manual`'s exact code path —
> their timing model lives in prose only and is NOT yet implemented, so their
> identical numbers are construction, not measurement. They are marked `stub`,
> not "clears bar". Promoting `semi`/`auto` from stub to live requires a REAL
> per-arm timing implementation + a live AB run under genuine 双子星 concurrency.
> The harness's validity gate now requires BOTH (1) the control arm to miss
> collisions (falsifiable) AND (2) the live `manual` arm's real gate to clear
> detection≥0.90 / fp≤0.05 — so it cannot pass on a broken gate or a broken
> control.
