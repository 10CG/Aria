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
timestamp: 2026-09-14T11:08:40.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [tech-lead]
---

# post_spec Round 2 — tech-lead 席 (被审 SHA 55bc9f3)

## R1 对账

聚合报告中 `found_by` 含 tech-lead 的 11 条 (2 / 3 / 4 / 5 / 16 / 17 / 18 / 19 / 20 / 21 / 22)。结果: closed 8 / partially 3 / open 0。

| R1# | 严重度 | 判定 | v2 落点 (段名) 与核实 |
|---|---|---|---|
| 2 | major | **closed** | §D1 首段「落在决策表哪一格」明确「§2 第二行的细化, 不新增行」+ 给出不属第三行的理由 + §3 边界注; §D1 表第二列三条「旧句 (逐字)」经 `grep -F` 在三处文件各命中 1 次 (见数据核实记录 5)。与 §3 的重叠消歧成立 —— §3 line 45 确有「测量剧场」原词, §D1 的交叉引用不悬空。 |
| 3 | major | **closed** | §D1「只改 description 时场景 1 还跑不跑」独立成段, 答「不跑」, 并按 Rule #10 升级为 OQ-6 请 owner 裁, 给出否决时的回退形态 (「场景 1 + 场景 4b 都跑」)。义务边界不再分叉。(OQ-6 的代价数字另见 Finding 2。) |
| 4 | major | **partially** | 落点: §Impact 末条 + OQ-7。做对的部分: 成本写明、不自行豁免、升级 owner (Rule #10 合规)。未闭合: OQ-7 的代价只写「每个首次改 description 的 cycle 多约 1 小时」, 未写与 OQ-3 的耦合 —— 若 owner 采纳 OQ-3 的「先审」, 建套件即含 owner 审阅, 42/43 的硬阻回到 owner 可用性, 正是 R1-4 的原命题; 且 §D2 末条「首次为某 skill 跑场景 4b 的 cycle 建套件 (约 1 小时 + 一次运行)」对「新套件要不要 owner 审阅」沉默, 与 OQ-3 冲突。→ Finding 3。 |
| 5 | major | **partially** | 落点: §D4 改写为「新建, 宿主 = SOT §4」+ 明列现状「SOT §4 只有一句散文」+ authoring 路径经 D5.3 开 aria-plugin issue 承接。核心事实错误已修 (反事实核实: 五个字段名在 SOT / CLAUDE.md / 手册 grep 全为 0, SC-3 不真空)。残余: 模板落地后仍无任何机械 enforcement, 且宿主 §4 的标题是「与规则 #10 的关系」, 放模板属寄居。→ Finding 6 (降为 minor)。 |
| 16 | minor | **closed** | §D2 第二条「参数钉死」: `--runs-per-query 3` / `--trigger-threshold 0.5` / `--timeout 120` / 套件 20 条, 并写明「改任一参数 = 换判据, 须 owner 裁」。阈值与 runs 现在绑在一起裁。 |
| 17 | minor | **partially** | 落点: §D3 表新增「机读实证」列 + 两份探针 json。97 / 12 与 0.604 / 0.079 已从 json 字段直读核实 (核实记录 3)。残余: SC-2 的判据是「路径 `test -e` 为真」, 而表里第 1/2/5 行写的是 `v1-…/*.json`、`v2-…`、`v3-…/negctrl.json` —— 省略号不是真路径, `*.json` 在 `test -e` 下会因多参数报错, SC-2 按字面不可机械执行。→ Finding 5。 |
| 18 | minor | **closed** | §Impact 成本条注明来源「RESULT.md v2 §时长与成本」, 并行 12–14 分钟 / 串行 24 分钟两个数都给, 约 10 美元标为按探针单次 0.08 估。机械核对: 探针 `total_cost_usd` = 0.078603, 120 × 0.08 = 9.6 ≈ 10, 自洽。 |
| 19 | minor | **closed** | 文件头 ship target 写明「standards 仓无 tag 无 VERSION 文件, meta-repo 类只动 gitlink」且 SOT 头 Version 1.0.0 → **1.1.0 (MINOR)**, 与 SemVer 一致; T7 补齐「对 origin 与 github 各自 `git ls-remote` 比对 SHA, 全部一致才算推成功」+ 主仓同样逐 remote 核验, 与 CLAUDE.md 多远程约束 1/2 逐条对得上。相邻新问题 → Finding 8。 |
| 20 | minor | **closed** | SC-1 删去「或 owner 定稿的同义句」逃生口, 改「逐字, 无同义替代」, 可机械判定。 |
| 21 | minor | **closed** | §D3 第 1 行「两者正交: 单 worker 消除同根内兄弟命令文件; 独立根允许多臂并行」, 并写明上游修好缺陷 (a) 后可放宽哪一半。 |
| 22 | minor | **closed** | RESULT.md v2 结论 3(a) 改为「压低幅度定性为『显著』, 不定量为 1/N (v1 负控 0/30 与 1/4 期望不符)」, 并点破 v1→v2 同批改两个变量、因果靠 diag02 分离。 |

## Findings

- [major] testing/proposal.md §D2 (issue): 「≥ 负控 + 4 ⇒ Fisher 单侧 p 约 0.03 以内」数字错。实算 n=10 时 +4 差距的单侧 p 在 0.0433–0.0894; 与通过门合取后 (被评必为 10/10) 最紧也只有 0.0433。要落到 0.03 以内须 +5 (10 vs 5, p = 0.0163)。
- [major] documentation/proposal.md §OQ-6 (issue): 备选「两者都跑」的代价写「每次多约 30 分钟 / 15 美元」, 全仓无来源; 手册自身唯一估算是 $0.50/skill (28 skills ≈ $14), 差约 30 倍。owner 据此裁「要不要放宽不可协商规则字面义务」会被误导。
- [major] architecture/proposal.md §D1+§D5 (risk): 42/43 无套件 skill 的即时成本与 OQ-3 的「owner 先审 query 集」耦合未写进 OQ-7 代价; §D2 建套件流程对「新套件要不要 owner 审阅」沉默。两处不合并裁, 硬阻仍落在 owner 可用性上。
- [major] architecture/aria-standards#17 (decision): #17 提议在同一 SOT 增「AB 范围」节, 定义「照跑 = 该 Skill 全套件 + 定向 fixture」—— 与本 Spec 对同一第二行「照跑」按 hunk 再定义语义相交 (description hunk 是否还要全套件?)。D5.5 把它降格为「协调编号」, 低估了合流工作。
- [minor] testing/proposal.md §SC-2 (issue): SC-2 以「路径 `test -e` 为真」为判据, 但 D3 表第 1/2/5 行的实证列写的是省略号缩写 (`v2-…`) 与 glob (`*.json`), 二者都不可直接 `test -e`; 需逐文件全路径或改 `ls` 判据。
- [minor] implementation/proposal.md §D4 (issue): 五字段模板落地后无任何机械 enforcement (无 custom check / state-check), 「description_changed: yes 而 scenario4b 空 ⇒ 不合规」只能靠人读; 且宿主 SOT §4 标题是「与规则 #10 的关系」, 模板属寄居, 宜新起 §4.1 或独立小节。
- [minor] documentation/AB_TEST_OPERATIONS.md §边界与留痕 (issue): 该段原文是「完整 fail-closed 边界**三条** (A / B / 拿不准照跑)」, D1 新句把中间一条拆成「description 变动…, 指令面变动…」两项, 计数语变成四项却无对应 SC (SC-7 只覆盖 SOT §6 的计数语)。
- [minor] implementation/proposal.md §T5 (risk): `version-management.md §5.1` 有未裁项 (standards 的版本自称口径 A/B 两案, 原文「在裁定前, 不要拿这两个数字中的任何一个当权威」)。T5 给 SOT 文件头 bump 到 1.1.0 等于新增第三个版本自称面, 应在 Spec 里声明它与该待裁项正交, 或一并请裁。
- [minor] testing/proposal.md §D2 (issue): 负控判据不满足时「本轮数字作废」无重试上限、无升级路径。零裁量规则下重复作废会把 cycle 卡死且 AI 不得自行豁免 (Rule #10), 须写明「连续 N 轮作废 ⇒ 升级 owner」。

## Verdict

PASS_WITH_WARNINGS —— critical 0 / major 4 / minor 5 (本轮仍 open 或新发现)。

R1 的 11 条我席结论闭合 8 条, 3 条部分闭合; 数据面这次全部可机械复核且逐格对上 (v4 两臂 / query 级 Fisher / 探针字段 / 负控分布 / 三条旧句逐字), R1 里「未能核实」的两组数字 (技能数、单次成本) 现在有机读产物, 这是本轮最大的实质进步。

仍投 REVISE 的原因集中在**owner 决策材料的准确性**, 不在数据或架构: 一个新引入的统计断言经实算为假 (+4 ⇒ 0.043 而非 0.03), 一个代价数字与本仓自有估算差 30 倍, 两个待裁项 (OQ-3 × OQ-7) 的耦合未合并陈述, 以及一个同 SOT 的并行提案被降格处理。按 memory `feedback_never_write_unverified_impossibility_claims` 与 `feedback_owner_item_summary_must_not_invent_defaults`, 这四条在提交 owner 裁定前必须修——它们直接决定 owner 会不会做出建立在错数字上的裁定。四条都是文字级修补, 不需要重跑基线。

## Vote

REVISE

## 数据核实记录

核实方式: 全部直接 `json.load` 原始产物重算, 不读 RESULT.md 的数字; Fisher 用 `math.comb` 自算精确检验 (双侧 = 枚举所有 p(x) ≤ p(obs) 的表; 单侧 = 自观测值向上求和)。

1. **v4 两臂 (逐 query 重新累加)**: overbroad should-trigger 30/30 (query 级 10/10), should-not **22/30**, 其中 **7/10** 条 `trigger_rate ≥ 0.5` 判红 —— 与 RESULT.md v2 与 Spec §Why 第 2 条一致。realroot should-trigger 30/30 (10/10), should-not **0/30 (0/10)** —— 一致。⇒ R1 critical 1 (should-not 的 FAIL 分支从未见过) 与 R1-12 (非空项目根未验) 两条均由数据闭合。

2. **query 级 Fisher (n=10)**: new (10 命中) vs negctrl (3 命中) 双侧 p = **0.0030959752** ≈ 0.0031, 与 RESULT.md 表格一致; 单侧 = 0.0015480。run 级 n=30 的 new vs old = 1.0、new vs negctrl < 0.0001 与 R1 复算一致。

3. **探针 json 直读字段**: `probe-setting-sources-default.json` → `result` = `"97,yes"`, `total_cost_usd` = **0.6043545**; `probe-setting-sources-project.json` → `result` = `"12,no"`, `total_cost_usd` = **0.078603**。与 RESULT.md 的 97 / 12 与 0.604 / 0.079 逐字段一致。**口径提示 (非 finding)**: 技能数是模型在探针回答里的**自报**, 不是机械枚举, RESULT.md 已诚实写「自报」, 但 Spec §D3 第 3 行的实证列没带这个限定词; 另外探针 `num_turns` = 1, 以它的单价外推 eval 单次成本属**下限**估计。

4. **负控分布 (v3 negctrl.json)**: should-trigger 命中恰好 3 条 —「周期收尾: spec `aria-ci-backend-abstraction` …并核对一下归档后的路径」3/3、「我想把 …aria-secret-guard-manifest-precision 标记为已完成并放到归档目录, 记得归档后要检查 proposal.md 是不是真的到了目标目录」2/3、「D.2 归档 + 落点校验, change = aria-124-submodule-pointer-regression-gate」3/3; 其余 7 条 0/3; should-not 全 0/30。与 RESULT.md v2 的勘正段 (3 条: 3/3, 2/3, 3/3) 完全一致, R1-9 的漏计已修。

5. **D1 旧句逐字核 (`grep -F -c`)**: `CLAUDE.md` 第 110 行「`description` 或指令流程变动一律照跑; 豁免须在 spec/tasks 留 `rule6_note`。」= 1; SOT 第 33 行「`description` 或指令流程变动 ⇒ 一律第二行。」= 1; 手册第 480 行「description 与指令面变动零裁量照跑」= 1。**三条全部逐字命中, T1 可执行**。附带发现手册那条嵌在「边界三条 (…/…/…)」括号里 → Finding 7。

6. **D2 判据的统计依据 (本轮新算)**:

| 被评 / 负控 (n=10 each) | 单侧 Fisher p | 双侧 |
|---|---|---|
| 10 vs 6 (+4, 与通过门合取下的最紧情形) | **0.04334** | 0.08669 |
| 9 vs 5 / 8 vs 4 / 7 vs 3 / 6 vs 2 (+4) | 0.0704 / 0.0849 / 0.0894 / 0.0849 | 0.141 / 0.170 / 0.179 / 0.170 |
| 10 vs 5 (+5) | **0.01625** | — |
| 10 vs 4 (+6) | 0.00542 | — |
| 10 vs 3 (基线 v3) | 0.00155 | 0.00310 |

⇒ 「n=10 时 +4 的 Fisher 单侧 p 约 0.03 以内」在**任何** +4 组合下都不成立 (最小 0.0433)。基线自己的 10 vs 3 (差 7) 是 0.00155, 与 +4 规则不是一回事。修法二选一: 判据改 **+5** (可写 p ≤ 0.017), 或保留 +4 但把括号改成「p ≤ 0.044」。

7. **SC-3 反事实**: 五个字段名 (`decision_table_row` / `description_changed` / `scenario1` / `scenario4b` / `negctrl`) 在 SOT、CLAUDE.md、手册三处 grep 均为 0 ⇒ SC-3 的「改前全 0」成立, 非真空断言。SC-7 前提也成立: SOT 第 71 行现为「后者另有**两个**已知缺陷记录在案」。SC-8 前提成立: 手册现只有一个「### 场景 4: Description 触发准确率优化」标题。

8. **OQ-5 / OQ-6 / OQ-7 的推荐与代价完整性**: OQ-5 给了本 Spec 的选择 + 理由 + issue 字面备选 + 备选代价, 但**未给推荐方案自身的代价** (description 维度只拿到地板守卫 + 全仓建套件); OQ-6 无「推荐」字样且同样只给备选代价, 且该数字有误 (Finding 2); OQ-7 有推荐有代价但代价不全 (Finding 3)。OQ-1/2/3/4 推荐与代价齐备。

9. **T7 顺序核**: 查 `10CG/aria-standards#17` (已 API 核实: 存在且 **open**, 标题为「单 Skill 局部变更的 Rule #6 AB lane 缺成文」) → standards 本地 `--no-ff` merge → 双推 → 逐 remote `ls-remote` 比对 → 主仓 gitlink bump → 主仓双推逐 remote 核验: 与 CLAUDE.md「多远程两条硬约束」逐条一致 (约束 1: 子模块禁服务端合并 ✔; 约束 2: 不信 push 回执 ✔), 顺序与 memory `feedback_sequenced_multirepo_gitlink_bump` 一致, **无违规**。两点执行期提醒 (观察, 不计 finding): (a) 子模块若处于 detached HEAD, push 须用 `HEAD:master` 且 gate/diff 前先 `git branch -f master origin/master`; (b) `10CG/Aria#211` 亦已核实 open, T8 回帖对象存在。

10. **CLAUDE.md 预算核 (D1 + D4 会加长规则 #6)**: 现状 151 行 / 13316 字节, 上限 200 行 / 24000 字节 ⇒ 新增两句不触预算, 无 finding。仅提示: 新句里的「(基线: RESULT.md v2)」是指向带日期 ab-results 的易变指针, RESULT 升到 v3 时 CLAUDE.md 会静默过期, 宜把版本指针只留在 SOT。
