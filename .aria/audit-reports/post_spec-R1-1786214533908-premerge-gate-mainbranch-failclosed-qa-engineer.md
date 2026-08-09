---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T19:05:01.293Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R1 — premerge-gate-mainbranch-failclosed — qa-engineer

## 审计结论

镜头: 测试策略与可证伪性。方法: 通读 `proposal.md` 全文 (179 行), 实读 `pre_merge_gate.py` (444 行全文)、`ci_backends/aether.py` (270 行全文)、`path_coverage.py` (509 行全文)、`test_pre_merge_gate.py` (748 行全文)、`SKILL.md` §C.2.4 相关段 (155-300 行区间), 并实跑 `pytest` / `unittest discover` / `git ls-remote` / `git symbolic-ref` / `aether ci status` 等命令核验 Spec 的经验性主张。

**头号发现 (Critical)**: Spec 引入的新 verdict 值 `error` 是一个未被下游任何消费面接纳的「第四态」——`pre_merge_gate.py` 的 verdict 常量 (`VERDICT_GREEN/WAIT/FAIL`, 三值)、`SKILL.md` 的 Output schema (`"green" | "wait" | "fail"`)、`SKILL.md` 的路由决策表 (green/wait/fail 三分支, 无 default/else)、`SKILL.md` 明确以「**三态结果**」命名整个机制 (§C.2.4 正文 :170), 全部是封闭三态设计。Spec 的 Impact 表只字未提这四处需要同步; Rule #6 自评「零运行时指令流程新增」也因此站不住——若路由表要新增第四分支, 那正是「处方性·运行时指令面」变更。这与 Spec 自己引用的 memory `feedback_invariant_needs_failclosed_default` (「枚举分区必须 fail-CLOSED」) 在自己身上失效, 构成自反性缺陷。

其余 Major 发现集中在: (a) `<remote>` 是什么从未钉死, 而本仓恰好有 2 个语义不同的 remote; (b) 既有 46 个 `gate_check` 端到端测试 100% 未显式传 `main_branch`, 修复后会在毫无防备的情况下各新增 2 次真实 subprocess 调用 (其中 ls-remote 会打真网络) ——本次审计过程中就实测到一次真实的瞬时网络失败, 印证了这不是纸面风险; (c) SC-3/SC-7 两条负控在新的存在性核验语义下隐含一个未言明的新 mock 依赖; (d) SC-1 若不经 `main()`/argv 端到端验证, 有 collapse 成浅层测试的风险。

SC 表本身的场景/期望描述总体是清晰、可证伪的 (这点应予肯定); 问题集中在「实现这些 SC 会牵连出的、Spec 未覆盖的下游契约面」和「新增 SC 的 fixture 会不会在断言前就打真实 I/O」。

## 逐 SC 复核

### SC-1 — CLI 不传 `--main-branch` → 从 `refs/remotes/origin/HEAD` 解析出 `master`

**「怎么会红」核实**: 成立。`_build_output()` (`pre_merge_gate.py:232-263`) 当前产出的字典只有 6 个键 (`verdict/pr_ci_status/in_flight_runs/primitive_used/primitive_version_sha/raw_message`, 外加可选 `path_coverage`), **没有 `main_branch_resolved` 键**。任何断言 `out["main_branch_resolved"] == "master"` 在当前代码上必然失败 (KeyError 或空值不等), 且当前查询目标恒为字面量 `"main"`(`:427`)。baseline-red 成立。

**实现踩坑点 (Major, 见交叉发现 M4)**: SC-1 场景描述为「**CLI** 不传 `--main-branch`」, 与 SC-2「直接调 `gate_check(...)` 不传 `main_branch`」并列, 暗示两者测的是两条不同代码路径 (CLI argparse 默认值 vs. 函数签名默认值)。但 `main()` (`:424-440`) 内联构建 `argparse.ArgumentParser`, 没有可单独调用的 `build_parser()`。要如实测「CLI 不传参」这一命题, 测试必须调用 `gate.main(argv=[...])` 并捕获 stdout 解析 JSON——这是 111 个既有用例里**从未出现过**的调用形态 (全部既有 `GateCheckTests` 都直调 `gate.gate_check(...)`)。Spec 没有点出这个新测试脚手架需求, 存在被简化为「只断言 `parser.get_default('main_branch') is None`」的风险——那样就只验证了 argparse 默认值本身, 没有验证「解析出 master 并据此查询」这条端到端链路, 与「期望」列承诺的内容脱节。

### SC-2 — 直接调 `gate_check(...)` 不传 `main_branch`

**「怎么会红」核实**: 成立, 理由同 SC-1 (键不存在 + 现状默认值恒为 `"main"`)。

**文字缺陷 (Minor, 见 m1)**: 场景列写的是「直接调 `run_gate(...)`」(proposal.md:140)。全仓 `grep -rn "run_gate"` 命中的唯一符号是 `tests/test_submodule_gate.sh:126` 里一个与本 Spec无关的 bash 函数 (子模块回滚检测测试, 不同子系统)。本 Spec 真正指的函数是 `pre_merge_gate.py:298` 的 `gate_check`。不影响理解 (上下文清楚), 但与本 Spec 全篇「逐行号/逐字引用真实代码」的高精度风格不符, 值得订正。

**「唯一覆盖内部调用路径」的论证核实**: 成立——只要 CLI 侧 (`main()`) 总是显式把 `args.main_branch` (无论其值是 `None` 还是历史遗留的 `"main"`) 传给 `gate_check(main_branch=...)`, CLI 路径就永远不会触发 `gate_check` 自身的函数级默认值; SC-2 确实是唯一在「完全省略该实参」意义上测试函数签名默认值的用例。设计上无缺陷。

### SC-3 — 显式传 `--main-branch master` (负控)

**是否是真负控**: 部分成立, 但描述「行为与现状一致 (不因本 change 改变)」不完全准确。D3 (proposal.md:126-128, 90-98) 写明存在性核验「查 in-flight **之前**」执行, 且 SC-4 的场景 (`--main-branch main`, **显式**传参的不存在分支) 本身就证明存在性核验对**显式传参**同样生效——即存在性核验是无条件插入的新步骤, 不是只发生在「从 symbolic-ref 解析」这条支路。因此 SC-3 描述的「显式传 master」在修复后实际上**新增经过**了一次 `git ls-remote --exit-code --heads <remote> master` 调用, 只是因为 master 确实存在而结果不变——这不是「零变化」, 而是「新步骤 + 良性结果」。

**踩坑点 (Major, 见交叉发现 M3)**: 若该 SC-3 fixture 没有显式 mock「ls-remote 返回存在」, 会出现两种坏结果之一: 要么真的对外发起网络调用 (打破套件的隔离性/确定性, 与既有 `test_sc22_no_real_git_subprocess_in_suite` 建立的卫生先例背道而驰), 要么如果实现层选择「未打桩就报错」的保守测试基座 (镜像 SC-22 的 `_forbidden` 模式), SC-3 会因为「fixture 没预料到新依赖」而伪红——红的原因不是「改坏了既有路径」, 而是「测试基座没跟上新代码路径」, 恰恰会被误判为负控生效, 实际上只是没写全 mock。

### SC-4 — 传一个不存在的分支 (`--main-branch main`) → verdict=error

**「怎么会红」核实 (经验性验证)**: 成立且已实测。`git ls-remote --exit-code --heads origin main` 在本仓实际执行结果为 **exit code 2** (无匹配 ref), 而 `git ls-remote --exit-code --heads origin master` 执行结果为 **exit code 0** + 返回 SHA。两者可用退出码区分, SC-4 (「不存在」) 与 SC-6 (「查询本身失败」, 见下, 应为 128 一类的 fatal 错误) 在机制上确实可以被区分实现, D4 的「两个方向都不能猜」在技术上是可落地的判据, 未发现不可证伪问题。

**当前代码确认**: `AetherBackend.query_branch_in_flight` (`ci_backends/aether.py:117-135`, 尤其 `:121-124`) 目前对「分支不存在」和「分支无 in-flight run」两种情况都返回 `ok=True, data.runs=[]`, 无法区分——这与 Spec 的「Why」section 描述完全一致, 已用 `aether ci status --branch main --in-flight --json` 实测复现, 返回 `{"status":"ok","data":{...,"runs":[]}}` (exit 0)。

**留痕 (与 M2 相关)**: message 要求「含分支名与 remote 名」——「remote 名」这个字段目前在整个 `pre_merge_gate.py` / `ci_backends/` 里没有任何先例 (`grep -rn "remote" scripts/*.py` 零命中), 是本 Spec 引入的全新概念, 但「remote 是什么」这件事本身在 Spec 里未钉死 (见 M1)。

### SC-5 — `git symbolic-ref refs/remotes/<remote>/HEAD` 失败 → verdict=error, 不得回落字面量

**「怎么会红」核实**: 成立, 但要指出一个通用性质: 由于当前代码里**根本不存在** `verdict="error"` 这个值 (三个常量 `VERDICT_GREEN/WAIT/FAIL` 之外没有第四个, `pre_merge_gate.py:47-49`), 任何断言 `verdict=="error"` 在 baseline 上都必然为红, 不论 fixture 是否真的精确命中了「symbolic-ref 失败」这个具体分支。这不代表 SC-5 无效 (它仍然是一个真实要修的行为), 但意味着「baseline-red」这一项对 SC-4/SC-5/SC-6 而言证明力较弱——真正有证明力的是「post-fix 是否精确地只在该场景下产出 error, 其余场景不受影响」, Spec 的 SC 表本身没有反向断言 (例如「symbolic-ref 成功时不得产出 error」), 建议 Phase B 在实现测试时补一条紧邻的正相位断言, 否则「怎么会红」这一列的证明力主要来自枚举值本身不存在, 而非精确命中失败分支。

**fixture 可行性 (Major, 见交叉发现 M2/M5)**: `git symbolic-ref` 是纯本地操作 (无网络), 用 `mock.patch` 在 subprocess 边界打桩即可低成本模拟失败, 技术上可行。但 Spec 未指明这条新 git 调用的实现位置 (`pre_merge_gate.py` 新增私有函数? 还是复用 `path_coverage.py` 已有的 `_run_git()` 契约, 见 `path_coverage.py:78-102`, 该函数已经有「never raises, 返回 (ok, out, err)」的现成契约, 与本 Spec 要做的事情几乎同形)。未点名复用路径, 有重复造轮子风险, 但不构成阻断性缺陷。

### SC-6 — `git ls-remote` 自身失败 (重试后仍失败) → verdict=error

**「怎么会红」核实**: 逻辑成立 (两个方向都会被 SC-6 抓到, 上文 SC-4 段已验证 exit code 2 vs 128 的可区分性)。

**踩坑点 (Major, 见交叉发现 M5)**: 「重试后仍失败」隐含一个重试策略 (次数/backoff), 但 D4 只说「对齐 CLAUDE.md 硬约束 2」, 未给出具体参数。现有 `AetherBackend._run_with_retry` 的重试是 `RETRY_BACKOFF=(5,15,45)` 秒、`MAX_RETRY_ATTEMPTS=3` (`ci_backends/aether.py:38-39, 164-187`), 真实 `time.sleep`。若 SC-6 的实现照搬这套真实 sleep 而测试不 mock `time.sleep`, 单条测试会真实耗时数十秒; 若另起一套不同的重试参数, 又会和现有 Aether 重试语义不一致, 增加认知负担。两个方向 Spec 都没有明确, 需 Phase B 自行决定并在测试里显式 mock 时间。

### SC-7 — 分支存在且有 in-flight run (负控) → verdict 与现状一致 (wait)

**是否是真负控**: 与 SC-3 同款问题 (见 M3)——存在性核验现在无条件插入, SC-7 的 fixture 同样需要显式 mock「该分支存在」, 否则同样有打真网络或伪红的风险。SC-7 的场景描述比 SC-3 稍好 (「分支存在**且**有 in-flight run」至少显式写出了「存在」这个前提), 但仍未点明这需要一个新的 mock 挂钩。

## 交叉性问题 (跨 SC, 系统性)

### C1 (Critical) — 新 verdict 值 `error` 是未纳入下游消费面的「第四态」

证据链:
1. `pre_merge_gate.py:47-49` 只定义三个 verdict 常量 (`VERDICT_GREEN="green"`, `VERDICT_WAIT="wait"`, `VERDICT_FAIL="fail"`), 无 `VERDICT_ERROR`。
2. `SKILL.md:170-174` 用「三态结果」为标题描述 green/wait/fail 三态语义 (这是本 Spec 涉及的 C.2.4 pre-merge gate 段落, 非 :193 的另一个不相关的 submodule gate「三态结果」——两者是不同子系统, 已核实不可混淆)。
3. `SKILL.md:252-255` (§C.2.4 步骤 6「路由决策」) 只有 `green`/`wait`/`fail` 三个分支, 无 default/else, 无第四分支。
4. `SKILL.md:267` Output schema 把 `verdict` 字面类型标注为 `"green" | "wait" | "fail"` 三值联合类型。
5. `SKILL.md:167` 与 `:243` 两处「primitive 调用」示例性文案里的 `aether ci status --branch main --in-flight --json` 同样是本缺陷遗留的字面量, 均未被 Impact 表点名。

而 proposal.md 在 D2 (`:84`)、D3 (`:97`)、D4 (`:98,128`)、SC-4/5/6 (`:142-144`) 反复用带反引号的字面量风格写 `verdict=`error``——与该文档引用其余枚举值 (`` `green` ``/`` `wait` ``/`` `fail` ``) 的书写习惯完全一致, 说明这确实被当作一个新增的、独立于 `fail` 的枚举值, 而非「fail 的一种说法」。

Impact 表 (proposal.md:163-169) 只列了 3 个文件改动点, 其中 SKILL.md 只提到 `:242` 一行「散文勘正」, 完全没有提及需要同步 §1-4 列出的 4 处消费/schema/命名面。Rule #6 note (proposal.md:110) 自评「零运行时指令流程新增 (指令面是**减少**一条人工义务)」——但如果路由决策表要新增第 4 分支 (「verdict=error 时 AI 应该做什么」), 这恰恰是 Rule #6 判据表里「处方性 · 运行时指令面」那一档, 依 CLAUDE.md 判据「能 ⇒ 照跑 AB, 零裁量」, 该 hunk 应该跑 skill-creator benchmark, 而不是被 substitute 豁免。

后果风险: 本项目消费方是 AI agent 读 SKILL.md 执行 (非严格 switch-case 代码), 一个见多识广的 agent 遇到未枚举的 `error` 大概率会保守处理 (不合并)——但这依赖「agent 会正确临场推断」, 与本 Spec 反复援引的 memory `feedback_invariant_needs_failclosed_default`(「枚举分区必须 fail-CLOSED, 不能靠隐含推断」) 恰恰矛盾: 这条原则被用来论证 D2 不该给默认值回落, 却没有被用来审视 D2/D3/D4 自己制造的新状态该如何在下游 fail-CLOSED。这是一个自反性缺陷。

最坏情况: 如果任何调用方 (现在没有, 但不排除未来出现) 用形如 `if verdict != "fail": proceed()` 的宽松判断, `error` 会被误判为「可以继续」, 直接复活本 Spec 要修的那个 fail-OPEN 缺陷, 只是换了个位置。

### M1 (Major) — `<remote>` 从未被钉死为具体值/参数来源

proposal.md §2 (`:83`) 和 §3 (`:90-98`) 全程用泛型占位符 `<remote>` 描述 symbolic-ref 与 ls-remote 的目标, 从未声明它是硬编码常量 `"origin"`、新增 CLI flag、还是复用既有的 `multi_remote.enforced_remotes` 配置 (`SKILL.md:585` 已有先例概念, 但本 Spec 完全没有提及是否复用)。SC-1 的场景列倒是具体写了 `refs/remotes/origin/HEAD`, 暗示实际上是硬编码 origin, 但 D2/D3 决策记录本身没有明确这一点——场景描述与决策记录之间存在术语层级不一致。

本仓是一个具体反例, 值得注意: `git remote -v` 显示两个 remote (`origin`=Forgejo, `github`=GitHub 镜像); 已实测 `git symbolic-ref refs/remotes/origin/HEAD` 成功解析为 `refs/remotes/origin/master`, 而 `git symbolic-ref refs/remotes/github/HEAD` 直接报错「not a symbolic ref」(该 ref 在本地根本不存在, 因为 github 是后加的第二 remote, clone 时没有对它跑 `git remote set-head`)。如果 Phase B 没有显式钉死用 `origin`, 或者钉死逻辑与「CI 到底跑在哪个 remote 上」这个事实脱节, SC-1/SC-4/SC-5/SC-6 描述的行为在这个真实仓库上就不是唯一确定的。

### M2 (Major) — 既有 46 个 `gate_check` 端到端测试 100% 未显式传 `main_branch`, 修复后全部新增 2 次真实 subprocess 调用 (其中一次可能打网络)

实测: `grep -c "gate\.gate_check(" test_pre_merge_gate.py` = 24 处直接调用, 其中 **0 处**带 `main_branch=` 关键字参数 (`grep -n "gate\.gate_check(" | grep -c "main_branch"` = 0)。这覆盖了 `GateCheckTests` 全部 8 个方法、`TestGHAStubAbortNotSkip` 3 个方法、`PathCoverageGateTests` 的大多数方法等——即绝大多数「成功路径」端到端测试。

D3 (存在性核验无条件执行, 参见 SC-4 对显式传参同样生效的证据) 意味着: 一旦 `main_branch` 参数默认值改为 `None` 且解析逻辑落地, 这些测试在不打桩的情况下会依次真实执行 `git symbolic-ref refs/remotes/origin/HEAD` (本地操作, 无网络, 但仍是新增的真实 subprocess) 和 `git ls-remote --exit-code --heads origin master` (**真实网络调用**, 打向 `forgejo.10cg.pub`)。

这不是纸面推测——本次审计过程中, 独立执行 `git ls-remote --exit-code --heads origin master` 时**第一次调用就发生了一次真实的瞬时网络失败** (`kex_exchange_identification: Connection closed by remote host`), 重试后才成功。如果 46 个既有测试在修复后都毫无防备地各打一次这样的网络调用, 套件会同时变慢、变得环境耦合、且间歇性变红——而且是以一种与「代码逻辑本身对不对」无关的方式变红, 这正是本项目已经在 `test_sc22_no_real_git_subprocess_in_suite` (`test_pre_merge_gate.py:710-724`) 里为 `path_coverage` 集成专门写卫生断言防范过的同一类问题, 而且解决模式也是现成的——`_ProbeCacheResetMixin.setUp()` (`test_pre_merge_gate.py:59-80`) 已经在 v1.65.0 (#122) 引入 path_coverage 评估时, 为了保既有测试不受「新增的无条件步骤」影响, 加了一个 `mock.patch.object(gate, "evaluate_path_coverage", ...)` 的类级桩。本 Spec 要做的事情 (在 `gate_check` 里再插入一个新的、无条件执行的步骤) 与 v1.65.0 那次改动是同一种形状, 但 proposal.md 的「What Changes」和「Impact」都没有提到需要在 mixin 层面新增一个类似的桩。

「§Impact 声称既有用例逐字不改」——若「用例」严格理解为 test 方法体的源码文本, 这个说法可以成立 (改的是 mixin 而不是方法体); 但若不新增 mixin 级桩, 既有用例的**运行时行为**(是否打网络、是否变慢、是否偶发失败) 会发生实质变化, 这与「逐字不改」想传达的「零回归风险」在精神上是不一致的。

补充一个具体实现顺序坑: `evaluate_path_coverage(main_branch=main_branch, pr_branch=pr_branch)` 的调用点在 `pre_merge_gate.py:356-360`, 早于本 Spec 要新插入的 in-flight 查询 (`:365-366`)。若「main_branch 解析」逻辑被安放在这次调用**之后**, `evaluate_path_coverage` 会收到字面量 `None`, 拼出 `f"{None}...{pr_branch}"` = `"None...feat/x"` 这种非法 git rev-range (已用 `python3 -c` 验证过 f-string 行为), 导致 `git diff` 报错、退化为 `unknown` (fail-toward-covered, 不算错误但会在日志里留下令人费解的 "None" 字样)。Spec 没有明确「解析步骤必须插在 `:356` 之前」这条顺序约束, 值得在 tasks.md/实现阶段显式钉一下。

### M3 (Major) — SC-3/SC-7 负控隐含一个未言明的新 mock 依赖

已在逐 SC 复核中展开, 汇总: D3 的存在性核验对「显式传参」路径同样生效 (SC-4 本身就是明证), 因此 SC-3 (显式传 master) 和 SC-7 (分支存在) 这两条负控在修复后的代码里也会新增经过一次 ls-remote 调用。Spec 没有言明这两条负控的 fixture 需要显式 mock「ls-remote 返回存在」, 若遗漏, 会导致负控本身打真网络, 或者 (若实现采用类似 SC-22 的「未打桩即报错」卫生基座) 负控会因为基座跟不上新代码路径而伪红——这种红不是「改坏了既有路径」信号, 而是噪音, 恰恰会被误判成负控生效, 削弱负控的诊断价值。

### M4 (Major) — SC-1「CLI 不传」端到端验证方式不明确, 有 collapse 成浅层测试的风险

已在 SC-1 段展开。核心问题: 现有 `main()` 未提供可独立测试的 parser 构建入口, 要如实测「CLI 不传 --main-branch」这一命题必须新增「调用 `main(argv=...)` + 捕获 stdout」这类此前 111 个用例里从未出现过的测试形态, Spec 未提及, 存在被简化为「只测 argparse 默认值本身」从而弱化 SC-1「期望」列所承诺的端到端验证力度的风险。

### M5 (Major) — SC-6「重试后仍失败」缺少具体重试参数, 影响测试可实现性与套件耗时

已在 SC-6 段展开。若沿用 `AetherBackend` 现有的真实 `(5,15,45)` 秒重试节奏且不 mock `time.sleep`, 单条 SC-6 测试将真实耗时超过 60 秒; 若另立新参数, 则与既有 Aether 重试语义不一致。两个方向 Spec 都未取舍。

## Minor 发现

- **m1**: SC-2 场景文字提到的函数名 `run_gate(...)` (proposal.md:140) 在代码库中不存在; 真实符号是 `gate_check` (`pre_merge_gate.py:298`)。`run_gate` 仅在 `tests/test_submodule_gate.sh:126` 存在, 是完全不相关的子系统 (子模块回滚检测) 里的 bash 函数。不影响理解, 建议订正以维持本 Spec 一贯的高精度引用风格。
- **m2**: 本次审计任务书对必读文件的旁注写「`test_pre_merge_gate.py` (748 行, 现有 111 tests)」。实测: `test_pre_merge_gate.py` 单文件本身是 748 行准确, 但该文件自身只有 **46** 个测试方法 (`python3 -m unittest test_pre_merge_gate -v` → `Ran 46 tests`); **111** 是 `phase-c-integrator/tests/` 目录下三个 python 测试文件 (`test_pre_merge_gate.py` 46 + `test_ci_backends.py` 25 + `test_path_coverage.py` 40 = 111) 汇总后的 skill 级数字, 与 `run_all_tests.sh` 对每个 skill 目录做 `unittest discover` 的计数口径一致。Spec 自身的表述「`phase-c-integrator` 现 111 tests」(proposal.md:179) 是准确的 (它说的是 skill, 不是单文件), 这条不算 Spec 缺陷, 但任务书旁注的转述容易让人误以为 111 条测试都在这一个文件里, 记录以免误导后续读者。
- **m3**: `SKILL.md:167` 与 `:243` 另有两处 `aether ci status --branch main --in-flight --json` 字面量示例, 是本缺陷遗留的同款文案, 均未被 Impact 表 (`:163-169`) 点名要同步; 只修 `:242` 一处会让同一小节内前后描述不一致 (`:167`/`:243` 仍写死 "main" 示例, `:242` 已经改成「显式传真值/自动解析」的新语义)。
- **m4**: `evaluate_path_coverage()` 接收的 `main_branch` 是裸分支名 (如解析出的 `"master"`), 会被原样拼进 `git diff {main_branch}...{pr_branch}` (`path_coverage.py:436-445`), 依赖调用环境存在同名**本地**分支 (而不仅是 `refs/remotes/<remote>/<name>` 远程追踪分支)。在只做了 `git fetch` 未 checkout 本地 `master` 分支的 clone 拓扑下 (例如某些 CI 场景只有 detached HEAD + `origin/master`), `git diff master...pr` 会失败, 退化为 `unknown` → fail-toward-covered——不算错误 (安全), 但会悄悄让 path coverage 优化在这类拓扑下失效, 值得留一笔观察记录, 非阻断项。

## 测试基线数字核实

```
$ cd aria/skills/phase-c-integrator/tests
$ python3 -m unittest discover -s . -p "test_*.py"
Ran 111 tests in 0.972s
OK

$ python3 -m unittest test_pre_merge_gate -v 2>&1 | tail -3
Ran 46 tests in 0.036s
OK

$ python3 -m unittest test_ci_backends -v 2>&1 | tail -3
Ran 25 tests in 0.007s
OK

$ python3 -m unittest test_path_coverage -v 2>&1 | tail -3
Ran 40 tests in 0.903s
OK

$ cd aria/skills/phase-c-integrator/tests && python3 -m pytest tests/test_pre_merge_gate.py -q
46 passed in 0.09s   (等价于上面 unittest 的 46, pytest 视角)
```

`phase-c-integrator` 现 111 tests (46+25+40) 核实**准确**, 与 proposal.md:179 一致。`test_ci_backends.py` / `test_path_coverage.py` 两个文件均不引用 `main_branch` / 不 import `pre_merge_gate` / 不调用 `gate.gate_check` (已 grep 确认零命中), 完全不受本 Spec 影响, 这 65 个测试可视为与本 change 无关的基线背景。真正的变更半径精确落在 `test_pre_merge_gate.py` 的 46 个既有测试 + 计划新增的 ≥7 个 SC 测试。

「本 change 新增按 SC 计 ≥7」——7 条 SC 中 SC-3/SC-7 为负控, SC-1/2/4/5/6 为证据面, 若每条 SC 对应至少 1 个新测试方法, 下限 7 合理, 未见矛盾。

## Verdict

**FAIL** —— 1 条 Critical (C1: 新 verdict 值 `error` 未纳入下游消费/schema/命名面, 且反身性地违反了 Spec 自己援引的 fail-CLOSED 枚举原则, 同时使 Rule #6 豁免自评失效) + 5 条 Major (M1 remote 未钉死 / M2 既有测试新增真实网络依赖且有直接先例未被复用 / M3 负控隐含未言明 mock / M4 SC-1 端到端验证方式不明确 / M5 SC-6 重试参数未钉死)。

SC 表本身的场景/期望/怎么会红三列设计思路是扎实的, 5 条证据面 SC 与 2 条负控 SC 的配对逻辑 (D1 的「两个缺省必须同批改」被 SC-1/SC-2 分别把守) 站得住; D4 的「两个方向都要防」在 exit code 层面 (2 vs 128) 也确认可机械区分。**建议**: 在进入 Phase B 前, 先补齐 (a) verdict 枚举扩容后的下游三处同步 (常量/schema/路由表) 及其 Rule #6 归类重新评估, (b) `<remote>` 的具体来源声明, (c) mixin 级 mock 策略 (镜像 `_ProbeCacheResetMixin` 对 `evaluate_path_coverage` 的先例) 使 46 条既有测试与 SC-3/SC-7 负控保持网络隔离, (d) SC-1 的测试形态 (是否经 `main()`/argv) 与 SC-6 的重试参数。这些都不是推翻 Spec 方向的理由 (缺陷诊断本身准确, Why/发现路径部分的实测复现均核实无误), 而是「按当前文字直接进 Phase B 会在未预警的情况下产出一个下游断链的、测试套件变慢变脆的实现」的具体、可定位的补丁点。

## 轮次记录

- **Round 1** (本轮, qa-engineer 席位): 完整通读 proposal.md + 全文实读 4 个核心代码/测试文件 + SKILL.md 相关段; 实跑 unittest/pytest (111/46/25/40 计数核验) + git symbolic-ref/ls-remote/aether CLI 经验性复现; 产出 1 Critical + 5 Major + 4 Minor。未与其他并行席位 (tech-lead / backend-architect / code-reviewer) 的报告做交叉阅读, 保持本席位独立判断 (post_spec R1 尚在进行中, 尊重跨 agent 独立验证惯例)。收敛判定 (converged) 留给编排层做四元组比较, 本报告不单方面宣称收敛。
