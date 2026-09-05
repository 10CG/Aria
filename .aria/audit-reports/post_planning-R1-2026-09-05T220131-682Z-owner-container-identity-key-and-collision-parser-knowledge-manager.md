---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-05T22:01:31.682Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/detailed-tasks.yaml
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 — owner-container-identity-key-and-collision-parser — knowledge-manager 席

> 审计对象: commit `60808b2` 的 `tasks.md` (6 组 41 项) / `detailed-tasks.yaml` (41 TASK)。对照 `proposal.md` v7 (逐行实读)、决策单 `.aria/decisions/2026-09-05-owner-container-identity-key-rulings.md`、`aria/skills/openspec-archive/SKILL.md`、`aria/skills/state-scanner/scripts/lib/spec_complete.py`、`aria/skills/phase-d-closer/SKILL.md`、`standards/` 子模块目录结构、及全部被点名的六处消费文档实际行号内容。

## 审计结论

### Major-1 — Lab 内部指针决策单落点自相矛盾, T12→TASK-035 丢件

proposal.md §D2 (:43) 与 T12 (:121) 都写明「10CG Lab 内部指针 (Aether 两账号模型) 放主仓 `docs/decisions/` 决策单 (D 期)」。但:

- 已实读的决策单 `.aria/decisions/2026-09-05-owner-container-identity-key-rulings.md` §「与 Aether 两账号模型的关系」(:16-18) 原文自述「本容器 git 身份的实际变更是 owner 的环境动作 (10cglocal 范围), 不由本 Spec 执行」且该节标题本身就是这份 Lab 指针内容 —— 换句话说, Lab 指针今天已经存在, 且落在 `.aria/decisions/`, 不是 `docs/decisions/`。
- `detailed-tasks.yaml` 里唯一承接 T12「发布同步」的任务是 TASK-035 (parent 5.2), 其 `deliverables` 实读只有: `plugin.json` / `marketplace.json` / `VERSION` / `CHANGELOG.md` / `README.md` (aria) + `CLAUDE.md` / `VERSION` / `README.md` / `system-architecture.md` / `version-scheme.md` (主仓) —— **没有任何 `docs/decisions/*.md` 条目**。`grep -n "docs/decisions"` 命中整个 `tasks.md` + `detailed-tasks.yaml` 结果为 0。

即: proposal 承诺的「D 期在 `docs/decisions/` 新建 Lab 指针决策单」这件事, 在任务分解里没有落地到任何一个 TASK 的 deliverables, 而已存在的 `.aria/decisions/` 决策单又自称就是那份指针。两处矛盾若不澄清, D 期会出现两种坏结果之一: (a) 没人做这件事 (承诺落空), 或 (b) 有人机械地在 `docs/decisions/` 又建一份内容重复的指针文件, 制造「同一件事两处记录、后续谁改谁不改」的知识漂移源头。

一致口径建议: `.aria/decisions/2026-09-05-owner-container-identity-key-rulings.md` 已满足 D2/T12 对「Lab 内部指针」的全部要求 (不引用 Lab 私有文档进 standards, 只记 10CG Lab 内部关系), 不需要在 `docs/decisions/` 重建; 应把 T12/TASK-035 的措辞改为「指向既有 `.aria/decisions/2026-09-05-...-rulings.md`, 不新建 `docs/decisions/` 文件」, 并在 `standards/conventions/session-handoff.md` §2.3.9 或 CHANGELOG 条目里补一处指针引用即可。

### Major-2 — `state-snapshot-schema.md` 仅锁 `:1085`, 未覆盖 dedupe 语义的既有大段说明

`references/state-snapshot-schema.md` 实读 (`grep -n`) 确认: `:1084-1088` 是 `collision` 字段声明块 (`kind`/`groups`/`dedupe`), 但紧随其后的 `:1107` `:1109` `:1111` `:1119` `:1121` `:1127` 是一整段对当前 dedupe 行为的详细说明, 其中 `:1111` 原文明确写「collector 调用 `dedupe_latest_per_track_container(tracks) -> (deduped, stats)`, which groups `tracks` by **`(track_id, owner/container)`** —— i.e. the OWNER and CONTAINER segments only, split via `lib.collision.split_owner_container`」。

本 Spec 的 TASK-015 (2.4) 把 dedupe 键从「按 `(track_id, owner, container)` 三元组」改成「按 `(track_id, identity_key)`」—— 对 uuid 容器, 不同 owner 串会被同一个 `identity_key` 折叠, 这与 `:1111` 现在的措辞 (「OWNER and CONTAINER segments only」的字面描述) 不再等价, 会在 ship 后变成描述旧行为的过时文档。而 TASK-024 (3.4) 给 `state-snapshot-schema.md` 的 deliverable 只标注了 `:1085` (collision 段 + `identity_advisories` additive bump), 完全没有点名 `:1107-1127` 这一段既有 dedupe 行为说明。

这正落在 CLAUDE.md 不可协商规则 3「文档与代码必须同步更新」的口子上 —— 不是没有文档, 而是文档存量已经很详细, 但任务分解漏掉了要同步改写的既有段落。建议: TASK-024 的 `state-snapshot-schema.md` deliverable 行号扩展为 `:1085, :1109-1121` (或直接写「collision 段 + dedupe 语义段」), 并在 SC-9 或 rule6_note 里补一句「`identity_key` 折叠语义需替换旧的 `(track_id, owner, container)` 措辞, 不能只加字段不改旧句」。

### Major-3 — `references/phase-1-collectors.md` 当前对 SC-9 判据字面「零交集」, 任务未给出具体编辑指令

SC-9 的机械判据是「每个文件 F 与 token 集合 `{cross_owner, self_multi_container, identity_advisories}` 的交集不为空」。逐文件实读结果:

| 文件 | 实读结果 |
|---|---|
| `layer-l-integration.md` | `:26` `cross_owner`、`:27` `self_multi_container`、`:73` `:77` `cross_owner` — 已非空 |
| `RECOMMENDATION_RULES.md` | `:31` 只有 `collision.kind`, 无三个 token 字面; proposal §D4 已明确点名「加 `identity_advisories` 一句」, 指令完整 |
| `advanced-rules.md` | `:549` 起 `cross_owner`/`self_multi_container` 字面已存在 — 已非空 |
| `phase-1-collectors.md` | 全文 `grep` 只命中「collision」作为英文子串 (如 `:75` 「跨 owner collision」) 和 `tracks_multibranch`，**零处**出现 `cross_owner` / `self_multi_container` / `identity_advisories` 字面 |

`phase-1-collectors.md` 是唯一一个「今天字面零命中」且 proposal 正文没有像 RECOMMENDATION_RULES.md 那样给出具体编辑指令（「加 `identity_advisories` 一句」）的文件。TASK-024 把它和另外四个文件並列列为 deliverable, 但完全没有说明 `:75` 那句「跨 owner collision」该怎么改才能满足 SC-9。这会让 B.2 执行者要么漏改 (SC-9 对此文件判定失败), 要么临场自行决定改法而无 spec 依据。建议在 TASK-024 verification 里补一句类似 RECOMMENDATION_RULES.md 的具体指令 (如「`:75` 补一句 `identity_advisories` 或把「跨 owner collision」改写为含 `cross_owner` 字面的措辞」)。

### Major-4 — TASK-038「issue 回帖」D 期实际执行方无接收任务

`tasks.md` §范围边界表把 Phase D 全部交给 `phase-d-closer` (cycle 进度 / 归档 / 周期 handoff / claim 释放), 但没有把「issue 回帖 / 关闭 #193 / 留 #135 缺口」列入 phase-d-closer 的职责范围。TASK-038 (parent 5.5, 组 5, 本文件范围内) 的 deliverable 只是 `.aria/triage-comment.md` 追加 ship 段, notes/tasks.md 5.5 原文明确写「D 期执行, 本条只准备文案」。

实读 `aria/skills/phase-d-closer/SKILL.md` 的全部「issue」相关段落 (:111,:113,:119,:123-124,:261-262,:281), 其唯一的 issue 相关职责是「委托 openspec-archive Step 7 建 D auto-issue (deferred/unverified 项追踪)」, 与「把已经写好的 `.aria/triage-comment.md` POST 到既有 issue #193/#135/#174 并关闭 #193」是完全不同的两件事 —— 后者在 phase-d-closer 的 SKILL.md 里没有任何一处提及会读取或消费 `.aria/triage-comment.md`。`.aria/triage-comment.md` 本身是 `issue-triage` Skill 的产物惯例 (草稿态), 也没有任何 Skill 声明会在 Phase D 自动 POST 它。

结论: 「issue 回帖」这个动作被 tasks.md 明文托付给「D 期执行」, 但 D 期唯一的接口 Skill (phase-d-closer) 不认领这项职责, 存在一个没有 owner 的执行缺口 —— 若无人手工记得去做, 该动作会静默丢失 (#193 不会被关闭, #174 不会收到 ship 结果通知, 与 memory「复核轮临时报告必须落盘」同类的可审计性问题: 至少要有一个任务或 handoff 段明确点名「谁在 D 期执行这条」)。建议: 要么在 Phase D 的 handoff 模板/phase-d-closer 调用清单里显式加一条「消费本 Spec 的 `.aria/triage-comment.md` 并 POST」, 要么把这个动作挪回本文件组 5 (在 merge 后同 session 内直接执行, 不依赖「D 期」这个没有落地机制的托付)。

### Major-5 — S1 形态下组 6 四个 checkbox 会触发归档 Step 1 默认 BLOCK, 任务文档未记录逃生舱路径

实读 `aria/skills/state-scanner/scripts/lib/spec_complete.py` 的 `is_spec_complete` 判据 (docstring :10-16 + 实现): `complete := tasks.md 全 [x] 且无 carry-forward 注释, OR (tasks.md 缺失时 yaml 全部 status ∈ {done, completed}), OR Status 归一化 == 'done'`。代码里没有任何分支把 `status: deferred-s2` 或带 `(DEFERRED-S2)` 前缀的未勾选行视为「已完成」——`_extract_deferred_or_unchecked_items` 只是把它们收进 `deferred_items` 喂给 Step 7 的 tracker issue payload, 不改变 `complete` 布尔值。

`aria/skills/openspec-archive/SKILL.md` 的 verdict 路由表 (:152-154) 明确: 「`complete=false ∧ verdict∈{pass,warn} ∧ 未配逃生舱`: 默认 BLOCK」。S1 ship 形态下, `detailed-tasks.yaml` 的 TASK-027~030 (组 6, parent 6.1-6.4) 会保持 `status: pending` (tasks.md §Impact/组 6 头部写「归档门按 `status: deferred-s2` 识别」, 但目前 yaml 里 TASK-027~030 的 `status` 字段实读仍是字面 `pending`, 只有说明文字提到未来要改; TASK-000 verification 也只写「S1 时 TASK-027~030 status 置 deferred-s2」——`deferred-s2` 本身也不在 `spec_complete.py` 认识的 done-family 里), `tasks.md` 组 6 的 4 个 `- [ ]` 也会保持未勾选。两者叠加 = `complete=False`, 若不配 `--archive-design-only <reason>` 逃生舱, Step 1 会默认 BLOCK 整个归档。

先例核实: `openspec/archive/2026-08-21-subprocess-decode-hardening/` 与 `2026-08-22-...-ci-path-coverage/` 两份 #95 硬化后 (2026-07-05+) 的归档都是走 `archive_type: implementation-deferred` + `archived_reason` 路径过的 Step 1, 而不是把 checkbox 硬性勾满; 这条路径同时会经 Step 7 自动建 tracker issue 承接未完成项 (与 commit 记录的 sibling-spec-probe tracker #192 是同一 Step 7 机制, 虽然那次是 `verdict=warn` 触发, 不是 `complete=false` 触发, 但 Step 7 的 payload 组装逻辑对两种触发源一致)。

`tasks.md` / `detailed-tasks.yaml` 全文没有一处提到 D 期需要 `--archive-design-only` 这个逃生舱, 也没有在组 6 或 §范围边界表里给 phase-d-closer 留一句「S1 归档走 design-only + 理由, Step 7 会自动建 tracker 追踪 S2 四项」的指引。若无此认知, D 期很可能因为组 6 未完成而卡在归档 Step 1, 造成不必要的困惑或被误当作「本 Spec 真的没做完」。建议在 tasks.md 组 6 标题下或 §范围边界表补一行: 「S1 形态归档 (phase-d-closer D.2) 须用 `--archive-design-only` + 理由 (S2 待 a1-entry B.2 落地) 通过 Step 1; Step 7 会自动为组 6 四项建 tracker issue」。

## 确认无越界 / 无问题项 (核实后排除, 不计入 finding)

- **CLAUDE.md 改动范围**: TASK-035 (5.2) 对 CLAUDE.md 的 deliverable 明确标注只动「# 版本行」, 未触及「项目状态」段落的其余叙事 (M6 blocker / 并发 track 指针等), 符合 `claude-md-hygiene.md` 覆写而非追加、且不越界改动本 Spec 无关内容的要求。
- **组 3 (TASK-021~026) 与 proposal D2/D4/D5 的映射**: 逐条核对, §2.3.1/§2.3.5/§2.3.9 (T5) 三块、七处消费文档 (五处文档改动 + SKILL.md 显式不改 + 模板改动, 合计七处与 proposal 原文「七处」吻合) 均有对应 TASK 且 deliverables 路径可实读定位 (Major-2/3 是"覆盖不全"而非"完全缺失", 已单独列出)。
- **决策单与审计聚合路径引用**: `tasks.md` 头部引用的 `.aria/decisions/2026-09-05-owner-container-identity-key-rulings.md` 与 `post_spec-R{1..5}-...-aggregated.md` 全部实读存在 (`ls .aria/audit-reports/` 核实 R1-R5 每轮 aggregated + 5 席位报告齐全)。
- **TASK-00A #174 留言无本地落盘**: 已核实 `#174` 是相邻 Spec `a1-entry-claim-duplicate-work-guard` 的真实立项 issue (非本 Spec 自建), TASK-029 的 verification 要求「对方 ack 留言 id 记录」, 说明 ack 结果确有留痕点; 留言本身「外向, 无仓内文件」属既有惯例 (issue-triage 类 Skill 同样只产出草稿供 POST, 不强制本地存副本), 未达到需要单独 finding 的程度。

## Verdict

PASS_WITH_WARNINGS

## Vote

PASS

## 轮次记录

- Round 1 (knowledge-manager 席): Critical 0 / Major 5 / Minor 0。0 Critical → 不构成 REVISE 门槛；5 项 Major 均为可在 B.2/D 期通过补一到两句任务说明修复的知识架构/文档同步缺口，未发现结构性阻断项。投 PASS，5 项 Major 建议随 B.2 或本报告一并处理。
