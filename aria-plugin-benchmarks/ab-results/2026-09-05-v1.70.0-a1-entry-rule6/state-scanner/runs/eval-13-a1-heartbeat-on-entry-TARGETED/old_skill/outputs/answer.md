按你的要求，下面只回答、不跑任何命令。以下结论全部按 state-scanner SKILL.md v3.1.1 的成文契约推导（`enabled` 的实际取值需读 `.aria/config.json`，我没读，所以按你给的两种假设分别答）。

---

## 先说一个贯穿三问的前提

state-scanner 的入口路径是固定的三段：**Step 0 跑 `scan.py` → 阶段 1 读 snapshot → 阶段 2 推荐**。协调闸门 `phase1_gate` **不在这条入口路径上**。

SKILL.md「Layer L Phase B 集成」§编排契约写得很死：

> **接线点 = AI 编排层, 不是 `scan.py`**（layer-l-integration.md:15 Design A: 闸门仅在用户确认进 Phase B 时调用, 不在只读 collector 内自动跑）

调用时序也是四步，闸门在**用户确认之后**：

```
scan.py → snapshot (含 tracks_multibranch.collision.kind)
  → 阶段 2 推荐: AI 读 collision.kind + 读最新 handoff §6 选定 carry-id
  → 用户确认进入 Phase B (phase-b-developer B.1 / branch-manager)
  → AI 编排层经 subprocess 调 phase1_gate CLI
```

而闸门的触发条件是**两个条件的合取**，不是单看 `enabled`：

> 触发条件（默认开启, opt-out）: `state_scanner.coordination.enabled == true`（缺省即 true）**且** `tracks_multibranch.collision.kind` 非空（cross-owner / self_multi_container）

---

## (A) `enabled == true` 时，这次入口应该做什么

**1. 入口这一步只该跑一条命令 —— `scan.py`：**

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/scan.py" \
  --output .aria/state-snapshot.json
```

退出码契约：0 = 全部成功，读 snapshot 进阶段 2；10 = 部分软错误，读 snapshot 但对受影响子阶段展示 warning 后继续；20 / 30 = abort（不读 snapshot，展示 stderr）。

**2. 入口不该跑 `phase1_gate`。** 理由是上面的 Design A：只读扫描阶段不写 claim。而且按 (C) 给的条件（`collision.kind` 为空），合取条件的第二项本来就不成立 —— `enabled == true` 只满足了一半。

**3. 只有在「本次会话继续走到用户确认进入 Phase B」且 collision 非空时**，AI 编排层才在 Phase B 启动前跑这条（这就是你要的完整命令行）：

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
  --raw-track-id "<handoff §6 选定 carry-id 的原始串>" \
  --phase B \
  --mode advisory \
  --repo-path "/home/dev/Aria"
```

几点契约细节，别写错：

- `--raw-track-id` 传的是 **handoff §6 结构化 `{id, desc}` 里的 carry-id 原始串**，编排层**不预归一**（归一 `derive_track_id` 在 `run_gate` 内部做，R1-m6）。你给我的 `a1-entry-claim-duplicate-work-guard-023236f2` 是**已归一后的 track_id**，不是 carry-id 原始串 —— 按契约这里该传 §6 那个原始串。
- `--mode` 由 `state_scanner.coordination.mode` 决定，默认 `advisory`。别手写 `--mode block`：CLI 单次 JSON I/O 传不了活体 user_decision 回调，`block` 经 CLI 会退化为安全默认 abort（已知限制）。
- 可选 `--linked-issue <ref>`：会把 issue 写进 claim，并在输出 JSON 追加 `linked_issue_overlap[]`（同一件事两个 track-id 的 advisory 告警，🔴 提示但不阻断）。
- 输出解析 `{outcome, proceed, track_id, error, own_claim, competing_winner, surface, push_success}`；`proceed == true` 放行，`surface != null` 按 `surface.kind`（`occupied` / `clock_skew` / `push_failed`）分化渲染 🔴 告警行，不 blanket 静默。

**4. 关于你那条 heartbeat 停在 6 小时前的 active claim —— 我必须诚实说：按当前这版 SKILL.md，state-scanner 入口对它什么都不做，成文契约里没有「入口刷新/续期 heartbeat」这个动作。**

成文的 claim 生命周期只有三个写入点，没有一个挂在 scanner 入口上：

| 操作 | 调用方 | 时机 |
|------|--------|------|
| `acquire_claim` | `phase1_gate` | Phase B 启动前（且需 collision 非空才触发） |
| `heartbeat`（`update_heartbeat()`） | **`phase-b-developer` mid-cycle**，每 10 min（caller 负责调度） | Phase B 执行期间 |
| `release`（`release_gate.py`） | `phase-d-closer` D.2b 收尾 | cycle 完成 / 放弃 |

stale claim 的成文处置是 `release_gate.py --sweep-stale`（heartbeat 超 `STALE_TTL` 的 active → abandoned），由 phase-d-closer 侧调用，**不是 scanner 入口的职责**。

这有个现实后果值得你现在就知道：`STALE_TTL = 1800s`（30 min），你这条 heartbeat 停了 **6 小时 ≈ 12 倍 TTL**，在任何其他容器眼里它已经是 stale claim，下一次 `--sweep-stale` 会把它判成 `abandoned`。而按 (C) 的条件（无 collision），本次入口既不会给它续期，也不会清理它、甚至不会在推荐区提到它 —— 它对本次扫描是完全不可见的。

我的建议（这是我的判断，不是 SKILL.md 的规定，请你复议）：如果这条 track 确实还是你手上正在做的事，别指望 scanner 入口帮你续，要么走到 Phase B 让 phase-b-developer 的 mid-cycle heartbeat 接上，要么明确把它 release 掉再重新 acquire，避免留一条「看着 active、实则 12 倍超时」的僵尸 claim 去干扰别的容器的 reconcile 仲裁（reconcile 按 earliest `claimed_at` 胜）。这个「入口对自己容器的 stale claim 无感知、无动作」看起来是当前设计的一个真实缺口，值得开单。

---

## (B) `enabled == false` 时

**入口该做什么：还是只跑那条 `scan.py`，一模一样。**

差别在于协调侧的处置路径整体切换：

1. **对 `phase1_gate` / `run_gate` 是零调用。** SKILL.md 明写：`enabled == false`（显式 opt-out；Part A1 起默认为 true）→ **零调用 `run_gate`**，collision 改由推荐规则 **1.54 `concurrent_churn_detected`** 以 advisory 方式 surface。
2. **两态严格互斥，同一次 scan 绝不双触发**（#133 AC-2）：`enabled == true` 走闸门，`enabled == false` 走 rule 1.54，不存在既跑闸门又出 1.54 提示的情况。
3. **但在你这次的具体状态下，连 rule 1.54 也不会触发** —— 它的触发条件是 `tracks_multibranch.collision.kind != none` **且** `coordination_enabled == false`，而 (C) 说 collision 为空，第一项就挂了。所以这次入口的实际表现是：正常出 10 区块状态 + 推荐，协调相关的提示一条都没有。
4. **heartbeat 同样不做**：`enabled == false` 只是让协调机制整体不参与，它不会新增任何 claim 维护动作。你那条 6h stale claim 在这条分支下同样无人问津。
5. 顺带一提：rule 1.54 即便触发，也**不会自动改 config**（DEC-20260519-001 advisory-over-hardlock），只会提示你可以在 `.aria/config.json` 里手动打开：

```json
{ "state_scanner": { "coordination": { "enabled": true } } }
```

---

## (C) `collision.kind` 为空，会改变 (A) 的答案吗？

**分两层看，答案是「入口层不变，闸门层变」。**

**1. 对「本次入口该跑什么命令」—— 不改变。** 入口本来就只跑 `scan.py`，跟 collision 无关。这一层 (A)(B)(C) 三问的答案是同一个。

**2. 对「后续会不会跑 `phase1_gate`」—— 决定性地改变，而且是把它彻底关掉。** 触发条件是 `enabled == true` **AND** `collision.kind` 非空 的合取。collision 为空意味着第二项恒假，所以**即使 `enabled == true`，这次会话从入口到 Phase B 全程都不会调用 `phase1_gate`**。也就是说 (A) 里那条 `phase1_gate` 命令行，在你描述的这次实际状态下**不会被执行** —— 我把它写出来是回答你「该跑的完整命令行长什么样」，不是说这次该跑它。

**3. 连带后果（这是我认为你真正该关心的那一条）：**

- 不跑 `phase1_gate` ⇒ 不会 `acquire_claim` ⇒ 不会有任何 claim 写入或刷新；
- 不进 Phase B（或进了但没经闸门）⇒ phase-b-developer 的 10 min mid-cycle heartbeat 也不会给这条 track 续期；
- collision 为空 ⇒ rule 1.54 那条 advisory 也不触发。

**三条路径全部不触发，结论是：你那条 heartbeat 已停 6 小时的 active claim，在本次 `/aria:state-scanner` 入口里既不会被续期、不会被清理、也不会被提及。**如果你的预期是「跑一次 scanner 就能把自己容器的 claim 续上或至少告警一声」，那按当前这版 skill 的成文契约，这个预期不成立 —— 我不打算替它编一个不存在的机制。这一条建议记进 handoff 请你复议是否要补入口侧的 claim 自检。

---

### 小结（一句话版）

- 三种情况下，state-scanner 入口都**只跑 `scan.py --output .aria/state-snapshot.json`**，不跑闸门。
- `phase1_gate` 只在「`enabled == true` **且** collision 非空 **且** 用户已确认进 Phase B」三条同时成立时，由 AI 编排层调用；你这次 collision 为空，所以不会调用。
- `enabled == false` 时闸门零调用，改由 rule 1.54 advisory —— 但 collision 为空时它同样不触发。
- **入口没有任何 heartbeat 续期机制**；heartbeat 归 phase-b-developer mid-cycle，stale 清理归 phase-d-closer 的 `release_gate.py --sweep-stale`。你那条 6h claim（≈12× `STALE_TTL` 1800s）本次不会被处理，这是我认为需要你复议/开单的缺口。
