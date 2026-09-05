# owner-container 身份键与 collision 解析器修正 (合并处置 Aria #193 + aria-plugin #135 缺口 3)

> **Level**: Minimal (Level 2 Spec)
> **Status**: Draft (A.1, 2026-09-05; owner 指令「起 Level 2 Spec 合并处置 #193 与 #135 缺口 3, 本容器接」)
> **Created**: 2026-09-05
> **Linked Issue**: `10CG/Aria#193, 10CG/aria-plugin#135`
> **Track / claim**: `owner-container-identity-key-and-collision-parser` (phase A claim `s-8204@1355`, container `bfe8285d`, linked_issue `10CG/Aria#193`, overlap 告警空)
> **代码落点**: `aria/` 子模块 (state-scanner) + `standards/` 子模块 (session-handoff.md §2.3); Spec 落主仓 (Rule #5)
> **Triage 依据**: `.aria/triage-report.json` / [#193 comment 21431](https://forgejo.10cg.pub/10CG/Aria/issues/193#issuecomment-21431) (partial-repro / major / next-cycle)
> **相邻在飞 Spec**: [`a1-entry-claim-duplicate-work-guard`](../a1-entry-claim-duplicate-work-guard/proposal.md) (对方容器 `023236f2`, 待 B.1) — 该 Spec §3 已把「`owner-container` 与 claim container 段口径不同, 两标识关系需成文」记为 follow-up 且**明示不在其内统一**; 本 Spec 即该 follow-up。文件级相邻面与排序规则见 §Impact「与 a1-entry 的边界」。

## Why

多终端协调的唯一 advisory 信号 `tracks_multibranch.collision` 目前**两个方向都不可信**, 且不可信的原因有三层, 分别由三张票/一次 triage 揭出:

1. **解析器格式契约错位 (本 Spec triage 新发现, 主根因)**: `lib/collision.py::split_owner_container` 自 2026-05-30 (aria `83a1a45`) 引入起按三段式 `owner/container/session` 解析, 而 handoff frontmatter 按 `session-handoff.md §2.3.1` 是两段式 `<owner>/<container-id>` (主仓 154 份 frontmatter 实测: 142 份两段 / 12 份零段 / **0 份三段**)。两段串被拆成 `(owner='', container=<owner 段>, session=<uuid>)` ⇒ `owner` 恒 `unknown` ⇒ `classify_claims` 的 `cross_owner` 分支**从 handoff 数据永远不可达**。用真函数直接调用复现 (triage case-2..5): 同容器双 owner 串 → 🟡; **真两人两机 → 也是 🟡 (真撞车降级)**; **同人两机 → `none` (漏报)**; 喂三段式串才得 🔴, 证明分类逻辑本身没错, 错在输入契约。
2. **owner 段随 git 身份漂移 (Aria #193)**: 同一物理容器的 `git user.email` 变更后, 机械填规则忠实记录 → 同一 container 在历史中出现多个 owner 串。实测两个容器都发生且方向相反: `bfe8285d` = `simonfish/…` 34 份 (07-05..08-27) + `aria-runner-bot/…` 2 份 (09-03..), 漂移点钉在 08-26/08-27 之间; `023236f2` = `aria-runner-bot/…` 23 份 (07-05..08-16) + `simonfish/…` 17 份 (07-03..09-05)。Aria 现行规范只定义 `<owner>` = git `user.email` local-part, **没有任何 AI runner 该以什么 git 身份提交的规范** (standards/conventions + CLAUDE.md grep 零命中)。
3. **container 段来源不稳 (aria-plugin #135 缺口 3 + 08-13 补充)**: 历史上 container 段先后是主机名 (`dev-claude` / `dev-claude2`, 跨机不唯一) 与 uuid (`bfe8285d`); 且 `lib/identity.py::get_container_id()` 是 `label if label else uuid`, 文件头注释又邀请用户填 label ⇒ 填一个可读名就静默换了协调身份 (08-12 实测: 认领 `bfe8285d`、释放时解析成 `dev-claude2` → `claim_not_found` 孤儿 claim)。主仓 frontmatter 今天仍是 **9 种 owner-container 串对应 2 台机器**。

三层叠加的后果 (真实数据实测, 见 §What 实验表): 修好第 1 层后看板才第一次能区分 🔴/🟡, 但立刻暴露第 2/3 层 —— `aria-runner-bot/023236f2` 与 `simonfish/bfe8285d` 会被判 cross_owner (两人撞车), 而它们是同一位 owner 的两台机器。所以三层必须一起处置, 单修 parser 会把「静默失灵」换成「响亮误报」。

## What

一个 Level 2 change, 三个交付面 (代码 / 规范 / 测试), 外加两项 owner 决策点 (§决策点, 未预设结论)。

### Key Deliverables

**D1 — 解析器与判定键对齐规范 (aria, `lib/collision.py` + 两个消费方)**
- `split_owner_container` 改为按 §2.3.1 两段式解析: `<owner>/<container>` → `(owner, container, session='')`; 三段式 (Layer L `superseded_from` 形) 保持 `(owner, container, session)`; 零段串 → `(owner='', container=<串>, session='')` (主机名时代遗留, 只能当 container 看)。**规范不改成三段**: frontmatter 没有 session 概念 (§2.3.3 写入频度 = 会话结束一次), 强加第三段只会制造第二个假契约。
- `classify_claims` 的判定键改为 **container 为同一性主键**: 先按 container 分组; ≥2 个 distinct container 时再看 owner —— owner 全同 → `self_multi_container`, owner 不同 → `cross_owner`; **同一 container 无论 owner 段几种, 视为同一身份**, 不参与 collision 计数, 但触发 D3 的显式 advisory。§2.3.5 判据表同步改写 (见 D2)。
- `scripts/collectors/handoff_multibranch.py:518` (dedupe key) 与 `scripts/renderers/track_board.py:412` (标签查找) 不改逻辑, 但因 `split` 语义变化, 其行为必须被 SC 锁住 (dedupe 现在能把同容器同 owner 的多行折叠; 标签仍回显原串)。
- `lib/identity.py::get_container_id()` 恒返回 `uuid`; `label` 降为展示字段 (新 accessor `get_container_label()`, board 渲染时并列显示)。**与 a1-entry 的关系见 §Impact**。

**D2 — 规范成文 (standards, `session-handoff.md §2.3`)**
- §2.3.1 `owner-container` 行: `<owner>` 语义按 §决策点 D-1 裁定写死 (「提交身份」= git email local-part, 或「人」= 另立映射); `<container-id>` 明确 = container-id 文件的 **uuid 字段** (label 不参与), 与 Layer L claim 的 `container` 同口径 —— 闭合 a1-entry §3 留下的「两标识关系需成文」。
- §2.3.5 判据表改为 container 主键版本 (与 D1 一致), 并新增第三行 **`same-container-multi-owner`**: 同一 container 在同一 track 或全仓历史中出现 ≥2 个 owner 段 → ⚪ 信息级 advisory「同容器多 owner 串 (git 身份漂移), 不计入 collision」, 不静默归类。
- 新增 §2.3.7「AI runner 提交身份」: 按 §决策点 D-2 裁定写入 (候选见下), 并交叉引用 Aether 人机两账号模型的边界 (Aria 只规定 owner 段怎么来, 不规定 Aether 账号)。
- 历史 handoff **不 rewrite** (与 Kairos DEC-2026-09-04 一致): 分类器按 container 主键合并后, 双串自然归到同一容器。

**D3 — 看板显式告警 (aria, `track_board.py` + snapshot)**
- `tracks_multibranch.collision` 新增 additive 字段 `identity_advisories[]`: 每条 `{container, owners[], first_seen, last_seen}`, 由 D1 的分组副产物产出; board 渲染为 ⚪ 行。零证据不当正证据: 无 frontmatter (legacy) 行不参与。
- 与 #182 (status 从不收口 → 历史 active 行堆积) 正交: 本 Spec 不改 status 语义; 但 SC 里用真实数据跑一遍, 把「修 parser 后暴露出的 stale active 撞车」如实记录到 handoff, 交 #182 处置。

### 实验表 (真实 handoff 数据, 2026-09-05 snapshot, 154 份 frontmatter)

| 变体 | `collision.kind` | groups |
|---|---|---|
| A 现状 (三段式解析) | self_multi_container | `[dev-claude, simonfishgit/dev-claude]`, `[aria-runner-bot/023236f2, simonfish/bfe8285d]` |
| B 只修 parser | **cross_owner** | 上两组 + `[simonfish/dev-claude, simonfish/dev-claude2]` |
| C 修 parser + container 主键 | cross_owner | `[simonfish/dev-claude, simonfish/dev-claude2]` (🟡), `[aria-runner-bot/023236f2, simonfish/bfe8285d]` (🔴 — 实为同一 owner 两机, 由 D-1/D-2 裁定后消解) |

同容器多 owner 串 (D3 将告警的对象): `dev-claude: ['', simonfish, simonfishgit]` · `dev-claude2: ['', simonfish]` · `023236f2: [aria-runner-bot, simonfish]` · `bfe8285d: [aria-runner-bot, simonfish]`。

## 决策点 (owner, 未预设; 裁定后回填 D2 文本)

**D-1 `<owner>` 段语义**
- 选项 (a) **提交身份** (现状: git `user.email` local-part, 机械可得, 不需要映射表)。后果: 同一人换 email 就是「另一个 owner」, 必须靠 D-2 把 AI runner 的身份收敛到一个值, 否则 cross_owner 会误报 (实验表 C 那组 🔴)。
- 选项 (b) **人** (需 `owner-map`: email local-part → 人名, 放 `.aria/` 或 standards)。后果: 分类准确但引入一张要维护的表, 且跨采用方不可移植。
- 执笔建议: (a) + D-2 收敛。理由: Aria 是可移植方法论, 不该要求采用方维护身份映射表; 「同容器多 owner」由 D3 显式告警, 不靠映射消解。

**D-2 AI runner 的 git 提交身份**
- 选项 (a) **统一机身份** (如 `aria-runner-bot@…`): 所有 AI 会话 commit 署 bot; owner 段恒同 ⇒ 同一 owner 的多机永远是 🟡, 另一人的容器 (另一个 bot 或人邮箱) 才 🔴。与 Aether「人 / 机」两账号模型对齐 (AI runner 归入机账号一类, 不是第三类)。
- 选项 (b) **人身份** (AI 会话沿用操作者 email): 署名可追溯到人, 但两位操作者的 AI 会话之间才能区分 🔴, 且与 Kairos/aria-runner 生产侧 (Layer 2 已用 bot) 不一致。
- 选项 (c) **不规定** (维持现状): 漂移继续, D3 告警持续常亮。
- 执笔建议: (a)。**本 Spec 只写 Aria 侧规范 (owner 段怎么来、AI 会话该署什么)**; 容器上 `git config` 如何被设置 (10cglocal) 与 Aether 账号/凭据治理不在本 Spec 范围, 规范文本里以交叉引用标出边界, 不越界。

## Impact

| Type | Description |
|------|-------------|
| **Positive** | collision 信号第一次同时满足: 真两人撞车 = 🔴 (不再降级)、同人多机 = 🟡 (不再漏报)、同容器多 owner = ⚪ 显式告警 (不再静默); Layer H (`owner-container`) 与 Layer L (claim `container`) 的 container 口径统一为 uuid; label 陷阱 (#135 08-13 形态) 结构性消除 |
| **Risk** | (1) 判定键变化会改变现有看板输出 (实验表 A→C), 修后首次扫描会「突然」出现 🔴 —— 缓解: SC 用真实数据冻结快照跑前后对照, handoff 写明差异来源 (stale active 行, 归 #182), 不为让看板好看而改数据。(2) `identity.py` 与 a1-entry 相邻 —— 见下。(3) standards 是共享子模块, §2.3 措辞变更影响所有采用方 —— 缓解: additive (新增第三行 + §2.3.7), 既有两行只改判据措辞不改字段 |
| **与 a1-entry 的边界** | a1-entry 在 `lib/identity.py` **新增**「直取 uuid」accessor (其 Impact 表), 且在 `lib/collision.py::linked_issue_overlaps` 加 `include_terminal` 形参; 本 Spec 改 `get_container_id()` 语义 + `split_owner_container` / `classify_claims`。**同文件不同函数, 语义相容** (a1-entry 的 accessor 在本 Spec 落地后等价于 `get_container_id()`, 可保留或由其 D 期收敛)。**排序规则**: 谁后进 master 谁 rebase; 本 Spec B.1 起手前 `git fetch` 并读 a1-entry 分支实况, 若其 accessor 已落, 本 Spec 复用而不再造第二个 |
| **Rule #6** | 本 Spec 不改任何 SKILL.md 指令面 / description; 变更全在 `lib/` + collector/renderer 代码 + standards 规范文本 ⇒ 按 `skill-benchmark-exemption.md` 第一行「描述性 / 机械」档: substitute = SC 级 baseline-failing 结构化测试 (见 SC-1..SC-6, 每条对当前代码必须先红)。`rule6_note` 随 B.2 写入 |

## Tasks

- [ ] T1 `split_owner_container` 两段式语义 + 零段/三段兼容; 现有 `test_split_owner_container_variants` 的 2-part 断言按新契约改写 (它当前锁的是错误行为)
- [ ] T2 `classify_claims` container 主键 + `identity_advisories[]` 副产物; `classify()` 透传; snapshot schema additive bump 记录到 `state-snapshot-schema.md`
- [ ] T3 `get_container_id()` 恒 uuid + `get_container_label()`; container-id 文件头注释改写 (label 只作展示)
- [ ] T4 `track_board.py` 渲染 ⚪ 行 + label 并列显示; `handoff_multibranch.py` dedupe 行为随 split 变化的锁定测试
- [ ] T5 `standards/conventions/session-handoff.md` §2.3.1 / §2.3.5 / 新 §2.3.7 (按 D-1/D-2 裁定回填)
- [ ] T6 真实数据前后对照: 对冻结的 snapshot 跑 A→C, 差异写入 B.2 handoff; stale active 撞车项抄送 #182
- [ ] T7 回帖 #193 / aria-plugin#135 (缺口 3 部分) 指向本 Spec; ship 后关 #193, #135 留缺口 1/2

## Success Criteria

- [ ] SC-1 (T1) `split_owner_container("simonfish/bfe8285d") == ("simonfish", "bfe8285d", "")`; 三段式仍 `("a","b","c")`; 零段 `("", "dev-claude", "")`。**对当前代码先红** (现返回 `("", "simonfish", "bfe8285d")`)
- [ ] SC-2 (T2) 用 triage case-2/3/4 三组 2-part 输入调用 `classify()`: 同容器双 owner → `none` + 1 条 `identity_advisories`; 两人两机 → `cross_owner`; 同人两机 → `self_multi_container`。**三条对当前代码先红** (现分别为 🟡 / 🟡 / none)
- [ ] SC-3 (T3) container-id 文件含非空 `label` 时 `get_container_id()` 仍返回 uuid, `get_container_label()` 返回 label; 反事实: 复现 #135 08-13 时间线 (acquire 后加 label 再 release) 不再 `claim_not_found`。**对当前代码先红**
- [ ] SC-4 (T4) 同 track 同容器同 owner 的两行 handoff (不同 session/日期) 经 dedupe 折叠为 1; 同容器不同 owner 两行折叠为 1 且产出 advisory; board 标签回显原串; **现 dedupe 把两段串按 `('', owner)` 分组, 对「同容器不同 owner」不折叠 → 先红**
- [ ] SC-5 (T5) `session-handoff.md` §2.3.5 表三行 + §2.3.7 存在且与 D-1/D-2 裁定文本一致; `linked-issue-field-availability` 与 `claude-md-changelog-free` 等既有 check 全绿 (规范变更不引入新 check, 复用 phase-d D.2 gate)
- [ ] SC-6 (T6) 对冻结快照 (本 Spec 起草日 `.aria/state-snapshot.json` 的 tracks[]) 前后对照表落在 handoff; 修后 `collision.kind` 的每一组都能归因到「真撞车 / 同人多机 / stale active (#182)」三类之一, 无「不可解释」组
- [ ] SC-7 全套 state-scanner 测试 (pytest) 与 session-closer/phase-d-closer 的 handoff 写入测试零回归; 主仓 14 state-check 全绿

## 非目标

- 不改 Layer L claim schema / reconcile 仲裁规则 (earliest claimed_at 胜) —— 那是 `multi-terminal-coordination` 的契约。
- 不处理 aria-plugin #135 缺口 1 (snapshot 不解析 claim) / 缺口 2 (闸门只覆盖 Phase B, 由 a1-entry 处置)。
- 不处理 #182 (status 从不收口), 只把实测暴露的 stale active 组抄送过去。
- 不规定 Aether 账号 / 凭据, 不规定容器 `git config` 的供给方式 (10cglocal)。
- 不 rewrite 历史 handoff frontmatter。

## References

- Triage: `.aria/triage-report.json` (2026-09-05, partial-repro) · #193 comment 21431
- 规范: `standards/conventions/session-handoff.md §2.3.1 / §2.3.5 / §2.3.6`
- 代码: `aria/skills/state-scanner/lib/collision.py` (`split_owner_container` :63, `track_to_claim_record` :86, `classify_claims` :143, `classify` :300) · `lib/identity.py` (`get_container_id` :191) · `scripts/collectors/handoff_multibranch.py:518` · `scripts/renderers/track_board.py:412`
- 决策记录: DEC-20260704-002 (病根 #3 机械填) · Kairos `docs/decisions/DEC-2026-09-04-git-identity-scope.md` (权利边界裁定, 本地 checkout 已核)
- 相邻 Spec: `a1-entry-claim-duplicate-work-guard` §2.1 (container_uuid 段) / §3 (口径待定 follow-up)
