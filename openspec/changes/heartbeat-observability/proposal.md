# aria-orchestrator 心跳可观测性: 执行日志 + 扫描级熔断

> **Level**: Minimal (Level 2 Spec)
> **Status**: Approved
> **Created**: 2026-04-08
> **Parent Story**: [US-007](../../docs/requirements/user-stories/US-007.md)
> **Target Version**: v1.4.1
> **Parent Spec**: [aria-orchestrator](../aria-orchestrator/proposal.md)

## Why

v1.4.0 的心跳扫描已在 Aether light-1 上 24/7 运行 (Hermes cron, 60m 间隔, 飞书通知)。但存在两个可观测性盲区:

1. **无执行日志**: 心跳结果仅发往飞书，无本地持久化。无法回溯历史扫描、分析趋势、排查漏报
2. **无熔断机制**: scan.sh 或 notify-feishu.sh 连续失败时，cron 继续盲目重试，无告警

这两项原在 US-007 Phase 3b-M3 中定义，v1.4.0 时移至 Phase 3c。经评估，它们不依赖 AIAgent dispatch，可独立实现为扫描级别的可观测性增强。

### 范围边界

```
本 Spec 范围 (扫描级):              Phase 3c 范围 (dispatch 级):
──────────────────────              ──────────────────────────
✅ 记录每次心跳扫描结果              ❌ 记录 claude -p 执行过程
✅ scan/notify 失败计数 + 熔断       ❌ dispatch 失败计数 + 熔断
✅ 熔断时飞书告警                    ❌ AIAgent dispatch 执行
✅ 手动恢复 (.aria/heartbeat-breaker) ❌ 自动恢复 / 分级安全策略
```

## What

### 1. 执行日志

**修改文件**: `aria-orchestrator/heartbeat.sh`

在每次心跳执行后，追加日志到 `.aria/heartbeat-log/{YYYY-MM-DD}.log`:

```
[2026-04-08T18:30:00Z] mode=git total=3 L1=1 L2=1 L3=1 notify=ok
[2026-04-08T19:30:00Z] mode=git total=0 silent=true
[2026-04-08T20:30:00Z] mode=git total=2 L1=0 L2=2 L3=0 notify=fail err="feishu_timeout"
```

**字段说明**:

| 字段 | 说明 |
|------|------|
| 时间戳 | ISO 8601 UTC |
| mode | git 或 api (扫描模式) |
| total | 发现的 open issue 数量 |
| L1/L2/L3 | 各复杂度级别数量 |
| silent | total=0 时标记 |
| notify | ok / fail / skip (通知结果) |
| err | 失败原因 (仅 notify=fail 时) |

**实现要点**:
- `mkdir -p` 确保目录存在
- 追加模式 (`>>`)，非覆盖
- silent 模式 (0 issues) 也记录，确保完整审计轨迹
- scan.sh 失败时记录 `scan=fail`

### 2. 扫描级熔断

**修改文件**: `aria-orchestrator/heartbeat.sh`

**熔断检查 (heartbeat.sh 入口)**:
```bash
if [ -f "$PROJECT_DIR/.aria/heartbeat-breaker" ]; then
    # 记录日志并退出
    exit 0
fi
```

**失败计数**:
- 文件: `.aria/heartbeat-fail-count`
- 内容: 当前连续失败次数 (纯数字)
- scan.sh 或 notify-feishu.sh 非零退出 → 计数 +1
- 成功执行 → 重置为 0

**熔断触发 (连续 3 次失败)**:
1. 创建 `.aria/heartbeat-breaker` (内容: 触发时间 + 最近错误)
2. 调用 `notify-feishu.sh` 发送告警: "心跳熔断: 连续 3 次失败"
3. 后续 cron 触发时直接跳过

**手动恢复**:
```bash
rm .aria/heartbeat-breaker   # 删除熔断文件
rm .aria/heartbeat-fail-count # 重置计数
```

## Decision Records

| ID | 决策 | 理由 |
|----|------|------|
| D1 | 扫描级而非 dispatch 级 | dispatch 未实现，扫描级可独立交付价值 |
| D2 | 文件系统计数而非 Hermes memory | 简单、可调试、shell 原生，无 Hermes 依赖 |
| D3 | 单行 append 格式而非 Markdown | 机器可解析、grep 友好、磁盘开销小 |
| D4 | 熔断告警仍走飞书 | 复用现有通知通道，无需新增基础设施 |
| D5 | v1.4.1 patch 而非 v1.5.0 | 不改变系统行为，只增加可观测性和容错 |

## Acceptance Criteria

- [ ] 每次心跳执行后，`.aria/heartbeat-log/{date}.log` 有对应日志行
- [ ] silent 模式 (0 issues) 也有日志记录
- [ ] scan.sh 失败时日志记录 `scan=fail`
- [ ] notify-feishu.sh 失败时日志记录 `notify=fail`
- [ ] 连续 3 次失败后创建 `.aria/heartbeat-breaker`
- [ ] 熔断时飞书收到告警消息
- [ ] 熔断后 cron 触发直接跳过 (日志记录 `breaker=tripped`)
- [ ] 删除 `.aria/heartbeat-breaker` 后恢复正常执行
- [ ] 成功执行重置失败计数
