# aria-orchestrator — 外部编排器与自动开发闭环

> **Level**: Full (Level 3 Spec)
> **Status**: In Progress
> **Created**: 2026-04-03
> **Parent Story**: [US-007](../../docs/requirements/user-stories/US-007.md)
> **Target Version**: v1.4.0 (Phase 3b ✅), v2.0.0 (Phase 3c)

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

### Phase 3b-M1.5: Hermes 技术验证 (spike) ✅ PASS (2026-04-03)

> 验证 Hermes Agent 是否满足 aria-orchestrator 的基础设施需求。
> **结果: GO — 全部 5 项验证通过，无阻塞性问题。**

**验证结果**:

| 项目 | 通过标准 | 结果 | 关键代码 |
|------|---------|------|---------|
| cron scheduler | 定时执行 + 隔离 session | ✅ PASS | `cron/scheduler.py:540-626` — 文件锁隔离, cron/interval/一次性, 超时 600s |
| terminal tool | 执行 `claude -p` + 捕获输出 | ✅ PASS | `tools/terminal_tool.py:900+` — 任意命令, stdout/stderr, 6 种后端 |
| 消息网关 | 发送审批 + 接收回复 | ✅ PASS* | `gateway/config.py:48-65` — 16+ 平台, *cron 不能同步等待回复 (轮询解决) |
| 工具裁剪 | 最小权限 | ✅ PASS | `toolsets.py` — `disabled_toolsets` + `create_custom_toolset()` |
| 扩展点 | 自定义 Tool/Skill | ✅ PASS | `tools/registry.py` + `skills.external_dirs` 外部 SKILL.md 加载 |

**关键发现**:
- Hermes `skills.external_dirs` 支持加载外部 SKILL.md → Aria Skills 可能直接映射
- cron job 一次性执行模型 → 人类审批需轮询模式 (发通知 → 下次 tick 检查回复)
- 回退条件未触发，FastAPI+SQLite 方案作为备用保留

### Phase 3b-M2: 轻节点 E2E 验证 ✅ PASS (2026-04-07)

> 在 Aether light-1 节点 (1 core / 1 GB RAM) 实际部署并完成端到端验证。

**部署环境**:

| 项 | 值 |
|----|------|
| 节点 | light-1 (192.168.69.90), exec driver, 1C/1G |
| Hermes | v0.7.0, /opt/aria-orchestrator/venv/ (140MB) |
| LLM | GLM-4.7-Flash (智谱 zai provider, **免费**) |
| Config | ~/.hermes/config.yaml (非 cli-config.yaml!) |
| Skills | ~/.hermes/skills/ (external_dirs 在 cron 中不生效) |

**E2E 验证链**:

```
hermes cron create → cron run → cron tick
  → Hermes AIAgent (GLM-4.7-Flash)
    → 理解 heartbeat-scan Skill
    → terminal tool: ./scan.sh /tmp/test-project --json
    → read_file: .aria/heartbeat-scan.json
    → 格式化报告输出
    → 检查 auto_develop 配置
  → cron output 写入 ~/.hermes/cron/output/{job-id}/
```

**关键修复 (部署经验)**:
1. cron scheduler 读 `config.yaml`，不是 `cli-config.yaml`
2. Skills 需放 `~/.hermes/skills/` 子目录，cron 中 external_dirs 不生效
3. `GLM_API_KEY` 需写入 `~/.hermes/.env`
4. zai provider 需要 config.yaml 中 `model.default` 字段，否则 model code 为空

**资源实测**:
- 磁盘: 140MB venv + ~1KB/job 输出
- 内存: 轻节点 1GB 足够 (Hermes ~100MB)
- API 成本: **零** (GLM-4.7-Flash 免费)

### Phase 3b-M3: 完整 Hermes 集成 + 定时心跳 (v1.5.0)

**在 E2E 验证基础上增量添加**:

| 组件 | 实现方式 |
|------|---------|
| 定时扫描 | Hermes cron job → terminal tool → scan.sh --json |
| Triage | Hermes cron job → 规则引擎 (确定性, LLM 禁用) |
| 人类审批 | Hermes gateway → Telegram/Slack 通知 |
| 开发执行 | Hermes AIAgent (GLM-4.7-Flash 调度) → terminal → claude -p (Opus) |
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
| D13 | GLM-4.7-Flash 免费模型 (zai provider) | 零 API 成本, 工具调用能力足够 triage |
| D14 | 轻节点 (1C/1G) 足够运行 Hermes | 实测 140MB venv, ~100MB 运行时 |
| D15 | config.yaml (非 cli-config.yaml) 为 cron 配置源 | 部署经验, scheduler.py:349 |
| D16 | Skills 放 ~/.hermes/skills/ (非 external_dirs) | cron 中 external_dirs 不生效 |
| D17 | 飞书必须配 ENCRYPT_KEY + VERIFICATION_TOKEN | 无此配置时事件不推送 (2026-04-08 踩坑) |
| D18 | 飞书必须配 FEISHU_HOME_CHANNEL | cron deliver 需要目标 chat_id |
| D19 | GATEWAY_ALLOW_ALL_USERS=true | Hermes 默认拒绝所有用户 |
| D20 | 所有 env 必须在 Nomad env 块 | dotenv 不被子进程继承 (Hermes 限制) |
| D21 | 飞书应用可用范围不能为空 | 可见范围为空 → WebSocket 连接成功但零事件 |
| D22 | 避免频繁重连飞书 WebSocket | 短时间大量重连会被飞书临时限流 |
| D5 | git worktree 隔离执行 | 不接触主工作目录，最低安全要求 |
| D6 | C.2 合并永远人类审批 | PR 是安全最后防线，不自动合并 |
| D7 | Forgejo webhook + cron 双触发 | webhook 实时，cron 兜底 |
| D8 | 白名单标签 aria:auto | 仅标记的 issue 进入自动流程 |
| D9 | 熔断: 连续 3 次失败暂停 | 防止失控循环消耗资源 |
| D10 | Dashboard 不迁移 | 生成是工具层职责，调度是运行时层职责 |
| D11 | heartbeat scan 直接做编排器，跳过 Skill | 扫描是确定性逻辑，双重实现浪费 |
| D12 | Phase 3a+3b 合并，编排器第一个 PR = scan-only | 代码从第一天在正确仓库，增量演进 |
| D23 | M3 拆分为 M3-slim (v1.5.0) + 剩余留 v2.0 | M3 中 dispatch/状态机/审批 60% 会被 v2.0 容器架构替代,仅 triage+通知 (40%) 可复用。Agent Team 4 轮审计收敛 (2026-04-11) |

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
| Phase 3b-M1 (scan-only) | 4-6h | ✅ 已完成 (2026-04-03) |
| Phase 3b-M1.5 (Hermes spike) | 4-6h | ✅ PASS (2026-04-03) |
| Phase 3b-M2 (轻节点 E2E) | 4-6h | ✅ PASS (2026-04-07) |
| Phase 3b-M3-slim (triage+通知) | ~4h | ✅ v1.5.0 交付 (D23: dispatch/状态机/审批 → v2.0) |
| Phase 3b-M3 剩余 (状态机+dispatch+审批) | — | → v2.0 (PRD v2.0 US-010~017) |
| Phase 3c (闭环) | 20h+ | → v2.0 |
