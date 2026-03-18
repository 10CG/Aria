# Tasks: Workflow Automation Enhancement

> **Spec**: changes/workflow-automation-enhancement/proposal.md
> **Level**: Full (Level 3)
> **Status**: Approved
> **Created**: 2026-03-16
> **Revised**: 2026-03-16 (Post-review consolidation, 11 agents)
> **Estimated**: 22-28h

---

## 0. Prerequisites (实现前必须完成)

- [ ] 0.1 基线度量: 记录当前 Level 2 功能端到端手动步骤计数
- [ ] 0.2 state-scanner SKILL.md 精简到 <500 行 (提取到 references/)
- [ ] 0.3 workflow-runner SKILL.md 精简到 <500 行 (提取到 references/)

## 1. Workflow State 持久化

- [ ] 1.1 定义 workflow-state.json schema (→ references/workflow-state-schema.md)
- [ ] 1.2 实现 state 写入逻辑 (原子写入: 写临时文件后 rename)
- [ ] 1.3 实现 state 读取和 Git 一致性校验
- [ ] 1.4 实现 state 清理逻辑 (工作流完成或放弃时清理)
- [ ] 1.5 实现并发会话检测 (session_id 不匹配时警告 + 提供接管选项)

## 2. Auto-Proceed 模式

- [ ] 2.1 workflow-runner 增加 auto-proceed 配置选项
- [ ] 2.2 实现 Phase 间自动转换逻辑
- [ ] 2.3 定义"开发完成"可观测信号 (test_passed=true + 无未提交变更)
- [ ] 2.4 实现 Gate 1 (Spec 审批): 读 proposal.md Status 字段，非 Approved 则暂停
- [ ] 2.5 实现 Gate 2 (Merge to main): 强制交互暂停，无法绕过
- [ ] 2.6 实现手动模式回退 (用户可随时切换)
- [ ] 2.7 实现 auto-proceed 失败恢复 (持久化失败状态 → 回退手动 → 展示上下文)

## 3. 中断恢复

- [ ] 3.1 state-scanner 增加中断检测逻辑 (→ references/interrupt-recovery.md)
- [ ] 3.2 创建 SessionStart hook 脚本 (hooks/session-start-check.sh, 官方格式)
- [ ] 3.3 实现恢复执行逻辑 (从中断点继续，恢复 Phase 上下文)

## 4. 推荐引擎优化

- [ ] 4.1 为每条推荐规则添加置信度评分
- [ ] 4.2 实现高置信度 (>90%) 自动执行机制
- [ ] 4.3 添加自动执行审计日志
- [ ] 4.4 添加 auto-proceed 工作流变体到 WORKFLOWS.md

## 5. 验证与文档

- [ ] 5.1 端到端测试: Level 2 功能完整流程 (auto-proceed 开启)
- [ ] 5.2 手动步骤计数对比 (对照 Phase 0 基线，验证 ≥50% 减少)
- [ ] 5.3 验证 Gate 1 + Gate 2 在 auto-proceed 下强制暂停
- [ ] 5.4 更新 workflow-runner SKILL.md (保持 <500 行)
- [ ] 5.5 更新 state-scanner SKILL.md (保持 <500 行，更新触发词)

---

## Summary

| Phase | Tasks | Estimated Hours |
|-------|-------|-----------------|
| 0. Prerequisites | 3 | 4-5h |
| 1. Workflow State 持久化 | 5 | 3-4h |
| 2. Auto-Proceed 模式 | 7 | 5-7h |
| 3. 中断恢复 | 3 | 2-3h |
| 4. 推荐引擎优化 | 4 | 3-4h |
| 5. 验证与文档 | 5 | 3-4h |
| **Total** | **27** | **22-28h** |

---

## Dependencies

```
Phase 0 (Prerequisites)
    │
    v
Phase 1 (持久化) ──┬──> Phase 2 (Auto-Proceed) ──┬──> Phase 4 (推荐优化)
                   │                               │
                   └──> Phase 3 (中断恢复)         └──> Phase 5 (验证)
                                                   │
                        Phase 3 ───────────────────┘
```
