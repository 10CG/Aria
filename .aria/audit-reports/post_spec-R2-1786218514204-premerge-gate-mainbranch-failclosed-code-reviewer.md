---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T19:59:32.594Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R2 — code-reviewer 席位报告

被审对象: `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md` (387 行, R1 后结构性重写版)
仓库状态: `/home/dev/Aria` master @ 98ad1f5 (proposal.md 为工作树未提交修改, `git diff --stat HEAD` = +266/-58)
本席镜头: 新写内容自身的毛病 (fail-CLOSED 方向 / 修类不修实例 / 假自陈 / 枚举完整性 / 恒红恒绿对偶 / 条款间交叉一致性)

## 审计结论

Phase 1 (Spec 对现有代码的陈述属实性) **基本通过**: 抽查的 22 处行号/数字断言中 18 处逐字属实 (含
`pre_merge_gate.py:47-49/:300/:356-366/:378-388/:427`、`aether.py:117-135`、`base.py:29`、
`SKILL.md:167/:242/:243/:252-255/:267/:279`、`gate_state_helper.py:32-34/:147`、
`workflow-state-schema.md:38-54`、`path_coverage.py:19/:24`、`fetch_gate.py:108-128/:55`、
测试 24 调用点/0 显式传参/46+25+40=111、AB 套件 v1.1.0 7 fixtures 逐个 id、owner 裁定 `db2e983`
明文 "hook 非 capability skill"、本仓 origin/HEAD 与 github/HEAD 实测差异、`main...` RC=128 vs
`master...` RC=0)。**失实/漂移 4 处**, 见 M8 与 m4。

Phase 2 (按此 Spec 原样实施的正确性) **不通过**。核心问题: **承重条款 §5 的命令本身是 fail-OPEN 的**
—— 实跑证明它在「主分支真不存在」时可返回 exit 0, 精确复活本 Spec 要治的恒绿。另有 8 条 Major, 其中
7 条由 R1-fix 新写内容引入 (符合本项目「fix 轮在自己新写的内容里复发同形状缺陷」的实证)。

---

## Findings

### Critical

#### C-1 §5 承重条款的 `ls-remote` 命令因尾段 glob 语义 fail-OPEN — 存在性核验可在分支不存在时判「存在」

- **锚点**: `proposal.md §5 分支存在性核验` (第 158 行代码块 / 第 162-166 行判据表) + `D-F`
- **Spec 原文 (第 158 行)**: `git ls-remote --exit-code --heads <remote> <main_branch>`, 表中
  「exit **0** | 存在 | 继续原流程」。
- **实跑推翻** (fixture: upstream 仅有 `trunk` 与 `wip/master`, **无** `refs/heads/master`):

  ```
  $ git ls-remote --exit-code --heads origin master
  0c0c553fe59a54084318580f8404d01511557b50	refs/heads/wip/master
  RC=0                                    ← Spec 判「存在」

  $ git ls-remote --exit-code --heads origin refs/heads/master
  RC=2                                    ← 锚定 pattern 才是正确答案
  ```

  git 2.39.5。原因: ls-remote 的 `<patterns>` 是 glob, 匹配 ref 的**尾段** (从 ref 起点或任一
  `/` 分隔符起), 故 `master` 同时命中 `refs/heads/master` 与 `refs/heads/wip/master`。
- **后果链**: 仓内存在 `wip/master` / `backup/main` / `release/master` 之类分层分支而主分支名错或缺失时
  → §5 判「存在」→ 放行 → `backend.query_branch_in_flight("master")` → aether 返回 `runs=[]`
  (`aether.py:124` `data.get("runs") or []`) → `compute_verdict` 落 `pre_merge_gate.py:218-220`
  else 支 → **green**。这与 §Why 描述的原缺陷**逐字同形**: 查询成功 + 空载荷 = 判绿。
- **为什么是 Critical**: 这是 Spec 自称的「承重条款」, 是把 Rule #8 那条腿从 fail-OPEN 扳回
  fail-CLOSED 的**唯一机械兜底**。一个能被常见分支命名绕过的兜底, 正是本 Spec §Why 结尾自己写的
  「闸门存在 ≠ 闸门有判别力」。
- **修法**: pattern 改为完整 ref —— `git ls-remote --exit-code --heads <remote> refs/heads/<main_branch>`
  (实测 RC=2 正确)；或核验返回行的第二列**逐字等于** `refs/heads/<main_branch>` 后再判存在。
  另建议在 SC-4 增一条 fixture: 仓内存在 `wip/<name>` 但 `<name>` 不存在 ⇒ 必须仍 `main-branch-not-found`。
- **introduced_by_r1fix**: **false** — 该命令在原版 (HEAD 版 proposal 第 93 行) 即已存在。但 R1-fix
  以 M6 之名把它「钉死」成字符级契约 (§5 表 + D-F) 并升格为 SC-4 的承重断言, 五席 R1 + 本次重写
  均未核验其语义。

### Major

#### M-1 §3 权威路径缺「RC=0 但无 `ref:` 行」分支 —— 要治的「成功+空载荷」形状在新写路径上复发

- **锚点**: `proposal.md §3` 第 122 行 (「`git ls-remote --symref <remote> HEAD` → 解析
  `ref: refs/heads/<name>\tHEAD`」) + 第 123 行 (「两者均失败 ⇒ abort」)
- **实跑**: 对一个**空仓** (`git init` 后无 commit) 执行

  ```
  $ git ls-remote --symref <empty-repo> HEAD
  RC=0                                    ← 退出码 0, stdout 完全为空
  ```

  正常仓则输出 `ref: refs/heads/trunk\tHEAD` + SHA 行。
- **问题**: §3 只给了「解析出 `<name>`」与「失败」两态, 未定义「命令成功但输出里没有 `ref:` 行」。
  实施者可以 (a) 判为失败 → abort (正确), 也可以 (b) 认为 RC=0 即成功、`<name>` 取到空串 →
  空分支名流入 §5 与 `evaluate_path_coverage`。这与 §Why 第 44 行控诉 aether 的问题**同一形状**:
  「后端结构上无法区分『分支不存在』与『没有 run』, 二者都产出空集」。
- **修法**: §3 第 2 步补一行判据 ——「RC=0 但 stdout 无 `^ref: refs/heads/` 行 ⇒ 视为解析失败,
  落 `main-branch-unresolved`」; 并在 SC-5 的 fixture 里覆盖该形态 (它与「命令非零失败」是两个红窗)。
- **introduced_by_r1fix**: **true** (原版只有本地 `symbolic-ref` 一级, `ls-remote --symref` 是 m6 新增)

#### M-2 D-G/§6 援引的规范只管 timeout, 却被用来规定「其他非零也重试」—— 与 §5/SC-6 互相矛盾

- **锚点**: `proposal.md §6` (第 173-183 行) / `§5` 判据表第三行 (第 165 行) / `SC-6` (第 261 行) / `D-G`
- **Spec 声称**: 「§5 其他非零 / timeout → 按 §6 重试」;「§6 复用 `SKILL.md:257-259` 既有成文规范, 不新造参数」。
- **回源 (逐字)**:
  - `SKILL.md:259` — 「**timeout 触发** → max 3 attempts retry (backoff 5s/15s/45s) → 仍超时则 `fail` verdict」
  - `SKILL.md:260` — 「exit-code 映射 (per-backend, Aether 示例): `0` = success / **`1-126` = 错误 → `fail`** /
    `127` = binary not found → `no_ci_fallback` / `-SIGTERM` = subprocess timeout → **retry** → 仍失败则 `fail`」
- **矛盾**: 被援引的规范对「非 timeout 的非零退出」明文规定**直接 fail、不重试**; 只有 timeout 走 3 次退避。
  而 §5 表第三行与 SC-6 要求对「其他非零」也重试 3 次。**两个独立实现者会得到相反实现** —— 正是 §What
  Changes 开头 (第 92 行) 自设的判据「两个独立实现者读本节应得同一结果」所要消除的欠定, 且 SC-6 的
  「重试 3 次」断言会让照 :259/:260 实现的那位直接红。
- **实测放大**: `git ls-remote --exit-code --heads nosuchremote master` → **RC=128** (确定性失败, 不可能靠重试
  转好), 按 §5/SC-6 要白等 5+15+45=65s 才 fail。
- **额外注意**: 原版 (HEAD 版第 98 行) 援引的是 CLAUDE.md 硬约束 2「ls-remote 自身失败 → 重试几次再下结论」——
  那条**确实**支持「任何失败都重试」。R1-fix 为了「不新造参数」把它换成了一条**不支持该语义**的引用。
  这是 memory `exact-exception-condition` 的形状: 援引成文规范前须逐字核对确切触发条件。
- **修法**: §6 明写两分支 ——「timeout → 3 次退避重试 (沿用 :259); 非 timeout 非零 (含 128) → 不重试, 直接
  `main-branch-verify-failed`」, 并同步改 §5 表第三行与 SC-6; 或显式声明本 Spec 在 :260 之外**新增**一条
  「git 平面命令的失败一律重试」的口径并说明为何不与 :260 冲突 (不能再说「不新造」)。
- **introduced_by_r1fix**: **true**

#### M-3 §3 把可能陈旧的本地 ref 放在「权威」路径**之前**, 只在其失败时才回落 —— m6 的恒红对偶只修了一半

- **锚点**: `proposal.md §3` 第 121-125 行 + `D-C` (第 236 行)
- **Spec 自己的理由 (第 125 行)**: 「`refs/remotes/<remote>/HEAD` **只在 `clone` / `remote set-head` 时写入,
  `fetch` 不更新**」——这条事实同时蕴含**两个**失效维度: (i) ref **缺失** (脚本化 checkout 的容器);
  (ii) ref **陈旧** (上游默认分支改名后本地仍指旧名)。
- **§3 只处理了 (i)**: 权威路径的触发条件写死为「快路径**失败**时」。(ii) 情形下快路径**成功**返回旧名,
  权威路径永不执行。
- **后果**: 上游把默认分支从 `master` 改名为 `main` 之后, 本地 ref 仍解析出 `master` → §5 `ls-remote` exit 2
  → `verdict=fail` + `kind="main-branch-not-found"` + message「主分支 `master` 在 remote 上不存在」。
  **健康仓恒红, 且 kind 指向错误方向** (真因是本地 ref 陈旧, 不是主分支不存在), 排查者会去查 remote。
  判据「该信号在健康常态下应是什么值」: 应为 green/wait, 实为 fail ⇒ 恒红对偶未消除, 只是换了触发条件。
- **修法**: §5 表增一行 —— exit 2 **且** `resolved_from == "symbolic-ref"` 时, **先**用权威路径
  (`ls-remote --symref`) 重解析并复核一次, 仍不存在才落 `main-branch-not-found`; 陈旧命中时 message 须点明
  「本地 `refs/remotes/<remote>/HEAD` 陈旧, 建议 `git remote set-head <remote> -a`」。
- **introduced_by_r1fix**: **true** (两级解析是 R1-fix 新设计)

#### M-4 SC-9 的比较对象之一不存在 —— 恒绿 SC

- **锚点**: `proposal.md SC-9` (第 264 行) + `§2 约束 (承重)` (第 115 行)
- **SC-9 原文**: 「存在性核验用的 remote 与 **in-flight 查询用的 remote** | 同一个值 (来自同一 `remote` 参数) |
  两处各自取值的实现在此必红」。
- **回源**: `pre_merge_gate.py:366` → `backend.query_branch_in_flight(main_branch)`;
  `ci_backends/base.py` 抽象方法与 `aether.py:117` 实现的签名**只接受 branch, 不接受 remote**;
  aether 按 cwd 的 Forgejo remote 自行解析 —— **§2 第 115 行 Spec 自己也写了这一点** (「ls-remote 走 git 平面,
  CI backend 走 API 平面…二者不保证同源, 本 Spec **不消除**该限制」)。
- **⇒ 「in-flight 查询用的 remote」在代码里根本不是一个值**, 无从与之比较。SC-9 只能退化成「`_verify_branch_exists`
  收到的 remote 等于参数 remote」这种同义反复, **无论实现对错都绿**。这是 memory
  `feedback_verify_predicate_inputs_exist` 的形状: 判定机制的输入不存在。
- **修法**: 二选一 —— (a) 把 SC-9 改成真有红窗的表述:「`_resolve_main_branch` 与 `_verify_branch_exists`
  收到同一个 `remote` 值 (在 `_verify_branch_exists` 内硬编码 `origin` 的实现必红)」; (b) 承认跨平面无法钉,
  把 §2「承重」二字撤掉, 并把残留限制写成显式 known-limitation 而非 SC。
- **introduced_by_r1fix**: **true** (C5 的产物)

#### M-5 SC-11 没有任何机械红窗 —— 单测测不到、AB 套件按 Spec 自陈也测不到

- **锚点**: `proposal.md SC-11` (第 266 行) + `§Rule #6 已知套件缺口` (第 287 行)
- **SC-11 原文**: 「AI surface 义务照常触发 (`SKILL.md:252` (a) 项警告行) | 本修复使该义务**首次可能真触发**;
  若实现让它触发不到则红」。
- **回源 `SKILL.md:253`** (Spec 引的 `:252` 是「6. **路由决策**:」标题行, 实际内容在 :253 —— 见 m4):
  「AI **必须**在 workflow report 加警告行…」。**这是对 AI 的散文义务, 没有任何代码产出它** ——
  `compute_verdict` 只产 `raw_message` (`pre_merge_gate.py:210-214`), 不产该警告行。
- **且 Spec 自陈 (第 287 行)**: 「两套件均覆盖不到 C.2.4 的 D9 surface 措辞。本 Spec 新增的 `gate_error` /
  `main_branch_resolved` surface 同样落在该缺口内」。⇒ **单测无观测面, AB 无观测面**, SC-11 在两条通道上
  都不可能红。这与本项目 memory `feedback_falsifiable_evidence_for_binary_acceptance` /
  `feedback_false_green_dual_is_permanent_red` 直接冲突。
- **修法**: 要么把 SC-11 降级为 §Impact 里的一条文档同步项 (非 SC), 要么把它改成有观测面的断言 (例如
  「`not_applicable` 且 in-flight 空时 `raw_message` 必含 `not_applicable` 与 pc reason」—— 但注意
  `test_sc10_not_applicable_clean_green_with_message:641-643` **已经这么断言且今天就是绿的**, 见 M-6)。
- **introduced_by_r1fix**: **true**

#### M-6 SC-10 的「怎么会红」在 §Impact 强制的打桩方案下不成立 (SC-1 同形状)

- **锚点**: `proposal.md SC-10` (第 265 行) / `SC-1` (第 255 行) / `§Impact 处置 (Phase B 强制)` (第 344 行)
- **SC-10 断言**: 「`path_coverage.decision == "not_applicable"` 且 **PR CI 查询被跳过** (`assert_not_called`)」,
  红窗理由「现状 `main` ⇒ `git diff` RC=128 ⇒ 恒 `unknown` ⇒ 必红」。
- **实读推翻**: 同文件 `tests/test_pre_merge_gate.py` 已有

  ```
  :623  def test_sc9_not_applicable_with_inflight_waits_and_skips_pr_query
  :631      b.query_pr_ci.assert_not_called()
  :634  def test_sc10_not_applicable_clean_green_with_message
  :644      b.query_pr_ci.assert_not_called()
  ```

  它们经 `_ProbeCacheResetMixin` (:59-80) 把 `gate.evaluate_path_coverage` 整体打桩为 NA stub,
  **今天在 baseline 上是绿的**。任何按本文件既有写法实现新 SC-10 的人, 写出来的就是这两条的副本 ⇒
  **baseline 绿 ⇒ SC-10 的红窗自述为假**。
- **要让 SC-10 真红**必须用**真 git fixture** (临时仓 + master 分支 + 无 workflow 文件 + 真跑
  `evaluate_path_coverage`), 但: (a) Spec 全文未规定该 fixture; (b) 它与 mixin 对 `evaluate_path_coverage`
  的全局打桩冲突, 须另起不含 mixin 的测试类; (c) 与 `test_sc22` 的「suite 内零真实 git 子进程」卫生取向相悖。
  三点都没写 ⇒ 两个实现者必得不同结果。
- **SC-1 同形状**: 要求「**经 `main(argv)` 端到端**…`main_branch_resolved == {"name":"master","source":"symbolic-ref"}`」,
  但 §Impact 第 344 行**强制**为 `_resolve_main_branch` / `_verify_branch_exists` 提供模块级 mock 接缝。
  一旦打桩, SC-1 断言的就是自己的桩 (同义反复); 不打桩则 SC-1 依赖「测试进程 cwd 所在仓恰好有
  `refs/remotes/origin/HEAD` → master」——而 §3 的 m6 注记恰恰说该 ref 在容器里可能不存在 ⇒ SC-1 在
  Layer 2 容器里会走网络 `ls-remote` 或直接红。**「端到端 + 真解析 + 打桩隔离」三者不可同时成立**, Spec 三者全要。
- **修法**: 为 SC-1/SC-10 指定「临时 git 仓 fixture (本地 remote, 零网络) + 不继承 mixin 的新测试类」,
  并在 §Impact 明确它们是**唯二**允许真跑 git 子进程的用例; 同步扩 `test_sc22` 的白名单表述。
- **introduced_by_r1fix**: **true** (SC-10/11 是 C4 的新增, SC-1 的「经 main(argv)」是 M9 的新增)

#### M-7 新 SC 编号与同文件既有 `test_sc9..test_sc22` 正面碰撞 —— 原版 7 条不碰, 扩到 12 条才碰

- **锚点**: `proposal.md §Success Criteria` 表头 (第 251 行「原版 7 条 → **12 条**」) + `§Impact` 第 327 行
  (「`tests/test_pre_merge_gate.py` | 扩展 SC-1..SC-12」)
- **实读**: 同一文件已有 (均属 aria-plugin #122 那个 Spec 的编号体系)

  ```
  :623 test_sc9_...   :634 test_sc10_...  :647 test_sc11_...  :663 test_sc12_...
  :672 test_sc13_...  :683 test_sc15_...  :699 test_sc21_...  :710 test_sc22_...
  ```

- **后果**: 新 SC-9/10/11/12 落同一文件后, 文件内将出现两套语义完全不同的「SC-10」/「SC-12」;
  若落进**同一个 TestCase 类**且方法名前缀相同, Python 会**静默覆盖**先定义者 —— 被覆盖的既有测试
  不报错、直接从 suite 里消失 (而 §测试基线 只数总数 111, 数量掩护下更难发现)。原版 7 条 (SC-1..SC-7)
  与既有编号不重叠, 这个碰撞是 R1-fix 扩到 12 条**新造**的。
- **修法**: 新 SC 加 change 前缀 (如 `MBF-SC-1..12` / `test_mbf_sc4_...`), 并在 §Impact 写明命名空间约定 +
  Phase B 交付时核验 `unittest` 收集到的用例数 = 111 + 新增数 (防静默覆盖)。
- **introduced_by_r1fix**: **true**

#### M-8 §同形状兄弟位置 的枚举一错一漏 —— follow-up issue 会继承失实根因

- **锚点**: `proposal.md §同形状兄弟位置` (第 311-318 行) + `§Impact follow-up` (第 332 行)
- **(a) 错**: 表中第二行 `state-scanner/scripts/.../sync.py` 记「同族 (默认分支解析器)」, 首句更断言
  「同 plugin 内**已有两份**默认分支解析器」。**实读 `sync.py` 无此物**:

  ```
  $ grep -n "_resolve_default_branch|_DEFAULT_BRANCH_FALLBACKS|default_branch" \
        aria/skills/state-scanner/scripts/collectors/sync.py
  (零命中)
  ```

  `sync.py:46-50` 的 `_ORIGIN_HEAD_REFS` 是**子模块 `remote_commit` 的 SHA 回落链**, 在 `:384`
  以 `git rev-parse <ref>` 取 commit, 从不返回分支名。⇒ 「两份解析器」实为**一份** (`fetch_gate.py:108-128`)。
  失实来源可追: `fetch_gate.py:48-49` 注释写「Mirrors state-scanner sync.py::`_ORIGIN_HEAD_REFS` +
  `_DEFAULT_BRANCH_FALLBACKS`」、`:111` 写「Mirrors state-scanner sync.py::`_resolve_default_branch`」
  —— 本 Spec 逐字继承了这句注释而未去 target 核验 (memory `feedback_cross_doc_claim_verify_at_target`)。
- **(b) 漏**: 真正同形的第三处未列 —— `audit-engine/SKILL.md:389-390`:

  ```
  base = .aria/config 配置的 base  OR  git symbolic-ref refs/remotes/origin/HEAD
         (fallback origin/main → origin/master; 全部失败 → file-scope skip + warn, 不 crash)
  ```

  symbolic-ref + `main`/`master` 字面回落 + 全失败 fail-OPEN(skip+warn), 与 D-C 明令禁止的动作逐条对应,
  且它决定的是**审计范围**而非纯信息性输出。
- **后果**: 按此表开的 follow-up issue 会 (i) 指向一个不存在的缺陷位置, (ii) 漏掉一个真实位置。
  「修类不修实例」这一节因此没有真正把类划全。
- **修法**: 把 sync.py 一行删除或改述为「非同族 (SHA 回落链)」并顺手勘正 `fetch_gate.py:48-49/:111`
  的失实注释; 补 `audit-engine/SKILL.md:389-390` 进表与 follow-up。
- **introduced_by_r1fix**: **true** (§同形状兄弟位置 整节是 M3 的新增)

### Minor

#### m-1 §7 「五个消费点」未穷举 `verdict` 消费者

- **锚点**: `proposal.md §7` 表 (第 190-195 行)
- 漏 `workflow-runner/SKILL.md:332-336` 的 **Exit conditions** (「3. **verdict=fail** → 转为 stop (fatal);
  4. **verdict=green** → 继续 merge」, first-match-wins, **无 catch-all**) 与 `:313`/`:324`
  (`verdict: "wait"` 作为 `wait_recoverable` 的 triggered_by)。这是第 6/第 7 个消费点, 且与表中已列的
  `SKILL.md:252-255` 同性质 (封闭三分支)。
- 结论 (不新增第四枚举值) 不受影响 —— 但本节的立论方式**就是穷举**, 漏项削弱其证明力。
- **introduced_by_r1fix**: **true**

#### m-2 follow-up (b) 只保护 `main_branch_resolved`, 漏了同批新增且诊断价值更高的 `gate_error`

- **锚点**: `proposal.md §8` R1 注记 (第 226 行) + `§Impact follow-up (b)` (第 332 行)
- §8 正确指出 `gate_state_helper.write_gate_state()` 的具名参数集与 `workflow-state-schema.md:38-54`
  没有 `main_branch_resolved` 的位置 ⇒ 静默丢弃。**同一分析对 `gate_error` 完全成立且未做**:
  `write_gate_state(state, *, name, verdict, in_flight_runs, primitive_used, raw_message, intervals)`
  (`gate_state_helper.py:115-124`) 同样没有 `gate_error` 的位置。
- 后果: `verdict=fail` 时 workflow-runner「保留 gate_state 给 audit trail」(`SKILL.md:355`), 而 trail 里
  只剩 `status=fail`, **三个 kind 全部丢失** —— memory `fix-recurs-in-fallback` 的「有记录 ≠ 有路由」。
  §5 只对 `main-branch-not-found` 规定了 message 措辞, 另两个 kind 连 `raw_message` 兜底都没要求。
- **修法**: §3/§5 强制三个 kind 都写进 `raw_message` (它是被持久化的字段), 并把 `gate_error` 一并列进 follow-up (b)。
- **introduced_by_r1fix**: **true**

#### m-3 §Impact「其余 23 处会真起子进程」与 §4 自相矛盾

- **锚点**: `proposal.md §Impact 既有测试必然要动` 第 341 行 vs `§4` 第 135-139 行
- §4 钉死解析点在**三个早退之后**。24 个调用点中至少 3 个永远走不到解析点:
  `tests/test_pre_merge_gate.py:301` (`config={"enabled": False}`)、`:311` / `:321`
  (`resolve_ci_backend` 返回 None)。⇒ 会起子进程的上限是 **21**, 不是 23。
- 方向保守 (多打桩无害), 但这是两条新写条款之间的算术不一致, 且 Phase B 会照 23 去核对。
- **introduced_by_r1fix**: **true**

#### m-4 行号/自陈微漂移 4 处

- `§Impact` 第 344 行称 `_ProbeCacheResetMixin` 为 `:59-88` —— 实际类体是 **:59-80** (:83-86 是下一个测试
  组的 banner 注释, 属 `ComputeVerdictTests`)。
- `SC-11` 第 266 行引 `SKILL.md:252` 的「(a) 项警告行」—— :252 是标题行「6. **路由决策**:」,
  (a) 项警告行在 **:253**。
- `§Impact` SKILL.md 行 (第 328 行) 枚举了 `:242`/`:243`/`:167` 三处 `main` 字面量, **漏 `:270`**
  (`{"run_id": 3161, "branch": "main", ...}`, 全文 `--branch main`/`"main"` 共 3 处: 167/243/270),
  且 `:270` 恰在本 Spec 要改的 `:267-277` Output schema 代码块内。
- `§R1 审计吸收记录` C2 行 (第 367 行) 写处置为「§Impact **+ SC**」—— SC-1..SC-12 **无一条**覆盖
  SKILL.md 字面量勘正; 括号里的「(Impact 表已列三处)」才是真实处置。属假自陈。
- **introduced_by_r1fix**: **true**

---

## 已核验属实 (供收敛判断, 不计 finding)

- `pre_merge_gate.py`: `:47-49` 三常量 / `:300` 签名 `main_branch: str = "main"` / `:427` CLI `default="main"` /
  `:328`/`:338`/`:344` 三早退 / `:356-360` pc / `:366` in-flight / `:378-386` not_applicable 早退 — 全部逐字属实。
- `_build_output` 确为六键 (`:253-260`), SC-12 的契约基础成立。
- `aether.py:117-135` 引文逐字属实; `base.py:29` `not_found` 属实; `SKILL.md:279` 「gate 输出目前不产生」逐字属实。
- `SKILL.md:242` 尾部确有「`main_branch` 显式传真值 (本项目 `master`), 不依赖 CLI default」;
  `:243` 确为处方性指令行且标注「无条件执行」; `:167` 确含 `--branch main`。
- `gate_state_helper.py:32-34` 三常量 / `:147` `"status": verdict` 原样写入无校验 — 属实。
- `workflow-state-schema.md:38-54` `gate_state` 字段集 — 属实, 确无 `main_branch_resolved` 位置。
- 测试: `gate_check(` 24 处、显式传 `main_branch` 0 处、`test_sc12:663-670` 逐字断言
  `main_branch="main"`、`test_sc22:710-724` patch 的是 `pc_module.subprocess` — 全部属实。
- 计数: 46+25+40 = **111** 属实 (`tests/` 另有 2 个 `.sh`, Spec 已限定「三文件」)。
- AB: `ab-suite/phase-c-integrator-pre-merge-gate.json` **v1.1.0 / 7 fixtures**, id 逐个吻合
  (green, wait, wait_then_green, fail, NEG-1-malformed, NEG-2-timeout, NEG-3-internal-error-surface);
  `phase-c-integrator.json` 存在。§Rule #6 证据 1 属实。
- `db2e983` commit message 逐字含「不走 /skill-creator AB, 因 **hook 非 capability skill**」——
  §Rule #6 证据 3「先例不适用」属实。
- 本仓实测: `origin/HEAD` → `refs/remotes/origin/master`; `github/HEAD` 非 symbolic ref (RC=128);
  `git diff main...HEAD` RC=128 / `master...HEAD` RC=0 — §2/§Why 实测表属实。
- `SC-2` 关于 `run_gate` 归属的勘正属实: `def run_gate` 仅存在于 `state-scanner/scripts/phase1_gate.py:1031`。
- R1 汇总计数「5C + 10M + 6m = 21」与 aggregate 报告 `:142` 一致。

## Verdict

**FAIL** (1 Critical + 8 Major + 4 Minor)

Critical C-1 单独即构成阻断: 本 Spec 的承重兜底命令经实跑证明可在「主分支不存在」时返回 exit 0,
即闸门的机械兜底本身带着与被修缺陷同形的 fail-OPEN 洞。

**收敛拐点信号 (memory `marginal-return-negative` / `stop-adding-rounds`)**:
本轮 13 条 finding 中 **12 条 `introduced_by_r1fix=true`** (占比 92%), 且 R1 的 5C 在字面上确已各有落点。
即本轮产出**几乎全部来自 R1-fix 新写的内容**, 而非 R1 遗留。按「本轮 fix 引入的 major 占比 > 1/2 即到拐点」
的判据, 本 Spec 已进入「每轮 fix 引入约等量同形状缺陷」的区间。**建议 R3 不再加轮加席, 改为**:
(1) 先修 C-1 (可 1 行定音, 有实跑证据); (2) M-2/M-4/M-5/M-6/M-7 一律**做减法** —— 撤掉测不到的 SC、
撤掉不成立的「承重」措辞、撤掉与既有编号碰撞的编号, 而不是再写更多注记去论证它们成立;
(3) M-8 需要一次去 target 的实读 (顺带勘正 `fetch_gate.py` 的失实注释)。

## 轮次记录

| 轮次 | 席位 | 判定 | Findings | 备注 |
|---|---|---|---|---|
| R1 | 5 (tech-lead / backend-architect / qa-engineer / code-reviewer / knowledge-manager) | 5/5 REVISE · FAIL | 5C + 10M + 6m = 21 | 结构性重写 (+266/-58) |
| R2 | code-reviewer (本报告) | **REVISE · FAIL** | **1C + 8M + 4m = 13** | 12/13 由 R1-fix 新引入 (92%) ⇒ 边际产出拐点信号 |

**本轮方法**: 全部 finding 均经只读实跑或实读回源 —— 3 个一次性 git fixture (分层分支 / 空仓 / 不存在 remote)
验证 `ls-remote` 语义; 22 处行号断言逐个 `awk` 回源; 4 处跨文件声称去 target 核验。零文件修改, 零 commit/push。
