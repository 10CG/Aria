# owner-container 身份键与 collision 解析器修正 (合并处置 Aria #193 + aria-plugin #135 缺口 3)

> **Level**: Minimal (Level 2 Spec) — **owner 2026-09-05 指令为 Level 2**。执笔按 SOT 判据 (`standards/core/ten-step-cycle/phase-a-spec-planning.md:126-137`, 三项性质任一为 Yes → Level 3) 逐项自评: architecture = **否** (不引入新原语, 改一个 collector 内部判定 + 一个 lib 函数的输入契约); cross-module = **是** (aria 子模块 + standards 子模块, 且 `identity.py` 语义面被 claim 目录结构共同消费); breaking = **否** (`collision.kind` 枚举取值不变, snapshot 字段 additive, §2.3.5 判据变更经 owner 决策点显式裁定)。**按流程图 cross-module 即 Level 3** —— 执笔结论: 判据上是 Level 3。owner 维持 Level 2 即为显式 override (Rule #10: Level 由 owner 决定, 执笔不自行上下调), 请在批准时二选一并回填本行。
> **Status**: Draft **v3** (post_spec R2 五席 FAIL/REVISE 后 rework, 2026-09-05; R1/R2 聚合见 §References)。**v3 撤销了 v2 引入的「owner 等价类」机制** (R2 五席从不可逆 / 语料依赖 / 无数据通路 / 空 owner 未定义 / 零 baseline-failing SC 五个方向证伪), 回到纯输入的确定性规则。
> **Created**: 2026-09-05
> **Linked Issue**: `10CG/Aria#193, 10CG/aria-plugin#135`
> **Track / claim**: `owner-container-identity-key-and-collision-parser` (phase A claim `s-8204@1355`, container `bfe8285d`, linked_issue `10CG/Aria#193`, overlap 告警空)
> **代码落点**: `aria/` 子模块 (state-scanner `lib/` + collector + renderer + references; phase-d-closer `fetch_gate.py` 测试) + `standards/` 子模块 (session-handoff.md §2.3); Spec 落主仓 (Rule #5)
> **Triage 依据**: `.aria/triage-report.json` / [#193 comment 21431](https://forgejo.10cg.pub/10CG/Aria/issues/193#issuecomment-21431) (partial-repro / major / next-cycle)
> **冻结语料**: `.aria/repro/handoff-tracks-frozen-2026-09-05.json` (起草日 `tracks_multibranch.tracks[]` 非 legacy 行, 996 行, 已纳入版本控制; 实验表与 SC-6 都对它跑)
> **相邻在飞 Spec**: [`a1-entry-claim-duplicate-work-guard`](../a1-entry-claim-duplicate-work-guard/proposal.md) (对方容器 `023236f2`, 待 B.1) — 其 §3 已把「`owner-container` 与 claim container 段口径不同, 两标识关系需成文」记为 follow-up 且明示不在其内统一; 本 Spec 即该 follow-up。**两处耦合**: (1) `identity.py` flip 与其 SC-3 (§Impact 排序); (2) **其 track-id 含 `<container_uuid>` 段, 与本 Spec 的同 track 分组正面冲突 (决策点 D-0)**。

## Why

多终端协调的唯一 advisory 信号 `tracks_multibranch.collision` 目前不可信, 原因有三层:

1. **解析器格式契约错位 (triage 新发现, 主根因)**: `lib/collision.py::split_owner_container` 按三段式 `owner/container/session` 解析 (契约起点 aria `f9306a0` 2026-05-20 `track_board.py`, `83a1a45` 05-30 迁入 `collision.py`), 而 handoff frontmatter 按 `session-handoff.md §2.3.1` 是两段式 `<owner>/<container-id>` (主仓 154 份 frontmatter: 142 两段 / 12 零段 / **0 三段**)。两段串被拆成 `(owner='', container=<owner 段>, session=<uuid>)` ⇒ `owner` 恒 `unknown` ⇒ `cross_owner` 从 handoff 数据**永远不可达**。直接调用复现 (triage case-2..5): 同容器双 owner 串 → 🟡; **真两人两机 → 也是 🟡 (降级)**; **同人两机 → `none` (漏报)**; 三段式串才得 🔴。
2. **owner 段随 git 身份漂移 (Aria #193)**: 同一物理容器 `git user.email` 变更后机械填规则忠实记录 → 同一 container 出现多个 owner 串。两个 uuid 容器都发生且方向相反: `bfe8285d` = `simonfish/…` 34 份 (07-05..08-27) + `aria-runner-bot/…` 2 份 (09-03..), 漂移点在 08-26/08-27 之间; `023236f2` = `aria-runner-bot/…` 23 份 (07-05..08-16) + `simonfish/…` 17 份 (07-03..09-05)。Aria 现行规范只定义 `<owner>` = git `user.email` local-part, **没有 AI runner 该以什么 git 身份提交的规范**。附带事实: Aether 的机器账号已于 2026-07-01 从 `aria-runner-bot` 改名 `10cg-ci-bot`, 本容器现用的 local-part `aria-runner-bot` 本身是旧名 (D-2 后果之一)。
3. **container 段来源不稳 (aria-plugin #135 缺口 3 + 08-13 补充)**: container 段先后是主机名 (`dev-claude` / `dev-claude2`, 跨机不唯一) 与 uuid (`bfe8285d` / `023236f2` / `f9c6e8cd`); `lib/identity.py::get_container_id()` 是 `label if label else uuid`, 文件头注释又邀请填 label ⇒ 填个可读名就静默换了协调身份 (08-12 实测 `claim_not_found` 孤儿 claim)。主仓 frontmatter 今天是 **10 种 owner-container 串, 5 个 container 标识 (3 uuid + 2 主机名), 实际 2 台在用机器**。

**为什么三层一起处置 (冻结语料 + 生产路径 `collector dedupe → classify` 实测)**: 只修第 1 层会把「静默失灵」换成「响亮误报」—— 主机名时代同一 owner 的两台机 (`simonfish/dev-claude` vs `simonfish/dev-claude2`) 与零段/两段混写的同一台机 (`dev-claude` vs `simonfishgit/dev-claude`) 立刻被判 🔴。第 2/3 层给出身份键与「不可归属 owner 不计数」两条**确定性**规则后, 这两组回到 🟡; 而漂移造成的「两个提交身份」在数据上就是两个身份, 本 Spec **不再推断它们是不是同一个人** (v2 的等价类正是这么做而失败的), 而是判 🔴 并用 ⚪ 漂移 advisory 并排解释, 由 D-2 停止未来漂移。

## What

四个交付面 (代码 / 规范 / 看板告警 / 消费文档同步), 四项 owner 决策点 (D-0 ~ D-3)。

### Key Deliverables

**D1 — 解析器、身份键、判定键 (aria: `lib/collision.py` + `handoff_multibranch.py` + `track_board.py` + `lib/identity.py`)** — 全部是**纯输入函数**, 不读语料历史、不持久化状态:

- **解析**: `split_owner_container` 按两段式: `<owner>/<container>` → `(owner, container, "")`; 三段式 (Layer L `superseded_from` 形, 不经此函数校验) 保持 `(owner, container, session)`; 零段 → `("", <串>, "")`。规范不改三段 (frontmatter 无 session 概念, §2.3.6 写入频度 = 会话结束一次)。
- **身份键** `identity_key(owner, container)`: container 匹配 `^[0-9a-f]{8}$` ⇒ `container` (uuid 全局唯一, owner 不参与同一性); 否则 (主机名 / 空 / 只读 fs 兜底) ⇒ `owner + "/" + container` (主机名跨机不唯一, 保留 owner 段区分)。**已知限制** (成文): 兜底 hostname 或用户 label 恰为 8 位小写 hex 会被当 uuid; 该路径本身是降级路径, 且 D3 advisory 可见。
- **dedupe 键** (`handoff_multibranch.py:518-523`, **显式改动**) = `(track_id, identity_key)`: 同 uuid 容器多 owner 串折叠为最新一行; 主机名容器保留 owner 段 (既有测试 `test_owner_segment_participates_in_grouping_key` 的不变式只在主机名域成立, 改写为两臂)。
- **判定** `classify_claims` (签名不变): 同 track 的 active 行 (dedupe 后) 按 `identity_key` 计数: `<2` → `none`; `≥2` 时取 **非空且非 `unknown`** 的 owner 串集合 (空 owner = 不可归属, **不计为独立 owner**): 集合大小 `≥2` → `cross_owner`; `≤1` → `self_multi_container`。**没有「同一个人」推断**: 两个不同 owner 串在两个 uuid 容器上 = 两个提交身份 = 🔴, 即使 D3 显示它们曾在同一容器共现 (那是给人看的解释, 不是判定输入)。
- **board 标签** (`track_board.py:412-417`, **显式改动**): 建表键与查表键同源归一 (都经 `track_to_claim_record` 的 `"unknown"` 填充), 修掉今天就查不中的 bug。
- **`lib/identity.py`**: 新增 `get_container_label()`; `get_container_id()` 改 uuid 优先 (只读 fs 兜底仍 hostname, 不写「恒 uuid」); **落地时机受 §Impact 排序约束 (S1/S2 两种 ship 形态)**。flip 前一次性迁移检查 (T3b) **挂在 `phase1_gate` / `release_gate` 启动路径** (它们本就读 coordination ref), 不进 `identity.py` (保持零依赖、零子进程): 若 container-id `label` 非空且 `claims/<label>/` 有 active ⇒ 输出告警并拒绝在本次运行 flip 语义 (走旧口径), 直到 release/迁移完成。

**D2 — 规范成文 (standards, `session-handoff.md §2.3`)** — 判据用**标准自身定义的词**写, 不引用 aria 代码:
- §2.3.1 `owner-container` 行改写为三态 + 规则: `<owner>` 语义按 D-1; `<container-id>` = `~/.aria/container-id` 的 **uuid 字段** (v1.22.x+ 有该文件的机器; label 不参与); 无该文件的历史行 = 主机名; 只读 fs 兜底 = hostname。**并在此定义 `identity_key`**: 8 位小写 hex 形 ⇒ 该串本身; 否则 ⇒ `<owner>/<container-id>`。
- §2.3.5 判据表 (**实质变更**, 对采用方是行为变更, 在 standards 变更说明 + aria CHANGELOG 明示): `cross-owner` = 同 track ≥2 个 `identity_key` 且非空 `<owner>` 集合 ≥2 → 🔴; `self-multi-container` = ≥2 个 `identity_key` 且非空 `<owner>` 集合 ≤1 → 🟡; 新增 **`same-identity-multi-owner`** = 同一 `identity_key` 在语料中出现 ≥2 个 `<owner>` → ⚪ 信息级 advisory (git 身份漂移), 不计入 collision。
- **新增 §2.3.9**「AI runner 提交身份」(§2.3.7/§2.3.8 已占用): 按 D-2 裁定写入 Aria 侧规则; 只写「采用方的人机账号治理与容器 `git config` 供给不在本规范」, **不引用任何 Lab 私有文档**; 10CG Lab 内部指针 (Aether 两账号模型) 放 Aria 主仓 `docs/` (D 期 closeout), 不进 standards。
- 历史 handoff **不 rewrite** (与 Kairos DEC-2026-09-04 一致)。

**D3 — 漂移 advisory (aria: 新 lib 函数 + collector + renderer + schema)**
- 新增 `lib/collision.py::identity_drift_advisories(tracks) -> list[dict]`: 输入 = collector 的**全部非 legacy 行 (dedupe 前)**, 输出每个出现 ≥2 个非空 owner 串的 uuid `identity_key`: `{identity_key, owners[], first_seen, last_seen}`。**`classify()` / `classify_claims()` 签名不变**; collector 在 `handoff_multibranch.py:709` dedupe **之前**对原始 `tracks` 调用它, 写入 `tracks_multibranch.collision.identity_advisories[]` (additive); 渲染器 `track_board.py` 已持有原始 `tracks` (`:176-183` 它自己 dedupe), 同样调用该函数渲染 ⚪ 行 —— 两处同源, 不重开 collector/renderer 分叉。legacy 行 (`owner_container == "unknown"`) 不参与 (SC 锁)。D-3 的新鲜度截止**不**作用于 advisory (它是漂移史, 不是活跃信号)。
- 与 #182 的关系是**依赖**: `track_to_claim_record` 把 `active`/`legacy` 与 **8 种非 enum status (`complete` 119 / `closed` 64 / `in_progress` 40 / `ship_ready` 16 / `superseded` 16 / `blocked` 10 / `paused` 8 / `partial` 7 = 280/996 行)** 一律映射为 active (`collision.py:113-124`), 其中 104 行 `active` 最早 2026-05-20, 全部远超 `STALE_TTL=1800` 却仍被 `:374-379` 捞回参与判定。本 Spec 修的是**分类逻辑正确性**; 信号**可用性**由 D-3 裁定; 非 enum status 的终态归一属 #182, 本 Spec 只记数字不改映射。

**D4 — 消费文档与消费代码同步 (aria)** — `collision.kind` 枚举取值不变, 但真实数据上的命中面变了 (`cross_owner` 首次可达):
- 文档: `references/layer-l-integration.md:25-27,73,77` · `RECOMMENDATION_RULES.md:31` (rule 1.54) · `references/rules/advanced-rules.md:544-572` · `references/state-snapshot-schema.md:1085` (collision 段 + 新字段) · `references/phase-1-collectors.md:75`。`SKILL.md:149-154` 只引用字段名不引用取值, 不在同步面 (Rule #6 零 SKILL.md 改动成立)。
- 代码消费方: `aria/skills/phase-d-closer/scripts/fetch_gate.py:251` (`collision_kind != "none"` → advisory) + `tests/test_fetch_gate.py` (硬编码枚举字面) —— 行为不变, 加一条真实两段式 `cross_owner` 夹具确认 advisory 文案。

### 实验表 (冻结语料 996 行, **生产路径** `dedupe_latest_per_track_container → classify`, 2026-09-05 实跑)

| 变体 | dedupe | `collision.kind` | groups |
|---|---|---|---|
| A 现状 (三段式解析, 现 dedupe 键) | 996→121 | self_multi_container | `[dev-claude, simonfishgit/dev-claude]` |
| B 只修解析 | 996→122 | **cross_owner (误报)** | 上组 + `[simonfish/dev-claude, simonfish/dev-claude2]` |
| **v3 D1 全套** (解析 + identity_key dedupe + 不可归属规则) | 996→122 | self_multi_container | 同 B 的两组, 均 🟡 (主机名时代同一 owner 两机 / 同一机零段+两段混写) |

合成用例 (经 dedupe → classify, 与语料无关, 结果确定): 两人两机 `alice/aaaa1111` + `bob/bbbb2222` → **cross_owner**; 同容器双 owner `simonfish/bfe8285d` + `aria-runner-bot/bfe8285d` → **none** (+ 1 条 advisory); 同人两机 `simonfish/bfe8285d` + `simonfish/023236f2` → self_multi_container; 漂移后 `aria-runner-bot/bfe8285d` + `simonfish/023236f2` → **cross_owner** (两个提交身份, 诚实 🔴 + advisory 解释); 既有隔离夹具对 `aria-runner-bot/023236f2` + `simonfish/bfe8285d` → **cross_owner** (该测试期望改写, 见 T4); 零段 vs 两段同主机名 → self_multi_container; 两人先后共用一机 `erin/eeeeeeee` + `frank/eeeeeeee` → none (+ advisory)。

D3 advisory 对象 (冻结语料): `023236f2: [aria-runner-bot, simonfish]` · `bfe8285d: [aria-runner-bot, simonfish]`。**结论**: 真实语料里没有真正的两人撞车; 修后两组 🟡 都是 2026-05..07 的 stale 行 (#182 形态), 可全部归因 (SC-6)。

## 决策点 (owner; 未预设; D-0 须在 B.1 前裁定, 其余裁定后回填 D2)

**D-0 与 a1-entry 的 track-id 契约冲突 (R2 tech-lead C-1)** — a1-entry 把 A.1 派生串定为 `<spec-slug>-<container_uuid>` 并规定它就是 carry-id; `session-handoff.md §2.3.8.2` 要求 carry-id 与 frontmatter `track-id` 同串 ⇒ 两容器对同一 Spec 写出的 handoff 落**不同** `track_id`, 本 Spec 的全部判定 (在 `track_id` 内, `collision.py:363`) 对 A.1 认领的 Spec 恒 `none`。
- (a) **本 Spec 加「track 族键」**: 分组键 = `track_id` 去掉尾部 `-<8hex>` 段 (仅当该 8hex 是语料中出现过的 `identity_key`) —— Aria 侧可独立落地, 确定性, 不改 a1-entry 契约。后果: 多一条派生规则要写进 §2.3.1 (track-id 尾段语义); 两容器对同一 Spec 各自认领时 Layer H 仍能报 🔴/🟡。
- (b) **请 a1-entry 把容器段留在 claim raw id, 不写进 frontmatter `track-id`** —— 跨 Spec 改动, 需对方容器同意且其已过 R6 收敛。后果: 本 Spec 零改动, 但依赖对方返工。
- (c) **接受 A.1 认领的 Spec 不走 Layer H collision**, 只靠 Layer L overlap (a1-entry 的主机制)。后果: Layer H 看板对新 Spec 失去 🔴/🟡, 只剩 handoff 接棒功能。
- 执笔建议: (a), 并在 Aria #174 留言征求 a1-entry 侧意见 (不是知会)。

**D-1 `<owner>` 段语义** (与 D-2 **耦合**, 请一起裁)
- (a) **提交身份** (现状: git `user.email` local-part; 机械可得, 零配置)。后果: 同一人换 email 就是另一个 owner 串 ⇒ 与其他容器并存时判 🔴 (诚实但需人读 ⚪ advisory 才知是漂移); D-2(a) 生效后新漂移停止, 历史双串靠「不 rewrite + dedupe 取最新行」自然淡出。
- (b) **人** (需 `owner-map` 映射表)。后果: 分类不受漂移影响; 但引入常驻维护面, 跨采用方不可移植, 与 Aria「不要求采用方维护身份数据」定位相悖。
- 执笔建议: (a)。代价是历史漂移期的 🔴 需要人看 ⚪ 行, 收益是零状态、零推断、跨容器结果一致。

**D-2 AI runner 的 git 提交身份**
- (a) **统一机身份**: 所有 AI 会话 commit 署同一 bot local-part。收益: owner 段稳定; 与 Aether「人 / 机」两账号对齐 (AI runner 归机器一类)。**代价**: (1) 与 D-1(a) 叠加后, **同一 owner 的 AI 会话之间 `cross_owner` 结构性不可达** —— 🔴 的真实含义变成「另一个提交身份」(另一位操作者的容器 / 人手工署名的会话), Positive 只能条件成立; (2) commit 署名失去「哪位操作者在场」, 须靠 handoff / claim 的 container 段追溯; (3) bot 名要选: Aether 已把 `aria-runner-bot` 改名 `10cg-ci-bot` (2026-07-01), 沿用旧名会与 Aether 台账不一致, 改名则本容器又漂移一次 (一次性, D3 可解释)。
- (b) **人身份** (沿用操作者 email)。收益: 署名可追溯到人; 两位操作者之间 🔴 可达。代价: 与 Layer 2 生产侧 (bot) 不一致; 操作者换 email 即漂移。
- (c) **不规定**。收益: 零改动。代价: 漂移继续, ⚪ 常亮。
- 执笔建议: (a) 且 local-part 与 Aether 现名一致; 「操作者可追溯性由 container 段 + handoff 承担」写进 §2.3.9。范围边界: 本 Spec 只写 Aria 侧规则; 容器 `git config` 供给 (10cglocal) 与 Aether 账号治理不在范围。

**D-3 Layer H 新鲜度截止 (回应 #182 依赖)**
- (a) **本 Spec 内加截止**: `updated-at` 早于 N 天 (建议 30) 的行在 Layer H 记录构造阶段直接不进 reconcile/classify (人口 = 被映射为 active 的全部行, 含 280 行非 enum), board 以「stale」列出; **不与 `:374-379` 叠成三档** (被截止的行 reconcile 看不到)。后果: 信号 ship 即可用; 新增一个常量 (`lib/constants.py`, 与 `STALE_TTL` 分开命名与量纲) + 一条规范句。
- (b) **不加, 交 #182**。后果: 本 Spec 只保证逻辑正确, board 上仍有 2026-05 的 🟡 组, Positive 只能写「逻辑正确」。
- 执笔建议: (a)。#182 无人认领 (对方容器 M4 队列末位), 等它意味着主要收益延期不定。

## Impact

| Type | Description |
|------|-------------|
| **Positive (条件式)** | 分类逻辑第一次同时满足: **不同提交身份**跨容器并存 = 🔴 (不再降级); 同一提交身份多机 = 🟡 (不再漏报); 同容器多 owner 串 = ⚪ 显式告警 (不再静默); Layer H 与 Layer L 的 container 口径统一为 uuid。**条件**: D-1(a)+D-2(a) 下 🔴 = 「另一提交身份」而非「另一个人」; **信号可用性**取决于 D-3 (选 (a) ship 即可用); **label 陷阱结构性消除**只在 S2 形态成立 (见排序), S1 形态下由 T3b 检查 + ⚪ 缓解 |
| **Risk** | (1) §2.3.5 判据实质变更 + dedupe 键变更 ⇒ 采用方看板输出改变 (实验表 A→v3: 组数 1→2, 都是 stale 🟡); 缓解: SC-6 逐组归因 + standards 变更说明 + aria CHANGELOG。(2) reconcile tie-break 键 `container/session` 两段式下退化为 `container/unknown`, `claimed_at` 全同的同容器两行退回输入顺序; Layer H `claimed_at` 是秒级 `updated-at`, 实践不出现; 加 SC 锁「不崩溃」。(3) `oc_by_tid_key` 三元组在未 dedupe 输入上可撞键; 生产路径恒先 dedupe, SC 锁契约注释。(4) 8 位 hex 主机名/label 被当 uuid (已知限制, 见 D1)。(5) 漂移期历史 🔴 需人读 ⚪ 行 (D-1(a) 已述) |
| **`get_container_id()` 消费方 (全列)** | `lib/identity.py::get_identity()` → `lib/claim_lifecycle.py:39,88` / `scripts/phase1_gate.py:294` (winner 归属) 与 `:486` (调用点) / `lib/concurrent_tracks.py:25,133` / `scripts/release_gate.py:132` (间接, 按 container 定位 claim) / session-closer `handoff_autofill.py:391` (`def owner_container`, frontmatter 机械填)。flip 影响面即这六处; T3b 覆盖迁移期 |
| **与 a1-entry 的边界与两种 ship 形态** | 耦合 1 (`identity.py`): a1-entry 新增 `get_container_uuid()` (:660), 其 SC-3 (:571) 以「`get_container_id()` label 优先 ⇒ 直接调它的实现必红」为前提, 本 Spec flip 会让它恒绿 (语义耦合, rebase 不报冲突)。**S1 形态 (a1-entry 未落地时 ship)**: 只加 `get_container_label()` + T3b 检查, **不 flip**; label 陷阱不消除 (Positive 已条件化)。**S2 形态 (a1-entry B.2 已落地且对方在 #174 ack 改写其 SC-3)**: flip + 由本 Spec 改写其 SC-3 为「`get_container_uuid()` 与 flip 后 `get_container_id()` 同值; label 只在 `get_container_label()`」。未取得 ack 不动对方文本。耦合 2 (track-id 容器段): 见 D-0, B.1 前须裁定。行号漂移: 后落地方在 D 期 refresh |
| **Rule #6** | 不改任何 SKILL.md 指令面 / description ⇒ `skill-benchmark-exemption.md` 第一行「描述性 / 机械」档 (与 §5 样例 `state-scanner-stale-refs-false-parity` 同性质): substitute = SC 级 baseline-failing 结构化测试 **SC-1 / SC-2 / SC-3 / SC-4 / SC-8** (每条对当前代码先红); SC-5 / SC-6 / SC-7 / SC-9 / SC-10 为文档 / 对照 / 回归 / 渲染项。`rule6_note` 随 B.2 写入 |

## Tasks (4 个 .py + 1 份规范 + 7 处消费面; 11 个 checkbox)

- [ ] T1 `split_owner_container` 两段式 (含零段 / 三段兼容); 改写 `test_split_owner_container_variants` 的 2-part **与 1-part (`"solo"`)** 断言, 先红后绿两臂 → SC-1
- [ ] T2 `classify_claims` 确定性判定 (identity_key 计数 + 不可归属规则) + 新函数 `identity_drift_advisories(tracks)`; collector `handoff_multibranch.py:709` dedupe 前调用并写 `collision.identity_advisories[]`; `state-snapshot-schema.md` additive bump + `test_normalize_snapshot` 锁字段 → SC-2 / SC-8
- [ ] T3 `get_container_label()` (S1 即落); `get_container_id()` uuid 优先 (S2 才落, 见排序); container-id 文件头注释改写 → SC-3
- [ ] T3b 迁移检查挂 `phase1_gate` / `release_gate` 启动路径 (label 非空且 `claims/<label>/` 有 active → 告警 + 本次不 flip) → SC-3
- [ ] T4 dedupe 键 `(track_id, identity_key)`; `test_owner_segment_participates_in_grouping_key` 两臂 (uuid 折叠 / 主机名不折叠 / **8 位非 hex 主机名 `devbox01` 不折叠**); `test_both_latest_active_still_reports_self_multi_container` 期望改为 `cross_owner` (原绿是 owner 段被解析丢) + 新增同 owner 串变体断 🟡; `track_board.py:412-417` 键同源 → SC-4
- [ ] T5 `session-handoff.md` §2.3.1 (三态 + `identity_key` 定义) / §2.3.5 (三行, 实质变更说明) / 新 §2.3.9 (按 D-1/D-2/D-3 裁定回填; 不引用 Lab 私有文档) → SC-5
- [ ] T6 冻结语料复制为 aria 测试 fixture; 前后对照测试逐组归因 (真撞车 / 同人多机 / stale (#182)) → SC-6
- [ ] T7 消费面同步: 五处文档 (D4) + `fetch_gate.py` 真实两段式 `cross_owner` 夹具; rule 1.54 触发面锁定 → SC-9
- [ ] T8 `track_board.py` ⚪ 行渲染 (调用 `identity_drift_advisories`) + label 并列显示 → SC-10
- [ ] T9 D-0 裁定落地 (选 (a) 时: track 族键 + §2.3.1 尾段语义 + SC-2 加「两容器各自认领同 Spec → 🟡/🔴 可达」用例; 选 (b)/(c) 时: 本条改为记录) → SC-2 (条件)
- [ ] T10 全套回归 (state-scanner pytest 基线 104 + 全套; phase-d-closer `test_fetch_gate.py`; session-closer handoff 写入测试) + 主仓 14 state-check → SC-7
- [ ] T11 回帖 #193 / aria-plugin#135 (缺口 3) 指向本 Spec; #174 留言 D-0 与 SC-3 改写征求 ack; ship 后关 #193, #135 留缺口 1/2 (文档动作, 无 SC; 归 D 期)

## Success Criteria

- [ ] SC-1 (T1) `split_owner_container("simonfish/bfe8285d") == ("simonfish","bfe8285d","")`; `("solo") == ("","solo","")`; `("a/b/c") == ("a","b","c")`。**先红** (现 `("","simonfish","bfe8285d")` / `("","","solo")`)
- [ ] SC-2 (T2/T9) 经 dedupe → `classify()`: 同容器双 owner → `kind == "none"` 且 advisory 恰 1 条 `{identity_key: bfe8285d, owners: [aria-runner-bot, simonfish]}`; 两人两机 → `cross_owner`; 同人两机 → `self_multi_container`; 漂移后无共现 (`aria-runner-bot/bfe8285d` + `simonfish/023236f2`) → `cross_owner`; 零段 vs 两段同主机名 → `self_multi_container`; **端到端** (collector 夹具 → dedupe → classify) 真实两段式两人两机 → `cross_owner`; ≥3 owner 的 uuid 容器 → advisory `owners[]` 长度 3; legacy 行不产生 advisory; D-0(a) 时两容器对同一 Spec 各自认领 (`<slug>-<uuid1>` / `<slug>-<uuid2>`) → 可达 🟡/🔴。**前三条先红** (现 🟡 / 🟡 / none)
- [ ] SC-3 (T3/T3b) S2 形态: container-id 含非空 `label` 时 `get_container_id()` 返回 uuid、`get_container_label()` 返回 label; 复现 #135 08-13 时间线不再 `claim_not_found`。S1/S2 共同: label 非空且 `claims/<label>/` 有 active 时 `phase1_gate` 输出迁移告警。**先红**
- [ ] SC-4 (T4) 同 track 同 uuid 容器不同 owner 两行经 dedupe 折叠为 1 (**先红**); 同主机名不同 owner 不折叠; **`devbox01`/两 owner 不折叠** (对抗 `len==8` 实现); board 对两段式串回显原串 (**先红**: 键 `""` vs `"unknown"` 失配); 隔离夹具对断 `cross_owner`, 同 owner 变体断 `self_multi_container`
- [ ] SC-5 (T5) §2.3.1 含 `identity_key` 定义与三态; §2.3.5 恰三行且判据只用 §2.3.1 定义的词 (grep 断言无 `等价类` / 无 aria 代码路径); §2.3.9 存在、含 D-2 裁定文本、不含 `/home/` 或 Aether 私有路径; §2.3.7/§2.3.8 diff 零
- [ ] SC-6 (T6) 对 fixture 跑生产路径: 改前 A = 1 组 / 改后 = 2 组 (D-3(a) 时 0 组), 每组由断言归入「真撞车 / 同人多机 / stale (#182)」之一, 归因表由测试计算而非手写
- [ ] SC-7 (T10) state-scanner 全套 pytest 零回归 (基线 104 + 改写项全绿); `test_fetch_gate.py` 全绿; session-closer / phase-d-closer 测试全绿; 主仓 14 state-check 全绿
- [ ] SC-8 (T2) snapshot `collision.identity_advisories` 存在且为 list; 旧 snapshot 缺该字段时 `track_board` / rule 1.54 / `fetch_gate` 不崩 (additive)。**先红** (字段不存在)
- [ ] SC-9 (T7) rule 1.54 触发面测试 (`coordination.enabled=false` + 真实两段式 `cross_owner` 夹具 → 命中); 五处文档的取值措辞与 §2.3.5 三行一致 (grep 断言, 含 `references/rules/advanced-rules.md`); `fetch_gate` advisory 文案含 `cross_owner`
- [ ] SC-10 (T8) board 对 fixture 渲染恰 2 条 ⚪ 行 (`023236f2` / `bfe8285d`), 每行列出 owners[] 与 first/last_seen; 无 advisory 时不渲染 ⚪ 段

## 非目标

- 不推断「两个 owner 串是不是同一个人」(v2 等价类已撤销); 不引入映射表、不持久化身份状态。
- 不改 Layer L claim schema / reconcile 仲裁规则; tie-break session 退化记为已知限制。
- 不处理 aria-plugin #135 缺口 1 / 缺口 2 (a1-entry 处置); 不改 a1-entry 的 track-id 契约 (D-0 只在本 Spec 侧适配或上呈)。
- 不修 #182 (status 收口与非 enum 归一); D-3(a) 只让 stale 行不参与判定。
- 不规定 Aether 账号 / 凭据, 不规定容器 `git config` 供给 (10cglocal); standards 不引用 Lab 私有文档。
- 不 rewrite 历史 handoff frontmatter。

## References

- Triage: `.aria/triage-report.json` (2026-09-05, partial-repro) · #193 comment 21431
- 审计: `.aria/audit-reports/post_spec-R1-2026-09-05T140104-375Z-…-aggregated.md` / `post_spec-R2-2026-09-05T143543-081Z-…-aggregated.md` (+ 各席位报告)
- 规范: `standards/conventions/session-handoff.md §2.3.1 (:116) / §2.3.5 (:178-186) / §2.3.6 (:189) / §2.3.7-§2.3.8 (:204,:217, 已占用) / §2.3.8.2 (:234)`
- 代码: `aria/skills/state-scanner/lib/collision.py` (`split_owner_container` :63, `track_to_claim_record` :86 (status 映射 :113-124), `classify_claims` :143, `classify` :300 (track_id 分组 :363, stale 捞回 :374-379)) · `lib/identity.py` (`get_container_id` :191, label 优先 :222, hostname 兜底 :242) · `scripts/collectors/handoff_multibranch.py:518-523, :709-714` · `scripts/renderers/track_board.py:176-183, :412-417, :430` · `lib/reconcile.py:151` · `lib/constants.py:36` · `aria/skills/phase-d-closer/scripts/fetch_gate.py:251`
- 消费文档: `references/layer-l-integration.md:25-27,73,77` · `RECOMMENDATION_RULES.md:31` · `references/rules/advanced-rules.md:544-572` · `references/state-snapshot-schema.md:1085` · `references/phase-1-collectors.md:75`
- 决策记录: DEC-20260704-002 (病根 #3 机械填) · Kairos `docs/decisions/DEC-2026-09-04-git-identity-scope.md` (本地 checkout 已核; standards 不引用)
- 相邻 Spec: `a1-entry-claim-duplicate-work-guard` §2.1 (`<spec-slug>-<container_uuid>`) / §2.1a / §3 (follow-up) / SC-3 (:571) / Impact `get_container_uuid` (:660)
