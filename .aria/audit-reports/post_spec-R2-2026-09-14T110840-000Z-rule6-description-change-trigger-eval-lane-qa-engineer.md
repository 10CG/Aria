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
verdict: FAIL
timestamp: 2026-09-14T11:25:00.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [qa-engineer]
---

# post_spec Round 2 — qa-engineer 席

> 被审 SHA `55bc9f3` (rework v2)。对照: R1 聚合报告 `post_spec-R1-...-aggregated.md`, 本席 R1 报告。

## R1 对账 (found_by 含 qa 的条目, 共 8 条; 逐条复算)

| # | R1 严重度/摘要 | v2 状态 | 依据 |
|---|---|---|---|
| 1 | critical — should-not 三轮四臂恒 0/30, D2 拒绝能力从未证伪 | **partially closed** | v4 `overbroad.json`: should-not 22/30 (query 级 7/10 判红), FAIL 分支确定可达。经逐条核查 (见下「critical 复算」), 7 条判红 query 均非误标 (确系真实近似误触, 非应重归为 should)。**但**: overbroad description 是「任意关键词命中即必须先用」式极端构造, 不是「轻微越界」的现实型坏 description; 守卫的**敏感度/掐点**(多接近真实误改才会被抓到)仍未验证。核心质疑(从未见过 FAIL)已解, 残余降级为新 major (见 Findings)。 |
| 2 | major — n=30 伪重复, query 级 n=10 重算 | **closed** | RESULT v2 §统计给出双单元表, new vs negctrl query 级 p=0.0031 与 R1 复算一致; new vs old p=1.0 一致。 |
| 3 | major — 负控 8/30 分布集中 3 条含"收尾/核对/校验"语义, 未删净通用动作词, 正文漏计一条 2/3 | **closed** | RESULT v2 已勘正为"两条3/3+一条2/3"三条分布, 且新增局限第 3 条如实标注"没删净通用动作词"。R1 rework 计划给的是"加第二负控**或**如实标注"两选一, v2 选了后者, 满足该分支。 |
| 4 | major — D3 第 4 条"显著"无检验方法/alpha/最小差值, 与零裁量相悖 | **partially closed** | v2 D2 给出机械判据(query 级命中 ≥ 负控 +4, 声称"n=10 时 Fisher 单侧 p 约 0.03 以内")。**但**复算显示该声称在判据边界(评 10/10、负控 6/10, 差值恰为 4)不成立: 单侧 p≈0.0433, 双侧≈0.087, 均超出"0.03 以内"; 当被评本身未饱和(如 8/10)时同一"+4"差值对应 p 可到 0.085~0.31。"零裁量"的操作性阈值给出了, 但其自证的统计强度是错的, 见 Findings。 |
| 5 | major(+minor) — OQ-4 Level 未给判据 | **closed** | v2 OQ-4 给出两条判据("跨模块→L3" vs "2-5文件→L2")+ 推荐(默认 L2, 仅 owner 要求 tasks.md 逐项验收才升 L3)+ 代价(+1 小时)。 |
| 6 | minor(tech-lead, qa) — SC-1"或 owner 定稿的同义句"逃生口不可机械判 | **closed** | v2 SC-1 改为"逐字, 无同义替代", 逃生口已删。 |
| 7 | minor — 运行脚本路径写死 scratchpad, 插件缓存 hash / 模型无后备 | **partially closed** | RESULT v2 工具行给出 hash 漂移的 `find` 兜底命令; 模型 (`claude-fable-5-1`) 仍无弃用后备。未交付可复用参数化脚本模板, 未来每个 skill 跑场景 4b 仍需从散文重新拼装脚本 (原风险未消除, 仅缓解一半)。 |
| 8 | minor — 20 条 query 未经 owner 审阅即计划原样搬入 | **partially closed** | OQ-3 原样保留待裁 (符合预期, 这是给 owner 的开放问题非 AI 自行拍板); D2 新增"沿用 ab-suite 版本化规则"降低了"审阅后改动与基线数字脱节不可查"的风险 (改动会被版本号强制标记并要求重跑)。残余: owner 若一直不裁, "未审"状态可无限期随 T4 搭车进正式套件, v2 未加时间/门槛兜底。 |

**closed**: 3 条 (#2 #3 #6) · **partially closed**: 4 条 (#1 #4 #7 #8) · **open**: 0 条

### critical 复算 (task 1 明细)

```python
from scipy.stats import fisher_exact
# 判据边界: 评 10/10, 负控恰在 +4 门槛线上 (6/10)
fisher_exact([[10,0],[6,4]], alternative='greater')   # -> p ≈ 0.04334
fisher_exact([[10,0],[6,4]], alternative='two-sided') # -> p ≈ 0.08669
fisher_exact([[10,0],[7,3]], alternative='greater')   # 差值3(应作废) -> p ≈ 0.10526
fisher_exact([[10,0],[3,7]], alternative='greater')   # 基线v3实测 10 vs 3 -> p ≈ 0.001548 (与RESULT v2一致)
# 被评本身未饱和 (8/10) 时同一 "+4" 规则的行为
fisher_exact([[8,2],[4,6]], alternative='greater')    # 8 vs 4 (差4, 满足门槛) -> p ≈ 0.08490
fisher_exact([[8,2],[6,4]], alternative='greater')    # 8 vs 6 (差2, 不满足门槛) -> p ≈ 0.31424
```

overbroad.json should-not 判红 7 条逐条核查 (原始索引对齐 `trigger-eval-openspec-archive.json` should-not 段第 2/3/5/7/8/9/10 条, 0-based 11/12/14/16/17/18/19):

- "挪 handoff 文档进 archive/2026-05/" — 目标是 docs/handoff/, 非 openspec 变更归档, 真实近似误触, 非误标。
- "起一份新 proposal.md" — 新建而非归档已完成变更, 真实近似误触。
- "核对 Archive Tracker issue 里哪些做完可以关" — 核对待办不等于执行 D.2 归档动作, 真实近似误触。
- "把 proposal.md 的 Status 从 Approved 改成 In Progress" — 编辑状态字段而非归档, 真实近似误触。
- "查项目整体状态, 推荐下一步跑哪个阶段" — 属 state-scanner 类查询, 非归档, 真实近似误触。
- "openspec/archive/ 145 个目录按年份分层" — 目录重排脚本, 非单个变更归档, 真实近似误触。
- "汇总已关闭 issue 成 changelog 归档到 docs/" — 归档对象是 changelog 文本非 OpenSpec 变更, 真实近似误触。

七条均无需重归为 should — ground truth 站得住; overbroad 臂测到的是真实误触发, 不是标注噪声。

## Findings

- [major] testing/RESULT.md §已知局限 (issue): "记入本 session 的 handoff (docs/handoff/, 与本文件同批提交)" 为可核验虚假声明——`git show 55bc9f3 --stat` 显示同批提交仅含 proposal.md / RESULT.md / 六份审计报告等, 不含任何 `docs/handoff/*.md`; 全仓搜索本 spec 相关关键词 (`Aria#211`/`未经审阅`) 在 `docs/handoff/` 下零命中。R1 minor #28 未闭合, 反而换成了更具体、更容易被核验为假的措辞。
- [major] documentation/proposal.md §D2 negctrl+4 判据 (risk): 声称"query 级 n=10 时差值 4 对应 Fisher 单侧 p 约 0.03 以内", 但判据边界情形 (评 10/10、负控 6/10) 实测单侧 p≈0.0433、双侧≈0.087, 均超出声称范围; 被评本身未饱和 (如 8/10) 时同一"+4"差值对应 p 在 0.085~0.31 间, 固定绝对差值判据的显著性随基线饱和度剧烈漂移。给出了可操作阈值但其自证的统计强度不成立, 执行者若照字面"约 0.03 以内"论证会得到错误结论。
- [major] documentation/AB_TEST_OPERATIONS.md §SC-5 (risk): 该文件现有第 193 行「新版本的结果与旧版本 **不可直接比较**」(位于 §版本管理小节, 与 D1 三落点无关) 已命中 grep 模式「新版.*旧版」; SC-5 若按裸 `grep -c` 全文执行, 无论 D1 是否正确落地都会读到非零, 使该 SC 结构上不可能通过 (除非顺手删掉这句无关文字, 那又是未声明的副作用)。需把 SC-5 的 grep 限定到三处 D1 新增语句本体, 不能是整文件搜索。
- [major] testing/v4-counterfactuals/overbroad.json (risk): critical 核心质疑(拒绝能力从未证伪)已由 overbroad 臂关闭, 但该臂是"任意关键词命中即必须先用"式极端构造描述, 不代表真实世界渐进式的轻微越界(如多加 2-3 个泛化词); 场地板守卫对"多接近真实误改才会触发 FAIL"这一敏感度/掐点仍未验证, 存在"只挡得住荒谬 description, 挡不住现实型 description creep"的风险未消。
- [minor] documentation/proposal.md §SC-2 第 4 行 (risk): "配置推导, 无对照实测"豁免以表格行位置("第 4 行")定位而非稳定锚点/字段名标识; 六行前置表若日后增删或重排, 复核者(人工或脚本)易错认豁免行, 或该短语字面被复制到其它行以规避 `test -e`。
- [minor] documentation/proposal.md §SC-2 (risk): 未显式要求"手册 4b 前置表必须恰有六行且内容对齐 D3 表"作为前置判定; 若 4b 小节整体未落地(机制缺失), "每行…test -e 为真"在零行上可真空成立 (vacuous truth), 需先判"表存在且六行齐"再逐行核验。
- [minor] documentation/proposal.md §SC-6 (risk): "两张 issue 存在且 open"把瞬时状态当持久判据——D5.2/D5.3 两张 issue 对应的后续工作(43 技能建套件 / spec-drafter 模板加字段)一旦被正常关闭(工作完成的期望结果), SC-6 会从 PASS 翻转为 FAIL; 建议改判据为"存在"(不限状态)或只在落地当轮评审窗口内检查。
- [minor] testing/RESULT.md §统计 (risk): query 级 n=10 修正了 run 级伪重复, 但同一 arm 内 10 条 query 仍共享同一个"被评 description"处理, 并非 10 次独立的 description 抽样; Fisher 结论的外部效度(能否推广到其它 description/套件)局限于本 20 条固定套件本身。RESULT v2 已承认"套件偏差"方向, 但未点名"query 级独立性本身也是相对同一处理而言, 非跨处理独立"这层统计前提。
- [minor] documentation/proposal.md §OQ-3 (risk): 20 条 query 未经 owner 审阅仍计划 T4 逐字节搬入正式套件; D2 版本化规则降低了"审阅后改动与基线数字脱节不可查"的风险(改动会强制升版重跑), 但若 owner 长期不裁 OQ-3, "未审"状态可无限期随 T4 搭车进正式套件, v2 未给时间或门槛兜底。

## Verdict

FAIL — 0 critical (原 1 条降级) / 4 major / 5 minor。R1 的 1 条 critical 与 3 条 qa 关联 major 中 2 条已 closed, 但本轮新增/残余 4 条 major (含 1 条从 critical 降级而来), 按 convergence 判据"Major 归零才可 PASS", 本席判 Major 非零 ⇒ 不收敛。

## Vote

REVISE

## 复算记录

```python
from scipy.stats import fisher_exact

# 1) D2 "+4" 判据边界情形复算 (对应 D3 第4条声称 "n=10 时 p 约 0.03 以内")
fisher_exact([[10,0],[6,4]], alternative='greater')   # p ≈ 0.04334  (超出 0.03)
fisher_exact([[10,0],[6,4]], alternative='two-sided') # p ≈ 0.08669
fisher_exact([[10,0],[7,3]], alternative='greater')   # 差3(应作废场景) p ≈ 0.10526
fisher_exact([[10,0],[3,7]], alternative='greater')   # 基线v3实测 p ≈ 0.001548 (与 RESULT v2 一致)
fisher_exact([[8,2],[4,6]], alternative='greater')    # 被评未饱和(8/10)+差4  p ≈ 0.08490
fisher_exact([[8,2],[6,4]], alternative='greater')    # 被评未饱和(8/10)+差2(不满足门槛)  p ≈ 0.31424
```

```bash
# 2) SC-3 反事实: 现行 SOT/CLAUDE.md/手册对五个字段名 grep 是否为 0
for name in decision_table_row description_changed scenario1 scenario4b negctrl; do
  grep -rn "$name" standards/conventions/skill-benchmark-exemption.md CLAUDE.md aria-plugin-benchmarks/AB_TEST_OPERATIONS.md
done
# 输出: 全部 exit 1 / 零命中 —— SC-3 反事实成立 (现行 SOT 确实没有这五个字段名)

# 3) SC-5 反事实: 三处落点 grep 比较判据模式是否已恒非零 (与 D1 是否落地无关)
grep -rn "新版.*旧版\|≥ 旧版\|不低于旧版" CLAUDE.md standards/conventions/skill-benchmark-exemption.md aria-plugin-benchmarks/AB_TEST_OPERATIONS.md
# 命中: aria-plugin-benchmarks/AB_TEST_OPERATIONS.md:193: "新版本的结果与旧版本 **不可直接比较**" (§版本管理, 与 D1 无关)
# 结论: SC-5 若裸 grep 全文, 与 D1 是否合规实现无关地非零

# 4) "见 handoff" / "同批提交" 反事实
git show 55bc9f3 --stat | grep -i "docs/handoff" # 零命中
ls docs/handoff/ | grep 2026-09-13               # 三个当日 handoff 文件均与本 spec/issue 无关
grep -rl "Aria#211\|未经审阅" docs/handoff/*.md   # 零命中
```

结果汇总: D2 "+4" 判据声称的统计强度在边界情形不成立 (0.0433/0.0867 均超"0.03以内"); SC-3 反事实确认现行 SOT 干净 (5 字段名零命中, 该 SC 可正确判红); SC-5 反事实证明该检查存在与实现无关的假阳性来源 (第 193 行既存无关句已命中三模式之一); RESULT v2 的"同批提交 handoff"声明经 git 与目录核验为假。
