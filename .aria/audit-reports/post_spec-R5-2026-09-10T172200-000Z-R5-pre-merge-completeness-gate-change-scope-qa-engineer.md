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
timestamp: 2026-09-10T22:13:59.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [qa-engineer]
---

# post_spec R5 单席审计报告 — qa-engineer

席位透镜: SC 可证伪性 (逐条反事实) / hermetic case 可构造性 / 既有测试与冻结语料受影响面 / 缺失的负向测试 / 既有失败项处置。本席为新席位, 不继承前四轮结论; 所有事实断言均本轮实读或实跑核验。

## 审计结论

### Decisions

- [minor] testing/R4 Major `b2bc13a6` 的 Level 统计订正已落地且实跑复现: 本席按 §1.3 判据 1-3 (整文件扫描 + 文档序第一条 + 行首 `>`/`-`/`#`/空白/`*` 剥离 + `Level`|`Spec Level` + 可选 `**` + ASCII/全角冒号 + 取值前剥 `~~…~~`) 独立实现解析器, 对 `openspec/{changes,archive}/*/proposal.md` **153 份**实跑: 剥删除线 ⇒ **L3 58 / L2 85 / L1 1**, 不剥 ⇒ 57/86/1; 解析失败 **9** 份且目录名与正文清单逐份同集; 首命中 >15 **恰 7** 份且行号逐一相同 (`runtime-probe-archive-gate-integration:22` · `secret-guard-bash3-multiline-hardening:21` · `state-scanner-stale-refs-false-parity:22` · `premerge-gate-branch-existence:29` · `premerge-gate-mainbranch-failclosed:44` · `phase-c-integrator-ci-path-coverage:21` · `a1-entry-claim-duplicate-work-guard:58`)。订正落在判据本体与校准段正文, 非批注 (证据: proposal.md:180-184)。
- [minor] testing/R4 Major `29c39e2c` 的 AB 绑定订正**可执行**: 实读 `aria-plugin-benchmarks/ab-suite/phase-c-integrator-pre-merge-gate.json` —— `type: workflow_skill_subextension`, 无 `evals` 键, 8 `fixtures[]`; 指向 `GateCheckTests` 的**恰 4** 条, `NEG-4` → `NotFoundVerdictTests.test_sc2_trigger_matched_message`, `NEG-3` → `test_path_coverage.InternalErrorReasonTests.test_internal_error_has_own_reason`, `wait_then_green` / `NEG-2-timeout` **无 node id**。Tasks 拆出的三条命令本席逐条实跑: 7 / 1 / 1 tests, 全 OK (证据: proposal.md:389 区 · ab-suite/phase-c-integrator-pre-merge-gate.json)。
- [minor] testing/SC-12 基线三套件全绿, 无既有失败项需 carve-out: 本席实跑 `audit-engine/tests` **104 tests OK** · `phase-c-integrator/tests` **148 tests OK** · `state-scanner/tests` **1593 tests OK**, 0 failure。R4 Major `4cbe35ce` 的处置 (删 SC-12 归档门 liveness 子句 + F7 落点改挂 SC-13) 前提核实成立: `spec_complete.py:1642` 逐字「两文件皆缺 (proposal-only) → 维持 v1.54.0 designed 零评估早退」, `:924-930` 的 `if name == "SKILL.md":` liveness 分类器在本 cycle 不运行 (证据: proposal.md:415 · spec_complete.py:924-930,1642)。
- [minor] documentation/语料底盘与 SOT 行号抽验零漂移: 本席全枚举 `.aria/audit-reports/` —— 顶层 **843** 份 `.md` (语料活体, R4 记 837)、真 2-field legacy **6**、unattributed 全 8 checkpoint 口径 **170** / 本仓 2-checkpoint 口径 **160**、末段族 **62**、`*-audit-trail.md` **恰 5** 且与 §1.2b 逐字同集、子目录恰 `pr19-submodule-scan/` `wf-r1fix/` 两个; `C` 今日 **153** (8 changes + 145 archive), 前缀碰撞 1 对 (`aria-orchestrator` ⊂ `aria-orchestrator-divestiture`) / 后缀 0 / 中缀 0。SOT 抽验全中: `execution-modes.md` 围栏 `:34` 开 `:66` 闭、Step 1-5 在 `:37`/`:41`/`:46`/`:54`/`:63`、`:44` 与 `:82` 两种豁免拼法、`:152` 逐字含「机械护栏 SC-17 计数恰 2」、`:185` 「消费方不得从 `hits == []` 推断结论」; `audit-engine/SKILL.md:391`/`:405`/`:410-411`; `phase-c-integrator/SKILL.md:131`/`:132`/`:137`/`:157`/`:252`/`:253`; `config-loader/SKILL.md:8-10,28,37,305-331` + `DEFAULTS.json` (audit 八键全 off, `adaptive_rules` 三档, 无两个 `allow_*`) + `config-example.md:276-280,381-400,402-417,419-440,442`; `run_all_tests.sh` 的 `is_pytest_suite()` 与 `test_sibling_spec_probe.py` 的 `TestNoPytestImport` 逐字只读 `Path(__file__)` (证据: proposal.md:465 References 全条)。

### Issues

- [major] testing/SC-2 选样候选 × Tasks B.0 (b1) 双列交叉: SC-2 逐字称实测候选 `state-scanner-inter-cycle-surfacing`「F-a **2** / F-b **3**, **5/5 全部带独立源字段** (frontmatter 可取第一列) ⇒ 双列交叉可执行」。本席逐份实读这 5 份: 2 份 F-a (`post_spec-R1/R2-2026-05-08-…`) 带 `change_id: state-scanner-inter-cycle-surfacing` ✓, 但**全部 3 份 F-b** (`pre_merge-R1-R4/R5-2026-05-09-…-sub-pr-{a,b,c}.md`) 只有 `context:` 且其值是自由散文 —— 逐字 `context: state-scanner-inter-cycle-surfacing sub-PR (a) — TX.0 + TX.1 prerequisite` —— **不是 change_id**。B.0 (b1) 逐字「两列一致 ⇒ 取该值; 两列不一致 **或** 第一列取不到 ⇒ 该文件**整份剔出**」, 而全文未定义 prose→id 的归一化, 也未给 frontmatter 与 git 历史两个来源定序 ⇒ 按逐字比对这 3 份被剔, **F-b 归零 < 本轮刚放宽的下界 3**, 规则 (c) 又明禁自造样本 ⇒ 无人值守 Phase B 在该族上再次无合法动作。另: 本席复算全库仅 3 个 id 满足 F-a≥2 ∧ F-b≥3, 另两个是被 R4 剔出的 `state-scanner-mechanical` 与 `secret-guard-per-segment-evaluation` (实读 39/39 **零**独立源字段) ⇒ 换 id 亦无解。⇒ R4 修 `6c4455bd`/`2370f1f9` 的修法把同一失效以更软形态带了回来。附带: SC-2 正文仍写「期望值 = 冻结产物里的独立**人工**标注归属」, 与 B.0 自述的无人值守机械仲裁互斥 (证据: proposal.md:405, :373; `.aria/audit-reports/pre_merge-R1-R4-2026-05-09-state-scanner-inter-cycle-surfacing-sub-pr-a.md` frontmatter)。
- [major] testing/SC-20(7) 逐对不叉乘格的期望值与本文自定的 Step 3 枚举互斥: 该格 config 逐字 `{audit:{enabled:true, mode:'adaptive', adaptive_rules:{level_1:'off', level_2:'convergence', level_3:'challenge'}}}` (**无 `checkpoints` 块**), 锚点 b 是 Level 3。按 §1.3 优先级链级 2a, **每个**未显式写的 checkpoint 取 `level_3='challenge'`; 而本文排除清单只有四项 (`pre_merge`/`post_closure`/`mid_post_spec`/`mid_implementation`) —— `post_brainstorm` 的排除**仍在待 owner 复议 #1**, 未成文 ⇒ 非排除项是 `post_brainstorm`/`post_spec`/`post_planning`/`post_implementation` **四个**, 对 b 全部纳入。fixture「目录**只放**属于 b 的 post_spec 报告一份」⇒ `(post_brainstorm, b)` 无任何 not_applicable 通道 ((b) 限 post_implementation, (c) 限 post_planning) ⇒ 判 `missing` ⇒ **verdict=fail exit 1、`results` ≥2 条**, 与本条断言的「`results` **恰 1 条**、`verdict=pass` exit 0」直接冲突。后果与 R4 反复钉的形态同型: 正确实现必红, 且该条要锁的「不叉乘」不变量因两种实现同样红而**失去鉴别力** (R4 Major `95ddb322` 的修法未闭合)。同族失准: SC-15(5) 写「逐对判 `missing`」, 而其 4 对里 `post_planning` 按 (c) 落 `not_applicable/no-a2-artifact` (锚点只有一行 Level, 无 `## Tasks`), 只有 verdict=fail 这半成立 (证据: proposal.md:423, :418, :215, :236, :437)。
- [major] architecture/§1.4「四格互斥与全覆盖证」未覆盖 `allow_dangling_change_ids` 降级路径, 分割不全: 该证只按 `enabled_by(pre_merge)` 枚举级 1 / 2a / 2b / 2c / 2d 并把级 3 支出为 `config_unreadable`, 结论「不存在落不进任何一格的输入」。但同文 §1.1 末段在 R3 新开了第六种状态: `allow_dangling_change_ids=true` 且锚点缺失时「该 id 记 `[WARN] … Level 不可解析, **跳过 adaptive 推导**」并按「只有 `explicit` 档的 checkpoint 纳入」继续评估。代入官方 `config-example.md:402-417` **场景 B** (adaptive + **无** `checkpoints` 块) + 该键 + 拼错 id: 零 explicit ⇒ 纳入集空 ⇒ 进 P5; 而 `pre_merge` 自身同样走级 2a、同样被跳过 ⇒ `resolved(pre_merge)` **无值**, `enabled_by(pre_merge)` 也取不到 —— 且 R3 已把封闭集里的 `default` 档删除 (「不再有『不知为何是 off』这一档」) ⇒ 格 A 假 (enabled=true)、格 B/C/D 三格的判据都取不到值 ⇒ **行为未定义**, 与 R4 判 Major `955907f2` 的失效结构逐字同型, 且零 SC 覆盖 (SC-7(d) 的 fixture 靠含 explicit checkpoint 侥幸绕开)。次要同族: 多 change 混合 Level 时 `resolved(pre_merge)` / `enabled_by(pre_merge)` 非单值 (四个非排除项显式 off + a=L1 / b=L3 ⇒ a 落格 D、b 落格 B), 两格 verdict 同为 pass 但 `[INFO]` 文案不同, 契约未指定取哪一个 (证据: proposal.md:276, :138, :279, :410; config-example.md:402-417; DEFAULTS.json `adaptive_rules`)。
- [major] testing/最承重的两条散文落点无任何机检承接: §1.4 的**消费方 fail-closed 义务**「exit≠0 或 stdout 非 JSON 或 `schema_version` 未知 ⇒ 按 `fail` 处置, 不得按 PASS」(写进 `execution-modes.md`) 与 §3 的**步骤 4.5 三态处置**「fail → 阻塞并输出 ERROR; not_applicable → 必带 `[INFO]` 行; `unattributed_count > 0` → 必带 `[WARN]` 行」(写进 `phase-c-integrator/SKILL.md`) 是整个修复在**生产路径**上生效的唯一保障 —— 门只输出 JSON 与 exit code, 不落地这两条则门被调用了也不阻断。本席逐条核 SC-13 的九条 grep (通配清零 / `completeness_gate.py` 在 bash 块 / `change_id` +≥1 / `{timestamp}` 清零 / 三条 report-storage 逐字串 / `adaptive_rules` +≥1 / bypassed 两处同字面 / 分块计数与两侧逐字相等 / 调用方接缝两条), **无一覆盖这两条**; SC-14(b) 的 eval id 3 三条 expectation 也不含 fail-closed。这与本文自己在 R2 对 §1.2b 两条枚举边界立的判据 (「原本『schema 文档写明』却未点名任何文件、也无机检, **可静默不做**」⇒ 补两条逐字 grep) 同一判据, 结论却相反 (证据: proposal.md:282, :308, :416, :417)。
- [minor] implementation/`--repo-path` 的 argparse 必填性未定义, SC-11 的活体命令因此不可判定: §1 只给 `--base` 写了「**无缺省** (#137 教训), 缺失即 argparse exit 2」, §2 输入参数表给 `repo_path` 写「pre_merge 必传」, 但脚本层是必填还是取 cwd 缺省全文无一处声明; SC-10 也只锁 `--base` 缺失与 `--change-id`×`--no-spec` 互斥两格。SC-11 的 dogfood 命令逐字是 `--change-id pre-merge-completeness-gate-change-scope --base master`, **不带 `--repo-path`** ⇒ 取必填则该命令直接 exit 2、取 cwd 缺省则与「锚点面恒主仓根 (子模块合并时不是当前工作目录)」的跨仓契约留下隐式冲突 (证据: proposal.md:86, :296, :413, :414)。
- [minor] testing/`unattributed` WARN 模板未定义文件名连接符, 使 SC-4 的「逐字相等」期望值仍由实现者定: §1.2 计数表与 §1.4 trail 行的模板逐字都是 `… N 份 — <按字典序前 20 个文件名>[, … 其余 K 份见 stdout 的 \`unattributed\`]`, 但 20 个文件名之间用 `, ` / `,` / 空格哪一种全文未写。R4 修 `e83dca40` 时把 SC-4 从 endswith 升级为「**对整条 WARN 行逐字相等**比对」⇒ 比对目标无法从 spec 推导, Phase B 必须先写实现再回填断言, 正是 minor `243ad3d8` 判定的「期望值由实现者按自己的实现重算 ⇒ 反事实失去独立性」形态 (证据: proposal.md:182, :285, :407)。

### Risks

- [minor] testing/`--no-spec` 合法格的 `not_applicable` 断言在 adaptive 档真空成立: §1.1 S3 规定 `--no-spec` ⇒ `change_ids=[]` 且「Level 视为 1」, 而 DEFAULTS 实测 `adaptive_rules.level_1 = "off"` ⇒ adaptive 档下**每个** checkpoint 都解析为 off ⇒ 纳入集空。此时 SC-7 的「`--no-spec` 合法 → **全部** `not_applicable/level1-no-spec` + `results` 每条 `change_id is None`」与 SC-17(4) 后半格的同类断言**全部是空集上的全称谓词**, 未实现 S3 的 not_applicable 通道也能绿。两条 SC 只要求 fixture「显式钉 `audit.mode`」(§1.0 硬约束 1), **未要求钉出非空纳入集**。低成本修法: 两处 fixture 逐字钉 `mode:'manual'` + 至少一个 explicit 非 off 的 checkpoint, 并加「`results` 非空」前置断言 (证据: proposal.md:111, :103, :410, :420; DEFAULTS.json)。
- [minor] testing/SC-13 的 `execution-modes.md` 切片界依赖两个未列入保留项的行首标记: R4 修 `d9578e5d` 后, 该护栏改为「以 `Step 4:` 行起、`Step 5:` 行止 (不含 `Step 5:` 行) 的行区间内计数 `scripts/completeness_gate.py` 恰 1」。但同文 §2 与 §4 授权的改动正是「Step 4-5 改为调用行 + 1.2 规则 + 1.3 三态表 + 1.4 契约」, 全文未把「保留 `Step 4:` / `Step 5:` 两个行首标记」写成约束 (SOT 现值实测 `:54` / `:63`)。若重写把两个 Step 合并, 切片起止再次无定义 —— 与本轮刚修掉的失效同型 (证据: proposal.md:416, :290 区, :320 区; execution-modes.md:54,63)。
- [minor] testing/TDD RED 清单与未裁复议项的顺序冲突: Tasks 要求「先写 SC-1~SC-10 + SC-15~SC-17 + SC-18 + SC-19~SC-22, baseline 全红」, 但其中 SC-18 (复议 #1)、SC-5 的 (b) 通道存废 (复议 #7)、SC-15 的格 B 语义与格 D 存废 (复议 #8)、SC-9(4)+SC-7(d) 的逃生口归属 (复议 #10)、SC-17(5) 的硬阻处置 (复议 #11) 各自逐字写着「裁完 Phase B 只保留其一」。全 Tasks 只有版本项挂了「裁定前不动手」的前置门 ⇒ 无人值守 Phase B 面对 SC-18 的「不得两条都不写」既不能两条都写、也不能自行择一 (Rule #10)。建议给 B.0 加一条与版本项同级的「复议 #1/#7/#8/#10/#11 未裁前不进 RED」门 (证据: proposal.md:379, :421, :437-461)。

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **4** / Minor **5** (另 4 条 decision 不计入)。

rationale: R4 的 14 条 Major 逐条抽验, **修法确实落在正文判据本体而非批注**, 且本席对其中三条 (Level 统计 `b2bc13a6` / AB 绑定 `29c39e2c` / 归档门 liveness `4cbe35ce`) 做了独立实跑复现, 结论与订正后的文本逐字吻合; 语料底盘与约 30 处 SOT 行号抽验零漂移; 既有三套件 104/148/1593 全绿, 无需 carve-out。故无 Critical。但本轮四条 Major 中有三条 (`SC-2 候选` / `SC-20(7)` / `四格分割证`) 是 **R4 rework 自身的下游未闭合** —— 修法各自成立, 却在真实语料 (散文 `context:`)、自定枚举口径 (post_brainstorm 未排除) 与自开的降级路径 (`allow_dangling_change_ids` 跳过推导) 上留下新的不可执行 / 不可判定格; 第四条 (fail-closed 义务零机检) 是全设计最承重的散文落点缺机械承接, 与本文自立的判据自相矛盾。四条均可在正文当场闭合, 不需重开设计。⇒ vote **REVISE**。

## 轮次记录

### Round 5: Agents

- qa-engineer (本席, 单席报告)

Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品

Conclusions 数: 13 (Decisions 4 / Issues 6 / Risks 3; 其中 Critical 0 · Major 4 · Minor 5, decision 4 条不计入缺陷计数)

Vote: REVISE
