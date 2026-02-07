# 两阶段代码审查集成测试计划

> **测试任务**: TASK-006
> **测试日期**: 2026-02-07
> **测试范围**: aria:code-reviewer Agent + requesting-code-review Skill

---

## 测试环境

```yaml
项目: Aria
分支: master
基础提交: d986fd9
测试变更: 两阶段代码审查实现
```

---

## 测试场景

### 场景 1: 正常流程 - Phase 1 PASS + Phase 2 PASS

**目标**: 验证正常代码能通过两阶段审查

**测试步骤**:
1. 创建符合规范的测试文件
2. 调用 aria:code-reviewer Agent
3. 验证 Phase 1 PASS
4. 验证 Phase 2 PASS
5. 验证输出格式正确

**预期结果**:
```
Phase 1: ✅ PASS
Phase 2: ✅ PASS
Assessment: 可以继续下一任务
```

---

### 场景 2: 规范检查失败 - Phase 1 FAIL 阻塞

**目标**: 验证 Phase 1 FAIL 能正确阻塞审查

**测试步骤**:
1. 创建不符合计划的代码（缺少必需功能）
2. 调用 aria:code-reviewer Agent
3. 验证 Phase 1 FAIL
4. 验证审查终止（不执行 Phase 2）
5. 验证阻塞问题报告清晰

**预期结果**:
```
Phase 1: ❌ FAIL
Phase 2: 跳过
结果: 审查终止，必须修复后重新提交
```

---

### 场景 3: 质量检查警告 - Phase 2 PASS_WITH_WARNINGS

**目标**: 验证 Phase 2 Important 问题处理

**测试步骤**:
1. 创建有质量问题的代码
2. 调用 aria:code-reviewer Agent
3. 验证 Phase 1 PASS
4. 验证 Phase 2 发现 Important 问题
5. 验证评估建议合理

**预期结果**:
```
Phase 1: ✅ PASS
Phase 2: ⚠️  PASS_WITH_WARNINGS
Issues: [2] Important
Assessment: 建议修复 Important 问题后继续
```

---

### 场景 4: 无计划降级 - 仅 Phase 2

**目标**: 验证无计划文件时降级到仅 Phase 2

**测试步骤**:
1. 不提供 detailed-tasks.yaml
2. 调用 aria:code-reviewer Agent
3. 验证 Phase 1 跳过
4. 验证 Phase 2 正常执行

**预期结果**:
```
Phase 1: ⏭️ 跳过 / Skipped
Phase 2: ✅ 执行
原因: 未找到 detailed-tasks.yaml 或 OpenSpec proposal.md
```

---

### 场景 5: Skill 调用

**目标**: 验证 requesting-code-review Skill 正常工作

**测试步骤**:
1. 确认 Skill 已注册
2. 模拟 Skill 调用流程
3. 验证模板填充正确
4. 验证 Agent 调用正确

**预期结果**:
```
Skill: requesting-code-review
状态: 已注册
功能: 自动收集参数，填充模板，调用 Agent
```

---

### 场景 6: Agent 直接调用

**目标**: 验证直接调用 aria:code-reviewer Agent

**测试步骤**:
1. 使用 Task tool 调用 code-reviewer
2. 验证 Agent 正确启动
3. 验证 Agent 正确执行两阶段审查
4. 验证输出格式符合预期

**预期结果**:
```
Agent: aria:code-reviewer
状态: 可调用
功能: 执行两阶段审查，输出报告
```

---

### 场景 7: subagent-driver 集成

**目标**: 验证 enable_two_phase 参数生效

**测试步骤**:
1. 检查 subagent-driver SKILL.md 更新
2. 验证 enable_two_phase 参数存在
3. 验证两阶段审查流程文档正确

**预期结果**:
```
subagent-driver:
  enable_two_phase: true  # 参数存在
  流程: 任务完成 → 两阶段审查 → 继续
```

---

## 测试结果模板

```yaml
场景: 场景 1 - 正常流程
状态: PASS / FAIL / SKIP
执行时间: HH:MM:SS

步骤结果:
  - 步骤 1: PASS / FAIL
  - 步骤 2: PASS / FAIL
  ...

问题记录:
  - 问题描述
  - 严重程度
  - 修复建议

截图/日志:
  - (可选)
```

---

## 测试执行记录

### 执行开始

- **开始时间**: 2026-02-07
- **执行人**: Claude (Agent)
- **测试环境**: Aria 项目本地环境

---

**测试计划版本**: 1.0.0
**创建日期**: 2026-02-07
**维护**: Aria 项目组
