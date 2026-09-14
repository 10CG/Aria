---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
drift_terminated: false
drift_check_skipped: false
drift_warning: false
is_refocus: false
verdict: PASS
timestamp: 2026-09-14T13:20:32.000Z
context: openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md
agents: [qa-engineer]
---

# post_spec Round 4 — qa-engineer 席

> 被审 SHA `e822829` (rework v4)。对照: 本席 R3 报告 (1 major + 2 minor) 与 R3 聚合报告。方法: 在临时目录 (`/tmp/claude-1000/-home-dev-Aria/e91a9d6a-05ff-4b26-af79-8d903c21a292/scratchpad/r4-qa/`) 用 python 从 proposal.md 逐字提取 D1-D6 文本 (非手抄, 消除转录风险), 落地一份「正确落地」模拟副本, 实现 SC-1/2/3/5/7/9/10 的字面判定, 对真实基线产物 (RESULT.md v4、`v5-mildcreep-opus5/*.json`、`PREREGISTRATION.md`) 做独立重算与溯源核对。全程只读仓库, 未编辑任何仓库内文件。

## R3 对账

| # | R3 严重度/摘要 | v4 状态 | 依据 |
|---|---|---|---|
| 1 | major — 地板守卫对「自然措辞扩张」的敏感度仍是零经验证据, OQ-8 推荐路径是不补跑, 该义务将带着未验证掐点直接生效 | **closed** | **(a) 预登记溯源**: `v5-mildcreep-opus5/PREREGISTRATION.md` 与三臂产出 (`mildcreep.json`/`new.json`/`negctrl.json`/`run.log`) 同一个提交 (`e822829`) 落盘, git 历史层面不能独立证明先后顺序; `stat` 核实这 5 个文件在工作区的 mtime 完全相同 (`2026-09-14 12:57:34`, 到微秒), 是 `git commit` 落盘时刻, 不是真实写入时刻, **文件系统证据对时序中立, 不能单独佐证「跑前写定」**。转向内容证据: PREREGISTRATION.md 全文不含任何具体结果数字 (不写「0/10」这类会暴露事后知情的字面), 只写了**对称的两分支判读规则**——「至少一条 should-not ≥0.5 ⇒ 敏感」与「0 条 ⇒ 局限的实证确认, 不是守卫失效」——这种双支路都先给出解释、不偏向单一结论的结构, 是事前预登记的典型特征 (事后编造通常会写成单向断言); run.log 内部时间戳 (三臂 `12:28:13Z` 同时起, `12:43–12:47Z` 陆续止) 与 run_arms_v5.sh 描述的「三臂同批 `&…&…&wait`」并行执行方式吻合, 无内部矛盾。**结论: 内容层面自洽支持「跑前写定」, 但这是一致性推断而非密码学/时间戳级的独立证明**——已作为限度写入下方观察, 不影响本条 major 的收关判断 (该判断不依赖预登记本身是否被伪造, 而依赖下面 (b)(c) 两点)。<br><br>**(b) 独立重算**: 用 python 重新解析三份原始 json (不是转抄 RESULT.md 的数字), 得 `new`: should-trigger 10/10、should-not 0/10、`summary.passed=20/20`; `negctrl`: should-trigger 0/10 (即 ≤5/10 门槛下的「命中数」)、should-not 0/10；`mildcreep`: should-trigger 10/10、should-not **0/10**。三项均与 RESULT.md v4 §v5 表格逐字一致, 且与 PREREGISTRATION 写定的两条前提 (`new` 须过门、`negctrl` ≤5/10) 相符——三臂数据本身有效, 可解读 mildcreep。<br><br>**(c) 判读站得住吗 + 承诺是否收窄到与证据一致**: mildcreep 命中「0 条 should-not ≥0.5」这一预先定义好的分支, 对应判读「局限的实证确认, 不是守卫失效」。这个判读的逻辑基础是: 守卫的契约 (D2「只承诺已验证的两类破坏」) 本来就没有承诺覆盖套件之外的近似误触, mildcreep 命中的正是「套件没有覆盖到的扩张方向」这一支, 不违反守卫对**已验证两类**破坏 (删词/强制过宽) 的既有保证 (v1-v4 数据仍显示这两类破坏能被抓到)。核对三条 major 判据门槛后, 均未越线: 不会让执行者做错事 (D2/D6 已明确「一次自然措辞扩张实测不判红」, 未过度承诺)、不使任何 SC 不可执行 (见下 SC 实测记录)、无事实不成立 (v5 数字复算吻合)。这与 R2→R3 那次「披露到位≠风险清零」的降级理由不同: 那次是「只成文, 零新增证据」, 这次是**拿到了真实的、可证伪的实证数据**(两分支预先都有解释, 且 mildcreep 确实可能落进「至少一条触发」那支, 不是稳赢的设计), 且 D2/D6 已把承诺相应收窄、OQ-8 按 Rule #10 给出带代价的推荐, 走的是本项目一贯认可的正规升级路径。**判closed**。残留的「已知有缺口但当批 T4 若执行会原样搬入」张力记入下方观察 (不足以够回 major 门槛, 见 Findings 说明)。 |
| 2 | minor — SC-2 未显式限定"仅第三列", 整行裸反引号扫描会把 D3 第 6 行「机读实证」列的通配路径模板误判为待核验路径 | **closed** | v4 SC-2 逐字新增「**只取每行第三列(『机读实证』列)** 的反引号路径」「第二列(前置)里的反引号串...不参与判定」, 并直接点名本席 R3 举的那个例子 (产物落点模板 ``aria-plugin-benchmarks/ab-results/<date>-<skill>-trigger/``)。本轮在临时副本重新实现「整行裸扫描」(`sc_checks.sc2_naive_wholerow`) 与「只取第三列」两版, 对同一份正确落地文本跑: 前者误判红 (命中 `.claude/`/`name: helper`/`claude -p`/`result`/`openspec-archive`/第 6 行占位串等 6 处假阳性, 比 R3 发现的范围还大), 后者全绿——证实 v3 的漏洞是真实的, v4 的显式列限定切实堵住了它。另做「防真空」双重测试: 整节 (标题+表) 被替换为完全不含 `### 场景 4b` 字样的占位文本时判红 (不会因搜不到而真空通过); 表格 0 行时判红; 单独删一行使总行数=5 时判红 (见 SC 实测记录扰动 5)。 |
| 3 | minor — SC-10 按小节整体扫描, 若只删掉 D2 判据正文里的 `--num-workers 1`, D3 前置表第 1 行的同一字符串会造成假阴性 (漏判) | **closed** | v4 SC-10 改「**按行判, 不按小节判**」, 逐字点名本席这条反事实并把机制写死: 只检查含「参数钉死」的**那一行**是否同时含 4 个参数串与「20 条」。本轮复现 R3 的原始反事实 (只删「参数钉死」行内的 `` `--num-workers 1` (D3 第 1 条), `` 子串, D3 表第 1 行原样保留): v3 判据下会漏判 (R3 已证), v4 判据下**正确转红**, 且未牵连其余 SC-1/2/3/5/7/9 (逐一跑过, 无collateral)。另做 SC-10 双条件独立性测试: 只删 SOT 边界注句 (`description hunk 不走本节`)、保留参数行不动, SC-10 单独因这一子条件转红, 证实这条判据的两个必要条件(行内容 + SOT 边界注)彼此独立起作用, 不是一个条件掩盖另一个。 |

**closed**: 3 条 (#1 #2 #3) · **partially closed**: 0 条 · **open**: 0 条

## Findings

无。本席 R3 的 1 major + 2 minor 全部 closed (证据见上表); 本轮对 SC-1/2/3/5/7/9/10 的字面可执行性 + 六项指定反事实 (删「不得 ship」/ 删参数行 `--num-workers 1` / 删「两套编号」句 / 写入比较判据句 / 删一行前置表 / 「边界四条」写回「边界三条」) 全部命中预期且无交叉误判 (见「SC 实测记录」); 独立重算 v5 三臂原始 json 与 Fisher 精确值, 未发现新的不可证伪或统计口径问题; 未发现新的 critical / major; 未发现「不改就不能进 Phase B」的 minor。两点非阻塞的残留观察见下节 (均未达 major/blocking-minor 门槛, 理由见各条末尾)。

## 观察

- **D2 新增覆盖要求与 T4/SC-4 的时序张力 (非阻塞)**: D2 新句「should-not 的近似误触须覆盖该 skill 最可能被扩到的相邻任务」字面上适用于所有套件, 但 T4 (把 `trigger-eval-openspec-archive.json` 搬进 `ab-suite/trigger/`) 受 SC-4 约束须与基线**逐字节同一**, 不含 v5 才发现的「整理收尾材料」类近似误触。也就是说, 若 OQ-3 之后 T4 真的执行, 第一份进入生产的套件本身就带着刚被证实存在的盲区, 而 D5.2/D5.3 两张新 issue 都不承接「给 openspec-archive 套件补这一类近似误触」这件具体事——只有 OQ-8「备选」提了一句, 且不是推荐项。**未计入 Findings 的理由**: (1) T4 当前默认路径是「OQ-3 裁定前不执行」, 这张张力在本 cycle 很可能根本不会落地; (2) D2/D6 已经诚实披露这个具体缺口 (v5 数字点名), 没有误导执行者的风险; (3) `ab-suite/` 本身允许日后升版补测, 结构上不是"一次定终身"。建议(不阻塞): OQ-3 裁定为执行 T4 时, owner 顺手确认是否要把「整理收尾材料」这一条 should-not 近似误触补进 openspec-archive 套件 v2, 否则 D2 那句新要求对这份套件会一直是具文。
- **D2「多加『相关文档 / 整理项目收尾材料 / 收尾整理』」的短语枚举比实际测试少列一项**: 用 `difflib` 比对 `run_arms_v5.sh` 里 `new` 与 `mildcreep` 两个 description 字面, 实际新增了 4 处: 「与相关文档」「整理项目收尾材料」「整理归档文档」「收尾整理」。RESULT.md v4 的 v5 表格与结论 2 都完整列出 4 项, 但 proposal.md D2 正文只写了 3 项 (漏「整理归档文档」)。不影响任何 SC (无 SC 逐字核对这个枚举), 也不改变「守卫判不出这一幅度扩张」的定性结论, 纯属复述精度问题, 建议下次改 proposal.md 时把 D2 这句补成 4 项、与 RESULT.md 对齐。
- **统计口径自查 (未发现问题, 记录复核过程)**: 重新核对 RESULT.md「统计」表 query 级 `new vs negctrl (8/3)` 标注的 `p = 0.0031`, 独立算得两侧 Fisher exact = 0.0030960 (四舍五入一致); 而 D2 判据用的「10 对 5」「10 对 6」是**单侧** (`alternative='greater'`) 检验, 算得 0.016254 / 0.043344, 与 proposal 的 0.016 / 0.043 一致。两处用的是不同方向假设的检验 (「统计」表答"两版是否有差异", D2 门槛答"负控是否显著低于某上界"), 各自标注了「双侧」/「单侧」, 没有混用或误标, 不构成新引入的统计口径问题。
- **v5 换模型可比性表述核查 (未发现问题)**: RESULT.md 与 proposal.md 在提到 `claude-opus-5` 数字时反复加了「只做臂间比较, 不与 v1–v4 数字直接比」「模型不同不直接比, 但方向与…一致」这类限定语, 没有发现把 opus-5 与 fable-5-1 的数字直接放进同一显著性检验或直接相减比较的地方; 表述恰当。
- **D5.4 独立核对 (未发现问题)**: 独立读取 `run_eval.py` 源码 (`/home/dev/.claude/plugins/cache/claude-plugins-official/skill-creator/bb335391eb83/skills/skill-creator/scripts/run_eval.py` 第 52/54/65/66 行), 确认 v4 的更正——技能名泄漏点是「命令文件名 `{skill_name}-skill-{unique_id}.md`」与「正文标题 `# {skill_name}`」两处, 首句 `This skill handles: {skill_description}` 嵌入的是 description 而非技能名——与源码逐行相符。这是其他席 R3 的 major (backend-architect #5), 不计入本席 R3 对账, 但作为本轮「新引入问题」排查的一部分独立复核, 结果是修正准确, 未发现新问题。
- CLAUDE.md / SOT / 手册现状仍是改前原句 (Tasks 未打勾, 符合预期: 本 Spec 仍是 Draft, 尚未执行落地任务); 本轮反事实验证全部基于临时副本模拟, 不代表已落地。

## Verdict

PASS — 0 critical / 0 major / 0 minor。

## Vote

PASS

## SC 实测记录

**方法**: 临时目录 `/tmp/claude-1000/-home-dev-Aria/e91a9d6a-05ff-4b26-af79-8d903c21a292/scratchpad/r4-qa/`。`extract.py` 用 python 从 proposal.md 按锚点字符串切片提取 D1 表 3 行 (old/new 句对)、D2/D3/D4/D6 整段全文, 避免手抄转录误差。`build.py` 读取仓库里真实的 `CLAUDE.md`(截取 Rule #6 段落, 与 R3 先例一致)、`standards/conventions/skill-benchmark-exemption.md`、`aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` 三份现状文件, 对每处「旧句」先 `assert count==1` 再替换, landing 出 `CLAUDE.correct.excerpt.md` / `skill-benchmark-exemption.correct.md` / `AB_TEST_OPERATIONS.correct.md` 三份「正确落地」模拟副本 (§场景 4 拆 4a/4b、D2 判据+D3 前置表写入 4b、SOT 新增 §4.1、SOT §6 计数语与第三条、版本号 1.1.0)。`sc_checks.py` 按 proposal v4 字面实现 SC-1/2/3/5/7/9/10 的判定函数 (SC-5 用 python `re`, 不用 grep, 遵照 proposal 原文对 ugrep 复杂度限制的说明)。`perturb_and_test.py`/`extra_checks.py`/`extra_checks2.py` 做扰动与补充穿透测试。

### 0. 前置事实核验 (D1 三处「逐字」声明)

```
CLAUDE.md  旧句命中次数: 1
SOT        旧句命中次数: 1
handbook   旧句命中次数: 1
```
与 proposal.md「2026-09-14 `grep -F` 各命中 1 次」的声明一致 (独立验证, 非转抄)。

### 1. 正确落地 → SC-1/2/3/5/7/9/10 全绿

```
PASS SC-1  {'CLAUDE': 1, 'SOT': 1, 'HB': 1}
PASS SC-2  {'n_rows': 6, 'config_derive_rows': 1}
PASS SC-3  {'decision_table_row': 2, 'description_changed': 2, 'scenario1': 2, 'scenario4b': 5, 'negctrl': 1}
PASS SC-5  {'body_hits': [], 'has_exclusion_phrase': True, 'landing_detail': {'CLAUDE': 0, 'SOT': 0, 'HB': 0}}
PASS SC-7  {'三个已知缺陷': 1, '两个已知缺陷': 0, 'version_1_1_0': 1, '边界四条': 1, '边界三条': 0}
PASS SC-9  {'le_5_10': 1, 'continuous_2': 1, 'not_ship': 2}
PASS SC-10 {'missing_in_param_line': [], 'sot_boundary_note_count_ok': True}
```

对照组 FAIL SC-2(naive-buggy) (整行裸反引号扫描, 不按第三列): 命中 6 处假阳性 `[('1','.claude/'), ('2','name: helper'), ('3','claude -p'), ('3','result'), ('3','openspec-archive'), ('6','aria-plugin-benchmarks/ab-results/<date>-<skill>-trigger/')]` —— 证实 R3 发现的问题真实存在, 且比当时报告的范围更大 (不止第 6 行一处); v4 显式限定第三列后此对照组转绿。

### 2. 六项指定反事实 → 对应 SC 是否转红 (逐项 diff, 检查是否牵连其余 SC)

| 扰动 | 操作 | 目标 SC 转红 | 是否只影响目标 SC |
|---|---|---|---|
| 删「不得 ship」 | 全文删除该子串 (命中 2 处一并删) | SC-9: True→False | 是, 仅 SC-9 翻转 |
| 删 `--num-workers 1` 于参数钉死行 | 只删「参数钉死」那一行内的 `` `--num-workers 1` (D3 第 1 条), `` 子串, D3 表第 1 行原样保留 | SC-10: True→False | 是, 仅 SC-10 翻转 (R3 minor #3 的原始反例, 现正确判红) |
| 删「两套编号」句 | 删 SOT §4.1 内含「两套编号不同轴」的整句 | SC-3: True→False | 是, 仅 SC-3 翻转 |
| 写入一句比较判据 | 在 4b 判据前插入「新版触发率不低于旧版时视为改进。」(不含排除词) | SC-5: True→False | 是, 仅 SC-5 翻转 |
| 删一行前置表 | 删 D3 第 3 行 (`claude -p` 加 `--setting-sources project`) | SC-2: True→False | 是, 仅 SC-2 翻转 (行数=5≠6) |
| 「边界四条」写回「边界三条」 | 手册计数语还原 | SC-7: True→False | 是, 仅 SC-7 翻转 |

六项全部命中预期目标 SC 且零交叉误伤, 说明 7 条 SC 的判据边界彼此正交。

### 3. 补充穿透测试

```
SC-2 防真空 A (整节含标题彻底不存在, 非"标题存在但改了后半截"): sc2 -> False {'reason': 'no ### 场景 4b section'}
SC-2 防真空 B (标题存在, 表格 0 行): sc2 -> False {'reason': 'row count != 6 (or 0, vacuous-guard)', 'n': 0}
SC-10 双条件独立性 (只删 SOT 边界注, 参数行不动): sc10 -> False {'missing_in_param_line': [], 'sot_boundary_note_count_ok': False}
  同一份文件上 SC-3 未被此删除牵连: sc3 -> True (两套编号句与边界注句是不同句子)
SC-5 正则自测:
  正样本1「新版触发率不低于旧版时视为改进。」-> 命中 1
  正样本2「被评 description 的触发率 >= 旧 description 才算通过。」-> 命中 1
  负控门槛行「须 ≤ 5/10」(算子不在正则的比较符集合里) -> 命中 0
  排除词行本身「不设比较判据 (如新版触发率不低于旧版)...」孤立测试命中 1 (因此必须先按行剔除再统计, 验证了 SC-5「先去掉含不设比较判据的行, 再统计」这一步骤的必要性, 不是冗余步骤)
SC-3 反事实 (对现行未改 SOT 文件): decision_table_row/description_changed/scenario1/scenario4b/negctrl 全部命中 0, 与 proposal 声明一致
```

### 4. v5 三臂原始数据独立重算 (不转抄 RESULT.md, 直接解析 json)

```
new:       should-trigger query级 10/10, should-not query级 0/10, summary.passed=20/20
negctrl:   should-trigger query级 0/10 (即负控门槛 ≤5/10 项), should-not query级 0/10, summary.passed=10/20(10 条应触发未触发标记 fail, 属预期设计)
mildcreep: should-trigger query级 10/10, should-not query级 0/10 (四条最可能误触 query 全部 0/3), summary.passed=20/20
```

三项与 RESULT.md v4 §v5 表格逐字一致; 与 PREREGISTRATION.md 写定的前提 (`new` 过门 / `negctrl` ≤5/10) 相符, mildcreep 落进预先定义好的「门通过」分支。

### 5. Fisher exact 独立复算

```python
fisher_exact([[10,0],[5,5]], alternative='greater')  # -> 0.016254  (D2 声称 0.016, 精确)
fisher_exact([[10,0],[6,4]], alternative='greater')  # -> 0.043344  (D2 声称 0.043, 精确)
fisher_exact([[10,0],[3,7]], alternative='greater')  # -> 0.001548  (单侧, 供参照)
fisher_exact([[10,0],[3,7]], alternative='two-sided')# -> 0.003096  (双侧, 与 RESULT「统计」表 p=0.0031 一致; 与上一行是不同检验方向, 未误用)
```

### 6. 落盘脚本 (仅供复核, 未改动仓库)

`extract.py` / `build.py` / `sc_checks.py` / `perturb_and_test.py` / `extra_checks.py` / `extra_checks2.py`, 均在 `/tmp/claude-1000/-home-dev-Aria/e91a9d6a-05ff-4b26-af79-8d903c21a292/scratchpad/r4-qa/`。
