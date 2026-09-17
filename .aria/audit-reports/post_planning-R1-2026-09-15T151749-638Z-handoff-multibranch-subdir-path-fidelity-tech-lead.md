---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-09-15T16:28:10.094Z
context: openspec/changes/handoff-multibranch-subdir-path-fidelity/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 — tech-lead 席 — handoff-multibranch-subdir-path-fidelity (10CG/Aria#195)

## 审计结论

### 实读范围

- 审计对象 (全文): `openspec/changes/handoff-multibranch-subdir-path-fidelity/tasks.md` (122 行) · `detailed-tasks.yaml` (684 行)
- 依据: `proposal.md` 按行切片读了头部 1-29 行、§触点清单 30-114 行、§6 文档同步 300-342 行、Tasks 364-407 行、SC 表 415-433 行 (SC-1/2/4/5/6/7/8/10/11/12a/12b/13 全文)、§待 owner 复议 469-517 行; 决策单 `.aria/decisions/2026-09-12-…-technical-rulings.md` 全文 (116 行); `.aria/decisions/2026-09-07-…-pointer-guard.md` 的「落地约束」一节 (56-61 行)
- 规划规范: `aria/skills/task-planner/SKILL.md`、`DUAL_LAYER_SPEC.md`; 先例 `openspec/archive/2026-09-06-owner-container-identity-key-and-collision-parser/detailed-tasks.yaml` 组 5 (540-667 行)
- 代码真值 (aria `1cb3872`): `collectors/handoff_multibranch.py` 的 14-66、350-560 行及全部被引行号; `scan.py` 160-215 行; `writers/latest_md_writer.py` 1-60、100-175、255-320 行; `lib/spec_complete.py` 186-300、330-378、508-600、775-810、1000-1222、1757-1823 行; `lib/carry_forward.py`; `release_gate.py` 185-215 行; `phase1_gate.py` 的 self-resume 相关段
- 其它: `openspec-archive/SKILL.md` Step 7 (282-356 行); `phase-b-developer/SKILL.md` B.0 (80-130 行); `standards/conventions/{configured-gate-authority.md,content-integrity.md §4.4-4.5,session-handoff.md}`; `.aria/config.json` audit / phase_c_integrator 段; `aria-plugin-benchmarks/AB_TEST_OPERATIONS.md` 发版前清单 (545-560 行)

### 实跑命令与关键输出 (全部只读; 临时件放 scratchpad, 用完已删)

1. `git -C aria diff --stat f314785 1cb3872 -- $(41 条触点)`: 从 proposal 表机械导出 41 行 (改写 12 / 改写待定 2 / 新增 1 / 引用 26) ⇒ **`8 files changed, 109 insertions(+), 10 deletions(-)`**, 代码落点零 diff —— 与 yaml `baseline_rebase` 一致。
2. 16 条 `sc11_baseline_predicates` 在 `1cb3872` 上逐条跑 ⇒ **16/16 FAIL** —— 与 yaml 声称一致。
3. `python3 -B -m unittest <9 模块>` ⇒ `Ran 169 … OK`; 单跑 `test_collision` ⇒ **`Ran 0 tests`**; 8 模块 ⇒ `Ran 169 … OK`。pytest 腿: `test_collision.py` **28 passed**、phase-d-closer `tests/` **11 passed**。单模块计数: dedupe 23 / track_board_advisories 5 / p1_layer_h 24 / scan_integration 19 —— 全部与 yaml 一致。`run_tests.py` 全量 1605 本席**未复跑** (它会在真仓上跑 scan.py, 而 v1.73.2 之后 scan.py 会写本地 `refs/aria/coordination`, 属本席禁令); 只核对了主控放在 scratchpad 的 `run_tests_baseline_1cb3872.txt:123` = `Ran 1605`。
4. yaml 解析: 32 任务 / 92.5h / 代理分布与 metadata 一致; DAG 无环、无悬空依赖; 冗余边 6 条; 同文件并行只出现在 `verification-ledger.md`。
5. `_CHECKBOX_ANY_RE` 对 `- [ ] 2.0a foo` 取 parent = `None` (「读前必看」第 10 条属实); tasks.md 共 25 个 checkbox, 与 yaml 的 25 个 parent 一一对应。
6. 行号核验: collector `:20/:36/:40/:42/:177/:178/:243/:246/:247/:277/:280/:298/:301/:313/:315/:321/:332/:494/:586/:596/:619/:637/:665/:687`、`test_max_branches_resolver.py:286,300,316,332`、schema `:1072/:1106/:1110/:1112/:1116/:1124/:1127/:1128/:1138`、`layer-l-integration.md:105`、`phase-1-collectors.md:102`、`session-handoff.md:97/:171-173` —— 均命中所述内容。`VERSION:24` = v1.73.0, 其余 15 个版本点 = 1.73.3; `git show --stat 5990b85/5fe15b0/1b9734a -- VERSION` 三次都没碰 VERSION (「读前必看」第 9 条属实)。
7. 其它工具检查: `check_bare_issue_refs.py tasks.md detailed-tasks.yaml` ⇒ `裸 issue 引用: 0`; 两个文件都没有带圈字符和希腊字母编号。

下面逐条列 finding。

---

### M1 [Major] type=issue · category=documentation · scope=TASK-019 / TASK-020 / tasks.md「读前必看」第 1 条

**证据**: 采用改键支 (决策单 §2 第 4 行附问 + §5 终裁) 以后, 所有描述 dedupe 键层级的句子都得改。计划沿用的是 proposal 在默认支下列的落点: 默认支只改不变量句, 只有 `:396`、`_dedupe_sort_key` docstring、schema `:1126` 三处。本席实跑 `grep -rn -i 'four-level\|four levels\|then dictionary-max' aria/skills/state-scanner/{scripts,references}`, 结果:
- `handoff_multibranch.py:355` 写着「greatest under the **four-level** key below wins」
- `handoff_multibranch.py:58-61` 写着「ties broken by dictionary-max filename then dictionary-max branch (… input-order-invariant)」
- `handoff_multibranch.py:490-492` (公开函数 `dedupe_latest_per_track_container` 的 docstring) 写着「ties broken by dictionary-max filename, then dictionary-max branch」
- `state-snapshot-schema.md:1134` 写着「inherits … the **four-level** sort key by construction」

TASK-020 的 deliverables 注释 (yaml:452) 只列了 `:368-399` 和 `_dedupe_sort_key docstring`; TASK-019 (yaml:437) 只列了 `:1124/:1127/:1128`。上面 4 处都没被任何任务覆盖。SC-11 的 (j1)(j2)(j3) 分别锚在 `_dedupe_sort_key` docstring、含 `compound key` 的那一行、`# Tie-break, finalized` 注释块, 对这 4 处都测不到。

**照计划执行会出的错**: 代码已经是五级键, 三处文档也改成了五级, 但 `:355` 和 `:1134` 仍然写「four-level」, 另外两处只列到 branch。这就是 Rule #3 要防的文档与代码不一致, 而 SC-11 的 (j) 组谓词会全绿, 给出假绿。

**建议改法**: TASK-020 deliverables 补 `:54-66`、`:350-358`、`:490-492`; TASK-019 补 `:1134`。再加一条按类别覆盖的谓词: 改后 `grep -n -i 'four-level\|four levels' scripts/collectors/handoff_multibranch.py references/state-snapshot-schema.md` 零命中 (本席在 `1cb3872` 实测为 5 行命中, 改前为红, 有鉴别力)。「读前必看」第 1 条的执行口径也要改成「全部键层级描述 (至少 7 处) 都改写」, 不能只写「三处」。

---

### M2 [Major] type=issue · category=testing · scope=yaml `metadata.sc11_baseline_predicates` (a)(b)(l1) · TASK-019 / TASK-020 / TASK-001

**证据**: yaml:70 已经自己意识到「函数体代码本身会出现 rel_path, 用 grep 整段会被代码满足」, 并据此把 (j1) 改成只查 docstring。但同样的问题在 (a)(b)(l1) 上没修。本席在 scratchpad 副本上构造了贴近真实的坏实现: writer 只按 TASK-013 改代码, `:32/:279/:287-290` 的契约 docstring 一行没动; schema 只改 legacy 公式, 再加一行 Change history 和一行字段定义, 不补 TrackEntry 的 `rel_path` 行, 也不改 fail-soft 形状。实跑结果:
```
297:    degraded_reason = None
304:        content, degraded_reason = _render_pointer(active_tracks[0], now)
321:        "degraded_reason": degraded_reason,
l1 PASS   a PASS   b PASS   g PASS
```
另外, TASK-019 自己要求的 Change history 行必须「含 rel_path / unreadable_count」(yaml:439)。这等于**结构上保证** (a) 至少有 1 次计数、(b) 至少有 1 次命中, 与目标行改没改无关。

**照计划执行会出的错**: TASK-013 一落地, (l1) 就已经为真, 比 TASK-020 开工还早。TASK-020 用「(l1)(l2) 为真」(yaml:459)、TASK-019 用「(a)(b)… 为真」(yaml:440) 来验收文档同步, 结果会是: fail-soft 形状、TrackEntry 字段行、writer 三处契约面都漏改, 验收仍然全绿。TASK-001 只证明了「基线全红」, 这只能说明谓词对基线有鉴别力, 不能说明它能区分「代码改了但文档没改」这种真实坏实现 (memory `adversarial-fixture`)。

**建议改法**: 按 (j1) 的思路给这几条谓词加定位。(l1) 用 `ast.get_docstring` 分别取模块 docstring 和 `write_latest_md` docstring, 断言 `degraded_reason` 出现在其中; (a) 改成对 `**Fail-soft**` 那一行做 `grep 'Fail-soft' | grep -q unreadable_count`, 再对 `track_id:`/`filename:` 所在的 TrackEntry 块切片后断言 `rel_path:` 行存在, 这就覆盖了 (b)。TASK-001 增加一步: 对每条谓词写一个「只改代码/只加 Change history」的坏实现, 断言谓词仍为 FAIL。

---

### M3 [Major] type=issue · category=testing · scope=TASK-015 / TASK-016 / TASK-017 / TASK-018 · hard_constraints yaml:80 · tasks.md:75

**证据**: 组 3 的全部反事实都要求「在 scratchpad 的一次性 git worktree 副本上打补丁」(yaml:366、:382、:398、:417)。但 tasks.md 和 yaml 都没有规定 Phase B 什么时候提交代码: `grep -n -i '提交\|commit\|worktree\|起分支' tasks.md` 只命中表格说明和 3.4 本身; yaml 里的「提交」只在 TASK-023 (standards) 和 TASK-005 (基线 JSON) 出现。`git worktree add` 检出的是**提交**, 不带工作树里未提交的改动。本席用一次性临时仓实跑确认:
```
uncommitted implementation in working tree:  def f(): return "rel_path"
worktree copy (HEAD):                        def f(): return "basename"
```
同时, 四个任务的 verification 都只要求「打补丁后红」, 没有要求「打补丁前在同一副本上为绿」这个对照。

**照计划执行会出的错**: 如果组 2 的实现还没提交就 `worktree add … HEAD`, 副本里是基线代码。例如 TASK-017 的「legacy id 沿用 basename ⇒ (a) 红」: 基线本来就是 basename, 补丁是空操作, 测试照样红, 台账会记下「反事实红, 鉴别力成立」, 实际上什么都没测。rule6_note 把这些 GREEN/反事实记录列为 substitute 证据 (yaml:82), 于是假证据会进 Rule #6 台账。

**建议改法**: (1) 明确提交点: 组 2 结束时由主控在 aria feature 分支提交, 并把 SHA 记进台账; 组 3 所有副本一律 `worktree add <path> <该SHA>`。(2) 每条反事实的 verification 统一改成三步: 「未打补丁的副本上该用例 GREEN → 打补丁后 RED → 记录副本 HEAD SHA + 补丁 diff」, 其中第一步必须留下输出。

---

### M4 [Major] type=issue · category=testing · scope=TASK-021 / TASK-026 / TASK-029 (依赖图)

**证据**: TASK-021 是全量回归两腿, 依赖为 `[TASK-015..020]` (yaml:470)。本席算了祖先集: **不含 TASK-023, 也不含 TASK-024**。TASK-026 (AB) 依赖 `[021, 022, 024]` (yaml:560), **不含 TASK-023**。而确实有测试直接读这两个任务要改的文件:
- `tests/test_coordination_default_lockin.py:290,324,360` 读 `references/layer-l-integration.md` (TASK-023 改 `:105`), 并做分节切片断言
- `tests/test_git_operation_rule.py:13-14` 读 `RECOMMENDATION_RULES.md` 和 `references/rules/advanced-rules.md` (TASK-024 若落编辑就会改它们)
- `SKILL.md:192,194` 用渐进披露的方式链接 `layer-l-integration.md`, AB 运行中 AI 可能读到它

TASK-029 (本地 merge、推送) 的 verification (yaml:623-625) 里也没有「对合并结果重跑回归」这一步, 而合并前那次 fetch 可能带进并发提交。

**照计划执行会出的错**: TASK-021 记下的「零失败」、TASK-026 的 AB 结果, 测的都不是最终合并进 master 的那棵树。TASK-023 或 TASK-024 若在它们之后落地并打红既有结构测试, 或者 merge 时拉进来的并发改动与本 cycle 冲突, 在推送前都没有任何一步能发现, SC-10 / Task 4.3 的「全绿」就成了假绿。

**建议改法**: TASK-021 的依赖补 `TASK-023, TASK-024` (本席核过, 不会成环); TASK-026 的依赖补 `TASK-023`; TASK-029 在「本地 merge 之后、推送之前」补一条 verification: 对 merge 结果重跑 `run_tests.py` 和两条 pytest 腿, Ran 数与 TASK-021 的差值要逐条归因。

---

### M5 [Major] type=issue · category=architecture · scope=TASK-032 (Phase D 归档) · tasks.md 4.3 / 4.4 行措辞

**证据**: TASK-032 只验归档门的二元 `complete` (yaml:681)。openspec-archive 实际调用的是 `spec_complete.py --gate` 的三态结果, 另外还有 Step 7: 只要 `d_payload != null`, 在 **headless 默认**下就自动在 Forgejo 建 `[Archive Tracker]` issue (`openspec-archive/SKILL.md:287-295,343-346`)。本席把 tasks.md 25 个 checkbox 全部置为 `[x]`, 放在 scratchpad 副本上跑 `python3 -B scripts/lib/spec_complete.py --gate <副本>`, 结果是 `complete True`、`verdict warn`, **d_payload 非空**。其中两条与环境无关, 真仓上必然复现:
- tasks.md 4.3 行含 `dogfood` (`_DOGFOOD_BENCHMARK_DEPLOY_KEYWORDS`), 行内没有 `ab-results|ab-suite` 路径 (`_ARTIFACT_PATH_TOKEN_RE`, spec_complete.py:1140) ⇒ `dogfood/benchmark/deploy claim 无可链接产物路径`
- tasks.md 4.4 行里的 `layer-l-integration.md` 以子串形式命中 `integration` 关键词 (spec_complete.py:324), 行内只有 `.md` 路径 ⇒ `no extractable symbol (fail-soft)`

2.2 行也因 `test_scan_integration.py` 和「调用方」被当成集成声称, 其中 `HEALTHY_TRACKS` 只定义在测试里, 无生产定义, 至多判 warn。先例: a1-entry cycle 归档时 Step 7 真的建了 `10CG/Aria#201` (见 `docs/handoff/2026-09-06-a1-entry-shipped-v1.71.0-and-gate-fix-v1.71.1-archived.md:156`)。

**照计划执行会出的错**: Phase D 归档时会自动发出一条外向 issue, 内容是这两条检查器假阳性。这与 yaml:75 的硬约束「外向动作执行前逐项请 owner 授权」冲突, TASK-032 也没有预期或核验这一步。另外, 归档门要求 25 个 checkbox 全部勾选, 其中包括 5.4 自己, 5.4 的子步骤 (release_gate、回帖、handoff) 还没做完就得先勾。

**建议改法**: TASK-032 在归档前先跑一次只读的 `spec_complete.py --gate`, 把 verdict 和 `unverified_claims` 记进台账; Step 7 的 tracker issue 列入外向授权清单, 或者先请 owner 决定建还是不建。把「文件名子串命中 integration」「dogfood 声称只认 ab-results 路径」这两类假阳性报给 10CG/aria-plugin。**不要**为了躲检查器去改 4.3 / 4.4 的措辞 (memory `author-to-match-checker`)。5.4 的勾选时点要写明: 归档前勾, 其余子步骤的完成证据记进台账。

---

### M6 [Major] type=issue · category=documentation · scope=TASK-025 (yaml:549) · tasks.md 5.3 行 (:89) vs 范围边界表 (:40) 与「读前必看」第 3 条 (:20)

**证据**: tasks.md:40 的范围边界表写明「`handoff.py` 子目录支持 / **`handoff-mechanics.md:114-124` 处方表** / **mv 日语义** / `reference-snapshot-aria.json` 重采样 / schema `errors[].tracks[]` 形状 | 不在本文件 | … **统一登记进 5.3 的 issue**」。「读前必看」第 3 条也写「(AI 手改路径) 缺口并入 5.3 issue」。但 yaml 规定的 issue 正文清单 (TASK-025 verification, yaml:549) 只有: handoff.py 两函数 + (a)-(f) + `session-handoff.md:97`「自动」+ 子目录布局锚点 + 两个 collector 的 exists 矛盾。**`handoff-mechanics.md:114-124` 手改路径没有同步第三态**、**`_get_file_commit_date` mv 日语义**这两项都不在里面。tasks.md:89 的 5.3 行同样漏了这两项。

**照计划执行会出的错**: 执行者按 yaml (本 cycle 的 verification 单一 SOT) 开 issue, 这两项就不会被登记。决策单 §2 第 2 行第 (4) 问只裁了「本 cycle 不动」, 并没有说「不跟踪」; 结果共享 SOT 里「AI 手改路径未同步」这个缺口将没有任何跟踪载体。这正是 focus 第 4 条所问的「明确不做的面没有登记」。

**建议改法**: TASK-025 的 verification 和 tasks.md 5.3 行补两条: (g) `handoff-mechanics.md:114-124` 生产 D.3 手改路径未同步第三态 (决策单 §2 第 2 行 (4)); (h) mv 日语义 (决策单 §2 第 5 行; 改语义的候选方案见 proposal 待复议 5)。如果主控认为 mv 日只需记在 CHANGELOG, 就改 tasks.md:40, 让范围边界表与 TASK-025 一致。

---

### M7 [Major] type=issue · category=testing · scope=TASK-026 (Rule #6)

**证据**: TASK-026 的 verification (yaml:565-568) 只规定了前置条件、用什么工具、基线臂输入、要有 `RESULT.md`、要开套件缺口 issue、substitute 台账保留, **没有任何通过判据, 也没有止损规则**。可对照的依据: CLAUDE.md §版本管理「Skill 变更发版前须**过** Rule #6 benchmark」; `AB_TEST_OPERATIONS.md:552-556`「发版前 — 无 WITHOUT_BETTER verdict 的 Skill (否则必须修复); 与上一次结果比对, 无回归」; `.aria/config.json` `benchmarks.require_before_merge: true`。先例 `ab-results/2026-09-05-v1.70.0-a1-entry-rule6/RESULT.md` §1.2 也专门区分了「回归面无效度」与「无回归」的证据来源。

**照计划执行会出的错**: AB 跑完只要产出了 RESULT.md, TASK-026 就算完成, TASK-027 → TASK-029 照常 bump、merge、push。即使 state-scanner 新臂劣于 old_skill, 或出现 WITHOUT_BETTER, 发布也不会被拦住。Rule #6 从「过」退化成了「跑」。

**建议改法**: TASK-026 补两条 verification。第一, 判据: 既有 eval 上 with_skill 不劣于 old_skill (对照上一次存档), 且无 WITHOUT_BETTER; 回归臂分数无效度时, 按先例写明证据来源和结论强度。第二, 止损: 出现回归或 WITHOUT_BETTER ⇒ 阻断 TASK-027/029, 上报 owner, 不得自行降级为「记录在案」。

---

### M8 [Major] type=issue · category=architecture · scope=tasks.md「读前必看」(:12-28) · TASK-032 (yaml:683) · Rule #10

**证据**: `standards/conventions/configured-gate-authority.md:109-113` (Rule #10 SOT §5)「AI **任何**自作主张的流程判断 (跳过 / 降级 / 改序 / 替代) … 都必须在 **session handoff 中显式写出**: 跳了什么 + 理由 + 请 owner 复议」, CLAUDE.md Rule #10 也有同一句。「读前必看」表头写着「proposal 不改, 以本节为准」, 表中有几条是主控自己拿的主意, 不来自 09-12 裁定:
- 第 6 条: SC-10 追加 pytest 腿
- 第 7 条: SC-12a 的「改前」扫描改为基线 SHA 的 worktree 旧代码背靠背跑, 属于**替代**已批准 SC 的核验程序
- 第 10 条: 编号合并与重编
- 第 11 条: 3.1-3.3 的用例本体提前到组 1, 属于**改序**

另外还有两处: TASK-014 在决策单只写「其余字典序」的情况下选定了「取大」方向; 范围边界表把 B.0 可能出现的 `occupied` 预先定性为「属已知缺口, 不是竞争者」。`grep -n '复议' tasks.md detailed-tasks.yaml` ⇒ **0 命中**。TASK-032 规定的 handoff 内容 (yaml:683) 只有两处记录 (`reference-snapshot-aria.json` 未重采样、standards 已改)。

**照计划执行会出的错**: 这些判断只以「执行口径」的身份生效。周期 handoff 按计划写, 就不会出现「请 owner 复议」, 与 Rule #10 §5 的要求不符, 这些判断也会悄悄沉淀成惯例。本席定为 Major 而不是 Critical, 理由有二: 这些判断已经在 tasks.md 里公开列出, 并由本 enabled 闸门审阅; 其中部分内容属于 owner 09-01 分工下 AI 可以直接裁的技术级事项。但「写进 handoff 请复议」是 Rule #10 明文要求, 不能用「已经列在 tasks.md」来替代。

**建议改法**: TASK-032 的 verification 补一条: 周期 handoff 列出本 cycle 的 AI 流程判断清单 (至少包括上面 6 项, 以及 Phase B 期间新增的), 每项写「做了什么 + 理由 + 请 owner 复议」。更好的做法是在 post_planning 收口时就写一次 handoff, 不必等到 Phase D。

---

### m1 [Minor] type=issue · category=documentation · scope=tasks.md「读前必看」第 1 / 3 / 7 / 8 条

**证据与问题**:
- 第 1 条在「proposal 正文」列只写了 Task 4.1 / 4.2 / SC-11(j) 三处。实际上仍写着默认支的还有: §6 的 `proposal.md:308` 与 `:320` (tasks.md 组 4 的依据正是 §6)、Risk 表 `:353`、SC-7 单元格 `:421`「A′ 下真正打开的 tie 面 … 本 spec 不加断言」、Task 2.0 `:370`「待复议 1 / 3 / 4 / 5 均取各自的推荐默认推进」。
- 第 3 条引号里的「AI 手改路径是否同步该态待 owner 裁」, 原文在 §6 `:330`, Task 4.4 (`:384`) 的写法是「注明处方路径待裁」。
- 第 7 条的「改前在 B.1 时跑」不是原文。SC-12a (`:426`) 写的是「同一工作区先跑改前」, 这句是推论。
- 第 8 条写「`:1062` 后插 2 行 ⇒ `:1074` 起全部 +2」。本席 `git diff` 实测: `:1062` 是原位改写, 真正的插入点在旧 `:1064` 之后, proposal 待复议 6 引用的 `:1070` 同样 +2 (yaml:40 写 `:1070→:1072` 是对的)。
- 此外, proposal 头部 `:26`「停在 Phase A 出口, 不进 A.2」和 `:473`「5c28d58f 定级差」这个硬前置门, 决策单都没有逐条处置, 表里也没有提。

**照计划执行会出的错**: 执行者去读 §6 时, 看到的仍是默认支的处方, 需要自己推断它已失效。好在执行口径列写得够泛, 所以只定 Minor。

**建议改法**: 第 1 条的「proposal 正文」列补全上面各处行号; 第 3 / 7 条改为标注原文位置, 注明是转述还是推论; 第 8 条改为「`:1064` 之后插入, `:1065` 起 +2」。

### m2 [Minor] type=risk · category=documentation · scope=tasks.md:3 头部依据链接

**证据**: tasks.md:3 把 `2026-09-07-…-pointer-guard.md` 列为依据「(A′ + 写侧守卫, 09-12 追认)」。该文件第 56-61 行的标题是「落地约束 (**Phase B 必须遵守**)」, 其中三处已由 proposal 勘正、决策单 §2 第 2 行 (5) 裁定「以 proposal 为准」: 字段名 `relpath` (应为 `rel_path`)、守卫判据 `relpath != filename` (即 R2 critical `6f8fa9f7`)、SC-15 的归档-only 夹具。「读前必看」没有提示这一点。

**照计划执行会出的错**: TASK-013 / TASK-006 的 verification 写对了字面, 所以风险低。但执行者一旦按那份决策单「必须遵守」的字面去做, 所有缺 `rel_path` 键的 track 都会一律降级。

**建议改法**: 「读前必看」加一行, 说明 09-07 决策单落地约束第 1、2、4 条已作废, 以 proposal §2.5 / SC-15 为准。

### m3 [Minor] type=issue · category=documentation · scope=tasks.md:65 · yaml:295

**证据**: 两处判据写的是**字面 U+FFFD 字符** (本席用 Python 逐字符扫描命中 `line 65 U+FFFD`、`line 295 U+FFFD`)。proposal Task 2.3 (`:375`) 写的是 Python 转义形式 (反斜杠、字母 u、再接 fffd, 与 `chr(0xFFFD) in rel` 等价), 不是字面字符。

**照计划执行会出的错**: 字面 U+FFFD 与解码损坏无法区分 (memory `output-hygiene`)。审查者如果按转义串 (反斜杠 u fffd) 去 grep 源码, 也会漏掉字面写法。

**建议改法**: 两处都统一写成转义形式 (反斜杠 u fffd) 或 `chr(0xFFFD) in rel`, 文档里不放字面字符。

### m4 [Minor] type=risk · category=architecture · scope=`verification-ledger.md` 的全部写入任务

**证据**: TASK-001 与 TASK-002 都没有依赖 (yaml:102、:120), 两者都写台账, TASK-001 还负责新建它。TASK-015/016/017/018 互相并行, 也都写台账; TASK-023/024/025 也会与它们并行写入。memory `workflow-file-domain` 的规则是「同文件串行」。

**照计划执行会出的错**: 并行的 subagent 同时改同一份 Markdown, 会互相覆盖或反复冲突重试, 台账段落的顺序也可能错乱。

**建议改法**: 台账统一由主控写, subagent 只把证据交回; 或者按任务拆成 `ledger/<TASK>.md`。至少给 TASK-002 加上对 TASK-001 的依赖。

### m5 [Minor] type=issue · category=documentation · scope=TASK-023 (yaml:511)

**证据**: `standards/conventions/session-handoff.md:329` 规定「修订流程 … 版本号 (header) 同步 bump」; 先例 `c955783` 的做法是在被改小节加 `> **Amended**: 2026-09-06 by OpenSpec …` (`:180`)。TASK-023 对这两点都没有交代。此外, 计划要写进共享 SOT 的原句是「本 cycle 不同步 (owner 2026-09-12 裁定)」。「本 cycle」对以后读 SOT 的人没有所指; 而且决策单 §2 是 AI 技术裁定, 由 owner 批准追认, 最终口径是 §5 在 09-13 确认的, 所以「owner 2026-09-12 裁定」这个归属写得不准。

**建议改法**: 按先例加 Amended 标注, 版本头是否 bump 的判断记进台账; 措辞改为「AI 手改路径 (`handoff-mechanics.md`) 尚未同步该态, 跟踪见 10CG/aria-plugin#<n>」。

### m6 [Minor] type=issue · category=testing · scope=tasks.md:110 SC 映射表

**证据**: 映射表 SC-11 行的「钉测 / 反事实」列写的是 **5.6**, 而 5.6 是裸 issue 引用自检, 与 SC-11 文档同步无关。同一行的「转绿」列漏了 5.4 (SC-11 (d)(h))。另外, 最后一次文档编辑 (TASK-023 / TASK-027) 之后, 没有任何任务把 16 条谓词整体再跑一遍。

**建议改法**: 把「钉测」列改成一个明确的任务, 例如在 TASK-021 或 TASK-029 的合并前回归里加一条「16 条谓词全 PASS」。

### m7 [Minor] type=risk · category=testing · scope=TASK-005 新增基线 JSON · TASK-021 (yaml:477)

**证据**: 冻结守卫只覆盖两份 09-05 语料 (hard_constraints yaml:77、TASK-021 yaml:477)。TASK-005 新建的 `handoff-multibranch-flat-baseline-YYYY-MM-DD.json` 按要求「必须用 B.1 基线代码生成」, 但没有对应的守卫。

**照计划执行会出的错**: 实现后如果 SC-2 变红, 执行者可以用新代码重新生成这份 JSON 让它转绿, SC-2 就成了恒真, TASK-021 发现不了。

**建议改法**: TASK-021 补一条: `git log --format=%H -- <新 JSON>` 只有 TASK-005 那一次提交, 且 `git diff <该提交> -- <新 JSON>` 为空。

### m8 [Minor] type=risk · category=architecture · scope=TASK-026 前置 · TASK-032 (yaml:682)

**证据**: TASK-026 要求会话以 `ARIA_COORDINATION_NO_PUSH=1` 启动, 但计划里没有「AB 结束后换一个不带该变量的会话再继续」这一步。`release_gate.py:193-203` 在设了 no_push 时只更新本地 ref, 返回 `push_skipped=True`, 且不算 hard_error。

**照计划执行会出的错**: 如果同一个会话一路跑到 TASK-032, claim 释放不会推到远端。TASK-032 自己的「push 后 ls-remote 核验」能发现这个问题, 所以定 Minor。

**建议改法**: TASK-026 结尾加一步: 记录「退出 NO_PUSH 会话」, TASK-027 起在新会话执行。

### m9 [Minor] type=risk · category=architecture · scope=「读前必看」· TASK-001

**证据**: proposal 头部 `:15` 写的是「**Phase B 在 `f314785` 起分支**」。计划的意图是以 B.1 实测的 aria `origin/master` 为基线 (TASK-001, yaml:106, 此刻实测为 `1cb3872`), 但没有明确写出分支起点, 「读前必看」也没把这句列为已失效。

**照计划执行会出的错**: 如果从 `f314785` 起分支, A.2 的行号偏移表 (schema 的 +2) 就对不上, 本地 merge 时 plugin.json / CHANGELOG 会冲突, Ran 数也不可比。

**建议改法**: TASK-001 明写「aria / standards / 主仓的 feature 分支都从 B.1 实测的 origin/master 起」, 并把 proposal `:15` 列进「读前必看」。

### m10 [Minor] type=issue · category=architecture · scope=依赖图

**证据**:
- TASK-026 的产物目录名是 `YYYY-MM-DD-v<vNEXT>-…` (yaml:562), 但版本号要到后续的 TASK-027 (yaml:586) 才算出来。
- TASK-024 复核的量包括「leader pointer 仍在 latest.md」, 这个量由 TASK-013 的守卫决定, 可 TASK-024 的依赖是 `[014, 017]` (yaml:525), 不含 TASK-013。
- 冗余边 6 条 (都是传递依赖已隐含的边): TASK-018/019/020 → TASK-012、TASK-026 → TASK-021、TASK-027 → TASK-019/020。

**建议改法**: 目录名在 TASK-027 取号后再重命名, 或改用不含版本号的名字; TASK-024 补上对 TASK-013 的依赖; 冗余边可以留着, 不影响执行。

### m11 [Minor] type=issue · category=documentation · scope=TASK-028 (yaml:600) · TASK-032

**证据**: 5.6 的写法自检排在 TASK-029..032 之前, 但这之后还会产生新文字: 台账追加、主仓同步面、周期 handoff、10CG/Aria#195 回帖, 这些都不在自检范围内。TASK-032 也没有写 Phase D 产生的主仓提交 (归档目录、handoff、checkbox 勾选) 要双推并逐个 `ls-remote` 核验, 只能靠全局硬约束兜底。

**建议改法**: TASK-032 补两条: 「新写文字按 content-integrity §4.4 / §4.5 自检」, 以及「Phase D 提交经 owner 授权后双推, 逐 remote `ls-remote` 核验」。

### m12 [Minor] type=decision · category=architecture · scope=TASK-029 粒度

**证据**: TASK-029 把两个子模块的本地 merge、打 tag、owner 授权推送、`ls-remote` 核验捆在一个 2h 的 backend-architect 任务里。先例把「merge + tag」(TASK-034) 和「owner 授权后双推」(TASK-036) 拆成了两个任务。owner 授权是一个等待点, subagent 拿不到授权。就整体粒度而言, 32 个任务中有 17 个低于 4h, 基本是核验 / 外向动作类的 S 任务, task-planner 规定「S 任务保持原样」, 可以接受。

**建议改法**: 把 TASK-029 拆成「merge + tag (backend-architect)」和「owner 授权推送 + 核验 (主控)」两个任务; 其余粒度不动。

---

## Verdict

**PASS_WITH_WARNINGS** —— 0 Critical / 8 Major / 12 Minor。

计划做对了的部分, 本席都实跑复核过:
- 依赖图无环, 组 5 标题写的执行序与 yaml 依赖一致。
- 决策单 §2 第 1-8 行和 §5 的两处分歧都按 §2 落地: 改键支、MINOR、Level 3 不拆、issue 开在 10CG/aria-plugin、mv 日不加 `--follow`、第三态措辞。
- 基线复核的数字全部复现: 41 触点 8 文件 109/10、16 条谓词全红、169/0/28/11、VERSION:24。
- 多远程两条硬约束和 Rule #8 都有任务承载。

8 条 Major 可以归成四类:
1. 改键支带出的文档落点和谓词没有补齐, 会造成假绿 (M1、M2)。
2. 核验证据的来源和时点没有钉住: 反事实可能跑在基线代码上; 回归和 AB 测的不是最终合并树 (M3、M4)。
3. 收尾阶段缺规定: 归档门会自动发外向 issue; 遗留 issue 漏登记两项; AB 没有通过判据 (M5、M6、M7)。
4. Rule #10 §5 要求的「AI 流程判断写进 handoff 请复议」没有任务承载 (M8)。

## Vote

**REVISE**

## 轮次记录

Round 1 (tech-lead, convergence): REVISE — 0C/8M/12m; 要点: 改键支漏 4 处键层级描述 (M1), SC-11 谓词 (a)(b)(l1) 会被代码或 Change history 行满足而假绿 (M2), 反事实 worktree 检出源与「补丁前为绿」对照缺失 (M3), 回归与 AB 不覆盖 TASK-023/024 和合并结果 (M4), 归档门对 4.3/4.4 必出 unverified 进而自动建外向 tracker issue (M5), TASK-025 漏 handoff-mechanics 与 mv 日两项 (M6), AB 无通过/止损判据 (M7), AI 流程判断未进 handoff 请复议 (M8)。
