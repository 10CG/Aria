# Tasks — `owner-container-identity-key-and-collision-parser`

> **Spec**: [proposal.md](./proposal.md) (v7, Approved 2026-09-05) | **决策单**: [`.aria/decisions/2026-09-05-owner-container-identity-key-rulings.md`](../../../.aria/decisions/2026-09-05-owner-container-identity-key-rulings.md) | **审计**: post_spec R1–R5 聚合 `.aria/audit-reports/post_spec-R*-…-aggregated.md`
> **Level**: 3 (owner 裁定; 判据 cross-module) — 本文件 (A.2) + `detailed-tasks.yaml` (A.3) + post_planning 收敛审计
> **Status**: A.2/A.3 产出 2026-09-05; post_planning 待跑
> **Scope**: **三个仓** — `aria/` 子模块 (@ `7dd0135` v1.69.1: state-scanner `lib/collision.py` `lib/identity.py` `lib/constants.py` `scripts/collectors/handoff_multibranch.py` `scripts/renderers/track_board.py` `scripts/phase1_gate.py` `scripts/release_gate.py` + 6 处 references + `aria/templates/session-handoff.md` + phase-d-closer `tests/test_fetch_gate.py` + 版本 5 文件) · `standards/` 子模块 (@ `cc864ee`: `conventions/session-handoff.md` §2.3.1 / §2.3.5 / 新 §2.3.9) · 主仓 (@ `abb4fd3`: 冻结语料 `.aria/repro/handoff-tracks-frozen-2026-09-05.json` 已在; 版本同步面; 本 Spec 三文件)
> **ship target**: aria-plugin `<vNEXT>` — 档位按 proposal D5: 判据上 PATCH (bug 修复 + additive 字段), owner 可因 §2.3.5 行为变更升 MINOR; **本文件不写字面版本号**, 5.2 执行时按当时 `plugin.json` 计并记入 CHANGELOG
> **ship 形态 (proposal §Impact)**: **S1** = a1-entry 未落地时 ship: 不 flip `get_container_id()`, 只加 `get_container_label()` + 迁移 inventory 告警; **S2** = a1-entry B.2 已落地且对方在 #174 ack: flip + 发布门 + 改写其 SC-3。B.1 起手第一件事是 fetch a1-entry 分支实况定形态 (1.0)。S2 专属任务 (6.x) 在 S1 下**不执行、不勾选、不算未完成** (归档门按 `status: deferred-s2` 识别)

---

## 范围边界 — 本文件到哪里为止

| 阶段 | 归属 | 理由 |
|------|------|------|
| 组 1–5: 形态判定 / 测试先行 / 实现 / 规范与文档 / Rule #6 substitute + 回归 + 版本面 + 两子模块本地合并 + 双推 + gitlink | **本文件** | change 自身交付物 (CLAUDE.md 多远程硬约束 1+2: 子模块一律本地 merge, 推后逐 remote `ls-remote`) |
| 组 6: S2 形态专属 (flip / 发布门 / a1-entry SC-3 改写) | **本文件, 条件** | 仅 S2 执行 |
| Phase C: 主仓 PR / pre-merge gate (Rule #8) / merge | **`phase-c-integrator`** (5.6 交付) | 通用流程 |
| Phase D: cycle 进度 / 归档 / 周期 handoff (Rule #9) / claim 释放 | **`phase-d-closer`** | 归档门消费本文件全部 checkbox |
| 改 a1-entry 的 track-id 契约 / 修 #182 status 归一 / #135 缺口 1-2 / Aether 账号 / 容器 `git config` 供给 | **不在本文件** | proposal §非目标 |

---

## Task Group Overview

| 组 | 主题 | 依据 |
|----|------|------|
| **0** | B.1 起手: ship 形态判定 + 对方容器知会 | proposal §Impact 排序 / D-0 裁定 |
| **1** | 测试先行 (RED): SC-1/2/4/8/10/11 的 baseline-failing 结构化测试 + 既有测试改写 + 冻结语料 fixture | proposal §SC「先红」子句 + Rule #6 substitute 档 |
| **2** | 实现: 解析 / 身份键 / 判定 / advisory / dedupe / board / 族键 / 新鲜度谓词 / identity label + 迁移 inventory | proposal D1 / D3 / D-0(a) / D-3(a) |
| **3** | 规范与文档: standards §2.3.1 / §2.3.5 / §2.3.9; aria 六处取值文档 + 模板 + schema; CHANGELOG | proposal D2 / D4 / D5 |
| **4** | Rule #6 substitute 留痕 + 全套回归 + 主仓 state-check | proposal §Impact Rule #6 / SC-7 |
| **5** | 发布同步 + 两子模块本地合并 + 双推核验 + gitlink + 外向 (issue 回帖) | proposal D5 / T11 / T12 |
| **6** | S2 形态专属 (条件) | proposal §Impact S2 |

---

## 0. B.1 起手 (ship 形态判定)

- [ ] 0.1 `git fetch` 全远程, 实读 a1-entry 分支实况 (`origin/feature/*a1-entry*` 是否存在、其 `lib/identity.py` 是否已加 `get_container_uuid()`、是否已进 master); 据此在 detailed-tasks.yaml `metadata.ship_shape` 写 **S1** 或 **S2**; S1 时组 6 全部标 `deferred-s2`
- [ ] 0.2 Aria #174 留言: 告知 D-0(a) 裁定 (Layer H 侧纯形状剥离, 不改 a1-entry 契约) + S2 条件下本 Spec 需改写其 SC-3 的判据, 征求 ack (S2 前置); 留言不阻塞 S1 路径

## 1. 测试先行 (RED — 每条对 aria `7dd0135` 先红, 组 2 落地后转绿)

- [ ] 1.1 `tests/test_collision.py`: 改写 `test_split_owner_container_variants` (2-part → `("simonfish","bfe8285d","")`, 1-part `"solo"` → `("","solo","")`, 3-part 不变) — SC-1
- [ ] 1.2 `tests/test_collision.py` 新增判定臂用例 (经 `dedupe_latest_per_track_container` → `classify`): 同容器双 owner → `none`; 两人两机 → `cross_owner`; 同人两机 → `self_multi_container`; 漂移后无共现 → `cross_owner`; 零段 vs 两段同主机名 → `self_multi_container`; 三 owner 同 uuid advisory 长度 3; legacy / `unknown` owner 不产生 advisory — SC-2 判定臂 + advisory 函数级
- [ ] 1.3 `tests/test_handoff_multibranch_collision_dedupe.py`: `test_owner_segment_participates_in_grouping_key` 改三臂 (uuid 折叠 / 主机名不折叠 / `devbox01` 不折叠); `test_both_latest_active_still_reports_self_multi_container` 期望改 `cross_owner` + 新增同 owner 串变体断 `self_multi_container`; board 回显原串断言 — SC-4
- [ ] 1.4 `tests/test_collision.py`: 改写 `test_real_collector_emits_cross_owner_collision` / `test_real_collector_no_collision_is_none` 的 `keys == {kind, groups}` 为含 `identity_advisories`; 新增旧 snapshot 缺字段时 `track_board` / rule 1.54 / `fetch_gate` 不崩 — SC-8
- [ ] 1.5 **端到端接线锁**: 真实 collector 夹具 (`_build_repo` 风格, uuid 容器 `aaaa1111`, **同一 `track_id`** 两份 handoff 两串) 经 `collect_handoff_multibranch` → snapshot `collision.identity_advisories` 恰 1; 接线反事实 (`:709` 传 `deduped_tracks`) → 0; 真实两段式两人两机端到端 → `cross_owner` — SC-2 端到端
- [ ] 1.6 冻结语料复制为 `tests/fixtures/handoff-tracks-frozen-2026-09-05.json` (八字段 `track_id / owner_container / status / phase / updated_at / filename / branch / legacy`); 前后对照测试: 改前 A = 1 组 / 改后 = 0 组 (D-3(a) 生效); **机械归因** (组内全部 `updated_at` 早于 30 天 → stale(#182); 否则 kind 映射); 注入一组合成真撞车行 (显式标注) 必须归「真撞车」 — SC-6
- [ ] 1.7 D-0(a) 族键夹具: `slug-aaaa1111` + `slug-bbbb2222` 同组可达 🟡/🔴; `x-20260719` 剥后与冻结语料零碰撞; `slug-abcdefg` (7 位) 不剥 — SC-2 族键子句
- [ ] 1.8 `lib/identity.py` 测试 (新建 `tests/test_identity_label.py`): label 非空时 `get_container_label()` 返回 label 且 `get_container_id()` **仍**返回 label (S1 lock-in); `phase1_gate` / `release_gate` 在 label 非空且 `claims/<label>/` 有 active 时各自输出迁移告警 (含 active 数) — SC-3 S1 臂
- [ ] 1.9 `track_board` ⚪ 行测试: fixture 渲染恰 2 条 ⚪ (`023236f2` / `bfe8285d`) 含 owners[] + first/last_seen; 无 advisory 不渲染; 反事实 (对 dedupe 后行算) → 0 行 — SC-10
- [ ] 1.10 新鲜度谓词测试: fixture 中早于窗口的 active 行不出现在 `groups`; collector 与 renderer 同一 fixture 同 `kind`/`groups`; `updated_at` 与天数比较表达式只在 lib 一处 — SC-11
- [ ] 1.11 rule 1.54 触发面 + `fetch_gate` 夹具: `coordination.enabled=false` + `kind=cross_owner` → 规则命中; `test_fetch_gate.py` 加 `kind="cross_owner"` 字符串夹具断 advisory 文案 — SC-9 (代码部分)

## 2. 实现 (aria `state-scanner`)

- [ ] 2.1 `lib/collision.py::split_owner_container` 两段式 (零段 `("",串,"")`; 三段兼容) — 1.1 转绿
- [ ] 2.2 `lib/collision.py` 新增 `identity_key(owner, container)` (`^[0-9a-f]{8}$` ⇒ container; 否则 `owner + "/" + container`) + `classify_claims` 确定性判定 (identity_key 计数; 非空非 `unknown` owner 集合) — 1.2 转绿
- [ ] 2.3 `lib/collision.py::identity_drift_advisories(tracks)` (dedupe 前全语料, 跨 track; `{identity_key, owners[], first_seen, last_seen}`; legacy / `unknown` 排除) + `handoff_multibranch.py:709` dedupe **前**调用并写 `collision.identity_advisories[]` (恒存在) — 1.4 / 1.5 转绿
- [ ] 2.4 `handoff_multibranch.py:518-523` dedupe 键 `(track_id, identity_key)`; `track_board.py:412-417` 建表/查表键同源 (都经 `track_to_claim_record`) — 1.3 转绿
- [ ] 2.5 `lib/collision.py::track_to_claim_record` 族键剥离 (`-[0-9a-f]{8}$`, 只改 `ClaimRecord.track_id`, 不动 frontmatter 原串); `track_board.py` `tracks_by_tid` 索引改用剥离后键 — 1.7 转绿 (D-0(a))
- [ ] 2.6 `lib/constants.py` 新增 `LAYER_H_ACTIVE_WINDOW_DAYS = 30` + `lib/collision.py::layer_h_is_fresh(row, now, days)`; Layer H 记录构造阶段 (collector `:709` 前 / renderer `:743` 前) 同一调用, 被截止行不进 reconcile/classify; board 以「stale」列出 — 1.10 转绿 (D-3(a))
- [ ] 2.7 `lib/identity.py` 新增 `get_container_label()`; `~/.aria/container-id` 文件头注释改写 (label 仅展示) — 1.8 转绿 (S1 部分)
- [ ] 2.8 T3b 迁移 inventory: `phase1_gate.py` (复用 `:486` Identity) 与 `release_gate.py` (import identity + `get_container_label()` + `read_claims` 枚举 + 传 `identity=`) 在 label 非空且 `claims/<label>/` 有 active 时输出告警 (S1: 无抑制) — 1.8 转绿
- [ ] 2.9 `track_board.py` ⚪ 行渲染 (dedupe 前调用 `identity_drift_advisories`) + label 并列显示 — 1.9 转绿

## 3. 规范与文档

- [ ] 3.1 `standards/conventions/session-handoff.md` §2.3.1: `<owner>` = 提交身份 (D-1(a)), 注明可取 `unknown`; `<container-id>` 三态 (uuid 字段 / 历史主机名 / 只读 fs hostname); 定义 `identity_key`; track-id 尾段 `-<8hex>` 族键句 (**限定仅用于 §2.3.5 Layer H 分组, 不改 §2.3.8.2 同串规则, 不用于 Layer L**) — SC-5
- [ ] 3.2 §2.3.5 判据表三行 (`cross-owner` / `self-multi-container` 用 `identity_key` + 非空非 `unknown` `<owner>` 集合; 新增 `same-identity-multi-owner` ⚪, 作用域 = 采用方仓 handoff 全集跨 track 跨分支) + Layer H 新鲜度截止一句 (D-3(a)) + 「实质变更」说明 — SC-5
- [ ] 3.3 新增 §2.3.9「AI runner 提交身份」(D-2(a): 统一机器身份, local-part 与采用方机器账号名一致; 可追溯性由 `<container-id>` + handoff 承担; 不引用 Lab 私有文档; 采用方人机账号治理与 `git config` 供给不在本规范) — SC-5
- [ ] 3.4 aria 六处取值文档同步: `references/layer-l-integration.md:25-27,73,77` / `RECOMMENDATION_RULES.md:31` (加 `identity_advisories` 一句) / `references/rules/advanced-rules.md:544-572,578` / `references/state-snapshot-schema.md:1085` (collision 段 + `identity_advisories` additive bump) / `references/phase-1-collectors.md:75`; `SKILL.md:149-154` 取值字面不变**不改动** — SC-9 (文档部分)
- [ ] 3.5 `aria/templates/session-handoff.md`: owner-container 示例改 uuid 形, **删除**「设 label 使更可读」鼓励句 — SC-9 反向 grep
- [ ] 3.6 aria `CHANGELOG.md` 条目: 明示 §2.3.5 判据实质变更 (采用方看板输出改变) + `identity_advisories` 新字段 + `get_container_label()`; 版本档位按 D5 记录 — 5.2 前置

## 4. Rule #6 substitute + 回归

- [ ] 4.1 `rule6_note` 写入本文件与 yaml: 无 SKILL.md 指令面 / description 改动 (取值字面存在但不变) ⇒ 「描述性 / 机械」档 substitute = SC-1 / SC-2 / SC-3 (S1 臂) / SC-4 / SC-8 五条 baseline-failing 结构化测试, 各自 RED→GREEN 记录 (改前 `7dd0135` 实跑红, 改后绿)
- [ ] 4.2 state-scanner 全套 pytest (起草日 1492 个 test 定义) 零回归 (点名改写项 1.1 / 1.3 / 1.4 外无新增红); phase-d-closer `test_fetch_gate.py` 全绿; session-closer / phase-d-closer handoff 写入测试全绿 — SC-7
- [ ] 4.3 主仓 14 条 state-check 全绿 (含 `plugin-cache-currency` / `m6-version-badge-match` / `plugin-version-arch-docs-match` 版本面); `linked-issue-field-availability` 对本 Spec 三文件 OK — SC-7

## 5. 发布同步 + 合并推送 + 外向

- [ ] 5.1 aria 子模块: 本地 feature 分支 → 本地 `git merge` 进 master (禁 Forgejo 服务端合并, CLAUDE.md 硬约束 1) + tag; standards 子模块同法 (§2.3 改动)
- [ ] 5.2 aria-plugin 版本 5 文件 bump (`plugin.json` SOT + marketplace.json 两处缩进 + VERSION + CHANGELOG + README) 按 D5 档位; 主仓同步面 (CLAUDE.md §版本管理列表: gitlink + VERSION + README badge + i18n 仅版本串 + 架构文档版本行)
- [ ] 5.3 **owner 逐条授权后**双推 aria / standards (`origin` + `github`), 推后逐 remote `ls-remote` 核验 (硬约束 2, 不信 push 回执); 主仓 gitlink bump 在子模块推送核验后 (memory `feedback_sequenced_multirepo_gitlink_bump`)
- [ ] 5.4 冻结语料 fixture 已在 aria 测试目录 (1.6) — 确认 github 镜像可公开 (八字段无敏感项, R3 qa 实读结论)
- [ ] 5.5 issue 回帖: #193 与 aria-plugin#135 (缺口 3) 指向本 Spec + 关键裁定; #174 (0.2 已留) 补 ship 结果; ship 后关 #193, #135 留缺口 1/2 (D 期执行, 本条只准备文案)
- [ ] 5.6 主仓 feature 推 origin → `phase-c-integrator` C.2.4 pre-merge gate → PR → merge → github 镜像 (交付给 Phase C)

## 6. S2 形态专属 (条件: a1-entry B.2 已落地 且 #174 ack; S1 下标 `deferred-s2`)

- [ ] 6.1 `get_container_id()` 改 uuid 优先 (只读 fs 兜底仍 hostname); 与 a1-entry `get_container_uuid()` 同值 — SC-3 S2 臂
- [ ] 6.2 发布门: phase-c-integrator C.2 前 release 清单加「T3b 迁移检查通过」勾选项; 未通过则 flip 提交不进合并集 — SC-3 S2 臂
- [ ] 6.3 改写 a1-entry SC-3 判据 (「`get_container_uuid()` 与 flip 后 `get_container_id()` 同值; label 只在 `get_container_label()`」), 仅在 #174 ack 后动对方文本
- [ ] 6.4 复现 #135 08-13 时间线 (acquire 后加 label 再 release) 不再 `claim_not_found` — SC-3 S2 臂

---

## Success Criteria ↔ 任务映射

| SC | 任务 |
|----|------|
| SC-1 | 1.1 → 2.1 |
| SC-2 | 1.2 / 1.5 / 1.7 → 2.2 / 2.3 / 2.5 |
| SC-3 | 1.8 → 2.7 / 2.8 (S1); 6.1 / 6.2 / 6.4 (S2) |
| SC-4 | 1.3 → 2.4 |
| SC-5 | 3.1 / 3.2 / 3.3 |
| SC-6 | 1.6 → 2.6 (0 组) |
| SC-7 | 4.2 / 4.3 |
| SC-8 | 1.4 → 2.3 |
| SC-9 | 1.11 / 3.4 / 3.5 |
| SC-10 | 1.9 → 2.9 |
| SC-11 | 1.10 → 2.6 |

## rule6_note

见 4.1。豁免判据: `standards/conventions/skill-benchmark-exemption.md` 第一行「描述性 / 机械」档 (与 §5 样例 `state-scanner-stale-refs-false-parity` collector 代码层同性质); substitute 五条均为改前先红的结构化测试; 无 description / 指令流程变动 ⇒ 不照跑 AB。若 B 期发现任何 SKILL.md 文本必须改动 (含 `:149-154` 取值字面), 立即转「照跑」并在此更新。
