# OpenSpec Proposal: Benchmark Full Coverage

- **Level**: 3 (Full)
- **Status**: Approved
- **Created**: 2026-03-17
- **Author**: 10CG Lab

## Summary

将 aria-plugin-benchmarks 的全部 28 个 Skill 接入 `run_benchmarks.py` 真实执行测试，实现基准测试 100% 覆盖。当前仅 7 个 Skill 接入 runner，21 个仅有模拟评估数据。

## Motivation

- 模拟评估 (evals.json) 使用 JS 风格断言 (`output.includes(...)`)，无法被 runner 执行
- 7 个已接入 Skill 验证了 runner 架构可行性，需要推广到全量
- 缺乏真实执行数据无法准确评估 Skill 效果
- 为 v1.1.0 工作流自动化增强提供完整基线数据

## Scope

### 已接入 (7 个 — 不变)

| Skill | Evals | 通过率 |
|-------|-------|--------|
| commit-msg-generator | 1 | 100% (Very Stable) |
| state-scanner | 1 | 100% (Stable) |
| arch-search | 2 | 100% (Stable) |
| spec-drafter | 1 | 100% (Stable) |
| requirements-validator | 2 | 100% (Stable) |
| task-planner | 1 | 75% (Flaky - has_dependencies) |
| strategic-commit-orchestrator | 1 | 100% (Stable) |

### 待接入: Tier A — 单轮可测 (16 个)

可直接通过 `claude -p` 单轮调用测试：

| Skill | 模拟 Evals | 建议真实 Evals | 说明 |
|-------|-----------|---------------|------|
| agent-router | 5 | 2 | 任务分类 + 多 Agent 检测 |
| api-doc-generator | 5 | 1 | 从代码生成 API 文档 |
| arch-common | 4 | 1 | L0/L1/L2 层级体系验证 |
| arch-scaffolder | 5 | 1 | 从 PRD 生成架构骨架 |
| arch-update | 5 | 1 | 架构文档同步更新 |
| branch-manager | 10 | 2 | 分支命名 + 模式决策 |
| branch-finisher | 4 | 1 | 分支完成流程 |
| openspec-archive | 4 | 1 | Spec 归档路径验证 |
| phase-a-planner | 5 | 1 | Phase A 编排 |
| phase-b-developer | 5 | 1 | Phase B 编排 |
| phase-c-integrator | 5 | 1 | Phase C 编排 |
| phase-d-closer | 5 | 1 | Phase D 编排 |
| progress-updater | 5 | 1 | 进度状态更新 |
| requesting-code-review | 4 | 1 | 代码审查调度 |
| tdd-enforcer | 5 | 1 | TDD 流程验证 |
| workflow-runner | 5 | 1 | 工作流编排 |

### 待接入: Tier B — 需适配 (5 个)

需要特殊处理或降级测试策略：

| Skill | 问题 | 策略 |
|-------|------|------|
| brainstorm | 多轮对话 | 测试首轮输出质量 (单轮降级) |
| subagent-driver | Agent 生命周期管理 | 测试任务分解和分配逻辑 (不启动真实 subagent) |
| forgejo-sync | 依赖 Forgejo API | 测试同步计划生成 (不执行真实 API 调用) |
| requirements-sync | 依赖外部系统 | 测试漂移检测逻辑 (本地验证) |
| integration-tests | 跨 Skill 编排 | 测试单个集成场景 (A→B 衔接) |

## Deliverables

1. `runner/config.json` — 扩展到 28 个 Skill，每个至少 1 个真实执行 eval
2. 每个新增 Skill 的 eval 包含: prompt + regex assertions + 可选 setup/cleanup
3. 更新 `OVERALL_BENCHMARK_SUMMARY.md` 反映全量覆盖
4. 至少 1 次全量运行结果 (28 Skills)

## Constraints

- 单次全量运行成本控制在 ~$5 以内 (当前 7 Skill ~$1.9)
- 每个 eval 超时上限 300s (沿用现有配置)
- 不修改 runner 核心架构 (run_benchmarks.py)
- Tier B 技能使用降级策略，不要求多轮/外部 API

## Success Criteria

- [ ] 28/28 Skill 在 config.json 中有 enabled eval
- [ ] 全量运行通过率 >= 80%
- [ ] Tier A 通过率 >= 90%
- [ ] 无新增环境依赖 (不要求 Forgejo/Jira 连接)
- [ ] OVERALL_BENCHMARK_SUMMARY.md 更新

## Out of Scope

- runner 架构重构 (并行执行、retry 机制)
- CI/CD 集成
- 多模型对比测试 (Opus vs Sonnet)
- Tier 2 断言精细化优化
