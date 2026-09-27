按你的要求，这次只回答，不跑任何命令（没有运行 scan.py，也没有调用 phase1_gate.py）。

依据是 state-scanner SKILL.md 的「Layer L A.1 heartbeat 集成」一节，以及 references/layer-l-integration.md 里同名的设计段。

## (A) `coordination.enabled == true`：本次入口要刷新一次心跳

触发条件同时满足：本会话持有 active claim，并且 `enabled == true`。SKILL.md 规定，这种情况下**每次 `/state-scanner` 入口都要调用一次** `--heartbeat-only`，不看 `collision.kind`。

完整命令行（SKILL.md 原文）：

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
  --heartbeat-only --raw-track-id "a1-entry-claim-duplicate-work-guard-023236f2" --phase A.1 --repo-path "/home/dev/Aria"
```

在本仓里展开路径后是：

```bash
python3 /home/dev/Aria/aria/skills/state-scanner/scripts/phase1_gate.py \
  --heartbeat-only --raw-track-id "a1-entry-claim-duplicate-work-guard-023236f2" --phase A.1 --repo-path "/home/dev/Aria"
```

说明：
1. **carry-id 从哪来**：三级回落的第 1 级，也就是本会话已持有 claim 的 `track_id`，直接用 `a1-entry-claim-duplicate-work-guard-023236f2`，不用去翻 handoff §6。这个串是纯 ASCII、小写、44 个字符（不超过 64），`derive_track_id` 对它不会再改动，所以原样传进去就能对上这条 claim。
2. **它具体做什么**：`heartbeat_by_track` 按 (本容器, 归一后的 track_id, active) 找到这条 claim，只改写 `heartbeat_at`，然后推送一次。它不做 reconcile，不自己 fetch，也不新建 claim。如果这个容器在不同 session 里对同一 track 有多条 active claim，会全部刷新。
3. **为什么现在必须刷**：heartbeat 已经停了 6 小时。到 `SWEEP_TTL`（24h）时，这条 claim 会被 `--sweep-stale` 扫成 `abandoned`，一条还在干活的轨道就会从所有碰撞面上消失。
4. **失败了怎么办（fail-soft）**：退出码恒为 0。成功时 `outcome` 为 `refreshed`；失败时为 `error`，只记进 `heartbeat` 遥测分区（不进 production），**不挡扫描，也不挡后面的阶段**。push 失败时本地的刷新仍然有效，等下次 fetch/reconcile 时收敛。fetch 降级时也不要为心跳重跑 fetch（否则每次入口要多花约 13.8s）。
5. 心跳之后，扫描照常进行：跑 scan.py，然后进阶段 2 推荐。输出 JSON 里的 `outcome` 和 `push_success` 要在报告里如实写出来。

## (B) `enabled == false`：零触发

- 不调用 `--heartbeat-only`（零触发），**也不调用** Phase B 的 `run_gate`/phase1_gate 认领闸门（零调用）。
- 如果有碰撞，只由 rule 1.54 做 advisory 提示；扫描和推荐照常进行。
- 建议在报告里写明「心跳被配置关闭而跳过（`skipped_disabled`）」。这样读报告的人能区分「被关掉了」和「心跳坏了/从没跑过」。
- 后果要说清楚：这条 claim 的 heartbeat 会一直停在原处。现在是 6 小时，过了 24h 就可能被 sweep 扫成 `abandoned`。这是 opt-out 配置本身带来的代价，AI 不应自己改配置去绕开。如果 owner 希望保住这条 claim，要由 owner 决定是否重新打开 `enabled`。

## (C) `collision.kind` 为空：不改变 (A) 的答案

- A.1 心跳的触发条件**只有**「持 active claim 且 `enabled == true`」。SKILL.md 明确写了「不依赖 `collision.kind`」。没有碰撞时，(A) 里那条 `--heartbeat-only` 命令照样要跑。
- `collision.kind` 为空只影响**另一个**触点：Phase B 入口的认领闸门（`phase1_gate.py --raw-track-id ... --phase B --mode advisory ...`）。它的触发条件是 `enabled == true` **且** `collision.kind` 非空。所以本次没有碰撞时，那条 Phase B 闸门调用不会触发。但这和心跳是两件事，不要混在一起。
- 还有一点：「collision 为空」要当成「无碰撞」来用，前提是协调视图是新鲜的，也就是 `coordination_fetch.success == true` **且** `coordination_ref_present == true`。两者任一不成立，就只能算**未核实**，不能说「无碰撞」。不过这一点也不影响心跳要不要调。

## 总结

| 情形 | 心跳 `--heartbeat-only` | Phase B 认领闸门 |
|------|------------------------|-----------------|
| enabled=true, collision 为空 | **调用**（命令见 A） | 不调用（collision 为空） |
| enabled=true, collision 非空 | 调用 | 用户确认进 Phase B 时调用 |
| enabled=false | 不调用（报告里记 `skipped_disabled`） | 不调用 |
