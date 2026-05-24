# aria-submodule-pointer-regression-gate — Phase C.2.4.5 (B+) hardened pre-merge gate

> **Level**: 3 (Full — Skill behavior change + replay test fixtures + convention doc + 2-phase rollout + tripwire mechanism)
> **Status**: ✅ **Approved** (Phase A.2 CONVERGED 2026-05-24 via R2 unanimous 3/3 CONVERGED + 0 new Critical; ready for Phase A.3 → Phase B.1)
> **Change ID**: `aria-submodule-pointer-regression-gate`
> **Parent Forgejo issue**: [Aria #124](https://forgejo.10cg.pub/10CG/Aria/issues/124)
> **Source incident**: 2026-05-23 PR #123 silent submodule pointer regression (commit `6fea5d7`) caught by post-merge audit + fast-forward fix `a8e0096`
> **Brainstorm Source**: [DEC-20260524-002](../../../.aria/decisions/2026-05-24-aria-124-submodule-pointer-regression-gate.md) — 4 R1 agents + 3 R2 reversals (tech-lead + code-reviewer mutual concession) + ai-engineer R2 neutral 3rd path unified anchor + 4 R3 unanimous ACCEPT_R3 + 3 Q-NEW MINOR (all resolved in this Spec)
> **Predecessor Spec (incident origin)**: [aria-layer2-docker-auth-cold-pull-fix](../../archive/2026-05-23-aria-layer2-docker-auth-cold-pull-fix/) (archived 2026-05-23, where PR #123 incident occurred)
> **Effort baseline**: ~9h Phase B impl (T-gate ~2.5h + T-override ~1h + T-telemetry ~0.5h + T-replay ~3.5h + T-convention ~0.5h + T-rollout ~0.5h + T-rule6 ~1h + T-tripwire ~0.5h) + ~3.5h Phase A.2-A.3 audit/allocation + ~2h Phase C+D = **~15h end-to-end** across 2-3 sessions
> **Target version**: aria-plugin **v1.28.0** (warn-only) → **v1.29.0** (block flip, 14d hard date after v1.28.0 ship OR FP threshold <2% over 20+ WOULD-BLOCK events with ≥3 minimum-observation guard)
> **Modified Skill**: `aria/skills/phase-c-integrator/SKILL.md` — **NEW sub-step §C.2.4.5 inserted between existing §C.2.4 (Rule #8 `aether ci status` gate) and existing §C.2.5 (Multi-Remote Push Enforcement, v1.15.0+)**. No existing section is renumbered; minimal-cascade insertion per Rev1 R1-tl-1 fix.
> **NEW convention doc**: `standards/conventions/submodule-pointer-hygiene.md` (zero-code (C) doc, NOT Rule #10 — convention SOT only)
> **NEW telemetry directory**: `aria/metrics/` (created on first run if absent — see T-telemetry-0)
> **Tripwire observer location**: `.forgejo/workflows/submodule-gate-tripwire.yml` in `10CG/Aria` main repo (weekly cron — NOT `aria/cron/` in aria-plugin per Rev1 R1-tl-3 fix)
> **Risk class**: Backward-compatible per `向后兼容` Aria principle — v1.28.0 ships in warn-only mode (logs WOULD-BLOCK, doesn't refuse merge); ecosystem has 14d to surface false positives before v1.29.0 flips to block.

> **Audit trajectory** (R1 audit completed 2026-05-24T~14:59Z):
>   - **Phase A.2 R1** (2026-05-24, 4-agent parallel: tech-lead + backend-architect + qa + knowledge-manager): **PASS_WITH_WARNINGS 4/4 unanimous** — 4 Critical + 19 Important + 20 Minor. Aggregate report: `.aria/audit-reports/post_spec-R1-2026-05-24T1459Z-aria-submodule-pointer-regression-gate.md`
>   - **Phase A.2 Rev1 applied** (2026-05-24, this commit): 4 Critical (C-tl-1 numbering / C-tl-2 placement / C-tl-3 tripwire location / C-km-1 memory refs) + ~10 Important addressed inline
>   - **Phase A.2 R2** (2026-05-24T~15:15Z, 3-agent parallel: tech-lead + qa + code-reviewer-NEW): **CONVERGED 3/3 unanimous** — all 4 R1 Critical CLOSED + 11 new Minor (all cosmetic / spec polish / batch-fixable Phase B.1). Aggregate report: `.aria/audit-reports/post_spec-R2-2026-05-24T1515Z-aria-submodule-pointer-regression-gate.md`
>   - ✅ **CONVERGED** 2026-05-24 — per `feedback_post_spec_audit_pragmatic_convergence` 收敛准则 (unanimous + verdict 改善 + 无振荡 + 0 new Critical) + Level 2/3 pragmatic baseline (R1→R2 unanimous, no R3 needed)

---

## Why

**Direct incident** (2026-05-23, PR #123 in `10CG/Aria`):
Track E Spec `aria-layer2-docker-auth-cold-pull-fix` Phase B rebased PR #123 against master. During rebase conflict resolution on submodule pointer `aria`, executor ran:

```bash
git checkout origin/master -- aria
```

**But the local `origin/master` ref had not been refreshed** (no `git fetch` before the checkout). Staged aria pointer was a stale SHA (`3b688a9`). When merged, this **silently reverted 4 dev-claude2 commits** shipped from the parallel terminal:
- aria-plugin v1.24.1
- atomicity-guard bidirectional regex forbid
- aria-plugin v1.25.0
- aria-plugin v1.26.0

Caught by post-merge audit + fast-forward fix `a8e0096` in ~10 minutes. If audit had been delayed:
- dev-claude2's hook performance optimization work invisibly reverted
- Plugin marketplace (pulls from GitHub mirror) sees old version
- Every fresh clone of master is broken until detected
- Possibly multi-day silent data loss window

**Root cause analysis**:
1. Stale local `origin/master` ref (no fetch before rebase)
2. Rebase conflict-resolution shortcut (`git checkout origin/master -- <path>`) trusts the stale ref
3. **Layer L 6-rule reconcile** (multi-terminal-coordination v1.22.0+) covers orphan ref claim conflicts but does **not** cover submodule pointer write conflicts during PR rebase

**Class of incident**: any rebase that resolves submodule pointer conflict from stale `origin/<branch>` ref will silently regress unless caught by manual audit. Aria's master is consumed downstream (plugin marketplace, fresh-clone workflows); silent regressions there have user-visible impact.

**Why mechanical gate (not docs alone)**:
- Operator workflow discipline already exists (Layer L 6-rule + convention reading), but human-only enforcement fails under time pressure
- Post-merge audit caught this incident, but audit is bursty manual activity — at N=2 incidents we cannot guarantee both will be caught
- Pre-merge mechanical gate eliminates the failure mode at the merge transaction itself

---

## What

This Spec ships **5 deliverables** in a single change unit, bundled because they are interdependent (gate logic, override mechanism, test fixtures, convention doc, rollout strategy):

### A. (B+) hardened pre-merge gate

**Hook point** (Rev1 R1-tl-2 fix): NEW sub-step **§C.2.4.5** in `aria/skills/phase-c-integrator/SKILL.md`, inserted between existing §C.2.4 (Rule #8 `aether ci status` gate) and existing §C.2.5 (Multi-Remote Push Enforcement, v1.15.0+). **Pre-merge** — invoked by phase-c-integrator BEFORE the branch-manager merge API call, AFTER §C.2.4 CI gate passes. If §C.2.4.5 blocks, merge never executes. (Existing §C.2.5 Multi-Remote Push runs POST-merge and is untouched by this Spec.)

Mechanism (Bash):

```bash
# Step 1 — fail-loud fetch (mandatory, exit-code-only abort per AD-FOLLOWUP-1 / backend-architect R3 Q-NEW-1)
# Rev1 R1-ba-1 fix: use bare `git fetch origin` (NOT `git fetch origin master`) — the bare form
# updates origin/master remote-tracking ref reliably. `git fetch origin master` updates FETCH_HEAD
# but does NOT advance origin/master in general, defeating Step 2 refspec assertion.

# Capture BEFORE (Rev1 R1-ba-2 fix: BEFORE must be captured BEFORE fetch, not after)
BEFORE_REMOTE=$(git rev-parse origin/master 2>/dev/null || echo "FIRST_RUN")

# Wait_recoverable bounded retries (Rev1 R1-tl-3 fix: drop stderr regex classifier, use bounded retry)
RETRY_DELAYS=(1 2 4)  # exponential backoff, 3 attempts total
for delay in "${RETRY_DELAYS[@]}"; do
    if git fetch origin 2>&1; then
        FETCH_OK=1
        break
    fi
    sleep "$delay"
done
if [[ "${FETCH_OK:-0}" != 1 ]]; then
    echo "BLOCK: git fetch origin failed after 3 attempts (1s/2s/4s backoff). Submodule pointer ancestry cannot be verified safely." >&2
    echo "       Manual remediation: investigate auth (PAT expiry?), network connectivity, or origin URL drift, then retry merge." >&2
    log_gate_telemetry "FETCH_FAILURE" "$BEFORE_REMOTE" "(unknown)" "fetch_exhausted_retries"
    exit 1
fi

# Step 2 — refspec assertion (Rev1 R1-ba-2 fix: AFTER captured strictly after fetch)
AFTER_REMOTE=$(git rev-parse origin/master)
# If expected-to-advance (e.g., upstream had new commits per `git log HEAD..origin/master`)
# and BEFORE == AFTER → abort with operator confirm

# Step 3 — per-submodule fetch + 双向 ancestry check
for SUBMODULE in $(git config --file .gitmodules --get-regexp path | awk '{print $2}'); do
    git -C "$SUBMODULE" fetch origin

    FEATURE_PTR=$(git ls-tree HEAD "$SUBMODULE" | awk '{print $3}')
    MASTER_PTR=$(git ls-tree origin/master "$SUBMODULE" | awk '{print $3}')

    # nil-SHA handling: first-time submodule (empty ls-tree output on master)
    if [[ -z "$MASTER_PTR" ]]; then
        echo "INFO: $SUBMODULE first introduced on this PR, no prior gitlink to compare. Gate passes."
        continue
    fi

    # No-change: same pointer trivially OK
    if [[ "$FEATURE_PTR" == "$MASTER_PTR" ]]; then
        echo "OK: $SUBMODULE pointer unchanged ($FEATURE_PTR)"
        continue
    fi

    # Visible SHA diff print (Hardening 3, every run)
    echo "GATE: submodule=$SUBMODULE master=$MASTER_PTR feature=$FEATURE_PTR"

    # 主 ancestry check: is MASTER_PTR an ancestor of FEATURE_PTR (= forward bump)?
    if git -C "$SUBMODULE" merge-base --is-ancestor "$MASTER_PTR" "$FEATURE_PTR" 2>/dev/null; then
        echo "PASS: $SUBMODULE forward bump"
        continue
    fi

    # Not forward — check if FEATURE_PTR is ancestor of MASTER_PTR (= regression)
    if git -C "$SUBMODULE" merge-base --is-ancestor "$FEATURE_PTR" "$MASTER_PTR" 2>/dev/null; then
        VERDICT="REGRESSION"
    else
        VERDICT="DIVERGENT"
    fi

    # Check override (per-PR commit trailer OR PR label)
    if check_override_trailer "$SUBMODULE" "$MASTER_PTR" "$FEATURE_PTR"; then
        echo "ALLOW: $SUBMODULE $VERDICT overridden by commit trailer (audit logged)"
        log_override_audit "$SUBMODULE" "$VERDICT" "$MASTER_PTR" "$FEATURE_PTR"
        continue
    fi

    if check_pr_label "submodule-rollback-approved"; then
        echo "ALLOW: $SUBMODULE $VERDICT overridden by PR label (audit logged)"
        log_override_audit "$SUBMODULE" "$VERDICT" "$MASTER_PTR" "$FEATURE_PTR"
        continue
    fi

    # No override — block (v1.29.0+) OR warn (v1.28.0)
    if [[ "$ARIA_SUBMODULE_GATE_MODE" == "warn" ]]; then
        echo "WOULD-BLOCK: submodule=$SUBMODULE master=$MASTER_PTR feature=$FEATURE_PTR reason=$VERDICT"
        log_warn_telemetry "$SUBMODULE" "$VERDICT" "$MASTER_PTR" "$FEATURE_PTR"
    else
        echo "BLOCK: $VERDICT — submodule=$SUBMODULE master=$MASTER_PTR feature=$FEATURE_PTR" >&2
        echo "       To override: add commit trailer 'Submodule-Rollback: $SUBMODULE $MASTER_PTR→$FEATURE_PTR reason=<reason>'" >&2
        echo "       Or add PR label 'submodule-rollback-approved'" >&2
        exit 1
    fi
done
```

**Race scenario** (per backend-architect R3 missing scenario #9): concurrent force-push to `origin/master` during gate execution → refspec assertion (Step 2) compares before/after rev-parse; if change is legitimate ancestry-forward, gate continues; if force-push rewrote history non-ancestor, gate detects and aborts with operator confirm.

### B. Override mechanism (per-PR explicit only)

Two ways to override gate when shipping legitimate revert:

**Option 1 — commit trailer** in the merge commit message (preferred — per-commit explicit justification):
```
Submodule-Rollback: aria a8e0096→3b688a9 reason=v1.24.1 introduced critical regression in hook X
```

ASCII alternative (per Rev1 R1-ba-4 fix — UTF-8 fragility in non-UTF-8 locales LANG=C/POSIX):
```
Submodule-Rollback: aria a8e0096->3b688a9 reason=v1.24.1 introduced critical regression
```

Both forms are accepted by the parser. Convention doc documents both. SHA can be short (≥7 chars) — parser resolves via `git rev-parse` before comparison (Rev1 R1-qa M-qa-5 fix).

**Option 2 — PR label** `submodule-rollback-approved` (settable only by repo maintainers via Forgejo):
- Lower granularity (PR-level not commit-level)
- For multi-commit reverts where trailer would clutter

**NOT supported**: sticky config flag (`.aria/config.json` `gate.disable=true`). Sticky flags get forgotten on permanently, defeating the gate. This mirrors Rule #7 `secret-leak-ok-explicit` pattern — per-instance justification required, no global escape hatch.

Override audit log entry: written to `aria/metrics/submodule-gate-overrides.json` (append-only) with `{timestamp, pr_id, submodule, master_sha, feature_sha, verdict, reason, override_type}`. Monthly review of override usage rate (qa R1 metric): if >15% gate fires use override → re-audit gate sensitivity.

### C. Measured tripwire pre-commitment (codified §Risks)

Auto-promote **(A) post-merge backward-move detector** without re-brainstorm if any of:

1. Any submodule pointer regression escapes (B+) within next **12 months** OR **100 merges** (whichever first)
2. Any (B+) fetch-failure incident manifests in audit logs (degraded mode triggered)
3. Any non-PR-flow regression observed (direct master push bypassing PR + §C.2.4.5)

**Counter mechanism** (per code-reviewer Q-NEW-1): tracked in `aria/metrics/submodule-gate-misses.json` (mechanical, append-only) with `{timestamp, miss_type, pr_id_if_known, master_sha, feature_sha, detected_by}`.

**Monitoring observer** (per qa Q-NEW-1; Rev1 R1-tl-3 fix — proposal/tasks contradiction resolved): weekly Forgejo Actions workflow at **`.forgejo/workflows/submodule-gate-tripwire.yml` in `10CG/Aria` main repo** (NOT `aria/cron/` in aria-plugin). Bash logic in workflow runs:
```bash
# Compare master HEAD~1 vs HEAD submodule gitlinks for ancestry
for SUB in $(git config --file .gitmodules --get-regexp path | awk '{print $2}'); do
    OLD=$(git ls-tree HEAD~1 "$SUB" | awk '{print $3}')
    NEW=$(git ls-tree HEAD "$SUB" | awk '{print $3}')
    if [[ -n "$OLD" && -n "$NEW" && "$OLD" != "$NEW" ]]; then
        if ! git -C "$SUB" merge-base --is-ancestor "$OLD" "$NEW" 2>/dev/null; then
            # Regression escaped (B+) — append to misses.json + file Forgejo issue
            ...
        fi
    fi
done
```

This addresses qa R3 concern about "dead tripwire" — the observer fires regardless of human attention.

### D. (C) convention doc (zero code)

New file `standards/conventions/submodule-pointer-hygiene.md`. Content:
- "Always `git fetch origin` before any rebase that may touch submodule pointers"
- "Never resolve submodule pointer conflict via `git checkout origin/<branch> -- <sub>` without explicit `git fetch` immediately prior in the same shell session"
- "If conflict resolution requires a stale ref (deliberate revert), abort the rebase and use the override mechanism (commit trailer or PR label) instead"
- Cross-reference to phase-c-integrator §C.2.4.5 + this Spec

**NOT added as numbered Rule** in `CLAUDE.md` (per code-reviewer R3 — Rules #1-#9 already heavy; convention SOT in `standards/conventions/` is sufficient).

### E. Two-phase rollout

| Phase | Version | Mode | Behavior | Duration |
|-------|---------|------|----------|----------|
| Warn-only | aria-plugin **v1.28.0** | `ARIA_SUBMODULE_GATE_MODE=warn` (default) | Logs `WOULD-BLOCK` to telemetry, does NOT refuse merge | 14 calendar days OR until FP threshold judged stable |
| Block | aria-plugin **v1.29.0** | `ARIA_SUBMODULE_GATE_MODE=block` (default) | Refuses merge with exit 1 + remediation hint | Permanent |

**Flip decision criteria** (per qa R3 + code-reviewer R3 concerns about indefinite warn-only):
- **FP rate < 2%** computed as `FP_count / total_WOULD-BLOCK_events` (Rev1 R1-qa-4 denominator fix — denominator is alerted cases, not all merges) sustained over **≥20 WOULD-BLOCK events** OR
- **14d hard date** elapsed since v1.28.0 ship WITH **≥3 minimum gate executions observed in warn-only window** (Rev1 R1-qa-3 zero-activity guard); if <3 executions observed → document as "insufficient warm observation" in flip decision record + extend warn-only window to next 20 PR merges OR flip with explicit risk-acceptance note
- Default-on policy: silence (no defer OpenSpec filed) = ready to flip at hard date IF minimum-observation guard met

**FP labeling mechanism** (Rev1 R1-qa-4): warns schema includes `human_reviewed_as_fp: true|false|null` field. Monthly review (named owner: simonfishgit per Rev1 M-qa-6 fix) sets the field by examining each WOULD-BLOCK event against PR intent (legitimate rollback → true; actual regression → false; under investigation → null). FP rate = `count(true) / count(true+false)` excluding null pending entries.

This mirrors Rule #8 rollout cadence + addresses warn-only drift risk.

---

## How

### High-level architecture

```
                         (B+) Hardened Pre-Merge Gate Architecture
                         ─────────────────────────────────────────

phase-c-integrator §C.2.4.5 (after §C.2.4 CI gate, before branch-manager merge API)
        │
        ▼
  ┌────────────────────────────────┐
  │  Step 1: fail-loud fetch       │
  │  git fetch origin master       │  ← exit-code-only abort
  └──────┬─────────────────────────┘     (no fragile grep)
         │ (non-zero exit) → abort §C.2.4.5 with diagnostic
         ▼
  ┌────────────────────────────────┐
  │  Step 2: refspec assertion     │
  │  before/after rev-parse        │  ← detect silent partial fetch
  └──────┬─────────────────────────┘
         │ (expected-advance + no-change) → abort with operator confirm
         ▼
  ┌────────────────────────────────┐
  │  Step 3: per-submodule loop    │
  │   for each submodule:          │
  │     fetch + ls-tree + ancestry │
  └──────┬─────────────────────────┘
         │
         ▼
  ┌────────────────────────────────────────────┐
  │  Per-submodule verdict ladder              │
  │  1. nil-SHA (first-time) → PASS + INFO    │
  │  2. no-change → PASS trivially            │
  │  3. forward bump → PASS                    │
  │  4. ancestor of master → REGRESSION       │
  │  5. neither direction → DIVERGENT         │
  └──────┬─────────────────────────────────────┘
         │ (REGRESSION or DIVERGENT)
         ▼
  ┌────────────────────────────────┐
  │  Override check                │
  │  - commit trailer?             │  → ALLOW + audit
  │  - PR label?                   │  → ALLOW + audit
  └──────┬─────────────────────────┘
         │ (no override)
         ▼
  ┌────────────────────────────────┐
  │  Mode dispatch                 │
  │  - warn → log + telemetry      │
  │  - block → exit 1 + hint       │
  └────────────────────────────────┘
```

### AD allocation (next available — M6 reserves AD-M6-1..3 for cost-acceptance Spec)

AD-FOLLOWUP-1: (B+) gate canonical command spec (drop fragile fetch grep, exit-code-only — backend-architect R3 Q-NEW-1)
AD-FOLLOWUP-2: tripwire observer is mechanical weekly cron, not human review cadence (qa R3 Q-NEW-1)
AD-FOLLOWUP-3: tripwire counter is mechanical `aria/metrics/submodule-gate-misses.json` append-only file (code-reviewer R3 Q-NEW-1)
AD-FOLLOWUP-4: (C) convention doc NOT added as CLAUDE.md numbered Rule — convention SOT in `standards/conventions/` per code-reviewer R3
AD-FOLLOWUP-5: Two-phase rollout uses hard date (v1.28.0 + 14d) default-on, not indefinite "monthly review" — per qa R3 + code-reviewer R3

(AD numbering uses FOLLOWUP prefix to avoid collision with M6 Spec #1's AD-M6-1..3 reservation. If Aria adopts global AD registry post-M6, renumber.)

### Implementation language

Bash for the gate logic (consistency with existing phase-c-integrator + aria/hooks/ Bash) — NOT Python. Reasons:
- Hooks ecosystem in aria-plugin is Bash (per `feedback_bash_hook_perf_subprocess_fork_dominates`)
- Gate logic is git plumbing — Bash + git CLI is idiomatic
- No dependency on Python runtime in §C.2.4.5 critical path

Performance budget (Rev1 R1-ba-5 fix — realistic CI cold-path estimate):
- **Warm cache (local dev)**: per-submodule fetch ~200ms + ls-tree <10ms + ancestry ×2 ~100ms ≈ ~310ms per submodule. 3 submodules sequential ≈ ~930ms total.
- **CI cold-path (Forgejo Actions runner, fresh container, no warm git cache)**: per-submodule fetch ~500-2000ms + ls-tree <10ms + ancestry ~100ms ≈ ~610-2110ms per submodule. 3 submodules sequential ≈ ~1830-6330ms total.
- **Worst case acceptable**: 3s warm / 6s cold. Comparable to or slightly higher than Rule #8 `aether ci status` (~3-5s). Phase B may add background-subshell parallelization for submodule loop if CI dogfood shows >5s sustained; defer optimization until measured.

---

## Effort baseline

| Phase | Work | Estimated effort |
|-------|------|------------------|
| A.1 | Spec drafting (this doc + tasks.md) | ~2h (mostly done) |
| A.2 | post_spec audit R1+R2 convergence | ~1.5h (4 agents × 2 rounds = 8 agent-calls, sequential pacing) |
| A.3 | Agent allocation + branch creation | ~0.5h |
| B.1 | branch creation + scaffolding | ~0.5h |
| B.2.a | Bash gate implementation in phase-c-integrator §C.2.4.5 | ~2h |
| B.2.b | Override parser (commit trailer + PR label via forgejo CLI) | ~1h |
| B.2.c | Telemetry + audit log writer | ~0.5h |
| B.3.a | 9-scenario replay test fixture infrastructure (ephemeral fixture repos) | ~2h |
| B.3.b | 9-scenario assertions + dogfood replay | ~1.5h |
| B.4 | (C) convention doc + cross-references | ~0.5h |
| B.5 | Rule #6 deterministic structural substitute (fixture README + unit tests + atomicity guard) | ~1h |
| B.6 | 5+1 SOT version bump to v1.28.0 + CHANGELOG | ~0.5h |
| C.1 | Commit + push aria-plugin PR | ~0.5h |
| C.2 | PR merge + main Aria submodule pointer re-bump + dual-push | ~0.5h |
| D.1 | Spec archive + handoff + memory | ~1h |
| **Total** | **~15h** (vs ~5h gate-only estimate from brainstorm — full Spec includes A.2 audit + B fixtures + D closure) |

Note: ~15h is the Spec total including all phases. The brainstorm's "~5h" was for B-phase implementation only.

**Two-session strategy** (per brainstorm session timing constraints): 
- Session 1 (this): Phase A.1 + A.2 audit convergence + A.3 (~3.5h)
- Session 2: Phase B.1-B.6 + C + D (~11h)
OR ship across more sessions if owner pacing prefers smaller chunks.

---

## Risks

| # | Risk | Severity | Mitigation |
|---|------|----------|------------|
| R1 | Tripwire dead-zone — observer cron never runs, 12mo passes silently | HIGH | Tripwire counter file `aria/metrics/submodule-gate-misses.json` checked by weekly periodic Forgejo Actions OR Aria-Aether cron job (Phase B.2.c spec'd as mechanical, not "monthly human review") |
| R2 | Warn-only mode permanent (zero FP → no trigger to flip) | MEDIUM | Hard date default-on policy: v1.28.0 + 14d → v1.29.0 auto-flips unless explicit OpenSpec PR-defers (per qa + code-reviewer R3) |
| R3 | Fail-loud fetch false-positive on transient network blip | MEDIUM | `wait_recoverable` error class (per workflow-runner pattern) — transient fetch failure auto-retries with exponential backoff; only non-transient (auth, URL drift) becomes terminal block |
| R4 | Override trailer abuse — operator routinely uses override to skip checks | LOW | Monthly override usage rate review (qa R1 metric); >15% of gate fires using override → re-calibrate sensitivity |
| R5 | First-time submodule false-block | HIGH if missed | nil-SHA explicit handling (qa R1 CRITICAL TEST GAP) — scenario 7 must verify gate exits 0 with INFO on empty ls-tree |
| R6 | Concurrent force-push race during gate execution | LOW | Refspec assertion (Step 2) detects unexpected origin/master mid-flight; legitimate ancestry-forward continues, history-rewrite aborts with operator confirm (backend-architect R3 missing scenario #9) |
| R7 | URL drift attack (submodule remote URL swapped to attacker server) | **Out of scope** | Supply-chain threat model — separate Spec; if manifests, tripwire condition #3 (non-PR-flow) catches + escalates |
| R8 | Multi-terminal coordination — another session's `phase-c-integrator/SKILL.md` edits conflict with this Spec | MEDIUM (Rev1 R1-tl-5 upgrade) | Spec lives in main Aria `openspec/changes/` (unique per Spec ID), BUT the modified Skill file `aria/skills/phase-c-integrator/SKILL.md` is a shared resource. **Phase B.1 must claim** `aria/skills/phase-c-integrator/SKILL.md` via Layer L (multi-terminal-coordination v1.22.0+) before edits — write claim YAML with track-id `aria-submodule-pointer-regression-gate` to `refs/aria/coordination`. See T-layerL task. |
| R9 (Rev1 NEW) | Tripwire dead-zone — observer cron skipped silently for weeks | MEDIUM | Cron itself writes `last_run_timestamp` to misses.json on every execution (Rev1 R1-qa M-qa-3); monthly review (owner: simonfishgit) checks for absence of recent timestamp = cron failure signal |
| R10 (Rev1 NEW) | Telemetry retention unbounded | LOW | 4 JSONL files in `aria/metrics/` — append-only with no automated rotation. Monitor disk; manual rotation annually or when file >1MB. Estimated ~3-4 events/month → years before reaching 1MB. |
| R11 (Rev1 NEW) | `aria/metrics/` directory does not exist on fresh clone | MEDIUM | T-telemetry-0 (NEW task) creates directory on first gate run (`mkdir -p aria/metrics`) with `.gitkeep` placeholder; idempotent |
| R12 (Rev1 NEW) | 3 brainstorm pattern memory files referenced in Spec do not yet exist in user memory dir | LOW | **R1 C-km-1 finding**: `feedback_brainstorm_forcing_function_unified_anchor` + `feedback_brainstorm_owner_escalation_discipline` + `feedback_paper_fix_antipattern` are queued for write in Phase D D.3 of brainstorm cycle. Spec marks them as "(to be created Phase D)" in cross-refs. T-memory task added. |

---

## Open questions (resolved during brainstorm, restated here for spec-drafter completeness)

All 3 R3 Q-NEW resolved:
- **backend-architect Q-NEW-1**: exit-code-only fetch abort spec'd in §What A Step 1 (drop fragile grep)
- **qa Q-NEW-1**: tripwire observer = weekly periodic cron, not human review (spec'd in §What C)
- **code-reviewer Q-NEW-1**: tripwire counter = mechanical `aria/metrics/submodule-gate-misses.json` (spec'd in §What C)

No remaining open Q for owner. Phase A.2 audit may surface additional questions; those will be handled inline R1+R2.

---

## Dependencies

- aria-plugin source repo `/home/dev/Aria/aria/` — modifications to `aria/skills/phase-c-integrator/SKILL.md`
- standards source repo `/home/dev/Aria/standards/` — new file `conventions/submodule-pointer-hygiene.md`
- main Aria repo `/home/dev/Aria/` — submodule pointer bump after aria-plugin PR merges; this Spec itself lives here
- Forgejo `10CG/Aria/aria-plugin/aria-orchestrator/standards` — PR targets for ship
- Existing Rule #8 (phase-c-integrator §C.2.4 `aether ci status` gate) — this Spec adds NEW §C.2.4.5 sub-step between §C.2.4 and existing §C.2.5 (Multi-Remote Push); no conflict
- Aria #124 issue — closed by aria-plugin PR merge in Phase C

NOT a dependency: `aether` plugin (not invoked by this gate). The fail-loud fetch is local git, not Aether-mediated.

---

## Acceptance criteria (Phase B exit + Phase C ready)

### Mechanical (Phase B exit)

- [ ] (B+) gate code in `aria/skills/phase-c-integrator/SKILL.md` §C.2.4.5 with exact bash commands per §What A
- [ ] All 9 replay test scenarios PASS (per tasks.md T-replay-1 through T-replay-9)
- [ ] Override mechanism (commit trailer + PR label) works per dogfood test
- [ ] Telemetry writer creates `aria/metrics/submodule-gate-overrides.json` + `submodule-gate-misses.json`
- [ ] (C) convention doc `standards/conventions/submodule-pointer-hygiene.md` created with required sections
- [ ] aria-plugin 5+1 SOT bumped to v1.28.0 (warn-only mode default)
- [ ] CHANGELOG entry written
- [ ] Tripwire weekly cron config drafted (separate file, can defer enable to v1.29.0)

### Mechanical (Phase C ready)

- [ ] aria-plugin PR opened against master with this Spec as Why
- [ ] PR description includes 9-scenario test result table
- [ ] Override mechanism dogfood evidence in PR comment
- [ ] Reviewer (owner or audit-engine) confirms gate behavior on dogfood
- [ ] 3-way SHA parity verified post-merge (forgejo + github)
- [ ] Main Aria submodule pointer re-bumped to merged aria-plugin SHA

### Mechanical (Phase D close)

- [ ] Spec archived to `openspec/archive/2026-MM-DD-aria-submodule-pointer-regression-gate/`
- [ ] Forgejo Aria #124 closed with PR reference + 9-scenario evidence
- [ ] Phase D session handoff per Rule #9
- [ ] Memory entry decision: new entry for "R2 mutual concession unified anchor pattern" if deemed cross-cycle value (default: write, evaluate at audit)

### Non-mechanical (post-ship monitor)

- [ ] Warn-only telemetry collected for 14 days starting v1.28.0 ship
- [ ] Flip decision made at v1.28.0 + 14d (default → flip; deferred only via explicit OpenSpec)
- [ ] v1.29.0 (block mode) shipped per flip decision
- [ ] Tripwire counter monitored monthly for first 90 days; quarterly thereafter

---

## Cross-references

### Source artifacts (this Spec's foundation)

- DEC: [.aria/decisions/2026-05-24-aria-124-submodule-pointer-regression-gate.md](../../../.aria/decisions/2026-05-24-aria-124-submodule-pointer-regression-gate.md)
- Forgejo issue: [Aria #124](https://forgejo.10cg.pub/10CG/Aria/issues/124)
- Incident commits: `6fea5d7` (PR #123 merge with regression) + `a8e0096` (fast-forward fix)
- Track E Spec (archive): `openspec/archive/2026-05-23-aria-layer2-docker-auth-cold-pull-fix/`
- Track F handoff (incident document): `docs/handoff/2026-05-24-m6-brainstorm-converged-track-f.md` §3 R1
- Track E follow-up handoff (#16+#17 ship): `docs/handoff/2026-05-24-track-e-followups-17-16-done.md`

### Methodology dependencies

- CLAUDE.md Rule #5 (project's own openspec/changes/) ✓
- CLAUDE.md Rule #6 (Skill benchmark) — deterministic structural substitute per `feedback_deterministic_structural_skill_rule6_substitute`
- CLAUDE.md Rule #8 (Phase C.2.4 pre-merge gate pattern) — this Spec adds NEW §C.2.4.5 with parallel pattern (no rename of existing §C.2.5 Multi-Remote Push)
- CLAUDE.md Rule #9 (session-handoff) — Phase D handoff per template
- Version cadence: MINOR bump (new Skill behavior + new convention)
- 向后兼容 principle: warn-only first, then block (mirrors Rule #8 rollout)

### Brainstorm pattern memory

- `feedback_brainstorm_forcing_function_unified_anchor` **(to be created Phase D — Rev1 R1-km-1 fix)** — R3 orchestrator forcing function (this brainstorm replicated M6 pattern)
- `feedback_brainstorm_owner_escalation_discipline` **(to be created Phase D — Rev1 R1-km-1 fix)** — Q-escalation count (this brainstorm: 3 Q-NEW total across R3, healthy threshold)
- `feedback_post_spec_audit_pragmatic_convergence` ✓ exists — pragmatic convergence (this brainstorm: 4/4 R3 ACCEPT_R3)
- `feedback_paper_fix_antipattern` **(to be created Phase D — Rev1 R1-km-1 fix)** — R2 mutual concession (this brainstorm: substance-level reversals, non-paper)
- `feedback_r2_mutual_concession_third_path_synthesis` **(NEW candidate, to be created Phase D)** — R2 fork resolution via ai-engineer neutral 3rd path; current brainstorm 1st empirical evidence; cross-cycle valuable per `feedback_brainstorm_forcing_function_unified_anchor` lineage

**T-memory task** added to tasks.md (Phase D scope) to create these memory entries before closeout.

### Related infrastructure

- `aria/skills/phase-c-integrator/SKILL.md` — modified
- `aria/skills/branch-finisher/SKILL.md` — unchanged this Spec (tripwire promotes (A) here later if triggered)
- `standards/conventions/submodule-pointer-hygiene.md` — NEW
- Forgejo Actions / GitHub Actions cron — tripwire observer (Phase B.2.c spec'd, can defer enable to post-v1.29.0)

---

**Created**: 2026-05-24T~12:00Z
**Author**: spec-drafter (Claude Opus 4.7 1M context) based on DEC-20260524-002
**Status**: Draft → Phase A.2 post_spec audit pending
**Next step**: invoke `aria:audit-engine post_spec` checkpoint with 4 agents (tech-lead + backend-architect + qa + code-reviewer) parallel — per `feedback_post_spec_audit_two_round_pragmatic_for_l2` (Level 2 pattern) OR `feedback_audit_convergence_4_round_baseline` (Level 3 pattern, expected for this Spec)
