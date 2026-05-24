# aria-submodule-pointer-regression-gate — Phase B Tasks

> **Spec**: [proposal.md](./proposal.md)
> **Level**: 3 (Full)
> **Status**: Draft (Phase A.1)
> **Brainstorm Source**: [DEC-20260524-002](../../../.aria/decisions/2026-05-24-aria-124-submodule-pointer-regression-gate.md)
> **Estimated Phase B total**: ~9h (gate ~5h + tests ~3.5h + docs ~0.5h)
> **Recommended Agent**: backend-architect (Bash + git plumbing primary)

---

## Task Group Overview (Rev1 — added T-layerL / T-memory / T-telemetry-0)

| Group | Topic | Scope ref | Est |
|-------|-------|-----------|-----|
| **T-layerL** (Rev1 NEW) | Phase B.1 prerequisite: Layer L claim for shared Skill file | §Risks R8 | ~0.2h |
| T-gate | (B+) gate implementation in phase-c-integrator §C.2.4.5 | §What A | ~2.5h |
| T-override | Override mechanism (commit trailer + PR label parser, ASCII `->` alt, SHA normalization) | §What B | ~1h |
| **T-telemetry-0** (Rev1 NEW) | Create `aria/metrics/` directory + `.gitkeep` | §Risks R11 | ~0.1h |
| T-telemetry | Telemetry writers + audit logs + `human_reviewed_as_fp` field | §What B+C | ~0.5h |
| T-replay | 9-scenario replay test fixture + assertions (+ T-replay-10 detached HEAD) | §What A + §Acceptance | ~3.5h |
| T-convention | (C) convention doc in `standards/conventions/submodule-pointer-hygiene.md` | §What D | ~0.5h |
| T-rollout | v1.28.0 5+1 SOT bump + CHANGELOG (style anchor [1.27.0]) | §What E | ~0.5h |
| T-rule6 | Rule #6 deterministic structural substitute | §Risks methodology | ~1h (Rev1 R1-tl M-tl-5: bumped from 0.5h) |
| T-tripwire | Tripwire counter + Forgejo Actions workflow at `.forgejo/workflows/submodule-gate-tripwire.yml` (in 10CG/Aria main repo, NOT aria-plugin) | §What C | ~0.5h |
| **T-memory** (Rev1 NEW) | Phase D: write 3-4 brainstorm pattern memory files cited in Spec but not yet present | §Risks R12 + §Cross-references | ~0.5h |

**Total Phase B**: ~9.8h (Rev1 added ~0.8h for new tasks + T-rule6 bump)
**Total end-to-end** (Phase A.2 + A.3 + B + C + D): ~15h unchanged (Rev1 absorbed within original buffer)

---

## T-layerL — Layer L claim for shared Skill file (Rev1 NEW, ~0.2h)

per Risks R8 + Rev1 R1-tl-5 fix — `aria/skills/phase-c-integrator/SKILL.md` is shared resource.

- [ ] Before any T-gate edit: write claim YAML to `refs/aria/coordination` per multi-terminal-coordination v1.22.0+ Layer L
- [ ] track-id: `aria-submodule-pointer-regression-gate`
- [ ] claimed-paths: `["aria/skills/phase-c-integrator/SKILL.md"]`
- [ ] Heartbeat every 10min during Phase B (per Layer L claim_lifecycle)
- [ ] Release claim in Phase D.2 after archive

---

## T-gate — (B+) gate implementation (~2.5h)

### T-gate-1 — Sketch gate inline in phase-c-integrator §C.2.4.5 (Bash) (~0.5h)

per Rev1 R1-tl-1 fix — NEW sub-step §C.2.4.5 (NOT §C.2.5 which is existing Multi-Remote Push)

- [ ] Read current `aria/skills/phase-c-integrator/SKILL.md` §C.2.4 (Rule #8 aether ci gate) AND §C.2.5 (Multi-Remote Push) for context
- [ ] Add NEW sub-step §C.2.4.5 between them: "Submodule Pointer Regression Gate (B+)"
- [ ] Document mode toggle: `ARIA_SUBMODULE_GATE_MODE=warn|block` (env var; default via `.aria/config.json` `phase_c_integrator.submodule_gate.mode` set per version: v1.28.0=warn, v1.29.0=block) — per Rev1 R1-tl M-tl-4
- [ ] Document order: §C.2.4 CI gate → **§C.2.4.5 submodule gate (NEW)** → branch-manager merge API call → §C.2.5 Multi-Remote Push (existing, untouched)
- [ ] **Lock pre-merge invocation hook point** (Rev1 R1-tl-2 fix): explicit "called by phase-c-integrator BEFORE branch-manager merge API; not as post-merge hook"

### T-gate-2 — Implement fail-loud fetch (Step 1) (~0.3h)

per Rev1 R1-ba-1/2 + R1-tl-3 fixes

- [ ] `git fetch origin` (bare — NOT `git fetch origin master`; per R1-ba-1 latter doesn't update `origin/master` ref reliably)
- [ ] Capture BEFORE_REMOTE = `git rev-parse origin/master 2>/dev/null || echo "FIRST_RUN"` **before** fetch (R1-ba-2 ordering fix)
- [ ] **Bounded retries** (R1-tl-3 fix — drop stderr regex classifier): exponential backoff 1s/2s/4s × 3 attempts; if all fail → terminal block with explicit "fetch_exhausted_retries" telemetry entry + remediation hint (auth/network/URL drift)
- [ ] No `grep` of success patterns (AD-FOLLOWUP-1 prohibition)
- [ ] Capture AFTER_REMOTE = `git rev-parse origin/master` strictly after fetch
- [ ] First-run handling (R1-ba-3): if BEFORE_REMOTE == "FIRST_RUN" → skip refspec assertion (no prior state to compare); proceed to Step 3 ancestry checks

### T-gate-3 — Implement refspec assertion (Step 2) (~0.4h)

- [ ] Before fetch: `git rev-parse origin/master 2>/dev/null` → `BEFORE`
- [ ] After fetch: `git rev-parse origin/master` → `AFTER`
- [ ] If `BEFORE != AFTER` → ensure `BEFORE` is ancestor of `AFTER` (`git merge-base --is-ancestor "$BEFORE" "$AFTER"`)
- [ ] If non-ancestor → abort with "origin/master history rewritten, operator confirm required" (use `wait_recoverable` classifier)

### T-gate-4 — Implement per-submodule loop (Step 3) (~0.8h)

- [ ] Enumerate submodules from `.gitmodules`
- [ ] Per submodule: `git -C "$SUB" fetch origin`
- [ ] Get FEATURE_PTR + MASTER_PTR via `git ls-tree`
- [ ] Handle nil-SHA case (empty `MASTER_PTR` = first-time submodule) → INFO + continue (qa CRITICAL TEST GAP)
- [ ] Handle no-change case (`FEATURE_PTR == MASTER_PTR`) → OK + continue
- [ ] Print visible SHA diff `GATE: submodule=X master=Y feature=Z`

### T-gate-5 — Implement 双向 ancestry check (~0.3h)

- [ ] Primary: `git -C "$SUB" merge-base --is-ancestor "$MASTER_PTR" "$FEATURE_PTR"` → exit 0 = PASS forward
- [ ] Reverse: `git -C "$SUB" merge-base --is-ancestor "$FEATURE_PTR" "$MASTER_PTR"` → exit 0 = REGRESSION
- [ ] Else: DIVERGENT

### T-gate-6 — Mode dispatch (warn vs block) (~0.2h)

- [ ] If `ARIA_SUBMODULE_GATE_MODE=warn` (v1.28.0 default) → log `WOULD-BLOCK ...` + telemetry append + continue
- [ ] If `ARIA_SUBMODULE_GATE_MODE=block` (v1.29.0 default) → emit BLOCK message with remediation hint + exit 1

---

## T-override — Override mechanism (~1h)

### T-override-1 — Commit trailer parser (~0.4h)

per Rev1 R1-ba-4 + R1-qa M-qa-5 fixes

- [ ] Parse merge commit message via `git log -1 --format=%B HEAD`
- [ ] Match trailer pattern (BOTH Unicode and ASCII forms): `^Submodule-Rollback: (\S+) (\S+)(?:→|->)(\S+) reason=(.+)$` (Rev1 R1-ba-4 ASCII `->` alternative)
- [ ] **SHA normalization** (R1-qa M-qa-5): resolve short SHAs (≥7 chars) via `git -C "$SUB" rev-parse "$short_sha"` before comparison
- [ ] Verify trailer SHAs match the actual FEATURE/MASTER pointers (forbid mismatched override)
- [ ] Return: allowed | not-allowed (mismatched) | absent

### T-override-2 — Forgejo PR label fetcher (~0.4h)

- [ ] Use `forgejo GET /repos/10CG/Aria/issues/<PR>/labels` to check labels
- [ ] Match `submodule-rollback-approved`
- [ ] Handle API error gracefully (treat as no-label, gate proceeds)

### T-override-3 — Override audit log writer (~0.2h)

- [ ] Append to `aria/metrics/submodule-gate-overrides.json` (JSONL or append-array)
- [ ] Fields: `timestamp, pr_id, submodule, master_sha, feature_sha, verdict, reason, override_type (trailer|label)`

---

## T-telemetry-0 — Create `aria/metrics/` directory (Rev1 NEW, ~0.1h)

per Risks R11 + R1-km-4 fix

- [ ] Idempotent `mkdir -p aria/metrics/` on first gate run (or as Phase B.1 scaffolding step)
- [ ] Add `.gitkeep` file so empty dir is checked in
- [ ] Add `aria/metrics/*.json` line to aria-plugin `.gitignore` (telemetry files are per-deployment, not committed)
- [ ] Verify file system permissions (0755 dir / 0644 .gitkeep)

---

## T-telemetry — Telemetry + audit (~0.5h)

### T-telemetry-1 — Warn-only telemetry writer (~0.3h)

per Rev1 R1-qa-4 + R1-ba M-ba-3 fixes

- [ ] Append to `aria/metrics/submodule-gate-warns.json` on every WOULD-BLOCK event
- [ ] **JSONL format** (R1-ba M-ba-3: race-safe for concurrent appends; one JSON object per line; kernel write atomic for <PIPE_BUF=4096 bytes)
- [ ] Fields: `timestamp, pr_id, submodule, master_sha, feature_sha, verdict, mode, human_reviewed_as_fp (initial: null)` — Rev1 R1-qa-4 adds FP-review field
- [ ] Used to compute FP rate for v1.29.0 flip decision: FP = `count(human_reviewed_as_fp==true) / count(true+false)` excluding null pending entries
- [ ] Monthly review owner (Rev1 M-qa-6): simonfishgit sets `human_reviewed_as_fp` field per WOULD-BLOCK event

### T-telemetry-2 — Block-mode audit logger (~0.2h)

- [ ] Append to `aria/metrics/submodule-gate-blocks.json` on every BLOCK event
- [ ] Fields: `timestamp, pr_id, submodule, master_sha, feature_sha, verdict, remediation_hint`

---

## T-replay — 9-scenario replay test fixture (~3.5h)

### T-replay-fixture — Fixture infrastructure (~1.5h)

- [ ] Per-test ephemeral dir `/tmp/aria-gate-test-<uuid>/`
- [ ] Helper: `create_fake_submodule_repo()` → bare repo with N commits
- [ ] Helper: `create_parent_repo_with_submodule(submodule_repo, base_sha)` → parent repo tracking submodule at SHA
- [ ] Helper: `create_feature_branch(parent_repo, submodule_target_sha)` → feature branch with submodule pointer at target SHA
- [ ] Cleanup: full directory remove per test

### T-replay-1 — Happy path forward bump (~0.2h)

- [ ] Fixture: master submodule = v1.0; feature submodule = v1.0 + 5 commits (descendant)
- [ ] Assert: gate exits 0 + stdout contains "PASS"

### T-replay-2 — Pure regression (~0.2h)

- [ ] Fixture: master submodule = v1.0 + 5 commits; feature submodule = v1.0 (ancestor)
- [ ] Assert: gate exits 1 + stderr contains "REGRESSION" + SHA values
- [ ] In warn mode: assert exits 0 + telemetry file contains entry

### T-replay-3 — Divergent history (~0.3h)

- [ ] Fixture: master submodule on branch-A (5 commits); feature submodule on branch-B (5 commits, no common ancestor)
- [ ] Assert: gate exits 1 + stderr contains "DIVERGENT" (not "REGRESSION")

### T-replay-4 — Stale-ref incident replay (~0.5h)

- [ ] Fixture: simulate incident — origin/master at HEAD-of-master; local origin/master ref points to an older commit
- [ ] Run gate with mode=warn; assert fetch refreshes ref + ancestry check accurate
- [ ] Variation: fetch fails (mock network error) → assert exit non-zero with explicit fetch-fail diagnostic
- [ ] Variation: silent partial fetch (e.g., wrong remote URL) → refspec assertion catches via before/after diff

### T-replay-5 — Legitimate revert with trailer override (~0.3h)

- [ ] Fixture: master submodule = v1.0 + 5 commits; feature submodule = v1.0
- [ ] Add commit trailer `Submodule-Rollback: aria v1.0+5→v1.0 reason=test revert`
- [ ] Assert: gate exits 0 + audit log file contains entry
- [ ] Variation: mismatched SHAs in trailer → gate rejects override + exits 1

### T-replay-6 — No-change (same pointer) (~0.1h)

- [ ] Fixture: master submodule == feature submodule
- [ ] Assert: gate exits 0 trivially + stdout contains "OK"

### T-replay-7 — First-time submodule (nil prior gitlink) (~0.3h)

- [ ] Fixture: master tree has NO submodule path; feature adds new submodule
- [ ] Assert: `git ls-tree HEAD <new-sub>` returns empty
- [ ] Assert: gate exits 0 + stdout contains "INFO: first introduced"
- [ ] CRITICAL: this test is the qa R1 CRITICAL TEST GAP coverage

### T-replay-8 — Submodule removed (~0.2h)

- [ ] Fixture: master has submodule; feature removes it (.gitmodules + tree)
- [ ] Assert: gate does not crash + exits 0 or appropriate path-removed handling

### T-replay-9 — Concurrent force-push race (~0.4h)

per backend-architect R3 missing scenario + Rev1 R1-ba M-ba-5 fix — use deterministic pre-staged fixture

- [ ] Fixture: deterministic pre-stage — bare remote repo has commits A→B→C; create parent repo with origin/master at A; pre-stage bare remote at C (=force-pushed ahead)
- [ ] Run gate; verify BEFORE rev-parse returns A, fetch advances to C, AFTER rev-parse returns C
- [ ] If A is ancestor of C → gate continues (ancestry-forward)
- [ ] **Variation**: bare remote rewrites to alternative branch A→D (non-ancestor of C) → gate aborts with operator confirm
- [ ] Do NOT use real background concurrent processes (flaky)

### T-replay-10 — Detached HEAD submodule (Rev1 NEW, ~0.2h)

per qa R1 I-qa-1 — uncovered scenario

- [ ] Fixture: submodule on detached HEAD at a commit that exists in origin but is not on any current branch
- [ ] Verify: `fetch origin` succeeds, `ls-tree HEAD <sub>` returns valid SHA, `merge-base --is-ancestor` operates on raw SHAs correctly
- [ ] Assert gate behavior matches expected verdict (PASS / REGRESSION / DIVERGENT based on relationship to master gitlink)

---

## T-convention — (C) convention doc (~0.5h)

### T-convention-1 — Write `standards/conventions/submodule-pointer-hygiene.md` (~0.4h)

- [ ] Sections:
  - Overview (incident origin + why)
  - Rule 1: Always `git fetch origin` before rebase touching submodules
  - Rule 2: Never `git checkout origin/<branch> -- <sub>` without fresh fetch in same shell
  - Rule 3: For deliberate rollback, use override mechanism (commit trailer or PR label)
  - Cross-references to phase-c-integrator §C.2.5 + this Spec
  - Source incident (PR #123 / commits)
- [ ] Match `standards/conventions/secret-hygiene.md` style + frontmatter

### T-convention-2 — Cross-reference from CLAUDE.md (~0.1h)

- [ ] Add to CLAUDE.md "信息地图" table:
  - `Submodule pointer 卫生 → standards/conventions/submodule-pointer-hygiene.md`
- [ ] Do NOT add as numbered Rule (per code-reviewer R3 + AD-FOLLOWUP-4)

---

## T-rollout — v1.28.0 5+1 SOT bump (~0.5h)

### T-rollout-1 — Bump 5+1 SOT files (~0.3h)

- [ ] `aria/.claude-plugin/plugin.json` version 1.27.0 → 1.28.0
- [ ] `aria/.claude-plugin/marketplace.json` version + plugins[].version
- [ ] `aria/VERSION` snapshot
- [ ] `aria/CHANGELOG.md` add `[1.28.0]` section with this Spec summary
- [ ] `aria/README.md` version line
- [ ] `aria/hooks/hooks.json` review (no change expected — gate is in phase-c-integrator Skill, not hooks)

### T-rollout-2 — CHANGELOG entry detail (~0.2h)

- [ ] Title: `[1.28.0] — Submodule Pointer Regression Gate (warn-only, v1.29.0 will flip to block)`
- [ ] Summary: 3-line description
- [ ] Reference: Aria #124, DEC-20260524-002, Spec aria-submodule-pointer-regression-gate
- [ ] Migration note: existing PR workflows unaffected (warn-only); v1.29.0 flip will require commit trailer / label override for legitimate rollbacks

---

## T-rule6 — Rule #6 deterministic structural substitute (~0.5h)

per `feedback_deterministic_structural_skill_rule6_substitute` (non-LLM AB):

- [ ] Structural fixture README in `aria-plugin-benchmarks/submodule-gate/README.md`
- [ ] 9-scenario unit tests scripted (reuses T-replay fixtures)
- [ ] Dogfood: real feature branch with deliberately stale submodule pointer → run gate → verify block
- [ ] Atomicity guard test: race scenario #9 covered
- [ ] **Skip** `/skill-creator benchmark` (LLM AB is wrong instrument for deterministic gate)

---

## T-tripwire — Tripwire counter + observer cron (~0.5h)

### T-tripwire-1 — Counter file format spec (~0.2h)

- [ ] Define `aria/metrics/submodule-gate-misses.json` schema
- [ ] Append-only JSONL or JSON array
- [ ] Fields: `{timestamp, miss_type (escaped_regression|fetch_failure|non_pr_bypass), pr_id_if_known, master_sha, feature_sha, detected_by}`

### T-tripwire-2 — Observer cron drafting (DEFER enable to v1.29.0) (~0.3h)

per Rev1 R1-tl-3 fix — resolve proposal/tasks contradiction; location is **main 10CG/Aria repo**, NOT aria-plugin

- [ ] Draft `.forgejo/workflows/submodule-gate-tripwire.yml` in `10CG/Aria` main repo (Forgejo Actions workflow)
- [ ] Weekly cron schedule (e.g., `0 4 * * 0` = Sunday 04:00 UTC)
- [ ] Logic in workflow step: compare master HEAD~1 vs HEAD submodule gitlinks ancestry; on regression → append to `aria/metrics/submodule-gate-misses.json` + file Forgejo issue with label `gate-tripwire-count`
- [ ] **Cron always writes `last_run_timestamp` field** to misses.json (Rev1 R1-qa M-qa-3 fix) — monthly review owner detects cron skip via absence of recent timestamp
- [ ] Spec the cron schedule but **DO NOT activate** workflow in v1.28.0 (`on: workflow_dispatch` only, manual trigger for testing); switch to `on: schedule` cron in v1.29.0 commit
- [ ] Backup detection: workflow emits Aether alert OR Feishu webhook on failure (per qa M-qa-3)

---

## T-memory — Phase D: create 3-4 brainstorm pattern memory files (Rev1 NEW, ~0.5h)

per Risks R12 + R1 C-km-1 fix — Spec cites these as cross-references but they don't yet exist

- [ ] `feedback_brainstorm_forcing_function_unified_anchor.md` — R3 orchestrator forcing function (M6 origin + this brainstorm 2nd empirical)
- [ ] `feedback_brainstorm_owner_escalation_discipline.md` — Q-escalation ≤2 per round healthy threshold; >2 = brainstorm cop-out signal
- [ ] `feedback_paper_fix_antipattern.md` — substance-level vs surface-verdict-match distinction; M6 brainstorm R2 paper-fix caught, this brainstorm R2 substance-level reversal verified
- [ ] **NEW candidate**: `feedback_r2_mutual_concession_third_path_synthesis.md` — when R1 fork's R2 challengers both concede to opposite positions, neutral 3rd party's synthesis path (strict superset of both concessions) is often the forcing-function unified anchor; this brainstorm = 1st empirical evidence post-M6
- [ ] Index in MEMORY.md per Aria memory protocol
- [ ] Decide at Phase D audit: ship all 4 OR drop NEW candidate if not deemed cross-cycle valuable (avoid memory inflation per `feedback_brainstorm_owner_escalation_discipline` lineage)

---

## Acceptance gates (Phase B exit)

- [ ] All T-gate-* tasks complete + dogfood replay PASS
- [ ] All T-override-* tasks complete + commit trailer + PR label both tested
- [ ] T-telemetry writes valid JSON to metrics files
- [ ] All 9 T-replay scenarios PASS individually + as suite
- [ ] T-convention doc reviewed + cross-ref'd from CLAUDE.md
- [ ] T-rollout 5+1 SOT bump consistent (programmatic verify per Aria version policy)
- [ ] T-rule6 structural substitute documented + scenarios reproducible
- [ ] T-tripwire counter + cron drafted (enable deferred)

---

## Dependencies between tasks

```
T-gate-1 (sketch) → T-gate-2/3/4/5/6 (parallel implementation)
                  ↘
                    T-replay-fixture (depends on T-gate-* for gate to test against)
                                    ↘
                                      T-replay-1..9 (parallel)
T-override-* (independent of T-gate, but cross-cuts T-replay-5)
T-telemetry-* (depends on T-gate-6 for mode dispatch hooks)
T-convention (independent)
T-rule6 (depends on T-replay completion for structural fixture link)
T-rollout (LAST — bumps version after all code+test settled)
T-tripwire (independent, can be deferred but spec'd in this Phase B)
```

---

**Created**: 2026-05-24T~12:00Z (Phase A.1 spec-drafter)
**Status**: Draft → Phase A.2 audit pending
**Total Phase B effort**: ~9h
**Estimated session decomposition**:
- Session 1: T-gate + T-override + T-telemetry (~4h)
- Session 2: T-replay-fixture + T-replay-1..9 (~3.5h)
- Session 3: T-convention + T-rollout + T-rule6 + T-tripwire + Phase C (~3h)
