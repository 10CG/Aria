# aria-context-monitor — 暴露 Claude Code context usage 给 skills/agents

> **Level**: 2 (Minimal — proposal.md only; context-monitor skill + token-telemetry internal skill + statusLine relay, 不跨多 service)
> **Status**: ✅ **Approved** — Phase A.2 CONVERGED 2026-05-29 via R1 (3 PWW + 1 FAIL, 2C+8M) → Rev1 (闭合全部 2C+8M) → R2 PASS_WITH_WARNINGS unanimous (qa PWW + tech-lead PWW + code-reviewer PASS, 0 new critical/major, 5 non-blocking minor carried to task-planner). Level 2 baseline per [[feedback_post_spec_audit_two_round_pragmatic_for_l2]]。
> **R2 carried minors** (non-blocking, 实施期吸收): config-loader `DEFAULTS.json` 注册 `context_monitor` namespace + 注册 task / `used_percentage_proxy` 准确度交叉校验 / proxy null 一致性 (unavailable 态) / atomic-write tmp 文件并发命名 (用 `$$` PID) / internal skill 加载边界。
> **Change ID**: `aria-context-monitor`
> **Source**: Forgejo Aria [#104](https://forgejo.10cg.pub/10CG/Aria/issues/104)
> **决策来源**: [DEC-20260529-001](../../../.aria/decisions/2026-05-29-context-monitor-architecture.md)
> **Spike 依据**: [.aria/notes/2026-05-29-context-monitor-spike.md](../../../.aria/notes/2026-05-29-context-monitor-spike.md)
> **Target version**: aria-plugin v1.33.0 (next minor)
> **Ship target**: 单 cycle (~4-5h end-to-end, Rev1 后 scope 略增)
> **Risk class**: Additive (新 2 skill + 1 行 relay + cache; 无 API break; statusLine 未配项目走 fallback 仍可用)
> **关联**: aria-plugin #18 (ai-native-estimator) — 共享 `aria-token-telemetry` internal skill, 独立 Spec, 后续 cycle

> **Rev1 changelog (post_spec R1 audit 闭合, 2026-05-29, R1 = 3 PWW + 1 FAIL / 2C + 8M)**:
>   - **C1 (qa)** staleness 阈值: 新增 §Staleness 契约 (默认 300s, config 可覆盖) + Success Criteria 可验值 + Task 1.6 固化常量
>   - **C2 (qa)** relay 幂等: §Relay 注入语义 定义 marker-注释锚点检测 + Task 1.7 加 run-twice / pre-existing-relay / user-custom-bar 场景
>   - **M-collector-location (tech-lead)**: 共享 collector 落点改为**独立 internal skill `aria-token-telemetry`** (复用 git-remote-helper US-012 Layer 3 先例), 非寄生 state-scanner
>   - **M-schema-evidence (code-reviewer S1)**: Task 1.1 标 **BLOCKING pre-Phase-B gate** + 失败回退条款 (若 `context_window_size` 缺失则 fallback 推断链升为主路径)
>   - **M-used%-semantics (code-reviewer S2)**: 拆分 `used_percentage` (relay 口径 total_input/window) vs `used_percentage_proxy` (transcript input+cache 合计), 两字段不混用, schema 显式标注口径
>   - **M-relay-stdin (tech-lead)**: §Relay 注入语义 明确复用 `$input` 变量 + 注入位置必须在 `input=$(cat)` 之后
>   - **M-window-source-enum (qa/cr/ba)**: window_source enum 补全 + relay_cache 命中必 = `runtime` 约束 + 加 `cached_size_reuse` 值映射 DEC 4-tier
>   - **M-atomic-write (backend)**: relay 写改 tmp→rename 原子替换 + token_telemetry 捕获 JSONDecodeError → unavailable + Task 1.7 加 corrupt-cache 场景
>   - **M-schema-version + config-path (backend)**: cache 加顶层 `schema_version` (对比 issues.json) + 规范 config key `context_monitor.window_tokens`
>   - **M-rule6 + jq (qa)**: Rule #6 = deterministic structural substitute (明确 fixture 路径) + jq 硬依赖 aria-doctor 检测 + 缺失 graceful degradation

---

## Why

### Direct trigger

aria 十步循环 + Phase B 实施期间, AI 频繁需要"当前会话继续推进 vs 暂停"的决策。最优依据是**剩余 context 容量**: 充足→继续 (省会话切换); 紧张→暂停 + 形成自然 commit boundary。**但 AI 当前靠"感觉"判断, 常失准。**

### 实证 (Forgejo #104)

10cg.local `passwall2-route-verify` Phase B: AI 估"剩 ~23%" 实际"剩 45%", **+22% 偏差** → 触发不必要暂停, 用户被迫显式"继续"。每 cycle 损失 5-10min round-trip。反向灾难: 低估消耗 → 真撞限 → 硬丢上下文。

### 为什么对 aria 尤其重要

aria 十步循环本质流程编排, 单次会话可横跨多步; "在哪个 step 暂停"是关键决策点, 准确 context 余量是必要输入, 缺失则编排逻辑退化为"猜"。

---

## What

新增 2 个 skill + statusLine relay 机制, 让 AI 机读当前 context 占用 (runtime-truth, 零猜测):

1. **`aria-token-telemetry`** (internal, `user-invocable: false`) — 共享数据层, 复用 [git-remote-helper US-012 Layer 3 先例](../../../aria/skills/git-remote-helper/SKILL.md) 的"internal skill 作跨-skill 共享基础设施"模式
2. **`aria-context-monitor`** (user-facing) — 消费 telemetry, 返回结构化 occupancy

### 核心机制: statusLine relay (spike 验证)

Claude Code runtime 每次渲染 statusLine 时 pipe 一个丰富 JSON 到 statusLine command 的 **stdin**。Spike 单次 capture 见到:

```json
{
  "model": { "id": "claude-opus-4-8[1m]", "display_name": "Opus 4.8 (1M context)" },
  "context_window": {
    "context_window_size": 1000000, "used_percentage": 67, "remaining_percentage": 33,
    "total_input_tokens": 673955, "total_output_tokens": 615, "current_usage": {...}
  },
  "exceeds_200k_tokens": false, "transcript_path": "...", "session_id": "...", "cost": {...}, "rate_limits": {...}
}
```

> **⚠️ 证据状态 (R1-S1 fix)**: 生产 `statusline-command.sh` 已独立佐证 `used_percentage` / `total_input_tokens` / `total_output_tokens` / `cost` / `rate_limits` / `model.display_name`。但 `context_window_size` / `model.id`(带[1m]) / `remaining_percentage` / `exceeds_200k_tokens` / `transcript_path` **仅来自单次已删 spike capture, 无独立可复现证据**。**Task 1.1 是 BLOCKING pre-Phase-B gate**: 必须重新 capture 固化 schema 再实施 1.2+。**失败回退条款**: 若 `context_window_size` 实际不存在, fallback window 推断链 (config/peak/200K) 升级为主路径, relay 仅供 used_percentage 直读。

### Staleness 契约 (R1-C1 fix)

| 项 | 值 |
|----|-----|
| 默认 staleness 阈值 | **300s** (config `context_monitor.staleness_threshold_seconds` 可覆盖) |
| `staleness_seconds > 阈值` | skill 返回 `confidence=estimate` + 触发 fallback 降级 (不再信任 relay cache 的 used_percentage) |
| `staleness_seconds ≤ 阈值` | `confidence=high`, 用 relay cache runtime-truth |

### Relay 注入语义 (R1-C2 + R1-relay-stdin fix)

statusLine 首行 `input=$(cat)` **耗尽 stdin** (一次性流)。故 relay 行约束:

- **必须复用** 已捕获的 `$input` 变量 (不可再 `cat`)
- **必须注入在 `input=$(cat)` 之后** (位置敏感, 非"位置无关 1 行")
- **marker-注释锚点**: relay 行用 `# >>> aria-context-monitor relay >>>` / `# <<< aria-context-monitor relay <<<` 包裹; `setup_relay.sh` 检测此 marker 判定"已注入" (非脆弱字符串匹配)
- **原子写 (R1-atomic-write fix)**: `echo "$input" | jq -c '{schema_version:"1.0", ...}' > "$tmp" && mv "$tmp" "$cache"` (tmp→rename, 避免 truncate→write 间并发读 corrupt)

### 数据来源优先级 (3 档 fallback, 保证可移植性)

数据 schema (statusLine stdin) 是**通用 Claude Code 特性**; relay 抓取依赖 statusLine 配置 + relay marker。3 档:

| 档 | 来源 | 何时 | confidence |
|----|------|------|-----------|
| 1 | `.aria/cache/context-window.json` (relay cache, fresh) | statusLine 已配 + relay marker + staleness≤阈值 | high (runtime-truth) |
| 2 | setup helper 检测 statusLine 无 relay marker → 提示注入 | 未注入 | — (引导) |
| 3 | transcript JSONL 解析 (`aria-token-telemetry`) | 无 statusLine / cache 缺失/陈旧/corrupt | estimate |

### window_source 解析链 (R1-window-source fix, 对齐 DEC 4-tier)

```
relay cache 命中 (source=relay_cache) → window_source 恒 = "runtime"  (约束: 不得标其他值)

transcript fallback (source=transcript_fallback) window 4 档:
  1. cached_size_reuse  — 复用上次 relay cache 见过的 context_window_size (session 内不变)
  2. config             — .aria/config.json `context_monitor.window_tokens`
  3. empirical_peak     — observed-peak 反推下界 (snap 最小 fitting tier)
  4. default            — 200K 保守兜底
```

### Key Deliverables

- `aria/skills/aria-token-telemetry/SKILL.md` + `scripts/token_telemetry.py` — internal 共享层: relay cache 读 (含 schema_version 校验 + JSONDecodeError→unavailable 防御) + transcript usage 解析 + window 4 档 resolve。**raw counts 解析独立于 window%** (Q2=a, #18 复用基础)
- `aria/skills/aria-context-monitor/SKILL.md` — user-facing: 调 telemetry → 返回结构化 JSON + staleness 判定 + confidence 标注
- statusLine relay marker 块 + `aria/skills/aria-context-monitor/scripts/setup_relay.sh` — 幂等注入 (marker 检测) / 用户无 statusLine 时建最小 reference (仅 context bar + relay, 无个人偏好); **仅注入通用 relay, 不纳入用户 PEAK/BUSY 等 instance-layer 偏好**
- aria-doctor 集成 — 3 态检测 (relay-installed / statusline-no-relay / no-statusline) + jq 可用性检测
- 消费集成点文档: `phase-b-developer` / `phase-c-integrator` "暂停 vs 继续"决策调用点 + 阈值建议

### 输出结构 (skill 返回, R1-used%-semantics fix — 拆分两口径)

```json
{
  "source": "relay_cache | transcript_fallback | unavailable",
  "confidence": "high | estimate",
  "schema_version": "1.0",
  "used_percentage": 67,              // 仅 relay_cache: runtime 口径 (total_input/window). transcript 路径为 null
  "used_percentage_proxy": null,      // 仅 transcript_fallback: (input+cache_read+cache_creation)/window. relay 路径为 null
  "remaining_percentage": 33,
  "context_window_size": 1000000,
  "window_source": "runtime | cached_size_reuse | config | empirical_peak | default",
  "total_input_tokens": 673955,
  "model_id": "claude-opus-4-8[1m]",
  "exceeds_200k_tokens": false,
  "captured_at": "2026-05-29T...",
  "staleness_seconds": 12
}
```

> **口径不混用 (R1-S2)**: relay 路径填 `used_percentage` (runtime total_input/window 口径); transcript 路径填 `used_percentage_proxy` (last-turn input+cache 合计口径) —— **两者是不同的量, 不共用字段**。消费方按 `source` 读对应字段, 避免重蹈 22% drift。

---

## Impact

| 组件 | 变更 | 风险 |
|------|------|------|
| 新 skill aria-token-telemetry (internal) | 新增 | 无 (additive, user-invocable:false) |
| 新 skill aria-context-monitor (user-facing) | 新增 | 无 (additive) |
| 用户 statusLine command | 注入 marker-包裹 relay 块 (helper 幂等, 复用 $input, atomic write) | 低 (marker 检测 + 备份 + 位置约束) |
| aria-doctor | 加 relay 3 态 + jq 检测 | 低 |
| phase-b/c-developer | 文档加调用建议 | 无 (建议性) |

**Backward compat**: statusLine 未配/未注入 → transcript fallback (confidence=estimate) 或 unavailable, **不报错**; corrupt/stale cache → 降级不抛异常; 不依赖 Anthropic 新 API; 不改 statusLine 显示。

---

## Tasks

- [ ] 1.1 **[BLOCKING pre-Phase-B gate]** 重新 capture statusLine stdin + 固化 schema 字段契约到 aria-token-telemetry SKILL.md; 验证 `context_window_size`/`model.id[1m]`/`transcript_path`/`remaining_percentage`/`exceeds_200k_tokens` 真实存在; **若 `context_window_size` 缺失 → 触发回退条款 (fallback 链升主路径), 回 A.2 修 Spec**
- [ ] 1.2 实现 `aria-token-telemetry/scripts/token_telemetry.py`: relay cache 读 (schema_version 校验 + JSONDecodeError/OSError→unavailable) + transcript JSONL usage 解析 + window 4 档 resolve (cached_size_reuse>config>empirical_peak>default)
- [ ] 1.3 实现 statusLine relay marker 块 + `setup_relay.sh`: 幂等 (marker 锚点检测) / 复用 $input / 注入在 input=$(cat) 后 / atomic tmp→rename / 用户无 statusLine 建最小 reference
- [ ] 1.4 实现 aria-context-monitor SKILL.md: 调 telemetry → staleness 判定 (300s 默认) → 返回结构化 JSON (used_percentage vs used_percentage_proxy 按 source 二选一) + confidence
- [ ] 1.5 aria-doctor 集成: relay 3 态检测 (installed/statusline-no-relay/no-statusline) + jq 可用性
- [ ] 1.6 固化 staleness 阈值常量 (300s, config `context_monitor.staleness_threshold_seconds` 可覆盖) + window_source enum 5 值
- [ ] 1.7 fallback 路径单测: 无 statusLine / cache 陈旧(>300s) / **corrupt cache JSON** / transcript-only window 4 档 / **setup_relay run-twice 幂等** / **pre-existing relay marker** / **user 已有 custom context bar**
- [ ] 1.8 消费集成文档: phase-b/c-developer 调用点 + 决策阈值建议 (e.g. used%>85 建议暂停)
- [ ] 1.9 Rule #6: deterministic structural substitute (token_telemetry parse 单测 fixture at `aria-plugin-benchmarks/context-monitor/` — relay/transcript/corrupt/stale 各 1 fixture + window 4 档断言; 非 LLM AB, 参 `feedback_deterministic_structural_skill_rule6_substitute`)

---

## Success Criteria

- [ ] statusLine 已配 + fresh (staleness≤300s): skill 返回 `source=relay_cache` + `confidence=high` + `used_percentage` 与状态栏显示 0 偏差
- [ ] statusLine 未配: skill 返回 `source=transcript_fallback` + `confidence=estimate` + `used_percentage_proxy` 非 null (used_percentage = null), 不报错
- [ ] cache staleness > 300s: skill 降级 `confidence=estimate`, 不再信任 relay used_percentage
- [ ] corrupt cache JSON: token_telemetry 捕获 JSONDecodeError → `source=unavailable`, 不抛异常
- [ ] 复现 #104 场景: AI 调 skill 得准确 % (消除 22% 凭感觉偏差)
- [ ] setup_relay.sh 幂等: run-twice 不重复注入 (marker 检测); pre-existing relay marker 识别正确; user 已有 custom context bar 不冲突
- [ ] window_source 正确: relay_cache 命中恒 = `runtime`; transcript 路径按 4 档正确标注
- [ ] aria-doctor 正确报告 3 态 + jq 缺失提示
- [ ] `token_telemetry.py` raw-counts 解析接口可被 #18 estimator 复用 (独立于 window%)
- [ ] 跨项目可移植: 无 statusLine sandbox 项目跑 skill, fallback 正常

---

## Out of Scope

- **#18 ai-native-estimator** — 复用本 Spec `aria-token-telemetry`, 独立 Spec, 后续 cycle
- **Anthropic getContextUsage() API (path d)** — 数据已在 statusLine stdin, 不 file feature request
- **model→window 静态表** — runtime 直接给 size; fallback 用 observed-peak 下界, 不查表
- **自动暂停执行** — skill 只提供数据, 暂停决策由 AI/phase skill 判断, 不自动中断
- **用户 statusLine 个人偏好** (PEAK/BUSY/quota-ETA 等) — instance-layer, 留用户 ~/.claude/, 不纳入 aria 标准 (DEC D2)
