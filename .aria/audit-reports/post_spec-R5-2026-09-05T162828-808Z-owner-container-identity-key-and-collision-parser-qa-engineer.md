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
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## R4 处置核对

方法: 对我 R4 报告 (`.aria/audit-reports/post_spec-R4-2026-09-05T155052-857Z-owner-container-identity-key-and-collision-parser-qa-engineer.md`) 的 1 Major + 2 minor 逐条核对 v5 proposal.md 文本, 并对 Major 项做真实源码实跑复现验证 (方法见「审计结论」R5 一节)。

- **R4-Major (SC-2 advisory 臂「dedupe 前调用」生产接线端到端未锁定, T2 点名改写的两条真实 collector 测试用 `box-A`/`box-B` 非 uuid 夹具, 天生 vacuous)**: **闭合** (细节见下「审计结论」新增 finding, 与本条同根同源, 未视为独立新 Major, 定性为 minor 残留)。v5 proposal.md:123 SC-2 advisory 臂新增子句「**生产接线端到端**: 真实 collector 夹具 (`_build_repo` 风格, uuid 形容器 `aaaa1111` 而非 `box-A`) 两份 handoff 两串 → 经 `collect_handoff_multibranch` 完整采集后 snapshot `collision.identity_advisories` 恰 1 条 (**接线反事实**: `:709` 传 `deduped_tracks` → 0, 红)」。实跑复现 (真实源码 `aria/skills/state-scanner/scripts/collectors/handoff_multibranch.py` / `lib/collision.py` 未改动主仓, 只在 scratchpad `v3repo/`(v4 语义补丁, R3/R4 沿用) 与新建 `v3repo_bad_wiring/`(在 `v3repo/` 基础上把 `:714-716` 的 `_identity_drift_advisories(tracks)` 改为 `_identity_drift_advisories(deduped_tracks)`) 两份完整 state-scanner 目录里跑, 只读不改仓内文件): 用与 SC-2 字面完全一致的 fixture 形状 (uuid 容器 `aaaa1111`, 两分支两份 handoff, `alice`/`bob` 两串, **同 track_id**) 跑真实 `collect_handoff_multibranch()`, 接对 (`v3repo/`) 得 `identity_advisories == [{"identity_key": "aaaa1111", "owners": ["alice","bob"], ...}]` (恰 1 条); 接反 (`v3repo_bad_wiring/`) 得 `identity_advisories == []` (0 条, 红) —— 与 SC-2 声称逐字符合, 该子句**真能分辨接线方向**。同时复核 T2 点名改写的两条既有测试 (`test_real_collector_emits_cross_owner_collision`/`test_real_collector_no_collision_is_none`, `box-A`/`box-B` 夹具) 在接对/接反两份代码上重跑, **两条测试在两个方向下都 PASS** (与 R4 finding 一致, box-A/box-B 非 uuid, `identity_drift_advisories` 内部 `_UUID_RE` 直接跳过, vacuous) —— 证明这两条既有测试对本 Major **不构成**任何防线, 新子句 (uuid 夹具) 是唯一能抓到接反的判据, 且它确实抓到了。**残留精度问题降级为 minor**, 见「审计结论」。
- **R4-minor-1 (SC-11「谓词只有一个实现 (grep 断言无第二份)」按名字 grep 可被同义改名绕过)**: **闭合**。v5 proposal.md:132 SC-11 改写为「谓词只有一个实现 (grep 断言: `updated_at` 与天数比较的表达式在 collector / renderer 各零处, 只在 lib 一处; **同义改名绕过属 B 期 review 责任, 成文**)」—— 与我 R4 建议的处置方式 (承认 grep 判据的边界, 把改名绕过明文划给人工 review 而非声称机械防死) 完全一致, 不再是隐含的过度声称。
- **R4-minor-2 (T6 七字段清单未列出 `phase`, 但 `track_to_claim_record` 确实读取该字段)**: **闭合**。v5 proposal.md:111 T6 改为「只保留 `track_id / owner_container / status / phase / updated_at / filename / branch / legacy` **八字段** (`phase` 被 `track_to_claim_record` 读取)」, 字段清单与代码实际读取字段对齐。

**三态计数**: Critical 0 closed / 0 reopened / 0 not-addressed; Major 1 closed / 0 reopened / 0 not-addressed。

## 审计结论

方法论: (1) 对 v5 SC-2 新增的「生产接线端到端」子句, 用 scratchpad 既有 v4 语义补丁 (`v3repo/`, R3/R4 沿用未改动) + 新建接反补丁 (`v3repo_bad_wiring/`, 仅 `:714-716` 一处调用点改 `tracks`→`deduped_tracks`) 两份完整 state-scanner 目录, 按 SC-2 字面 fixture 形状实跑真实 `collect_handoff_multibranch()`, 双向验证判据分辨力; (2) 额外构造「两份 handoff 用不同 track_id」的变体 (SC-2 文本未显式排除的一种字面合规读法), 双向重跑, 定位残留精度缺口; (3) 对 R4 聚合报告列出的 3 条 Major (M1 本席 / M2+M3 knowledge-manager) 与 12 条 minor 逐条对读 v5 文本, 确认全部落地且未引入恒绿或不可实现表述; (4) 对未改动的 `test_real_collector_emits_cross_owner_collision`/`test_real_collector_no_collision_is_none` 在接对/接反两版代码上各跑一次, 确认其对本 Major 判定力为零 (符合 R4 finding, 无退化)。

### type: issue / severity: minor / category: testing / scope: SC-2「生产接线端到端」子句未显式要求两份 handoff 共享同一 `track_id`, 存在一种字面合规但不discriminating 的 fixture 读法

**summary**: SC-2 v5 新子句写「两份 handoff 两串 → ... 恰 1 条 (接线反事实: `:709` 传 `deduped_tracks` → 0, 红)」, 未点名两份 handoff 是否共享同一 `track_id`。`identity_drift_advisories()` 本身按纯 container `identity_key` 分组、不看 `track_id`; 但生产侧 dedupe 键是 `(track_id, identity_key)` 二元组 —— 只有当两份 handoff **同 `track_id`** 时, dedupe 才会把它们折叠成 1 行, 「传 `tracks` 还是 `deduped_tracks`」这个分支才会产生不同结果。若 fixture 用**不同** `track_id` (SC-2 字面「两份 handoff 两串」没有排除这种读法, 且与 T2 点名改写的既有测试里 `test_real_collector_no_collision_is_none` 恰好就是「不同 track_id」的用法同构), dedupe 不折叠, 接对/接反两版代码得到的 `identity_advisories` **完全相同** (均为恰 1 条, 而非声称的 0), 判据字面上的「接线反事实 → 0, 红」不成立, 子句退化为不分辨接线方向的冗余断言。
**evidence**: 用与「不同 `track_id`」读法 (`track-one`/`track-two`, 同 uuid 容器 `aaaa1111`, `alice`/`bob` 两串) 实跑真实 `collect_handoff_multibranch()`: 接对 (`v3repo/`) 得 `identity_advisories == [{"identity_key":"aaaa1111","owners":["alice","bob"],...}]`; 接反 (`v3repo_bad_wiring/`) 得**同样** `identity_advisories == [{"identity_key":"aaaa1111","owners":["alice","bob"],...}]` —— 两版代码结果逐字节相同, 且两次输出里均**不含** `dedupe` 字段 (`dedupe_stats["after_dedupe"] == dedupe_stats["input_tracks"] == 2`, 未发生折叠), 证实「不同 track_id」读法下判据不成立。
**为何不判 Major / 为何不必再开一轮**: 该子句本身把「接线反事实必须读到 0」写成了**显式验收判据**的一部分 (不是描述性旁注) —— 与 R4 发现的原始缺口性质不同: R4 时 SC-2 文本**完全没有**要求验证接反场景, 缺口是「结构性未设防」; v5 现在**要求** implementer 在 B.2 落地时把这条反事实真正跑到 0, 若 fixture 选了「不同 track_id」这条岔路, 该反事实断言字面上就通不过 (读到 1 而非 0), B.2 执笔人会在满足 SC-2 判据的过程中被自身文本逼着发现并改用同 `track_id` 的 fixture (即我在「R4 处置核对」里验证过、真正 discriminating 的那种形状) —— 这是一种自纠正结构, 不是恒绿陷阱。且紧邻的上一分句 (「同 uuid 容器两串跨两份 handoff, **dedupe 折叠后** advisory 仍恰 1 (函数级反事实: 对 deduped 调用 → 0)」) 已经用「dedupe 折叠后」显式钉住了「必须折叠」的前提, 生产接线子句是该分句的 E2E 版本, 上下文同构性进一步降低被岔开的概率。**建议修法** (窄, B.1 顺手一句话): 在「生产接线端到端」子句里把「两份 handoff 两串」改为「两份 handoff **同 `track_id`** 两串 (使 dedupe 真正折叠为 1 行)」, 消除这一处字面歧义, 省一次 B.2 实现→发现→回头改 fixture 的来回。

## Verdict

PASS_WITH_WARNINGS (0 Critical / 0 Major / 1 minor)

## Vote

PASS

**理由**: R4 遗留的 1 条 Major 经真实源码双向实跑 (接对/接反两份完整 state-scanner 目录) 证实已被 v5 新增的 SC-2「生产接线端到端」子句真正闭合 —— 按 SC-2 字面推荐的 fixture 形状 (同 uuid 容器、同 track_id) 实测, 接反必红, 且 T2 点名改写的两条既有 `box-A`/`box-B` 测试对该 Major 判定力仍为零 (符合 R4 finding, 未退化), 新子句是唯一防线且防线成立。R4 的 2 条 minor (SC-11 grep 改名绕过 / T6 缺 `phase` 字段) 均已按建议方式闭合。新发现的 1 条 minor (SC-2 子句未显式钉 `track_id` 相同, 存在一种字面合规但不 discriminating 的岔路读法) 因该子句自身把「接反必须读 0」写成显式验收判据、implementer 在满足判据过程中会被自身文本逼着发现并修正, 不构成恒绿陷阱, 属于 B 期顺手可补的文本精度项, 不影响 SC-2 的整体可验证性。本轮为 max_rounds 最后一轮, 三席 (tech-lead/code-reviewer/backend-architect) 已在 R4 投 PASS 且本轮未复审 (仅 knowledge-manager 的 2 条 Major 与本席 1 条 Major 是 R4→v5 的收敛目标); 就我审的范围 (SC-2 及其关联的 R4 全部 minor) 而言 0 Critical / 0 Major, 投 PASS。

## 轮次记录

Round 5 (qa-engineer, convergence mode, max_rounds 最后一轮, 镜头「终检: v5 的 SC-2 advisory 臂'生产接线端到端'子句是否真能抓住接反」): 用 scratchpad 既有 v4 语义补丁目录 (`v3repo/`, R3/R4 沿用未改动) 与新建接反补丁目录 (`v3repo_bad_wiring/`, 仅 `handoff_multibranch.py:714-716` 一处调用点改 `tracks`→`deduped_tracks`, 未改仓内文件) 两份完整 state-scanner 目录, 对 SC-2 v5 新子句按字面推荐 fixture 形状 (uuid 容器 `aaaa1111`, 两分支两份 handoff, 同 `track_id`, `alice`/`bob` 两串) 实跑真实 `collect_handoff_multibranch()`: 接对得 `identity_advisories` 恰 1 条, 接反得 0 条 —— 与 SC-2 声称逐字符合, R4-Major 闭合。同时验证 T2 点名改写的两条既有 `box-A`/`box-B` 测试在两个方向下均 PASS (对本 Major 判定力为零, 无退化)。额外构造「两份 handoff 用不同 track_id」的字面岔路读法双向重跑, 发现该读法下接对/接反结果完全相同 (均恰 1 条, `dedupe` 字段均不出现即未发生折叠), 判据字面「接反 → 0」不成立 —— 但因该反事实本身是 SC-2 显式验收判据 (implementer 必须让它读到 0 才算过), 这一岔路会在 B.2 落地过程中被自身文本逼着发现并改正, 不构成恒绿陷阱, 定性为 minor 而非 Major, 建议 B.1 顺手在子句里加「同 `track_id`」四字消歧。核对 R4 另 2 条 minor (SC-11 grep 改名绕过成文 / T6 补 `phase` 字段) 均已按建议方式在 v5 文本中闭合。复核 v5 其余定点编辑 (SC-3 S1 `get_container_id()` lock-in 断言、SC-5 反向 token `Kairos`/`DEC-2026`/`10cglocal`、SC-6 `LAYER_H_ACTIVE_WINDOW_DAYS` 常量作用域、SC-9 「非空交集 + 人工核语义」量词澄清、SC-11 成文、T6 八字段、D-0(a)/D2 §2.3.1 尾段作用域限定「仅用于 §2.3.5...不改变 §2.3.8.2...不用于 Layer L」、D4 模板鼓励句删除、14 checkbox 计数) 逐条读原文确认均为真实、可证伪的定点编辑, 未发现任何一条被改成恒绿断言或不可实现判据。就本席审查范围投 PASS, 0 Critical / 0 Major / 1 minor (标记 B 期顺手项)。
