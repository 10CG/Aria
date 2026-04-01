# 十步循环自动审计系统 — 任务分解

> **Parent**: proposal.md
> **Estimated Total**: 40-56 hours

## Phase 1: 核心引擎 (16-22h)

### T1: 审计引擎 Skill (audit-engine)
- **估时**: 8-10h
- **内容**: 新建 `aria/skills/audit-engine/SKILL.md`
  - convergence 模式执行流程
  - challenge 模式执行流程
  - 结论提取器（结构化输出: decisions/issues/risks）
  - 收敛判定器（结论比较 + 投票）
  - max_rounds 保护 + 未收敛警告
  - 审计报告生成（.aria/audit-reports/）
- **依赖**: 无
- **Agent**: tech-lead

### T2: config-loader 扩展 — 项目特征分析
- **估时**: 4-6h
- **内容**: 扩展 `aria/skills/config-loader/SKILL.md`
  - 无配置时自动检测项目特征（技术栈、目录结构、测试框架）
  - 推断相关 Agent 子集
  - 生成完整 .aria/config.json（含审计配置块）
  - 展示给用户确认
- **依赖**: T1（需要知道审计配置 schema）
- **Agent**: backend-architect

### T3: 审计配置模板
- **估时**: 4-6h
- **内容**:
  - 完整 Agent 分组模板（11 Agents x 7 检查点的默认分配）
  - adaptive 规则默认值
  - config.template.json 更新
  - config-loader DEFAULTS.json 更新
- **依赖**: T1
- **Agent**: knowledge-manager

## Phase 2: 检查点集成 (16-22h)

### T4: 已有检查点升级 (post_spec, post_implementation, pre_merge)
- **估时**: 6-8h
- **内容**:
  - phase-a-planner: post_spec 触发审计引擎
  - phase-b-developer: post_implementation 触发审计引擎
  - phase-c-integrator: pre_merge 触发审计引擎
  - 替换现有 agent-team-audit 单轮逻辑
  - 保持向后兼容（audit.enabled=false 时行为不变）
- **依赖**: T1, T3
- **Agent**: backend-architect

### T5: 新增检查点 (post_brainstorm, post_planning, mid_implementation, post_closure)
- **估时**: 6-8h
- **内容**:
  - brainstorm: post_brainstorm 触发点
  - task-planner: post_planning 触发点
  - phase-b-developer: mid_implementation 触发点（基于代码变更量阈值）
  - phase-d-closer: post_closure 触发点
- **依赖**: T1, T3, T4
- **Agent**: backend-architect

### T6: state-scanner adaptive 集成
- **估时**: 4-6h
- **内容**:
  - state-scanner 复杂度评估结果传递给审计路由
  - adaptive 模式下自动选择 off/convergence/challenge
  - 审计状态在 state-scanner 输出中展示
- **依赖**: T1, T4
- **Agent**: tech-lead

## Phase 3: 验证与文档 (8-12h)

### T7: AB 基准测试
- **估时**: 4-6h
- **内容**:
  - audit-engine Skill AB 测试（with/without）
  - convergence vs challenge 对比测试
  - 收敛轮次统计
  - 结果存入 aria-plugin-benchmarks/
- **依赖**: T1-T6
- **Agent**: qa-engineer

### T8: 文档更新
- **估时**: 4-6h
- **内容**:
  - CLAUDE.md 更新（审计规则说明）
  - config.template.json 完整审计配置示例
  - system-architecture.md 更新（审计子系统）
  - README 更新（Skills 数量）
  - CHANGELOG 更新
- **依赖**: T7
- **Agent**: knowledge-manager

## 依赖图

```
T1 (audit-engine) ─┬─→ T3 (配置模板) ─┬─→ T4 (已有检查点) ─→ T5 (新增检查点)
                   │                   │                        ↓
T2 (config-loader) ┘                   └─→ T6 (state-scanner) → T7 (AB 测试)
                                                                 ↓
                                                              T8 (文档)
```

## 里程碑

| 里程碑 | 完成标志 | 预计 |
|--------|---------|------|
| M1: 引擎可用 | T1-T3 完成，convergence 模式可手动触发 | Phase 1 |
| M2: 全检查点集成 | T4-T6 完成，adaptive 模式可用 | Phase 2 |
| M3: 发布就绪 | T7-T8 完成，AB 验证通过 | Phase 3 |
