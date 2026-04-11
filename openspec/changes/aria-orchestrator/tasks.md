# aria-orchestrator M3-slim — Task Plan

> **Scope**: Phase 3b-M3-slim (v1.5.0)
> **Parent Spec**: [proposal.md](./proposal.md) (D23: M3 拆分)
> **Audit**: 4 轮 Agent Team 收敛 (2026-04-11, post_planning-2026-04-11T0530Z)
> **Estimate**: ~4h

## Tasks

### Task 0: notify-feishu.sh JSON 转义修复 [P0, 前置]

**现有 bug**: `$MESSAGE` 直接插入 JSON 字符串 (line 33), issue 标题含双引号/换行时 payload 损坏。

**实现**:
- 用 python3 构造完整 JSON payload, 替代 bash `$MESSAGE` 字符串插值
- notify 失败时 `exit 1` (当前隐式 exit 0, Hermes cron 无法检测)

**验收**: 含换行和双引号的消息能正常发送到飞书

---

### Task 1: triage.sh — 路由决策引擎 [核心]

**输入**: `heartbeat-scan.json`
- 消费字段契约: `issues[].complexity_tier`, `issues[].title`, `issues[].source`, `issues[].number` (api) / `issues[].file` (git)

**输出**: `triage-result.json`
```json
{
  "schema_version": "1",
  "triage_timestamp": "2026-04-11T06:00:00Z",
  "source_scan_hash": "<sha256 of heartbeat-scan.json>",
  "summary": {
    "total": 5,
    "by_action": {
      "dispatch_ready": 2,
      "approval_required": 2,
      "human_only": 1
    }
  },
  "decisions": [
    {
      "issue_ref": "api#42",
      "tier": 1,
      "action": "dispatch_ready",
      "reason": "Tier 1, auto-dispatch enabled"
    }
  ]
}
```

**issue_ref 格式**: `api#<number>` (Forgejo API) / `git:<filename>` (Git native)

**配置**: `.aria/config.json` → `orchestrator.dispatch_policy`
```json
{
  "orchestrator": {
    "dispatch_policy": {
      "tier1_action": "dispatch_ready",
      "tier2_action": "approval_required",
      "tier3_action": "human_only",
      "dry_run": false
    }
  }
}
```

**边界处理**:
- 0 issues → 空 `decisions[]`, summary 全 0
- 100+ issues → 正常处理 (截断在通知层, 非 triage 层)
- 配置缺失 → 使用默认策略 (tier1=dispatch_ready, tier2=approval_required, tier3=human_only)

**冒烟测试**: `test-fixtures/` 含 3 个样本 JSON (tier 1/2/3 各一)

**验收**: 3 种 fixture 输入均产出结构正确的 triage JSON

---

### Task 2: heartbeat.sh 集成 triage [集成]

**流程变更**:
```
旧: scan → [total=0? SILENT] → build message → notify → log
新: scan → [total=0? SILENT] → triage → 分级通知 → log
```

**Fallback**: `triage.sh` 失败时:
- 降级为原始通知格式 (当前行为)
- **不向 `heartbeat-fail-count` 写入**, breaker 计数不变
- 日志记录 `triage=fallback`

**兼容性约束**:
- 不新增必需 env 变量或 CLI 参数
- 现有 Nomad job spec 不改动即可运行

**验收**: triage 失败时 heartbeat 降级通知, breaker 计数不变

---

### Task 3: notify-feishu.sh 分级通知 [通知]

**消息类型**: 纯文本 (Interactive Card 留 v2.0 S7_HUMAN_GATE)

**分级格式**:
```
🟢 [Tier 1] Quick fix — v2.0 可自动派发
   #42 fix: typo in README → dispatch_ready

🟡 [Tier 2] 需 Spec + 审批
   #38 feat: add user export → approval_required

🔴 [Tier 3] 架构/安全 — 需人工处理
   #35 security: SQL injection risk → human_only
```

**截断**: 超过 10 条 issue 只显示前 10 + "...及 N 条更多"

**验收**: 飞书收到的通知按 tier 有可区分的格式差异

---

### Task 4: 文档更新 [收尾, 依赖 Task 0-3]

**4a. aria-orchestrator/README.md**:
- Roadmap: M2 → done, M3-slim → done
- v2.0 条目标注 "dispatch-development (v2.0 pending)"

**4b. Spec Decision Records**:
- 追加 D23: M3 拆分决策 (已完成)

**4c. Spec Estimation 表**:
- M3-slim 行标注 ✅ v1.5.0 (已完成)
- M3 剩余 + Phase 3c → v2.0

**验收**: Spec + README 已更新

---

## Acceptance Criteria (总验收)

1. `triage.sh` 接受 3 种 fixture 输入, 输出结构正确的 triage JSON
2. triage 失败时 heartbeat 降级为原始通知, 不向 `heartbeat-fail-count` 写入, breaker 计数不变
3. 飞书收到的通知按 tier 有可区分的格式差异
4. 现有 Nomad job 未改动, dry-run heartbeat 无报错
5. Spec + README 已更新
6. 新脚本 (`triage.sh`) 在 Nomad job volume 路径内

## Deferred (不在 v1.5.0 范围)

- `scan.sh` schema_version (v2.0 M6)
- 飞书 Interactive Card (v2.0 S7_HUMAN_GATE)
- dispatch.sh / 状态机 / 审批轮询 (v2.0 M1-M2)
