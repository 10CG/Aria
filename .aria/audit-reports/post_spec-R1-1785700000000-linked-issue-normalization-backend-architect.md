# post_spec R1 — backend-architect (linked-issue-normalization)

**verdict**: REVISE
**scope_ok**: true
**counts**: critical=1 major=2 minor=2

> **方法**: 全部引用行号实读 `openspec/changes/linked-issue-normalization/proposal.md` (工作树版, 160 行)、`aria/skills/state-scanner/lib/collision.py`、`lib/track_id.py`、`scripts/phase1_gate.py`。核心行为断言均用按 Spec 五步规则逐字写出的参考实现实跑验证 (脚本见文末「复现方式」), 并对生产 `linked_issue_overlaps` 跑基线核实 Rule #6 substitute 前提。零写入、零 commit。

## Findings

### [CRITICAL] 规则 2 的自证例句与规则 3 直接互斥, 且该矛盾原样复制进 SC-4 vs SC-6 —— 两条 SC 按字面互不可满足

- **位置**: `proposal.md:56` (规则 2, "`故 #007 ≡ #7`") vs `:57` (规则 3, "`repo_basename` 空 ⇒ 不可解析") vs `:107` (SC-4) vs `:110` (SC-6)

- **问题**: 规则 2 用括注 `(故 #007 ≡ #7)` 把「`#007`」「`#7`」当作**已确定可解析且应相等**的例子, 但这两个字面串在「`#`」之前**什么都没有** —— 按规则 3「取最后一段为 `repo_basename`…`repo_basename` 空 ⇒ 不可解析」, `left=""` ⇒ `repo_basename=""` ⇒ **这两个值本身就是不可解析的**, 应退回规则 4「原字符串精确比较」, 而 `"#007" != "#7"` (原串不同) ⇒ **不命中**。

  这个矛盾原样复制进了 SC 表: **SC-4** 断言 `#007` × `#7` 必须「命中」, 而 **SC-6** 把结构完全相同的「裸 `#<数字>`, 前面无仓名」的例子 (`#5`) 列为**不可解析值**的正式测试用例之一。`#007`、`#7`、`#5` 三者是**同一种形态** (空 `left`), SC 表却给了相反的分类: SC-4 要求这类值参与「number 解析为 int」的归一并命中, SC-6 要求这类值整体退回原串比较。

  这不是可以靠「实现者自行选择一种解释」化解的歧义 (Q1 问的「实现者会分叉的地方」的最强形态) —— 它是**同一份文档、同一个函数、结构相同的输入被要求满足两个互斥的行为**, 没有任何单一实现能同时通过 SC-4 与 SC-6。Phase B 实现者若照 SC 表逐条写 baseline-failing 测试 (本 Spec rule6_note 承诺的 substitute 路径), 会在写测试阶段当场卡住, 只能自行拍板一个未经 owner 裁决的解释 —— 这正是 Rule #10 要防的「AI 临场判断」。

- **证据** (按五步规则逐字实现的参考实现, 含 S5, 见文末脚本 `probe_normalize.py`):
  ```
  normalize_key('#007') -> ('RAW', '#007')      # left='' -> repo_basename 空 -> 不可解析 (规则3)
  normalize_key('#7')   -> ('RAW', '#7')         # 同上
  normalize_key('#5')   -> ('RAW', '#5')         # SC-6 自己的例子, 同一形态

  matches('#007', '#7')  = False   # 退回原串比较: "#007" != "#7"
  # 但 SC-4 表格要求: matches('#007','#7') 必须为 True ("命中")
  ⇒ SC-4 与「五步规则字面执行」矛盾; 且与 SC-6 对同形态输入的分类矛盾。
  ```
  完整运行:
  ```
  $ python3 probe_normalize.py
  ...
  **MISMATCH** SC-4 (#007 vs #7)  matches('#007','#7') = False  (expected True)
  ```
  （其余全部 SC 用例 —— SC-1/2/3/5/5b —— 均与 Spec 期望一致, 只有 SC-4 按字面规则不可满足。）

  旁证: 这个例子在母 Spec `a1-entry-claim-duplicate-work-guard/proposal.md:236` 的原始语境下是「SC-4: `#007` 与 `#7` 派生**同一 track-id**」—— 那里的输入前提是「已知合法的 `<basename>-<number>` issue 派生串」, `basename` 非空是隐含前提。抽出到本 Spec、复用同一对裸串测试 `linked_issue_overlaps` 本身时, 这个隐含前提 (非空 basename) 未被重新核对, 撞上了本 Spec 自己新写的 SC-6 (裸 `#N` 是规范化的不可解析反例)。**这正是本 Spec 自陈「post_spec 应聚焦抽出过程是否引入偏差」这句话点名的那类问题。**

- **建议修法**: SC-4 的两个例子改成带仓名的形式 (如 `aria-plugin#007` × `aria-plugin#7`), 使其落在「可解析」分支并单纯测试「number 按 int 而非字符串比较」这一件事, 不再触碰空 `repo_basename` 分支。同时规则 2 的括注例句同步换成带仓名的例子, 避免规则 2 自己给出一个被规则 3 推翻的例证。

---

### [MAJOR] S5「为什么必须加」的必要性论证引用的是母 Spec 已排除机制的碰撞场景, 在本 Spec 实际改动的代码路径里不存在对应的双层归一

- **位置**: `proposal.md:59` (「为什么必须加」) + `:109` SC-5b 「怎么会红」列的 "(与 `derive_track_id` 对齐)" + `:69` (极性段 "`repo_basename` 用**精确相等**") vs `:122-123` (非目标: 「不引入 track-id 形态变更 (母 Spec 范围, R3 判其有碰撞域风险)」) vs `.aria/spikes/2026-08-02-S2-S4-S5-S6-batch.md` (S5 spike 原始产出) + `.aria/spikes/2026-08-02-S3-track-id-derivation.md` (S3, S5 引用的「track-id 派生」定案)

- **问题**: `:59` 的论证是「既有 `derive_track_id` 已经把 `/`.`_` 全译成 `-`。若本 Spec 只做 casefold, **两层归一不一致** —— `10cg.local#20` 与 `10cg-local#20` 在**本 Spec 判不同仓**, 却在 `derive_track_id` 后**塌成同一 track_id**」。

  这段话描述的「塌成同一 track_id」场景, 前提是有人把 `linked_issue` 的 `<basename>-<number>` 送进 `derive_track_id` 生成 track_id —— 这**正是母 Spec `a1-entry-claim-duplicate-work-guard` §1 的「issue 派生 track-id」机制** (S5 spike 文档自己写明: 该场景取自「**S3 定案形态**」, 即 `.aria/spikes/2026-08-02-S3-track-id-derivation.md` 里母 Spec 专属的 `<归一后 basename>-<number>-<container_uuid>` 派生规则)。

  而**本 Spec 的非目标 (`:123`) 明确排除了这个机制**:「不引入 track-id 形态变更 (母 Spec 范围, R3 判其有碰撞域风险)」。全仓 grep 确认 `derive_track_id` 只在 `--raw-track-id` (session/carry-id 命名) 一条数据流上被调用, `collision.py` 从未 import 它, `linked_issue_overlaps` 的两个字符串参数 (`own_linked_issue` / `c.linked_issue`) 从未流向 `derive_track_id`。⇒ **在本 Spec 实际改动、实际会上线的代码里, "两层归一" 根本不存在共享输入, "塌成同一 track_id" 这句话所描述的缺陷不可能发生。**

  这不影响 SC-5b 本身的正确性 (它只断言 `linked_issue_overlaps` 内部的匹配行为, 与 `derive_track_id` 无关) —— 但它是「审计资产继承」框架下应该被本轮抓住的**抽出偏差**: S5 spike 是为母 Spec (issue 派生 track-id 机制) 做的碰撞穷举, 其结论与证据被逐字搬进子 Spec, 支撑的却是子 Spec 里一个不存在对应机制的论点。子 Spec 自己在 `:61` 也写了一条独立、真正适用的理由 (「副作用是正收益: 修好同仓两种拼写别名的一个真实子集」) —— 但这条被排在「且这不是理论风险」之后、作为附带收益, 而不是主论证, 导致「为什么必须加」读起来像在防一个活跃的双层不一致 bug, 实际防的东西不存在。

  连带问题: `:69` 极性段紧接在 S5 之后仍无条件断言「`repo_basename` 用**精确相等**」——但 S5 已经让 `repo_basename` 比较在 `.`/`_`/`-` 这一维上不是精确相等 (SC-5b 要求三者互相命中)。两处对同一件事 (`repo_basename` 比较是否精确) 给出不一致描述, 单读 `:69` 会得到错误的心智模型。`:109` SC-5b「怎么会红」列的 "(与 `derive_track_id` 对齐)" 也重复了同一个不成立的论证, 且严格来说连字面对齐都不完整: `derive_track_id` 用 `.lower()`、S5 用 `.casefold()` (两者仅在极少数 Unicode 字符上不同, 对仓名场景无害但称"对齐"不够精确), `derive_track_id` 还有 64 字符截断与非 ASCII/超长时的 sha256 兜底, S5 均未复刻——这些差异在本 Spec 无害 (因为压根不共享输入), 但恰好印证"对齐"不是准确的论证框架。

- **证据**:
  ```
  $ grep -rn "derive_track_id" aria/skills/state-scanner/ --include="*.py" | grep -v __pycache__
  # 命中: track_id.py 定义 + claim_lifecycle.py / worktree_manager.py / release_gate.py / phase1_gate.py
  #       全部消费 raw_track_id / carry-id, collision.py 零命中, linked_issue 零命中
  ```
  ```
  $ grep -n "derive_track_id\|import" aria/skills/state-scanner/lib/collision.py | head -3
  40:from __future__ import annotations
  45:from .claim_schema import ClaimRecord
  46:from .reconcile import reconcile_all
  # 无 track_id 相关 import
  ```
  `.aria/spikes/2026-08-02-S2-S4-S5-S6-batch.md:95` 明写 S5 场景基于 "**S3 定案形态**" (`<归一后 basename>-<number>-<container_uuid>` 派生 track_id) —— 该形态即母 Spec §1, 本 Spec 非目标 `:123` 已排除。
  Forgejo API 实测 (核实 S5 的另一半事实性主张, 该部分属实): `10CG/10cg.local` 确为真实仓 (`full_name: "10CG/10cg.local"`, `open_issues_count: 11`); 但 `10CG/10cg-local`、`10CG/10cg_local` 均 **404** (不存在), 即 S5 的 separator-fold 目前不会把两个**不同**真实仓误判为同一仓 (无当下副作用, 但这是运气而非设计保证——Spec 未提及若未来 `10cg-local` 被注册为独立仓时该如何处理)。

- **建议修法**: 把 `:59-61` 改写为以 `:61` 的独立理由为主论证 ("`.`/`_`/`-` 互换是同仓拼写变体, 折叠它们代价低且已用 Forgejo API 核实当前无跨仓误判"), 明确标注 derive_track_id 对齐**目前不适用** (本 Spec 未触碰该数据流), 仅作为「若母 Spec §1 未来复活, 这条修法会同时受益」的前瞻性注脚, 不作为必要性依据。同步更新 `:69` 极性段, 加一句「`repo_basename` 比较对 `.`/`_`/`-` 三种分隔符不敏感 (S5), 除此之外精确相等」, 并把 `:109` 的 "(与 `derive_track_id` 对齐)" 改为 "(折叠分隔符别名, 独立于 track-id 机制)"。

---

### [MAJOR] SC-8「Phase B 路径行为除原漏报现能报外无差异」是散文级描述, 未落成可机械核验的谓词

- **位置**: `proposal.md:79` (D6 「签名与返回 schema 不变」) + `:112` (SC-8) vs `aria/skills/state-scanner/scripts/phase1_gate.py:1229-1237` (唯一生产调用点)

- **问题**: SC-8 实际打包了两件事:
  1. **签名/schema 不变** —— 可直接机械断言, 且本仓已有先例 (`test_phase1_gate_telemetry.py:134` 用 `inspect.signature(g.run_gate).parameters` 冻结签名契约)。返回 dict 的键集合 (`track_id/owner/container/session/status/linked_issue/claimed_at`, `collision.py:222-230`) 同理可用 `set(d.keys())` 逐条断言。
  2. **「Phase B 路径行为除『原漏报现能报』外无差异」** —— 这句话字面上是一个行为对比 (旧实现 vs 新实现在**任意**输入上的差异应恰好是「旧返回 `[]` 处新可能非空」), 但 SC 表没有把它转成一个可以对语料跑的谓词。「无差异」的反面 (新实现在旧实现**已经命中**的地方变得不命中, 或者字段值变化) 不会被现有 SC-1~7 的逐点断言捕获到, 因为那些都是「新增命中」方向的正例, 没有「存量命中不能丢」方向的负控。

     这正是本项目 memory `feedback_falsifiable_evidence_for_binary_acceptance` 点名的形状: 验收条件写成叙述性判断, AI/实现者只能自己「觉得像」, 审计者事后也无法机械复核「真的无差异」是否成立。

- **证据**: 对既有 4 个单测 (`test_release_by_track.py:224-247`) 重放, 确认它们全部使用无分隔符/无大小写差异的简单 token (`"A#7"` / `"B#8"`), 因此**现有测试集合本身不构成「新旧行为一致」的负控** —— 新旧实现在这 4 个用例上恰好都给出相同结果, 不是因为 SC-8 钉住了这件事, 而是因为这些具体输入没有触发归一逻辑的任何分支:
  ```
  $ python3 -c "
  import sys; sys.path.insert(0, 'aria/skills/state-scanner')
  from lib.collision import linked_issue_overlaps
  from lib.claim_schema import ClaimRecord
  c = ClaimRecord(schema_version='1', track_id='theirs', owner='o', container='c',
                  session='s', phase='B', status='active',
                  claimed_at='t', heartbeat_at='t', linked_issue='A#7')
  print(linked_issue_overlaps([c], 'mine', 'A#7'))
  "
  [{'track_id': 'theirs', 'owner': 'o', 'container': 'c', 'session': 's', 'status': 'active', 'linked_issue': 'A#7', 'claimed_at': 't'}]
  ```
  （旧实现按裸 `!=` 已经命中, 新实现按归一键比较结果相同 —— 这是「巧合覆盖」而不是「设计覆盖」, 因为 `A#7` 里没有任何字符会被 casefold/分隔符折叠改变。）

- **建议修法**: 把 SC-8 拆成两条可机械断言的子项:
  - **SC-8a (签名/schema 冻结)**: `inspect.signature(linked_issue_overlaps).parameters` 与实现前快照逐字段相等; 返回的每个 dict 的 `set(keys())` 恒等于 7 字段集合。
  - **SC-8b (单调性/无回归)**: 对一个覆盖三族 + SC-5/5b/6 的语料集合, 断言 **旧实现判定「命中」的每一对, 新实现必然也判定「命中」**(旧结果 ⊆ 新结果, 只增不减)。这是一个可以直接对语料跑 `all(old_match(a,b) <= new_match(a,b) for a,b in corpus_pairs)` 的谓词, 比散文「无差异」更强也更可判。

---

### [MINOR] 规则 3 只对 `left` 做尾部空白剥离, `number_str` 侧的空白处理未写明, 实现选择 (`int()` 宽容 vs `isdigit()`/`isdecimal()` 严格) 会静默分叉, 且无 SC 覆盖

- **位置**: `proposal.md:56` (规则 2, "必须能解析为非负整数") + `:57` (规则 3, "`left` 剥尾部空白") — 母 Spec `post_spec-R2` 的 m2 (`.aria/audit-reports/post_spec-R2-1785660000000-a1-entry-claim-duplicate-work-guard-type-design-analyzer.md:246-259`) 已指出同一空白不对称问题, 但只有「str vs int 比较」半条 (规则 2 的 "解析为 `int` 后比较") 被本 Spec 吸收, 空白不对称半条未被吸收/未留痕

- **问题**: 规则 3 明确说「`left` 剥尾部空白 (处置 C 族)」, 但对 `number_str` (`#` 右侧) 只字未提是否要 strip。若实现者用 `number_str.strip().isdecimal()` 之类的**严格前置校验**, `"repo# 122"` (`#` 后有空格) 的 `number_str=" 122"` 会因含空白被判不可解析; 若实现者直接 `int(number_str)` (Python 的 `int()` 自动容忍首尾空白), 同一输入会被判可解析且等于 122。两种实现都满足 SC-6 的「不抛异常」要求, 结果却不同, 而 SC 表没有任何用例覆盖这个位置的空白。

- **证据**:
  ```
  >>> int(" 122")
  122
  >>> " 122".isdigit()
  False
  # 二者对同一个 number_str 给出相反的"可解析"判定, Spec 未择一
  ```
  用本审计的参考实现 (选了 `int()` 宽容路线) 实测: `matches('repo#122', 'repo# 122')` = `True`; 换成 `isdigit()` 前置校验会得到 `False`。两个都是「字面规则」的合理实现, 结果相反。

- **建议修法**: 规则 3 补一句「`number_str` 同样剥两侧空白后再判定」, 与 `left` 对称; 且明确指定判定函数 (建议: `strip()` 后 `str.isdecimal()`, 再 `int()` 转换 —— 避免 `int()` 对 `"+7"` 之类符号串的隐式接受), 从而把「怎样算能解析为非负整数」钉到不需要实现者选择的地步。SC-6 可加一例 `"repo# 122"` 固定选定行为。

---

### [MINOR] 规则 1 未显式覆盖「整串不含 `#`」的情形, 需实现者从 SC-6 反推

- **位置**: `proposal.md:55` (规则 1, "按最后一个 `#` 拆为 `left` / `number_str`") vs `:110` (SC-6 的 `no-hash-here` 例子)

- **问题**: 规则 1 假设输入总能按「最后一个 `#`」拆成两段, 但没有说明**没有 `#`** 时 `left`/`number_str` 该怎么取值。实现者要么在 SC-6 逼出这个分支前不会意识到需要单独处理 (`str.rsplit("#", 1)` 在无 `#` 时只返回单元素列表, 直接拆包会抛异常, 与 SC-6「不抛异常」矛盾), 要么侥幸用「返回值长度是否为 2」这类隐式判断蒙对。这是可以被 SC-6 测出来并纠正的分叉点 (故列 MINOR 而非 CRITICAL), 但既然规则宣称「钉到字符级」, 该分支不应该留给实现者反推。

- **证据**: `"no-hash-here".rsplit("#", 1)` → `['no-hash-here']` (长度 1, 不是规则 1 隐含的 2 段), 直接 `left, number_str = s.rsplit(...)` 会 `ValueError: not enough values to unpack`, 与 SC-6「不抛异常」直接冲突; 必须显式先判 `"#" in s`。

- **建议修法**: 规则 1 末尾加一句「若整串不含 `#`, 整体视为不可解析 (进入规则 4)」, 使五步描述自洽, 不依赖 SC-6 反推。

---

## 已核实成立、下轮无需重审的部分

- **D1 等价关系声明, 加入 S5 后重新穷举依然成立**: 用严格按五步字面规则 (含 S5) 写的参考实现, 对一个 18 元语料 (三族 + SC-1~SC-6 全部例子 + S5 分隔符变体) 做 `permutations` 级穷举, 自反 / 对称 / 传递**零违例**。数学上这也符合预期——「按值计算一个 key、用 key 相等定义等价」在 key 计算是纯函数的前提下必然是等价关系, 不依赖具体 key 计算逻辑是否含 S5——但既然被问到, 已实测重新确认, 结论与 R2 一致, 未被 S5 破坏。
- **不可解析/可解析的论域划分在 S5 之后依然干净**: S5 的翻译只发生在 `repo_basename` 非空之后 (即已经落入「可解析」分支内部), 且字符替换不改变字符串「是否为空」这一属性, 因此不会把一个不可解析的原始输入变成可解析、反之亦然; 跨分支比较的「原串完全相同 ⇒ 可解析性必然相同」论证不受 S5 影响。
- **`/` 的作用域差异 (derive_track_id 还译 `/`) 对本 Spec 无实际影响**: `repo_basename` 由「按最后一个 `/` 切分取最后一段」构造而来, 按构造不可能再含 `/`；含 `/` 的部分 (`org`) 按规则 5 本就不参与匹配。二者作用域差异不产生意外行为（但如 MAJOR finding 所述，"为什么要对齐" 这个大前提本身站不住）。
- **`phase1_gate.py:1232` 生产调用点零改动**: 实读确认调用为 `linked_issue_overlaps(claims, result.track_id, args.linked_issue)` 三个位置参数, 本 Spec 只改函数内部比较谓词, 不touch 签名/返回 schema, 该调用点字面不需要任何修改。
- **Rule #6 substitute 的「baseline-failing」前提对现状代码属实**: 对当前未修改的 `collision.py` 实跑 SC-1/SC-3/SC-4/SC-5b 对应的输入对, 全部返回 `[]` (漏报), 与 Spec「SC-1~6 均在现状代码上可红」的断言一致。

## 复现方式

参考实现与全部穷举/断言脚本: `/tmp/claude-1000/-home-dev-Aria/622639d7-c716-4c28-9cb1-8679549e38e9/scratchpad/probe_normalize.py` (纯函数, 无副作用, 可直接 `python3` 运行复现全部证据; 未写入仓库任何文件)。基线核实的一次性命令见上方各 finding 的「证据」块。

**AI 不预判裁决。**
