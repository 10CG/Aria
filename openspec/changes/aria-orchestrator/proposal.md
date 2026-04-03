# aria-orchestrator — 外部编排器与自动开发闭环

> **Level**: Full (Level 3 Spec)
> **Status**: Draft
> **Created**: 2026-04-03
> **Parent Story**: [US-007](../../docs/requirements/user-stories/US-007.md)
> **Target Version**: v1.5.0 (Phase 3b), v2.0.0 (Phase 3c)

## Why

Aria 方法论的十步循环目前完全依赖人类在 Claude Code 内交互式执行。US-005 Phase 2 实现了 Issue 提交能力 (.aria/issues/)，但 Issue 创建后仍需人类手动启动开发流程。

经 Agent Team 六轮讨论 (2026-04-03)，确认核心矛盾和技术路径:

```
心跳/编排需要的:              Claude Code 提供的:       Hermes Agent 提供的:
─────────────────              ─────────────────         ─────────────────
持久化状态机                    无状态单次会话            ✅ FTS5 memory
长时间运行 (daemon)             交互式 session           ✅ 持久进程
队列 + 重试 + 熔断              无内置容错               ✅ run_agent 内置
外部事件触发 (webhook)          人类输入触发             ✅ 消息网关
定时调度                        /schedule (受限)         ✅ cron scheduler
人类审批通道                    无                       ✅ Telegram/Slack
隔离执行                        无                       ✅ Docker/SSH backend
```

**结论**: 基于 Hermes Agent (NousResearch) 作为运行时底座，通过 `claude -p` 调用 Claude Code 执行 Aria Skills。Aria 扩展 Hermes，方法论独立于具体运行时。

## What

### 系统架构

```
┌─────────────────────────────────────────────────┐
│              Forgejo                             │
│  issue.created ──────┐  PR merge ◀──────────┐  │
└──────────────────────┼───────────────────────┼──┘
                       │                       │
                       ▼                       │
┌──────────────────────────────────────────────────┐
│  aria-orchestrator (基于 Hermes Agent)            │
│  部署: Aether Nomad service job (Docker)          │
│                                                   │
│  ┌─ Hermes cron layer (确定性, LLM 禁用) ─────┐  │
│  │  scan_job:   terminal → scan.sh --json      │  │
│  │  triage_job: 规则引擎 → Level 判定          │  │
│  │  notify_job: gateway → Telegram/Slack 审批  │  │
│  └──────────────────┬──────────────────────────┘  │
│                     │ human approves               │
│                     ▼                              │
│  ┌─ Hermes AIAgent (LLM 启用, 按需) ──────────┐  │
│  │  model: Haiku/Sonnet (调度决策, 低成本)     │  │
│  │  terminal tool → claude -p (Opus)            │  │
│  │  backend: Docker / local (git worktree)      │  │
│  └──────────────────┬──────────────────────────┘  │
│                     │                              │
│  ┌─ Safety Layer ───┼──────────────────────────┐  │
│  │  白名单 (aria:auto) │ token 预算            │  │
│  │  熔断 (3x fail)     │ 执行超时 (10min)      │  │
│  │  并发锁 (max=1)     │ 接口适配层 (退出策略) │  │
│  └──────────────────────────────────────────────┘  │
└──────────────────────┬─────────────────────────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ claude -p "..."  │
              │ (git worktree)   │
              │                  │
              │ 自动加载:        │
              │ - CLAUDE.md      │
              │ - 33 Aria Skills │
              │ - 11 Agents      │
              │ - Hooks          │
              └──────────────────┘
```

### Phase 3b-M1: scan-only 模式 (v1.4.0, 4-6h)

**独立项目**: `aria-orchestrator` (GitHub/Forgejo 新仓库)

**第一个 PR — 最小切片**:

```
aria-orchestrator/
├── scan.sh          # 确定性 issue 扫描 (glob + frontmatter 解析)
├── analyze.sh       # 确定性复杂度分析 (规则匹配)
├── report.sh        # 人类可读报告生成
├── schema/
│   └── scan-result.json  # 输出 schema (为 AI 层和看板预留)
└── README.md
```

**设计原则**: 可确定的不用 AI，省下 tokens 给真正需要推理的环节。

- 手动触发 `./scan.sh`，无 cron/SQLite/状态机
- 纯 shell + forgejo CLI，零 AI token 消耗
- 输出格式与未来 AI 增强层 (claude -p) 对齐

### Phase 3b-M1.5: Hermes 技术验证 (spike, 4-6h)

> 验证 Hermes Agent 是否满足 aria-orchestrator 的基础设施需求。
> 验证失败则回退到 FastAPI+SQLite 自建方案 (~400 行 Python)。

**验证项**:

| 项目 | 验证内容 | 通过标准 |
|------|---------|---------|
| cron scheduler | tick()/60s, 隔离 session | 能定时执行 scan.sh 并捕获 JSON 输出 |
| terminal tool | 执行 `claude -p` | 能传入 prompt, 捕获 stdout, 设超时 |
| 消息网关 | Telegram/Slack | 能发送审批请求, 接收用户回复 |
| 工具裁剪 | 禁用不需要的工具 | 仅保留 terminal + shell, 攻击面可控 |
| 扩展点 | 自定义 Tool/Skill 注入 | 能注入 Aria 十步循环调度逻辑 |

### Phase 3b-M2: Hermes 集成 + 定时心跳 (v1.5.0, 12-16h)

**基于 Hermes Agent 重构 aria-orchestrator**:

| 组件 | 实现方式 |
|------|---------|
| 定时扫描 | Hermes cron job → terminal tool → scan.sh --json |
| Triage | Hermes cron job → 规则引擎 (确定性, LLM 禁用) |
| 人类审批 | Hermes gateway → Telegram/Slack 通知 |
| 开发执行 | Hermes AIAgent (Haiku) → terminal → claude -p (Opus) |
| 状态持久化 | Hermes FTS5 memory |
| Webhook | Hermes gateway 或独立端点 |
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
| D4 | 基于 Hermes Agent 构建 (4:1) | 覆盖 80% 基础设施 (cron/gateway/memory/隔离), 省 60% 自研 |
| D4a | 模式 A: Hermes 调度 + claude -p 执行 | 双层各司其职, Haiku 调度 + Opus 开发, Skill 零重写 |
| D4b | 生态关系: Aria 扩展 Hermes | 方法论独立于运行时 = 研究成果, 可替换底座 |
| D4c | 接口适配层隔离 Hermes API | 退出策略: Hermes 停维时可迁移 |
| D4d | 回退方案: FastAPI+SQLite | 若 Hermes spike 失败, ~400 行 Python 自建 |
| D5 | git worktree 隔离执行 | 不接触主工作目录，最低安全要求 |
| D6 | C.2 合并永远人类审批 | PR 是安全最后防线，不自动合并 |
| D7 | Forgejo webhook + cron 双触发 | webhook 实时，cron 兜底 |
| D8 | 白名单标签 aria:auto | 仅标记的 issue 进入自动流程 |
| D9 | 熔断: 连续 3 次失败暂停 | 防止失控循环消耗资源 |
| D10 | Dashboard 不迁移 | 生成是工具层职责，调度是运行时层职责 |
| D11 | heartbeat scan 直接做编排器，跳过 Skill | 扫描是确定性逻辑，双重实现浪费 |
| D12 | Phase 3a+3b 合并，编排器第一个 PR = scan-only | 代码从第一天在正确仓库，增量演进 |

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
| Phase 3b-M1 (scan-only) | 4-6h | 低 (确定性脚本) ✅ 已完成 |
| Phase 3b-M1.5 (Hermes spike) | 4-6h | 中 (外部依赖验证) |
| Phase 3b-M2 (Hermes 集成) | 12-16h | 中 (Hermes 集成) |
| Phase 3c (闭环) | 20h+ | 高 (全自动开发安全性) |
