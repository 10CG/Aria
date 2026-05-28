# aria-ci-backend-abstraction Tasks — CI backend abstraction (Sprint 2 boundary audit P0 C5+C6)

> **Spec**: [aria-ci-backend-abstraction](./proposal.md)
> **Level**: 3 (Full)
> **Status**: Draft — pending post_spec audit (3 agents × convergence mode, L3 default 4-round baseline per [[feedback_audit_convergence_patterns]])
> **Brainstorm Source**: [`.aria/decisions/2026-05-28-ci-backend-abstraction-brainstorm.md`](../../../.aria/decisions/2026-05-28-ci-backend-abstraction-brainstorm.md) (Q1-Q5 owner-approved + R1 audit PASS_WITH_WARNINGS × 3 unanimous)
> **Estimated total**: **~10-10.5h** (revised from initial 8.5h per R1 substance-converged M-1 test rewrite estimate)
> **Agent**: backend-architect primary (~7-8h:T-backends + T-refactor + T-tests + T-rule6),qa-engineer review (AC + test design audit ~0.5h),knowledge-manager T-docs propagation (~1.25h)
> **Ship target**: aria-plugin v1.31.0 (single cycle Phase B → D)

---

## Task Group Overview

| Group | Topic | Scope ref | Est |
|-------|-------|-----------|-----|
| T-backends | New `ci_backends/` package (ABC + dataclasses + Aether + GHA stub + static registry) | proposal §A | ~3h |
| T-refactor | `pre_merge_gate.py` refactor (DEFAULT_CONFIG + `_normalize_config` alias + `resolve_ci_backend` + dispatch in `gate_check`) | proposal §B | ~1h |
| T-tests | Test rewrite (23 mock target collapse + 6 new test classes covering AC-2 through AC-5) | proposal §C | ~3-3.5h |
| T-docs | Doc updates (CLAUDE.md Rule #8 + 2 SKILL.md files) | proposal §D | ~1.25h |
| T-rule6 | Rule #6 substitute (structural fixture + ≥27 unit tests README + dual-path dogfood) | proposal §E | ~1.5-2h |
| T-bump | 5+1 SOT v1.31.0 bump | proposal §F | ~0.5h |

---

## T-backends — New `ci_backends/` package (~3h)

<!-- AC-4 (registry pattern) + AC-5 (contract surface) + AC-2 (GHA stub safety) -->

- [ ] 1.1 Create `aria/skills/phase-c-integrator/scripts/ci_backends/` directory
- [ ] 1.2 Implement `base.py` — `CIBackend` ABC + `CIStatus` + `InFlightStatus` dataclasses (per proposal §A.1 + AC-5)
- [ ] 1.3 Implement `aether.py` — migrate `detect_aether()` + `_query_aether()` + `verify_aether_in_flight_flag()` logic from `pre_merge_gate.py` (zero behavior change, Hard Constraint #1)
- [ ] 1.4 Implement `github_actions.py` — real `probe()` (`shutil.which("gh")` + `gh auth status`) + `query_pr_ci()` / `query_branch_in_flight()` raising NIE with operable message (Hard Constraint #4 + AC-2.2)
- [ ] 1.5 Implement `__init__.py` — static import `BACKENDS = [AetherBackend, GitHubActionsBackend]` (Hard Constraint #8 + AC-4.1)
- [ ] 1.6 Verify zero decorator / zero entry-point — `grep -rn "@register\|entry_points" aria/skills/phase-c-integrator/scripts/ci_backends/` returns 0 (AC-4.4)

## T-refactor — `pre_merge_gate.py` refactor (~1h)

<!-- AC-1 (Aether backward) + AC-3 (alias) + AC-7 (NIE abort) -->

- [ ] 2.1 Update `DEFAULT_CONFIG` (replace `primitive_preference` / `no_aether_fallback` with `ci_backends` / `no_ci_fallback`, per proposal §B.1)
- [ ] 2.2 Implement `_normalize_config(config)` — alias translation **before** `{**DEFAULT_CONFIG, **config}` merge with DeprecationWarning emit + both-keys-present new-wins resolution (Hard Constraint #3 + #9 + AC-3)
- [ ] 2.3 Implement `_translate_value(old_key, old_value)` — handles per-key value-shape translation (`primitive_preference: ["aether-ci-cli"]` → `ci_backends: [{"name": "aether-ci-cli"}]`)
- [ ] 2.4 Replace `detect_aether()` with `resolve_ci_backend(config)` — config-first explicit then `BACKENDS` static-order probe fallback (Hard Constraint #8 + AC-4.2)
- [ ] 2.5 Refactor `gate_check()` body — dispatch via `backend.query_pr_ci()` / `backend.query_branch_in_flight()`;**NIE MUST propagate** (Hard Constraint #7 + AC-2.3, do NOT catch-and-route-to-`_no_ci_output`)
- [ ] 2.6 Rename `_no_aether_output()` → `_no_ci_output()` (preserve all behavior, only rename)
- [ ] 2.7 Update imports: `from ci_backends import CIBackend, CIStatus, InFlightStatus, BACKENDS, AetherBackend, GitHubActionsBackend`

## T-tests — Test rewrite (~3-3.5h)

<!-- AC-1 (regression) + AC-2 (GHA stub safety) + AC-3 (alias) + AC-4 (registry + precedence) -->

### Mock target collapse (existing 21 test methods)

- [ ] 3.1 Refactor `TestDetectAether` → `TestAetherBackendProbe` — 4 cases (which aether ok / no binary / config exists / both miss) — change mock target to `AetherBackend.probe`
- [ ] 3.2 Refactor `GateCheckTests` (15 cases) — collapse 3 stacked mocks (`detect_aether` + `verify_aether_in_flight_flag` + `_query_aether`) to `AetherBackend.probe` + `AetherBackend.query_pr_ci` + `AetherBackend.query_branch_in_flight` (per R1 M-1 substance convergence)
- [ ] 3.3 Refactor `TestNoAetherFallback` → `TestNoCIFallback` — 2 cases (skip_with_warning / abort), update mock to `resolve_ci_backend` returns None
- [ ] 3.4 Verify all 21 existing test methods PASS post-rewrite (AC-1.1 regression check)

### New test classes (AC-2 through AC-5)

- [ ] 3.5 `TestGHAStubAbortNotSkip` (3 cases per AC-2): probe success + query_pr_ci NIE → propagate / query_branch_in_flight NIE → propagate / verify NIE is **NOT** caught and routed to `_no_ci_output`
- [ ] 3.6 `TestAliasKeyPath` (3 cases per AC-3.1+3.2+3.4): old `no_aether_fallback` solo → translated + warning / old `primitive_preference` solo → translated + warning / warning message contains exact expected string (AC-3.4 silent rot prevention)
- [ ] 3.7 `TestBothKeysPresentNewWins` (1 case per AC-3.5 + Hard Constraint #9): old + new both present → new wins + `both_keys_present` warning emitted + old discarded
- [ ] 3.8 `TestBackendRegistry` (5 cases per AC-4): empty config auto-detect / explicit config order / unknown name skip / Aether-precedes-GHA when both probe true / decorator-free verify
- [ ] 3.9 `TestNormalizeConfigSequencing` (2 cases per ba F-04): `_normalize_config` runs **before** `{**DEFAULT_CONFIG, **config}` merge (assertion: stub `_normalize_config` to track call order)
- [ ] 3.10 `TestProbeCacheIsolation` (2 cases per ba F-05): tearDown invokes `cache_clear()` OR module-level dict reset; verify probe call count consistent across tests

### Test isolation hardening (ba F-05)

- [ ] 3.11 Choose lru_cache strategy:**Option A** — keep `@functools.lru_cache(maxsize=1)` on `probe()`, add `tearDown` cache_clear calls;**Option B** — replace with module-level `_probe_cache: dict[type[CIBackend], bool]` + `reset_probe_cache()` helper. **Recommended Option B** per backend-architect F-05 (less hidden state)
- [ ] 3.12 Add `tearDown` (or `pytest` fixture) ensuring probe cache reset between tests

## T-docs — Doc updates (~1.25h)

<!-- AC-6 (doc consistency) + AC-2 (NIE behavior in SKILL.md) -->

- [ ] 4.1 Rewrite `CLAUDE.md` Rule #8 L432-444 to backend-agnostic phrasing (per proposal §D.1 + AC-6.1) — keep Aether as "default backend (10CG Lab 内部)" example
- [ ] 4.2 Update `aria/skills/phase-c-integrator/SKILL.md` — replace ~10 aether-specific references with backend-agnostic phrasing; verify all 10 sites against grep `aether-ci-cli\|aether ci status\|no_aether_fallback` post-edit
- [ ] 4.3 Add `aria/skills/phase-c-integrator/SKILL.md` §C.2.4.X "CI Backends" new section (~40 lines): backend selection algorithm + backend table (Aether real + GHA stub + future) + config schema example + alias deprecation notes + NIE-abort behavior callout (Hard Constraint #7)
- [ ] 4.4 Add `aria/skills/config-loader/SKILL.md` L183/L189 alias deprecation note (R1 M-2 fix): "v1.31.0+: `no_aether_fallback` → `no_ci_fallback`; old key still readable until v2.0"
- [ ] 4.5 Verify `standards/` zero touch — `git diff --stat standards/` empty (AC-6.4 + Hard Constraint #5)

## T-rule6 — Rule #6 substitute (~1.5-2h)

<!-- AC-7 (Rule #6 substitute per deterministic Skill pattern) -->

- [ ] 5.1 Create `aria-plugin-benchmarks/aria-ci-backend-abstraction/` directory
- [ ] 5.2 Write `README.md` — mirror Sprint 1 forgejo-hosts pattern: §AC behavior table (12+ rows mapping AC-1~AC-8 to test name + expected) + §Structural fixture explanation (decorator-free static registry rationale) + §Unit test count breakdown + §How this substitutes Rule #6 (deterministic Skill — no AI capability AB testable)
- [ ] 5.3 Write structural fixture sample — `mock_ci_backend.py` showing how to implement new backend (subclass `CIBackend` + add to `BACKENDS` list in `__init__.py`)
- [ ] 5.4 Verify ≥27 unit tests count (T-tests delivers 30+;summary in README §Unit test breakdown)
- [ ] 5.5 Dual-path dogfood smoke evidence (Aether-installed run):
  - `python3 -c "from ci_backends.aether import AetherBackend; print(AetherBackend.probe())"` (expect True on Aria self)
  - `python3 -m phase_c_integrator.scripts.pre_merge_gate --pr <test-pr>` (expect verdict equivalent pre-refactor)
- [ ] 5.6 Dual-path dogfood smoke evidence (GHA-installed run, manual):
  - `python3 -c "from ci_backends.github_actions import GitHubActionsBackend; print(GitHubActionsBackend.probe())"` (expect True if `gh auth` ok)
  - Manual: invoke gate_check via Python REPL with mock probe returning GHA → assertRaises NotImplementedError (Hard Constraint #7 verification)
- [ ] 5.7 Document substitute rationale in README §"Why not /skill-creator benchmark": deterministic Python function refactor + ABC contract, no LLM prompt variable → structural fixture + unit test + behavior preservation = substantive equivalent (per [[feedback_deterministic_structural_skill_rule6_substitute]])

## T-bump — 5+1 SOT v1.31.0 (~0.5h)

<!-- AC-8 (5+1 SOT ship) -->

- [ ] 6.1 `aria/.claude-plugin/plugin.json` — `"version": "1.31.0"`
- [ ] 6.2 `aria/.claude-plugin/marketplace.json` — top-level `"version": "1.31.0"` + `plugins[].version: "1.31.0"`
- [ ] 6.3 `aria/VERSION` — `1.31.0`
- [ ] 6.4 `aria/CHANGELOG.md` — new entry **above** v1.30.0 entry (per R1 m-1); v1.29.0 placeholder block 不动
- [ ] 6.5 `aria/README.md` — version field + Skills count + Agents count verify
- [ ] 6.6 Main repo `CLAUDE.md` — `插件版本: v1.31.0` line
- [ ] 6.7 6 SOT consistency check — grep `1.31.0` across all SOT files, count = 6 expected unique appearances

---

## Phase boundary tasks (Phase C + D, post Phase B)

### Phase C.1 — Commit (~10min, after Phase B all green)

- [ ] 7.1 Stage aria/ submodule files (ci_backends/ + pre_merge_gate.py + tests + 3 SKILL.md files + 5 SOT files) per Aria git-add-specific-files convention (no `git add -A`)
- [ ] 7.2 Commit aria/ submodule with Conventional Commits message (`feat(phase-c-integrator): CI backend abstraction + Aether migration + GHA stub (#XXX)`)
- [ ] 7.3 Stage main repo files (`openspec/changes/` archive prep + CLAUDE.md plugin version + `aria-plugin-benchmarks/aria-ci-backend-abstraction/` fixture + 6 audit reports from post_spec)
- [ ] 7.4 Commit main repo `feat(m6-hygiene): aria-ci-backend-abstraction v1.31.0 + gitlink bump + benchmark fixture`

### Phase C.2 — PR + merge + Rule #8 pre-merge gate (~30min)

<!-- This Spec touches the very file Rule #8 enforces — verify dogfood -->

- [ ] 8.1 Push aria/ submodule branch → create Forgejo PR aria-plugin#XX
- [ ] 8.2 Rule #8 pre-merge gate self-check (`/aria:state-scanner` or direct invocation):aria-plugin master 无 in-flight + PR CI passing (or vacuously satisfied per aria-plugin no-required-CI state)
- [ ] 8.3 Merge aria-plugin PR → post-merge SHA verify dual remote (forgejo origin + github mirror)
- [ ] 8.4 Update main repo aria/ gitlink to post-merge SHA + push main repo branch → create main repo PR (if separate) OR direct push to master
- [ ] 8.5 3-way SHA parity verify: aria-plugin local=origin=github + main repo local=origin=github
- [ ] 8.6 Race-guard: `git fetch --all` before merge to detect sister terminal CHANGELOG.md or CLAUDE.md edits (per [[feedback_claude_md_project_status_high_contention]])

### Phase D.1 — Progress update (~5min)

- [ ] 9.1 Update main repo CLAUDE.md L488 `**更新**` line to ship date
- [ ] 9.2 Update aria-plugin VERSION file mtime ensures fresh
- [ ] 9.3 No UPM update needed (Aria self has no UPM, per `[[project_aria_no_runtime_upm]]`)

### Phase D.2 — Archive (~5min)

- [ ] 10.1 Move `openspec/changes/aria-ci-backend-abstraction/` → `openspec/archive/{ship-date}-aria-ci-backend-abstraction/` per Rule #5 + Phase D.2

### Phase D.3 — Handoff (~15-30min if session > 4h)

- [ ] 11.1 Evaluate Rule #9 handoff trigger (this cycle ~10-10.5h = clear trigger)
- [ ] 11.2 Write `docs/handoff/{date}-aria-ci-backend-abstraction-v1.31.0-shipped.md` with 9-section template per `standards/conventions/session-handoff.md`
- [ ] 11.3 Update `docs/handoff/latest.md` pointer
- [ ] 11.4 Memory candidates evaluation per DEC §Memory candidates (2 candidates pending: brainstorm-phase substance convergence + Critical-but-addressable-downstream pattern)
- [ ] 11.5 Commit + push handoff doc

---

## Task ordering + dependency notes

**Critical path** (must run sequentially):
1. T-backends 1.2 (base.py ABC) **must precede** T-backends 1.3 (aether.py) + 1.4 (github_actions.py)
2. T-backends 1.5 (`__init__.py` static registry) **must precede** T-refactor 2.4 (`resolve_ci_backend`)
3. T-refactor (full) **must precede** T-tests (mock target depend on new symbols)
4. T-tests 3.1-3.4 (regression rewrite) **must precede** T-tests 3.5-3.10 (new test classes) — gives clean baseline
5. T-docs 4.2 (SKILL.md edit) + 4.3 (new §C.2.4.X section) can parallelize with T-tests
6. T-rule6 5.5-5.6 (dogfood smoke) **must run after** T-tests 3.4 (all tests green) for valid evidence
7. T-bump (full) **must be last** in Phase B — needs all Deliverables A-E green
8. Phase C/D ordering per `[[feedback_sequenced_multirepo_gitlink_bump]]`:aria PR merge first → main gitlink bump second → main push

**Parallel opportunities** (within Phase B):
- T-backends 1.3 + 1.4 (Aether + GHA stub) can run parallel if same dev (different files)
- T-docs 4.1 (CLAUDE.md) + 4.2 (SKILL.md) + 4.4 (config-loader SKILL.md) parallel
- T-rule6 5.2 (README) writing parallel with T-tests
- Phase C.1 7.2 commit message can be drafted in parallel with 8.1 PR creation prep

---

## Dependencies

- **Predecessor (must be done)**: Sprint 1 `aria-forgejo-hosts-parameterization` v1.30.0 ✅ shipped 2026-05-27
- **Parallel sibling tracks (no file collision)**:
  - M6 sister terminal Spec #1 / #2 / #3 / #4 — touches aria-orchestrator + main repo CLAUDE.md (collision risk: §项目状态 section + footer);本 cycle 触 Rule #8 段 (L432-444) 与 sister 改动区域**不在同一 markdown block**,理论低风险但需 race-guard `git fetch` 前置
  - `aria-submodule-gate-block-flip` Spec — v1.29.0 reserved,2026-06-07 hard date;本 cycle 不动 CHANGELOG v1.29.0 placeholder block (per R1 m-1 + Hard Constraint TBD)
- **External**: 无 (Aether 现行版本足够;无 aether-plugin 改动需求)

---

## Risk acknowledgment (cross-ref proposal §Risk + Mitigation)

| Task | Risk | Acknowledged mitigation |
|------|------|----------------------|
| 3.1-3.10 | Test rewrite estimate 2h → 3-3.5h (R1 M-1) | Estimate locked at 3-3.5h;超 4h 触发 owner check |
| 3.11-3.12 | lru_cache test isolation (ba F-05) | Option B (module-level dict) recommended |
| 6.4 | CHANGELOG v1.31.0 vs v1.29.0 ordering | v1.31.0 entry 写在 v1.30.0 上方,v1.29.0 placeholder 不动 |
| 8.6 | Sister terminal CLAUDE.md race | `git fetch --all` 前置 + 改动只触 Rule #8 段 |
| 11.2 | Handoff Rule #9 trigger | session > 4h confirmed,clear trigger |

---

**Total Estimated**: ~10-10.5h Phase B + ~1h Phase C + ~30-50min Phase D = **~12h end-to-end cycle**
