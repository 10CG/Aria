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
timestamp: 2026-09-10T19:15:00.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [code-reviewer]
---

# post_spec R5 单席报告 — code-reviewer (pre-merge-completeness-gate-change-scope)

席位透镜: 代码级核对 —— 逐条打开 proposal 引用的「文件:行号」验证真伪 (行号漂移 / 函数名错 / 分支描述与真代码不符 均算 finding); 改动是否破坏同文件其它调用路径; 文档同步面是否列全。本轮只审不改, 未编辑任何仓库文件。

## 审计结论

### Decisions

- [minor] implementation/R4 `b2bc13a6` (Level 分布) 落地复算: 本席按 §1.3 三条判据独立实现解析器对 `openspec/{changes,archive}/*/proposal.md` **153** 份实跑 —— 剥删除线 L3 **58** / L2 **85** / L1 **1**, 不剥 57/86/1, 两跑唯一取值不同的文件 = `openspec/archive/2026-08-16-premerge-gate-branch-existence/proposal.md`; 解析失败 **9** 份 (与点名清单逐份同集)、首命中行 >15 共 **7** 份 (最深 `2026-09-06-a1-entry-claim-duplicate-work-guard` L58)、行首形态 **139/3/2/0**、含 `Spec Level` **15**。R4 的这条 4 席 Major 已真正落进判据本体, 数字属实。(证据: proposal.md:219-223 vs 本席实跑)
- [minor] testing/R4 `29c39e2c` 与 `6c4455bd` 的事实面: `aria-plugin-benchmarks/ab-suite/phase-c-integrator-pre-merge-gate.json` 实读 `type: "workflow_skill_subextension"`、**无 `evals` 键**、8 条 `fixtures[]`, 绑定分布 = `GateCheckTests` 4 / `NotFoundVerdictTests` 1 / `test_path_coverage.InternalErrorReasonTests` 1 / 无可执行 node id 2, 与 proposal.md:431 逐条一致; SC-2 候选 `state-scanner-inter-cycle-surfacing` 实测 F-a **2** (`post_spec-R1/R2-2026-05-08-…`) / F-b **3** (`pre_merge-R1-R*-2026-05-09-…-sub-pr-{a,b,c}`), 独立源字段命中 **5/5**。(证据: proposal.md:376,405)
- [minor] documentation/外部 SOT 行号全量抽验: `execution-modes.md` (:15 优先级链 · :23-82 节 · :32 触发条件 · 围栏 :34/:66 · Step 1-5 = :37/:41/:46/:54/:63 · :44/:82 两种豁免拼法 · :51-52 mid_post_spec · :152 「机械护栏 SC-17 计数恰 2」· :185 「不得从 hits == [] 推断」) · `audit-engine/SKILL.md` (:49-54 四参表 · :75-81 · :105 · :123-125 探针块 · :381-388 两个 allow_* · :391 优先级链 · :398-400 DEC-4 降级非 skip · :403-419 file-scope · :410-411 pass-through · :427-433) · `phase-c-integrator/SKILL.md` (:131/:132 两道早退 · :136 context=PR diff · :137 处理 verdict · :157 旧 schema · :252 执行上下文契约 + `--no-renames` · :253 裸 master · :265 surface 义务 · :299) · `report-storage.md:8,18,34-39,43` · `pre-write-validation.md:3,14,16-18,20-26,25,28-30` · `report-format.md:5` · `collectors/audit.py:52,62-69` (`_CHECKPOINT_PREFIX` + `"-" + name[m.end():]` 单侧合成属实) · `spec_complete.py:924,1642` (proposal-only 零评估早退逐字属实) · `config-loader/SKILL.md:8-10,28,37,305-331,316-327` + 零 `.py` · `DEFAULTS.json` audit 块 (八键全 off / adaptive_rules off-convergence-challenge / 无两个 allow_*) · `config-example.md:276-277,280,381-400,402-417,419-440,442` · `standards/openspec/project.md:117,118` · `proposal-minimal.md:28-32` · `configured-gate-authority.md:35,38,40` · `skill-benchmark-exemption.md:26-31,33,35` · 三份先例 proposal (`sibling-spec-probe:387,397,513,544` / `pre-merge-gate-no-run-for-branch:55-57,228,282-284` / `handoff-multibranch:372,386,510`) —— **逐条命中, 无一错格**。
- [minor] documentation/语料与发版面统计复算: `.aria/audit-reports/` 顶层 **843** 份 `.md`, 子目录恰 `wf-r1fix` / `pr19-submodule-scan`; 末段形态 **62**、unattributed (全 8 checkpoint 口径) **170**、真 2-field legacy **6**; `C` = 8 + 145 = **153**。主仓 16 个版本字符串点逐点实读: `README.md:8,242` + `README.{zh,ja,ko}.md:3,10,244` (共 11) + `VERSION:24` + `CLAUDE.md:139,141` + `docs/architecture/system-architecture.md:189` + `docs/architecture/version-scheme.md:23` = **16** ✓; gitlink `f314785` = v1.73.0 ✓; 最高 tag `v1.73.0`, `v1.71.2`/`v1.72.0` 未被占用但已过号 ✓; `.aria/state-checks.yaml:47-62` `skill-md-sha-backlink-literal-sync` 存在、`enabled: true`、description 逐字含「2026-09-06 实测已漂移」✓。

### Issues

- [major] architecture/§3 步骤 3 调用方链 × §1.3 优先级链级 2b/2c: §3 把调用方步骤 3 改写为「`checkpoints` 显式值 > `adaptive_rules` 推导值 > 默认 off 的优先级链 + **adaptive 档取上界**」, 只给三档, 未定义 `audit.mode` ∈ {`convergence`, `challenge`, `manual`} 时调用方如何判。而门侧 §1.3 是**五档** (级 1 / 2a / 2b / 2c / 2d)。对 `{audit:{enabled:true, mode:"convergence"}}` 且无 `checkpoints` 块的采用方 —— 正是 SC-15(5) 的 fixture、R3 Critical `7877bac6` 的目标人群、本 spec 自述本仓 `.aria/config.json` 「只是它同时写了 checkpoints 块才没被击穿」的那一格 —— 一个合法读法下调用方走 `explicit 未命中 → adaptive_rules 不适用 (mode≠adaptive) → 默认 off` ⇒ **步骤 3 早退, 门根本不被调用** ⇒ 级 2b 的修复在生产路径不可达。这与 R4 判 Major 的 `bb0e565f` 是同一失效, 修法只覆盖了 2a 一档; §5 第 7 条的新增前提同样只提 `adaptive_rules` 推导那一类。SC-13 新增的接缝 grep 只断言文件含逐字串 `checkpoints 显式值 > adaptive_rules 推导值`, 两个读法都能过。(证据: proposal.md:309-313, :215, :418 SC-15(5); `phase-c-integrator/SKILL.md:132`; `config-loader/config-example.md:276-277`)
- [major] implementation/§1.0 求值总序 × §1.1 S4-bypassed × §1.4 四格分割证: 总序表 P0→P6 从未定义「bypass / 短路是否终止求值」。构造实例: config `{audit:{enabled:true, mode:"manual", checkpoints:{post_spec:"convergence"}, allow_incomplete_checkpoints:true}}`, 不传 `--change-id`/`--no-spec`, diff 不触 `openspec/changes/**` —— P2 落 S4 ⇒ 按 §1.1 降为 `verdict=bypassed` exit 0, `change_ids=[]`, `results=[]`, `checked_checkpoints=['post_spec']`; 但 `change_ids=[]` ⇒ 纳入集空 ⇒ **P5 照总序求值格 B/C/D**, `resolved(pre_merge)` 走级 2d 得 `"off"` + `enabled_by="manual-default"` ⇒ **格 C `pre_merge_not_enabled` exit 2**。R4 新增的「四格互斥与全覆盖证」明写「不存在落不进任何一格的输入」且唯一豁免条件是「纳入集非空」, 反而把这条冲突钉死。SC-9(2) 第一跑用的正是这一 config 并断言 `verdict=bypassed` / exit 0 / `error_kind=null` ⇒ 两个合法实现判决相反, 与 R3 `506ce733`、R4 `01b9faf6` 同族的「Phase B 结构性必红」。SC-9(4) 的 `spec_level_undetermined` 一格同理。(证据: proposal.md:101-112 总序表, :138 豁免行, :146 S4-bypassed 字段, :273-276 格 C 与分割证, :412 SC-9(2))
- [major] documentation/proposal 全文自引行号 (v4 397 行 → v5 469 行未回扫): R4 rework 增 72 行后**内部自引一处未更新**。本席逐条实读比对, 至少 18 处错位: `:82`→实为 92 (「子模块 PR 是主力场景」, 4 处引用) · `:84`→94 (`--no-spec` 恒取锚点仓, 3 处) · `:86`→96 (`--base` 无缺省) · `:87`→97 (`--change-id`/`--no-spec` 互斥, 3 处) · `:81`→91 (`--diff-repo-path`) · `:103`→114 (fixture 硬约束) · `:114`→138 (两个 allow_* 豁免面, 3 处) · `:143`→182 (§1.2 计数表) · `:186`→225 (`spec_level_undetermined` ERROR 文案) · `:190`→229 (逐对不叉乘) · `:202`→241 (§1.3(c) 自证段) · `:220`→259 (格 A/C 生产不可达论证) · `:222`/`:230`→255 (报告目录不存在) · `:243`→285 (§1.4 unattributed trail 行) · `:286`→343 (§5 第 6 条)。其中 line 82 / 222 / 226 / 230 在当前文件里**是空行**。Phase B 无人值守, 这些是导航指针; rework 记录的「下游同步核对」列了键数、格数、条数、编号面、参数面五轴, **独缺自引行号一轴**。(证据: proposal.md:94,109,134,135,161,279,313,314,347,407,413,418,420,423,425,459,461 与对应真实行内容)
- [major] testing/Tasks AB 命令 / SC-14(a) / rule6_note / 待 owner 复议 #9: R4 `29c39e2c` 逐条实读了 catalog json, 但**没有核实 node id 指向的方法是否存在**。`NEG-1-malformed` 绑定的 `test_pre_merge_gate.GateCheckTests.test_case_e_malformed_aether_routes_fail` 在全插件树只出现于该 json 一处 (`ab-suite/phase-c-integrator-pre-merge-gate.json:55`), 真实方法名是 `test_case_e_malformed_aether_main_leg_routes_fail` (`test_pre_merge_gate.py:266`); 本席按字面实跑该 node id 得 `FAILED (errors=1)`。⇒ 按 node id 可执行的绑定实为 **5/8** 而非 proposal 写的 6/8, 该 catalog 自身缺口是 **3** 条而非「余下 2 条」; 复议 #9 请 owner 拍板的数字再次不准 —— 与 R4 刚判 Major 的那句假陈述同一根源 (只读目录不核目标)。本 spec 规定的三条命令按类跑仍能覆盖 NEG-1, 不构成假绿, 但缺口枚举与 owner 依据错。(证据: proposal.md:386-392, :417 SC-14(a), :431, :455; `ab-suite/phase-c-integrator-pre-merge-gate.json:55`; `phase-c-integrator/tests/test_pre_merge_gate.py:266`)
- [major] documentation/§4 同步表 execution-modes 行 × §5 第 2 条: §5 第 2 条逐字声明反转 `execution-modes.md:41-44` 的豁免语义 ——「原义是『跳过校验, 继续执行』(整门不算), 本 spec 改为『仍逐对评估三态并全部留痕, 只把 missing / S4 降为 bypassed』」。但 §4 同步表的 execution-modes 行只列 `:23-82` (含 `:15` / `:37-38` / `:46-52` / `:44` / `:82`), §2 的 execution-modes 条目也只枚举「互补说明 :25-30 / Step 1 :37-38 / Step 3 :46-52 / Step 4-5 / :68-80 / :44 与 :82 文案统一」—— **`:43` 逐字「→ 跳过校验, 继续执行 pre_merge 审计」没有任何落点**。Phase B 照表执行后 SOT 会变成自相矛盾的 Step 2 (「跳过校验」却打印 `missing={cp}@{change_id}` 列表)。SC-13 只断言两处 bypass 文案逐字相同, 抓不到这一格。Rule #3 面。(证据: proposal.md:337-339 §5 第 2 条, :304 §2, :321 §4 同步表, :416 SC-13; `execution-modes.md:41-44`)
- [minor] implementation/§1.3 优先级链表头 × §1.4 config 读取: 表头逐字写「判据 (对**原始** `.aria/config.json` + 旧配置兼容映射后的视图求值)」, 但级 2a 要读 `audit.adaptive_rules.level_{N}`、级 2b/2c/2d 要读 `audit.mode`。严格 raw 读法下, 一份合法的最小 config `{audit:{enabled:true}}` (无 `mode`) 会落级 3 ⇒ `config_unreadable` exit 2 硬阻。§1.0 末段「脚本内联缺省 `mode=\"adaptive\"`」与 §1.4「内联 DEFAULTS audit 子集缺省」才把它消歧 ⇒ 建议把 raw 视图的适用面收窄到「级 1 的键存在性判定」一处。(证据: proposal.md:206, :114, :247)
- [minor] documentation/§1 `[WARN] base ref 陈旧` 文案: 文案模板逐字含「merge-base 可能偏移, **S2/S3 的 diff 判据**会被弱化」, 但 R4 `a00c52bb` 已把 S2 与 S3 双双改取锚点面 ⇒ 驱动它们的是 `--anchor-base`, `--base` 轴只剩 §1.3 `not_applicable` (b) 通道一个消费点。R-h 与 SC-22(1)(iii) 都已按新轴改写, 唯独 WARN 文案本体没跟着改 —— 而它是要逐字写进实现和 SC 的。(证据: proposal.md:96 与 :91, :358, :425)
- [minor] documentation/Tasks Phase D `check_bare_issue_refs.py` 计数: 写「对本 proposal **今日**实跑报 **64** 条裸 `#N` (审计当时 55, 语料在长)」。本席同日实跑 `python3 aria/skills/state-scanner/scripts/check_bare_issue_refs.py <proposal>` 得 **84**。该数字显然在 R4 rework 增 72 行之前取, 落盘即过期。同一句里「该脚本未被任何 SKILL.md / `.aria/state-checks.yaml` / `standards/` 引用」经本席 `grep -rl` 复核**成立**。(证据: proposal.md:398)
- [minor] testing/SC-11 活体命令 × `--repo-path` 契约: SC-11 的命令写作 `--change-id pre-merge-completeness-gate-change-scope --base master` —— 既缺 §1 调用模板与 §2 输入参数表 (标「pre_merge 必传」) 的 `--repo-path`, 又用裸 `master` 与 §1「生产调用方**必须**传远程跟踪 ref」相冲 (会触发本 spec 自己定义的 `[WARN] base ref 陈旧`)。且 `--repo-path` 是否 argparse 必填、缺失时是否 exit 2, 全文未定义, SC-10 只锁了 `--base` 缺失一格。(证据: proposal.md:414, :75-78, :90, :96, :297, :413)

### Risks

- [minor] testing/活体语料增长对数字类断言的侵蚀: 顶层语料本轮实测 **843** 份 (R1 记 786, R4 记 843), `C` 由 152 长到 **153**, 本 proposal 自身的裸 `#N` 由 64 长到 **84**。SC-2 / SC-4 / SC-11 的字面数字全靠 B.0 `corpus-freeze.md` 兜底, 而 B.0 的「取样时刻」与 Phase B 实施之间若跨天, 期望值会再次漂移。proposal 已把「语料是活体」成文 (Tasks B.0 item 4), 缓解到位; 此处只记为持续风险, 不作为 finding 要求改动。(证据: proposal.md:376, :405, :414)

## Verdict

**PASS_WITH_WARNINGS** — Critical 0 / Major 5 / Minor 4 (另 4 条 decision + 1 条 risk 不计入缺陷数)。

理由: 本轮逐条打开 proposal 引用的**外部** SOT 文件行号 (execution-modes / audit-engine SKILL / phase-c-integrator SKILL / report-storage / pre-write-validation / report-format / collectors-audit.py / spec_complete.py / config-loader 全组 / standards 四文件 / 三份先例 proposal), **无一错格**; R4 三条最重的落地 (`b2bc13a6` Level 分布 58/85/1 · `29c39e2c` catalog 绑定拆解 · `6c4455bd` 选样候选) 经本席独立实跑逐项复现, 修法都落在判据本体而非批注 —— 方案没有错误, 没有会破坏消费方的改动, 也没有发现新的 SC 恒绿假绿, 故 **0 Critical**。

但五条 Major 都是可机械证伪的实体缺陷: 两条是「同一个失效只补了一半」(调用方链缺 2b/2c 档、Step 2 语义反转无同步落点), 一条是求值总序留下的两读法冲突 (S4-bypassed 与 P5 空集分格互斥, SC-9(2) 必有一读法红), 一条是 R4 勘正本身漏核 (catalog node id 在真代码不存在, 6/8 实为 5/8), 一条是 rework 未回扫自引行号 (≥18 处错位, 4 处指向空行)。按判定规则 0 Critical + ≥1 Major ⇒ PASS_WITH_WARNINGS; 按本席投票口径 Major > 0 ⇒ **REVISE**。

## 轮次记录

### Round 5

- **Agents**: code-reviewer (五席之一, 本报告为单席产出)
- **Sibling probe**: 本轮已完整扫描, 未发现同 issue 竞品
- **Conclusions 数**: 14 (Decisions 4 / Issues 9 [Major 5 + Minor 4] / Risks 1)
- **Vote**: REVISE
