---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-05T16:28:28.808Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R4 处置核对

对照本席 R4 报告 (`.aria/audit-reports/post_spec-R4-2026-09-05T155052-857Z-owner-container-identity-key-and-collision-parser-backend-architect.md`) 的唯一 Finding R4-1 (minor / `tracks_by_tid` 索引键用未剥离原始 `track_id`, 与 `verdicts` 键域在 D-0(a) 剥离后分叉)，在 v5 (`681e872`) 上核对：

**closed**。逐项核实：

1. **proposal 文本是否已成文该缝隙**——v5 三处一致点名：D1 族键段 (`:35`)「渲染器 `tracks_by_tid` 标签索引须用同一剥离后键构造 (T8)」；Impact Risk 表 (7) (`:98`)「D-0(a) 日期形尾段被剥; 渲染器 `tracks_by_tid` 索引若未随剥离归一会退化标签 (T8 锁)」；Tasks T8 (`:113`)「D-0(a) 时 `tracks_by_tid` 标签索引改用剥离后键 (与 `verdicts` 键域一致)」。三处文本相互一致，指向同一修复方向，未出现表述分叉。
2. **该修复在代码位置是否可行**——实读 `aria/skills/state-scanner/scripts/renderers/track_board.py:778-793`：`claim_records` 构造 (`:779-784`, 逐项 `try: rec = _track_to_claim_record(t) / except ValueError: continue`) 与 `tracks_by_tid` 构造 (`:786-790`, 逐项 `tid = t.get("track_id") or ""`) 是**同一 `all_collidable` 列表上的两条独立循环**，彼此不共享中间结果。要让 `tracks_by_tid` 改用剥离后键，最小改法是把两条循环合并成一条：在成功转换出 `rec` 之后，用 `rec.track_id`（而非重新从 `t` 取原始字段）建 `tracks_by_tid` 索引——`tracks_by_tid.setdefault(rec.track_id, []).append(t)`，同时把失败项的 `continue` 语义带过去（转换失败的 track 本来就不会进 `claim_records`/`verdicts`，让它也不进 `tracks_by_tid` 是与键域完全对齐的正确行为，不是新增副作用）。这是在现有代码结构上的局部重排，不需要新函数、不需要改 `_track_to_claim_record` 签名。**可行**。
3. **与 `verdicts` 键域是否一致**——实读 `aria/skills/state-scanner/lib/reconcile.py:347-374`（`reconcile_all`）：`grouped.setdefault(claim.track_id, []).append(claim)` 后 `return {track_id: reconcile(...) for track_id, group in grouped.items()}`——`verdicts` 的键就是 `ClaimRecord.track_id` 本身，即 `_track_to_claim_record` 返回值的 `.track_id` 字段（D-0(a) 落地后即剥离后的值）。按 (2) 的改法用 `rec.track_id` 建 `tracks_by_tid`，两个字典的键域字面上来自同一次转换调用的同一属性，天然同源、不可能分叉。**一致**。

T8 文本给出的方向在代码上确认可行、且与 `verdicts` 键域天然对齐（不是需要额外校验的巧合对齐，而是复用同一转换结果的结构性对齐）。这条 v4/R4 遗留的 minor 在 v5 上已经从「proposal 未提及」升级为「三处文本 + 可执行任务 + 明确的目标键域」，达到 Level 2 粒度所需的成文深度。

**R4 处置三态计数：closed 1 / partial 0 / open 0**（本席 R4 仅此一条 finding）。

## 审计结论

### 镜头 1：SC-2 advisory「生产接线端到端」子句 —— 缺同 `track_id` 前提（新 minor，与 code-reviewer R5-m4 独立复现一致）

- **scope**: proposal `:123` SC-2 「生产接线端到端」句；对照 `aria/skills/state-scanner/scripts/collectors/handoff_multibranch.py:512-524`（`dedupe_latest_per_track_container` 的分组键构造）。
- **实读**: `handoff_multibranch.py:512-524`——`key = (t.get("track_id"), owner, container)`（改后即 `(track_id, identity_key)`，`:33` 显式改动点）——折叠**只在同一 `track_id` 分组内**发生（`groups.setdefault(key, []).append(t)` 的 `key` 首段永远是 `track_id`）。而 `identity_drift_advisories` 按 `:47` 的定义是对「collector 的全部非 legacy 行（dedupe 前，**跨 track**）」按 `identity_key` 聚合、不看 `track_id`。
- **推导**: SC-2 生产接线端到端句要求的反事实是「把 `:709` 的入参从 `tracks`（原始、dedupe 前）换成 `deduped_tracks` 后，advisory 从 1 变 0（红）」。这个反事实要成立，必须真的发生一次**折叠**——即两份 handoff 在 dedupe 之后合并成一行，使得 `identity_drift_advisories` 少看到一次 owner 出现。但折叠的前提是两份 handoff **同 `track_id`**（上一段实读确认）。若 SC-2 描述的夹具「两份 handoff 两串」落在两个不同的 `track_id`（proposal 原文未排除这种构造，也未显式要求同 `track_id`），`dedupe_latest_per_track_container` 不会折叠它们——`deduped_tracks` 里两行原样保留，`identity_drift_advisories(deduped_tracks)` 仍会在同一 `identity_key` 下看到 2 个 owner 串，advisory 计数仍是 1，不会变成 0。此时「接线反事实 → 0，红」这句断言本身不成立，测试作者在按字面实现该反事实分支时会立即撞见「期望 0 实得 1」的矛盾。
- **与 code-reviewer R5-m4 的关系**: 本席独立实读同一份 `dedupe_latest_per_track_container` 得到相同结论（对方报告 `.aria/audit-reports/post_spec-R5-2026-09-05T162828-808Z-owner-container-identity-key-and-collision-parser-code-reviewer.md` 的 R5-m4），两席收敛一致，判为同一条 finding 而非各自独立计数。
- **是否升级为 Major**: 不升级。理由——(a) advisory 的**正向断言**（「两份 handoff 两串 → snapshot `identity_advisories` 恰 1 条」）与 `track_id` 是否相同无关（`identity_drift_advisories` 定义就是跨 track 聚合），这条不受影响，能在 B.2 直接落地为绿；(b) 只有**反事实分支**（验证接线正确性的对照实验）依赖同 `track_id` 前提，且该依赖在测试作者按字面构造 fixture 时会**立即自曝**（断言从预期的红变成不红，而不是静默维持假绿）——不存在「测试写完、CI 全绿、但反事实其实没测到东西」的隐蔽假绿路径；(c) 不影响 SC-2 判定臂（前四条）、不影响 D-0~D-3 的裁定基础、不阻塞 B.1 入口。
- **最小修法（B 期顺手项）**: 在 SC-2「生产接线端到端」句的夹具描述里加一个从句，锁定「两份 handoff 落同一 `track_id`」这一前提，例如把 `:123` 现有的「真实 collector 夹具（`_build_repo` 风格, uuid 形容器 `aaaa1111` 而非 `box-A`）两份 handoff 两串」改为「…（`_build_repo` 风格, uuid 形容器 `aaaa1111` 而非 `box-A`, **两份 handoff 落同一 `track_id`**）两串」。一句话插入，不改判定臂、不改其余四条断言。

### 镜头 2：T8 `tracks_by_tid` 索引键可行性 —— 见上方「R4 处置核对」，closed，不重复计数。

### 镜头 3：投票

除上述 1 条 minor（镜头 1，与 code-reviewer 独立复现一致）外，未发现新的 Critical/Major。该 minor 具备自曝性（测试作者按字面构造反事实 fixture 时会立即撞见断言不成立，不构成静默假绿路径），且修法是单句插入、不触及判定臂/D-0~D-3 裁定基础，可在 B 期顺手处理，不构成阻塞本轮收敛的理由。

## Verdict

PASS_WITH_WARNINGS — 0 Critical + 0 Major + 1 Minor（0C/0M/1m）。R4-1 已 closed。

## Vote

PASS

## 轮次记录

**读了什么**: proposal.md v5 全文相关段落（Why/D1 全段含族键剥离句/实验表/D-0(a)/Impact Risk 表 (7)/Tasks T7-T9/SC-2/SC-10/代码落点索引）；本席 R4 报告全文；code-reviewer R5 报告全文（核对 R5-m4 与本席独立发现是否收敛一致）；`aria/skills/state-scanner/scripts/collectors/handoff_multibranch.py:490-560`（`dedupe_latest_per_track_container` 全函数, 分组键 `:512-524` 逐字核对）；`aria/skills/state-scanner/lib/collision.py:86-140`（`track_to_claim_record` 全函数, 当前未做 D-0(a) 剥离, 确认该剥离是本 Spec 待落地项非既有行为）；`aria/skills/state-scanner/lib/reconcile.py:347-374`（`reconcile_all` 全函数, 确认 `verdicts` 键 = `ClaimRecord.track_id`）；`aria/skills/state-scanner/scripts/renderers/track_board.py:760-800`（`claim_records`/`tracks_by_tid` 两条并列循环全段, 逐行核对当前实现与 T8 目标的结构差异）。

**跑了什么**: 无需额外脚本；本轮判据靠逐行代码实读 + 与 R4/code-reviewer 报告交叉核对完成。

**未发现问题的项**: T8 修复方向在代码结构上可行（合并两条循环, 复用 `rec.track_id`）且与 `verdicts` 键域天然同源, 不是需要额外校验的巧合对齐；SC-2 判定臂前四条与「两份 handoff 两串 → advisory 恰 1」正向断言均不受同 `track_id` 缺口影响；D1/Risk(7)/T8 三处文本相互一致, 无表述分叉。
