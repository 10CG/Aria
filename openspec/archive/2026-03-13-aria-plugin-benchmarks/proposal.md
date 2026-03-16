# OpenSpec Proposal: Aria Plugin Skills Benchmark

- **Level**: 2 (Minimal)
- **Status**: Complete
- **Created**: 2026-03-13
- **Author**: 10CG Lab

## Summary

为 Aria Plugin 的核心 Skills 建立系统化的基准测试体系，量化评估每个 Skill 的效果提升。

## Motivation

- Skills 缺乏客观的效果评估数据
- 无法量化 "使用 Skill" vs "不使用 Skill" 的差异
- 需要为后续 Skill 优化提供基线数据

## Scope

### 已完成测试的 Skills (Tier 1)

| Skill | 测试数 | 通过率 | 关键指标 |
|-------|--------|--------|----------|
| commit-msg-generator | 15 | 100% | 格式合规提升 87% |
| arch-search | 15 | 93% | Token 节省 75-87% |
| state-scanner | 8 | 100% | 状态感知和智能推荐 |
| branch-manager | 10 | 100% | 5 维度自动决策 |
| task-planner | 10 | 100% | 任务分解粒度 4-8h |

### 整体改进统计

| 指标 | With Skill | Without Skill | 提升 |
|------|------------|---------------|------|
| 格式合规率 | 95%+ | 20-40% | +55-75% |
| Token 效率 | 高 | 低 | 70-85% 节省 |
| 决策准确性 | 90%+ | 60% | +30% |

## Deliverables

- `aria-plugin-benchmarks/` 目录，包含 5 个 Skill 的完整评估数据
- 每个 Skill 包含: evals 定义、iteration 结果、benchmark 报告
- `OVERALL_BENCHMARK_SUMMARY.md` 综合报告

## Out of Scope

- Tier 2 Skills 测试 (spec-drafter, subagent-driver, arch-update)
- 自动化回归测试框架
