---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T18:51:56.159Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec Round 1 审计报告 — backend-architect

被审对象: `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md` (Level 2, 179 行)

镜头: 实现可行性与接口契约 — `<remote>` 参数存在性/来源、`git symbolic-ref` / `git ls-remote` 在真实仓库(含子模块)的实跑行为、D3 存在性核验对现有 backend 抽象层与 111-test 基线的实际影响、fail-CLOSED 方向性在实现层是否会在新写的分支里重新引入 fail-OPEN。

**方法论**: 已完整读 proposal.md 全文 + `pre_merge_gate.py` (444 行全文) + `ci_backends/{aether,base,__init__,github_actions}.py` 全文 + `path_coverage.py` 全文 (508 行) + `test_pre_merge_gate.py` 关键区段 (imports/mixin/GateCheckTests/PathCoverageGateTests) + `SKILL.md` §C.2.4 相关段落。所有 grep/实跑命令均在 `/home/dev/Aria` 工作树内执行 (只读, 未改动任何文件)。

---

## 审计结论

Spec 对缺陷本身的诊断**准确且已实证** —— `pre_merge_gate.py:300` / `:427` 两处 `default="main"`、`ci_backends/aether.py:117-135` `query_branch_in_flight` 把"分支不存在"与"分支无 in-flight run"合流为同一 `InFlightStatus(runs=[])` 的机制描述, 逐字核对与真实代码一致。`SKILL.md:242` 引文锚点核对准确。

但 Spec 提出的补救方案 (§2/§3, D2/D3 — 作者自称"承重条款") 在**实现层面存在两个 Critical 级别的欠定问题**, 且都指向同一个方向性风险: **补救方案自己引入的新分支, 有可能重新造出一个未声明的隐式默认值 / 悄悄放行真实副作用**, 这正是本 Spec 要根治的病灶的同构复现 (本项目 memory `feedback_fix_recurs_in_its_own_fallback_path` 命中)。另有 2 项 Major + 1 项 Minor, 详见下方 FINDINGS。

### 已验证为准确的部分 (非 finding, 供参考)

- `pre_merge_gate.py:300` `main_branch: str = "main",` — 实读逐字匹配。
- `pre_merge_gate.py:427` `parser.add_argument("--main-branch", default="main", ...)` — 实读逐字匹配。
- `ci_backends/aether.py:117-135` `query_branch_in_flight` 的"不存在"与"无 run"合流机制 — 实读逐字匹配 Spec 引文。
- `SKILL.md:242` 引文「`main_branch` 显式传真值 (本项目 `master`), 不依赖 CLI default」— 实读逐字匹配。
- SC-1 的核心断言 (`refs/remotes/origin/HEAD` → `master`) — 本仓实跑验证为真 (见 FINDINGS 中 F1 的实跑记录, `origin` 分支下确认无误)。
- 测试基线"现 111 tests" — `pytest --collect-only` 实跑确认: `111 tests collected`, 与 Spec 陈述一致。

---

## FINDINGS 详述

### F1 (Critical) — `<remote>` 参数在全代码库中不存在, Spec 未定义其来源

Spec §2/§3 (proposal.md:79-101, D2/D3 at :126-128, SC-1/4/5/6 at :139-144) 反复使用 `<remote>` 作为已知/给定量:

```
git symbolic-ref refs/remotes/<remote>/HEAD
git ls-remote --exit-code --heads <remote> <main_branch>
```

实测: 全代码库 grep 「remote」于 `pre_merge_gate.py` 与 `ci_backends/*.py` **零命中** —— `gate_check()` 现有签名是 `gate_check(pr_branch, main_branch="main", config=None)` (:298-302), CLI 只有 `--pr-branch` / `--main-branch` / `--config-file` 三个参数 (:426-432), `AetherBackend.query_branch_in_flight(self, branch)` 也不接受 remote 参数。`<remote>` 在现有代码里**不存在任何绑定点**。

Spec 全文 (D1-D7 决策表、What Changes、Impact 表、全部 7 条 SC) **没有一处**声明: (a) `<remote>` 是否要做成新 CLI flag / 新函数参数; (b) 若不做成参数, 硬编码成什么字面量; (c) 若硬编码 `"origin"`, 这个决策本身要不要留痕 (它本身就是本 Spec 正在消灭的那类"未声明缺省值")。

本仓实跑证实这不是纸面问题 —— 本仓 (含 CLAUDE.md 自己记载的"多远程推送"惯例) 真实存在两个 remote, 但只有一个有 HEAD symref:

```
$ git remote -v
github  git@github.com:10CG/Aria.git (fetch/push)
origin  ssh://forgejo@forgejo.10cg.pub/10CG/Aria.git (fetch/push)

$ git symbolic-ref refs/remotes/origin/HEAD
refs/remotes/origin/master
$ echo $?
0

$ git symbolic-ref refs/remotes/github/HEAD
fatal: ref refs/remotes/github/HEAD is not a symbolic ref
$ echo $?
128
```

`github` remote 从未做过 `git remote set-head github -a` (这是标准 git 行为: 只有 clone 时使用的 remote 会自动获得 HEAD symref), 故 `refs/remotes/github/HEAD` 在任何全新 clone 里天然缺失, 不是本仓的配置疏漏。若 Phase B 实现者对 `<remote>` 的解释稍有偏差 (例如遍历 `git remote` 列表取第一个字母序 / 取 `git branch --show-current` 的 upstream remote / 未来某个调用方偏好 `github`), SC-5 的"解析失败⇒error"分支会在**完全合规的多远程仓库**上意外触发, 把一个健康仓库判成"闸门瘫痪"。反之, 若实现者悄悄硬编码 `"origin"` 又不在 SC/D 表留痕, 就是把"哪个 remote"这个决策从"未声明缺省值"平移成"未声明硬编码常量"—— 换了皮的同一个病。

**为什么是 Critical 而非 Major**: D3 被作者自己标注为"本 Spec 的承重条款"; 承重条款的输入参数完全未定义, Phase B 无法在不擅自决策的情况下写出这段代码, 而擅自决策 (硬编码且不留痕) 正是本 Spec 存在的理由所指向的反模式, 对自身递归复发。

**锚点**: `proposal.md:79-101,126-128,139-144` (Spec 侧); `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py:298-302,426-432` (代码侧, 已实读确认 `<remote>` 无绑定点); 实跑命令与输出见上。

---

### F2 (Critical) — 「既有用例逐字不改」与代码实测矛盾; 且现有的"套件零真实 git 子进程"卫生断言对新调用拓扑失明

Spec Impact 表 (proposal.md:166) 明确声明: `test_pre_merge_gate.py` 的变更是「扩展 — SC-1..SC-7 (**既有用例逐字不改**)」。rule6_note (proposal.md:110-118) 的 substitute 论证也建立在"改动面小、可控"这个前提上。

实测 (`grep -n 'gate\.gate_check(' tests/test_pre_merge_gate.py | grep -v main_branch`) 显示 **23 处**现有调用点在不传 `main_branch=` 的情况下调用 `gate.gate_check(...)`, 全部依赖函数签名缺省值 (行号含 192/210/226/234/247/267/282/301/311/321/373/383/394/524/628/638/651/654/667/675/688/695/708/723)。D1 一旦把该缺省从 `"main"` 改成 `None` 并触发 §2 的新解析逻辑, 这 23 处调用的**行为语义全部改变**, 并非"不改"。

具体而言, 至少两类既有测试会被直接打破, 且性质不同 (一个是断言值错, 一个是隐蔽副作用泄漏):

**(a) 断言值直接错误** —— `test_sc12_default_true_lock` (`tests/test_pre_merge_gate.py:664-670`):
```python
def test_sc12_default_true_lock(self) -> None:
    b = self._backend()
    with mock.patch.object(gate, "resolve_ci_backend", return_value=b):
        gate.gate_check(pr_branch="feat/x", config={})
    self.pc_eval.assert_called_once_with(
        main_branch="main", pr_branch="feat/x"
    )
```
该测试显式断言"不传 main_branch 时, `evaluate_path_coverage` 收到的是字面量 `"main"`"—— 这正是 Spec 要治的那个 bug 的断言化。D1 落地后此断言必错 (新解析值不再是字面 `"main"`), 该测试必须重写, 不是"逐字不改"。

**(b) 更深的问题 —— 本仓已有的"套件零真实 git 子进程"卫生断言对新调用拓扑结构性失明**:

`tests/test_pre_merge_gate.py:59-76` 的 `_ProbeCacheResetMixin.setUp()` 全局 patch `gate.evaluate_path_coverage` (被全部 9 个测试类继承), docstring 原话:

```
v1.65.0+ (#122): 同时统一 patch gate.evaluate_path_coverage (QA-3 隔离方法论)
— 既有测试不因 path_coverage_enabled 默认 true 触发真实 git 子进程 (SC-22)。
```

这段 mixin 本身就是本项目**上一次**为同一类问题 (新增一个默认开启、内部会调用真实 git 的能力) 专门建的机械防线。配套的显式断言测试是 `test_sc22_no_real_git_subprocess_in_suite` (`:710-724`):

```python
def test_sc22_no_real_git_subprocess_in_suite(self) -> None:
    import path_coverage as pc_module
    def _forbidden(*_a, **_k):
        raise AssertionError("real git subprocess spawned in unit suite")
    with mock.patch.object(pc_module.subprocess, "run", _forbidden):
        ...
        out = gate.gate_check(pr_branch="feat/x")
    self.assertEqual(out["verdict"], "green")
```

这个断言只 patch 了 `path_coverage` 模块的 `subprocess.run` 引用 —— 它是为"防止 `evaluate_path_coverage` 泄漏真实 git 调用"这一具体威胁模型定制的, 拓扑上**看不到**任何绑定在 `gate` (即 `pre_merge_gate.py`) 自己模块命名空间下的新 subprocess 调用。而 D3 明确要求存在性核验"放 gate 层" (:127), 即新的 `git symbolic-ref` / `git ls-remote` 调用天然要写进 `pre_merge_gate.py` 自身 (该文件当前 `import` 列表里**没有 `subprocess`**, 是全新引入)。

后果: 一旦 D1+D2+D3 落地且 Phase B 未同步给 `_ProbeCacheResetMixin` 加第三个全局 patch (Spec 全文未提及需要这么做, 也未命名这个新解析函数该叫什么), 上面 23 个既有调用点在测试运行期间会真实执行 `git symbolic-ref` / `git ls-remote` 子进程 (打到跑测试的机器当时的实际 git 配置上, 非确定性、环境耦合) —— 且 `test_sc22` 自己反而会**误报通过** (它监视的是错误的 subprocess 引用, 抓不到新泄漏点), 与其名称"no_real_git_subprocess_in_suite"承诺的东西背道而驰。这是「测出绿但没测到该测的东西」的典型模式 (本项目 memory `feedback_test_asserts_what_its_name_claims` 命中)。

**为什么是 Critical**: (1) 直接证伪 Spec 一处具体书面声明 ("既有用例逐字不改"), 该声明是 rule6_note substitute 论证与 D7 (PATCH 定级) 风险评估的依据之一, 声明失实会连带动摇这两处的结论; (2) 影响面不是"个别测试需要调整"这种量级 —— 是 23 个调用点 + 1 个专门为同类风险设的卫生防线被绕过, 且这条防线的绕过是**静默的** (test_sc22 会继续 PASS, 不会红)。

**锚点**: `proposal.md:166` (Impact 表"既有用例逐字不改"); `aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py:59-76` (`_ProbeCacheResetMixin.setUp`, 已实读); `:664-670` (`test_sc12_default_true_lock`, 已实读); `:710-724` (`test_sc22_no_real_git_subprocess_in_suite`, 已实读); 23 处调用点行号见上 (grep 实跑确认)。

---

### F3 (Major) — D3 插入点表述遗漏 `evaluate_path_coverage` 这一更早的 `main_branch` 消费点

proposal.md §3 (:90) 原话: "查 in-flight **之前**, 独立核验该分支在目标 remote 上存在"。这句话把插入点锚定在 `backend.query_branch_in_flight(main_branch)` 调用 (`pre_merge_gate.py:366`) 之前。

但实读 `gate_check()` 现有控制流 (:354-366) 发现, **同一个 `main_branch` 变量在此之前已经被消费一次**:

```python
354	    pc: dict[str, Any] | None = None
355	    if cfg.get("path_coverage_enabled", True):
356	        pc = evaluate_path_coverage(
357	            main_branch=main_branch, pr_branch=pr_branch
358	        )
359	    ...
365	    try:
366	        in_flight = backend.query_branch_in_flight(main_branch)
```

`path_coverage_enabled` 默认 `True` (`DEFAULT_CONFIG` :64), 所以这不是边缘配置 —— 默认路径下 `evaluate_path_coverage` 几乎总会先于 in-flight 查询执行, 且它自己的 `_evaluate()` (`path_coverage.py:434-445`) 会拿 `main_branch` 去跑 `git diff ...{main_branch}...{pr_branch}`。

Spec 未交代: 若 `main_branch` 解析/存在性核验只插在 :366 之前 (严格按 §3 字面), 则 :356-358 这次调用会先拿到**未解析** (`None`) 或**未验证存在性**的值。`None` 会被拼进 `f"{main_branch}...{pr_branch}"` 变成字面串 `"None...feat/x"` 传给 git diff, 触发 `path_coverage.py` 规则 1 的 `git-diff-failed` → `unknown` → fail-toward-covered (不会 fail-OPEN, 但会把根因诊断误导成"path_coverage 评估失败", 而真实原因是"main_branch 还没解析", SC-4/SC-5 想要的清晰错误信息在这条路径上不会出现 —— 与 D5"回显真值使假绿在 surface 可见"的意图直接冲突)。若实现者反而把解析核验提到函数最顶端 (更合理的选择), Spec 也没有明说, 相当于把一个会影响两个消费点执行顺序的决策留给 Phase B 隐式做出。

**锚点**: `proposal.md:90` (D3 原文); `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py:354-366` (已实读, 确认 :356-358 是比 :366 更早的同变量消费点)。

---

### F4 (Major) — `ls-remote`/`symbolic-ref` 失败判据机制与超时值未钉死; 网络不可达时会挂起而非快速失败

D4 (proposal.md:128) 与 SC-6 (:144) 要求: "ls-remote 自身失败 ⇒ 重试后仍失败则 error, 不得判存在也不得判不存在"; SC-6 的"怎么会红"栏还专门点名"把 ls-remote 失败当成『分支不存在』的实现 → 误报"这个反模式。但 Spec 全文没有指出**用什么信号**在代码里区分「分支不存在」(SC-4, 不该重试) 与「查询本身失败」(SC-6, 该重试)。

本仓实跑验证了这个区分在 git 层面确实可行, 但 Spec 没有把它钉下来:

```
$ git ls-remote --exit-code --heads origin master
71bdd60fc62fce940ba9c88117badef21b19c1a0  refs/heads/master
exit=0

$ git ls-remote --exit-code --heads origin this-branch-does-not-exist-xyz123
exit=2                                          # 远端可达, 确认分支不存在 → SC-4 该走这支, 不重试

$ git ls-remote --exit-code --heads not-a-registered-remote master
fatal: 'not-a-registered-remote' does not appear to be a git repository
exit=128                                        # remote 名本身无效 → SC-6 该走这支

$ timeout 5 git ls-remote --exit-code --heads ssh://forgejo@10.255.255.1/10CG/Aria.git master
exit=124                                        # 用我外加的 timeout 才拿到确定结果 —— 说明 git 本身对不可达主机没有内建超时, 会挂起
```

三个观测:
1. exit code 2 与其余非零 exit code 在真实 git 行为里是可区分的 (2 = "远端可达但无匹配 ref", 其余 = 各类失败) —— 这条判别式是可实现的, 但 Spec 正文没有写"用 exit_code == 2 判定『不存在』, 其余判定『查询失败』", 只写了目标状态没写机制, 让"该判别式"这件事完全留给 Phase B 默会, 而 SC-6 自己指出的反模式恰恰是"没分清这两者", 说明作者知道这里容易踩错却没有把避坑机制写进 Spec 本体。
2. 真实网络不可达时, `git ls-remote` **不会自行超时**, 会挂起 (需要我外部套 `timeout` 才能拿到结果)。Spec 的"ls-remote 自身失败 → 重试"这句话隐含"会失败", 但没有规定给这次新 subprocess 调用设多长超时——没有超时, "重试" 无从触发, 挂起会直接卡住整个 merge gate。
3. `pre_merge_gate.py` 目前**零**行 git/subprocess 代码, 无可直接复用的超时/重试基础设施: `path_coverage.py._run_git` (`:78-102`) 是私有函数、单次调用、`_GIT_TIMEOUT=15` 但**无重试**; `AetherBackend._run_with_retry` (`ci_backends/aether.py:164-187`) 有重试 + backoff `(5,15,45)`, 但绑定在 `self.binary` (即 `aether` 可执行文件) 上, 不是给任意 `git` 命令用的通用设施。Spec 没有指明新代码复用哪一个模式、还是照抄 `RETRY_BACKOFF` 常量、还是另起一套——这直接影响 SC-6 的可测性 (测试要 mock 多少次调用、backoff 数值要不要断言)。

**为什么是 Major 而非 Critical**: 目标状态本身 (SC-4/SC-5/SC-6 三条负控/正控) 陈述清楚, 且区分机制在 git 层确实存在、可实现, 不是逻辑上无法达成; 缺的是"钉死到字符级"这一步, 一个仔细的实现者读 git 文档能补上, 但这类"缺具体机制只给目标"的 Spec 缺口, 本项目已有实证会导致两个独立实现者对同一句话给出相反结果 (memory `feedback_spec_underdetermination_two_implementer_test`)。

**锚点**: `proposal.md:98,128,144` (D4/SC-6 原文); `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py` 全文 (已确认零 subprocess/git 代码); `aria/skills/phase-c-integrator/scripts/path_coverage.py:78-102` (`_run_git`, 已实读, 私有/单次/无重试); `aria/skills/phase-c-integrator/scripts/ci_backends/aether.py:164-187` (`_run_with_retry`, 已实读, 绑定 `self.binary`); 实跑命令与输出见上。

---

### F5 (Minor) — D5 承诺的 `main_branch_resolved` 输出字段未列入 Impact 表要同步的 SKILL.md 位置

D5 (proposal.md:129) 承诺 `gate_result` 新增 `main_branch_resolved` + 来源字段。proposal.md Impact 表 (:167) 只列了 `SKILL.md:242` (散文勘正, 讲 `main_branch` 该怎么传参), 但 `SKILL.md:264-277` 是**另一处、独立的** Output schema JSON 范例块 (完整列出 `verdict`/`pr_ci_status`/`in_flight_runs`/`primitive_used`/`primitive_version_sha`/`raw_message`/`path_coverage` 七键), 且紧随其后的 :279 有一段专门的"枚举归层注记", 逐字段交代每个可选键在哪些早退分支存在/不存在 (例如 `path_coverage` 的"additive 可选键"约定)。这是本项目对该文件已经建立的强先例——新增输出键必须在这个 schema 块里落一行。

Spec 的 Impact 表没有把 SKILL.md:264-279 这个位置列进变更范围, 若 Phase B 只照 Impact 表字面执行, `main_branch_resolved` 会成为代码里存在但文档 schema 块里查不到的字段, 违反 CLAUDE.md 不可协商规则 #3 (文档与代码必须同步)。

**为什么是 Minor**: 不影响运行时正确性/fail-closed 方向性, 是纯文档完整性缺口, 且修法直接 (照抄 :279 已有的注记范式加一行即可), Phase B 阶段容易在 code review 中被发现并补上。

**锚点**: `proposal.md:129,167` (D5/Impact 表); `aria/skills/phase-c-integrator/SKILL.md:242` (Impact 表列出的位置) vs `SKILL.md:264-279` (实际 schema 定义位置, 已实读, 两者是不同锚点)。

---

## Verdict

**FAIL** (≥1 Critical: F1, F2)

判据回顾: PASS = 0 Critical + 0 Major; PASS_WITH_WARNINGS = 0 Critical + ≥1 Major; FAIL = ≥1 Critical。本轮识别 2 Critical + 2 Major + 1 Minor ⇒ FAIL。

两个 Critical 都不是"方向错了"意义上的缺陷 (Spec 的诊断与目标状态本身是对的, D2/D3/D4 的"宁可 error 不可回落缺省"这个方向性判断也是对的), 而是"承重条款缺少可实现的具体机制"与"变更影响面自述失实"—— 都在 Phase B 落地前可以修复, 不构成推翻 Spec 整体方向的理由, 但会在当前文本状态下让 Phase B 实现者被迫自行拍板两个未声明的设计决策 (`<remote>` 取值来源 / 新 subprocess 调用的测试隔离机制), 而这两个决策点恰好都落在"未声明的隐式默认值/未受控副作用"这个 Spec 本体正在治理的问题类型上。建议 Revise 后收窄 §2/§3 与 Impact 表, 补齐 `<remote>` 的显式来源声明与测试隔离机制, 再进入下一轮。

## 轮次记录

- **Round 1** (本轮, backend-architect 席位): 实读 proposal.md 全文 + 5 个真实代码文件全文/关键区段 + 实跑 6 组只读 git 命令 (symbolic-ref × 2, ls-remote × 4 变体, 含子模块场景) + pytest --collect-only 验证测试基线计数。产出 2 Critical + 2 Major + 1 Minor, verdict=FAIL。本报告为 post_spec 检查点第一轮; 收敛判定 (converged) 留给编排层按四元组比较其余席位后裁定, 本席位不单方面宣称收敛。
