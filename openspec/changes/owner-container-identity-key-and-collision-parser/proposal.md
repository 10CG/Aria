# owner-container 身份键与 collision 解析器修正 (合并处置 Aria #193 + aria-plugin #135 缺口 3)

> **Level**: Minimal (Level 2 Spec) — **owner 2026-09-05 指令为 Level 2**; post_spec R1 tech-lead 席依 `standards/core/ten-step-cycle/phase-a-spec-planning.md:126-137` 判据 (architecture / cross-module / breaking 任一为 Yes → Level 3) 认为三项全中, 建议 Level 3。**请 owner 复议** (Rule #10: Level 由判据与 owner 决定, 执笔不按性价比下调, 也不越过 owner 上调)。维持 Level 2 的可辩护理由: 交付面 5 个代码文件 + 1 份规范 + 3 处消费文档, 9 个任务, 无 schema 破坏 (snapshot 字段 additive), 判据变更经 D-1/D-2/D-3 由 owner 显式裁定而非隐含。
> **Status**: Draft **v2** (post_spec R1 五席 FAIL/REVISE 后 rework, 2026-09-05; R1 聚合 `.aria/audit-reports/post_spec-R1-2026-09-05T140104-375Z-owner-container-identity-key-and-collision-parser-aggregated.md`)
> **Created**: 2026-09-05
> **Linked Issue**: `10CG/Aria#193, 10CG/aria-plugin#135`
> **Track / claim**: `owner-container-identity-key-and-collision-parser` (phase A claim `s-8204@1355`, container `bfe8285d`, linked_issue `10CG/Aria#193`, overlap 告警空)
> **代码落点**: `aria/` 子模块 (state-scanner `lib/` + collector + renderer + references) + `standards/` 子模块 (session-handoff.md §2.3); Spec 落主仓 (Rule #5)
> **Triage 依据**: `.aria/triage-report.json` / [#193 comment 21431](https://forgejo.10cg.pub/10CG/Aria/issues/193#issuecomment-21431) (partial-repro / major / next-cycle)
> **冻结语料**: `.aria/repro/handoff-tracks-frozen-2026-09-05.json` (起草日 `scan.py` 产出的 `tracks_multibranch.tracks[]` 非 legacy 行, 996 行, 已纳入版本控制; 所有实验表数字与 SC-6 都对它跑, 不对会漂的 `.aria/state-snapshot.json` 跑)
> **相邻在飞 Spec**: [`a1-entry-claim-duplicate-work-guard`](../a1-entry-claim-duplicate-work-guard/proposal.md) (对方容器 `023236f2`, 待 B.1) — 其 §3 已把「`owner-container` 与 claim container 段口径不同, 两标识关系需成文」记为 follow-up 且明示不在其内统一; 本 Spec 即该 follow-up。**硬排序**见 §Impact「与 a1-entry 的边界」。

## Why

多终端协调的唯一 advisory 信号 `tracks_multibranch.collision` 目前不可信, 原因有三层, 分别由一次 triage 和两张票揭出:

1. **解析器格式契约错位 (triage 新发现, 主根因)**: `lib/collision.py::split_owner_container` 按三段式 `owner/container/session` 解析 (契约起点 aria `f9306a0` 2026-05-20 的 `track_board.py`, `83a1a45` 05-30 迁入 `collision.py`), 而 handoff frontmatter 按 `session-handoff.md §2.3.1` 是两段式 `<owner>/<container-id>` (主仓 154 份 frontmatter 实测: 142 份两段 / 12 份零段 / **0 份三段**)。两段串被拆成 `(owner='', container=<owner 段>, session=<uuid>)` ⇒ `owner` 恒 `unknown` ⇒ `classify_claims` 的 `cross_owner` 分支**从 handoff 数据永远不可达**。直接调用真函数复现 (triage case-2..5): 同容器双 owner 串 → 🟡; **真两人两机 → 也是 🟡 (真撞车降级)**; **同人两机 → `none` (漏报)**; 喂三段式串才得 🔴 —— 分类逻辑没错, 错在输入契约。
2. **owner 段随 git 身份漂移 (Aria #193)**: 同一物理容器的 `git user.email` 变更后, 机械填规则忠实记录 → 同一 container 出现多个 owner 串。两个 uuid 容器都发生且方向相反: `bfe8285d` = `simonfish/…` 34 份 (07-05..08-27) + `aria-runner-bot/…` 2 份 (09-03..), 漂移点钉在 08-26/08-27 之间; `023236f2` = `aria-runner-bot/…` 23 份 (07-05..08-16) + `simonfish/…` 17 份 (07-03..09-05)。Aria 现行规范只定义 `<owner>` = git `user.email` local-part, **没有任何 AI runner 该以什么 git 身份提交的规范** (standards/conventions + CLAUDE.md grep 零命中)。
3. **container 段来源不稳 (aria-plugin #135 缺口 3 + 08-13 补充)**: container 段先后是主机名 (`dev-claude` / `dev-claude2`, 跨机不唯一) 与 uuid (`bfe8285d` / `023236f2` / `f9c6e8cd`); `lib/identity.py::get_container_id()` 是 `label if label else uuid`, 文件头注释又邀请用户填 label ⇒ 填个可读名就静默换了协调身份 (08-12 实测: 认领 `bfe8285d`、释放时解析成 `dev-claude2` → `claim_not_found` 孤儿 claim)。主仓 frontmatter 今天是 **10 种 owner-container 串, 对应 5 个 container 标识 (3 个 uuid + 2 个主机名), 实际 2 台在用的机器**。

**为什么三层必须一起处置 (按生产路径 `collector dedupe → classify` 在冻结语料上实测, 见 §What 实验表)**: 只修第 1 层 (parser) 会把「静默失灵」换成「响亮误报」—— 主机名时代同一 owner 的两台机 (`simonfish/dev-claude` vs `simonfish/dev-claude2`, 2026-05) 与零段/两段混写的同一台机 (`dev-claude` vs `simonfishgit/dev-claude`) 立刻被判 🔴 cross_owner; 两个 uuid 容器各自带两个 owner 串, 一旦它们在同一 track 上并存 (R1 前的实验把 `state-scanner-stale-refs-false-parity` 6 行 stale active 直接喂 classify 时正是这样) 同一 owner 的两台机也会 🔴。第 2/3 层给出的身份键与 owner 等价类, 才让「同人多机 🟡 / 两人两机 🔴 / 同容器多 owner ⚪」三态在真实语料上同时成立。

## What

一个 change, 四个交付面 (代码 / 规范 / 看板告警 / 消费文档同步), 外加三项 owner 决策点 (§决策点, 未预设结论)。

### Key Deliverables

**D1 — 解析器、身份键、判定键对齐规范 (aria: `lib/collision.py` + `handoff_multibranch.py` + `track_board.py` + `lib/identity.py`)**

D1 是**三步**, 缺一步都会退回 R1 指出的误报:

- **步骤 1 解析**: `split_owner_container` 按 §2.3.1 两段式解析: `<owner>/<container>` → `(owner, container, session='')`; 三段式 (Layer L `superseded_from` 形, `claim_schema._validate_superseded_from` 自行 `split("/")` 不经此函数) 保持 `(owner, container, session)`; 零段串 → `(owner='', container=<串>, session='')` (主机名时代遗留)。规范不改成三段: frontmatter 无 session 概念 (§2.3.6: 写入频度 = 会话结束一次)。
- **步骤 2 身份键** (`identity_key`): container 段匹配 `^[0-9a-f]{8}$` (container-id 文件 uuid 形) ⇒ `identity_key = container` (uuid 全局唯一, owner 段不参与同一性); 否则 (主机名 / 空) ⇒ `identity_key = owner + "/" + container` (主机名跨机不唯一, 保留 owner 段区分 —— 这正是既有测试 `test_owner_segment_participates_in_grouping_key` 那条不变式的成立域, 该测试改写为「uuid 容器折叠 / 主机名容器不折叠」两臂)。**dedupe 键改为 `(track_id, identity_key)`** (`handoff_multibranch.py:518-523`, **显式改动项**, 不再「不改逻辑」)。
- **步骤 3 owner 等价类**: 对**全语料** (collector 扫到的全部非 legacy 行, 不是 dedupe 后的行) 建并查集: 同一 uuid 容器上共现过的 owner 串两两等价; 空 / `unknown` owner 不可归属, **不构成独立类**。`classify_claims` 改为: 先按 `identity_key` 分组, ≥2 个 key 时比较 owner **等价类代表** —— 类数 ≥2 → `cross_owner`; 类数 ≤1 → `self_multi_container`; 同一 `identity_key` 内多 owner 不参与 collision 计数 (由 D3 告警)。等价类只从共现关系推导, 不引入映射表, 对采用方零配置。
- `track_board.py:412-417` 标签查找: 建表键与查表键**同源归一** (都经 `track_to_claim_record` 的 `"unknown"` 填充或都不经), 修掉今天就查不中的 bug (**显式改动项**)。
- `lib/identity.py`: 新增 `get_container_label()` (展示用); `get_container_id()` 改为 uuid 优先, 只读 fs 兜底仍返回 hostname (**不写「恒 uuid」**, hostname 分支是既有降级路径); 该 flip 的**落地时机受 §Impact 硬排序约束**。flip 前守卫 (T3b): 若本机 container-id 文件 `label` 非空且 `claims/<label>/` 下存在 active claim ⇒ 先按 D1 前的口径 release 或迁移到 `claims/<uuid>/`, 否则 flip 会让在飞 claim 变孤儿 (#135 08-13 事故的镜像方向)。

**D2 — 规范成文 (standards, `session-handoff.md §2.3`)**
- §2.3.1 `owner-container` 行: `<owner>` 语义按 D-1 裁定写死; `<container-id>` 明确 = container-id 文件的 **uuid 字段** (label 不参与), 与 Layer L claim `container` 同口径 —— 闭合 a1-entry §3 的 follow-up。
- §2.3.5 判据表: **实质变更, 不是措辞变更** (对 SilkNode / Kairos / nexus 等采用方是行为变更, 在 standards 变更说明与 aria CHANGELOG 明示): `cross-owner` = 同 track ≥2 个 `identity_key` 且 owner 等价类 ≥2; `self-multi-container` = ≥2 个 `identity_key` 且等价类 ≤1; 新增第三行 **`same-identity-multi-owner`** = 同一 `identity_key` 出现 ≥2 个 owner 段 → ⚪ 信息级 advisory「同容器多 owner 串 (git 身份漂移), 不计入 collision」。
- **新增 §2.3.9**「AI runner 提交身份」(§2.3.7 = #137 frontmatter enforcement, §2.3.8 = carry-id schema, 均已占用; 真空档 §2.3.9): 按 D-2 裁定写入, 交叉引用 Aether 人机两账号模型的边界 (Aria 只规定 owner 段怎么来与 AI 会话该署什么, 不规定 Aether 账号 / 凭据 / 容器 `git config` 供给)。
- 历史 handoff **不 rewrite** (与 Kairos DEC-2026-09-04 一致): 等价类让历史双串自然归到同一身份。

**D3 — 看板显式告警 (aria: `classify()` + `track_board.py` + snapshot schema)**
- `classify()` 返回 dict 新增 additive 字段 `identity_advisories[]`: 每条 `{identity_key, owners[], first_seen, last_seen}`, 从步骤 3 的全语料并查集产出 (**宿主是 `classify()` 的 dict, 不是 `classify_claims` 的 2-tuple**, 渲染器 `track_board.py:430` 的解包不受影响); legacy 行 (`owner_container == "unknown"`) 不参与 (沿用 `classify()` 顶部过滤, 由 SC 锁死)。board 渲染为 ⚪ 行; `state-snapshot-schema.md` 记录 additive bump。
- 与 #182 的关系是**依赖, 不是正交**: 19 份历史 `status: active` frontmatter (最早 2026-05-20) 全部远超 `STALE_TTL=1800`, 仍被 `collision.py:374-379` 捞回参与判定。本 Spec 修的是**分类逻辑正确性**; 信号**可用性**还取决于 stale active 行如何收口 —— 由 D-3 裁定是否在本 Spec 内加 Layer H 新鲜度截止。

**D4 — 消费文档同步 (aria references)**
- `references/layer-l-integration.md:73` (`kind == "cross_owner"` → 推荐 worktree) 与 `:14`; `RECOMMENDATION_RULES.md` rule 1.54 (`collision.kind != none` 触发); `references/advanced-rules.md:578` 过时注释 —— 三处按 D1 新语义改写, 并由 SC 锁 rule 1.54 触发面 (本 Spec 让 `cross_owner` 首次在真实数据上可达, 消费面不能靠「从未触发过」侥幸)。

### 实验表 (冻结语料 996 行, **生产路径** `dedupe_latest_per_track_container → classify`, 2026-09-05 实跑)

| 变体 | dedupe | `collision.kind` | groups |
|---|---|---|---|
| A 现状 (三段式解析, 现 dedupe 键) | 996→121 | self_multi_container | `[dev-claude, simonfishgit/dev-claude]` |
| B 只修 parser (步骤 1) | 996→122 | **cross_owner (误报)** | 上组 + `[simonfish/dev-claude, simonfish/dev-claude2]` |
| D 三步齐全 (步骤 1+2+3) | 996→122 | self_multi_container | 同 B 的两组, 均判 🟡 (主机名时代同一 owner 两机 / 同一机零段+两段混写) |

合成用例 (直接调 `classify`, 等价类由冻结全语料建): 两人两机 `alice/aaaa1111` + `bob/bbbb2222` → **cross_owner**; 同容器双 owner → **none** + 1 条 advisory; 同人两机 `simonfish/bfe8285d` + `simonfish/023236f2` → self_multi_container; 漂移后本容器 vs 对方容器 `aria-runner-bot/bfe8285d` + `simonfish/023236f2` → self_multi_container (靠等价类, 二者在各自容器上共现过)。

D3 告警对象 (uuid 容器多 owner): `023236f2: [aria-runner-bot, simonfish]` · `bfe8285d: [aria-runner-bot, simonfish]`。主机名容器 (`dev-claude: ['', simonfish, simonfishgit]`, `dev-claude2: ['', simonfish]`) 不入等价类、不告警 (跨机不唯一, 无法断言是同一台)。

**结论**: 真实语料里**没有**真正的两人撞车; 现状 A 的唯一一组与 B 多出的一组都是 2026-05..07 的 stale active 行 (#182 形态), 修后可全部归因 (SC-6)。

## 决策点 (owner, 未预设; 裁定后回填 D2 文本)

**D-1 `<owner>` 段语义**
- (a) **提交身份** (现状: git `user.email` local-part; 机械可得, 零配置)。后果: 同一人换 email 就是另一个 owner 串, 靠 D1 步骤 3 的等价类消解 (只覆盖在 uuid 容器上共现过的串); 从未共现的两个串 (如某人换了新机器又换了 email) 仍会 🔴 一次, 直到该机器上出现两串共现。
- (b) **人** (需 `owner-map`: email local-part → 人名, 放 `.aria/` 或 standards)。后果: 分类准确且不依赖共现, 但引入一张要维护的表, 跨采用方不可移植, 与「Aria 不要求采用方维护身份数据」的定位相悖。
- 执笔建议: (a)。不是因为它没代价, 而是它的代价 (罕见的一次 🔴) 有 D3 告警可解释, 而 (b) 的代价是常驻维护面。

**D-2 AI runner 的 git 提交身份**
- (a) **统一机身份** (如 `aria-runner-bot@…`): 所有 AI 会话 commit 署 bot。收益: owner 段稳定, 与 Aether 人机两账号模型对齐 (AI runner 归入机账号一类)。**代价**: commit 署名失去「哪位操作者在场」的可追溯性 (须靠 handoff / claim 的 container 段补), 且两位操作者的 AI 会话之间无法区分 —— 若将来出现第二位人类操作者, 需要第二个 bot 身份或退回 (b)。
- (b) **人身份** (AI 会话沿用操作者 email)。收益: 署名可追溯到人。**代价**: 与 Layer 2 生产侧 (aria-runner 容器已用 bot) 不一致; 操作者换 email 即触发漂移, 等价类要重新学习。
- (c) **不规定**。收益: 零改动。**代价**: 漂移继续, D3 告警常亮, 等价类持续增长。
- 执笔建议: (a), 并把「操作者可追溯性由 container 段 + handoff 承担」写进 §2.3.9。**本 Spec 只写 Aria 侧规范**; 容器上 `git config` 如何供给 (10cglocal) 与 Aether 账号治理不在范围, 规范文本以交叉引用标边界。

**D-3 Layer H 新鲜度截止 (回应 #182 依赖)**
- (a) **本 Spec 内加截止**: `updated-at` 早于 N 天 (建议 N=30, 与 STALE_TTL 不同量纲, 因 Layer H 是会话粒度) 的 `active` 行不参与 collision 判定, 但仍在 board 以「stale」标出。后果: 信号立刻可用; 引入一个新阈值常量 + 一条规范句; 与 #182 (status 收口) 是互补不是替代。
- (b) **不加, 交 #182**: 本 Spec 只保证分类逻辑正确; 在 #182 落地前 board 上仍会出现 2026-05 的 🟡 组。后果: scope 干净; 但「信号可信」这个目标在本 Spec ship 时不成立, Positive 只能写「逻辑正确」。
- 执笔建议: (a)。理由: #182 无人认领且是类级修 (对方容器 M4 队列末位), 等它意味着本 Spec 的主要收益延期不定。

## Impact

| Type | Description |
|------|-------------|
| **Positive** | collision **分类逻辑**第一次同时满足: 真两人撞车 = 🔴 (不再降级)、同人多机 = 🟡 (不再漏报)、同容器多 owner = ⚪ 显式告警 (不再静默); Layer H 与 Layer L 的 container 口径统一为 uuid; label 陷阱 (#135 08-13 形态) 结构性消除。**信号可用性**取决于 D-3: 选 (a) 则 ship 即可用; 选 (b) 则待 #182 |
| **Risk** | (1) §2.3.5 判据实质变更 + dedupe 键变更 ⇒ 采用方看板输出改变 (实验表 A→D: 组数 1→2, 都是 stale 🟡); 缓解: SC-6 对冻结语料前后对照并逐组归因, 变更说明写进 standards 与 aria CHANGELOG。(2) reconcile tie-break 键 `container/session` 在两段式下退化为 `container/unknown`, `claimed_at` 完全相同的同容器两行退回输入顺序 (TL m-1); 缓解: Layer H 记录的 `claimed_at` 是 `updated-at` 秒级时间戳, 同容器同秒两份 handoff 在实践中不出现, 记为已知限制并加 SC 锁定「不因此崩溃」。(3) `oc_by_tid_key` 三元组键在未 dedupe 输入上可能撞键 (BA m); 生产路径恒先 dedupe, SC 锁「classify 只接受 dedupe 后输入」的契约注释 |
| **`get_container_id()` 消费方 (全列)** | `lib/identity.py::get_identity()` → `lib/claim_lifecycle.py:39,88` (写 claim 的 container 目录与字段) / `scripts/phase1_gate.py:294` (winner 归属 `verdict.winner.container == identity.container_id`) / `lib/concurrent_tracks.py:25,133` (同容器 active 计数) / `scripts/release_gate.py` (按 container 定位 claim) / session-closer `handoff_autofill.py:391` (frontmatter 机械填)。flip 影响面即这六处; T3b 守卫覆盖「label 非空 + 在飞 claim」的迁移期 |
| **与 a1-entry 的边界 (硬排序)** | a1-entry 在 `lib/identity.py` 新增 `get_container_uuid()` (其 Impact 表 :660), 其 SC-3 (:571) 以「`get_container_id()` label 优先 ⇒ 直接调它的实现必红」为 baseline-failing 前提; 本 Spec 的 flip 会让该 SC-3 恒绿 —— 语义耦合, `git rebase` 不报冲突。**规则**: (i) 本 Spec 的 `identity.py` 改动**排在 a1-entry B.2 落地之后**; 在此之前本 Spec 只加 `get_container_label()`, 不 flip; (ii) flip 落地时由本 Spec 承担改写 a1-entry SC-3 的判据 (改为「`get_container_uuid()` 与 flip 后的 `get_container_id()` 同值; label 只出现在 `get_container_label()`」) 并在 Aria #174 留言知会对方容器; (iii) 本 Spec 改 `collision.py` 上游函数会让 a1-entry 钉的 `lib/collision.py:265-266` 等行号漂移 —— B.1 起手前 fetch 其分支实况, 由后落地方在 D 期 refresh 行号 |
| **Rule #6** | 不改任何 SKILL.md 指令面 / description (state-scanner 阶段 2 读的是 snapshot 字段, 渲染改动属机械输出) ⇒ 按 `skill-benchmark-exemption.md` 第一行「描述性 / 机械」档 (与 §5 样例 `state-scanner-stale-refs-false-parity` collector 代码层同性质): substitute = SC 级 baseline-failing 结构化测试 (**SC-1 / SC-2 / SC-3 / SC-4 / SC-8**, 每条对当前代码先红); SC-5 / SC-6 / SC-7 / SC-9 是文档 / 对照 / 回归项, 不计入 substitute 点名。`rule6_note` 随 B.2 写入 |

## Tasks

- [ ] T1 `split_owner_container` 两段式语义 (含零段 `("", 串, "")`、三段兼容); 改写 `test_split_owner_container_variants` 的 2-part **与 1-part (`"solo"`)** 断言为新契约, 先红后绿两臂 → SC-1
- [ ] T2 `classify_claims` 三步判定 (identity_key + owner 等价类) + `classify()` dict 新增 `identity_advisories[]`; `state-snapshot-schema.md` additive bump + `test_normalize_snapshot` 锁字段存在 → SC-2 / SC-8
- [ ] T3 `get_container_label()` 新增 (可先落); `get_container_id()` uuid 优先 (hostname 兜底保留) **排在 a1-entry B.2 后**; container-id 文件头注释改写 → SC-3
- [ ] T3b flip 前守卫: 检测 `label` 非空且 `claims/<label>/` 有 active → release/迁移 或 拒绝 flip 并告警 → SC-3
- [ ] T4 `handoff_multibranch.py` dedupe 键 `(track_id, identity_key)`; 改写 `test_owner_segment_participates_in_grouping_key` 为两臂 (uuid 折叠 / 主机名不折叠); 点名并改写 `test_both_latest_active_still_reports_self_multi_container` (等价类下语义不变, 断言加等价类前提); `track_board.py:412-417` 键同源 + ⚪ 行 + label 并列 → SC-4
- [ ] T5 `session-handoff.md` §2.3.1 / §2.3.5 (三行, 实质变更说明) / 新 §2.3.9 (按 D-1/D-2/D-3 裁定回填) → SC-5
- [ ] T6 冻结语料复制为 aria 测试 fixture (`tests/fixtures/handoff-tracks-frozen-2026-09-05.json`); 前后对照测试逐组归因 (真撞车 / 同人多机 / stale active) → SC-6
- [ ] T7 消费文档同步: `layer-l-integration.md:14,73` / `RECOMMENDATION_RULES.md` rule 1.54 / `advanced-rules.md:578`; rule 1.54 触发面锁定测试 → SC-9
- [ ] T8 全套回归 (state-scanner pytest 基线 104 + 全套; session-closer / phase-d-closer handoff 写入测试) + 主仓 14 state-check → SC-7
- [ ] T9 回帖 #193 / aria-plugin#135 (缺口 3) 指向本 Spec; ship 后关 #193, #135 留缺口 1/2 (文档动作, 无 SC; 归 D 期 closeout 清单)

## Success Criteria

- [ ] SC-1 (T1) `split_owner_container("simonfish/bfe8285d") == ("simonfish","bfe8285d","")`; `("solo") == ("","solo","")`; `("a/b/c") == ("a","b","c")`。**对当前代码先红** (现分别为 `("","simonfish","bfe8285d")` / `("","","solo")`)
- [ ] SC-2 (T2) 三组 2-part 输入经 `classify()`: 同容器双 owner → `kind == "none"` 且 `identity_advisories` 恰 1 条 `{identity_key: bfe8285d, owners: [aria-runner-bot, simonfish]}`; 两人两机 → `cross_owner`; 同人两机 → `self_multi_container`; **端到端** (collector 夹具 → dedupe → classify) 真实两段式两人两机 → `cross_owner`; ≥3 owner 的 uuid 容器 → advisory `owners[]` 长度 3; legacy 行不产生 advisory。**前三条对当前代码先红** (现 🟡 / 🟡 / none)
- [ ] SC-3 (T3/T3b) container-id 文件含非空 `label` 时 `get_container_id()` 返回 uuid、`get_container_label()` 返回 label; 复现 #135 08-13 时间线 (acquire 后加 label 再 release) 不再 `claim_not_found`; label 非空且 `claims/<label>/` 有 active 时守卫拒绝 flip 并输出告警。**对当前代码先红**
- [ ] SC-4 (T4) 同 track 同 uuid 容器不同 owner 两行经 dedupe 折叠为 1 (**先红**: 现键含 owner 不折叠); 同 track 同主机名不同 owner 两行**不**折叠 (既有不变式保留域); board 对两段式串回显原串 (**先红**: 现建表/查表键 `""` vs `"unknown"` 恒失配); `test_both_latest_active_still_reports_self_multi_container` 在新语义下仍绿
- [ ] SC-5 (T5) `session-handoff.md` §2.3.5 表恰三行且判据文本含 `identity_key` / 等价类 / `same-identity-multi-owner`; §2.3.9 存在且含 D-2 裁定文本与 Aether 边界交叉引用; §2.3.7/§2.3.8 原文不变 (diff 零)
- [ ] SC-6 (T6) 对 fixture `handoff-tracks-frozen-2026-09-05.json` 跑生产路径: 改前 A = 1 组 / 改后 D = 2 组, 逐组归因表落在测试断言与 handoff; 每组归入「真撞车 / 同人多机 / stale active (#182)」之一, 无「不可解释」组; D-3 选 (a) 时改后 = 0 组
- [ ] SC-7 (T8) state-scanner 全套 pytest 零回归 (基线 104 + 受影响测试改写后全绿); session-closer / phase-d-closer 测试全绿; 主仓 14 state-check 全绿
- [ ] SC-8 (T2) snapshot `tracks_multibranch.collision.identity_advisories` 字段存在且为 list; 旧消费者 (`track_board` / rule 1.54) 在字段缺失的旧 snapshot 上不崩 (additive 兼容)。**对当前代码先红** (字段不存在)
- [ ] SC-9 (T7) rule 1.54 的触发面测试: `coordination.enabled=false` + `kind=cross_owner` (真实两段式夹具) → 规则命中; `layer-l-integration.md:73` 与 `RECOMMENDATION_RULES.md` 的取值措辞与 §2.3.5 三行一致 (grep 断言)

## 非目标

- 不改 Layer L claim schema / reconcile 仲裁规则 (earliest claimed_at 胜); tie-break session 退化记为已知限制。
- 不处理 aria-plugin #135 缺口 1 (snapshot 不解析 claim) / 缺口 2 (闸门只覆盖 Phase B, 由 a1-entry 处置)。
- 不修 #182 (status 从不收口) 本身; D-3 (a) 只是让 stale 行不参与判定, 不改 status 语义。
- 不规定 Aether 账号 / 凭据, 不规定容器 `git config` 的供给方式 (10cglocal)。
- 不 rewrite 历史 handoff frontmatter。

## References

- Triage: `.aria/triage-report.json` (2026-09-05, partial-repro) · #193 comment 21431
- R1 审计: `.aria/audit-reports/post_spec-R1-2026-09-05T140104-375Z-owner-container-identity-key-and-collision-parser-{aggregated,tech-lead,backend-architect,qa-engineer,code-reviewer,knowledge-manager}.md`
- 规范: `standards/conventions/session-handoff.md §2.3.1 / §2.3.5 / §2.3.6 / §2.3.7-§2.3.8 (已占用)`
- 代码: `aria/skills/state-scanner/lib/collision.py` (`split_owner_container` :63, `track_to_claim_record` :86, `classify_claims` :143, `classify` :300, stale 捞回 :374-379) · `lib/identity.py` (`get_container_id` :191, label 优先 :222, hostname 兜底 :242) · `scripts/collectors/handoff_multibranch.py:518-523, :709-714` · `scripts/renderers/track_board.py:412-417, :430` · `lib/reconcile.py:151` · `lib/constants.py:36` (STALE_TTL)
- 消费文档: `references/layer-l-integration.md:14,73` · `RECOMMENDATION_RULES.md:31` (rule 1.54) · `references/advanced-rules.md:578` · `references/state-snapshot-schema.md`
- 决策记录: DEC-20260704-002 (病根 #3 机械填) · Kairos `docs/decisions/DEC-2026-09-04-git-identity-scope.md` (权利边界裁定, 本地 checkout 已核)
- 相邻 Spec: `a1-entry-claim-duplicate-work-guard` §2.1 (container_uuid 段) / §3 (口径待定 follow-up) / SC-3 (:571) / Impact `get_container_uuid` (:660)
