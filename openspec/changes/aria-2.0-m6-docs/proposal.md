# Aria 2.0 M6 Spec #3 — Documentation Suite (CLAUDE.md v2.0 + Architecture + standards/autonomous)

> **Level**: 3 (Full — cross-cuts CLAUDE.md / standards/autonomous / docs/architecture / aria-orch/docs / Aria README)
> **Status**: Draft
> **Change ID**: `aria-2.0-m6-docs`
> **Parent US**: [US-026](../../../docs/requirements/user-stories/US-026.md)
> **Parent PRD**: [prd-aria-v2.md §M6](../../../docs/requirements/prd-aria-v2.md) (post `a786444` PRD patch, §M6 4-5w timeline)
> **Predecessor Spec**: [aria-2.0-m5-replay-reconciler-drift-review-loop-audit](../../archive/2026-05-23-aria-2.0-m5-replay-reconciler-drift-review-loop-audit/proposal.md) (M5 archived 2026-05-23)
> **Brainstorm Source**: [.aria/decisions/2026-05-24-us026-m6b-brainstorm.md](../../../.aria/decisions/2026-05-24-us026-m6b-brainstorm.md) (DEC-20260524-001 §2 Spec #3 + §4 P-10..P-13, CONVERGED 2026-05-24)
> **Effort baseline**: ~33h impl (TG-DOCS-A ~11h release-blocker + TG-DOCS-B ~22h architecture). Single SoT per `[[feedback_spec_v2_body_propagation_2pass]]`.
> **v2.0.1-deferrable**: TG-DOCS-B (~22h architecture) may ship as v2.0.1 if 5w calendar slips per Q-final-1 Menu C. TG-DOCS-A (~11h) is v2.0.0 release-blocker (ships with v2.0.0 unconditionally).
> **AD allocation reservation**: **AD-M6-7** and **AD-M6-8** are reserved for this Spec #3 only. Spec #1 (`aria-2.0-m6-cost-acceptance`) holds AD-M6-1/2/3; Spec #2 (`aria-2.0-m6-e2e-resilience`) holds AD-M6-4/5/6. **AD-M5-11** (pre-existing M5 RESERVED slot in `aria-orchestrator/docs/architecture-decisions.md`) is claimed by this Spec for M6 docs architectural decisions. (per DEC-20260524-001 §2 AD-M6-* allocation lock 2026-05-24)
> **Sibling Spec (Approved)**: [aria-2.0-m6-cost-acceptance](../aria-2.0-m6-cost-acceptance/proposal.md) (Spec #1, commit `c29a800`, AD-M6-1/2/3)
> **Sibling Spec (parallel draft)**: [aria-2.0-m6-e2e-resilience](../aria-2.0-m6-e2e-resilience/proposal.md) (Spec #2, AD-M6-4/5/6)
> **Successor**: [aria-2.0-m6-release-closeout](../aria-2.0-m6-release-closeout/proposal.md) (Spec #4, gates on this Spec's CLAUDE.md v2.0 + state-checks probes)

---

## Why

M5 shipped a production-grade autonomous dispatch loop that passed the "can-run + can-be-trusted + can-self-manage" bar. Before Aria 2.0 releases under a "verified autonomous" label, two documentation problems block release:

**Problem 1 — CLAUDE.md is stale for Aria 2.0.** The current CLAUDE.md (v1.0.4, last updated 2026-04-12) still describes Aria as a "方法论研究项目" in interactive-only terms. It has no reference to the two-layer AI execution architecture (Layer 1 / Layer 2), the v2.0 runtime scope, or the autonomous mode boundary rules. A CLAUDE.md v2.0 was drafted at `aria-orchestrator/docs/claude-md-revision-draft.md` (M0 T5.3 deliverable) with 8 structured diffs; those diffs were deliberately deferred to US-026. Additionally, Rules #7/8/9 (added post-draft) plus plugin version catch-up (v1.22.0 → v1.27.0) constitute a Diff 9 increment not in the original draft. Without this update, every future AI session reading CLAUDE.md misunderstands the v2.0 boundary.

**Problem 2 — Architecture documentation has not caught up with M1-M5 delivery.** The `docs/architecture/system-architecture.md` still references v1.9.0 (last updated 2026-04-12, predating the entire M1-M5 build). There is no `docs/architecture/version-scheme.md` disambiguating the four independent versioning streams (Aria main repo / aria-plugin / aria-orchestrator / Aria 2.0 PRD). The `standards/` submodule has no `autonomous/` directory, leaving the Lab-shareable autonomous operation patterns (decision-autonomy-matrix, humanized-command-patterns) undocumented. The `aria-orchestrator` directory has no `docs/layer-boundary-contract.md` to pin the inter-layer cost.json schema contract (Spec #1 `c29a800`).

**Problem 3 — No automated drift detection.** Without state-checks.yaml probes for version badge drift and stale architecture docs, the documentation inconsistencies observed in M1-M5 will recur silently. Three targeted probes (`[[feedback_pre_draft_bug_hunt_discipline]]`) provide continuous detection.

**Gate role in M6 sequencing**: Spec #4 (`aria-2.0-m6-release-closeout`) requires this Spec's CLAUDE.md v2.0 + state-checks probes as pre-release checklist prerequisites. Per DEC Q-final-1 Menu C, TG-DOCS-B can slip to v2.0.1 if the 5-week calendar is tight, but TG-DOCS-A must ship with v2.0.0.

**Comms clarification for release**: the "Plugin Compatibility" boundary (aria-plugin does NOT bump to v2.0 alongside Aria 2.0) is a source of confusion identified in brainstorm R1 cr-CH-8. Release notes and a Forgejo Discussion FAQ must address this explicitly.

---

## What

### In scope (~33h impl)

#### TG-DOCS-A: Release-blocker deliverables (~11h)

<!-- P-13: CLAUDE.md 8 diffs listed here verbatim, 2-pass per feedback_spec_v2_body_propagation_2pass -->

##### A.1 — CLAUDE.md v1.0.4 → v2.0 (8+1 diffs) (~4h)

Source draft: `aria-orchestrator/docs/claude-md-revision-draft.md` (M0 T5.3 deliverable).
The 9 diffs to apply (Diff 1-8 from draft + Diff 9 incremental):

**Diff 1 — 文档顶部"项目本质"段落扩展** (draft §Diff 1):
Replace the three-line header block. Change "AI 辅助的领域驱动设计方法论研究" → "AI-DDD 方法论的定义与端到端参考实现 (v1.x 方法论 + v2.0 自主运行时)". Change 核心假设 and version line per draft.

**Diff 2 — "项目定位"章节补充 v2.0 演进说明** (draft §Diff 2):
Add "身份演进 (v1.x → v2.0)" subsection before §研究目标. Content: v1.x = 方法论研究 (人类交互式), v2.0 = 方法论定义 + 端到端参考实现 (AI 自主式). Cross-link to architecture-decisions.md.

**Diff 3 — "核心概念"新增"两层 AI 分工"小节** (draft §Diff 3):
After §十步循环, add §两层 AI 分工 (v2.0 新增). Layer 1 (Hermes + GLM) = PM role. Layer 2 (aria-runner + CC + aria-plugin) = engineering role. Cross-link AD1 + AD6.

**Diff 4 — "信息地图"子模块表格新增 aria-orchestrator 行** (draft §Diff 4):
Add table row: `aria-orchestrator/` | v2.0 运行时 (Layer 1/2) | Hermes fork / Docker 镜像 / Nomad job / ADR. Add two §目录导航 entries: Aria 2.0 架构决策 → aria-orchestrator/docs/architecture-decisions.md; Layer 边界契约 → aria-orchestrator/docs/layer-boundary-contract.md.

**Diff 5 — "技术约束"补充 v2.0 边界** (draft §Diff 5):
Add "✅ 实现 (v2.0): 端到端参考实现 (aria-orchestrator, 仅限 10CG Lab 内部)" line. Add clarifying paragraph: v2.0 runtime ≠ general framework.

**Diff 6 — "不可协商规则"章节不修改** (draft §Diff 6 — hard constraint per AD11):
Rules #1-#6 text body is FROZEN. No deletions, no modifications. AD11 compliance.

**Diff 7 — 新增"Aria 2.0 运行时"独立章节** (draft §Diff 7, ≤50 lines):
New H2 section after §不可协商规则. Includes: 分层叙述 (standards / aria-plugin / aria-orchestrator), 与 6 条规则的关系 (how Layer 2 enforces each), 人类参与点 (AD10: S7_AWAITING_MERGE), 详细入口 (architecture-decisions.md / spikes / M0 Spec / PRD v2.0).

**Diff 8 — "项目状态"版本号更新** (draft §Diff 8, using M6-time actual values):
Update stage: "研究中 → v2.0 规划已批准" → "v2.0 M6 执行中 (M1-M5 shipped)". Update 插件版本 from v1.22.0 to actual v1.27.0 (current per `c7e611f` submodule bump). Update 主项目版本 v1.7.0. Add 运行时版本 line. Update "更新" date at bottom.

**Diff 9 — Rules #7/#8/#9 + §2.3 frontmatter schema catch-up** (incremental beyond original draft, ~0.5h):
Rules #7/8/9 and the Rule #9 §2.3 frontmatter schema extension were added to CLAUDE.md AFTER the M0 draft was written (post-M1 through post-M5). The draft does not cover them. Diff 9 is therefore a no-op edit on Rule #7/8/9 body text (they are already in the live CLAUDE.md as of 2026-04-12 updates) — but requires:
- Plugin version synchronization: CLAUDE.md §项目状态 must reference v1.27.0 (not v1.22.0) per commit `c7e611f`.
- Rule #8 §exception clause must reference the actual `.aria/config.json` field name `phase_c_integrator.pre_merge_gate.no_aether_fallback` (already present; verify no drift from config.template.json).
- Rule #9 §2.3 frontmatter extension must cite `aria-plugin v1.22.x+` (already present; verify not stale).
- Version field: bump `**版本**: 1.0.4` → `**版本**: 2.0.0`.

Constraint (AD11): Diff 9 MUST NOT alter Rule #1-#6 text. It only updates §项目状态 version numbers and bumps the top-level version field.

##### A.2 — 主 Aria README updates (~1.5h)

**Target file**: `/home/dev/Aria/README.md`

Changes:
1. Plugin version badge: update `v1.15.2` → `v1.27.0` (current per commit `c7e611f` submodule bump to `1b8ec3f`).
2. Add Aria 2.0 positioning paragraph after the "What is Aria?" section: "**Aria 2.0 (v2.0.0, in progress)** extends the methodology to autonomous execution. See [docs/architecture/system-architecture.md](docs/architecture/system-architecture.md) for the two-layer architecture."
3. Add cross-link to PRD v2.0 under the "Why Aria?" section or in a new "Roadmap" subsection.

Binary-falsifiable post-check: `grep -q "v1.27.0" README.md && grep -q "Aria 2.0" README.md && exit 0`.

##### A.3 — Release notes v2.0.0 (~2h)

**Target file**: `/home/dev/Aria/docs/release-notes-v2.0.0.md` (new file)

Mandatory section: **"Plugin Compatibility — aria-plugin 不随 Aria 2.0 同 bump"** (closes brainstorm R1 cr-CH-8):

```markdown
## Plugin Compatibility

aria-plugin (the Claude Code plugin that provides Aria's Skills and Agents) follows its own
independent versioning stream (currently v1.27.0). It is NOT bumped to v2.0 when Aria
main repo releases v2.0.0.

Semantic boundary:
- **Aria main repo (v2.0.0)**: the methodology definition + autonomous runtime (aria-orchestrator)
- **aria-plugin (v1.27.x)**: the interactive Skills + Agents used in Claude Code sessions

Projects using aria-plugin for interactive AI-DDD collaboration do not need to do anything
when Aria 2.0 releases. The plugin version you have installed continues to work unchanged.
```

Additional sections: v2.0.0 highlights (M1-M5 delivery summary), migration notes ("non-migration" — no breaking changes for methodology users; the autonomous runtime is an additive internal layer), known limitations (TG-DOCS-B architecture may be in v2.0.1 if calendar slips per Q-final-1 Menu C).

Binary-falsifiable post-check: `grep -q "Plugin Compatibility" docs/release-notes-v2.0.0.md && grep -q "aria-plugin 不随" docs/release-notes-v2.0.0.md && exit 0`.

##### A.4 — aria/README.md cross-link (~0.5h)

**Target file**: `/home/dev/Aria/aria/README.md`

Add a cross-link section pointing to Aria 2.0 context: "This plugin (aria-plugin v1.x) is the interactive layer of Aria. For the Aria 2.0 autonomous runtime, see the [main Aria repository](https://github.com/10CG/Aria)."

Binary-falsifiable post-check: `grep -q "Aria 2.0" aria/README.md && exit 0`.

##### A.5 — Forgejo Discussion FAQ post (draft text in release notes) (~1.5h)

**Target**: Draft the FAQ text in `docs/release-notes-v2.0.0.md` under a "Forgejo Discussion FAQ" section. Actual posting to Forgejo Discussion is an owner action (outside AI-implementable scope). The FAQ text answers:
- Q: Does aria-plugin need to be updated when Aria 2.0 releases? A: No.
- Q: What changed in Aria 2.0 vs 1.x? A: Added autonomous runtime (aria-orchestrator). Methodology and plugin unchanged.
- Q: Who is Aria 2.0 for? A: 10CG Lab internal projects only. The plugin remains universally available.

Evidence: `grep -q "Forgejo Discussion FAQ" docs/release-notes-v2.0.0.md`.

Note: Spec #4 (`aria-2.0-m6-release-closeout`) will verify the actual Forgejo Discussion URL. This Spec verifies the FAQ text exists in the release notes file (Spec #4 verifies URL liveness).

##### A.6 — .aria/state-checks.yaml 3 drift probes (TG-DOCS-A portion) (~1.5h)

<!-- P-12: Probe scripts detailed per feedback_pre_draft_bug_hunt_discipline -->

Three new entries in `.aria/state-checks.yaml`. Each probe is a 1-line (or minimal multi-line) shell command that exits non-zero on drift. Bug-hunt requirement: each command must be tested against both the PASS case (no drift) and the FAIL case (simulate drift) before commit.

**Probe 1 — version-badge-match**: README.md plugin badge version matches aria/.claude-plugin/plugin.json version field.

```yaml
- name: "m6-version-badge-match"
  description: |
    Verify README.md Plugin badge version matches aria/.claude-plugin/plugin.json.
    Drift = README badge stale after a plugin version bump.
  command: |
    BADGE=$(grep -oP '(?<=Plugin-v)[0-9]+\.[0-9]+\.[0-9]+' README.md | head -1)
    PLUGIN=$(python3 -c "import json; print(json.load(open('aria/.claude-plugin/plugin.json'))['version'])")
    [ "$BADGE" = "$PLUGIN" ] && echo "OK badge=$BADGE" || { echo "DRIFT badge=$BADGE plugin=$PLUGIN"; exit 1; }
  severity: warning
  fix: "Update README.md Plugin badge to match aria/.claude-plugin/plugin.json version"
  timeout_seconds: 5
  enabled: true
```

**Probe 2 — claude-md-version-match**: CLAUDE.md top-level `**版本**:` field matches the v2.0 milestone. Specifically, after TG-DOCS-A ships, CLAUDE.md version must be `2.0.0`.

```yaml
- name: "m6-claude-md-version"
  description: |
    Verify CLAUDE.md top-level version field is 2.0.0 after Aria 2.0 release.
    Drift = CLAUDE.md not yet updated after v2.0.0 ships, or accidentally reverted.
  command: |
    VER=$(grep -oP '(?<=\*\*版本\*\*: )[0-9]+\.[0-9]+\.[0-9]+' CLAUDE.md | head -1)
    [ "$VER" = "2.0.0" ] && echo "OK version=$VER" || { echo "DRIFT claude-md-version=$VER (expected 2.0.0)"; exit 1; }
  severity: warning
  fix: "Apply CLAUDE.md Diff 9 version bump: **版本**: 1.0.4 → **版本**: 2.0.0"
  timeout_seconds: 5
  enabled: true
```

Note: this probe is intentionally set to `enabled: true` but will exit 1 until TG-DOCS-A ships (Diff 9 version bump). state-scanner treats `warning` severity as non-blocking. The probe becomes a real guard after CLAUDE.md v2.0 is committed.

**Probe 3 — arch-doc-stale-warning**: `docs/architecture/system-architecture.md` last-updated header is not older than 90 days from today.

```yaml
- name: "m6-arch-doc-stale"
  description: |
    Warn if docs/architecture/system-architecture.md **Last Updated** header is ≥90 days old.
    Architecture docs that age without review silently diverge from reality (post-M5 experience).
  command: |
    LAST=$(grep -oP '(?<=\*\*Last Updated\*\*: )\d{4}-\d{2}-\d{2}' docs/architecture/system-architecture.md | head -1)
    [ -z "$LAST" ] && { echo "MISSING Last Updated header"; exit 1; }
    EPOCH_DOC=$(date -d "$LAST" +%s 2>/dev/null)
    [ -z "$EPOCH_DOC" ] && { echo "UNPARSEABLE Last Updated: $LAST"; exit 1; }
    EPOCH_NOW=$(date +%s)
    AGE_DAYS=$(( (EPOCH_NOW - EPOCH_DOC) / 86400 ))
    [ $AGE_DAYS -lt 90 ] && echo "OK age=${AGE_DAYS}d" || { echo "STALE age=${AGE_DAYS}d (threshold=90d)"; exit 1; }
  severity: warning
  fix: "Update docs/architecture/system-architecture.md **Last Updated** header and review content"
  timeout_seconds: 5
  enabled: true
```

#### TG-DOCS-B: Architecture deliverables (~22h, v2.0.1-deferrable per Q-final-1 Menu C)

##### B.1 — docs/architecture/system-architecture.md v2.0 (~10h)

**Target file**: `/home/dev/Aria/docs/architecture/system-architecture.md`

Update from v1.9.0 (last updated 2026-04-12) to v2.0. The v2.0 content must include:

1. **Executive Summary update**: add two-layer AI execution model to "核心架构模式". Change "方法论研究项目" framing to "方法论定义 + 参考实现".
2. **New §Three-Layer Architecture**: standards (methodology) / aria-plugin (tools) / aria-orchestrator (runtime). ASCII diagram showing Layer 1 (Hermes + GLM) and Layer 2 (aria-runner + CC + aria-plugin).
3. **Autonomy model section**: 状态机 S0-S9 + S_FAIL overview. Human gate: S7_AWAITING_MERGE only (AD10). Dispatch flow diagram.
4. **Layer 1 / Layer 2 boundary**: cross-reference `aria-orchestrator/docs/layer-boundary-contract.md` (B.4). Note cost.json schema (Spec #1 `c29a800` locked schema).
5. **Update "Last Updated"** header to 2026-05-24 (or implementation date).
6. **Update Parent PRD** reference to include `prd-aria-v2.md`.
7. Version bump: `**Version**: 1.9.0` → `**Version**: 2.0.0`.

Post-check: `grep -q "Version.*2.0.0" docs/architecture/system-architecture.md && grep -q "Layer 1" docs/architecture/system-architecture.md && grep -q "Layer 2" docs/architecture/system-architecture.md && exit 0`.

##### B.2 — docs/architecture/version-scheme.md (new file) (~3h)

**Target file**: `/home/dev/Aria/docs/architecture/version-scheme.md`

New document disambiguating the four independent versioning streams:

| Stream | Repo / File | Current | SoT | Bump Trigger |
|--------|-------------|---------|-----|-------------|
| Aria main repo | `/home/dev/Aria/` (VERSION, README badge) | v1.7.0 | `VERSION` file | Milestones M0-M6; MAJOR on autonomous runtime launch |
| aria-plugin | `aria/.claude-plugin/plugin.json` | v1.27.0 | `plugin.json` | MINOR on new Skill/Agent; PATCH on bug fix |
| aria-orchestrator | `aria-orchestrator/` (pyproject.toml or VERSION) | v2.x | pyproject.toml | MINOR on new Layer 1/2 capability |
| Aria 2.0 PRD | `docs/requirements/prd-aria-v2.md` frontmatter | v2.0 | PRD frontmatter | Document revisions |

Key disambiguation: aria-plugin does NOT bump to v2.0 when Aria main repo releases v2.0.0. The version numbers are semantically independent. This is the "non-migration" described in release notes.

Minimum content requirement: ≥80 lines covering all four streams, cross-references, and the "Plugin Compatibility" rationale.

Post-check: `[ -f docs/architecture/version-scheme.md ] && grep -q "aria-plugin" docs/architecture/version-scheme.md && grep -q "aria-orchestrator" docs/architecture/version-scheme.md && grep -q "Aria 2.0 PRD" docs/architecture/version-scheme.md && exit 0`.

##### B.3 — standards/autonomous/ directory (Lab-shareable files) (~5h)

<!-- P-10: standards submodule operation sequence — detailed runbook in tasks.md T-B3-0 -->
<!-- P-11: content boundary between standards/autonomous/ and aria-orch/evals/ -->

**Target submodule**: `/home/dev/Aria/standards/` (own git repo per `[[project_meta_repo_pattern]]`)

**Operation sequence (P-10)**: Changes to `standards/` require:
1. Create feature branch in the standards submodule: `git -C standards checkout -b feat/autonomous-docs`.
2. Create files `standards/autonomous/decision-autonomy-matrix.md` and `standards/autonomous/humanized-command-patterns.md`.
3. Commit in the standards submodule with a conventional commit message.
4. If owner has merge authority: push directly to standards master and merge. Otherwise: open PR in the standards repo.
5. After the standards branch/commit is on master: in the main Aria repo, `git -C standards checkout master && git -C standards pull` to advance the submodule pointer.
6. In the main Aria repo: `git add standards` to stage the new pointer, then commit `chore(submodule): bump standards pointer to include autonomous/ docs`.

See tasks.md T-B3-0 for the full step-by-step runbook.

**B.3.1 — standards/autonomous/decision-autonomy-matrix.md** (Lab-shareable)

Content: autonomy decision matrix per PRD §553. Rows = decision types (triage / dispatch / merge approval / cost alarm / schema migration). Columns = autonomy level (fully-auto / auto-with-log / human-gate). Each cell: condition + rationale. Header: `<!-- Lab-shareable: this file is in standards/ and may be reused by other 10CG Lab projects. -->`.

Minimum content: ≥100 lines. Must include cross-reference to `aria-orchestrator/docs/layer-boundary-contract.md` (B.4) for implementation specifics.

**B.3.2 — standards/autonomous/humanized-command-patterns.md** (Lab-shareable, ≥10 curated samples)

<!-- P-11: BOTH-locations content boundary design -->
Content boundary clarification (P-11):
- THIS file (`standards/autonomous/humanized-command-patterns.md`): Lab-shareable CURATED patterns. Contains ≥10 distilled examples demonstrating good vs bad command phrasing, the PRD §639 rubric explanation, and scoring guidance. Does NOT contain raw corpus files.
- SPEC #2 TG-C (`aria-orch/evals/m6-prompt-quality/corpus/sample-{01..10}.md`): the actual M6 E2E run samples with per-sample scoring. Does NOT duplicate the pattern guide.
- Cross-reference: this file references Spec #2 TG-C corpus with `See also: aria-orch/evals/m6-prompt-quality/ for M6 E2E corpus samples`. Spec #2 TG-C references this file with `See also: standards/autonomous/humanized-command-patterns.md for Lab-wide pattern guide`.
- No content duplication between the two locations.

Content requirements: ≥10 curated samples (pattern name + bad example + good example + rationale). PRD §639 rubric (scoring dimensions). Header: `<!-- Lab-shareable: this file is in standards/ and may be reused by other 10CG Lab projects. -->`. Cross-reference to Spec #2 TG-C corpus.

Minimum content: ≥200 lines (rough proxy for ≥10 patterns at ~15-20 lines each + rubric section).

Post-check: `wc -l < standards/autonomous/humanized-command-patterns.md` ≥ 200.

##### B.4 — aria-orchestrator/docs/layer-boundary-contract.md (Aria-specific, NOT in standards/) (~3h)

<!-- km M-km-R2-005: this file is Aria-specific, must NOT go into standards/ -->

**Target file**: `/home/dev/Aria/aria-orchestrator/docs/layer-boundary-contract.md`

Content: the Layer 1 / Layer 2 interface contract. Specifically:
1. **cost.json schema** (locked at Spec #1 `c29a800`): full schema reproduction including `metered_usd`, `subscription_usd`, `freshness_ts` fields. Note: "schema locked at commit c29a800; changes require a new Spec with AD-M6-* decision slot."
2. **Command format**: how Layer 1 issues YAML humanized commands to Layer 2. Cross-reference `standards/autonomous/humanized-command-patterns.md` (B.3.2).
3. **State machine boundary**: which states are owned by Layer 1 vs Layer 2. S0-S4 triage/dispatch (Layer 1 initiated). S5-S9 execution (Layer 2 primary). S7 human gate (owner via Feishu).
4. **Error escalation protocol**: Layer 2 failure modes → Layer 1 response.
5. **Header**: `<!-- Aria-specific: this file is NOT Lab-shareable. It belongs in aria-orchestrator/docs/, not in standards/. Per km M-km-R2-005 decision. -->`.

Post-check: `[ -f aria-orchestrator/docs/layer-boundary-contract.md ] && grep -q "cost.json" aria-orchestrator/docs/layer-boundary-contract.md && grep -q "c29a800" aria-orchestrator/docs/layer-boundary-contract.md && exit 0`.

##### B.5 — aria-orchestrator/README v2.0 update (~1h)

**Target file**: `/home/dev/Aria/aria-orchestrator/README.md` (if exists) or create minimal one.

Update/create to reflect current state: Layer 1/2 architecture, M1-M5 shipped capabilities, M6 in progress. Cross-link to `docs/layer-boundary-contract.md` and `docs/architecture-decisions.md`.

Post-check: `[ -f aria-orchestrator/README.md ] && grep -q "Layer 1" aria-orchestrator/README.md && exit 0`.

##### B.6 — architecture-decisions.md AD-M5-11 slot claim (~0.5h + AD-M6-7/8 stubs)

**Target file**: `/home/dev/Aria/aria-orchestrator/docs/architecture-decisions.md`

1. Claim AD-M5-11 RESERVED slot with the M6 docs architectural decision: document the `standards/autonomous/` namespace creation decision (Lab-shareable vs Aria-specific content boundary — why `layer-boundary-contract.md` goes in `aria-orchestrator/docs/` rather than `standards/`, and why `humanized-command-patterns.md` goes in `standards/autonomous/` rather than `aria-orch/`).
2. Add stubs for AD-M6-7 (this Spec's state-checks probe design decision) and AD-M6-8 (reserve slot).

### Out of scope (explicit drops per DEC §3 + R3)

| ID | Description | Drop reason |
|----|-------------|-------------|
| OOS-1 | m6-core Spec (km m6-core) | Content = M5-OS-PB-1 in disguise, violates Q6 "defer all carry-forward". km R3 self-correction. |
| OOS-2 | INFRA sub-Spec (km m6-infra) | Track E `aria-layer2-docker-auth-cold-pull-fix` already shipped (2026-05-23); ghost work. |
| OOS-3 | Real-time dashboard (PRD §352) | PRD §352 explicit deferral: "M6 后考虑, MVP 不做". |
| OOS-4 | cost.json schema implementation | That is Spec #1 (`aria-2.0-m6-cost-acceptance`, `c29a800`). This Spec documents it only. |
| OOS-5 | M5-OS-PB-1 carry-forward | Owner Q6 decision: "defer all carry-forward". |
| OOS-6 | Spec #4 pre-release submodule branch verify probe | That probe lives in state-checks.yaml but is owned by Spec #4. This Spec owns 3 probes (A.6). |
| OOS-7 | DOCS as two separate Specs (A + B) | R3 single Spec + internal TG split (km R3 self-correction). |

---

## Constraints

### standards/ submodule is its own git repository (P-10)

Per `[[project_meta_repo_pattern]]`: `standards/` is NOT vendored. It is an independent git repository (`https://github.com/10CG/aria-standards`). Changes require: feature branch in the submodule → merge/push → submodule pointer bump in main Aria repo. The detailed runbook is in tasks.md T-B3-0.

### CLAUDE.md Rule #1-#6 text is FROZEN (AD11 hard constraint)

Diff 6 is explicitly a no-op. No diff to apply to Rules #1-#6 body text. AD11 "不修改现有 6 条不可协商规则, 只新增 Aria 2.0 运行时章节". Diff 7 and Diff 9 are additive or update-only.

### layer-boundary-contract.md must NOT enter standards/ (km M-km-R2-005)

`aria-orchestrator/docs/layer-boundary-contract.md` is Aria-specific (pinned to aria-orchestrator internal contracts). It goes in `aria-orchestrator/docs/`, not `standards/autonomous/`. Enforce via header comment in the file itself.

### TG-DOCS-B is v2.0.1-deferrable

Per Q-final-1 Menu C: if 5-week calendar slips, TG-DOCS-B (B.1-B.6, architecture docs) may ship as v2.0.1 while v2.0.0 ships with TG-DOCS-A only. This is an owner decision gate, not an AI decision. The Spec covers both TGs in full.

### Cost.json schema is locked at Spec #1 c29a800

TG-DOCS-B B.4 `layer-boundary-contract.md` documents the cost.json schema but does NOT modify it. The schema is owned by Spec #1 and is locked.

### Pre-commit preflight (per `[[feedback_clear_cache_before_code_change]]`)

Before committing CLAUDE.md v2.0, run: verify no Claude Code plugin cache interference by doing a cache-clear if the plugin reports unexpected behavior during Phase B.2 testing.

---

## How

### Technical approach

```
TG-DOCS-A (release-blocker):
  CLAUDE.md  ← apply 9 diffs from claude-md-revision-draft.md + Diff 9 increment
  README.md  ← badge bump + Aria 2.0 cross-link
  release-notes-v2.0.0.md  ← new file (Plugin Compatibility + FAQ text)
  aria/README.md  ← cross-link addition
  .aria/state-checks.yaml  ← 3 new probe entries appended

TG-DOCS-B (architecture, v2.0.1-deferrable):
  docs/architecture/system-architecture.md  ← v1.9.0 → v2.0 update
  docs/architecture/version-scheme.md  ← new file (4-stream disambiguation)
  standards/autonomous/  ← new directory + 2 files (via submodule feature branch)
    decision-autonomy-matrix.md
    humanized-command-patterns.md
  aria-orchestrator/docs/layer-boundary-contract.md  ← new file (Aria-specific)
  aria-orchestrator/README.md  ← v2.0 update
  aria-orchestrator/docs/architecture-decisions.md  ← AD-M5-11 claim + AD-M6-7/8 stubs
  submodule pointer bump:
    git add standards  ← after standards feature branch lands on master
```

### Key design decisions

| ID | Topic | Decision |
|----|-------|----------|
| AD-M5-11 | standards/autonomous/ namespace creation | `standards/autonomous/` is created as a new subdirectory for Lab-shareable autonomous AI operation patterns. Files here are published under the standards submodule and reusable by other 10CG Lab projects. Aria-specific implementation contracts (like `layer-boundary-contract.md`) go in `aria-orchestrator/docs/` instead. Rationale: Lab-shareable patterns benefit from being in the shared standards submodule; Aria-specific contracts would pollute standards/ with Aria internals and create dependency issues for other projects importing standards. |
| AD-M6-7 | state-checks.yaml probe design (3-probe set) | Three probes address version-badge-match, claude-md-version, and arch-doc-stale. Severity = `warning` (non-blocking) to allow gradual adoption. Commands use standard POSIX tools (grep, date, python3) with no external dependencies. `enabled: true` even during pre-v2.0 window so state-scanner surfaces status proactively. |
| AD-M6-8 | (Reserved — no topic assigned at Phase A) | RESERVED for Phase B decisions discovered during implementation. Per `[[feedback_ad_slot_backfill_checkpoint]]`: AD-M6-8 must be filled or explicitly retired before this Spec archives. |

---

## Acceptance criteria

All criteria are binary-falsifiable per `[[feedback_falsifiable_evidence_for_binary_acceptance]]`. No subjective language.

### AC-1 — CLAUDE.md v2.0 content verified (TG-DOCS-A)

**Evidence**:
```bash
grep -c "Rule #" CLAUDE.md  # must return ≥ 9 (Rules #1-#9 all present)
grep -q "**版本**: 2.0.0" CLAUDE.md  # Diff 9 version bump applied
grep -q "两层 AI 分工" CLAUDE.md  # Diff 3 applied
grep -q "Aria 2.0 运行时" CLAUDE.md  # Diff 7 chapter present
grep -q "aria-orchestrator" CLAUDE.md  # Diff 4 table row present
```
All five commands exit 0.

### AC-2 — Release notes file exists + Plugin Compatibility section present (TG-DOCS-A)

**Evidence**:
```bash
[ -f docs/release-notes-v2.0.0.md ] \
  && grep -q "Plugin Compatibility" docs/release-notes-v2.0.0.md \
  && grep -q "aria-plugin 不随" docs/release-notes-v2.0.0.md \
  && grep -q "Forgejo Discussion FAQ" docs/release-notes-v2.0.0.md \
  && exit 0
```

### AC-3 — README.md badge and Aria 2.0 cross-link updated (TG-DOCS-A)

**Evidence**:
```bash
grep -q "v1.27.0" README.md && grep -q "Aria 2.0" README.md && exit 0
```
Plugin version badge must show v1.27.0 (matches `aria/.claude-plugin/plugin.json`).

### AC-4 — .aria/state-checks.yaml contains 3 new M6 probes (TG-DOCS-A)

**Evidence**:
```bash
grep -c "m6-version-badge-match\|m6-claude-md-version\|m6-arch-doc-stale" .aria/state-checks.yaml
# must return 3 (exactly one match per probe name)
python3 -c "
import yaml, sys
data = yaml.safe_load(open('.aria/state-checks.yaml'))
names = [c['name'] for c in data.get('checks', [])]
required = {'m6-version-badge-match', 'm6-claude-md-version', 'm6-arch-doc-stale'}
missing = required - set(names)
sys.exit(1 if missing else 0)
"
# must exit 0 (all 3 probe names present in checks list)
```

### AC-5 — version-scheme.md exists and covers all 4 streams (TG-DOCS-B)

**Evidence**:
```bash
[ -f docs/architecture/version-scheme.md ] \
  && grep -q "aria-plugin" docs/architecture/version-scheme.md \
  && grep -q "aria-orchestrator" docs/architecture/version-scheme.md \
  && grep -q "Aria 2.0 PRD" docs/architecture/version-scheme.md \
  && exit 0
```

### AC-6 — standards/autonomous/ 2 files exist with Lab-shareable headers and required cross-refs (TG-DOCS-B)

**Evidence**:
```bash
[ -f standards/autonomous/decision-autonomy-matrix.md ] \
  && [ -f standards/autonomous/humanized-command-patterns.md ] \
  && grep -q "Lab-shareable" standards/autonomous/decision-autonomy-matrix.md \
  && grep -q "Lab-shareable" standards/autonomous/humanized-command-patterns.md \
  && grep -q "aria-orch/evals/m6-prompt-quality" standards/autonomous/humanized-command-patterns.md \
  && exit 0
# Minimum line count for humanized-command-patterns.md:
[ $(wc -l < standards/autonomous/humanized-command-patterns.md) -ge 200 ] && exit 0
```

### AC-7 — layer-boundary-contract.md exists with cost.json schema pin (TG-DOCS-B)

**Evidence**:
```bash
[ -f aria-orchestrator/docs/layer-boundary-contract.md ] \
  && grep -q "cost.json" aria-orchestrator/docs/layer-boundary-contract.md \
  && grep -q "c29a800" aria-orchestrator/docs/layer-boundary-contract.md \
  && grep -q "Aria-specific" aria-orchestrator/docs/layer-boundary-contract.md \
  && exit 0
```

### AC-8 — system-architecture.md updated to v2.0 (TG-DOCS-B)

**Evidence**:
```bash
grep -q "Version.*2.0.0" docs/architecture/system-architecture.md \
  && grep -q "Layer 1" docs/architecture/system-architecture.md \
  && grep -q "Layer 2" docs/architecture/system-architecture.md \
  && grep -q "Last Updated.*2026" docs/architecture/system-architecture.md \
  && exit 0
```

### AC-9 — state-checks.yaml arch-doc-stale probe exits 0 after system-architecture.md update (TG-DOCS-B, coupled)

**Evidence**: after B.1 ships, run probe 3 manually:
```bash
bash -c "$(python3 -c "
import yaml
data = yaml.safe_load(open('.aria/state-checks.yaml'))
probe = next(c for c in data['checks'] if c['name'] == 'm6-arch-doc-stale')
print(probe['command'])
")"
# must exit 0 and print "OK age=<N>d" where N < 90
```

### AC-10 — AD-M5-11 slot claimed and AD-M6-7/8 documented (TG-DOCS-B)

**Evidence**:
```bash
grep -q "AD-M5-11" aria-orchestrator/docs/architecture-decisions.md \
  && grep -q "standards/autonomous" aria-orchestrator/docs/architecture-decisions.md \
  && grep -q "AD-M6-7" aria-orchestrator/docs/architecture-decisions.md \
  && grep -q "AD-M6-8" aria-orchestrator/docs/architecture-decisions.md \
  && exit 0
```

---

## Risks

| ID | Risk | Severity | Mitigation |
|----|------|----------|------------|
| R-M6D-1 | CLAUDE.md Diff 6 accidentally modifies Rule #1-#6 text (AD11 violation) | High | After writing CLAUDE.md v2.0, run `git diff HEAD -- CLAUDE.md` and verify Rules #1-#6 lines are unchanged. AC-1 `grep -c "Rule #"` count ≥ 9 is a necessary but not sufficient check — also verify line-for-line identity on the 6 rule bodies. |
| R-M6D-2 | standards/ submodule pointer drift: feature branch merged in submodule but main Aria pointer not bumped | Medium | Per `[[feedback_submodule_regression_pitfall]]`: after standards branch lands on master, explicitly run `git -C standards pull && git add standards && git commit`. T-B3-0 runbook enforces this. |
| R-M6D-3 | humanized-command-patterns.md content duplicated in Spec #2 TG-C corpus (BOTH-locations boundary violation) | Medium | P-11 content boundary is explicit: standards/ file = curated patterns + rubric guide; aria-orch/evals/ file = raw corpus samples. Cross-references point to each other. Enforced via header comment in both files. |
| R-M6D-4 | state-checks.yaml Probe 1 (badge match) fails immediately after AC-3 (README badge update) if there is a version mismatch between badge and plugin.json | Low | Probe 1 is designed to expose real drift. If it fails after the update, it means the badge update itself is wrong. Bug-hunt requirement: test probe against PASS case (badge = plugin.json) and FAIL case (mismatch) before commit. |
| R-M6D-5 | layer-boundary-contract.md accidentally placed in standards/ violating km M-km-R2-005 | Medium | File header enforcement + tasks.md T-B4 explicit path. AC-7 evidence checks for `aria-orchestrator/docs/` path (file existence at that path). |
| R-M6D-6 | TG-DOCS-B v2.0.1 slip causes state-checks.yaml Probe 3 (arch-doc-stale) to fire continuously during v2.0.0 window | Low | Probe 3 severity=warning (non-blocking). If TG-DOCS-B slips, state-scanner reports the staleness as advisory only. AC-9 verification is deferred to TG-DOCS-B completion. |
| R-M6D-7 | AD-M6-8 slot not filled before Spec archives (`[[feedback_ad_slot_backfill_checkpoint]]`) | Low | tasks.md T-B6 explicitly includes "fill or retire AD-M6-8" as a Phase B checklist item. |
| R-M6D-8 | Spec #2 humanized-command-patterns.md samples not yet available during TG-DOCS-B implementation (parallel Spec) | Medium | B.3.2 is structured as a curated pattern guide, not a corpus dump. The ≥10 curated samples can be drafted from M5 E2E evidence and prior brainstorm examples, independent of Spec #2 TG-C corpus timeline. Cross-reference is added once Spec #2 TG-C corpus path is confirmed. |

---

## Effort baseline

```
TG-DOCS-A (release-blocker, must ship v2.0.0):
  A.1  CLAUDE.md 9 diffs (Diff 1-8 from draft + Diff 9 increment)    ~4h
  A.2  README.md badge + Aria 2.0 cross-link                         ~1.5h
  A.3  release-notes-v2.0.0.md (Plugin Compat + FAQ draft)           ~2h
  A.4  aria/README.md cross-link                                      ~0.5h
  A.5  Forgejo FAQ text (in release-notes, owner posts)              ~0.5h (included in A.3)
  A.6  .aria/state-checks.yaml 3 probes (write + bug-hunt)           ~1.5h
  ─────────────────────────────────────────────────────────────────────
  TG-DOCS-A subtotal                                                  ~11h

TG-DOCS-B (architecture, v2.0.1-deferrable):
  B.1  docs/architecture/system-architecture.md v2.0                 ~10h
  B.2  docs/architecture/version-scheme.md (new)                     ~3h
  B.3  standards/autonomous/ (2 files, submodule ops)                 ~5h
       incl. B.3.0 submodule operation runbook execution             (~1h)
       incl. B.3.1 decision-autonomy-matrix.md                       (~2h)
       incl. B.3.2 humanized-command-patterns.md ≥10 samples         (~2h)
  B.4  aria-orchestrator/docs/layer-boundary-contract.md (new)       ~3h
  B.5  aria-orchestrator/README v2.0                                  ~0.5h (collapsed into B.4 pass)
  B.6  architecture-decisions.md AD-M5-11 claim + stubs              ~0.5h
  ─────────────────────────────────────────────────────────────────────
  TG-DOCS-B subtotal                                                  ~22h

Total (AI-implementable):                                            ~33h
```

Owner manual action (post-ship, not in B.2):
- Post the Forgejo Discussion FAQ (text drafted in A.3; URL evidence collected by Spec #4).
- Confirm plugin version badge value is correct after Phase B.

---

## Dependencies

| Dependency | Direction | Notes |
|------------|-----------|-------|
| Spec #1 cost.json schema (`c29a800`) | Upstream (locked) | B.4 `layer-boundary-contract.md` documents this schema but does NOT modify it. Schema is frozen. |
| Spec #2 TG-C corpus path `aria-orch/evals/m6-prompt-quality/` | Cross-reference | B.3.2 cross-refs this path. If Spec #2 changes the corpus path, B.3.2 must be updated. Coordinate with backend-architect. |
| `aria-orchestrator/docs/claude-md-revision-draft.md` | Upstream (existing draft) | A.1 consumes diffs 1-8 from this file. |
| `aria/.claude-plugin/plugin.json` | Upstream (read-only) | A.3 and Probe 1 read the version field for badge verification. |
| Spec #4 `aria-2.0-m6-release-closeout` | Downstream | Spec #4 gates on CLAUDE.md v2.0 (AC-1) + state-checks probes (AC-4) from this Spec. |
| `standards/` submodule git repo | Infrastructure | B.3 requires feature branch + merge + pointer bump. Submodule must be on default branch before archive per `[[feedback_submodule_branch_before_archive]]`. |

---

## Cross-references

**Predecessors**:
- [openspec/archive/2026-05-23-aria-2.0-m5-replay-reconciler-drift-review-loop-audit/](../../archive/2026-05-23-aria-2.0-m5-replay-reconciler-drift-review-loop-audit/) — M5 archived, CLAUDE.md draft was M0 T5.3 deliverable
- [aria-orchestrator/docs/claude-md-revision-draft.md](../../../aria-orchestrator/docs/claude-md-revision-draft.md) — M0 T5.3: 8 diffs draft ready for consumption

**Sibling Specs (M6 parallel)**:
- [aria-2.0-m6-cost-acceptance](../aria-2.0-m6-cost-acceptance/proposal.md) — Spec #1, Approved `c29a800`. B.4 layer-boundary-contract.md documents Spec #1 cost.json schema.
- [aria-2.0-m6-e2e-resilience](../aria-2.0-m6-e2e-resilience/proposal.md) — Spec #2, parallel. B.3.2 cross-refs Spec #2 TG-C corpus path.
- [aria-2.0-m6-release-closeout](../aria-2.0-m6-release-closeout/proposal.md) — Spec #4, sequential after all M6 Specs. Gates on CLAUDE.md v2.0 + state-checks probes.

**Decisions**:
- [.aria/decisions/2026-05-24-us026-m6b-brainstorm.md](../../../.aria/decisions/2026-05-24-us026-m6b-brainstorm.md) — DEC-20260524-001 §2 Spec #3 scope + §4 P-10..P-13 (source-of-truth)

**PRD references**:
- [docs/requirements/prd-aria-v2.md §M6](../../../docs/requirements/prd-aria-v2.md) — M6 scope (Week 26-30, ~82h total, post `a786444`)
- PRD §553 — decision autonomy matrix rationale
- PRD §639 — humanized command rubric

**Memory entries**:
- `[[feedback_pre_draft_bug_hunt_discipline]]` — P-12 probe scripts bug-hunted against PASS/FAIL before commit
- `[[feedback_falsifiable_evidence_for_binary_acceptance]]` — all ACs cite concrete verifiable evidence
- `[[feedback_spec_v2_body_propagation_2pass]]` — P-10..P-13 precision items propagated to both §What and tasks.md
- `[[feedback_submodule_branch_before_archive]]` — P-10 standards submodule sequence; verify pointer on default branch before archive
- `[[project_meta_repo_pattern]]` — standards as own git repo, not vendored
- `[[feedback_clear_cache_before_code_change]]` — M6 release verification preflight: clear plugin cache before CLAUDE.md v2.0 testing
- `[[feedback_submodule_regression_pitfall]]` — concurrent Spec landing + submodule pointer bump discipline
- `[[feedback_ad_slot_backfill_checkpoint]]` — AD-M6-8 must be filled or retired before Spec archives
