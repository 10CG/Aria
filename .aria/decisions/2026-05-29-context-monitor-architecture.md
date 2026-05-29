# 决策: DEC-20260529-001 — aria-context-monitor 架构 (#104 + #18 关系)

> **日期**: 2026-05-29 | **模式**: technical brainstorm
> **关联**: Forgejo Aria #104 (context-monitor) + aria-plugin #18 (ai-native-estimator)
> **前置**: spike `.aria/notes/2026-05-29-context-monitor-spike.md`

## 背景

两个 issue 都需要 Claude Code 的 context/token 信号:
- #104 aria-context-monitor: 实时 context 占用 → AI 决定"推进 vs 暂停" (实证: 22% 偏差误触发提前暂停)
- #18 ai-native-estimator: per-task token 工作量估算 (替代 4-8h 工时假设, 影响 6 个 skill)

Spike 先验证数据可机读性, 过程中连续推翻多个假设, 最终发现 statusLine stdin 直接提供全部所需数据。

## 约束条件

| 类型 | 约束 | 影响 |
|------|------|------|
| 数据来源 | `/context` slash command 非 shell-invocable | #104 原提 path A 作废 |
| 数据来源 | transcript JSONL `message.model` 丢 `[1m]` 后缀, 且 4-7/4-8 跳变 | model→window 查表在 transcript 路径不可靠 |
| 数据来源 | transcript `usage` block 只有 raw counts, 无 window/% | 纯 transcript 需自行推断 window |
| **数据来源** | **statusLine stdin JSON 含 `.context_window.{context_window_size, used_percentage, ...}` + `.model.id` (带 [1m])** | **runtime 直接给 size+%, 推翻所有 window 推断方案** |
| 可移植性 | statusLine stdin schema 通用 (任何 statusLine command 都收到), 但 relay 需配置挂载点 | 需 3 档 fallback + setup helper |

## 考虑的方案

| 方案 | 描述 | 评分 | 状态 |
|------|------|------|------|
| 合并单 Spec | #104+#18 一个 "AI-native 工作度量" 大 Spec | 中 | ❌ 否决 (#18 是 6-skill 重构, 会拖住小而确定的 #104) |
| **数据层共享 + 2 独立 Spec** | 共享 collector `lib/token_telemetry.py` + context-monitor / estimator 各自 Spec | 高 | ✅ **选定 (Q1=b)** |
| collector 算 % | collector 内置 window 推断 + 返回 used_pct | 低 | ❌ 否决 (Q2=a, estimator 不需要 window, 违反单一职责) |
| context 数据源: path A 调 /context | skill Bash 调 slash command | — | ❌ 不可行 (非 shell binary) |
| context 数据源: path A' transcript | 解析 JSONL raw counts + 猜 window | 中 | ⚠️ 降为 fallback |
| **context 数据源: statusLine relay** | statusLine 加 1 行写 cache, skill 读 | 高 | ✅ **选定 (Q3)** |
| window 推断: config/peak/path-d | 多种 window-size 推断 | — | ❌ **全作废** — statusLine 的 `context_window_size` 直接给 |

## 最终选择

**架构**: 数据层共享 collector + 2 独立 Spec; context-monitor 主走 statusLine relay (runtime-truth), transcript 解析为 fallback。

```
Claude Code runtime
   │ (每次渲染 statusLine, pipe 完整 JSON 到 stdin — 通用 CC 特性)
   ▼
statusLine command ──relay 1 行──► .aria/cache/context-window.json
   │                                {used_percentage, remaining_percentage,
   ▼                                 context_window_size, total_input/output_tokens,
 (照常显示状态栏)                     model_id, exceeds_200k_tokens, cost_usd, captured_at}
                                            │
        ┌───────────────────────────────────┤
        ▼                                   ▼
  aria-context-monitor (#104)         lib/token_telemetry.py (共享)
  读 cache → 实时 occupancy %          解析 transcript usage (fallback + estimator 数据源)
                                            ▲
                                            │
                                      ai-native-estimator (#18, 独立 Spec)
                                      per-task token 累加 (不碰 window%)
```

**3 档可移植性 fallback** (context-monitor 数据源):
1. relay cache 存在且 fresh → runtime-truth (size + %)
2. statusLine 存在但无 relay → setup helper 提示注入 (类 secret-guard dual-install)
3. 无 statusLine → transcript 解析 (window 来源: relay-cached size > config window_tokens > observed-peak 反推 > 200K 默认)

## 理由

1. **spike 推翻假设的链条**: /context 不可调 → transcript 缺 window → model 字段丢 [1m] → **statusLine stdin 全有**。owner 两个直觉 (从 model 定 window / 环境能看到 %) 都被 statusLine `.model.id`(带 [1m]) + `.context_window_size`(直接给数) 证实。
2. **零计算/零推断 (主路径)**: `context_window_size: 1000000` + `used_percentage: 67` runtime 已算好, 不需 config/peak/path-d 任何推断。
3. **共享数据层避免 #57 式重复**: collector 单一来源喂 context-monitor + estimator。
4. **2 独立 Spec 解耦成熟度**: #104 是窄 feature (relay+读), #18 是 6-skill 方法论重构, 不互相拖累。

## 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| relay 依赖 statusLine 配置 (非通用) | 3 档 fallback + aria setup helper 注入 relay 行 (类 secret-guard) |
| statusLine stdin schema 未来变动 | collector 防御式读取 + schema_version 标注; transcript fallback 兜底 |
| relay cache 陈旧 (statusLine 未渲染) | cache 带 `captured_at`, skill 判 staleness; window_size session 内不变可复用 |
| transcript fallback 仍需 window | relay-cached size 复用 (见过即持久) > config > peak 下界 > 200K |

## 后续

- 起草 #104 Spec (aria-context-monitor): relay 机制 + collector + 3 档 fallback + setup helper
- #18 (ai-native-estimator) 独立 Spec, 复用 `lib/token_telemetry.py`, 后续 cycle
- path d (Anthropic getContextUsage API) **不再需要** — 数据已在 statusLine stdin; 不 file feature request
