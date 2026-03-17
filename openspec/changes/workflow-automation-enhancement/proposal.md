# Workflow Automation Enhancement

> **Level**: Full (Level 3 Spec)
> **Status**: Approved
> **Created**: 2026-03-16
> **Parent Story**: US-001
> **Target Version**: v1.1.0

## Why

十步循环当前自动化程度约 75-80%，Phase 间转换需要用户手动触发，会话中断后无法恢复工作流状态。US-001 要求端到端手动步骤减少 50%，需要系统性提升工作流自动衔接能力。

## What

增强 workflow-runner 和 state-scanner，实现 Phase 间自动推进、工作流状态持久化和中断恢复，同时保留两个关键人工确认门。

### 人工确认门 (不可跳过)

| Gate | 位置 | 原因 |
|------|------|------|
| Gate 1 | Spec 审批 (A.1 → B.1) | 需求进入开发必须经人工确认 |
| Gate 2 | Merge to main (C.2) | develop → main 合并绝对不能自动执行 |

### Key Deliverables

- workflow-state 持久化规范 (`.aria/workflow-state.json`)
- workflow-runner `auto-proceed` 模式
- state-scanner 中断恢复检测逻辑
- 高置信度推荐自动执行机制

## Impact

| Type | Description |
|------|-------------|
| **Positive** | 端到端手动步骤减少 50%+，Phase 间转换零等待 |
| **Positive** | 会话中断后可自动恢复到正确状态，降低上下文丢失风险 |
| **Risk** | 自动推进可能导致意外执行，通过两个 Gate 和置信度阈值缓解 |
| **Risk** | 持久化状态与实际 Git 状态不一致，需要 state-scanner 启动时校验 |

## Definitions

| 术语 | 定义 |
|------|------|
| 手动步骤 | 用户必须提供的每次输入 (命令、确认、选择)，Gate 确认计入总数但单独标注 |
| 开发完成 | phase-b-developer 输出 test_passed=true 且无未提交的非测试目录变更 |
| 非 main 合并 | 目标分支不是 main 或 master 的任何合并操作 |
| Gate 1 信号 | proposal.md 的 Status 字段从 Draft 变为 Approved (文件状态读取，非交互) |
| Gate 2 信号 | 强制交互暂停，无论 auto-proceed 设置如何 |

## Constraints

| Type | Constraint |
|------|-----------|
| 架构 | 必须向后兼容现有手动工作流，auto-proceed 为可选模式 |
| 安全 | Gate 1 (Spec 审批) 和 Gate 2 (Merge to main) 绝对不可自动跳过 |
| 依赖 | 基于现有 workflow-runner v2.2.0 和 state-scanner v2.4.0 增强 |
| 并发 | workflow-state.json 使用原子写入 (写临时文件后 rename)；session_id 不匹配时警告用户 |
| 失败恢复 | Auto-proceed 期间 Phase 失败时：(1) 持久化失败状态 (2) 回退到手动模式 (3) 展示恢复上下文 |

## Baseline Measurement Protocol

实现前必须建立基线，否则 SC-6 (手动步骤减少 50%) 无法验收。

**度量方法**:
1. 选择一个 Level 2 功能作为标准场景
2. 使用当前工作流 (v1.0.2) 端到端执行 A.0 → D.2
3. 记录每个人类输入为一个"手动步骤" (命令/确认/选择)
4. Gate 确认计入总数但单独标注
5. 执行至少 2 次取平均值

**验收公式**: `(baseline_steps - post_steps) / baseline_steps >= 0.50`

## Success Criteria

- [ ] Phase A → Phase B 的转换在 Spec 审批后自动推进
- [ ] Phase B → Phase C 的转换在开发完成后自动推进
- [ ] Phase C → Phase D 在非 main 合并场景下自动推进
- [ ] 会话中断后，state-scanner 检测到未完成工作流并提示恢复
- [ ] 高置信度场景 (如 commit_only) 跳过推荐确认直接执行
- [ ] 端到端完成一个 Level 2 功能所需的手动步骤减少 50% (基于 Baseline 度量)
- [ ] Gate 1 和 Gate 2 在任何模式下均强制人工确认
- [ ] Auto-proceed 失败时自动回退到手动模式并通知用户
