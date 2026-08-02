# post_spec R1 — qa-engineer (linked-issue-normalization)
**verdict**: REVISE
**scope_ok**: true
**counts**: critical=2 major=3 minor=1

> 方法: 所有行号均实读 (`proposal.md` / `lib/collision.py` / `lib/track_id.py` / `lib/claim_schema.py` / `tests/test_release_by_track.py`)。所有"怎么会红"均用可复跑代码验证——对现状生产函数 `linked_issue_overlaps` 直接跑 12 个 SC 场景 (baseline 红/绿实测), 并对 §What Changes 的四步归一算法写了一份逐字忠实实现, 再对 6 种候选实现 (1 正确 + 5 错误) × 12 场景做判别矩阵。探针脚本: `/tmp/claude-1000/-home-dev-Aria/622639d7-c716-4c28-9cb1-8679549e38e9/scratchpad/probe_{baseline,algorithm,matrix}.py`。零写入、零 commit。

---

## SC 逐条红窗表

| SC | 被测对象 | 怎么会红 | 判定 |
|----|---------|---------|------|
| **SC-1** | `linked_issue_overlaps` 比较谓词, 3 组两两配对 | 反例 `naive_wholestring`(整串 casefold + 取末尾 `/` 段, 不单独解析 `number`、不 strip `#` 前空格) 在 A-C/B-C 两对上失败 (矩阵实测)。**现状裸 `!=` 三对全部误判"不匹配"** (`aria-plugin#122` vs `10CG/aria-plugin#122` 等), 已用真实 `linked_issue_overlaps()` 实跑确认 | **baseline-red 已验证** (三对全红), 可红 |
| **SC-2** | 同上, 负控: 同 org 同号不同仓 | 反例 `number_only`(只比数字, 忽略 basename) 失败, 已实测。但**现状裸 `!=` 对本例已经输出"不匹配"**——两串本就不同, 与期望一致 | 可红 (对退化实现), **非 baseline-red**——与 rule6_note 声称矛盾, 见 CRITICAL-2 |
| **SC-3** | 同上, 正控: 两侧都有 org 且不同 | 反例 `org_when_both`("仅两侧都有 org 才比较 org") 失败, 已实测; 现状裸 `!=` 亦红 | **baseline-red 已验证**, 且**已核实是全 SC 表中唯一命中 `org_when_both` 反例的一条** (见"已核实成立"§1) |
| **SC-4** | 同上, number 按 int 比较 | 逐字实现 §What Changes 步骤 1-5 后测试: 若照字面裸 `#007`×`#7` (无 repo 限定词), 依步骤 3 "`repo_basename` 空 ⇒ 不可解析", 两值都判不可解析 ⇒ 退回原串比较 ⇒ **连 100% 合规的"正确实现"也判不匹配**, 与期望"命中"矛盾, 且与 SC-6 把同形状 `#5` / `10CG/#7` 判"不可解析"正面冲突。若隐含 repo 前缀 (如 `aria-plugin#007`): 反例 `naive_wholestring` 失败, 现状裸 `!=` 亦红 | 字面读法**不可满足** (CRITICAL-1); 宽容读法 baseline-red 已验证 |
| **SC-5** | 同上, basename 轴已知限 (截断型不归一) | 反例 `number_only` 失败; 但**现状裸 `!=` 对本例已经输出"不匹配"**——与期望一致 | 可红 (对退化实现), **非 baseline-red**——与 rule6_note 声称矛盾 |
| **SC-5b** | 同上, 分隔符型别名 (`.`/`_`/`-` 互换) | 反例 `naive_wholestring`(不做 `.`/`_`→`-` 翻译) 失败, 已实测; 现状裸 `!=` 三对全部误判"不匹配" | **baseline-red 已验证** (三对全红), 但 rule6_note 的"SC-1~6"与 Impact 表的"SC-1~8"两处枚举都未点名它 |
| **SC-6** | 同上, 不可解析值回落 | 反例 `unparseable⇒硬编码 False`(而非退回原串比较) 失败, 甚至连自反性都破 (同值比自己都不匹配)。但回落语义本身就是"精确字符串比较", **与现状裸 `!=`/`==` 在这类输入上行为恒等**——现状代码对 SC-6 全部构造场景已经是绿的 | 可红 (对特定错误实现), **非 baseline-red**——与 rule6_note 声称矛盾 |
| **SC-7** | 归一后比较谓词的**整体**代数性质 (自反/对称/传递) | 反例 `prefix_onedir`(单向前缀匹配) 失败, 22 处对称性违例 (已实测)。但**任何"算 key 再比较"形状的实现 (含现状裸 `!=`、含 `org_when_both`/`number_only` 等错误实现) 都自动满足三性质**——baseline 本身就是合法 (只是过细粒度) 的等价关系, 结构上不可能 baseline-red | 概念上可红 (窄, 仅对非对称/硬编码特例形态有效), 但**"语料全集"未定义, 不可执行/不可复现** (见 MAJOR-1) |
| **SC-8** | 签名+返回 schema (代码) / Phase B 路径行为 (执行期) | 签名/schema 半: 改参数序或返回字典键名即红, 可机械断言。行为半: 若新比较逻辑对某个 near-miss 输入产生错误的新结果, 但不触及任何既有测试用到的字面值, **不会**被现有 6 个既有测试捕捉到——它们全部用完全相同的字面串或与比较逻辑无关的分支 | 签名半可红且可执行; 行为半"无其他差异"这一全称命题**不能被现有测试证伪**, 只是被动通过, 判别力薄弱 (见 MAJOR-3) |

---

## Findings

### [CRITICAL] C1 — SC-4 字面读法 (裸 `#007`×`#7`) 不可满足, 且与 SC-6 对同形状值的分类正面矛盾

- **位置**: `openspec/changes/linked-issue-normalization/proposal.md:107` (SC-4) vs `:110` (SC-6) vs `:57` (§What Changes 步骤 3 "`repo_basename` 空 ⇒ 不可解析")

- **问题**: 我把步骤 1-5 逐字翻成 Python (无任何自由发挥), 对 SC-4 的字面例子 `#007` × `#7` 跑一遍: 两者按最后一个 `#` 拆分后 `left` 均为空串, 不含 `/`, 于是 `repo_basename = ""`——按步骤 3 明文"`repo_basename` 空 ⇒ 不可解析", 两值都是不可解析, 按步骤 4 退回原字符串精确比较, `"#007" != "#7"` ⇒ **不匹配**。而 SC-4 声称的期望是"**命中** (number 解析为 int)"。

  这不是"钉得不够细"的普通歧义, 而是**同一份文档内部的自相矛盾**: SC-6 (`:110`) 明确把 `#5` 与 `10CG/#7` 列为"不可解析值"的**范例**——两者与 SC-4 的 `#007`/`#7` 是**完全相同的形状** (裸 `#<数字>`, 或"org/" + 空 basename + `#<数字>`)。SC-6 说这个形状"不可解析", SC-4 说这个形状"解析为 int 后命中"——两条 SC 对同一输入形状给出了相反的分类。**没有任何单一、内部一致的分类规则能同时满足两者**: 要么放宽步骤 3 使空 basename 可解析 (则 SC-6 的 `#5`/`10CG/#7` 范例失效), 要么维持步骤 3 (则 SC-4 字面例子永远无法通过, 哪怕实现完全合规)。

  R3 (母 Spec 审计) 曾称"`collision.py` 改动核心逻辑可直接照写, 不需要实现者猜"(本提案 `:147` 引用), 但 SC-4 恰恰需要实现者"猜"一个未写明的隐含 repo 前缀才能避开这个矛盾——猜对了 (比如写成 `aria-plugin#007` × `aria-plugin#7`) 测试才有意义, 猜错了 (照字面写裸值) 会产生一个**任何合规实现都无法通过**的红色测试, Phase B 排查时容易被误诊为实现 bug。

- **证据** (可复跑, `probe_algorithm.py`):
  ```
  normalize('#007')    = ('unparseable', '#007')
  normalize('#7')      = ('unparseable', '#7')
  normalize('#5')      = ('unparseable', '#5')       # SC-6 范例, 判定一致
  normalize('10CG/#7') = ('unparseable', '10CG/#7')  # SC-6 范例, 判定一致
  compare('#007', '#7')                     = False   (SC-4 期望 True)  *** 矛盾 ***
  compare('aria-plugin#007', 'aria-plugin#7') = True  (SC-4 期望 True)  一致 (隐含 repo 前缀时)
  ```
  判别矩阵进一步显示: 在我测的 6 种实现里, **唯一能让 `#007`/`#7` 字面例子通过的是 `number_only`**(完全忽略 basename 的退化实现)——而 `number_only` 正是 SC-2 存在的目的就是要杀死的那个实现。也就是说, 若 SC-4 坚持字面裸值写法, SC-2 与 SC-4 变成**互斥的验收标准**, 没有实现能同时满足两者。

- **建议修法**: 把 SC-4 的例子改成与 SC-1/2/3/5/5b 同款、带显式 repo 限定词的形式, 如 `aria-plugin#007` × `aria-plugin#7` (或直接复用 SC-1 的 `aria-plugin`), 并在该行补一句"裸 `#N` (无 repo 限定词) 的形态由 SC-6 的不可解析回落规则管辖, 不属于本 SC"——把两条 SC 的管辖边界写清楚, 而不是留给字面语义去打架。

---

### [CRITICAL] C2 — rule6_note 声称"SC-1~6 均在现状代码上可红", 实测三条 (SC-2/SC-5/SC-6) 并不成立; 唯一符合却未被计入的 SC-5b 反而被漏列

- **位置**: `openspec/changes/linked-issue-normalization/proposal.md:94` ("substitute: SC 级 baseline-failing 结构化测试替代 (SC-1~6 均在现状代码上可红)") + `:96` ("substitute 须实证而非声称")

- **问题**: 我直接 import 生产代码 `aria/skills/state-scanner/lib/collision.py` 里现状 (未修复) 的 `linked_issue_overlaps()`, 对 SC-1~6 每一条的具体场景真实调用一遍 (非猜测、非读代码脑内模拟), 结果:

  | SC | 现状代码实际行为 | SC 期望行为 | 是否 baseline-red |
  |---|---|---|---|
  | SC-1 (3 对) | 三对全部"不匹配" | 三对全部"命中" | **是**, 三对全红 |
  | SC-2 | "不匹配" | "不得命中" | **否**——两者本就一致, 现状已绿 |
  | SC-3 | "不匹配" | "命中" | **是**, 红 |
  | SC-4 | "不匹配" | "命中" | **是**, 红 (但见 C1, 字面例子红是"永远红", 不是"修复后转绿"的红) |
  | SC-5 | "不匹配" | "不命中 (已知限)" | **否**——两者本就一致, 现状已绿 |
  | SC-6 (fallback 场景) | 精确字符串比较 | 精确字符串比较 (退回原串) | **否**——回落语义与现状裸 `!=` 在这类输入上行为恒等, 现状已绿 |

  即: rule6_note 点名的 6 条里, **只有 3 条 (SC-1/SC-3/SC-4) 是真正的 baseline-failing**; SC-2/SC-5/SC-6 这三条在现状 (未修复) 代码上**已经通过**, 原因是它们的期望结果 (负控"不得命中" / 已知限"不命中" / 回落"精确比较") 恰好与现状裸 `!=` 产生的结果重合——不是因为现状代码"对", 而是巧合式重合 (负控天然靠字符串不同来满足, 回落语义天然就是精确比较)。这三条测试仍有价值 (它们锁住修复后不应该退化的行为), 但**不能被称为"baseline-failing"**, 用它们支撑"substitute 是可证伪的、不是摆设"这个论证站不住脚。

  这与本 Spec 自己在 §Why 里点名的失败形状 (`feedback_completion_signals_vs_runtime_invocation`——"所有表面信号都是绿的") 是**同一种病灶**, 只是这次发生在 Rule #6 合规论证本身而不是产品代码里: 一句"SC-1~6 均可红"的断言, 一半是真的、一半没有对现状代码实跑验证就写了下来。而 `:96` 的框定合规条款明确要求"substitute 须实证而非声称"——这条要求应该也约束提案文本自己写下的判断, 不能只约束 Phase B。

  另外, **SC-5b (`:109`) 经实测确实是 baseline-red** (三对全部误判不匹配), 完全符合"baseline-failing"的定义, 但 rule6_note 的"SC-1~6"与 Impact 表 (`:132`) 的"SC-1~8"两处枚举都没有把它单独点名——是无害的遗漏 (漏掉一条真正成立的, 不是漏报一条不成立的), 但既然 SC-5b 是本轮唯一带 ⭐ 强调"必须加"的新增条款, 枚举里却看不到它的编号, 建议一并补上。

- **证据** (可复跑, `probe_baseline.py`, 直接调用生产 `linked_issue_overlaps`):
  ```
  SC-2: own='10CG/Aria#147' other='10CG/aria-plugin#147' actual_matched=False sc_expects_match=False
        => baseline already matches expectation (GREEN, not a red-window)
  SC-5: own='10CG/aria-orch#5' other='10CG/aria-orchestrator#5' actual_matched=False sc_expects_match=False
        => baseline already matches expectation (GREEN, not a red-window)
  SC-6 same-unparseable-value: own='no-hash-here' other='no-hash-here' actual_matched=True sc_expects_match=True
        => baseline already matches expectation (GREEN, not a red-window)
  SC-5b dot-vs-dash: own='10CG/10cg.local#20' other='10CG/10cg-local#20' actual_matched=False sc_expects_match=True
        => BASELINE-RED (differs from expectation)
  ```

- **建议修法**: 不需要推翻 substitute 路径本身 (SC-1/SC-3/SC-4-修正后/SC-5b 四条已足以撑起"非摆设"的论证), 只需把 `:94` 的括注改写成诚实的版本, 例如:「SC-1/SC-3/SC-4/SC-5b 在现状代码上可红 (已实测); SC-2/SC-5/SC-6 是负控/已知限/回落语义的正确性锁, 现状代码上本就为绿, 其价值在于防止修复引入回归, 不在于揭露现状 bug」。这个改写本身不影响 Rule #6 substitute 判据表第一行的适用性, 只是把论证从"声称"换成"实证", 与 `:96` 自己要求的标准一致。

---

### [MAJOR] M1 — SC-7"语料全集"未定义; 唯一先例未入库且不可复现; 结构上无法区分 baseline 与目标实现

- **位置**: `openspec/changes/linked-issue-normalization/proposal.md:111` (SC-7) vs `:87`/`:146` (D1 引用"R2 已用 18 元语料穷举验证")

- **问题**: 三层递进问题。

  **(a) 语料全集是什么, 全文没有定义。** SC-7 只写"对语料全集断言", 未指向任何具体文件、fixture 或生成规则。唯一的历史先例是 D1 引用的"R2 18 元语料"——我去查了, 那次验证的探针脚本明确记在 R2 报告的"复现方式"一节 (`.aria/audit-reports/post_spec-R2-1785660000000-a1-entry-claim-duplicate-work-guard-type-design-analyzer.md:312`): "本轮 4 个只读探针脚本…位于 `/tmp/claude-1000/…/scratchpad/probe{1,2,3,4}.py`"——**scratchpad 目录, 从未提交进仓库**, 现在已经不存在。也就是说, D1 拿来证明"良定义等价关系"的那份具体语料, 本身就是一次性、不可复现的产物, Phase B 没有任何东西可以直接复用。

  **(b) 若语料全集指真实 `refs/aria/coordination` ref, 它是持续变化的共享资源, 不适合做确定性回归断言。** 我在三个不同时间点看到三个不同的数字: 本 proposal `:75`("13 条已有记录原样有效") 及 `:29-33`(三族表 4+9+0=13) 说"13 条"; R2 报告 (`post_spec-R2-…type-design-analyzer.md:191`) 说"25 条 claim / 15 条带 linked_issue"; 我刚才 (审计当下) 直接查询该 ref 得到 **27 条 claim / 16 条带 linked_issue**。三个数字互不相同, 因为这是一个所有 Lab 容器都在持续写入的活 ref。若 SC-7 的测试直接读这个 ref, 测试结果会随其他会话的并发写入而漂移——这是一个会本仓 CI/回归套件里制造 flaky test 的典型模式, 与"结构化测试替代 AB benchmark"要求的确定性、可复现性直接冲突。

  **(c) 更根本的问题: 即使语料全集确定下来, SC-7 对区分"现状 bug"与"已修复"的判别力也很弱。** 我验证了: 任何"先算一个 key、再比较 key 相等"形状的实现——不管这个 key 算得对不对——都会自动满足自反/对称/传递三条性质 (这是等价关系的数学结构决定的, 不是算法设计得好)。现状裸 `!=` 本身也是"key = 原字符串, 比较相等"这种形状, 所以**它自己也是一个合法的 (只是分类粒度过细的) 等价关系, 三性质零违例**。我用同一份语料重新验证: `org_when_both`(R2/M1 点名的错误实现)、`number_only`(SC-2 要杀的退化实现)、`naive_wholestring`(不完整的归一实现) 全部零违例; 唯一被 SC-7 抓到的只有故意设计的单向前缀匹配 (22 处对称性违例)。也就是说 SC-7 能抓到的错误类型很窄 (基本只有"非 key-based"的病态实现), 抓不到本提案实际关心的那些错误 (org 处理方式错、basename 处理方式错)——那些错误由 SC-1~SC-6/SC-8 覆盖, SC-7 在这个 Spec 里增量价值有限。

- **证据** (可复跑, `probe_matrix.py` 与直接查询):
  ```
  git ls-tree -r refs/aria/coordination --name-only | grep claims/ | wc -l   → 27  (今天)
  ... | grep linked_issue: | wc -l                                          → 16  (今天)
  # 对照: proposal.md 记 13 条; R2 报告记 25 条 / 15 条 —— 三个时间点三个数字

  baseline (裸 !=)        : reflexive=True symmetric_violations=0 transitive_violations=0
  org_when_both (错误实现) : reflexive=True symmetric_violations=0 transitive_violations=0
  number_only (错误实现)   : reflexive=True symmetric_violations=0 transitive_violations=0
  naive_wholestring (错误) : reflexive=True symmetric_violations=0 transitive_violations=0
  prefix_onedir (错误实现) : reflexive=True symmetric_violations=22 transitive_violations=0   ← 唯一被抓到的
  ```

- **建议修法**: 在 tasks 拆分阶段把"语料全集"改成一个**提交进测试文件的、有限的、手工维护的固定 fixture** (例如直接复用 SC-1~SC-6/SC-5b 各场景涉及的全部字符串, 去重后跑穷举 permutation), 显式声明"这是代表性样本, 不是穷举所有字符串, 也不读取任何共享 git ref"; 同时把 SC-7 的定位从"主力验收标准"降格为"防非对称/防硬编码特例的辅助夹具", 避免它在 Rule #6 substitute 的证据链里被过度倚重。

---

### [MAJOR] M2 — `.`/`_` 之外的分隔符替换 (如误按空格代替连字符) 既不被 SC-5 覆盖也不被 SC-5b 覆盖, 且未像 D4 那样被显式记为已知限

- **位置**: `openspec/changes/linked-issue-normalization/proposal.md:58` (S5 归一表: 只翻译 `.` 与 `_`) 对照 `:108`(SC-5) / `:109`(SC-5b) / `:69-71`(D4 已知限声明) / `aria/skills/state-scanner/lib/track_id.py:28`

- **问题**: 提案把别名分成两类并声称"两者的处置不同, SC 须分开钉": 分隔符型 (`.`/`_`/`-` 互换, SC-5b 能归一) vs 截断型 (`aria-orch` vs `aria-orchestrator`, SC-5 不能归一, 且 D4 把这条**显式写成已知限**)。但归一规则本身 (`:58`) 只对 `.` 和 `_` 两个字符做翻译——这个选择是有道理的 (对齐 `derive_track_id` 的 `_SUBSTITUTION_TABLE = str.maketrans({"/": "-", ".": "-", "_": "-"})`, `track_id.py:28`), 但它的**后果**没有被说清楚: 任何其他字符被用作分隔符替代——最现实的是**空格误代连字符** (`linked_issue` 是自由文本 CLI 参数, 不是受 Forgejo 命名规则约束的仓名, 打错一个字符完全可能) ——既不会被 casefold 修好, 也不会被这张 `.`/`_` 翻译表修好, 会静默落进"不匹配"的结果, 表现得像截断型别名, 但它本质上既不是"截断"也不是 SC-5b 声称已覆盖的"分隔符型"。

  这是一个**没写下来的第三类**, 恰好卡在 SC-5 和 SC-5b 中间: 概念上它属于"分隔符替换"家族 (体感上应该能归一), 实际行为上却和"截断型"一样静默失配, 而 D4 只字面点名了"basename 别名"一种已知限, 没有覆盖"分隔符字符集选择过窄"这一种。

  我检索了 `openspec/` + `docs/` 全量 prose, **没有找到空格代替连字符或其他非 `.`/`_` 分隔符的真实实例**——这点上我如实报告证据强度不如 `10cg.local` (S5 自己找到的、有 11 个 open issue 的真实反例) 那么硬。但我认为不能因此把这条判成"不用管": `linked_issue` 与仓名不同, 是自由文本, prose 语料 (受过润色的书面记录) 天然不会保留敲键盘的手误; 而本提案自己在 `:60` 刚刚指出"R3 判 `.`/`_` 场景为 dormant, 结果 S5 穷举时发现真实反例", 用的正是"检索不到 ≠ 不会发生"这个论证——同一把尺子理应同样适用于这里。

- **证据**:
  ```
  compare('10CG/10cg local#20', '10CG/10cg-local#20') = False   # 空格误代连字符, 不匹配
  compare('10CG/10cg.local#20', '10CG/10cg-local#20') = True    # 对照: 点号, 按 SC-5b 规则命中
  grep -rhoE 分隔符变体 openspec/ docs/  →  零命中 (与 10cg.local 的"11 个 open issue"实据不同量级)
  ```

- **建议修法**: 二选一, 与"危害=未言明的静默残余缺口"方向一致: (a) 把归一表的翻译字符集从 `{.  _}` 扩到"任意非字母数字分隔符" (含空格、`+` 等), 但需重新评估是否与 `derive_track_id` 的翻译表脱节 (母 Spec R2 audit M4 点名过的"两套归一不组合"问题, 扩得比 `derive_track_id` 宽会重新引入那个问题); (b) 若维持现状 (只对齐 `derive_track_id` 的三字符), 在 D4 或 SC-5 旁边加一句**明确声明**"分隔符归一仅限 `.`/`_`, 其他分隔符替代 (含空格误植) 未覆盖, 按 basename 精确匹配的已知限处理"——把这条隐藏在算法选择背后的残余缺口显式化, 不要让 SC-5/SC-5b 的"两类"措辞暗示"分隔符问题已全部解决"。

---

### [MAJOR] M3 — SC-8"Phase B 路径行为除原漏报现能报外无差异"这半不可被机械证伪; 唯一操作化路径 (既有 6 个测试) 未被点名, 且这 6 个测试对"新比较逻辑是否误配"零判别力

- **位置**: `openspec/changes/linked-issue-normalization/proposal.md:112` (SC-8) vs `aria/skills/state-scanner/tests/test_release_by_track.py:206-247` (`TestLinkedIssueOverlaps`, 4 个 lib 层测试) + `:527-576` (`TestPhase1GateLinkedIssueCli`, 2 个 CLI 层测试)

- **问题**: SC-8 把两种性质不同的断言写进同一行:
  1. "签名与返回 schema 逐字段不变"——这是**代码结构断言**, 用 `inspect.signature()` 比对参数列表、用返回 dict 的 key 集合比对字段名即可机械核实, 无歧义。
  2. "Phase B 路径行为除『原漏报现能报』外无差异"——这是一个**全称行为断言** ("除了这个特定改变, 其余全部行为都不变"), 数学上等价于要求穷举验证所有输入下新旧实现的输出相同 (只在归一确实改变判定的那些输入上除外)。这类全称命题无法被"测试通过"直接证明, 只能退化为"现有的回归测试集合仍然全部通过"这种代理断言。

  我去找了这个代理断言实际能覆盖到什么: 全仓 `linked_issue_overlaps` 的既有测试只有 6 个 (`test_same_issue_different_track_flagged` / `test_same_track_not_flagged` / `test_terminal_and_no_issue_ignored` / `test_none_own_issue_short_circuits` 4 个 lib 层, 加 `test_linked_issue_written_and_overlap_surfaced` / `test_no_linked_issue_no_overlap_key` 2 个 CLI 层)。逐一读过之后发现: **这 6 个测试在"匹配"这一侧全部使用完全相同的字面字符串** (如 `"A#7"` 对 `"A#7"`, `"10CG/Aria#160"` 对 `"10CG/Aria#160"`), 在"不匹配"这一侧全部靠 status/None 过滤或 track_id 排他分支, 跟 `linked_issue` 比较谓词本身完全无关。**没有一个测试用到"格式不同但语义相同"或"格式相同但语义不同"的 near-miss 输入。** 这意味着: 新比较逻辑无论对着 basename、org、number 三个维度如何误配 (只要不影响这 6 个测试用到的那些恒等字符串对), 这 6 个测试**原样通过, 不会报警**。SC-8 若只靠这 6 个测试撑腰, "无其他差异"这句话事实上验证的范围极窄, 真正的判别力全部压在 SC-1~SC-7 身上, SC-8 自己贡献的是"没有破坏无关分支"而不是"新逻辑没有引入误配"。

- **证据**: 见位置引用的源码; 6 个测试的匹配对字面比对如下 (均为逐字相同):
  ```
  test_same_issue_different_track_flagged: linked="A#7"  vs own_linked_issue="A#7"        (逐字相同)
  test_linked_issue_written_and_overlap_surfaced: linked="10CG/Aria#160" vs "10CG/Aria#160" (逐字相同)
  ```

- **建议修法**: Impact 表 (`:132`) 里把这 6 个既有测试逐个点名为 SC-8 的操作化宿主 (而不是笼统写"既有宿主"), 并在 SC-8 这一行补一句诚实的范围声明: "『无其他差异』通过既有 6 个测试保持绿来代理验证, 这些测试仅覆盖恒等字符串场景与比较逻辑无关的过滤分支; 归一逻辑本身是否误配由 SC-1~SC-7 独立把关, 不依赖本条"。这不要求新增测试, 只要求把 SC-8 实际能证明什么、不能证明什么写清楚。

---

### [MINOR] m1 — SC 表未言明配对双方须使用不同 `track_id`; 若 Phase B fixture 疏忽复用同一 track_id, 断言会在错误分支上恒真

- **位置**: `aria/skills/state-scanner/lib/collision.py:217-220` (先比较 `linked_issue`, 再判断 `track_id == own_track_id` 时 `continue`) vs `proposal.md:104-109` (SC-1/SC-3/SC-4/SC-5/SC-5b 均只给出两个 `linked_issue` 字符串, 未提及 track_id)

- **问题**: `linked_issue_overlaps` 的判定顺序是: 状态过滤 → `linked_issue` 非空过滤 → `linked_issue` 相等比较 → **`track_id` 与 `own_track_id` 相同则排除** (`:219-220`, 注释"same-name collision — reconcile's job, not ours")。SC 表的每一对例子只给了两个 `linked_issue` 字面值, 完全没有提示实现者两侧 claim 该用什么 `track_id`。如果 Phase B 写 fixture 时图省事把两侧 track_id 写成一样的 (比如都叫 `"t1"`, 复制粘贴时最容易犯), `:219` 的排他分支会先于 `linked_issue` 比较逻辑生效, 使函数**恒返回空列表**——测试断言"不命中"时会望文生义地"通过", 但这次通过与被测的归一逻辑毫无关系, 是命中了错误的分支 (本项目 memory `feedback_test_asserts_what_its_name_claims` 点名的同一形状: 测试名/声称验证的 ≠ 它真验证的)。

  这不是本提案独有的新问题 (`:219` 是既有代码), 且现有 `TestLinkedIssueOverlaps` 类已经用"mine"/"theirs" 这种明显不同的 track_id 命名规避了它, 是一个良好先例。但 SC 表本身没有把这条隐性前提写下来, 纯粹依赖 Phase B 实现者自己发现既有测试的命名习惯。

- **证据**: `collision.py:217` `if c.linked_issue != own_linked_issue: continue`; `:219-220` `if c.track_id == own_track_id: continue  # same-name collision — reconcile's job, not ours`。我在 `probe_baseline.py` 里为避免踩这个坑, 特意把两侧 track_id 固定为不同的 `"mine"`/`"theirs"`——这是审计脚本自己需要主动规避的细节, 而不是从 SC 表文字里读出来的。

- **建议修法**: 在 SC 表旁边 (或 tasks 拆分阶段的测试实现说明里) 补一句"每对配对示例默认两侧 `track_id` 不同 (仿现有 `TestLinkedIssueOverlaps` 的 mine/theirs 命名), 避免 `:219` 的同名排他分支抢先生效"。

---

## 已核实成立的部分 (Phase B 可直接采信, 不必重审)

1. **SC-3 确系全表唯一能区分"org 不参与匹配"与"两侧都有 org 才比较 org"两种实现的用例** —— 我逐条核对了 SC-1/SC-2/SC-4/SC-5/SC-5b/SC-6/SC-7/SC-8 全部 8+1 条, 用一个真实实现 `org_when_both`(仅两侧都有 org 时才比较 org) 去跑全部场景, 只有 SC-3 判它不合格, 其余全部通过 (SC-1 的三对里没有"双方都有 org 且不同"的组合; SC-2/SC-5 由 basename 差异本身就否决, 与 org 策略无关; SC-5b/SC-4/SC-6/SC-7/SC-8 的例子里 org 要么缺失要么两侧相同)。R2/M1 与本提案的"唯一"论断成立, 非自我复述式声称。
2. **§What Changes 四步归一算法的核心等价关系设计是良定义的** —— 我用忠实实现在自己构造的语料上重新验证了自反/对称/传递零违例, 与 R2 的结论independent 吻合。传递性论证 ("可解析/不可解析两个子集不可能跨类相等") 站得住。
3. **D1 关于 `#007 ≡ #7` 应按 int 而非字符串比较的裁决本身是对的**——这条修正了母 Spec R2 audit m2 点名的旧歧义, 只是新例子 (SC-4) 的具体写法引入了一个新的、不同的问题 (见 CRITICAL-1), 不代表 int-比较这个设计决策错了。
4. **SC-6 四个不可解析范例 (`no-hash-here` / `repo#abc` / `#5` / `10CG/#7`) 相互之间及与算法规则的一致性良好**——除了与 SC-4 的字面冲突外, 这四个例子本身各自都被步骤 1-3 正确分类为不可解析, 不抛异常。

---

## 复现方式

3 个只读探针脚本 (纯函数 + 一次只读 `git ls-tree`/`git show` 查询 `refs/aria/coordination`, 零写入) 位于
`/tmp/claude-1000/-home-dev-Aria/622639d7-c716-4c28-9cb1-8679549e38e9/scratchpad/probe_{baseline,algorithm,matrix}.py`。
运行前置: `sys.path.insert(0, "/home/dev/Aria/aria/skills/state-scanner")` (仅 `probe_baseline.py` 需要, 用于 import 生产 `ClaimRecord`/`linked_issue_overlaps`)。

**AI 不预判下一轮裁决。**
