# Aria Hooks 系统

> **版本**: 1.0.0
> **用途**: 在关键节点自动执行验证和检查

---

## 概述

Hooks 系统允许在开发工作流的关键节点自动执行脚本，确保代码质量和规范合规性。

## 可用的 Hook 点

| Hook 点 | 触发时机 | 阻塞 | 状态 |
|---------|----------|------|------|
| `session-start` | Claude Code 会话开始 | 否 | ✅ 启用 |
| `pre-commit` | Git 提交前 | 是 | ⏳️ 计划中 |
| `task-complete` | 任务完成时 | 否 | ⏳️ 计划中 |

## 目录结构

```
aria/hooks/
├── hooks.json           # Hook 配置文件
├── session-start.sh     # 会话初始化脚本 (Linux/Mac)
├── session-start.cmd    # 会话初始化脚本 (Windows)
├── run-hook.cmd         # Hook 运行器 (Windows)
├── validators/
│   ├── spec-compliance.py    # 规范合规性验证
│   └── code-quality.py       # 代码质量验证
└── README.md            # 本文件
```

## 配置说明

### hooks.json

```json
{
  "enabled": true,
  "hooks": {
    "session-start": {
      "enabled": true,
      "script": "session-start.sh",
      "blocking": false
    }
  }
}
```

| 字段 | 说明 |
|------|------|
| `enabled` | 全局开关 |
| `hooks.{name}.enabled` | 单个 hook 开关 |
| `hooks.{name}.blocking` | 是否阻塞后续操作 |
| `hooks.{name}.timeout` | 超时时间（秒） |

## 禁用 Hooks

### 临时禁用

```bash
# 环境变量
export ARIA_HOOKS_ENABLED=false

# 或禁用特定 hook
export ARIA_HOOK_SESSION_START=false
```

### 永久禁用

编辑 `hooks.json`:
```json
{
  "enabled": false
}
```

或重命名目录:
```bash
mv aria/hooks aria/hooks.bak
```

## 开发新 Hook

1. 在 `aria/hooks/` 创建脚本文件
2. 在 `hooks.json` 中添加配置
3. 测试: `./run-hook.cmd session-start`

## 相关文档

- [Aria Workflow Enhancement](../../../standards/openspec/changes/aria-workflow-enhancement/proposal.md)
- [十步循环](../../../standards/core/ten-step-cycle/README.md)

---

**版本**: 1.0.0
**创建**: 2026-01-18
