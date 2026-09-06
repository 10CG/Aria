---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-09-05T22:32:08.490Z
context: openspec/changes/owner-container-identity-key-and-collision-parser/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R2 — code-reviewer 席 (双层一致性 + 规格合规终检)

审计对象: commit `03c6a9e` 的 `tasks.md` v2 (组 0–5, 38 checkbox + S2 后续表 + SC 映射表) 与 `detailed-tasks.yaml` v2 (38 TASK + `metadata.s2_followup`)。依据: 同目录 `proposal.md` v8、本席 R1 报告、R1 聚合 (`post_planning-R1-2026-09-05T220131-682Z-…-{code-reviewer,aggregated}.md`)。只审不改; 所有行号均实读 (aria @ `7dd0135`, standards @ `cc864ee`, 主仓 @ `03c6a9e`)。

## R1 处置核对

| R1 项 | 三态 | v2 证据 |
|---|---|---|
| M-1 `deferred-s2` 归档机制不存在 | **已解决** (结构性改法) | 组 6 已从 checkbox 移出: `tasks.md:93-102` 改为「S2 后续」表 (非 checkbox) + 激活规则; yaml `tasks[]` 无 TASK-027..030, 四项定义留在 `metadata.s2_followup` (`detailed-tasks.yaml:40-58`); `tasks.md:8` / `:17` / yaml `:7-8` 三处写明「归档门只读 checkbox」。实跑 `spec_complete.py --gate`: `tasks.md has 38/38 unchecked task(s)`, `deferred_items` 恰 38 条 = 全部真实任务, 无杂散 checkbox。S1 归档时不再有「条件任务」被当未完成上报 |
| M-2 发布顺序倒置 (tag 先于 bump) | **已解决** | yaml deps: TASK-034 (merge+tag) `dependencies: [TASK-035, TASK-037]` (`:544`), TASK-035 (bump) 在 feature 分支 merge 前 (`:522`, `:527`); TASK-036 verification 加「`ls-remote refs/tags/v<NEXT>` 对象 SHA == 本地」(`:562`); 新增 TASK-041 主仓同步面含 i18n README ×3 + 架构文档 ×2 + CLAUDE.md 版本行 (`:564-584`), TASK-033 state-check 改依赖 TASK-041 (`:511`)。拓扑序脚本核 = 035→034→036→041→033→039→038, 与 `tasks.md:81` 括注及 yaml `:518` 注释逐字一致 |
| M-3 rule6_note 漏 TASK-007 / TASK-031 deps 漏 016 / 两份 note 不同文 | **已解决** | yaml `rule6_note` (`:39`) 点名 `TASK-001 / 002 / 003 / 004 / 005 / 007 / 008` 且写明「tasks.md 不复述本条 (单一来源)」; TASK-031 `dependencies` 含 TASK-016 (`:484`); `tasks.md:120-122` rule6_note 节只留指针 |
| m-1 `TASK-00A` 非数字 id / 编号乱序 / `est_hours` 字段名 | **已解决** (按 R1 聚合裁定) | id 改 `TASK-040` (`:84`), 38 个 id 全为 `TASK-{NNN}` 形 (脚本核零例外); 027..030 保留给 S2 并在 yaml `:7-8` 写明「编号不可变 … 激活时追加」; `est_hours` 沿仓内先例保留 (聚合 Minor 段记录) |
| m-2 TASK-003 行锚 `:958-971` 指错 | **已解决** | yaml `:140` 与 `tasks.md:44` 改为 `:1039` (实读 `tests/test_handoff_multibranch_collision_dedupe.py:1039` = `def test_owner_segment_participates_in_grouping_key`), `:305` 保留 (实读 = `test_both_latest_active_still_reports_self_multi_container`) |
| m-3 T12「Lab 内部指针决策单」路径 (`docs/decisions/` vs 实存 `.aria/decisions/`) | **已解决** | proposal v8 `:121` T12 改「Lab 内部指针已在 `.aria/decisions/` 决策单」; D2 段写「不另建 `docs/decisions/` 文件」; `tasks.md:3` 决策单链接指向 `.aria/decisions/2026-09-05-owner-container-identity-key-rulings.md` (文件存在) |

R1 处置三态计数: 已解决 6 / 部分 0 / 未处理 0。

## 机械核对结果 (全部通过)

- parent ↔ checkbox: 38 ↔ 38, 双向差集空, 无重复 parent / 重复 id; id 全为 `TASK-{NNN}` 数字形。
- 必需字段 (id / parent / title / status / complexity / est_hours / agent / dependencies / deliverables / verification) 38 条齐全; dependencies 全部指向存在的 TASK; DFS 无环。
- 工时逐条相加 = 82.5h; agent 计数 backend-architect 15 / qa-engineer 15 / knowledge-manager 8 = 38, 与 `metadata.agents` / `total_tasks: 38` 一致。
- tasks.md 头部 (`:3-8`) vs proposal v8 头部 (`:3-4`) / §Impact (`:104`) / SC-7 (`:132`): Level 3 / Status (v8 Approved; tasks v2) / ship target `<vNEXT>` 按 D5 / S1、S2 定义 (S2 = a1-entry B.2 已落地且 #174 ack) 一致。Scope 三 SHA: `git submodule status` = aria `7dd0135` (v1.69.1) / standards `cc864ee`; 主仓 `60808b2` = `03c6a9e` 的父提交 (v2 起草基线), 一致。
- 组 5 顺序: `tasks.md:81` 括注 (5.2 → 5.1 → 5.3 → 5.7 → 4.3 → 5.6 → 5.5) = yaml 拓扑序 (035→034→036→041→033→039→038), 一致; 5.4 (TASK-037) 为 034 的旁支前置, 不在线性链内, 合理。
- rule6_note: yaml 单一来源点名 001/002/003/004/005/007/008 = 五条 substitute 的承载任务 (SC-1: 001; SC-2: 002/005/007 三个全在; SC-3 S1: 008; SC-4: 003; SC-8: 004) 完整; TASK-031 verification (`:488`) 点名同一集合。
- S2 后续表 (`tasks.md:95-100`) vs yaml `s2_followup.items` (`:42-58`): S2-1 / S2-2 / S2-4 标题与验收逐字对应; S2-3 见下 m-3。激活规则 `tasks.md:102` vs yaml `:41`: 三条件 (0.1/TASK-000 判 S2-candidate 且 #174 ack 且 5.1/TASK-034 未执行) 与两分支后果 (追加 6.1–6.4 + TASK-027..030 接入 merge 前置 / 维持 S1 + D 期 Step 7 tracker issue, 先例 #192) 同义, 差异只在 id 记法 (checkbox 号 vs TASK 号) 与 tasks.md 多一句「handoff 记录激活时点」; proposal v8 `:104` 「满足激活条件 (S2-candidate + ack + merge 前) 时追加 6.x 任务; 否则 D 期以 tracker issue 记录 S2 后续 (先例 #192)」与之一致。
- SC ↔ 任务映射表 (`tasks.md:106-118`) vs yaml verification 的 SC 引用 (脚本抽取): SC-1 1.1 / SC-2 1.2+1.5+1.7 / SC-3 1.8 (S1 臂; S2 臂 = 后续表, yaml 无 SC-3 S2 承载任务, 与表一致) / SC-4 1.3 / SC-5 3.1-3.3 / SC-6 1.6 / SC-7 4.2+4.3 (含 plugin-cache-currency 例外, 与 proposal `:132` 同) / SC-8 1.4 / SC-9 1.11+3.4+3.5 / SC-10 1.9 / SC-11 1.10 —— 双向一致。yaml 里另有两处 SC 字样不在表内且属合理: TASK-031 (`:488`) 是留痕汇总非验收承载; TASK-040 (`:96`) 的「SC-3」指 a1-entry 的 SC-3 而非本 spec。
- 路径与外链: `.aria/decisions/…rulings.md` / `.aria/repro/handoff-tracks-frozen-2026-09-05.json` / `.aria/triage-comment.md` / `.aria/notes/` / `tests/run_tests.py` / `scripts/release_gate.py` / `lib/constants.py` / 五处取值文档 / `docs/architecture/version-scheme.md` / README ×3 i18n 全部存在; post_spec R1–R5 + post_planning R1 aggregated 六份在 `.aria/audit-reports/`; Forgejo API 实查 Aria#193 / #174 / #192 与 aria-plugin#135 均存在 (open)。
- state-check 面: `.aria/state-checks.yaml` 共 14 条全部 enabled, 「13 条全绿 + `plugin-cache-currency` 例外」= 14 计数吻合; TASK-041 verification 点名的 `m6-version-badge-match` / `i18n-readme-translation-currency` / `plugin-version-arch-docs-match` / `main-project-version-consistency` / `m6-claude-md-version` 五个 id 全部实存。
- v2 新改行锚全部命中: `collision.py:349` (`rec = track_to_claim_record(t)`) / `:63` / `:86` / `:143` / `:379-383`; `track_board.py:459-475` (kind 分支) / `:744` (`_dedupe_tracks_for_collision`) / `:783` (`_track_to_claim_record`) / `:412`; `handoff_multibranch.py:518` / `:709`; `identity.py:126` / `:222`; `phase1_gate.py:486`; `state-snapshot-schema.md:1085` (kind enum) / `:1109-1121` (aria-plugin#155 dedupe 段); `phase-1-collectors.md:75`; `RECOMMENDATION_RULES.md:31` (rule 1.54); `SKILL.md:149-154`; `templates/session-handoff.md:43` 含「设 label 使更可读」; standards `:116` / `:178` / `:186`; `_build_repo` 在 `:208`。
- 带圈数字 / 希腊字母: 两文件 grep 零命中。

## 审计结论

无 Critical, 无 Major。以下三条 Minor 均为 B 期顺手项, 不阻塞进入 B.1。

### Finding m-1 (Minor)
- type: text-residue / cross-doc
- severity: Minor
- category: proposal v8 S2 改写残留
- scope: `proposal.md:104` (§Impact 表「与 a1-entry 的边界与两种 ship 形态」行), `proposal.md:128` (SC-3)
- summary: v7→v8 把「由本 Spec 改写其 SC-3 为『…』」改成「SC-3 的 S2 臂不进本 cycle 验收」时, 原句尾的引文没删干净, 现读作「…SC-3 的 S2 臂不进本 cycle 验收 为「`get_container_uuid()` 与 flip 后 `get_container_id()` 同值; label 只在 `get_container_label()`」。」—— 「为「…」」成了无主语的孤儿片段。同表 SC-3 (`:128`) 「仅 S2」子句仍写「断言写在 tasks.md 的 T3 完成条件」, 而 v2 起 S2 项已不在 tasks.md checkbox (承载改为 S2 后续表 S2-2 行)。
- 为什么重要: `:104` 是 R1 C1 改法的 proposal 侧落点, 也是 B 期判 S2 激活时会引用的那句; 孤儿引文恰好是 a1-entry SC-3 的改写目标文本, 读者分不清它是「本 spec 承诺的改写文本」还是残句。`:128` 会让 D 期按字面去 tasks.md 找 T3 完成条件而找不到。
- 建议: `:104` 改为「…SC-3 的 S2 臂不进本 cycle 验收; 激活后由本 Spec 改写 a1-entry SC-3 为「`get_container_uuid()` 与 flip 后 `get_container_id()` 同值; label 只在 `get_container_label()`」」; `:128` 「断言写在 tasks.md 的 T3 完成条件」改「断言写在 tasks.md S2 后续表 S2-2 行 (激活后转 6.2 完成条件)」。

### Finding m-2 (Minor)
- type: dependency-completeness
- severity: Minor
- category: 组 0 与发布链的 DAG 边
- scope: `detailed-tasks.yaml:76` (TASK-000 deps), `:91` (TASK-040 deps), `:544` (TASK-034 deps), `:619` (TASK-038 deps)
- summary: 脚本核 TASK-034 (merge+tag) 的祖先集不含 TASK-000 / TASK-040 (TASK-040 无任何下游); TASK-038 (「#174 补 ship 结果」) 只依赖 TASK-039, 不依赖 TASK-040 (它要「补」的那条留言)。激活规则 (yaml `:41`) 的判定前提「TASK-000 判形态 + ack 已到 + TASK-034 未执行」在 DAG 里没有边保证 000/040 先于 034。
- 为什么重要: yaml 是 deps 的单一 SOT (`tasks.md:4`); 按 deps 调度时 000/040 是根节点、一般会最先跑, 所以 S1 ship 不受影响 —— 但「merge 前必须已判形态并已留言」这一顺序目前只靠 tasks.md 的组序与散文, 不靠机器可读的边; 若 B 期 000/040 被延后, S2 分支会静默塌回 S1 而无违约信号。
- 建议: TASK-034 `dependencies` 加 TASK-040 (传递含 000); TASK-038 `dependencies` 加 TASK-040。两条边, 不改编号不改工时。

### Finding m-3 (Minor)
- type: dual-layer-drift
- severity: Minor
- category: S2 后续表 vs `s2_followup.items`
- scope: `tasks.md:99` (S2-3 行「验收」列) vs `detailed-tasks.yaml:54` (TASK-029 verification)
- summary: 四项里唯一不逐字对应的一项: tasks.md S2-3 验收 = 「ack 留言 id 记录」; yaml = 「ack 留言 id 记录; 判据改为 get_container_uuid() 与 flip 后 get_container_id() 同值」。yaml 多出的后半句才是改写的实质判据。
- 为什么重要: 激活时 6.3 checkbox 会从 tasks.md 表行复制, 只带记录性子句、丢实质判据; 与 m-1 的 proposal 孤儿引文同源 (同一段文本三处三种形态)。
- 建议: tasks.md S2-3 验收列补「; 判据 = `get_container_uuid()` 与 flip 后 `get_container_id()` 同值」, 与 yaml 同文。

### 观察 (非 finding, 不计数)
- `tasks.md:77` 4.1 checkbox 仍列出五条 substitute 与七个任务号。这是任务标题需要自描述, 且集合与 yaml `rule6_note` 今日完全一致; 与 R1 M-3 的「两份不同文」不是同一性质。若要绝对单一来源, 可缩成「按 yaml `metadata.rule6_note` 点名任务集留痕」—— 可做可不做。
- `proposal.md:119` T10 仍写「state-scanner 全套 pytest」, 而 SC-7 (`:132`) 与 tasks 4.2 已改 `tests/run_tests.py` 为正规跑法、pytest 为备选。不矛盾 (pytest 仍可用), 只是 T10 措辞未跟上, 可与 m-1 一并顺手改。

## B 期顺手项 (随 PASS 附带, 不要求回炉)

1. m-1: proposal `:104` 孤儿引文 + `:128` 「tasks.md 的 T3 完成条件」措辞 (两处文本编辑)。
2. m-2: yaml 加两条边 TASK-034←TASK-040、TASK-038←TASK-040。
3. m-3: tasks.md S2-3 验收列补判据子句。
4. 观察项 T10 「pytest」措辞。

## Verdict

PASS (Critical 0 / Major 0 / Minor 3)

## Vote

PASS — R1 三条 Major 与三条 Minor 全部闭合且有 v2 证据; 双层 38↔38、工时 82.5h、agent 15/15/8、DAG 无环、组 5 拓扑序与括注一致、rule6_note 单一来源七任务齐全、S2 后续表 / 激活规则 / proposal §Impact 三处同义、SC 映射双向一致、引用路径 / issue / check 名全部实存。剩余三条 Minor 是文本残留与两条 DAG 边, B.1 起手顺手改即可, 不构成回炉理由。

## 轮次记录

- R1: PASS_WITH_WARNINGS (0C/3M/3m), vote REVISE。
- R2 (本轮): 实读 tasks.md 全文 (122 行) / detailed-tasks.yaml 全文 (625 行) / proposal v8 头部 + D2 / D4 / D5 / §Impact / Tasks / SC 段 / R1 本席报告 + 聚合全文; 脚本核 parent 双向 / 必需字段 / 工时 / agent 计数 / id 形 / DAG 无环 / 拓扑序 / SC 引用抽取 / TASK-034 祖先集; 实跑 `spec_complete.py --gate` (38/38 unchecked, 无杂散 checkbox); `git submodule status` 核三 SHA; 逐一 ls 引用路径; Forgejo API 实查四个 issue; 读 `.aria/state-checks.yaml` 核 14 条与五个 check id; 逐一 sed 核 v2 新改行锚 (`:1039` / `:349` / `:459-475` / `:744` / `:208` 等); 带圈数字 / 希腊字母 grep。未引用任何未实读行号。
