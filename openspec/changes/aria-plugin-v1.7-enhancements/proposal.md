# OpenSpec Proposal: Aria Plugin v1.7.0 Enhancements

- **Level**: 3 (Full)
- **Status**: Approved
- **Created**: 2026-03-18
- **Author**: 10CG Lab
- **Target Version**: v1.7.0
- **Reviewed By**: Agent Team (Tech Lead + Backend Architect + QA Engineer + Knowledge Manager)

## Scope Rationale

4 个 Issue 合并为 1 个 OpenSpec 的理由：
- Issue 3 (配置基础设施) 是 Issue 4 (Agent Team 审计) 的硬性前置依赖
- Issue 1 + 2 都是 state-scanner 扩展，修改相同文件 (SKILL.md + RECOMMENDATION_RULES.md)
- 4 个 Issue 共同构成 v1.7.0 版本边界，拆分会导致版本语义碎片化
- 执行顺序 Issue 3 → 1+2 → 4 存在因果链

## Summary

4 项增强提升 Aria 插件的项目适配能力和质量保障机制：
1. README.md 同步检查
2. standards 子模块挂载检测
3. 项目级配置基础设施 (`.aria/config.json`)
4. Agent Team 集体审计实验功能

## Issue 1: README.md 同步检查

### 问题

state-scanner 扫描项目状态时不检查 README.md 版本同步，导致 GitHub/Forgejo 首页展示过时信息。

### 方案

在 state-scanner 新增 **阶段 1.8 (README 同步检查)**：

```yaml
阶段 1.8 - README 同步检查:
  检测路径:
    - README.md (项目根目录)
    - aria/README.md (插件子模块, 如存在)

  检查项:
    - 版本号是否与 VERSION 文件或 plugin.json 一致
    - 最后更新日期是否与 CHANGELOG 最新条目日期一致 (非 wall-clock)

  输出:
    readme_status:
      root:
        exists: true
        version_match: false
        suggestion: "更新 README.md 版本号为 v1.6.0"
      submodules:
        aria: { exists: true, version_match: true }
```

**日期检查数据源**: 以 CHANGELOG.md 最新条目日期为基准，非 wall-clock 时间。避免随时间推移产生误报。

### 影响范围

- 修改: `state-scanner/SKILL.md` (新增阶段 1.8)
- 修改: `state-scanner/RECOMMENDATION_RULES.md` (新增 `readme_outdated` 规则)

## Issue 2: standards 子模块挂载检测

### 问题

装了 aria 插件但未挂载 standards 子模块的项目，Skills 引用 `standards/` 路径时失效，但无提醒。

### 方案: state-scanner 启动时检测

在 state-scanner 新增 **阶段 1.9 (插件依赖检测)**：

```yaml
阶段 1.9 - 插件依赖检测:
  检查项:
    - .gitmodules 中是否有 standards 条目
    - standards/ 目录是否存在且非空

  三种状态:
    1. .gitmodules 无 standards 条目 → 不提示 (项目不需要)
    2. .gitmodules 有条目但 standards/ 为空 → 警告 (未初始化)
    3. standards/ 正常存在 → 无提示

  输出 (状态 2):
    "⚠️ aria-standards 子模块已注册但未初始化。
     建议: git submodule update --init standards"

  推荐规则: standards_missing (优先级 1.5, 建议性, 非阻塞)
```

**注意**: standards 对非 Aria 项目是**可选的**。检测结果为建议性提醒，不阻塞任何工作流。

### 测试环境

需要创建 fixtures 目录: `aria-plugin-benchmarks/state-scanner/fixtures/`
- `no-standards-project/` — 有 .gitmodules 但 standards/ 为空
- `healthy-project/` — 全部正常

### 影响范围

- 修改: `state-scanner/SKILL.md` (新增阶段 1.9)
- 修改: `state-scanner/RECOMMENDATION_RULES.md` (新增 `standards_missing` 规则)
- 新增: `aria-plugin-benchmarks/state-scanner/fixtures/` (测试环境)

## Issue 3: 项目级配置基础设施

### 格式决策: `.aria/config.json`

**选择 JSON 而非 YAML**, 理由 (Agent Team 全员一致):
- v1.6.0 已发布的文档 (confidence-scoring.md, state-scanner/SKILL.md, CHANGELOG.md) 全部使用 `.aria/config.json`
- `.aria/workflow-state.json` 已是 JSON 格式，保持一致
- 向后兼容是 Aria 核心原则
- AI Agent 原生理解 JSON，无需额外解析

### 配置 Schema

```json
{
  "_comment": "Aria 项目级配置 — 所有字段可选，未设置使用默认值",
  "version": "1.0",

  "workflow": {
    "auto_proceed": false
  },

  "state_scanner": {
    "confidence_threshold": 90,
    "auto_execute_enabled": false,
    "auto_execute_rules": ["commit_only", "quick_fix", "doc_only"],
    "audit_log_path": ".aria/audit.log"
  },

  "tdd": {
    "strictness": "advisory"
  },

  "benchmarks": {
    "require_before_merge": true
  },

  "experiments": {
    "agent_team_audit": false,
    "agent_team_audit_points": ["pre_merge"]
  }
}
```

### 与现有 `.claude/tdd-config.json` 的关系

```
优先级 (高 → 低):
  .aria/config.json tdd.strictness     ← 项目统一配置 (推荐)
  .claude/tdd-config.json              ← 遗留配置 (向后兼容)
  Skill 内置默认值                      ← 兜底

策略: .aria/config.json 存在时覆盖 .claude/tdd-config.json 的对应字段。
      .claude/tdd-config.json 中的细粒度字段 (skip_patterns, test_patterns)
      不在 .aria/config.json 中重复，继续在原位生效。
```

### `auto_proceed` 所有权

```
.aria/config.json workflow.auto_proceed  → 静态配置 (项目级意图)
.aria/workflow-state.json auto_proceed   → 运行时状态 (派生自 config)

规则: workflow-runner 在 session 创建时从 config.json 读取并写入 workflow-state.json。
      运行时只读 workflow-state.json。两处不应独立设置。
```

### 配置加载架构: config-loader (独立 Skill)

新建 `aria/skills/config-loader/SKILL.md`:
- `user-invocable: false` (内部基础设施)
- 职责: 查找 → 解析 → 验证 → 合并默认值
- 错误处理: 文件缺失 → 静默返回默认值; 格式错误 → 警告 + 返回默认值; 字段超范围 → 警告 + clamp
- 提供 `DEFAULTS.json` 集中管理所有默认值

### .gitignore 补充

```gitignore
# Aria 运行时文件 (不提交)
.aria/workflow-state.json
.aria/workflow-state.json.tmp
.aria/audit.log
.aria/audit.log.*

# Aria 配置文件 (应提交)
# .aria/config.json — 不要 ignore
```

### 受影响 Skills

| Skill | 读取字段 |
|-------|---------|
| state-scanner | `state_scanner.*`, `workflow.auto_proceed` |
| workflow-runner | `workflow.auto_proceed` |
| tdd-enforcer | `tdd.strictness` |
| branch-finisher | `benchmarks.require_before_merge` |
| phase-c-integrator | `experiments.agent_team_audit*` |
| phase-b-developer | `experiments.agent_team_audit*` |

### 影响范围

- 新增: `aria/skills/config-loader/SKILL.md` + `DEFAULTS.json`
- 新增: `.aria/config.template.json` (带注释的模板)
- 修改: 上述 6 个 Skills 的 SKILL.md
- 修改: `.gitignore`

## Issue 4: Agent Team 集体审计实验功能

### 审计点定义

```yaml
pre_merge (C.2 合并前):
  触发: branch-finisher 完成，准备合并到 master/main
  Agents: Tech Lead + Code Reviewer + Knowledge Manager
  阻塞性: 任一 Agent 报告 Critical 级别问题即 FAIL
  超时: 单 Agent 120s, 整体 300s, 超时标记 skipped 不视为 FAIL

post_implementation (B.2 实现完成后):
  触发: 所有任务标记完成，准备进入 Phase C
  Agents: QA Engineer + Code Reviewer
  阻塞性: 任一 Agent 报告 Critical 即 FAIL
  超时: 同上

post_spec (A.1 规范完成后, 可选):
  触发: OpenSpec 创建完成
  Agents: Tech Lead + Knowledge Manager
  阻塞性: 非阻塞 (建议性)
  超时: 同上
```

### Issue Severity 分级

```yaml
Critical (阻塞):
  - 数据丢失风险
  - 安全漏洞
  - 版本号不一致
  - 架构规则违反

Major (记录但不阻塞):
  - 测试覆盖不足
  - 文档过时
  - 代码规范违反

Minor (仅建议):
  - 排版问题
  - 命名建议
  - 优化机会
```

### FAIL 判定规则

```
verdict = PASS           如果: 0 Critical + 0 Major
verdict = PASS_WITH_WARNINGS  如果: 0 Critical + >=1 Major
verdict = FAIL           如果: >=1 Critical (任一 Agent)

FAIL 阻塞: pre_merge 和 post_implementation
FAIL 不阻塞: post_spec
```

### 问题去重算法

```
1. 收集所有 Agent 的 issues 列表
2. 对每个 issue 提取: {severity, category, affected_file}
3. 两个 issue 被视为相同当: category 相同 且 affected_file 相同
4. 去重后标注: "发现者: Agent A, Agent B" (交叉验证证据)
5. 最终报告中同时展示去重后列表和各 Agent 原始发现数
```

### 并发控制

```yaml
max_parallel_agents: 2    # 默认值, 可在 config.json 中覆盖
hard_cap: 3               # 不可超过

规则:
  - 调用方 (phase-b/c) 不应在其他 subagent 运行时触发审计
  - 超时 Agent 标记为 skipped, 不阻塞其他 Agent
  - 529 错误时等待 30s 后重试一次, 仍失败则 skip
```

### AB 测试方法论

**采用 defect-detection test (QA Engineer 建议):**
- 植入 2-3 个已知缺陷到 fixture 文档
- eval case 1: 植入版本号不一致 → 验证审计是否发现
- eval case 2: 植入缺失 OpenSpec → 验证审计是否发现
- with_skill: 审计执行, 应检出植入缺陷
- without_skill: 无审计结构, 缺陷可能被忽略
- 指标: 确定性的 "是否检出" 而非开放式 "发现多少问题"

### 实验标记

- 默认关闭 (`experiments.agent_team_audit: false`)
- SKILL.md frontmatter: `experimental: true`
- 首次启用时展示实验声明

### 影响范围

- 新增: `aria/skills/agent-team-audit/SKILL.md`
- 新增: `aria/skills/agent-team-audit/references/` (audit-points.md, agent-selection-matrix.md, verdict-format.md)
- 新增: `aria/skills/agent-team-audit/evals/evals.json`
- 修改: `phase-c-integrator/SKILL.md` (pre_merge 触发)
- 修改: `phase-b-developer/SKILL.md` (post_implementation 触发)

## Dependencies

```
Issue 3 (.aria/config.json) ← Issue 4 (audit 开关)
Issue 1 (README check) ← 无依赖
Issue 2 (standards check) ← 无依赖

执行顺序: Issue 3 → Issue 1+2 (并行) → Issue 4
```

## Technical Debt (记录)

- state-scanner 阶段号膨胀 (1.0 到 1.9, 编号空间枯竭)
- state-scanner SKILL.md header "v2.5" vs version field "2.4.0" 不一致
- `.claude/tdd-config.json` 与 `.aria/config.json` 长期并存需统一

## Success Criteria

- [ ] state-scanner 检测 README.md 版本同步状态
- [ ] state-scanner 检测 standards 子模块挂载状态
- [ ] `.aria/config.json` 被 6 个 Skills 正确读取和尊重 (每个有 config-driven eval case)
- [ ] Agent Team 审计在 pre_merge 触发点成功执行
- [ ] 审计 defect-detection test 通过 (植入缺陷被检出)
- [ ] 实验功能可通过配置开关控制 (有/无 config 行为差异可验证)
- [ ] ab-suite 升版 v1.1.0, state-scanner AB 测试 delta 保持正值

## Out of Scope

- CLI 工具支持
- 配置文件 GUI 编辑器
- 跨项目配置继承
- CI/CD 集成
- YAML 格式支持 (统一使用 JSON)
