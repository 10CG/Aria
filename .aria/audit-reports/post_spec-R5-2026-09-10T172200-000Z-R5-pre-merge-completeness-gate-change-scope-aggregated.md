---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: false
oscillation: false
overridden_by_user: true  # owner 2026-09-12 裁三路径 [1] 接受当前结论 (决策单 .aria/decisions/2026-09-12-two-l2-specs-195-199-owner-gates-and-technical-rulings.md)
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

# post_spec 聚合审计报告 — pre-merge-completeness-gate-change-scope (Round 5)

本文件由汇总引擎席产出, 合并本轮 5/5 席位的结构化结论。五份单席报告原文逐字落盘于同目录 `post_spec-R5-2026-09-10T172200-000Z-R5-pre-merge-completeness-gate-change-scope-{role}.md` (role ∈ tech-lead / backend-architect / qa-engineer / code-reviewer / knowledge-manager)。五份 frontmatter 均 15 字段齐全, **0 份需补齐**; `round_incomplete: false`, `skipped_agents: []`。

**合并规则 (与 Round 1 / Round 2 / Round 3 / Round 4 同一套, 供 Round 6 复算对齐)**:

1. 按 `{category, scope}` 匹配, 语义同、写法异的合并为一条; `found_by` 列全部提出席位, `severity` 取最高。
2. `category` / `type` 席位间不一致时取多数标注; 平票取席位序在先者 (顺序: tech-lead → backend-architect → qa-engineer → code-reviewer → knowledge-manager)。每处不一致均在条目内注明原始标注。
3. 同 scope 的**矛盾**意见 (结论相反, 非同一缺陷的不同 severity) 保留双方并标 `conflicted: true`, 汇总席**不裁决**。**本轮 conflicted 对 = 1** (`fbe16e0a` ↔ `2ee0164c`, 见条目内说明)。
4. `scope` 语义不同则不合并 —— 即使锚在同一节 (本轮据此保留了 §3 调用方接缝的三条、§1.4 分割证的两条、§1.0 fixture 硬约束的两条、SC-11 的两条各自独立)。
5. `finding id` = `sha256("{category}:{scope}:{severity}:{type}")[:8]`, scope 取归一写法 (trim + 折叠空白 + ASCII 小写), 用 python3 实算 (45 条全部唯一, 无碰撞; 其中 `e87f97bd` / `7560bcd5` 与 R4 同 id ⇒ 与上轮同一算法, 可交叉验证)。
6. 席位 `### Decisions` / `### Risks` 有条目只在报告正文出现、未进结构化清单时一并纳入 (Round 1-4 先例)。**本轮命中 3 条**, 全部出自 backend-architect 正文: 两条 decision (`2ee0164c` 求值总序自洽性 / `94c5803e` error_kind 封闭集穷举) 与一条 risk (跨仓 (b) 通道靠调用方传参 —— 依规则 1 并入 tech-lead 的 `2555f938`)。
7. 一条单席 finding 同时载有两个不同 scope 的论断时, 分别计入两条合并条目的 `found_by` 并互相点名; 去重前计数仍按单席原始条目数计。**本轮命中 3 处**: code-reviewer 的 SC-11 条 (同载 `--repo-path` 必填性与裸 `master` 两论断 ⇒ 进 `2cac2ac0` 与 `d8d037be`)、backend-architect 的「语料与 Level 解析器数字」(进 `6292d37d` 与 `17417aee`)、knowledge-manager 的「版本面/残留族/基线冻结/并发轨枚举」(进 `9344c3a0` 与 `34f4c7b6`)。

**汇总席本轮的机械复算** (只读复核, 不改变任何 finding 的 severity 与处置; 本席未编辑任何仓库文件):

- **`7e78199f` (CR 单席 Major, 与四席 decision 有交叠面) —— 实测成立且是本轮唯一「勘正自身再次漏核」**: 汇总席解析 `ab-suite/phase-c-integrator-pre-merge-gate.json` 得 8 条 fixture 绑定 = `GateCheckTests` 4 / `NotFoundVerdictTests` 1 / `test_path_coverage.InternalErrorReasonTests` 1 / 无 node id 2 (四席的 decision 面属实); 但其中 `NEG-1-malformed` 的 node id 逐字是 `test_pre_merge_gate.GateCheckTests.test_case_e_malformed_aether_routes_fail`, 而全插件树 grep 该方法名**只有该 json 一处命中**, 真代码里是 `test_case_e_malformed_aether_main_leg_routes_fail` (`aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py:266`)。⇒ CR 的「可执行绑定 5/8 非 6/8、catalog 缺口 3 条非 2 条」成立; qa-engineer 实跑的三条**类级**命令 (7/1/1 tests OK) 与之不矛盾 —— 类级跑法绕开了坏 node id, 两席事实一致, **不构成 conflicted**。
- **`b5f7ca8f` (CR + KM 双席 Major) 实读成立**: `execution-modes.md:41` 逐字 `Step 2: 豁免检查`, `:43` 逐字 `→ 跳过校验, 继续执行 pre_merge 审计` —— 而 proposal §2 (`:304`) / §4 (`:321`) 的位置列均只到 `:44` 与 `:82`, `:42-43` 无落点。
- **`4d9ff818` (TL 单席 Major) 实读成立**: `execution-modes.md:5` `## 入口逻辑`, `:9` `- audit.enabled == false → 静默返回`, `:10` `- checkpoint 未启用 → 静默返回`, `:15` `- checkpoints 显式配置 > adaptive_rules 推导 > 默认 off`; 对被审 proposal 全文 grep「静默返回」**0 命中**、「入口逻辑」**0 命中** ⇒ 第二道启用守卫确实全文零提及。
- **`4fca2e7a` (KM 单席 Major) 的四个产出侧调用点逐条命中**: `phase-a-planner/SKILL.md:246` 逐字「检查 audit.checkpoints.post_spec — "off" 则跳过」· `task-planner/SKILL.md:123` · `phase-b-developer/SKILL.md:255` (另 `:49`) · `brainstorm/SKILL.md:141`; `DEFAULTS.json` 实测 `audit.checkpoints` 八键全 `"off"`、`adaptive_rules = {level_1:"off", level_2:"convergence", level_3:"challenge"}`、无两个 `allow_*` 键 ⇒ 该席的推演前提成立。
- **`52ce53b6` / `7221bb22` 的共同前提实测成立**: `DEFAULTS.json` 的 `adaptive_rules.level_2 = "convergence"` / `level_3 = "challenge"` (故 adaptive 档下未写的 checkpoint 会被纳入); proposal 的排除清单实为 4 项 (`pre_merge` / `post_closure` / `mid_post_spec` / `mid_implementation`), `post_brainstorm` **未**在其中 (`:37` 与 `:217` 两处口径一致) ⇒ qa-engineer 关于 SC-20(7) 会多出 `(post_brainstorm, b)` 一对的实算成立。
- **`66a29a89` (QA 单席 Major) 汇总席逐份复读确认**: `state-scanner-inter-cycle-surfacing` 的 3 份 F-b (`pre_merge-R1-R4-…-sub-pr-a.md` / `-sub-pr-c.md` / `pre_merge-R1-R5-…-sub-pr-b.md`) 的 frontmatter **只有 `context:` 一行且值为散文** (逐字如 `context: state-scanner-inter-cycle-surfacing sub-PR (a) — TX.0 + TX.1 prerequisite`), **无 `change_id:` / `spec_id:` 字段**; 2 份 F-a 带 `change_id:`。⇒ code-reviewer 的「独立源字段命中 5/5」与 QA 的「3 份不是 change_id」两者都真, QA 的读数更细 (指向 B.0 (b1) 的逐字剔除规则), **不构成 conflicted**; SC-2 `:405` 的「frontmatter 可取第一列」对这 3 份为假。
- **`00976693` / `77262ffd` / `6541a212` / `01ad5637` 四条 minor 逐条实测**: (a) proposal `:114` 标题逐字「全部 hermetic fixture 的**两条**硬约束」却列 (1)(2)(3), Tasks `:378` 逐字「补 §1.0 末段的**三条**硬约束」—— 互斥属实; (b) 汇总席实跑 `check_bare_issue_refs.py` 对本 proposal 得 **84** (proposal 写 64) —— CR/KM 两席数字一致; (c) `config-loader/config-example.md` 场景 A 的 `checkpoints` 块实为 **7 键 = 6 个 `off` + `pre_merge: "convergence"`** 且 `mode` 是 `"manual"` ⇒ proposal `:263`/`:454` 的「七键 off」算错一键; (d) `audit-engine/SKILL.md:381-384` = `allow_dangling_change_ids` 注释块、`:385-388` = `allow_incomplete_checkpoints` 注释块 ⇒ §4 位置列只写 `:385-388` 确实漏掉前者。
- **`e4c206aa` (CR 单席 Major) 抽样复核成立**: 被审 proposal 现为 **469 行**; 抽验 `:82` / `:222` / `:226` / `:230` 四行**全部是空行**, `:92` = 「为什么必须拆 (R1 rework)」、`:96` = `--base` 无缺省、`:114` = fixture 硬约束、`:138` = 两个 `allow_*` 豁免面、`:285` = unattributed trail 行 —— 与 CR 给出的「旧号 → 新号」映射同向。

---

## 审计结论

### Critical (0)

本轮无 Critical。五席**各自独立**抽验 R4 的 14 条 Major / 15 条 minor 的落地形态, 一致结论是**修法全部落在判据本体而非批注** (`d6208ae9`); 其中三条最重的落地 (`b2bc13a6` Level 分布 / `29c39e2c` catalog 绑定 / `4cbe35ce` 归档门 liveness 删子句) 被 backend-architect / qa-engineer / code-reviewer 三席各自写解析器、跑 fixture、跑 `spec_complete.py --gate` 独立复现, 数字与文本逐字吻合。本轮无一条新缺陷构成「方案错误 / 破坏消费方 / SC 恒绿导致假绿」。

### Major (15)

- `4d9ff818` [major] architecture/§3 调用方接缝 — audit-engine 自身入口逻辑 (execution-modes.md:9-10) 第二道启用守卫未处理 — **found_by: tech-lead (1/5)** · conflicted: false
  门与 C.2 之间有**两道**启用守卫: 调用方 `phase-c-integrator/SKILL.md:132` (本 spec §3 已改) 与 audit-engine 自身入口 `execution-modes.md:9-10`「`audit.enabled == false` → 静默返回」/「checkpoint 未启用 → 静默返回」(**全文零提及**, 汇总席 grep 复核: 「静默返回」0 命中 / 「入口逻辑」0 命中)。后者不在 §4 同步表 (`:326` 只列 `:23-82`, 其中 `:15` 是引证不是改动目标)、无 Tasks、无 SC。三重后果: (1) §5 第 7 条 (`:344`) 声称的「行为变更在生产可达」仍未建立 —— 即便 R4 的 `bb0e565f` 改了调用方步骤 3, 场景 B/C 采用方仍会被 `:10` 的字面读法拦在门外; (2) §1.4 `:271`/`:273` 的「生产不可达 (调用方早退)」论证只点了一道守卫; (3) R4 为 `f637d129` 新增的**格 D** 是否可达取决于 `:10` 的两种合法读法 (字面合并视图键 vs 优先级链 + Level) —— 按后者读格 D 成死码, 按前者读格 D 可达, 两读法无 SC 区分。
  *与 `c18eda35` / `4fca2e7a` 的关系*: 三条同属「§3 调用方对齐面没穷举完」, 但指向**三个不同对象** (本条 = audit-engine 自身入口; `c18eda35` = 已改的那道守卫其档位不全; `4fca2e7a` = 产出侧四个调用点), 依规则 4 不合并; 建议一次画全「谁在读同一条链」的清单后合并处置。

- `2555f938` [major] architecture/§1 `--diff-repo-path` 缺省 = fail-open (跨仓漏传即 post_implementation 假绿) — **found_by: tech-lead, backend-architect (2/5)** · conflicted: false
  R4 的 `a00c52bb` 把 S2/S3 都改取锚点面后, `:91` 自述该参数只剩 §1.3 (b) 一个消费点, 而 (b) 在跨仓被禁 ⇒ 它实际只当「跨仓标记」。缺省 = `--repo-path` 是 **fail-open**: 子模块 PR 漏传时 (b) 拿主仓 diff 判 Phase A-only —— 按顺序化 ship (子模块先 merge、gitlink 后 bump), 此刻主仓分支常只有 `openspec/changes/{id}/**` + `.aria/audit-reports/**` ⇒ **`post_implementation` 假绿**, 与被修 bug 同型, 且正落在自称的「pre_merge 主力场景」。两席都点名 `:91` 自认该危害却不设任何机械阻力; tech-lead 补: SC-17(1)-(6) 与 SC-5(5) **全是「显式传」格**, 无一格覆盖漏传, 与 `--base` 因 #137 教训被定为必填 (`:96`) 相比处置不对称。backend-architect 给出低成本机械反证: 要求锚点仓与 diff 仓的 `git rev-parse --show-toplevel` 相同才允许 (b)。
  *severity / type 分歧注*: tech-lead 记 issue/major, backend-architect 记 risk/minor ⇒ 依规则 1 取最高 major; type 1:1 平票按席位序取 tech-lead 的 issue。

- `c18eda35` [major] architecture/§3 步骤 3 调用方链只给三档 — mode ∈ {convergence/challenge/manual} 未定义 (级 2b/2c 生产不可达) — **found_by: code-reviewer (1/5)** · conflicted: false
  §3 把调用方步骤 3 改写为「`checkpoints` 显式值 > `adaptive_rules` 推导值 > 默认 off + adaptive 档取上界」**只有三档**, 未定义 `audit.mode` ∈ {`convergence`, `challenge`, `manual`} 时调用方如何判; 而门侧 §1.3 是**五档** (级 1 / 2a / 2b / 2c / 2d)。对 `{audit:{enabled:true, mode:"convergence"}}` 且无 `checkpoints` 块的采用方 —— 正是 SC-15(5) 的 fixture 与 R3 Critical `7877bac6` 的目标人群 —— 一个合法读法下调用方走「explicit 未命中 → adaptive_rules 不适用 (mode≠adaptive) → 默认 off」⇒ 步骤 3 早退, 门不被调用 ⇒ 级 2b 的修复生产不可达。这与 R4 判 Major 的 `bb0e565f` 是同一失效, 修法只覆盖了 2a 一档; SC-13 新增的接缝 grep 只断言文件含逐字串 `checkpoints 显式值 > adaptive_rules 推导值`, **两个读法都能过**。

- `4fca2e7a` [major] architecture/§3、§5 产出侧四个调用方未对齐 (adaptive 档新纳入 checkpoint 的报告结构上不产出) — **found_by: knowledge-manager (1/5)** · conflicted: false
  §3 只改 pre_merge 调用方, 而**产出侧**四个非排除 checkpoint 的调用点仍是同一句字面键早退 —— `phase-a-planner/SKILL.md:246` / `task-planner/SKILL.md:123` / `phase-b-developer/SKILL.md:255`(+`:49`) / `brainstorm/SKILL.md:141` (汇总席逐条实读命中), 而 `config-loader` 的加载流程不解析 `adaptive_rules`、只与 `DEFAULTS.json` 合并 (八键缺省全 `off`, 汇总席实测)。后果: 本 spec 让门首次把 adaptive 档推导出的 checkpoint 纳入校验 (SC-20(1)(2) 正是这么断言), 但这批 checkpoint 的报告**在生产链上结构性永不产出** ⇒ 场景 B/C 采用方在 pre_merge 拿到 `missing` + `verdict=fail` exit 1 + 消费方 fail-closed = **新的假红硬阻**; 且 ERROR 模板保留的第一条 fix「补跑缺失 checkpoint 审计 (对应 Phase Skill 重新调用)」(`execution-modes.md:76`) 对这批人**不可执行** —— 重新调用只会再次早退。而 §5 (`:336`) 恰恰声明这些调用方「不受影响」, §5 第 7 条把该人群的 `missing` 一律称作「这是修复本身」。方向是 fail-closed (假红不是假绿), 该席按 Rule #10 **不建议 AI 自行放宽放行面**, 主张转 owner 裁 (与复议 #11 同族)。

- `615cb4a5` [major] architecture/§1.4 四格分割证未覆盖 allow_dangling_change_ids 降级路径 (四格皆不成立) — **found_by: qa-engineer (1/5)** · conflicted: false
  R4 新增的「四格互斥与全覆盖证」只按 `enabled_by(pre_merge)` 枚举级 1 / 2a / 2b / 2c / 2d 并把级 3 支出为 `config_unreadable`, 结论「不存在落不进任何一格的输入」。但 §1.1 末段在 R3 新开了**第六种状态**: `allow_dangling_change_ids=true` 且锚点缺失 ⇒「记 `[WARN]` … 跳过 adaptive 推导」。代入官方场景 B (adaptive + 无 `checkpoints` 块, 汇总席实读 `config-example.md` 确认该形态) + 该键 + 拼错 id: 零 explicit ⇒ 纳入集空 ⇒ 进 P5; `pre_merge` 自身同样走级 2a、同样被跳过 ⇒ `resolved(pre_merge)` 与 `enabled_by(pre_merge)` **双双无值**, 而 R3 已把封闭集里的 `default` 档删除 ⇒ 格 A 假、格 B/C/D 判据取不到值 ⇒ **行为未定义**, 与 R4 判 Major `955907f2` 的失效结构同型, 零 SC 覆盖 (SC-7(d) 靠 fixture 含 explicit checkpoint 侥幸绕开)。
  *与 `9d331ca1` 的关系*: 两条都指「分割证不全」, 但一条是**多出一条未枚举的降级路径**, 一条是**把 per-pair 值当标量**, 失效机制不同, 依规则 4 不合并; 建议同批重写分割证时一次覆盖两维。

- `fbe16e0a` [major] implementation/§1.0 求值总序 × §1.1 S4-bypassed × §1.4 四格分割证 (bypass 是否短路未定义) — **found_by: code-reviewer (1/5)** · **conflicted: true** (与 decision `2ee0164c` 结论相反)
  总序表 P0→P6 从未定义「bypass / 短路是否终止求值」。构造实例: `{audit:{enabled:true, mode:"manual", checkpoints:{post_spec:"convergence"}, allow_incomplete_checkpoints:true}}` + 不传 `--change-id`/`--no-spec` + diff 不触 `openspec/changes/**` —— P2 落 S4 ⇒ 按 §1.1 降为 `verdict=bypassed` exit 0; 但 `change_ids=[]` ⇒ 纳入集空 ⇒ **P5 照总序求值格 B/C/D**, `resolved(pre_merge)` 走级 2d 得 `"off"` ⇒ **格 C `pre_merge_not_enabled` exit 2**。R4 新增的分割证明写「不存在落不进任何一格的输入」且唯一豁免是「纳入集非空」, 反把冲突钉死。SC-9(2) 第一跑用的正是这一 config 并断言 `bypassed` / exit 0 ⇒ **两个合法实现判决相反**。SC-9(4) 的 `spec_level_undetermined` 一格同理。
  *conflicted 说明*: backend-architect 的 decision `2ee0164c` 逐字判「P0→P1→P2a→P2→P3(按需)→P4→P5→P6 逐格代入未发现环或不可达 …… S4-bypassed 早退于 P5 之前 ⇒ 无悬空格」—— 即该席把「bypass 短路」当作已定义并据此判自洽, 而 code-reviewer 判该点**恰恰未定义**且两读法判决相反。同 scope、结论相反 ⇒ 依规则 3 **两条并存并标 conflicted, 汇总席不裁决**。可注意的是: 两席都未主张改设计, 分歧只在「§1.0 是否需要补一句短路语义」, 补一句即可同时消解。

- `284459ce` [major] testing/§1.0 fixture 硬约束 (1)(3) × SC-15(4) / SC-21(2) (加 audit 块令兼容映射永不触发) — **found_by: backend-architect (1/5)** · conflicted: false
  `:114` 的两条全称句 (每份 fixture config 必须显式钉 `audit.mode` / 必须显式写 `audit.enabled: true`) 只给格 A (SC-15(1)) 一个 carve-out, 与 Tasks `:378`「逐条给 SC-1~SC-22 的 fixture 补三条硬约束」合起来, 会把 `audit` 块加进两条**判据前提是「无 audit 块」**的 fixture: SC-15(4) 逐字「`{experiments:{...}}` 且无 `audit` 块」、SC-21(2) 触发条件「`experiments.agent_team_audit === true` **且**无 `audit` 块」。该席实读 `config-loader/SKILL.md:311-314`, 兼容映射触发条件 2 逐字是「配置文件中不存在 `audit` 块」(汇总席复核命中) ⇒ 一旦补键, 映射永不触发, 两条 SC 的断言**结构性必红**, SC-21(2) 的「只满足一条 → 不映射」对照格亦失去正例。危害与本文自己反复钉的失效同型: 无人值守下面对必红断言, 最省力的处置就是改断言。

- `52ce53b6` [major] testing/§1.0 硬约束 (1) 未钉 mode 取值 × SC-15(2) / SC-16 (钉 adaptive 则期望值翻转) — **found_by: backend-architect (1/5)** · conflicted: false
  硬约束只要求「必须显式钉 `audit.mode`」却不指定取值, 而 `:121` 的作用域对照表给这批 fixture 统一补「`--change-id x` + 锚点含逐字 `> **Level**: 2` 行」并标注「期望值不随之变化」。代入优先级链实算: 钉 `adaptive` (硬约束 (2) 恰为 adaptive 档准备了 Level 行, 是自然读法) ⇒ 未写的 checkpoint 走级 2a 取 `adaptive_rules.level_2 = "convergence"` (汇总席实测 DEFAULTS 确为该值) ⇒ 纳入集**非空** ⇒ 按 P5「格 B/C/D 只在纳入集为空时求值」, SC-15(2) 期望的 `pre_merge_not_enabled` exit 2 **不可达** (实际落 missing exit 1); SC-16 的三个 checkpoint 同样被纳入且零报告 ⇒ verdict 由 `pass` 翻成 `fail`。钉 `manual` 则两条都成立 ⇒ **两个合法 fixture 判决相反**, 与本文已对 SC-8 处置过的同族缺口未清扫。

- `67f2a651` [major] testing/Tasks B.0 规则 (b2) 的 F-e / F-f 标注仍由被测谓词现算 (SC-2 该两族恒绿) — **found_by: backend-architect (1/5)** · conflicted: false
  `:374` 称对 F-e/F-f「改用两条同样机械、**同样不与被测谓词共享心智**的判据」, 但 F-e 第一合取项 `^{checkpoint}-[0-9TZ:.\-]+\.md$` 与 `:181` 计数表里 `excluded_legacy_count` 的实现判据是**逐字同一串正则**; F-f 的「文件名有 id 段但该 id ∉ `C`」同样是实现侧 `unattributed` 定义的换句话说, 独立源只作用在第二合取项。后果: SC-2 明写「期望值 = 冻结产物里的独立标注, 不得由被测谓词现算」, 而这两族的标注恰恰由被测谓词现算 ⇒ 若实现把 legacy 正则或 `C` 归属规则写错, 标注跟着一起错 ⇒ 该维**恒绿**, B.0 设立的目的落空。SC-4 的手造 fixture 尚能独立证伪两计数分离, 故未升 Critical。

- `66a29a89` [major] testing/SC-2 选样候选 × Tasks B.0 (b1) 双列交叉 (F-b 三份只有散文 context ⇒ 整族剔空) — **found_by: qa-engineer (1/5)** · conflicted: false
  SC-2 `:405` 逐字称候选 `state-scanner-inter-cycle-surfacing`「5/5 全带独立源字段 (frontmatter 可取第一列)」。qa-engineer 逐份实读: 2 份 F-a 带 `change_id:` ✓, 但**3 份 F-b 只有 `context:` 且值是自由散文** (逐字 `context: state-scanner-inter-cycle-surfacing sub-PR (a) — TX.0 + TX.1 prerequisite`), **不是 change_id**; **汇总席已独立复读三份 frontmatter 确认**。B.0 (b1) 逐字「两列不一致 **或** 第一列取不到 ⇒ 整份剔出」, 而全文未定义 prose→id 归一化 ⇒ F-b 归零 < 本轮刚放宽的下界 3, 规则 (c) 又明禁自造样本 ⇒ 无人值守 Phase B 在该族上**再次无合法动作**。该席复算全库仅 3 个 id 满足 F-a≥2 ∧ F-b≥3, 另两个 (`state-scanner-mechanical` / `secret-guard-per-segment-evaluation` 39/39 零字段) 已被 R4 剔出 ⇒ 换 id 亦无解。附带: SC-2 正文仍写「期望值 = 独立**人工**标注归属」, 与 B.0 自述的无人值守机械仲裁互斥。
  *与 code-reviewer decision `c70af7f4` 的关系*: CR 记「独立源字段命中 5/5」、QA 记「其中 3 份的值不是 id」—— 两者事实一致 (字段确实存在), QA 读得更细, **不构成 conflicted** (与 R4 对同族两条的处置一致)。

- `7221bb22` [major] testing/SC-20(7) 逐对不叉乘格的期望值与排除清单互斥 (正确实现必红) — **found_by: qa-engineer (1/5)** · conflicted: false
  该格 config 为 adaptive + 无 `checkpoints` 块, 锚点 b 是 Level 3 ⇒ 按级 2a **每个**未显式写的 checkpoint 取 `level_3='challenge'`; 而排除清单只有四项, `post_brainstorm` 的排除**仍在待 owner 复议 #1、未成文** (汇总席实测 proposal 两处口径均为 4 项) ⇒ 非排除项是四个, 对 b 全部纳入。fixture「目录只放属于 b 的 post_spec 报告一份」⇒ `(post_brainstorm, b)` 无任何 not_applicable 通道 ⇒ 判 `missing` ⇒ **verdict=fail exit 1、`results` ≥2 条**, 与本条断言的「`results` 恰 1 条 / `verdict=pass` exit 0」直接冲突。后果双重: 正确实现必红, 且该条要锁的「不叉乘」不变量因两种实现同样红而**失去鉴别力** (R4 Major `95ddb322` 的修法未闭合)。同族失准: SC-15(5) 的 4 对里 `post_planning` 按 (c) 落 `not_applicable/no-a2-artifact`, 「逐对判 missing」只有 verdict=fail 这半成立。

- `0c3a4660` [major] testing/SC-13 机检清单未覆盖消费方 fail-closed 义务与 §3 步骤 4.5 三态处置 — **found_by: qa-engineer (1/5)** · conflicted: false
  §1.4 的**消费方 fail-closed 义务**「exit≠0 / stdout 非 JSON / `schema_version` 未知 ⇒ 按 `fail` 处置, 不得按 PASS」与 §3 的**步骤 4.5 三态处置**「fail → 阻塞并输出 ERROR; not_applicable → 必带 `[INFO]`; `unattributed_count > 0` → 必带 `[WARN]`」是整个修复在**生产路径**上生效的唯一保障 —— 门只输出 JSON 与 exit code, 不落地这两条则门被调用了也不阻断。该席逐条核 SC-13 的九条 grep, **无一覆盖这两条**; SC-14(b) 的 eval id 3 三条 expectation 亦不含 fail-closed。与本文自己在 R2 为 §1.2b 两条边界立的判据 (「既无落点也无核验 ⇒ 可静默不做」⇒ 补两条逐字 grep) 同一判据、结论相反。

- `7e78199f` [major] testing/AB catalog 的 NEG-1 node id 在真代码不存在 (可执行绑定 5/8 非 6/8) — **found_by: code-reviewer (1/5)** · conflicted: false
  R4 `29c39e2c` 逐条实读了 catalog json, 但**没有核实 node id 指向的方法是否存在**。`NEG-1-malformed` 绑定的 `test_pre_merge_gate.GateCheckTests.test_case_e_malformed_aether_routes_fail` 在全插件树只出现于该 json 一处, 真实方法名是 `test_case_e_malformed_aether_main_leg_routes_fail` (`test_pre_merge_gate.py:266`); 按字面实跑该 node id 得 `FAILED (errors=1)`。**汇总席已 grep + 解析 json 双向复核, 成立**。⇒ 可执行绑定实为 **5/8**、catalog 自身缺口 **3** 条而非 2 条, **待 owner 复议 #9 的裁决数字再次不准** —— 与 R4 刚判 Major 的那句假陈述同一根源 (只读目录不核目标, memory `feedback_author_and_verifier_must_differ_for_corrections`)。本 spec 规定的三条命令按**类**跑仍能覆盖 NEG-1 (qa-engineer 实跑 7/1/1 全 OK), 故不构成假绿, 但缺口枚举与 owner 依据错。

- `e4c206aa` [major] documentation/proposal 全文自引行号 rework 后未回扫 (≥18 处错位, 4 处指向空行) — **found_by: code-reviewer (1/5)** · conflicted: false
  R4 rework 使 proposal 从 397 行增至 **469 行** (汇总席实测), 而内部自引一处未更新; 该席逐条比对给出至少 18 处错位 (`:82`→92 · `:84`→94 · `:86`→96 · `:87`→97 · `:81`→91 · `:103`→114 · `:114`→138 · `:143`→182 · `:186`→225 · `:190`→229 · `:202`→241 · `:220`→259 · `:222`/`:230`→255 · `:243`→285 · `:286`→343), 其中 **line 82 / 222 / 226 / 230 现为空行** (汇总席抽验四行全部确认为空行, 另抽验 `:92`/`:96`/`:114`/`:138`/`:285` 五处新号内容与映射同向)。Phase B 无人值守, 这些是导航指针; rework 记录的「下游同步核对」列了键数、格数、条数、编号面、参数面五轴, **独缺自引行号一轴**。

- `b5f7ca8f` [major] documentation/§5 第 2 条 Step 2 语义反转在 §2/§4 同步面与 SC-13 无落点 (execution-modes.md:41-44) — **found_by: code-reviewer, knowledge-manager (2/5)** · conflicted: false
  §5 第 2 条逐字声明反转 `execution-modes.md:41-44` 的豁免语义 (原义「跳过校验, 继续执行」→ 本 spec「仍逐对评估三态并全部留痕, 只把 missing / S4 降为 bypassed; S3 的输入矛盾错不被豁免」), 但 §2 (`:304`) 与 §4 同步表 (`:321`) 的位置列都只到 `:44` 与 `:82`, **`:42-43` 逐字「→ 跳过校验, 继续执行 pre_merge 审计」没有任何落点** (汇总席实读: `:41` = `Step 2: 豁免检查`, `:43` = 该句)。落地后 SOT 会停在自相矛盾的 Step 2 (「跳过校验」却打印 `missing={cp}@{change_id}` 列表), 而 `execution-modes.md` 是**编排者运行时唯一会读的那份处方**。SC-13 只断言两处 bypass 文案逐字相同, 抓不到这一格。Rule #3 面。

### Minor (15)

- `9d331ca1` [minor] architecture/§1.4 四格分割证把 per-pair 解析当标量 (混合 Level 多 change 落格与格 D {N} 未定义) — **found_by: tech-lead, backend-architect (2/5)**
  `:276` 的互斥与全覆盖证把 `resolved(pre_merge)` / `enabled_by(pre_merge)` 当**标量**三轴, 而 §1.3 明写解析是 per (checkpoint, change_id)。tech-lead 构造: `mode=adaptive` + 四个非排除项显式 off + change A(L1)/B(L2) ⇒ 纳入集空且 `resolved(pre_merge)` 同时为 off 与 convergence ⇒ 落格 B 还是格 D **未定义**。backend-architect 补同族: 格 D 的 `[INFO]` 文案把 `adaptive_rules.level_{N}` 渲染成单值, 采用方自定两档同 off 时混合 Level 多 change 的 `{N}` 无定义。两席同判缺省 `adaptive_rules` 下影响低。正是 memory `feedback_predicate_tiers_need_total_partition_proof` 要求补的那一维。
  *type 分歧注*: tech-lead 记 issue, backend-architect 记 risk ⇒ 1:1 平票按席位序取 issue。

- `2cac2ac0` [minor] implementation/`--repo-path` 的 argparse 必填性未定义 × SC-11 dogfood 命令缺该参数 — **found_by: backend-architect, qa-engineer, code-reviewer (3/5)**
  §1 只给 `--base` 写了「无缺省 (#137 教训), 缺失即 argparse exit 2」, §2 输入参数表给 `repo_path` 只写「pre_merge 必传」, 脚本层是必填还是取 cwd 缺省**全文无一处声明**; SC-10 也只锁 `--base` 缺失与互斥两格。三席一致指出 SC-11 的活体命令逐字只有 `--change-id … --base master`, **不带 `--repo-path`** ⇒ 取必填则本文唯一的活体证据命令直接 exit 2, 取 cwd 缺省则与「锚点面恒主仓根 (子模块合并时不是当前工作目录)」的跨仓契约隐式冲突。backend-architect 另指调用模板 (`:74-78`) 把 `--diff-repo-path` 写成不带方括号的形态, 与 `:91`/§2「缺省 = `--repo-path`」= 可选互斥。
  *category 分歧注*: backend-architect / qa-engineer 记 implementation, code-reviewer 记 testing ⇒ 取多数 implementation。

- `d8d037be` [minor] testing/SC-11 活体命令用裸 master 违「远程跟踪 ref」契约且不断言 WARN 路径 — **found_by: tech-lead, code-reviewer (2/5)**
  `:414` 的唯一活体命令写 `--base master` (裸本地分支名), 与 §1 `:96` 自定的生产契约「必须传远程跟踪 ref」及 R-h 的假红论证直接冲突, 且不断言 R4 新增的 `[WARN] {base|anchor-base} ref 陈旧` 路径。tech-lead 实测本仓 `master == origin/master` (`0483c69`)、`aria` 亦对齐 ⇒ 当下不触 WARN, 属**潜伏不一致**; 但该输出要「抄进 handoff」, 会成为错误的调用范例。处置二选一: 改 `origin/master` 并断言不出 WARN, 或保留 `master` 并断言 WARN 出现。
  *与 `2cac2ac0` 的关系*: code-reviewer 一条 finding 同载两论断, 依规则 7 分别计入两条并互相点名; 两条同处一行命令, 建议一次改完。

- `08acc985` [minor] documentation/基线冻结的行号有效范围未覆盖 phase-a-planner / phase-b-developer 两个编辑目标 — **found_by: tech-lead (1/5)**
  头部 `:9`/`:16` 把行号有效性限定为「代码/规程六文件」+ 五项 carve-out, 而 §4 与 Tasks **以行号点名的编辑目标** `phase-a-planner/SKILL.md:267` 与 `phase-b-developer/SKILL.md:204,277` **不在任一集内**。该席实跑 `git -C aria diff --stat 301641b f314785` 对二者为空、三行逐字同文 ⇒ 事实无误但**声明面有缺口** (同伴轨 #195 R5 major `dbdd80e9` 同型: 冻结面只覆盖代码落点而引用面更宽)。建议把两文件补进已核验集 (tech-lead 已代跑, 结论为空 diff)。

- `00976693` [minor] documentation/§1.0 硬约束标题写「两条」实列三条 (与 Tasks 回扫行「三条」互斥) — **found_by: backend-architect (1/5)**
  `:114` 标题逐字「全部 hermetic fixture 的**两条**硬约束」却列出 (1)(2)(3) (R4 新增第三条时未改标题), 与 Tasks `:378`「补 §1.0 末段的**三条**硬约束」互斥 (**汇总席实读两行确认**)。本文对同类计数漂移的既有处置是就地订正 (SC-5 原稿四条/五条已在 R2 订正), 本处未照办。

- `461840f2` [minor] implementation/§1.3 优先级链表头「对原始 config 求值」与级 2a/2b 读 mode/adaptive_rules 互斥 — **found_by: code-reviewer (1/5)**
  表头逐字写「判据 (对**原始** `.aria/config.json` + 旧配置兼容映射后的视图求值)」, 但级 2a 要读 `audit.adaptive_rules.level_{N}`、级 2b/2c/2d 要读 `audit.mode`。严格 raw 读法下, 合法的最小 config `{audit:{enabled:true}}` (无 `mode`) 会落级 3 ⇒ `config_unreadable` exit 2 硬阻; 只有 §1.0 末段「脚本内联缺省 `mode="adaptive"`」与 §1.4「内联 DEFAULTS audit 子集缺省」才消歧。建议把 raw 视图的适用面收窄到「级 1 的键存在性判定」一处。

- `d1ea7c48` [minor] documentation/§1 `[WARN] base ref 陈旧` 文案的后果描述未随 S2/S3 改锚点面更新 — **found_by: code-reviewer (1/5)**
  文案模板逐字含「merge-base 可能偏移, **S2/S3 的 diff 判据**会被弱化」, 但 R4 `a00c52bb` 已把 S2 与 S3 双双改取锚点面 ⇒ 驱动它们的是 `--anchor-base`, `--base` 轴只剩 §1.3 (b) 通道一个消费点。R-h 与 SC-22(1)(iii) 都已按新轴改写, 唯独 WARN 文案本体没跟着改 —— 而它是要逐字写进实现和 SC 的。

- `77262ffd` [minor] documentation/Tasks Phase D 的 check_bare_issue_refs.py 计数快照过期 (64 实跑 84) — **found_by: code-reviewer, knowledge-manager (2/5)**
  Tasks 写「对本 proposal 今日实跑报 **64** 条裸 `#N` (审计当时 55)」, 两席同日实跑均得 **84** (**汇总席第三次实跑复核 = 84**), 差额来自 R4 rework 自身新增的 72 行 —— 落盘即过期。knowledge-manager 给出体例建议: 该处只留口径与命令 (「实跑该脚本, 数量以当次为准」), 不写死计数, 与版本号一栏已用的「有保质期, 不得照抄」写法一致。code-reviewer 另复核同句里「该脚本未被任何 SKILL.md / state-checks.yaml / standards 引用」**成立**。
  *type 分歧注*: code-reviewer 记 issue, knowledge-manager 记 risk ⇒ 1:1 平票按席位序取 issue。knowledge-manager 的 scope 另含 SC-2 的快照数字, 与 `0520e4aa` 互补。

- `9a046c1f` [minor] testing/unattributed WARN 模板未定义文件名连接符 × SC-4 逐字相等断言 — **found_by: qa-engineer (1/5)**
  §1.2 计数表与 §1.4 trail 行的模板逐字都是 `… N 份 — <按字典序前 20 个文件名>[, … 其余 K 份见 stdout 的 unattributed]`, 但 20 个文件名之间用 `, ` / `,` / 空格哪一种**全文未写**。R4 修 `e83dca40` 时把 SC-4 从 endswith 升级为「对整条 WARN 行逐字相等比对」⇒ 比对目标无法从 spec 推导, Phase B 必须先写实现再回填断言 —— 正是 minor `243ad3d8` 判定的「期望值由实现者按自己的实现重算 ⇒ 反事实失去独立性」形态。

- `6541a212` [minor] documentation/§1.4 格 B 人群 1 与复议 #8 的场景 A 描述算错一键 (实为六键 off + pre_merge) — **found_by: knowledge-manager (1/5)**
  `:263` 与 `:454` 把官方场景 A 写成「`checkpoints` 显式把**七键**写 off、只有 `pre_merge: convergence`」, 两句自相矛盾; **汇总席实读 `config-loader/config-example.md` 场景 A** = **六键 off + `pre_merge: "convergence"`, 共七键**, 且无 `mid_post_spec` 键 (`mode` 为 `"manual"`)。结论 (纳入集空) 不受影响, 但 #8 是请 owner 拍板的条目, 其人群描述算错一键; 同段 SC-15(3) 的逐字 fixture 反而是对的, 两处口径不一。

- `01ad5637` [minor] documentation/§4 同步表 audit-engine/SKILL.md 位置列漏 :381-384 (allow_dangling 注释块) — **found_by: knowledge-manager (1/5)**
  §2 (`:304`) 写「`## 配置依赖` (`:381-388`) **两个** `allow_*` 键的注释各补一句」, 而 §4 (`:322`) 位置列只有 `:385-388` —— **汇总席实读: `:381-384` = `allow_dangling_change_ids` 注释块、`:385-388` = `allow_incomplete_checkpoints` 注释块** ⇒ §4 自述是「Phase B 的照单」, 照单派工会漏改 `allow_dangling` 那半句 (它正是 S1 锚点校验继承该键这条新语义的落点), 与 R4 Major `8acafe0a` 同型。

- `1396abec` [minor] risk · testing/SC-7 / SC-17(4) 的 `--no-spec` 合法格在 adaptive 档真空成立 — **found_by: qa-engineer (1/5)**
  S3 规定 `--no-spec` ⇒ `change_ids=[]` 且「Level 视为 1」, 而 DEFAULTS 实测 `adaptive_rules.level_1 = "off"` (汇总席复核) ⇒ adaptive 档下每个 checkpoint 都解析为 off ⇒ 纳入集空。此时 SC-7 的「全部 `not_applicable/level1-no-spec` + `results` 每条 `change_id is None`」与 SC-17(4) 后半格全是**空集上的全称谓词**, 未实现 S3 的 not_applicable 通道也能绿。两条 SC 只要求 fixture「显式钉 mode」, 未要求钉出非空纳入集。低成本修法: 钉 `mode:'manual'` + 至少一个 explicit 非 off 的 checkpoint, 并加「`results` 非空」前置断言 (memory `feedback_universal_predicate_vacuous_truth_on_empty_set`)。

- `aa1d9dd0` [minor] risk · testing/SC-13 的 execution-modes 切片界 Step 4:/Step 5: 未列入保留项 — **found_by: qa-engineer (1/5)**
  R4 修 `d9578e5d` 后该护栏改为「以 `Step 4:` 行起、`Step 5:` 行止的行区间内计数 `scripts/completeness_gate.py` 恰 1」(SOT 现值实测 `:54` / `:63`, 汇总席复核命中)。但 §2 与 §4 授权的改动正是「Step 4-5 改为调用行 + 三态表 + 契约」, 全文未把「保留两个行首标记」写成约束 ⇒ 若重写把两个 Step 合并, 切片起止**再次无定义** —— 与本轮刚修掉的失效同型。

- `92d7eb81` [minor] risk · testing/Tasks TDD RED 清单 × 未裁复议项决定的 SC 取舍 (无人值守无合法动作) — **found_by: qa-engineer (1/5)**
  Tasks 要求「先把 SC-1~SC-22 写成全红」, 但 SC-18 (复议 #1)、SC-5 的 (b) 通道存废 (复议 #7)、SC-15 的格 B 语义与格 D 存废 (复议 #8)、SC-9(4)+SC-7(d) 的逃生口归属 (复议 #10)、SC-17(5) 的硬阻处置 (复议 #11) 各自逐字写着「裁完 Phase B 只保留其一」, 而全 Tasks **只有版本项挂了「裁定前不动手」的前置门** ⇒ 无人值守 Phase B 面对 SC-18 的「不得两条都不写」既不能两条都写、也不能自行择一 (Rule #10)。建议给 B.0 加一条与版本项同级的「复议 #1/#7/#8/#10/#11 未裁前不进 RED」门。

- `0520e4aa` [minor] risk · testing/活体语料增长对数字类断言的侵蚀 (843 / C=153 / 裸 #N 84) — **found_by: code-reviewer (1/5)**
  顶层语料本轮实测 843 份 (R1 记 786, R4 记 843), `C` 由 152 长到 153, 本 proposal 自身的裸 `#N` 由 64 长到 84。SC-2 / SC-4 / SC-11 的字面数字全靠 B.0 `corpus-freeze.md` 兜底, 而 B.0 的「取样时刻」与 Phase B 实施之间若跨天, 期望值会再次漂移。proposal 已把「语料是活体」成文 (Tasks B.0 item 4), 缓解到位; 记为持续风险, 该席明确不要求改动。

### Decisions (15, 不计入缺陷 severity 计数)

- `d6208ae9` [minor] documentation/R4 的 14 Major / 15 minor 逐条落进正文 (非批注) — **found_by: tech-lead, backend-architect, knowledge-manager (3/5, 另 qa-engineer / code-reviewer 以逐条实跑形式各自佐证)**
  本轮最重要的正面结论。tech-lead 抽验七条 (`955907f2` 格 B 第四合取项整条删除 + 新增分割证 / `f637d129` 新增格 D / `a657bf0a` 新增 P2a / `a00c52bb` S2 改锚点面 / `8acafe0a` 占位来源表 + §2 五项 / `4cbe35ce` SC-12 删 liveness 子句 / `29c39e2c` AB 拆三条命令); backend-architect 逐条抽验 14 Major + 15 minor 全部在正文落地并复核 R4 引用的外部事实全为真; knowledge-manager 抽验四条并实跑 `spec_complete.py --gate` 复现 `verdict=pass` 零符号分类。三席一致: **无一条以批注形式敷衍**; `7127ab68` / `aebd2f9f` 按 Rule #10 转 待 owner 复议 #11/#12, **未自行放宽放行面**。
  *category 分歧注*: knowledge-manager 记 testing, 另两席记 documentation ⇒ 取多数 documentation。

- `6292d37d` [minor] implementation/Level 解析统计与分布复算 (58/85/1 · 失败 9 · 首命中 >15 恰 7 · 行首 139-3-2-0 · Spec Level 15) — **found_by: backend-architect, qa-engineer, code-reviewer (3/5)**
  三席各自独立实现 §1.3 三条判据的解析器对 153 份 proposal 实跑, 结果**逐项一致**: 剥删除线 L3 58 / L2 85 / L1 1, 不剥 57/86/1, 唯一取值不同的文件 = `archive/2026-08-16-premerge-gate-branch-existence`; 失败 9 份且与点名清单同集; 首命中 >15 恰 7 份且行号逐一相同 (最深 `a1-entry-claim-duplicate-work-guard` L58); 行首形态 139/3/2/0; 含 `Spec Level` 15 份。⇒ **R4 的 4 席 Major `b2bc13a6` 已真正落进判据本体且订正后的数字属实**。
  *category 分歧注*: qa-engineer 记 testing, 另两席记 implementation ⇒ 取多数 implementation。

- `c70af7f4` [minor] testing/ab-suite catalog 8 条绑定与拆出的三条命令实跑 (4+1+1+2 / 7·1·1 tests OK) — **found_by: qa-engineer, code-reviewer (2/5, 另 backend-architect / knowledge-manager 在 R4 落地核验中各自复核同一结构)**
  四席各自解析 `ab-suite/phase-c-integrator-pre-merge-gate.json`: `type=workflow_skill_subextension`、无 `evals` 键、8 fixtures, 绑定分布 `GateCheckTests` 4 / `NotFoundVerdictTests` 1 / `test_path_coverage.InternalErrorReasonTests` 1 / 无 node id 2 —— 逐条一致 (汇总席复核命中)。qa-engineer 另把 Tasks 拆出的三条命令逐条实跑得 7 / 1 / 1 tests 全 OK ⇒ **R4 `29c39e2c` 的订正可执行**。
  *与 `7e78199f` 的关系*: 本条确认的是「绑定分布与三条命令」这一层; code-reviewer 在同一 json 上多走一步 (核 node id 指向的方法是否存在) 才发现 NEG-1 那条名字过期。两层结论互不否定, **不构成 conflicted**。

- `e87f97bd` [minor] testing/SC-12 既有测试基线三套件全绿 (104 / 148 / 1593) — **found_by: qa-engineer (1/5)**
  实跑 `audit-engine/tests` 104 tests OK · `phase-c-integrator/tests` 148 tests OK · `state-scanner/tests` 1593 tests OK, 0 failure ⇒ **无既有失败项需 carve-out**。同时复核 R4 `4cbe35ce` 的处置前提: `spec_complete.py:1642` 逐字「两文件皆缺 (proposal-only) → 零评估早退」, `:924-930` 的 liveness 分类器在本 cycle 不运行。**该 id 与 R4 同 id, 是本轮与上轮字面相等的两条之一**。

- `17417aee` [minor] documentation/语料事实底盘独立复算 (顶层 843 / 末段族 62 / unattributed 170·160 / legacy 6 / C=153) — **found_by: backend-architect, qa-engineer, code-reviewer (3/5)**
  三席各自全枚举 `.aria/audit-reports/`, 数字逐项一致: 顶层 **843** 份 `.md` (R4 记 837 → 本轮 843, 语料活体)、真 2-field legacy **6**、unattributed 全 8 checkpoint 口径 **170** / 本仓 2-checkpoint 口径 **160**、末段族 **62**、`C` = **153** (8 changes + 145 archive)、子目录恰 `wf-r1fix` / `pr19-submodule-scan` 两个。qa-engineer 另核 `*-audit-trail.md` 恰 5 且与 §1.2b 逐字同集、前缀碰撞 1 对 / 后缀 0 / 中缀 0。
  *category 分歧注*: backend-architect 记 implementation, 另两席记 documentation ⇒ 取多数 documentation。

- `09602bb8` [minor] documentation/SOT 行号引用抽验零漂移 (逐条实读, 无一错格) — **found_by: qa-engineer, code-reviewer, knowledge-manager (3/5)**
  code-reviewer 做了本轮最广的一次: `execution-modes.md` 全组 · `audit-engine/SKILL.md` 全组 · `phase-c-integrator/SKILL.md` 全组 · `report-storage.md` · `pre-write-validation.md` · `report-format.md` · `collectors/audit.py:52,62-69` · `spec_complete.py:924,1642` · `config-loader` 全组 · `standards` 四文件 · 三份先例 proposal —— **逐条命中, 无一错格**; qa-engineer 与 knowledge-manager 各自独立抽验约 30 处, 结论相同 (含 `execution-modes.md` 围栏 `:34`/`:66`、Step 1-5 落 `:37/:41/:46/:54/:63`、`:152` 逐字含「机械护栏 SC-17 计数恰 2」、`:185` 防 vacuous-true 句)。⇒ **R4 minor `db4cd4eb` / `d9578e5d` 的勘正已落地且正确**。

- `122aed36` [minor] architecture/§5 消费方枚举与向后兼容零破坏 (零代码消费方 / collectors/audit.py:62-69 / state-checks 零命中) — **found_by: tech-lead, backend-architect (2/5)**
  两席各自 grep 而非采信 §5: 全插件树 `.py/.json/.yaml` 对 `allow_incomplete_checkpoints` / `missing_checkpoint` **零命中** (出现面只有三份 `.md`); 文件名 schema 的唯一代码消费方 = `state-scanner/scripts/collectors/audit.py:52,62-114` (`_CHECKPOINT_PREFIX = re.compile(r"^[^-]+-")` + 单侧合成首连字符), dashboard 侧走 glob + frontmatter + 文件名 fallback; `.aria/state-checks.yaml` 16 条 check 对 audit-engine / audit-reports 零命中。⇒ 本 spec 只读文件名、不动 writer schema ⇒ **消费方破坏面为零**。

- `9344c3a0` [minor] documentation/基线冻结与版本面实测 (六文件零 diff / {timestamp} 残留 4 处 / gitlink f314785 = v1.73.0 / 主仓 16 版本点) — **found_by: tech-lead, backend-architect, code-reviewer, knowledge-manager (4/5)**
  四席交叉复核, 无一分歧: `git -C aria diff --stat 301641b f314785 --` 对六个代码/规程文件**输出为空** (backend-architect 另用 md5 对四文件与插件缓存副本比对全 MATCH); 四处旧 schema `{timestamp}` 残留在 `f314785` 上仍逐字落 `phase-a-planner:267` / `phase-b-developer:204,277` / `phase-c-integrator:157`, 全树计数**恰 4**; gitlink `git ls-tree HEAD aria` = `f314785` = v1.73.0, `submodule status` 无 `+`, 最高 tag `v1.73.0` (`v1.71.2`/`v1.72.0` 未被占但已过号), `aria/VERSION` 与 `plugin.json` 均 1.73.0, `ab-suite/version.yaml` 1.5.0; 主仓 **16** 个版本字符串点逐点实读全部在场且现值一致 (README×4 共 11 + `VERSION:24` + `CLAUDE.md:139,141` + `system-architecture.md:189` + `version-scheme.md:23`)。
  *category 分歧注*: tech-lead 记 architecture, 另三席记 documentation ⇒ 取多数 documentation。

- `34f4c7b6` [minor] architecture/越界面: 同伴在飞轨 #195 与本 spec 零代码交叠 — **found_by: tech-lead, knowledge-manager (2/5)**
  `openspec/changes/` 下 8 个在飞目录; 同伴轨 `handoff-multibranch-subdir-path-fidelity` 仍在飞 (538 行, 「待 owner 复议 6」今日实读落 `:510`, 推荐 MINOR v1.74.0), 其落点为 state-scanner collectors/scan/latest_md_writer 与 phase-d-closer, **与本 spec 触点零交叠**; 共享面仅版本号与 `ab-suite/version.yaml`。本 spec 对 `phase-a-planner` / `phase-b-developer` 只做 1 行 `{timestamp}` 勘正, 未触 phase1_gate / claim_lifecycle / spec-drafter / AB 套件本体。
  *category 分歧注*: knowledge-manager 记 documentation, tech-lead 记 architecture ⇒ 1:1 平票按席位序取 architecture。

- `f0bc7287` [minor] architecture/根因覆盖与候选方案取舍成立 (A/C/D 否决理由实读成立) — **found_by: tech-lead (1/5)**
  两层根因各有对应修法 (匹配面无 change 维度 → §1.2 双侧/末段界定 + 对称有界包含排除; change_id 在 pre_merge 无输入 → §3 pre_hook 五参数 + §2 输入表)。否决理由经实读成立: A 无法写 hermetic 红转绿且不解根因 2; D 的 frontmatter 形态不统一 (837 份中 255 份无任一独立字段); C 需新 config 键而 F8 注册面缺口实测存在 (`DEFAULTS.json` audit 键集无两个 `allow_*`, 汇总席复核命中)。

- `1605510e` [minor] implementation/归属谓词假绿方向实测 (843 份无一多归 / 441 份独立源 0 分歧) — **found_by: backend-architect (1/5)**
  对 843 份语料按规则 1-3 全枚举, **无一份**被归给 >1 个 change_id; 再用与文件名无关的独立源 (frontmatter `context:` / `spec_id:` / `change_id:`) 对 **441** 份可解析报告交叉比对, 名匹配归属与独立源归属 **0 分歧** ⇒ 「末段界定 + 对称有界包含排除」在真实语料上**无误归实例**, 残余理论口子在本仓被 F3 的「后缀碰撞 0 对」结构性堵住。这是本轮对修法正确性最强的一条正面证据。

- `2ee0164c` [minor] architecture/§1.0 求值总序自洽性 (P0→P6 无环无悬空格) — **found_by: backend-architect (1/5, 正文条目, 依合并规则 6 纳入)** · **conflicted: true** (与 `fbe16e0a` 结论相反)
  该席逐格代入 P0→P1→P2a→P2→P3(按需)→P4→P5→P6, 判「未发现环或不可达」: `--no-spec` 经 P2a 保证锚点面 diff 非空且不触 `openspec/changes/**` ⇒ S2 必空 ⇒ S3 必被求值 (first-match 契约不动); lazy P3 对格 B/C/D 需要的 `resolved(pre_merge)` 仍会触发; **S4-bypassed 早退于 P5 之前** ⇒ 无「需要 Level 却取不到」的悬空格。code-reviewer 的 `fbe16e0a` 恰恰判「bypass 是否短路**未定义**」并给出两读法判决相反的可构造实例。⇒ 同 scope、结论相反, **汇总席依规则 3 保留双方并标 conflicted, 不裁决**。

- `94c5803e` [minor] architecture/error_kind 九项封闭集穷举无未定义出口 — **found_by: backend-architect (1/5, 正文条目, 依合并规则 6 纳入)**
  九项对本文列出的全部失败路径一一对应 (坏 JSON / 未知 mode → `config_unreadable`; `enabled != true` → `audit_not_enabled`; P2a 两格 → `no_spec_unverifiable`/`no_spec_contradicted`; S1 → `change_id_unanchored`; S4 → `change_scope_unresolved`; Level → `spec_level_undetermined`; 格 C → `pre_merge_not_enabled`; git → `git_failed`), argparse 两格由「stdout 非 JSON ⇒ 按 fail」兜住, 报告目录缺失走 `scan_status=dir_missing` 而非 error ⇒ **无未定义出口**。

- `7560bcd5` [minor] documentation/头部 Linked Issue 字段过 spec-drafter 机械判据 — **found_by: knowledge-manager (1/5)**
  实跑 SOT `lib/linked_issue_field.extract_linked_issue_field` 得 `verdict=OK` / `line_no=6` / `token_elements=('10CG/Aria#199','10CG/aria-plugin#161')`; 仓级探针全仓 OK 且本 spec **不在** grandfathered 白名单 ⇒ 写法三条 (code span / 同 span 逗号分隔 / 无 markdown 链接形) 全合规。**该 id 与 R1-R4 同 id, 是本轮与上轮字面相等的两条之一 (四轮持存)**。

- `8bf95e90` [minor] documentation/被引 issue / memory / 归档先例真实性 — **found_by: knowledge-manager (1/5)**
  forgejo API 复核 `10CG/Aria#199` = open、`10CG/aria-plugin#161` = open 且标题与头部逐字相符; 四条被引 memory 文件全部在场; 归档先例 `2026-08-23-pre-merge-gate-no-run-for-branch:228`(catalog 登记 fixture) `:284`(「照跑 = 测量剧场」) 与 `2026-09-04-sibling-spec-probe:513`(分块计数先例) `:544`(测试宿主与 run_all_tests 发现) 逐字命中。

---

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **15** / Minor **15** (缺陷类 = issue + risk; 另有 15 条 minor decision 不计入)。

rationale: 按 `report-storage.md §Verdict` 计算, 0 Critical + ≥1 Major ⇒ **PASS_WITH_WARNINGS**。post_spec 的阻塞行为是 `blocking: false` (report-format.md 阻塞行为表), 本判定不阻断流程; 按 Rule #10 该判定不得由 AI 自行升降。

**本轮的形状: verdict 与上轮持平, 事实面进一步变干净, 但缺陷总量不降反升 (R4 29 → R5 30), 收敛未发生。**

- **五席全部换了新席位、全部不继承上轮结论, 却给出同一个正面结论**: R4 的 14 Major / 15 minor **逐条落在判据本体而非批注** (`d6208ae9`), 且其中最重的三条被三席各自独立实跑复现 —— Level 解析器五组数字逐项吻合 (`6292d37d`)、AB catalog 绑定与三条命令可执行 (`c70af7f4`)、归档门 liveness 删子句的前提经 `--gate` 实跑确认 (`e87f97bd`)。事实面本轮**无一条断言被证伪**: 语料底盘四类计数三席一致 (`17417aee`)、SOT 行号约 40 处逐条命中零漂移 (`09602bb8`)、消费方枚举零破坏 (`122aed36`)、基线冻结与 16 个版本点四席交叉命中 (`9344c3a0`)、归属谓词在 843 份真实语料上 0 误归 (`1605510e`)。这是五轮以来事实面最干净的一版, 故 **0 Critical**。
- **但十五条 Major 中至少十一条是「R4 修法自身的下游未闭合」**: `4d9ff818` / `c18eda35` / `4fca2e7a` (R4 `bb0e565f` 只对齐了三道守卫中的一道、且那一道的档位不全、且没扫产出侧)、`2555f938` (R4 `a00c52bb` 收窄参数用途后没收紧缺省语义)、`615cb4a5` / `fbe16e0a` (R4 新增的分割证漏掉一条降级路径、又与 S4-bypassed 撞车)、`284459ce` / `52ce53b6` (R4 新增第三条 fixture 硬约束时没给两条「必须无 audit 块」的 SC 开 carve-out、也没钉 mode 取值)、`66a29a89` / `67f2a651` (R4 重写的 B.0 仲裁规则在真实语料上把候选族剔空、且自称的「独立标注」仍由被测谓词现算)、`7221bb22` (R4 新增的 SC-20(7) 与自定的排除清单互斥)。**这是本 spec 连续第四轮出现同一模式** (memory `feedback_rework_leaves_downstream_ac_drift` / `feedback_spec_rework_leaves_downstream_ac_drift`)。
- **另有两条是「勘正动作自身再次漏核」**: `7e78199f` (R4 逐条读了 catalog json 却没核 node id 指向的方法是否存在, 6/8 实为 5/8, owner 复议 #9 的数字**第二次不准**) 与 `e4c206aa` (rework 增 72 行后自引行号一处未回扫, 4 处指向空行)。两条与 R4 已点名的 memory `feedback_author_and_verifier_must_differ_for_corrections` 同型 —— **勘正批建议第三次换非执笔者复核**。

四组最值得优先处置的:

1. **调用方接缝三条 (`4d9ff818` + `c18eda35` + `4fca2e7a`)**: 三席各自从不同方向发现「谁在读同一条优先级链」这张清单没穷举完 —— 一条守卫全文零提及、一道守卫只补了 5 档中的 2 档、产出侧四个调用点根本没扫。三条合看的后果是本 spec 的中心声称 (「修复在生产路径可达」) 仍未建立, 而 `4fca2e7a` 更指出对场景 B/C 采用方可能**制造新的假红硬阻**。建议一次画全清单再改, 不要逐条打补丁。
2. **fixture 前提三条 (`284459ce` + `52ce53b6` + `92d7eb81`)**: 全部会在无人值守 Phase B 直接产出**结构性必红**的断言, 而本 spec 自己反复钉的失效模式正是「必红断言逼实施者改断言」。修法成本极低 (两个 carve-out + 钉一个 mode 取值 + 一条前置门)。
3. **SC-2 语料两条 (`66a29a89` + `67f2a651`)**: R1 Critical-1 的封口 (两个计数分离必须有真实语料佐证) 在本轮被两个方向同时削弱 —— 唯一候选被 (b1) 的逐字规则剔空, 剩下两族的标注又由被测谓词现算。这是唯一一处「修了两轮仍未站住」的证据面。
4. **`7e78199f` + `e4c206aa` 两条勘正类**: 都在给 owner 与 Phase B 提供**错误的导航依据** (复议 #9 的数字、18 处自引行号), 修法都是机械动作, 但必须换人执笔核。

十五条 Minor 的共性: 九条是「R4 新写的条款缺一条断言 / 缺一处回灌 / 少写一个位置」(`9d331ca1` / `2cac2ac0` / `d8d037be` / `00976693` / `461840f2` / `d1ea7c48` / `9a046c1f` / `01ad5637` / `aa1d9dd0`), 三条是**勘正自身写错**或**快照数字过期** (`77262ffd` 64→84 / `6541a212` 七键实为六键 / `08acc985` 冻结声明面漏两文件), 修法成本普遍是一句话或一条 SC。

计算依据:
- Critical issues: 0
- Major issues: 15 (15 issue + 0 risk)
- Minor issues: 15 (11 issue + 4 risk)
- Decisions (不计入): 15
- Conflicted 对: 1 (`fbe16e0a` ↔ `2ee0164c`)

---

## 轮次记录

### Round 5

- Agents: 5/5 (tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager) —— 无缺席, `round_incomplete: false`, `skipped_agents: []`; frontmatter 15/15 字段齐全 5 份, **0 份需补齐**
- Sibling probe: **本轮已完整扫描, 未发现同 issue 竞品** (五席各自独立报同一结论; tech-lead 与 knowledge-manager 另实读同伴在飞轨 `handoff-multibranch-subdir-path-fidelity` 的 `:510`, 确认与本 spec 触点零交叠)
- Conclusions: 45 (去重前 61 = 58 条席位结构化条目 + 3 条依合并规则 6 从 backend-architect 正文纳入) —— Critical 0 / Major 15 / Minor 15 / Decisions 15
- Delta vs 上轮: 上轮 40 keys, 本轮 45 keys, **字面交集 2 条** (`7560bcd5` 头部 Linked Issue decision 四轮持存; `e87f97bd` SC-12 三套件全绿 decision 两轮持存) ⇒ `stable_vs_prev: false`。R4 的 14 条 Major 去向: **判真闭合 6 条** (`b2bc13a6` Level 分布已订正为 58/85/1 且三席复现 → `6292d37d`; `4cbe35ce` SC-12 liveness 子句已删且前提经 `--gate` 实跑确认 → `e87f97bd`; `29c39e2c` catalog 拆三条命令已可执行 → `c70af7f4`; `8acafe0a` 五参数已进 §2/§4/Tasks; `01b9faf6` P3 已改按需解析; `b451a016` 第三条 fixture 硬约束已新增); **修法留下下游 9 条** (`bb0e565f` → 派生 `4d9ff818`+`c18eda35`+`4fca2e7a`; `a00c52bb` → 派生 `2555f938`; `955907f2`+`f637d129` 的分割证 → 派生 `615cb4a5`+`9d331ca1`+`fbe16e0a`; `b451a016` 的硬约束 → 派生 `284459ce`+`52ce53b6`+`00976693`; `2370f1f9`+`6c4455bd` 的 B.0 仲裁 → 派生 `66a29a89`+`67f2a651`; `95ddb322` 的 SC-20(7) → 派生 `7221bb22`; `29c39e2c` 的 catalog 勘正 → 派生 `7e78199f`); **本轮未再被提出 2 条** (`a657bf0a` S2/S3 求值序 —— P2a 前置已封; `7127ab68` 跨仓硬阻 —— 已转 待 owner 复议 #11)。R4 的 15 Minor 中 5 条 (`db4cd4eb` 先例锚注 / `d9578e5d` 切片界定 / `642c9e5e` 调用模板 / `03d241c7` 守卫引述 / `2f664130` checkpoint 枚举) 经 `09602bb8` 与 `d6208ae9` 确认已落地, 本轮未再出现。conflicted 对: R4 = 0, **本轮 = 1**
- Vote 票型: REVISE 5 / PASS 0 ⇒ `unanimous_pass: false`
  - 单席 verdict: PASS_WITH_WARNINGS **5/5** (tech-lead C0M2m3 / backend-architect C0M3m3 / qa-engineer C0M4m5 / code-reviewer C0M5m4 / knowledge-manager C0M2m3) —— 连续第二轮五席自判 verdict 全部一致且无 FAIL, 但五席仍全部投 REVISE, 理由高度同构: 「Major 均为『无人值守 Phase B 会变成结构性必红一条, 或两个合法实现判决相反』, 且都可在正文内当场闭合、不需重开设计」
  - 计数口径注: code-reviewer 自报「Minor 4 (另 1 条 risk 不计入)」, 本聚合按 R1-R4 一贯口径 (缺陷类 = issue + risk) 计其为 5; backend-architect 自报「Minor 3」未含其正文第二条 risk (该 risk 依规则 1 已并入 `2555f938`)。
- Duration: N/A (编排脚本未提供计时)

---

## 统计

| 指标 | 值 |
|------|-----|
| 总轮次 | 5 |
| 总耗时 | N/A |
| Agent 参与率 | 5/5 (缺席 0) |
| Frontmatter 契约完整率 | 5/5 (15/15 字段齐全, 0 份需补齐) |
| 去重前/后 conclusions | 61 / 45 |
| Critical / Major / Minor (缺陷类 = issue + risk) | 0 / 15 / 15 |
| 其中 issue / risk | 26 / 4 |
| Decisions (不计入缺陷计数) | 15 |
| Conflicted 对 | 1 (`fbe16e0a` ↔ `2ee0164c`) |
| 5/5 全席独立命中 | 0 finding + 0 decision |
| 4/5 席命中 | 0 finding + 1 decision (`9344c3a0`) |
| 3/5 席命中 | 1 finding (`2cac2ac0`) + 4 decisions (`d6208ae9` / `6292d37d` / `17417aee` / `09602bb8`) |
| unanimous_pass | false |
| stable_vs_prev (四元组集合逐条相等) | false (40 vs 45, 字面交集 2 条) |
| converged | false (集合不等 且 unanimous_pass=false) |
| 收敛轮次 | N/A |

---

## Rework 清单

按 severity 排序; critical / major 逐条列出。**汇总席只列动作建议, 不代替 owner 与 Phase B 实施者裁决** —— 标 `待 owner 复议` 的按 Rule #10 不得由 AI 自行处置。

| # | id | severity | 席位 (found_by) | 建议动作 |
|---|----|----------|-----------------|----------|
| 1 | `4d9ff818` | major | tech-lead (1/5) | §4 同步表与 Tasks 补 `execution-modes.md` **入口逻辑** (`:9-10`) 这一触点, 把「checkpoint 未启用」的解析语义与门侧 / 调用方钉成同一条优先级链 (三处一致); 随后决定 §1.4 `:271`/`:273` 的「生产不可达」论证与 §5 第 7 条是否同批改写、格 D 存废是否随之定。**与第 3、4 项合并成一张「谁在读同一条链」清单一次处置**。汇总席已实读复核 `:5/:9/:10/:15` 与 proposal 内 0 命中 |
| 2 | `2555f938` | major | tech-lead, backend-architect (2/5) | pre_merge 下把 `--diff-repo-path` 提为必填 (同仓显式等于 `--repo-path`), 把静默假绿变成 argparse exit 2; 或采纳 backend-architect 的机械反证 (锚点仓与 diff 仓 `git rev-parse --show-toplevel` 相同才允许 (b) 通道)。补一条 SC 覆盖「跨仓形态漏传」并回灌 R-e (`:361`) —— 现在 R-e 只覆盖「跨仓显式传」那一格 |
| 3 | `c18eda35` | major | code-reviewer (1/5) | §3 调用方步骤 3 的优先级链补齐到与门侧 §1.3 同样的五档 (至少定义 `mode` ∈ {convergence, challenge, manual} 时的行为), 并把 SC-13 那条接缝 grep 改成能区分两个读法的形态 (现在两读法都能过)。与第 1、4 项同批 |
| 4 | `4fca2e7a` | major | knowledge-manager (1/5) | **待 owner 复议** (属放行面变更, 建议并入复议 #11): (a) 把「adaptive 档新纳入的 checkpoint 其报告在产出侧结构上不产出」作为 §5 新增一条成文, 并把 ERROR 模板的第一条 fix 改成对该人群**可执行**的措辞 (「在 `audit.checkpoints` 里显式写该 checkpoint」); (b) 由 owner 裁「产出侧四个调用点 (`phase-a-planner:246` / `task-planner:123` / `phase-b-developer:255` / `brainstorm:141`) 是否随本 spec 一起对齐」。汇总席已逐条实读四个调用点与 DEFAULTS 八键全 off |
| 5 | `615cb4a5` | major | qa-engineer (1/5) | §1.4 分割证补第六种状态 (`allow_dangling_change_ids=true` + 锚点缺失 ⇒ 跳过 adaptive 推导) 的落格: 该状态下 `resolved(pre_merge)` / `enabled_by(pre_merge)` 双双无值, 需显式指定归入哪一格或新开一格; 并补一条 SC (fixture 不得含 explicit checkpoint, 否则又被侥幸绕开)。**与第 6、第 16 项 (`9d331ca1`) 同批重写分割证, 一次覆盖三维** |
| 6 | `fbe16e0a` | major | code-reviewer (1/5) · **conflicted** | §1.0 求值总序补一句短路语义: bypass / 早退是否终止后续 P 阶段。二选一并成文 —— (a) S4-bypassed 短路返回 (则分割证的「纳入集非空」豁免需追加「或已 bypassed」); (b) 不短路 (则 SC-9(2) 的期望值须改为格 C exit 2)。**注意本条与 decision `2ee0164c` 标记为 conflicted, 汇总席不裁决**; 补这一句可同时消解两席分歧 |
| 7 | `284459ce` | major | backend-architect (1/5) | §1.0 硬约束 (1)(3) 的 carve-out 清单补上 SC-15(4) 与 SC-21(2) 两格 (判据前提是「无 `audit` 块」, 加键即令兼容映射永不触发), 并同步 Tasks `:378` 的回扫清单。汇总席已实读 `config-loader/SKILL.md` 触发条件 2 逐字「配置文件中不存在 `audit` 块」 |
| 8 | `52ce53b6` | major | backend-architect (1/5) | §1.0 硬约束 (1) 从「必须显式钉 `audit.mode`」改为**钉死取值** (对 SC-15(2) / SC-16 建议 `manual`), 或逐条给出该 SC 的 mode 取值与随之而来的期望值。汇总席已实测 DEFAULTS `adaptive_rules.level_2 = "convergence"` ⇒ 钉 adaptive 确会翻转两条 SC 的期望值 |
| 9 | `67f2a651` | major | backend-architect (1/5) | Tasks B.0 (b2) 二选一: (a) 给 F-e / F-f 换一条**真正独立**的标注源 (不复用实现侧的 legacy 正则与 `C` 归属模型); (b) 把 (b2) 自述的「不与被测谓词共享心智」改写成实情, 并在 SC-2 里显式声明这两族只测「分类不串台」不测「判据本身正确」。现状是自述强度高于实际 |
| 10 | `66a29a89` | major | qa-engineer (1/5) | B.0 (b1) 补 prose→id 归一化规则 (或给 frontmatter 与 git 历史两个来源定序), 否则 `state-scanner-inter-cycle-surfacing` 的 3 份 F-b 会被逐字规则整族剔空、下界 3 不可满足而规则 (c) 又禁自造样本; 同时把 SC-2 正文残留的「独立**人工**标注」改成与 B.0 一致的机械仲裁措辞。汇总席已逐份复读三份 frontmatter 确认只有散文 `context:` |
| 11 | `7221bb22` | major | qa-engineer (1/5) | SC-20(7) 的期望值按本文自定的排除清单 (4 项, `post_brainstorm` **未**排除) 重算 —— 现状下正确实现必得 `verdict=fail` + `results` ≥2 条; 二选一: 改期望值, 或在 fixture 里显式把 `post_brainstorm` 置 off。顺带订正 SC-15(5) 的「4 对逐对判 missing」(其中 `post_planning` 实落 `not_applicable/no-a2-artifact`)。**注意 `post_brainstorm` 的排除仍在复议 #1, 未裁前不得自行加进排除清单 (Rule #10)** |
| 12 | `0c3a4660` | major | qa-engineer (1/5) | SC-13 补两条逐字 grep, 分别锁 §1.4 的消费方 fail-closed 义务 (写进 `execution-modes.md`) 与 §3 步骤 4.5 的三态处置 (写进 `phase-c-integrator/SKILL.md`) —— 与本文 R2 为 §1.2b 两条边界所立的判据同一处置。这两条是全设计在生产路径生效的唯一保障, 现状可静默不做 |
| 13 | `7e78199f` | major | code-reviewer (1/5) | 订正三处: 可执行绑定 **5/8** (非 6/8)、catalog 自身缺口 **3** 条 (非 2 条)、`NEG-1-malformed` 的 node id 名过期 (真代码为 `test_case_e_malformed_aether_main_leg_routes_fail`, `test_pre_merge_gate.py:266`)。**待 owner 复议 #9 的裁决依据须随之重给 (第二次)**; 该 catalog 的 node id 修不修属 aria-plugin-benchmarks 侧, 建议一并请 owner 定。**按 memory `feedback_author_and_verifier_must_differ_for_corrections`, 本条勘正须由非 R4 执笔者执行**。汇总席已 grep + 解析 json 双向复核 |
| 14 | `e4c206aa` | major | code-reviewer (1/5) | 对 469 行全文做一次自引行号回扫 (至少 18 处错位, `:82`/`:222`/`:226`/`:230` 四处现指空行), 并把「自引行号」补进 rework 记录的下游同步核对轴 (现有五轴: 键数 / 格数 / 条数 / 编号面 / 参数面)。**建议改用锚点式引用 (小节名 + 逐字串) 替代行号自引**, 以免第六轮再犯。汇总席已抽验四处空行 + 五处新号内容 |
| 15 | `b5f7ca8f` | major | code-reviewer, knowledge-manager (2/5) | 把 `execution-modes.md:41-43` (Step 2 正文「跳过校验, 继续执行 pre_merge 审计」) 列进 §2 与 §4 同步表的改动面 (与 `:44` 同批改), 并给 SC-13 加一条逐字 grep 锁新措辞。否则落地后 SOT 的 Step 2 会自相矛盾 (「跳过校验」却打印 missing 列表), 而这是编排者运行时唯一会读的处方 (Rule #3 面)。汇总席已实读 `:41`/`:43` 逐字 |

Minor 15 条与 Decisions 15 条不入 rework 清单, 随稿修订即可。其中六条建议优先随手闭合 (成本一句话或一处改写, 且汇总席已代为实测): `77262ffd` (裸 `#N` 实为 **84**, 建议改成只留口径与命令、不写死计数)、`6541a212` (官方场景 A 实为**六键 off + `pre_merge: convergence`**, 复议 #8 的人群描述须订正)、`01ad5637` (§4 位置列补 `:381-384` 的 `allow_dangling` 注释块)、`00976693` (`:114` 标题「两条」改「三条」, 与 Tasks `:378` 对齐)、`08acc985` (`:16` 的行号有效范围补进 `phase-a-planner/SKILL.md` 与 `phase-b-developer/SKILL.md`, tech-lead 已代跑为空 diff)、`d1ea7c48` (`[WARN] base ref 陈旧` 文案里的「S2/S3 的 diff 判据」改为「§1.3 (b) 通道」)。

另按 memory `feedback_author_and_verifier_must_differ_for_corrections`: 本轮再次出现**勘正动作自身漏核** (`7e78199f` 只读目录不核目标 —— 与 R4 同根因第二次) 与**勘正后未回扫** (`e4c206aa`), **本轮的勘正批建议第三次换非执笔者复核**, 且把「自引行号」与「node id 指向的方法是否存在」两轴写进回扫清单。
