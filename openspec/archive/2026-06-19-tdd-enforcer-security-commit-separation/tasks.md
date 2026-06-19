# Tasks — tdd-enforcer-security-commit-separation

> ✅ SHIPPED 2026-06-19 (v1.47.0, PR #88 `281388d`)。Cycle D of v1.47.0 release train。#32。安全代码 RED/GREEN commit 强制分离。

## TG-A — schema
- [x] A1. `tdd-config-schema.json` 加 `security_commit_separation` (enabled/path_patterns/commit_msg_keywords/trigger_on_spec_level_3/bypass_token), 默认 enabled=false。
- [x] A2. schema examples 加一条 security 配置示例。

## TG-B — SKILL.md 检测节
- [x] B1. 加「安全代码 RED/GREEN commit 分离」节: 检测触发 (路径/commit-msg/spec level:3/安全 skill) + RED/GREEN/REFACTOR commit 规则。
- [x] B2. 明确命名: 此即 #32 `level_3_strict`, 改名避开 strictness "Level 3 Superpowers" 歧义。

## TG-C — 升级路径
- [x] C1. SKILL 文档升级路径: advisory=warn / strict=block+[skip-tdd] bypass / superpowers=不可绕过。

## TG-D — reference hook + example
- [x] D1. `examples/config-examples/` 加 security_commit_separation 示例 (或并入既有 strict/superpowers 示例)。
- [x] D2. SKILL 附可选 PreCommit hook 参考实现 (项目侧 opt-in; 不接入 Aria hooks.json)。

## TG-E — 验证 (Rule #6 substitute)
- [x] E1. structural: schema 有效 JSON; 检测 pattern 良构; 升级路径矩阵与既有 strictness 一致。
- [x] E2. dogfood-by-construction: Aether #42 `f105646` (bundled +349 test +108 impl) → 检测命中 (auth/credential 路径 + 单 commit 含 test+impl) → 要求拆 RED/GREEN。
- [x] E3. 向后兼容: enabled=false 默认 → 现有行为零变化。

## Phase B/C/D (release train)
- [x] agent-team review (code-reviewer 检测规则 + tech-lead 升级路径设计)。
- [x] commit 到 release 分支。
- [x] 随 v1.47.0 批量 Phase D + close #32 + 归档。
