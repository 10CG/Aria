# Tasks: aria-secret-guard-plugin-default

> **Spec**: openspec/changes/aria-secret-guard-plugin-default/proposal.md
> **Level**: Full (Level 3)
> **Status**: Draft (Rev1, post R1 audit)
> **Created**: 2026-05-22
> **Estimated**: 5.5-9h (single cycle; +0.5h Rev1 mitigations vs original)

---

## 1. Hook Source Migration (aria-plugin SOT)

- [ ] 1.1 Cherry-pick `secret-guard.sh` + `secret-scan.sh` from SilkNode v1.2 commit `8eef709` to `aria/hooks/`
- [ ] 1.2 Audit cherry-picked source for path references: grep for `$CLAUDE_PROJECT_DIR`, classify each occurrence as (a) project-scoped (keep as-is, e.g., scanning project files) vs (b) plugin-internal (replace with `${CLAUDE_PLUGIN_ROOT}`); document classification in commit message
- [ ] 1.3 Verify `~/.claude/logs/guard-bypass.log` path survives plugin-context (user-home, not project-dir — should be unchanged)
- [ ] 1.4 Port 251 self-tests (207 guard + 44 scan) to `aria/hooks/tests/` (pure bash, jq唯一 dep, 0 bats)
- [ ] 1.5 Add 1 new test: `${CLAUDE_PLUGIN_ROOT}` substitution resolves correctly at plugin-context runtime (env-var resolution test)
- [ ] 1.6 Local verify: `bash aria/hooks/tests/secret-guard.test.sh` + `secret-scan.test.sh` → 252/252 PASS (251 ported + 1 new)
- [ ] 1.7 Update `aria/hooks/hooks.json`: add PreToolUse (Bash + Read|Edit|Write|MultiEdit → secret-guard.sh) + PostToolUse (Bash|Read|Edit|Write|MultiEdit → secret-scan.sh); **NotebookEdit 不注册** (per proposal §Tool Matcher decision)

## 2. aria-doctor Detection (Mid scope, Rule #6 structural substitute)

- [ ] 2.1 Implement `check_secret_guard_install()` 5-state schema per proposal §State Schema: `not_installed` / `single_plugin` / `single_local` / `dual_install` / `corrupted_settings` + sub-flags `stale_local_version` / `divergent_content` (output: `{state, sub: []}`)
- [ ] 2.2 Detection logic: scan `${CLAUDE_PROJECT_DIR}/.claude/scripts/secret-guard.sh` existence + parse `.claude/settings.json` hook registration + (for dual_install) parse local copy version banner + SHA256 vs plugin SOT
- [ ] 2.3 Document check function in `aria/skills/aria-doctor/SKILL.md`: state semantics + advisory text per state + Rule #6 atomicity guard (output schema is **append-only** in subsequent minors;primary state enum frozen until major bump)
- [ ] 2.4 Write 7 unit tests: 5 primary states + 2 sub-flag detection (stale_local_version on version-banner mismatch + divergent_content on SHA mismatch); cover edge: file present but not registered → `single_local` with advisory "settings.json 未注册";registered but file missing → `corrupted_settings`
- [ ] 2.5 Document Rule #6 structural substitute compliance in `aria-plugin-benchmarks/ab-results/2026-MM-DD-aria-secret-guard-plugin-default-structural/`: structural fixture README (per precedent `2026-05-17-h0-handoff-structural`) + atomicity guard evidence + dogfood evidence + 说明 "no LLM AB per `feedback_deterministic_structural_skill_rule6_substitute` deterministic-skill substitute pattern"

## 3. Documentation Sync (standards)

- [ ] 3.1 Update `standards/conventions/secret-hygiene.md`: add §Layer 2 enforcement 段 (referencing plugin SOT `aria/hooks/secret-guard.sh`); cherry-pick origin = SilkNode v1.2 historical credit
- [ ] 3.2 Add Path↔Layer terminology mapping table at top of secret-hygiene.md (R1 audit M9): "Path 1 prose hygiene" ↔ Layer 0 / "Path 2 ack escape" ↔ inline / "Path 3 hook" ↔ Layer 2 (本 Spec v1.24.0)
- [ ] 3.3 Note Q1 evidence boundary (R1 audit BA F5): 实证覆盖 PreToolUse on Write event;Bash + 其他 tool types 由 hook orchestrator 同等处理 (理论 + 251 self-tests 覆盖 Bash + Read|Edit 实际行为)
- [ ] 3.4 Document local copy + plugin coexist 模式 + 5-state aria-doctor advisory pointer

## 4. Plugin Release (5+1 SOT bump v1.23.0 → v1.24.0)

- [ ] 4.1 Pre-bump verify: `cat aria/VERSION && python3 -c "import json;print(json.load(open('aria/.claude-plugin/plugin.json'))['version'])"` → expect both `1.23.0` (R1 audit T-current-version-verification)
- [ ] 4.2 Update `aria/.claude-plugin/plugin.json` `version` → `1.24.0` (真理来源)
- [ ] 4.3 Sync `aria/.claude-plugin/marketplace.json` (`version` + `plugins[].version` → `1.24.0`)
- [ ] 4.4 Update `aria/VERSION` snapshot → `1.24.0` + 发布日期 + 描述段
- [ ] 4.5 Add `aria/CHANGELOG.md` `[1.24.0]` section: features (default-on secret-guard hooks) + **known limitations 全集** (per proposal §Impact Risk-Known): (a) `cat <script> && grep .env <script>` false-positive (regex 保守 trade-off); (b) log-file grep false-negative (risky_patterns 未覆盖 log scanning, parent DEC §2.6 deferred Q4) + ack 路径
- [ ] 4.6 Update `aria/README.md`: version `1.24.0` + Skills count (维持) + hooks count (新增 secret-guard + secret-scan, 见 §Hooks 系统 section)

## 5. Dogfood & Ship Gate Smoke (Q2 P2 + Rev1 fallback paths)

- [ ] 5.1 Aria self dogfood: install plugin v1.24.0-rc locally, run ~10 daily-use commands (git status / git log / ls / grep / find / cat / docker ps / nomad node status / consul members / nomad var get -out=keys); **capture timing per event** to verify p95 < 100ms (per proposal §Performance Budget)
- [ ] 5.2 SilkNode cross-project smoke (P2 default): pull plugin v1.24.0-rc, run SilkNode owner-provided daily-use command set (~10 commands), record results
- [ ] 5.2.fallback If SilkNode owner unavailable Day 0-7: 降级 P2.5 (SilkNode smoke 转 post-ship 7-天 dogfood);Day 14+: P3 Aria owner stand-in (跑 SilkNode 通用集合 + 3-5 项目特有, mode=`owner_stand_in`)
- [ ] 5.3 Write `openspec/changes/aria-secret-guard-plugin-default/smoke-evidence.md` with schema:
  ```yaml
  smoke_runs:
    - project: <Aria|SilkNode|Aether>
      mode: <owner_provided|owner_stand_in|deferred_post_ship>
      date: <YYYY-MM-DD>
      commands: [list]
      results:
        - command: <cmd>
          tool: <Bash|Read|Edit|Write|MultiEdit>
          hook_path: <plugin|project|both>
          outcome: <allow|block>
          classification: <expected_allow|expected_block|known_limitation|unexpected_false_positive|unexpected_false_negative>
          notes: <free text>
      timing:
        p50_ms: <int>
        p95_ms: <int>
  ```
- [ ] 5.4 Ship gate verdict rubric (R1 audit M5):
  - **PASS**: 0 entries with `classification: unexpected_false_positive` OR `unexpected_false_negative` (`known_limitation` entries permitted unbounded)
  - **REVIEW**: 1-2 unexpected entries → triage (regex narrow or accept as additional known limitation in CHANGELOG)
  - **BLOCK**: ≥3 unexpected entries OR any timing p95 > 100ms → 投资 v1.24.0 OD ("放弃 ship 或接受新发现")

## 6. Audit & Merge (Rule #8 pre-merge gate)

- [ ] 6.1 Trigger `post_implementation` audit (convergence mode) with 5-agent team **locked** (R1 audit CR F1 + T5): `aria:tech-lead + aria:backend-architect + aria:qa-engineer + aria:code-reviewer + aria:knowledge-manager` (与 post_spec 同, 一致性 + Lab security 视角已覆盖于 backend-architect + qa-engineer 的 fail-open/test-strategy lens; **未加 security-reviewer agent** 理由: Aria plugin agent list 当前不含此 role, 安全审视由 backend-architect F3 PostToolUse contract + qa-engineer 251 test 覆盖率确保, 后续 cycle 若加 security-reviewer 可补 post-ship)
- [ ] 6.2 Trigger `pre_merge` audit + run `aether ci status --branch main --in-flight --json` verify (Aether plugin available 时);否则 fallback per `.aria/config.json` `phase_c_integrator.pre_merge_gate.no_aether_fallback` (skip_with_warning 默认)
- [ ] 6.3 Merge standards PR first (prose-only update, low conflict risk)
- [ ] 6.4 **Pre-merge rollback gate**: 在 §6.5 aria-plugin PR merge 前 verify aria-plugin PR Rule #8 gate ALL pass;若 fail → **revert standards PR** (revert commit) 回到 pre-spec state (per proposal §Rollback Plan Row 1)
- [ ] 6.5 Re-bump standards submodule pointer in aria-plugin PR to post-merge HEAD (per memory `feedback_sequenced_multirepo_gitlink_bump`)
- [ ] 6.6 Merge aria-plugin PR (含 v1.24.0 SOT bump)
- [ ] 6.7 Aria main repo: submodule pointer re-bump (aria + standards 各自到 post-merge HEAD) + commit + multi-remote push (origin + github 双推, post-push SHA verify per `feedback_release_phase_d_5_files_synchronization`)
- [ ] 6.8 **Post-push rollback gate**: 若任一远程 post-push SHA 不一致 → 重试; 若始终不一致 → revert aria-plugin merge commit + revert standards (per proposal §Rollback Plan Row 2)

## 7. Closure (Phase D)

- [ ] 7.1 D.1 progress update: Aria 自身无 UPM (memory `project_aria_no_runtime_upm`), 此步骤 no-op
- [ ] 7.2 D.2 archive: move `openspec/changes/aria-secret-guard-plugin-default/` → `openspec/archive/{YYYY-MM-DD}-aria-secret-guard-plugin-default/` (包含 smoke-evidence.md, 一并归档)
- [ ] 7.3 D.3 close Forgejo Aria #84 + #107: post comment with aria-plugin v1.24.0 commit hash + 跨项目 smoke summary + Q1 evidence link (DEC §4) + aria-doctor 5-state 检测命令示例 + §Rollback Plan reference
- [ ] 7.4 D.3 SilkNode PR #429 add reference comment: "framework default complete in aria-plugin v1.24.0 (commit <SHA>); 上游 v1.2 仍可作历史 SOT, 迁移由 SilkNode owner 自决"; (此 deliverable 也写在 proposal §Key Deliverables R1 audit CR F2)
- [ ] 7.5 D.3 write handoff doc `docs/handoff/{YYYY-MM-DD}-aria-secret-guard-plugin-default-shipped.md` with **Rule #9 §2.3 frontmatter** (5 必填字段):
  ```yaml
  ---
  track-id: aria-secret-guard-plugin-default
  owner-container: <从 ~/.aria/container-id 或 hostname 读取>
  phase: D.3
  status: done
  updated-at: <ISO 8601 UTC timestamp>
  ---
  ```
  template ref: `aria/templates/session-handoff.md` (Layer L 急切认领 phase1_gate 不触发, 本 cycle 单 track 单 container)
- [ ] 7.6 D.3 memory verify: confirm `feedback_claude_code_hook_merge_all_fire` indexed (R1 verified ✓); add 1-2 new ship-lesson memory entries if surfaced during cycle (例如 5-state schema design lesson, owner-unavailable fallback experience 等)

## 8. Post-Ship (Out of Cycle, owner-gated)

- [ ] 8.1 Aether 7-day dogfood: Aether owner 在可用时跑 daily-use command set, 记录到 Aether-side issue; **escalation deadline 14 days** (per proposal §Ship Gate Fallback Path Aether) — Day 14+ Aria owner stand-in or escalate to Aria session OD
- [ ] 8.2 v1.24.1 minor trigger condition + SLA: any Aether dogfood unexpected false-positive → 启动 minor cycle within **48h** (narrow regex + changelog 显式 "放宽 X pattern" per Q2 mitigation #3); SLA per proposal Success Criteria Rollback SLA
- [ ] 8.3 v1.25.x scoping: aria-doctor `self-test` 子命令 (run hook against project's typical commands, Q2 mitigation #4)
- [ ] 8.4 PreToolUse Write 内容扫描 (Q4 candidate per parent DEC §2.6): 当前 Write 落入 case default pass-through, 后续 minor 加 Write pre-image content scan

---

## Summary

**8 phases**, ~5.5-9h 单 cycle (§1-§7), §8 post-ship out-of-cycle (含 14-天 Aether escalation + 48h v1.24.1 SLA)。

**Critical path**: §1 → §2 → §5 (Aria + SilkNode smoke per P2/P2.5/P3 path) → §6 (audit + merge + rollback gates) → §7 (closure)

**Parallelizable**: §3 (docs prose) + §4 (version bump) 可与 §1/§2 同时推进

**Ship gate (Q2 P2 + Rev1 fallback)**: §5.1 + §5.2 (or fallback P2.5/P3) must satisfy §5.4 rubric (PASS verdict)

**Audit checkpoints**: §6.1 post_implementation (5-agent locked) + §6.2 pre_merge + Rule #8 (must pass), §6.4 + §6.8 rollback gates

**Out-of-scope deferrals**: §8.3 aria-doctor self-test (v1.25.x), §8.4 Write content scan, Aether dogfood Day 0-13 (Day 14+ escalation policy locked), known false-positive 修 (changelog only)
