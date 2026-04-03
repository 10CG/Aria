# aria-orchestrator — 外部编排器与自动开发闭环

> **Level**: Full (Level 3 Spec)
> **Status**: Draft
> **Created**: 2026-04-03
> **Parent Story**: [US-007](../../docs/requirements/user-stories/US-007.md)
> **Target Version**: v1.5.0 (Phase 3b), v2.0.0 (Phase 3c)

## Why

Aria 方法论的十步循环目前完全依赖人类在 Claude Code 内交互式执行。US-005 Phase 2 实现了 Issue 提交能力 (.aria/issues/)，但 Issue 创建后仍需人类手动启动开发流程。

经 Agent Team 三轮讨论 (2026-04-03)，确认核心矛盾:

```
心跳/编排需要的:              Claude Code 提供的:
─────────────────              ─────────────────
持久化状态机                    无状态单次会话
长时间运行 (daemon)             交互式 session
队列 + 重试 + 熔断              无内置容错
外部事件触发 (webhook)          人类输入触发
```

**结论**: 编排逻辑应在 Claude Code 外的独立进程中，通过 `claude -p` 调用 Claude Code 作为执行器。

## What

### 系统架构

```
┌─────────────────────────────────────────────┐
│            Forgejo                           │
│  issue.created webhook ──────┐              │
│  PR review / merge ◀────────┤              │
└──────────────────────────────┼──────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────┐
│  aria-orchestrator (Aether Nomad service)    │
│                                              │
│  ┌──────────┐  ┌─────────────────────────┐  │
│  │ Webhook  │→ │ State Machine (SQLite)   │  │
│  │ Receiver │  │ queued → analyzing       │  │
│  │ (HMAC)   │  │ → developing → pr_created│  │
│  └──────────┘  │ → resolved / failed      │  │
│                └────────────┬────────────┘  │
│  ┌──────────┐               │               │
│  │ Cron     │→──────────────┘               │
│  │ Fallback │                               │
│  └──────────┘  ┌────────────────────────┐   │
│                │ Safety Layer            │   │
│                │ - 白名单标签 (aria:auto)│   │
│                │ - token 预算            │   │
│                │ - 熔断 (3x fail → stop) │   │
│                │ - 执行超时 (10min)      │   │
│                │ - 并发锁 (max=1)        │   │
│                └────────────────────────┘   │
│                         │                    │
│                         ▼                    │
│               ┌──────────────────┐           │
│               │ claude -p "..."  │           │
│               │ (git worktree)   │           │
│               │                  │           │
│               │ 自动加载:        │           │
│               │ - CLAUDE.md      │           │
│               │ - 33 Skills      │           │
│               │ - 11 Agents      │           │
│               │ - Hooks          │           │
│               └──────────────────┘           │
└──────────────────────────────────────────────┘
```

### Phase 3b: 编排器 MVP (v1.5.0, 16-20h)

**独立项目**: `aria-orchestrator` (GitHub/Forgejo 新仓库)

**核心组件**:

| 组件 | 职责 |
|------|------|
| Webhook Receiver | 接收 Forgejo issue 事件, HMAC-SHA256 签名验证, 幂等去重 |
| State Machine | Issue 生命周期管理, SQLite 持久化 |
| Step Scheduler | cron 兜底扫描 + webhook 实时触发 |
| Executor | `claude -p` subprocess, worktree 隔离, 超时控制 |
| Safety Layer | 白名单/熔断/预算/并发锁 |
| Log Writer | .aria/heartbeat-log/{date}.md 审计日志 |

**Issue 状态机**:

```
open → queued → analyzing → [Level 判定]
                              ├─ Level 1 → executing → pr_created → resolved
                              ├─ Level 2 → spec_pending (等人类确认) → executing → ...
                              └─ Level 3 → report_only (仅生成分析报告)
失败路径: any → failed → needs_human_review
```

**执行模型**:

```bash
# 编排器调用 claude -p (在 git worktree 中)
git worktree add /tmp/aria-work-{issue-id} -b auto/{issue-id}
cd /tmp/aria-work-{issue-id}

claude -p "$(cat <<EOF
处理 Issue: {issue-title}
内容: {issue-description}
复杂度: Level {N}

按十步循环执行:
1. 创建 OpenSpec (Level 2+)
2. 规划任务
3. 开发 + 测试
4. 提交到当前分支
不要合并到 master，创建 PR 即可。
EOF
)" --allowedTools Bash,Read,Write,Glob,Grep \
   --timeout 600000

git worktree remove /tmp/aria-work-{issue-id}
```

### Phase 3c: 半自动开发闭环 (v2.0.0, 20h+)

**在 Phase 3b 基础上增加**:

| 能力 | 说明 |
|------|------|
| 人类确认门控 | Forgejo comment `/approve` → 编排器继续 |
| Dashboard 集成 | 心跳后自动 `claude -p "/aria:dashboard"` 刷新 |
| 多 issue 队列 | FIFO 排序, 可配置优先级 |
| 成本监控 | 每 issue token 消耗记录, 日预算上限 |
| 看板进度回显 | Issue 处理进度在看板实时展示 |

### 不做什么

- 不重写 Dashboard 生成逻辑 (Skill 作为生成器不变)
- 不重写 5 个数据解析器 (Phase 3b/3c 阶段保持 AI 解析)
- 不做通用 CI/CD (仅编排十步循环)
- 不做多项目支持 (v2.0.0 以后考虑)

## Decision Records

| ID | 决策 | 理由 |
|----|------|------|
| D1 | 外部编排器 (非 Claude Code 内) | daemon 需求 vs 会话模型不匹配 |
| D2 | `claude -p` 复用 Skill 生态 | 33 Skills 零重写，Agent SDK 需全部重写 |
| D3 | 独立项目 aria-orchestrator | 不污染方法论层，submodule 接入 |
| D4 | SQLite 状态存储 | 轻量、单文件、进程重启可恢复 |
| D5 | git worktree 隔离执行 | 不接触主工作目录，最低安全要求 |
| D6 | C.2 合并永远人类审批 | PR 是安全最后防线，不自动合并 |
| D7 | Forgejo webhook + cron 双触发 | webhook 实时，cron 兜底 |
| D8 | 白名单标签 aria:auto | 仅标记的 issue 进入自动流程 |
| D9 | 熔断: 连续 3 次失败暂停 | 防止失控循环消耗资源 |
| D10 | Dashboard 不迁移 | 生成是工具层职责，调度是运行时层职责 |

## Impact

| Type | Description |
|------|-------------|
| **Positive** | Issue→PR 半自动闭环，大幅减少人工干预 |
| **Positive** | 编排器本身是 Aria 方法论可重现性的验证案例 |
| **Positive** | 三层架构明确化，方法论/工具/运行时职责清晰 |
| **Risk** | 编排器膨胀为"又一个 CI 系统"，需严格限定职责 |
| **Risk** | `claude -p` 执行的不确定性需要充分的错误恢复 |
| **Architecture** | Aria 从"方法论+工具"演进为"方法论+工具+运行时"，需更新 CLAUDE.md |

## Dependencies

- Aether 集群 (Nomad/Consul) — 部署环境
- Forgejo webhook 能力 — 事件触发
- Claude Code `claude -p` — 执行引擎
- US-005 Phase 1-2 — Dashboard + Issue 存储
- US-005 Phase 3a — heartbeat scan Skill (验证复杂度分析)

## Estimation

| Phase | 工作量 | 风险 |
|-------|--------|------|
| Phase 3b (MVP) | 16-20h | 中 (新项目架构) |
| Phase 3c (闭环) | 20h+ | 高 (全自动开发安全性) |
