---
checkpoint: post_planning
mode: convergence
rounds: 8
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS
timestamp: 2026-09-29T10:04:01.027Z
context: openspec/changes/pre-merge-completeness-gate-change-scope/detailed-tasks.yaml
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R8 · tech-lead 席 · 10CG/Aria#199 A.2/A.3 v2.7 (`7ef09ea`)

> 报告文件写入被拒，本回复即报告全文，请主控原样落盘。

## 已实读文件

派单 sha256[:16] = 4631e7fd6c98fbe2

- 派单 `p199-r8/prompts/tech-lead.md`，全文。
- 本轮审查面 `git diff 320d523 7ef09ea -- openspec/changes/pre-merge-completeness-gate-change-scope/`，全文 695 行，存在我 scratch 下的 `scope.diff`。
- `tasks.md` 全文 (260 行)。
- `detailed-tasks.yaml`：
  - 31 个任务的结构全量导出 (id / 依赖 / 工时 / agent / 条目数)。
  - metadata 以下各键全文：`baseline_rebase` / `hard_constraints` / `owner_gates` / `c25_five_questions` / `coord_push_verify` / `commit_attribution` (含 code) / `stage_cells` / `rule6_note`。
  - TASK-001 / 005 / 008 / 018 / 023 / 025 / 028 / 029 / 030 / 031 全文；TASK-027 只读了 v2.7 改动的几条。
- 执笔报告 `writer-reports/v2.7-writer-report.md` 与派单 `v2.7-dispatch.md`，全文。
- R7 聚合全文；R3 code-reviewer 席 m2 (`af5e1e47`) 原文。
- 决策单 2026-09-12 全文 (§1–§5)，决策单 2026-09-27 全文。
- proposal 切片：`:115` / `:162` / `:170` / `:251` / `:314` / `:466`。
- CLAUDE.md 的多远程两条硬约束与规则 3 / 6 / 8 / 10 (会话上下文)。
- aria `5215cf2` 源码：
  - `phase-c-integrator/SKILL.md:596-645`、`:505-530`
  - `phase-c-integrator/scripts/submodule_gate.sh:96-158`、`:216-335`
  - `git-remote-helper/scripts/push_all_remotes.sh:40-60`、`:95-135`
  - `config-loader/DEFAULTS.json:6-15`
  - `state-scanner/lib/collision.py:360-445`、`:512-516`
  - `lib/claim_lifecycle.py:316-319`、`:407-410`
  - `lib/reconcile.py:55-70`、`:220-262`
  - `scripts/phase1_gate.py:1455-1470`、`:1536-1560`
  - `scripts/lib/spec_complete.py` 的 `_is_hooks_or_config_path`
  - `scripts/collectors/custom_checks.py:350-380`
- 主仓 `7ef09ea`：
  - `.aria/state-checks.yaml`：16 条逐条列出，六条 command 读全文。
  - `.aria/probes/plugin-cache-currency.py` 与 `main-project-version-consistency.py` 的全部输出点。
  - `.aria/config.json`、`docs/handoff/latest.md` 头部、16 个版本点、`aria-plugin-benchmarks/ab-suite/`。
  - `.aria/decisions/2026-06-07-v1.29.0-block-flip.md:92`。
  - 10CG/Aria#211 归档目录 proposal / tasks 里的 T4 条。
- standards `2bc1c4c`：`git-commit.md:194-197`；`session-handoff.md` 在 `940cb5b..2bc1c4c` 的 diff。
- 远端只读查询：
  - `git ls-remote`：主仓两端 master、aria 两端 tag。
  - `forgejo GET`：仓级 labels、10CG/Aria#213、10CG/Aria#220、组织级 labels (返回 403)。
- 我自己实跑的内容，全部在 `scratchpad/audit-R8-tech-lead/` 下：
  - 在 `state-base` 的 `cp -a` 副本上不带种子复跑 v2 三态脚本。
  - 用 CRLF 夹具对照两种 grep。
  - 对照 TASK-001 基线区间与 v2.7 记录区间。
  - 核 `phase_d_sot` 六个文件在三个端点的 cat-file 与 diff。
  - 在 `7ef09ea` 上以「脚本缺失」态跑 liveness 分类器 (`python3 -B`，前后核过共享副本零改动)。

## Findings

无 critical，无 major，共 4 条 minor。

### m1 `749f8d15` · minor · issue · implementation · scope `detailed-tasks.yaml TASK-030`

**一句话**：owner 裁定的 C.2.4.5 override 默认路径 (PR 标签 `submodule-rollback-approved`) 缺一个前提。该标签在 10CG/Aria 仓级没有定义。计划没要求事先核实，没把「建标签定义」登记成外向动作，打标签之后也没有「标签确已挂上」的核验。

**证据**：
- yaml `:235` (owner_gates 第 17 项)：「默认路径 = PR 标签 submodule-rollback-approved … 标签由 owner 自己打, 或由主控在这一授权下经 forgejo 接口打 (记台账)」。`:2174` (TASK-030 的 C.2.4.5 条) 同义。
- 实跑 `forgejo GET '/repos/10CG/Aria/labels?limit=100'`，输出：`rc=0 len=934` / `count 5` / `has submodule-rollback-approved: False` / `['aria-auto', 'bug', 'feature', 'post-m0', 'stale']`。
- 实跑 `forgejo GET '/orgs/10CG/labels'`，输出：`forgejo: HTTP 403 from internal endpoint {"message":"[redacted] does not have at least one of required scope(s): [read:organization]", …}`。组织级因此无法核验。
- `.aria/decisions/2026-06-07-v1.29.0-block-flip.md:92`：`label_count: 0  # 0 'submodule-rollback-approved' labels`。仓内检索不到建立这个标签的记录。
- `submodule_gate.sh:147-148`：只 `forgejo GET …/issues/$ARIA_PR_NUMBER/labels` 后 grep 这个名字，取不到就 `return 1`，走 BLOCK。
- 执笔自报薄弱点 5：标签路径只在本地假 forgejo 垫片上测过。

**失败场景**：
1. TASK-030 的闸判 BLOCK。
2. owner 按第 17 项裁定 override，点名 {aria}，授权主控打标签。
3. 主控照 `:235` 经接口给 PR 挂标签。仓级 (以及组织级) 未定义该标签时，Forgejo 挂不上。具体是报错还是静默忽略，我没实测，不作断言。
4. 照 `:2174` 重跑闸。读不到标签，仍打印 BLOCK 并退出 1；`ALLOW:` 集合为空，不等于点名集合。
5. 再次停在第 17 项。

后果：
- 白走一次授权往返。
- 如果把接口回执当成功记进台账，台账与事实不符。
- 如果主控为让标签生效自行建标签定义，就做了一次未登记的外向写，与 hard_constraints 第 3 条「全部外向动作列于 owner_gates」相左。

定 minor 的理由：闸是 fail-closed，不会误合并；执行者仍有合法下一步 (按第 17 项上报)。这与 R6 `749f8d15`、R7 `3de4b245` 对同一 override 路径的定级口径一致。

**三态**：

| 情形 | 结果 |
|---|---|
| 不需要 override | 不涉及 |
| 需要 override，标签已定义 | `ALLOW:` 集合等于点名集合，放行 |
| 需要 override，标签未定义 | 这条路径恒红，直到有人建标签定义 |

**建议修法**：在第 17 项与 TASK-030 该条补三句：
1. 请 override 授权前，先核标签是否已定义。仓级用 `forgejo GET /repos/10CG/Aria/labels`；组织级需要带 `read:organization` 的凭据，或由 owner 在网页确认。
2. 未定义时，「建标签定义」是一次单独的外向写。要么和打标签在同一授权请求里点明，要么由 owner 在网页建。
3. 打标签后，先用 `forgejo GET /repos/10CG/Aria/issues/<PR>/labels` 核名字在位，回执原样记台账，再重跑闸。

**键注**：按 id 公式，本条与 R6 `749f8d15` 同键 (同 scope、同定级)，但内容不同：R6 那条讲 trailer 的调用时机，本条讲标签路径的前提。

### m2 `af5e1e47` · minor · issue · documentation · scope `detailed-tasks.yaml metadata.owner_gates`

**一句话**：第 14 项为 `--include-terminal` 新写的理由仍与源码不符。这个旗标只作用于「同一 linked issue、不同 track_id」的 advisory 重叠列表，与本轨自身 claim 处于哪一终态、看不看得见无关。

**证据**：
- yaml `:232`：「三态统一带上 --include-terminal: done / abandoned 不带它时被 collision 的终态过滤跳过 (aria 5215cf2 的 lib/collision.py:416 定义 _TERMINAL 为 done / abandoned / unknown, :420 在未带该旗标时跳过), yielded 不在该集合里、不带也看得见, 带上属无害冗余」。
- aria `5215cf2` 的 `skills/state-scanner/lib/collision.py`：
  - `:365`：这个过滤所在的函数是 `def linked_issue_overlaps(`。
  - `:372` docstring：「Detect active claims sharing our linked_issue under a DIFFERENT track_id.」
  - `:385-387`：「ADVISORY-ONLY … It never feeds winner determination and never blocks」。
  - `:426-427`：`if c.track_id == own_track_id:` / `continue  # same-name collision — reconcile's job, not ours`。
- `scripts/phase1_gate.py:1542-1552`：这个旗标只决定 `linked_issue_overlap` 与 `unknown_schema_claims` 两个输出键。`:1463` 的 help 文本是「把终态 claim (done / abandoned) 也纳入重叠检测」。
- 本轨同名 claim 的终态由 reconcile 处理，不看这个旗标：
  - `lib/reconcile.py:62`：`_TERMINAL_STATUSES: frozenset[str] = frozenset({"done", "abandoned"})`
  - `:232`：Rule 2 的终态判定。
  - `:57-59` 注明 yielded 是「voluntarily PAUSED session that can still be reconciled back into ownership」，仍当候选。
- R3 code-reviewer 席 m2 的建议句原文就是「done / abandoned 需要它才看得见; yielded … 带上属无害冗余」。v2.7 照建议落地，连建议里的误读一起继承了。

**失败场景**：读者照 `:232` 会理解为「本轨 claim 为 done / abandoned 时，认领闸不带该旗标就看不见它」。这一次命令照旧带着旗标，执行动作不变，所以定 minor。但以后若有人据此推断「yielded 态可以不带」，或在认领出问题时把这个旗标当关键去排查，会查错地方。

**建议修法**：理由句改为「`--include-terminal` 只影响 phase1_gate 的 `linked_issue_overlap` (他轨、同 linked issue 的 claim, 含 done / abandoned; collision.py:426 排除本轨) 与 `unknown_schema_claims` 两个 advisory 键, 不参与胜负判定; 带上它是为了让『同一 issue 已有他轨做完或放弃』可见 (phase1_gate.py:1463), 与本轨 claim 处于哪一终态无关; 本轨终态的处理见 reconcile.py:62 / :232」。

**键注**：按公式与 R3 `af5e1e47` 同键；本条就是该 minor 未闭合的部分 (见对账第 12 行)。

### m3 `b8cc29e0` · minor · issue · testing · scope `detailed-tasks.yaml TASK-001`

**一句话**：基线复核条改成了「与 v2.7 记录比对」，但两边不是同一个区间：
- TASK-001 实际跑的是 `301641b..<aria 起点>`；
- `aria_shifted` 有 4 条的「v2.7 复测」值记的是 `1cb3872..5215cf2`。

零漂移时两者也对不上，「新出现的 diff」没有可照做的判法。

**证据**：
- yaml `:1585` (TASK-001 基线复核条)：「对 … aria_shifted 各条冒号前的文件跑 git -C aria diff --shortstat 301641b <aria 起点> -- <文件> … 与 v2.7 记录比对 (metadata.baseline_rebase 各条的「v2.7 复测」值; 其中的「A.2 记」只作历史), 只有 B.1 时相对 v2.7 记录新出现的 diff 才逐处实读被引位置并在台账写偏移表」。
- `aria_shifted` (v2.7) 的写法：
  - `spec_complete.py` / `multi_remote.py` / `check_bare_issue_refs.py` 三条都是「v2.7 复测 1cb3872..5215cf2 零 diff」。
  - `README.md` 是「v2.7 复测 1cb3872..5215cf2 +1 / -1」，没记 `301641b..5215cf2`。
  - CHANGELOG / VERSION / README.zh.md 另记了 `301641b..5215cf2` 的值，可以直接比。
- 实跑 (起点取 `5215cf2`，即 v2.7 之后零漂移)，原样输出：

```
skills/state-scanner/scripts/lib/spec_complete.py       TASK-001 区间 301641b..5215cf2 rc=0 [ 1 file changed, 1 insertion(+), 1 deletion(-)] | v2.7 记录区间 1cb3872..5215cf2 rc=0 []
skills/state-scanner/scripts/collectors/multi_remote.py TASK-001 区间 301641b..5215cf2 rc=0 [ 1 file changed, 3 insertions(+), 3 deletions(-)] | v2.7 记录区间 1cb3872..5215cf2 rc=0 []
skills/state-scanner/scripts/check_bare_issue_refs.py   TASK-001 区间 301641b..5215cf2 rc=0 [ 1 file changed, 157 insertions(+)] | v2.7 记录区间 1cb3872..5215cf2 rc=0 []
README.md                                               TASK-001 区间 301641b..5215cf2 rc=0 [ 1 file changed, 2 insertions(+), 2 deletions(-)] | v2.7 记录区间 1cb3872..5215cf2 rc=0 [ 1 file changed, 1 insertion(+), 1 deletion(-)]
```

**失败场景**：B.1 时 aria 起点就是 `5215cf2` (没有新发布)。执行者照字面比，这 4 个文件的输出与「v2.7 复测」值不相等，于是判为「新出现的 diff」。接下来他要么逐处读被引行号、写一份全是零偏移的偏移表 (白做)，要么不知道怎么比而停下来问。反方向不会漏：`5215cf2` 之后的任何改动只会让两者更不相等。只多做、不做错、不漏，所以定 minor。

**三态**：

| 情形 | 结果 |
|---|---|
| 基线 (零漂移) | 字面比较误报 4 个文件 |
| 目标 (同口径比较) | 零漂移为绿；`5215cf2` 之后有改动为红 |
| 坏态 (`5215cf2` 之后插行，使 `spec_complete.py:924` 下移) | 两种比法都红，不漏 |

**建议修法**：二选一：
- 比对口径改为：另从 v2.7 复测端点到 B.1 起点跑一次 `git -C aria diff --shortstat 5215cf2 <aria 起点> -- <文件>`；主仓用 `90a1351`、standards 用 `2bc1c4c`、phase_d_sot 同理；两端点与路径的 cat-file 口径同上。退出 0 且输出为空，即无新 diff。
- 或在 `aria_shifted` 各条补齐 `301641b..5215cf2` 的值。

### m4 `c2513059` · minor · issue · documentation · scope `detailed-tasks.yaml TASK-023`

**一句话**：`ab-suite/version.yaml` 撞号的显形位置，TASK-023 与 TASK-029 两处说法对不上：
- v2.7 在 TASK-029 新加了「改版本面之前先把主仓 origin/master 并入 feature」。这样撞号会最先在这次并入时显形，处置是 abort 后停在第 6 项、解法由 owner 定。
- TASK-023 该条 (v2.7 同样改过) 仍写「以 TASK-030 合并时的冲突或合并后复读为准」「已被占 ⇒ 顺延」。

**证据**：
- yaml `:2015` (TASK-023 的 version.yaml 条)：「已被占 ⇒ 顺延; 在飞轨未合并前看不到 (如 10CG/Aria#211 标 deferred 的 T4 若在此之前解冻并升号), 以 TASK-030 合并时的冲突或合并后复读为准」。
- yaml `:2149` (TASK-029 前置条)：「在改任何版本面之前先把主仓 origin/master 并入主仓 feature 分支 … 冲突 ⇒ git merge --abort, 停下上报 (owner_gates 第 6 项)」。`:223` 第 6 项：「主仓侧的并入冲突无先例指针, 解法由 owner 定」。
- 执行序：TASK-023 (5.1) 提交 version.yaml，TASK-024 到 028 只动 aria，TASK-029 是主仓 feature 在 5.1 之后第一次并入 origin/master。
- 执笔报告「新建机制交互表」第 (2) 项只核了 commit_attribution、只前进断言与 TASK-030 同步合并，没核 TASK-023 的撞号条。

**失败场景**：他轨 (例如 10CG/Aria#211 的 T4 解冻) 在 5.1 之后把 version.yaml 升过 1.5.0。TASK-029 并入时 version.yaml 冲突，执行者按 TASK-029 abort 并停在第 6 项；而读 TASK-023 的人以为撞号在 TASK-030 显形、可以「顺延」。结果在安全方向 (停下交 owner，不会写错号)，只是两处说法打架，所以定 minor。

**建议修法**：
- TASK-023 该句改为「以 TASK-029 前置条并入主仓 origin/master 时的冲突 (停在第 6 项, 由 owner 定是否顺延) 或 TASK-030 合并后复读为准」。
- 可选：TASK-029 并入后，若 `git diff --stat <并入前 HEAD> HEAD -- aria-plugin-benchmarks/ab-suite/` 有输出，当场按 TASK-023 的命令重算两个计数，并复核 version 没撞号。

## 对账

### (i) R7 六簇

| 簇 | 判定 | 本席亲验证据 |
|---|---|---|
| `6be9db6a` | closed | (1) 16 条 check 逐条列出后，能打印 `##SKIP##` 的共 6 条：command 字面带的只有 plugin-version-arch-docs-match；探针里带的是 `config-template-key-currency.py` / `plugin-cache-currency.py` / `forgejo-app-token-liveness.py`；aria 侧 `issue_cache_freshness_probe.py:49` / `:67` 与 `linked_issue_field_probe.py:142` / `:313` 也会打印。与 hard_constraints 第 14 条 (3) 的新写法一致。`plugin-cache-currency.py:42-44` 的 `_skip` 打印哨兵后 `return 0`。(2) TASK-029 (`:2154`) 已改为「首行须以 OK 开头 —— 前缀比较」。五条的成功首行依次是 `OK badge=` / `OK (` / `OK plugin=` / `OK 主项目版本` / `OK (aria/ …`；失败首行 DRIFT / MISSING / MALFORMED / STALE / FAIL / UNRESOLVED / UNVERIFIED 无一以 OK 开头，所以判据能被证伪 |
| `76949787` | closed | revision_log v2.7 第 1 条勘正了 `29325b2c`。我用脚本比对 v2.6 与 v2.7 两版 yaml：`rev_log first 43 identical: True` |
| `6e4535a3` + `ab143d74` | closed | 我自造 8 个夹具实跑 (`type grep` 是函数；`/usr/bin/grep` 是 GNU grep 3.8)。旧断言在 `good-crlf` / `empty-oc-crlf` 上，函数版得 1、GNU 版得 0；新断言 (`tr -d '\r'`) 两者都得 1；多一字母 / 行尾空格 / 全大写三类，去 CR 前后都得 0 |
| `ce6f31fc` | closed | `:205` (hard_constraints 第 3 条) 与 `:232` (第 14 项) 都补了「并已按第 4 条强制对齐到 origin、对齐后重跑三元组解析」；`:2210` (TASK-031 latest.md 子步骤 2) 同样补上；TASK-001 的重新认领段补了「对齐后先重跑解析」。我在 `state-base` 副本上不带种子复跑 v2 三态脚本，97 行与嵌入输出逐字节一致；其中 N13 分叉态一对为 `push_success=False` / `True` |
| `bdce52c6` | closed | tasks.md `:102` 第 47 条已改为「这 10 处改锚点式; 其余 … 保留, 但增删条目时须整族重扫」；revision_log v2.7 条同时勘正了 `6ad0a84b`。我扫了 v2.7 新增行：新出现的位置式写法只有对旧写法的引述，和 TASK-027 固定编号的「第 7 步」。两版逐任务比对条目数、依赖、工时，结果 `task-level diffs: []`，既有位置式引用不会移位 |
| `3de4b245` | closed | 代价已写入 `:235` / `:2174` / tasks.md `:146` / 5.8 / 第 58 条，放行判据收紧为集合相等，与闸源码一致：`submodule_gate.sh:152-157` 先按子模块验 trailer，再调只收标签名的 `check_pr_label`；`:296-297` 对每个受影响子模块各打一行 `ALLOW: $SUB …`，点名集合可判。本路径上另有一个前提缺口，单列为 m1，不算该簇未闭合 |

### (ii) 执笔报告 B 组 21 行

| 行 | 键 | 判定 | 本席核验 |
|---|---|---|---|
| 1 | R2 TASK-018 (qa) | closed | 新标题列出 N1–N4 / N7 / N8 / 四份 frontmatter；TASK-018 第 2 条实际包含 n1–n4、n8、crlf_guard 与四份 frontmatter |
| 2 | R2 TASK-029 (cr/m1) | closed | `7ef09ea` 上 `CLAUDE.md:138` / `:142` 两处都是 1.74.0 |
| 3 | R2 TASK-029 (km) | closed | `main-project-version-consistency.py` 的 POINTS 共 9 个 (VERSION 两处、CLAUDE.md、四份 README、两份架构文档)，与计划所写一致。保留它有据：`CLAUDE.md:142` 同一行既有 aria-plugin 版本，又有「主项目 v1.7.5」 |
| 4 | R2 TASK-030 (tl/m1) | closed | 过时记录已删。真仓三个子模块都在 `refs/heads/master` 且等于 gitlink：aria `5215cf2` / standards `2bc1c4c` / aria-orchestrator `237045a` |
| 5 | R2 c25 (cr/m4) | closed | `push_all_remotes.sh` @`5215cf2`：`:49` 取 PRE_LOCAL_HEAD，`:107` push，`:112` 读 refs/remotes，`:119` 比较；全文 grep `ls-remote` 退出 1；`1cb3872..5215cf2` 零 diff |
| 6 | R2 读前必看 4 (tl/m3) | closed | `version.yaml` 为 `"1.5.0"`；`a563192..7ef09ea` 之间 ab-suite 零 diff，计数 32 / 84；10CG/Aria#211 归档 tasks `:136` 标 T4 deferred；10CG/Aria#213 正文含 T4 / deferred / version.yaml / 解冻 |
| 7 | R2 TASK-022 (cr/m5) | closed | TASK-022 第 1 条、读前必看第 16 条、第 59 条同步改成观察项，执行动作不变 |
| 8 | R2 guard (qa) | closed | `_is_hooks_or_config_path` 对路径里任意位置含 `/.aria/` 的 config.json 都判真，而守卫的尾部正则只认 `.aria` 为直接父目录，口径差属实；blind_spots 已补 |
| 9 | R2 v2_state_runs (cr/m3) | closed | 我不带种子复跑，输出逐字节一致 |
| 10 | R3 `31b4c0f1` | closed | standards `2bc1c4c` 的 `git-commit.md:196` 为 `Spec: standards/openspec/changes/{feature}/spec.md`；yaml 三处已改为「参照形制、本轨自定」，第 28 条加了链接注 |
| 11 | R3 `a5996c58` | closed | 我在 `7ef09ea` 以「脚本缺失」态调分类器，得 `{"status": "alive", "alive_categories": ["code_reference", "generic_path_call"]}` (L1 真、L2 假)，与重写 a 新写的前提说明一致 |
| 12 | R3 `af5e1e47` | partially | yielded 那半句已改；但新理由把旗标作用归到了本轨终态，与 collision.py `:365` / `:426` 不符，见 m2 |
| 13 | R3 `a2d80059` | closed | `latest.md` 首行是 `# Latest Session Handoff`，前 2000 字符里 `track-id` 行为 0 处；cannot_catch 已写明依赖这一形态 |
| 14 | R3 `a090f077` | closed | proposal `:162` (豁免降级)、`:170` (只定义 S4-bypassed 一格)、`:251` (逃生口无字段取值)、`:314` (16 键) 与新定位一致 |
| 15 | R4 `9c0dcb27` | closed | N13 可复跑，我复跑一致 |
| 16 | R4 `d931db51` | closed | 同第 2 行 |
| 17 | R4 `0dd2d3f2` | closed | 同第 11 行 |
| 18 | R3 + R4 `ea958583` | closed | 第 61 条与 `rule6_note` 实值一致 (decision_table_row 3 / scenario4b not_required / negctrl n/a / scenario1 为占位)；第 62 条与 `coord_push_verify.assert` 的 (d) 一致 |
| 19 | R5 `34b92188` | closed | 读前必看 24 / TASK-005 / TASK-008 / TASK-019 四处落点齐。stage_cells 里 TASK-008 只有 `SC-10.error-verdict-keyset` 一格带类型与非负断言；P6 那一跑的上下界只落在 TASK-012 起才观测得到的运行上，中间阶段验收不会被误红 |
| 20 | R5 `27cee280` | closed | 修法对题 (见下节第 1 条)；与 TASK-023 的接缝另计为 m4 |
| 21 | R5 `ae4753f5` | closed | 六个文件在 `301641b` / `1cb3872` / `5215cf2` 三个端点 cat-file 都退出 0；`1cb3872..5215cf2` 输出全部为空；`301641b..1cb3872` 只有 `phase-d-closer/SKILL.md` 为 `1 file changed, 2 insertions(+), 2 deletions(-)`，冻结点取 `1cb3872` 有据 |

## 对 10 条实质改动候选的逐条判断

1. **`27cee280` (主仓 feature 先并入)**：改法正确。
   - 并入放在 TASK-028 之后、改版本面之前。此时本轨还没改版本行，版本行不会在这次并入里冲突。
   - 合并提交会被 `commit_attribution` 判为 `sync-merge`：代码对多父提交的规则是「非首父都是基准的祖先」即 `sync-merge`，TASK-030 核验时满足。
   - 只前进断言的基线改为并入后的 gitlink，正确 (本轨此前不动 gitlink)。
   - 本机未设 `submodule.recurse`，主仓 merge 不会改 aria 工作树，「aria 工作树 HEAD 等于合并 SHA 时 git add aria」的前提不受影响。
   - 接缝：TASK-023 的撞号句 (m4)；只前进断言由此变得可以失败，但失败分支没写 (风险 1)；TASK-030 自己那次同步合并的冲突仍无编号停点 (风险 2，v2.6 既有)。
2. **`ae4753f5` (phase_d_sot)**：改法正确，路径存在与零 diff 都经我实测；TASK-001 第四组与 TASK-031 的比对口径一致，tasks.md 1.1 / 5.9 已同步。无新的不一致。另注意：10CG/Aria#220 (open) 针对的正是六个文件之一 `handoff-mechanics.md`，它的修复若先落地，TASK-031 必走重做映射分支 (风险 8)。
3. **`34b92188` (elapsed_ms)**：在我的视角内 (阶段验收、stage_cells) 改法正确；断言细节属 backend / qa 视角，未深核。TASK-005 的括注「(verdict 为 pass 或 fail)」与读前必看第 8 条「格 B 在 P6 前终止」字面上不严，但不会误红 (风险 5)。
4. **`9c0dcb27` (N13)**：改法正确，我复跑逐字节一致；无接缝。
5. **`6e4535a3` + `ab143d74` (先去 CR)**：改法正确，我的夹具能复现。接缝：同条相邻的 v2.5 值非空检查不去 CR，CRLF 下对空 owner-container 仍得 5 (夹具 `empty-oc-crlf` 实测 `E1-nonempty(gnu)=5`)。在本机 shell 的 grep 下 v2.6 就是这样，不是 v2.7 引入的 (风险 3)。
6. **`ce6f31fc` + R7 cr 风险 5 (对齐后重解析)**：改法正确，N13 分叉态一对可复现。小接缝：hard_constraints 第 3 条现在把「未强制对齐」也路由到第 15 项，而第 15 项 (`:233`) 的触发列表没列「强制对齐的 fetch 退出非 0」。第 3 条已给出路由，不影响行动 (风险 4)。
7. **`3de4b245` + C1 (标签默认路径)**：代价与放行判据的写法正确，与闸源码一致。有问题的是默认路径的标签前提 (m1)。另外，它与 hard_constraints 第 7 条「任何情况下不回退」的覆盖关系没写 (v2.5 起既有，风险 7)。
8. **`6be9db6a` + C3 (首行口径与占位符检查)**：改法正确；TASK-027 第 7 步、TASK-029、TASK-030 合并后复核三处同口径；无接缝。
9. **C2 (History 节交 10CG/Aria#220)**：改法正确，与决策单 2026-09-27 第 3b 项第 2 个决定一致，第 13b 项与 TASK-031 两处已同步。小歧义：「若 10CG/Aria#220 已定案，按其结论落」没限定本轨只落本条 prepend (风险 11)。
10. **D 组基线平移**：记录值我抽核全部属实：
    - CHANGELOG 小节数：`5215cf2` 上 139，`1cb3872` 上 138。
    - 16 个版本点及行号属实，`VERSION:24` 为 v1.74.0。
    - version.yaml 为 1.5.0；ab-suite 计数 32 / 84，加 eval 后目标 32 / 85 的前提成立。
    - standards `940cb5b..2bc1c4c` 只动了 `session-handoff.md`，新增的第三态限「经机械 latest_md_writer 写入时」。
    - 计划里没有按行号引用 `AB_TEST_OPERATIONS.md`，该文件整体下移一行不影响计划。

    有问题的是 TASK-001 的比对口径 (m3)。

## 对执笔人自报薄弱点的表态

1. 可接受：我核了 v2.7 `bdce52c6` 条的勘正，以及 revision_log 前 43 条逐项相等，没发现同类漏勘正。
2. 可接受：我抽核的记录值 (版本点、行号、计数、区间 diff) 全部属实；「机器只核交叉关系」这一局限执笔已如实写明。
3. 可接受：「Ran 数不得少于基线、差值逐条归因」本就能接住 `5215cf2` 上用例数的增加。
4. 可接受：该 check 不在本计划的运行面上，且 Rule #7 优先。
5. 不可接受：垫片恰好掩盖了真实前提——仓级未定义该标签 (实测)，见 m1。
6. 可接受：过了 P1 的每一跑都会先起 git 子进程 (同仓判定)，计时从入口起算，下界 1 ms 不依赖 P6 本身起子进程。
7. 可接受，建议补一句：停下上报是合法的下一步；重做映射里若出现新的外向动作，写明「另行逐项请授权并记台账」，不要写成「照 owner_gates」(那里没有对应项)。
8. 可接受：hard_constraints 第 4 条的通则本就要求对齐后重跑解析，执行条补齐是纠正漏写，N13 实测支撑。
9. 可接受：这是 v2.5 既有措辞，不改变动作 (handoff_autofill 那一项在它自己的条目里已按「退出码 + 空串」处置)。
10. 可接受：我抽核的数目字全部属实。

## 对执笔请裁 11 条的表态

1. 无意见。本轮就是 owner 为此重开的 R8；本席看 10 条里没有需要升为 major 的改法错误。
2. 赞成执笔取舍：5.5 那条 command 的首行自带同一断言；5.7 的前置只是提前拦住目录错，成本低。
3. 赞成执笔取舍：断言与 grep 实现无关，比兼守行尾更要紧，且与 `commit_attribution` 对 CRLF 的判法一致。建议同条的值非空检查一并去 CR (风险 3)。
4. 赞成执笔取舍：通则本就要求，且有 N13 实测。
5. 赞成执笔取舍：proposal 只给了键名，这是补空白，不改既有期望值，三态可以区分。
6. 赞成执笔取舍：10CG/Aria#220 很可能在本轨 Phase D 之前改 `handoff-mechanics.md`，若一律停下，会把常规演进变成必然的 owner 往返。重做内容照录进判断清单交复议，新外向动作仍逐项授权。
7. 赞成执笔取舍，但须先补前提：标签定义当前不存在 (m1)；「建标签定义」与「打标签」须在同一授权里点明，打后用 GET 核验。
8. 赞成执笔取舍：仓内没有这一族文件；放宽正则会改守卫判据与 N10 证据，blind_spots 已记下。
9. 赞成执笔取舍：遵守头部「不写字面版本号」，取号在 5.3 执行时实取，且有 5.5 的终核。
10. 赞成执笔取舍：`CLAUDE.md:142` 同一行同时有 aria-plugin 版本与主项目版本，这条 check 正好兜住改这一行时的误伤。
11. 赞成执笔取舍：改称观察项名实相符，执行动作不变。

## 风险 / 疑问

(不计入 finding)

1. TASK-029 的只前进断言 (`:2150`) 在 v2.7 下变得可以失败：他轨在 TASK-028 与 TASK-029 之间发了 aria 并 bump 主仓 gitlink 的竞态。失败分支没写，但 hard_constraints 第 7 条 (`:209`「主仓 gitlink 只前进, 任何情况下不回退」) 兜得住。建议显式写「不成立 ⇒ 不 bump、停下上报」。
2. TASK-030「合并方式」那次同步合并若冲突，没有编号停点 (v2.6 既有)。v2.7 只把第 6 项扩到了 TASK-029；TASK-029 与 TASK-030 之间 origin/master 若再前进，仍可能在那里冲突。
3. TASK-031 的值非空检查 (`:2208`，v2.5 写的) 不去 CR，与同条新改的取值断言对 CR 的处理不一致。
4. 第 15 项 (`:233`) 的触发列表没列「强制对齐的 fetch 退出非 0」，而 hard_constraints 第 3 条已把这种情况路由过去。
5. TASK-005 的括注「走到 P6 的那一跑 (verdict 为 pass 或 fail)」不严：格 B 是 pass，但在 P5 就终止。下界仍然成立 (P2 已起 git 子进程)，不会误红。
6. 第 17 项要求「恰等于」：点名的子模块若在重新同步后不再回退，也会判不放行。方向是 fail-closed，代价是多一次往返。
7. override 放行 aria 回退，等于主仓 gitlink 回退；这与 hard_constraints 第 7 条「任何情况下不回退」的覆盖关系没写 (v2.5 起既有)。
8. TASK-031 (M，3–5h) 若触发 phase_d_sot 重做映射分支，可能明显超估；10CG/Aria#220 (open) 修的正是六个文件之一。
9. `reconcile.py:57-62` 把 yielded 当候选而非终态，与第 14 项「三个终态下一步相同」的模型不一致 (v2.6 既有；与 m2 同源，属插件侧口径不一)。
10. 组织级标签因 token 缺 `read:organization` 无法核验 (HTTP 403)；m1 的「未定义」结论只对仓级成立。
11. latest.md 子步骤 1 (`:2209`) 写「若 10CG/Aria#220 已定案，按其结论落」，没限定本轨只落本条 prepend。若结论是恢复 History 的历史条目，可能把范围外的工作带进 5.9。

## Verdict

**PASS** · counts `0C/0M/4m` · **Vote: PASS**

## 是否足以开始 Phase B

足以开始。没有 critical / major，四条 minor 都不阻塞 B.1：
- m3 在 1.1 只会让执行者多做一份全零的偏移表，建议进 B.1 前顺手澄清比对口径。
- 其余三条分别落在 5.1 的措辞 (m4)、5.8 override 这条条件路径 (m1) 和第 14 项的理由句 (m2)。
- 入口门第 1 项事实上已满足：`03f97ac` 是两端 master `7ef09ea` 的祖先。
- 进 B.1 前仍要等 owner 对执笔的 11 条请裁一并裁定。