---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-09T10:28:14.116Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [backend-architect]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R5 — backend-architect 席位报告

镜头: 实现可行性与接口契约 —— 受控实验为主, 逐条判断「两个独立实现者读它会不会得到同一结果」。

对象: `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md` (271 行, R4-fix 版)。全部实验在 `/home/dev/Aria` 与 `/tmp/claude-1000/.../scratchpad` 下实跑, 命令与输出见各节。

---

## 审计结论

### 镜头 1 — §1 四行调用块路径解析: 五种 cwd 实测 (含独立复核 code-reviewer 席位已报的 C1)

实跑逐字复制 §1 四行块 (含 `[ -f ]` 判定与 `exit 2`), 分别在 5 种 cwd 下执行:

```
cwd=/home/dev/Aria                (主仓根)                rc=0  RESOLVED=aria/skills/.../pre_merge_gate.py (走第一分支)
cwd=/home/dev/Aria/aria           (aria 子模块根)          rc=0  RESOLVED=.../pre_merge_gate.py (走第二分支, 第一分支因 aria/aria/ 不存在而 miss, 已用 ls 确认)
cwd=/home/dev/Aria/standards      (standards 子模块根)     rc=2  C.2.4 ABORT: pre_merge_gate.py 不可达
cwd=/home/dev/Aria/aria-orchestrator (aria-orchestrator 子模块根) rc=2  C.2.4 ABORT: pre_merge_gate.py 不可达
cwd=<模拟第三方采用方仓> (/tmp 下新建纯净 git repo)         rc=2  C.2.4 ABORT: pre_merge_gate.py 不可达
```

`find /home/dev/Aria -name pre_merge_gate.py` 全树只有一份, 在 `aria/` 内; `standards/` 无 `skills/` 目录; `aria-orchestrator/skills/` 只有 `dispatch-development` 与 `heartbeat-scan`, 无 `phase-c-integrator`。

**这不是边角**: `git submodule status` 确证本仓有三个子模块 (`aria` / `aria-orchestrator` / `standards`), CLAUDE.md 硬约束 1 逐字把三者并列为「子模块合并必须本地 git merge」的受管对象, `SKILL.md:242` 逐字要求 C.2.4 「在执行 C.2 合并的目标仓根内调用 (子模块合并 → 子模块根)」——这是**成文契约要求的合法执行位置**。`standards/` 子模块自身 git log 可见真实 PR 合并记录 (`Merge fix/170-secret-hygiene-out-keys-correction`), `aria-orchestrator/` 有活跃 feature 分支 (`feature/m6-cost-model-telemetry` 等, 与 CLAUDE.md「项目状态」段一致) —— 两者都是会走 phase-c-integrator C.2 的真实场景, 不是假设。§1 逐字规定「helper 不可达 ⇒ abort (exit 2), 不得降级放行」⇒ 在这两个子模块根下, Rule #8 闸门**结构性、永久性、无绕过路径地阻死合并**, D1 落地即生效。

第五个 cwd (模拟第三方采用方仓) 进一步证实: `${CLAUDE_PLUGIN_ROOT}` / `${ARIA_PLUGIN_ROOT}` 在本运行时均 `UNSET` (`echo` 实测确认), 而 `${ARIA_PLUGIN_ROOT:-aria}` 是本仓 **48 处**引用 (`grep -rn '\${ARIA_PLUGIN_ROOT'`) 的既有 fallback 约定 (`SKILL.md:262` `:610` 均用此形态), `${CLAUDE_PLUGIN_ROOT}` 引用 **129 处**——但两者在全仓 grep 下**零处被真正赋值** (`grep 'ARIA_PLUGIN_ROOT='` 命中仅两份既有审计报告, 非代码)。这与 Spec §1 D2 的陈述本身一致 (Spec 说得对: 两个环境变量确实不能作为承重路径来源); 但同时说明: 该四行块**没有采用本仓自己的既有约定** (`${VAR:-aria}` 复合 fallback), 而是新发明了一套「仅两个 git-toplevel 分支」的窄化方案——这窄化方案物理上只能覆盖「脚本与目标仓同树」这一种拓扑, 结构性排除了三分之二的本仓子模块与全部下游采用方。

**核验「精确比对」类的修法是否可行** (为下面镜头 2 一并验证, 也适用于此处的修复方向讨论): 如果改为「复合解析: `${CLAUDE_PLUGIN_ROOT}`/`${ARIA_PLUGIN_ROOT}` 优先 → 两个 git-toplevel 分支 fallback → 都不中才 abort」, 在 `standards`/`aria-orchestrator` 场景下由于两环境变量本就 unset, 依然会走到 fallback 并 miss——**光加环境变量优先级不能单独解决这个问题**, 除非同时确保运行时真的注入了 `CLAUDE_PLUGIN_ROOT` (取决于 Claude Code 是否在这些 cwd 下把它设为指向 aria-plugin 的安装根, 本 Spec 未验证这一点)。

**独立复核说明**: 本发现与本轮 code-reviewer 席位报告的 C1 (`.aria/audit-reports/post_spec-R5-1786269298673-...-code-reviewer.md:69-96`) 结论一致 —— 我在其报告产出前独立设计并执行了同样的 5-cwd 实验 (含额外的「精确比对修法可行性」验证), 两次独立复现互相印证, 不是同一次实验的转述。

**severity**: critical。**blocks_phase_b**: true。

---

### 镜头 2 — §5 存在性核验 pattern 语义: `refs/heads/<name>` 锚定关闭了「尾段 glob」但没关闭「元字符注入」

受控裸仓 (`remote.git` + refs: `refs/heads/{master, mas, other, wip/master}`) 实测:

```
pattern="master"              (裸分支名)         → 匹配 master + wip/master, rc=0  (D6 已知问题, 复核一致)
pattern="refs/heads/master"   (D6 锚定形态)      → 只匹配 master,             rc=0  (合法场景, 正确)
pattern="refs/heads/nonexistent" (锚定+不存在)   → 无匹配,                    rc=2  (正确)
pattern="refs/heads/*"        (name 含字面 '*')  → 匹配全部 4 个 heads,        rc=0  ⚠️
pattern="refs/heads/mas*"     (name 含 '*')      → 匹配 mas + master,          rc=0  ⚠️
pattern="refs/heads/maste?"   (name 含 '?')      → 匹配 master,                rc=0  ⚠️
pattern="refs/heads/mas[t]er" (name 含 '[')      → 匹配 master,                rc=0  ⚠️
```

`git ls-remote` 的 pattern 匹配是 git 自己的 fnmatch 引擎, 与「裸名后缀匹配」是**两条独立的宽松规则**: 前缀锚定 `refs/heads/` 只关闭了第一条 (后缀匹配), 对第二条 (pattern 内的 `*`/`?`/`[...]` 被当 glob 展开) 完全不设防。**D6 的论证与 SC-6 都只验证了「裸分支名」这一种失效, 没有验证「`<name>` 本身含 glob 元字符」这另一种独立失效**——Spec 全文没有出现对 `--main-branch` 取值做 `git check-ref-format` 式合法性校验的任何要求, `:427` 的 `argparse` 改动 (`required=True`) 也只管「有没有传」, 不管「传的是不是合法 ref 分量」。

**可利用性评估**: 真实 git 分支名结构上不可能含 `*`/`?`/`[` (`git check-ref-format` 本身禁止), 所以**正常路径**下 (`--main-branch` 传一个真实存在的分支名) 不会触发。但 `--main-branch` 是自由文本 CLI 参数, 没有任何东西阻止调用方 (配置误写 / 变量插值出错 / 未来某处拼接 bug) 传入一个含元字符的字符串——一旦发生, 结果是**该核验对任何非空仓库恒返回「存在」**, 与 Spec §5 结尾「⛔ 任何情形都不得当成「存在」放行」的不变量直接相悖, 且恰好是本 Spec 要新增的这条腿自己的失效模式, 不是既有代码的.

**验证了一个可行的修法** (非仅指出问题): 不要只信 `--exit-code` 的 RC, 额外解析 stdout 并要求**恰好一行**且该行 ref 字段与期望值 `refs/heads/<name>` **逐字符串相等**:

```
pattern="refs/heads/*"      → 输出的 4 行没有一行字面等于 "refs/heads/*"  → 精确比对正确拒绝 (验证通过)
pattern="refs/heads/master" → 输出行字面等于 "refs/heads/master"        → 精确比对正确放行 (验证通过)
```

命令与完整输出见上文 Bash 记录 (`glob-test/work`)。这个修法零额外依赖, 与 Spec 既有的「core」(`git` + stdlib) 承诺兼容。

**severity**: major (非阻塞主路径, 但 Spec 对 D6「已关闭」的表述与本表 SC-6 的覆盖面均不完整, 且核心不变量在此残留路径上被违反)。**blocks_phase_b**: false (建议 Phase B 落地时一并加精确比对, 不必回炉 Spec)。

---

### 镜头 3 — §5 退出码表完备性: 表格自称「完整分区」, 实测证伪

```
git 二进制缺失 (PATH 清空后 subprocess.run(['/nonexistent/git', ...])):
  → Python 抛 FileNotFoundError, 不产生 returncode (进程从未启动)

非 git 目录 + 命名 remote 'origin' (无法解析):
  → rc=128, "fatal: 'origin' does not appear to be a git repository"  (与表中「remote 名不存在」一致, 确认无误)

非 git 目录 + 直接 URL (file:///nonexistent/path.git):
  → rc=128, 同上错误族  (确认无误)

--exit-code --heads --bogus-flag origin ... (用法错误):
  → rc=129, "error: unknown option `bogus-flag'" + usage 提示   ⚠️ 表外新值
```

表格现有 4 行 (0/2/128/TimeoutExpired) 外, 实测另有两类真实会发生的情形未被覆盖:

1. **`FileNotFoundError` 不是退出码, 是 Python 异常** —— 若实现直接 `subprocess.run(["git", "ls-remote", ...])` 不包一层 `try/except`, git 二进制缺失时会是**未捕获异常**导致进程崩溃, 而不是走表中任何一行的「fail + kind=...」优雅路径。这与「⛔ 任何情形都不得当成存在放行」的精神不冲突 (崩溃也不会误判成「存在」), 但与 Spec 别处反复强调的「不得静默降级 / 必须走结构化 fail」原则不一致——一个未捕获异常会让整个 `pre_merge_gate.py` 主进程非 0 退出且没有 JSON 输出, 调用方 (`SKILL.md` 步骤 6) 拿不到 `raw_message`/`gate_error` 可 surface, 退化成比「fail 但有诊断信息」更差的用户体验。
2. **129 (usage error) 落在表外**, 表格声称「本表自带完整分区, 不依赖越界援引」这一断言被证伪——虽然 129 在正确实现下不该被触发 (触发条件是实现自身的 flag 拼写错误), 但作为「完整分区」的字面主张, 它确实不完整; 更重要的是表里没有一条**兜底/catch-all** 规则说「非 0/2/128 且非 TimeoutExpired 的任何返回值一律按 `main-branch-verify-failed` 处理」, 只逐一列举了已知三个值。两个独立实现者面对「表里没写的第四个值」时没有唯一可依据的条款。

**直接复用点**: `path_coverage.py:93` 的 `except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as exc:` 三合一异常处理**恰好覆盖上述两类情形的第一类** (`FileNotFoundError` 是缺二进制, `OSError` 覆盖权限拒绝等其余 OS 层失败, `TimeoutExpired` 与 Spec 自己的重试需求呼应)。它是同一个 `scripts/` 包内的既有代码, 签名 `_run_git(args, cwd) -> (bool, stdout, err_summary)` 与 `_verify_branch_exists()` 要做的事高度同构 (调用 git 子进程、统一错误落地成一个 ok/err 二元组)。Spec 的 Impact 表只写"`_verify_branch_exists()`" 一个新函数名, 完全没提是否复用/镜像这个既有模式——这是可核实的空白, 不是猜测。

**severity**: major (「待 R5 重点审」条目 3 点名要求核实这张表是否穷尽, 结论是否, 但不阻断: 只要 Phase B 实现时补上 catch-all + 三合一异常捕获, 无需改 Spec 决策本身)。**blocks_phase_b**: false。

---

### 镜头 4 — 重试实现: Spec 要求为 gate 层新造第二份「3 attempts / 5-15-45」, 且全篇未提复用

```
grep -n 'RETRY_BACKOFF\|MAX_RETRY_ATTEMPTS\|_run_with_retry\|复用.*retry' proposal.md   → 零命中
grep -n '重试\|backoff\|5-15-45\|3 attempts' proposal.md → 仅 §5 表格行 + SC-7/SC-8, 均只重申「按 SKILL.md:259 既有规范」, 未提源码级复用
```

`ci_backends/aether.py:38` 确认 `RETRY_BACKOFF = (5, 15, 45)` 与 `MAX_RETRY_ATTEMPTS = len(RETRY_BACKOFF)` 是**模块级常量**(非 class 绑定), 可被任意模块 `from ci_backends.aether import RETRY_BACKOFF, MAX_RETRY_ATTEMPTS` 直接导入; 而 `_run_with_retry()` (`:164-187`) 是绑定 `self.binary`/`self.timeout` 的 **AetherBackend 实例方法**, 不能原样脱离 `AetherBackend` 直接调用 (它 `subprocess.run([self.binary] + args, ...)`, 目标是 aether 而非 git)。

因此结论精确到: **常量层面可以零成本直接复用, 循环/重试结构层面需要抽一个通用小工具函数才能复用** (例如 `run_with_retry(argv: list[str], timeout: int, backoff: tuple[int,...]) -> (rc, stdout, stderr)`, 与 `binary` 无关, `AetherBackend._run_with_retry` 与新的 `_verify_branch_exists()` 都可以调用它)。Spec 目前的 Impact 表 (`:227`) 只列 `_verify_branch_exists()` 一个新符号, 没有任何迹象表明会做这层抽取或至少导入共享常量——按目前文字, 两个独立实现者最可能的产出是: 在 `pre_merge_gate.py` 里手写一份 `for attempt in range(3): ... time.sleep([5,15,45][attempt])`, 字面量硬编码, 与 `aether.py` 的版本文本上几乎相同但物理上是第二份。

这与本 Spec §Why 的开篇论断直接对照: 「根因: 同一算法有两份实现, 而 AI 走的是没被加固的那份」——本 Spec 正在**为一个不同的目标 (git ls-remote 重试) 重演同一形状**: 如果日后 `RETRY_BACKOFF` 因故调整 (例如 aether 服务端限流策略变化), 硬编码在 `pre_merge_gate.py` 里的第二份 `(5,15,45)` 不会跟着变, 两处重试策略静默漂移——这正是 memory `fix-the-class` 条目描述的「修实例不修类」的一个新实例: 本 Spec 修的是「main-branch 存在性判定的两份实现」这个类, 但对「重试策略的两份实现」这个同形状的类没有推广处理。

**不是虚假等价**: 我确认了两者调用的子进程不同 (`git` vs `aether` 二进制), 所以不能整段复制 `_run_with_retry`; 但「重试循环结构 + backoff 元组」与「目标二进制是谁」是可分离的关注点, 不构成「必须重写」的理由。

**severity**: major (不阻断——按现状实现依然功能正确; 但与 Spec 自身根因论断直接矛盾, 且此刻 (Phase B 尚未写代码) 是修正成本最低的时间点, 一旦 Phase B 照抄字面量, 之后再抽取需要动两处并补测试)。**blocks_phase_b**: false (建议 Phase B 任务列表加一条: `_verify_branch_exists()` 的重试从 `ci_backends.aether` import `RETRY_BACKOFF`/`MAX_RETRY_ATTEMPTS`, 或抽出共享 helper; 不需要现在改 Spec 决策记录)。

---

## Verdict

**FAIL** —— 存在 1 项 Critical (镜头 1: §1 四行调用块在两个本仓子模块根与全部下游采用方场景下结构性 `exit 2` 恒 abort, 把「main 判定恒绿」换成了「Rule #8 闸门在成文合法执行位置上恒红」, 二者对系统的伤害是同一量级, 只是方向相反)。

另有 3 项 Major (镜头 2 glob 元字符残留 / 镜头 3 退出码表不完整 + 缺 catch-all / 镜头 4 重试逻辑二次复刻), 均不单独阻断 Phase B, 但建议在 C1 修复的**同一次改动**里一并处理 §1/§5 的字符 (Spec 自己在「待 R5 重点审」结尾也提示「分次改动正是新缺陷的主要来源」, 与 code-reviewer 报告的建议一致)。

若仅论「本席位单独锁定的镜头 2/3/4」而不计入 C1 (万一 C1 已被其他机制单独裁定不算数), 三项 Major 单独不会把 verdict 从 PASS_WITH_WARNINGS 推到 FAIL; 但 C1 是我独立复现、确凿、且与 Spec 自身写明的不变量 (「不得降级放行」) 正面冲突的结构性阻断, 不能计入「拿不准」区间, 故本席位独立给出的 verdict 是 **FAIL**。

---

## 轮次记录

R5 (本轮, backend-architect 席位): 实读 `proposal.md` 全文 (271 行) + `SKILL.md` 指定段落 (`:99` `:218` `:242` `:252-255` `:259` `:262` `:279`) + `pre_merge_gate.py` 全文 + `ci_backends/aether.py` 全文 + `path_coverage.py` 前 120 行 + `gate_state_helper.py` 全文。实跑 5-cwd 四行块复现实验、7 种 ls-remote pattern 受控裸仓实验 (含一个「精确比对」候选修法的正反两向验证)、4 种退出码/异常边界实验、`RETRY_BACKOFF` 复用可行性静态核验。与本轮 code-reviewer 席位的 C1 独立收敛 (交叉验证, 非转述); 未见本轮其余席位覆盖镜头 2/3/4。产出 1 Critical + 3 Major, verdict=FAIL。
