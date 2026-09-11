---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-10T21:56:43.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [backend-architect]
---

# post_spec R5 — backend-architect 席位报告

透镜: 数据契约与实现可行性 (字段语义变更的向后兼容与消费方枚举 / 错误路径穷举 / 伪代码与真代码结构对齐)。本轮**只审不改**, 未编辑任何仓库文件。所有数字均为本席独立实跑, 不采信 proposal 自述。

## 审计结论

### Decisions

- [minor] documentation/基线冻结与行号有效性: `git -C aria diff --stat 301641b f314785` 对六个代码/规程文件输出为空; 插件缓存副本与 `git show 301641b:` 的 md5 对 `execution-modes.md` / `phase-c-integrator/SKILL.md` / `config-loader/DEFAULTS.json` / `collectors/audit.py` 四文件全 MATCH ⇒ 本文行号在两 SHA 通用这一断言成立 (证据: proposal.md:9,16; 本席实跑 `git diff --stat` + `md5sum`)。四处旧 schema 残留在 `f314785` 上仍逐字落 `phase-a-planner/SKILL.md:267` / `phase-b-developer/SKILL.md:204,277` / `phase-c-integrator/SKILL.md:157`, 全树计数恰 4 (证据: proposal.md:325; 本席 `git show f314785:<file> | grep -n`)。
- [minor] implementation/语料与 Level 解析器数字: 本席按 §1.3 三条判据重写解析器实跑 `openspec/{changes,archive}/*/proposal.md` **153** 份 —— 剥删除线得 L3 **58** / L2 **85** / L1 **1**, 不剥得 57/86/1, 失败恒 **9** 且名单与文中九项逐字相同, 首命中行 >15 恰 **7** 且七个目录名与行号 (22/21/22/29/44/58/21) 全对, 行首形态 `> **` **139** / `- **` **3** / `##` **2** / 其它 **0**, 首命中含 `Spec Level` **15** 份 (证据: proposal.md:212-214)。语料侧实跑: 顶层 **843** 份 `.md`, 真 2-field legacy **6**, unattributed **170**, 末段族 **62**, `C` = **153** (8 changes + 145 archive) (证据: proposal.md:51-53,181-183)。SC-2 的选样候选亦复核成立: `state-scanner-inter-cycle-surfacing` F-a **2** / F-b **3** 且独立源字段 **5/5**; `state-scanner-mechanical` F-a **6** / F-b **9** 但独立源 **0/15** (证据: proposal.md:405, Tasks B.0 item 4)。
- [minor] architecture/消费方枚举与向后兼容: 本席自行 grep 而非采信 §5 —— 全插件树 `--include=*.py --include=*.json --include=*.yaml` 对 `allow_incomplete_checkpoints` / `missing_checkpoint` **零命中**, 三个 token 的出现面只有 `execution-modes.md` / `audit-engine/SKILL.md:385` / `CHANGELOG.md:3017,3020`; 文件名 schema 的唯一代码消费方 = `state-scanner/scripts/collectors/audit.py:52,62-114` (只挑 `-aggregated.md`/`-aggregate.md` 候选 + token 正则), dashboard 侧 `aria-dashboard/references/parse-rules.md:79-103` 是 glob + frontmatter + 文件名 fallback。本 spec 只读文件名、不动 writer schema ⇒ 消费方破坏面为零 (证据: proposal.md:331-334)。
- [minor] implementation/归属谓词的假绿方向实测: 对 843 份语料按规则 1-3 全枚举, **无一份**被归给 >1 个 `change_id`; 再用与文件名无关的独立源 (frontmatter `context:` / `spec_id:` / `change_id:`) 对 **441** 份可解析报告交叉比对, 名匹配归属与独立源归属 **0 分歧** ⇒ 「末段界定 + 对称有界包含排除」在真实语料上无误归实例, 残余理论口子 (真实 id ∉ `C` 而其尾段 ∈ `C`) 在本仓被 F3 的「后缀碰撞 0 对」结构性堵住 (证据: proposal.md:170-174)。
- [minor] documentation/R4 findings 落地核验: 逐条抽验 R4 的 14 Major / 15 minor, 全部在**正文**落地而非批注 —— P2a 前置 (:98)、S2 改锚点面 (:131)、格 D (:232)、§2 五项参数表 (:296-300)、占位来源表 (:79-83)、SC-15(6)(7) (:418)、SC-17(5)(6) (:420)、SC-20(7) (:423)、SC-12 删 liveness 子句 (:415)、`scan_status` 16 键 (:279)、B.0 (b1)(b2)(c) (:373-375)、待复议 #11/#12 (:459,:461) 均在场。R4 引用的外部事实亦逐条复核为真: `phase-c-integrator/SKILL.md:132` 仍是合并视图字面键判断、`config-loader/SKILL.md:28` 第 5 步合并 DEFAULTS、`DEFAULTS.json` 八 checkpoint 全 `off` 且 `adaptive_rules = {off, convergence, challenge}`、`test_sibling_spec_probe.py:314` 逐字 `Path(__file__).read_text` (只读自己)、`run_all_tests.sh:43-45` 目录级 `is_pytest_suite`、`spec_complete.py:1642` proposal-only 零评估早退、`ab-suite/phase-c-integrator-pre-merge-gate.json` 8 fixture 绑定 (GateCheckTests 仅 4 条, NEG-3 落 `test_path_coverage`, 两条无 node id)。
- [minor] architecture/求值总序自洽性: P0→P1→P2a→P2→P3(按需)→P4→P5→P6 逐格代入未发现环或不可达: `--no-spec` 经 P2a 保证「锚点面 diff 非空且不触 `openspec/changes/**`」⇒ S2 必空 ⇒ S3 必被求值 (first-match 契约不动); lazy P3 对格 B/C/D 需要的 `resolved(pre_merge)` 仍会触发 (级 2a), `--no-spec` 走 S3 的「Level 视为 1」, S4-bypassed 早退于 P5 之前 ⇒ 无「需要 Level 却取不到」的悬空格 (证据: proposal.md:93-99,133-135)。
- [minor] architecture/error_kind 封闭集穷举: 九项对本文列出的全部失败路径一一对应 (坏 JSON / 未知 mode → `config_unreadable`; `enabled != true` → `audit_not_enabled`; P2a 两格 → `no_spec_unverifiable`/`no_spec_contradicted`; S1 → `change_id_unanchored`; S4 → `change_scope_unresolved`; Level → `spec_level_undetermined`; 格 C → `pre_merge_not_enabled`; git → `git_failed`), argparse 两格由「stdout 非 JSON ⇒ 按 fail」兜住, 报告目录缺失走 `scan_status=dir_missing` 而非 error ⇒ 无未定义出口 (证据: proposal.md:279)。

### Issues

- [major] testing/§1.0 fixture 硬约束 (1)(3) × SC-15(4) / SC-21(2): `:114` 的两条全称句 (「每份 fixture config **必须显式钉 `audit.mode`**」/「**每份 fixture config 必须显式写 `audit.enabled: true`** —— 除格 A 那一格 (SC-15(1)) 刻意反着来」) 与 Tasks `:378`「逐条给 SC-1~SC-22 的 fixture 补 §1.0 末段的**三条**硬约束」合起来, 会把 `audit` 块加进两条**必须没有 `audit` 块**的 fixture: SC-15(4) 自述逐字「`{experiments:{...}}` **且无 `audit` 块**」(`:418`), SC-21(2) 自述触发条件「`experiments.agent_team_audit === true` **且**无 `audit` 块」两条同时成立 (`:424`)。本席实读 `config-loader/SKILL.md:311-314`: 兼容映射的触发条件 2 逐字是「配置文件中不存在 `audit` 块」⇒ 一旦补键, 映射永不触发, SC-15(4) 的 `checked_checkpoints == ['post_spec']` 与「同结构 `['pre_merge']` 落格 B 判 pass」两条断言**结构性必红**, SC-21(2) 的「只满足一条 → 不映射」对照格亦失去正例。carve-out 清单缺这两格。危害与本文自己反复钉的失效同型: 无人值守下 Phase B 面对必红断言, 最省力的处置就是改断言 (证据: proposal.md:114,378,418,424 · config-loader/SKILL.md:311-314)。
- [major] testing/§1.0 硬约束 (1) 未钉 mode 取值 × SC-15(2) / SC-16: 硬约束只说「必须显式钉 `audit.mode`」, 不说钉哪个值; 而 `:121` 的作用域对照表给这批 fixture 统一补「`--change-id x` + 锚点含逐字 `> **Level**: 2` 行」并逐条标注「期望值是否随之变化 = **否**」。代入本文自定的优先级链实算: 若 Phase B 钉 `mode:'adaptive'` (硬约束 (2) 恰恰为 adaptive 档准备了 Level 行, 是自然读法), 则 config 未写的 checkpoint 走级 2a 取内联缺省 `adaptive_rules.level_2 = "convergence"` (本席实读 `DEFAULTS.json`) ⇒ 纳入集**非空** ⇒ 按 §1.0 P5「格 B/C/D 只在纳入集为空时求值」, SC-15(2) 期望的 `pre_merge_not_enabled` **exit 2 根本不可达** (实际落 missing exit 1); SC-16 的 `post_planning`/`post_implementation`/`post_brainstorm` 同样被纳入且零报告 ⇒ `verdict` 由期望的 `pass` 翻成 `fail`。钉 `manual` 则两条都成立 ⇒ **两个合法 fixture 判决相反**, 正是本文对 SC-8 已用「显式钉 `mode: 'manual'`」处置过的同族缺口, 这两条未清扫 (证据: proposal.md:114,121,411,418,419 · config-loader/DEFAULTS.json `adaptive_rules`)。
- [major] testing/Tasks B.0 规则 (b2) 的 F-e / F-f 标注: `:374` 称对 F-e/F-f「改用两条同样机械、**同样不与被测谓词共享心智**的判据」, 但 F-e 的第一合取项 `文件名匹配 ^{checkpoint}-[0-9TZ:.\-]+\.md$` 与 `:181` 计数表里 `excluded_legacy_count` 的**实现判据是逐字同一串正则**; F-f 的「文件名有 id 段但该 id ∉ `C`」同样是实现侧 `unattributed` 定义的换句话说。独立源只作用在第二合取项 (字段缺失 / 值 ∉ `C`)。后果: SC-2 明写「期望值 = 冻结产物里的独立标注, **不得由被测谓词现算**」, 而 F-e/F-f 两族的标注恰恰由被测谓词现算 ⇒ 若实现把 legacy 正则或 `C` 归属规则写错 (例如漏 `Z`/`.` 字符类、或把 `archive/README.md` 计进 `C`), 标注会跟着一起错 ⇒ 该维**恒绿**, 正是 B.0 设立的目的落空。SC-4 的手造 fixture 尚能独立证伪两计数分离, 故未升到 critical (证据: proposal.md:181,374,405)。
- [minor] documentation/§1.0 硬约束标题计数: `:114` 标题逐字「**全部 hermetic fixture 的两条硬约束**」却列出 (1)(2)(3) 三条 (R4 新增第三条时未改标题), 与 Tasks `:378`「补 §1.0 末段的**三条**硬约束」互斥。本文对同类计数漂移的既有处置是就地订正 (SC-5「原稿标题写四条正文却列五条 —— R2 rework 一并订正为逐条计数」), 本处未照办 (证据: proposal.md:114 vs :378)。
- [minor] implementation/§1 调用模板 / §2 参数表 / SC-11 命令: 调用模板 (`:74-78`) 把 `--diff-repo-path` 写成**不带方括号**的形态, 而 `:81` 与 §2 参数表 (`:298`) 都定义它「缺省 = `--repo-path`」= 可选; `--repo-path` 是否 argparse required 则全文无一处定义 (只有 `--base` 明写「无缺省, 缺失即 argparse exit 2」, SC-10 也只锁 `--base` 与互斥两格)。SC-11 的活体 dogfood 命令逐字只有 `--change-id … --base master`, 两个路径参数都省略 ⇒ 若实现按模板把 `--repo-path` 设成 required, 本文唯一的活体证据命令直接 exit 2。建议在 §1 明写两者的必填性与缺省, 并让 SC-11 的命令与之一致 (证据: proposal.md:74-78,81,296-300,414)。

### Risks

- [minor] architecture/§1.4 格 D 的 [INFO] 文案与四格分割证: `enabled_by` 按 §1.3 是 **per (checkpoint, change_id)** 的值 (adaptive 档随该 change 的 Level 变), 而格 D 的 trail 行渲染成单值 `adaptive_rules.level_{N}` / 「被审 change 是 Level {N}」, 四格互斥证也把 `enabled_by(pre_merge)` 当单值轴。采用方自定 `adaptive_rules` 使两档同为 `"off"` (如 level_1/level_2 都 off) 时, 一个混合 Level 的多 change PR 可以既落空纳入集、又让不同 change 的 `enabled_by(pre_merge)` 取不同 `{N}` ⇒ 文案占位无定义, 分割证未覆盖该格。缺省 `adaptive_rules` 下不可达 (只有 level_1 是 off), 故列 risk 而非 issue; 处置可以是「多值时 trail 行逐 change 各出一行」或在格 D 判据里显式要求 `{N}` 一致 (证据: proposal.md:190,228,232)。
- [minor] architecture/跨仓 (b) 通道的假绿依赖调用方传参: `:81` 的 fail-closed 附加条款把「跨仓禁用 (b)」建立在 `--diff-repo-path != --repo-path` 上, 而该参数缺省即等于 `--repo-path` ⇒ 子模块 PR 的编排者**漏传**时, 门会拿主仓那份 Phase A-only 形态的 diff 判 `post_implementation = not_applicable` = 假绿。本文已在同处点名该后果, §3 也把它列进 pre_hook 必传五项, 故不另计 issue; 但这是本 spec 里唯一「靠调用方纪律兜住假绿」的一格, 建议 Phase B 在脚本侧加一条低成本机械反证 (例如锚点仓与 diff 仓的 `git rev-parse --show-toplevel` 相同才允许 (b)) (证据: proposal.md:81,296-300)。

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **3** / Minor **3** (另 7 条 decision 不计入)。

rationale: 本轮把 proposal 的事实面按「数据可用性」原则全量机械复核 (基线冻结、语料四类计数、Level 解析器五组数字、消费方枚举、四个提交的文件清单、ab-suite catalog 绑定、tag/gitlink/版本号), **无一条事实断言被证伪**, R4 的 14 Major / 15 minor 亦全部在正文落地而非批注 —— 这是四轮以来事实面最干净的一版。剩下的三条 Major 全部落在**同一族**: fixture 前提的全称句与个别 SC 的判据前提互斥 (旧配置兼容映射两条 fixture 必须无 `audit` 块 / mode 取值未钉死使两条 SC 的期望值可被合法翻转 / B.0 (b2) 对 F-e·F-f 的「独立标注」仍由被测谓词现算)。三条都不改设计本体, 只需在 §1.0 硬约束与 Tasks 回扫清单上补两个 carve-out、钉一个取值、把 (b2) 的自述强度改写成实情 (或给 F-e/F-f 换一条真正独立的标注源)。按 post_spec 非阻塞语义, 本席不主张阻断; 但票型取 **REVISE** —— Major 非零, 且这三条一旦带进无人值守的 Phase B, 会直接产出结构性必红的断言, 而本 spec 自己反复钉的失效模式正是「必红断言逼实施者改断言」。

## 轮次记录

### Round 5

- Agents: backend-architect (五席之一, 本报告只代表本席; 新席位, 不继承 R1-R4 结论)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 13 条 (Decisions 7 / Issues 5 / Risks 2 — 其中 Issues 内 Major 3、minor 2, Risks 全为 minor)
- Vote: REVISE
