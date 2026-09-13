---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-13T18:20:00.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [knowledge-manager]
---

## Findings

- [major] documentation/手册 §场景 4 (issue): 手册现状场景 4 指 run_loop.py 优化流程 (产出 best_description 建议), 本 Spec T2 拟重写为 run_eval.py 地板守卫 (pass/fail 门禁), 未说明同名场景内两种机制 (优化 vs 门禁) 是并存、降级还是被替换, 易致执行者混淆该跑哪个脚本。
- [major] architecture/proposal.md §D1 (issue): D1 未点名「另跑场景 4 地板守卫」落在 SOT §2 决策表哪一格 (第二行细化, 还是新增独立义务), 也未点名要替换的是 CLAUDE.md 表后哪句 / SOT §33 (「附加约束」段) 哪句的具体旧文字, 三处执行者各自改写易生结构分叉。
- [minor] documentation/SOT §6 (risk): T3 拟在 §6 追加第三条已知局限, 但 §6 开篇「后者另有两个已知缺陷记录在案」的计数语未列入待改任务, ship 后与新增第三条内容数目不符。
- [major] documentation/proposal.md §D4 (issue): grep 既有 rule6_note 语料 (2026-08-23-linked-issue-normalization、2026-09-06-owner-container-identity-key-and-collision-parser 等) 显示 rule6_note 是自由格式 markdown 表格 (字段因 spec 而异), SOT §4 本身未定义一个带固定"栏位"的结构化模板; D4「加两栏」假设了一个当前不存在的实体, SC-3「试填模板」缺可编辑的具体锚点。
- [major] architecture/proposal.md §D5 (issue): 「为 43 个 skill 建 trigger-eval.json 是增量债, 本 Spec 不建」的决定拟只记入手册散文, 未开专门 issue 追踪; 与 #150 / #190 同类缺口均开 issue 的项目惯例及 SOT §3「套件盲区是债, 须开 issue」的机制不一致, 决定容易随手册改写丢失可追溯性。
- [major] testing/proposal.md SC-2 & D3 (risk): RESULT.md 未标注 commit SHA/版本, 其具体数字 (负控 8/30、p<0.0001、技能数 97 vs 13) 被 CLAUDE.md/SOT/手册三处正文直接复述; 若 qa 席指出的 n=30 应按 query 级 n=10 重算 Fisher 检验等复核意见成立并修订 RESULT.md, 三处复述文本会与之脱钩, proposal 未设「RESULT.md 修订后需重核三处引用」的机制。
- [minor] documentation/proposal.md Why (observation): Why 节引用 `10CG/Aria#211` 与其 triage comment 23915, 但未直接引用 `10CG/aria-plugin#190` comment 22921 (该洞最早的实测记录处, #211 原文亦称"目前这个洞只活在 #190 的一条评论里"), 建议补交叉引用以完善溯源链。
- [minor] architecture/aria-standards#17 (risk): #17 提议在同一 SOT 文件 (skill-benchmark-exemption.md) 相近区域 (§2/§4/§6 附近) 新增"AB 范围"一节, 目前 open 且 comments=0 未见 draft; proposal 未提及 #17。T6 本地合并前应 check #17 是否已产生并行编辑, 以免结构/编号冲突。

## Verdict

PASS_WITH_WARNINGS — 0 critical / 5 major / 3 minor。Spec 结构完整 (Why/What/Deliverables/Impact/Tasks/SC/OQ/rule6_note 齐备), 核心句已在 D1/SC-1 钉死可 grep 的字面, RESULT.md 三点结论与 Spec 结论一致、无夸大。但存在 5 项 major: 场景 4 新旧含义并存未消歧、落点未点名决策表具体格位与旧文字、rule6_note"模板"概念与既有语料形态不符、trigger-eval 覆盖缺口未开 issue 追踪、RESULT.md 引用稳定性无版本锚点。建议 Phase B 执行前 (或作为 T1/T2 的前置澄清) 逐条处理, 不构成阻断性缺陷但会影响三处文本落地的一致性与可维护性。

## Vote

REVISE

## 术语与关系对照表

| 术语/概念 | proposal.md | RESULT.md | SOT (skill-benchmark-exemption.md) | 手册 (AB_TEST_OPERATIONS.md) | 一致性 |
|---|---|---|---|---|---|
| 场景 4 | D2/D3: run_eval.py 触发率地板守卫 (pass/fail 门) | 未直接用"场景 4"一词, 但工具即 run_eval.py | 未提及 (T3 待引用) | 现状 (行 263-275): run_loop.py 优化流程 (产出 best_description); 触发时机已写"修改 description/frontmatter 后" | **不一致** — 同名不同工具/不同输出形态, 见 Finding 1 |
| 地板守卫 | D1/D2 核心概念, 判据 = should-trigger≥阈值 且 should-not<阈值 | 首次提出 ("它可以当地板守卫") | 未提及 (T3 待新增) | 未提及 (T2 待新增) | 一致 (spec 忠实继承 RESULT.md 用语, 尚未落地到 SOT/手册) |
| 测量剧场 | Why 节引用 ("是另一个测量剧场") | 结论 1 使用同词 | §3 末尾原创该词 | 未出现 | 一致, 溯源清晰 (SOT → RESULT.md → proposal) |
| 触发率评测 / 区分力 | D2/D3, OQ-1 | 全篇核心量化指标 (Fisher p 值) | 未出现 | 场景 4 现状未用"区分力"一词, 只说"优化 description" | 基本一致, 但"区分力"是 RESULT.md/proposal 的分析框架, 手册現状场景 4 无此维度 (印证 Finding 1) |
| rule6_note | D4: "模板加两栏" (假设结构化模板存在) | 未涉及 | §4: 只要求"留 rule6_note 引用本规范", 未定义字段/栏位 | 未提及 rule6_note | **不一致** — 既有 archive 语料显示 rule6_note 实践中是自由格式表格/段落, 无固定"栏"概念, 见 Finding 4 |
| Rule #6 判据表落点 | D1 说"表后那句"三处同批, 未点名具体是决策表第几行的延伸 | 不涉及 (RESULT.md 只谈证据, 不谈规则落点) | §2 决策表第二行 + §33"附加约束"段现文本 | §480 附近"边界与留痕"现文本 | proposal 未显式声明落在第二行 (细化) 而非新增第四行, 见 Finding 2 |
| 43-skill 覆盖缺口 (trigger-eval.json) | D5: "本 Spec 不建, 只建 openspec-archive 一份"; 记入手册"已知局限" | 不涉及 | §3 规则: "套件盲区是债, 须开 issue" | T2 待新增"已知局限" | 决定内容本身合理, 但落盘方式 (仅手册散文, 无 issue) 与 SOT §3 机制及 #150/#190 先例不符, 见 Finding 5 |
