---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-07T05:26:10.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [code-reviewer]
---

# post_spec R2 单席报告 — code-reviewer (pre-merge-completeness-gate-change-scope)

席位透镜: 逐条打开 proposal 引用的 `文件:行号` 验真伪 · 改动是否破坏同文件其它调用路径 · 文档同步面是否列全。本轮实读 SOT 12 份 + 实跑语料全枚举 6 次 + 逐字节冻结核验 10 文件。**只审不改**, 未触碰仓库任何文件。

## 审计结论

### Decisions

- [minor] documentation/语料与 A.2 统计全量复算: 独立全枚举复算 proposal 的全部数字, 逐个为真 —— `|C|`=152 (9 changes + 143 archive dirs, 第 144 项是 `README.md`)、前缀碰撞 1 对 (`aria-orchestrator` ⊂ `aria-orchestrator-divestiture`) / 后缀 0 / 中缀 0、以 checkpoint 前缀开头的末段族 **62**、`unattributed` **170**、真 2-field legacy **6**、原稿旧定义 **238**、post_spec 499 · post_planning 209 · post_implementation 3、A.2 归档语料 52 无文件 / 15 内联 / 37 全无 (证据: 冻结快照 `3f4b379` 全量 `git ls-tree` + 本席 python 全枚举; proposal.md:36,49,50,51,153)
- [minor] architecture/基线冻结 `301641b` 逐字节核验: 对 10 个被引文件 (execution-modes / report-storage / pre-write-validation / report-format / audit-engine SKILL / phase-c-integrator SKILL / collectors/audit.py / spec_complete.py / config-loader SKILL / DEFAULTS.json) 与 `git show 301641b:` 比 SHA1 全部 SAME ⇒ 本轮所有行号对该 SHA 有效 (证据: proposal.md:9 的「行号有效范围」勘正成立)
- [minor] implementation/R1 五条 Critical 的落地核验: 五条均落在正文而非批注 —— 末段规则 (proposal.md:112)、两个排除计数拆分 (:119-126)、(b) 换成 Phase A-only (:148,151)、(c) 含内联 `## Tasks` (:148,153)、SC-2 期望取人工标注 + 选样硬约束 (:245)。规则 3 改对称有界包含后, 本席在真语料上验得**多归属文件 = 0**, 未引入新的跨 change 误计 (证据: 本席 python 全枚举)
- [minor] documentation/R1 conflicted 行号冲突机械闭合: `sed -n '136,137p' phase-c-integrator/SKILL.md` ⇒ `:136` = `context: PR diff (branch_name vs base)`, `:137` = 「5. 处理 verdict」⇒ R1 `ffd3834a` 成立, 上轮**同席位** `9a245f24`「逐条核验无一漂移」确属错误; v2 已按 `:136` / `:250` 勘正 (证据: proposal.md:42)

### Issues

- [major] implementation/§1.4 stdout 契约 vs §1.2b (SC-10 与 SC-19 互斥): §1.4 把顶层键集写成「**逐字**」13 项且**不含** `scanned_dir_depth` (proposal.md:164), SC-10 断言「顶层键集逐字 = 1.4 列表」(:253); 而 v2 新增的 §1.2b 要求「在 stdout 契约里输出 `scanned_dir_depth: 1`」(:134), SC-19(a) 断言「stdout 含 `scanned_dir_depth: 1`」(:262)。两条 SC 结构上不可同时为绿 —— 满足 SC-10 的实现必红 SC-19, 反之亦然。**修法**: 把 `scanned_dir_depth` 补进 §1.4 的键集枚举 (14 项), 或把 §1.2b 的可见性义务改走 audit trail 行而非 stdout 顶层键
- [major] architecture/§1.4 config 读取 (config-loader 在脚本层无实现面): §1 与 §1.4 强制「config 一律经 **config-loader** 读取, **不直读** `<repo>/.aria/config.json`」(proposal.md:82,159), 但 `skills/config-loader/` 目录只有 `SKILL.md` + `DEFAULTS.json` + `config-example.md` —— **没有任何脚本/模块**; 全插件 `.py` 对 `agent_team_audit` 零命中 ⇒ 旧配置兼容映射在代码层根本不存在。同族先例反向: `audit-engine/scripts/sibling_spec_probe.py:380` 与 `phase-c-integrator/scripts/pre_merge_gate.py:721` 都直读 `<repo>/.aria/config.json`。后果二选一: (a) Phase B 在 `completeness_gate.py` 内联复制映射 —— 正是 R1 `013d0274` 判过的「第二副本 + 漂移」换个位置重开, 而 §5 (:204) 宣称该副本「已一并消失」; (b) 落回直读 ⇒ SC-15 第二格 (`test_legacy_config_mapping_via_loader`) 恒红。**叠加矛盾**: config-loader SOT 规定「JSON 格式错误 → 警告用户 + 返回默认值」(config-loader/SKILL.md:37), 若真「一律经 config-loader」, SC-10 要求的 `坏 config JSON → config_unreadable exit 2` (:253) 结构上不可达 —— 该输入只会落成 `no_checkpoints_configured`
- [major] testing/SC-14(a) 与 rule6_note 的「照跑面」认定: `ab-suite/phase-c-integrator-pre-merge-gate.json` **不是 eval 套件** —— 实读其顶层键为 `skill_name/version/type/parent_skill/spec/issue/release_pr/fixtures_dir/changelog/fixtures/primary_pass_gate_metric/quality_target_deferred_to_dogfood`, `type = "workflow_skill_subextension"`, **无 `evals` 键**, `fixtures` 8 项每项带 `test_case_in_unit_tests` 指向单测 ⇒ 无法按 SC-14(a) 的「各跑一次 with/without 臂」执行 (proposal.md:233,257,268)。本 spec 自己引作先例的 `archive/2026-08-23-pre-merge-gate-no-run-for-branch/proposal.md:284` 恰恰把它记作「**7** fixtures」并明写「照跑 = 测量剧场」, 其处置是往 catalog 登记 fixture (同文 `:228`), 不是跑 AB 臂。**修法**: 照跑面收敛为 `audit-engine.json` + `phase-c-integrator.json` 两个真 eval 套件, pre-merge-gate 这份改为「登记 fixture / 记缺口」并在 rule6_note 点名其形态差异
- [major] architecture/§1.1 S1 锚点校验与既有豁免键 `allow_dangling_change_ids` 冲突: S1 明写「复用 `pre-write-validation.md:20-26` 锚点链」(proposal.md:90), 却不继承该链的既有豁免开关 —— `pre-write-validation.md:16-18` Step 1 = `config-loader → audit.allow_dangling_change_ids`, `audit-engine/SKILL.md:381-384` 明写该键「仅用于临时场景 (如遗留 change_id 迁移期)」。而 §1.1 (:95) 又规定 `allow_incomplete_checkpoints` **不豁免** S1 的 error ⇒ 迁移期采用方开了 `allow_dangling_change_ids`, 写盘侧放行、新门 exit 2 硬阻, **无任何逃生舱**。§5 (:206-210) 自称穷举了「共三条」行为变更, 未列此条
- [minor] documentation/§1.2b 非递归理由的例证不成立: 「递归会把历史上手工归置的一次性目录 (上述两个正是这种) 突然算成证据」(proposal.md:134) 与语料不符 —— 冻结快照 `3f4b379` 里 `pr19-submodule-scan/` 内是 `AGGREGATE.md` + 五份 `*.yaml`, `wf-r1fix/` 内是 `PLAN-*.json` / `VERDICT-*.json`, **无一以 checkpoint 名开头** ⇒ 即便换 `rglob()` 也 0 份计入。非递归的**结论**仍成立 (与现行 glob 语义一致 = 不改变现状), 但理由须换成「未来子目录可能被误计」。另 `:135` 列的 5 个「无 checkpoint 前缀形态」里 `phase-b-review-179-secret-guard-manifest-precision.md` 不属 audit-trail 族, 而真实的 5 份 `*-audit-trail.md` 少列了 `premerge-gate-mainbranch-failclosed-audit-trail.md` —— 与 SC-19 语料依据写的「5 份 `*-audit-trail.md`」(:262) 对不齐
- [minor] documentation/§1.2 规则2 证据句「全部 3 份 post_implementation 报告」: 实测 3 份中只有 `post_implementation-R1-2026-06-11-audit-drift-guard.md` 属末段族; 另两份 `…-state-scanner-mechanical-t3.md` 与 `…-aria-secret-guard-plugin-default-orchestrator.md` 按**旧的纯中缀规则**即已命中 `state-scanner-mechanical` / `aria-secret-guard-plugin-default` (两者均 ∈ `C`, 且 `-t3` / `-orchestrator` 是同 change 的任务/席位后缀) ⇒ 它们不在「会被判 missing 假红」的集合里 (proposal.md:113)。62 份与 25 组合两个主数字本席独立复算为真, 只有这一句是 R1 聚合原话被抄进正文 (换人执笔仍逃逸, 符合 memory `author_and_verifier_must_differ` 的反例形态)
- [minor] documentation/标准文件行号漂移 2 处: (a) `standards/openspec/project.md:118` 实为 **Level 3** 行, Level 2 在 `:117` —— proposal.md:153 与 :288 均写「`:118` 规定 Level 2 输出 = proposal.md」; (b) `skill-benchmark-exemption.md` 的「SKILL.md 有变动时的附加约束」在 `:33`, `:35` 是「## 3. 第三行不是逃生舱」标题 —— proposal.md:288 写「`:35` 附加约束」。其余 30+ 处行号 (execution-modes 全节 / audit-engine SKILL.md:49-54,60,63,105,123-125,381-388,398-400,403-419 / phase-c-integrator:130,131,133-136,136,137,157,252,253,260,265,299 / report-storage:8,18,34-39,37,43 / pre-write-validation:3,14,20-26,28-30 / collectors/audit.py:52,62-69 / spec_complete.py:924-930 / DEFAULTS.json:118-123 / configured-gate-authority:38,40 / proposal-minimal:27-31 / 归档先例:282-284,55-57) 经逐条实读**全部命中**
- [minor] implementation/§1.1 与 §1.4 三处取值未定义: (a) `scope_source=no_spec` (S3) 时 `results[].change_id` 与 `change_ids` 取何值未定义 —— S4-bypassed 已在 R1 rework 中补齐 (proposal.md:103), S3 这一路没有; (b) `no_checkpoints_configured` 与 `allow_incomplete_checkpoints=true` 的交互未定义 (:95 只说「S1/S3 的 error 不被豁免」, :163 只说空集恒 exit 2) ⇒ SC-7 与 SC-15 的期望值会随实现者的合理解读红绿翻转, 与 R1 `dc50ea10` / `98462082` 同型
- [minor] documentation/ab-suite 套件版本现值已陈旧: proposal.md:12 与 :198 写「`ab-suite/version.yaml` 现值实测 **1.4.0**」并以 `1.4.0 → 1.5.0` 为动作; 工作树实测 `version: "1.5.0"` (提交 `5697477`「Group 7 套件编辑」, 晚于冻结快照 `3f4b379` 的 1.4.0) ⇒ 目标号已被占用。同格的并发预案 (fetch + 撞号顺延 1.6.0) 已覆盖处置, 但「现值 1.4.0」这句须更正为 1.5.0

### Risks

- [major] architecture/§1.3(b) Phase A-only not_applicable 判据 (两向都不成立, 支撑复议 #7 的删除侧): (1) **假绿向** —— 判据「全部变更文件在 `openspec/changes|archive` 之下 ⇒ B.2 实现工序整个未发生」(proposal.md:148) 对**交付物本身就是 openspec 语料**的 cycle 不成立 (典型: 批量勘正归档 proposal 的语料迁移), 实施确已发生却被判未发生 —— 与 R1 `8c7972ce` 判死的「路径形状代理工序」同species, 只是面窄了; (2) **空转向** —— 本仓真实 Phase A 分支惯例把审计报告与 triage 一并落 `.aria/audit-reports/` (实测 `813e82c` .aria=12 / openspec=2, `f634d83` .aria=6 / openspec=1, `2c8eaa6` 1/1), 该目录不在 `openspec/**` 下 ⇒ (b) 在本仓的规范工作流里几乎不可能触发, 与 `:283` 保留 (b) 的理由「它对应 issue 里真实发生过的 Phase A-only PR 场景」冲突。两条合起来使 knowledge-manager R1 的「(b) 无合法触发场景」论证更硬, 建议 owner 在复议 #7 优先考虑删除 (b), 或把判据改为「diff 只触本 change 的 `openspec/changes/{id}/**` ∪ `.aria/audit-reports/**`」并配相应反事实 SC

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **5** / Minor **5** (另 4 条 decision 为正面记录, 不计入缺陷)。

rationale: R1 的五条 Critical 已**真落地**且方向正确 (末段形态、两计数拆分、(b)/(c) 判据收窄、SC-2 去自指), 我用真语料复算了它们的全部数字与不变量 (多归属 = 0, 62/25/170/6/238 全对, A.2 52/15/37 全对), 事实底盘经得起机械核。本轮 5 条 Major 全部**不是**对 R1 结论的重开, 而是 rework 与 v2 新增内容自身引入的新面:

- 两条是 v2 自造的**内部矛盾**: §1.2b 与 §1.4/SC-10 的键集互斥 (M1); §1.4 强制 config-loader 而 config-loader 无脚本面、且其错误语义使 `config_unreadable` 不可达 (M2)。
- 两条是**外部事实错配**: 被写进 Rule #6 照跑面的 `phase-c-integrator-pre-merge-gate.json` 根本没有 evals, 本 spec 自引的先例正说它「照跑 = 测量剧场」(M3); S1 复用锚点链却不继承既有豁免键, 迁移期采用方无逃生舱 (M4)。
- 一条是**判据 species 未变**: (b) 换了路径集合, 但仍以路径形状代理工序, 且在本仓的真实 Phase A 分支形态下几乎不触发 (M5)。

全部 5 条都在 Phase B 落地时会立刻显形 (TDD RED 互斥 / 无 API 可调 / 无 eval 可跑), 无一构成生产假绿, 故不判 Critical; 但按 verdict-format.md 的计算规则 (0C + ≥1M ⇒ PASS_WITH_WARNINGS), 且按 audit-points 横切原则「数据可用性核实结果对 verdict 载重」, 本席投 **REVISE**。

计算依据:
- Critical issues: 0
- Major issues: 5 (4 issue + 1 risk)
- Minor issues: 5 (5 issue)
- Decisions (不计入): 4

## 轮次记录

### Round 2

- Agents: code-reviewer (本报告为五席之一的单席产出)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions: 14 (Major 5 / Minor 5 / Decisions 4)
- Delta vs 上轮 (R1 本席位口径): R1 本席位的 `9a245f24`「行号无一漂移」经机械反证不成立, 本轮以新席位身份确认否定并复核了 30+ 处行号 (仅 2 处标准文件行号漂移); R1 的 5C/9M 无一条在 v2 中重开, 本轮 5 条 Major 全为 rework/v2 新增面
- Vote: REVISE
- Duration: N/A
