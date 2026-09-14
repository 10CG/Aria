---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-14T12:24:57.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [qa-engineer]
---

# post_spec Round 3 — qa-engineer 席

> 被审 SHA `0c41e53` (rework v3)。对照: 本席 R2 报告 (9 条: 4 major + 5 minor) 与 R2 聚合报告。

## R2 对账 (本席 R2 的 9 条逐条判)

| # | R2 严重度/摘要 | v3 状态 | 依据 |
|---|---|---|---|
| 1 | major — RESULT.md §已知局限 "记入本 session 的 handoff" 为可核验虚假声明 | **closed** | RESULT.md v3 版本行自陈"删除一处失实的「同批提交」声明"; 全文 grep `handoff`, 仅剩 2 处合法用法 (臂配置行"archive / handoff / README" 描述 realroot 臂的合成目录、结论段"handoff 归档"描述 overbroad 臂的 query 内容), 均非"记入 docs/handoff/"式声明; §已知局限末条改写为"跑时 owner 不在线...写在 Spec 的 OQ-3 与 rule6_note 段, 由 owner 复议", 不再提 handoff/同批提交。另核实 proposal.md line 9 现存"同批提交"表述 (指 RESULT v3 与 proposal v3) 对 `git show 0c41e53 --stat` 为真 (两文件确实同一 commit)。 |
| 2 | major — D2 "+4" 判据边界情形 (10 对 6) 实测单侧 p≈0.0433, 超出声称"0.03 以内", 且随被评饱和度漂移 | **closed** | v3 §D2 弃用"+4 相对差值"改"绝对门槛 ≤5/10"; 复算确认新声称的两个数字均精确: `fisher_exact([[10,0],[5,5]],'greater')` = 0.016254 (v3 写"0.016"); `fisher_exact([[10,0],[6,4]],'greater')` = 0.043344 (v3 写"10 对 6 为 0.043, 不取", 与 R2 复算一致)。且"门通过时被评必为10/10"不再是经验声称而是同一"命中:=trigger_rate≥0.5"定义下的恒等式 (通过⇒全部 should-trigger 命中⇒10/10), 不再有"被评未饱和时 p 会漂移"的问题, 因为判据已改绝对门槛, 不再引用被评自身的命中数。 |
| 3 | major — SC-5 若裸 grep 全文, 手册既存第 193 行"新版本的结果与旧版本不可直接比较"(§版本管理) 会命中, 与 D1 是否正确落地无关地判红 | **closed (已执行反事实验证, 见下「SC 实测记录」)** | v3 SC-5 改为: (a) 限定"手册 §场景 4b 小节正文"(非全文), (b) 用 python `re` 而非 grep, (c) 正则加比较算子约束 (`≥/>=/不低于/高于/优于/不差于`), (d) 先剔除含"不设比较判据"的行。手册第 193/562 行远在 §版本管理/检查清单, 不在 §场景 4b 边界内, 且原句不含比较算子, 双重排除。本轮在临时副本实际落地 4b 小节并跑 SC-5 判定函数: 正确落地全绿; 插入一句真实比较判据 (不含排除词) 正确转红 (见 SC 实测记录 扰动2)。 |
| 4 | major — overbroad 臂是"触发词表+强制指令"式极端构造, 不代表真实渐进式轻微越界; 守卫对"多接近真实误改才会触发 FAIL"的敏感度/掐点仍未验证 | **partially closed** | v3 做了三处披露强化: D2 新增"只承诺已验证的两类破坏"句 (与 CLAUDE.md/SOT 核心句同批, SC-1 管); RESULT v3 结论 2 与已知局限第 3 条同口径重申"未验证: 自然措辞扩张..."; 新开 OQ-8 专门讨论"是否在 ship 前补跑一臂'轻微过宽'", 给出推荐 (不阻塞) 与代价, 且已写入 SOT §6 新增第三条局限。**但**: 这是纯披露/流程强化, 真实的经验证据 (自然扩张会不会被套件的近似误触抓到) 一次也没有新增采集; OQ-8 的推荐路径是"不补跑", 意味着这条 Rule #6 新增强制义务在可预见的将来会带着这个未验证掐点直接生效于 42 个 skill。披露到位 ≠ 风险清零 —— 判据两侧"应验证的两类破坏"确凿有真实 FAIL 样本, 但对最可能在日常 description 编辑中出现的"渐进式扩张"这一类, 门是否会漏判仍是真正的未知数, 且不会随时间自动缩小 (除非有人真的跑一次 OQ-8)。降级理由: 原 R2 批评的核心是"未披露/未成文", 现已妥善成文并走 Rule #10 正规升级路径 (OQ), 不构成 AI 自行豁免; 残余理由: 技术风险本身 (而非流程合规) 未变化, 作为 QA 席按风险对系统的影响判, 仍计 major, 留给 owner 在 OQ-8 一并裁。 |
| 5 | minor — SC-2 第 4 行"配置推导, 无对照实测"以行位置("第 4 行")定位, 表格重排则错认 | **closed** | v3 SC-2 改为"带 `[配置推导]` 标记的行恰一行", 用内容标记代替行位定位; D3 表第 4 行机读实证列确实写了 `[配置推导]` 前缀 (本轮临时副本按此原样落地并核验, 见下)。 |
| 6 | minor — SC-2 未防"表整体缺失时逐行核验在零行上真空成立" | **closed** | v3 SC-2 显式加"(零行或行数不等于六即判红, 防真空成立)"。本轮反事实验证: 手册 4b 小节不存在时判定函数返回 False (非真空 PASS); 删一行后行数=5≠6 同样判红 (见 SC 实测记录 扰动3)。 |
| 7 | minor — SC-6 "两张 issue 存在且 open"把瞬时状态当持久判据, issue 正常关闭会使 SC-6 从 PASS 翻转为 FAIL | **closed** | v3 SC-6 明确"forgejo GET 返回 200, 不限状态"。 |
| 8 | minor — RESULT §统计 未点名"query 级独立性也只是相对同一处理而言, 非跨处理独立"这层统计前提 | **closed** | RESULT v3 §统计新增专段: "query 级单元的独立性也是相对的: 同一臂的 10 条 query 共享同一个被评 description...这些 p 值...不能外推到别的套件或别的 description。"逐字命中该批评。 |
| 9 | minor — OQ-3 "20 条 query 未审阅仍搭车 T4"未给未裁时的默认/门槛兜底 | **closed** | v3 OQ-3 新增"默认 (未裁时): T4 不执行, 不让未审套件搭车进 ab-suite/", 且 Tasks T4 本身已标注"OQ-3 裁定前不执行"。 |

**closed**: 8 条 (#1 #2 #3 #5 #6 #7 #8 #9) · **partially closed**: 1 条 (#4) · **open**: 0 条

## Findings

- [major] testing/proposal.md §D2「只承诺已验证的两类破坏」+ §OQ-8 (risk): 地板守卫对「自然措辞扩张」(最贴近真实 description 日常编辑的退化路径) 的敏感度仍是零经验证据, 只是从"未披露"变成"已披露 + 已开 OQ-8 请裁"; OQ-8 推荐路径是不补跑, 该义务将带着这个未验证掐点直接对 42 个 skill 生效。R2 partially closed 残留, 降级理由与残留理由见对账表 #4。
- [minor] testing/proposal.md §SC-2 (risk): 反事实实测发现, 若不显式限定"仅取表格第三列(机读实证)里的反引号路径", 而是对整行做裸反引号扫描, D3 表第 4 行「前置」列里的路径样式占位串 `` `aria-plugin-benchmarks/ab-results/<date>-<skill>-trigger/` `` (第 6 行, 含 `<date>`/`<skill>` 通配, 永不可能 `test -e`) 会被误当作待核验路径, 使**正确落地**的 SC-2 判定为假阴性 (误判红)。SC-2 文字本身写了"「机读实证」列", 但未写明机械实现须按列而非按行抓取反引号 token, 对照本仓其余 SC 多为一行 grep 的实现风格, 有被裸实现的风险。建议 SC-2 补一句"仅取该行最后一个 `|` 分隔单元格内的反引号路径"。
- [minor] testing/proposal.md §SC-10 (risk): 反事实实测发现, 从 D2「参数钉死」句中单独删除 `--num-workers 1` (其余 3 个钉死参数串不变) 后, SC-10 仍判绿——因为同一字符串 `--num-workers 1` 也逐字出现在 D3 前置表第 1 行 (不同语义: 该行说的是"消除同一项目根内的兄弟命令文件"的运行前置, 不是 D2 的判据参数)。SC-10 按字面只检查"该字符串在 §场景 4b 小节内出现 >=1 次", 未要求出现在 D2 判据正文本身, 对这一个参数 (其余 3 个不受影响, 因它们不在 D3 表出现) 存在"文档字面已被裁减但机械检查读不出来"的假阴性缝隙。风险有限 (信息未真正丢失, 只是 D2 判据正文与 D3 前置表的重复覆盖了漏改), 但与 Rule #6 "零裁量"的设计初衷有摩擦。

## 观察

- RESULT.md v3 结论 1 仍保留"「新版 ≥ 旧版」类比较判据对任意两个真 description 都打平"这一未加限定语的全称表述; 而 proposal.md v3 §Why 第 1 条的同一事实已改写为"两个都能让 should-trigger 饱和的 description 必然打平", 显式把量词限定在"双方都已饱和"这个子集上, 不再是无条件全称。RESULT 与 proposal 是本 Spec 明文要求同步的一对文档 (proposal.md line 9:"RESULT 再修订须同步重核本文 §Why 与 §D2 §D3"), 但这条同 R1/R2 曾被 code-reviewer 点名 (R2 minor #25) 的精确化修正似乎只单向传到了 proposal.md, 未回填 RESULT.md 的对应表述。charitable 读法下 (把"在饱和处"读成同时限定主语的量词) 该句仍可解释为真, 不构成新的恒红/恒绿风险, 也不受任何 SC 管辖, 故未计入 Findings; 建议下次修订 RESULT.md 时顺手把结论 1 也改成与 Why 一致的限定语。
- D2 的负控三分支 (fail / pass / void) 对 negctrl 命中数 0-10 的整数域构成无缝全分割 (≤5 与 ≥6 互斥且穷尽), 未发现 "谓词拆档不总分割" 类问题; "门通过时被评必为 10/10"经确认是"命中:=trigger_rate≥0.5"定义下的恒等式, 不是需要额外证据支撑的经验声称, 表述准确。
- OQ-8 的推荐 (不阻塞 ship) 与代价说明本身写得完整 (给了成本 12 分钟/5 美元、模型一致性要求), 履行了 Rule #10 "推荐项须带代价"的要求, 无格式问题——本条只是走流程正确, 不代表 Findings 中 major 项的技术风险已缩小 (两者正交, 见 Findings 第 1 条)。
- CLAUDE.md 现状仍是改前原句 (Tasks T1 未打勾, 符合预期: 本 Spec 是 Draft, 尚未执行落地任务); 三处 D1 新句 / SOT §4.1 / 手册 4a-4b 拆分均须留到 Phase B 才会真正写入仓库, 本轮反事实验证全部基于临时副本模拟, 不代表已落地。

## Verdict

PASS_WITH_WARNINGS — 0 critical / 1 major / 2 minor。

## Vote

REVISE

（Major 未归零, 按收敛判据"vote=PASS 要求 critical 与 major 同时为 0"不满足; 但 R1→R2→R3 三轮 critical 1→0→0、major(本席) 4→1、且本轮唯一残留 major 是结构性无法用文档修订单方面关闭的经验证据缺口 [已走 OQ-8 正规升级], 供聚合裁量参考。)

## SC 实测记录

方法: 在 `/tmp/claude-1000/-home-dev-Aria/e91a9d6a-05ff-4b26-af79-8d903c21a292/scratchpad/r3-qa/` 建三份临时副本 (`AB_TEST_OPERATIONS.correct.md` / `skill-benchmark-exemption.correct.md` / `CLAUDE.correct.excerpt.md`, 后者为节省 token 只截取 Rule #6 上下文而非全文, 不影响 grep 计数类判定), 按 proposal v3 §D1/§D2/§D3 逐字落一份 `### 场景 4b` 小节 + 三处新句 (构造脚本 `build_sim.py`), 然后用 python 实现 SC-2/SC-5/SC-9/SC-10 的字面判据 (`sc_checks.py`), 对"正确落地"与"三项指定扰动 + 两项附加扰动"分别跑。真实文件系统路径 (`aria-plugin-benchmarks/ab-results/2026-09-13-.../*.json` 等) 用的是仓库里已存在的真实基线产物, 未虚构。

### (a) 正确落地 → 全绿 (SC-2 首次实现有误, 修正后全绿, 过程见下)

```
SC-2: PASS(绿)   # 首次用"整行裸反引号扫描"实现时误判红 (见 Findings §SC-2), 改成"仅第三列"后绿
SC-5: PASS(绿)
SC-9: PASS(绿)   # ≤5/10 次数=1, 连续2轮 次数=1
SC-10: PASS(绿)  # 4个钉死参数串 + "20 条" 均命中; SOT 边界注命中=1
```

### (b) 三项指定扰动 → 对应 SC 是否转红

| 扰动 | 操作 | SC-2 | SC-5 | SC-9 | SC-10 |
|---|---|---|---|---|---|
| 删掉负控门槛 | 把"须 **≤ 5/10**...p = 0.016"改写为"须达标" | 绿 | 绿 | **红** (`≤ 5/10` 次数=0) | 绿 |
| 写进一句比较判据 | 插入新句"新版触发率不低于旧版时视为改进。"(不含"不设比较判据"排除词) | 绿 | **红** (剔除后比较句命中=1) | 绿 | 绿 |
| 删掉一行前置表 | 删 D3 第 3 行 (`claude -p --setting-sources project`) | **红** (行数=5≠6) | 绿 | 绿 | 绿 |

三项指定扰动均命中预期的目标 SC、且不误伤其余三个 SC —— 说明这三条 SC 的判据边界彼此正交, 未发现交叉误判。

### (c) 附加扰动 (SC-10 专属排查) → 发现假阴性缝隙

| 扰动 | 操作 | SC-2 | SC-5 | SC-9 | SC-10 |
|---|---|---|---|---|---|
| 删 D2 判据正文里的 `--num-workers 1` (D3 表第 1 行原样保留) | 只改"参数钉死"句, 去掉其中一个参数 | 绿 | 绿 | 绿 | **绿 (应红而未红, 见 Findings)** |
| 删 SOT §3 边界注「description hunk 不走本节...」 | 删该整句 | 绿 | 绿 | 绿 | **红** (`grep -cF` = 0) |

### 统计复算 (D2 绝对门槛)

```python
from scipy.stats import fisher_exact
fisher_exact([[10,0],[5,5]], alternative='greater')  # -> p = 0.016254  (v3 写 "0.016", 精确)
fisher_exact([[10,0],[6,4]], alternative='greater')  # -> p = 0.043344  (v3 写 "10对6为0.043, 不取", 精确)
fisher_exact([[10,0],[3,7]], alternative='greater')  # -> p = 0.001548  (基线 v3 实测 10 vs 3, 与 RESULT v3 一致)
```

### 完整性核验 (git / grep)

```bash
git show 0c41e53 --stat   # 确认 RESULT.md 与 proposal.md 同批提交 (proposal.md line 9 声明为真)
grep -n "handoff" RESULT.md proposal.md   # 仅剩 2 处合法用法 (测试数据描述), 无失实声明残留
```

脚本落盘 (仅供复核, 不影响仓库): `build_sim.py` / `sc_checks.py` / `perturb_and_test.py`, 均在本报告开头所列临时目录。
