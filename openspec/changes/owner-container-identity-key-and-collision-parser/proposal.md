# owner-container 身份键与 collision 解析器修正 (合并处置 Aria #193 + aria-plugin #135 缺口 3)

> **Level**: Full (Level 3 Spec) — **owner 2026-09-05 裁定升 Level 3** (判据: cross-module 成立, aria + standards 两子模块; 决策单 `.aria/decisions/2026-09-05-owner-container-identity-key-rulings.md`)。Level 3 交付 = 本 proposal + `tasks.md` (A.2) + `detailed-tasks.yaml` (A.3) + post_planning 收敛审计。
> **Status**: **Shipped 2026-09-06 (S1; aria-plugin v1.70.0, 主仓 PR #197 → 990318e; S2 后续 tracker Aria #198)** — 原 Approved (owner 2026-09-05) — v11 = post_planning R4 后同步 (SC-9 尾句门槛 / T11 两时点拆开 / SC-7 文件级限定 + test_collision.py carve-out); v10 = post_planning R3 后同步 (SC-7 双跑法可执行形态 / T10 T11 措辞 / T2 删不成立子句 / :104 先例句 / Impact S1 限定); v9 = post_planning R2 后同步 (SC-9 rule 1.54 子句改文档断言 / SC-3 S2 宿主句改 S2 后续表 / 孤儿引文清理); v8 = post_planning R1 后同步 (S2 项改为「激活后追加」/ SC-7 plugin-cache-currency 例外 / 决策单路径勘正); post_spec R1–R5 (R5 五席全票 PASS 0C/0M; 严格键集合未稳定 ⇒ MAX_ROUNDS_EXHAUSTED, owner 裁定 [1] 接受, `overridden_by_user=true`); 四项决策点已裁 (Level 3 / D-0 a / D-1 a / D-2 a / D-3 a, 决策单同上), **v7 = 裁定回填** (条件任务 T9/T13 转正); 下一步 A.2/A.3。R1..R5 聚合见 §References。
> **Created**: 2026-09-05
> **Linked Issue**: `10CG/Aria#193, 10CG/aria-plugin#135`
> **Track / claim**: `owner-container-identity-key-and-collision-parser` (phase A claim `s-8204@1355`, container `bfe8285d`, linked_issue `10CG/Aria#193`, overlap 告警空)
> **代码落点**: `aria/` 子模块 (state-scanner `lib/collision.py` `lib/identity.py` `lib/constants.py` `scripts/collectors/handoff_multibranch.py` `scripts/renderers/track_board.py` `scripts/phase1_gate.py` `scripts/release_gate.py` + references; phase-d-closer `tests/test_fetch_gate.py`) + `standards/` 子模块 (session-handoff.md §2.3); Spec 落主仓 (Rule #5)
> **Triage 依据**: `.aria/triage-report.json` / [#193 comment 21431](https://forgejo.10cg.pub/10CG/Aria/issues/193#issuecomment-21431) (partial-repro / major / next-cycle)
> **冻结语料**: `.aria/repro/handoff-tracks-frozen-2026-09-05.json` (起草日 `tracks_multibranch.tracks[]` 非 legacy 行, 996 行, 已纳入版本控制; 实验表与 SC-6 都对它跑)
> **相邻在飞 Spec**: [`a1-entry-claim-duplicate-work-guard`](../a1-entry-claim-duplicate-work-guard/proposal.md) (对方容器 `023236f2`, 待 B.1) — 其 §3 已把「`owner-container` 与 claim container 段口径不同, 两标识关系需成文」记为 follow-up 且明示不在其内统一; 本 Spec 即该 follow-up。**两处耦合**: (1) `identity.py` flip 与其 SC-3 (§Impact 排序); (2) 其 track-id 含 `<container_uuid>` 段, 与本 Spec 的同 track 分组正面冲突 (决策点 D-0)。

## Why

多终端协调的唯一 advisory 信号 `tracks_multibranch.collision` 目前不可信, 原因有三层:

1. **解析器格式契约错位 (triage 新发现, 主根因)**: `lib/collision.py::split_owner_container` 按三段式 `owner/container/session` 解析 (契约起点 aria `f9306a0` 2026-05-20 `track_board.py`, `83a1a45` 05-30 迁入 `collision.py`), 而 handoff frontmatter 按 `session-handoff.md §2.3.1` 是两段式 `<owner>/<container-id>` (主仓 154 份 frontmatter: 142 两段 / 12 零段 / **0 三段**)。两段串被拆成 `(owner='', container=<owner 段>, session=<uuid>)` ⇒ `owner` 恒 `unknown` ⇒ `cross_owner` 从 handoff 数据**永远不可达**。直接调用复现 (triage case-2..5): 同容器双 owner 串 → 🟡; **真两人两机 → 也是 🟡 (降级)**; **同人两机 → `none` (漏报)**; 三段式串才得 🔴。
2. **owner 段随 git 身份漂移 (Aria #193)**: 同一物理容器 `git user.email` 变更后机械填规则忠实记录 → 同一 container 出现多个 owner 串。两个 uuid 容器都发生且方向相反: `bfe8285d` = `simonfish/…` 34 份 (07-05..08-27) + `aria-runner-bot/…` 2 份 (09-03..), 漂移点在 08-26/08-27 之间; `023236f2` = `aria-runner-bot/…` 23 份 (07-05..08-16) + `simonfish/…` 17 份 (07-03..09-05)。Aria 现行规范只定义 `<owner>` = git `user.email` local-part, **没有 AI runner 该以什么 git 身份提交的规范**。附带事实: Aether 的机器账号已于 2026-07-01 从 `aria-runner-bot` 改名 `10cg-ci-bot`, 本容器现用 local-part `aria-runner-bot` 本身是旧名 (D-2 后果之一)。另: `<owner>` 在 git 未配置 email 或 email 无 `@` 时会真实取值 `unknown` (`lib/identity.py:165-185`), 判据必须显式排除它。
3. **container 段来源不稳 (aria-plugin #135 缺口 3 + 08-13 补充)**: container 段先后是主机名 (`dev-claude` / `dev-claude2`, 跨机不唯一) 与 uuid (`bfe8285d` / `023236f2` / `f9c6e8cd`); `lib/identity.py::get_container_id()` 是 `label if label else uuid`, 文件头注释又邀请填 label ⇒ 填个可读名就静默换了协调身份 (08-12 实测 `claim_not_found` 孤儿 claim)。主仓 frontmatter 今天是 **10 种 owner-container 串, 5 个 container 标识 (3 uuid + 2 主机名), 实际 2 台在用机器**。

**为什么三层一起处置 (冻结语料 + 生产路径 `collector dedupe → classify` 实测)**: 只修第 1 层会把「静默失灵」换成「响亮误报」—— 主机名时代同一 owner 的两台机 (`simonfish/dev-claude` vs `simonfish/dev-claude2`) 与零段/两段混写的同一台机 (`dev-claude` vs `simonfishgit/dev-claude`) 立刻被判 🔴。第 2/3 层给出身份键与「不可归属 owner 不计数」两条**确定性**规则后, 这两组回到 🟡; 而漂移造成的「两个提交身份」在数据上就是两个身份, 本 Spec **不推断它们是不是同一个人**, 而是判 🔴 并用 ⚪ 漂移 advisory 并排解释, 由 D-2 停止未来漂移。

## What

四个交付面 (代码 / 规范 / 看板告警 / 消费面同步) + 发布同步, 四项 owner 决策点 (D-0 ~ D-3)。

### Key Deliverables

**D1 — 解析器、身份键、判定键 (aria)** — 全部是**纯输入函数**, 不读语料历史、不持久化状态:

- **解析**: `split_owner_container` 按两段式: `<owner>/<container>` → `(owner, container, "")`; 三段式 (Layer L `superseded_from` 形, 不经此函数校验) 保持 `(owner, container, session)`; 零段 → `("", <串>, "")`。规范不改三段 (frontmatter 无 session 概念, §2.3.6 写入频度 = 会话结束一次)。
- **身份键** `identity_key(owner, container)`: container 匹配 `^[0-9a-f]{8}$` ⇒ `container`; 否则 (主机名 / 空 / 只读 fs 兜底) ⇒ `owner + "/" + container` (零段串 owner 为空 ⇒ `"/" + container`)。**已知限制** (成文): 兜底 hostname 或 label 恰为 8 位小写 hex 会被当 uuid; 该路径本身是降级路径。
- **dedupe 键** (`handoff_multibranch.py:518-523`, **显式改动**) = `(track_id, identity_key)`: 同 uuid 容器多 owner 串折叠为最新一行; 主机名容器保留 owner 段 (既有测试 `test_owner_segment_participates_in_grouping_key` 的不变式只在主机名域成立, 改写为两臂 + `devbox01` 对抗臂)。
- **判定** `classify_claims` (签名不变): 同 track 的 active 行 (dedupe 后) 按 `identity_key` 计数: `<2` → `none`; `≥2` 时取 **非空且非 `unknown`** 的 owner 串集合 (空 / `unknown` = 不可归属, **不计为独立 owner**): 集合大小 `≥2` → `cross_owner`; `≤1` → `self_multi_container`。**没有「同一个人」推断**: 两个不同 owner 串在两个 uuid 容器上 = 两个提交身份 = 🔴。
- **Layer H track 族键 (仅 D-0 选 (a) 时, 见决策点)**: 在 **`track_to_claim_record` 一处** (Layer H 两条路径 `collision.py:347` / `track_board.py:783` 同源; Layer L claim 不经它) 对 `ClaimRecord.track_id` 做**纯形状**剥离: 尾段匹配 `-[0-9a-f]{8}$` 即剥。行内确定, 不查语料。**作用域**: 只改 Layer H `ClaimRecord.track_id` 用于 §2.3.5 collision 分组; **不改** frontmatter 原串、不影响 §2.3.8.2 carry-id 同串规则、不触及 Layer L claim 的 track_id 匹配 (Layer L 不经 `track_to_claim_record`); 渲染器 `tracks_by_tid` 标签索引须用同一剥离后键构造 (T8)。**已知限制**: 日期形尾段 (如 `-20260719`) 也会被剥; 冻结语料 117 个 track_id 只此 1 例且剥后零合并 (SC-2 反例夹具锁住)。
- **board 标签** (`track_board.py:412-417`, **显式改动**): 建表键与查表键同源归一 (都经 `track_to_claim_record`), 修掉今天就查不中的 bug。
- **`lib/identity.py`**: 新增 `get_container_label()` (公开 accessor, S1 即落); `get_container_id()` 改 uuid 优先 (只读 fs 兜底仍 hostname; **S2 才落**)。
- **T3b 迁移检查 (两态, 不进 `identity.py`)**: 挂 `phase1_gate.py` (它在 `:486` 已解析 `Identity` 并显式传入 `acquire_claim` `:773`) 与 `release_gate.py` (今天零 identity 耦合, `release_claim_by_track` 内部重解析 ⇒ 需 import identity + `get_container_label()` + `read_claims` 枚举 + 传 `identity=` 覆盖)。**S1 语义** = 纯 inventory 告警: label 非空 → 告警并列出 `claims/<label>/` 下 active 数, **无抑制**。**S2 语义** = 发布门: 该检查是 flip 发布前置 (检查不过则本次发布不含 flip), 不是运行时开关 (静态语义无法按进程「拒绝」)。

**D2 — 规范成文 (standards, `session-handoff.md §2.3`)** — 判据用标准自身定义的词写, 不引用 aria 代码; **不引用任何 Lab 私有文档**:
- §2.3.1 `owner-container` 行改写为三态 + 规则: `<owner>` 语义按 D-1, 并注明取值可为 `unknown` (git 未配置 email); `<container-id>` = `~/.aria/container-id` 的 **uuid 字段** (v1.22.x+ 有该文件的机器; label 不参与); 无该文件的历史行 = 主机名; 只读 fs 兜底 = hostname。**在此定义 `identity_key`**: 8 位小写 hex 形 ⇒ 该串; 否则 ⇒ `<owner>/<container-id>`。按 D-0(a) 裁定加一句 track-id 尾段 `-<8hex>` 的族键语义, **显式限定**「仅用于 §2.3.5 Layer H collision 分组; 不改变 §2.3.8.2 carry-id 与 frontmatter `track-id` 同串的规则, 不用于 Layer L claim 匹配」。
- §2.3.5 判据表 (**实质变更**, 对采用方是行为变更, 在 standards 变更说明 + aria CHANGELOG 明示): `cross-owner` = 同 track ≥2 个 `identity_key` 且**非空、非 `unknown`** 的 `<owner>` 集合 ≥2 → 🔴; `self-multi-container` = ≥2 个 `identity_key` 且该集合 ≤1 → 🟡; 新增 **`same-identity-multi-owner`** = 同一 `identity_key` 在**采用方仓的 handoff 全集 (跨 track、跨分支)** 出现 ≥2 个非空非 `unknown` `<owner>` → ⚪ 信息级 advisory, 不计入 collision。
- **新增 §2.3.9**「AI runner 提交身份」(§2.3.7/§2.3.8 已占用): 按 D-2 裁定 (a) 写: 「AI runner 会话的 git 提交身份统一为机器身份, `user.email` local-part 与采用方机器账号名一致; 操作者可追溯性由 `<container-id>` + handoff 承担」; 只写「采用方的人机账号治理与容器 `git config` 供给不在本规范」。10CG Lab 内部指针 (Aether 两账号模型) 已落主仓决策单 `.aria/decisions/2026-09-05-owner-container-identity-key-rulings.md`, 不进 standards (不另建 `docs/decisions/` 文件)。
- 历史 handoff **不 rewrite** (与 Kairos DEC-2026-09-04 一致)。

**D3 — 漂移 advisory (aria)**
- 新增 `lib/collision.py::identity_drift_advisories(tracks) -> list[dict]`: 输入 = collector 的**全部非 legacy 行 (dedupe 前, 跨 track)**, 输出每个出现 ≥2 个非空非 `unknown` owner 串的 uuid `identity_key`: `{identity_key, owners[], first_seen, last_seen}` (`first/last_seen` 取 `updated_at` 极值)。**`classify()` / `classify_claims()` 签名不变**; collector 在 `handoff_multibranch.py:709` dedupe **之前**对原始 `tracks` 调用, 写入 `tracks_multibranch.collision.identity_advisories[]` (**恒存在**, 空时 `[]`; 既有断 `keys == {kind, groups}` 的两条测试点名改写, 见 T2); 渲染器 `track_board.py:743-747` 已持有原始 `tracks` (它自己 dedupe), 在 dedupe 前同样调用, 渲染 ⚪ 行 —— 两处同源。legacy 行 (`owner_container == "unknown"`) 不参与。D-3 的新鲜度截止**不**作用于 advisory。
- 与 #182 的关系是**依赖**: `track_to_claim_record` 把 `active`/`legacy` 与 **8 种非 enum status (280/996 行)** 一律映射为 active (`collision.py:113-124`), 其中 104 行 `active` 最早 2026-05-20, 全部远超 `STALE_TTL=1800` 却仍被 `:374-379` 捞回。本 Spec 修分类逻辑正确性; 信号可用性由 D-3 裁定; 非 enum status 的终态归一属 #182。

**D4 — 消费面同步 (aria)** — `collision.kind` 枚举取值不变, 但真实数据上的命中面变了 (`cross_owner` 首次可达):
- 文档 (七处): `references/layer-l-integration.md:25-27,73,77` · `RECOMMENDATION_RULES.md:31` (rule 1.54) · `references/rules/advanced-rules.md:544-572,578` · `references/state-snapshot-schema.md:1085` (collision 段 + 新字段) · `references/phase-1-collectors.md:75` · `SKILL.md:149-154` (**含取值字面** `cross-owner` / `self_multi_container` 作为编排触发条件; **取值不变故不改动**, 语义变更经 §2.3.5 + CHANGELOG 明示 ⇒ Rule #6 零 SKILL.md 改动成立) · `aria/templates/session-handoff.md` (owner-container 示例改 uuid 形, **并删除**示例旁「设 label 使更可读」的鼓励句 —— S1 窗口期它仍会把用户引向 #135 缺口 3 的 bug 入口)。
- 代码消费方: `aria/skills/phase-d-closer/scripts/fetch_gate.py:251` (`collision_kind != "none"`) + `tests/test_fetch_gate.py`: 它只收 kind 字符串, 行为不变; 加一条 `kind="cross_owner"` 字符串夹具确认 advisory 文案 (不是两段式夹具)。

**D5 — 发布同步 (aria-plugin 版本档位)**: 按 CLAUDE.md §版本管理「新增 Skill / Skill 架构重构 = MINOR+; 文档更新 / bug 修复 = PATCH」: 本 Spec 无新 Skill、无架构重构, 是 bug 修复 + additive 字段 ⇒ 判据上 **PATCH**; 但 §2.3.5 对采用方是行为变更, owner 可据此升 MINOR (二选一记入 CHANGELOG); 同步面按 CLAUDE.md §版本管理 (aria 子模块 5 文件 + 主仓 gitlink + VERSION + README badge + i18n 仅版本串 + 架构文档版本行); standards 版本口径沿对方容器待裁项 (`standards/openspec/project.md` 2.2.2 vs 主仓 VERSION 2.2.3), 本 Spec 不另起口径。

### 实验表 (冻结语料 996 行, **生产路径** `dedupe_latest_per_track_container → classify`, R3 三席独立复现一致)

| 变体 | dedupe | `collision.kind` | groups |
|---|---|---|---|
| A 现状 (三段式解析, 现 dedupe 键) | 996→121 | self_multi_container | `[dev-claude, simonfishgit/dev-claude]` |
| B 只修解析 | 996→122 | **cross_owner (误报)** | 上组 + `[simonfish/dev-claude, simonfish/dev-claude2]` |
| **D1 全套** (解析 + identity_key dedupe + 不可归属规则) | 996→122 | self_multi_container | 同 B 的两组, 均 🟡 (主机名时代同一 owner 两机 / 同一机零段+两段混写) |

合成用例 (经 dedupe → classify, 与语料无关): 两人两机 `alice/aaaa1111` + `bob/bbbb2222` → **cross_owner**; 同容器双 owner `simonfish/bfe8285d` + `aria-runner-bot/bfe8285d` → **none**; 同人两机 `simonfish/bfe8285d` + `simonfish/023236f2` → self_multi_container; 漂移后 `aria-runner-bot/bfe8285d` + `simonfish/023236f2` → **cross_owner** (两个提交身份, 诚实 🔴 + ⚪ 解释); 既有隔离夹具对 `aria-runner-bot/023236f2` + `simonfish/bfe8285d` → **cross_owner** (期望改写, T4); 零段 vs 两段同主机名 → self_multi_container; 两人先后共用一机 `erin/eeeeeeee` + `frank/eeeeeeee` → none; 三 owner 同 uuid → advisory `owners[]` 长度 3; `devbox01`/两 owner → 不折叠。

D3 advisory 对象 (冻结语料, 对 dedupe 前全语料算): `023236f2: [aria-runner-bot, simonfish]` · `bfe8285d: [aria-runner-bot, simonfish]`。**结论**: 真实语料里没有真正的两人撞车; 修后两组 🟡 都是 2026-05..07 的 stale 行 (#182 形态), SC-6 机械归因。

## 决策点 (owner 2026-09-05 已全部裁定; 选项与后果保留为记录)

**D-0 与 a1-entry 的 track-id 契约冲突 (R2 tech-lead C-1)** — a1-entry 把 A.1 派生串定为 `<spec-slug>-<container_uuid>` 并规定它就是 carry-id; `session-handoff.md §2.3.8.2` 要求 carry-id 与 frontmatter `track-id` 同串 ⇒ 两容器对同一 Spec 写出的 handoff 落**不同** `track_id`, 本 Spec 的全部判定 (在 `track_id` 内, `collision.py:367`) 对 A.1 认领的 Spec 恒 `none`。
- (a) **本 Spec 加 Layer H track 族键**: `track_to_claim_record` 对 `track_id` 尾段 `-[0-9a-f]{8}$` 纯形状剥离 —— Aria 侧可独立落地, 行内确定, 不改 a1-entry 契约。后果: §2.3.1 多一句尾段语义; 日期形尾段会被剥 (已知限制, 语料上零合并); 两容器各自认领同一 Spec 时 Layer H 仍能报 🔴/🟡。
- (b) **请 a1-entry 把容器段留在 claim raw id, 不写进 frontmatter `track-id`** —— 跨 Spec 改动, 需对方容器同意且其已过 R6。后果: 本 Spec 零改动, 依赖对方返工; 且 §2.3.8.2「carry-id 与 frontmatter track-id 同串」要求 carry-id 也随之去掉容器段, 与 a1-entry 用 carry-id 喂 `phase1_gate --raw-track-id` 的设计相冲, 对方要连带改 §2.1b。
- (c) **接受 A.1 认领的 Spec 不走 Layer H collision**, 只靠 Layer L overlap。后果: Layer H 对新 Spec 失去 🔴/🟡, 只剩接棒功能。
- (d) **两 Spec 合并为一个 Spec 处理**。后果: 范围膨胀到 40+ 任务, 且需对方容器让渡 claim; 不建议。
- 执笔建议: (a), 并在 Aria #174 留言征求 a1-entry 侧意见。
- **✅ 裁定: (a)**。T9 转正式任务; #174 留言改为「告知」(不改对方契约)。

**D-1 `<owner>` 段语义** (与 D-2 **耦合**, 请一起裁)
- (a) **提交身份** (现状: git `user.email` local-part; 机械可得, 零配置)。后果: 同一人换 email 就是另一个 owner 串 ⇒ 与其他容器并存时判 🔴 (需人读 ⚪ 才知是漂移); D-2(a) 生效后新漂移停止, 历史双串靠「不 rewrite + dedupe 取最新行」淡出。
- (b) **人** (需 `owner-map`)。后果: 不受漂移影响; 引入常驻维护面, 跨采用方不可移植。
- 执笔建议: (a)。
- **✅ 裁定: (a) 提交身份**。

**D-2 AI runner 的 git 提交身份** (每个选项都写 `cross_owner` 可达性)
- (a) **统一机身份**: 所有 AI 会话署同一 bot local-part。收益: owner 段稳定, 与 Aether 人机两账号对齐。**代价**: 同一 owner 的 AI 会话之间 `cross_owner` 结构性不可达 (🔴 = 另一提交身份: 另一位操作者的容器 / 人手工署名会话); 署名失去「哪位操作者在场」(靠 container 段 + handoff 追溯); bot 名要选 (Aether 现名 `10cg-ci-bot`; 沿旧名与台账不一致, 改名则一次性漂移, ⚪ 可解释)。
- (b) **人身份**。收益: 可追溯到人; 两位操作者之间 🔴 可达。代价: 与 Layer 2 生产侧 (bot) 不一致; 操作者换 email 即漂移。
- (c) **不规定**。收益: 零改动。代价: 漂移继续, ⚪ 常亮; `cross_owner` 可达但**不可解释** (每次身份变动都可能制造一次 🔴, 无法区分真撞车与漂移)。
- 执笔建议: (a) 且 local-part 与 Aether 现名一致。范围: 本 Spec 只写 Aria 侧规则。
- **✅ 裁定: (a) 统一机器身份, local-part 与采用方机器账号名一致** (10CG Lab = `10cg-ci-bot`); 本容器 git 身份的实际变更为 owner 环境动作。

**D-3 Layer H 新鲜度截止 (回应 #182 依赖)**
- (a) **本 Spec 内加截止** (条件任务 T13 / SC-11): 共享谓词 `layer_h_is_fresh(row, now, days)` (lib), `updated-at` 早于 `LAYER_H_ACTIVE_WINDOW_DAYS` (建议 30; 与 `STALE_TTL` 秒级分名分量纲) 的行在 Layer H 记录构造阶段不进 reconcile/classify (人口 = 被映射为 active 的全部行, 含 280 行非 enum), board 以「stale」列出; collector 与 renderer 调同一谓词; **不与 `:374-379` 叠成三档** (被截止的行 reconcile 看不到)。后果: 信号 ship 即可用; 多一个常量 + 一条规范句。
- (b) **不加, 交 #182**。后果: 逻辑正确但 board 仍有 2026-05 的 🟡 组, Positive 只能写「逻辑正确」。
- 执笔建议: (a)。
- **✅ 裁定: (a)**。T13 转正式任务, `LAYER_H_ACTIVE_WINDOW_DAYS = 30`。

## Impact

| Type | Description |
|------|-------------|
| **Positive (条件式)** | 分类逻辑第一次同时满足: **不同提交身份**跨容器并存 = 🔴; 同一提交身份多机 = 🟡; 同 uuid 容器多 owner 串 = ⚪。Layer H 与 Layer L 的 container 口径统一为 uuid (**S2 后完全成立**; S1 下 `handoff_autofill` 仍经 label 优先的 `get_container_id()`, 设了 label 的机器仍会写 label 形)。**条件**: D-1(a)+D-2(a) 下 🔴 = 「另一提交身份」; 信号可用性取决于 D-3; **label 陷阱结构性消除只在 S2 形态成立**; S1 形态下 label 形态既无 flip 也无 ⚪ (⚪ 只对 uuid key), 只有 T3b 的 inventory 告警 |
| **Risk / 已知限制** | (1) §2.3.5 判据实质变更 + dedupe 键变更 ⇒ 采用方看板输出改变 (A→D1: 组数 1→2, 都是 stale 🟡); 缓解: SC-6 归因 + standards 变更说明 + CHANGELOG。(2) reconcile tie-break 键两段式下退化为 `container/unknown`; 秒级 `updated-at` 全同的同容器两行实践不出现; SC 锁不崩溃。(3) `oc_by_tid_key` 三元组在未 dedupe 输入上可撞键; 生产路径恒先 dedupe, SC 锁契约注释。(4) 8 位 hex 主机名/label 被当 uuid。(5) 漂移期历史 🔴 需人读 ⚪。(6) **两个真人在同一 uuid 容器上认领同一 track → `none`** (owner 不参与同一性的镜像漏报), 只有 ⚪ 提示。(7) D-0(a) 日期形尾段被剥; 渲染器 `tracks_by_tid` 索引若未随剥离归一会退化标签 (T8 锁) |
| **`get_container_id()` 消费方 (全列)** | `get_identity()` → `lib/claim_lifecycle.py:39,88` / `scripts/phase1_gate.py:294` (winner 归属) 与 `:486` (Identity 解析) `:773` (传入 acquire) / `lib/concurrent_tracks.py:25,133` / `scripts/release_gate.py:132` (间接; 今天零 identity 耦合) / session-closer `handoff_autofill.py:391` (`def owner_container`)。flip 影响面即这六处 |
| **与 a1-entry 的边界与两种 ship 形态** | 耦合 1 (`identity.py`): a1-entry 新增 `get_container_uuid()` (:660), 其 SC-3 (:571) 以「`get_container_id()` label 优先 ⇒ 直接调它的实现必红」为前提; 本 Spec flip 会让它恒绿。**S1 (a1-entry 未落地时 ship)**: 只加 `get_container_label()` + T3b inventory 告警, **不 flip**。**S2 (a1-entry B.2 已落地且对方在 #174 ack 改写其 SC-3)**: flip + 发布门 + 由本 Spec 改写其 SC-3。**S2 项不进 tasks.md checkbox** (归档门只读 checkbox, 无条件任务机制): 满足激活条件 (S2-candidate + ack + merge 前) 时追加 6.x 任务; 否则由 tasks.md 5.8 在 merge 后、归档前**手动**开 tracker issue 记录 S2 后续 (归档 Step 7 干净归档不自动产出; #192 是 deferred 非空时的自动路径, 型别不同), SC-3 的 S2 臂不进本 cycle 验收。S2 激活时对方 SC-3 改写为「`get_container_uuid()` 与 flip 后 `get_container_id()` 同值; label 只在 `get_container_label()`」; 未取得 ack 不动对方文本。耦合 2: D-0。行号漂移: 后落地方在 D 期 refresh |
| **Rule #6** | 不改任何 SKILL.md 指令面 / description (取值字面存在但不变) ⇒ 「描述性 / 机械」档 substitute = SC 级 baseline-failing 结构化测试 **SC-1 / SC-2 / SC-3 (S1 臂; flip 臂仅 S2) / SC-4 / SC-8**; SC-5/6/7/9/10/11 为文档 / 对照 / 回归 / 渲染 / 条件项。`rule6_note` 随 B.2 写入 |

## Tasks (代码 6 个 .py + `lib/constants.py` + 1 份规范 + 7 处文档 + 1 处代码消费方; 14 个 checkbox 含 T3b; **T9 / T13 经 D-0(a) / D-3(a) 裁定已转正式任务**)

- [x] T1 `split_owner_container` 两段式 (含零段 / 三段兼容); 改写 `test_split_owner_container_variants` 的 2-part 与 1-part (`"solo"`) 断言, 先红后绿两臂 → SC-1
- [x] T2 `classify_claims` 确定性判定 + `identity_drift_advisories(tracks)`; collector `:709` dedupe 前调用并写 `collision.identity_advisories[]` (恒存在); **改写 `test_real_collector_emits_cross_owner_collision` / `test_real_collector_no_collision_is_none` 的 `keys == {kind, groups}` 断言**; `state-snapshot-schema.md` additive bump; 字段集回归由上述两条 collector `keys` 断言 + 双跑全套承担 (`test_normalize_snapshot` 实读不锁 collision 段, 不引用) → SC-2 / SC-8
- [x] T3 `get_container_label()` (S1 即落); `get_container_id()` uuid 优先 (S2 才落); container-id 文件头注释改写 → SC-3
- [x] T3b 迁移检查两处: `phase1_gate.py` (复用 `:486` Identity) / `release_gate.py` (import identity + `get_container_label()` + `read_claims` + 传 `identity=`); S1 = inventory 告警; S2 = 发布门 → SC-3
- [x] T4 dedupe 键 `(track_id, identity_key)`; `test_owner_segment_participates_in_grouping_key` 三臂 (uuid 折叠 / 主机名不折叠 / `devbox01` 不折叠); `test_both_latest_active_still_reports_self_multi_container` 期望改 `cross_owner` + 新增同 owner 串变体断 🟡; `track_board.py:412-417` 键同源 → SC-4
- [x] T5 `session-handoff.md` §2.3.1 (三态 + `identity_key` 定义 + `unknown` 取值说明) / §2.3.5 (三行, 「非空非 unknown」, advisory 作用域, 实质变更说明) / 新 §2.3.9 (按 D-1/D-2 回填) → SC-5
- [x] T6 冻结语料复制为 aria 测试 fixture (只保留 `track_id / owner_container / status / phase / updated_at / filename / branch / legacy` 八字段 (`phase` 被 `track_to_claim_record` 读取)); 前后对照测试机械归因 (判据见 SC-6); 「真撞车」档注入一组合成行 (显式标注) → SC-6
- [x] T7 消费面同步: 七处文档 (D4) + `test_fetch_gate.py` `kind="cross_owner"` 字符串夹具; rule 1.54 触发面锁定 → SC-9
- [x] T8 `track_board.py` ⚪ 行渲染 (dedupe 前调用 `identity_drift_advisories`) + label 并列显示; D-0(a) 时 `tracks_by_tid` 标签索引改用剥离后键 (与 `verdicts` 键域一致) → SC-10
- [x] T9 (D-0(a) 已裁) `track_to_claim_record` 族键剥离 + §2.3.1 尾段语义 + 三条夹具 (`slug-aaaa1111`/`slug-bbbb2222` 同组; `x-20260719` 剥后与语料零碰撞; `slug-abcdefg` 不剥) → SC-2 条件用例
- [x] T10 全套回归: state-scanner 两种跑法 (run_tests.py 全套 + pytest 对 test_collision.py; 点名改写项全绿) + `test_fetch_gate.py` + session-closer / phase-d-closer handoff 写入测试 + 主仓 state-check 13 条全绿 + `plugin-cache-currency` 例外 → SC-7
- [x] T11 issue 回帖 (文档动作, 无 SC), 两个时点: **B.1 起手** (tasks.md 0.2) #174 留言 D-0 与 SC-3 改写征求 ack (S2 激活前提之一, 见上表 :104 行); **merge 后、归档前** (tasks.md 5.5) 回帖 #193 / aria-plugin#135 指向本 Spec + 版本, #174 补 ship 结果, 关 #193; #135 措辞按形态 (S1 = 缺口 3 部分闭合, label 陷阱待 S2 或 tracker; S2 = 缺口 3 闭合), 缺口 1/2 均留
- [x] T12 发布同步 (D5): aria-plugin 版本 bump (档位按 D5 二选一, 记入 CHANGELOG) + CLAUDE.md §版本管理同步面 (含 i18n README ×3 版本串) + CHANGELOG 明示 §2.3.5 行为变更; Lab 内部指针已在 `.aria/decisions/` 决策单 → SC-7
- [x] T13 (D-3(a) 已裁) `layer_h_is_fresh` 共享谓词 + `LAYER_H_ACTIVE_WINDOW_DAYS` 常量 + collector/renderer 同一调用 + §2.3.5 规范句 → SC-11

## Success Criteria

- [ ] SC-1 (T1) `split_owner_container("simonfish/bfe8285d") == ("simonfish","bfe8285d","")`; `("solo") == ("","solo","")`; `("a/b/c") == ("a","b","c")`。**先红** (现 `("","simonfish","bfe8285d")` / `("","","solo")`)
- [ ] SC-2 (T2/T9) **判定臂** (经 dedupe → `classify()`): 同容器双 owner → `kind == "none"`; 两人两机 → `cross_owner`; 同人两机 → `self_multi_container`; 漂移后无共现 → `cross_owner`; 零段 vs 两段同主机名 → `self_multi_container`; 端到端 (collector 夹具 → dedupe → classify) 真实两段式两人两机 → `cross_owner`; D-0(a) 时 `<slug>-<uuid1>` / `<slug>-<uuid2>` 两容器 → 可达 🟡/🔴, 且 `x-20260719` 剥后与语料零碰撞、`slug-abcdefg` 不剥。**advisory 臂** (对 dedupe **前**全语料): 同容器双 owner → advisory 恰 1 条 `{identity_key: bfe8285d, owners: [aria-runner-bot, simonfish]}`; 同 uuid 容器两串跨两份 handoff, dedupe 折叠后 advisory 仍恰 1 (**函数级反事实: 对 deduped 调用 → 0**); **生产接线端到端**: 真实 collector 夹具 (`_build_repo` 风格, **uuid 形容器** `aaaa1111` 而非 `box-A`) **同一 `track_id`** 下两份 handoff 两串 (dedupe 只在同 track 内折叠, 否则反事实读不到 0) → 经 `collect_handoff_multibranch` 完整采集后 snapshot `collision.identity_advisories` 恰 1 条 (**接线反事实: `:709` 传 `deduped_tracks` → 0, 红**); ≥3 owner → `owners[]` 长度 3; legacy 行不产生 advisory; owner 为 `unknown` 的行不产生 advisory。**判定臂前三条先红** (现 🟡 / 🟡 / none)
- [ ] SC-3 (T3/T3b) **S1/S2 共同**: container-id `label` 非空且 `claims/<label>/` 有 active 时, `phase1_gate` **与** `release_gate` 各自输出迁移告警 (含 active 数); `get_container_label()` 返回 label。**仅 S1**: lock-in 断言 `get_container_id()` 在 label 非空时**仍**返回 label (S1 不得偷 flip, 否则 a1-entry SC-3 静默恒绿)。**仅 S2**: `get_container_id()` 返回 uuid; 复现 #135 08-13 时间线不再 `claim_not_found`; 发布门检查不过时 flip 不进该次发布 (**宿主 = phase-c-integrator C.2 前的 release 清单检查项**: 清单含「T3b 迁移检查通过」勾选, 未勾选则 flip 提交不进合并集; 断言写在 S2 激活后追加的 6.2 任务, 非运行时代码)。**先红** (现无 label accessor、无告警)
- [ ] SC-4 (T4) 同 track 同 uuid 容器不同 owner 两行经 dedupe 折叠为 1 (**先红**); 同主机名不同 owner 不折叠; `devbox01`/两 owner 不折叠; board 对两段式串回显原串 (**先红**: 键 `""` vs `"unknown"` 失配); 隔离夹具对断 `cross_owner`, 同 owner 变体断 `self_multi_container`
- [ ] SC-5 (T5) §2.3.1 含 token `identity_key` 与三态 (`uuid` / `主机名` / `hostname`) 与 `unknown` 说明; §2.3.5 恰三行, 含 token `非空` `unknown` `same-identity-multi-owner` `全集`, **不含** token `等价类` / `aria/skills` / `lib/`; §2.3.9 存在、含 D-2 裁定文本、**不含** `/home/` `Aether` `forgejo-token-map` `Kairos` `DEC-2026` `10cglocal`; §2.3.1 的尾段句 (D-0(a) 时) 含 token `仅用于` 与 `§2.3.8.2`; §2.3.7/§2.3.8 diff 零
- [ ] SC-6 (T6) 对 fixture 跑生产路径: 改前 A = 1 组 / 改后 = 2 组 (D-3(a) 时 0 组); **机械归因**: 组内全部行 `updated_at` 早于 30 天 (D-3(a) 时读常量 `LAYER_H_ACTIVE_WINDOW_DAYS`; D-3(b) 时该常量不存在, 归因测试自带 30 天字面只作标签, 此时改后组数为 2 而非 0) → `stale(#182)`; 否则 kind `cross_owner` → 真撞车, `self_multi_container` → 同人多机; 注入的合成真撞车组必须归入「真撞车」; 归因表由断言产出
- [ ] SC-7 (T10/T12) state-scanner 全套**两种跑法**在点名改写后零回归: (a) `python3 aria/skills/state-scanner/tests/run_tests.py` (unittest discover, 覆盖全部 TestCase 文件; 起草日 Ran 1476) 零失败; (b) `cd aria/skills/state-scanner && pytest -q tests/test_collision.py` (pytest 风格裸函数文件, 起草日 16 passed; 本 Spec 新建测试**文件**一律写 TestCase 以归 (a) 覆盖; 对 `test_collision.py` 的新增用例沿用该文件的 pytest 风格, 计入 (b) 的 passed 基数) 零失败; `test_fetch_gate.py` 全绿; session-closer / phase-d-closer 测试全绿; 主仓 state-check **13 条全绿 + `plugin-cache-currency` 例外** (bump 后必 STALE 直到 owner D 期 `/plugin update` + 重启, 与既往 ship 同形, handoff 记录 owner 动作)
- [ ] SC-8 (T2) snapshot `collision.identity_advisories` 恒存在且为 list (无漂移时 `[]`); 旧 snapshot 缺该字段时 `track_board` / rule 1.54 / `fetch_gate` 不崩。**先红** (字段不存在)
- [ ] SC-9 (T7) rule 1.54 为散文规则 (全仓 py 零命中, 无求值引擎) ⇒ 其触发面由**文档断言**承载: `RECOMMENDATION_RULES.md:31` 与 `references/rules/advanced-rules.md:544-572` 的 rule 1.54 行含 token `cross_owner` 与 `identity_advisories`; 六处取值文档 (不含 `aria/templates/session-handoff.md`, 它无取值字面; 模板由反向 grep 锁「设 label 使更可读」句已删) 的取值措辞与 §2.3.5 三行一致: 每个文件 F 与 token 集 {`cross_owner`, `self_multi_container`, `identity_advisories`} 的交集**不为空**, 且 F 中出现的每个该集 token 的上下文句与 §2.3.5 对应行同义 (人工核, 机械只锁非空交集; `RECOMMENDATION_RULES.md:31` 今日两 token 均无, 须同时补 `cross_owner` 与 `identity_advisories` 才满足首句); `fetch_gate` advisory 文案含 `cross_owner`
- [ ] SC-10 (T8) board 对 fixture 渲染恰 2 条 ⚪ 行 (`023236f2` / `bfe8285d`), 每行列 owners[] 与 first/last_seen; 无 advisory 时不渲染 ⚪ 段; **反事实**: 渲染器改为对 dedupe 后行算 → 0 行 (红)
- [ ] SC-11 (T13) fixture 中早于窗口的 active 行不出现在 `groups` 任一组; collector 与 renderer 对同一 fixture 得同一 `kind`/`groups`; 谓词只有一个实现 (grep 断言: `updated_at` 与天数比较的表达式在 collector / renderer 各零处, 只在 lib 一处; 同义改名绕过属 B 期 review 责任, 成文)

## 非目标

- 不推断「两个 owner 串是不是同一个人」; 不引入映射表、不持久化身份状态。
- 不改 Layer L claim schema / reconcile 仲裁规则; tie-break session 退化记为已知限制。
- 不处理 aria-plugin #135 缺口 1 / 缺口 2 (a1-entry 处置); 不改 a1-entry 的 track-id 契约 (D-0 只在本 Spec 侧适配或上呈)。
- 不修 #182 (status 收口与非 enum 归一); D-3(a) 只让 stale 行不参与判定。
- 不规定 Aether 账号 / 凭据, 不规定容器 `git config` 供给 (10cglocal); standards 不引用 Lab 私有文档。
- 不 rewrite 历史 handoff frontmatter。

## References

- Triage: `.aria/triage-report.json` (2026-09-05, partial-repro) · #193 comment 21431
- 审计: `.aria/audit-reports/post_spec-R{1,2,3,4,5}-…-owner-container-identity-key-and-collision-parser-aggregated.md` (+ 各席位报告; R5 终局 MAX_ROUNDS_EXHAUSTED, 五席全票 PASS 0C/0M)
- 规范: `standards/conventions/session-handoff.md §2.3.1 (:116) / §2.3.5 (:178-186) / §2.3.6 (:189) / §2.3.7-§2.3.8 (:204,:217, 已占用) / §2.3.8.2 (:234)`
- 代码: `aria/skills/state-scanner/lib/collision.py` (`split_owner_container` :63, `track_to_claim_record` :86 (status 映射 :113-124), `classify_claims` :143, `classify` :300 (Layer H 记录 :347, track_id 分组 :367, stale 捞回 :374-379 注释 / :379-383 代码)) · `lib/identity.py` (`get_owner` :158 (`unknown` :185), `get_container_id` :191, label 优先 :222, hostname 兜底 :242) · `scripts/collectors/handoff_multibranch.py:518-523, :709-714` · `scripts/renderers/track_board.py:177-185 (import), :412-417, :430, :743-747 (dedupe 调用), :783` · `scripts/phase1_gate.py:294, :486, :773` · `scripts/release_gate.py:132` · `lib/reconcile.py:151` · `lib/constants.py:36` · `aria/skills/phase-d-closer/scripts/fetch_gate.py:251`
- 消费文档: `references/layer-l-integration.md:25-27,73,77` · `RECOMMENDATION_RULES.md:31` · `references/rules/advanced-rules.md:544-572,578` · `references/state-snapshot-schema.md:1085` · `references/phase-1-collectors.md:75` · `SKILL.md:149-154` · `aria/templates/session-handoff.md`
- 决策记录: DEC-20260704-002 (病根 #3 机械填) · Kairos `docs/decisions/DEC-2026-09-04-git-identity-scope.md` (本地 checkout 已核; standards 不引用)
- 相邻 Spec: `a1-entry-claim-duplicate-work-guard` §2.1 (`<spec-slug>-<container_uuid>`) / §2.1a / §3 / SC-3 (:571) / Impact `get_container_uuid` (:660)
