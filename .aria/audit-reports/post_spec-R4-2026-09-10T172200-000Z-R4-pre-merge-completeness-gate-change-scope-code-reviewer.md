---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-10T20:19:28.434Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [code-reviewer]
---

# post_spec R4 单席报告 — code-reviewer (代码级核对透镜)

本席为 Round 4 新席位, 不继承前三轮任何结论。全部结论以**实读 SOT / 实跑复算**为准: 约 40 处 `文件:行号` 逐条打开比对, 语料数字与 Level 解析统计独立用 python 全枚举复算, R3 的 3 Critical + 12 Major 逐条回到 proposal 正文定位落地位置。

## 审计结论

### Decisions

- [minor] documentation/SOT 行号引用抽验: `execution-modes.md` 的 `:15`(优先级链) `:32`(触发条件) `:37-44`(Step 1-2 + 豁免文案) `:46-52`(Step 3 + mid_post_spec 条款) `:54-61`(Step 4 两条通配) `:63-65` `:70-82` 与 `:90/:121/:159`(探针三处) 全部逐字命中; `audit-engine/SKILL.md:49-54`(输入参数恰四项, 无 change_id) `:60/:63`(post_brainstorm / mid_implementation 条件触发) `:123-125`(fenced bash 先例) `:381-388`(两个 allow_* 仅散文默认 false) `:391`(优先级链) `:398-419`(DEC-4 降级非 skip + base 取法 + `:410` 防 vacuous-true) `:427-433` 命中; `phase-c-integrator/SKILL.md:131/:132`(两次早退) `:136`(context = PR diff) `:137`(5. 处理 verdict) `:157`(旧 schema) `:252-253`(执行上下文契约 + 裸 `master`) `:260/:265/:299`(not_applicable 语义与 surface 义务) 命中; `report-storage.md:8/:18/:34-39`、`pre-write-validation.md:14/:16-18/:25/:28-30`、`report-format.md:5`、`config-loader/SKILL.md:8-10/:37/:305-331`、`DEFAULTS.json:118-123` 与 audit 键集(确无两个 `allow_*`)、`config-example.md:276-280/:381-400/:402-417/:419-440/:442`、`standards/openspec/project.md:117/:118`、`proposal-minimal.md:28-32`、`configured-gate-authority.md:35/:38/:40`、`skill-benchmark-exemption.md:26-31/:33/:35`、`spec-drafter/SKILL.md:426`、`collectors/audit.py:52/:62-69`、`spec_complete.py:924-930`、`sibling_spec_probe.py:147-151/:380/:684`、`multi_remote.py:107-113`、`test_sibling_spec_probe.py:303-316/:319-336`、`archive/2026-09-04-sibling-spec-probe/proposal.md:513/:387/:397/:544`、`archive/2026-08-23-pre-merge-gate-no-run-for-branch/proposal.md:228/:282-284` 全部命中, **未发现行号漂移**。R1/R2/R3 做的四次行号勘正 (`:250` / `:117-118` / `:28-32` / `:35`) 经实读均正确。
- [minor] implementation/本仓语料数字复算: 顶层 `.md` **837**、含 `context:|spec_id:|change_id:` **582**、`unattributed` 全 8 checkpoint 口径 **170** / `{post_spec,post_planning}` 口径 **160**、真 2-field legacy **6** (六个文件名与定义逐一相符)、`*-audit-trail.md` 族 **5** (含 R2 补列的 `premerge-gate-mainbranch-failclosed-audit-trail.md`, 与 §1.2b 逐字同集)、前缀碰撞 1 对 / 后缀 0 / 中缀 0 —— 全部与文中一致。Critical-1 的证据可复现: `aria-2.0-m6-release-closeout` / `-cost-acceptance` / `-e2e-resilience` 三个在飞 change 的报告 **infix 命中 0 / 末段命中 9·9·1** ⇒ 纯中缀规则确会把它们判 `missing` 假红。
- [minor] implementation/Level 解析统计复算: 按 §1.3 三条判据实跑 `openspec/{changes,archive}/*/proposal.md` **153** 份 → 成功 **144** / 失败 **9** (九个目录名与文中逐一相同) / 首命中 >L15 **恰 7 份** (七个名与行号逐一相同, 最深 `2026-09-06-a1-entry-claim-duplicate-work-guard:58` 实读为 `> **Spec Level**: 2`) / 含 `Spec Level` **15** / 行首 `> **`139 `- **`3 `##`2 其它 **0**。A1 不采纳聚合席「6 份 / 138-3-2-1」的判断**成立** (差源就是 `premerge-gate-branch-existence:13` 那条叙述句被行首锚约束排除)。A3 点名的三型样本 (`:3` 处 `- **Level**: 2` / `- **Level**: 3` / `## Level: 2`) 逐字属实。
- [minor] architecture/R3 findings 落地核验: 3 Critical + 12 Major **全部落在正文** (非批注)。`2d7cccbe`→§1.3 判据 1-3 + §1.1 末段逃生口 + SC-20(3)-(6) + 复议 #10; `7877bac6`→§1.3 级 2b/2c/2d + 级 3 + §1.4 格 B 的 `enabled_by` 前置 + SC-15(5); `34507656`→§1 `--anchor-base` + §1.1 S3 三条 + `no_spec_unverifiable` + SC-5(8)/SC-17(4); `3fa67e89`→§4:270 / Tasks:328 / 复议 #4 三处已一致改为 v1.73.1(PATCH)/v1.74.0(MINOR), 实测 `git -C aria tag --list` 最高 `v1.73.0`、`plugin.json`=`1.73.0`、`VERSION:3`=1.73.0、gitlink=`f314785`, 版本回退风险已解除。基线声明经实测成立: `git diff --stat 301641b f314785` 对六个代码/规程文件**输出为空**, 而 `CHANGELOG.md:3020@301641b` 与 `:3045@f314785` 逐字同行。
- [minor] architecture/消费方与同步面核验: 全 skill 树对 `allow_incomplete_checkpoints` / `missing_checkpoint` **零代码消费** (两处 grep 命中是 `state-scanner` 里同名短语「completeness gate」, 语义无关); `.aria/state-checks.yaml` 16 个已注册 check 无一触及 audit-engine / audit-reports (`config-template-key-currency` 作用域仅 `phase_c_integrator.pre_merge_gate`, `skill-md-sha-backlink-literal-sync` 锚在 openspec-archive); `grep -rn 'audit-reports/[a-z_]*-{timestamp}\.md' skills/` **恰 4 处**且与 §4 列表逐一相符; 主仓 16 个版本字符串点逐行实读全部在场且现值 v1.73.0。`check_bare_issue_refs.py` 确实未被任何 SKILL.md / state-checks.yaml / standards 引用 ⇒ Tasks 里「不当门, 请 owner 明确」的处置符合 Rule #10。
- [minor] testing/SC-2 采样可行性: Tasks B.0 第 4 条属实 —— 「两族各 ≥3」的唯一候选 `state-scanner-mechanical` 的 15 份报告实测 **0 份**有独立源字段。补充一条对 Phase B 有用的实测: 放宽到「两族各 ≥1 且两列都可取」时**存在真实语料候选** `state-scanner-inter-cycle-surfacing` (F-a 2 份 / F-b 3 份, 均带 frontmatter 字段), 故规则 (c) 分支不必退化成「用 `--change-id` 自造样本」(那会把 SC-2 推回它要防的自指)。

### Issues

- [major] implementation/§1.3 Level 判据的实跑校准段: `proposal.md:184` 写「上述判据对 153 份的结果 = 解析成功 144 (Level 3 → 57 / Level 2 → 86 / Level 1 → 1)」并断言「严格判据 vs 原稿宽松正则逐份对照, 144 份取值**逐个相同**, 判据收窄未引入取值漂移」。本席按 `:181` 判据 2 (含**本轮新增**的剥 `~~…~~` 子规则) 实跑得 **Level 3 → 58 / Level 2 → 85**, 且严格判据与宽松正则**恰有 1 份取值不同**: `openspec/archive/2026-08-16-premerge-gate-branch-existence` 由 2 翻 3 —— 正是 A2 用来论证剥删除线必要性的那一份。⇒ 该段的分布数字与「零漂移」断言是**剥离规则加入之前的旧结果**, 与同节判据自相矛盾; 「零漂移」若被 Phase B 采信, 可反推出「剥不剥都一样 ⇒ 可省」的错误结论 (SC-20(4) 会挡住, 故未升 Critical)。修法: 分布改 58/85, 「逐个相同」改为「144 份中 1 份取值由 2 变 3, 即 A2 点名的那份, 其余逐个相同」。(证据: proposal.md:181,184; 实跑 153 份全枚举)
- [major] testing/Rule #6 替代面对 `phase-c-integrator-pre-merge-gate.json` 的事实陈述与动作定义: 文中四处 (`:12` 头部 Rule #6 行 / `:324` Tasks AB / `:348` SC-14(a) / `:362` rule6_note) 均称「8 条 `fixtures[]` **每条**带 `test_case_in_unit_tests` 指向 `test_pre_merge_gate.GateCheckTests.*`」, 并据此把动作定义为 `python3 -m unittest test_pre_merge_gate.GateCheckTests`。实读该 json 的 8 条绑定: `green`/`wait`/`fail`/`NEG-1-malformed` → `GateCheckTests.*` (4 条); `NEG-4-no-run-for-branch` → `test_pre_merge_gate.**NotFoundVerdictTests**.test_sc2_trigger_matched_message`; `NEG-3-internal-error-surface` → `**test_path_coverage**.InternalErrorReasonTests.*` (另一模块, 实测该类在 `test_path_coverage.py:907`); `wait_then_green` → `test_gate_state_helper polling tests + integration` (该模块实际在 **workflow-runner/tests/**, 跨 skill); `NEG-2-timeout` → `test_pre_merge_gate (timeout path; integration scenario)` (**无可执行 node id**)。⇒ (1) 事实陈述为假; (2) 规定的命令只覆盖 **4/8**, SC-14(a)「8 条 fixture 对应用例全绿」按字面不可执行; (3) 待 owner 复议 #9 的裁决依据也建立在这句假陈述上。修法: 把绑定按实际拆成三条命令 (`GateCheckTests` + `NotFoundVerdictTests` + `test_path_coverage.InternalErrorReasonTests`), 对 `NEG-2` / `wait_then_green` 两条无可执行绑定的显式记为该 catalog 自身的缺口 (与套件缺口 issue 同面)。(证据: proposal.md:12,324,348,362; aria-plugin-benchmarks/ab-suite/phase-c-integrator-pre-merge-gate.json fixtures[]; aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py:187,964)
- [major] architecture/`no_spec_unverifiable` 在跨仓 Level 1 是无逃生口硬阻, 且未进 §5 枚举: `:84` 规定 `--no-spec` 的核验面**恒取锚点仓** (主仓), `:111` S3(ii) 规定锚点面 `len(diff)==0` ⇒ `no_spec_unverifiable` exit 2 **不放行**, `:114` 明示该 error **不被** `allow_incomplete_checkpoints` 豁免 (S1 的 `allow_dangling_change_ids` 也不覆盖它)。但本项目自述「子模块 PR 正是 pre_merge 的主力场景」(`:82`), 而 **Level 1 周期按定义无 spec ⇒ 主仓侧通常没有任何伴随提交** ⇒ 锚点面 `git diff $(merge-base HEAD origin/master)` 结构性为 0 行 ⇒ 该格必然触发, 消费方 fail-closed + `on_fail: 阻塞合并` 且**两个 owner 旗标都救不了**。这与 R2 判 Critical 的 `fdb30703`「无逃生口硬阻」同结构 (方向 fail-closed 且人群更窄, 故本席记 major 而非 critical)。另: `:280-288` 的「八条行为变更」自称穷举, 未含这条新增硬阻; `:298` R-b 只讨论了残余假绿, 未提该假红面。修法二选一 (属放行面变更, 宜列 owner 裁): (a) 把「锚点仓在本分支零 diff」与「diff 非空但不触 change 目录」区分开, 前者降级为 `[WARN] --no-spec 不可核验` + 继续按 `missing`/`present` 评估; (b) 保持硬阻但显式给它挂一个既有旗标 (并入复议 #10 一并裁), 同时补进 §5 与 SC-17 的跨仓格。(证据: proposal.md:82,84,111,114,280-288,298)
- [minor] documentation/SC-13 的先例锚点勘正注写反: `:347` 称「原稿锚的 `execution-modes.md:152` 实为竞品探针节的 blockquote …… **不含任何计数断言**」。实读 `:152` 逐字含「上方 Convergence / Challenge 两个围栏块内各有一条同字面的两行调用串 (**机械护栏 SC-17 计数恰 2**)」—— 它不但含计数断言, 而且正是「分块计数 / 两块共 2」这一读法的**直接 SOT 支撑**。分块计数的结论本身与 `archive/2026-09-04-sibling-spec-probe/proposal.md:513` (「两节的围栏块切片分别计数……每块恰 1 次 (共 2)」+ 块外 0 次负控) 一致, 故只需改这句注的措辞, 不必改 SC-13 的判据。(证据: proposal.md:347; execution-modes.md:152; archive/2026-09-04-sibling-spec-probe/proposal.md:513)
- [minor] testing/SC-15(4) 缺作用域前提且不在回扫清单里: `:349` SC-15(4) 的两格 fixture 只给 `experiments.*` 配置, 无 `--change-id`、无锚点、无触 `openspec/changes/**` 的 diff ⇒ 按 `:91` 的求值总序 P2 先落 S4 `change_scope_unresolved` exit 2, 与其断言的 `checked_checkpoints == ['post_spec']` / 「落格 B 判 pass」直接冲突。而 `:103` 与 Tasks `:316` 的作用域补齐清单逐字只列到「SC-15(2)(3)」, (4) 两格既不在清单内、自身也没写 —— 与 R3 修 `94c6bfb1` 时清扫的是同一族。修法: 把 SC-15(4) 加进 `:103`/`:316` 的补齐清单 (或就地补 `--change-id x` + 锚点)。(证据: proposal.md:103,316,349)
- [minor] implementation/S4-bypassed 的 `checked_checkpoints` 在 adaptive 档未定义: `:122` 规定 S4 被豁免时 `change_ids=[]`、`results=[]`、「`checked_checkpoints` 照常枚举」。但 `:99` P4 的纳入判定是 per (checkpoint, change_id) 且 adaptive 档要读**该 change 的** Level (`:170` 级 2a) —— `change_ids=[]` 时无 Level 可取, 「照常枚举」在 adaptive 下无定义; SC-9(2) 也只锁 `verdict/exit/error_kind/scope_source/change_ids/results`, 未锁该字段 ⇒ 两个合法实现可给不同值 (空 list vs 仅 explicit 档), 正是本 spec 反复要消除的那类歧义。修法: 明确该格 `checked_checkpoints` 取「仅 `explicit` 档的键」或直接取 `[]`, 并在 SC-9(2) 加一条字面断言。(证据: proposal.md:99,122,170,343)

### Risks

- [minor] 无新增风险条目。本席对既有 Impact 表的 R-a/R-b/R-c/R-e/R-f/R-g/R-h 逐条核对方向与量级, 除上文 major 3 指出的 R-b 缺一半失效面外未见新问题; R-h 的「陈旧 base ⇒ 超集 ⇒ 假红」方向与我对 `git merge-base` 语义的独立判断一致。

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **3** / Minor **3** (另 6 条 decision 不计入)。

理由: 本轮从代码级透镜做的约 40 处 `文件:行号` 抽验**零漂移**, 语料与 Level 统计的独立复算除一处分布数字外全部命中, R3 的 15 条 C/M 全部落在正文而非批注, 版本回退这类会真正伤到 Phase B 的项已修实。三条 major 都不是「方案错」: 两条是**勘正自身引入的事实错误**(Level 分布/零漂移断言、AB fixture 绑定陈述), 一条是**修 Critical `34507656` 时新开的硬阻面未闭合**(跨仓 Level 1 无逃生口 + 未进 §5 枚举)。三者均为局部改写即可闭合, 不触及 §1.1-§1.4 的判据骨架, 故不阻断继续收敛; 但按本项目「事实断言必须实证」的硬规则, 它们必须在下一版落地后才谈收敛。

## 轮次记录

### Round 4

- Agents: code-reviewer (本报告为五席之一; 本席为本轮新席位, 不继承前三轮结论)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions 数: 12 (Decisions 6 / Issues 6 / Risks 0)
- Vote: REVISE
