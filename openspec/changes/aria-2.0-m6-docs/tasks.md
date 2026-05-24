# Tasks — aria-2.0-m6-docs

> **Spec**: [proposal.md](proposal.md)
> **Status**: Draft
> **Effort baseline**: ~33h impl (TG-DOCS-A ~11h + TG-DOCS-B ~22h; T-B0.10 +0.1h v1.29.0 gate). Single SoT — matches proposal.md §Effort baseline and frontmatter.
> **v2.0.1-deferrable**: TG-DOCS-B tasks (T-B*) may defer to v2.0.1 if 5w calendar slips (owner decision gate). TG-DOCS-A tasks (T-A*) ship with v2.0.0 unconditionally.
> **Agent**: knowledge-manager
> **AD allocation**: AD-M6-9 (namespace creation decision, T-B6; replaces AD-M5-11 per Q2 owner lock 2026-05-24 R1 audit), AD-M6-7 (probes design, T-A6), AD-M6-8 (reserved, T-B6)
> <!-- R1-X-T4 fix: AD-M5-11 → AD-M6-9 in frontmatter per Q2 owner lock. R1-T3-1 audit added to trajectory. -->

---

## Phase setup checklist (run before Phase B.1)

- [ ] Confirm standards submodule is on `master` branch: `git -C standards branch --show-current` → must output `master`
- [ ] Confirm no in-flight feature branch on standards: `git -C standards branch -a` → no `feat/` branch
- [ ] Confirm aria/.claude-plugin/plugin.json version field: `python3 -c "import json; print(json.load(open('aria/.claude-plugin/plugin.json'))['version'])"` → record actual value for AC-3 badge check
- [ ] Confirm CLAUDE.md current version: `grep "^\*\*版本\*\*" CLAUDE.md` → must show `1.0.4` (pre-TG-DOCS-A)
- [ ] Confirm docs/architecture/system-architecture.md current version: `grep "^\*\*Version\*\*" docs/architecture/system-architecture.md` → must show `1.9.0`
- [ ] Read `aria-orchestrator/docs/claude-md-revision-draft.md` fully — source for A.1 Diffs 1-8
- [ ] Per `[[feedback_clear_cache_before_code_change]]`: if plugin reports unexpected behavior, clear Claude Code plugin cache before testing CLAUDE.md v2.0

---

## TG-DOCS-A: Release-blocker tasks (~11h)

### T-A1: CLAUDE.md v1.0.4 → v2.0 (9 diffs) (~4h)

**Description**: Apply 9 structured diffs to `/home/dev/Aria/CLAUDE.md`. Source: `aria-orchestrator/docs/claude-md-revision-draft.md` for Diffs 1-8; Diff 9 is incremental (plugin version + version field bump).

**Pre-condition**: Phase setup checklist complete.

**Subtasks**:
- [ ] T-A1.1 Apply Diff 1: update top-level header block (项目本质 + 核心假设 + version line). Do NOT change 版本 number yet — that is Diff 9.
- [ ] T-A1.2 Apply Diff 2: add §身份演进 (v1.x → v2.0) subsection before §研究目标.
- [ ] T-A1.3 Apply Diff 3: add §两层 AI 分工 subsection after §十步循环 (live CLAUDE.md ~line 66). Max 20 lines. Layer 1: Hermes + Luxeno-routed GLM models = PM role. Layer 2: aria-runner + CC + aria-plugin = engineering role. Cross-link AD1 + AD6. <!-- R1-I3-4 fix: "Hermes + GLM" → "Hermes + Luxeno-routed GLM models" per 2026-05-21 redirect -->
- [ ] T-A1.4 Apply Diff 4: add `aria-orchestrator/` row to §子模块职责 table. Add two §目录导航 entries (architecture-decisions.md + layer-boundary-contract.md).
- [ ] T-A1.5 Apply Diff 5: add `✅ 实现 (v2.0)` line to §技术约束. Add clarifying v2.0 exception paragraph.
- [ ] T-A1.6 Apply Diff 6 (NO-OP): verify Rules #1-#6 text is UNCHANGED. Run `git diff HEAD -- CLAUDE.md | grep "^[-+]" | grep -E "规则 #[1-6]"` and confirm no deletions or modifications to rule bodies. If any diff appears on rule bodies, ABORT and investigate.
- [ ] T-A1.7 Apply Diff 7: add §Aria 2.0 运行时 chapter after §不可协商规则. Strictly ≤50 lines. Include: 分层叙述 (3-line ASCII), 与 6 条规则的关系 (table or list), 人类参与点 (S7), 详细入口 (4 cross-links).
- [ ] T-A1.8 Apply Diff 8: update §项目状态. Set: 当前阶段 = "v2.0 M6 执行中 (M1-M5 shipped)". 成熟度 = 0.9. 插件版本 = actual value from `aria/.claude-plugin/plugin.json`. 主项目版本 = v1.7.0. Add 运行时版本 line. Update 更新 date at bottom.
- [ ] T-A1.9 Apply Diff 9 (incremental): bump `**版本**: 1.0.4` → `**版本**: 2.0.0`. Update §项目状态 `插件版本:` field — live CLAUDE.md line ~434 shows `v1.22.0` (stale); read current value dynamically: `python3 -c "import json; print(json.load(open('aria/.claude-plugin/plugin.json'))['version'])"` and update to match (no hardcode). Verify Rule #7/#8/#9 body text is already present (no edit needed — they are already in live CLAUDE.md). Verify `phase_c_integrator.pre_merge_gate.no_aether_fallback` field name in Rule #8 matches `config.template.json`. Verify Rule #9 §2.3 cites `aria-plugin v1.22.x+` (already present; no edit if correct). <!-- R1-T3-3 fix: dynamic plugin.json read for §項目状態 version update; live CLAUDE.md shows v1.22.0 (stale vs v1.27.0 plugin.json SoT) -->

**AC verification (inline)**:
```bash
grep -c "Rule #" CLAUDE.md  # → ≥ 9
grep -q "**版本**: 2.0.0" CLAUDE.md  # → exit 0
grep -q "两层 AI 分工" CLAUDE.md  # → exit 0
grep -q "Aria 2.0 运行时" CLAUDE.md  # → exit 0
grep -q "aria-orchestrator" CLAUDE.md  # → exit 0
# Rule #1-#6 body freeze check (R1-I3-1 addition):
git diff HEAD -- CLAUDE.md | grep "^[-]" | grep "Rule #[1-6]"  # → must produce NO output
```

**AD11 compliance check (mandatory before next task)**:
```bash
# Rules #1-#9 text must be identical to pre-edit. Use git diff to verify.
# If any line in Rules #1-#9 block appears in the diff as a deletion, STOP.
# R1-I3-1: The Rule freeze scope extends to all 9 rules (not just #1-#6).
# Live CLAUDE.md already has Rules #7/#8/#9; Diff 6 confirms NO-OP for all 9 rule bodies.
git diff HEAD -- CLAUDE.md | grep "^[-+]" | grep "Rule #[1-9]"
# Deletions of rule body lines = AD11 violation → abort immediately.
```

---

### T-A2: README.md plugin badge + Aria 2.0 cross-link (~1.5h)

**Description**: Update `/home/dev/Aria/README.md` badge and add Aria 2.0 positioning paragraph.

**Subtasks**:
- [ ] T-A2.1 Update Plugin version badge: change `v1.15.2` → actual version from `aria/.claude-plugin/plugin.json` (read dynamically: `python3 -c "import json; print(json.load(open('aria/.claude-plugin/plugin.json'))['version'])"` — current is v1.27.0 per commit `c7e611f` but do not hardcode). Verify badge URL still resolves by inspecting badge format. <!-- R1-T3-3 fix: explicit dynamic read instruction; no hardcode -->
- [ ] T-A2.2 Add Aria 2.0 positioning paragraph after §What is Aria? section: "**Aria 2.0 (v2.0.0, in progress)** extends the methodology to autonomous execution. See [docs/architecture/system-architecture.md](docs/architecture/system-architecture.md) for the two-layer architecture."
- [ ] T-A2.3 Add cross-link to `docs/requirements/prd-aria-v2.md` in a suitable location (Roadmap subsection or Why Aria? section).

**AC verification**:
```bash
grep -q "v1.27.0" README.md && grep -q "Aria 2.0" README.md && exit 0
```

---

### T-A3: Release notes v2.0.0 (new file) (~2h)

**Description**: Create `/home/dev/Aria/docs/release-notes-v2.0.0.md`.

**Subtasks**:
- [ ] T-A3.1 Create file. Add frontmatter: `# Aria v2.0.0 Release Notes` + date + status.
- [ ] T-A3.2 Write **Plugin Compatibility** section (mandatory, closes brainstorm R1 cr-CH-8):
  - Title: `## Plugin Compatibility — aria-plugin 不随 Aria 2.0 同 bump`
  - Content: semantic boundary explanation (Aria main repo = methodology + autonomous runtime; aria-plugin = interactive Skills + Agents). Statement: aria-plugin does NOT bump to v2.0 when Aria v2.0.0 releases. Instructions for plugin users: no action needed.
- [ ] T-A3.3 Write **Highlights** section: M1-M5 delivery summary (Layer 1/2 architecture, dispatch loop, crash recovery, cost tracking, E2E resilience).
- [ ] T-A3.4 Write **Migration Notes** section: "non-migration" — no breaking changes for interactive Aria methodology users. Autonomous runtime is an additive internal layer. Note TG-DOCS-B v2.0.1 possibility.
- [ ] T-A3.5 Write **Known Limitations** section: TG-DOCS-B architecture docs may ship as v2.0.1 if calendar slips per Q-final-1 Menu C.
- [ ] T-A3.6 Write **Forgejo Discussion FAQ** section (text to be posted by owner as Forgejo Discussion thread post-release):
  - Q: Does aria-plugin need updating when Aria 2.0 releases? A: No.
  - Q: What changed in Aria 2.0 vs 1.x? A: Added autonomous runtime (aria-orchestrator). Methodology and plugin unchanged.
  - Q: Who is Aria 2.0 for? A: 10CG Lab internal projects only. The plugin remains universally available.

**AC verification**:
```bash
[ -f docs/release-notes-v2.0.0.md ] \
  && grep -q "Plugin Compatibility" docs/release-notes-v2.0.0.md \
  && grep -q "aria-plugin 不随" docs/release-notes-v2.0.0.md \
  && grep -q "Forgejo Discussion FAQ" docs/release-notes-v2.0.0.md \
  && exit 0
```

---

### T-A4: aria/README.md cross-link (~0.5h)

**Description**: Add Aria 2.0 cross-link to `/home/dev/Aria/aria/README.md`.

**Subtasks**:
- [ ] T-A4.1 Read existing `aria/README.md` to understand current content.
- [ ] T-A4.2 Add cross-link section at a suitable location (near bottom or after introduction): "This plugin (aria-plugin) is the interactive layer of Aria. For the Aria 2.0 autonomous runtime, see the [main Aria repository](https://github.com/10CG/Aria) and [aria-orchestrator](../aria-orchestrator/)."

**AC verification**:
```bash
grep -q "Aria 2.0" aria/README.md && exit 0
```

---

### T-A5 (merged into T-A3): Forgejo FAQ text

Forgejo Discussion FAQ text is written as part of T-A3.6. No separate task needed. Owner action: post the text as a Forgejo Discussion thread after Spec #4 tags v2.0.0. Spec #4 verifies the URL liveness; this Spec verifies the text exists.

---

### T-A6: .aria/state-checks.yaml 3 drift probes (~1.5h)

**Description**: Append 3 new probe entries to `/home/dev/Aria/.aria/state-checks.yaml`. Per `[[feedback_pre_draft_bug_hunt_discipline]]`: each probe command must be tested against both PASS and FAIL cases before commit.

**P-12 implementation (probes with detailed logic)**:

**Subtasks**:
- [ ] T-A6.1 Write Probe 1 `m6-version-badge-match` per proposal.md §A.6 (with anchored regex per R1-T3-2 fix). Task dependency: Probe 1 verification MUST run AFTER T-A2.1 (README badge update); before T-A2.1 it is expected to FAIL (stale badge v1.15.2 ≠ plugin.json v1.27.0). Test PASS case: run probe AFTER T-A2.1 → exit 0 "OK badge=1.27.0". Test FAIL case: before T-A2.1 (or temporarily restore old badge) → exit 1 "DRIFT badge=1.15.2 plugin=1.27.0". <!-- R1-T3-2 fix: ordering-independent via anchored regex; explicit task dependency note added -->
- [ ] T-A6.2 Write Probe 2 `m6-claude-md-version` per proposal.md §A.6. Test PASS case: run after T-A1.9 (CLAUDE.md version = 2.0.0), verify exit 0. Test FAIL case: before T-A1.9, probe must exit 1 with DRIFT message (version = 1.0.4 ≠ 2.0.0).
- [ ] T-A6.3 Write Probe 3 `m6-arch-doc-stale` per proposal.md §A.6 (with python3 datetime arithmetic per R1-I3-3 fix — no GNU `date -d`). Test PASS case: run after T-B1 (system-architecture.md Last Updated = 2026-05-24 → age = 0d < 90d), verify exit 0 "OK age=0d". Test FAIL case: temporarily set Last Updated to 2025-01-01 (age ≈ 508d > 90d), verify exit 1 "STALE age=508d". <!-- R1-I3-3 fix: date -d is GNU-only; replaced with python3 datetime in proposal.md §A.6 command -->
- [ ] T-A6.4 Append all 3 probes to `.aria/state-checks.yaml` under the `checks:` list. Maintain YAML validity: `python3 -c "import yaml; yaml.safe_load(open('.aria/state-checks.yaml'))"` must exit 0 after append.
- [ ] T-A6.5 Record AD-M6-7 decision in proposal.md §Key design decisions and in T-B6.

**AC verification**:
```bash
grep -c "m6-version-badge-match\|m6-claude-md-version\|m6-arch-doc-stale" .aria/state-checks.yaml
# must return 3
python3 -c "
import yaml, sys
data = yaml.safe_load(open('.aria/state-checks.yaml'))
names = [c['name'] for c in data.get('checks', [])]
required = {'m6-version-badge-match', 'm6-claude-md-version', 'm6-arch-doc-stale'}
missing = required - set(names)
sys.exit(1 if missing else 0)
"
# must exit 0
```

---

## TG-DOCS-B: Architecture tasks (~22h, v2.0.1-deferrable)

**Pre-condition for TG-DOCS-B**: TG-DOCS-A (T-A1 through T-A6) complete. Owner has confirmed whether TG-DOCS-B ships in v2.0.0 or v2.0.1 per Q-final-1 Menu C.

---

### T-B0: Standards submodule operation runbook (P-10) (~prerequisite, ~0.5h overhead)

**Description**: Execute the P-10 submodule operation sequence. This task is a prerequisite for T-B3 (which creates files in `standards/`). The runbook must be executed in this exact order. Per `[[feedback_submodule_branch_before_archive]]` and `[[project_meta_repo_pattern]]`.

**Runbook (step-by-step, execute sequentially)**:

- [ ] T-B0.1 Verify standards submodule is clean and on master: `git -C standards status` → clean working tree. `git -C standards branch --show-current` → `master`.
- [ ] T-B0.2 Create feature branch in standards submodule: `git -C standards checkout -b feat/autonomous-docs`
- [ ] T-B0.3 Create the `standards/autonomous/` directory: `mkdir -p standards/autonomous/`
- [ ] T-B0.4 Implement T-B3 (create files in `standards/autonomous/`). Return here after T-B3 subtasks complete.
- [ ] T-B0.5 Stage and commit in standards submodule:
  ```bash
  git -C standards add autonomous/
  git -C standards commit -m "feat(autonomous): add decision-autonomy-matrix + humanized-command-patterns (aria-2.0-m6-docs)"
  ```
- [ ] T-B0.6 Push feature branch to standards remote: `git -C standards push origin feat/autonomous-docs`
- [ ] T-B0.7 Owner action: merge the feature branch in the standards repo (via PR or direct push to master, owner discretion). Wait for merge confirmation.
- [ ] T-B0.8 After merge, update local standards pointer to master:
  ```bash
  git -C standards checkout master
  git -C standards pull origin master
  ```
- [ ] T-B0.9 Verify standards pointer is on master at the new commit: `git -C standards log --oneline -1` → should show the autonomous/ commit.
- [ ] T-B0.10 Stage the submodule pointer bump in the main Aria repo:
  <!-- R1-X-T2 fix: added v1.29.0 block-mode gate precondition per Q5 owner pre-decision (DEC-20260524-002 Aria #124). T-B0.10 pointer bump could be BLOCKED by the gate if standards feature branch is not a strict forward ancestor of master post-merge. -->
  **Precondition (v1.29.0 gate, per DEC-20260524-002 Aria #124)**: Before staging the pointer bump, verify aria-plugin v1.29.0+ block-mode gate compatibility. The standards feature branch must be a strict ancestor of master post-merge:
  ```bash
  # Fetch to ensure origin/master ref is fresh (fail-loud — do not grep success patterns):
  git -C standards fetch origin master
  # Verify standards feature branch is strict ancestor of master post-merge:
  MASTER_PTR=$(git -C standards rev-parse origin/master)
  FEATURE_PTR=$(git -C standards rev-parse HEAD)
  git -C standards merge-base --is-ancestor "$FEATURE_PTR" "$MASTER_PTR"
  # exit 0 = forward/ancestor relationship confirmed (safe to bump)
  # exit 1 = regression or divergence → ABORT and investigate
  echo "Gate PASS: standards branch is ancestor of master at $MASTER_PTR"
  ```
  Cross-ref: DEC-20260524-002 `.aria/decisions/2026-05-24-aria-124-submodule-pointer-regression-gate.md` §4 (B+) pre-merge gate design. This is the v1.29.0 block-mode precondition applied to standards submodule operations.
  Then stage:
  ```bash
  git add standards
  git status  # verify standards shows "modified: standards"
  ```
  This `git add standards` will be included in the main Aria repo commit that also includes all other TG-DOCS-B changes.

**Pre-archive verification** (per `[[feedback_submodule_branch_before_archive]]`):
Before this Spec archives, verify: `git -C standards branch --show-current` → `master`. Submodule must be on default branch at archive time.

---

### T-B1: docs/architecture/system-architecture.md v2.0 (~10h)

**Description**: Update `/home/dev/Aria/docs/architecture/system-architecture.md` from v1.9.0 to v2.0.

**Subtasks**:
- [ ] T-B1.1 Read the current file fully to understand existing structure and what must be preserved vs updated.
- [ ] T-B1.2 Update frontmatter: `**Version**: 1.9.0` → `**Version**: 2.0.0`. `**Last Updated**: 2026-04-12` → `**Last Updated**: 2026-05-24` (or actual implementation date). Add `**Parent PRD**: [prd-aria-v2.md]` reference alongside existing prd-aria-v1.md reference.
- [ ] T-B1.3 Update §Executive Summary: add two-layer AI execution model to "核心架构模式" list. Change "方法论研究项目" framing to include "参考实现". Add 自主运行时 as a new characteristic.
- [ ] T-B1.4 Add new §Three-Layer Architecture section: methodology layer (standards/) / tools layer (aria-plugin) / runtime layer (aria-orchestrator). ASCII diagram: show Layer 1 (Hermes + GLM 5.1) and Layer 2 (aria-runner container + CC + aria-plugin). Cross-link to `aria-orchestrator/docs/architecture-decisions.md`.
- [ ] T-B1.5 Add §Autonomy Model subsection: state machine overview (S0→S9 + S_FAIL). Human gate at S7_AWAITING_MERGE (AD10). Note crash recovery (M5 shipped, 3 infra modes + 3 LLM modes per Spec #2).
- [ ] T-B1.6 Add §Layer Boundary section: note that `aria-orchestrator/docs/layer-boundary-contract.md` (B.4) pins the inter-layer contract. Reference cost.json schema locked at Spec #1 `c29a800`.
- [ ] T-B1.7 Add §Version Scheme cross-reference: point to `docs/architecture/version-scheme.md` (B.2) for disambiguation of the four versioning streams.
- [ ] T-B1.8 Review all existing sections for accuracy against M1-M5 actual state. Update any v1.x-only descriptions to note v2.0 evolution. Preserve all valid existing content.
- [ ] T-B1.9 Final proofread: confirm Last Updated header is recent, Version is 2.0.0, all cross-links are relative paths.

**AC verification**:
```bash
grep -q "Version.*2.0.0" docs/architecture/system-architecture.md \
  && grep -q "Layer 1" docs/architecture/system-architecture.md \
  && grep -q "Layer 2" docs/architecture/system-architecture.md \
  && grep -q "Last Updated.*2026" docs/architecture/system-architecture.md \
  && exit 0
```

---

### T-B2: docs/architecture/version-scheme.md (new file) (~3h)

**Description**: Create `/home/dev/Aria/docs/architecture/version-scheme.md` disambiguating all four versioning streams.

**Subtasks**:
- [ ] T-B2.1 Create file with frontmatter: title, created date, status.
- [ ] T-B2.2 Write §Four Independent Versioning Streams table (per proposal.md §B.2 content spec). Include: stream name, repo/file, current version, SoT file, bump trigger, notes.
- [ ] T-B2.3 Write §Why Streams Are Independent section: explain why aria-plugin version ≠ Aria main repo version. Emphasize semantic boundary (plugin = interactive tools; main repo = methodology + runtime).
- [ ] T-B2.4 Write §Plugin Compatibility Clarification section: aria-plugin does NOT bump to v2.0. Cross-reference `docs/release-notes-v2.0.0.md §Plugin Compatibility`.
- [ ] T-B2.5 Write §Version Lookup Reference section: for each stream, the exact command or file path to find the current version.
- [ ] T-B2.6 Ensure ≥80 lines total.

**AC verification**:
```bash
[ -f docs/architecture/version-scheme.md ] \
  && grep -q "aria-plugin" docs/architecture/version-scheme.md \
  && grep -q "aria-orchestrator" docs/architecture/version-scheme.md \
  && grep -q "Aria 2.0 PRD" docs/architecture/version-scheme.md \
  && exit 0
```

---

### T-B3: standards/autonomous/ 2 files (Lab-shareable) (~5h)

**Pre-condition**: T-B0 feature branch setup complete (T-B0.1 through T-B0.3 done).

**P-11 content boundary**: `standards/autonomous/` files = curated Lab-shareable patterns + rubric guide. `aria-orchestrator/evals/m6-prompt-quality/corpus/` = raw M6 E2E corpus (Spec #2 TG-C). Cross-reference only; no content duplication. <!-- R1-X-T1 fix: aria-orch/ → aria-orchestrator/ -->

#### T-B3.1: standards/autonomous/decision-autonomy-matrix.md (~2h)

**Subtasks**:
- [ ] T-B3.1.1 Create file `/home/dev/Aria/standards/autonomous/decision-autonomy-matrix.md`.
- [ ] T-B3.1.2 Add Lab-shareable header: `<!-- Lab-shareable: this file is in standards/ and may be reused by other 10CG Lab projects. See aria-orchestrator/docs/layer-boundary-contract.md for Aria-specific implementation. -->`.
- [ ] T-B3.1.3 Write §Overview: what is an autonomy decision matrix, when to use it, PRD §553 source reference.
- [ ] T-B3.1.4 Write the core decision matrix table: rows = decision types (triage / dispatch / merge approval / cost threshold alarm / schema migration / crash recovery escalation). Columns = autonomy level (fully-auto / auto-with-audit-log / human-gate-required). Each cell: condition that triggers this level + rationale.
- [ ] T-B3.1.5 Write §How to Adapt for Your Project section (Lab-shareable guidance).
- [ ] T-B3.1.6 Add cross-reference: "See `aria-orchestrator/docs/layer-boundary-contract.md` for how Aria implements this matrix in the Layer 1 / Layer 2 boundary."
- [ ] T-B3.1.7 Verify ≥100 lines.

**AC verification** (included in AC-6):
```bash
[ -f standards/autonomous/decision-autonomy-matrix.md ] \
  && grep -q "Lab-shareable" standards/autonomous/decision-autonomy-matrix.md \
  && exit 0
```

#### T-B3.2: standards/autonomous/humanized-command-patterns.md (~2h)

**Subtasks**:
- [ ] T-B3.2.1 Create file `/home/dev/Aria/standards/autonomous/humanized-command-patterns.md`.
- [ ] T-B3.2.2 Add Lab-shareable header: `<!-- Lab-shareable: this file is in standards/ and may be reused by other 10CG Lab projects. For M6 E2E corpus samples, see aria-orchestrator/evals/m6-prompt-quality/corpus/ (Spec #2 TG-C). -->`. <!-- R1-X-T1 fix: aria-orch/ → aria-orchestrator/ -->
- [ ] T-B3.2.3 Write §PRD §639 Rubric section: **7 dimensions D1-D7** (SoT = Spec #2 §C.2; no divergence allowed):
  - D1: Naturalness — 0=robotic/template; 10=indistinguishable from skilled human
  - D2: Specificity — 0=vague; 10=precise actionable steps with exact file/function refs
  - D3: Tone appropriateness — 0=wrong tone for context; 10=matches request severity and relationship
  - D4: Completeness — 0=missing required context; 10=all context a developer needs included
  - D5: Conciseness — 0=verbose padding; 10=minimal words to convey full intent
  - D6: Technical accuracy — 0=incorrect references; 10=all file/function/commit references correct
  - D7: Autonomy footprint — 0=over-delegates; 10=appropriately scoped with no unnecessary asks
  Explain the **median** ≥ 7/10 threshold (per PRD §656 patched 2026-05-24 e884e62, median replaces mean — robust against bimodal score distributions).
  <!-- R1-X-T5 fix: original had 5 dimensions (naturalness/actionability/context-completeness/brevity/tone-appropriateness); synced to 7 dimensions D1-D7 per Spec #2 §C.2 SoT -->
  <!-- R1-X-T3 fix: mean → median per Q4 owner lock 2026-05-24, PRD §656 patched -->
- [ ] T-B3.2.4 Write ≥10 curated pattern entries. Each entry:
  ```
  ### Pattern N: <name>
  **Anti-pattern** (score < 5): <bad example>
  **Good practice** (score ≥ 7): <good example>
  **Rationale**: <why the good practice is better>
  ```
  Draw patterns from M5 E2E evidence (triage commands, dispatch approvals, cost review instructions, merge approval phrasing, crash recovery notifications).
- [ ] T-B3.2.5 Write §BOTH-Locations Design Note: "This file contains Lab-shareable curated patterns. The M6 E2E run corpus samples (raw data with per-sample scoring) are in `aria-orchestrator/evals/m6-prompt-quality/corpus/sample-{01..10}.md` (Spec #2 TG-C). These two locations serve different purposes and do not duplicate content." <!-- R1-X-T1 fix: aria-orch/ → aria-orchestrator/ -->
- [ ] T-B3.2.6 Add cross-reference: "See also: `aria-orchestrator/evals/m6-prompt-quality/` for M6 E2E corpus samples and scores (Spec #2 TG-C deliverable)." <!-- R1-X-T1 fix: aria-orch/ → aria-orchestrator/ -->
- [ ] T-B3.2.7 Verify ≥200 lines (rough proxy for ≥10 patterns at ~15-20 lines each + rubric section).

**AC verification** (included in AC-6):
```bash
# R1-X-T1 fix: aria-orch/ → aria-orchestrator/ in cross-ref check
# R1-X-T5 fix: wc -l proxy replaced with grep -c "^### Pattern" structural check
[ -f standards/autonomous/humanized-command-patterns.md ] \
  && grep -q "Lab-shareable" standards/autonomous/humanized-command-patterns.md \
  && grep -q "aria-orchestrator/evals/m6-prompt-quality" standards/autonomous/humanized-command-patterns.md \
  && [ $(grep -c "^### Pattern" standards/autonomous/humanized-command-patterns.md) -ge 10 ] \
  && exit 0
```

#### T-B3.3: Complete T-B0 submodule operation sequence

- [ ] T-B3.3.1 Return to T-B0.5 and complete the commit + push + merge + pointer bump sequence.

---

### T-B4: aria-orchestrator/docs/layer-boundary-contract.md (new file) (~3h)

**Description**: Create `/home/dev/Aria/aria-orchestrator/docs/layer-boundary-contract.md`. This file is Aria-specific and must NOT be placed in standards/ (per km M-km-R2-005 decision documented in AD-M6-9, Q2 owner lock 2026-05-24). <!-- R1-X-T4 fix: AD-M5-11 → AD-M6-9 -->

**Subtasks**:
- [ ] T-B4.1 Create file with Aria-specific header: `<!-- Aria-specific: this file is NOT Lab-shareable. It belongs in aria-orchestrator/docs/, not in standards/. Per km M-km-R2-005 decision recorded in AD-M6-9 (namespace creation decision, Q2 owner lock 2026-05-24). -->`. <!-- R1-X-T4 fix: AD-M5-11 → AD-M6-9 in header reference -->
- [ ] T-B4.2 Write §cost.json Schema (locked at Spec #1 c29a800):
  - Full schema reproduction (metered_usd + subscription_usd + freshness_ts fields with types and semantics).
  - Note: "Schema locked at Spec #1 commit c29a800. Changes require a new OpenSpec with a new AD-M6-* or later decision slot."
  - Include the `null` semantics for `subscription_usd.cost_usd` (Luxeno=0 false-positive prevention).
- [ ] T-B4.3 Write §Humanized Command Format section: how Layer 1 issues YAML commands to Layer 2. Cross-reference `standards/autonomous/humanized-command-patterns.md` for curated examples.
- [ ] T-B4.4 Write §State Machine Ownership Boundary table:

  | State | Owner | Notes |
  |-------|-------|-------|
  | S0_NEW | Layer 1 initiates | Issue arrives from Forgejo |
  | S1_TRIAGED | Layer 1 | PM role: triage decision |
  | S2_PLANNING | Layer 2 | Engineering: Phase A |
  | S3_IN_PROGRESS | Layer 2 | Engineering: Phase B |
  | S4_DISPATCHED | Layer 1 + Layer 2 | Handoff point |
  | S5_REVIEWING | Layer 2 | Phase C pre-merge |
  | S6_RECONCILING | Layer 2 | MechanicalReconciler (M5 shipped) |
  | S7_AWAITING_MERGE | Human gate (owner via Feishu) | AD10: single human participation point |
  | S8_MERGED | Layer 1 confirms | Feishu sign-off triggers |
  | S9_CLOSED | Layer 1 | D-phase closure |
  | S_FAIL | Layer 1 escalation | Crash recovery + Feishu alert |

- [ ] T-B4.5 Write §Error Escalation Protocol: Layer 2 failure modes (S_FAIL) → Layer 1 Feishu notification → owner optional intervention. Cross-reference aria-orchestrator/docs/architecture-decisions.md §AD-M5-* for crash recovery decisions.
- [ ] T-B4.6 Verify `c29a800` commit reference is present and accurate.

**AC verification**:
```bash
[ -f aria-orchestrator/docs/layer-boundary-contract.md ] \
  && grep -q "cost.json" aria-orchestrator/docs/layer-boundary-contract.md \
  && grep -q "c29a800" aria-orchestrator/docs/layer-boundary-contract.md \
  && grep -q "Aria-specific" aria-orchestrator/docs/layer-boundary-contract.md \
  && exit 0
```

---

### T-B5: aria-orchestrator/README.md v2.0 (~0.5h)

**Description**: Update or create `/home/dev/Aria/aria-orchestrator/README.md`.

**Subtasks**:
- [ ] T-B5.1 Check if `aria-orchestrator/README.md` exists: `[ -f aria-orchestrator/README.md ]`.
- [ ] T-B5.2 If exists: update to reflect M1-M5 shipped capabilities + M6 in progress. Add cross-links to `docs/layer-boundary-contract.md` and `docs/architecture-decisions.md`.
- [ ] T-B5.3 If not exists: create minimal README with: title "Aria Orchestrator (Aria 2.0 Runtime)", description (Layer 1/2 architecture overview), current milestone (M6 in progress), cross-links to architecture-decisions.md and layer-boundary-contract.md.
- [ ] T-B5.4 Verify `grep -q "Layer 1" aria-orchestrator/README.md`.

**AC verification**:
```bash
[ -f aria-orchestrator/README.md ] && grep -q "Layer 1" aria-orchestrator/README.md && exit 0
```

---

### T-B6: architecture-decisions.md AD-M6-9 claim + AD-M6-7/8 stubs (~0.5h)

<!-- R1-X-T4 fix: renamed T-B6 from "AD-M5-11 claim" to "AD-M6-9 claim". AD-M5-11 collision with M5-spillover scope discovered in R1 audit (live architecture-decisions.md:3460-3478 reserves AD-M5-11 for M5-spillover topics). Spec #3 vacates AD-M5-11 claim per Q2 owner lock 2026-05-24; AD-M6-9 reserved instead. -->

**Description**: Update `/home/dev/Aria/aria-orchestrator/docs/architecture-decisions.md`.

Per `[[feedback_ad_slot_backfill_checkpoint]]`: AD-M6-8 must be filled or explicitly retired before this Spec archives. Document the retirement decision here if no Phase B topic emerges.

**Subtasks**:
- [ ] T-B6.1 Add a new **AD-M6-9** entry (append after the last existing AD-M6-* entry or in the M6 section). Do NOT overwrite AD-M5-11 (it is reserved for M5-spillover topics at lines ~3460-3480 — leave untouched). AD-M6-9 content:
  - **状态**: Decided (2026-05-24, this Spec aria-2.0-m6-docs T-B6)
  - **决策**: Create `standards/autonomous/` as a new subdirectory for Lab-shareable autonomous AI operation patterns (decision-autonomy-matrix.md + humanized-command-patterns.md). Aria-specific implementation contracts (layer-boundary-contract.md) go in `aria-orchestrator/docs/` not in `standards/`. Content boundary: standards/ = curated portable patterns; aria-orchestrator/docs/ = Aria-internal contracts pinned to specific code commits (e.g., cost.json locked at c29a800).
  - **Rationale**: Lab-shareable patterns in standards/ can be imported by other 10CG Lab projects (Kairos, SilkNode) without pulling in Aria-internal dependencies. Aria-specific contracts in aria-orchestrator/docs/ clearly scope their applicability to this repo only.
  - Include alternatives considered (put everything in aria-orchestrator/docs vs put everything in standards/) and why boundary split was chosen.
  - Note: AD-M5-11 vacated by this Spec per Q2 owner lock 2026-05-24 (R1 audit: AD-M5-11 reserved for M5-spillover in architecture-decisions.md:3460).
- [ ] T-B6.2 Add AD-M6-7 entry documenting the state-checks probe design decision:
  - **状态**: Decided (2026-05-24, T-A6)
  - **决策**: 3 probes in .aria/state-checks.yaml: version-badge-match / claude-md-version / arch-doc-stale. Severity = warning (non-blocking). POSIX tools only (grep, python3). `enabled: true` even pre-v2.0 so state-scanner surfaces status proactively. Probe 3 date arithmetic uses python3 datetime (not GNU `date -d`) for cross-platform compatibility.
- [ ] T-B6.3 Add AD-M6-8 stub:
  - **状态**: RESERVED or Retired (fill during Phase B if a new decision topic emerges; retire with explicit justification if none found by Phase C).
  - Note: if Phase B produces no new architectural decision topic for this slot, update this entry to "Retired — no Phase B topic materialized; AD-M6-7 covered probe design; AD-M6-9 covered namespace creation; no further doc-Spec decisions identified."

**AC verification**:
```bash
# R1-X-T4: verify AD-M6-9 present (not AD-M5-11 overwrite)
grep -q "AD-M6-9" aria-orchestrator/docs/architecture-decisions.md \
  && grep -q "standards/autonomous" aria-orchestrator/docs/architecture-decisions.md \
  && grep -q "AD-M6-7" aria-orchestrator/docs/architecture-decisions.md \
  && grep -q "AD-M6-8" aria-orchestrator/docs/architecture-decisions.md \
  && exit 0
# Verify AD-M5-11 still present and NOT overwritten (must still show RESERVED/M5-spillover):
grep -q "AD-M5-11" aria-orchestrator/docs/architecture-decisions.md \
  && grep -q "Reserved slot\|RESERVED" aria-orchestrator/docs/architecture-decisions.md \
  && exit 0
```

---

## Full AC verification sweep (run before Phase C.1)

Run all ACs in order. All must exit 0 (except TG-DOCS-B ACs if v2.0.1 deferred by owner decision).

```bash
# AC-1: CLAUDE.md v2.0 content
grep -c "Rule #" CLAUDE.md  # ≥ 9
grep -q "**版本**: 2.0.0" CLAUDE.md && echo "AC-1a PASS" || echo "AC-1a FAIL"
grep -q "两层 AI 分工" CLAUDE.md && echo "AC-1b PASS" || echo "AC-1b FAIL"
grep -q "Aria 2.0 运行时" CLAUDE.md && echo "AC-1c PASS" || echo "AC-1c FAIL"
grep -q "aria-orchestrator" CLAUDE.md && echo "AC-1d PASS" || echo "AC-1d FAIL"

# AC-2: Release notes
[ -f docs/release-notes-v2.0.0.md ] \
  && grep -q "Plugin Compatibility" docs/release-notes-v2.0.0.md \
  && grep -q "Forgejo Discussion FAQ" docs/release-notes-v2.0.0.md \
  && echo "AC-2 PASS" || echo "AC-2 FAIL"

# AC-3: README badge
grep -q "v1.27.0" README.md && grep -q "Aria 2.0" README.md && echo "AC-3 PASS" || echo "AC-3 FAIL"

# AC-4: state-checks.yaml probes
python3 -c "
import yaml, sys
data = yaml.safe_load(open('.aria/state-checks.yaml'))
names = [c['name'] for c in data.get('checks', [])]
required = {'m6-version-badge-match', 'm6-claude-md-version', 'm6-arch-doc-stale'}
missing = required - set(names)
print('AC-4 PASS' if not missing else f'AC-4 FAIL missing={missing}')
sys.exit(1 if missing else 0)
"

# AC-5 (TG-DOCS-B): version-scheme.md
[ -f docs/architecture/version-scheme.md ] \
  && grep -q "aria-plugin" docs/architecture/version-scheme.md \
  && grep -q "Aria 2.0 PRD" docs/architecture/version-scheme.md \
  && echo "AC-5 PASS" || echo "AC-5 FAIL (TG-DOCS-B)"

# AC-6 (TG-DOCS-B): standards/autonomous/ files
# R1-X-T1: aria-orch/ → aria-orchestrator/; R1-X-T5: wc-l proxy → grep -c "^### Pattern"
[ -f standards/autonomous/humanized-command-patterns.md ] \
  && grep -q "Lab-shareable" standards/autonomous/humanized-command-patterns.md \
  && grep -q "aria-orchestrator/evals/m6-prompt-quality" standards/autonomous/humanized-command-patterns.md \
  && [ $(grep -c "^### Pattern" standards/autonomous/humanized-command-patterns.md) -ge 10 ] \
  && echo "AC-6 PASS" || echo "AC-6 FAIL (TG-DOCS-B)"

# AC-7 (TG-DOCS-B): layer-boundary-contract.md
[ -f aria-orchestrator/docs/layer-boundary-contract.md ] \
  && grep -q "c29a800" aria-orchestrator/docs/layer-boundary-contract.md \
  && grep -q "Aria-specific" aria-orchestrator/docs/layer-boundary-contract.md \
  && echo "AC-7 PASS" || echo "AC-7 FAIL (TG-DOCS-B)"

# AC-8 (TG-DOCS-B): system-architecture.md v2.0
grep -q "Version.*2.0.0" docs/architecture/system-architecture.md \
  && grep -q "Layer 1" docs/architecture/system-architecture.md \
  && echo "AC-8 PASS" || echo "AC-8 FAIL (TG-DOCS-B)"

# AC-10 (TG-DOCS-B): AD-M6-9 and AD-M6-7/8 (R1-X-T4: AD-M5-11 → AD-M6-9)
grep -q "AD-M6-9" aria-orchestrator/docs/architecture-decisions.md \
  && grep -q "standards/autonomous" aria-orchestrator/docs/architecture-decisions.md \
  && grep -q "AD-M6-7" aria-orchestrator/docs/architecture-decisions.md \
  && echo "AC-10 PASS" || echo "AC-10 FAIL (TG-DOCS-B)"
```

---

## Pre-archive checklist (run before Phase D.2)

- [ ] AD-M6-8 is either filled with a real decision topic OR explicitly retired with justification. Not RESERVED.
- [ ] standards/ submodule is on `master` branch: `git -C standards branch --show-current` → `master`.
- [ ] Main Aria repo `git status` shows `standards` pointer updated (included in Phase C.1 commit).
- [ ] CLAUDE.md AD11 compliance verified: Rules #1-#6 bodies are unchanged from pre-edit.
- [ ] AC-9 (state-checks arch-doc-stale probe): if TG-DOCS-B shipped, run probe manually and confirm exit 0.
- [ ] If TG-DOCS-B deferred to v2.0.1 per owner decision: document the deferral decision in `docs/release-notes-v2.0.0.md §Known Limitations` (T-A3.5 already includes this placeholder).
