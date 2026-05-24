# Aria 2.0 M6 Spec #3 — Documentation Suite (CLAUDE.md v2.0 + Architecture + standards/autonomous)

> **Level**: 3 (Full — cross-cuts CLAUDE.md / standards/autonomous / docs/architecture / aria-orchestrator/docs / Aria README)
> **Status**: **Approved** (Phase A.2 CONVERGED 2026-05-24 via R3 stability check; ready for Phase A.3 → Phase B.1; TG-DOCS-B may slip to v2.0.1 per Q-final-1 Menu C)
> **Change ID**: `aria-2.0-m6-docs`
> **Parent US**: [US-026](../../../docs/requirements/user-stories/US-026.md)
> **Parent PRD**: [prd-aria-v2.md §M6](../../../docs/requirements/prd-aria-v2.md) (post `a786444` + `e884e62` PRD patches, §M6 4-5w timeline)
> **Predecessor Spec**: [aria-2.0-m5-replay-reconciler-drift-review-loop-audit](../../archive/2026-05-23-aria-2.0-m5-replay-reconciler-drift-review-loop-audit/proposal.md) (M5 archived 2026-05-23)
> **Brainstorm Source**: [.aria/decisions/2026-05-24-us026-m6b-brainstorm.md](../../../.aria/decisions/2026-05-24-us026-m6b-brainstorm.md) (DEC-20260524-001 §2 Spec #3 + §4 P-10..P-13, CONVERGED 2026-05-24)
> **Effort baseline**: ~33h impl (TG-DOCS-A ~11h release-blocker + TG-DOCS-B ~22h architecture; T-B0.10 +0.1h v1.29.0 gate). Single SoT per `[[feedback_spec_v2_body_propagation_2pass]]`.
> **v2.0.1-deferrable**: TG-DOCS-B (~22h architecture) may ship as v2.0.1 if 5w calendar slips per Q-final-1 Menu C. TG-DOCS-A (~11h) is v2.0.0 release-blocker (ships with v2.0.0 unconditionally).
> **AD allocation reservation**: **AD-M6-7**, **AD-M6-8**, and **AD-M6-9** are reserved for this Spec #3. AD-M6-7 = state-checks probe design. AD-M6-8 = reserved slot. **AD-M6-9** = `standards/autonomous/` namespace creation decision (claimed by this Spec per Q2 owner lock 2026-05-24 — AD-M5-11 collision with M5-spillover scope discovered in R1 audit; Spec #3 vacates AD-M5-11 claim). Spec #1 holds AD-M6-1/2/3; Spec #2 holds AD-M6-4/5/6. (per DEC-20260524-001 §2 AD-M6-* allocation lock 2026-05-24)
> **Audit trajectory**:
>   - Phase A.2 R1 (2026-05-24, 4-agent combined sister-Specs): NEEDS_FIX 4/4 — 5C (T3-1..T3-5) + 4 X-C (X-T1/T2/T4/T5) + 5I; aggregate `post_spec-R1-aggregate-2026-05-24-aria-2.0-m6-sister-specs.md`
>   - Phase A.2 R1-fix applied (commit `8a5fdc4` w/ PRD §568/§656 catch-up): knowledge-manager pass
>   - Phase A.2 R2 challenge (3-agent): SPLIT — cr SCOPE_OK_R2 23/23 / ai SCOPE_OK_R2 / tl-critic NEEDS_FIX 2 NEW C self-spot (paper-fix completion + v1.29.0 gate args inversion)
>   - Phase A.2 R2-fix applied (commit `c0e9d79`): NC-tl-R2-2 gate args inverted → 3-zone branching (match dev-claude2 SoT) + paper-fix Rule #1-#6 → #1-#9 propagation
>   - Phase A.2 R3 stability (tech-lead-critic 1-agent scope-limited): **R3_STABLE** — 0 new C + 0 new I; 3/3 R2 fixes CLOSED byte-for-byte
>   - **CONVERGED** 2026-05-24 — ready for Phase A.3 (knowledge-manager) → Phase B.1 (TG-DOCS-A v2.0.0-blocker first; TG-DOCS-B v2.0.1-deferrable per Q-final-1 Menu C)
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

##### A.1 — CLAUDE.md v1.0.4 → v2.0 (9 diffs) (~4h)

<!-- R1-T3-1 fix: title was "8+1 diffs" conflicting with body count of "9"; unified to "9 diffs" per live CLAUDE.md read. Live file is 454 lines, 9 Rules (#1-#9) already present. Diffs enumerated below are anchored to live line ranges. -->

Source draft: `aria-orchestrator/docs/claude-md-revision-draft.md` (M0 T5.3 deliverable).
The 9 diffs to apply (Diff 1-8 from draft + Diff 9 incremental).
Live CLAUDE.md section map (v1.0.4, 454 lines):
- Lines 1-5: Header block (项目本质 / 核心假设 / 版本)
- Lines 9-18: 文档边界 (no change)
- Lines 21-37: 项目定位 → 研究目标 (Diff 1 + Diff 2)
- Lines 40-76: 核心概念 (Diff 3 adds §两层AI分工 after §十步循环, line ~66)
- Lines 120-188: 信息地图 (Diff 4 adds aria-orchestrator/ row to table at line ~124)
- Lines 208-228: 技术约束 / Aria 的边界 (Diff 5 adds v2.0 boundary line)
- Lines 343-426: 不可协商规则 #1-#9 (Diff 6 = NO-OP verify; Rules #7/#8/#9 body already present)
- Lines 429-453: 项目状态 (Diff 8 updates versions, Diff 9 bumps version field)
- After line 426 (after §不可協商規則): Diff 7 adds new §Aria 2.0 运行时 chapter

**Diff 1 — 文档顶部"项目本质"段落扩展** (draft §Diff 1):
Replace the three-line header block. Change "AI 辅助的领域驱动设计方法论研究" → "AI-DDD 方法论的定义与端到端参考实现 (v1.x 方法论 + v2.0 自主运行时)". Change 核心假设 and version line per draft.

**Diff 2 — "项目定位"章节补充 v2.0 演进说明** (draft §Diff 2):
Add "身份演进 (v1.x → v2.0)" subsection before §研究目标. Content: v1.x = 方法论研究 (人类交互式), v2.0 = 方法论定义 + 端到端参考实现 (AI 自主式). Cross-link to architecture-decisions.md.

**Diff 3 — "核心概念"新增"两层 AI 分工"小节** (draft §Diff 3):
After §十步循环 (live CLAUDE.md ~line 66), add §两层 AI 分工 (v2.0 新增). Layer 1 (Hermes + Luxeno-routed GLM models) = PM role. Layer 2 (aria-runner + CC + aria-plugin) = engineering role. Cross-link AD1 + AD6.
<!-- R1-I3-4 fix: "Hermes + GLM" → "Hermes + Luxeno-routed GLM models" per 2026-05-21 redirect recorded in memory feedback_diagnose_from_provider_config_not_symptom and project_glm_routing_luxeno -->

**Diff 4 — "信息地图"子模块表格新增 aria-orchestrator 行** (draft §Diff 4):
Add table row: `aria-orchestrator/` | v2.0 运行时 (Layer 1/2) | Hermes fork / Docker 镜像 / Nomad job / ADR. Add two §目录导航 entries: Aria 2.0 架构决策 → aria-orchestrator/docs/architecture-decisions.md; Layer 边界契约 → aria-orchestrator/docs/layer-boundary-contract.md.

**Diff 5 — "技术约束"补充 v2.0 边界** (draft §Diff 5):
Add "✅ 实现 (v2.0): 端到端参考实现 (aria-orchestrator, 仅限 10CG Lab 内部)" line. Add clarifying paragraph: v2.0 runtime ≠ general framework.

**Diff 6 — "不可协商规则"章节不修改 (Rules #1-#9 all FROZEN)** (draft §Diff 6 — hard constraint per AD11):
<!-- R1-T3-1 fix: original Diff 6 said "Rules #1-#6 FROZEN" but live CLAUDE.md already has 9 rules (#1-#9 all present, lines 343-426). AD11 freeze scope applies to ALL rules present in the live file. Updated to: Rules #1-#9 text body is FROZEN. -->
Rules #1-#9 text body is FROZEN. No deletions, no modifications to any existing rule body. AD11 compliance extended to all 9 rules.
Verify after edits: `git diff HEAD -- CLAUDE.md | grep "^[-]" | grep "Rule #[1-9]"` must produce no output (Rules #1-#9 bodies unmodified per I3-1 AC addition).

**Diff 7 — 新增"Aria 2.0 运行时"独立章节** (draft §Diff 7, ≤50 lines):
New H2 section after §不可协商规则. Includes: 分层叙述 (standards / aria-plugin / aria-orchestrator), 与 9 条规则的关系 (how Layer 2 enforces each), 人类参与点 (AD10: S7_AWAITING_MERGE), 详细入口 (architecture-decisions.md / spikes / M0 Spec / PRD v2.0).

**Diff 8 — "项目状态"版本号更新** (draft §Diff 8, using M6-time actual values):
Update stage: "研究中 → v2.0 规划已批准" → "v2.0 M6 执行中 (M1-M5 shipped)". Update 插件版本 from v1.22.0 to actual v1.27.0 (current per `c7e611f` submodule bump). Update 主项目版本 v1.7.0. Add 运行时版本 line. Update "更新" date at bottom.

**Diff 9 — Rules #7/#8/#9 + §2.3 frontmatter schema catch-up + plugin version sync** (incremental beyond original draft, ~0.5h):
<!-- R1-T3-1 fix: clarified Diff 9 scope against live CLAUDE.md. Live §项目状态 shows 插件版本: v1.22.0 (stale — plugin.json SoT reads v1.27.0 per dynamic read). DEC-20260524-001 cited v1.26.0 which was draft-time snapshot from dev-claude2 burndown session. -->
<!-- R1-T3-3 fix: plugin version SoT is aria/.claude-plugin/plugin.json. No hardcode — Phase B implementor MUST read dynamically: `python3 -c "import json; print(json.load(open('aria/.claude-plugin/plugin.json'))['version'])"` -->
Rules #7/8/9 and the Rule #9 §2.3 frontmatter schema extension were added to CLAUDE.md AFTER the M0 draft was written (post-M1 through post-M5). The draft does not cover them. Diff 9 is therefore a no-op edit on Rule #7/8/9 body text (they are already in the live CLAUDE.md) — but requires:
- **Plugin version synchronization** (non-trivial): Live CLAUDE.md §项目状态 (line ~434) shows `插件版本: v1.22.0` — this is stale. Plugin SoT `aria/.claude-plugin/plugin.json` reads `v1.27.0`. DEC-20260524-001 cited v1.26.0 as draft-time snapshot; dev-claude2 burndown session shipped v1.27.0 same session. Update to: read version dynamically via `python3 -c "import json; print(json.load(open('aria/.claude-plugin/plugin.json'))['version'])"` — do NOT hardcode.
- Rule #8 §exception clause: verify `phase_c_integrator.pre_merge_gate.no_aether_fallback` field name in live CLAUDE.md §Rule #8 matches `config.template.json` (already present; no edit if correct).
- Rule #9 §2.3 frontmatter extension: verify cites `aria-plugin v1.22.x+` (already present; no edit if correct).
- Version field: bump `**版本**: 1.0.4` → `**版本**: 2.0.0`.

Note: Plugin version SoT = `aria/.claude-plugin/plugin.json`. DEC-20260524-001 v1.26.0 was draft-time snapshot; dev-claude2 burndown shipped v1.27.0 in the same session. AC-3 and Diff 9 must read the version dynamically, not hardcode any snapshot value.

Constraint (AD11): Diff 9 MUST NOT alter Rule #1-#9 text. It only updates §项目状态 version numbers and bumps the top-level version field.

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

<!-- R1-T3-2 fix: original `head -1` ordering is fragile to README layout changes and extracts v1.15.2 (stale badge) rather than the plugin badge. Replaced with anchored regex on the badge token. Task dependency: Probe 1 verification must run AFTER T-A2.1 (README badge update) to get PASS result; before T-A2.1 it is expected to FAIL (stale badge). Explicit dependency note added. -->

```yaml
- name: "m6-version-badge-match"
  description: |
    Verify README.md Plugin badge version matches aria/.claude-plugin/plugin.json.
    Drift = README badge stale after a plugin version bump.
    Task dependency: this probe produces PASS only after T-A2.1 (README badge update to v1.27.0).
    FAIL before T-A2.1 is expected and correct behavior.
  command: |
    BADGE=$(grep -m1 -oP 'badge[^\d]*v?\K[0-9]+\.[0-9]+\.[0-9]+' README.md)
    PLUGIN=$(python3 -c "import json; print(json.load(open('aria/.claude-plugin/plugin.json'))['version'])")
    [ -z "$BADGE" ] && { echo "MISSING badge pattern in README.md"; exit 1; }
    [ "$BADGE" = "$PLUGIN" ] && echo "OK badge=$BADGE" || { echo "DRIFT badge=$BADGE plugin=$PLUGIN"; exit 1; }
  severity: warning
  fix: "Update README.md Plugin badge to match aria/.claude-plugin/plugin.json version"
  timeout_seconds: 5
  enabled: true
```

Probe 1 PASS/FAIL fixture (T-A6 bug-hunt requirement per `[[feedback_pre_draft_bug_hunt_discipline]]`):
- FAIL case: run probe BEFORE T-A2.1 (badge still v1.15.2, plugin.json = v1.27.0) → must exit 1 with "DRIFT badge=1.15.2 plugin=1.27.0".
- PASS case: run probe AFTER T-A2.1 (badge updated to v1.27.0, plugin.json = v1.27.0) → must exit 0 with "OK badge=1.27.0".

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

<!-- R1-I3-3 fix: original `date -d` is GNU-only (fails on macOS/BSD). Replaced with python3 datetime arithmetic which is cross-platform. -->

```yaml
- name: "m6-arch-doc-stale"
  description: |
    Warn if docs/architecture/system-architecture.md **Last Updated** header is ≥90 days old.
    Architecture docs that age without review silently diverge from reality (post-M5 experience).
  command: |
    LAST=$(grep -oP '(?<=\*\*Last Updated\*\*: )\d{4}-\d{2}-\d{2}' docs/architecture/system-architecture.md | head -1)
    [ -z "$LAST" ] && { echo "MISSING Last Updated header"; exit 1; }
    python3 -c "
import sys, datetime
last = datetime.date.fromisoformat('$LAST')
today = datetime.date.today()
age = (today - last).days
if age < 90:
    print(f'OK age={age}d')
    sys.exit(0)
else:
    print(f'STALE age={age}d (threshold=90d)')
    sys.exit(1)
" || exit 1
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
<!-- P-11: content boundary between standards/autonomous/ and aria-orchestrator/evals/ -->
<!-- R1-X-T1 fix: aria-orch/evals/ → aria-orchestrator/evals/ in comment -->

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
<!-- R1-X-T1 fix: `aria-orch/` shorthand replaced with `aria-orchestrator/` full path throughout this section. Lab-shareable file in standards/ must reference the full path to avoid broken links on other Lab projects cloning standards. -->
<!-- R1-X-T3 fix: "mean" → "median" per Q4 owner lock 2026-05-24 (PRD §656 patched e884e62). Median is more robust for bimodal score distributions. -->
<!-- R1-X-T5 fix: rubric dimensions synced to 7 (D1-D7) per Spec #2 §C.2 SoT. Original had 5 dimensions (naturalness / actionability / context-completeness / brevity / tone-appropriateness); Spec #2 §C.2 defines D1-D7 which is the canonical 7-dimension set. Cross-ref note added. -->
Content boundary clarification (P-11):
- THIS file (`standards/autonomous/humanized-command-patterns.md`): Lab-shareable CURATED patterns. Contains ≥10 distilled examples demonstrating good vs bad command phrasing, the PRD §639 rubric explanation, and scoring guidance. Does NOT contain raw corpus files.
- SPEC #2 TG-C (`aria-orchestrator/evals/m6-prompt-quality/corpus/sample-{01..10}.md`): the actual M6 E2E run samples with per-sample scoring. Does NOT duplicate the pattern guide.
- Cross-reference: this file references Spec #2 TG-C corpus with `See also: aria-orchestrator/evals/m6-prompt-quality/ for M6 E2E corpus samples`. Spec #2 TG-C references this file with `See also: standards/autonomous/humanized-command-patterns.md for Lab-wide pattern guide`.
- No content duplication between the two locations.

Content requirements: ≥10 curated samples (pattern name + bad example + good example + rationale). PRD §639 rubric (7 dimensions D1-D7, median ≥ 7/10 threshold). Header: `<!-- Lab-shareable: this file is in standards/ and may be reused by other 10CG Lab projects. -->`. Cross-reference to Spec #2 TG-C corpus.

**PRD §639 rubric — 7 dimensions (SoT = Spec #2 §C.2):**
Rubric 7 dimensions D1-D7 SoT = Spec #2 §C.2; Spec #3 humanized-command-patterns.md re-uses identical dimension structure (no divergence allowed):

| Dim | Name | Scoring guidance |
|-----|------|-----------------|
| D1 | Naturalness | 0=robotic/template; 10=indistinguishable from skilled human |
| D2 | Specificity | 0=vague; 10=precise actionable steps with exact file/function refs |
| D3 | Tone appropriateness | 0=wrong tone for context; 10=matches request severity and relationship |
| D4 | Completeness | 0=missing required context; 10=all context a developer needs included |
| D5 | Conciseness | 0=verbose padding; 10=minimal words to convey full intent |
| D6 | Technical accuracy | 0=incorrect references; 10=all file/function/commit references correct |
| D7 | Autonomy footprint | 0=over-delegates; 10=appropriately scoped with no unnecessary asks |

Pass threshold: per-sample **median** of D1-D7 ≥ 7.0. Corpus pass: median(sample-01..10 medians) ≥ 7/10 (per PRD §656 patched 2026-05-24 e884e62, mean → median per Q4 lock).

Minimum content: ≥200 lines (rough proxy for ≥10 patterns at ~15-20 lines each + 7-dimension rubric section).

Post-check: `grep -c "^### Pattern" standards/autonomous/humanized-command-patterns.md` ≥ 10 (structural check; replaces fragile `wc -l ≥ 200` proxy per X-T5 fix).

##### B.4 — aria-orchestrator/docs/layer-boundary-contract.md (Aria-specific, NOT in standards/) (~3h)

<!-- km M-km-R2-005: this file is Aria-specific, must NOT go into standards/ -->
<!-- R1-T3-5 fix: PRD §568 patched 2026-05-24 (e884e62) per Q3 R1 audit lock to follow Spec #3 implementation insight (km M-km-R2-005 brainstorm decision). PRD §568 now reads: `aria-orchestrator/docs/` (Aria-specific 内部契约,非 Lab-shareable). Spec #3 §B.4 was already correct; PRD caught up to the Spec. -->
Note: PRD §568 patched 2026-05-24 (e884e62) per Q3 R1 audit lock — location confirmed as `aria-orchestrator/docs/layer-boundary-contract.md`. This file is Aria-specific and must NOT enter `standards/`. PRD §568 post-patch text and Spec #3 §B.4 are now in alignment.

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

##### B.6 — architecture-decisions.md AD-M6-9 claim + AD-M6-7/8 stubs (~0.5h)

<!-- R1-X-T4 fix: AD-M5-11 collision with M5-spillover scope discovered in R1 audit. Live architecture-decisions.md:3460-3478 reserves AD-M5-11 for "M5-spillover topics" (originally reserved for M6 spec drafter to back-fill M5 retroactive decisions). Spec #3 vacates AD-M5-11 claim per Q2 owner lock 2026-05-24. AD-M6-9 reserved instead for standards/autonomous/ namespace creation decision. -->

**Target file**: `/home/dev/Aria/aria-orchestrator/docs/architecture-decisions.md`

Note: AD-M5-11 collision with M5-spillover scope discovered in R1 audit; Spec #3 vacates claim per Q2 owner lock 2026-05-24; AD-M6-9 reserved instead.

1. Add **AD-M6-9** entry for the `standards/autonomous/` namespace creation decision (Lab-shareable vs Aria-specific content boundary — why `layer-boundary-contract.md` goes in `aria-orchestrator/docs/` rather than `standards/`, and why `humanized-command-patterns.md` goes in `standards/autonomous/` rather than `aria-orchestrator/evals/`). Do NOT edit AD-M5-11 (that slot is reserved for M5-spillover topics per its existing text at lines 3460-3480).
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

### CLAUDE.md Rule #1-#9 text is FROZEN (AD11 hard constraint)

Diff 6 is explicitly a no-op. No diff to apply to Rules #1-#9 body text. AD11 "不修改现有 9 条不可协商规则, 只新增 Aria 2.0 运行时章节". Diff 7 and Diff 9 are additive or update-only.

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
  aria-orchestrator/docs/architecture-decisions.md  ← AD-M6-9 claim + AD-M6-7/8 stubs <!-- R1-X-T4 fix: AD-M5-11 → AD-M6-9 -->
  submodule pointer bump:
    git add standards  ← after standards feature branch lands on master
```

### Key design decisions

| ID | Topic | Decision |
|----|-------|----------|
| AD-M6-9 | standards/autonomous/ namespace creation | `standards/autonomous/` is created as a new subdirectory for Lab-shareable autonomous AI operation patterns. Files here are published under the standards submodule and reusable by other 10CG Lab projects. Aria-specific implementation contracts (like `layer-boundary-contract.md`) go in `aria-orchestrator/docs/` instead. Rationale: Lab-shareable patterns benefit from being in the shared standards submodule; Aria-specific contracts would pollute standards/ with Aria internals and create dependency issues for other projects importing standards. AD-M5-11 was vacated (M5-spillover scope collision, Q2 owner lock 2026-05-24 R1 audit). <!-- R1-X-T4 fix: AD-M5-11 → AD-M6-9 per Q2 owner lock 2026-05-24 --> |
| AD-M6-7 | state-checks.yaml probe design (3-probe set) | Three probes address version-badge-match, claude-md-version, and arch-doc-stale. Severity = `warning` (non-blocking) to allow gradual adoption. Commands use standard POSIX tools (grep, date, python3) with no external dependencies. `enabled: true` even during pre-v2.0 window so state-scanner surfaces status proactively. |
| AD-M6-8 | (Reserved — no topic assigned at Phase A) | RESERVED for Phase B decisions discovered during implementation. Per `[[feedback_ad_slot_backfill_checkpoint]]`: AD-M6-8 must be filled or explicitly retired before this Spec archives. |

---

## Acceptance criteria

All criteria are binary-falsifiable per `[[feedback_falsifiable_evidence_for_binary_acceptance]]`. No subjective language.

### AC-1 — CLAUDE.md v2.0 content verified (TG-DOCS-A)

<!-- R1-I3-1 fix: added Rule #1-#9 body freeze check (git diff based). Count-based check (grep -c "Rule #") is necessary but not sufficient — a rename attack could pass the count while modifying rule bodies. -->

**Evidence**:
```bash
grep -c "Rule #" CLAUDE.md  # must return ≥ 9 (Rules #1-#9 all present)
grep -q "**版本**: 2.0.0" CLAUDE.md  # Diff 9 version bump applied
grep -q "两层 AI 分工" CLAUDE.md  # Diff 3 applied
grep -q "Aria 2.0 运行时" CLAUDE.md  # Diff 7 chapter present
grep -q "aria-orchestrator" CLAUDE.md  # Diff 4 table row present
# Rule #1-#9 body freeze check (AD11 + Rule #9 extension: all rules frozen):
git diff HEAD -- CLAUDE.md | grep "^[-]" | grep "Rule #[1-9]"  # must produce no output (R1-I3-1)
```
All six commands pass (first five exit 0; sixth produces no output).

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

<!-- R1-T3-3 fix: replaced hardcoded v1.27.0 with dynamic plugin.json read. Hardcoding is brittle — next plugin bump will silently fail this AC. DEC-20260524-001 v1.26.0 was draft-time snapshot; plugin.json SoT is authoritative. -->

**Evidence**:
```bash
PLUGIN_VER=$(python3 -c "import json; print(json.load(open('aria/.claude-plugin/plugin.json'))['version'])")
grep -qF "$PLUGIN_VER" README.md && grep -q "Aria 2.0" README.md && exit 0
```
Plugin version badge must match the version in `aria/.claude-plugin/plugin.json` (current: v1.27.0 per `c7e611f` — but read dynamically, no hardcode). Plugin version SoT = `aria/.claude-plugin/plugin.json`; DEC-20260524-001 v1.26.0 was draft-time snapshot, dev-claude2 burndown shipped v1.27.0 same session.

### AC-4 — .aria/state-checks.yaml contains 3 new M6 probes (TG-DOCS-A)

<!-- R1-I3-2 fix: `grep -c` counts total lines matching the pattern, not distinct probe names. If a probe description contains the name string, the count doubles. Replaced with per-probe name existence check using `grep -qF "name: \"${probe}\""` loop. Python YAML check is the authoritative gate. -->

**Evidence**:
```bash
# Per-probe name existence check (replaces fragile grep -c count):
for probe in "m6-version-badge-match" "m6-claude-md-version" "m6-arch-doc-stale"; do
  grep -qF "name: \"${probe}\"" .aria/state-checks.yaml || { echo "MISSING probe: $probe"; exit 1; }
done
echo "All 3 probe names present"
# Python YAML structural check (authoritative gate):
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

<!-- R1-X-T1 fix: `aria-orch/evals/m6-prompt-quality` → `aria-orchestrator/evals/m6-prompt-quality` in cross-ref check. -->
<!-- R1-X-T5 fix: `wc -l >= 200` proxy replaced with `grep -c "^### Pattern" >= 10` structural check. The line count proxy passes repetitive content; pattern count directly verifies the ≥10 curated samples requirement. -->

**Evidence**:
```bash
[ -f standards/autonomous/decision-autonomy-matrix.md ] \
  && [ -f standards/autonomous/humanized-command-patterns.md ] \
  && grep -q "Lab-shareable" standards/autonomous/decision-autonomy-matrix.md \
  && grep -q "Lab-shareable" standards/autonomous/humanized-command-patterns.md \
  && grep -q "aria-orchestrator/evals/m6-prompt-quality" standards/autonomous/humanized-command-patterns.md \
  && exit 0
# Structural check for ≥10 curated pattern sections (replaces wc -l proxy per X-T5):
[ $(grep -c "^### Pattern" standards/autonomous/humanized-command-patterns.md) -ge 10 ] && exit 0
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

### AC-10 — AD-M6-9 claimed and AD-M6-7/8 documented (TG-DOCS-B)

<!-- R1-X-T4 fix: AC-10 originally verified AD-M5-11 was "claimed". Per Q2 owner lock, Spec #3 vacates AD-M5-11 and uses AD-M6-9 instead. AC-10 now verifies AD-M6-9 presence (the new namespace creation decision) plus AD-M6-7/8 stubs. AD-M5-11 must remain as RESERVED/M5-spillover in architecture-decisions.md (Spec #3 does NOT overwrite it). -->

**Evidence**:
```bash
grep -q "AD-M6-9" aria-orchestrator/docs/architecture-decisions.md \
  && grep -q "standards/autonomous" aria-orchestrator/docs/architecture-decisions.md \
  && grep -q "AD-M6-7" aria-orchestrator/docs/architecture-decisions.md \
  && grep -q "AD-M6-8" aria-orchestrator/docs/architecture-decisions.md \
  && exit 0
# Verify AD-M5-11 is still present and NOT overwritten (it belongs to M5-spillover):
grep -q "AD-M5-11" aria-orchestrator/docs/architecture-decisions.md \
  && grep -q "Reserved slot\|RESERVED" aria-orchestrator/docs/architecture-decisions.md \
  && exit 0
```

---

## Risks

| ID | Risk | Severity | Mitigation |
|----|------|----------|------------|
| R-M6D-1 | CLAUDE.md Diff 6 accidentally modifies Rule #1-#9 text (AD11 violation) | High | After writing CLAUDE.md v2.0, run `git diff HEAD -- CLAUDE.md` and verify Rules #1-#9 lines are unchanged. AC-1 `grep -c "Rule #"` count ≥ 9 is a necessary but not sufficient check — also verify line-for-line identity on the 9 rule bodies. |
| R-M6D-2 | standards/ submodule pointer drift: feature branch merged in submodule but main Aria pointer not bumped | Medium | Per `[[feedback_submodule_regression_pitfall]]`: after standards branch lands on master, explicitly run `git -C standards pull && git add standards && git commit`. T-B3-0 runbook enforces this. |
| R-M6D-3 | humanized-command-patterns.md content duplicated in Spec #2 TG-C corpus (BOTH-locations boundary violation) | Medium | P-11 content boundary is explicit: standards/ file = curated patterns + rubric guide; `aria-orchestrator/evals/` file = raw corpus samples. Cross-references point to each other. Enforced via header comment in both files. <!-- R1-X-T1 fix: aria-orch/ → aria-orchestrator/ --> |
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
  B.6  architecture-decisions.md AD-M6-9 claim + AD-M6-7/8 stubs     ~0.5h <!-- R1-X-T4 fix: AD-M5-11 → AD-M6-9 -->
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
| Spec #2 TG-C corpus path `aria-orchestrator/evals/m6-prompt-quality/` | Cross-reference | B.3.2 cross-refs this path. If Spec #2 changes the corpus path, B.3.2 must be updated. Coordinate with backend-architect. <!-- R1-X-T1 fix: aria-orch/ → aria-orchestrator/ --> |
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
- [.aria/decisions/2026-05-24-aria-124-submodule-pointer-regression-gate.md](../../../.aria/decisions/2026-05-24-aria-124-submodule-pointer-regression-gate.md) — DEC-20260524-002 Aria #124: v1.29.0 block-mode gate; T-B0.10 precondition source (X-T2 fix) <!-- R1-X-T2 fix: added DEC-20260524-002 cross-ref per Q5 owner pre-decision -->

**PRD references**:
- [docs/requirements/prd-aria-v2.md §M6](../../../docs/requirements/prd-aria-v2.md) — M6 scope (Week 26-30, ~82h total, post `a786444` + `e884e62` patches)
- PRD §567-568 (post `e884e62`) — layer-boundary-contract.md location confirmed as `aria-orchestrator/docs/` (T3-5 Q3 lock)
- PRD §639 (content ref) — humanized command rubric, 7 dimensions D1-D7
- PRD §656 (post `e884e62`) — rubric scoring metric patched to median (Q4 lock 2026-05-24)

**Memory entries**:
- `[[feedback_pre_draft_bug_hunt_discipline]]` — P-12 probe scripts bug-hunted against PASS/FAIL before commit
- `[[feedback_falsifiable_evidence_for_binary_acceptance]]` — all ACs cite concrete verifiable evidence
- `[[feedback_spec_v2_body_propagation_2pass]]` — P-10..P-13 precision items propagated to both §What and tasks.md
- `[[feedback_submodule_branch_before_archive]]` — P-10 standards submodule sequence; verify pointer on default branch before archive
- `[[project_meta_repo_pattern]]` — standards as own git repo, not vendored
- `[[feedback_clear_cache_before_code_change]]` — M6 release verification preflight: clear plugin cache before CLAUDE.md v2.0 testing
- `[[feedback_submodule_regression_pitfall]]` — concurrent Spec landing + submodule pointer bump discipline
- `[[feedback_ad_slot_backfill_checkpoint]]` — AD-M6-8 must be filled or retired before Spec archives
- `[[feedback_audit_driven_fix_conventions]]` — R1 fix-trail: inline `<!-- R1-T3-X fix: ... -->` and `<!-- R1-X-TN fix: ... -->` trace applied throughout this file
