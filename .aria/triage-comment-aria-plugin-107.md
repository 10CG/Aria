本评论是按 owner 2026-09-30 决策单第 6 项 (10CG/Aria 仓的 `.aria/decisions/2026-09-30-urgent-issue-plan-owner-rulings.md`, issue 卫生清扫) 做的 triage 核验。该项把 10CG/Aria#180 与本单记为重复, 并要求先核验再评论 / 关闭; 核验结论: 两单同根因 (心跳不刷, `heartbeat_at` 停摆, 30 分钟的 `STALE_TTL` 判 stale, 同名 advisory 通道静默), 但不是重复。10CG/Aria#180 是症状级总单 (对方心跳停摆超过 30 分钟后, 同名通道的 advisory 碰撞面静默, 以及修法 (a) / (c)), 本单是其修法 (b) 中心跳接线的那一部分。**两单都保持 open, 互相引用** (10CG/Aria#180 下已有 2026-09-30 发出的对应 triage 评论); 本评论不代为关闭任何一单。本单的 to-do 全部做完, 也不等于 10CG/Aria#180 的症状已解 (见 Verdict Rationale)。

## Triage Report

**Verdict**: `partial-repro` | **Severity**: `major` | **Recommended Action**: `next-cycle`

> 保持 open, 不关闭 (Recommended Action 表示排期, 不表示关闭)。关联 issue: 10CG/Aria#180 (症状级总单) / 10CG/aria-plugin#202 (承接 to-do 1) / 10CG/aria-plugin#168 (审计轮内不刷心跳)。

---

### Version

| Field | Value |
|-------|-------|
| Reported | `1.56.0` (正文: 「v1.56.0 pre-merge review C1」) |
| Current | `1.74.1` (10CG/aria-plugin 仓 master `268da8f`; origin / github 两端 master 均为该 SHA, `git ls-remote` 实测) |
| Gap | behind — minor 号 1.56 → 1.74, 落后 18 个 minor 版本 |

正文写于 v1.56.0 时代 (issue 创建于 2026-07-11, forgejo API 实查; 2026-09-27 评论里的「本单写于 08-08」与创建时间不符, 08-08 是 10CG/aria-plugin#133 在时间线上引用本单的日期)。此后 v1.71.0 已为心跳接上生产路径, 正文的核心前提因此部分失效 (见 Reproduction 与 Verdict Rationale)。

### Code Path

路径约定: 无目录前缀的 `lib/` / `scripts/` / `references/` / `tests/` / `SKILL.md` 均指 10CG/aria-plugin 仓 `skills/state-scanner/` 目录内的相对路径 (在 10CG/Aria 主仓里对应 `aria/skills/state-scanner/`); 其他 skill 的路径写全 (如 `skills/phase-b-developer/SKILL.md`, 相对 10CG/aria-plugin 仓根); 以 `openspec/` / `docs/` / `.aria/` 开头的属 10CG/Aria 主仓。

collector 对 `lib/constants.py` 报 `file not found` —— 它按主仓根解析, 而该文件实际在 `skills/state-scanner/lib/constants.py` (monorepo 布局假设的缺口, 同一类问题另见 10CG/Aria#200, 那张在版本发现一侧); 已手工对照 v1.74.1, 正文点名的位置现状:

- `lib/claim_lifecycle.py::heartbeat()` → `:179`, 仍无生产调用点 (非测试代码里只剩定义 / 注释 / docstring 与 `lib/__init__.py:20` 的再导出); 但同文件的 `heartbeat_by_track()` (`:475`) 已被 `scripts/phase1_gate.py:1160` 调用。
- `lib/constants.py` 的 `SWEEP_TTL` → `:58` = 86400 (24h); `:38-57` 的注释已改写为「历史注记 + 仍不收回」。
- self-resume → `scripts/phase1_gate.py:303-318` (`_self_resume` 仍按 `(container, session)` 匹配) 与 `:567-582` (该分支仍不刷心跳; `:571-572` 的 logger 文案与 `:577-581` 的注释都已过时)。
- 锁定测试: 正文写 `test_sweep_default_ttl_spares_live_sessions`, 现名 `test_sweep_default_ttl_spares_live_long_sessions` (`tests/test_release_by_track.py:398`), 仍断言 `SWEEP_TTL >= 86400`。

### Git History

collector 的 `likely_fix_candidates` 为空 (Step 4 因路径未解析而 skipped)。手工 `git log -S` 找到心跳生产路径的三个提交, 均在 10CG/aria-plugin 仓的 master 上, 随 `v1.71.0` (`985e629`, 2026-09-06) 发布 (`git ls-remote` 两端 master 均为 `268da8f`, tag `v1.71.0` 两端都在; `git merge-base --is-ancestor` 对三个提交相对 `268da8f` 与 `985e629` 均成立):

| SHA | 日期 | 内容 |
|-----|------|------|
| `0ae207f` | 2026-09-05 | `heartbeat_by_track()`: 按 (container, 归一 track_id) 刷全部 active claim, 与 session 无关 |
| `9c00aa5` | 2026-09-05 | `phase1_gate.py --heartbeat-only` 模式 |
| `ab3dbd0` | 2026-09-05 | state-scanner `SKILL.md`「Layer L A.1 heartbeat 集成」段 (每次 `/state-scanner` 入口触发) |

来源: 10CG/Aria 主仓的归档 Spec `openspec/archive/2026-09-06-a1-entry-claim-duplicate-work-guard/` (立项 issue 10CG/Aria#174)。

### In-flight

| Category | Matches |
|----------|---------|
| Remote PRs | none (10CG/aria-plugin 与 10CG/Aria 两仓开放 PR 均为 0, forgejo API 实查) |
| Local branches | none (没有以本单为目标的分支; 名称相关的只有已合入 master 的 `feature/a1-entry-claim-duplicate-work-guard`, 即 v1.71.0 的 Spec 分支, 不算在制) |
| Worktrees | 仅主工作树 |

10CG/Aria 仓的 `openspec/changes/` 下没有以本单为锚的在制 Spec。相邻的 open issue: 承接本单一部分的有 10CG/aria-plugin#202 (to-do 1) 与 10CG/aria-plugin#168 (审计轮内不刷); 同主题但不同题的有 10CG/aria-plugin#163 (文案把 `SWEEP_TTL` 写成 `STALE_TTL`) 与 10CG/aria-plugin#169 (`resilient_push` 的 non-FF 恢复路径失败, 心跳刷了推不上去, 2026-09-27 评论已提); 症状级总单是 10CG/Aria#180。

### Reproduction

**Mode**: `auto` | **Hit rate**: `6/7` (复现 = 缺陷/缺口仍在; case-8 为旁证, 结论未定, 不计入分母)

实验目录 = 10CG/aria-plugin 仓 `268da8f` 的副本 + 临时 git 仓 + 本地 bare origin + 独立 HOME, 未触碰真仓; 独立复核对 case-2 至 case-7 另行复现, 结论一致。相关既有测试在副本里复跑全绿: `test_heartbeat_by_track` 12 · `test_heartbeat_only_cli` 7 · `test_release_by_track` 53 · `test_phase1_gate_advisory` 13 · `test_reconcile_golden_table` 58 · `test_coordination_default_lockin` 26 (终稿前在 10CG/Aria 主仓的 `aria/` 目录下不写 bytecode / 缓存地复跑, 计数一致, `git status` 保持干净)。终稿前又直接调用 `reconcile()` 与 `linked_issue_overlaps()` 两个纯函数 (内存构造 claim, 不落盘) 复核了两个边界: 心跳年龄 30 分钟仍有 winner, 31 分钟起 winner 为空 (`sole_active+stale_takeover_eligible`); `linked_issue_overlaps()` 仅当双方都带同一 `linked_issue` 且 track-id 不同才命中 (双方都带 → 1 条, 对方未带 → 0 条, 本方未带 → 0 条, 同 track-id → 0 条)。

- case-1 (未复现): 正文前提「零生产调用点 / `heartbeat_at` 冻结」—— v1.65.5 (`af87cae`) 上属实, `268da8f` 已有 `scripts/phase1_gate.py:1160` 的 `heartbeat_by_track` 调用; 真 CLI `--heartbeat-only` 把 120 分钟旧的 claim 刷到 0 分钟 (`outcome=refreshed`, claim 数不变)。`heartbeat()` 本身仍零调用。
- case-2 (复现): to-do 1 —— 同容器**新 session** 跑完整 `phase1_gate`: `advisory_proceed` + `occupied` (把自己容器的旧 session 当竞争者), **新增第二条 active claim**, 旧 claim 心跳仍 5.0 分钟未刷。即 10CG/aria-plugin#202 所述缺陷。
- case-3 (复现): to-do 1 —— **同 session** self-resume (20 分钟旧 claim): `passed`, 心跳前后 20.0 → 20.0, 未刷新。
- case-4 (复现): to-do 2 —— `skills/phase-a-planner/SKILL.md` / `skills/phase-b-developer/SKILL.md` / `skills/phase-c-integrator/SKILL.md` / `skills/audit-engine/SKILL.md` 零 heartbeat 字样; `skills/phase-d-closer/SKILL.md:56` 只在讲 `--sweep-stale` (另见 10CG/aria-plugin#163); `--heartbeat-only` 只规定在 `/state-scanner` 入口 (`SKILL.md:180-192`); `references/layer-l-integration.md:35` 仍写「heartbeat 周期设置 (10min, 由 phase-b-developer mid-cycle 调用)」, 与实现不符 (同文件 `:46` 已改写为「每次调用 (非定时器)」)。
- case-5 (复现): to-do 3 —— `SWEEP_TTL=86400` 未动; `lib/constants.py:43-57` 明写「The threshold below is NOT relaxed on that account … Revisit if the heartbeat ever becomes unconditional (a timer rather than an entry hook)」; 锁定测试仍在 (该模块 53 tests OK)。
- case-6 (复现): 背景后果 —— 对方闲置 1 / 10 / 29 分钟 → `occupied`; 31 / 120 / 1439 / 1500 分钟 → `passed`, `competing_winner=null`, `surface=null` (真 CLI 35 分钟档同); 分界恰在 `STALE_TTL=1800s`。
- case-7 (复现): 2026-09-27 评论的残余缺口 —— `SKILL.md:182` 触发条件原文仍是「本会话**持 active claim**」(措辞自 `ab3dbd0` 起未改); 代码层 `heartbeat_by_track` 换 session 照刷且不新建 claim (实测, claim 数仍为 1), 缺口在 `SKILL.md` 的触发条件文本。
- case-8 (未定, 旁证): 只读本机协调 ref 的本地视图 (2026-09-30T19:37Z): active 2 条, 心跳年龄 1.7h / 12.7h, 无一在 30 分钟内 (与「30 分钟窗形同虚设」同向), 但也无一超过 24h; 评论里「四次 >24h」是历史观测, 今天的数据复现不出也无法复核。本地 ref (`bf05ee9`) 与 origin (`9805ebe`) / github (`ad0287f`) 的 ref SHA 三端各异, 本地视图未必权威 (github 端 `ad0287f` 是 2026-05-24 的提交, 即 10CG/aria-plugin#195 所述非权威 remote 上的陈旧 ref)。

**Deviation note**: 正文 (写于 v1.56.0 时代) 的核心前提「`heartbeat()` 零生产调用点 / 所有 claim 的 `heartbeat_at` 冻结在 acquire」在 v1.74.1 已部分失效 (case-1)。仍然成立的是:

1. to-do 1 未做: self-resume 仍按 (container, session) 且不刷心跳 (case-2 / case-3)。
2. to-do 2 未做: 只有 `/state-scanner` 入口一个挂载点 (case-4)。
3. to-do 3 被成文推迟: `SWEEP_TTL` 仍 24h (case-5)。
4. 同名 advisory 通道在心跳停摆 30 分钟后静默的后果完整复现 (case-6)。
5. 2026-09-27 评论的残余缺口属实: `SKILL.md:182` 触发条件仍按「会话」写 (case-7)。

所以不是「已修」, 也不是原样复现, 而是缺陷收窄为「心跳覆盖不连续」。

### 子项状态

| 子项 | 状态 | 要点 |
|------|------|------|
| 背景前提: `heartbeat()` 零生产调用点, `heartbeat_at` 冻结在 acquire | 部分修复 (零调用前提已失效; 刷新仍只在 `/state-scanner` 入口、且按「本会话」触发) | `0ae207f` / `9c00aa5` / `ab3dbd0`, v1.71.0; `heartbeat()` 本身仍零调用; 不再进入 `/state-scanner` 的容器不刷新, 按 `SKILL.md:182` 现行文本, 新会话继承的 claim 也不刷新 (case-7) |
| to-do 1: self-resume 真刷新 (同 container 匹配即刷) | 未修 | `_self_resume` 仍按 `(container, session)`; `get_identity()` 每次新 session_id (`lib/identity.py:353`); 由 10CG/aria-plugin#202 承接 |
| to-do 2: phase 转换点 (B→C→D) 调一次心跳 CLI | 未修 | 只有 `/state-scanner` 入口一个挂载点; 审计轮内窗口见 10CG/aria-plugin#168 |
| to-do 3: `SWEEP_TTL` 收回到 3×心跳窗口并更新锁定测试 | 未修 (成文推迟) | 前提是心跳无条件 (如定时器), 尚未满足; 属有条件延后而非遗漏 |
| 背景后果: 30min stale-takeover 对活 session 误报 | 未修 | 仍复现 (case-6); 归档 Spec 记为成文残余风险 |
| 2026-09-27 评论: `SKILL.md` 触发条件改为「本容器持 active claim」 | 未修 | `SKILL.md:182` 原文未改; 评论对 `heartbeat_by_track` docstring 的引文逐字核对属实 (`lib/claim_lifecycle.py:515-516`); 属处方性运行时指令改动, Rule #6 照 SOT 处置 |

### 关联单 10CG/Aria#180 的要点 (供排期参考)

10CG/Aria#180 (2026-08-09, aria-plugin 1.65.5 / 1.63.0) 是同一问题的症状侧报告, 保持 open。以下是本单正文没有、仍由 10CG/Aria#180 跟踪的内容 (详见该单正文与 2026-09-30 的 triage 评论):

1. **症状与复现**: advisory 碰撞面在 claim 建立 30 分钟后静默失效。会话 A 对 track X 认领 → 等待 > 30 分钟 (A 仍在正常工作) → 会话 B 对同一 track 跑 `phase1_gate` (advisory)。预期 `outcome=occupied` / `surface.kind="occupied"`; 实际 `outcome=passed` / `competing_winner=null` / `surface=null`。v1.74.1 上仍复现 (上文 case-6; 真 CLI 与库调用一致)。
2. **真实后果 (2026-08-09, SilkNode)**: 两个会话对同一 spec `customer-data-controls-cache-transparency` 的 T14 / T15 / T16 各做了一遍完整实现 —— 会话 A 有 3 条 active claim 并 link 了 issue, 产出 3 个 PR (5 + 20 + 42 个文件); 会话 B 未跑 B.0 (无 claim), 产出 1 个 PR (74 个文件); 同一个 schema 变更出现两套迁移目录 (T16: `20260808000000_training_annotation_backfill` vs `20260808210000_backfill_trains_on_data`; T15: `20260809000000_account_level_data_controls` vs `20260808211000_account_level_data_controls`), 另有 3 个文件双向冲突。关键点: 即使 B 当初跑了 B.0 也不会收到告警 —— A 最早那条 claim (08-08 03:21) 到 B 开工 (08-09 03:14) 已 stale 24 小时; 事后补跑 `phase1_gate`, 3 条 active claim 在场仍 `surface=null`。
3. **修法 (a)** (把 `reconcile()` 的 takeover 判定改用 `SWEEP_TTL`, 或引入与其同量级的 `COLLISION_TTL`): 未实现。owner 2026-08-23 在 10CG/Aria 主仓的归档 Spec 内裁定 `STALE_TTL` 维持 30min (`openspec/archive/2026-09-06-a1-entry-claim-duplicate-work-guard/proposal.md` 的 `:308` / `:651` / `:687`), 同一 Spec 还把「主检测责任由 overlap 通道承担」写成成文残余风险 (`:340`); 这一裁定的作用域是该归档 Spec, 是否对修法 (a) 永久适用待 owner 裁定 (已在 10CG/Aria#180 下的评论提请 owner 决定)。另需注意它不是「一行常量」: `_is_stale` 同时服务 Rule 5.1 的 fresh-only clock-skew 判定 (`lib/reconcile.py:283`, 见 10CG/aria-plugin#111) 与 Rule 6 (`:255` / `:328`); `track_board` 另直接用 `STALE_TTL` 分黄 / 红 (`scripts/renderers/track_board.py:293-297`); `tests/test_reconcile_golden_table.py` 的 Case 3.x 钉住该语义。
4. **修法 (c)** (对 stale claim 在 collision surface 单独降级提示, 如「该 track 有 N 个已 stale 的 claim, 可能有会话仍在进行」, 而不是完全静默): 未实现 —— 7d 仍「No prompt needed」(`scripts/phase1_gate.py:791-793`), `AdvisorySurface.kind` 只有 `occupied` / `clock_skew` / `push_failed` (`:187-191`)。由 10CG/Aria#180 继续跟踪: 两仓 (open + closed) 全部 issue 全量翻页, 按 COLLISION_TTL / 降级提示 / stale claim 检索标题与正文, 只命中该单。
5. **根因 4** (heartbeat 要求同一 Identity 实例): 已被 `heartbeat_by_track` 绕开 (上文 case-7 同款夹具实测); 对应 acquire 侧的口径不一致见 10CG/aria-plugin#202。
6. **同类事故今天还会不会发生** (本次核对新增): 带 `--linked-issue` 的 A.1 入口认领 (track-id 含 `<container_uuid>` 段) 由不做心跳新鲜度过滤的 `linked_issue_overlap` 通道报出 48 小时前的对方 claim (实测; `lib/collision.py:365-440`) —— 前提是**双方 claim 都带同一 `linked_issue`**; 对方 claim 未带 (该 flag 可选) 时, 即使 B 带了也是 `linked_issue_overlap=[]`, 双通道皆静默。另一条路径: **同一个 track-id** 的两个容器 (Phase B 按 carry-id 认领, 或旧形态) 只走同名通道 —— 对方闲置超过 30 分钟即 `passed` / `surface=null` 且 `linked_issue_overlap=[]` (`lib/collision.py:426-427` 把同名交给 reconcile, 而 reconcile 已判 stale)。这些路径就是 10CG/Aria#180 所述缺陷在今天的残余。

### Verdict Rationale

正文写作时的核心前提 (heartbeat 零生产调用点) 已在 v1.71.0 部分失效, 所以是 `partial-repro` 而非原样复现; 但缺陷本身仍在, 只是收窄为「心跳覆盖不连续」: 刷新只发生在 `/state-scanner` 入口且条件按「会话」写 (`SKILL.md:182`), 没有定时器, 也没有 phase 转换点或审计轮内的挂载点, 因此同名 advisory 通道 (30 分钟) 与 durable sweep (24h) 之间的保护窗仍靠「编排层恰好入口」维持 (case-2 至 case-7)。三条 to-do 中 to-do 1 / 2 未做、to-do 3 被成文推迟; 2026-09-27 评论的残余缺口逐字属实, 且是最小可修项 (代码层 `heartbeat_by_track` 已按容器匹配, 只需改 `SKILL.md` 触发条件文本)。

Severity 取 `major` 而非 `critical`: 这是功能性缺陷 (advisory 协调保护窗失效, 10CG/Aria#180 记载过一起真实的重复劳动), 但 advisory 不是硬闸; 带同一 `linked_issue` 且 track-id 不同的认领另有不做新鲜度过滤的 overlap 通道兜底 (前提见上文要点 6); 另有人工规避 (会话开场手动补刷, 见 2026-09-27 评论)。`next-cycle`: 本单在 owner 决策单第 6 项的 P1 批内, 最小可做项已由 2026-09-27 评论给出。建议保持 open、按 `next-cycle` 排期。

注意: 最小修法和 to-do 1 / 2 都是挂载点, 不是定时器; 做完后, 长阶段内同名通道仍会在最后一次刷新 30 分钟后静默 (复核: 生产 `--heartbeat-only` 刷新后再过 31 分钟即 `passed` / `surface=null`)。因此将来按本单范围关单时, 须在 10CG/Aria#180 留言说明, 不得连带关闭它。

顺带: 同一过时前提 (「no production heartbeat loop exists」) 还出现在 `scripts/phase1_gate.py:571-572` 的 logger 文案与 `lib/gc.py:355-359` 的 docstring; `scripts/phase1_gate.py:577-581` 的过时注释已由 10CG/aria-plugin#202 点名, 其余几处 (含上文 `references/layer-l-integration.md:35`) 按标题与正文检索未见 issue 点名。

---

*Generated by `/issue-triage` v1.74.1 — Ref: 10CG/aria-plugin#107*
