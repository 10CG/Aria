# Cross-Project Methodology Validation

> **Level**: Minimal (Level 2 Spec)
> **Status**: Complete
> **Created**: 2026-03-16
> **Parent Story**: US-002
> **Target Version**: v1.1.0

## Why

Aria 方法论目前仅在自身项目中验证，缺乏外部项目的适用性证据。需要建立反馈收集基础设施和可移植性文档，为跨项目验证创造条件。

## What

分两步推进：先建设反馈基础设施和可移植性文档，再进行外部项目试点验证。

### Key Deliverables

- GitHub Issue Templates (适用性报告 + 适配问题)
- aria-plugin 快速上手指南
- standards 子模块独立使用文档
- benchmark runner 跨项目适配
- 至少 1 个外部项目试点报告

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 证明方法论的普适性，提升可信度和采用率 |
| **Positive** | 通过外部反馈发现方法论盲点，推动迭代改进 |
| **Risk** | 外部项目适配成本过高导致验证失败，通过充分的文档和模板降低门槛 |

## Tasks

- [x] 设计 GitHub Issue Templates (Adoption Report + Adaptation Issue)
- [x] 编写 aria-plugin 快速上手指南 (从安装到首次十步循环)
- [x] 编写 standards 子模块独立复用文档
- [x] 适配 benchmark runner 支持外部项目评估
- [x] 选择并执行试点项目 → **Kairos** (TypeScript/Node.js, AI 销售自动化, 已部分采用 OpenSpec/UPM)
- [x] 编写适配过程记录 (Adaptation Log)
- [x] 通过 Issue Template 提交试点适用性报告 → [aria-plugin#2](https://forgejo.10cg.pub/10CG/aria-plugin/issues/2)

## Success Criteria

- [ ] GitHub Issue Templates 已发布到 aria-plugin 仓库
- [ ] 快速上手指南完整覆盖安装→配置→首次使用流程
- [ ] 至少 1 个外部项目通过 Issue Template 提交适用性报告
- [ ] 适用性报告包含效果对比数据 (至少一项指标提升 30%+)
- [ ] 试点项目的适配文档记录所有必要调整及遇到的问题 (Adaptation Log)

## Dependencies

- 依赖 US-001 (workflow-automation-enhancement) 完成后再进行试点验证
- 反馈基础设施 (Issue Templates + 文档) 可与 US-001 并行准备
