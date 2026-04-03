# state-scanner 项目级自定义健康检查

> **Level**: Minimal (Level 2 Spec)
> **Status**: In Progress
> **Created**: 2026-04-03
> **Parent Story**: [US-006](../../docs/requirements/user-stories/US-006.md)
> **Target Version**: v1.4.0
> **Source**: Forgejo Issue #4

## Why

state-scanner v2.7.0 只检查内置通用指标 (git status/OpenSpec/architecture/audit)，无法检测项目特有的健康指标。Aether 项目的 `OVERALL_BENCHMARK_SUMMARY.md` 两周未更新、累积 50+ 新 AB eval 未汇总，暴露了这个盲区。当前通过 PostToolUse hook 临时解决，但声明式配置是更优雅的长期方案。

## What

### 新增阶段 1.11: 项目级自定义检查

在阶段 1.10 (审计状态) 之后、阶段 2 (推荐决策) 之前，插入自定义健康检查阶段。

### 配置 Schema (`.aria/state-checks.yaml`)

```yaml
version: "1"                      # 必填，schema 版本
checks:
  - name: string                  # 必填，唯一标识
    description: string           # 必填，人类可读描述 (AI 用于解释)
    command: string               # 必填，shell 命令
    severity: info|warning|error  # 必填，影响推荐权重
    fix: string                   # 选填，修复命令提示 (不自动执行)
    timeout_seconds: integer      # 选填，默认 15，上限 60
    enabled: boolean              # 选填，默认 true
```

**退出码协议**: 0 = pass, 非 0 = fail。stdout 首行用于报告展示。

### 执行模型

- **串行执行**: 逐一运行，工作目录为项目根目录
- **超时**: 单检查默认 15s (上限 60s)，总超时 60s
- **容错**: 超时/命令不存在/格式错误均不阻塞主流程，降级为 warning 报告
- **安全**: 与 hooks.json 信任模型一致，不做沙箱。`fix` 命令仅展示，需用户显式触发

### Severity 联动推荐引擎

| severity | fail 时行为 |
|----------|------------|
| error | 新增 `custom_check_failed` 推荐规则，阻断推荐，强制修复提示 |
| warning | 降级推荐，附加 fix 提示 (类似 `audit_unconverged`) |
| info | 仅展示，不影响推荐 |

### 输出格式

```
🔧 自定义检查
───────────────────────────────────────────────────────────────
  ✅ db-migration-status: OK
  ⚠️ benchmark-summary-freshness: STALE (severity: warning)
     修复建议: python3 scripts/aggregate-results.py
  ✅ license-audit: OK
```

### 不做什么

- 不做命令沙箱 (破坏实用性)
- 不自动执行 fix 命令 (安全风险)
- 不并行执行检查 (简单优先，避免资源竞争)
- 不扩展 config-loader (职责边界清晰)
- 不支持结构化 JSON 输出 (v1 保持简单，未来可扩展)

## Decision Records

| ID | 决策 | 理由 |
|----|------|------|
| D1 | 插入点为阶段 1.11 | 不阻塞核心收集，结果供阶段 2 消费 |
| D2 | 配置独立于 config.json | 项目级扩展点 vs 插件级配置，职责不同 |
| D3 | 串行执行 + 超时 15s/60s | 简单优先，避免并行资源竞争 |
| D4 | fix 命令不自动执行 | 遵循 Phase 3 用户确认原则 |
| D5 | 失败不阻塞主流程 | state-scanner 是十步循环入口，中断代价高 |
| D6 | 不做沙箱 | 与 hooks.json 信任模型一致 |

## Scope

### 影响文件

| 文件 | 变更类型 |
|------|---------|
| `aria/skills/state-scanner/SKILL.md` | 新增阶段 1.11 定义 + 输出格式 |
| `aria/skills/state-scanner/RECOMMENDATION_RULES.md` | 新增 `custom_check_failed` 规则 |
| `aria/skills/state-scanner/references/output-formats.md` | 新增自定义检查输出区块 |
| `docs/architecture/system-architecture.md` | PATCH 级更新，标注扩展点 |

### 不影响

- workflow-runner、Phase Skills、audit-engine
- config-loader (配置独立加载)

## Estimation

- **工作量**: 4-6 小时
- **风险**: 低 (单模块，无跨模块依赖)
- **AB Benchmark**: 必须 (Rule #6, SKILL.md 变更)
