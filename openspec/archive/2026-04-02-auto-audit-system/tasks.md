# 十步循环自动审计系统 — 任务分解

> **Parent**: proposal.md
> **Estimated Total**: 54-74 hours (revised after 3-round audit)
> **Audit**: 3-round convergence audit applied, 25+ issues addressed

## Phase 1: 核心引擎 (22-30h)

### T1: 审计引擎 Skill (audit-engine)
- **估时**: 14-18h (revised from 8-10h)
- **内容**: 新建 `aria/skills/audit-engine/SKILL.md`
  - convergence 模式完整执行流程
  - challenge 模式完整执行流程 (含数据传递 schema)
  - 汇总引擎 (合并 + 去重 + 结构化提取, 复用 agent-team-audit 去重算法)
  - 结论提取器 (结构化输出: `{type, severity, category, scope, summary}`)
  - 收敛判定器 (四元组集合比较 + 投票 + 振荡检测)
  - max_rounds 保护 + 未收敛降级策略 (三路径选择)
  - 错误处理 (spawn 失败/超时/529 降级)
  - 审计报告生成 (含 verdict 计算, Severity 兼容)
- **依赖**: 无
- **Agent**: tech-lead

### T2: config-loader 扩展
- **估时**: 8-12h (revised from 4-6h)
- **内容**: 扩展 `aria/skills/config-loader/SKILL.md`
  - T2a: 旧配置兼容层 — `experiments.agent_team_audit` 自动映射到 `audit.*` (4-5h)
  - T2b: 项目特征分析 — 生成建议配置 (非自动写入, 展示给用户确认) (4-7h)
  - 字段验证规则更新 (valid_values 扩展到 7 个检查点)
  - 注意: config-loader 当前 `disable-model-invocation: true`, 项目特征分析可能需要调整此约束或拆分为独立子功能
- **依赖**: T1 (需要审计配置 schema)
- **Agent**: backend-architect

### T3: 审计配置模板
- **估时**: 4-6h
- **内容**:
  - 完整 Agent 分组默认值 (11 Agents x 7 检查点, proposal 中已定义 6 Agent 覆盖, 其余 5 Agent 的检查点分配需补充)
  - adaptive 规则默认值
  - config.template.json 更新 (含 audit 块)
  - config-loader DEFAULTS.json 更新
- **依赖**: T1
- **Agent**: tech-lead + knowledge-manager

## Phase 2: 检查点集成 (20-26h)

### T4: 已有检查点升级 (post_spec, post_implementation, pre_merge)
- **估时**: 6-8h
- **内容**:
  - phase-a-planner: post_spec → 调用 audit-engine (替代直接调用 agent-team-audit)
  - phase-b-developer: post_implementation → 调用 audit-engine
  - phase-c-integrator: pre_merge → 调用 audit-engine
  - 更新消费方 hardcoded `skill: agent-team-audit` 引用
  - 保持向后兼容 (audit.enabled=false 时行为不变)
- **依赖**: T1, T3
- **Agent**: backend-architect

### T5: 新增检查点 (post_brainstorm, post_planning, mid_implementation, post_closure)
- **估时**: 6-8h
- **内容**:
  - brainstorm: post_brainstorm 触发点 (需确认 brainstorm 的 allowed-tools 是否支持 Agent spawn)
  - task-planner: post_planning 触发点
  - phase-b-developer: mid_implementation 触发点 (基于 task_progress >= threshold% 条件)
  - phase-d-closer: post_closure 触发点 (限制为 convergence + max_rounds=1)
- **依赖**: T1, T3 (T4 非硬依赖, 可并行)
- **Agent**: backend-architect

### T6: state-scanner adaptive 集成
- **估时**: 4-6h
- **内容**:
  - state-scanner 复杂度评估结果传递给审计路由
  - adaptive 模式下自动选择 off/convergence/challenge
  - 审计状态在 state-scanner 输出中展示
- **依赖**: T1, T3
- **Agent**: tech-lead

### T6b: 并发控制验证
- **估时**: 2-4h
- **内容**:
  - 验证 agent-team-audit 的并发限制 (max_parallel: 2, overall: 300s) 在多轮场景下的行为
  - 确认每轮独立计时、轮次间串行
  - challenge 模式组间串行确认
- **依赖**: T1, T4
- **Agent**: qa-engineer

## Phase 3: 验证与文档 (12-18h)

### T7a: audit-engine AB 基准测试
- **估时**: 4-6h
- **内容**:
  - audit-engine with/without AB 测试 (使用 /skill-creator)
  - convergence vs challenge 效果对比 (研究性测试, 非 Rule #6)
  - 收敛轮次统计
  - 结果存入 aria-plugin-benchmarks/audit-engine/
- **依赖**: T1-T6
- **Agent**: qa-engineer

### T7b: 被修改 Phase Skills 回归测试
- **估时**: 4-6h
- **内容**:
  - 回归 AB 测试清单: config-loader, phase-a-planner, phase-b-developer, phase-c-integrator, phase-d-closer, brainstorm, task-planner, state-scanner
  - 每个 Skill 的 AB delta ≥ 0 (无回归)
  - 使用现有 ab-suite 基线对照
- **依赖**: T4, T5, T6
- **Agent**: qa-engineer

### T8: 文档更新
- **估时**: 4-6h
- **内容**:
  - CLAUDE.md: 审计规则说明
  - config.template.json: 完整审计配置示例
  - system-architecture.md: 新增审计子系统章节 (Section 8.7)
  - aria/README.md + README.zh.md: Skills 数量更新 (30→31)
  - aria/CHANGELOG.md: v1.9.0 条目
  - 版本文件: plugin.json (真理来源), marketplace.json, VERSION
  - US-004.md: Status pending → done, 验收标准勾选
  - DEC-20260401-001: 补充 Status 字段
- **依赖**: T7a, T7b
- **Agent**: knowledge-manager

## 依赖图

```
T1 (audit-engine, 14-18h) ──┬──→ T3 (配置模板) ──┬──→ T4 (已有检查点升级)
                             │                     │
T2 (config-loader, 8-12h) ──┘                     ├──→ T5 (新增检查点) ← 与 T4 并行
                                                   │
                                                   └──→ T6 (state-scanner)
                                                        │
                                                   T6b (并发验证)
                                                        │
                                                   ┌────┴────┐
                                                   T7a       T7b  ← 并行
                                                   └────┬────┘
                                                        T8 (文档)
```

**关键路径**: T1 → T3 → max(T4, T5) → T7 → T8
**可并行**: T1 与 T2 | T4 与 T5 | T7a 与 T7b

## 里程碑

| 里程碑 | 完成标志 | 预计 |
|--------|---------|------|
| M1: 引擎可用 | T1-T3 完成, convergence 模式可手动触发 | Phase 1 |
| M2: 全检查点集成 | T4-T6b 完成, adaptive 模式可用 | Phase 2 |
| M3: 发布就绪 | T7-T8 完成, AB 验证通过, 无回归 | Phase 3 |
