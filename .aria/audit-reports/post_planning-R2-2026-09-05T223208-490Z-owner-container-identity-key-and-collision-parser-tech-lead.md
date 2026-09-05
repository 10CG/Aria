---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-05T22:32:08.490Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R2 — tech-lead 席 (验证 v2 结构改法是否真解掉 C-1 / C-2)

审计对象: `tasks.md` (组 0-5, 38 checkbox + 「S2 后续」表) + `detailed-tasks.yaml` (38 TASK + `metadata.s2_followup`) @ commit `03c6a9e`, 依据 `proposal.md` v8。

机械底账 (脚本实跑 `/tmp/claude-1000/-home-dev-Aria/660cdd00-d2ad-4227-a5bb-5312810322f1/scratchpad/dag2.py`):
38 任务 / id 唯一 / 依赖全部可解析 / 无环 (topo len = 38) / 总工时 82.5h / 最大 6h 最小 0.5h / agent 实计 `backend-architect 15 · qa-engineer 15 · knowledge-manager 8` 与 `metadata.agents` 一致 / tasks.md checkbox 实测 38 与 `metadata.total_tasks: 38` 一致 (「S2 后续」表是 `|` 表格行, 不被 `_CHECKBOX_RE` 捕获) / 预留 id `TASK-027..030` 与 parent `6.1-6.4` 在现 tasks[] 中零占用 ⇒ 「追加不改既有编号」约束成立 / 三文件零带圈数字零希腊字母。

---

## R1 处置核对

| R1 finding | v2 三态 | 依据 (实读 / 实跑) |
|---|---|---|
| **C-1** `deferred-s2` 归档机制不存在 | **closed** | 沙箱把 v2 tasks.md 全部 38 个 `[ ]` 改 `[x]` 后实跑 `is_spec_complete` = `{'complete': True, 'reason': "tasks.md 全 [x] (38 task(s), 无 carry-forward/defer 注释)"}`。对未改的真文件跑 `_extract_carry_forward_annotations` 得 `[]` (tasks.md 与 yaml 皆无残留标注)。补跑 `gate_result` 侧的 C-block 面: 6 条含集成关键词的 checkbox 行抽出的符号 liveness 实测**无一 `dead`** (`aaaa1111` / `identity_advisories` / `cross_owner` 为 `ambiguous`, 其余 `alive`) ⇒ verdict 最坏 `warn`, 按 `openspec-archive/SKILL.md:140-156` 路由表 `complete=true ∧ verdict=warn` 不 BLOCK。S1 归档路径打通 |
| **C-2** TASK-033 全绿不可达 | **closed** | `proposal.md:132` SC-7 已改为「主仓 state-check **13 条全绿 + `plugin-cache-currency` 例外**」, 与 `tasks.md:79` / yaml TASK-033 verification 同文。算术核对: `.aria/state-checks.yaml` 实读 `checks` 长度 = 14 且 14 条全 `enabled` ⇒ 13 + 1 例外 = 全集。该 check `severity: warning` (非 error)。先例成文: `docs/handoff/2026-09-03-sibling-spec-probe-b2-complete-…md:11` 「state checks 13/14 (唯一 fail = plugin-cache-currency, owner 刷缓存)」, `docs/handoff/2026-08-30-…md:56` 把它列为 H7 owner action 行 ⇒ 属 Rule #10 白名单「已成文 lane 降级」而非 AI 临场豁免 |
| **M-1** 合并闸前置漏 6 个交付/留痕任务 | **closed** | TASK-034 传递闭包实算 30 项, 覆盖组 1 全部 (001-011) / 组 2 全部 (012-020) / 组 3 全部 (021-026) / 4.1 (031) / 4.2 (032) / 5.2 (035) / 5.4 (037)。R1 点名的 016 / 022 / 025 / 031 / 037 全部进闭包。唯一不在闭包的组 4 项是 TASK-033 (4.3), 按设计须排在 TASK-041 之后 ⇒ 不是缺口 |
| **M-2** S2 在 DAG 上是死支 | **partial** | 027-030 已移出 tasks[] (进 `metadata.s2_followup`), 主 DAG 不再有零反向依赖的 S2 叶子 (实算叶子仅 `TASK-040` / `TASK-038` 两个外向项)。但「未激活时的兜底承载」是不存在的机制 → 本轮 **M-1** |
| **M-3** S2 判定时点自相矛盾 | **closed** | `ship_shape` 值域改为 `{S1, S2-candidate}` (yaml:80), ack 从 0.1 的判据里剥出, 移进激活条件 (yaml:41 / `tasks.md:102`), 重评点即「merge 前任一时刻」⇒ 首轮不可达的矛盾消解。激活窗口本身无机械承载另计 → 本轮 **M-2** |
| **M-4** tag 落在未 bump 的 commit 上 | **closed** | 依赖倒过来了: yaml:544 `TASK-034 dependencies: [TASK-035, TASK-037]`, 拓扑实跑序 `035(5.2) → 037(5.4) → 034(5.1) → 036(5.3)`; yaml:549 verification 明写「tag 落在 plugin.json 已 bump 的 commit 上」; yaml:562 TASK-036 verification 已补「`ls-remote refs/tags/v<NEXT>` **对象 SHA** == 本地」逐 remote 核验 |
| **M-5** TASK-011 无转绿归属 / 断言基线即绿 | **partial** | 计划侧已修: `tasks.md:52` 标注「**baseline-green, 非 RED**」, 组 1 抬头 (`tasks.md:40`) 由全称改为「「先红」项」, yaml:259-260 verification 写「基线即绿, 作回归锁, 不计入 RED」+ notes 把 rule 1.54 触发面转给 TASK-024。但 proposal SC-9 的对应子句未同步 → 本轮 **M-3** |
| **m-1** container-id 注释「label 仅展示」与 S1 事实反向 | **partial** | `tasks.md:62` 已删掉「(label 仅展示)」这个措辞, 危险文案不再被计划点名。但 yaml:359-360 TASK-018 verification 仍只锁「accessor 子句转绿 / S1 lock-in 仍绿」, 对注释该写什么零断言 → 本轮 **m-1** |
| **m-2** 关 issue 无归属 | **closed** | TASK-038 已收进本 cycle: yaml:619 `dependencies: [TASK-039]`, title 写「merge 后、归档前, 执笔容器执行」, yaml:624 verification 含「#193 关闭」;`tasks.md:19` 边界表把 Phase D 的 owner 插件更新单列, 不再把关 issue 推给 phase-d-closer |

三态计数: **closed 6 · partial 3 · open 0**。

---

## 审计结论

### M-1 (major · issue · architecture) — S1 兜底「D 期 Step 7 用既有 tracker 机制开 issue 记录 S2 后续」不是既有机制; 干净归档时该 Step 完全不执行

- **scope**: `tasks.md:102` (激活规则末句) · `tasks.md:17` (边界表) · `detailed-tasks.yaml:41` (`metadata.s2_followup.activation`) · `proposal.md:104` · 实现面 `aria/skills/state-scanner/scripts/lib/spec_complete.py:1200-1234` + `aria/skills/openspec-archive/SKILL.md:267-276`
- **summary**: C-1 的改法用「未激活 ⇒ D 期 Step 7 tracker issue」换掉了归档 BLOCK。实读 Step 7 与 `_build_d_payload`: 该 Step 的触发量与载荷都只由「未勾 checkbox + carry-forward 注释」和「unverified_claims」两个集合组成, 「S2 后续」表不是其中任何一个的输入; 干净归档时 payload 为 `None`, Step 7 一行不输出。硬 BLOCK 被换成了静默丢失。
- **evidence**:
  - `spec_complete.py:1200-1213` `_build_d_payload(spec_dir, deferred_items, unverified_claims)` → `if not deferred_items and not unverified_claims: return None`; `:1218-1228` body 只拼「## 未完成/deferred 项」与「## Unverified claims」两段, 无第三个来源。
  - `openspec-archive/SKILL.md:272` 「触发: `gate_result.d_payload … != null`」; `:276` 「干净归档 (无 deferred 且无 unverified) → `d_payload=null` → 本 Step 完全跳过, **不产生任何输出**」。
  - 本 Spec 恰好逃过一劫但不解决问题: 实跑 `classify_symbol_liveness` 得 `aaaa1111` / `identity_advisories` / `cross_owner` 三个符号为 `ambiguous` ⇒ `unverified_claims` 非空 ⇒ 会开出一个 tracker issue —— 但其 body 由上述两段机械拼成, 内容是「符号 `aaaa1111` 引用形态未分类」之类, **一个字不提 S2 后续**。
  - 先例不同型: `#192` (sibling-spec-probe) 是 gate warn 触发的 unverified-claims tracker (`git log` commit `5f5c2e0` 自陈「D.2 gate warn 归档 (tracker #192)」), 不是「把一张计划外的后续表登记成 issue」的先例。
  - 归档确实会把 `tasks.md` 原样搬进 `openspec/archive/`(SKILL.md Step 6), 所以「S2 后续」表不会消失 —— 但归档目录不是待办队列, 没有任何消费方会再看它。
- **建议**: 给 S2 后续一个真正的承载体, 两条都可: (a) 把「S1 收尾时开一个 S2 后续 tracker issue (标题点名 flip / 发布门 / a1-entry SC-3 / #135 时间线四项)」写成 TASK-038 的一条 verification 子句 (它本来就在 merge 后、归档前跑, 且已是 issue 动作的宿主); 或 (b) 单列一条 5.8 任务。无论哪条, 都把 `tasks.md:102` / yaml:41 / `proposal.md:104` 里「用既有 tracker 机制」的措辞改掉 —— 那不是既有机制。

### M-2 (major · issue · architecture) — 激活窗口「merge 尚未执行」在 DAG 上无承载: 0.1 / 0.2 不是 merge 的前置, 拓扑上允许带着 `ship_shape: "TBD-at-0.1"` 合进 master

- **scope**: `detailed-tasks.yaml:17` (`ship_shape: "TBD-at-0.1"`) · `:76` (`TASK-000 dependencies: []`) · `:91` (`TASK-040 dependencies: [TASK-000]`) · `:544` (`TASK-034 dependencies: [TASK-035, TASK-037]`) · `tasks.md:102`
- **summary**: 激活规则的三个条件里有两个 (0.1 判 S2-candidate / #174 ack 已到) 由 TASK-000 与 TASK-040 产出, 第三个是「TASK-034 尚未执行」。但反向依赖实算显示 TASK-000 与 TASK-040 **不在** TASK-034 / 036 / 041 / 033 / 039 的任何一个传递闭包内 —— 整条发布链不以「形态已判定」为前提。
- **evidence**:
  - 闭包实算: `TASK-034` 闭包 30 项, 缺 `TASK-000(0.1)` `TASK-040(0.2)`; `TASK-039` 闭包 34 项, 同样缺这两项 (另缺按设计外向的 `TASK-038`)。零反向依赖叶子实算 = `TASK-040(0.2)` / `TASK-038(5.5)`; **`TASK-000` 虽有 1 个 dependent (TASK-040), 但那条边只回流到组 0 内部, 不通向发布链**。
  - 后果不止「S2 窗口静默关闭」: `TASK-000` 的 deliverable 就是本 yaml 的 `metadata.ship_shape` (yaml:77-78), 现值 `"TBD-at-0.1"` (yaml:17)。DAG 允许 041/039 先跑, 于是 master 上落一份 `ship_shape: "TBD-at-0.1"` 的 A.3 产物 —— 归档门此后才在 D.2 用 checkbox 逼出 0.1, 已经晚了一步。
  - 这与 R1 M-1 是同一类缺陷 (「拓扑上允许未做完就 ship」), R1 的修法只补了组 1-4 的边, 组 0 没补。
- **建议**: `TASK-034 dependencies` 补 `TASK-000, TASK-040` (035 也可以, 但 034 是激活规则点名的那道线)。补完后 0.1/0.2 → … → 034 的顺序由 DAG 保证, 「merge 前」这个窗口才有机械含义。

### M-3 (major · issue · documentation) — proposal SC-9 首句仍要求一个「rule 1.54 触发面测试」, 而 v2 计划已实证该测试不可实现且改由文档 token 断言承载; AC 与计划两份不同文

- **scope**: `proposal.md:134` (SC-9) · `tasks.md:52` (1.11) · `detailed-tasks.yaml:259-260` (TASK-011) · `:446` (TASK-024 verification)
- **summary**: R1 M-5 的处置只落在 tasks/yaml 一侧。proposal SC-9 的第一子句「rule 1.54 触发面测试 (`coordination.enabled=false` + `kind=cross_owner` → 命中)」描述的是一个**代码级求值测试**, 而 v2 计划的立论正是「rule 1.54 为散文规则, 无求值引擎」。同一件事在 SOT 里有两个互斥版本, D 期验收时必然要有人临场裁一次。
- **evidence**:
  - 复核 R1 的判断 (不沿用结论): `grep -rn "coordination_churn\|concurrent_churn\|\"1\.54\"\|'1\.54'" --include=*.py aria/` **零命中**; 1.54 只出现在 4 个 .md (`SKILL.md` / `RECOMMENDATION_RULES.md` / `references/layer-l-integration.md` / `references/rules/advanced-rules.md`)。无 rules 求值引擎文件。
  - `detailed-tasks.yaml:260` notes: 「rule 1.54 为散文规则 (全仓 py 零命中), 触发面由 TASK-024 文档 token 断言承载」; `tasks.md:52` 同义。
  - `proposal.md:134` 该子句在 v7→v8 的 diff 中**未被触碰** (`git diff HEAD~1 HEAD -- …/proposal.md` 只改了 Status / :43 决策单路径 / :104 / :119 T12 / :132 SC-7 五处)。
  - 缓解因素 (故为 major 而非 critical): SC-9 不在 Rule #6 substitute 的五条 (SC-1/2/3/4/8) 之内, 不承载发版闸。
- **建议**: `proposal.md:134` 首句改为「rule 1.54 触发面 = 文档 token 断言 (`RECOMMENDATION_RULES.md:31` 行含 `identity_advisories`), 该规则为散文规则无求值引擎, 不设代码级命中测试」, 与 TASK-011/TASK-024 同文。

### M-4 (major · issue · implementation) — 5.5 回帖文案「#135 留缺口 1/2」在 S1 形态下是超报: proposal 自陈缺口 3 的 label 陷阱「结构性消除只在 S2 形态成立」

- **scope**: `tasks.md:87` (5.5) · `detailed-tasks.yaml:612-624` (TASK-038) · `proposal.md:101` · `proposal.md:19`
- **summary**: TASK-038 的 verification 无条件断言「#193 关闭; #135 留缺口 1/2」, 即向外宣告缺口 3 已闭。但 S1 不 flip `get_container_id()`, 按 proposal 自己的话, 缺口 3 的 label 陷阱在 S1 下仍然在线 —— 这条回帖会让采用方以为陷阱没了。
- **evidence**:
  - `proposal.md:19` 定义缺口 3 = 「container 段来源不稳 … `get_container_id()` 是 `label if label else uuid`, 文件头注释又邀请填 label ⇒ 填个可读名就静默换了协调身份」。
  - `proposal.md:101`: 「**label 陷阱结构性消除只在 S2 形态成立**; S1 形态下 label 形态既无 flip 也无 ⚪ (⚪ 只对 uuid key), 只有 T3b 的 inventory 告警」。
  - `detailed-tasks.yaml:623-624` verification: 「文案含: 三层根因 / 裁定 / 版本 / 采用方影响; **#193 关闭; #135 留缺口 1/2**; comment id 回填草案」—— 无 S1/S2 分档。`tasks.md:87` 同文。
  - 这是外向且难回收的动作 (关 issue + 公开留言), 与 M-1 同根 (S1 残留无承载) 但修法不同。
- **建议**: TASK-038 verification 拆成两档 —— S2 已激活: 维持现文案; S1: 文案须写明「缺口 3 的解析/分组/告警面已闭, `get_container_id()` label 优先仍在 (见 S2 后续 tracker #<n>)」, 且 `#135` 的缺口 3 **不标完成**。是否关 #193 也随之复核 (#193 本身是解析器 bug, 与 S1/S2 无关, 可关)。

### m-1 (minor · risk · documentation) — R1 m-1 只做了一半: 危险措辞已从计划里删掉, 但 TASK-018 对注释该写什么仍零断言

- **scope**: `tasks.md:62` (2.7) · `detailed-tasks.yaml:349-360` (TASK-018)
- **summary**: v2 把 2.7 的「(label 仅展示)」删了, 反向断言的风险降了; 但 `container-id 文件头注释 (:126-140) 改写` 改成什么没有任何验收条件, 而这个注释正是 #135 缺口 3 的诱因本体。
- **evidence**: `tasks.md:62` 现文「`lib/identity.py` 新增 `get_container_label()`; container-id 文件头注释 (`:126-140`) 改写 — 1.8 accessor 子句转绿 (S1 不动 `get_container_id()`)」; yaml:359-360 verification 两条只讲 accessor 与 lock-in。
- **建议**: TASK-018 verification 加一条 S1 措辞锁: 注释须写明「label 当前**仍参与**协调身份, 将在后续版本改为仅展示」, 并反向 grep 锁「仅展示」不得单独出现。

### m-2 (minor · issue · documentation) — proposal T10 仍写「主仓 14 state-check」, 未随 SC-7 的「13 条 + 例外」同步

- **scope**: `proposal.md:119` (T10) vs `proposal.md:132` (SC-7)
- **evidence**: `:119` 「… + 主仓 **14** state-check → SC-7」;`:132` 「主仓 state-check **13 条全绿 + `plugin-cache-currency` 例外**」。v7→v8 diff 只改了 `:132`。两句不是数学矛盾 (14 条跑, 13 绿 + 1 例外), 但 T10 的裸「14 state-check」读起来就是「14 全绿」, 正是 C-2 想根除的读法。
- **建议**: `:119` 改「主仓 state-check (13 + `plugin-cache-currency` 例外, 见 SC-7)」。

### m-3 (minor · issue · documentation) — v2 在 proposal:104 插入的新句切断了原句, 「改写其 SC-3」的目标文本成了悬空短语

- **scope**: `proposal.md:104`
- **evidence**: v7 原文为「… flip + 发布门 + 由本 Spec 改写其 SC-3 **为**「`get_container_uuid()` 与 flip 后 `get_container_id()` 同值; label 只在 `get_container_label()`」」。v8 在「改写其 SC-3」与「为「…」」之间插入了「。**S2 项不进 tasks.md checkbox** … (先例 #192), SC-3 的 S2 臂不进本 cycle 验收 」, 于是现文成了「… SC-3 的 S2 臂不进本 cycle 验收 为「`get_container_uuid()` 与 flip 后 …」」—— 主谓失配。而这段被切断的引号文本, 恰恰是 S2 激活时要拿去改写 a1-entry SC-3 的原文 (TASK-040 的留言草案也要引它)。
- **建议**: 把引号文本还给「改写其 SC-3 为」, 新插入句另起一句。

### m-4 (minor · risk · architecture) — SC-7 的 `plugin-cache-currency` 例外是 owner Approved 之后由 AI 写入的, Status 行仍是原 Approved 戳; 按 Rule #10 应在 handoff 点名请复议

- **scope**: `proposal.md:4` (Status) · `proposal.md:132` (SC-7) · `detailed-tasks.yaml:515` (TASK-033 verification)
- **summary**: 例外本身站得住 (severity=warning + 两次 ship 的成文先例, 属白名单「已成文 lane 降级」), 判定不改。但改动的对象是一条 **enabled 闸的期望态**, 且发生在 owner 的 Approved 戳之后 —— Rule #10 末句要求「AI 任何自作主张的流程判断必须写进 handoff 请复议」。现在 TASK-033 只要求 handoff 记录 **owner 的动作**, 没要求记录「这条例外是本轮 AI 引入的」。
- **evidence**: `proposal.md:4` Status 仍为「**Approved (owner 2026-09-05)** — v8 = post_planning R1 后同步 (… / SC-7 plugin-cache-currency 例外 / …)」, 即 v8 自陈包含该例外却沿用旧 Approved;`detailed-tasks.yaml:515` verification 只写「handoff 记录 owner D 期动作」。
- **建议**: TASK-033 verification 追加一句「handoff 同时记录: `plugin-cache-currency` 例外为 post_planning R1 rework 引入, 请 owner 在 D 期复议」。零成本, 且把 Rule #10 的留痕做实。

---

## Verdict

PASS_WITH_WARNINGS (Critical 0 / Major 4 / Minor 4)。

两个 Critical 都实证解掉了, 且是用结构改法而不是措辞回避: C-1 经沙箱实跑确认 38 个 checkbox 全勾即 `complete=True`, 并补验了 `gate_result` 的 C-block 面无 `dead` 符号 (最坏 warn, 不 BLOCK); C-2 经 `.aria/state-checks.yaml` 实读 (14 条全 enabled) + severity=warning + 两份 handoff 先例确认「13 + 例外」既算术正确又落在 Rule #10 白名单内。发布顺序按拓扑实跑逐段核对与 `tasks.md:81` 宣称完全一致 (`035 bump → 034 merge+tag → 036 push → 041 主仓同步面 → 033 → 039 PR → 038 回帖`), TASK-034 的反向依赖已覆盖组 1-3 全部与 4.1/4.2, R1 点名的六个孤立任务全部进闭包。

剩下的 4 个 Major 分两类。一类是**改法自身留下的新面** (M-1 / M-2): 把组 6 移出 checkbox 消掉了硬 BLOCK, 但接住它的兜底 (Step 7 tracker) 经实读证明收不到「S2 后续」这类输入, 且激活窗口的三个条件里两个的产出任务不在发布链的传递闭包内 —— 换句话说, C-1 从「必撞墙」变成了「可能静默丢」, 还没变成「有人接」。这与 R1 M-1 是同一类拓扑缺陷, 只是从组 1-4 挪到了组 0。另一类是 **rework 的下游漂移** (M-3 / M-4): SC-9 与 5.5 回帖文案没跟上 v2 的新事实, 一个要求了实证不存在的测试, 一个会对外宣告一个 S1 下并未闭合的缺口。四条的修法都是定点编辑 (三条加依赖/加 verification 子句, 一条改 proposal 措辞), 不动 DAG 骨架, 不改编号。

---

## Vote

REVISE

## 轮次记录

| 轮次 | 席位 | 结论 | 备注 |
|------|------|------|------|
| R1 | tech-lead | FAIL (2C / 5M / 2m) | 首轮; 归档门 `deferred-s2` 机制不存在 + `plugin-cache-currency` 不可绿 两个 Critical |
| R2 | tech-lead | PASS_WITH_WARNINGS (0C / 4M / 4m) | 本轮镜头 = 验证 v2 结构改法是否真解掉 C-1/C-2 且无新死支。R1 三态: closed 6 (C-1 / C-2 / M-1 / M-3 / M-4 / m-2) · partial 3 (M-2 / M-5 / m-1) · open 0。新增 4 Major 全部来自 v2 引入的新结构面或其下游未同步项, 无一是 R1 结论的重复。全部 finding 附实读 file:line 或脚本实跑输出; 归档门与 d_payload 结论经 scratchpad 沙箱复现 (未触碰仓内文件)。Critical 归零 ⇒ 收敛面显著收窄, 但严格判据集合 R2 ≠ R1, converged=null 交编排层判 |

**B 期顺手项 (不构成 finding, 执行时带上即可)**:
- TASK-033 的 verification 引用了「handoff 记录 owner D 期动作」, 而 handoff 由 Phase D 的 phase-d-closer 产出 (`tasks.md:19` 边界表已明确委托) —— 该条在 TASK-033 自身执行时点不可自验, 执行时按「记入待写 handoff 的 owner action 清单」处理即可。
- 若 S2 激活, `metadata.total_tasks: 38` (yaml:59) 与 `metadata.agents` 三个计数需同步改为 42 / 按新任务的 agent 归属重算 —— 激活规则 (yaml:41) 只写了「追加 checkbox + TASK-027..030」, 没提这两个计数字段。
- `classify_symbol_liveness` 对 `tasks.md:46` (1.5 行) 里的 `` `aaaa1111` `` 会当成一个待验符号 (实测 ambiguous, 仅命中 audit-reports 类 prose 文件)。B 期若把该夹具常量写进测试文件, 它仍只有 test 侧引用 ⇒ D.2 gate 会稳定给一条 unverified_claim (warn, 不 block)。想让 D.2 更干净, 可把 1.5 行里的 `` `aaaa1111` `` 改成非 backtick 写法 (如 8 位 hex 容器 id `aaaa1111`)。
