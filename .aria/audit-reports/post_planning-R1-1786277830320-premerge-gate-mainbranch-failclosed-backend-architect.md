---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-09T13:00:19.517Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 — premerge-gate-mainbranch-failclosed — backend-architect

> 审的是 A.2 产物 (`tasks.md` + `detailed-tasks.yaml`, 19 条), 参照 `proposal.md`。不重审 proposal 已收敛/未收敛的判断本身; 仅在 proposal 硬伤直接导致任务错时点名 (`layer: proposal`)。全部 finding 均基于本会话内对仓库文件的实读/实跑, 方法与命令见各节。

## 方法论

工作目录 `/home/dev/Aria` (submodule `aria` @ `af87cae`, 与本地插件市场安装 `~/.claude/plugins/marketplaces/10CG-aria-plugin` 同 SHA, 逐文件 diff 确认 identical)。对 5 项审查逐条实读源码 + 在 `/tmp/.../scratchpad/gitprobe` 建受控裸仓做 git 行为实验, 命令与输出见下文各节引用。

---

## 1. TASK-002 (路径解析 spike) 的输入核验

**(a) helper 三个副本位置是否真存在** — 实读确认: `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py` 与 `~/.claude/plugins/marketplaces/10CG-aria-plugin/skills/phase-c-integrator/scripts/pre_merge_gate.py` 逐字节 identical (`diff` 零输出), 且两者 git HEAD 同 SHA `af87caeeed88af6af76f29a8002badbe1228d927`。但严格讲这是 **2 个物理副本、3 个 cwd 访问入口** —— "主仓根" 与 "aria 子模块根" 指向同一个 inode, 不是两份可独立漂移的拷贝; 只有 plugin 安装态是真正独立的第三份 (不同 git remote, 可能不同步更新节奏)。输入表把两者都记为"副本位置"概念上不精确 (见 Finding #2), 但不影响 SC-12 的四 cwd 测试矩阵本身。

**(b) `SKILL.md:262/:559/:610` 用 `${CLAUDE_PLUGIN_ROOT}` 这句 —— 逐行实读, 证伪**:

```
$ sed -n '262p;559p;610p' aria/skills/phase-c-integrator/SKILL.md
**Helper 实现**: `${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/pre_merge_gate.py` ...
**Helper 实现**: `${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/submodule_gate.sh` ...
**降级策略**: 检测 `test -f "${ARIA_PLUGIN_ROOT:-aria}/skills/git-remote-helper/SKILL.md"` ...(`ARIA_PLUGIN_ROOT` 环境变量优先)
```

三行**全部**用 `${ARIA_PLUGIN_ROOT:-aria}`, 不是 `${CLAUDE_PLUGIN_ROOT}`。`grep -n CLAUDE_PLUGIN_ROOT SKILL.md` 只命中 `:737` 一处 (aria-context-monitor 调用示例, 与 helper 定位无关); `grep -n ARIA_PLUGIN_ROOT SKILL.md` 命中的正是 `:262/:559/:610` 这三行。

进一步核实仓内 (`aria/` 子模块范围) 汇总计数: `CLAUDE_PLUGIN_ROOT`=65 处、`ARIA_PLUGIN_ROOT`=5 处 —— proposal.md §1 "66 处 / 仅 5 处" 的**汇总比例基本准确** (65≈66, 5 精确匹配)。但据此推出的具体结论"`SKILL.md:262/:559/:610` 均用它 [`CLAUDE_PLUGIN_ROOT`]" 是**反的**: 这三行恰恰就是全仓 5 处 `ARIA_PLUGIN_ROOT` 少数派用法中的 3 处, 不是 65 处多数派用法的例证。proposal.md §1 用统计上正确的"仓内约定是 CLAUDE_PLUGIN_ROOT"论据, 支撑了一个方向相反的具体行引用。

**影响**: 若 TASK-002 spike 执行者信任"已实证输入"字面 (`须核 CLAUDE_PLUGIN_ROOT... 与 SKILL.md:262/:559/:610 的既有约定是否可直接沿用`) 而不重新读文件, 可能误判"本文件既有约定已经是 CLAUDE_PLUGIN_ROOT, 只需照抄", 从而漏掉一个真实存在、且 TASK-014 需要收口的分叉: **本文件 3 处既有声明用的是仓内少数派写法** (`ARIA_PLUGIN_ROOT:-aria`, 且带字面 `aria` fallback —— 对 "standards 子模块根" cwd 而言这个 fallback 本身就是错的, fallback 到 `aria` 而不是 `standards`)。SC-12 的行为验收会在真实测试时自然暴露这个问题, 但输入表的错误陈述仍构成一次可避免的返工风险。

**(c) `SKILL.md:242` cwd 契约** — 实读确认逐字准确: "**执行上下文契约**: 在执行 C.2 合并的目标仓根内调用 (子模块合并 → 子模块根); `main_branch` 显式传真值 (本项目 `master`), 不依赖 CLI default"。此条输入无误。

---

## 2. TASK-003 (精确比对 spike) 可实现性 —— 受控实验复现

在 `/tmp/.../scratchpad/gitprobe` 建两个裸仓验证 proposal §5 / SC-6 / SC-13 的判据链:

- 裸仓仅有 `refs/heads/wip/master`: `git ls-remote --heads <repo> master` → **RC=0** 命中 `wip/master` (尾段 glob 误判, 实测复现"裸分支名"行的失效); 改用锚定 `git ls-remote --heads <repo> "refs/heads/master"` → **RC=2** 正确拒绝。
- 裸仓仅有 `refs/heads/master`: 锚定 pattern `refs/heads/mast*` / `refs/heads/m[a]ster` / `refs/heads/maste?` / `refs/heads/*` **全部 RC=0** 且都返回 `refs/heads/master` 这一行 —— 复现"锚定仍 fail-OPEN"的第二行结论。

⇒ proposal/TASK-003 的判据("对返回的 ref 名列表做精确字符串比对, 不依赖 pattern 语义")是**必要且经我独立复现验证有效**的修法: 无论上面哪种 pattern, git 返回的 ref 名字面量永远是 `refs/heads/master`, 与 `"refs/heads/" + main_branch` (若 main_branch 传入恶意/异形值如 `"mast*"`) 做字符串 `==` 比较必然为 False, 正确拒绝。**判据可实现, 且是唯一在我实验范围内确认无 fail-open 的方案。**

"取列表方式" 上, 两条路径都能满足判据: (i) `ls-remote --heads <remote>` 不传 pattern, 拿全量再精确比对; (ii) `ls-remote --heads <remote> <main_branch>` 传 pattern 当"性能提示", 但仍强制精确比对兜底。建议 spike 优先选 (i) —— 结构上消除 glob 语义面, 不依赖"记得每次都做精确比对"这条纪律; (ii) 需要额外的"绝不能跳过精确比对"约束才安全, 多一个可被后续维护者破坏的隐含前提。此为**建议**, 非阻塞。

---

## 3. TASK-004 (复用 spike) 的两个先例是否真能复用 —— 实读, 有保留

```
ci_backends/aether.py:164-187  AetherBackend._run_with_retry(self, args)
path_coverage.py:78-102        _run_git(args, cwd)  (模块级自由函数)
```

**`_run_with_retry`**: 是 `AetherBackend` 的**私有实例方法**, 签名硬编码 `[self.binary] + args` (`self.binary` 在 `__init__` 里被强制解析为 `shutil.which("aether")` —— 只能是 aether 二进制, 不能指向 `git`)。字面复用 (直接调用) 不可行, 只能靠**抽取**成自由函数或子类化取巧 (后者语义扭曲, 不建议)。且它的异常捕获范围**只有 `except subprocess.TimeoutExpired`** (`:180`) —— `FileNotFoundError`/`OSError` 不在捕获范围内, 会未捕获地从 `_run_with_retry` → `_query` → `query_pr_ci`/`query_branch_in_flight` 一路上抛, `gate_check()` 目前只 `except NotImplementedError` / `except AetherQueryError` (`:367-376`, `:390-399`), 两者都接不住裸 `FileNotFoundError`。也就是说**如果字面照抄 `_run_with_retry` 的异常处理形态, 会直接违反本 Spec 自己定的 catch-all 要求** (TASK-004 验收第 3 条: "任何未枚举情形 (`FileNotFoundError` / `OSError` /...) 一律 fail, 不得放行"; proposal §5 退出码表同样列了这一行)。

**`_run_git`**: 是**模块级自由函数**, 签名 `(args: list[str], cwd: str | None)`, 已捕获 `(TimeoutExpired, FileNotFoundError, OSError)` 三元组 (`:93`) 且承诺"永不 raise"。真正可直接复用 (`pre_merge_gate.py` 已经 `from path_coverage import evaluate_path_coverage`, 加一个 `_run_git` 导入零新增耦合)。但它**没有重试逻辑** —— 单次 `subprocess.run` 失败就返回 `(False, "", err)`, 不会对 `TimeoutExpired` 做 `RETRY_BACKOFF` 重试。

⇒ **两个先例对本任务而言互补而非互斥**: `_run_git` 提供正确广度的异常安全 (但缺重试), `_run_with_retry` 提供重试策略 (但异常安全范围不够、且绑定错误的二进制)。TASK-004"须说明复用方式"的验收要求已经预留了这个空间, 但任务本文和 notes 都把两者并列成一对可"选一/都用"的先例, 没有点出**单独复用任一个都不满足本任务自己的验收条件**, 需要组合 (至少复用 `_run_git` 的 subprocess 包装 + `RETRY_BACKOFF`/`MAX_RETRY_ATTEMPTS` 常量做独立重试循环, 或抽取 `_run_with_retry` 的重试骨架并把异常捕获范围扩到三元组)。3h 估时下, 若执行者未经我这轮实读就直接假设"两个都能直接调", 有较高概率产出一个悄悄继承 `_run_with_retry` 异常盲区的实现, 而这恰恰是本 Spec 自己反对的"同一算法两份实现、走了没被加固那份"的翻版。

---

## 4. 依赖顺序语义正确性

DAG 无环 (机械验过), 但发现 **3 处语义上应有而缺失的依赖边**, 同一类问题:

- **TASK-008 缺 TASK-007**: `_verify_branch_exists()` 的核验对象是"`<main_branch>` 在 `<remote>` 上是否存在" (proposal §5), `remote` 是 TASK-007 新增的 `gate_check(..., remote=...)` 参数。TASK-008 当前只 `dependencies: [TASK-003, TASK-004, TASK-005]`, 不含 TASK-007。TASK-007 自己的验收又写"核验与 in-flight 查询使用同一个 remote 值"——即 TASK-007 的验收依赖 TASK-008 的产物存在, 而 TASK-008 的依赖表没反过来声明它需要 TASK-007 的参数。当前状态下这两个任务在 DAG 里彼此独立、可并行派发, 但内容上互相需要对方先落地, 并行执行会撞同一段 `gate_check()` 函数体, 或导致 TASK-008 执行者不知情地把 `remote` 硬编码成字面 `"origin"` (正是本 Spec 治的"该做参数却写死字面量"病的翻版)。
- **TASK-011 缺 TASK-003 (或 TASK-008)**: TASK-011 折叠块须"补上分支存在性核验步"的描述 (验收第 3 条), 但该核验的算法语义 (精确比对判据) 由 TASK-003 定稿, 具体实现由 TASK-008 落地。TASK-011 当前只 `dependencies: [TASK-002]` (路径解析), 不含 TASK-003/TASK-008 任一。
- **TASK-012 缺 TASK-009**: TASK-012 的验收要求判断"若既有措辞已覆盖 raw_message 的 surface, 不加句"——这个判断需要知道 TASK-009 产出的 `raw_message` 内容形态。TASK-012 当前只 `dependencies: [TASK-011]`。**对照组**: TASK-013 在同样场景下正确地把 TASK-009 列为依赖 (`dependencies: [TASK-009, TASK-011]`)——说明任务作者理解这类耦合, 只是没有把它套用到 TASK-011/TASK-012 这两个同形位置, 属于"同一修法未推广到全部姊妹位置"的模式。

三处均不构成对 Phase B **启动**的阻塞 (TASK-001 可以立即开始, 且各 spike 本身的经验验证很可能会在执行时自然暴露这些耦合), 但会影响 A.3 派发/并行调度的正确性——若调度依据 `dependencies` 字段做并行分派 (本项目已有 "按文件域分 track" 的并行派发先例), 当前的 DAG 会允许 TASK-007/008 或 TASK-002/011 等被错误地并行分派到不同 agent, 产生同文件竞态或语义不一致。

**衍生观察 (verification 完整性, 非 DAG 结构问题)**: 没有任何任务在 TASK-008 (新 subprocess 落地) **之后**显式要求重跑全量套件并重新确认 `test_sc22` 仍能拦截真实 subprocess。TASK-010 的"全量 111 tests 绿"检查只依赖 TASK-006, 在 DAG 上可以早于/独立于 TASK-008 完成, 不能替代这个收口点。TASK-005 建的隔离接缝是**前瞻性**设计 (针对尚未写出的 TASK-008 代码建缝), 需要一个收尾断言确认 TASK-008 落地后接缝确实对上了、`test_sc22` 依然对真实 subprocess 敏感。

---

## 5. 工时估算

三条 spike 合计 11h (4+4+3)、全表 55h, 逐项相加复核无误。结合本轮实读结果, 有两处具体的乐观信号 (非泛泛而谈):

- **TASK-004 (3h)**: 第 3 节的实读发现两个先例都不能直接复用, 真正work 是"组合/抽取", 可能牵涉修改 `ci_backends/aether.py` 这个有 25 个既有测试 (`test_ci_backends.py`) 覆盖的模块——3h 覆盖"决定形态 + 实现 + 说明复用方式"偏紧。
- **TASK-011 (6h)**: notes 自己承认 `:99` 段"须单独 spike, 不得照搬 `:218` 段形态"——即 TASK-011 内部悄悄含着一个和 TASK-002 (4h) 量级相当的子问题, 却没有单独计工时; 且 C.2.4 这个文件区段是五轮 post_spec 未收敛的主战场, 历史证据 (R4→R5 两分支路径解析被四席证伪) 指向这里的返工率高于表面复杂度。

此项从优先级看是 minor: 本 Spec 是 owner 明确裁定"停止改文档, 用 TDD 接管"的产物, spike 超时属预期内的正常迭代, 不需要现在改数字, 仅供执行时的进度预期校准。

---

## 审计结论

19 条任务的整体拆解质量高: 抽样核验的十余处 file:line / grep 计数 (SC-1/2/3/4/5 今日实测值、24 处调用点计数、`worktree_manager.py:170`、`fetch_gate.py:55`、`SKILL.md:242`、`pre_merge_gate.py:21/300/427`) **全部逐字精确**, TDD 红窗 (TASK-001) 的四条断言经我独立重跑, 数值与任务声称完全一致。TASK-003 的核心判据经我用受控裸仓独立复现, 确认有效。组 0 (spike-first) 的设计意图被严格贯彻。

但在 backend-architect 关注的"可执行性"维度上, 发现三类需要处理的问题: (1) proposal §1 一处具体行引用与源码方向相反 (§1); (2) TASK-004 的两个复用先例经实读证明互补而非可互换, 任务表述可能诱导字面复用出一个继承异常盲区的实现 (§3); (3) DAG 里三处结构性缺失的依赖边, 同一模式的三个实例, 会影响并行派发正确性 (§4)。三者均不构成 Phase B 启动阻塞, 但建议在派发 TASK-002/004/007/008/011/012 前用本报告做一次快速修订 (补依赖边 + 更正 proposal §1 的行引用 + 给 TASK-004 执行者预先带上第 3 节的实读结论), 以避免可预见的返工。

## Verdict

**PASS_WITH_WARNINGS** — 0 Critical, 3 Major, 4 Minor。无阻塞 Phase B 启动的缺陷; 建议按上述清单在派发前做轻量修订。

## 轮次记录

| 轮次 | 席位 | 结论 | 备注 |
|------|------|------|------|
| R1 | backend-architect | PASS_WITH_WARNINGS | 单席位 round 1; 是否需要额外席位/轮次由 audit-engine 编排层按 convergence 模式规则裁定 |
