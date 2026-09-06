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
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R2 — owner-container-identity-key-and-collision-parser — knowledge-manager 席

> 审计对象: `tasks.md` (6 组 38 checkbox + 「S2 后续」表) / `detailed-tasks.yaml` (38 TASK + `metadata.s2_followup`) @ commit `03c6a9e`, 对照 `proposal.md` v8。镜头: 组 3 文档任务与知识链终检 (标准仓 CHANGELOG 惯例 / S1 兜底 tracker 机制 / issue 回帖措辞 / `.aria/notes/` 用法 / CLAUDE.md 同步面完整性)。全部结论基于本轮实读 (`standards/conventions/session-handoff.md`、`aria/skills/openspec-archive/SKILL.md`、`git log -p -- CLAUDE.md`、`.aria/state-checks.yaml`、`.aria/notes/`)。

## R1 处置核对

| R1 finding (knowledge-manager 席) | v2 处置 | 三态 |
|---|---|---|
| Major-1 — 决策单落点矛盾 (proposal/T12 写 `docs/decisions/`, 实存 `.aria/decisions/…rulings.md`) | proposal v8 §D2 (:43) 改为「已落主仓决策单 `.aria/decisions/2026-09-05-owner-container-identity-key-rulings.md`, 不进 standards (不另建 `docs/decisions/` 文件)」; `tasks.md:3` 头部引用同一路径; 全文 `grep -rn "docs/decisions" tasks.md detailed-tasks.yaml` 零命中 | **resolved** |
| Major-2 — `state-snapshot-schema.md` 只锁 `:1085`, 漏 `:1109-1121` 旧 dedupe 语义段 | `detailed-tasks.yaml` TASK-024 deliverables 第 4 行明列「`:1085` collision 段 + `identity_advisories` additive; **`:1109-1121` dedupe 语义段改写**」 | **resolved** |
| Major-3 — `phase-1-collectors.md:75` 无具体编辑指令 | TASK-024 deliverables 第 5 行「`:75` 加一句 (三态语义 + `identity_advisories`)」, 具体度与同任务内 `RECOMMENDATION_RULES.md:31` 的「加 `identity_advisories` 句」持平; SC-9 (proposal:134) 判据 (token 交集非空 + 上下文同义人工核) 对两文件适用同一标准 | **resolved** |
| Major-4 — TASK-038 issue 回帖托付「D 期」但 `phase-d-closer` 无此职责 (执行方缺口) | `tasks.md:87` (5.5) 改「**5.6 merge 后、归档前由执笔容器执行**」; yaml TASK-038 `dependencies: [TASK-039]`, 边界表 (`tasks.md:19`) 不再把此动作算进 Phase D | **resolved** (执行方缺口已补; 但**文案内容本身**新出现 S1/S2 未分档问题, 见下方新 finding, 不算 R1 该条的重开) |
| Major-5 — `deferred-s2` 归档机制不存在, S1 形态组 6 四项触发归档 Step 1 默认 BLOCK | 组 6 整体移出 `tasks.md` checkbox 与 yaml `tasks[]`, 改 `metadata.s2_followup` (非 checkbox); 激活规则三条件 AND；未激活 ⇒ 声称「D 期 Step 7 用既有 tracker 机制开 issue」 | **resolved (BLOCK 风险消除), 但兜底承载本身经本轮实读证伪 —— 见下方新 finding, 与 tech-lead R2 M-1 同源独立复现** |

三态计数: **resolved 5 / partially 0 / not_resolved 0**（其中 2 条「resolved」在解决原问题的同时打开了新的知识链缺口, 计入本轮新 finding, 不计入 R1 条目本身的重开）。

## 审计结论

### Major-A — S1 兜底「D 期 Step 7 用既有 tracker 机制」并非实际存在的机制; 干净归档时该 Step 完全不产出

`tasks.md:102` (激活规则末句) 与 `detailed-tasks.yaml:41` (`metadata.s2_followup.activation`) 都写: 三条件不满足 ⇒「维持 S1, D 期 Step 7 用既有 tracker 机制开 issue 记录 S2 后续 (先例 sibling-spec-probe #192)」。proposal v8 `:104` 同文。

实读 `aria/skills/openspec-archive/SKILL.md`:

- `:272-276`: 「phase-d-closer D.2 检出 deferred/unverified 后**委托**本 Step … `d_payload` 由 lib 聚合 "tasks.md 未勾选项 + carry-forward 注释, 或 (tasks.md 缺失时) detailed-tasks.yaml 非-done status 项 + carry-forward 注释" (deferred) 与 "全部 unverified_claims" … **干净归档 (无 deferred 且无 unverified) → `d_payload=null` → 本 Step 完全跳过, 不产生任何输出**」。

「S2 后续」表 (`tasks.md` 「## S2 后续 (非 checkbox; 激活规则见下)」) 与 `metadata.s2_followup.items` (`id_reserved`/`parent_reserved` 字段, 非 `id`/`parent`, 刻意不落入 `tasks:` 数组) **不是** `d_payload` 聚合逻辑读取的任何一个输入集合的成员: 它既不是 tasks.md 的未勾选 checkbox (它是一张 markdown 表格, 不含 `- [ ]` 语法), 也不是 yaml `tasks[]` 里的非-done status 项 (它压根不在 `tasks[]` 里), 也不属于 gate 探针产出的 `unverified_claims` (那是符号 liveness 探针的独立产物, 与「计划外文本表」无关)。

S1 形态下 38 个主任务全部 `[x]`, 若无其他原因触发 `unverified_claims` 非空, `d_payload=null`, Step 7 一行不跑, S2 后续表随归档目录一并搬进 `openspec/archive/`, 但**没有任何消费方会再读归档目录里的旧 Spec 文件去找「S2 后续」**。即: 声称的「兜底」在干净归档路径上是空话, C-1 (R1 Critical, 组 6 触发 BLOCK) 从「必撞墙的硬失败」换成了「S2 后续静默消失的软失败」, 后者对知识连续性 (AI-DDD 的核心诉求 —— 文档驱动开发、文档是单一真相源) 的破坏更隐蔽, 因为它不产生任何可见信号。

先例引用有误配: `sibling-spec-probe #192` 是由 `verdict=warn` (符号 liveness `ambiguous`) 触发的 unverified-claims tracker, 内容是「符号引用形态未分类」类文本 —— 与「把一张计划外的后续任务表登记进 issue」是完全不同的两件事; 即使本 Spec 恰好因 `aaaa1111`/`identity_advisories`/`cross_owner` 等符号被判 `ambiguous` 而触发一次 warn tracker (这属偶然, 不是设计出的承载), 该 issue 正文也不会提及 S2 的四项后续 (S2-1..4)。

此发现与 tech-lead 本轮 M-1 独立复现一致 (各自实读同一 `SKILL.md` 段落得出同一结论), 加固了「需要真正的承载体, 而非文字上的『既有机制』」这一判断。

**建议**: 二选一, 且需同步改掉 `tasks.md:102` / yaml `:41` / `proposal.md:104` 里「用既有 tracker 机制」这句不成立的措辞:
(a) 把「S1 归档前开一个具名 S2 后续 tracker issue (标题/正文点名 S2-1..4 四项)」写成 TASK-038 (5.5, 已在 merge 后、归档前执行) 的一条新增 verification 子句 —— 它已是本 cycle 内、由执笔容器执行的 issue 动作宿主, 零新增任务;
(b) 单列一条 5.8 checkbox 任务, 显式承载「S1 时创建/更新 S2 tracker issue」, verification 直接点名 S2-1..4。

### Major-B — TASK-038「#135 留缺口 1/2」文案在 S1 形态下超报, 与 proposal 自陈的「结构性消除只在 S2 形态成立」矛盾

`detailed-tasks.yaml:623-624` (TASK-038 verification) 与 `tasks.md:87` (5.5) 均无条件写: 「#193 关闭; **#135 留缺口 1/2**」——字面含义是 aria-plugin#135 的缺口 3 (本 Spec 的处置对象) 已完全闭合, 只剩缺口 1/2 未处理。

但 proposal v8 `:19` 定义缺口 3 = 「container 段来源不稳 … `get_container_id()` 是 `label if label else uuid` … 填个可读名就静默换了协调身份」(即「label 陷阱」), `:101` (§Impact Positive 条件式行) 明文: 「**label 陷阱结构性消除只在 S2 形态成立**; S1 形态下 label 形态既无 flip 也无 ⚪ (⚪ 只对 uuid key), 只有 T3b 的 inventory 告警」。

也就是说: S1 ship (a1-entry 未落地时的默认路径, `tasks.md:8` 明写「S1 = a1-entry 未落地时 ship」) 下, 缺口 3 只是**部分闭合** —— 解析器/身份键/判定/advisory 三层根因已修, 但 label 陷阱本体 (`get_container_id()` label 优先) 仍在生产路径上, 只多了一条不抑制的 inventory 告警。TASK-038 现有文案若原样发到 aria-plugin#135, 会让采用方误以为整条缺口 3 已经收口, 后续若因 label 陷阱复现 `claim_not_found` (即 08-13 那类事故), 排查者会先被这条回帖的措辞误导。

`.aria/triage-comment.md` 是外向且难回收的动作 (关闭 issue + 公开留言), 一旦按 S1 无条件措辞发出, 事后更正的成本 (需要二次留言澄清) 远高于起草时按 `ship_shape` 分档。

**建议**: TASK-038 verification 按 `metadata.ship_shape` 分两档:
- S2 已激活并 ship: 维持现文案「#135 留缺口 1/2」;
- S1 ship (默认路径): 文案须显式写明「#135 缺口 3 **部分闭合** (解析/身份键/判定/advisory 已修; `get_container_id()` label 优先仍在生产路径, 见 S2 后续 tracker #<n> —— 需配合上述 Major-A 的承载体一并落地); 缺口 1/2 未处理」, 不使用「留缺口 1/2」这一暗示「缺口 3 已收口」的简写。
- `#193` (本身是纯解析器 bug, 三层根因均已修) 是否直接关闭不受此影响, 可维持现文案。

### Major-C — TASK-022「变更说明落节末小段」与 `session-handoff.md` 全文 3/3 既有惯例 (Added/Purpose/Status 头部 blockquote) 不一致

实读 `standards/conventions/session-handoff.md` 全部三处「本节由某 Spec 新增/变更」的既有标注 (`grep -n "Added\*\*\|^> \*\*"`):

- `:103-106` (§2.3 头部): `> **Added**: 2026-05-19 by OpenSpec \`multi-terminal-coordination\` Phase 1.1 …` / `> **Purpose**: …` / `> **Status**: additive …` —— 紧贴 `## 2.3` 标题正下方。
- `:219-221` (§2.3.8 头部): `> **Added**: 2026-07 by OpenSpec \`interactive-session-dedup-coordination\` …` / `> **Purpose**: …` / `> **Status**: additive …` —— 紧贴 `#### 2.3.8` 标题正下方。
- `:230` 区 (§2.3.7 头部): `> 本小节是 **content enforcement**…` —— 同样紧贴标题正下方。

三处 100% 一致的模式: 「本节因某 Spec 而生 / 而变」的元注记, 统一采用「标题正下方 blockquote (`> **Added/Purpose/Status**: …`)」, **无一例外**放在小节**开头**, 没有任何一处放在小节**末尾**。

`detailed-tasks.yaml` TASK-022 deliverables (`:414`) 却要求「`:178-186` + **节末**「变更说明 2026-09-05」小段」, `tasks.md:69` 同文。这与全文 3/3 的既有惯例方向相反: 读者按既有心智模型 (「小节头部找变更来源」) 找 §2.3.5 的变更说明会扑空, 需要往下翻过整张判据表才能在结尾发现它——对一份被本 Spec 自己列为「single source of truth」候选、且明确要求「判据用标准自身定义的词写」 (proposal `:40`) 的规范文件, 这种反直觉的放置方式会成为下一次 OpenSpec 变更 (若照抄 TASK-022 的先例) 复制传播的新惯例, 属知识架构一致性问题, 落在本席「Documentation Quality Control」职责内。

`standards` 无 CHANGELOG 因此「变更说明需要一个落点」这个前提本身成立, 问题只在**放哪**, 不在**要不要写**。

**建议**: TASK-022 deliverables 改为「`:178-186` 判据表三行改写 + 新鲜度截止句 **+ 紧贴 `### 2.3.5` 标题正下方新增 `> **Changed**: 2026-09-05 by OpenSpec \`owner-container-identity-key-and-collision-parser\` — 判据表实质变更 (旧版按 \`owner\`/\`container-id\` 而非 \`identity_key\`; 对采用方是行为变更, 看板输出会改变)` blockquote」, 与既有 3 处同构; verification 里的「变更说明段存在」判据改为「紧贴 `### 2.3.5` 标题的 blockquote 存在且以 `> **Changed**:` 起始」。

### Major-D — TASK-041 (CLAUDE.md 同步) 范围排除 `:139`, 与连续 14+ 次发布 100% 同步该行的既有实践相反, 且无任何机械 check 兜底

`detailed-tasks.yaml:582` (TASK-041 deliverables) 对 CLAUDE.md 只写: 「`CLAUDE.md`  「版本: 插件 aria-plugin vX」一行, **项目状态段其余不动** (claude-md-hygiene)」——只覆盖当前 `:141` 一行, 显式排除 `:139` (「aria-plugin 方法论轨: v1.52.0–v1.69.1 已 ship — 逐版本史见 aria/CHANGELOG.md (SOT)」)。

`git log -p --follow -- CLAUDE.md` 实读: 从 `v1.66.1` 到 `v1.69.1` 之间**全部 12 次**版本 bump 提交, `:139` 与 `:141` 的版本号**逐次同步改动, 无一例外** (含最近两次: `2a46d08` v1.69.0 与 `6b840f5` v1.69.1)。多条 commit message 本身直接点名 「`CLAUDE.md :139/:141`」 为同一同步单元 (如 `42f0292` / `086ee32` / `057acfa8` / `01dab46` / `de75443`)。`main-project-version-consistency` 探针 (`.aria/probes/main-project-version-consistency.py`) 与 `m6-claude-md-version` check 都只核对 CLAUDE.md 的**其他**字段 (分别是 `:141` 里的「主项目 v…」子串与文件顶部 `> **版本**: 2.0.0`), 两者均不涉及 `:139` 的版本区间端点。`.aria/state-checks.yaml:297-305` 自身注释已承认「既有两条 version check … 也只比插件版本 ⇒ 主项目漂移在机械层完全不可见」, 而 `:139` 这条 aria-plugin 版本区间端点连一条"比插件版本"的既有 check 都没有覆盖到——它是纯人工维护面。

若 TASK-041 按现文案执行, ship 后 `:139` 会停留在旧版本号 (如仍写 `v1.52.0–v1.69.1`), 与同一段落 `:141` 刚更新的新版本号并列出现, 造成 CLAUDE.md「项目状态」段 (本席审计范围内的核心知识资产之一) 内部自相矛盾, 且**不会触发任何一条已启用的 state-check** —— 与 CLAUDE.md 顶部「项目状态」块自身的维护规矩 (「写入前读我: 本段覆写非追加」, `claude-md-hygiene.md §2.4`) 并不冲突 (更新一个既有覆写行内的版本号字面量, 不是新增 changelog/流水), 单纯是 TASK-041 的覆盖面写窄了。

**建议**: TASK-041 deliverables 的 CLAUDE.md 一项改为「`CLAUDE.md`  `:139` 版本区间端点 (`v1.52.0–vX`) 与 `:141` 「版本: 插件 aria-plugin vX」两处同步更新为新版本号, 项目状态段其余叙事不动 (claude-md-hygiene)」, 与连续 12 次的既有实践对齐。

## 确认无越界 / 无新问题项

- **组 3 (TASK-021~026) 与 proposal D2/D4/D5 映射**: 逐条核对, §2.3.1 (TASK-021) / §2.3.5 (TASK-022, 内容层面) / §2.3.9 (TASK-023, 含反向 grep 锁 `/home/` `Aether` 等 Lab 私有 token) / 六处消费文档+模板 (TASK-024+025, 七处口径与 proposal「七处」吻合, SKILL.md 显式「不改动」计入其一) / CHANGELOG (TASK-026) 均有对应任务且路径可实读定位; 内容覆盖面本身无缺失 (Major-C 是**放置位置**问题, 非内容缺失)。
- **`.aria/notes/` 用法一致性 (TASK-040)**: 实读目录 22 个既有文件, 命名一律 `YYYY-MM-DD-<slug>.md` (或纯 `<slug>.md`), 内容涵盖研究笔记/决策队列/复核记录/issue-triage 草稿等多种「session 内部工作产物」; `.aria/notes/2026-09-05-174-comment-draft.md` 命名与用途 (issue 留言草案) 与既有 `issue-triage-2026-05-19.md` 同类先例一致, 不构成越界。
- **S2 激活时点的 handoff 记录要求**: 已写入 `tasks.md:102` (「并在 handoff 记录激活时点」), 但未绑定到任何一个具体 TASK 的 verification —— 因激活本身是**追加** 6.1-6.4 + TASK-027..030 的动态行为, 现有固定任务集在写作时无法预先绑定一个尚不存在的未来任务; 判定为**已有文字承载但缺机械抓手**, 严重度不足以列 Major (定级: minor, 见下)。

## Minor

- TASK-040 附近 (`tasks.md` 「S2 后续」表激活规则句): S2 激活时「在 handoff 记录激活时点」目前只是散文承诺, 未绑定进 TASK-027..030 的 `verification` 模板 (`detailed-tasks.yaml:40-58` `s2_followup.items`)。建议: 激活规则追加的 6.1 (TASK-027) verification 增补一句「激活时点/证据 (0.1 结论 + #174 ack comment id) 已写入本 cycle 或次 cycle handoff」, 使其在激活动作发生时天然带上。不阻断本轮开工。

## Verdict

PASS_WITH_WARNINGS

## Vote

REVISE

## 轮次记录

- Round 1 (knowledge-manager 席, `60808b2`): Critical 0 / Major 5 / Minor 0, 投 PASS (五席聚合仍因 tech-lead/code-reviewer 的 2 Critical 判 FAIL → rework v2)。
- Round 2 (本轮, knowledge-manager 席, `03c6a9e`): R1 五条 Major 三态核验 = **resolved 5 / partially 0 / not_resolved 0**, 但其中 2 条 (Major-4 执行方缺口 / Major-5 归档 BLOCK) 的**解决手法本身**在本轮实读中被证实留下新缺口, 已作为独立 finding 重新列出 (Major-A 对应旧 Major-5 的兜底承载缺失, 与 tech-lead 本轮 M-1 独立复现一致; Major-B 对应旧 Major-4 的回帖内容准确性)。另新增 2 条本轮首次发现的知识架构问题: Major-C (`session-handoff.md` 变更说明放置位置与全文 3/3 既有惯例相反) / Major-D (CLAUDE.md `:139` 同步面漏项, 与连续 12 次既有实践相反且无机械 check 兜底)。Critical 0, Major 4, Minor 1。投 REVISE — 四条 Major 均为定点编辑 (改措辞/补 verification 子句/调整 deliverables 覆盖面), 不动 DAG 骨架、不改任务编号, 预计 R3 可收敛。
