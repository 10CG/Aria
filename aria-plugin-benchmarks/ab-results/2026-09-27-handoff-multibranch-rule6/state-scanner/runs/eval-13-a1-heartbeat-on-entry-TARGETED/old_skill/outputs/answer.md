按你的要求只回答、不跑命令。依据是 state-scanner SKILL.md 的「Layer L A.1 heartbeat 集成」和「编排契约」两节，以及 references/layer-l-integration.md 的同名设计段。

先说一个前提：这次入口里有**两个互相独立**的协调触发点，判断条件不同，别混在一起。

| 触发点 | 时机 | 触发条件 |
|---|---|---|
| A.1 心跳 (`--heartbeat-only`) | **每次** `/state-scanner` 入口 | 本会话持有 active claim **且** `coordination.enabled == true`；**不看** `collision.kind` |
| Phase B 认领闸 (`run_gate`，`--phase B --mode advisory`) | 用户确认进入 Phase B 之后、B.1 之前 | `coordination.enabled == true` **且** `tracks_multibranch.collision.kind` 非空 |

---

### (A) `enabled == true`：这次入口该做什么

1. **Step 0 照常跑 scan.py**（硬约束，不能跳过）：
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/scan.py" \
     --output .aria/state-snapshot.json
   ```
2. **刷新一次心跳**。本会话持有 active claim，而且 enabled 为 true，所以这次入口必须调一次 `--heartbeat-only`。carry-id 按三级回落取第 1 级，也就是本会话已持有的那条 claim 的 `track_id`，**原样传入**。归一由 CLI 内部完成，编排层不预先处理：
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
     --heartbeat-only --raw-track-id "a1-entry-claim-duplicate-work-guard-023236f2" \
     --phase A.1 --repo-path "/home/dev/Aria"
   ```
   在 Aria 仓内直调时，`${CLAUDE_PLUGIN_ROOT:-aria}` 会回落成 `aria`，也就是 `/home/dev/Aria/aria/skills/state-scanner/scripts/phase1_gate.py`。

   为什么现在必须刷：heartbeat 已经停了 6 小时。`SWEEP_TTL` 是 24 小时，所以它现在还是 active；但如果一直没人刷新，到 24 小时就会被 `--sweep-stale` 扫成 `abandoned`，这条还在干活的轨道就会从所有碰撞面上消失。刷一次，TTL 就重新计时。

   执行时注意三点：
   - **失败也不阻断**：心跳失败只记遥测，写入独立的 `heartbeat` 分区，不进 production 分区；不阻断扫描，也不阻断后续推荐。
   - **不额外 fetch**：协调视图降级时不重跑 fetch（重跑一次每次入口要多付约 13.8s）。照常写本地，push 只试一次，失败就留给下次 fetch 或 reconcile 去收敛。
   - **新鲜度判断**：只有 `coordination_fetch.success == true` 且 `coordination_ref_present == true` 时，协调视图才算新鲜；任一条件不成立都按「未核实」处理，不能当成「无碰撞」。
3. 然后照常进入阶段 2、3、4（推荐 → 用户确认 → 启动工作流）。Phase B 认领闸能不能触发，要看 `collision.kind`，见 (C)。

> 说明：我这个评测环境不允许调用 `phase1_gate.py`，因为它会写协调 ref。上面的命令只是按 skill 规定写出来的，没有实际执行。

### (B) `enabled == false`：该做什么

- **只跑 Step 0 的 scan.py**，然后照常进入阶段 2、3、4。
- **完全不调用协调闸**：`--heartbeat-only` 心跳不调，Phase B 的 `run_gate` 认领闸也不调。三个触发点（A.1 入口认领、每次入口心跳、Phase B 认领）都受 `coordination.enabled` 控制，`false` 就是显式关闭。
- 如果快照里有碰撞，只由推荐规则 1.54 给出 advisory 提示，不写也不推任何 claim。
- 代价要说清楚：这条 claim 的 heartbeat 会继续停在原处。6 小时后再过 18 小时就到 24 小时 `SWEEP_TTL`，一旦执行 stale 清扫，它会被判成 `abandoned`。如果你确实还在做这条轨道，要么把 `enabled` 改回 true（缺省就是 true，关掉是显式 opt-out），要么接受这个后果。

### (C) `collision.kind` 为空：会不会改变 (A) 的答案？

**不会改变心跳这一步。** 心跳的触发条件明确写着「每次入口都调用一次，**不依赖 `collision.kind`**」，只看两件事：持有 active claim、`enabled == true`。所以 (A) 的第 2 步照样要执行，命令完全一样。

它只影响另一个触发点，也就是 **Phase B 认领闸**：这个闸的条件是 `enabled == true` **且** `collision.kind` 非空（`cross-owner` 或 `self_multi_container`）。`kind` 为空时，即使之后你确认进入 Phase B，也不会触发这条命令：
```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
  --raw-track-id "<§6 选定 carry-id>" --phase B --mode advisory --repo-path "/home/dev/Aria"
```
推荐区也不会出现碰撞告警。

另外要注意：`kind` 为空只有在协调视图新鲜时才等于「确实没有碰撞」，也就是 `coordination_fetch.success == true` 且 `coordination_ref_present == true`。如果这两个字段有一个不成立，空 `kind` 应该渲染成「未核实」，不能写成「无碰撞」。

**结论**：(A) 刷新心跳。(B) 不调用任何协调闸，但 claim 有 24 小时后被判 `abandoned` 的风险。(C) 心跳照刷，只是这次不会触发 Phase B 认领闸。
