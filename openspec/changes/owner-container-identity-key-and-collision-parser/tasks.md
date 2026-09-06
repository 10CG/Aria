# Tasks — `owner-container-identity-key-and-collision-parser`

> **Spec**: [proposal.md](./proposal.md) (v11, Approved 2026-09-05) | **决策单**: [`.aria/decisions/2026-09-05-owner-container-identity-key-rulings.md`](../../../.aria/decisions/2026-09-05-owner-container-identity-key-rulings.md) | **审计**: post_spec R1–R5 + post_planning R1–R9 聚合 (R9 CONVERGED) `.aria/audit-reports/post_{spec,planning}-R*-…-aggregated.md`
> **Level**: 3 (owner 裁定; 判据 cross-module) — 本文件 (A.2) + `detailed-tasks.yaml` (A.3, 单一 SOT: verification / deps / 工时 / rule6_note) + post_planning 收敛审计
> **Status**: A.2/A.3 **v9** (2026-09-06; post_planning **9 轮 CONVERGED**: R9 结论集 == R8 且五席全票 PASS, owner 两次加轮 5→7→9; v9 = 收敛后落延后 minor, 计划结构不变) — 进 B.1
> **Scope**: **三个仓** — `aria/` 子模块 (@ `7dd0135` v1.69.1) · `standards/` 子模块 (@ `cc864ee`) · 主仓 (@ `60808b2`; 冻结语料 `.aria/repro/handoff-tracks-frozen-2026-09-05.json` 已在)
> **ship target**: aria-plugin `<vNEXT>` — 档位按 proposal D5 (判据 PATCH; owner 可升 MINOR); **本文件不写字面版本号**, 5.2 执行时按当时 `plugin.json` 计并记入 CHANGELOG
> **ship 形态 (proposal §Impact)**: **S1** = a1-entry 未落地时 ship: 不 flip `get_container_id()`, 只加 `get_container_label()` + 迁移 inventory 告警; **S2** = a1-entry B.2 已落地 **且** 对方在 #174 ack。**S2 项不在本文件 checkbox 内** (归档门 `spec_complete.py` 只读 checkbox, 无「条件任务」机制 — post_planning R1 C-1); 见文末「S2 后续」表与激活规则

---

## 范围边界 — 本文件到哪里为止

| 阶段 | 归属 | 理由 |
|------|------|------|
| 组 0–5: 形态判定 / 测试先行 / 实现 / 规范与文档 / Rule #6 substitute + 回归 / 发布同步 + 两子模块本地合并 + 双推核验 + 主仓同步面 + 外向回帖 | **本文件** | change 自身交付物 (CLAUDE.md 多远程硬约束 1+2) |
| S2 后续 (flip / 发布门 / a1-entry SC-3 改写 / #135 时间线复现) | **激活后追加为 6.x checkbox; 未激活 ⇒ 5.8 手动开 tracker issue** (归档 Step 7 干净归档不自动产出) | 归档门只认 checkbox; 追加不改既有编号 |
| Phase C: 主仓 PR / pre-merge gate (Rule #8) / merge | **`phase-c-integrator`** (5.6 交付) | 通用流程 |
| Phase D: cycle 进度 / 归档 / 周期 handoff (Rule #9) / claim 释放 / **owner 插件更新 (`/plugin marketplace update` + `/plugin update` + 重启)** | **`phase-d-closer` + owner** | 归档门消费本文件全部 checkbox; `plugin-cache-currency` 在 owner 更新前预期 STALE |
| 改 a1-entry 的 track-id 契约 / 修 #182 / #135 缺口 1-2 / Aether 账号 / 容器 `git config` 供给 | **不在本文件** | proposal §非目标 |

---

## Task Group Overview

| 组 | 主题 | 依据 |
|----|------|------|
| **0** | B.1 起手: ship 形态判定 + 对方容器知会 | proposal §Impact / D-0 裁定 |
| **1** | 测试先行 (RED): SC-1/2/3(S1)/4/8 baseline-failing 结构化测试 + 既有测试改写 + 冻结语料 fixture + 回归锁 | proposal §SC「先红」子句 + Rule #6 substitute 档 |
| **2** | 实现: 解析 / 身份键 / 判定 / advisory / dedupe / board / 族键 / 新鲜度谓词 / label accessor + 迁移 inventory | proposal D1 / D3 / D-0(a) / D-3(a) |
| **3** | 规范与文档: standards §2.3.1 / §2.3.5 / §2.3.9; aria 六处取值文档 + 模板 + schema; CHANGELOG | proposal D2 / D4 / D5 |
| **4** | Rule #6 substitute 留痕 + 全套回归 + 主仓 state-check | proposal §Impact Rule #6 / SC-7 |
| **5** | 版本 bump → 本地 merge + tag → 双推核验 → 主仓同步面 → PR → 回帖 | proposal D5 / T11 / T12; 顺序由 yaml deps 定 (bump 先于 tag) |

## 0. B.1 起手

- [x] 0.1 `git fetch` 全远程, 实读 a1-entry 分支实况 (分支是否存在 / HEAD / `lib/identity.py` 是否已加 `get_container_uuid()` / 是否已进 master); 写 yaml `metadata.ship_shape` (S1 | S2-candidate) 并附证据
- [ ] 0.2 Aria #174 留言 (草案先落 `.aria/notes/2026-09-05-174-comment-draft.md`): 告知 D-0(a) 裁定 (Layer H 侧纯形状剥离, 不改 a1-entry 契约) + S2 条件下需改写其 SC-3 的判据草案, 征求 ack; 留言不阻塞 S1

## 1. 测试先行 (RED — 「先红」项对 aria `7dd0135` 实跑红, 组 2 落地后转绿)

- [ ] 1.1 `tests/test_collision.py:158-164` 改写 `test_split_owner_container_variants` (2-part / 1-part 新契约) — SC-1, 先红
- [ ] 1.2 `tests/test_collision.py` 判定臂 + advisory 函数级用例 — SC-2, 前三条先红
- [ ] 1.3 `tests/test_handoff_multibranch_collision_dedupe.py`: `test_owner_segment_participates_in_grouping_key` (`:1039`) 三臂; `test_both_latest_active_still_reports_self_multi_container` (`:305`) 期望改 `cross_owner` + 同 owner 变体; board 回显原串 — SC-4, 先红
- [ ] 1.4 `tests/test_collision.py` keys 断言改写 (`test_real_collector_emits_cross_owner_collision` / `test_real_collector_no_collision_is_none`); 新建 `tests/test_track_board_advisories.py` 承载「旧 snapshot 缺字段不崩」 — SC-8, 先红
- [ ] 1.5 端到端接线锁: uuid 容器 `aaaa1111`、**同一 `track_id`** 两份 handoff 两串 → snapshot `identity_advisories` 恰 1; 接反 → 0; 真实两段式两人两机端到端 → `cross_owner` — SC-2 端到端
- [ ] 1.6 冻结语料 fixture (`tests/fixtures/handoff-tracks-frozen-2026-09-05.json`, 八字段) + 裁剪脚本 `tests/fixtures/freeze_corpus.py` + `tests/test_collision_frozen_corpus.py` 前后对照机械归因 (含注入合成真撞车组) — SC-6
- [ ] 1.7 D-0(a) 族键夹具三条 — SC-2 族键子句, 先红
- [ ] 1.8 新建 `tests/test_identity_label.py` (label accessor + S1 lock-in) 与 `tests/test_migration_inventory.py` (phase1_gate / release_gate 迁移告警) — SC-3 S1 臂, 先红
- [ ] 1.9 `tests/test_track_board_advisories.py` ⚪ 行渲染 + 反事实 — SC-10
- [ ] 1.10 `tests/test_collision_frozen_corpus.py` 新鲜度谓词 (截止生效 / collector-renderer 同结论 / 单一实现 grep) — SC-11
- [ ] 1.11 SC-9 代码侧回归锁 (**baseline-green, 非 RED**): `phase-d-closer/tests/test_fetch_gate.py` 加 `kind="cross_owner"` 字符串夹具 (rule 1.54 为散文规则无求值引擎, 其触发面由 3.4 的文档 token 断言承载, proposal v9 SC-9 已同步)

## 2. 实现 (aria `state-scanner`)

- [ ] 2.1 `lib/collision.py::split_owner_container` (`:63-84`) 两段式 — 1.1 转绿
- [ ] 2.2 `lib/collision.py` 新增 `identity_key()` + `classify_claims` (`:143-168`) 确定性判定 — 1.2 判定臂转绿
- [ ] 2.3 `lib/collision.py::identity_drift_advisories(tracks)` + `handoff_multibranch.py:709-716` dedupe 前接线 + `identity_advisories[]` 恒存在 — 1.4 / 1.5 转绿
- [ ] 2.4 `handoff_multibranch.py:518-523` dedupe 键 `(track_id, identity_key)`; `track_board.py:412-417` 键同源 — 1.3 转绿
- [ ] 2.5 `lib/collision.py::track_to_claim_record` (`:86-140`; 调用点 `collision.py:349` / `track_board.py:783`) 族键剥离; `track_board.py:778-793` `tracks_by_tid` 用剥离后键 — 1.7 转绿
- [ ] 2.6 `lib/constants.py` `LAYER_H_ACTIVE_WINDOW_DAYS = 30` + `lib/collision.py::layer_h_is_fresh()`; collector `:709` 前 / renderer `:744` 前同一调用; board stale 标注 — 1.10 转绿, 1.6 改后 0 组
- [ ] 2.7 `lib/identity.py` 新增 `get_container_label()`; container-id 文件头注释 (`:126-140`) 改写为**S1 实况措辞**: 「label 当前仍参与协调身份 (设了会换身份), 后续版本改为仅展示; 建议留空」— 机械锁两条 grep (`:126-140` 区间含「当前仍参与协调身份」; 每个含「仅展示」的行同时含短语「后续版本」, `grep -cE`; 字面下限, 语义人工核) — 1.8 accessor 子句转绿 (S1 不动 `get_container_id()`)
- [ ] 2.8 迁移 inventory: `phase1_gate.py` (复用 `:486` Identity) 与 `release_gate.py` (import identity + `get_container_label()` + `read_claims` + `release_claim_by_track(identity=…)`) 告警, S1 无抑制 — 1.8 告警子句转绿
- [ ] 2.9 `track_board.py` ⚪ 行渲染: **独立数据路径**, 在顶层 `render_track_board` 于 dedupe (`:744`) 前对原始 tracks 调 `identity_drift_advisories`, 输出为 collision 段 (`:796` `_render_collision_lines` 结果) 之后的独立段, **不进** per-track 循环 (`:459-475` 只有 dedupe 后数据); label 并列显示 — 1.9 转绿

## 3. 规范与文档

- [ ] 3.1 `standards/conventions/session-handoff.md:116` §2.3.1: `<owner>` = 提交身份 (可取 `unknown`); `<container-id>` 三态; 定义 `identity_key`; 族键句 (限定仅用于 §2.3.5 Layer H 分组) — SC-5
- [ ] 3.2 §2.3.5 (`:178-186`) 三行判据 + 新鲜度截止句 + 「实质变更」说明 (standards 无 CHANGELOG; 按该文件既有惯例写成紧贴 §2.3.5 标题下方的 `> **Amended**: 2026-09-05 … / **Status**: …` blockquote, 与 §2.3 头部 Added/Purpose/Status 同形) — SC-5
- [ ] 3.3 新增 §2.3.9 (D-2(a)); 不引用 Lab 私有文档 — SC-5
- [ ] 3.4 aria 六处取值文档: `layer-l-integration.md:25-27,73,77` / `RECOMMENDATION_RULES.md:31` (该行须同时含 `cross_owner` 与 `identity_advisories` 两 token, 今日均无, 与 SC-9 首句对齐) / `references/rules/advanced-rules.md:544-572,578` / `references/state-snapshot-schema.md:1085` **与 `:1109-1121` 旧 dedupe 语义段** / `references/phase-1-collectors.md:75` (加一句: collision 三态语义 + `identity_advisories`); `SKILL.md:149-154` 取值不变**不改动** — SC-9 文档
- [ ] 3.5 `aria/templates/session-handoff.md` 示例改 uuid 形 + 删「设 label 使更可读」句 — SC-9 反向 grep
- [ ] 3.6 aria `CHANGELOG.md` 条目 (§2.3.5 实质变更 / `identity_advisories` / `get_container_label` / 档位) — 5.2 前置

## 4. Rule #6 substitute + 回归

- [ ] 4.1 rule6_note (yaml `metadata.rule6_note` 为单一来源): substitute = SC-1 / SC-2 (含族键臂) / SC-3 (S1 臂) / SC-4 / SC-8 ⇒ TASK-001/002/003/004/005/007/008 各有改前红 (`7dd0135`) / 改后绿实跑记录
- [ ] 4.2 全套回归 **两种跑法都必跑, 各管一类文件** (unittest discover 收不到 pytest 风格裸函数; 反之 pytest 吃整个 `tests/` 目录会因 `tests/__init__.py` 包语义让 12 个 `from _helpers import` 模块收集失败 — R3 实测): (a) `python3 aria/skills/state-scanner/tests/run_tests.py` 覆盖全部 TestCase 文件, 零失败, Ran ≥ 1476 + 本 Spec 新增 TestCase 数 (起草日实跑 1476); (b) `cd aria/skills/state-scanner && /home/dev/.local/bin/pytest -q -p no:cacheprovider tests/test_collision.py` 覆盖唯一 pytest 风格文件, 零失败, passed ≥ 16 + 本 Spec 在该文件新增数 (起草日实跑 16 passed, 两个 cwd 形态均可); **本 Spec 新建测试文件一律写 `unittest.TestCase`** 归 (a); `phase-d-closer/tests/test_fetch_gate.py`; session-closer / phase-d-closer handoff 写入测试 — SC-7
- [ ] 4.3 主仓 state-check: **13 条全绿**; `plugin-cache-currency` 预期 STALE 直到 owner D 期更新插件 (SC-7 例外条款) — 在 5.7 主仓同步面之后跑; **Rule #10 留痕**: handoff 记录「该例外为 post_planning R1 rework 引入 (owner Approved 之后), 请 owner D 期复议」

## 5. 发布 (顺序: 5.4 fixture 公开性 (5.1 前置) → 5.2 bump → 5.1 merge+tag → 5.3 双推核验 → 5.7 主仓同步面 → 4.3 → 5.6 PR → 5.5 回帖 ‖ 5.8 tracker (与 5.5 并行))

- [ ] 5.1 aria / standards 子模块本地 `git merge` 进 master + aria tag (**在 5.2 bump 之后**, 禁服务端合并)
- [ ] 5.2 aria-plugin 版本 5 文件 bump (`plugin.json` SOT + marketplace.json 两处 + VERSION + CHANGELOG + README) 按 D5 档位, 在 feature 分支上、merge 前
- [ ] 5.3 **owner 逐条授权后**双推 aria (master + tag) / standards, 推后逐 remote `ls-remote` 核验 master **与 tag 对象** SHA
- [ ] 5.4 fixture 公开性确认 (八字段无邮箱 / token / 内网地址; github 镜像可见)
- [ ] 5.5 issue 回帖 (**5.6 merge 后、归档前由执笔容器执行**): #193 / aria-plugin#135 指向本 Spec + 版本; #174 补 ship 结果; ship 后关 #193。#135 措辞按形态: **S1** = 「缺口 3 部分闭合 (解析 / 身份键 / dedupe / 漂移 advisory); label 陷阱 (08-13 形态) 待 S2 或 tracker」; **S2** = 「缺口 3 闭合」; 缺口 1/2 均留
- [ ] 5.6 主仓 feature 推 origin → `phase-c-integrator` C.2.4 gate → PR → merge → github 镜像
- [ ] 5.7 主仓同步面 (子模块推送核验后): 两 gitlink + `VERSION` + `README.md` badge + `README.zh.md` / `README.ja.md` / `README.ko.md` 版本串 + `docs/architecture/system-architecture.md` §2.8 与 `docs/architecture/version-scheme.md` 版本行 + CLAUDE.md **两行** (`:141` 版本行 + `:139` 方法论轨区间端点 `v1.52.0–v<NEXT>`; 项目状态段其余不动)
- [ ] 5.8 S2 后续的承载体 (归档 Step 7 只在 deferred/unverified 非空时产出, 干净归档不会自动记录): **S1** ⇒ 5.6 merge 后、归档前手动开 tracker issue (标题「S2 后续: flip / 发布门 / a1-entry SC-3 改写 / #135 时间线」, 含激活条件与 S2-1..S2-4 原文), 编号回填本文件「S2 后续」表; **S2 已激活** ⇒ 本条勾选为「已激活, 见 6.x」

---

## S2 后续 (非 checkbox; 激活规则见下)

| 项 | 内容 | 验收判据 |
|----|------|------|
| S2-1 | `get_container_id()` flip 为 uuid 优先 (只读 fs 兜底 hostname), 与 a1-entry `get_container_uuid()` 同值; 同 PR 成对撤销全部 S1 期产物: `identity.py:126-140` 注释改「label 仅展示」(撤销 2.7 机械锁) + 1.8 `test_identity_label.py` 的 S1 lock-in 断言翻转为「返回 uuid」+ 2.7 验收「S1 lock-in 仍绿」改 S2 + 4.1 Rule #6 台账加 S2 臂; 激活依赖: 排在 1.8 / 2.7 / 0.1 / 0.2 之后 | label 非空时返回 uuid (翻转后断言绿且改前对 S1 实现红); 注释区间不再含「当前仍参与协调身份」; state-scanner `lib/` `tests/` 内无 label 优先的 lock-in 断言 |
| S2-2 | 发布门: C.2 前 release 清单加「T3b 迁移检查通过」勾选项 | 未勾选则 flip 提交不进合并集 |
| S2-3 | 改写 a1-entry SC-3 判据 (仅 #174 ack 后) | ack 留言 id 记录; 判据改为「`get_container_uuid()` 与 flip 后 `get_container_id()` 同值; label 只在 `get_container_label()`」 |
| S2-4 | 复现 #135 08-13 时间线不再 `claim_not_found` | acquire 后加 label 再 release 成功 |

**激活规则**: 0.1 判 S2-candidate **且** #174 ack 已到 **且** 5.1 merge 尚未执行 (yaml 里 0.1 / 0.2 是 5.1 的前置, 保证判定与留言发生在 merge 前) ⇒ 追加 `6.1`–`6.4` checkbox + yaml TASK-027..030 (接入 5.1 前置), 并在 handoff 记录激活时点; 三条件任一不满足 ⇒ 维持 S1, 由 5.8 **手动**开 tracker issue 记录 S2 后续 (归档 Step 7 不会自动产出, 先例 sibling-spec-probe #192 是 deferred 非空时的自动路径)。**回退条款**: 激活后若 S2 前提失效 (a1-entry 被 revert / ack 撤回), 回退 S1 须 owner 裁定并记入 handoff; AI 不得自行删除已追加的 6.x checkbox 或 TASK-027..030 (它们是归档门输入, Rule #10)。 激活时同步改依赖边: 4.2 全套回归须在 6.1-6.4 之后重跑 (yaml TASK-032 deps += TASK-027..030)。 各 6.x 项按 yaml `dependencies_on_activation` 排序 (6.1 在 1.8 / 2.7 之后); 4.1 台账加 S2 臂并排在 6.1 之后。

## Success Criteria ↔ 任务映射

| SC | 任务 |
|----|------|
| SC-1 | 1.1 → 2.1 |
| SC-2 | 1.2 / 1.5 / 1.7 → 2.2 / 2.3 / 2.5 |
| SC-3 | 1.8 → 2.7 / 2.8 (S1 臂); S2 臂 = S2 后续表 |
| SC-4 | 1.3 → 2.4 |
| SC-5 | 3.1 / 3.2 / 3.3 |
| SC-6 | 1.6 → 2.6 |
| SC-7 | 4.2 (两种跑法) / 4.3 (含 plugin-cache-currency 例外) |
| SC-8 | 1.4 → 2.3 |
| SC-9 | 1.11 (回归锁) / 3.4 (文档 token 含 rule 1.54 行) / 3.5 |
| SC-10 | 1.9 → 2.9 |
| SC-11 | 1.10 → 2.6 |

## rule6_note

单一来源 = `detailed-tasks.yaml` `metadata.rule6_note` (本节不复述, 防两份不同文)。
