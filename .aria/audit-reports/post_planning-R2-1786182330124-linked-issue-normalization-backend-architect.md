---
checkpoint: post_planning
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-08T09:45:30.000Z
context: openspec/changes/linked-issue-normalization/detailed-tasks.yaml
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R2 — backend-architect 审计报告

## 审计对象与方法

对比 R1 (`a52ab81`, 17 任务) 与 R1-fix (`3fc6f3f`, 21 任务)。逐条重读我自己 R1 的 1 Major + 3 minor
是否真闭合(读实际文本, 不读 commit message 自陈), 并对「实现类任务与路径真实性」这一轴做地毯式核验:
`git ls-tree` 核 gitlink/tree 类型、逐条 deliverables 路径 `[ -e ]` 存在性、`diff` 核 `aria/VERSION`
与主仓 `VERSION` 非别名、Python 脚本重建 DAG (无环/无悬空/同文件全有序)、逐条实读 9 处 file:line 引用、
实读 `.aria/repro/sc-baseline-linked-issue-normalization.py` 全文核证 `:277` 机制、经 Forgejo API 独立
核验 aria-plugin#133 评论确已落地。

---

## Part 1 — 我 R1 四条闭合核验

### Major (TASK-009 依赖 007 未依赖 008; TASK-009/010 同文件跨 agent 无边) — **CLOSED**

实读当前 yaml: `TASK-007.dependencies=[001,002,003,004,005]` → `TASK-008.dependencies=[007]` →
`TASK-009.dependencies=[008]` → `TASK-010.dependencies=[009], agent=backend-architect`。四任务的
`deliverables` 全部是 `lib/collision.py`, 依赖字段构成一条无分叉直链 007→008→009→010, 且 TASK-010
的 `agent` 字段已从 `knowledge-manager` 改为 `backend-architect`——与该文件另外三个任务同 owner。

**机械复核**(自写脚本, 只读): 用 `detailed-tasks.yaml` 重建全部 21 节点的依赖图, 断言 (a) 无环
(拓扑排序成功, 21/21 全部出现在序列里); (b) 每个共享同一 `deliverables` 路径的任务对, 其一必须是
另一个的祖先(可达)。跑遍 `collision.py`(007/008/009/010) 与 `test_release_by_track.py`
(001/002/003/004/005/006) 两组共享文件, **零个"UNORDERED PAIR"输出**——不存在任何未定序的同文件对。
`metadata.file_domain_serialization` 块对两条链的文字描述("007→008→009→010 全链串行"/
"001→002→003→004→005 串行; 006 另在 007 之后")与实际 `dependencies` 字段逐条吻合(006 虽不直接依赖
005, 但通过 006→007→{001..005} 的传递闭包保证 005 必先于 006 完成, 无并行风险, 不是缺陷)。

**判定: closed, 且用独立机械核验非仅读字段。**

### minor (TASK-008 绿名单漏 SC-11) — **CLOSED, 集合精确核验**

现有列表 12 条: `SC-1/1b/2/3/4/5/5b/5c/11/13/14/15`。对照 proposal.md 的 baseline 表(`性质`/`✅❌`两列)
逐条核算这 12 条是否恰是"经归一比较谓词(TASK-008 wiring)即可判定、不需要 TASK-009 的解析守卫"这一集合:

- 12 条全部是"主判据(跨族/切分点/casefold/number 相等)"或"负控/已知限"类, 对应的是**比较键构造**是否正确
  (basename 归一 + int 比较), 不涉及**畸形输入的异常隔离**。
- 17 条 SC 里剩下的 5 条 `{SC-6, SC-6b, SC-9, SC-10, SC-12}` 分别正确落在别处: SC-6/6b/10 是"回落语义
  /边界负控/护栏"——测的正是 D7 那批解析守卫(TASK-009 专属); SC-9 是 baseline-GREEN 的原串回显, `:228`
  未被 TASK-008/009 任一任务改动, 不需要任何 TG-2 任务重新钉它; SC-12 是导出契约, 由 TASK-006/007 承担。
- 12 + 5 = 17, **无遗漏、无重复计入、无跨任务错配**。

**判定: closed。**

### minor (D7 `isascii()/isdigit()` 谓词未逐字点名) — **CLOSED(见下方新发现 B 的标签瑕疵)**

原版(`a52ab81`)TASK-009 verification 只有 3 行, D7 四条约束里唯独缺失
`number_str.isascii() and number_str.isdigit()` 这条——`grep -n "isascii" a52ab81:...yaml` 零命中,
实证属实。现版 4 行齐全, 新增行 `"可解析谓词逐字为 number_str.isascii() and number_str.isdigit()
(D7 第二条)"` 中的代码表达式与 proposal.md D7 行的原文 **逐字符一致**(均为
`number_str.isascii() and number_str.isdigit()`)。**判定: closed**——D7 四条约束现在全部出现在
TASK-009 verification 里。附带标签瑕疵见新发现 B(不影响本条闭合判定, 单列)。

### minor (TASK-008「签名与 schema 逐字不变」未继承「限本 Spec 变更面」限定词) — **NOT 完全 CLOSED / carryover**

R1 的 `suggested_fix` 逐字要求: "TASK-008 **verification** 该行末尾加「(限本 Spec 变更面; ...)」"。

实读现有 TASK-008 (`detailed-tasks.yaml:302-317`):

```
verification:
  - "SC-1/1b/2/3/4/5/5b/5c/11/13/14/15 全绿 (12 条 — R1-fix 补入首版漏列的 SC-11)"
  - "linked_issue_overlaps 的签名与返回 schema 逐字不变 ⇒ Phase B 现有调用方零改动"
  - "collision.py:228 的 linked_issue 回显不动 (SC-9 守着)"
notes: >
  ... 「签名与 schema 不变」**限本 Spec 变更面** — owner 2026-08-08 已裁 include_terminal
  形参归母 Spec 落地时追加 keyword-only 形参不视为对本条的违反、不构成回归 ...
```

`verification` 第 2 行的文字**逐字未变**(与原版比对: 原文 `"函数签名与返回 schema 逐字不变 ⇒ Phase B
现有调用方零改动 (D6)"`, 现版仅把「函数」换成「linked_issue_overlaps 的」、去掉了 `(D6)` 标记——**限定词
未加入这一行**)。限定词只出现在 `notes` 段, 而 R1 的具体诉求是 verification 字段本身缺它。

**风险评估**: 比原始缺陷(限定词只活在 tasks.md 一个完全独立的章节, `detailed-tasks.yaml` 内彻底不可见)
**已实质缓解**——现在限定词至少与该 verification 行同处一个 task block(notes 紧跟其后), Phase B 实施者
展开这个任务节点时会看到。但严格按 R1 suggested_fix 的字面要求("verification 该行末尾加"), **这一条
未被逐字执行**——它是"把答案写在旁边"而不是"写进要求的那一行"。

**判定: partially closed / carryover(实质风险已降但字面要求未满足)。** 建议: 把 notes 里那句限定词的
主干搬进 verification 第 2 行末尾(不需要删 notes, 两处保留不冲突), 消除"只读 verification 清单的人漏看"
这一具体读法风险(R1 原报告点名的正是这种读法)。

**Part 1 小结**: 4 条里 3 条 closed(其中 1 条 Major + 1 条 minor 附独立机械/集合复核), 1 条 minor
partially closed(carryover, 不构成新 Critical/Major, 已提供具体收尾操作)。

---

## Part 2 — 实现类任务与路径真实性(本轮重点)专项核验

### 全部 deliverables 路径 — 逐条 `[ -e ]` 存在性核验, 21 任务无一失败

| 路径 | 存在 | 备注 |
|---|---|---|
| `aria/skills/state-scanner/tests/test_release_by_track.py` | ✅ | TASK-001~006 宿主 |
| `aria/skills/state-scanner/lib/collision.py` | ✅ | TASK-007~010 宿主 |
| `aria/skills/state-scanner/lib/claim_schema.py` | ✅ | TASK-011 |
| `aria/skills/state-scanner/SKILL.md` | ✅ | TASK-012 |
| `aria-plugin-benchmarks/ab-results/` | ✅ | TASK-013;`git ls-tree` 确认 mode `040000 tree`(**非** `160000 commit`)——「主仓普通 tree, 非子模块」的注释属实 |
| `aria/.claude-plugin/plugin.json` / `marketplace.json` / `VERSION` / `CHANGELOG.md` / `README.md` | ✅×5 | TASK-015 |
| `aria`(gitlink) | ✅ | `git ls-tree HEAD -- aria` → `160000 commit af87cae... aria`——**确认是 gitlink 树条目本身**, 与目录 `aria/` 是两个不同的 git 对象类型, TASK-017 注释「gitlink (子模块指针)」技术上准确 |
| `VERSION` / `README.md`(主仓) | ✅ | 与 `aria/VERSION` / `aria/README.md` **内容实测不同**(`diff` 确认: 主仓 VERSION 首行「Aria 项目版本信息」/ 1.7.3, aria/VERSION 首行「Aria Plugin 版本信息」/ 1.65.5)——两份文件不是同名别名, 裸路径与 `aria/` 前缀路径确指不同文件, `path_convention` 的声明属实 |
| `README.zh/ja/ko.md` / `CLAUDE.md` | ✅×4 | TASK-018/019 |
| `.aria/repro/sc-baseline-linked-issue-normalization.py` | ✅ | TASK-021 |

**结论: 21 个任务的 deliverables 无一处路径失真、无一处指向错误仓/错误同名文件。**

### 9 处 file:line 引用 — 逐条实读, 全部精确(zero citation error)

`sed -n` / `grep -n` 逐条核对当前 aria 子模块工作树(HEAD 确认 = `af87caeeed88af6af76f29a8002badbe1228d927`,
与 `scope_repos` 声明一致):

| 引用 | 实读结果 |
|---|---|
| `collision.py:155` | ✅ `active = [c for c in claims if c.status not in ("done", "abandoned")]`(内联 tuple, 无常量绑定——描述属实) |
| `collision.py:210` | ✅ `_TERMINAL = ("done", "abandoned", "unknown")` |
| `collision.py:217` | ✅ `if c.linked_issue != own_linked_issue:` |
| `collision.py:228` | ✅ `"linked_issue": c.linked_issue,` |
| `collision.py:307` | ✅ `_TERMINAL = ("done", "abandoned")` |
| `claim_schema.py:107-114` | ✅ 107 行开 `linked_issue : Optional[str]`, 114 行闭 `winner determination.` |
| `SKILL.md:176` | ✅ 该行含「同一件事两个名字」逐字确认 |
| `phase1_gate.py:1232` / `:1235` | ✅ 1232 行 `linked_issue_overlaps(` 调用起始行, 1235 行 `except Exception as exc:` |
| `sc-baseline-*.py:277` | ✅(见下方专项核证) |

**结论: 9 处引用全部逐字精确, 无一处"注释声称但实际不是"。**

### `.aria/repro/sc-baseline-linked-issue-normalization.py:277` 机制专项核证

实读全文(287 行)。该脚本 `import` 的是**生产模块** `from lib.collision import linked_issue_overlaps`
(`sys.path.insert(0, sys.argv[1])` 后直接导入真实实现, 非 mock), `EVIDENCE_FACE`/`SPEC_TABLE` 由
`_parse_spec_table()` **现场解析** `proposal.md` 的 baseline 表(非硬编码常量, 漂移守卫属实)。核心比对:

```python
measured_face = {sc for sc, _, v, _, _ in results if v == "红"}   # 对生产函数实跑得到的真实红集合
...
if measured_face != EVIDENCE_FACE:      # :275
    ...
    sys.exit(1)                          # :277
```

`:277` 确实是 `measured_face != EVIDENCE_FACE` 分支的 `sys.exit(1)`, 与 TASK-021 notes 逐字一致。
`EVIDENCE_FACE` 是 proposal baseline 表里标 `✅` 的 8 行(`SC-1/1b/3/4/5b/11/13/15`), 现状(未修复)
这 8 条确实红(裸 `!=` 比较必不命中归一后应命中的变体), TASK-008 一旦把比较谓词切到归一键,
这 8 条会转绿并**从 `measured_face` 里消失**⇒ `measured_face` 与仍然声称"这 8 条应为红"的
`EVIDENCE_FACE` 不再相等 ⇒ 恒进 `:277` 分支。**机制与行号核证准确。**

**次要精度观察(见新发现 D)**: 触发 `:277` 只需要 8 条证据面 SC 转绿——这些全是"归一后比较键是否正确"
类(SC-1/1b/3/4/5b/11/13/15), 均**不涉及** TASK-009 专属的畸形输入守卫(它们的语料都是良构串)。因此
严格地说, 让 `:277` 首次触发只需要 **TASK-008** 落地, 不必等到 TASK-009。notes 原文「TASK-008/009
落地后该脚本恒红」把两个任务并列为触发条件, 略宽于实际机制(TASK-008 单独已足以触发)。这不影响
TASK-021 的**依赖设置**是否正确——依赖 TASK-009(collision.py 全链最后一棒)是更保守、更合理的工程选择
(避免在 TASK-008 刚落地、TASK-009 守卫尚未跟上的中间态就动手处置留证脚本), 只是文字归因偏宽,
不构成阻塞。

### `metadata.file_domain_serialization` 与实际 `dependencies` 一致性 — 确认

已在 Part 1 Major 项一并核verify(机械脚本无未定序对), 此处不重复。

### TASK-016(aria 子模块合并+双推+ls-remote)技术可执行性

三条 verification 均为标准 git 操作(`git merge` 本地合并 / `git push origin && git push github` /
逐远端 `git ls-remote <remote> master` 比对), 技术上均可执行, 无语法或工具链障碍。

**关于"是否漏前置(feature 分支从哪来/谁创建)"**: 检索本文件与 `tasks.md` 全文, 确认**没有**任何任务
显式声明"在 aria 子模块内创建 feature 分支"这一步。核对本项目已归档的同类 Spec
(`openspec/archive/2026-07-09-runtime-probe-archive-gate-integration/detailed-tasks.yaml`)发现同样
不显式列出分支创建任务——这与本项目十步循环约定一致(B.1 分支创建由 `phase-b-developer`/
`branch-manager` 在 Phase B 开工时统一处理, 不进入 `detailed-tasks.yaml` 的内容任务粒度, 该文件的
`scope_boundary` 也只声明 Phase C/D 委派, 未声明 B.1, 与既往先例同构)。**判定: 非 R1-fix 引入的缺口,
是本项目既有约定的一致延续, 不单列为发现。**

### TASK-020 grep 文件清单完整性 — 独立复核

对全仓做无约束 `grep -rln "1\.65\.5"` 扫描(不使用 TASK-020 命令自身的文件白名单), 命中 27 个文件。
逐条核对 TASK-020 清单(10 个文件)之外的 17 个文件是否"本该归零却被漏列":

- `aria/CHANGELOG.md` / 若干 `docs/handoff/*.md` / `.aria/audit-reports/*.md`(含本报告自身引用的历史数字)
  / `standards/conventions/secret-hygiene.md` / 另一 Spec `secret-guard-per-segment-evaluation/proposal.md`
  / 本 Spec 自己的 `tasks.md`/`detailed-tasks.yaml`(叙述"从 v1.65.5 升级到 v1.66.0"的历史行)/
  `.aria/triage-*` —— 全部是**历史叙述 / 版本史 / 审计存档**性质, 不是"当前版本声明", 纳入会造成
  永久假红(与 `aria/CHANGELOG.md` 被显式排除同理)。
- 未发现任何一份属于"当前版本声明但未被 TASK-020 命令覆盖"的文件。

**判定: TASK-020 的 10 文件清单维度匹配、无遗漏、无误纳**(与 qa-engineer R2 报告独立结论一致)。

### aria-plugin#133 评论 — 经 Forgejo API 独立核实(非仅信 commit message)

`forgejo GET /repos/10CG/aria-plugin/issues/133/comments` 返回 1 条 `2026-08-08T09:36:49Z` 的评论,
正文逐条列出 `collision.py:210`/`:307`/`:155` 三处 `_TERMINAL` 及其成员集差异, 与本报告上方独立实读
`collision.py` 得到的内容**逐字吻合**, 并更正 issue 标题为「6 处具名 + 1 处内联, 3 种成员集」。
**判定: TASK-008 notes 里"已给 #133 补评论"的自陈属实, 非声称未做的 paper-fix。**

---

## Part 3 — 新发现(R1-fix 引入, 均 minor/observation, 均 `new`)

- type: issue
  severity: minor
  category: documentation
  scope: detailed-tasks.yaml TASK-009 verification (D7 第二条标签)
  new_or_carryover: new
  summary: 新增的 isascii/isdigit 谓词行标注「(D7 第二条)」, 但按 proposal.md D7 行本身的分号顺序
    (可解析谓词 → limit → int()try-except → 不含#), isascii/isdigit 谓词是**第一条**而非第二条;
    「第二条」只在 tasks.md 自己重排后的顺序(不含# → isascii/isdigit → int() → limit)里成立
  evidence: >
    proposal.md:161 D7 行原文分号顺序: "可解析谓词 = number_str.isascii() and number_str.isdigit();
    limit = sys.get_int_max_str_digits() 且 limit > 0 and len > limit 判不可解析; int() 必须包
    try/except ValueError; 不含 # 先判不可解析, 不得无守卫拆分"——isascii/isdigit 是该行第 1 个分句。
    detailed-tasks.yaml TASK-009 verification 第 3 行标注 "(D7 第二条)"，若读者据此去 proposal.md
    D7 行按分号计数校验，会数到 limit 条款而非 isascii/isdigit 条款，产生错位。
  recommendation: 去掉「(D7 第二条)」这个序号标签, 或改标「D7·isascii/isdigit 谓词」按内容而非序号引用,
    避免两份文档各自编号不一致造成的交叉核对错位。不阻塞, 纯标签精度问题。

- type: issue
  severity: minor
  category: documentation
  scope: detailed-tasks.yaml TASK-017 deliverables (裸 `aria` 表示 gitlink)
  new_or_carryover: new
  summary: TASK-016 用带斜杠的 `aria/` 表示"子模块 master ref", TASK-017 用不带斜杠的裸 `aria` 表示
    "gitlink 指针"——两个不同 git 对象概念用一斜杠之差区分，而 `metadata.path_convention` 没有覆盖这个
    特例(它只讲"aria 内文件带 aria/ 前缀"和"裸 VERSION/README.md 指主仓"，没讲"裸 aria 本身/带斜杠的
    aria/ 本身各指什么")
  evidence: >
    `git ls-tree HEAD -- aria` 确认主仓树里 `aria`(无斜杠) 是 `160000 commit` 类型的 gitlink 条目——
    TASK-017 的注释「# gitlink (子模块指针)」在 git 对象模型上准确。但 YAML 纯字符串层面不携带这个
    类型信息，两处写法(`aria/` vs `aria`)完全靠各自行内注释区分，`path_convention` 段落本身未成文
    这条规则。若审阅者只扫 `path_convention` 不逐条看行内注释，容易把二者读混或当成同一交付物写重了。
  recommendation: 在 metadata.path_convention 补一句「裸 aria(无斜杠)= 主仓树里的 gitlink 指针本身；
    aria/(带斜杠)= 子模块整体工作树引用；二者不是同一交付物」。不阻塞，文档完整性问题。

- type: observation
  severity: minor
  category: testing
  scope: detailed-tasks.yaml TASK-021 notes(恒红触发点归因）
  new_or_carryover: new
  summary: notes 称「TASK-008/009 落地后该脚本恒红」，但 sc-baseline 脚本 :277 的 measured_face !=
    EVIDENCE_FACE 判据只依赖 8 条证据面 SC(均为良构语料、纯比较键正确性)，TASK-008 单独落地即足以
    让这 8 条转绿并触发该分支——TASK-009 的解析守卫对这一具体触发点不是必要条件
  evidence: >
    EVIDENCE_FACE = {SC-1,SC-1b,SC-3,SC-4,SC-5b,SC-11,SC-13,SC-15}——全部输入语料在 proposal SC 表里
    标注为"良构"(不含 SC-6/6b/10 等要求解析守卫才能安全处理的畸形语料)。故它们的判定只取决于
    normalize_linked_issue 的核心归一逻辑(TASK-007)是否被 linked_issue_overlaps 实际调用
    (TASK-008 完成的事)，与 TASK-009 新增的 isascii/isdigit/try-except/limit 守卫无关。
  recommendation: 不阻塞——TASK-021 依赖 TASK-009(而非仅 008)本身是更保守、更合理的工程选择(等
    collision.py 全链稳定再处置留证脚本)，不需要改依赖字段。仅建议 notes 措辞从「TASK-008/009 落地后
    恒红」改为「TASK-008 落地后即恒红(TASK-009 是否已完成不改变这一结论), 依赖 TASK-009 是为了等
    collision.py 全链落定后再一次性处置」，避免归因误导后续读者去追查"是不是 TASK-009 哪里没做对"。

---

## Verdict

**vote: PASS**(0 critical, 0 major——carryover 的 minor-4 已实质缓解且未升级为 major, 满足既往轮次
"0 critical 且 0 major ⇒ PASS" 判据)

verdict (frontmatter 口径): **PASS_WITH_WARNINGS**(0 Critical + 0 Major + 1 minor carryover(partially
closed) + 3 minor/observation(new)）

**fix 引入占比**: 本轮新发现的 3 条(D7 标签 / 裸 aria 记法 / 恒红归因偏宽)全部是 minor/observation，
**0 条 Critical、0 条 Major**——占「本轮新增 Critical/Major 计数 / R1 该四条总数」= **0/4 = 0%**。
未发现"fix 自身按同一规律再生成缺陷"的迹象(memory `feedback_audit_marginal_return_goes_negative`
描述的拐点未出现)。真正需要跟进的是 Part 1 的 minor-4(限定词只进 notes 未进 verification 行)——
这是**未完全闭合的 carryover**，不是新缺陷，且已给出一句话可执行的收尾操作，不阻塞发版但建议 Phase B
前顺手补。

## 轮次记录

- Round 1 (backend-architect): 0 Critical + 1 Major + 3 minor, verdict PASS_WITH_WARNINGS(vote REVISE)。
- Round 2 (backend-architect, 独立席位, 同一视角保持可比): 逐条核 R1 四条(1 Major + 3 minor)——3 条
  closed(其中 Major 项与 minor-1 项均附带独立机械/集合复核，非仅读字段)，1 条(minor-4，限定词位置)
  partially closed / carryover。本轮专项核验「实现类任务与路径真实性」: 21 个 deliverables 路径逐条
  存在性核验全通过、9 处 file:line 引用逐字精确、DAG 脚本化核验无环无悬空无未定序同文件对、
  sc-baseline 脚本 :277 机制核证准确、TASK-020 grep 清单经全仓无约束扫描反查确认维度匹配无遗漏、
  aria-plugin#133 评论经 Forgejo API 独立核实确已落地(非声称)。新增 3 条 minor/observation(D7 标签
  序号偏差 / 裸 aria 记法未成文 / 恒红归因偏宽)，均不阻塞。verdict PASS_WITH_WARNINGS，vote PASS。
