# OpenSpec Proposal: Strengthen Rule #6 Enforcement

- **Level**: 2 (Minimal)
- **Status**: Complete
- **Created**: 2026-03-19
- **Author**: 10CG Lab
- **Reviewed By**: Agent Team (Tech Lead + QA Engineer + Backend Architect + Knowledge Manager + Code Reviewer)

## Why

v1.7.0 开发中修复 aria-plugin#1 时，修改了 state-scanner/SKILL.md 但未自动触发 AB 测试验证。用户手动提醒后才补跑。

根因: CLAUDE.md 规则 #6 ("Skill 变更必须运行 AB 测试") 只存在于文档文本中，未编码到任何 Skill 执行流程。`benchmarks.require_before_merge` 配置字段已声明但从未实现检测逻辑。

## What

在 2 个 Skill 中增加 SKILL.md 变更检测，实现规则 #6 的自动化执行。

### 修改 1: branch-finisher — AB 验证门控 (步骤 2.5)

- 检测: `git diff base..HEAD -- 'skills/*/SKILL.md'`
- 判断: zone-based 启发式区分逻辑变更 vs 文档变更
- 行为: 由 `benchmarks.skill_change_block_mode` 控制 (warn/block/off)
- 新建参考文档: `references/ab-benchmark-gate.md`

### 修改 2: state-scanner — 前置感知 (阶段 1 扩展)

- 在阶段 1 变更分析中新增 `skill_changes` 字段
- 推荐工作流时附加 AB 验证提醒

### 新配置字段

- `benchmarks.skill_change_block_mode`: "warn" (default) / "block" / "off"

### 不做

- 不增加 PreToolUse Hook (P2 延后，数据驱动决策)
- 不修改 phase-c-integrator (branch-finisher 已足够)
- 不修改 commit-msg-generator (职责不符)

## Agent Team 审议决策记录

- Hook BLOCK 方案: 5/5 反对 (语义判断超出 Shell 能力、噪音高、子模块盲区)
- Hook MESSAGE 方案: 延后到 P2，用真实数据验证必要性
- Skill Only 方案: 5/5 同意作为 P1 实施

## Impact

- 修改: `branch-finisher/SKILL.md`, `state-scanner/SKILL.md`
- 修改: `config-loader/SKILL.md`, `config-loader/DEFAULTS.json`
- 新增: `branch-finisher/references/ab-benchmark-gate.md`
- 修改: `.aria/config.template.json`
