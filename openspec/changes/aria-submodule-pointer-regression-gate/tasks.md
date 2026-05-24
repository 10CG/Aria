# aria-submodule-pointer-regression-gate — Phase B Tasks

> **Spec**: [proposal.md](./proposal.md)
> **Level**: 3 (Full)
> **Status**: Draft (Phase A.1)
> **Brainstorm Source**: [DEC-20260524-002](../../../.aria/decisions/2026-05-24-aria-124-submodule-pointer-regression-gate.md)
> **Estimated Phase B total**: ~9h (gate ~5h + tests ~3.5h + docs ~0.5h)
> **Recommended Agent**: backend-architect (Bash + git plumbing primary)

---

## Task Group Overview

| Group | Topic | Scope ref | Est |
|-------|-------|-----------|-----|
| T-gate | (B+) gate implementation in phase-c-integrator §C.2.5 | §What A | ~2.5h |
| T-override | Override mechanism (commit trailer + PR label parser) | §What B | ~1h |
| T-telemetry | Telemetry writer + audit log + metrics files | §What B+C | ~0.5h |
| T-replay | 9-scenario replay test fixture + assertions | §What A + §Acceptance | ~3.5h |
| T-convention | (C) convention doc in standards/ | §What D | ~0.5h |
| T-rollout | v1.28.0 5+1 SOT bump + CHANGELOG | §What E | ~0.5h |
| T-rule6 | Rule #6 deterministic structural substitute | §Risks methodology | ~0.5h |
| T-tripwire | Tripwire counter + observer cron config (defer enable to v1.29.0) | §What C | ~0.5h |

---

## T-gate — (B+) gate implementation (~2.5h)

### T-gate-1 — Sketch gate inline in phase-c-integrator §C.2.5 (Bash) (~0.5h)

- [ ] Read current `aria/skills/phase-c-integrator/SKILL.md` §C.2.4 (Rule #8 aether ci gate) for existing pattern
- [ ] Add new §C.2.5 section header "Submodule Pointer Regression Gate (B+)"
- [ ] Document mode toggle: `ARIA_SUBMODULE_GATE_MODE=warn|block` (env var; defaults set per version: v1.28.0=warn, v1.29.0=block)
- [ ] Document order: §C.2.4 CI gate → §C.2.5 submodule gate → merge execution

### T-gate-2 — Implement fail-loud fetch (Step 1) (~0.3h)

- [ ] `git fetch origin master` (exit-code-only abort, per AD-FOLLOWUP-1)
- [ ] No `grep` of success patterns
- [ ] On non-zero exit: classify as `wait_recoverable` (transient) vs terminal (auth/URL) via stderr pattern
- [ ] Emit structured error to workflow-runner

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

- [ ] Parse merge commit message via `git log -1 --format=%B HEAD`
- [ ] Match trailer pattern: `^Submodule-Rollback: (\S+) (\S+)→(\S+) reason=(.+)$`
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

## T-telemetry — Telemetry + audit (~0.5h)

### T-telemetry-1 — Warn-only telemetry writer (~0.3h)

- [ ] Append to `aria/metrics/submodule-gate-warns.json` on every WOULD-BLOCK event
- [ ] Fields: `timestamp, pr_id, submodule, master_sha, feature_sha, verdict, mode`
- [ ] Used to compute FP rate for v1.29.0 flip decision

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

- [ ] Fixture: between `BEFORE=rev-parse` and `AFTER=rev-parse` in gate, simulate force-push to origin/master
- [ ] If new origin/master is ancestry-forward → gate continues
- [ ] If new origin/master is history-rewritten (non-ancestor) → gate aborts with operator confirm
- [ ] Per backend-architect R3 missing scenario

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

- [ ] Draft `aria/cron/submodule-gate-tripwire.sh` (Bash)
- [ ] Weekly cron via Forgejo Actions OR Aether scheduled job
- [ ] Logic: compare master HEAD~1 vs HEAD submodule gitlinks ancestry; on regression → append to misses.json + file Forgejo issue
- [ ] Spec the cron schedule but do NOT activate it in v1.28.0; activate post-v1.29.0 ship

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
