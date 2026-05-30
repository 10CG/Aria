# ai-native-estimator — Token 轴工作量估算 (v1 薄垂直切片)

> **Level**: 2 (Minimal — proposal.md only; 1 new skill + phase-d 集成 + 本地存储, 不跨多 service)
> **Status**: ✅ **Approved** — Phase A.2 CONVERGED 2026-05-30 via R1 (3/3 REVISE, 3 convergent Critical: parse_transcript_usage 复用错配 + transcript 字段未验 + cycle_meta 来源) → Rev1 → R2 (2 PWW + 1 REVISE: NEW-C-1 幂等自相矛盾, backend 发现 + qa corroborate) → Rev2 → R3 (2/2 PASS_WITH_WARNINGS, 0 new Critical, tech-lead CONVERGED)。Level 2 baseline + spike-verified transcript schema。2 doc-hygiene warning 已清。
> **Change ID**: `ai-native-estimator`
> **Source**: Forgejo aria-plugin [#18](https://forgejo.10cg.pub/10CG/aria-plugin/issues/18)
> **决策来源**: [DEC-20260530-001](../../../.aria/decisions/2026-05-30-ai-native-estimator-v1-architecture.md)
> **依赖 (已 ship)**: `aria-token-telemetry` (#104, v1.33.0) — `parse_transcript_usage()` raw counts
> **Target version**: aria-plugin v1.34.0
> **Risk class**: Additive (新 1 skill + phase-d 1 子步 + token-telemetry 新增 1 只读迭代器 API + 本地 .aria/estimator/; 无 API break; 无 transcript 走 fallback skip)
> **关联**: #18 完整双主轴愿景 (本 Spec 是 v1 Token 轴切片; Attention 轴 + L1/L2 + 5 集成 defer v2)

> **Rev1 changelog (post_spec R1 audit 闭合, 2026-05-30, R1 = 3/3 REVISE / 3 convergent Critical)**:
>   - **C1 (3/3) 复用契约错配**: `parse_transcript_usage()` 只返**末轮单值**, 无 range/turn-index/timestamp — 整个 watermark+wall_clock 设计建立在不存在的复用能力上。修: token-telemetry **新增** `iter_transcript_usage(path) → list[{uuid, timestamp, session_id, usage}]` (additive, 单一解析 SoT), estimator 消费它做区间和; Impact 表 token-telemetry 行从"无改动"改为"新增只读迭代器" + 加回归测 (Task 1.0)
>   - **C2 (backend+tl) transcript 字段未验**: spike (2026-05-30) 实证真实 transcript = `uuid`/`parentUuid`/`timestamp`(ISO8601)/`sessionId`, **无数字 turn_index**。修: watermark 锚改 `{last_uuid, last_timestamp, session_id}` (非 turn_index); §Transcript schema 固化实证字段
>   - **C2 (qa) cycle_meta 来源未定**: 修: `cycle_id = {spec_slug}-{captured_at_iso}` (deterministic); `spec_level` canonical 读 `openspec/changes/{spec}/proposal.md` frontmatter `Level`; 无 Spec cycle (L1 quick-fix) → spec_level=null 不计入 forecast 聚类
>   - **M (watermark 漂移)**: watermark 加 `session_id` + `transcript_path`; capture 先按 uuid 匹配, uuid 不在当前文件 (transcript 轮转/session 切换) → fallback `timestamp > last_timestamp` + warn; 越界/partial transcript → warn 不抛
>   - **M (幂等)**: capture 前全量扫 variance.jsonl 比对 cycle_id; 重复则 skip (record 不重 + watermark 不前进)
>   - **M (atomic write)**: variance.jsonl append + watermark.json 写均 tmp→`os.replace()` 原子 (v1 假设单进程, multi-terminal 并发写 defer v2 显式声明)
>   - **M (forecast cross-level 隔离)**: Success Criteria 加 "L1 N<3 即使 L2 N≥3 也返 L1 insufficient" 可机验约束
>   - **M (uncalibrated 防护)**: SC 改 "响应必含 `status=="insufficient"` + `uncalibrated==true` + `bootstrap` 数值, 缺一测试失败"
>   - **M (velocity 规范)**: velocity 加窗口 (configurable, 默认 10) + 排序 (captured_at desc) + 空 variance 返空列表不抛
>   - **m (wall_clock null fallback)**: timestamp 缺失 → `wall_clock_seconds: null` (合法值, history/velocity 跳过 null 不算术)
>   - **m (n_tasks nullable)**: 显式 nullable; 来源 = detailed-tasks.yaml count, 无则 null
>   - **m (fixture 补全)**: 加 empty variance / 不存在 variance / partial transcript (uuid 越界) / null timestamp / mixed-level fixture
>   - **m (enabled flag)**: SC 加 "enabled:false → phase-d capture 不触发"

> **Rev2 changelog (post_spec R2 audit 闭合, 2026-05-30, R2 = 2 PWW + 1 REVISE / 1 NEW Critical)**:
>   - **NEW-C-1 (backend, qa corroborated) 幂等自相矛盾**: `cycle_id` 嵌 capture 时刻 timestamp, 而幂等 key 在 cycle_id 上 — 同 cycle 重跑 captured_at 变 → cycle_id 变 → 去重失效。修: **幂等主机制 = watermark 空区间** (重跑无新 turn → range 空 → skip 不 append, watermark 不前进); `cycle_id = {spec_slug}-{end_uuid[:8]}` (range 末 uuid 锚, cycle 内稳定, 非 capture 时刻); cycle_id 全量扫降为 secondary guard
>   - **W-1 (backend) transcript_path 更新时机**: watermark `transcript_path` 在 capture **成功后**更新为当前路径 (fallback 路径也更新), 下次 capture 用新 path 的 uuid 锚
>   - **W-2 (backend) iter usage 字段命名**: `iter_transcript_usage` 透传 transcript **raw 字段名** (`input_tokens`/`output_tokens`/`cache_creation_input_tokens`/`cache_read_input_tokens`); estimator 内部映射到 variance 截短键 (`input`/`output`/`cache_creation`/`cache_read`)
>   - **W-3 (backend) forecast(None)**: `forecast(spec_level=None)` → 返回 `{status:"insufficient", reason:"no_spec_level"}` (不 raise, 与 advisory 非阻塞一致)
>   - **NEW-m (tl+qa) "25 tests" 事实错**: token-telemetry 现有套件实为 **15 py tests** (非 25); 改为 "现有 token-telemetry 测试套件 (当前 15) 零回归"
>   - **NEW-m (qa) captured_at 精度**: ISO8601 **毫秒级** (`...:00.123Z`) 固化于 SKILL.md (虽 cycle_id 已改 uuid 锚, captured_at 仍作记录时间戳, 毫秒避免碰撞)
>   - **NEW-m (qa) phase-d 末位步**: Task 1.4 改为"capture 作为 phase-d-closer **当前末位** D 子步" (实施前 verify 当前 phase-d 末步编号, 不硬编码 D.3)

---

## Why

### Direct trigger (#18)

aria 当前工时/进度估算建立在**传统人工时假设** (`task-planner` 4-8h 粒度 + S/M/L/XL 单维标量) 之上。但实际工作模式已是 **1 Human + Claude Code**, 该模式下传统估算失效: 同一小时 AI 可产出 1 行或 1000 行, "投入"分裂成 AI 烧 token / 人烧注意力两份异构资源, 不能互相换算。

### 为什么 Token 是更优的 AI 侧工作量单位

时间 (墙钟/工时) 在 AI 辅助模式有结构性缺陷 (需手工记录 / 被 idle+并行污染 / 预执行不可测 / 跨模型不可比)。Token 反之: API 响应自带、可自动测、线性映射成本、不受并行干扰、缓存感知。**#18 完整论证见 issue body**。

### 为什么现在可以做 (解锁点)

2026-05-29 ship 的 `aria-token-telemetry` (#104) 提供 `parse_transcript_usage()` — transcript JSONL 每 turn 的 raw counts (input/output/cache_read/cache_creation), window-independent。这正是 #18 预留的 Token 轴自动采集基础, 使 Axis 1 落地无需新数据管线。

### 为什么是薄切片 (scope discipline)

#18 原提案是 2.0 级愿景 (双轴 + L0/L1/L2 + 6 集成 + 校准)。v1 **只做能自动测且 de-risked 的 Token 轴**, 先积累 variance 数据 (L2 回归的前提), Attention 轴 (收集机制未解) + 集成面 + 高级预估策略全 defer。详见 DEC-20260530-001。

---

## What

新增 1 个 user-facing skill `ai-native-estimator` + phase-d-closer 1 个采集子步, 实现 **Token 轴 cycle 粒度的自动采集 + 查询 API**。

### Transcript schema (spike-verified 2026-05-30)

真实 transcript JSONL (`~/.claude/projects/{slug}/*.jsonl`) 每条 assistant 记录的字段 (spike 实证):

```jsonc
{
  "type": "assistant", "uuid": "...", "parentUuid": "...",   // 链式 id, 无数字 turn_index
  "sessionId": "...", "timestamp": "2026-05-29T04:47:40.799Z", // ISO8601, 所有 assistant 记录都有
  "message": { "usage": { "input_tokens":.., "output_tokens":.., "cache_creation_input_tokens":.., "cache_read_input_tokens":.. } }
}
```

> **关键**: **无数字 turn_index** — 记录用 `uuid`/`parentUuid` 链标识。`timestamp` 可靠存在 (wall_clock 来源)。`sessionId` 用于检测 session 切换。

### 核心机制: cycle 粒度 watermark 采集 (DEC-2, Rev1)

不做 per-task 微观归因。采集发生在 **phase-d-closer 收尾**。需 token-telemetry **新增只读迭代器** (additive, 单一解析 SoT):

```
token_telemetry.iter_transcript_usage(path) → list[{uuid, timestamp, session_id, usage}]
  (遍历 JSONL 所有含 usage 的 assistant 记录; usage 透传 raw 字段名:
   input_tokens/output_tokens/cache_creation_input_tokens/cache_read_input_tokens;
   区别于现有 parse_transcript_usage 只返末轮)

watermark.json: {last_uuid, last_timestamp, session_id, transcript_path}

estimator.capture(cycle_meta):
  turns = iter_transcript_usage(transcript_path)
  range = turns after (uuid == watermark.last_uuid)
          ├─ uuid 命中        → 增量从该 uuid 之后
          ├─ uuid 不在本文件   → transcript 轮转/session 切换: fallback timestamp > last_timestamp + warn
          │                     (此路径下 end_uuid = 该 timestamp-range 中时序末记录的 uuid, R3 NEW-W-1)
          └─ range 越界/空     → warn, 不抛 (partial transcript 保护)

  ★ 幂等主机制 = watermark 空区间 (Rev2): range 为空 (重跑无新 turn) → skip, 不 append, watermark 不前进
  range 非空:
    cycle_id = {spec_slug}-{end_uuid[:8]}   (range 末 uuid 锚, cycle 内稳定, 非 capture 时刻)
    secondary guard: 全量扫 variance.jsonl 比对 cycle_id; 命中 → skip
    逐 turn 累加 raw 分量 (映射截短键 input/output/cache_read/cache_creation)
      + 取首尾 timestamp 派生 wall_clock (null-safe)
    → atomic append variance.jsonl (tmp→os.replace)
    → 原子写 watermark (last_uuid/last_timestamp/session_id/transcript_path **均更新为本次 range 末态**)
```

### work_metric 与 raw 存储 (DEC-4)

variance.jsonl 存**全部四个 raw 分量** (input/output/cache_read/cache_creation), 不有损压缩, 使将来改公式无需重采集。headline 工作量指标:

```
work_metric = output_tokens + cache_creation_input_tokens
  (纯生成 + 新写上下文; cache_read 是上下文重载, 非"工作", 不计入 work_metric)
```

### 时间维度: 被动元数据 (DEC-7, owner alt-thinking)

`wall_clock_seconds = end_turn_ts − start_turn_ts`, 由新 `iter_transcript_usage` 一并提取的 range 首尾 `timestamp` 派生 (spike 实证 timestamp 可靠存在)。

> **⚠️ 语义边界**: wall_clock 是 **calendar-elapsed (日历经过时间), NOT effort/workload**。agent 跑 30min 时人在做别的事 — 墙钟 ≠ 人工投入 (正是 #18 警告的混淆)。`wall_clock_seconds` **不参与** 任何 forecast / workload 计算, 仅 `history()` / `velocity()` 附带展示列, 供人脑排期参考。
>
> **null fallback**: 若 range 首/尾 timestamp 缺失 → `wall_clock_seconds: null` (合法值); history/velocity 跳过 null, 不做算术 (避免 TypeError)。

### 查询 API (DEC-3: v1 仅采集 + 查询, 不集成 task-planner)

| API | 行为 |
|-----|------|
| `capture(cycle_meta)` | phase-d 调; append variance record + 更新 watermark; 幂等 (同 cycle_id 全量扫描去重) |
| `forecast(spec_level)` | 仅取**同 spec_level** records; N≥`min_samples`(3): `median(work_metric)`; N<3: `{status:"insufficient", have:N, need:3, bootstrap:<seed>, uncalibrated:true}`。**cross-level 隔离**: L1 N<3 即使 L2 N≥3 也返 L1 insufficient (不混算)。`forecast(None)` → `{status:"insufficient", reason:"no_spec_level"}` (不 raise) |
| `history()` | variance records 列表 (含 wall_clock 列, null 安全) |
| `velocity()` | 最近 `window` (configurable, 默认 10) cycles, 按 captured_at desc; work_metric + wall_clock 两列并排 (不合并); 空 variance → 空列表不抛 |

> `cycle_id = {spec_slug}-{end_uuid[:8]}` (range 末 uuid 锚, cycle 内稳定, 非 capture 时刻 — Rev2 NEW-C-1)。`captured_at` 用 ISO8601 **毫秒级**作记录时间戳。`spec_level` canonical 来源 = `openspec/changes/{spec}/proposal.md` frontmatter `Level` 行。无 Spec cycle (Level 1 quick-fix) → `spec_level=null`, 记录但**不计入 forecast 聚类**。

### 聚类与冷启动 (DEC-5, DEC-6)

- **聚类键 = `spec_level` (L1/L2/L3)** — issue 想要 task_type+context_load, 但 context_load 属 Attention 轴 (deferred); 三档够起步
- **bootstrap 种子表** (仅 N<3 fallback, 显式标 `uncalibrated:true`): `L1~30k / L2~150k / L3~500k` work_metric (来自 #18 失效场景锚点)

### variance.jsonl record schema

```jsonc
{
  "cycle_id": "aria-context-monitor-a4b3c2d1",  // {spec_slug}-{end_uuid[:8]}, range 末 uuid 锚 (Rev2)
  "spec": "aria-context-monitor",
  "spec_level": 2,                    // 聚类键; null = 无 Spec cycle (不计入 forecast)
  "captured_at": "2026-05-30T06:00:00.123Z",  // ISO8601 毫秒级
  "uuid_range": ["<start_uuid>", "<end_uuid>"],  // Rev1: uuid 锚 (无数字 turn_index)
  "n_turns": 42,
  "n_tasks": 9,                       // nullable; detailed-tasks.yaml count, 无则 null
  "tokens": { "input": ..., "output": ..., "cache_read": ..., "cache_creation": ... },  // raw 全存
  "work_metric": 1234,               // output + cache_creation (派生, 公式固化于 SKILL.md, 可重算)
  "wall_clock_seconds": 16200        // 被动元数据 (calendar-elapsed ≠ effort); null 合法
}
```

### Key Deliverables

- `aria/skills/ai-native-estimator/SKILL.md` + `scripts/estimator.py` (stdlib; capture/forecast/history/velocity + watermark + bootstrap; 复用 token-telemetry transcript 解析)
- `phase-d-closer` 集成: 收尾新增 D 子步调 `estimator.capture(cycle_meta)` (advisory, 非阻塞, 无 transcript 则 skip+warn)
- `.aria/estimator/{variance.jsonl, watermark.json}` schema + 存储 (append-only)
- config-loader 注册 `ai_native_estimator.{min_samples:3, bootstrap_seed:{L1,L2,L3}, enabled:true}` namespace
- 测试 + fixtures (Rule #6 deterministic structural substitute; internal data 逻辑无 LLM AB)

---

## Impact

| 组件 | 变更 | 风险 |
|------|------|------|
| 新 skill ai-native-estimator (user-facing) | 新增 | 无 (additive) |
| phase-d-closer | 加 1 采集子步 (advisory, 非阻塞) | 低 (无 transcript skip+warn) |
| config-loader | 加 ai_native_estimator namespace | 低 |
| **aria-token-telemetry** | **新增** `iter_transcript_usage()` 只读迭代器 (additive; 现有 parse_transcript_usage 不动) + 回归测 | 低 (additive, 不破坏现有契约; 但 #104 已 ship, 需跑现有 token-telemetry 套件 (当前 15 py tests) 零回归) |

**Backward compat**: 无 statusLine / 无 transcript → capture skip + warn, 不报错; variance.jsonl 缺失 → forecast 返回 insufficient + bootstrap; 不改 task-planner / 现有 S/M/L/XL 估算 (v1 旁挂, 共存); 不依赖 Anthropic 新 API。

---

## Tasks

- [ ] 1.0 **[token-telemetry additive]** 新增 `iter_transcript_usage(path) → list[{uuid, timestamp, session_id, usage}]` (usage 透传 raw 字段名; 现有 `parse_transcript_usage` 不动) + 单测 + 现有 token-telemetry 套件 (当前 15 py tests) 零回归
- [ ] 1.1 `estimator.py` 核心: watermark `{last_uuid, last_timestamp, session_id, transcript_path}` 读写 + capture (uuid 锚增量, uuid 不在文件→timestamp fallback+warn, 越界→warn 不抛; **幂等主机制=空区间 skip**; cycle_id={spec_slug}-{end_uuid[:8]} + secondary cycle_id 扫描; Σ raw 分量映射截短键; atomic tmp→os.replace; watermark 成功后更新含 transcript_path) + work_metric/wall_clock(null-safe) 派生
- [ ] 1.2 `estimator.py` 查询: forecast (cross-level 隔离: 仅同 spec_level, 3 态 insufficient含uncalibrated:true/median/bootstrap) + history (null-safe) + velocity (window 默认10, captured_at desc, work_metric+wall_clock 两列, 空→空列表)
- [ ] 1.3 `ai-native-estimator/SKILL.md`: user-facing 查询用法 + wall_clock 语义边界声明 (calendar≠effort) + work_metric 公式固化 + variance/watermark schema 文档
- [ ] 1.4 phase-d-closer 集成: 收尾**当前末位** D 子步调 capture (实施前 verify phase-d-closer 当前末步编号, 不硬编码 D.3; advisory 非阻塞); cycle_meta 构造 = `spec_slug` + `spec_level` 读 proposal.md frontmatter Level (无 Spec→null) + `n_tasks` 读 detailed-tasks.yaml (无→null); cycle_id 由 estimator 从 range 末 uuid 生成 (非 phase-d 传时刻); 无 transcript skip+warn
- [ ] 1.5 config-loader 注册 `ai_native_estimator` namespace (min_samples:3 / bootstrap_seed{L1,L2,L3} tokens / window:10 / enabled:true) + DEFAULTS.json + config-example.md
- [ ] 1.6 测试 + fixtures (Rule #6 structural substitute): fixtures = 多-turn transcript (含 uuid+timestamp+sessionId) / **partial transcript (uuid 越界)** / **null-timestamp transcript** / variance.jsonl (mixed-level) / **empty variance** / **不存在 variance** / watermark (stale uuid + session 切换); 单测 capture watermark 增量 / uuid-miss timestamp fallback / 越界 warn 不抛 / forecast 3 态 (含 uncalibrated:true 断言) / cross-level 隔离 / wall_clock 派生 + null / raw 全存 / spec_level 聚类 (含 null) / capture 幂等 (record 不重 + watermark 不前进) / velocity 空+window
- [ ] 1.7 跨项目可移植验证: 无 transcript sandbox 项目跑 capture → skip+warn 不报错; enabled:false → capture 不触发

---

## Success Criteria

- [ ] phase-d 收尾自动 capture: variance.jsonl append 1 record, watermark 推进到最新 assistant uuid
- [ ] watermark 增量: 连续两 cycle 采集, 第二次只含 last_uuid 之后的 turns (不重复计)
- [ ] watermark 漂移保护: uuid 不在当前 transcript (session 切换/轮转) → fallback timestamp + warn; `last_uuid` 越界/partial transcript → warn, **不抛异常**
- [ ] capture 幂等 (Rev2 主机制 = 空区间): 无新 turn 重跑 → range 空 → skip, record 不重复 append **且** watermark 不前进; cycle_id ({spec_slug}-{end_uuid[:8]}) 跨重跑稳定 (不随 capture 时刻变), secondary cycle_id 扫描命中亦 skip
- [ ] forecast(None) / spec_level 缺失: 返回 `{status:"insufficient", reason:"no_spec_level"}`, 不 raise
- [ ] forecast N<3: 响应**必含** `status=="insufficient"` + `uncalibrated==true` + `bootstrap`(数值), 任一缺失测试失败
- [ ] forecast N≥3: 返回同 spec_level 的 `median(work_metric)`; **cross-level 隔离**: L1 N<3 即使 L2 N≥3 也返 L1 insufficient (不混算)
- [ ] raw 全存: variance record 含 input/output/cache_read/cache_creation 四分量 (work_metric 可由固化公式重算)
- [ ] wall_clock 不污染 workload: forecast/work_metric 不含 wall_clock 字段; timestamp 缺失 → `wall_clock_seconds==null`, history/velocity null-safe 不抛
- [ ] 无 transcript: capture skip + warn, 不抛异常; `enabled==false` → capture 不触发
- [ ] velocity(): 默认 window=10, captured_at desc, work_metric + wall_clock 两列并排 (不合并); 空 variance → 空列表不抛
- [ ] spec_level=null (无 Spec cycle): record 写入但不计入任何 forecast 聚类

---

## Out of Scope (defer v2+)

- **Axis 2 (Attention-Minutes)** — 收集机制 (任务结束问答 / timeline 半自动推断) 是未解设计题, 独立 brainstorm
- **L1 (Haiku dry-run) / L2 (经验公式回归)** 预估策略 — 需 50+ 历史任务校准数据
- **5 skill 集成** — task-planner advisory / progress-updater dualAxisKPI / state-scanner 双轴 burndown / phase-a-planner 工期拆分 / requirements-sync
- **S/M/L/XL 替代** — v1 共存旁挂, 不改现有估算
- **per-task 粒度归因** — v1 只做 cycle 粒度; per-task 需 task 生命周期 hook (DEC-2 tradeoff)
- **时间作工作量轴** — 违背 #18 thesis; v1 时间仅被动元数据
- **usd_cost 计算 / 跨模型 normalized_tokens 权重** — 需 model_tier 单价表, defer (raw 已存, 将来可派生)
- **multi-terminal 并发写 variance.jsonl** — v1 假设单进程写 (atomic tmp→os.replace 防单写者截断, 但不防多 terminal 交错); multi-terminal file-lock defer v2 (与 multi-terminal-coordination Rule #9 对齐)
- **multi-terminal transcript 选择** — capture 继承 token-telemetry `find_transcript` mtime-newest 策略; 多 terminal 选错文件场景 defer v2
