---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: false
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: true
drift_warning: false
is_refocus: false
verdict: FAIL
timestamp: 2026-09-13T18:05:00.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
---

# post_spec Round 1 聚合 — rule6-description-change-trigger-eval-lane

> 被审 SHA `298d0e4`; drift_guard 未配置 (config 无 `audit.drift_guard`, convergence 模式默认不开) ⇒ `drift_check_skipped: true`, 不影响收敛判定。
> Sibling probe: 已完整扫描, 未发现同 issue 竞品 (`sibling_spec_probe.py` verdict=no_sibling_found, schema 1)。

## 审计结论 (去重后, 按 {category, scope} 合并; found_by 列席位)

### Critical
1. [critical] testing/trigger-eval-openspec-archive.json (issue) — should-not 10 条 query 在三轮四臂全部组合恒 0/30, D2「should-not < threshold」这半边门从未见过 FAIL 分支, 拒绝能力未经证伪 (qa)。

### Major
2. [major] architecture/proposal.md §D1 (issue) — 未点名新义务落在 SOT §2 决策表哪一格 (第二行细化还是新增); 与 §3「第三行不是逃生舱」重叠未消歧 (基线恰证第三行前提成立); 未点名 CLAUDE.md / SOT 被替换的旧句原文 (tech-lead, knowledge-manager)。
3. [major] architecture/proposal.md §D1 (issue) — 「场景 1 不替代场景 4」只否定单向; 只改 description 时场景 1 还跑不跑未定义, 执行者必分叉 (tech-lead)。
4. [major] architecture/proposal.md §D1+§D5 (risk) — 新零裁量义务对 42/43 个无 trigger 套件的 skill 即刻硬阻 (须先建套件), 无成文降级 lane; 叠加 Rule #10 会把 description 改动卡在 owner 可用性上 (tech-lead)。
5. [major] implementation/proposal.md §D4 §T3 §SC-3 (issue) — 「rule6_note 模板加两栏」的模板不存在: SOT §4 只有一句散文要求, 既有语料里 rule6_note 是自由格式; D4 实为新建模板, 且不在 spec-drafter / task-planner 任何 authoring 路径上; SC-3 反事实真空成立 (tech-lead, backend-architect, code-reviewer, knowledge-manager, qa minor)。
6. [major] documentation/proposal.md §Why §D2 §SC-5 (issue) — 「新版 ≥ 旧版会恒绿」与数据不符 (负控 8/30 对旧版 30/30 会判红); 真实结论是 should-trigger 饱和使比较判据退化为「以旧版为参照、噪声大」的地板, 不是恒绿 (code-reviewer)。
7. [major] documentation/proposal.md §Open Questions (issue) — 基线正命中 issue 验收第 2 条的分支 (new vs old p=1.0 ⇒「应改开评测不可用的单, 不写进 Rule #6」), Spec 仍选择写进 Rule #6 (改形为地板守卫) 却未把这一偏离列为 OQ 请 owner 复议; Rule #10 留痕缺 (code-reviewer)。
8. [major] testing/RESULT.md §记分 (risk) — Fisher 按 n=30 算, 3 次同 query run 是伪重复; 独立单元 n=10。复算 (本轮聚合时已做): new/old/pos 各 10/10, negctrl 3/10, new vs negctrl 双侧 p=0.0031 (仍显著), new vs old p=1.0 (结论稳健), 但显著余量从 8e-10 降到 3e-3 (qa)。
9. [major] testing/RESULT.md §负控设计 (issue) — 负控 8/30 集中在 3 条含「收尾 / 核对 / 校验」语义的 query (3/3, 2/3, 3/3), 负控只删净了领域词未删净通用动作语义; RESULT.md 正文「两条 3/3」漏计 2/3 那条 (qa)。
10. [major] documentation/proposal.md §D3 第 4 条 (issue) — 「负控必须显著低于」未定义「显著」(无检验、无 alpha、无最小差值), 与零裁量精神相悖 (qa)。
11. [major] architecture/proposal.md §OQ-4 (decision) — 跨主仓 CLAUDE.md + standards 子模块 + 手册, 改十条不可协商规则之一; LEVEL_GUIDE「跨模块 → Level 3」与模板「2-5 文件 → Level 2」拉扯; 应先决而非搁置, 且应把两条判据给 owner (qa, code-reviewer minor)。
12. [major] testing/RESULT.md §已知局限 · proposal.md §D3 第 1 条 (issue) — 地板守卫只在空白项目根验证; run_eval 判触发 = 第一个 tool_use 就是本技能, 探索式开局判未触发; 真实项目根下未验证, D3 未限定适用范围或加「空项目根」前置 (backend-architect)。
13. [major] documentation/手册 §场景 4 (issue) — 手册现状场景 4 = run_loop.py 描述优化流程; Spec 拟重写为 run_eval.py 地板守卫; 同名两种机制 (优化 vs 门禁) 是并存 / 替换未说明 (knowledge-manager)。
14. [major] architecture/proposal.md §D5 (issue) — 「43 skill trigger 套件不建」只记手册散文, 未按 SOT §3 / #150 先例开 issue 追踪 (knowledge-manager)。
15. [major] testing/proposal.md §SC-2 · §D3 (risk) — RESULT.md 无 SHA / 版本锚, 数字被三处正文复述; RESULT 修订 (如上 8、9) 后三处失真且无重核机制 (knowledge-manager)。

### Minor
16. [minor] testing/proposal.md §D2+§D3 — 阈值语义依赖 runs-per-query; D3 未固定 runs / 套件规模 / timeout (tech-lead)。
17. [minor] testing/proposal.md §SC-2 — 前置 (c) 的实证 (技能数 97 vs 13) 只在散文, 无机读产物; SC-2 可由散文自证; 「显式 --model」半条无实证; 「缺一条数字不可解读」对第 5 条不同类 (tech-lead, backend-architect, code-reviewer)。
18. [minor] documentation/proposal.md §Impact — 成本 (0.54 → 0.06 / 约 8 美元) 与「12 分钟」在归档产物无支撑; 12 分钟隐含并行, 串行约 22 分钟 (tech-lead, code-reviewer)。
19. [minor] implementation/proposal.md §T6 — standards 仓无 VERSION 文件, 「PATCH」无落点; 新增强制义务按 SemVer 应 MINOR; 未写多远程约束 2 (逐 remote ls-remote) (tech-lead, code-reviewer)。
20. [minor] testing/proposal.md §SC-1 — 「或 owner 定稿的同义句」逃生口不可机械判定, 有滑向永红之险 (tech-lead, qa)。
21. [minor] documentation/proposal.md §D3 第 1 条 — 「独立项目根 + 单 worker」把两个正交缓解捆成一条 (tech-lead)。
22. [minor] documentation/RESULT.md §结论 3a — 「压到约 1/N」与 v1 负控 0/30 不符, 改定性表述; v1→v2 同批改了两个变量, 因果分离靠 diag02 补强, 报告未点破 (tech-lead, backend-architect)。
23. [minor] architecture/proposal.md §D5 · SC-6 — 上游反馈只要求「发出证据」, 不要求含复现材料 / 修复方向; 单 worker workaround 可能永久化 (backend-architect)。
24. [minor] testing/run_arms_v3.sh — 脚本路径写死 scratchpad; 插件缓存 hash 与模型版本无后备 (qa)。
25. [minor] documentation/proposal.md §D1 — 落点用「行 480 附近」自引行号, 改锚点式 (code-reviewer)。
26. [minor] documentation/proposal.md §Why vs §D5 — 「两处缺陷」vs 反馈 (a)(b)(c) 三项口径不一 (code-reviewer)。
27. [minor] documentation/proposal.md §Key Deliverables · §T3 — 「SOT §6」无 D 锚, 孤儿; §6 开篇「另有两个已知缺陷」计数语未列入待改 (code-reviewer, knowledge-manager)。
28. [minor] documentation/RESULT.md §已知局限 — 「见 handoff」而 handoff 尚不存在 (code-reviewer)。
29. [minor] architecture/proposal.md §D2 — `ab-suite/trigger/` 未声明是否沿用 ab-suite 版本化规则 (code-reviewer)。
30. [minor] documentation/proposal.md §Why — 未直接交叉引用 `10CG/aria-plugin#190` comment 22921 (knowledge-manager)。
31. [minor] architecture/aria-standards#17 — 同一 SOT 相近区域的并行提案未提及, 合并前应查重 (knowledge-manager)。
32. [minor] documentation/trigger-eval-openspec-archive.json — 20 条未经 owner 审阅即计划搬入套件, 后续改动会与基线数字脱节 (qa)。

### Decisions (通过项, 记录)
- 头部字段 / Linked Issue 全限定 / `check_bare_issue_refs.py` rc 0 / 无禁用字形: 通过 (code-reviewer)。
- Rule #5 落点正确; `aria-plugin-benchmarks` 为主仓 tree 非子模块; Rule #6 自评「不触发」成立 (code-reviewer)。
- 四臂三轮全部计数 + Fisher (n=30) 由原始 json 复算一致; run_eval.py 两处缺陷从源码直读成立 (tech-lead, backend-architect, code-reviewer)。
- 未能核实: 技能数 97 vs 13、单次成本 0.54 / 0.06 美元 (无机读产物) (tech-lead, backend-architect)。

## Verdict

FAIL — 1 critical + 14 major + 17 minor (去重后)。post_spec 非阻塞 (继续, 仅记录), 但 vote 5/5 REVISE ⇒ 不收敛, 进 rework → Round 2。

## 轮次记录

### Round 1
- Agents: tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager (5/5 完成, 无超时)
- Sibling probe: 已完整扫描, 未发现同 issue 竞品
- Conclusions: 32 (去重前 46: 11 + 5 + 9 + 15 + 8; 去重后 32; 其中 decision 记录 4 组不计入 verdict)
- Vote: REVISE (5/5)
- Duration: 约 17 分钟 (并发 3 + 2 两批)

## Rework 计划 (进 R2 前)
- 用数据回答 1 与 12: v4 两个反事实臂 (过宽 description 验 should-not 的 FAIL 分支可达; 有文件的项目根验第一个 tool_use 判据), 结果并入 RESULT.md 并给 RESULT 加 SHA 锚 (15)。
- RESULT.md 修订: 按 query 级 n=10 复算 (8); 负控命中分布与「未删净」如实登记, 并加第二个负控 (删净通用动作词) 或如实标注 (9); 1/N 改定性 (22); 「见 handoff」改写 (28)。
- proposal 重写: D1 点名决策表落格 + 替换旧句原文 + 与 §3 关系 + 只改 description 时场景 1 是否跑 (2, 3); 新增降级 lane (4); D4 改为「新建 rule6_note 最小结构化模板 + 落 spec-drafter 模板」(5); 「恒绿」改「饱和退化」(6); 新增 OQ 请裁「偏离验收第 2 条」(7); 「显著」给可操作判据 (10); OQ-4 给两条判据 + 建议 (11); 手册场景 4 双机制关系 (13); 43 套件缺口开 issue 列入 T (14); minors 逐条。
