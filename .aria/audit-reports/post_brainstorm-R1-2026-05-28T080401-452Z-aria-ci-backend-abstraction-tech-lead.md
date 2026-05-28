---
checkpoint: post_brainstorm
mode: convergence
round: 1
agent: tech-lead
target: .aria/decisions/2026-05-28-ci-backend-abstraction-brainstorm.md
change_id: aria-ci-backend-abstraction
change_id_status: prospective (brainstorm phase, no proposal.md yet — pre-write validation bypassed for post_brainstorm)
timestamp: 2026-05-28T08:04:01.452Z
vote: PASS_WITH_WARNINGS
critical_count: 0
major_count: 3
minor_count: 4
---

# Round 1 Audit — aria-ci-backend-abstraction (tech-lead)

## §Findings

### M1 — Test scope under-estimated by 2.3× (Deliverable C)

- **id**: `7c4a1f3e`
- **severity**: major
- **category**: testing
- **scope**: `aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py`
- **type**: issue
- **summary**: DEC §Deliverables C claims `~10 处 mock.patch.object(gate, "detect_aether", ...)` need rewrite. Actual count = **23 lines** (verified via grep on real file, 254 LOC / 21 tests). Estimate is 2.3× under and the test file path in DEC is also wrong (`scripts/` should be `tests/`).
- **rationale**: Under-estimating test-rewrite blast radius is the single most common cause of 8h Spec slipping to 12-16h. The DEC's ~2h test-rewrite estimate within ~8.5h total is tight even at face value; at actual 23 mock sites + new ABC mock target (`AetherBackend.probe`) + new GHA stub behavior tests + new alias-key path tests, ~2h is unrealistic. The wrong path also signals the brainstorm did not open the actual file.
- **recommended_action**: Re-estimate Deliverable C from ~2h to ~3-3.5h; update DEC §Deliverables C path to `aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py`; have spec-drafter Phase A.1 grep-verify mock count before locking task estimates. Total Phase B estimate revises to ~9.5-10h (still within "8-12h L3" boundary audit memo upper bound).

### M2 — `config-loader/SKILL.md` doc surface omitted from Deliverable D

- **id**: `b2e8d917`
- **severity**: major
- **category**: documentation
- **scope**: `aria/skills/config-loader/SKILL.md` L183, L189
- **type**: issue
- **summary**: DEC §Deliverables D enumerates only `CLAUDE.md Rule #8 L432-444 重写` + `aria/skills/phase-c-integrator/SKILL.md ~10 处`. But `aria/skills/config-loader/SKILL.md` documents `primitive_preference` and `no_aether_fallback` config keys with original semantics — if Q2 alias path is to work and Q5 wording goes backend-agnostic, this file must also be updated (or its current text becomes outright misleading post-ship).
- **rationale**: config-loader is a cross-cutting infrastructure Skill; stale config-key documentation there is consumed by every Skill that reads `.aria/config.json`. Missing it from Deliverable D risks a post-ship inconsistency where the new ABC contract documentation (phase-c-integrator/SKILL.md) and the old key documentation (config-loader/SKILL.md) disagree. Memory `feedback_release_phase_d_5_files_synchronization` warns precisely that "code merged ≠ users benefited" without full doc sync.
- **recommended_action**: Add `aria/skills/config-loader/SKILL.md` to DEC §Deliverables D explicitly. Estimate +0.25h. Cover both adding new `ci_backends` key documentation and marking `primitive_preference` / `no_aether_fallback` as `Deprecated since v1.31.0 (alias preserved)`.

### M3 — Alias-vs-new-key conflict resolution policy undefined

- **id**: `91d4f2a7`
- **severity**: major
- **category**: architecture
- **scope**: `pre_merge_gate.py` config merge path + Q2/Q3 intersection
- **type**: decision
- **summary**: Q2 (soft alias) + Q3 (config-first + probe fallback) intersect at a case the DEC does not specify: what happens when a project's `.aria/config.json` contains **both** legacy `primitive_preference: ["aether-ci-cli"]` and new `ci_backends: [...]` keys simultaneously (e.g. half-migrated config copy-paste)? Which wins? Does the alias resolver run before or after the new-key resolver? Is there a precedence warning?
- **rationale**: This is exactly the silent-failure class Q2 §Drop (a) was trying to prevent. Without explicit precedence policy, two well-meaning users with sequential edits to the same config could get different runtime behavior on the same code. Standard practice (12-factor / Hashicorp config layering): new-key wins, alias only fires when new-key is absent, deprecation warning fires regardless. DEC should declare this.
- **recommended_action**: Add §Hard constraints #8: "Alias resolution precedence: if `ci_backends` is present, `primitive_preference` is ignored with a single-line warning; alias path only activates when `ci_backends` is absent or empty." Add a unit test in Deliverable C for the dual-key case. Estimate +0.1h.

### m4 — Ship-slot risk: CHANGELOG ordering vs v1.29.0 reserved slot

- **id**: `4e8c01a2`
- **severity**: minor
- **category**: documentation
- **scope**: `aria/CHANGELOG.md` versioning narrative
- **type**: risk
- **summary**: v1.31.0 ships ~2026-05-29 (today+1), v1.29.0 ships 2026-06-07 (hard date). After v1.31.0 lands, CHANGELOG will read `[1.31.0] 2026-05-29` above `[1.28.0] 2026-05-24` — with the `[1.29.0]` entry inserted **out-of-date-order** when block-flip ships. This creates a reverse-chronological violation that downstream changelog parsers (and humans) trip on.
- **rationale**: Most CHANGELOG conventions assume strict reverse-chrono. Date-skip is not formally forbidden but is unusual enough that PR reviewers will flag it. Pre-declaring the v1.29.0 slot's date in a `[1.29.0] - 2026-06-07 (reserved)` placeholder entry in v1.31.0's CHANGELOG bump avoids the surprise.
- **recommended_action**: Phase C SOT bump should insert a reserved placeholder for `[1.29.0]` between `[1.31.0]` and `[1.28.0]`, stating "version slot reserved for `aria-submodule-gate-block-flip` ship 2026-06-07; entry deferred". This is a 30-second edit and prevents reviewer confusion.

### m5 — ABC `probe()` membership ambiguity

- **id**: `5d3b91e0`
- **severity**: minor
- **category**: architecture
- **scope**: new `ci_backends/base.py` ABC contract
- **type**: decision
- **summary**: DEC §收敛逻辑 §Q1 mentions `GitHubActionsBackend` stub has `probe()` real-implemented while `query_pr_ci()`/`query_branch_in_flight()` raise `NotImplementedError`. This implies `probe()` is part of ABC. But §Q4 contract surface only enumerates two abstract methods. Is `probe()` ABC-abstract, ABC-concrete-default, or backend-internal helper?
- **rationale**: If `probe()` is ABC-abstract, all future backends (GitLab/Forgejo Actions) must implement it. If it's backend-internal, the registry's auto-detect (Q3 probe fallback) needs a different uniform entry point. This boundary affects the contract surface every future backend implementer reads first.
- **recommended_action**: Add to DEC §Q4 contract surface: "ABC declares 3 abstract methods: `probe() -> ProbeResult` + `query_pr_ci(branch) -> CIStatus` + `query_branch_in_flight(branch) -> InFlightStatus`. `ProbeResult` is a third dataclass (available: bool, version_sha: str | None, raw_message: str)." Update Deliverable A description.

### m6 — Q5 "通用化" wording transition: missing concrete before/after example

- **id**: `c93f7d18`
- **severity**: minor
- **category**: documentation
- **scope**: CLAUDE.md Rule #8 L432-444 rewrite
- **type**: issue
- **summary**: DEC says Rule #8 will be rewritten "backend-agnostic with Aether as default example" but provides no before/after text sample. This is the only piece of master-repo CLAUDE.md being touched by this Spec, so a literal diff sketch in the DEC (or Phase A.1 proposal.md) reduces audit/review friction in subsequent rounds.
- **rationale**: Rule #8 is one of 9 non-negotiable rules; wording change is high-visibility. Without a draft, post_spec audit reviewers will spend a round debating phrasing rather than substance. Per memory `feedback_claude_md_project_status_high_contention`, CLAUDE.md edits are also high-contention with sister terminals.
- **recommended_action**: Phase A.1 proposal.md must include a literal before/after diff of Rule #8 L432-444 — not deferred to Phase B implementation. Cite "current single CI primitive (Aether) is the default" in the new wording explicitly so Q5 §Drop (c) "misleading" concern stays addressed.

### m7 — Sister-terminal CLAUDE.md contention risk under-stated

- **id**: `f1a05c2d`
- **severity**: minor
- **category**: process
- **scope**: multi-terminal coordination during v1.31.0 ship window
- **type**: risk
- **summary**: DEC §Hard constraints lists 7 items but does not mention concurrent ship coordination. v1.31.0 (this Spec, ~target 2026-05-29) and v1.29.0 (block-flip, hard 2026-06-07) have a ~9 day overlap window where two tracks may simultaneously edit `CLAUDE.md` project-status footer + plugin version + Rule #8 area.
- **rationale**: Memory `feedback_claude_md_project_status_high_contention` explicitly cites the 2026-05-27 forgejo-hosts ship as evidence that CLAUDE.md project-status block is high-contention. v1.31.0 (Rule #8 rewrite) + v1.29.0 (block-flip, also touches phase-c-integrator config + likely CHANGELOG header) overlap is a textbook case. multi-terminal-coordination Layer H frontmatter is the existing mitigation but the DEC doesn't reference it.
- **recommended_action**: Add §Hard constraints #9: "Multi-terminal coordination — both tracks must carry Layer H frontmatter (`track-id`, `phase`, `status`); `git fetch && git rebase` before any CLAUDE.md edit in v1.31.0 ship window (2026-05-28 .. 2026-06-07)." 15-minute cost, eliminates a real risk.

---

## §Per-dimension verdict

### (a) Substance convergence

The 5 decisions are internally self-consistent and **do** solve C5+C6 (multi-CI backend abstraction + `AETHER_CONFIG` path override), not paper-fix. Q1 (stub-vs-full split) provides the structural change C5 demanded without GHA implementation creep. Q3 (config-first + probe fallback) addresses C6's hard-coded `~/.aether/config.yaml` by making the path resolution backend-internal rather than a global constant. Q4 dataclass contract is substance (not stringly-typed). Q5 wording change makes the documentation 1:1 with the code. The one substance gap is M3 (alias vs new-key precedence undefined) — a meaningful hole in the Q2/Q3 intersection that needs a one-line policy. Otherwise the design coheres.

### (b) Hard constraints completeness

6 constraints listed are testable and well-formed individually, but the set is incomplete: M3 surfaces the need for a #8 (alias precedence policy), and m7 surfaces the need for a #9 (multi-terminal coordination during the v1.31.0↔v1.29.0 overlap window). Constraint #5 (standards/ zero-touch) was independently verified by grep: `standards/conventions/{issue-triage,submodule-pointer-hygiene,session-handoff}.md` have **0 hits** for `no_aether_fallback`/`primitive_preference` and ≤1 generic "Aether" mention in session-handoff (unrelated to CI backend semantics). Constraint #7 (ship-slot strict v1.31.0) is firm but does not address m4 CHANGELOG ordering. No conflicts among constraints. No untestable constraints.

### (c) Risk identification

DEC's implicit risk register (alias dead code, test rewrite, sister terminal CLAUDE.md contention) covers the obvious surface but understates two architecture-specific risks. (i) Alias-vs-new-key precedence (M3) is the silent-bug class that surfaces months after ship when a user pastes a hybrid config. (ii) ABC `probe()` membership ambiguity (m5) becomes a contract debt the moment a third backend (GitLab/Forgejo Actions) implementer reads the ABC and finds an under-specified surface. The DEC also under-weights test-rewrite blast radius (M1) — a process risk, not architecture, but it cascades into ship-window timing risk. Sister-terminal coordination (m7) is explicitly cited in memory but not in the DEC.

### (d) DEC document quality

Per-Q alternative drop rationales are strong substance, not strawman: every dropped option has a concrete failure mode cited (e.g. Q1(c) "blast radius 大,审计 surface 也大", Q3(a) "破坏现网零配置 UX", Q4(c) "stringly-typed no IDE 补全"). Cross-references are thorough (Boundary audit memo + handoff §6 carry-forward + aria-fleet strategic memo + 3 memory entries + forward Spec slots). Two under-justifications surface: (i) Q5(c) "去 Aether 化 misleading" is the weakest reject reason — could be argued either way and benefits from m6's literal before/after example. (ii) Deliverable C estimate is the only number in the DEC without a verification step shown; given M1 found 2.3× under-count, all deliverable estimates would benefit from a "grep-verified count" note in spec-drafter Phase A.1.

### (e) Implementation feasibility

The ~8.5h Phase B total is **tight and likely under** by ~1-1.5h given M1 (test rewrite ~3-3.5h, not ~2h) + M2 (+0.25h config-loader/SKILL.md) + M3 (+0.1h dual-key unit test) + m6 (+0.25h Rule #8 draft moved to Phase A.1 but cost still incurred) + m7 (+0.25h Layer H coordination). Revised realistic estimate: **~9.5-10h**, still inside the boundary audit's "8-12h L3" upper bound. The file-size math (387 LOC pre_merge_gate.py refactor + 23 mock sites + 959 LOC SKILL.md edits) is consistent with that range. **No feasibility blockers.** The stub-vs-full Q1 split is the right cycle boundary — it cleanly separates "design the contract" from "fill in GHA" and matches memory `feedback_sub_pr_scope_splitting_pattern`'s 3-stage decomposition principle (this Spec = stage a "contract scaffolding"; v1.32.0 GHA = stage b "feature fill"). The boundary between this Spec and next is drawable: stop at GHA `raise NotImplementedError("PR welcome")`; ship.

---

## §Final vote

**PASS_WITH_WARNINGS** — The DEC is structurally sound, the 5 decisions converge on a coherent design that genuinely solves C5+C6, and Q1's stub-vs-full split is the architecturally correct cycle boundary. Three Major findings (M1 test-rewrite under-estimate, M2 missing config-loader doc surface, M3 alias precedence policy) and four Minors warrant a Phase A.1 spec-drafter pass to incorporate before locking proposal.md scope, but none constitute Critical issues requiring REVISE.

---

**Relevant files**:
- Target DEC: `/home/dev/Aria/.aria/decisions/2026-05-28-ci-backend-abstraction-brainstorm.md`
- Refactor target: `/home/dev/Aria/aria/skills/phase-c-integrator/scripts/pre_merge_gate.py` (387 LOC verified)
- Test file (correct path): `/home/dev/Aria/aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py` (254 LOC, 21 tests, 23 mock sites verified)
- Missing doc surface: `/home/dev/Aria/aria/skills/config-loader/SKILL.md` L183, L189
- Rule #8 location: `/home/dev/Aria/CLAUDE.md` L432-446 verified
- standards/ grep verification: 0 hits for `no_aether_fallback`/`primitive_preference` across `standards/conventions/*.md` (DEC §Hard constraint #5 holds)
