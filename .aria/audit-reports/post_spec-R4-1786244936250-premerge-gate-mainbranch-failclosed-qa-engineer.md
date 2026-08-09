---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-09T03:49:58.110Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [qa-engineer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 审计结论

本轮审的是范围重定后的新对象 (D1: `SKILL.md §C.2.4` 由散文改为强制 helper 调用)。全部 findings 均基于实读 `file:line` 或实跑命令得出, 方法论: 逐条 grep 断言按字面命令重跑 · 用 `/tmp` 受控裸仓验证 `ls-remote` 锚定行为 · 用最小 Python repro 验证 `TypeError`/`mock.patch.object` 跨模块作用域语义 · 对 SKILL.md 做代码块边界与标题层级的结构性通读。**未修改本仓任何文件, 未 commit/push。**

**核心判断: SC-3 (Spec 自称"承重断言, 对应 D1") 按 Spec 自己给出的逐字命令块实测拿不到绿 —— 即便 Phase B 完全正确实施 D1 也一样。** 这与 R1-R3 反复出现的"断言没断言它声称的东西"是同一形状缺陷, 且这次出现在**唯一**的机械信号上。另外还发现: D1 的"唯一执行入口"在本项目 3/4 的合并场景 (子模块本地合并, CLAUDE.md 硬约束钦定) 里启动不了; SKILL.md 里还有第二份、且文件序更靠前的未加固散文 5 步描述完全没被这版触及; D4 新增的强制 subprocess 调用对既有测试套件的"零真实 git 子进程"不变量造成结构性冲击, 而 Spec 给出的处方经实验证实是 no-op。四条互相独立, 任一条单独发生都足以让本版无法如实交付它对自己许下的验收标准。

## Verdict

**FAIL** — 4 项 Critical (每项均实读/实跑确认, 均 blocks_phase_b=true), 3 项 Major, 3 项 Minor。不建议进入 Phase B; 建议针对下列 4 处做一轮定向修订 (预计改动集中在 proposal.md §1 / SC-3 / §测试卫生 / Impact 表 SKILL.md 行, 均为文本级修改, 不涉及推翻既有决策记录), 是否需要再开一轮 post_spec 由 owner 视修订幅度裁定 (已到 max_rounds)。

---

## Findings

### C-1 · SC-3 (承重断言, 对应 D1) 对 Spec 自己给出的逐字命令块实测 = 0, 正确实施后仍然恒红

**锚点**: `proposal.md:69-72` (§1 "新增的唯一执行入口 (逐字)") vs `proposal.md:176` (SC-3 行)

**实跑**: 把 §1 给出的逐字文本原样存成文件, 跑 SC-3 自己的 grep pattern:

```
$ cat qa_r4_own/sc3_literal_repro.md
新增的唯一执行入口 (逐字):

```bash
python3 "${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/pre_merge_gate.py" \
  --pr-branch "<PR_BRANCH>" --main-branch "<MAIN_BRANCH>" --remote origin
```

$ /usr/bin/grep -cE 'python3.*--main-branch|--main-branch.*python3' qa_r4_own/sc3_literal_repro.md
0
```

**根因**: §1 给出的命令用 `\` 续行拆成两行 —— `python3` 在第 1 行, `--main-branch` 在第 2 行。grep 默认逐行匹配, `.*` 不跨行 (没有 `-z`/`-P` 多行模式), 所以两个子串永远不可能被同一次匹配捕获。用单行 sanity check 验证 pattern 本身没问题:

```
$ echo 'python3 "x/pre_merge_gate.py" --pr-branch "<PR_BRANCH>" --main-branch "<MAIN_BRANCH>" --remote origin' \
    | /usr/bin/grep -cE 'python3.*--main-branch|--main-branch.*python3'
1
```

**今日 (改前) 状态**: count=0, 符合 SC 表"必红"预期 —— 这一半没问题。问题在于**改完之后同样是 0**: SC-1..SC-5 表格开篇明文"本表不留裁量空间", 但 SC-3 恰恰是这张表里唯一一条"正确实施仍然拿不到绿"的断言, 且它被 Spec 自己标注为"承重断言, 对应 D1" —— 五条里最重要的一条不可证伪。这正是 qa-engineer 审计镜头第 1 条明确要防的形状: "一条永远拿不到绿的断言与一条恒绿的断言同样是零信息量"。

**后果推演**: Phase B 实现者迟早会亲自跑这条 grep (SC 本就是拿来跑的), 发现拿不到绿。摆在他面前只有两条路: (a) 把命令改成单行 (无害, 但属于对 Spec "逐字" 指令的沉默偏离, 且 Spec 文本本身未被修正), 或 (b) 悄悄放宽 SC-3 的 pattern (有害 —— 一旦退回类似"`grep -c 'pre_merge_gate.py'` ≥2"这种松散判据, 就正好落回 SC-3 自己在 `proposal.md:176` 警告的"该文件名今日已出现 4 次, 那半条断言恒绿零信息量")。两条路都不该由 Phase B 实现者在没有 Spec 授权的情况下自行拍板 (CLAUDE.md Rule #10)。

**修法建议** (二选一, 需在 Spec 文本内写死, 不能留给 Phase B 裁量):
- (a) §1 命令改单行 (完整命令约 155 字符, 单行完全可读, 且与 SC-3 引用的既有先例 `SKILL.md:737` token_telemetry.py 单行范式一致);
- (b) 保留两行, 但把 SC-3 改成对代码块整体求值 (如先 `awk '/^```bash/,/^```/'` 抽取代码块再 grep), 并同步改判据表里"必红/必绿"的复核方式。

---

### C-2 · D1「唯一执行入口」在本项目 3/4 的合并场景下启动不了 —— 相对路径 fallback + 从未被赋值的环境变量

**锚点**: `proposal.md:70-71` (§1 逐字命令) vs `SKILL.md:242` (执行上下文契约: "子模块合并 → 子模块根") vs CLAUDE.md「多远程推送 — 约束 1」(子模块合并必须本地 `git merge`)

**实跑** (本仓根环境, 独立验证, 未依赖任何其它 agent 的结论):

```
$ echo "ARIA_PLUGIN_ROOT=[${ARIA_PLUGIN_ROOT:-<UNSET>}]"
ARIA_PLUGIN_ROOT=[<UNSET>]

$ grep -rn 'ARIA_PLUGIN_ROOT=' --include='*.sh' --include='*.py' --include='*.md' \
       --include='*.json' --include='*.yaml' --include='*.yml' . 2>/dev/null | grep -v ':-aria'
(零命中 —— 全仓没有任何地方真正赋值这个变量, 只有消费点)

$ cd /home/dev/Aria/aria && python3 "${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/pre_merge_gate.py" --help
python3: can't open file '/home/dev/Aria/aria/aria/skills/phase-c-integrator/scripts/pre_merge_gate.py': [Errno 2] No such file or directory
RC=2

$ cd /home/dev/Aria/standards && python3 "${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/pre_merge_gate.py" --help
python3: can't open file '/home/dev/Aria/standards/aria/skills/phase-c-integrator/scripts/pre_merge_gate.py': [Errno 2] No such file or directory
RC=2
```

**为什么重要**: `SKILL.md:242` 逐字规定 C.2.4 的执行上下文是"在执行 C.2 合并的目标仓根内调用 (子模块合并 → 子模块根)"; CLAUDE.md 硬约束 1 又逐字规定"子模块 (aria / standards / aria-orchestrator) 的分支合并必须本地 `git merge`"。本项目 4 类合并 (主仓 + 3 个子模块) 里有 3 类的 cwd 是子模块根 —— 在这 3 类场景里, D1 新钦定的"**执行方式 (唯一)**"命令直接 `No such file or directory`。而 D1 恰恰把原本的 5 步散文降级成"⛔ 不要手工执行"的折叠块 —— 一旦"唯一被授权的动作"报错, AI 面前只剩两条路: 硬停 (对 3/4 的合并场景恒红), 或者自行改写路径/回到裸命令 (正好是本 Spec 要堵的口子)。SC 表里没有任何一条覆盖"从子模块根执行入口能否启动"这件事。

**修法建议**: §1 需要给出路径解析契约, 而非依赖一个从未被赋值的环境变量的相对回落; 可选方向: 用已确认在 Claude Code 插件宿主环境里会被自动注入的 `CLAUDE_PLUGIN_ROOT` (`SKILL.md:737` 先例用的正是它, 而非 `ARIA_PLUGIN_ROOT`), 或命令前显式加一步"解析仓根"逻辑, 或直接要求绝对路径。并建议补一条 SC: 从子模块根 cwd 执行 §1 逐字命令, 断言能正常启动 (今日 RC=2 ⇒ 必红)。

---

### C-3 · SKILL.md 内还有第二份、文件序更靠前、完全未被这版触及的 C.2.4 散文 5 步描述

**锚点**: `SKILL.md:101` (```yaml 开) ~ `SKILL.md:216` (``` 闭), 具体子块 `SKILL.md:161-181`; 对照 `proposal.md` Impact 表 "SKILL.md" 行

**实读**: SKILL.md 的标题层级是 `## 执行流程` (:70) → `### 步骤执行` (:99, 含一个从 :101 开到 :216 的单一 yaml 代码块, 内含 C.1/C.2/C.2.4/C.2.4.5 全部步骤) → 再往后才是 `### C.2.4 Pre-Merge Precondition Gate (v1.3.0+)` (:218, D1 改造的对象)。也就是说, "步骤执行" 这个 yaml 速查块**在文件里出现得比 D1 改造的详述段更早**, 且顶着一个听起来就是"这是要执行的步骤"的标题。其中 :161-181 是 C.2.4 的**第二份**完整 5 步描述:

```
161	C.2.4 - Pre-Merge Precondition Gate (v1.3.0+):
...
166	  primitive 调用:
167	    - aether ci status --branch main --in-flight --json (查 main 是否有 in-flight)
168	    - aether ci status --branch <PR_BRANCH> --json (查本 PR CI 状态)
```

`:167` 确实被 SC-1 的 pattern 命中 (`--branch main`, 我在 C-1 的独立复核里已确认 SC-1 今日计数=2, 恰好是 `:167`+`:243` 两处), 但 `proposal.md` Impact 表把 `:167` 明确归入"字面量"处置 (只换成占位符), **不属于**"§C.2.4 结构重整"的范围 (那个范围限定在标题 "§C.2.4" 之内, 即 :218 起的详述段)。这意味着改完之后, `:161-181` 这整段**仍然是完整、未折叠、可直接复制执行的 5 步散文** —— 只是其中一处字面量从 `main` 换成了占位符; `:168` 的 `aether ci status --branch <PR_BRANCH> --json` 从始至终没有被任何 SC 或 Impact 表提及。

**为什么重要**: 本 Spec 存在的全部理由 (R3 结论) 是"AI 走的是没被加固的那份散文, 只加固另一份对真实执行路径无效"。D1 把 `:238-263` 那份折叠 + 去命令字面量, 但 `:101-216` 这份 —— 文件序更靠前、标题更像"这是步骤"、结构更像可执行伪代码 —— 完全没被处理。如果一个 AI 在执行 Phase C 时先读到 "### 步骤执行" 这个标题下的 yaml 块 (这在线性阅读顺序下是大概率事件), D1 声称"收敛了两份实现"这句话就不成立: 仍然存在至少两份散文, 只是其中一份现在多了一层折叠的伪装。

**修法建议**: 要么把 `:161-181` 也纳入本 Spec 的字面量清理 + 结构化处理范围 (至少去掉 `:168` 这类可执行命令模板, 改成指向 `### C.2.4` 详述段的指针, 避免同一行为出现两份互相可能漂移的描述——这本身也是更干净的 Rule #3 落地方式), 要么在"待 R4 重点审"关心的"AI 还有没有别的地方能读到裸命令"这一问题上明确记录"已知残留, 本版不治, 开 follow-up"并说明为什么可以接受。当前 Spec 文本对这个位置保持沉默, 相当于默认它不存在。

---

### C-4 · D4 新增的无条件 subprocess 调用没有为既有测试套件规划隔离, 会击穿"零真实 git 子进程"不变量, 且 Spec 给出的处方是 no-op

**锚点**: `proposal.md` §5 (:117-129, 核验点插入位置) + `proposal.md:188` (测试卫生段) vs `test_pre_merge_gate.py:710-724` (`test_sc22_no_real_git_subprocess_in_suite`) + `path_coverage.py:47` (`import subprocess`)

**背景实测**: 当前 `test_pre_merge_gate.py` 46 个测试 0.056s 内全绿, 零真实 subprocess (已用 `python3 -m unittest test_pre_merge_gate -v` 实跑确认)。§5 把"存在性核验"插在 3 个早退**之后**、`evaluate_path_coverage`/`query_branch_in_flight`**之前**, 且明确是"对两条路径都有效"的**无条件**拦截 —— 没有任何 opt-out。这意味着除 SC-6/7/8 专属的裸仓 fixture 外, `GateCheckTests`/`FallbackTests`/`PathCoverageGateTests` 等类下、经 `_ProbeCacheResetMixin` 覆盖的全部既有 + 新增测试方法, 一旦机械补上 `main_branch="master"` (Impact 表已要求), 都会走到这条新调用 —— 而 `_ProbeCacheResetMixin.setUp()` 目前只桩了 `evaluate_path_coverage` 和 probe cache, 没有任何东西桩住新的分支核验。

**双重后果, 均已独立实证**:

1. **对没有任何 subprocess 守卫的 ~35 处既有/新增测试**: 会真实调用 `subprocess.run(["git","ls-remote","--exit-code","--heads","origin",...])` —— 网络/子进程依赖, 直接击穿今日 0.056s/零依赖的基线。

2. **对 `test_sc22_no_real_git_subprocess_in_suite` (:710) 本身**: Spec 在 `:188` 断言"该守卫当前 patch 的是 `pc_module.subprocess` (path_coverage 模块的), 看不见 gate 层新增的 subprocess", 并要求"扩到 patch `pre_merge_gate` 模块自己的 `subprocess`"。我用最小复现独立验证了这个判断本身有误, 且方向相反:

```python
# mod_a.py / mod_b.py 都 `import subprocess` 后调用 subprocess.run(...)
with mock.patch.object(mod_a.subprocess, "run", _forbidden):
    mod_b.call_b()   # 从未被"扩展"到 mod_b, 但依然被拦截
# 输出: "mod_b.call_b() ALSO raised -> patch is GLOBAL (shared module object)"
```

`path_coverage.py:47` 与 (预期新增到) `pre_merge_gate.py` 都会用 `import subprocess` (模块对象引用, 非 `from subprocess import run`) —— Python 的 `sys.modules` 缓存决定了两边引用的是**同一个** `subprocess` 模块对象, 对它的 `.run` 属性打一次 patch, 对所有引用它的模块**全局**生效, 与"patch 时用的是哪个模块的引用名"无关。我进一步用一个贴近真实结构的最小 repro (仿 D4 插入点形状: 3 个早退之后、`evaluate_path_coverage` 之前插入一次真实 `subprocess.run`) 复现了 `test_sc22` 在这种结构下的真实行为:

```
$ python3 -m unittest test_fakegate -v
FAIL: test_sc22_extended_per_literal_instruction
AssertionError: real git subprocess spawned in unit suite
  (在 gate_check → _verify_branch_exists → subprocess.run 处触发, 而非到达最终 assertEqual)
```

也就是说: `test_sc22` 今天**已经**"看得见"新代码 (不需要任何扩展), Spec `:188` 给的处方是 no-op; 真实后果的方向与 Spec 的判断相反 —— 不是"扩展前恒绿", 而是"D4 一落地, 这条已有的绿测试立刻变成 `AssertionError`, 且报错点在 `gate_check` 内部, 根本走不到 `self.assertEqual(out["verdict"], "green")`"。

**与 SC-6/7/8 的结构性矛盾**: `proposal.md:186` 要求 SC-6/7/8"不得用 ... mixin 打桩 —— 它们要验的正是真实 `ls-remote` 行为", 而 `test_sc22` 的名字与断言逐字是"no real git subprocess in suite"。这两条约束现在同时成文, 但没有人告诉 Phase B 实现者"suite-wide 无真 git" 与 SC-6/7/8 "必须真 git" 的边界具体划在哪 —— 结果最可能是实现者在毫无预期的情况下看到一条叫"卫生守卫"的测试变红, 最省事的处理方式就是弱化它, 这正好销毁这条守卫存在的意义。

**本仓已有可直接复用的解法先例**: `test_path_coverage.py:116` 的 `_RepoFixtureMixin` 就是这个问题的现成答案 —— 它用 `tempfile.mkdtemp()` + `self.addCleanup(shutil.rmtree, ...)` 构建真实临时仓, 只服务于需要真实 git 行为的测试类, 与 `test_pre_merge_gate.py` 的 `_ProbeCacheResetMixin` (只桩不真跑) 完全分离、互不干扰。

**修法建议**:
1. 删掉 `proposal.md:188` "扩到 patch pre_merge_gate 模块自己的 subprocess" 这句 (它基于对 mock 作用域的误判, 是 no-op);
2. 给 `_ProbeCacheResetMixin.setUp()` 新增第三处默认桩 (如 `mock.patch.object(gate, "_verify_branch_exists", return_value=(True, None))`), 覆盖 SC-6/7/8 之外的全部既有/新增测试, 并把这项工作量计入 Impact 表 (目前完全没提);
3. SC-6/7/8 (以及 SC-11, 见 minor 部分) 参照 `_RepoFixtureMixin` 模式, 建一个不继承 `_ProbeCacheResetMixin` 的独立测试类, 明确注释"本类故意不桩, 验证真实 ls-remote 行为";
4. `test_sc22` 的 docstring/断言范围改为"gate_check 集成路径内无真 git" (而不是笼统的 "suite 内"), 避免与 SC-6/7/8 名实冲突。

---

### M-1 · SC-7/SC-8 与"不得 mixin 打桩"的字面矛盾, 尤其 SC-8 (timeout) 在实践上无法不 mock

**锚点**: `proposal.md:186` ("这三条不得用 evaluate_path_coverage 那套 mixin 打桩 —— 它们要验的正是真实 ls-remote 行为") vs `proposal.md:180-181` (SC-7/SC-8 行, 均自带 "(mock)" 标注)

SC-6 我已用真实裸仓验证可行、且不需要 mock (见下方 D4 锚定验证)。SC-7 (`ls-remote` 返回非 0 非 2) 实测也**可以**不 mock 达成 —— 指向一个不存在的路径即可拿到真实 RC=128 (见 M-2)。但 SC-8 (timeout, 且明确要求"须 mock `time.sleep`") 在实践上很难不 mock `subprocess.run`/`time.sleep`: 真实触发一次 30s timeout × 3 attempts × 5/15/45s backoff, 单测会跑到 65s+, 且需要一个会真实挂起的 remote (例如监听但不响应的 socket) 才能可靠复现, 这与"这三条不得 mixin 打桩"字面冲突。

**合理解读** (但 Spec 文本没有明说): "不得 mixin 打桩" 应该是指不能像 `evaluate_path_coverage` 那样把 `_verify_branch_exists` 整个函数桩成一个固定返回值, 但可以在更底层 (`subprocess.run` 的返回值/异常) 打桩, 让 `_verify_branch_exists` 内部真实的重试计数/退避调用/exit-code 分派逻辑照常执行。建议 Spec 把这条边界明写, 否则 Phase B 要么被迫为 SC-8 搭一个真实会挂起的 fixture (脆弱、慢), 要么误把 `_verify_branch_exists` 整体桩掉 (违背 SC-7/8 要验证"真实分派逻辑"的初衷)。

---

### M-2 · §4 判据表"其他非零"分支引用的先例区间 (1-126) 与 git 的真实 fatal-error 退出码 (128) 不在同一数值空间

**锚点**: `proposal.md:108-109` (§4 判据表, "其他非零 | 按 SKILL.md:260 既有规范 (exit 1-126 → fail, 不重试)")

**实跑**:

```
$ git ls-remote --exit-code --heads /nonexistent/path/repo.git "refs/heads/master"
fatal: '/nonexistent/path/repo.git' does not appear to be a git repository
fatal: Could not read from remote repository...
RC=128
```

`SKILL.md:260` 的"1-126"是给 **aether** CLI 定的退出码惯例, 不是 git 的。git 对"仓库不存在/不可读"这类致命错误统一返回 **128**, 落在被引用区间之外。"其他非零"这个桶名字面上是"排除 0 和 2 之后的任意非零值", 所以行为判定 (fail + `kind="main-branch-verify-failed"`) 本身依然正确覆盖 128 —— 这不是功能 bug, 而是一条**引用先例本身对不上号**的表述问题, 容易让 Phase B 实现者误以为需要对"1-126"和"127+"做特殊区分处理, 浪费排查时间或引入不必要的分支。建议把这行引用改成"排除 0 与 2 之后的任意非零值 (含 git 常见的 128 fatal error)", 不再挂靠 aether 的退出码惯例。

---

### M-3 (与 C-3 同源, 单独列出以呼应"待 R4 重点审"第 1/2 条)

D1 的核心保护机制是"折叠 + 去掉全部可执行命令字面量", 但 `<details>` 标签只影响浏览器/markdown 渲染器的视觉折叠, 对 AI 通过文件读取工具看到的原始文本没有任何隐藏效果 —— 这意味着"折叠"本身是装饰性的, 真正起作用的只有"命令字面量是否被清空"这一件事。SC-1/SC-2 只窄验了两处含 "main" 的字面量, 对 `SKILL.md:240` (`aether --help | grep -q "in-flight"`) 与 `:244` (`aether ci status --branch <PR_BRANCH> --json`) 这类不含 "main" 但同样是可复制执行命令的残留, 零覆盖。若 Phase B 遗漏清理这些 (哪怕折叠块的标题/警告语都做对了), AI 仍可能手工执行折叠块内容, 绕过 D4 新增的核验步骤 —— 复现的是同一类"AI 走非 helper 路径"问题, 只是绕过对象从"main 硬编码"换成了"分支存在性核验"。SC 集对此没有任何机械检测。

---

### Minor

- **gate_error.message 语言不一致**: `proposal.md:138-144` 给出的 `gate_error.message` 示例是中文, 而 `pre_merge_gate.py` 现有全部 `raw_message` (`:279-296` 一带) 均为英文。Spec 未说明这是仅供文档读者理解的示意还是要求实现产出中文消息, 建议 Phase B 前明确, 避免语言不一致进入产物。
- **`main()`/argparse 层零直接调用测试**: SC-4/SC-5 只通过 grep 源码文本验证 `--main-branch required=True`, 现有及新增测试均不存在任何 `gate.main([...])` 形式的直接调用。风险较低 (argparse `required=True` 是标准库行为), 但既然本 change 恰好改这一行为, 建议顺手补一条 `main(["--pr-branch","x"])` (不给 `--main-branch`) 断言 `SystemExit` 的测试, 比纯文本 grep 更贴近"真的会不会红"。
- **`test_sc12_default_true_lock` (:663) 核对结果 = 一致, 非独立缺陷**: Impact 表两条子句 ("24 处补 `main_branch="master"`" + "该测试断言由 `"main"` 改 `"master"`") 合起来完整覆盖了这个测试需要的两处编辑, 我逐行核对无遗漏。但它同样会撞上 C-4 的 subprocess 空洞 (该测试今日 0.001s 内完成、零 subprocess; D4 落地且未加桩时会变成真实网络调用), 不需要单独修, 随 C-4 一并解决。

---

## 机械性核对结果 (逐项复核, 均确认与 Spec 描述一致)

| 项 | Spec 声称 | 实测 | 结论 |
|---|---|---|---|
| SC-1 | `--branch main` 今日计数 2 (`:167`/`:243`) | `/usr/bin/grep -c` = 2, 行号吻合 | 一致 |
| SC-2 | `"branch": "main"` 今日计数 1 (`:270`) | = 1, 行号吻合 | 一致 |
| SC-4a/b/c | `default="main"` / `main_branch: str = "main"` / `--main-branch main` 今日各 1 | 各 = 1, 行号 :427/:300/:21 吻合 | 一致 |
| SC-5 | `default: main` 今日 1 | = 1 | 一致 |
| SC-9 | 缺 `main_branch` → `TypeError` | 最小 repro 确认 `TypeError: gate_check() missing 1 required positional argument: 'main_branch'` | 一致 |
| D4 锚定 pattern | 裸分支名尾段 glob 误判存在; `refs/heads/<name>` 锚定后判不存在 | 受控裸仓 (仅 `refs/heads/wip/master`): 裸名 `master` → RC=0 (误判); 锚定 `refs/heads/master` → RC=2 (正确) | 一致, D4 本身成立 |
| 既有 `gate_check(` 调用点 | 24 处, 显式传 `main_branch` 的 0 处 | `grep -c` = 24, 逐一读取确认全部关键字参数形式, 无位置参数误绑定风险 | 一致 |
| 测试基线 111 | 46+25+40 | `grep -c 'def test_'` 三文件分别 46/25/40; `test_pre_merge_gate` 实跑 46/46 通过, 0.056s, 零 subprocess | 一致 |
| `test_sc12` 描述 | 断言 "main"→"master" | 与"24 处"子句合并后完整覆盖, 核对一致 | 一致 (但见 C-4) |
| `gate_state_helper.py:32-34`/`:147` | 三常量 + 原样写入无校验 | 行内容逐字吻合 | 一致 |
| `ci_backends/base.py:29` | `not_found` 是 backend 层 Literal 值 | 逐字吻合 | 一致 |
| `pre_merge_gate.py:47-49` | verdict 三态常量 | 逐字吻合 | 一致 |
| 其它 skill 对 C.2.4 的引用 (config-loader/workflow-runner/branch-manager) | — | `grep -rn -- '--branch main'` 在这三个文件 = 0 命中 | 无跨 skill 泄漏 |

## 轮次记录

- R1-R3: 范围经历三次修正, 最终由 owner 裁定重定为 D1 (SKILL.md 散文 → 强制 helper 调用)。本轮 (R4) 不复核 R1-R3 的旧结论, 只审当前 263 行 proposal.md 本身, 依指引执行。
- R4 (本轮, qa-engineer 席位): 4 项 Critical (SC-3 恒红 / 唯一入口子模块根启动不了 / SKILL.md 第二份未加固散文 / D4 subprocess 隔离缺失且处方 no-op), 3 项 Major, 3 项 Minor。与本轮同席 tech-lead / code-reviewer 的独立报告在"唯一入口路径解析"与"test_sc22 mock 作用域"两点上收敛 (各自独立复现, 方法不同, 结论一致), 提升这两项发现的置信度; 本报告中的具体实验 (SC-3 逐字复现、裸仓锚定实验、双模块 mock 作用域实验、`fakegate.py` 结构化 repro) 均为本席位独立完成, 非转述。
