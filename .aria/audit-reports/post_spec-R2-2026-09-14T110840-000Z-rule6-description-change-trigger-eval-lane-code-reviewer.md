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
timestamp: 2026-09-14T11:58:20.872Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [code-reviewer]
---

# post_spec R2 — code-reviewer 席 (Phase 1 规范合规 + Phase 2 质量)

被审对象: `openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md` rework v2 @ 主仓 HEAD `55bc9f3`; 基线目录 `aria-plugin-benchmarks/ab-results/2026-09-13-rule6-description-trigger-eval-baseline/` (RESULT.md v2)。只审不改。独立性: 未读本轮其他四席 R2 报告。下文每个数字都来自实跑 (命令与输出见「实跑记录」), 没核的不下结论。

## R1 对账

范围: R1 聚合报告里 found_by 含 code-reviewer 的 12 条。

| 序号 | R1 条目 (聚合编号) | v2 落点 | 状态 | 核对依据 |
|---|---|---|---|---|
| 1 | 「新版 ≥ 旧版会恒绿 / 恒打平」与数据不符 (聚合第 6 条, 本席 major) | Why 第 1 条; RESULT 结论 1 | partially | 「恒绿」已删, 改成「饱和」+「不是恒绿门」, 与「负控 8/30 对旧版 30/30 会判红」一致。残留: 全称句「对任何两个真 description 都打平」(RESULT 自己的局限段否定了「任何」); 「对照物」方向易误读。见 Findings 第 3 条 |
| 2 | 偏离 issue 验收第 2 条未请复议 (聚合第 7 条, 本席 major) | OQ-5 | closed | 引了验收条款, 给出备选 (issue 字面) 及其代价, 写明「请 owner 二选一」。残留: 已选项没写自身代价; 标「原文」实为删节。并入 Findings 第 14 条 |
| 3 | rule6_note 模板不存在 (聚合第 5 条) | D4 / T3 / SC-3 | closed | 改为「新建」五字段模板, 宿主 SOT §4。SC-3 反事实实跑: 现行 SOT 五个字段名 grep 各为 0, 不是真空成立。新问题 (值域) 见 Findings 第 10 条 |
| 4 | 落点自引行号 (聚合第 25 条) | D1 表「落点」列 | closed | 三处落点都改成小节名。proposal 与 RESULT 扫描行号自引: 0 处 (唯一命中「并行 12」是误报) |
| 5 | 「两处缺陷」对「三项反馈」 (聚合第 26 条) | Why 第 3 条; RESULT 结论 3; D5.4 | closed | 统一为「两处结构性缺陷 + 一处配置建议」; 上游反馈只带两条修复方向 |
| 6 | Impact 时长 / 成本无支撑 (聚合第 18 条) | Impact; RESULT §时长与成本 | partially | 并行 / 串行已分开写; 成本改用探针 json 的 `total_cost_usd` (0.604 / 0.079) 并标「估算」。但新写的「单 worker 一臂 10m39s–13m54s (run.log)」与 v2 的 run.log 对不上。见 Findings 第 6 条 |
| 7 | SC-2 里 `--model` 无实证; 第 5 条性质不同 (聚合第 17 条) | D3 第 4 行、D3 标题、SC-2 | closed | `--model` 单列一行, 标「配置推导, 无对照实测」, SC-2 豁免第 4 行; 标题把前五条和第六条 (产物形状) 分开。97/12 属于自报这一新发现见 Findings 第 7 条 |
| 8 | SOT §6 在映射里是孤儿 + 计数语 (聚合第 27 条) | D6 / T5 / SC-7 | closed | 新增 D6, 含「两个 → 三个」。SC-7 前半实跑: 现状「两个已知缺陷」= 1, 「三个」= 0, 是改前失败的有效反事实 |
| 9 | T6 缺 ls-remote 核验; PATCH 无落点 (聚合第 19 条) | T7; 头部 ship target | closed | T7 写明对 origin 与 github 逐个 `git ls-remote`, 两个仓的 remote 实查都是 origin + github。版本改为 MINOR; standards 0 个 tag、无 VERSION 文件, 与 version-management §5.1 (meta-repo 类) 一致 |
| 10 | 「见 handoff」而 handoff 不存在 (聚合第 28 条) | RESULT §已知局限末条 | open | 现在写的是「与本文件同批提交」, 但 `55bc9f3` 里没有任何 docs/handoff 文件。见 Findings 第 9 条 |
| 11 | ab-suite 版本化规则未声明 (聚合第 29 条) | D2 末条 / SC-4 | closed | 声明沿用, 升 `ab-suite/version.yaml` (现为 1.5.0)。套件文件是裸 JSON 数组 (20 条), 放不下文件内版本字段, 只能由 version.yaml 承载, 前后自洽 |
| 12 | OQ-4 没给 owner 判据 (聚合第 11 条) | OQ-4 | closed | 两条判据都能在原文找到: LEVEL_GUIDE「跨模块 → 自动提升为 Level 3」; proposal-minimal「Changes affecting 2-5 files」。表述框架的问题并入 Findings 第 14 条 |

合计: closed 9 / partially 2 / open 1。

## Findings

- [major] implementation/proposal.md §D2 同批负控 (issue): 负控有效性判据以被评 description 自身为参照 (被评命中 ≥ 负控 + 4, 否则作废、不判好坏), 于是 should-trigger 严重退化会被判「作废」而不是 FAIL, 退化越严重越容易逃过; 「作废」之后做什么没写, rule6_note 里也没有对应取值。
- [major] testing/proposal.md §SC-5 (issue): 按文件 grep「新版.*旧版」, 改前就已命中 SOT §6 和手册 §版本管理里的合法存量句, 所以 SC-5 改前改后都是红的、没有绿的状态, 还会诱导执行者删掉 SOT §6「能站住的是新版 vs 旧版」; v1 的 SC-5 是散文, 这是 v2 新引入的。
- [minor] documentation/proposal.md §Why 第 1 条 (issue): 残留全称句「对任何两个真 description 都打平」, 与 RESULT §已知局限「不是『任何』改动都测不出」冲突; 「只在对照物是坏 description 时才判红」方向容易读反 (实际是被评新版差时才判红)。
- [minor] testing/proposal.md §D2 p 值括注 (issue): 「+4 ⇒ n=10 单侧 Fisher p 约 0.03 以内」实算不成立: 余量恰为 4 时单侧 p 在 0.043–0.089 之间; 被评 10/10 时, 负控要 ≤ 5 才能做到 p ≤ 0.03 (此时 p = 0.016)。
- [minor] documentation/proposal.md §Impact §D5.2 §OQ-7 (issue): 「42/43」分母错: 已跟踪的 SKILL.md 共 42 个 (README 也写 42); 43 来自 `10CG/aria-plugin#150` 数目录的口径, 计入了 gitignored 的 issue-triage-workspace; 现状是 42/42, T4 之后是 41/42。
- [minor] documentation/RESULT.md §时长与成本 (issue): 「单 worker 一臂 10m39s–13m54s (run.log)」漏掉了同样是单 worker 的 v2 四臂 (最长 17m39s); 实际区间 10m39s–17m39s, 串行两臂约 22–34 分钟而不是「约 24」; Impact 跟着偏低。
- [minor] testing/proposal.md §D3 第 3 行 (issue): 97 / 12 是模型自报 (探针 result 字段为「97,yes」「12,no」), 不是枚举计数; manifest 在同一配置下记的是 13, 差异没解释; 0.604 对 0.079 的成本差里混了思考输出的差 (1190 对 5); D3 抄过来时去掉了 RESULT 的「自报」限定。
- [minor] testing/proposal.md §SC-2 §SC-7 (issue): 两条 SC 按字面执行对不上: D3 实证格里有省略号路径和 `*.json` 通配 (`test -e` 为假或直接报错), 第 6 行不是路径且未豁免; SC-7 的字面「Version: 1.1.0」永远匹配不到 SOT 头部的「**Version**: 1.1.0」。
- [minor] documentation/RESULT.md §已知局限末条 (issue): 「记入本 session 的 handoff (与本文件同批提交)」在 55bc9f3 不成立: 该提交没有 docs/handoff 文件, 最新 handoff 只把 `10CG/Aria#211` 列为待 triage; R1 同一条复发。
- [minor] implementation/proposal.md §D4 模板值域 (issue): 本 Spec 自己的 rule6_note 写了 decision_table_row: n/a 和 scenario4b: n/a, 都不在模板值域里; 值域里没有 D2 的「作废」; 「照跑」同时对应决策表第二行和第四行, 落格不唯一。
- [minor] documentation/proposal.md §Key Deliverables §T2 (issue): 「手册 §数据组织表」这个锚点不存在 (手册里既无此标题也无此词), 应指「### 固定测试集 vs 临时测试」表 (以及「### 目录结构」树); 这个错名出自本席 R1 报告, 在此更正。
- [minor] documentation/proposal.md §D1 CLAUDE.md 新句 §D6 (issue): 「RESULT.md v2」既无路径也无 SHA, ab-results 下有 9 份 RESULT.md, 无法定位, 也违反 RESULT 自定的引用格式「v2 @ <SHA>」; SOT 在 standards 子模块里, 须写主仓全路径; §6 末句的出处会误把新加的第三条也罩进去。
- [minor] architecture/proposal.md §D1 只改 description 不跑场景 1 (risk): 「跑它不产生信息」说得太满: 场景 1 的 with-skill 臂按 Skill path 读整份 SKILL.md, 其中含 description; description 可以带行为指令 (正控原文就有「不要自己手工 mv」); 它只对触发维度为空, OQ-6 应写出「不跑」一侧的这项代价。
- [minor] documentation/proposal.md §Open Questions (issue): 推荐项或已选项没写自身代价 (OQ-4 维持 Level 2 就不走 post_planning, 且 LEVEL_GUIDE 写的是「自动提升」, 与模板提示并不对等, 不是「拉扯」; OQ-5 的已选项; OQ-6 的「不跑」); OQ-5 标「原文」实为删节, 丢了「又一个测量剧场」那句理由。
- [minor] documentation/proposal.md §OQ-3 §OQ-6 (issue): OQ-3「重跑一臂约 12 分钟 / 5 美元」与 D2 的同批负控要求矛盾 (至少两臂, 约 10 美元); OQ-6「30 分钟 / 15 美元」没有出处, 仓内有 133 份场景 1 的 timing.json 可以拿来估算, 但没引用。
- [minor] testing/proposal.md §Success Criteria 覆盖 (issue): D2 判据正文 (runs / 阈值 / timeout / 条数 / 负控规则) 和 SOT §3 边界注都没有任何 SC 管, 门禁核心文字写错了 8 条 SC 仍会全绿; T3 的 CLAUDE.md 指向句与 D1 新句里的「(字段见 SOT §4)」重叠, 没说明是一句还是两句。
- [minor] architecture/proposal.md §D2 套件建立 (risk): OQ-3 引 skill-creator Step 2 推荐 owner 先审, 但 D2 没规定今后新建套件是否也要审, 于是每个首次改 description 的 cycle 都会再遇到 OQ-3 的问题; 审阅要花的时间也没算进 Impact 和 OQ-7。

## Findings 证据与修法

按上面列表顺序编号。

1. **D2 同批负控 (major)**
   - 原文: 「被评 description 的 should-trigger 命中数 ≥ 负控命中数 + 4 … 不满足 ⇒ 本轮数字作废 (套件或环境失效, 不归因 description), 不判 description 好坏」。
   - 按字面分情况推:
     - 被评 10/10 时, 这条等价于「负控 ≤ 6」, 这正是想要的有效性检查。
     - 被评 < 10 时 (should-trigger 这一侧已经 FAIL), 只要被评 ≤ 负控 + 3, 就落进「作废」。代入基线数字: 假设某次改动让 description 退化成 v3 负控那样 (query 级 3/10), 同批负控约 3/10, 3 < 7, 结果是「作废」而不是 FAIL。退化越严重, 被评就越接近负控, 就越一定被作废。这恰恰是 issue 验收第 3 条要守住的那类退化。
     - should-not 方向 (过宽) 不受影响: 过宽臂 should-trigger 10/10, 对负控 3/10 判为有效, 再按 should-not 7/10 判 FAIL。
   - 「作废」之后怎么办没写 (重跑? 阻断?), D4 的 scenario4b 值域里也只有 pass|fail。
   - 修法: 有效性判据改成不依赖被评对象, 例如「负控 query 级命中 ≤ 6/10」或「与同批已知良好的参照比」; 写明判定顺序 (先判有效性, 再判地板); 规定「作废 ⇒ 阻断, 修好套件或环境后重跑」, rule6_note 加上对应取值。

2. **SC-5 (major)**
   - 实跑 `grep -c "新版.*旧版"`:
     - CLAUDE.md: 0
     - SOT: 1 (§6 第一条「能站住的是**新版 vs 旧版**」)
     - 手册: 1 (§版本管理「新版本的结果与旧版本 **不可直接比较**」)
     - 另外两个 pattern 在三个文件里都是 0。
   - 按 SC-1 那样把「三处」读成三个文件, SC-5 改前改后都是红的。v1 的 SC-5 是散文 (「三处 D1 文字不含…」); v2 改成 grep 时没有对改前文件跑一遍。
   - 后果: T1 做得再对 SC-5 也不会绿。执行者只剩两条路: 临场解释 grep 范围 (违背零裁量), 或者删掉 SOT §6 那句。那句正是「场景 1 只有新旧对比站得住」这条方法论结论; 而 D6 恰好也在改 §6, 顺手删掉的风险更大。
   - 修法: 把 grep 目标限定到 D1 三条新句本身 (先用 `grep -F` 定位新句所在行再查), 或者去掉「新版.*旧版」只留「≥ 旧版」「不低于旧版」; 然后对改前文件实跑, 确认为 0。

3. **Why 第 1 条的残留**
   - proposal 写「对任何两个真 description 都打平」, RESULT §已知局限写的是「只测了一对真实 description; … 不是『任何 description 改动都测不出』」。RESULT 结论 1 本身也有这句全称句, 与它自己的局限段互相冲突。
   - 对照实验里「对照物」通常指参照 (旧版)。旧版差时「新版 ≥ 旧版」反而成立, 判绿。作者实际想说的是「被评的新版差时才判红」。
   - 修法: 改为「两个都含该领域词族的 description 在本套件上打平 (本次实测一对)」; 「对照物」改成「被评新版」。

4. **p 值括注**
   - 按 query 级 n=10 做单侧 Fisher 精确检验 (超几何分布), 余量恰为 4 的七种组合:
     - 4 vs 0: 0.0433
     - 5 vs 1: 0.0704
     - 6 vs 2: 0.0849
     - 7 vs 3: 0.0894
     - 8 vs 4: 0.0849
     - 9 vs 5: 0.0704
     - 10 vs 6: 0.0433
   - 被评 10/10 时: 负控 5 对应 p = 0.0163, 负控 6 对应 p = 0.0433。没有一种组合能做到「约 0.03 以内」。
   - 修法: 二选一交 owner 裁 (D2 自己写了「改任一参数 = 换判据」):
     - 改成「+5」, 被评 10/10 时即负控 ≤ 5, p 约 0.016;
     - 保留「+4」, 但写实数 (p 约 0.04, 最坏 0.09)。

5. **42/43**
   - 实跑结果:
     - `git -C aria ls-files 'skills/*/SKILL.md' | wc -l` = 42
     - `ls aria/skills | wc -l` = 44, 多出来的是 `run_all_tests.sh` 和 gitignored 的 `issue-triage-workspace/`
     - README 写「42 Skills」
     - `10CG/aria-plugin#150` 正文写「实测 `aria/skills/*/` 共 43 个 skill」, 这是数目录的口径
     - `ab-suite/trigger/` 目前不存在
   - 修法: Impact、D5.2 的 issue 标题、OQ-7 改成「T4 后 41/42」, 并写上计数命令。

6. **时长**
   - 各轮 run.log 算出的单臂时长:
     - v2 (单 worker, 四臂并行): new 11m26s / poscontrol 15m46s / negctrl 16m30s / old 17m39s
     - v3: old 10m39s / poscontrol 11m06s / new 11m07s / negctrl 12m03s
     - v4: overbroad 13m38s / realroot 13m54s
   - RESULT 的「10m39s–13m54s」只取了 v3 和 v4。另外 v3 四臂从 17:18:18 跑到 17:30:21, 共 12m03s, 不是「12 分钟内」。
   - 修法: 区间改成 10m39s–17m39s; 串行两臂写成区间 (约 22–34 分钟); Impact 同步改。

7. **探针**
   - 两份探针 json 的字段:

     | 字段 | default | project |
     |---|---|---|
     | result | "97,yes" | "12,no" |
     | total_cost_usd | 0.6044 | 0.0786 |
     | 输出 (其中思考) | 1190 (1184) | 5 (0) |
     | cache_creation | 27065 | 3696 |

   - 两份的 modelUsage 都是 claude-fable-5-1, 因为两次都显式传了 `--model`。所以它们证明不了「不传 `--model` 会换模型」。D3 第 4 行已经如实标了「无对照实测」, 但括注「(探针 modelUsage 字段)」容易让人误以为这就是证据。
   - manifest.json 记的是「97→13」, 与探针的 12 不一致, RESULT 没有说明原因。
   - 结论方向本身成立: 默认设置源确实会加载真的 openspec-archive, 上下文也明显变大, 由 yes/no 和 cache_creation 的差支撑。但精确数字和成本倍数不能当成机读计数。
   - 修法: D3 第 3 行写「自报 97 / 12 (manifest 同配置自报 13)」; 要机读计数就用 stream-json 的 init 事件列表; 成本对比注明其中混有思考输出的差。

8. **SC-2 / SC-7 字面执行**
   - 在基线目录里逐字跑 `test -e`:
     - `v1-shared-root-4workers/*.json`: 假 (加引号时通配不展开; 不加引号时 test 报 too many arguments, rc 2)
     - `v1-…/diag02-sibling-command-collision.jsonl`: 假
     - `v2-…`: 假
     - `v3-…/negctrl.json`: 假
     - 「基线目录本身」: 假
     - 三个具名文件: 真
   - SOT 头部实际是 `> **Version**: 1.0.0`。`grep -c "Version: 1.0.0"` = 0, 而 `grep -c "Version\*\*: 1.0.0"` = 1。所以改完后字面的「Version: 1.1.0」同样是 0。
   - 修法: D3 实证格写全路径, 或写成「目录 + 文件名列表」; SC-2 规定通配怎么判 (比如「至少一个匹配」); 第 6 行要么豁免, 要么给一个具体文件; SC-7 改为按 `**Version**: 1.1.0` 这个字面 grep。

9. **handoff**
   - `git show --name-only 55bc9f3` 共 14 个文件, 没有 docs/handoff。
   - docs/handoff 下 2026-09-13 的五份 handoff 里, 只有 aria-plugin-196 那份提到 `10CG/Aria#211`, 内容是「新到两条 issue 无人认领 … triage」, 时间早于本 Spec。
   - 修法: 先写好 handoff 再写「见」; 或者改成「将于本 session 收尾 handoff 登记」。

10. **D4 模板值域**
    - 模板定义的值域:
      - decision_table_row: 1 | 2 | 3 | 照跑
      - scenario1: 结果目录 | not_required | n/a
      - scenario4b: 结果目录 pass|fail | not_required
    - 本 Spec 自己的 rule6_note: decision_table_row: n/a、scenario4b: n/a、negctrl: n/a。
    - SOT §2 决策表第二行的处置是「照跑 AB, 零裁量」, 第四行 (拿不准) 是「照跑」, 单写「照跑」分不清是哪一行。
    - 修法: decision_table_row 取值改为 1 | 2 | 3 | 4 | n/a (n/a = 无 Skill 变更); scenario4b 加上 n/a 和 void; 写明 n/a 的适用条件。

11. **「数据组织」锚点**
    - 手册标题清单里没有「数据组织」; 全仓 grep 这个词, 只命中本 proposal 自己的两处。
    - 本席 R1 把「### 固定测试集 vs 临时测试」表 (「固定测试集 | ab-suite/ | 常态化比对 | 修改需升版本号，旧数据不可比」) 误称为「§数据组织」, v2 照搬了。这是本席的错, 在此更正。
    - 修法: Key Deliverables 和 T2 改为在「## 架构 / ### 固定测试集 vs 临时测试」表加 trigger 行, 并在「### 目录结构」树的 ab-suite/ 下加 trigger/。

12. **RESULT.md 的引用**
    - ab-results 下共有 9 份 RESULT.md, 其中 `2026-09-08-v1.73.0-archive-skill-drift` 那份同样与 openspec-archive 有关。
    - RESULT v2 头部要求「引用方请写 RESULT.md v2 @ <提交 SHA>」。proposal 头部、D1 的 CLAUDE.md 新句、D6 的 SOT 新句都没带 SHA, D1 和 D6 连路径也没有。
    - SOT §6 末句目前指向 `10CG/aria-plugin#116`, 那是前两条 (baseline 污染) 的出处。
    - 修法: CLAUDE.md 新句改成指向 SOT (由 SOT 承载全路径); SOT 写主仓相对路径加 `@ 55bc9f3`; D6 第三条自带出处 (`10CG/Aria#211` 加路径), §6 改为每条各注出处。

13. **「场景 1 是空证据」说得太满**
    - skill-creator SKILL.md Step 1 给 with-skill 臂的提示是「Skill path: <path-to-skill>」, 子代理按路径读 SKILL.md, frontmatter 里的 description 就在上下文中。
    - 描述里可以写行为: 基线正控的 description 原文有「不要自己手工 mv」; v1.71.1 → v1.73.0 的改动「自动修正 CLI bug」→「并做归档后落点校验」描述的也是行为。
    - 只改 description 时, 场景 1 新旧两臂唯一的差别就是这段文字: 它测不到触发, 但不一定测不到文字内容对执行的影响。同样的全称句还会写进 SOT §2 新句 (「对该维度是测量剧场」)。
    - 修法: 改为「对触发维度结构上是空证据」; OQ-6 写出「不跑」一侧的代价 (可能漏掉 description 文字对执行的影响), 交 owner 裁。

14. **OQ 的写法**
    - OQ 段标题自己写了「每项给推荐与代价」, 但有三项只写了一边:
      - OQ-4 只写了升 Level 3 的代价, 没写维持 Level 2 的代价 (不跑 post_planning 审计)。而且 LEVEL_GUIDE 原文是「跨模块条件 (满足任一): 涉及 2 个及以上模块 / 修改 shared/ 目录 / 需要 API 契约变更 / 影响多个子模块; 跨模块 → 自动提升为 Level 3」, 模板里的「Changes affecting 2-5 files」只是「When to use」提示, 两者分量不对等。
      - OQ-5 只写了备选项的代价。
      - OQ-6 只写了「两者都跑」的代价。
    - OQ-5 标「issue 原文」, 对照 issue 实际文字: 「若两个 description 的触发率在统计上无差别, 说明场景 4 在本仓语料下同样测不到, 那就是**又一个测量剧场**, 应改开「触发率评测本身不可用」的单而不是把它写进 Rule #6」。OQ-5 删掉了中间那句理由, 也改了用字。
    - 修法: 三项补上自身的代价; OQ-5 改成逐字引用, 或者标「节录」。

15. **OQ 里的数字**
    - D2 要求每次场景 4b 都同批跑负控; Impact 自己也写了「被评 + 负控两臂 约 120 次 … 约 10 美元」。OQ-3 却说改 query 后「需重跑一臂约 12 分钟 / 5 美元」, 按 D2 至少要两臂。
    - OQ-6 的「30 分钟 / 15 美元」在 proposal、RESULT、手册里都找不到出处。ab-results 下已有 133 份 timing.json (例: 2026-09-03 v1.69.0 那次单次运行 216–314 秒), 可以拿来估算。

16. **SC 覆盖**
    - 八条 SC 各管什么: SC-1 核心句 / SC-2 前置表路径 / SC-3 字段名 / SC-4 套件 diff 和版本号 / SC-5 比较句 / SC-6 issue / SC-7 §6 计数和版本号 / SC-8 标题。
    - D2 的「runs 3 / 阈值 0.5 / timeout 120 / 20 条 / 负控 +N / 作废后动作」没有任何一条 SC 能看到; SOT §3 的边界注也一样。反事实: T2 把阈值写成 0.8, 或者漏掉负控规则, 八条 SC 照样全绿。
    - T1 的 CLAUDE.md 新句已经包含「(字段见 SOT §4)」, T3 又要求「CLAUDE.md 加指向句」, 没说明是同一句还是另加一句。
    - 修法: 加一条 SC, grep 手册 4b 小节里的参数串和负控规则关键词 (改前手册应为 0), 以及 SOT §3 边界注的原句。

17. **今后新建套件要不要审**
    - OQ-3 推荐「先审」, 理由是 skill-creator Step 2 要求审阅; 可 D2 对以后每个 skill 首次建套件只写了「约 1 小时 + 一次运行」。
    - 修法: D2 写明新建套件是否须 owner 审阅 (或者给出不需要审阅的替代校验, 比如负控和过宽两个反事实臂), 并把等待审阅的时间算进 Impact 和 OQ-7。

## 优点

- R1 本席的三条 major 都改到了实处:
  - 删掉了「恒绿」, 并补了过宽反事实臂 (v4 overbroad should-not 22/30, query 级 7/10 判红), should-not 那半边门第一次有了真实的 FAIL 样本。
  - 偏离验收第 2 条改成了 OQ-5, 交给 owner 裁。
  - D4 改为「新建」模板, SC-3 的反事实不再是真空成立。
- D1 给出了逐字旧句和定稿新句。实跑三条旧句各自唯一命中, T1 可以机械执行; 核心句在三条新句里逐字相同, SC-1 改前为 0, 是一条改前失败、改后才能通过的好 SC。
- RESULT v2 的统计全部能从原始 json 复算出来: 14 份臂文件的 pass 字段, 与 run_eval.py 的 did_pass 语义逐条一致; query 级 p = 0.0031、负控命中分布 3/3、2/3、3/3 都复算一致。
- T7 把多远程约束 2 落成了逐 remote 的 ls-remote 核验。
- 头部字段、Linked Issue 全限定、裸引用、禁用字形、Rule #5 落点、rule6_note 段全部合规。

## Verdict

**PASS_WITH_WARNINGS** —— critical 0 / major 2 / minor 15。

- **Phase 1 (规范合规): PASS**
  - issue 的建议 1–3 都有落点 (分别是 D1 / D1 三处同批 / D4)。
  - 验收 1、3 由基线兑现; 验收 2 的改判已列为 OQ-5 请 owner 裁。
  - 实跑通过: `check_bare_issue_refs.py` 对 proposal 和 RESULT 都是 rc 0; 禁用字形扫描 0 命中; 头部四字段顺序与 proposal-minimal 一致; Rule #5 落点正确 (proposal 是主仓 blob, `aria-plugin-benchmarks` 是主仓 tree 而非子模块); rule6_note 段在场, 且自评「不触发 Rule #6」成立 (aria 子模块零改动)。
- **Phase 2 (质量)**
  - 两条 major 都是 v2 新引入的:
    - D2 负控判据在 should-trigger 方向会把严重退化判成「作废」, 而不是 FAIL。这是门禁的核心逻辑。
    - SC-5 从散文改成 grep 后, 对存量文字恒红。
  - 其余是数字、锚点和措辞层面的 minor。数字层面的主要偏差有三处: 时长区间漏了 v2; 「+4」的 p 值说错; 42/43 的分母错。

## Vote

**REVISE** —— major 没有清零。两条 major 都只需改文字: D2 把有效性判据改成与被评对象无关, 并写明「作废」之后的动作; SC-5 把 grep 目标限定到新句。改完后下一轮有望收敛。

## 映射表

| issue 条目 | D | T | SC | 备注 |
|---|---|---|---|---|
| 建议 1 (两个义务, 不互相替代) | D1 | T1 | SC-1 | 完整 |
| 建议 2 (SOT 与手册同批改) | D1 三处 | T1 | SC-1 | 完整 |
| 建议 3 (rule6_note 加栏) | D4 | T3 | SC-3 | 值域有缺口 (Findings 第 10 条) |
| 验收 1 / 3 (基线、负控) | 头部「基线数据」; D2 同批负控 | 无 (已完成) | 无 | 负控判据有逻辑洞 (Findings 第 1 条) |
| 验收 2 (区分力为零时的规定动作) | OQ-5 | 无 (待裁) | 无 | 已请复议 |

| D (子项) | T | SC | 备注 |
|---|---|---|---|
| D1 三处新句 | T1 | SC-1, SC-5 | SC-1 前提成立 (旧句各唯一; 核心句三处逐字相同; 改前各为 0); SC-5 恒红 (Findings 第 2 条) |
| D1 SOT §3 边界注 | T1 | 无 | 没有 SC 覆盖 (Findings 第 16 条) |
| D1 只改 description 不跑场景 1 | T1 (随新句落地) | 无 | 取决于 OQ-6 |
| D2 判据 / 参数 / 负控 / 不设比较 | T2 | 无直接 SC | Findings 第 1、4、16 条 |
| D2 套件文件 + version.yaml | T4 | SC-4 | 完整 |
| D2 手册「数据组织表」加 trigger 行 | T2 | 无 | 锚点不存在 (Findings 第 11 条) |
| D3 六条前置表 | T2 | SC-2 | 字面 `test -e` 对不上 (Findings 第 8 条) |
| D4 SOT §4 五字段模板 | T3 | SC-3 | 反事实非真空 |
| D4 CLAUDE.md 指向句 | T3 (与 T1 重叠) | 无 | Findings 第 16 条 |
| D5.1 拆 4a / 4b | T2 | SC-8 | 完整 |
| D5.2 无 trigger 套件 issue | T6 | SC-6 | 标题计数错 (Findings 第 5 条) |
| D5.3 aria-plugin 模板 issue | T6 | SC-6 | 完整 |
| D5.4 上游反馈 | T6 | SC-6 | 覆盖弱: 只查 `10CG/Aria#211` 有没有这条评论, 不查反馈内容的四个要素 |
| D5.5 合并前查 `10CG/aria-standards#17` | T7 | 无 (流程任务) | 可接受; 该单实查为 open |
| D6 §6 第三条 + 计数语 | T5 | SC-7 前半 | 完整 |
| SOT 头部 Version 1.1.0 | T5 | SC-7 后半 | 没有 D 锚 (由头部 ship target 承载); 字面对不上 (Findings 第 8 条) |
| 流程: 合并 / 双推 / 逐 remote 核验 | T7 | 无 | 流程任务, 不需要 D |
| 流程: `10CG/Aria#211` 回帖 | T8 | 无 | 流程任务 |

Key Deliverables 的 D 锚核对: 五条里各子项都有 D 锚, 例外两处: 「文件头 Version 1.0.0 → 1.1.0」没有 D 锚; 「§数据组织表」挂在 D2 下, 但它指向的小节不存在。

## 实跑记录

1. `python3 aria/skills/state-scanner/scripts/check_bare_issue_refs.py <proposal.md>` → 「裸 issue 引用: 0」, rc 0; 对 RESULT.md 跑 → 同样结果, rc 0。
2. 禁用字形扫描: 按 content-integrity §4.5 的四段 (U+2460–U+24FF / U+2776–U+2793 / U+3251–U+325F / U+32B1–U+32BF) 加希腊字母大小写区, proposal 与 RESULT 均 0 命中; NUL 字节 0。
3. `grep -cF` 查三条旧句:
   - CLAUDE.md 1 (规则 #6 表后那一行)
   - SOT 1 (§2 附加约束段末句)
   - 手册 1 (§确定性代码层变更「边界与留痕」段)
   - 核心句现状: 三个文件各 0。
   - 用 Python 取出三条新句检查: 核心句都在, 且逐字相同。
4. SC-5 的三个 pattern:
   - CLAUDE.md 0 / 0 / 0
   - SOT 1 / 0 / 0 (命中 §6 第一条)
   - 手册 1 / 0 / 0 (命中 §版本管理)
5. SC-3 反事实: SOT 里五个字段名各为 0。SC-7: 「两个已知缺陷」= 1, 「三个」= 0; `grep -c "Version: 1.0.0"` = 0, 而 `grep -c "Version\*\*: 1.0.0"` = 1。SC-8: `^### 场景 4a` 与 `^### 场景 4b` 均为 0。
6. SC-2: 在基线目录逐字 `test -e` —— 省略号路径、通配、「基线目录本身」共 7 个为假, 3 个具名文件为真; 不加引号的通配 → 「test: too many arguments」, rc 2。
7. 原始 json 重算 (query 级命中 := `trigger_rate ≥ 0.5`):

   | 轮 | should-trigger (run 级 / query 级) | should-not (run 级 / query 级) |
   |---|---|---|
   | v1 | new 4 (0) / old 7 (1) / negctrl 0 (0) / poscontrol 6 (0) | 四臂均 0 |
   | v2 | 27 (9) / 30 (10) / 27 (9) / 30 (10) | 四臂均 0 |
   | v3 | 30 (10) / 30 (10) / 8 (3) / 30 (10) | 四臂均 0 |
   | v4 overbroad | 30 (10) | 22 (7) |
   | v4 realroot | 30 (10) | 0 |

   14 份文件的 pass 字段都与 did_pass 语义一致。v3 负控命中分布 3 / 2 / 3, 与 RESULT 一致。
8. Fisher 检验:
   - run 级 new vs negctrl 双侧 8.3e-10
   - query 级 new vs negctrl 双侧 0.0031, 单侧 0.0015
   - new vs old 为 1.0
   - 余量恰为 4 的七种组合单侧 p: 0.0433 / 0.0704 / 0.0849 / 0.0894 / 0.0849 / 0.0704 / 0.0433
   - 被评 10/10 对负控 5 → 0.0163, 对负控 6 → 0.0433。
9. run.log 各臂时长: 见 Findings 证据第 6 条; v1 各臂串行, 每臂 3m20s–4m14s (4 worker)。
10. 探针 json 的字段: 见 Findings 证据第 7 条。
11. run_eval.py: 插件缓存 `bb335391eb83`、缓存 `unknown`、marketplace 三份内容完全相同。did_pass 在第 229–234 行 (should-trigger 为 `≥ threshold`, should-not 为 `< threshold`); 命令文件名 = `{skill_name}-skill-{uuid8}`, 正文含 `# {skill_name}`, 与缺陷 (b) 的描述一致。skill-creator SKILL.md 的 Step 1 with-skill 提示含「Skill path: <path-to-skill>」。
12. skill 计数: 已跟踪 SKILL.md 42 个; `ls aria/skills` 44 项; `issue-triage-workspace` 被 `.gitignore` 的 `skills/*-workspace/` 规则忽略; `ab-suite/trigger` 不存在; `ab-suite/version.yaml` 为 1.5.0; 套件文件是 list, 共 20 条。
13. Forgejo 实查:
    - `10CG/Aria#211`: open, 创建于 2026-09-09, 1 条评论 (comment 23915, triage 5/5)
    - `10CG/aria-standards#17`: open
    - `10CG/aria-plugin#150`: open, 正文写「共 43 个 skill」
    - comment 22921: 创建于 2026-09-08, 属于 `10CG/aria-plugin#190`
14. git:
    - `55bc9f3` 共 14 个文件, 无 docs/handoff
    - `git ls-tree HEAD`: proposal 为 blob (100644); `aria-plugin-benchmarks` 为 tree (040000); aria / standards 为 160000
    - 子模块只有 aria / aria-orchestrator / standards
    - standards: 0 个 tag、无 VERSION 文件, remote 为 origin + github; 主仓 remote 同为 origin + github
15. 判据原文: LEVEL_GUIDE 在 `aria/skills/spec-drafter/LEVEL_GUIDE.md` 的「跨模块判断」节; proposal-minimal 在「When to use Minimal (Level 2) Spec」下写有「Changes affecting 2-5 files」。
16. SOT 的运行时消费方: 全 aria/skills 里只有 `state-scanner/tests/test_runtime_probe_authoring_guide_contract.py` 在 docstring 里提到这份 SOT, 它实际读的是自己的 guide 文件, 不读 SOT。所以改 SOT 不会让任何测试转红。
