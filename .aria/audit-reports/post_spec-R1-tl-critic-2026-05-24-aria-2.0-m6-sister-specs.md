# Post_Spec R1 Audit (combined) — tech-lead-critic — Spec #2 + #3

> **Auditor**: tech-lead-critic
> **Round**: R1 combined (Phase A.2 post_spec)
> **Specs audited**: aria-2.0-m6-e2e-resilience (#2, 1634 lines) + aria-2.0-m6-docs (#3, 1057 lines)
> **Spec status at audit**: Draft (commit 5d85617)
> **Spec #1 baseline**: aria-2.0-m6-cost-acceptance Approved c29a800
> **DEC reference**: DEC-20260524-001
> **Verdict**: **NEEDS_FIX** (both Specs)
> **Per-Spec verdict**: Spec #2 = **NEEDS_FIX** (1 Critical anchor-target + 4 Important), Spec #3 = **NEEDS_FIX** (3 Critical + 4 Important)
> **Cross-Spec verdict**: 4 X-findings (2 X-Critical, 2 X-Important)

---

## Summary

Both Specs demonstrate strong R1 craft — Spec #1's lessons (REPO_ROOT 1-level canonical / schema column SoT / 0-1-2 exit code / binary-falsifiable / 2-pass propagation) are visibly applied throughout. However, a combined-mode audit surfaces **8 actionable defects that two parallel single-Spec dispatches would miss**, plus 4 cross-Spec consistency gaps. The single most severe finding is **C-tl-#2-1**: Spec #2's entire TG-B (~13h, AC-3/AC-4) is anchored on `aria_layer1/state_machine.py` as the cov target and DI refactor target, but **this file does not exist** in the codebase (state machine logic is distributed across `extension.py` / `comment_poll.py` / `reconciler.py` / `tick_runner.py`). This is a scaffold-helpers-drift-without-callers (`[[feedback_scaffold_helpers_drift_without_callers]]`) violation at Spec scope and blocks Phase B until owner picks one of three resolution paths. Spec #3 has 3 Critical findings (CLAUDE.md Diff enumeration is mis-counted in 2 places — frontmatter says "8+1 diffs" but tasks says "9 diffs"; existing Rules are #1-#9 not #1-#6; Probe 1 regex won't match the live README badge format) that together indicate the Diff enumeration was idealized rather than driven by `git diff` against the live CLAUDE.md. Cross-Spec finding **X-C-tl-1** identifies a BOTH-locations link-path drift (Spec #2 says `humanized-command-patterns.md` lives at `standards/autonomous/...` while Spec #3 README cross-refs use `../../../../standards/autonomous/...` — neither is hand-verified against actual repo depth from the Spec #2 sample location). 3 of 8 actionable defects (37%) are surfaced only via combined audit, validating the combined-mode rationale.

---

## Cross-Spec findings (priority)

### X-Critical

- **X-C-tl-1 — BOTH-locations cross-ref path arithmetic not byte-verified between Specs**

  Spec #2 §C.3 specifies the footer link in `aria-orchestrator/evals/m6-prompt-quality/corpus/sample-NN.md` as:
  `[standards/autonomous/humanized-command-patterns.md](../../../../standards/autonomous/humanized-command-patterns.md)`
  (4 `../` levels — `corpus/` → `m6-prompt-quality/` → `evals/` → `aria-orchestrator/` → repo root).

  Spec #2 tasks.md C-corpus-3 reproduces the same 4-level relative path in the template.

  Spec #3 B.3.2 says it cross-refs Spec #2 corpus at `aria-orch/evals/m6-prompt-quality/corpus/` (uses the **shorthand** `aria-orch/` — the actual repo directory is `aria-orchestrator/`). Spec #3 AC-6 evidence check `grep -q "aria-orch/evals/m6-prompt-quality" standards/autonomous/humanized-command-patterns.md` would PASS even if the file literally writes `aria-orch/` not `aria-orchestrator/` — encoding the shorthand permanently.

  Worse: Spec #3 task T-B3.2.6 says: `See also: aria-orch/evals/m6-prompt-quality/...` (literal `aria-orch/`, not a hyperlink). This is in a Lab-shareable file (`standards/autonomous/humanized-command-patterns.md`) destined for the `standards` submodule — other Lab projects (Kairos, SilkNode) cloning `standards` will see a path that doesn't resolve in their checkout.

  **Concrete fix**:
  - Spec #2 §C.3 + tasks C-corpus-3: keep 4-level relative path (`../../../../standards/autonomous/...`) — these are *within* the Aria main repo so a relative path is correct.
  - Spec #3 B.3.2 + tasks T-B3.2.6 + AC-6: change all `aria-orch/` to `aria-orchestrator/` (full directory name) AND change the cross-ref form from a bare path to an explanatory sentence: `In the Aria repository (https://github.com/10CG/Aria), see aria-orchestrator/evals/m6-prompt-quality/ for M6 E2E corpus samples and scores.` Lab-shareable file must not assume the reader is checked out at repo-root of `Aria`.
  - Update Spec #3 AC-6 evidence regex to: `grep -q "aria-orchestrator/evals/m6-prompt-quality" standards/autonomous/humanized-command-patterns.md`.

- **X-C-tl-2 — DEC-20260524-002 (Aria #124) submodule pointer gate not consumed by either Spec; Spec #3 P-10 runbook is now structurally out-of-date**

  `13035d8` (dev-claude2, 2026-05-24, just landed) ships `DEC-20260524-002` — a CONVERGED brainstorm for an `(B+) hardened pre-merge submodule pointer regression gate` to be Spec'd in aria-plugin `phase-c-integrator/SKILL.md §C.2.5`. The decision establishes a NEW invariant: any submodule pointer bump in a PR must pass `git merge-base --is-ancestor <master-ptr> <feature-ptr>` (with fail-loud fetch hardening), at PR-level (v1.28.0 warn-only → v1.29.0 block).

  Spec #3 T-B0 "standards submodule operation runbook" (10 steps) does NOT reference the new gate. Step T-B0.10 `git add standards` followed by a main-repo commit will, in v1.29.0+, be subject to the new gate. If the standards `feat/autonomous-docs` branch is force-pushed or rebased between T-B0.7 (merge) and T-B0.8 (local pull), the gate could BLOCK the main-repo commit that bumps the standards pointer.

  Spec #4 (release-closeout) per DEC-20260524-001 §2 lists `submodule branch verify (default branch on master not feature, per feedback_submodule_branch_before_archive)` as a pre-release gate. With DEC-20260524-002 landed, this pre-release gate should now align with (or subsume) the new `merge-base --is-ancestor` mechanism.

  **Concrete fix** — Spec #3 only (Spec #4 not in audit scope but flagged downstream):
  - Spec #3 §Constraints: add new constraint section `### DEC-20260524-002 submodule pointer gate coordination` noting that T-B0 runbook executes while aria-plugin v1.28.0 (warn-only) is shipping; record warn-mode output if observed during T-B0.10. If v1.29.0 (block-mode) is live before this Spec's Phase C, T-B0 runbook must explicitly include `git fetch standards origin` before T-B0.5 commit (per DEC-20260524-002 §4 Hardening 1).
  - Spec #3 §Risks: add R-M6D-9 (severity: Medium) — "v1.29.0 submodule gate may block T-B0.10 if standards/ feature branch is not strictly ancestor of master after merge. Mitigation: T-B0 runbook explicit `git fetch` step + check `git -C standards merge-base --is-ancestor master feat/autonomous-docs` before pointer bump."
  - Spec #3 §Cross-references: add `.aria/decisions/2026-05-24-aria-124-submodule-pointer-regression-gate.md` (DEC-20260524-002).

### X-Important

- **X-I-tl-1 — AD slot allocation ghosts: Spec #3 claims AD-M6-8 RESERVED without topic, but Spec #2 Q-NEW-1 introduces a NEW decision topic that has no AD slot**

  Spec #2 introduces Q-NEW-1 (Hybrid mock layer 4 SDK + 2 HTTP) as a NEW architectural decision post-brainstorm. Spec #2 AD-M6-4/5/6 are claimed for: is_synthetic mechanism / pre-flight provenance / AdvancingClock DI. The hybrid mock-layer matrix itself is documented in §B.1 mock-layer-per-mode rationale doc but **has no AD slot** — it is an architectural decision (deviating from a single-layer mock convention) that future maintainers would search architecture-decisions.md to find.

  Concurrently, Spec #3 §How AD-M6-8 explicitly RESERVED with no topic, with risk R-M6D-7 acknowledging `[[feedback_ad_slot_backfill_checkpoint]]` and tasks.md T-B6.3 hedging "Retired or filled during Phase B".

  Net effect: there is an unallocated architectural decision (Q-NEW-1 mock-layer rationale) at the same time another Spec reserves an unused slot. Per `[[feedback_ad_slot_backfill_checkpoint]]`, pre-archive checklist must fail-if-placeholder.

  **Concrete fix**: re-allocate Spec #3 AD-M6-8 to Spec #2 for the Hybrid mock-layer decision. Update both Specs:
  - Spec #2 frontmatter `AD allocation reservation`: change "AD-M6-4 / AD-M6-5 / AD-M6-6 reserved" to "AD-M6-4 / AD-M6-5 / AD-M6-6 / AD-M6-8 reserved (AD-M6-8 for Q-NEW-1 Hybrid mock-layer)".
  - Spec #2 §How table: add row `AD-M6-8 | Hybrid mock layer (4 SDK + 2 HTTP) per failure semantic | Mock layer is per-mode, NOT uniform. 4 modes (Infra-1/2/3 + LLM-4) at SDK boundary because failure originates above HTTP. 2 modes (LLM-5 invalid JSON, LLM-6 5xx) at HTTP layer because failure semantic IS the HTTP body shape. Per [[feedback_mock_layer_per_failure_semantic]] M6 evidence`.
  - Spec #3 frontmatter `AD allocation reservation`: remove AD-M6-8 claim. Note "AD-M6-8 transferred to Spec #2 for Q-NEW-1 Hybrid mock-layer decision".
  - Spec #3 §How AD-M6-8 row: delete or note "transferred to Spec #2".
  - Spec #3 R-M6D-7: delete (no longer applicable).

- **X-I-tl-2 — 3-day cost trending precondition gate is documented as prose only; mechanically enforceable but not enforced at Phase B branch creation**

  Spec #2 frontmatter line 9 states "Spec #2 Phase B MUST NOT start until Spec #1 AC-7 (`--check-3-day-history`) PASS". Spec #2 tasks "Phase B precondition" (lines 12-24) tells the user to run the command and STOP if it fails — but this is **prose discipline**, not a mechanically enforced gate.

  Spec #1 §G AC-7 ships the script `validate-m6-handoff.py --check-3-day-history`. Spec #2 has no integration that *automatically* invokes this script as part of `phase-a-planner` Phase A.3 → Phase B.1 branch creation. A future AI operator (or human) skimming "Phase B precondition" could pattern-match-skip if confident that Spec #1 shipped recently.

  Per `[[feedback_paper_fix_antipattern]]`: gate documentation without enforcement is a paper-fix.

  **Concrete fix** — Spec #2 only:
  - Spec #2 tasks.md A-infra-1: add explicit failure clause: `If exit code != 0, write '.aria/blocked-by-spec1-precondition.md' with run output, stage as the first commit of Phase B branch, and exit Phase B. Re-attempt Phase B kickoff only after cron has accumulated ≥3 consecutive snapshots and re-running --check-3-day-history exits 0.`
  - Spec #2 §AC-1 evidence section: add explicit gate-failure trace assertion: any Phase B commit message must NOT precede `--check-3-day-history` PASS. Verify via `git log --grep="--check-3-day-history" --pretty=format:%H | head -1` in feature branch; first AC-1 evidence commit must show this script output recorded in `.aria/probes/m6-gate-check.md`.

## Spec #2 findings (aria-2.0-m6-e2e-resilience)

### Critical

- **C-tl-#2-1 — `aria_layer1/state_machine.py` does not exist; entire TG-B AC-4 + B-sm-1 are anchored on a non-existent file (scaffold-helpers-drift-without-callers violation)**

  Spec #2 §B.3, §B-sm-1, §B-sm-2, §B-sm-4, AC-4 evidence, R-M6-14 — all reference `aria_layer1/state_machine.py` or `aria-orchestrator/hermes-extensions/aria-layer1/aria_layer1/state_machine.py` as both the cov target (`--cov=aria_layer1.state_machine`) and the DI refactor target (B-sm-1 "Audit `state_machine.py` for all `datetime.now()` calls. Replace each with `self._clock.now()`").

  **Filesystem verification**: this file does NOT exist. `find aria-orchestrator/hermes-extensions/aria-layer1 -name "state_machine.py"` returns nothing. State machine logic is distributed across at least 4 files:
  - `extension.py` (extension dispatch + rework-round cap default 3)
  - `comment_poll.py` (S7→S8 transition, per AD-M5-1)
  - `reconciler.py` (S7 fallback sweep, spec_drift threshold default 70)
  - `tick_runner.py` (alloc tick / state advancement)

  Plus tests at `aria-layer1/tests/test_state_machine_skeleton.py` covering S0/S_FAIL/S4_LAUNCH/S8_MERGE.

  Per `[[feedback_scaffold_helpers_drift_without_callers]]`: helpers/specs ahead of callers ship wrong column/signature. Here the Spec is ahead of the code — there is no `state_machine.py` to refactor or `--cov` against.

  Three resolution paths (owner decision REQUIRED before Phase B); each must be propagated 2-pass (proposal §B.2/B.3 + tasks B-sm-* + AC-4 + R-M6-14 + Cross-references):

  - **Path A — File extraction (~+4-6h B-sm-0 prerequisite)**: Phase B first creates `state_machine.py` by extracting the dispatch state machine from `extension.py` + `tick_runner.py` + `comment_poll.py` + `reconciler.py`. This is a refactor with its own risk; widen scope honestly.
  - **Path B — Multi-file cov target (~no scope change, but AC-4 must be rewritten)**: change `--cov=aria_layer1.state_machine` to `--cov=aria_layer1.extension --cov=aria_layer1.comment_poll --cov=aria_layer1.reconciler --cov=aria_layer1.tick_runner`. AdvancingClock DI is introduced across these 4 files (the actual `datetime.now()` sites are in `extension.py` / `comment_poll.py` / `reconciler.py` / `schema_migrate.py`). Update AD-M6-6 from "clock injected at AriaStateMachine constructor" to "clock injected at each module's dispatch entrypoint; module-level `_clock` reference defaulting to `RealClock()`".
  - **Path C — Treat state machine as a *logical* abstraction**: ship a new shallow `state_machine.py` module that re-exports the relevant transition functions from existing modules (≤50 LOC adapter); `--cov` against this re-export module exercises the underlying paths transitively. This is the minimal-scope variant of Path A.

  **Recommendation**: Path B (no new file, accurate against codebase reality, AD-M6-6 becomes clearer). Path B requires no extra task budget but does require rewriting AC-4 evidence, B-sm-1 task body, and AD-M6-6 decision text.

  **Severity = Critical**: this is not a typo — the Spec's AC-4 (100% cov gate) cannot pass against a non-existent file. Phase B implementer would either silently create a stub file (Path A surprise expansion) or rewrite AC-4 (Path B drift from Spec text). Either is a Spec-vs-reality break.

### Important

- **I-tl-#2-1 — Pre-flight $2/dispatch cap (§A.5) has no runtime enforcement mechanism**

  Spec §A.5 line 179 states "real throwaway cost; hard cap: $2 per dispatch, total ≤$6 for 3 dispatches combined". AC-6 evidence script greps `cost_usd` post-hoc from `m6-preflight-log.md`. There is no `pre-spending estimate → abort if expected > $2` mechanism described. If a single LLM call produces $5 of tokens, the post-hoc grep catches it after the money is spent.

  **Concrete fix**: §A.5 add sub-clause `Pre-spending estimate enforcement: before dispatching each pre-flight issue, query Zhipu (or the routed metered provider) for the estimated token count via dry-run/cost-preview API if available. If the estimate × unit_price exceeds $1.50 (75% of $2 cap), abort with [BLOCKED] message in m6-preflight-log.md. Document this in AD-M6-5.` Update task A-dispatch-5 to include the pre-spending estimate step. Add unit test fixture for the abort path.

  If no provider cost-preview API exists, ship a hard `max_tokens` clamp (e.g., `max_tokens=8000` → ~$0.50 ceiling at known unit price) on pre-flight dispatches and document the per-token unit price assumption.

- **I-tl-#2-2 — Mock-shape discipline asserts exception class identity but does not bind exception import path; SDK refactor renaming `RateLimitError` would silently break tests**

  §B.1 line 261 LLM-4 mock: `RateLimitError(retry_after=30)`. §B.1 tail "Mock-shape discipline" line 265-269: "use the actual exception classes from the production code path". But the §B.1 table merely names the exception, not its import location (`from zhipu_client import RateLimitError`? from `aria_layer1.errors`? from upstream Zhipu SDK?).

  Per `[[feedback_scaffold_helpers_drift_without_callers]]`: Phase B implementer might create a local `class RateLimitError(Exception): pass` in the test file rather than importing the actual class, restoring the mock-shape antipattern the Spec is trying to prevent.

  **Concrete fix**: §B.1 mock-shape discipline section: append `Each exception class MUST be imported by canonical path from its production module; the test file MUST contain an explicit import statement of the exception class. Verified by AC-3 evidence sub-check: 'grep -E "^from .* import (ProcessKilledError|AllocTerminatedError|RateLimitError|ProviderUnavailableError)" aria-orchestrator/tests/test_crash_*.py | wc -l' returns ≥ 6 (one per relevant test file).` Update AC-3 evidence section.

  If a needed exception class does NOT yet exist in the codebase (e.g., `ProcessKilledError`, `AllocTerminatedError`), Phase B must define it in the production code path FIRST, then import in tests. Mark this as B-scaffold-0 (NEW task, ~0.5h).

- **I-tl-#2-3 — Deterministic state list (S0/S1/S4/S5/S7/S8/S9 + S_FAIL) is not cross-cited against the existing test_state_machine_skeleton.py SoT**

  §B.3 line 300 enumerates deterministic states. `aria-orchestrator/hermes-extensions/aria-layer1/tests/test_state_machine_skeleton.py` (already committed) covers S0 idempotency + S_FAIL (quota_exhausted, timeout) + S4_LAUNCH (30s ack) + S8_MERGE (30s API). The Spec list omits S4_LAUNCH and S8_MERGE distinct from S4/S8 — actual code has more granular sub-states.

  Spec's S2/S3/S6 "stochastic" classification (line 309) — is S6 actually stochastic? Per existing test naming `test_t_cron_direct_transition.py`, S5→S6 might be deterministic (commit validator + reconciler). The S2/S3/S6 trio appears to be inferred from "LLM-driven transitions" but may not align with the actual M2-shipped state machine.

  **Concrete fix**: §B.3 add citation to `test_state_machine_skeleton.py` Coverage map header comment (lines 7-20 of that file): list the 10 tests and their state-transition mapping. Spec must explicitly resolve S4 vs S4_LAUNCH and S8 vs S8_MERGE. If S6 is not LLM-driven, move to deterministic list. **Required action**: open `test_state_machine_skeleton.py` + relevant production files; have backend-architect produce a definitive state list table in §B.3 with citations to source line numbers before Phase B kickoff.

- **I-tl-#2-4 — TG-A → TG-C sequencing claim "TG-C cannot meaningfully start until Day-7 probe is written" is NOT enforced in any task ordering**

  Spec §What says TG-C is "sequential after TG-A 7d run completes". Tasks ordering DAG (line 727-757) shows TG-C-corpus → TG-C-scores → TG-C-crossref → TG-C-acceptance as a sequential chain after TG-A. But TG-C-corpus task C-corpus-3 says "After the TG-A 7-day run completes, owner fills in actual dispatch data". The template creation (10 empty `sample-NN.md` files with placeholder content) could be done at Day-1.

  Risk: Phase B implementer creates all 10 sample-NN.md stubs at Day-1, marks TG-C-corpus tasks DONE, then forgets to backfill on Day-7. AC-5 grep check for "humanized-command-patterns.md" footer would PASS even with placeholder content.

  **Concrete fix**: tasks C-corpus-3 last bullet: split into C-corpus-3a (Day-1: create empty templates) and C-corpus-3b (Day-7+: fill `Dispatch ID` / `Issue type` / `State at dispatch` / `is_synthetic` / `Command text` placeholders with actual values from `dispatches` table). C-corpus-3b is blocked-on TG-A AC-1 PASS. Add to AC-5 evidence: `grep -c "\[FILL:" aria-orchestrator/evals/m6-prompt-quality/corpus/sample-*.md` must return 0 (no unfilled placeholders).

## Spec #3 findings (aria-2.0-m6-docs)

### Critical

- **C-tl-#3-1 — CLAUDE.md Diff enumeration inconsistent (8 vs 9 vs 8+1); existing CLAUDE.md has 9 rules but Diff 6 says "Rule #1-#6 frozen" implying only 6 exist**

  Three contradictory statements in Spec #3:

  1. §A.1 header line 44: `CLAUDE.md v1.0.4 → v2.0 (8+1 diffs)` — "8+1" suggests 8 original + 1 incremental.
  2. §A.1 body line 47: `The 9 diffs to apply (Diff 1-8 from draft + Diff 9 incremental)` — "9 diffs".
  3. Diff 6 (line 64): `"不可协商规则"章节不修改` — "Rules #1-#6 text body is FROZEN. No deletions, no modifications. AD11 compliance."

  **Live CLAUDE.md verification**: `grep -nE "^[0-9]+\.\s+\*\*" CLAUDE.md` returns **9 numbered rules** (Rules #1-#9). Rule #7 (Secret hygiene), Rule #8 (pre-merge gate), Rule #9 (session handoff) were added 2026-04-12 → 2026-05-13 incrementally — AFTER the M0 T5.3 draft was written.

  Diff 6's text "Rule #1-#6 FROZEN" implies 6 rules total or only Rules #1-#6 are non-modifiable while #7-#9 might be modifiable. Diff 9 doesn't clarify this — it merely says Rule #7/#8/#9 body "is already in live CLAUDE.md".

  Per `[[feedback_spec_v2_body_propagation_2pass]]` + `[[feedback_paper_fix_antipattern]]`: a Spec that enumerates diffs against a "live" target must verify each diff against the live file. The "8 diffs from draft" + "Diff 9 incremental" framing only makes sense if AD11 was written when only 6 rules existed. With 9 rules now in CLAUDE.md, the diff enumeration must be recomputed.

  **Concrete fix**:
  - Spec #3 §A.1: rename diffs to be unambiguous. The new enumeration should be:
    - Diffs 1-5: from M0 T5.3 draft (header / 项目定位 / 两层 AI 分工 / 信息地图 / 技术约束 — adds new content, no rule-body edits)
    - Diff 6: NO-OP on Rules #1-#9 (NOT #1-#6). All 9 rule bodies FROZEN. AD11 must be re-confirmed to cover all 9 rules.
    - Diff 7: add §Aria 2.0 运行时 chapter
    - Diff 8: update §项目状态 (plugin version v1.22.0 → v1.27.0 etc.)
    - Diff 9: bump `**版本**: 1.0.4 → 2.0.0` (single-line atomic edit)
  - Spec #3 AC-1 first check `grep -c "Rule #" CLAUDE.md` must return ≥ 9 (line 388 already states this — but the rest of the Spec text contradicts itself).
  - Spec #3 T-A1.6 task body: change "verify Rules #1-#6 text is UNCHANGED" to "verify Rules #1-#9 text is UNCHANGED".
  - Spec #3 §Constraints `### CLAUDE.md Rule #1-#6 text is FROZEN (AD11 hard constraint)`: rename header to `### CLAUDE.md Rule #1-#9 text is FROZEN (AD11 hard constraint extended)` and note AD11 was authored when only 6 rules existed; the constraint scope is now extended to all 9.
  - Spec #3 R-M6D-1 ("CLAUDE.md Diff 6 accidentally modifies Rule #1-#6 text"): extend to "#1-#9".

- **C-tl-#3-2 — Probe 1 regex `(?<=Plugin-v)[0-9]+\.[0-9]+\.[0-9]+` matches the EXISTING (stale) README badge `Plugin-v1.15.2`; verification of "drift" semantics is unclear**

  Spec #3 §A.6 Probe 1 (`m6-version-badge-match`) extracts version via `grep -oP '(?<=Plugin-v)[0-9]+\.[0-9]+\.[0-9]+' README.md | head -1`.

  **Live verification**: `grep -oP '(?<=Plugin-v)[0-9]+\.[0-9]+\.[0-9]+' README.md` returns `1.15.2` (badge currently stale). Compared against `plugin.json` version `1.27.0`, the probe currently reports `DRIFT badge=1.15.2 plugin=1.27.0` — exit 1.

  This is the **correct probe behavior** today. But Spec #3 task T-A6.1 says: "Test PASS case: ensure README badge and plugin.json version match (should pass after T-A2.1). Test FAIL case: temporarily edit plugin.json version to a dummy value." The PASS case ordering — "should pass after T-A2.1 [README badge update]" — implies T-A6 is RUN AFTER T-A2. But T-A6.1 is sequenced BEFORE T-A2.1 in the Effort baseline (`A.2 README ~1.5h, A.6 state-checks ~1.5h` — `T-A6` is documented after `T-A2`, so probably runs after). This is murky in the proposal.

  Worse: the **second line** of README ([line 217 confirmed via grep]) `aria/                       # Aria Plugin (submodule, v1.13.0)` ALSO matches `[0-9]+\.[0-9]+\.[0-9]+` if Probe 1 regex is changed. Currently the lookbehind `(?<=Plugin-v)` saves this — but `head -1` is order-dependent on grep line output.

  **Concrete fix**:
  - Spec #3 §A.6 Probe 1: clarify the regex purpose. The current `(?<=Plugin-v)` is fine but the line `head -1` means "first occurrence on first line containing `Plugin-v`". Pin the source line by adding `--line-number` filter or anchor to first 20 lines: `head -20 README.md | grep -oP '(?<=Plugin-v)[0-9]+\.[0-9]+\.[0-9]+' | head -1`.
  - Spec #3 T-A6.1: explicit task ordering — "T-A6 MUST execute after T-A2 (README badge update). If executed before, probe will fail expectedly; this is allowed but must be documented in tasks.md sequencing." Update T-A6 pre-condition to depend on T-A2.
  - Spec #3 task T-A6.1 sub-bullet: add literal command-line test trace: after T-A2.1 PASS, run `bash -c "BADGE=\$(head -20 README.md | grep -oP '(?<=Plugin-v)[0-9]+\.[0-9]+\.[0-9]+' | head -1); PLUGIN=\$(python3 -c \"import json; print(json.load(open('aria/.claude-plugin/plugin.json'))['version'])\"); echo \$BADGE \$PLUGIN; test \"\$BADGE\" = \"\$PLUGIN\" || exit 1"` — expected output `1.27.0 1.27.0` exit 0.

- **C-tl-#3-3 — Diff 9 references plugin version `v1.27.0` (current per `c7e376b`) but §A.6 Probe 1 + AC-3 + brainstorm-source DEC-20260524-001 §2 reference `v1.26.0` (stale by one bump)**

  Spec #3 in different places references the plugin version:
  - §A.2 line 86: `Plugin version badge: update v1.15.2 → v1.27.0 (current per commit c7e119f submodule bump to 1b8ec3f)`. ✓
  - §A.3 line 102: `(currently v1.27.0)`. ✓
  - §AC-3 line 411: `grep -q "v1.27.0" README.md`. ✓
  - But DEC-20260524-001 §2 line 110: `Diff 9 增量: Rule #7/#8/#9 + 插件版本 catch-up v1.26.0` (DEC says v1.26.0).
  - And the live CLAUDE.md line 434 currently states: `插件版本: v1.22.0 (aria-plugin, 30 user-facing + 6 internal Skills + 11 Agents + Rule #9 + §2.3 frontmatter schema...)` (v1.22.0).

  So the Spec correctly identifies v1.27.0 as the target, but the live CLAUDE.md is at v1.22.0 (5 bumps stale), the DEC says catch-up to v1.26.0 (1 bump stale from current), and the Spec itself says v1.27.0. This is THREE distinct version values across SoT documents.

  Diff 8 task T-A1.8: `插件版本 = actual value from aria/.claude-plugin/plugin.json` (read at write time). T-A1.8 actually does the right thing — read live SoT. But §A.3 release notes line 102 hardcodes "v1.27.0" — if T-A1.8 reads it later as v1.27.1 (post a patch bump), release notes will drift.

  **Concrete fix**:
  - Spec #3 §A.3 line 102: change `(currently v1.27.0)` to `(currently v$PLUGIN_VERSION where $PLUGIN_VERSION is read at task execution time from aria/.claude-plugin/plugin.json — Phase B implementer reads, then text-substitutes once at commit time)`.
  - Spec #3 §AC-3 evidence: change literal `grep -q "v1.27.0" README.md` to `PLUGIN=$(python3 -c "import json; print(json.load(open('aria/.claude-plugin/plugin.json'))['version'])"); grep -q "v$PLUGIN" README.md`. This way AC-3 stays valid if plugin version bumps mid-Phase-B.
  - Spec #3 T-A3 (Release notes): change all literal `v1.27.0` references to use `$PLUGIN_VERSION` substitution at task execution time.

### Important

- **I-tl-#3-1 — T-B0 standards submodule runbook does not specify what happens if owner declines T-B0.7 merge (PR pending)**

  Spec #3 T-B0.7: `Owner action: merge the feature branch in the standards repo (via PR or direct push to master, owner discretion). Wait for merge confirmation.`

  T-B0.8 onwards assumes merge has happened. But if owner has merge authority delegated to PR review and the PR sits pending for hours/days, the Spec's overall TG-DOCS-B is blocked. There is no documented "what to do while waiting" path or timeout.

  Per `[[feedback_t15_owner_blocking_pattern]]`: cluster deployment tasks split AI-runnable + owner-action; AI segment commits then task remains in_progress. This pattern is not applied here.

  **Concrete fix**: T-B0.6 (push feature branch) becomes the natural AI-segment terminus. T-B0.7-T-B0.10 are owner-action + post-merge AI-resume. Tasks.md should split T-B0 into:
  - T-B0-AI (T-B0.1 through T-B0.6 + AC-6 partial): AI ships standards files on feature branch, pushes, opens PR if applicable.
  - T-B0-OWNER: owner merge.
  - T-B0-AI-RESUME (T-B0.8 through T-B0.10): pointer bump after owner merge confirmation.
  - Phase B branch stays at in_progress between segments; task progress updater honors this.

- **I-tl-#3-2 — Lab-shareable vs Aria-specific boundary expressed only via header comment + km M-km-R2-005 reference; no machine-enforceable rule**

  Spec #3 §P-11 + §B.4 + §AD-M5-11 establish the boundary: `standards/autonomous/*.md` Lab-shareable, `aria-orchestrator/docs/layer-boundary-contract.md` Aria-specific. Enforcement is "header comment in file" + AD reference.

  Risk: future contributor adds Aria-specific file to `standards/autonomous/` (e.g., `standards/autonomous/aria-zhipu-routing.md`) — header comment is voluntary; nothing catches the boundary violation.

  Spec #3 ships 3 state-checks probes but none catches this. Per the Spec's own §Why Problem 3 ("No automated drift detection. Without state-checks.yaml probes for [...] stale architecture docs, the documentation inconsistencies observed in M1-M5 will recur silently"), this is an inconsistent application of the principle.

  **Concrete fix**: add Probe 4 `m6-standards-autonomous-aria-leak` to §A.6 (or defer to Spec #4 if Spec #3 is fully booked):
  ```yaml
  - name: "m6-standards-autonomous-aria-leak"
    description: |
      Detect Aria-specific filenames or content leaking into standards/autonomous/.
      Lab-shareable principle violation per km M-km-R2-005 / AD-M5-11.
    command: |
      LEAK=$(grep -lE "aria-orchestrator|aria-layer1|aria-layer2|hermes|aria-runner" standards/autonomous/ 2>/dev/null || true)
      [ -z "$LEAK" ] && echo "OK no aria-specific leak" || { echo "LEAK $LEAK"; exit 1; }
    severity: warning
    fix: "Move aria-specific content to aria-orchestrator/docs/; keep standards/autonomous/ Lab-shareable"
  ```
  (Note: `humanized-command-patterns.md` itself may legitimately reference `aria-orchestrator/evals/m6-prompt-quality/` as a "see also" — adjust regex to exclude legitimate cross-refs by negative lookahead or by counting occurrences > 3 as leak.)

- **I-tl-#3-3 — TG-DOCS-B v2.0.1-deferrable boundary creates an undefined state if owner defers AFTER Spec #3 archives**

  Spec #3 frontmatter: `TG-DOCS-B may ship as v2.0.1 if 5w calendar slips per Q-final-1 Menu C`. §Constraints `TG-DOCS-B is v2.0.1-deferrable`. §Out-of-scope OOS-7 (`DOCS as two separate Specs`) explains why single-Spec internal TG split was chosen.

  Pre-archive checklist (tasks.md line 455-462) says: `If TG-DOCS-B deferred to v2.0.1 per owner decision: document the deferral decision in docs/release-notes-v2.0.0.md §Known Limitations`. But what is Spec #3's archive status if TG-DOCS-A ships in v2.0.0 and TG-DOCS-B defers? Spec is partially archived? `phase-d-closer` openspec-archive Skill expects a single Spec → single archive event. Per `[[feedback_submodule_branch_before_archive]]`: substantial Spec changes (like TG-DOCS-B) cannot be in-flight at archive time.

  **Concrete fix** — one of two:
  - **Option A**: keep single Spec. Archive status: archive only after ALL of T-A* + T-B* complete (whether v2.0.0 or v2.0.1). If v2.0.0 ships without TG-DOCS-B, Spec stays in `openspec/changes/` (un-archived) until v2.0.1 ships. Document this in pre-archive checklist.
  - **Option B**: actually split into two Specs at deferral decision time. If owner defers at end of T-A6 (TG-DOCS-A complete), create a NEW Spec `aria-2.0-m6-docs-architecture` (carrying T-B* tasks) and archive current Spec as TG-DOCS-A-only. Update §Out-of-scope OOS-7 to note this conditional split.

  **Recommendation**: Option A (no Spec split), but spec the archive-status semantics explicitly. The current Spec ambiguity is a footgun — `aria:openspec-archive` Skill won't know how to handle partial completion.

- **I-tl-#3-4 — Probe 3 `m6-arch-doc-stale` will fire indefinitely if TG-DOCS-B is deferred to v2.0.1 — but the probe is `enabled: true`**

  `docs/architecture/system-architecture.md` `Last Updated: 2026-04-12` (live confirmed). Today (2026-05-24) age is 42 days, threshold 90 days. After TG-DOCS-A ships v2.0.0 (suppose 2026-06-21), age = 70 days. By 2026-07-12 (90 days from 2026-04-12), probe fires. If TG-DOCS-B is v2.0.1-deferred 4 more weeks past v2.0.0, the probe fires continuously during the deferral window.

  Spec acknowledges this in R-M6D-6 (severity: Low): "If TG-DOCS-B slips, state-scanner reports the staleness as advisory only." But state-scanner `severity: warning` still produces noise — every `state-scanner` invocation will surface this finding. The probe becomes uninformative (cried wolf) during the deferral.

  **Concrete fix**: Probe 3 add deferral-aware logic — read `docs/release-notes-v2.0.0.md` for the `TG-DOCS-B v2.0.1 deferral` marker (T-A3.5). If marker present AND v2.0.0 release date is within 60 days of today, suppress the probe with `OK (TG-DOCS-B deferred to v2.0.1, suppression active until v2.0.1 ships)`. Sample shell:
  ```bash
  if [ -f docs/release-notes-v2.0.0.md ] && grep -q "TG-DOCS-B deferred to v2.0.1" docs/release-notes-v2.0.0.md; then
    echo "OK (TG-DOCS-B deferred; probe suppressed)"; exit 0
  fi
  # then existing logic
  ```
  Document the suppression behavior in proposal §A.6 Probe 3 description.

---

## Verdict rationale

**Both Specs NEEDS_FIX** with **R2 highly likely to close most findings within ~1 round** of fix-pass + audit, given:

- **Spec #2** has only 1 Critical (C-tl-#2-1 state_machine.py absence) — but this Critical is a Spec-vs-reality break that blocks AC-4 ship and would surface as a Phase B blocker on Day 1. Once owner picks Path A/B/C and Spec text is updated 2-pass, this is straightforwardly resolved. The 4 Important findings are well-scoped (each has a specific §line/task fix). Spec #2 effort baseline 29h is realistic per `[[feedback_phase_budget_compounding]]` (TG-A 10h is reasonable for an observation infrastructure task; TG-B 13h includes a +1h for Q-NEW-1 documentation that has now been correctly absorbed; TG-C 6h aligns with collect+score+verify discipline).

- **Spec #3** has 3 Criticals all centered on the **CLAUDE.md Diff enumeration drift**. The root cause is that Diffs were enumerated from the M0 T5.3 draft (which assumed only 6 rules) without re-grounding against the live 9-rule CLAUDE.md. C-tl-#3-1, C-tl-#3-2, and C-tl-#3-3 together suggest the Spec author did not do `git diff` against the live CLAUDE.md/README.md before drafting; the Diff list and Probe regex were not bug-hunted per `[[feedback_pre_draft_bug_hunt_discipline]]`. Spec #3 fix-pass requires backend-architect or knowledge-manager to actually open both files side-by-side and re-list each diff with line citations.

- **Cross-Spec X-Critical** X-C-tl-1 (BOTH-locations path mismatch) and X-C-tl-2 (DEC-20260524-002 not consumed) are exactly the kind of finding combined-mode audit exists for — they would slip through a serial dispatch.

**Combined-mode audit value confirmed**: of 8 actionable findings, 3 (37%) require cross-Spec reasoning that single-Spec dispatch cannot perform: X-C-tl-1 (cross-Spec path math), X-C-tl-2 (cross-Spec DEC consumption), X-I-tl-1 (AD slot reallocation between Specs). This validates the combined-mode rationale.

**Recommended next-round trajectory** (per `[[feedback_audit_r2_collapse_default_vs_owner_invoked]]`):

- Fix-pass agent applies all 8 findings + 4 X-findings using inline `R1-X-tl-N` / `R1-C-tl-#2-1` / etc. trace comments per `[[feedback_audit_driven_fix_conventions]]`.
- R2 challenge (3-agent: cr + ai + tl-critic, scope-limited to R1 fixes) — if R1 reduction ≥70% AND no new C and ≤2 NEW Important, can collapse R3 per the R2-collapse rule (Spec #1 set the precedent at 90.6% R1 reduction).
- Spec #2 C-tl-#2-1 specifically requires **owner choice** between Path A/B/C — this is an owner-Q escalation per `[[feedback_brainstorm_owner_escalation_discipline]]`. Should be the only owner-Q in fix-pass; recommend Path B (no scope expansion, accurate against codebase reality).

**Anti-paper-fix self-check**: every Critical and Important above proposes a concrete §section/task line edit, not a "consider clarifying" hedge. The 8 + 4 findings are mechanically actionable by a fix-pass agent.
