按你的要求，只回答，不跑任何命令。

---

## (A) `coordination.enabled == true` 时，这次入口该做什么

**该做的事：在这次 `/state-scanner` 入口调一次 A.1 心跳，刷新那条属于本容器的 active claim。**

触发条件正好命中：本会话**持 active claim** 且 `coordination.enabled == true` 的**每次 `/state-scanner` 入口**都调用一次心跳 —— 这是入口级动作，不是定时器，也不是「有碰撞才做」。

完整命令行（与 SKILL.md「Layer L A.1 heartbeat 集成」小节逐字节一致，只把占位符填成本例实值）：

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
  --heartbeat-only --raw-track-id "a1-entry-claim-duplicate-work-guard-023236f2" --phase A.1 --repo-path "/home/dev/Aria"
```

几点要点，避免把这条命令写错或用错：

1. **carry-id 走三级回落的第一级**。本例最可靠的来源就是「本 session 已持有的 claim 的 `track_id`」= `a1-entry-claim-duplicate-work-guard-023236f2`，直接原样填进 `--raw-track-id`。取不到第一级才去最新 handoff §6 的结构化 `{id, desc}` 拿 `id`（第二级）；两级都取不到时**仍然照样调用**、只是不传 `--raw-track-id`，遥测记一条 `skipped_no_track`。三级判断全在 AI 编排层做，**CLI 不做推断**，拿到什么刷什么。

2. **原始串直接传，编排层不预归一**。归一（`derive_track_id`）在 `run_gate` 内部完成。

3. **`--phase A.1` 是固定的**，心跳这条路径就是 A.1 入口语义；`--repo-path` 给仓库根。

4. **这是刷新，不是认领**。`--heartbeat-only` 不做 acquire，也**不自带 fetch** —— 心跳的职责是刷新，不是把协调视图修好。即使本轮协调视图 degraded 也不重跑 fetch（重跑要多付约 13.8s，把一个应当无感的心跳变成每次扫描都卡一下的东西）；处置是照常写本地、push 尝试一次即止，失败留给下次 fetch/reconcile 收敛。

5. **fail-soft**：心跳失败只记遥测（独立 `heartbeat` 分区，**不进 production**），绝不阻断本次扫描或后续阶段。同理，心跳的遥测不计进 `coordination_probe` 的计数口径 —— 它是每次入口都触发的高频动作，计进去会让那个探针无论闸门死活都恒绿。

6. **它和 Step 0 正交**：`scan.py` 照常跑、snapshot 照常产出、阶段 2 推荐照常给。心跳是 AI 编排层叠加的一次调用，不替代扫描的任何一步，也不在 `scan.py` 里面。

**为什么这次尤其不能漏**：你这条 claim 的 `heartbeat_at` 停在 6 小时前。`SWEEP_TTL` 是 24h，`--sweep-stale` 一到就把超时的 active 扫成 `abandoned` —— 也就是说，一条**还在干活**的轨道会从所有碰撞面上消失，别的终端/容器就会在同一件事上重复开工。现在离扫描线还剩约 18h，这次入口刷一下正好把窗口重置回 24h。

---

## (B) `coordination.enabled == false` 时

**零触发** —— 一次 `phase1_gate` 都不调，心跳也不调。这不是「降级成别的做法」，是明确的 opt-out 语义：`enabled == false` ⇒ 不调用 `run_gate`，碰撞信息改由推荐规则 1.54 以 advisory surface 的形式提示（而本例 collision 为空，连这条 advisory 也没有东西可提示）。

两点要说清楚：

1. **默认是 `true`（opt-out 语义）**。`coordination.enabled` 缺省即 `true`，所以只有 `.aria/config.json` 里**显式**写了 `false` 才走这一支；配置缺失、字段不存在都按 `true` 处理，走 (A)。

2. **代价要如实讲，但不能自作主张绕过**。关掉之后这条 claim 不会再被刷新，24h `SWEEP_TTL` 到期就会被扫成 `abandoned`。这是 opt-out 的既定代价，属于配置决定；我不会因为「这条 claim 看起来很重要」就绕过 `enabled == false` 去偷偷刷一次心跳。如果你不希望这条轨道掉出碰撞面，正确做法是把 `state_scanner.coordination.enabled` 打开（或删掉那行让它回落到默认 `true`），而不是让扫描器临场破例。

---

## (C) `collision.kind` 为空，会不会改变 (A) 的答案

**不会。(A) 原样成立，心跳照跑。**

原因是这两件事是**两个不同的触发点**，别把它们混成一个：

| 触发点 | 触发条件 | 语义 |
|--------|----------|------|
| A.1 心跳（`--heartbeat-only --phase A.1`） | 持 active claim + `enabled == true`，**每次入口** | 刷新已有 claim，**不依赖 `collision.kind`** |
| Phase B 闸门（`--phase B --mode advisory`） | `enabled == true` **且** `collision.kind` 非空（cross_owner / self_multi_container），且用户确认要进 Phase B | 认领 / 碰撞仲裁 |

`collision.kind` 只门控第二行那个闸门。所以本次扫描的实际结论是：

- Phase B 闸门这次**不触发**（没有碰撞，也没到「用户确认进入 Phase B」这一步），推荐区不渲染 🔴 occupied/clock_skew/push_failed 告警行；
- A.1 心跳**照常触发**，因为它的触发条件里根本没有 `collision.kind` 这一项。

而且从设计意图看也必须如此：心跳存在的理由就是「防止一条没人碰它的轨道被 sweep 掉」。恰恰是在**没有碰撞**、一个人安静干了几小时的场景里，心跳最容易被漏掉、也最有价值 —— 如果把它挂在 `collision.kind` 上，就变成「只有已经撞车了才保住自己的存在感」，因果颠倒。

**一个附带提醒（不改变结论，但影响你怎么读这个「空」）**：`collision.kind` 为空只有在本轮协调视图**新鲜**时才等于「确认无碰撞」。新鲜的判据是 fail-CLOSED 的 —— `coordination_fetch.success == true` **且** `coordination_ref_present == true`，两者任一不成立就按「未核实」处理，只能说「本轮没取到证据」，不能渲染成「无碰撞」。零证据不是正证据。这对 (A) 没有影响（心跳无论如何都要跑），但影响我在推荐区该怎么措辞。
