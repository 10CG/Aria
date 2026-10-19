# issue-groomer Tier B 定向 fixture 套件 (Rule #6 判据表第三行, 10CG/Aria#240)

> **任务来源**: `openspec/changes/issue-groomer-p1-mvp/detailed-tasks.yaml` TASK-011 (task 2.2)
> **范围**: 勘正后 #240 (comment 29237) — **仅 Tier B 语义行为**: 疑似已修判断 / 优先级 vs 在制轨 / owner 决策面抽取的可证伪用例。原 #240 body 三条移交附注中的 (1)「评论编辑用例」与 (2)「态分量变体」属 Tier A 机械 fixture 项, 已归 spec task 1.3 (SC-1), **不在本套件**。
> **被测对象**: issue-groomer SKILL.md 适配层的 Tier B 判断行为 (Step 2 三类语义判断 + Step 3 写入), 即「处方性 · AB 套件覆盖外」lane — 本套件是其 Rule #6 义务的落地形态。groom.py (Tier A 机械核) 的测试在 `aria/skills/issue-groomer/tests/`, 与本套件正交。
> **建套日**: 2026-10-19 | **语料快照基线**: 2026-10-18

---

## 1. 点名行为定义 (三)

行为键与输出面对齐 `aria/skills/issue-groomer/scripts/lib/incremental.py` 的 `ASSESSMENTS_SCHEMA_DOC` + 机读锚点常量 (`ASSESSMENTS_ENTRY_REQUIRED_KEYS` / `ASSESSMENTS_ENTRY_OPTIONAL_KEYS`, 引用勿手抄, 以常量为准)。

| # | 行为 | 判断问题 | 输入材料 | 输出 assessment 面 |
|---|------|----------|----------|--------------------|
| B1 | 疑似已修可关单 (`suspected_fixed`) | 该 open issue 是否已被某项已 ship 的工作解决而可关单? | issue 记录 + openspec archive spec 史 + git log 修复迹 + CHANGELOG/状态文档 | `suspected_fixed: {verdict: bool, rationale}` — verdict=true 须带可核对证据引用; 无修复迹 ⇒ verdict=false 或省略面, 不猜 |
| B2 | 优先级 vs 在制轨道 (`verdict_priorities`) | issue 隐含的优先级/方向是否与在制 spec / 分支冲突, 或已被在制轨覆盖/推迟? | issue 记录 + `openspec/changes/` 在制清单 + proposal 摘录 + 活跃分支 + handoff 在制轨记录 | `verdict_priorities: [{from, to, rationale}]` — 有在制关联 ⇒ 非空列表且 rationale 锚定在制 spec 标识; 无关联 ⇒ 省略面或不含在制引用 |
| B3 | owner 决策面抽取 (`owner_decisions`) | 哪些事项需要人裁 (无法由 AI 依现存材料定夺)? | 一组 issue 记录 (含「待 owner 裁定」形态: 轮换/排期/审阅/拍板/请确认类) + 项目约束 | `owner_decisions: [<决策条目 string>, ...]` — 每条含来源 issue 键 (SKILL.md Step 4 「每条注来源 issue 键」); 无决策形态 ⇒ 省略面 |

**总原则 (SKILL.md Step 2)**: 拿不准 = 不猜。某面判不出就省略该面 — `assessment` 面缺席是合法态。本套件的可证伪性正是围绕这条纪律设计: 正向用例钉「证据充分时必须判出」, 反向用例钉「证据不足/不存在时不得编造」。

## 2. 用例清单 (7 例 = 3 正向 + 3 反向 + 1 边界; 每行为 1 正向 + 1 反向, B1 另含边界例)

| case_id | 行为 | 极性 | 语料取材 | 核心可证伪锚点 |
|---------|------|------|----------|----------------|
| `B1-POS-1` | B1 | 正向 | Aria#211 真语料 + **全真实**修复迹 (archive spec / PR #215 / merge commit df3c274 / CLAUDE.md 状态行, 2026-10-19 冻结) | verdict===true 且 rationale 引用证据 token; 以「跟进项仍 open」为由判 false = fail |
| `B1-NEG-1` | B1 | 反向 | Aria#229 真语料 + 冻结检索结果 (archive 命中均早于 issue 创建且属不同 facet; git log 零修复迹) | verdict===false 或省略面; 真实干扰项 (同主题历史归档) 面前不得 false positive |
| `B1-EDGE-1` | B1 | 边界 | Aria#213 真语料 (含真实 body_head) + 同车道已 ship 证据 vs 显式「跟进 open」标记并存 | verdict===false (区分「车道机制已 ship」与「本条诉求未做」); 把相邻已 ship 误当本条已修 = fail |
| `B2-POS-1` | B2 | 正向 | aria-plugin#208 真语料 + 在制 spec `issue-groomer-p1-mvp` proposal 摘录 (明文「修 plugin#208」) | 非空 verdict_priorities 且 rationale 含 `issue-groomer-p1-mvp`; 引用无关在制 spec = fail |
| `B2-NEG-1` | B2 | 反向 | truffle-hound#10 真语料 + 冻结在制清单 (8 spec, 主题无一相关) | 省略面或零在制引用; 主张与任一在制 spec 的覆盖/冲突关系 = fail |
| `B3-POS-1` | B3 | 正向 | 批量 3 条: Aria#212 / Kairos#66 / 10cg.local#33 真语料 (title 逐字) + 构造示意 body (展开 title 已含的决策形态, 已注明) | 非空 owner_decisions, ≥2 条, 每条含来源 issue 键, Aria#212 必抽 |
| `B3-NEG-1` | B3 | 反向 | 批量 2 条: shenquant-data#3 / SilkNode#1207 真语料 (机械修复形态, 无决策面) | 两 entry 均不产出决策条目; 把机械修复升格为 owner 决策 = fail |

极性语义: **正向** = 证据充分, 判断必须命中; **反向** = 证据不存在, 判断必须克制 (不得编造); **边界** = 存在诱导性干扰证据, 判断必须不被带偏。

## 3. 用例文件结构

每用例一个 JSON, 字段:

- `case_id` / `behavior` / `behavior_label` / `polarity` — 定位与极性
- `source_annotation` — 语料取材声明: 哪些逐字取自真语料快照、哪些是冻结的真实仓摘录、哪些是构造示意 (构造内容仅展开 title 已含信息, 不引入新事实)
- `input.issues[]` — issue 记录, 字段形态对齐语料快照 (`repo` / `number` / `title` / `labels` / `created` / `updated`, 日期为 date-only; 附 `body_head` 时对齐 body-comments 快照的截断形态)
- `input.context_materials[]` — 判断的交叉参照材料 (冻结摘录: archive 检索结果 / git commit / 状态文档行 / 在制清单 / proposal 摘录), 均带 `kind` + 冻结日
- `expected.assessment_entry_exemplar` — 期望 assessment entry 形态 (对齐 `ASSESSMENTS_SCHEMA_DOC` 键): 语义面给到值级示例; 必填三键 (`provenance` / `created_at` / `context_key`) 只验在位与形状, 值随运行轮次, **不做值比对** (`context_key` 真实运行须逐字取评估轮 `groom-state.json` 的 `last_run.context_key`)
- `expected.rationale_anchor_tokens` (或 `must_contain_any_of`) — rationale 的逐字锚 token
- `verdict_rules.pass` / `fail` / `miss` — 判读规则; `miss` = 面省略在可判语境下记漏报 (非编造, 不计 fail 但不判绿)

## 4. 判读协议 (谁评 / 怎么判 / 何时跑)

**何时跑**:
1. issue-groomer SKILL.md 适配层判断指令 (Step 2 三类判断的定义 / 交叉参照材料 / 拿不准纪律) 变更时 — Rule #6 判据表第三行 lane 的定向回归;
2. assessment 语义面契约 (`ASSESSMENTS_ENTRY_OPTIONAL_KEYS` 三键的形态) 变更时;
3. #240 关单前全量跑一遍 (见 §5)。

**谁评**: 独立评估席, **不得由本轮变更作者自评** (自写实现+自评 = 自洽假绿; 席位纪律同 audit 对抗轮)。评估席可以是另一个 AI 会话或人。

**怎么判** (逐例三步):
1. **构造运行**: 将 `input` (issues + context_materials) 作为判断材料喂给被测适配层 (真实路径 = 跑 `groom.py` 后按 SKILL.md Step 2 对该组 issue 产 assessment; 演练路径 = 直接以 input 材料执行 Step 2 判断指令), 收集产出的 assessment entry。
2. **机械锚点核对** (可脚本辅助): 类型断言 (verdict===bool / 列表元素类型 / 面在位性) + token 逐字匹配 (`rationale_anchor_tokens`, 在制 spec id, 来源 issue 键) + 编造检测 (引用的 spec 名/PR 号/SHA/issue 键是否都在 input 材料中出现)。
3. **语义方向核对** (评估席判): 判断方向是否符合 `verdict_rules` (已修 vs 未修; 覆盖 vs 冲突 vs 无关联; 决策抽取 vs 过度抽取)。

**结果分级**: 每例 PASS / FAIL / MISS (miss 语义见 §3); 汇总 = 三行为各报 正/反/边界 通过数。任何 FAIL ⇒ 行为面回归, 修复后重跑; MISS ⇒ 判读能力缺口, 记录并要求处置 (不得静默放过)。

**记录去处**: 评估结果 (逐例判定 + 汇总) 记入当轮 `rule6_note` 的 Tier B 条目处置说明与 handoff; 本套件文件本身不改动 (fixture 是冻结材料, 判读结果不回写用例)。

## 5. 与 #240 关单条件对应

#240 按 Rule #6 判据表第三行要求三条件, 对应关系:

| #240 条件 | 落地物 |
|-----------|--------|
| 点名行为 | 本 README §1 三行为定义 (输入材料 → 判断 → 输出面, 键对齐 ASSESSMENTS_SCHEMA_DOC) |
| 可证伪定向 fixture | §2 用例清单 + 7 个用例 JSON (每行为 ≥2 例: 1 正向 + 1 反向; B1 另含边界例), 每例带判读锚点 |
| 缺口单跟踪 | 本单 (#240) 自身; 关单时序 = task 4.2 (spec ship 收尾) 随 Tier B fixture 完成关, 关单前按 §4.3 全量跑一遍并留判定记录 |

关单核验口径: 三条件齐备 + §4.3 全量跑零 FAIL (MISS 须有处置记录) ⇒ SC-6 第 (3) facet 判绿。

## 6. 语料来源与材料冻结纪律

- **issue 语料**: 三快照之一 `scratchpad/issues-open-full-18repos-2026-10-18.json` (378 条) 与 `issues-sample-body-comments-2026-10-18.json` (body_head 形态)。快照不复制入库; 再生成: `python3 aria/skills/issue-groomer/scripts/regen_corpus.py` (原位恢复加 `--date 2026-10-18`)。
- **上下文材料**: 各用例内嵌的 archive 检索结果 / git commit / CLAUDE.md 状态行 / 在制清单 / proposal 摘录均为 **2026-10-19 对真实仓的冻结摘录** (真实 SHA / 目录名 / 引文逐字)。它们是 fixture 的组成部分, **不随活仓漂移** — 活仓后续变化不影响本套件判定 (重放时以用例内材料为准, 不重新检索)。这是刻意设计: 可证伪锚点必须钉死在冻结材料上, 否则「证据漂移」会让反向用例翻转成正向。
- **真实活仓的对应关系变动时** (如 Aria#211 被关单): 不改本套件; 如需新增反映新状态的用例, 加新 case_id, 旧例保留 (历史回归基线)。
- **改造声明**: 逐字引用 vs 构造示意在每个用例的 `source_annotation` 中逐一注明。构造内容仅展开 title 已含信息, 不引入新事实。

## 7. 契约对齐注记

- entry 键集 = `ASSESSMENTS_ENTRY_REQUIRED_KEYS` (provenance / created_at / context_key, 必填) + `ASSESSMENTS_ENTRY_OPTIONAL_KEYS` (三语义面, 可选)。本套件 exemplar 采用 `ASSESSMENTS_SCHEMA_DOC` 示例的富形态: `suspected_fixed` 为 `{verdict, rationale}` 对象、`verdict_priorities` 为 `[{from, to, rationale}]` 列表。
- **文件面 vs 报告面**: 富形态在报告面被白名单类型投影省略属预期非缺陷 (`groom.py` `_project_assessment`: 报告面要求 `suspected_fixed` 为 bool / `verdict_priorities` 为 string / `owner_decisions` 为 string 列表, 类型不符整面省略 — 机械层不转语义)。本套件判读对象是**文件面** (`.aria/groom-assessments.json` 的 entry), 报告面投影行为属 Tier A 机械核测试范围 (tests/), 不在本套件。
- `owner_decisions` 文件面形态 = **string 列表** (唯一可投影进报告面的形态; `ASSESSMENTS_SCHEMA_DOC` 条目图示中的 `{...}` 为占位示意, 以 `_project_assessment` 的 `isinstance(od, list) and all str` 判据为准)。
- `provenance.model_id = None` 会使整条评估经复用门判 stale (fail-closed), 因此 exemplar 恒给具体 model_id 示例值。
