---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-10T17:22:00.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
---

# post_spec 聚合审计报告 — pre-merge-completeness-gate-change-scope (Round 4)

本文件由汇总引擎席产出, 合并本轮 5/5 席位的结构化结论。五份单席报告原文逐字落盘于同目录 `post_spec-R4-2026-09-10T172200-000Z-R4-pre-merge-completeness-gate-change-scope-{role}.md` (role ∈ tech-lead / backend-architect / qa-engineer / code-reviewer / knowledge-manager)。五份 frontmatter 均 15 字段齐全, **0 份需补齐**; `round_incomplete: false`, `skipped_agents: []`。

**合并规则 (与 Round 1 / Round 2 / Round 3 同一套, 供 Round 5 复算对齐)**:

1. 按 `{category, scope}` 匹配, 语义同、写法异的合并为一条; `found_by` 列全部提出席位, `severity` 取最高。
2. `category` / `type` 席位间不一致时取多数标注; 平票取席位序在先者 (顺序: tech-lead → backend-architect → qa-engineer → code-reviewer → knowledge-manager)。每处不一致均在条目内注明原始标注。
3. 同 scope 的**矛盾**意见 (结论相反, 非同一缺陷的不同 severity) 保留双方并标 `conflicted: true`, 汇总席**不裁决**。**本轮 conflicted 对 = 0** (逐对核过: qa-engineer 的 SC-2 选样不可满足与 code-reviewer 的 SC-2 采样可行性在事实上一致 —— 两席都点名同一候选 `state-scanner-inter-cycle-surfacing` (F-a 2 / F-b 3), 前者记「正文未点名 ⇒ Phase B 无指引」, 后者记「放宽后有真语料 ⇒ 规则 (c) 不必退化成自造样本」, 互补非互斥)。
4. `scope` 语义不同则不合并 —— 即使锚在同一节 (本轮据此保留了 §1.4 格 B 的三条、§1.1 S2 的两条、SC-13 的两条、SC-2 的三条各自独立)。
5. `finding id` = `sha256("{category}:{scope}:{severity}:{type}")[:8]`, scope 取归一写法 (trim + 折叠空白 + ASCII 小写), 用 python3 实算 (40 条全部唯一, 无碰撞)。
6. 席位 `### Decisions` / `### Risks` 有条目只在报告正文出现、未进结构化清单时一并纳入 (Round 1-3 先例)。**本轮命中 1 条**: tech-lead 正文的第二条 risk (`66737069`, SKILL.md 与 execution-modes.md 同字面调用串无相等性断言) 不在其结构化清单内, 依本规则纳入并在条目内注明。
7. 一条单席 finding 同时载有两个不同 scope 的论断时, 分别计入两条合并条目的 `found_by` 并互相点名; 去重前计数仍按单席原始条目数计。**本轮命中**: backend-architect / qa-engineer / knowledge-manager 三席把「Level 解析统计复算」写在其他 decision 条目内, 依本规则一并计入 `edaf86a1` 的 `found_by`。

**汇总席本轮的机械复算** (只读复核, 不改变任何 finding 的 severity 与处置; 本席未编辑任何仓库文件):

- **Level 分布 (本轮唯一的数字分歧, 四席同判)**: 汇总席按 proposal `:180-181` 三条判据独立实现解析器 (整文件扫描 + 文档序第一条 + 行首 `>`/`-`/`#`/空白/`*` 剥离 + `Level`|`Spec Level` + 可选 `**` + ASCII/全角冒号 + 取值前剥 `~~…~~`), 对 `openspec/{changes,archive}/*/proposal.md` **153** 份实跑: **剥删除线 ⇒ L3 58 / L2 85 / L1 1; 不剥 ⇒ L3 57 / L2 86 / L1 1**; 两跑唯一取值不同的文件是 `openspec/archive/2026-08-16-premerge-gate-branch-existence` (2 → 3, 真字段行 `> **Spec Level**: ~~2 (proposal only)~~ → **3**`)。另: 解析失败 **9** 份 (与 proposal 点名清单逐份同集)、首命中 >15 恰 **7** 份 (最深 `2026-09-06-a1-entry-claim-duplicate-work-guard` L58)、行首形态 **139/3/2/0**、含 `Spec Level` **15** —— 除分布外全部命中。⇒ backend-architect / qa-engineer / code-reviewer / knowledge-manager 四席的 58/85 与「逐个相同为假」**实测成立**, proposal `:184` 两句均须订正。
- **TL 三条单席 Major 的前提逐条复核, 全部成立**: (a) `config-loader/DEFAULTS.json` 实测 `audit.mode="adaptive"` · `adaptive_rules={level_1:"off", level_2:"convergence", level_3:"challenge"}` · `checkpoints` 八键全 `"off"`; (b) `phase-c-integrator/SKILL.md:132` 逐字「检查 audit.checkpoints.pre_merge — "off" 则跳过」(:131 为 `audit.enabled` 早退); (c) 本 spec 目录 `ls` 结果**只有 `proposal.md`**, 实跑 `spec_complete.py --gate` 得 `{"complete": false, "verdict": "pass", "blocking_reasons": [], "unverified_claims": [], "d_payload": null}`, 代码 `:1642` 逐字「两文件皆缺 (proposal-only) → 维持 v1.54.0 designed 零评估早退」。
- **CR 的 AB 绑定陈述复核, 逐字成立**: `ab-suite/phase-c-integrator-pre-merge-gate.json` 实读 8 条 `test_case_in_unit_tests` —— `GateCheckTests.*` **4 条** (green / wait / fail / NEG-1-malformed); `NEG-4-no-run-for-branch` → `test_pre_merge_gate.NotFoundVerdictTests.test_sc2_trigger_matched_message`; `NEG-3-internal-error-surface` → `test_path_coverage.InternalErrorReasonTests.test_internal_error_has_own_reason`; `wait_then_green` → `test_gate_state_helper polling tests + integration`; `NEG-2-timeout` → `test_pre_merge_gate (timeout path; integration scenario)` (**无可执行 node id**)。`type=workflow_skill_subextension`, 无 `evals` 键, 8 fixtures。
- **KM 的 config 枚举复核, 成立**: `.aria/config.json` 实测 `audit.enabled=true` · `mode="convergence"` · `checkpoints` **7 键** (`post_spec`/`post_planning`=convergence, 其余 off), **无 `mid_post_spec`**, 无 `adaptive_rules`, 无两个 `allow_*` 键。
- **SC-13 切片与先例锚两条复核**: `execution-modes.md` 围栏实测 **`:34` 开 / `:66` 闭**, Step 1-5 分别在 `:37`/`:41`/`:46`/`:54`/`:63` —— 五个 Step 全在**同一个**围栏内, 不存在「Step 4 的围栏块」⇒ qa-engineer 与 knowledge-manager 的结论一致 (KM 的 `:34-66` 行号精确; QA 写的「`:23` 开」起点差 11 行 —— `:21` 是上一个围栏的闭合行, 不影响结论)。`execution-modes.md:152` 逐字含「(机械护栏 SC-17 计数恰 2)」⇒ code-reviewer 判 proposal `:347` 的勘正注写反**成立**。

---

## 审计结论

### Critical (0)

本轮无 Critical。R3 的三条 Critical (`2d7cccbe` / `7877bac6` / `34507656`) 经五席各自独立复核, **修法全部落在判据本体而非批注** (见 `ad5f1f6d`), 且落地文本经复算基本成立; 本轮无一条新缺陷构成「方案错误 / 破坏消费方 / SC 恒绿导致假绿」。

### Major (14)

- `b2bc13a6` [major] implementation/§1.3 判据 2 的实跑校准段 (Level 分布 57/86 实为 58/85, 「取值逐个相同」为假) — **found_by: backend-architect, qa-engineer, code-reviewer, knowledge-manager (4/5)**
  本轮唯一的 4 席共识缺陷, 也是**勘正自身引入的事实错误**。`:181` 判据 2 新增「取值前先剥掉 `~~…~~` 删除线片段」(R3 执笔席自验项 A2), 但紧接着 `:184` 的「本轮对真实语料的实跑校准 (可复现)」给的是 **L3 57 / L2 86 / L1 1** —— 四席各自写解析器实跑得 **58 / 85 / 1**, 关掉剥离才回到 57/86/1, 差的那份正是判据 2 自己举的唯一样本 `openspec/archive/2026-08-16-premerge-gate-branch-existence/proposal.md:29`。同段「另实跑『严格判据 vs 原稿宽松正则』逐份对照, 144 份取值**逐个相同**, 判据收窄未引入取值漂移」因此同为假: 该份宽正则在 `:13` 的叙述句上先命中取 2, 严判据落到 `:29` 剥线后取 3。**汇总席已独立复算确认** (见文首)。后果不是恒绿而是**反向消歧**: knowledge-manager / qa-engineer 均指出 Phase B 为对上 57/86 可能删掉剥离子规则, 把 SC-20(4) 要防的「静默取错 adaptive 档位」放回来; code-reviewer 记 SC-20(4) 会兜住故未升 Critical。
  *category 分歧注*: backend-architect / code-reviewer 记 implementation, qa-engineer / knowledge-manager 记 documentation ⇒ 2:2 平票, 按席位序取 backend-architect 的 implementation。

- `955907f2` [major] architecture/§1.4 格 B 的 enabled_by 前置条件 (空集全称真空成立 / 按意图读则三格穷举失败) — **found_by: tech-lead, backend-architect, knowledge-manager (3/5)**
  R3 修 Critical `7877bac6` 时新写的守卫。逐字是「纳入集空 **且** 该空集的每一项 `enabled_by` 都是 `explicit` / `manual-default` / `adaptive:level_{N}` 之一」—— 空集上全称谓词**真空成立**, 该合取项恒真, 三席一致判其按字面实现零效力 (knowledge-manager: 真正封口的是级 3 改判 `config_unreadable` exit 2, 该前置只是装饰; 同 memory `feedback_universal_predicate_vacuous_truth_on_empty_set`)。若按括注意图读成「每个**被解析**的 checkpoint 的 `enabled_by`」, backend-architect 给出可达反例: config `{enabled:true, mode:"convergence", 四个非排除项显式 "off"}` —— 纳入集空 ⇒ 四个排除项走级 2b 得 `convergence` ∉ 允许集 ⇒ 格 B 假; `resolved(pre_merge)="convergence"` ≠ off ⇒ 格 C 假; `enabled=true` ⇒ 格 A 假 ⇒ **三格穷举失败, 行为未定义** (tech-lead 同判「条件为假时空集三格无覆盖分支」)。两读法均无 SC 区分 (SC-15(3) 的格 B fixture 用场景 A 全 explicit, SC-15(5) 纳入集非空)。
  *severity 分歧注*: backend-architect 记 major, tech-lead / knowledge-manager 记 minor ⇒ 按规则 1 取最高 major。*category 分歧注*: tech-lead 记 implementation, backend-architect / knowledge-manager 记 architecture ⇒ 取多数 architecture。

- `a657bf0a` [major] implementation/§1.1 S2/S3 求值序 vs SC-7 (no_spec_contradicted 同仓格不可达) — **found_by: qa-engineer, knowledge-manager (2/5)**
  §1.1 声明 `S1 → S4 first-match` (`:105`), S2 命中任何 `openspec/changes/<id>/` 前缀的 diff 路径 (`:110`), 而 S3 的前置是「S2 为空 **且** `--no-spec`」(`:111`)。同仓格下 `--diff-repo-path` 缺省 = `--repo-path`、`--anchor-base` 缺省 = `--base` ⇒ 两个 diff 面同一份 ⇒ 「`--no-spec` 且 diff 触 change 目录」必然先被 S2 吃掉并返回 `scope_source=diff`, S3(iii) 的矛盾检测**永不求值** ⇒ SC-7 (`:341`) 断言的 exit 2 `no_spec_contradicted` 在同仓 fixture 上结构不可达, 只有 SC-17(4) 的跨仓格 (子模块内无 `openspec/`) 碰巧可达。两席同判两个分支都坏: Phase B 照 §1.1 实现 ⇒ SC-7 必红; 为满足 SC-7 把矛盾检测提到 S2 之前 ⇒ 改变已定的 first-match 契约与 §1.0 P2。qa-engineer 另指这与 R3 刚修的 minor `d081c6d9` 是**同一个失效**(「first-match 静默吞掉 `--no-spec`」) 只封了 argparse 那一半, 且待 owner 复议 #2 对该守卫残余强度的估价建立在「单仓可达」的前提上。

- `f637d129` [major] architecture/§1.4 格 B/格 C 分格 × adaptive 档 Level 1 (落格 C exit 2 硬阻与 :226/:283 的「仍 pass」互斥) — **found_by: tech-lead (1/5)**
  代入实算: adaptive 档 Level 1 时 `resolved(pre_merge) = adaptive_rules.level_1 = "off"` ⇒ 纳入集空 ⇒ 格 B 的 `resolved(pre_merge) != "off"` 前置不成立 ⇒ 落**格 C** `pre_merge_not_enabled` exit 2 + 消费方 fail-closed = 硬阻, 两个 `allow_*` 都不救; 而 `:226` 与 `:283` 把该人群列为格 B「仍 pass」, `:111` 又承诺 `--no-spec` 把全部 checkpoint 判 `not_applicable`。`:226` 的括注 (「Level 1 通常走 `--no-spec`/S3, 那条路在 P2 就把全部 checkpoint 判 `not_applicable`, 不到本格」) 与 §1.0 自钉的总序冲突 —— 三态在 P6、空集分格在 P5、S3 在 P2 只产出 `scope_source`。结果随采用方 config 翻转: 任一 checkpoint explicit 非 off (官方场景 C) ⇒ pass; 全 adaptive 推导 (场景 B) ⇒ 同一输入变 exit 2。无 SC 覆盖 (SC-7 未钉 `audit.mode`, 与 §1.0 末段「每份 fixture 必须显式钉 mode」相撞)。tech-lead 另指待 owner 复议 #8 的人群依据**第三次偏移** (R2 场景 A/B → R3 移出场景 B → 本轮新补的第 3 类实际落格 C)。**汇总席已复核 DEFAULTS.json 的 `level_1="off"`**, 该代入前提成立。
  *与 `955907f2` 的关系*: 同锚 §1.4 格 B, 但一条争的是 `enabled_by` 全称谓词的效力, 一条争的是 adaptive Level 1 人群落哪一格, 依规则 4 不合并。

- `bb0e565f` [major] architecture/§3 调用方接缝 — phase-c-integrator 步骤 3 的 pre_merge 解析语义未对齐 — **found_by: tech-lead (1/5)**
  门侧 Step 3 已被两轮 Critical 钉成优先级链 (`checkpoints` 显式 > `adaptive_rules` > off), 调用方守卫仍是对 config-loader **合并视图**的字面键判断: `phase-c-integrator/SKILL.md:132` 逐字「检查 `audit.checkpoints.pre_merge` — "off" 则跳过」, 而 `config-loader/SKILL.md:28` 第 5 步会把未写的 `pre_merge` 用 DEFAULTS 填成 `"off"` (**汇总席已实读复核两处**)。字面读法 ⇒ 官方场景 B/C 的采用方在步骤 3 早退, **门根本不被调用** ⇒ §5 第 7 条声称的行为变更 (adaptive_rules 推导的 checkpoint 首次进入校验面) 在生产路径不可达, SC-20(1)(2) 与 SC-15(5) 全是直调 fixture 测不到这一层; 链读法 (调用方也改成优先级链) ⇒ `f637d129` 的 adaptive Level 1 硬阻立刻变生产可达。两个读法各击穿本 spec 的一条声称, 而 §1.4 `:220` 恰恰把「调用方守卫」当作格 A/格 C「生产不可达」的论证前提。§3 只在步骤 4/4.5 加参数与三态处置, Tasks 无任何一项对齐步骤 2/3。

- `4cbe35ce` [major] testing/SC-12 的归档门 liveness 断言恒绿 (F7 落点, proposal-only 零评估早退) — **found_by: tech-lead (1/5)**
  本 spec 目录只有 `proposal.md` (无 `tasks.md` / `detailed-tasks.yaml`), 实跑 `spec_complete.py --gate <本 spec 目录>` 得 `verdict=pass` 且零符号分类 —— 代码 `:1642` 是「两文件皆缺 (proposal-only) → designed 零评估早退」, 符号分类器根本不运行 ⇒ SC-12 的「归档门判 `completeness_gate.py` alive、无 dead-code block」**结构上不可能红**; F7 (`:56`) 写的后果句「否则 D.2 判 dead-code」对本 cycle 不成立, 真正守住「调用行落 fenced bash 块」的只有 SC-13 的分块 grep。**汇总席已实跑复核** (ls + `--gate` + `:1642` 逐字)。处置二选一: 改成对合成的**带 tasks.md** spec 目录跑 `--gate` 的可证伪形态, 或删该子句并把 F7 落点明确改挂 SC-13。
  *与 `aebd2f9f` 的关系*: 该 risk (Level 2 定级) 是本条的**上游成因** (proposal-only 使归档门 liveness 轴结构性不运行), 但一条是 SC 可证伪性、一条是定级, scope 不同, 依规则 4 不合并; 两条建议一并处置。

- `01b9faf6` [major] implementation/§1.0 P3 Level 取法 eager 与 §1.3:186 / §5:286 的 lazy 表述互斥 — **found_by: backend-architect (1/5)**
  §1.0 P3 (`:98`) 逐字「逐 change 解析 Level N (§1.3)」, 依赖只有 P2、排在 P4 之前 = **eager**; 而 `:186` 的 ERROR 文案给的第二个 fix (「在 `audit.checkpoints` 里显式写该 checkpoint」) 只有 **lazy** 才有效, `:286` §5 第 6 条同样限定「`mode="adaptive"` 且某 checkpoint 无显式值时」才读 proposal 取 Level, `:103` 的 fixture 硬约束 (2) 也只要求 adaptive 档 fixture 补 Level 行 —— 三处不能同真。若 Phase B 照 P3 字面实现 eager, SC-8 (`mode:'manual'` + 显式 checkpoints, 未要求 Level 行) / SC-16 / SC-9(1)(2)(3) 这批 fixture 全落 `spec_level_undetermined` exit 2, 与各自期望冲突 = 与 R3 已判 major `3f817a3b` 同型的「Phase B 结构性必红」。生产面同样可达: 本仓四个非排除 checkpoint 全显式 ⇒ Level 永不被消费, 但 eager 下只要被审 change 的 proposal 无可解析 Level 行 (真实语料 **9/153**) 即硬阻, 且文案给的 fix 无效。建议改「按需解析 (仅当某对落到级 2a 时)」并同步 `:103` —— 循环依赖不因此复活 (Level 来源是 proposal.md, 与 `resolved_mode` 无环)。

- `a00c52bb` [major] architecture/§1.1 S2 作用域解析面仍绑 diff 面 (跨仓 scope_source=diff 结构不可达) — **found_by: backend-architect (1/5)**
  R3 把 S3 的核验面移到锚点仓 (`:84`, 理由「Rule #5 规定 spec 落主仓, `openspec/changes/**` 的家本来就在锚点仓」), 但同一条理由未同步给 S2 —— S2 (`:110`) 未另行指定仓 ⇒ 用 `--diff-repo-path` + `--base`。该席实测 `aria/openspec` 与 `aria/.aria` **均不存在** ⇒ 子模块 PR (自述主力场景 `:82`) 下 diff 面永远取不到 `openspec/changes/<id>/` 前缀 ⇒ S2 恒空, `scope_source=diff` 在主力场景结构不可达; 连带 S4 (`:111`) ERROR 文案的第二个 fix (「在分支里带上 change 目录变更」) 在跨仓形态不可执行。SC-5(5) 的 fixture 注已顺带承认这一点, 但那不是契约、也无 SC 断言。建议 S2 改取锚点面 (或锚点面优先、diff 面兜底) 并补一条跨仓无 `--change-id` 的 SC; 若刻意保留现状, 须把「跨仓下 S2 恒空、必须显式传 `--change-id`」写成契约并改 S4 文案。
  *与 `a657bf0a` 的关系*: 两条都锚 §1.1 S2, 但一条是「S2 抢在 S3 前面命中」(同仓), 一条是「S2 在跨仓恒空」, 失效方向相反, 依规则 4 不合并 —— 且两条合看正说明 S2 的解析面选择本身尚未定稿。

- `b451a016` [major] testing/§1.0 P1 无条件前置 vs §1.4 格 A + 十条 SC fixture 缺 enabled: true — **found_by: qa-engineer (1/5)**
  §1.0 P1 (`:96`) 逐字把「`audit.enabled != true` ⇒ `audit_not_enabled` exit 2」提为**无条件前置**并注明「刻意排在作用域之前」, 而 §1.4 该表仍挂在「**纳入集为空**: 按成因分三格」标题之下 (`:220`) ⇒ 同一文档两种合法读法。差别是承重的: SC-1 / SC-3 / SC-4 / SC-5 / SC-6 / SC-8 / SC-16 / SC-17 / SC-19 / SC-22 的 fixture config **字面都没有 `enabled: true`** (只有逐字引用官方场景 A/B/C 的那几条自带该键) ⇒ 按 P1 读法这十条一律先落 `audit_not_enabled` exit 2, 与各自期望的 exit 0/1 直接冲突; 而 §1.0 末段的两条 fixture 硬约束 (`:103`) 只钉了 `audit.mode` 与 Level 行, Tasks 的「既有 SC fixture 前提全量回扫」(`:316`) 也只列这两条 + 作用域, **`enabled` 这一格无任何任务承接**。

- `2370f1f9` [major] testing/Tasks B.0 仲裁规则结构性剔空 SC-2 的 legacy / unattributed 两族 — **found_by: qa-engineer (1/5)**
  R3 为修 major `affceac8` 新钉的 B.0 无人值守机械仲裁, 反过来把 SC-2 依赖的语料族剔空。规则 (b) 逐字「两列不一致 **或** 第一列取不到 ⇒ 该文件整份剔出 SC-2/SC-4 的 fixture 样本池……不是供人裁, 是当场剔除」(`:313`); 但第一列的两个来源 (frontmatter `context:`/`spec_id:`/`change_id:`, 或写盘时刻活跃 change 目录的 git 历史) **只能产出一个 change_id**, 而 F-e (真 legacy) 与 F-f (unattributed) 两族的正确标注按定义就是 `legacy` / `unattributed` ⇒ 两列恒不一致, 全族被剔。实测佐证: 6 份 legacy 里 3 份带 `context:` 字段, 170 份 unattributed 里 **106** 份带指向真 change 的独立字段, 其余第一列取不到 —— 两条通道都落进规则 (b)。规则 (c) 的兜底 (「换 id 重新采样, 换不到则该族降为 ≥1 份」) 在 0 样本时无解且明写「不得为了凑数把争议条目放回去」⇒ 无人值守的 Phase B 在这两族上没有任何合法动作; 而 SC-4 的「两个计数分离」正是 R1 Critical-1 的封口, 失去真实语料样本后只剩手造名字, B.0 想防的自指恒绿以更软形态回来。

- `95ddb322` [major] testing/两条 R3 新增规范条款零 SC 承接 (--change-id×--no-spec 互斥 / 逐对不叉乘) — **found_by: qa-engineer (1/5)**
  R3 为修两条 minor 新写的规范条款没有断言承接: (1) `--change-id` 与 `--no-spec` argparse 互斥 + exit 2 + 指定文案 (`:87`, 修 `d081c6d9`); (2)「迭代口径 = 逐对, 不是叉乘」并明写「不得被实现读成并集 × 全部 change_id —— 那会对本该 off 的那一对判 missing 假红」(`:190`, 修 `d3eeec78`)。SC-1~SC-22 全表对这两条**零断言** (该席 grep: `叉乘` 0 命中; `互斥` 的 2 处命中是 SC-10 / SC-13 里描述断言互斥的行, 与 argparse 无关)。第 2 条被误读的后果正是混合 Level 多 change PR 上的假红阻断合并 —— 本 spec 反复钉的失效族。

- `29c39e2c` [major] testing/Rule #6 替代面: phase-c-integrator-pre-merge-gate.json 8 条 fixture 绑定陈述为假 — **found_by: code-reviewer (1/5)**
  文中四处 (`:12` 头部 Rule #6 行 / `:324` Tasks AB / `:348` SC-14(a) / `:362` rule6_note) 均称「8 条 `fixtures[]` **每条**带 `test_case_in_unit_tests` 指向 `test_pre_merge_gate.GateCheckTests.*`」, 并据此把动作定义为单条 `python3 -m unittest test_pre_merge_gate.GateCheckTests`。**汇总席已逐条实读该 json 复核**: 仅 4/8 指向 `GateCheckTests`; `NEG-4` → `NotFoundVerdictTests`, `NEG-3` → `test_path_coverage.InternalErrorReasonTests` (另一模块), `wait_then_green` → `test_gate_state_helper` (实际在 workflow-runner/tests, 跨 skill), `NEG-2-timeout` **无可执行 node id**。⇒ (a) 事实陈述为假; (b) 规定的命令只覆盖 4/8, SC-14(a)「8 条 fixture 对应用例全绿」按字面不可执行; (c) 待 owner 复议 #9 的裁决依据建立在这句假陈述上。修法: 按实际拆成三条命令, 并把 `NEG-2` / `wait_then_green` 两条无可执行绑定显式记为该 catalog 自身的缺口。
  *与 `c623a2d2` 的关系*: knowledge-manager 的 decision 核的是 Rule #6 **档位取法**与 SOT 判据表对账 (成立), 本条核的是**替代面的事实陈述**, 两者不矛盾、scope 不同。

- `7127ab68` [major] architecture/§1.1 S3(ii) no_spec_unverifiable 在跨仓 Level 1 的无逃生口硬阻 — **found_by: code-reviewer (1/5)**
  `:84` 规定 `--no-spec` 的核验面**恒取锚点仓**, `:111` S3(ii) 规定锚点面 `len(diff)==0` ⇒ `no_spec_unverifiable` exit 2 不放行, `:114` 明示该 error **不被** `allow_incomplete_checkpoints` 豁免 (`allow_dangling_change_ids` 也不覆盖)。但自述「子模块 PR 正是 pre_merge 的主力场景」(`:82`), 而 **Level 1 周期按定义无 spec ⇒ 主仓侧通常没有伴随提交** ⇒ 锚点面 diff 结构性为 0 行 ⇒ 该格必然触发, 消费方 fail-closed + `on_fail: 阻塞合并` 且两个 owner 旗标都救不了 —— 与 R2 判 Critical 的 `fdb30703`「无逃生口硬阻」同结构 (方向 fail-closed 且人群更窄, 该席据此记 major)。另: `:280-288` 自称穷举的八条行为变更未含这条新增硬阻, `:298` R-b 只讨论残余假绿未提该假红面。修法二选一 (属放行面变更, 宜列 owner 裁): 把「锚点仓零 diff」与「diff 非空但不触 change 目录」分开, 前者降 `[WARN]` 继续评估; 或保持硬阻但显式挂一个既有旗标 (并入复议 #10), 同时补进 §5 与 SC-17 跨仓格。
  *与 `f637d129` / `a00c52bb` 的关系*: 三条都落在「跨仓 / Level 1 这批人群被硬阻或被放行」的同一面上, 但分别锚 §1.4 三格 / §1.1 S2 / §1.1 S3(ii), 依规则 4 各自独立; **建议 Phase B 一并消歧**, 否则改一处会推翻另一处的前提。

- `8acafe0a` [major] architecture/§2/§4/Tasks 的 audit-engine 输入声明面 vs §3 调用方实传五参数 — **found_by: knowledge-manager (1/5)**
  Rule #3 接口两侧不对账: §2 (`:250`) / §4 同步表 (`:265`) / Tasks (`:320`) 三处一致只给 `audit-engine/SKILL.md:49-54` 加 `change_id` 一项, 而 §3 (`:257`) 要求 pre_hook 追加 `change_id` / `repo_path` / `diff_repo_path` / `base` / `anchor_base` **五项** ⇒ 四个参数由调用方传出却在被调方零声明。这四项不能由 audit-engine 自行推导: `--base` 无缺省且契约要求远程跟踪 ref (`:86`, 缺失即 argparse exit 2), `--diff-repo-path` 按定义只有调用方知道 (`:81`) ⇒ §1 bash 块里的 `<主仓 root>` / `<C.2 合并目标仓 root>` / `<main_branch>` 三个占位无声明来源, 编排者只能猜; 猜错 `base` 的后果本文 R-h 已自证是假红阻断合并。同族漂移: Tasks `:321` 仍写三项旧清单, 漏 `base` / `anchor_base` —— 与 §3 自己刚补的「原稿接线三行漏了 `--base`, 照抄会直接红」同型复发。
  *与 `642c9e5e` 的关系*: 该 minor 是同一根因在**调用模板**上的表现 (`:74-78` 漏 `--anchor-base`), scope 不同不合并, 但同属「R3 加参数未回灌全部面」, 建议一次清扫。

### Minor (15)

- `7b17ada9` [minor] testing/SC-1 / SC-22(2) 输出通道残留 (stdout 文案与 15 键封闭 JSON 不可同绿) — **found_by: tech-lead, backend-architect (2/5)**
  §1.4 (`:238`) 已钉「全部 `[OK]`/`[INFO]`/`[WARN]`/ERROR 走 stderr, stdout 恒且仅恒一个 JSON」并要求「全部 SC 里 stdout 含文案的断言一律改到 stderr」, SC-5 与 SC-15(3) 已改, **SC-1 (`:335`) 仍写「stderr/stdout 文案含 `post_implementation@x`」** —— 该拼接串在 15 键封闭 JSON 里没有任何字段承载 (`checkpoint` 与 `change_id` 是两个字段), 合取读法下与 SC-10 不可同绿。backend-architect 另补一处: SC-22(2) (`:356`) 仍用 R3 后已不再是被定义通道名的「trail」措辞, 建议逐字改 stderr 并与 `:230` 的 WARN 全文对齐。

- `d9578e5d` [minor] testing/SC-13「execution-modes.md Step 4 的围栏块切片」边界未定义 — **found_by: qa-engineer, knowledge-manager (2/5)**
  SC-13 (`:347`) 要求「只在 Step 4 的围栏块切片内」计数字面串 `scripts/completeness_gate.py` 恰 1, 但 SOT 里 Step 1-5 全在**同一个**围栏内 (**汇总席实测 `:34` 开 / `:66` 闭, Step 4 占 `:54-61`**) ⇒ 不存在「Step 4 的围栏块」, 切片起止无定义, 两个合法实现 (按 `Step 4:`~`Step 5:` 文本切 vs 按整块切) 判决不同 —— 一条自称零裁量的机械护栏本身可判决相反。两席各给一条消歧路径: qa-engineer 建议改「以 `Step 4:` 行起、`Step 5:` 行止的行区间内恰 1」; knowledge-manager 指先例 `archive/2026-09-04-sibling-spec-probe/proposal.md:513` 锁的是**按小节**的围栏块切片, 可直接照搬。

- `642c9e5e` [minor] documentation/§1 调用块 (:74-78) 漏 --anchor-base — **found_by: tech-lead (1/5)**
  R3 为修 Critical `34507656` 新增的 `--anchor-base` 没有回灌调用模板, 而 §3 (`:257`) 要求调用方传 `anchor_base`、Tasks (`:318`) 要求 argparse 实现它。该模板正是 Phase B 逐字写进 `audit-engine/SKILL.md` fenced bash 块与 `execution-modes.md` 的那一份、也是 SC-13 计数的对象 ⇒ 照抄即缺参数名。与 `8acafe0a` 同根。

- `aebd2f9f` [minor] architecture/Spec Level 2 声明 vs 实际范围 (交付面偏 Level 3) — **found_by: tech-lead (1/5)** · risk
  交付面 = 新增可执行脚本 + 重写闸门 Step 3-5 + 两个新输入参数 + 15 键 stdout 契约 + 22 条 SC + 八条采用方行为变更 (含两条配置行为反转) + 10 个 owner 复议项, 版本推荐 MINOR; 对照 `standards/openspec/project.md:114-118` (Level 2 = 中型 1-3 天 / Level 3 = 架构变更, 输出含 `tasks.md`) 更贴 Level 3。附带效应即 `4cbe35ce`: proposal-only 使归档门 liveness 轴结构性不运行。**不建议 AI 自行改判**, 建议并入待 owner 复议 (Rule #10)。

- `66737069` [minor] documentation/SKILL.md 与 execution-modes.md 两份同字面调用串无相等性断言 — **found_by: tech-lead (1/5)** · risk · *依合并规则 6 从正文纳入 (不在该席结构化清单内)*
  §1 要求两处同字面, SC-13 只做**分块计数**不做**两侧比对**。本仓已有一条 enabled 机械闸 (`.aria/state-checks.yaml` `skill-md-sha-backlink-literal-sync`) 正是为同类「跨文件手工同步字面串」漂移而立, 其 description 自述 2026-09-06 实测已漂移 ⇒ 该风险在本仓有实证前科。低成本缓解: SC-13 加一条两侧切片逐字相等的断言。

- `d1da3190` [minor] documentation/§5 行为变更枚举漏「门首次引入 git 依赖」硬阻一类 — **found_by: backend-architect (1/5)**
  改前的门 (`execution-modes.md:54-65`) 只做文件名 glob、零 git 调用; 改后 `--base`/`--anchor-base` 解析失败或 `merge-base` 失败一律 `git_failed` exit 2 + 消费方 fail-closed ⇒ 浅克隆 / 无远程跟踪 ref / git 不可用的采用方从「静默通过」变成「硬阻合并」。同 skill 既有约定方向相反 (`audit-engine/SKILL.md:405` 逐字「全部失败 → file-scope skip + warn, 不 crash」), 与已列入第 5 条的「坏 config JSON 刻意不同于 config-loader 散文」同性质, 应同样成条。载重点: 复议 #4b (PATCH vs MINOR) 的论证正是按「§5 自述八条」做的, owner 拿到的行为变更面仍不完整。
  *与 `7127ab68` 的关系*: 后者也指出 §5 枚举缺一条 (跨仓 `no_spec_unverifiable` 硬阻), 但缺的对象不同; 两条合看 = §5 的「穷举」声称至少缺两类, 建议 Phase B 一次补齐。

- `fa07e91a` [minor] architecture/§1.4 stdout 15 键契约缺运行面字段 (扫描受损与扫完确无同形) — **found_by: backend-architect (1/5)** · risk
  `.aria/audit-reports/` 不存在时按零报告继续评估 (`:222`), 只在 stderr 留 WARN ⇒ stdout 的 `matched==[]` + `status=missing` 与「目录存在且确实没有报告」逐字节同形。本 spec 自称镜像的 sibling probe 恰恰为此把**运行面** (`status`: ok/degraded/skipped + `reason`) 与**判定面** (`verdict`) 拆开, 并在 `execution-modes.md:185` 明写「消费方不得从 `hits == []` 推断结论」; 本门只继承后半句而没继承前半句的字段。方向仍 fail-closed 故记 risk; 缓解成本极低 (加 `scan_status` 或复用 `reason`)。

- `6c4455bd` [minor] testing/SC-2 选样硬约束在真实语料上不可满足 (两族各 ≥3 的唯一候选被 B.0 剔出) — **found_by: qa-engineer (1/5)**
  SC-2 要求所选 id 同时有 F-a (末段) 与 F-b (role 后缀) 两族样本且每族 ≥3。全枚举 837 份: 同时满足的 id **只有** `state-scanner-mechanical` (F-a 6 / F-b 8, 与 Tasks B.0 item 4 的「唯一候选」一致), 而该族 15 份全部无 frontmatter 且写盘时刻目录名是 `state-scanner-mechanical-enforcement` (git 历史 `32422df` 实证) ⇒ 15/15 两列不一致被 B.0 剔出。剔后仍同时具两族的 id 只剩 `state-scanner-inter-cycle-surfacing` (F-a 2 / F-b 3), 正文未点名 ⇒ Phase B 只能自行摸索。
  *与 `f04d6729` 的关系*: code-reviewer 的 decision 独立实测出**同一个候选**并给出「放宽到各 ≥1 且两列可取时存在真实语料」的可执行结论 —— 两席事实一致、结论互补, 依合并规则 3 判**不构成 conflicted**; Phase B 直接把 `f04d6729` 的候选写进 SC-2 即可闭合本条。

- `e83dca40` [minor] testing/SC-4 截断文案断言与 §1.2/§1.4 逐字模板不一致 — **found_by: qa-engineer (1/5)**
  §1.2 计数表 (`:143`) 与 §1.4 trail 行 (`:243`) 的 WARN 模板逐字以「, … 其余 K 份见 stdout 的 `unattributed`」结尾, 而 SC-4 (`:338`) 断言「只列前 20 个文件名并以 `… 其余 2 份` **收尾**」⇒ 按 endswith 写的断言在正确实现上必红, 按 contains 写又漏掉模板后半段。

- `03d241c7` [minor] documentation/Tasks 对 TestNoPytestImport 守卫的引述失准 (只扫自身文件) — **found_by: qa-engineer (1/5)**
  Tasks (`:315`) 写「`TestNoPytestImport` 断言**本目录源码**不含顶层 `^(import|from)\s+pytest`」, 实读该用例只读自己 (`src = Path(__file__).read_text()`, test_sibling_spec_probe.py:315), 对同目录新文件失明; 真正覆盖新文件的是 `TestRunAllTestsDiscovery` 经 `run_all_tests.sh:43-45` 的**目录级** grep + `conftest.py` 探测。结论 (必须 unittest、禁 pytest import 与 conftest) 不变, 但引述需订正, 否则 Phase B 可能以为改自己那份文件就能绕开。

- `243ad3d8` [minor] testing/SC-15(2)(3)/SC-19/SC-20/SC-22(2) 作用域缺失推给 Phase B 自改期望值 — **found_by: qa-engineer (1/5)** · risk
  §1.0 明写「本 spec 钉死如下全序……全部 SC 的期望值按此顺序取」(`:89-103`), 但这几条 SC 的 fixture 至今没有作用域来源 ⇒ 按 P2 先落 `change_scope_unresolved` exit 2, 与各自期望 (`pre_merge_not_enabled` / `matched_count == 1` / `checked_checkpoints` 含 `post_implementation`) 冲突。修正被推给 Tasks 的「既有 SC fixture 前提全量回扫」(`:316`), 由**无人值守**的 Phase B 自行改写期望值 —— 期望值一旦由实现者按自己的实现重算, 反事实即失去独立性 (B.0 想防的「标注者与实现者同体」在 SC 期望值上的翻版)。建议在 spec 内当场补全, 与 SC-3/SC-4/SC-9 同等待遇。

- `db4cd4eb` [minor] documentation/SC-13 先例锚点勘正注写反 (execution-modes.md:152 逐字含计数断言) — **found_by: code-reviewer (1/5)**
  `:347` 称「原稿锚的 `execution-modes.md:152` 实为竞品探针节的 blockquote……**不含任何计数断言**」。**汇总席实读 `:152` 逐字含「(机械护栏 SC-17 计数恰 2)」** —— 它不但含计数断言, 而且正是「分块计数 / 两块共 2」这一读法的直接 SOT 支撑。分块计数的结论本身与 `archive/2026-09-04-sibling-spec-probe/proposal.md:513` 一致, 故只需改这句注的措辞, 不必改 SC-13 判据。

- `524adcba` [minor] testing/SC-15(4) legacy 映射两格缺作用域前提且不在回扫清单 — **found_by: code-reviewer (1/5)**
  `:349` SC-15(4) 的两格 fixture 只给 `experiments.*` 配置, 无 `--change-id`、无锚点、无触 `openspec/changes/**` 的 diff ⇒ 按 `:91` 的求值总序 P2 先落 S4 `change_scope_unresolved` exit 2, 与其断言的 `checked_checkpoints == ['post_spec']` / 「落格 B 判 pass」冲突; 而 `:103` 与 Tasks `:316` 的作用域补齐清单逐字只列到 SC-15(2)(3), **(4) 既不在清单内、自身也没写** —— 与 R3 修 `94c6bfb1` 时清扫的是同一族。
  *与 `243ad3d8` 的关系*: 两条同属「SC fixture 缺作用域来源」族, 但前者是**在清单内但推给 Phase B**、本条是**不在清单内**, 依规则 4 保留双条; 建议一次清扫时把 (4) 一并纳入。

- `d5c42905` [minor] implementation/§1.1 S4-bypassed 的 checked_checkpoints 在 adaptive 档未定义 — **found_by: code-reviewer (1/5)**
  `:122` 规定 S4 被豁免时 `change_ids=[]`、`results=[]`、「`checked_checkpoints` 照常枚举」; 但 `:99` P4 的纳入判定是 per (checkpoint, change_id) 且 adaptive 档要读**该 change 的** Level (`:170` 级 2a) —— `change_ids=[]` 时无 Level 可取 ⇒ 该字段在 adaptive 下无定义, SC-9(2) 也未锁它 ⇒ 两个合法实现可给不同值 (空 list vs 仅 explicit 档)。修法: 明确取「仅 explicit 档的键」或 `[]`, 并在 SC-9(2) 加字面断言。

- `2f664130` [minor] documentation/头部 :14 审计计划的 checkpoint 枚举漏 mid_post_spec — **found_by: knowledge-manager (1/5)**
  **汇总席实测** `.aria/config.json` 的 `audit.checkpoints` 只有 7 键、**无 `mid_post_spec`**, 且 `mode="convergence"` ⇒ 按本文自订的优先级链级 2b 与其引的 SOT (`config-example.md:276`「所有检查点强制使用该模式」), `mid_post_spec` 在本仓解析为 `convergence` = 启用。头部 `:13-14` 逐一点名了其余七个 checkpoint 的启停与白名单归属, 唯独它没有交代 —— 其结构性前提 (B.2 漂移未发生) 可归 Rule #10 白名单第四类, 但未成文即不构成留痕。

### Decisions (11, 不计入缺陷 severity 计数)

- `ad5f1f6d` [minor] documentation/R3 的 3 Critical + 12 Major 逐条落进正文 (非批注) — **found_by: tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager (5/5)**
  本轮唯一的 5/5 全席独立结论。五席各自抽验落点: `2d7cccbe` → §1.3 判据 1-3 (`:178-186`) + §1.1 末段逃生口 + SC-20(3)-(6) + 复议 #10; `7877bac6` → §1.3 级 2b/2c/2d + 级 3 + §1.4 格 B 的 `enabled_by` 前置 + SC-15(5); `34507656` → §1 `--anchor-base` (`:84`) + S3 三条 (`:111`) + `no_spec_unverifiable` + SC-5(8)/SC-17(4); `3fa67e89` → §4 `:270` / Tasks `:328` / 复议 #4 三处已一致改为 v1.73.1(PATCH)/v1.74.0(MINOR), 版本回退风险解除 (实测 tag 最高 `v1.73.0`, `plugin.json`=1.73.0, gitlink `f314785`); 另 §1.0 求值总序 P0-P6、§1.4 stderr 通道、15 键 + 9 `error_kind`、SC-13 分块计数、Tasks unittest 风格、B.0 无人值守机械仲裁均有实体条款。**无一条是换个说法糊过去** —— 这也是本轮四条 Major (`b2bc13a6` / `a657bf0a` / `01b9faf6` / `8acafe0a`) 全部落在「rework 自身的下游未闭合」而非「原缺陷复发」的原因。
  *category 分歧注*: tech-lead / backend-architect / knowledge-manager 记 documentation, qa-engineer 记 testing, code-reviewer 记 architecture ⇒ 取多数 documentation。

- `c8b56f72` [minor] documentation/SOT 行号引用抽验零漂移 (约 40 处逐条实读) — **found_by: code-reviewer, knowledge-manager (2/5)**
  code-reviewer 逐条打开约 40 处 `文件:行号` (execution-modes / audit-engine SKILL / phase-c-integrator / report-storage / pre-write-validation / config-loader / config-example / DEFAULTS.json / project.md / proposal-minimal / configured-gate-authority / skill-benchmark-exemption / spec-drafter / collectors/audit.py / spec_complete.py / sibling_spec_probe / multi_remote / 两份 archive proposal) **全部命中, 未发现行号漂移**; R1/R2/R3 做的四次行号勘正 (`:250` / `:117-118` / `:28-32` / `:35`) 经实读均正确。knowledge-manager 独立复核同一批锚点亦全中。tech-lead 与 backend-architect 在各自的机械核验清单里也记录了同类抽验结果 (未列为独立结论)。

- `2392bb72` [minor] testing/语料事实底盘独立复算 (837 / 末段族 62 / unattributed 170·160 / legacy 6 / C=153) — **found_by: backend-architect, qa-engineer, code-reviewer, knowledge-manager (4/5)**
  四席各自全枚举复算, 与正文逐字吻合: `.aria/audit-reports/` 顶层 **837** 份 `.md`; 含 `context:`|`spec_id:`|`change_id:` **582** / 皆无 **255** (与 Tasks B.0 `:310` 三数相同); 末段族 **62**; unattributed 全 8 checkpoint 口径 **170** / 本仓 2-checkpoint 口径 **160**; 真 2-field legacy **6**; 多归属 **0**; `*-audit-trail.md` 族 **5** (与 §1.2b 同集); `C` 今日 **153** (正文冻结快照 152, 差 1 = 本 spec 自身目录)。backend-architect 另验三桶互斥且穷尽 (650+6+170=826)、`openspec/archive/` 146 条目中只有 `README.md` 无日期前缀 ⇒ S1 的「去日期前缀后逐字相等」在本仓 100% 成立; code-reviewer 另验 Critical-1 证据可复现 (三个在飞 change 的报告 infix 命中 0 / 末段命中 9·9·1)。

- `edaf86a1` [minor] implementation/Level 解析统计复算 (144 成功 / 9 失败 / 首命中 >15 恰 7 / 含 Spec Level 15 / 行首 139-3-2-0) — **found_by: code-reviewer, backend-architect, qa-engineer, knowledge-manager (4/5)** · *依合并规则 7 计入 (后三席把该组数字写在其他 decision 条目内)*
  除分布外的全部统计四席逐项互洽: 153 份 → 成功 **144** / 失败 **9** (九个目录名逐一同集, `openspec/changes/` 下 8 个在飞 change 无一在内) / 首命中 >L15 **恰 7 份** (七个名与行号逐一相同, 最深 `2026-09-06-a1-entry-claim-duplicate-work-guard:58`) / 含 `Spec Level` **15** / 行首 `> **`139 · `- **`3 · `##`2 · 其它 **0**。⇒ R3 执笔席自验项 A1 不采纳 R3 聚合席「6 份 / 138-3-2-1」的判断**成立** (差源是 `premerge-gate-branch-existence:13` 那条叙述句被行首锚约束排除)。**汇总席已独立复算确认**上述全部数字。

- `e87f97bd` [minor] testing/SC-12 既有测试基线三套件全绿 (104 / 148 / 1593) — **found_by: qa-engineer (1/5)**
  今日实跑: `audit-engine/tests` 104 tests OK · `phase-c-integrator/tests` 148 tests OK · `state-scanner/tests` 1593 tests OK, 0 failure ⇒ SC-12 不存在需要 carve-out 的既有失败项; `run_all_tests.sh --list` 现把 audit-engine 归为 `(unittest)`, 与 Tasks 的 unittest 风格约束一致。(与 R3 `3d2287b0` 同结论持存。)

- `298cfee0` [minor] testing/R-h / SC-22(1) 陈旧 base 方向 hermetic 复跑成立 (超集 ⇒ 假红) — **found_by: qa-engineer (1/5)**
  hermetic 复跑 (tmp 仓 origin/master=c3、本地 master 强制退到 c1、feature 从 origin/master 开出): `git diff --name-only --no-renames $(git merge-base HEAD master)` 输出 **4** 个文件 (含他人 `openspec/changes/other/proposal.md`), 换 `origin/master` 输出 **2** 个 ⇒ 「陈旧 base ⇒ merge-base 更旧 ⇒ diff 超集 ⇒ 作用域膨胀 ⇒ `missing` 假红」方向成立, SC-22(1)(i) 的 fixture 可构造。⇒ R3 major `c4610d6b` (失效方向论证错) 的修法本轮**判真闭合**。

- `de206772` [minor] architecture/ship 前提与同伴在飞面实测 (gitlink f314785 / 六触点 diff 空 / version.yaml 1.5.0) — **found_by: tech-lead (1/5)**
  `git ls-tree HEAD aria` = `f314785` (= v1.73.0 + 1 个 state-scanner 测试修复提交); `git -C aria diff --stat 301641b f314785 --` 对六个代码/规程触点文件输出为空; 旧 schema `{timestamp}` 残留实测恰 4 处且行号逐字命中 (phase-b-developer:204,277 / phase-c-integrator:157 / phase-a-planner:267); `ab-suite/version.yaml` 仍 `1.5.0` (目标 1.6.0 未被占); 并发轨 #195 的「待 owner 复议 6」今日在 `:510`, 代码触点与本 spec 零交叠。⇒ Phase B 的起分支基线与同伴在飞面本轮无新冲突 (R3 `83b200e6` / `cbc6c524` 两条同向持存)。

- `020945aa` [minor] architecture/§5 消费方与同步面核验 (零代码消费方 / {timestamp} 4 处 / 主仓 16 版本点) — **found_by: code-reviewer (1/5)**
  全 skill 树对 `allow_incomplete_checkpoints` / `missing_checkpoint` **零代码消费** (两处 grep 命中是 state-scanner 里同名短语「completeness gate」, 语义无关); `.aria/state-checks.yaml` 16 个已注册 check 无一触及 audit-engine / audit-reports; `{timestamp}` 残留恰 4 处且与 §4 列表逐一相符; 主仓 16 个版本字符串点逐行实读全部在场且现值 v1.73.0; `check_bare_issue_refs.py` 确未被任何 SKILL.md / state-checks.yaml / standards 引用 ⇒ Tasks 里「不当门, 请 owner 明确」的处置符合 Rule #10。backend-architect 的机械核验清单第 5 项 (全插件树 grep 零命中) 与 knowledge-manager / tech-lead 的同步面数字独立复算与本条一致。

- `7560bcd5` [minor] documentation/头部 Linked Issue 字段过 spec-drafter 机械判据 — **found_by: knowledge-manager (1/5)**
  **本轮唯一与上轮四元组逐字相同的键** (R2 `d188f0b8` → R3 `7560bcd5` → R4 `7560bcd5`, 三轮持存)。`proposal.md:6` 经 `cat -A` 核字节为 `> **Linked Issue**: \`10CG/Aria#199, 10CG/aria-plugin#161\`` —— 单 code span 内 `, ` 分隔多 issue (写法 1)、行首无空白 + `>` 后恰一个空格 + 字段名两侧各两星号 + ASCII 冒号 + 非 markdown 链接形 (写法 3); 字段序 `Level → Status → Created → Linked Issue` 与模板一致。合规。

- `c623a2d2` [minor] documentation/Rule #6 档位与 SOT 判据表对账 + Rule #10 未自行删闸 — **found_by: knowledge-manager (1/5)**
  判据表实读在 `skill-benchmark-exemption.md:26-31`、附加约束 `:33`、`:35` 为「## 3. 第三行不是逃生舱」标题 —— References 的三处行号勘正全中。本 spec 取两读法**并集** (照跑 audit-engine.json 2 evals + phase-c-integrator.json 3 evals, 实测 version 1.0.0 / 1.1.0; 第三行三义务齐备), 严格宽于任一单行要求; `phase-c-integrator-pre-merge-gate.json` 实测 `type=workflow_skill_subextension` / 无 `evals` 键 / 8 fixtures, 其是否算照跑面列复议 #9 交 owner ⇒ 符合 Rule #10, 未自行删闸。(R3 `d9ad60ac` 同向持存; category 由 architecture 改记 documentation, 依席位本轮标注。)
  *与 `29c39e2c` 的关系*: 本条核的是**档位取法**, 该 major 核的是**替代面的事实陈述**, 两者不矛盾。

- `f04d6729` [minor] testing/SC-2 采样可行性 (Tasks B.0 第 4 条, 放宽到各 ≥1 存在真实候选) — **found_by: code-reviewer (1/5)**
  Tasks B.0 第 4 条属实 —— 「两族各 ≥3」的唯一候选 `state-scanner-mechanical` 的 15 份报告实测 **0 份**有独立源字段。补充一条对 Phase B 直接有用的实测: 放宽到「两族各 ≥1 且两列都可取」时**存在真实语料候选** `state-scanner-inter-cycle-surfacing` (F-a 2 / F-b 3, 均带 frontmatter 字段) ⇒ 规则 (c) 分支不必退化成「用 `--change-id` 自造样本」(那会把 SC-2 推回它要防的自指)。**与 `6c4455bd` 事实一致、结论互补, 不构成 conflicted**。

---

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **14** / Minor **15** (缺陷类 = issue + risk; 另有 11 条 minor decision 不计入)。

rationale: 按 `report-storage.md §Verdict` 计算, 0 Critical + ≥1 Major ⇒ **PASS_WITH_WARNINGS**。post_spec 的阻塞行为是 `blocking: false` (report-format.md 阻塞行为表), 本判定不阻断流程; 按 Rule #10 该判定不得由 AI 自行升降。

**本轮相对 R3 是一次真实的台阶跃迁, 但收敛尚未发生**:

- **verdict 从 FAIL 升到 PASS_WITH_WARNINGS** —— R3 的 3 Critical 全部消解, 5/5 席独立确认修法**落在判据本体而非批注** (`ad5f1f6d`), 且落地文本经四席各自写解析器 / hermetic fixture 复跑基本站得住: 语料底盘 (`2392bb72`)、Level 解析统计除分布外的全部字段 (`edaf86a1`)、SOT 约 40 处行号零漂移 (`c8b56f72`)、既有三套件全绿 (`e87f97bd`)、消费方接缝零破坏 (`020945aa`)、陈旧 base 方向已修真 (`298cfee0`)、版本回退风险已解除 —— 汇总席对其中六组数字做了独立机械复核, 全部命中。
- **十四条 Major 里没有一条是 R1/R2/R3 结论的原样重复**: 逐条比对四元组, 本轮 40 个键与上轮 42 个键的字面交集只有 **1** 条 (`7560bcd5`, 一条正面 decision)。R3 的 3 Critical + 12 Major 无一以同四元组复发 —— 这与 R2→R3 那轮 (6 条同 scope 缺陷复发) 有本质区别。
- **但缺陷总量没有下降** (R3 28 → R4 29), 且新缺陷高度集中在**同一个模式**: 十四条 Major 中至少九条 (`b2bc13a6` / `a657bf0a` / `01b9faf6` / `a00c52bb` / `8acafe0a` / `955907f2` / `7127ab68` / `95ddb322` / `2370f1f9`) 是 **R3 修法自身的下游未闭合** —— 改了判据却没回灌校准数字、搬了 S3 的解析面却没对齐 S2 的求值序、加了参数却没进输入声明面与调用模板、钉了新前置却没回扫十条 fixture、写了新条款却没建 SC、立了新仲裁规则却把它服务的样本族剔空。这正是 memory `feedback_rework_leaves_downstream_ac_drift` 与 `feedback_spec_rework_leaves_downstream_ac_drift` 描述的形态, 在本 spec 上连续第三轮出现。

三条最值得优先处置的:

1. `b2bc13a6` (4/5 席 + 汇总席复算): 本 spec 通篇在治「机械判据未对真实数据值域验证」, 而它自己那段「可复现」的校准数字在自己的判据下复现不出来, 还留了一句可证伪为假的「取值逐个相同」。风险不是恒绿而是**反向消歧** —— Phase B 为对上 57/86 可能删掉剥线子规则。修法只是两处数字与一句话。
2. `f637d129` + `7127ab68` + `a00c52bb` + `a657bf0a` 四条合看: 「跨仓 / Level 1 / `--no-spec`」这批人群究竟被硬阻、被放行还是走正常评估, 目前**四条条款各说各话且互为前提**。建议 Phase B 前一次性画出这批人群的判定表, 而不是逐条打补丁 —— 否则改一处会推翻另一处的前提 (本轮 `f637d129` 就是 R3 改 `fdb30703` 的直接产物)。
3. `bb0e565f`: 修法留在门内、门外的接线口 (调用方步骤 3) 没动, 使 §5 的行为变更在生产路径可能整段不可达。这是唯一一条「改对了也测不出来」的面 —— 全部 SC 都是直调 fixture。

十五条 Minor 的共性: 过半 (8 条) 是「R3 新写的条款缺一条断言 / 缺一处回灌」(`7b17ada9` / `d9578e5d` / `642c9e5e` / `e83dca40` / `243ad3d8` / `524adcba` / `d5c42905` / `66737069`), 修法成本普遍是一句话或一条 SC; 另有三条是**勘正自身写错** (`db4cd4eb` 的先例锚注写反、`03d241c7` 的守卫引述失准、`2f664130` 的 checkpoint 枚举漏项) —— 与 R3 已点名的 memory `feedback_author_and_verifier_must_differ_for_corrections` 同型, **本轮 minor 的勘正批建议继续换非 v4 执笔者复核**。

计算依据:
- Critical issues: 0
- Major issues: 14 (14 issue + 0 risk)
- Minor issues: 15 (11 issue + 4 risk)
- Decisions (不计入): 11
- Conflicted 对: 0

---

## 轮次记录

### Round 4

- Agents: 5/5 (tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager) —— 无缺席, `round_incomplete: false`, `skipped_agents: []`; frontmatter 15/15 字段齐全 5 份, **0 份需补齐**
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品 (五席各自独立报同一结论)
- Conclusions: 40 (去重前 55 = 54 条席位结构化条目 + 1 条依合并规则 6 从正文纳入) —— Critical 0 / Major 14 / Minor 15 / Decisions 11
- Delta vs 上轮: 上轮 42 keys, 本轮 40 keys, **字面交集 1 条** (`7560bcd5` 头部 Linked Issue decision, 三轮持存) ⇒ `stable_vs_prev: false`。R3 的 3 Critical **全部消解且无同四元组复发** (`2d7cccbe` / `7877bac6` / `34507656` 的修法本轮 5/5 席确认落地; 其下游各自派生出新 Major: `b2bc13a6`+`01b9faf6` 出自 Level 判据修法、`955907f2`+`f637d129` 出自四值 mode 链修法、`a657bf0a`+`a00c52bb`+`7127ab68` 出自 S3 锚点面修法)。R3 的 12 Major 去向: **判真闭合 5 条** (`3fa67e89` 版本目标三处已对齐 v1.73.1、`c4610d6b` 失效方向已改对并经 hermetic 实跑确认 → `298cfee0`、`3f817a3b` SC-13 已改分块计数、`1b189d49` stderr 通道已钉、`868def3b` unittest 风格已成文); **修法留下下游 4 条** (`506ce733` 求值序已钉但派生 `b451a016`+`243ad3d8`、`affceac8` B.0 仲裁已钉但派生 `2370f1f9`、`36cf2e53` fixture 回扫已列任务但 `enabled` 一格未覆盖、`54db6bfd` 逃生口已补但 `01b9faf6` 的 eager 读法会再抵消); **本轮未再被提出 3 条** (`d442a8c0` 格 B 人群论证、`3b8bf6dd` (b) 白名单证据、`3bd0562f` 版本级别 —— 后者本轮以 `aebd2f9f` (Level 定级) 换面出现)。R3 的 13 Minor 中 4 条头部回灌类本轮全部未再出现。conflicted 对: R3 = 1, **本轮 = 0**
- Vote 票型: REVISE 5 / PASS 0 ⇒ `unanimous_pass: false`
  - 单席 verdict: PASS_WITH_WARNINGS **5/5** (tech-lead C0M3m4 / backend-architect C0M4m3 / qa-engineer C0M5m4 / code-reviewer C0M3m3 / knowledge-manager C0M3m3) —— 五席自判 verdict 首次全部一致且无 FAIL, 但五席仍全部投 REVISE (理由同构: 缺陷均为「Phase B 无人值守下会变成必红一条或两个合法实现判决不同」)
- Duration: N/A (编排脚本未提供计时)

---

## 统计

| 指标 | 值 |
|------|-----|
| 总轮次 | 4 |
| 总耗时 | N/A |
| Agent 参与率 | 5/5 (缺席 0) |
| Frontmatter 契约完整率 | 5/5 (15/15 字段齐全, 0 份需补齐) |
| 去重前/后 conclusions | 55 / 40 |
| Critical / Major / Minor (缺陷类 = issue + risk) | 0 / 14 / 15 |
| 其中 issue / risk | 25 / 4 |
| Decisions (不计入缺陷计数) | 11 |
| Conflicted 对 | 0 |
| 5/5 全席独立命中 | 0 finding + 1 decision (`ad5f1f6d`) |
| 4/5 席命中 | 1 finding (`b2bc13a6`) + 2 decisions (`2392bb72` / `edaf86a1`) |
| unanimous_pass | false |
| stable_vs_prev (四元组集合逐条相等) | false (42 vs 40, 字面交集 1 条) |
| converged | false (集合不等 且 unanimous_pass=false) |
| 收敛轮次 | N/A |

---

## Rework 清单

按 severity 排序; critical / major 逐条列出。**汇总席只列动作建议, 不代替 owner 与 Phase B 实施者裁决** —— 标 `待 owner 复议` 的按 Rule #10 不得由 AI 自行处置。

| # | id | severity | 席位 (found_by) | 建议动作 |
|---|----|----------|-----------------|----------|
| 1 | `b2bc13a6` | major | backend-architect, qa-engineer, code-reviewer, knowledge-manager (4/5) | `:184` 两处订正: 分布改 **L3 58 / L2 85 / L1 1**; 「144 份取值逐个相同」改为「除 `premerge-gate-branch-existence` 一份由 2 变 3 外逐个相同 —— 那正是剥删除线子规则的唯一样本」。**优先随手闭合** (两处数字 + 一句话), 且必须与判据 2 同批改, 否则 Phase B 会反向删掉剥线规则。汇总席已实跑复核该组数字 |
| 2 | `955907f2` | major | tech-lead, backend-architect, knowledge-manager (3/5) | 格 B 第四合取项的量化对象改写成「每个**被解析** checkpoint 的 `enabled_by`」(消除空集真空成立), 并把 `mode:convergence` / `mode:challenge` 下的空纳入集处置显式写死 (补一格兜底或说明其结构上不产生空集); SC-15 补 backend-architect 给出的那个 config 形态 (`{enabled:true, mode:"convergence", 四个非排除项显式 off}`) 一格反事实 |
| 3 | `a657bf0a` | major | qa-engineer, knowledge-manager (2/5) | 二选一并成文: (a) 把 `--no-spec` 的矛盾检测提到 S2 之前 (同时改 §1.0 P2 与 §1.1 的 first-match 声明, 使契约自洽); (b) 保留现序并把 SC-7 的同仓格期望改为「S2 命中 ⇒ `scope_source=diff` 正常评估」, 把 `no_spec_contradicted` 的唯一可达面明写为跨仓。**须同时订正待 owner 复议 #2 对该守卫强度的描述** —— 现在给 owner 的前提是「单仓可达」 |
| 4 | `f637d129` | major | tech-lead (1/5) | §1.4 与 §5 (`:226`/`:283`) 的 adaptive 档 Level 1 人群重写: 该人群实际落格 C exit 2 硬阻, 不是格 B pass; 明确它与 `--no-spec`/S3 的先后 (P2 只产出 `scope_source`, 三态在 P6)。SC-7 补钉 `audit.mode` 并新增一格 adaptive+Level 1。**待 owner 复议 #8 的人群依据须第三次重给** (R2 → R3 → 本轮已偏移三次), 建议与 `7127ab68` / `a00c52bb` / `a657bf0a` 合并成一张「跨仓 × Level 1 × --no-spec」判定表一次裁 |
| 5 | `bb0e565f` | major | tech-lead (1/5) | §3 补一条对齐调用方步骤 2/3 的任务: 要么把 `phase-c-integrator/SKILL.md:132` 的字面键判断改成与门侧同一条优先级链 (则须同时闭合 `f637d129` 的硬阻), 要么在 §1.4 `:220` 删掉「调用方守卫使格 A/格 C 生产不可达」这一论证前提并承认 §5 第 7 条的行为变更在现状下不可达。**两个读法必须择一成文**, 且补一条走真实调用链 (非直调 fixture) 的 SC |
| 6 | `4cbe35ce` | major | tech-lead (1/5) | SC-12 的归档门 liveness 子句二选一: (a) 改成对**带 `tasks.md`** 的合成 spec 目录跑 `--gate`, 断言含 `completeness_gate.py` 的 `[x]` 集成声称被判 alive (反事实 = 调用行只写散文 ⇒ block); (b) 删该子句并把 F7 (`:56`) 的落点明确改挂 SC-13。汇总席已实跑确认本 spec (proposal-only) 下该断言结构上不可能红 |
| 7 | `01b9faf6` | major | backend-architect (1/5) | §1.0 P3 改为「按需解析 (仅当某对落到级 2a 时)」以与 `:186` 文案、`:286` §5 第 6 条、`:103` fixture 指引一致; 或保留 eager 并把 `:186` 的第二个 fix 与 `:286` 的限定句一并改写 + 给全部 fixture 补 Level 行。**须与 `b451a016` 的 fixture 回扫一次做完** (同族清扫) |
| 8 | `a00c52bb` | major | backend-architect (1/5) | S2 的解析面成文: 建议随 S3 一起改取锚点面 (或锚点面优先、diff 面兜底), 并补一条「跨仓 + 无 `--change-id`」的 SC; 若刻意保留 diff 面, 须把「跨仓下 S2 恒空、必须显式传 `--change-id`」写成契约条款 (而非 SC-5(5) 的 fixture 注) 并改 S4 (`:111`) 的第二个 fix 文案 |
| 9 | `b451a016` | major | qa-engineer (1/5) | 二选一: 把 P1 (`:96`) 的「无条件前置」与 §1.4 `:220` 的「纳入集为空时分三格」表述统一 (改标题或改 P1); 并在 `:103` 与 Tasks `:316` 的 fixture 硬约束里**补上 `enabled` 这一格**, 对十条缺 `enabled: true` 的 SC fixture 逐条回扫。当前该格无任何任务承接 |
| 10 | `2370f1f9` | major | qa-engineer (1/5) | B.0 规则 (b) 收窄: 对 F-e (legacy) / F-f (unattributed) 两族, 第二列的正确标注按定义就不是 change_id, 不能用「两列一致」当剔除判据 —— 建议改成「仅对**期望标注为某个 change_id** 的族做双列交叉, legacy/unattributed 两族改用另一条机械判据 (如 frontmatter 字段存在性 + 文件名族形态)」。否则 SC-4 的「两个计数分离」失去真实语料样本 (R1 Critical-1 的封口) |
| 11 | `95ddb322` | major | qa-engineer (1/5) | 为 R3 新增的两条条款各补一条 SC: (a) `--change-id` 与 `--no-spec` 同传 ⇒ exit 2 + 指定文案; (b) 混合 Level 多 change PR 下「逐对」与「叉乘」判决不同的那一格 (对本该 off 的对不得判 missing)。第 2 条无断言时被误读的后果正是假红阻断合并 |
| 12 | `29c39e2c` | major | code-reviewer (1/5) | 订正四处 (`:12` / `:324` / `:348` / `:362`) 对 `phase-c-integrator-pre-merge-gate.json` 的事实陈述, 并把动作拆成三条可执行命令 (`GateCheckTests` + `NotFoundVerdictTests` + `test_path_coverage.InternalErrorReasonTests`); 把 `NEG-2-timeout` / `wait_then_green` 两条无可执行 node id 的绑定显式记为该 catalog 自身缺口。**待 owner 复议 #9 的裁决依据须随之重给** (现依据是假陈述)。汇总席已逐条实读该 json 复核 |
| 13 | `7127ab68` | major | code-reviewer (1/5) | **待 owner 复议** (属放行面变更, 建议并入复议 #10 一并裁): 把「锚点仓在本分支零 diff」与「diff 非空但不触 change 目录」分开 —— 前者降为 `[WARN] --no-spec 不可核验` + 继续按 `missing`/`present` 评估, 或保持硬阻但显式挂一个既有旗标; 同时补进 §5 枚举与 SC-17 的跨仓格。与第 4 项合并成一张判定表处置 |
| 14 | `8acafe0a` | major | knowledge-manager (1/5) | 把 §3 实传的五个参数**全部**补进 §2 (`:250`) / §4 同步表 (`:265`) / Tasks (`:320`,`:321`) 的 audit-engine 输入声明面 (`SKILL.md:49-54`), 并为 §1 bash 块里的 `<主仓 root>` / `<C.2 合并目标仓 root>` / `<main_branch>` 三个占位写明来源 (Rule #3); 顺带把 `:74-78` 调用模板补上 `--anchor-base` (即 minor `642c9e5e`, 同根一次做完) |

Minor 15 条与 Decisions 11 条不入 rework 清单, 随稿修订即可。其中五条建议优先随手闭合 (成本一句话或一处改写): `db4cd4eb` 的先例锚注 (`execution-modes.md:152` 逐字含「机械护栏 SC-17 计数恰 2」, 汇总席已实读)、`d9578e5d` 的 SC-13 切片界定 (改按小节或按 `Step 4:`~`Step 5:` 行区间; 汇总席实测围栏为 `:34`-`:66`)、`642c9e5e` 的调用模板补 `--anchor-base`、`03d241c7` 的 `TestNoPytestImport` 引述订正、`2f664130` 的头部 checkpoint 枚举补 `mid_post_spec` (汇总席已实测本仓 config 7 键)。另按 memory `feedback_author_and_verifier_must_differ_for_corrections`, **本轮的勘正批建议换非 v4 执笔者复核** —— 本轮三条 minor (`db4cd4eb` / `03d241c7` / `2f664130`) 与一条 major (`b2bc13a6`) 都是勘正/自验动作自身写错, 与 R3 同型。
