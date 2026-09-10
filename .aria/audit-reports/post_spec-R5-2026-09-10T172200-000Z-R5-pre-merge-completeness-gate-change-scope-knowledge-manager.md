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
timestamp: 2026-09-10T22:37:50.000Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/proposal.md
agents: [knowledge-manager]
---

# post_spec R5 单席报告 — knowledge-manager (pre-merge-completeness-gate-change-scope)

本席为 R5 新席位, **不继承** R1-R4 任何结论。全部事实断言均自行实读/实跑复核 (proposal 自述一律不采信)。审计轮内**只审不改**, 未编辑任何仓库文件。

**本席核验面 (机械, 可复现)**: 被审 proposal 全文 469 行逐段读完; SOT 侧实读 `execution-modes.md` / `audit-engine/SKILL.md` / `phase-c-integrator/SKILL.md` / `report-storage.md` / `pre-write-validation.md` / `report-format.md` / `config-loader/{SKILL.md,DEFAULTS.json,config-example.md}` / `state-scanner/scripts/lib/spec_complete.py`; 实跑 `linked_issue_field_probe.py`、`lib.linked_issue_field.extract_linked_issue_field`、`spec_complete.py --gate`、`check_bare_issue_refs.py`、`git -C aria diff --stat 301641b f314785`、全仓 `{timestamp}` 残留 grep、`audit.checkpoints` 调用方 grep、ab-suite 三份 json 结构解析、forgejo API 取 Aria#199 / aria-plugin#161。

---

## 审计结论

### Decisions

- [minor] documentation/头部 Linked Issue 字段机械判据: 实跑 SOT `lib/linked_issue_field.extract_linked_issue_field` 得 `verdict=OK` / `line_no=6` / `token_elements=('10CG/Aria#199','10CG/aria-plugin#161')`; 仓级探针全仓 `OK (8 份在范围内, 6 条在册)` 且本 spec **不在** grandfathered 白名单 ⇒ spec-drafter 写法三条 (code span / 同 span 逗号分隔 / 无 markdown 链接形) 全合规 (证据: `aria/skills/state-scanner/lib/linked_issue_field.py` 实跑 · `.aria/linked-issue-field-grandfathered.txt` · proposal.md:6)
- [minor] documentation/SOT 行号锚点独立复核: 本文引用的行号逐条命中 —— `execution-modes.md` 围栏 `:34` 开 / `:66` 闭、Step 1-5 落 `:37/:41/:46/:54/:63` (R4 minor `d9578e5d` 的切片订正成立)、`:44` 与 `:82` 确为两种拼法、`:152` 确含「机械护栏 SC-17 计数恰 2」、`:185` 确为防 vacuous-true 句; `audit-engine/SKILL.md:49-54` 恰 4 参、`:123-125` 探针 fenced bash、`:381-388` 两个 `allow_*`、`:398-400` DEC-4「降级非 skip」、`:410-411` 空集 pass-through、`:427-433` 相关文档只写 `.md` 指针; `report-storage.md:8/:18/:34-39`; `project.md:117/:118`; `proposal-minimal.md:28-32`; `skill-benchmark-exemption.md` 判据表 `:26-31` / 附加约束 `:33` / `:35` 标题; `configured-gate-authority.md:35` 第一类与 `:38-40` 第四类边界 (证据: 各文件实读)
- [minor] documentation/版本面与残留族与基线冻结: 主仓 **16** 个版本字符串点 (README×4 共 11 + `VERSION:24` + `CLAUDE.md:139,141` + `system-architecture.md:189` + `version-scheme.md:23`) 逐行实读全部在场且现值均为 `v1.73.0`; `grep -rn 'audit-reports/[a-z_]*-{timestamp}\.md' skills/` **恰 4 处**且与 §4 列表逐一相符, `report-storage.md:37,43` / `report-format.md:5` 不匹配该式 ⇒ SC-13 的「= 0 命中」可达; `git -C aria diff --stat 301641b f314785 --` 对六个代码/规程文件为空 (21 文件变更无一落在其上) ⇒ proposal.md:16 收窄后的口径成立, `CHANGELOG:3020@301641b` 与 `:3045@f314785` 逐字同行 (证据: 实跑 git/grep · proposal.md:16,321-329)
- [minor] documentation/被引 issue·memory·先例真实性: forgejo API 复核 `10CG/Aria#199` = open、`10CG/aria-plugin#161` = open 且标题与 proposal.md:7 逐字相符; 四条被引 memory 文件 (`feedback_author_and_verifier_must_differ_for_corrections` / `feedback_universal_predicate_vacuous_truth_on_empty_set` / `feedback_concurrent_release_numbering_check_remote_tags_and_sibling_vnext` / `feedback_sequenced_multirepo_gitlink_bump`) 全部在场; 归档先例 `2026-08-23-pre-merge-gate-no-run-for-branch/proposal.md:228`(catalog 登记 fixture) `:284`(「照跑 = 测量剧场」+ aria-plugin#127) 与 `2026-09-04-sibling-spec-probe/proposal.md:513`(分块计数先例) `:544`(测试宿主与 run_all_tests 发现) 逐字命中 (证据: forgejo GET · `ls` memory 目录 · 归档件实读)
- [minor] testing/R4 处置落地抽验: 头部审计轨迹写的 R4 = C0/M14/m15、conflicted 0、PASS_WITH_WARNINGS 5/5 与聚合报告 `:192` 逐字一致; 抽验四条 Major 的落地形态 —— `955907f2` 的 SC-15(7) 三格穷举反例在场、`95ddb322` 的 SC-20(7) 逐对不叉乘格在场、`4cbe35ce` 经本席实跑 `spec_complete.py --gate` 复现 `{"verdict":"pass"}` 且零符号分类、`29c39e2c` 的 8 条 fixture 绑定经本席逐条解析确为 `GateCheckTests` 4 + `NotFoundVerdictTests` 1 + `test_path_coverage` 1 + 无 node id 2 ⇒ 均落入正文而非批注 (证据: proposal.md:418,423,415 · ab-suite/phase-c-integrator-pre-merge-gate.json 实读)

### Issues

- [major] architecture/§3 调用方对齐面 · §5 行为变更枚举 · §1.4 missing ERROR 模板: §3 (proposal.md:309) 只把 **pre_merge 调用方** `phase-c-integrator/SKILL.md:132` 改成优先级链读法, 而**产出侧**四个非排除 checkpoint 的调用点仍是同一句字面键早退 —— `phase-a-planner/SKILL.md:246` (post_spec) / `task-planner/SKILL.md:123` (post_planning) / `phase-b-developer/SKILL.md:255` + `:49` (post_implementation) / `brainstorm/SKILL.md:141` (post_brainstorm); 而 `config-loader/SKILL.md:23-29` 的加载流程**不解析 `adaptive_rules`**, 只在步骤 5 与 `DEFAULTS.json` 合并 (八键缺省全 `"off"`, `SKILL.md:243` 逐字 `default: "off"`)。后果: 本 spec 让门首次把 adaptive 档推导出的 checkpoint 纳入校验 (SC-20(1)(2) 正是这么断言的), 但这批 checkpoint 的**报告在生产链上结构性永不产出** ⇒ 场景 B/C 采用方在 pre_merge 拿到 `missing` + `verdict=fail` exit 1 + 消费方 fail-closed = **新的假红硬阻**; 更具体的缺陷是 ERROR 模板保留的 Fix 三项之首「补跑缺失 checkpoint 审计 (对应 Phase Skill 重新调用)」(`execution-modes.md:76`) 对这批人**不可执行** —— 重新调用 Phase Skill 会再次早退; 真正有效的那条 fix (「在 `audit.checkpoints` 里显式写该 checkpoint」) 本文只写给了 `spec_level_undetermined` 那格。而 §5 (proposal.md:336) 恰恰声明「其它 checkpoint 调用方 (phase-a-planner / task-planner / phase-b-developer / phase-d-closer) **不受影响**」, §5 第 7 条 (`:344`) 把该人群的 `missing` 一律称作「这是修复本身」。本条与 R4 已采纳的 `bb0e565f` **同型同族**, 只是形态族没穷举完 (R4 只扫了消费侧一个调用点)。方向是 fail-closed (假红不是假绿), 按 Rule #10 本席**不建议自行放宽放行面**; 最小处置 = (1) 把该类作为 §5 第 11 条成文并给出可执行的 fix 措辞, (2) 在 §4 同步面明确「产出侧四处是否随本 spec 一起对齐」由 owner 裁 (与 #11 同族)。(证据: proposal.md:309,336,344 · phase-a-planner/SKILL.md:246 · task-planner/SKILL.md:123 · phase-b-developer/SKILL.md:49,255 · brainstorm/SKILL.md:141 · config-loader/SKILL.md:23-29,243 · DEFAULTS.json audit.checkpoints 八键实读)
- [major] documentation/Rule #3 同步面 · execution-modes.md Step 2 (`:41-44`): §5 第 2 条 (proposal.md:339) 逐字声明 `allow_incomplete_checkpoints` 的语义被收窄 ——「`execution-modes.md:41-44` 原义是『跳过校验, 继续执行』(整门不算), 本 spec 改为『仍逐对评估三态并全部留痕, 只把 missing / S4 降为 bypassed; S3 的输入矛盾错**不被豁免**』」。但同步面**没有任何一处承接这句**: §2 的 execution-modes 条目 (`:304`) 逐项列的是 互补说明 `:25-30` / Step 1 `:37-38` / Step 3 `:46-52` / Step 4-5 / `:68-80` / `:44` 与 `:82` 文案统一 —— **Step 2 的语义正文 `:42-43` 不在其中**; §4 同步表该行 (`:321`) 的位置列同样只到 `:15/:37-38/:46-52/:44/:82`; SC-13 (`:416`) 的九条文档 grep 也无一断言它。落地后 SOT 会逐字停在「如果 `audit.allow_incomplete_checkpoints == true` → 跳过校验, 继续执行 pre_merge 审计」, 而实现会在同一旗标下对 `no_spec_contradicted` / `no_spec_unverifiable` / `change_id_unanchored` 照样 exit 2 —— 这是**编排者运行时唯一会读的那份处方**与实现直接矛盾, 且正是本 spec 立案要消灭的失效族。处置: 把 `:41-43` 列进 §2/§4 的改动面 (与 `:44` 同批改), SC-13 加一条逐字 grep 锁新措辞。(证据: proposal.md:304,321,339,416 · execution-modes.md:41-44 实读)
- [minor] documentation/§1.4 格 B 人群 1 与 待 owner 复议 #8 的场景 A 描述: proposal.md:263 与 :454 把官方场景 A 写成「`checkpoints` 显式把**七键**写 `off`、只有 `pre_merge: "convergence"`」, 两句自相矛盾; 实读 `config-loader/config-example.md:389-397` 为 **六键 off + `pre_merge: "convergence"`, 共七键** (无 `mid_post_spec` 键)。结论 (四个非排除项全 off ⇒ 纳入集空) 不受影响, 但 #8 是请 owner 拍板的条目, 其人群描述算错一键; 同段 SC-15(3) 的逐字 fixture 反而是对的, 两处口径不一。(证据: proposal.md:263,454,418 · config-example.md:389-397)
- [minor] documentation/§4 同步表 `audit-engine/SKILL.md` 行的位置列: §2 (proposal.md:304) 写「`## 配置依赖` (`:381-388`) **两个** `allow_*` 键的注释各补一句」, 而 §4 该行 (`:322`) 位置列只有 `:49-54 / :75-81 / :385-388 / :427-433` —— `:385-388` 是 `allow_incomplete_checkpoints` 的注释块, `allow_dangling_change_ids` 在 `:381-384`, 未被点名。§4 自述是「Phase B 的照单」, 照单派工会漏改 `allow_dangling` 那半句 (它正是 S1 锚点校验继承该键这条新语义的落点), 与 R4 Major `8acafe0a` 「头部/§2/§4 口径分叉导致漏项」同型。(证据: proposal.md:304,322 · audit-engine/SKILL.md:381-388)

### Risks

- [minor] documentation/Tasks Phase D 与 SC-2 里的活体快照数字: Tasks 记「`check_bare_issue_refs.py` 对本 proposal **今日实跑报 64 条**裸 `#N` (审计当时 55)」, 本席今日实跑得 **84 条** —— 差额来自 R4 rework 自身新增的 72 行。这类「随本文增长而失真」的数字每一轮都会过期 (55 → 64 → 84), 而 Tasks 是 Phase D 的照单; 风险是 Phase B/D 照抄快照值做判断。缓解建议: 该处只留口径与命令 (「实跑该脚本, 数量以当次为准」), 不写死计数; 版本号一栏已用「有保质期, 不得照抄」的写法, 此处沿用同一体例即可。(证据: proposal.md Tasks Phase D 行 · 实跑 `python3 aria/skills/state-scanner/scripts/check_bare_issue_refs.py <proposal>` = 84)

---

## Verdict

**PASS_WITH_WARNINGS** — Critical **0** / Major **2** / Minor **3** (缺陷类 = issue + risk; 另有 **5** 条 decision 不计入)。

rationale: 按 `report-storage.md §Verdict` 与 `verdict-format.md` 的判定规则, 0 Critical + ≥1 Major ⇒ PASS_WITH_WARNINGS; post_spec 的阻塞行为是 `blocking: false`, 本判定不阻断流程 (Rule #10: 该判定不得由 AI 自行升降)。

两条 Major 都不是方案性错误, 而是**同步面/枚举面缺口**, 且是同一族: 本 spec 的修法本身成立 (机械执行器 + 三态 + 优先级链), 但「谁在读同一条优先级链」与「哪些 SOT 正文承接被改的语义」这两张清单没有穷举完 —— 一条落在产出侧四个调用点 (导致新纳入的 adaptive 档 checkpoint 的证据结构上不可产出, 且 ERROR 给的第一条 fix 对该人群不可执行), 一条落在 `execution-modes.md` Step 2 的豁免语义正文。两者都可在正文内闭合, 无需改动本 spec 的核心机制; 涉及「是否连带改产出侧调用方」的部分建议按 Rule #10 转 owner 裁 (与既有复议 #11 同族), 本席不建议 AI 自行扩大或收窄放行面。

事实层面本文的质量在本席核验中很高: 抽查的**全部** SOT 行号锚点、16 个版本点、4 处 `{timestamp}` 残留、ab-suite 三份 json 结构与 8 条 fixture 绑定、并发轨 #195 的 `:510` 锚点、被引 issue/memory/先例, 逐条实测命中; 头部 `Linked Issue` 字段经 SOT 抽取器实跑判 `OK`。R4 的 14 条 Major 抽验四条均已落正文而非批注, 且未见落地引入新矛盾。

## 轮次记录

### Round 5: pre-merge-completeness-gate-change-scope (post_spec, convergence)

- Agents: knowledge-manager (本席, 五席之一; 本报告只代表本席结论, 不含汇总)
- Sibling probe: 本轮已完整扫描, 未发现同 issue 竞品
- Conclusions 数: **10** (Decisions 5 / Issues 4 / Risks 1); 缺陷类计数 Critical 0 / Major 2 / Minor 3
- Vote: **REVISE** (存在 Major ⇒ 按投票规则不投 PASS; 两条 Major 均可在正文内机械闭合)
