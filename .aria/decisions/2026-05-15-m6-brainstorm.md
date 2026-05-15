# M6 Brainstorm — Layer 2 Carryover + M6a/M6b Structure

> **Date**: 2026-05-15
> **Mode**: technical (per `aria:brainstorm` SKILL.md)
> **Scope**: M6 startup — split structure + Spec composition + Layer 2 architectural contract + governance boundary with US-025 closure
> **Status**: Decided (7 questions Q1-Q7 converged)
> **Audit**: post_brainstorm checkpoint not invoked (owner-deferred — small scope, all 7 decisions cross-referenced to existing PRD/AD/handoff sources)
> **Successor artifacts**: `openspec/changes/aria-2.0-m5-carryover-layer2-changes-mode/` (Spec X) + `openspec/changes/aria-2.0-m5-carryover-layer2-redo-mode-aux/` (Spec Y) via `aria:spec-drafter`

---

## 0. Context (loaded at brainstorm start)

**M5 status (2026-05-15 EOD per `docs/handoff/2026-05-15-us025-m5-c2-d1-done.md`)**:
- M5 Layer 1 shipped to master via PR #106 + aria-orchestrator PR #11
- US-025 = `in_progress — Phase D.1 done, awaiting D.2`
- Phase D.2 = owner-gated (T-deploy + Tier-1 live LLM + Tier-2 N≥3 path coverage)
- 11/11 AD-M5 Decided; 793 PASS + 6 SKIP tests; ~34.5h vs 156h baseline ×0.22

**Tension surfaced before Q1**:
- PRD §410-414 defines M6 = "E2E testing + docs + v2.0.0 release" (120h)
- M5 handoff `open_issues_for_m6` lists ~40h Layer 2 carryover work (M5-OS-1..5)
- These are categorically different (technical impl vs docs/release) and on different critical paths

---

## 1. Locked Decisions (Q1-Q7)

| # | Decision | Q | Rationale |
|---|----------|---|-----------|
| **D1** | M6 splits into **M6a** (Layer 2 carryover, ~40h) + **M6b** (US-026 PRD-original docs+release, ~120h) | Q1 | Critical path separation; M6a unblocks M6b's ≥10 dispatch + 7d acceptance |
| **D2** | M6a = 2 Specs: **Spec X = changes-mode (~22h)**, **Spec Y = redo+OS-3/4/5 aux (~19h)** | Q2 + Q6 correction | changes is highest-frequency owner usage; ship-first prioritization; risk-tier excluded per D6 |
| **D3** | Layer 2 reads rework context via **Nomad meta_optional**: `REWORK_MODE` / `REWORK_FEEDBACK` / `PARENT_PR_ID` / `REWORK_OF` | Q3 | Consistent with existing `ISSUE_ID`/`DISPATCH_ID`/`PROMPT_PATH` pattern; replayable via `nomad alloc status`; no new boundary |
| **D4** | M6a归 **US-025 carryover** (mirror M3 carryover trio pattern); no new US-028; PRD not patched | Q4 | PRD §588 US-020~US-027 boundary preserved; M3 silknode/result-path/hcl-crons-sweep precedent; cleaner traceability |
| **D5** | Spec X uses **A2 skeleton-then-fill**: `MODE_HANDLERS` dispatcher with `initial`+`changes` impl, `redo` slot = `NotImplementedError` | Q5 | Dispatcher exercised by X (avoid `feedback_scaffold_helpers_drift`); Y zero-refactor drop-in; total ~42h |
| **D6** | **risk-tier algorithm pushed to M7+** — v2.0 ships with `risk_tier_stub 'always'` literal (M5 ABI compat) | Q6 | Not in m5-handoff::open_issues_for_m6; not in PRD M6 definition; YAGNI for v2.0; classifier needs production calibration data |
| **D7** | US-025 close gate **reframed**: T-deploy + Tier-1 live + Spec X+Y archived (2 owner gates + 2 AI Specs); Tier-2 path coverage **absorbed to US-026 M6b ≥10 dispatch verification** | Q7 | Eliminates duplicate path-coverage verification; US-025 closes in ~1-2 weeks instead of indefinite owner-workload wait |

---

## 2. Spec X Design (changes-mode, ~22h)

**Path**: `openspec/changes/aria-2.0-m5-carryover-layer2-changes-mode/`

**Scope**:
- New module `aria_layer2_runner/mode_dispatcher.py`:
  - `MODE_HANDLERS: Dict[str, Callable] = {'initial': handle_initial, 'changes': handle_changes, 'redo': _not_implemented}`
  - Entry: `dispatch_mode(env: dict) -> int` reads `REWORK_MODE` env var
- Refactor existing entrypoint into `mode_initial.py` (zero behavioral change; test parity required)
- New `mode_changes.py`:
  - Forgejo API: fetch PR branch by `PARENT_PR_ID`
  - Forgejo API: pull all PR review comments (mitigates force-push-loses-context per AD-M5-3 §risk mitigation)
  - Prompt assemble: `REWORK_FEEDBACK` + original code diff (file-by-file, feedback-prioritized) + review comment history
  - Hard cap 60K tokens; overflow → audit log warn + fallback to redo mode (per AD-M5-3 prompt strategy)
  - Invoke `claude -p --prompt-file <assembled>`
  - Git `push --force-with-lease=<branch>:$(git rev-parse FETCH_HEAD)` (per `feedback_git_force_with_lease_shallow_clone`)
- Layer 1 `_handle_s4_launch` extension: write 4 meta_optional keys when `rework_mode='changes'`
- Nomad HCL `meta_optional`: add 4 keys
- Image: bump `claude-m6a-<sha>-v10` + sha256 digest pin (AD-M1-7)

**Acceptance** (Spec X internal):
- Synthetic: mock Forgejo + mock `claude -p` + verify force-push call happens with correct refs
- Unit: `mode_dispatcher` routing table + `mode_changes` prompt builder edge cases (empty feedback / 60K overflow / Forgejo 5xx)
- Integration: test dispatch row `rework_mode='changes'` → S4_LAUNCH → meta written → container mock → S5_AWAIT

**Production verification deferred**: real `/aria changes:` dispatch counted in US-026 M6b ≥10 dispatch (per D7)

---

## 3. Spec Y Design (redo + aux, ~19h)

**Path**: `openspec/changes/aria-2.0-m5-carryover-layer2-redo-mode-aux/`

**Scope**:
- **OS-2 mode_redo.py (~12h)**: drop `redo` handler into `MODE_HANDLERS` slot; logic = fresh checkout from main + feedback prompt context + new branch + new PR (no force-push, no Forgejo branch fetch)
- **OS-3 close-old-PR (~2h)**: in S5_PR_CREATED handler, if `rework_of IS NOT NULL AND rework_mode='redo' AND parent_pr_id IS NOT NULL` → Forgejo API: post `_Superseded by #<new>_` comment on parent PR + `PATCH /repos/.../issues/<parent>/state {state: closed}`
- **OS-4 spec_drift_fetcher (~3h)**: full impl — dispatch_id → spec_id mapping (Layer 2 writes `spec_id` field on dispatch row before S4) + read `openspec/changes/<spec_id>/proposal.md` + Forgejo PR diff API
- **OS-5 commit-lint retry hook (~2h)**: Layer 2 commit hook (post-claude pre-push) runs `commit_validator.validate(msg)` → invalid → `claude -p "rewrite commit message: <reason>"` up to 3 attempts → 3rd fail = S_FAIL(commit_lint_exhausted)

**Acceptance**: synthetic-only (mock Forgejo + mock claude) per Spec X precedent

**Image**: bump `claude-m6a-<sha>-v11`

---

## 4. Sequencing

```
Now → Spec X Phase A (drafting)
       ↓ (Phase A audit converges)
       Spec X Phase B (implementation)
       ↓ (PR merged)
       Spec X archive ← US-025 footer link Spec X
       ↓
       Spec Y Phase A (drafting; can overlap with Spec X Phase B if owner cycles allow)
       ↓
       Spec Y Phase B (implementation)
       ↓ (PR merged)
       Spec Y archive ← US-025 footer link Spec Y
       ↓
       (owner) T-deploy + Tier-1 live LLM gates → US-025 archive ← Phase D.2 final Go
       ↓
       US-026 (M6b) Phase A kickoff
```

**Parallelism allowed**: Spec X+Y Phase A can be drafted in parallel (Y depends only on X's `MODE_HANDLERS` interface, which is locked by D5).

**Parallelism prohibited**: US-026 Phase A may NOT start until US-025 archived (per D4 — M6 = US-026 only, M6a is US-025 carryover; US-025 must close before M6 proper begins).

---

## 5. Side-effect Patches (Spec X kickoff Phase A scope)

| File | Patch |
|------|-------|
| `docs/requirements/user-stories/US-025.md` | Footer "M5 Carryover Sub-Specs" linking Spec X+Y |
| `aria-orchestrator/docs/m5-handoff.yaml::open_issues_for_m6` | Rewrite: M5-OS-1..5 marked `absorbed_by: <spec-x or spec-y>`; `tier2_path_coverage` field moved to new `m6_carryover_to_us_026` field per D7 |
| `aria-orchestrator/docs/architecture-decisions.md::AD-M5-3` | Status update: "Decided 2026-05-14 — Layer 1 wiring DONE; Layer 2 IMPLEMENTATION **in progress via Spec X**" |
| `docs/requirements/prd-aria-v2.md` M6 row | **No change** (M6 = US-026 docs+release per original PRD; Layer 2 carryover lives under US-025) |

---

## 6. Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Spec X Phase A audit finds `MODE_HANDLERS` registry over-engineered | Roll back to A4 "concrete + Y-friendly naming"; reassess at Phase A.2 audit |
| Spec X `mode_changes.py` force-push breaks PR review threads | AD-M5-3 §risk mitigation locked: pull PR comments into prompt context (Forgejo `GET /repos/.../pulls/<pr>/reviews/comments` before force-push) |
| Layer 2 image v10 build breaks aria-build pipeline | Image bump same pattern as M1→M5 (5x previous bumps successful); `aria-build-verify` job validates digest |
| Owner T-deploy delayed beyond Spec X+Y archive | US-025 stays `in_progress` until owner ready; AI work parked clean. M6b cannot start; no impact other than v2.0 release timeline |
| Tier-2 absorbed-to-M6b interpretation rejected at PR review | Q7 explicitly enumerated this option; D7 documented as Decided; M6b verification gate (≥10 dispatch + 7d) is strictly stronger than Tier-2 N≥3, so absorption is provably safe |

---

## 7. Out of Scope

- **risk-tier algorithm** (D6 → M7+)
- **Layer 2 mode = 'retry'** for failure_analysis (M5 already ships this path; not part of M6a)
- **`claude -p` provider routing changes** (M3 ProviderRouter chain unchanged)
- **Schema migration v4 → v5** (none anticipated for Spec X/Y; if needed, Spec Y can add as task)
- **comment-poll cron cadence changes** (M5 already at <60s per AD-M5-1; no change)

---

## 8. Cross-references

- M5 brainstorm precedent: `.aria/decisions/2026-05-10-us025-m5-brainstorm.md`
- M5 handoff: `docs/handoff/2026-05-15-us025-m5-c2-d1-done.md`
- M5 deploy playbook: `docs/handoff/2026-05-15-m5-deploy-playbook.md`
- AD-M5-3 (Layer 1↔Layer 2 contract): `aria-orchestrator/docs/architecture-decisions.md:3574-3629`
- AD-M5-4 (force-push rationale): same file, §AD-M5-4
- AD-M5-8 (risk_tier dual-write boundary): same file, §AD-M5-8
- AD-M5-10 (forward-binding promises M5→M6): same file, §AD-M5-10
- PRD v2.0 M6 row: `docs/requirements/prd-aria-v2.md:410-414` + §588 US table
- US-025 spec: `openspec/changes/aria-2.0-m5-replay-reconciler-drift-review-loop-audit/`

---

**Brainstorm output ready for `aria:spec-drafter` (Spec X first)**.
