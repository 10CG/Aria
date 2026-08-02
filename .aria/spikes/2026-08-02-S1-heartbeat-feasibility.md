# Spike S1 — A.1 claim 的保护窗能不能做到 ≥72h?

> **母 Spec**: `openspec/changes/a1-entry-claim-duplicate-work-guard/` (spike-first 挂起)
> **触发**: post_spec R3/C1 —— R2-fix 判定「(i) heartbeat 更可取」, 而 R3 实证 heartbeat **在当前架构下不可按字面实现**。
> **执行**: 2026-08-02, 主控直接实读代码 + 生产 ref 取证 (不派 agent —— spike 是动手活)
> **结论形态**: 可证伪的三选一 + 支撑数据。**不写实现, 只答能不能 / 怎样才能。**

---

## 结论 (先给答案)

**选项 (b) 可行, 且在同一个文件里已有工作先例。** R2-fix 的「(i) heartbeat 更可取」判断**方向是对的但理由错了**, R3 的「不可按字面实现」**也只对了一半**。

| 选项 | 结论 | 依据 |
|---|---|---|
| (a) session_id 落盘复用 | ❌ **不需要** —— 被 (b) 完全取代, 且引入并发/过期新表面 | 见 §3 |
| **(b) heartbeat 匹配键改 `(container, track_id)`** | ✅ **可行, 有先例** | **`release_claim_by_track` 就是为同一个 defect 做的同款修法**, 见 §2 |
| (c) 只能延长 TTL | ❌ 非必需 | (b) 可行即无须动 TTL 语义 |
| **(d) 重新认领 (新发现, 不在原三选一里)** | ⚠️ **今天就已经在发生**, 但会累积记录 | 见 §4 —— 这条改变了问题的性质 |

---

## §1 事实基线 (实测)

**TTL 常量** (`lib/constants.py`):

| 常量 | 值 | 语义 |
|---|---|---|
| `HEARTBEAT_INTERVAL` | 600s (10min) | 期望的刷新周期 |
| `STALE_TTL` | 1800s (**30min**) | 超过即标 stale, 可被 takeover (不变量: `== 3 × HEARTBEAT_INTERVAL`) |
| `SWEEP_TTL` | 86400s (**24h**) | 超过即被 sweep 成 `abandoned` |

**heartbeat 现状** (`lib/claim_lifecycle.py:178-216` + `lib/constants.py:43-44`):

- 按 `(container_id, session_id)` 定位 —— 因为**存储路径就是 `claims/<container>/<session>.yaml`**, 是路径直查;
- `identity.py:252` 逐字:「**Each call returns a fresh value.**」⇒ 跨 subprocess 调用拿不到同一个 session_id;
- `constants.py:43-44` 逐字:「**NO production heartbeat loop exists (heartbeat() has zero production call sites; phase1_gate self-resume does not refresh either)**, so every live claim's heartbeat_at is frozen at acquire time.」
- grep 复核: `heartbeat()` **生产调用点 = 0** ✅ (R3 的这部分属实)

**事故窗** (母 Spec §3a): 第 4 次 ~48h / 第 5 次 ~72h。⇒ **`SWEEP_TTL` 24h < 事故窗**, 且 `STALE_TTL` 30min ≪ 事故窗。

---

## §2 决定性发现 —— 同一个 defect 已经被修过一次

`lib/claim_lifecycle.py:377-407` 的 `release_claim_by_track` docstring **逐字**:

> **Defect (c) fix (coordination-claim-lifecycle-and-overlap)**: `release_claim` locates by `(container, session)`, but a later ship/close invocation (phase-d-closer, on cycle completion) runs with a **FRESH `session_id`** and cannot match the original acquiring session — so claims never got released and accumulated as `active` forever. The ship context DOES know the `track_id` (the carry-id being closed), so this variant **locates by `(normalized track_id, container)` and ignores session**.

⇒ **这就是 S1 要解的同一个问题, 同一个根因, 已有同款解法在生产运行。**

**它顺带回答了 (b) 的两个实现细节**:

1. **一对多怎么办**: docstring 说「same container re-claimed a track across sessions — **the NORMAL case**, since every session mints a fresh session_id」⇒ 匹配到多条是常态。release 的选择是「**ALL matching active claims are released**」(review I1: 只放最早那条会让后来的仍 active)。heartbeat 的对偶选择应是**刷新全部匹配的 active claim** —— 同一理由。
2. **raw vs normalized**: 它对 `raw_track_id` 走 `derive_track_id` 归一后再匹配, 与 acquire 同一路径 ⇒ heartbeat-by-track 照抄即可, 无新归一表面。

**⇒ 选项 (b) 不是「需要设计」, 是「照抄隔壁函数」。** R2-fix 说它可取是对的; R3 说它「不可按字面实现」—— 准确说是**按 heartbeat 现有签名的字面**不可实现, 但换匹配键后可行, 且路径已被踩通。

---

## §3 为什么 (a) 不需要

选项 (a) 是「acquire 时把 session_id 落盘, 后续 heartbeat 读取复用」。它能工作, 但:

- 引入**新的并发面** (多 session 并行时谁的 id 落盘) 与**过期面** (落盘的 id 对应的 claim 已被 sweep 怎么办);
- 而 (b) **零新增状态** —— track_id 本来就是调用方已知的 (它就是 `--raw-track-id` 传进来的那个);
- 项目已经为**完全相同的问题**选了 (b) 的路 (release 侧)。两侧用不同解法徒增不一致。

**⇒ (a) 判否, 理由不是「做不到」而是「(b) 更省且已有先例」。**

---

## §4 ⚠️ 新发现: 问题的性质与三选一的预设不同

**每次调 `phase1_gate` 都会写一条新 claim** —— 存储路径含 `session`, 而 session 每次新生成。生产 ref 实证:

```
claims/023236f2/  → 7 条 (本容器)
claims/bfe8285d/  → 20+ 条 (并发轨容器)
```

⇒ **A.1 期间只要 AI 再调一次 phase1_gate, 就自然产生一条 `claimed_at`/`heartbeat_at` 全新的 claim** —— 保护窗事实上被「重新认领」续上了。

**这改变了 S1 的问题陈述**: 原问题是「怎么让一条 claim 活过 72h」; 真实问题是「**怎么保证 A.1 期间会有周期性的再调用**」。

- 若 A.1 流程本身包含多个 phase1_gate 触点 (如每次实质推进前重扫 —— 那正是母 Spec 要建的纪律), 则 (d) 天然成立, **连 (b) 都可能不需要**;
- 但 (d) 的代价是**记录累积** (已经 27+ 条); 且它依赖「AI 记得再调」—— **而 AI 记不住正是本 Spec 存在的理由** (母 Spec §Why 自证: 起草者 08-02 为 #124 认领却忘了为本轨认领)。

**⇒ 建议组合**: 主用 **(b)** (机械, 不依赖 AI 记性), (d) 作为自然冗余。**不要**只靠 (d)。

---

## §5 给母 Spec 重写时的可执行结论

1. **C3 的处置定为 (b)**: heartbeat 匹配键改 `(container_id, normalized track_id)`, 刷新**全部**匹配的 active claim, 归一走 `derive_track_id` —— 逐条照 `release_claim_by_track` 的既有实现。
2. **Impact 表须补** `lib/claim_lifecycle.py` (R3 指出原表零覆盖); **不需要**补 `lib/identity.py` (因为不走 (a))。
3. **不动 TTL 常量** —— `STALE_TTL`/`SWEEP_TTL` 语义保持, 由 heartbeat 续期。
4. **`heartbeat()` 现有签名保留**, 新增 by-track 变体 (仿 `release_claim` / `release_claim_by_track` 的并存模式), 避免动既有调用方 —— 虽然现在是 0 个。
5. **SC 须覆盖**: (i) 跨 subprocess 两次调用能刷新同一 track 的 claim; (ii) 一对多时全部刷新; (iii) 超 `SWEEP_TTL` 未刷新仍被 sweep (不许 heartbeat 变成永不过期)。

## §6 本 spike 未回答的

- **heartbeat 该由谁在什么时机调** —— 这是 SKILL.md 指令面设计, 属 Spec 范围不属 spike;
- **(d) 的记录累积要不要治** (27+ 条已在 ref 里) —— 与 `--gc` / retention 相关, 建议单独评估。
