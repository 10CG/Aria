# Spike: context/token 机读可行性 (Aria #104 + aria-plugin #18)

> **日期**: 2026-05-29 | **类型**: spike-first 数据验证 (feedback_spike_first_for_data_hypotheses)
> **触发**: owner 选择 spike-first 验证 `/context` 可机读性, 再决定 #104/#18 scope

## 问题

两个 issue 都假设能拿到 Claude Code 的实时 context/token 信号:
- **#104** aria-context-monitor — 提议路径 A: skill 内 Bash 调 `/context` slash command
- **#18** ai-native-estimator — Token 轴需要 per-turn token usage

## Spike 结果

| # | 验证项 | 结果 |
|---|--------|------|
| 1 | `/context` 是否 shell-invocable binary | ❌ **NO** — `which context` 空; `/context` 是 Claude Code TUI slash command, 由 harness 解释, **不经过 shell**。#104 路径 A **字面不可行** |
| 2 | context/token env var | ❌ 无 |
| 3 | transcript JSONL `usage` block 可机读 | ✅ **YES** — `~/.claude/projects/{cwd-slug}/{session}.jsonl` 每个 assistant turn 含 `usage: {input_tokens, cache_creation_input_tokens, cache_read_input_tokens, output_tokens, ...}` |
| 4 | model/window 可从 transcript 推导 | ⚠️ **部分** — `message.model` = `claude-opus-4-8` (缺 `[1m]` 后缀); window 大小**不能**可靠从 model 字段推 (实测 628K 占用证明是 1M window, 但字段无 1m 标记) |
| 5 | transcript 路径确定性 | ✅ `ls -t ~/.claude/projects/$(pwd│sed 's#/#-#g')/*.jsonl │ head -1` = 当前 session |
| 6 | 新鲜度 | ✅ last-turn usage 距 EOF 仅 2 行 (1 turn stale, pause/continue 决策可接受) |

## 关键洞察

**可行路径 = A' (读 transcript JSONL), 非 #104 原提的路径 A (调 /context)**:

```
context occupancy proxy = last_assistant_turn.usage.(input_tokens
                          + cache_read_input_tokens
                          + cache_creation_input_tokens)
实测本 session: 628,248 tokens ≈ 62.8% of 1M window
```

**遗留 blocker**: window 大小无可靠来源 (model 字段不带 1m 标记)。需:
- (a) `.aria/config.json` 显式配 `context_monitor.window_tokens`, 或
- (b) 经验最大值推断 (observed peak input_tokens × safety factor), 或
- (c) 向 Anthropic feature-request `getContextUsage()` API (#104 路径 B, 一劳永逸)

**#104 ↔ #18 共享数据源确认**: transcript `usage` block 同时喂养 context-monitor (实时占用) 和 estimator Token 轴 (per-task 累加)。**单一 collector 可服务两者** — 支持合并为一个底层 skill/collector (e.g. `aria-token-telemetry`) + 两个消费面。

## 建议 scope (spike 后修正)

1. **#104 改 Path A'**: skill `aria-context-monitor` 读 transcript JSONL last-turn usage (非调 /context); window 大小走 config + 经验 fallback; 不阻塞地向 Anthropic file 路径 B feature request
2. **#18 复用同 collector**: estimator Token 轴消费同一 `usage` 解析逻辑
3. **共享底层**: 提取 `lib/token_telemetry.py` (parse transcript usage) 供两 skill 复用 — 避免 #57 式 sandbox 数据层重复 bug

## ⚡ UPDATE (2026-05-29, brainstorm 中突破) — statusLine stdin 是金矿

前述"window 大小无可靠来源"的 blocker **完全消失**。Claude Code runtime 每次渲染 statusLine 时,
pipe 一个**远比想象丰富**的 JSON 到 statusLine command 的 stdin。实测 capture (临时给
`~/.claude/statusline-command.sh` 加 1 行抓取, 已还原):

```json
{
  "model": {
    "id": "claude-opus-4-8[1m]",              // 完整 ID 带 [1m]! (transcript 丢的后缀这里有)
    "display_name": "Opus 4.8 (1M context)"   // display_name 也带 1M 标记
  },
  "context_window": {
    "context_window_size": 1000000,           // 🔑 window 大小直接给 — 零推断
    "used_percentage": 67,                     // 🔑 runtime 算好的 %
    "remaining_percentage": 33,
    "total_input_tokens": 673955, "total_output_tokens": 615,
    "current_usage": { input/output/cache_creation/cache_read }
  },
  "exceeds_200k_tokens": <bool>, "fast_mode": <...>,
  "transcript_path": "<...>",                  // transcript 路径直接给
  "session_id", "cost", "rate_limits", "workspace", "version", ...
}
```

### 推翻的假设链 (spike 全程 4 次)
1. ❌ path A (skill 调 /context) — 非 shell binary
2. ⚠️ path A' (transcript usage) — 可行但缺 window → 需推断
3. ❌ model→window 查表 (transcript) — model 字段丢 [1m] 且 4-7/4-8 跳变
4. ✅ **statusLine stdin** — size + % + model.id(带[1m]) 全有, 零推断

### 修正架构 = 纯【中继】
statusLine 加 1 行 → 写 `.aria/cache/context-window.json` → skill 读。window 推断
(config/peak/path-d) **全部作废** (主路径)。

### 可移植性 (回答 "依赖 DIY 配置吗")
- 数据 schema = **通用** CC 特性 (任何 statusLine command 都收到此 stdin)
- relay 抓取 = 依赖 statusLine 配置 + relay 行 → 需 3 档 fallback + setup helper (类 secret-guard)

完整决策: `.aria/decisions/2026-05-29-context-monitor-architecture.md` (DEC-20260529-001)

## Cross-ref
- feedback_spike_first_for_data_hypotheses (本 spike 避免写无用 Spec + 连续推翻 4 假设)
- #57 教训 (数据层 prerequisite 要先验证, 否则上层 feature 0 价值)
- DEC-20260529-001 (架构决策)
