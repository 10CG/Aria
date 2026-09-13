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
timestamp: 2026-09-13T17:55:14.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [code-reviewer]
---

# post_spec R1 — code-reviewer 席 (Phase 1 规范合规 + Phase 2 质量)

被审对象: `openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md` @ 主仓 HEAD `298d0e4` (Level 2, Draft, Linked Issue `10CG/Aria#211`); 基线目录 `aria-plugin-benchmarks/ab-results/2026-09-13-rule6-description-trigger-eval-baseline/`。只审不改; 以下每条核对项均实读 / 实跑, 未核对的不下结论。

## Findings

- [major] documentation/proposal.md §Why §D2 §SC-5 (issue): 「新版 ≥ 旧版」判据「会恒绿 / 恒打平」与基线数据不符 —— 负控 8/30 对 旧版 30/30 会把该比较判红, 它并非恒绿; 真实结论是 should-trigger 饱和 (三个真 description 全 1.0) 使比较判据退化为「以旧版取值为参照的地板」, 且参照噪声大 (旧版 1.0 时 29/30 即失败)。D1 要求三处 SOT 逐字同批抄入此理由, 错句会复制成三份。
- [major] documentation/proposal.md §Open Questions (issue): 偏离 issue 验收第 2 条规定动作未请复议 —— 原文「若两个 description 触发率统计无差别, 应改开『触发率评测本身不可用』的单而不是把它写进 Rule #6」; 基线实测 new vs old p = 1.0 正命中该分支, 而 Spec 仍把场景 4 写进 Rule #6 (改为地板守卫)。Why 段有解释, 但这是 AI 对 owner 写下的验收动作的改判, 按 Rule #10 须列为 OQ 请 owner 裁, 现 OQ-1~4 均未涉及。
- [major] implementation/proposal.md §D4 §T3 §SC-3 (issue): 「rule6_note 模板」不存在 —— `grep -rn rule6_note` 于 `standards/` `CLAUDE.md` `AB_TEST_OPERATIONS.md` `spec-drafter/` 仅命中「留 `rule6_note` 引用该机制」两处, SOT §4 无任何字段定义。「模板加两栏」无宿主, SC-3 反事实「旧模板判不出」对不存在的模板真空成立。T3 须改为「在 SOT §4 定义 rule6_note 最小模板 (含既有隐含字段 + 新两栏)」, SC-3 反事实改为对比「无模板时的 ship 记录」。
- [minor] documentation/proposal.md §D1 (issue): 落点写「行 480 附近」自引行号 (今日正确, 手册 678 行, 每轮编辑必腐; memory: 长文档改锚点式) —— 改为引小节名「§确定性代码层变更 — deterministic substitute 豁免 / 边界与留痕」。
- [minor] documentation/proposal.md §Why 第 3 条 vs §D5 (issue): Why 说「两处结构性缺陷」, D5 反馈 (a) (b) (c) 三项; RESULT.md 把 (c) 标为「附带」(设置源与成本), 不是缺陷。二处口径统一, 或在 D5 注明 (c) 是配置建议非缺陷。
- [minor] documentation/proposal.md §Impact 成本行 (risk): 「约 12 分钟」隐含两臂并行 —— 基线 v3 是 4 臂并行各 `--num-workers 1` (run.log: 每臂 10m39s–12m03s), 顺序跑 2 臂约 22 分钟; 「0.06 美元/次」在仓内无机器产物 (各臂 json 无 cost 字段, `.err` 未入库, 仅 RESULT/manifest prose), SC-2 (c) 的「97 vs 13」同样只有 prose。宜注明并行假设, 并把 smoke 的成本/技能数原始输出补进基线目录。
- [minor] testing/proposal.md §SC-2 §D3 (issue): D3 第 3 条后半「显式 `--model`」无基线实证 (来自 skill-creator 指引, 三轮未对照), SC-2 「每条都能对应一个实证」对此半条不成立; D3 标题「缺一条数字不可解读」对第 5 条 (产物落盘形状) 不同类 —— 产物形状影响可复核性, 不影响数字可解读。收窄全称句: 第 1/2/4 条「缺则不可解读」(有 v1/v2/v3 实证), 第 3/5 条另立措辞。
- [minor] documentation/proposal.md §Key Deliverables §T3 (issue): Deliverables「SOT §6 (局限)」与 T3 后半「§6 已知局限追加『场景 4 只能当地板守卫』」无 D 锚 —— D5 第 2 条只写手册 §场景 4「已知局限」, 未提 SOT §6。给 D5 加一句或新开 D6, 否则映射表上是孤儿任务。
- [minor] implementation/proposal.md §T6 (risk): 只写「本地 `--no-ff` merge + 双推 + 主仓 gitlink」, 未写 CLAUDE.md 多远程约束 2 (推后对每个 remote 独立 `ls-remote` 比对 SHA, 全一致才算成功)。若走 phase-c-integrator C.2.5 自动化则注明; 若手工须显式列出。
- [minor] documentation/RESULT.md §已知局限 (issue): 「未经 owner 审阅 … 已如实登记, 见 handoff」—— `docs/handoff/` 2026-09-13 四份均无 `#211` / 场景 4 记载, 本 session handoff 尚未写 (memory: 写「见 Y」前先 ls Y)。改为「将于本 session handoff 登记」或先落 handoff 再指。
- [minor] architecture/proposal.md §D2 套件落点 (risk): 新增 `ab-suite/trigger/<skill>.json` 子目录; 手册 §数据组织「固定测试集 `ab-suite/` 修改需升版本号, 旧数据不可比」, D2 只写「改动须在 rule6_note 点名」。宜声明 trigger 套件是否沿用 ab-suite 版本化规则 (建议沿用: 文件内 `version` 字段, 改条目即升版)。
- [minor] documentation/proposal.md §OQ-4 (issue): Level 自判只给结论, 未给 owner 判据 —— LEVEL_GUIDE「跨模块 (影响多个子模块 / 涉及 2 个及以上模块) → 自动提升 Level 3」与 proposal-minimal「2-5 文件 → Level 2」两条相互拉扯 (本 Spec 触及主仓 + standards 子模块, 4 个文件); 把两条判据写进 OQ-4 供裁。
- [minor] documentation/proposal.md §头部 (decision): 头部四字段 Level / Status / Created / Linked Issue 顺序与 proposal-minimal 一致; Linked Issue 为 inline code span 全限定; `check_bare_issue_refs.py` 实跑 rc 0 (裸引用 0); 全文无带圈数字 / 希腊字母编号 (U+2460–24FF / U+2776–2793 / 希腊区扫描零命中); 「Rule #6 / #10」属 §4.4 允许例外。合规, 记录以备复核。
- [minor] implementation/proposal.md §rule6_note (decision): Rule #5 落点正确 (`git ls-tree HEAD` 显示 proposal 为主仓 blob); `aria-plugin-benchmarks` 为主仓 tree (mode 040000), 非子模块, `git submodule status` 仅 aria / aria-orchestrator / standards ⇒ D2 套件与手册改动都不落 aria-plugin; Rule #6 自评「不触发」成立。基线实跑前置引「跑 benchmark 本身不需要 OpenSpec」有 CLAUDE.md 原文支撑, 且 issue 验收与 triage 均要求先跑, 非 AI 自作主张。
- [minor] testing/proposal.md §Why 数字 (decision): 30/30 · 8/30 · p = 1.0 · p < 0.0001 · should-not 四臂三轮 0/30 · 负控 0.27 · 成本降约 9 倍 · 技能数 97 vs 13 —— 前五项由各臂原始 json 重算核实 (v3 new/old/pos 30, neg 8; 12 份 json should-not 全 0), 后三项仅 prose (见上一条 minor)。「三处同批」在 §D1 落点、§Key Deliverables、§SC-1 三处列的是同一组 (CLAUDE.md / SOT / 手册)。

## Verdict

**PASS_WITH_WARNINGS** —— critical 0 / major 3 / minor 12 (其中 3 条为 decision 记录, 非待修项)。

Phase 1 (规范合规): PASS 带保留 —— issue 建议 1–3 全部有落点; 验收 1、3 由基线兑现; 验收 2 的规定动作被改判但未请复议 (major 第 2 条)。头部 / Linked Issue / 裸引用 / 编号字形 / Rule #5 / Rule #6 自评全部核实通过。

Phase 2 (质量): D↔T↔SC 映射除 SOT §6 孤儿外完整; 内部数字与原始 json 一致; 但核心设计理由「恒绿」与自己的负控数据矛盾 (major 第 1 条), 且 D4 建立在不存在的模板上 (major 第 3 条)。三条 major 都是文字层修补, 不动方向。

## Vote

**REVISE** —— major 未归零; 三条 major 均可在 proposal 内一轮改完 (改「恒绿」论证为「饱和退化」+ 新增 OQ-5 请裁验收第 2 条改判 + T3 改为「定义模板」), 改完再过一轮即可收敛。

## 映射表

| issue 条目 | 内容 | D | T | SC | 备注 |
|---|---|---|---|---|---|
| 建议 1 | Rule #6 第二行拆两义务 (场景 1 / 场景 4 不互替) | D1 | T1 | SC-1, SC-5 | 落点完整 |
| 建议 2 | SOT 与手册同批改 (防口径分叉) | D1 (三处同批) | T1 | SC-1 (三处各 ≥ 1 且判据一致) | 完整 |
| 建议 3 | rule6_note 加栏「description 是否变动 / 场景 4 结果」, 空着即不合规 | D4 | T3 | SC-3 | 模板宿主不存在 (major 3) |
| 验收 1 | 取历史 description 对跑场景 4 | 头部「基线数据」(起草前完成) | 无 (已完成) | 无 | RESULT.md v1–v3 四臂 |
| 验收 2 | 区分力必须非零; 为零 → 开「评测不可用」单, 不写进 Rule #6 | Why 第 1 条 (实测为零) → 改判为 D1/D2 地板守卫 | T5 (仅上游缺陷单, 非「本仓不可用」单) | SC-5 (反向: 禁比较判据) | 改判未请 owner 复议 (major 2) |
| 验收 3 | 负控显著下降 (拒绝能力) | D3 第 4 条 (负控同批, 须显著低) | T2 | SC-2 (负控: v3 8/30) | 完整 |
| — (issue 未要) | 场景 4 运行前置成文 | D3 | T2 | SC-2 | 理由: 基线 v1/v2 证明缺前置数字不可解读; 已说明 |
| — (issue 未要) | 每 skill 一份 trigger 套件, 落 ab-suite/trigger/ | D2 | T4 | SC-4 | 理由: 场景 4 需固定套件; 版本化规则未声明 (minor) |
| — (issue 未要) | 上游 run_eval.py 缺陷反馈 + 43 skill 缺口记录 | D5 | T5, T2 (局限) | SC-6 | 理由: 基线发现; 已说明 |
| — | SOT §6 已知局限追加 | 无 | T3 后半 | 无 | 孤儿 (minor) |
| — | 子模块本地 merge + 双推 + gitlink; #211 回帖 | 无 (流程) | T6, T7 | 无 | 流程任务, 不需 D; T6 缺 ls-remote 核验 (minor) |
