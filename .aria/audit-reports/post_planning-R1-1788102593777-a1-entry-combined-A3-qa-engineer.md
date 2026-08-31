---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-30T15:28:06.000Z
context: openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml (+ linked-issue-field-availability + sibling-spec-probe)
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
seat: A3-qa-engineer
critical_count: 1
major_count: 3
minor_count: 1
---

## 摘要

本席逐条核对三份 A.2/A.3 派生产物 (`a1-entry-claim-duplicate-work-guard` 39 任务 / `linked-issue-field-availability` 25 任务 / `sibling-spec-probe` 18 任务) 与各自 `proposal.md` Success Criteria 表「怎么会红」列的忠实度。方法: 亲读三份文件的 `tasks.md` + `detailed-tasks.yaml` 全文 (非抽样), 逐一 `ls`/`grep -n`/`python3` 亲验被引用的 file:line 与文件存在性, 用归档门解析器 (`aria/skills/state-scanner/scripts/lib/detailed_tasks.py::parse_detailed_tasks`) 实跑三份文件核验机械可消费性, 并对可疑处派 3 个并行 fork 复核 (各自独立盲跑, 互不知晓对方发现)。

**总体质量**: 三份派生产物在对抗夹具设计上质量很高——baseline-绿回归守卫 (SC-2/SC-15/SC-23/SC-29, sibling SC-1/SC-10/SC-21) 普遍把「删掉具体几行代码验证真的会红」写成显式验收步骤; SC-18 假阳性拒绝四臂的合成夹具第四臂被正确要求「必造」而非可选; SC-22 七要件 (含最易被简化掉的续行折叠 ⑦ 与 8 处 yaml 围栏定位 ⑤, 且正确处理了 proposal 自身「7 处」与实测「8 处」的偏差) 逐字进了验收条目; KELVIN SIGN 非 ASCII 折叠负控、哨兵集合封闭六分支、跨仓已知限 fail-soft skip 均落地正确; 三份文件归档门解析器实测均 `parse_ok=True` 且任务数与 `metadata.total_tasks` 逐一吻合 (39/25/18, 全 `pending`)。

**但发现 1 条 critical + 3 条 major，构成同一类系统性缺陷 (memory `fix-the-class`)**: **机读 `dependencies:` 拓扑图与散文声明的执行顺序不一致**，在三份文件中以两种形态各复发两次:

- **形态 A (critical, 仅 a1)**: Group 6 (SC-22/SC-34 等结构化文本测试) 的 `dependencies` 整体指向 Group 5 (对应的文档 GREEN 实现), 与 Group 2→3/4 正确示范的 RED-先于-GREEN 方向相反, 且与 TASK-025 自己 notes 里「RED-first」的声明直接矛盾。
- **形态 B (major ×2, a1 + sibling-spec-probe)**: 文件自陈的 Phase B.1 硬前置任务 (a1 TASK-001「Phase B.1 阻塞」/ sibling TASK-003「proposal :473 逐字『未 done 则不得开始』」) 未被编码进任何下游实现任务的 `dependencies` 字段, 只以散文 (`notes`/`metadata.phase_b1_preconditions`) 存在。
- 外加 linked-issue-field-availability 的 1 条同族但更局部的 major (单任务依赖遗漏, 有粗粒度 `execution_order` 兜底) 与 1 条 minor。

三处 `dependencies` 缺陷都不会导致最终交付漏 SC (机制最终仍会跑到、baseline 事实断言均真), 但会让「机读拓扑图是执行顺序权威来源」这条三份文件自己反复宣称的原则在局部失守——若下游执行体 (subagent-driven-development / task-planner 自动化) 严格按图行事而非按 tasks.md 散文行事, 会在错误的时点开始工作。

## Findings

| id | severity | category | scope | type | 描述 |
|---|---|---|---|---|---|
| bd55ab9c | critical | testing | openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml | issue | Group 6 结构化测试 (TASK-025~030) 全体 `dependencies` 指向对应 Group 5 GREEN 实现任务, RED-先于-GREEN 顺序反转, 红窗形同虚设 |
| c23f47ce | major | testing | openspec/changes/linked-issue-field-availability/detailed-tasks.yaml | issue | TASK-007 (GREEN) 的 `dependencies` 缺 TASK-006, 但自身 verification 引用 TASK-006 矩阵作为验收依据 |
| 98e71a6a | major | architecture | openspec/changes/sibling-spec-probe/detailed-tasks.yaml | issue | Phase B.1 硬前置 TASK-003 (proposal `:473` 逐字) 未编码进任何下游任务 `dependencies`, 只以散文 `metadata.phase_b1_preconditions` 存在 |
| 3221f943 | major | architecture | openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml | issue | Phase B.1 硬前置 TASK-001 (自称「任一条不成立 ⇒ Phase B.1 阻塞」) 未编码进 Group 2 起点任务 TASK-004 的 `dependencies` |
| b0e8b171 | minor | documentation | openspec/changes/a1-entry-claim-duplicate-work-guard/detailed-tasks.yaml | documentation | rule6_note 自称「12-hunk 表」但全文无显式可数的 12 行对照表, 只能靠通读散文枚举推出 |

### bd55ab9c — Group 6 GREEN→RED 倒序, 红窗形同虚设 (critical)

**证据** (本席亲验 + fork 独立复核一致):

- `detailed-tasks.yaml:675` TASK-025 `dependencies: [TASK-017, TASK-018]` — TASK-017/018 (`:503`/`:528`) 是 Group 5 的 `phase-a-planner/SKILL.md`・`spec-drafter/SKILL.md` **GREEN 文本实现**任务, agent 均为 `knowledge-manager`。
- 同款: TASK-026 `:697` `deps:[TASK-019]`、TASK-027 `:715` `deps:[TASK-022]`、TASK-028 `:734` `deps:[TASK-021]`、TASK-029 `:752` `deps:[TASK-023]`、TASK-030 `:770` `deps:[TASK-020, TASK-021]` — Group 6 全部 6 条测试任务 `dependencies` 无一例外指向自己所验证文本的 Group 5 实现任务。
- 对照组: 同文件 Group 2 (代码层 TDD) 正确示范反方向——TASK-004~010 (RED, `deps:[TASK-003]`) 先行, TASK-011~016 (GREEN) 反过来 `deps` 指回对应 RED 任务 (如 `:383` TASK-011 `deps:[TASK-004]`)。Group 6 与此镜像相反。
- `tasks.md:26` 明写组间顺序「1→2→3/4→**5→6**→7→8」, 即文本实现 (5) 先于文本测试 (6), 与代码层「2 先于 3/4」方向相反——不是孤立的 YAML 疏漏, 而是本文件设计的既定组序。
- TASK-025 `notes` (`:686`) 自称「RED-first: 断言在 TASK-017/018 落文本前于 d69091d 跑一次全红并留痕」, 与自己的 `dependencies` 字段直接矛盾——按 dependencies 语义 (Group 2/3/4 已验证过的语义), 任何遵图执行的 subagent-driven-development 都会先跑完 TASK-017/018 再开始 TASK-025, 届时 SKILL.md 已含目标文本, 测试写出即绿, SC-22 ①–⑦ 的负控 (塞进 `## 相关文档`、只列参数子串无命令行、缺 ③ 等) 永远不会被真正观察到"必红"。
- TASK-026~030 甚至没写"RED-first"这句免责声明, 只是把当下 `grep` 得到的"baseline 必红"事实当断言依据, 可证伪性更弱。

**影响**: SC-22 (本 Spec 单条断言要件最多的 SC, 7 要件 + 续行折叠 + 8 处围栏定位) 与 SC-34 及 4 条 rule6_note substitute 测试的「红窗证明」在按图执行的路径上不可实现。

**处方**: 把 Group 6 拆成「文本层 RED」(逻辑不变, `dependencies` 只指向 Group 1 非文本前置如 TASK-003/014/016/022 等) 与 Group 5「文本层 GREEN」, 并让 Group 5 反过来 `depends_on` 对应 RED 任务 (镜像 TASK-011 `deps:[TASK-004]` 的模式); 同步把 tasks.md 组序改为「…3/4 → 6(RED) → 5(GREEN) → 7 → 8」。

### c23f47ce — TASK-007 verification 引用未声明依赖 (major)

`detailed-tasks.yaml:229` TASK-007 `dependencies: [TASK-001, TASK-002]`, 但 `:233` verification 第一条写「TASK-006 矩阵: 好实现全对、每夹具至少一坏实现被拒」——TASK-006 (`:205` `dependencies: [TASK-001, TASK-002, TASK-003, TASK-004]`) 不在 TASK-007 的依赖表里。顺序目前只靠粗粒度 `execution_order.phase_1_red_and_probe.then: [TASK-006]` (`:664-667`) 兜底, 与细粒度 `dependencies` 图不一致。**处方**: TASK-007 的 `dependencies` 补 `TASK-006`。

### 98e71a6a — sibling-spec-probe B.1 硬前置门缺可执行宿主 (major)

`detailed-tasks.yaml:34` `ordering_note` 自陈「执行顺序以 dependencies 拓扑为准」, 但全文 `dependencies:` 列表中只有 `:516` TASK-017 (Group 5 AB 实跑) 引用了 TASK-003; Group 2 起点 TASK-004 (`:194`) `dependencies: [TASK-001, TASK-002]` 不含 TASK-003。`metadata.phase_b1_preconditions` (`:35-38`) 不是本仓 task-planner (`aria/skills/task-planner/SKILL.md:197`) 识别的 schema 字段, `grep -rn phase_b1_preconditions .` 在本文件外零命中。对照组: 同文件另一条硬前置 TASK-001 (姊妹模块存在性) **正确**编码进了 TASK-004 依赖 (`:194` 含 `TASK-001`)。**处方**: 给 TASK-004 (及一切不经 TASK-004 传递依赖的 Group 2/3/4 起点任务) 的 `dependencies` 补 `TASK-003`。

### 3221f943 — a1-entry TASK-001 B.1 硬前置门同样缺可执行宿主 (major)

与 98e71a6a 同构, 本席独立发现: `detailed-tasks.yaml:115-141` TASK-001 (`--no-push` 已在双远端 + 主仓 gitlink 一致) `dependencies: []` (`:124`), 其 verification 末条 (`:141`) 逐字「任一条不成立 ⇒ Phase B.1 阻塞, 回 owner (闸门状态 #7); 不得以「差一个 commit」自行放行」——明确是全 Phase B.1 的硬阻断门。但 Group 2 起点 TASK-004 (`:229`) `dependencies: [TASK-003]`, 不含 TASK-001; 全文 `dependencies:` 列表中 TASK-001 只出现在 Group 7 的 AB 任务里 (`:791` TASK-031 `[TASK-001, TASK-017, TASK-025]` 等 5 条)。若按 `dependencies` 图严格调度, Group 2~6 的全部实现工作可以在 TASK-001 尚未验证通过时就开始。**处方**: 与 c23f47ce/98e71a6a 同一处方——把 TASK-001 加入 TASK-004 (及其余不经 TASK-004 传递依赖 TASK-001 的 Group 2/3/4/5/6 起点任务) 的 `dependencies`。

### b0e8b171 — rule6_note「12-hunk」不可独立核验 (minor)

`detailed-tasks.yaml:98-104` rule6_note 提及「12-hunk 表」但只有散文枚举 (照跑 4 类套件 + 覆盖外 4 fixture + issue 1 + substitute 5, 口径有重叠计数), 未给出显式 12 行对照表。数字本身经核对站得住, 但复核者需重新通读枚举才能验证「12」是否准确。**处方**: 补一张 12 行显式对照表 (hunk → 处置类别 → TASK 编号)。

## 实测记录

- 归档门解析器实跑三份文件: `parse_detailed_tasks()` 均 `parse_ok=True`, 任务数 39/25/18 且状态全 `pending`, 与 `metadata.total_tasks` 逐一吻合, 缩进/`tasks:` 顶层键/`- id:` 边界对本机制均兼容。
- 亲验多处 file:line 引用准确性 (与 aria 子模块 `d69091d` HEAD 逐字比对): `lib/identity.py:191/222`、`lib/collision.py:268/272-273/278-279`、`lib/claim_lifecycle.py:377/425-427`、`phase-a-planner/SKILL.md` 内 ` ```yaml` 围栏计数实测 8 处 (proposal SC-22⑤ 写「7 处」, detailed-tasks.yaml TASK-003/017/025 均正确记录该偏差并改用锚点定位而非计数定位, 未受影响)。
- `.aria/state-checks.yaml` 实测 12 条 (linked-issue-field-availability TASK-011「12→13」准确); `test_linked_issue_field.py` / `.aria/linked-issue-field-grandfathered.txt` / `aria/skills/audit-engine/{scripts,tests,lib,collectors}` 均确认当前不存在, 与三份文件「新建」标注一致。
- `git symbolic-ref refs/remotes/github/HEAD` 实测 exit 128、`refs/remotes/probe` 实测为陈旧 tracking ref (`remote.probe.url` 未配置) — 与 sibling-spec-probe SC-12/SC-14「本仓实况」逐字一致。
- KELVIN SIGN (U+212A) 非 ASCII 折叠负控 (`linked-issue-field-availability/detailed-tasks.yaml:100`)、`is_sentinel` 直测正负例矩阵 (`:126`) 均落地准确, 与 proposal O-5/6i 裁定一致。
- 跨 Spec 接口一致性: linked-issue-field-availability A.2 新增 additive 字段 `bad_elements` (`:48`) 被 sibling-spec-probe 的 `metadata.external_dependencies.token_str_nullability` (`:50`) 正确同步引用, 未见 split-makes-seams 形状的接缝缺陷。
- RED/GREEN agent 分派核对: a1 (TASK-004~010 qa-engineer → TASK-011~016 backend-architect)、linked-issue-field-availability (TASK-001~006 qa-engineer → TASK-007~011 backend-architect)、sibling-spec-probe (TASK-004~009 qa-engineer → TASK-010~014 backend-architect) 均无 RED+GREEN 同任务同 agent 吞并红窗的先例形状复发 (仅 Group 6/TASK-025 系列本身是「依赖方向」问题, 非「同任务同 agent」问题)。
- 三份文件各自 SC→TASK 覆盖表核对: linked-issue-field-availability 10/10、sibling-spec-probe 21/21 均声明「未覆盖: 无」且经抽样核实无虚报; a1 未见显式覆盖表但 39 任务逐条核对未见 SC 遗漏。
- 本审计由主控亲读三份文件全文 (每份 tasks.md + detailed-tasks.yaml 逐行过) + 3 个并行 fork 盲跑复核; 三个 fork 与主控各自独立发现的 finding 有重叠 (Group 6 由 fork1+主控独立确认; TASK-007 由 fork2+主控独立确认; TASK-003 B.1 门由 fork3 独立发现, 主控验证后确认; TASK-001 B.1 门为主控独立发现, 未被任一 fork 提及, 系比对 fork3 发现后类比排查所得)。

## Verdict

**FAIL** (1 critical, 3 major, 1 minor) — critical 项 (Group 6 红窗形同虚设) 直接命中审计纪律「按此执行会漏 SC / 红窗形同虚设」判据, 单条即可决定 verdict。3 条 major 均属同一系统性模式 (机读 `dependencies` 拓扑与散文声明的执行顺序不一致), 建议执笔席在处理 critical 项时一并处理, 而非逐条零散打补丁——四条 finding 共享同一处方形状 (把散文里已经写明的顺序关系显式翻译成 `dependencies` 边)。

## Vote

**REVISE**
