---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-13T02:10:00Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R5 — qa-engineer 独立报告

seat: qa-engineer · vote: **REVISE** · verdict: **PASS_WITH_WARNINGS** (0C + 2M + 1m)

审视角度: SC 可证伪性 — 12(18)条 SC 的红窗是否真实存在 / 有无恒红恒绿空真 / 打桩边界自洽 / 三条负控早退是否真能拒绝坏实现。

---

## 0. R4 的 12M 是否真闭合 — 逐条回源复核 (实跑, 非转述)

R4 五席原始 0C+12M+16m=28, 9 条 `blocks_phase_b`。R4-fix (commit `45c480a`) 自称「触点 12 处, 修了 10 组」。我逐条独立回源复核如下 (每条均实跑命令或实读源文件, 非采信 commit message):

| # | R4 Major | 我的独立验证 | 结论 |
|---|---|---|---|
| 1 | delegate「必然出六条 TASK」在 task-planner 处不成立 (tech-lead) | `grep -n '必然'` proposal.md 全部 9 处命中逐个读, 全部已改为「读到必然, 出 TASK 不必然」的正确表述, 六个落点 (:34/:96-107/:119/:155/:982/:1017-1028) 全扫到 | ✅ 真闭合 |
| 2 | §非目标 `:844` (第四份拷贝) 仍写已作废的 landmine 标注 (tech-lead+qa+code-reviewer 三席) | 现文 §非目标第二条 (:936-943) 已改为「只标注本步自身的作用域边界」, 与 §残余暴露/SC-A-step(c-含)/§Impact 三处口径统一; `grep -n '步骤 3 硬编码'` 全文件零命中 | ✅ 真闭合 |
| 3 | DEC §5.3 owner 裁定 (B 侧 6 条任务须留 cancelled 痕迹) 未执行、未上呈 (tech-lead, `introduced_by_r3fix:false`) | 独立用 `python3 -c "import yaml..."` 解析 B 侧 `detailed-tasks.yaml`: 21 条 task, status 分布 = pending 15 / cancelled 6, cancelled id = `[TASK-003,004,005,007,008,009]`, 逐条 notes 含 `⛔ CANCELLED (2026-08-12, DEC-20260812-001 §5.3)` 字样且指向 A 侧承接。与 A 文 `:867-875` 的复核数字逐字节相等 | ✅ 真闭合 (独立实测, 非采信文字) |
| 4 | Level (b) 跨模块腿仍是自造判据, SOT 四条件未逐条对账 (tech-lead) | 现文 BLOCKER 抬头 (:6-27) 已逐条对四条件 ①②③④ 判定, 条件③ (API 契约变更) 判「⚠️ AI 不自行判定, 上呈 D-c」而非自行判 NO | ✅ 真闭合 |
| 5 | Level (c) Breaking 腿是版本定档的函数, 而 `:119` 明文「不得合并处理」→ 可能产出违反 SOT 的组合 (tech-lead) | D-c 现文新增依赖声明「(c) Breaking=NO 以『版本裁定=MINOR』为前提」+ 裁定顺序改为「不得混为一题, 但须按序裁: 先版本, 后 Level」 | ✅ 真闭合 |
| 6 | SC-A-note 锚点 (`Output schema`/`配置参数:`) 在 SKILL.md 非唯一 (`:501`/`:523` 结构同形), 与刚修好的 SC-A-step 同款病 (**qa-engineer 本人 R4 finding**, `blocks_phase_b`) | 独立 `grep -n '\*\*Output schema\*\*\|\*\*配置参数\*\*:' SKILL.md` = 四行 264/281/501/523; 现文已加「两个锚一律取 `### C.2.4` 标题行 (:218) 之后、下一个 `###` 标题行 (:306) 之前的首个匹配」; 独立验证 `grep -n '^### '` 确认 :306 确是 :218 之后第一个 `###`, 故 [218,306) 区间精确排除 :501/:523 | ✅ 真闭合 (且区间边界我独立验证正确) |
| 7 | SC-A10c 移入「可达前提」适用集时丢了「precheck 必须返 (False,…)」这句括注, 与配方 `precheck()`→`(True,"")` 矛盾 → 完全正确实现下恒红 (code-reviewer) | 现文 (:718-725) 已补回「SC-A10c 是本配方在 precheck() 一项上的唯一例外…precheck() 必须返 (False,…)」, 并指向仓内既有先例 `test_pre_merge_gate.py:272` | ✅ 真闭合 |
| 8 | 定档依据块两条 SOT 行锚都不落在被引文本上 (`LEVEL_GUIDE.md:26`→实为 Q1/LEVEL1 行; `project.md:116`→实为 Level 1 行) (code-reviewer) | 现文 :10-11 已加「R4 更正行锚: 上一版写 :26, 实跑 sed -n '26p' 得的是 Q1 分支…」; :29 同款更正 project.md:117。我独立 `sed -n` 复核两处新锚均命中被引文本 | ✅ 真闭合 |
| 9 | O-1 gitlink 证据命令 `git diff --submodule=short` 提交后恒空, 零区分力 (code-reviewer) | 现文 :855 已换用 `git show --submodule=short <ship-commit> -- aria`; 我独立实跑 `git show --submodule=short fb5ed36 -- aria` 确认输出含两行 SHA, 对未 bump 的 `98ad1f5` 输出 0 行, 两向可区分 | ✅ 真闭合 |
| 10 | 打桩边界表引「B :358-361」实为 B 的 SC-M12/13/14/15 表行, 被引更正在 B :366-369 (code-reviewer) | 现文 :829 已换引 `:366-369`; 我独立 `sed -n '358,369p'` 读 B 侧文件确认「打桩边界 (前一版自相矛盾, 本版钉死)」与「两处自相矛盾」两句确实落在 :366-369 区间而非 :358-361 | ✅ 真闭合 |

**结论: R4 的 12 条 Major (deduped) 中, 11 条被本轮真实、正确地闭合** (含 1 条独立实测非采信文字的历史遗留 Major, 与 1 条我本人在 R4 提出的 finding)。**唯 1 条 Major 被明确声明不修**(`SC-A-step (a)(b)` 补内容序断言, 见下节)。

---

## 1. ⭐ 关于 R4-fix 唯一声明的「不修」Major (`SC-A-step (a)(b)`) — 理由是否成立

任务要求回答: 它自称「改法欠定」而非「不值得改」, 这个区分站得住吗?

**我的独立核验**:
- 三条依据逐条核实: (1) 「新增断言面, 不是修正」——属实, 现文 :368-369 独立成框, 且明确写「不是不值得改的价值评估 (会撞规则 #10), 而是改法欠定」, 措辞上确实做了这个区分, 不是把两者混为一谈后择优选择更省事的说法; (2)「新步骤锚 token 今日不存在, 要现编」——我独立验证: `grep -c 'evaluate_path_coverage' SKILL.md` = **1** (仅 `:242`), `grep -c 'resolve_ci_backend' SKILL.md` = **2** (`:241`/`:319`, 后者在 §C.2.4.X 内, 套用 SC-A-note 新规则后在 §C.2.4 内确为唯一) — 与文中自查推翻的过程逐字节吻合, 这两个数我独立复现且正确; (3)「残余风险有界: 退化为『无从求值』而非假绿」——我认可这个论证, 因为 (a)(b) 不写死, 顶多在 B 折叠后变成「提取序列为空⇒无从判定」, 不会产出一个对错误实现判 PASS 的假绿信号。
- **对「主动留痕自查」是否该计为 finding 的回答**: 不该计。我独立验证了 `evaluate_path_coverage=1` 与 `resolve_ci_backend=2` 两个数字均准确, 说明这次自查本身是真实、正确的自我纠错 (发现自己编造的「不唯一」论据不成立并删除, 只保留成立的「token 未定」论据)。若把诚实、且被证明准确的自我纠错计为扣分项, 会制造反向激励 (掩盖自查比不自查更划算), 这与本 Spec 反复引用的 audit-trail 诚实标注原则相悖。**不计为 finding。**
- **结论**: (a)(b) 不修的理由成立, 我不推翻这个决定。但下节指出: 这个「唯一声明不修」的清单本身**不完整** —— 至少还有 6 处 R4 findings 被静默放弃而未被同等地记录。

---

## 2. Major — SC-A-doc 的 JSON 块定位缺「首个匹配 + 章节内 scoped」规则, 与刚为 SC-A-note 修好的同款病同批留在了它的直接兄弟身上

**locator**: `openspec/changes/premerge-gate-branch-existence/proposal.md:785` (SC-A-doc 行) 对照
`aria/skills/phase-c-integrator/SKILL.md:264` (§C.2.4 正确目标块) · `:339-350` (§C.2.4.X 内的 Config schema example jsonc 块) · `:501-520` (§C.2.4.5 结构同形的第二处 Output schema 块)。

**evidence** (本轮按任务要求对**全部**文档侧锚点做了全文件重复扫描, 不再只验局部区间; 这是本轮的核心发现):

现文 SC-A-doc 逐字「从 `SKILL.md` §C.2.4 Output schema json 块 (`:265-277`) **实际解析**出的**顶层**键名集合」, 其「两条解析规则」(R2 补) 只规定**块内如何解析**(不用 `json.loads`、正则 `^  "([A-Za-z_]+)":`), **完全没有规定如何定位这个「json 块」本身** —— 不像它的两个兄弟 SC-A-step (R3 修) 与 SC-A-note (**本轮 R4-fix 刚修**) 那样有「取 XX 标题/短语的**首个**匹配, 限定在 §C.2.4 区间内」的显式规则。

我独立实跑验证这不是理论风险, 而是**今日就已存在的真实碰撞**:

```
$ grep -nE '^  "[A-Za-z_]+":' aria/skills/phase-c-integrator/SKILL.md
267:  "verdict": "green" | "wait" | "fail",         ← §C.2.4 正确块 (7键: verdict/pr_ci_status/
268:  "pr_ci_status": ...                              in_flight_runs/primitive_used/
269:  "in_flight_runs": [...                           primitive_version_sha/raw_message/
272:  "primitive_used": ...                            path_coverage)
273:  "primitive_version_sha": ...
274:  "raw_message": ...
275:  "path_coverage": {...}
342:  "phase_c_integrator": {                        ← §C.2.4.X「Config schema example」jsonc 块 (第三个碰撞源)
504:  "verdict": "pass" | "warn" | "block" | "bypass",  ← §C.2.4.5「Submodule Pointer Regression Gate」的
505:  "affected_submodules": [                            **第二个** Output schema (JSON) 块
514:  "telemetry_files": {
```

用 Python 精确复算两种最自然的坏实现:

- **不加区间限定, 对全文件跑该正则** ⇒ 得键集合 `{affected_submodules, in_flight_runs, path_coverage, phase_c_integrator, pr_ci_status, primitive_used, primitive_version_sha, raw_message, telemetry_files, verdict}`, **计 10 个**, 永远不等于 `_build_output` 的 7/8 键 ⇒ **对任何实现 (含完全正确的 A 实现) 恒红**。
- **重现 SC-A-step 旧 bug 那种「取『**Output schema**』短语的末次匹配」** ⇒ 定位到 `:501` 起的块, 解析得键集合 `{verdict, affected_submodules, telemetry_files}`, **计 3 个**, 同样永远不等于 7/8 ⇒ **同样恒红**, 且与 A 在 `:279`/hunk② 的真实编辑是否正确**完全脱钩** —— 与本 Spec 自己反复引用的 `memory feedback_false_green_dual_is_permanent_red` 描述的恰是同一类失效 (该 memory 讲的是恒绿, 但文中自己在 SC-A-note 处已承认「恒红同样零信息」的对称形态)。

**这不是假设性风险**: 本 Spec §Impact hunk ① 明文要求在 `:238` 与 `:257` 之间 (即 json 块**之前**) 插入新执行流程步骤 —— 这会使当前引用的 `:265-277` 行号本身**在 A 自己的实现完成后就整体下移**, 届时唯一还能定位这个块的方式就是某种文本锚搜索, 而现文对这个搜索**没有给出任何排歧规则**。

**how_it_goes_red**: Phase B 实现者 (或写测试的人) 如果对着「实际解析」四个字, 用最直接的写法 (对整个 SKILL.md 跑正则, 或搜「Output schema」标题取其后第一个/最后一个 json 围栏) 编写 SC-A-doc 判据代码, 两种写法在我的独立实测中**都产出与 `_build_output` 实产键集合(7 或 8)不相等的结果**, 与 A 的 `.py`/`SKILL.md` hunk② 是否正确实现**无关**。这与本轮 (R4-fix) 刚刚为 SC-A-note 修复的缺陷是**同一个类** (memory `fix-the-class`: 上一轮诊断出「两个锚在全文件都不唯一」这个类, 却只推广到了它自己新改的那一条, 没有回头检查同一批「三处一一对应 hunk 的纯文件读取」类里的另一个成员)。我核对了 R1-R4 全部 audit-reports 及 aggregate (`grep -rln SC-A-doc .aria/audit-reports/`), **过去 20 个席位轮次里没有一次对 SC-A-doc 做过这个方向的检查** —— 都止步于验证「两条解析规则」本身 (json.loads 排除 / 两空格正则), 没有人问过「这个正则要在哪个区间内跑」。

**introduced_by_r4fix**: false (缺口自 R2 引入 SC-A-doc「两条解析规则」时就存在, R3/R4-fix 均未触碰; 但 R4-fix **同批**修好了它的直接兄弟 SC-A-note 的同款病, 却没有把这个类推广到 SC-A-doc, 属于本轮该做而未做的遗漏)。

---

## 3. Major — 「明确不修项均已逐条给理由」这个自我声明不实: 至少 6 条 R4 minor finding 被静默放弃, 全文件搜索零匹配

**locator**: `openspec/changes/premerge-gate-branch-existence/proposal.md:58` (本版方法论声明)
对照 commit `45c480a` message 段落「不修 15 条, 逐条给了理由」中「14 条 minor…分三类」一段。

**evidence**: 文档 `:58` 逐字承诺「本版明确拒绝修的项与理由, **逐条写在它们各自的位置**, 不集中成清单」。我全文件搜索 (`grep -n "R4.*不修\|不修.*R4\|本轮不修\|本轮不改\|如实说不修"`) 只命中**一处** (`:369`, 且只覆盖 `SC-A-step` 这一条 Major)。但 R4 五席原始 28 条里, 除去我在 §0 验证的 11 条已修 Major + 1 条 `SC-A-step` Major, **还剩 16 条 minor 中的至少 6 条**在正文里**没有任何痕迹**表明它们被看到过、考虑过、或决定不修 —— 我逐条独立验证如下, 每条都实跑命令确认「今日仍存在, 且无任何邻近文字提及」:

| # | R4 finding (来源席位, severity) | 独立验证今日状态 |
|---|---|---|
| a | `LEVEL_GUIDE.md:26` 曾错锚 (knowledge-manager, minor) | 这条**是**被修的 (与 §0 第 8 条同批) —— 不计入本清单, 仅作对照 |
| b | 「D.2 handoff」混用 phase-d-closer 的 D.2(归档)/D.3(session-handoff) 两个步骤 (knowledge-manager, minor) | `grep -n 'D\.2 handoff'` proposal.md = 4 处命中 (`:326`/`:332`/`:862`/`:973`), 全部原样保留「D.2 handoff」措辞, 零改动, 零邻近说明 |
| c | O-3/F-1/F-2/F-3「完成判据」列全部只答「是否获授权」不答「怎么验证做完」 (knowledge-manager, minor) | 独立读 `:857-860` 四行, 完成判据列均仍是「见文首 D-a」, 与 R4 复核时完全相同, 零改动 |
| d | 表 1「6 条正是 DEC §2 点名过户给 A 的号段」— DEC §2 实为 **7** 条 (含 SC-M10), Spec 数成 6 (tech-lead, minor) | 独立读 `DEC-20260812-001-premerge-gate-spec-split.md` §2 逐字「SC-M6·M7·M8·**M10**·M11·M13·M14」= 7 条; proposal.md `:316`/`:360` 仍写「6 条」「SC-M6/M13/M7/M8/M11/M14」, 零改动 |
| e | `:500`(现 `:575`) 声称「改英文不在本 Spec 授权范围内 (§非目标)」, 而 §非目标九条里实际没有这一条 (悬空引用) (tech-lead, minor) | 独立读全部 §非目标九条 (`:933`-`:951`), 逐条核对, 确无「docstring 语言」相关条目; `:575` 仍原样引用 |
| f | 表 2「方向 2 归纳」算术错: 「3 类+1 条+**14** 条=18」应为「4 条(打爆)+1 条(不可断言)+**13** 条(不受影响)=18」, 且 `SC-A-step` 被两处重复计入 (tech-lead **与** code-reviewer 两席独立命中, minor) | 独立按 Table 2 逐行重新分类: 打爆 = {A10,A10b,A10c,A-baseline}=4; 不可断言={A-step}=1; 不受影响={A-doc,A-note,A-cli,A-sc22}+9条同族=13。4+1+13=18, 与文中「其余 14 条」矛盾。`:363-367` 原句一字未改 |
| g | SC-A-note (d) 腿的 token `各早退分支(**…**)保持**…**六键不变` 里两个「…」未定义是通配还是字面, 与同条刚钉死的「抹空白」规则精度不对称 (code-reviewer, minor) | 独立读 `SKILL.md:279`(「…保持**六键不变**」)与 `pre_merge_gate.py:245-246`(「…保持**既有**六键不变」), 两者在 `re.sub(r'\s+','',…)` 抹空白后仍不同 (`保持六键不变` vs `保持既有六键不变`, 后者不含前者作为子串) —— 若「…」按字面理解, 该 token **在两个操作数上都零命中**, (a)(d) 两腿恒红; `grep -n '通配\|字面 U+2026'` proposal.md 全文件零命中, 无任何澄清 |

**7 条中 6 条 (b-g) 在正文里完全没有被提及**——既不在「已修」清单, 也不在唯一一处「明确不修」框 (`:369`, 只覆盖 SC-A-step)。这与 `:58` 承诺的「逐条写在它们各自的位置」以及 commit message 声称的「14 条 minor…分三类…统一理由」**不符**: 那段分类与理由**只存在于 git commit message 里, 不存在于被审对象 (`proposal.md`) 本身**。

**how_it_goes_red**: 任何只读 `proposal.md` (不去翻 git log) 复核本轮「未修项是否都有理由」的人, 会在 (b)-(g) 六处找不到任何解释, 无法区分「AI 看过并判断不值得改」与「AI 没看到就漏了」——这正是本 Spec 反复援引的规则 #10 精神 (AI 自作主张的流程判断必须留痕请复议) 在它自己身上的一次未完成实践。其中 (g) 直接落在我 qa 席位的核心职责 (SC 可证伪性) 内: 若「…」被字面实现, `SC-A-note` 的 (a)(d) 两腿会对**任何**实现 (含正确实现) 恒红, 是与本节 §2 SC-A-doc 发现同一类的、未被发觉的潜在恒红点; 若按合理的通配符读法实现则无问题——这正是 `spec-underdetermination` (两个独立实现者会得到相反结果的判据) 而非确定性缺陷, 我因此把它计入本条的**证据**而非单列一条 Major, 严重度上尊重 R4 code-reviewer 已给出的 minor 定级 (未见证据要求升级)。

**introduced_by_r4fix**: true — 这 6 条本身是 R4 轮 (对 R3-fix 的审计) 才产生的 finding, 在 R3-fix 版本里不存在对应问题需要处理; R4-fix **本应**处理或至少记录它们 (依其自己的方法论承诺), 却让它们无声消失, 这个「消失」是 R4-fix 这次提交造成的结果。

---

## 4. 引入率与执笔方预测的对照

执笔方可证伪预测: 总数 14–20 (点估 17)、Critical 0、Major 5–8、引入率 70–85%。

**本席 (qa-engineer) 单席独立发现**: 0 Critical + 2 Major (§2 SC-A-doc 锚点缺口 [非本轮引入, 但本轮未推广"fix-the-class"] + §3 静默弃用声明失实 [本轮引入的失实断言, 证据含 6 条本轮产生但未处理的 minor]) + 1 minor (对 §3 证据 g 项单独的严重度判断, 已并入 §3 未单列计数)。

由于本任务只由单席完成, 无法直接验证跨 5 席去重后的总数是否落在 14–20 区间, 也无法独立判定全局引入率 (需要其余四席的 raw findings 才能计算分母/分子)。但可以给出两个可验证的局部判断:

1. **「Critical=0」这半预测, 本席复核成立** —— 我没有找到任何 Critical 级发现 (SC-A-doc 锚点缺口虽是「恒红」类缺陷, 但它是**本轮该推广而未推广**的旧类缺口, 不是本轮新写文本直接产生的新逻辑错误, 且残余风险是「无从求值/恒红」而非「误判为 PASS 的假绿」, 与 Critical 通常保留给「危害方向是静默通过」的口径一致, 定为 Major 更准确)。
2. **「引入率不会因为本轮而降到很低」这半预测, 本席复核也成立, 但机制不同于预测者的假设** —— 预测者认为引入率高是因为「新写文本产生新缺口」(如 §2 类型); 本席实际找到的引入率的另一个来源是**未写文本也会产生开放缺口**——§3 揭示的 6 条静默放弃项, 它们不是「新写出的错」, 而是「该写的解释没写」造成的**已知问题保持开放**。这提示: 若 R6 仍然只统计「新增文字引入的新错」, 会系统性低估「声明的不修事项 vs 实际的不修事项」之间的落差, 而这个落差在本轮至少贡献了 6 个开放 finding (若算作 R5 报告的一部分, 会拉高「R4 findings 存活到 R5」的比例, 但严格说它们 introduced_by_r4fix=true, 因为让「已获得独立 finding 编号」这件事本身消失是 R4-fix 造成的效果)。

**给 owner 判断「是否继续加轮」的输入**: 本轮 (R5) 若五席汇总后的引入率仍然主要来自「新论证块产生新缺口」这类模式 (如本席发现的 §2), 而非「旧问题被真正带回来重新出现」, 则符合 owner 在 R4 裁定时的预期 ("每一轮 fix 的产出几乎全部是它自己制造的新条目" 的性质没有变化, 只是绝对数量可能下降)。但本轮新出现的「不修清单不完整、部分 minor 消失不留痕」这个模式 (§3) 是**新的失效模式**, 不完全等价于 R1-R4 已经出现过的「换一个量掩盖真相」或「同类只修一个实例」, 更接近「审计负担被隐性转嫁给下一轮 (下一轮必须重新发现这些 6 条, 因为它们没有 introduced_by_r3fix 之类的痕迹可以追溯)」——这本身构成了「加轮边际收益递减」判断的一个新变量, 建议 owner 在决定是否用完剩余 2 轮时纳入考虑。

---

## 5. SC 自足性总评 (本席核心职责)

**覆盖面**: 18 行 SC-A* (`grep -c '^| \*\*SC-A'` = 18) 各自对应 A 的行为/doc/元三类承诺, 与「可达前提」(11+2+3+2=18) 和「打桩边界表」(6+1+2+4+3+2=18) 两套独立分区**均独立复算确认配平, 互不矛盾, 无重无漏**。

**恒红/恒绿/空真扫描结果**:
- **新发现 1 处潜在恒红** (SC-A-doc, §2, Major) —— 若按最自然的方式实现 (无区间限定的正则搜索, 或取「Output schema」短语的末次匹配), 会对**任何**实现 (含完全正确的 A 实现) 产生与被测代码无关的固定错误结果。
- **1 处已知但未修的潜在恒红/欠定** (SC-A-note (a)(d) 的「…」token, §3 证据 g, minor 级) —— 若按字面理解, 同样会对任何实现恒红; 若按合理的通配读法, 则正常工作, 是 `spec-underdetermination` 而非确定性缺陷。
- **未发现新的空真** —— 三条负控 (SC-A10/A10b/A10c) 经本轮「precheck 必须返 (False,…)」例外补回后, 我独立核对其「assert ls-remote 未被调用」因果腿在三道早退位置 (`:328`/`:338`/`:345`, 均独立读源码确认行号准确) 各自成立, 能真实拒绝「核验插错位置」这类坏实现; SC-A11 (正控) 同样能拒绝「误判存在分支为不存在」这类坏实现; 均非空真。
- **未发现新的假绿** —— SC-A14 腿 2 (R3 已把判据从「进程出口 stdout」换成「`gate_check()` 返回值直接 encode」, 本轮我复核该判据依然与 harness 捕获模式结构无关, 无回退)。

**三条负控早退的拒绝能力**: 逐条独立验证 —— SC-A10 (`enabled=false`, `:328` 早退, 结构上与 backend 无关) / SC-A10b (`backend is None`, `:338` 早退, 须 mock `resolve_ci_backend` 返 `None`) / SC-A10c (`precheck` 失败, `:345` 早退, 须 mock backend 且 `precheck()` 返 `(False,…)`) —— 三者的 mock 配方与其断言的早退点一一对应, **今日均无矛盾** (R4 已修好 SC-A10c 的配方冲突)。三者均能拒绝「核验插入点错位」这一类坏实现: 若实现把核验插在早退**之前**, 对应负控的「assert ls-remote 未被调用」会失败并转红。

**打桩边界自洽**: 本轮我对文档侧全部三个「纯文件读取」SC (SC-A-doc / SC-A-step / SC-A-note) 做了统一的全文件重复锚点扫描 (任务书 item 4 明确要求), 结果: SC-A-step (R3 已修) 与 SC-A-note (R4 本轮已修) 均自洽; **SC-A-doc 未获得同等处理, 是本轮最有价值的新发现**。

---

## 结论

**verdict = PASS_WITH_WARNINGS** (0 Critical + 2 Major + 相关 minor 证据并入 Major 证据链)。

**vote = REVISE** —— 2 条 Major 均建议在 R6 (若 owner 选择再加轮) 或 D.2 前修复: (1) 给 SC-A-doc 补齐与 SC-A-step/SC-A-note 同款的「首个匹配 + 章节内 scoped」定位规则, 这是本 Spec 自己已经证明有效的模式, 修法成本低、收益高 (防止一个核心 doc↔code 一致性 SC 变成零信息的恒红判据); (2) 要么把 §3 列出的 6 条 R4 minor 逐条补上「本轮不修 + 理由」的邻近说明 (与已有的 `:369` SC-A-step 框同规格), 要么如实承认「本版仅对 blocks_phase_b 项和 1 条 Major 做了逐条说明, 其余 minor 未及处理」, 二者选一, 不留「声称完整但实际不完整」的落差。
