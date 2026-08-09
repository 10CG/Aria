---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-09T10:11:18.187Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R5 — code-reviewer 席位报告

被审对象: `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md` (271 行, R4-fix 版)
镜头: 调用块实跑 / 退出码穷尽 / `raw_message` 主通道 / 恒红恒绿对偶 / 条款间交叉一致性 / 修实例不修类

---

## 审计结论

### 已独立复核并**证实**的陈述 (不重复编排层自检, 只列我实跑过的)

| Spec 陈述 | 我的核验方式 | 结果 |
|---|---|---|
| §Why 假绿前提 | 实跑 `aether ci status --branch '<main-branch>' / 'master' / 'main' --in-flight --json` | 三者输出同形 `runs:[]` RC=0 ✅ 属实 |
| `grep -c 'aether ci status'` = 4, 落 `:167 :168 :243 :244` | 实跑 grep -n | ✅ 属实 |
| SC-1..SC-5「今日实测」列 (4 / 1 / 0 / 1,1,1 / 1) | 逐条实跑 | ✅ 全部属实 |
| D6 尾段 glob | 受控裸仓: 只有 `refs/heads/wip/master` 时 `--heads <r> master` → RC=0 且输出 `refs/heads/wip/master`; `refs/heads/master` → RC=2 | ✅ 属实 |
| §5 表 rc: 分支不存在=2 / remote 名不存在·坏 URL·不可达·权限·非 git 目录·remote 是普通文件=128 | 8 种失败态实跑 | ✅ 表内三档属实 |
| §6 插入点行锚 `:328 :338 :344 :345 :356 :357 :358 :366` | 逐行读 `pre_merge_gate.py` | ✅ 全部准确 |
| `SKILL.md:242 :252-255 :259 :260 :267 :270 :279` | 逐行读 | ✅ 全部准确 |
| `gate_check:378-386` `not_applicable` 通路 · `aether.py:117-135` 只在自身失败时抛 · `base.py:29` `not_found` | 逐行读 | ✅ 全部准确 |
| `write_gate_state()` 签名无 `gate_error` 形参、有 `raw_message` 形参 | 读 `gate_state_helper.py:115-124` | ✅ 属实 — **D8 选 `raw_message` 作主通道是对的**, 它真能落到持久化 gate_state |
| `gate_state_helper.py:32-34` 封闭枚举 / `:147` `"status": verdict` 原样写入 | 读源码 | ✅ 属实 |
| 24 处 `gate_check(` 调用点、显式传 `main_branch` 的 0 处 | grep 全仓 + grep `main_branch` 全测试文件 (唯一命中 `:669` 是断言不是调用) | ✅ 属实 |
| `test_sc12` `:663` / `test_sc22` `:710` | 读源码 | ✅ 属实 |
| 111 tests | `pytest --collect-only -q` | ✅ 属实 |
| Rule #6 SOT 逐字「`description` 或指令流程变动 ⇒ 一律第二行」 | 读 `skill-benchmark-exemption.md:33` | ✅ 逐字属实; 第三行「典型: authoring 向导」亦属实 (`:30`) |
| CLAUDE.md:79 / :35 引文 · commit `7661e96` 同提交同步 Rule #8 先例 | 读 + `git show --stat` | ✅ 全部属实 |
| 非目标的**分支字面量类**兄弟位置完整性 | 全 `aria/` python sweep (缺省值 / argparse 缺省 / `("master","main")` 元组三种形状) | ✅ 该类只有 `worktree_manager.py:170` + `fetch_gate.py:55`, Spec 列全了 |
| §1 调用块「主仓根 / aria 子模块根」两行 cwd 表 | 实跑 7 种 cwd | ✅ 这两行属实; **但表不完整, 见 C1** |
| `python3 "$GATE"` 从任意 cwd 可跑 (`ci_backends` / `path_coverage` import 解析) | 从 `/tmp` 实跑 `--help` rc=0 | ✅ 无问题 |
| abort 分支在非 git 目录 / bare repo 下 fail-CLOSED | 实跑 cwd=/tmp → rc=2; bare repo → `--show-toplevel` fatal → 落 abort | ✅ 属实 |
| detached HEAD / worktree 下 `git rev-parse --show-toplevel` | 受控仓实跑 | ✅ 均正常返回, 无新失效面 |

**质量评价**: 这一版的**事实基座**是四轮里最扎实的 —— 我抽查的每一条行锚、每一条 grep 计数、每一条 SOT 逐字引用都成立, 且 §Why 的核心前提经独立工具链复现。缺陷全部落在**新写的处方面**, 与四轮规律一致。

---

## Phase 1 — 规范合规性 / 陈述属实性

**判定: FAIL** (1 Critical)

### C1 (Critical) — §1 路径解析对 plugin 安装态与 2/3 子模块**结构上不可达**, 强制 abort ⇒ Rule #8 由「恒绿」翻成「恒红」

**锚点**: `proposal.md:48-53` (§1 调用块) · `:57-64` (cwd 表 + D3) · `:159` (D2) · `:189` (SC-12)

**实跑证据** (7 种 cwd 跑 §1 逐字四行块):

```
cwd=/home/dev/Aria                     rc=0  RESOLVED: .../aria/skills/.../pre_merge_gate.py
cwd=/home/dev/Aria/aria                rc=0  RESOLVED: .../aria/skills/.../pre_merge_gate.py
cwd=/home/dev/Aria/standards           rc=2  C.2.4 ABORT: pre_merge_gate.py 不可达, Rule #8 闸门无法执行
cwd=/home/dev/Aria/aria-orchestrator   rc=2  C.2.4 ABORT: pre_merge_gate.py 不可达, Rule #8 闸门无法执行
cwd=/home/dev/Aria/openspec            rc=0  (走第一分支)
cwd=/home/dev/Aria/aria/skills/phase-c-integrator  rc=0  (走第二分支)
cwd=/tmp                               rc=2  (fail-closed, 正确)
```

`find /home/dev/Aria -name pre_merge_gate.py` 全树**只有一份**, 在 `aria/` 内。`standards/` 无 `skills/` 目录; `aria-orchestrator/skills/` 只有 `dispatch-development` 与 `heartbeat-scan`。

**为什么这是 Critical 而不是边角**:

1. **CLAUDE.md 硬约束 1 逐字**把 `standards` 与 `aria-orchestrator` 与 `aria` 并列为受管的三个子模块 (「子模块 (aria / standards / aria-orchestrator) 的分支合并必须本地 `git merge` + 双推」); `SKILL.md:242` 逐字要求 C.2.4 在「执行 C.2 合并的目标仓根内调用 (子模块合并 → 子模块根)」。⇒ 这两个 cwd 是**成文契约要求的合法执行位置**, 不是异常输入。
2. §1 逐字规定「helper 不可达 ⇒ abort (exit 2), **不得降级放行**」。⇒ 在这两个仓根下, Rule #8 闸门**永久无法执行且不可绕过**, 合并被结构性阻死。
3. **更硬的一条**: aria-plugin 的成文分发形态是 marketplace 安装 (CLAUDE.md「其他项目经 Plugin 安装用 `/aria:` 前缀」; `SKILL.md:262` 与 `:610` 的 `${ARIA_PLUGIN_ROOT:-aria}` 就是为此设的, aria/CHANGELOG.md:2796 逐字「支持跨项目场景 (非 Aria 主项目时通过环境变量指定路径)」)。安装态下 plugin 根**不在**被合并项目的 git 树内 ⇒ `$(git rev-parse --show-toplevel)` 派生的两个分支**都不可能**命中 ⇒ 所有下游采用方 (Spec 自己在 `:255` 承认存在, memory 记 Kairos) 的 C.2.4 全部变成 abort。
4. 这正是本轮镜头 4 的对偶: **假绿的反面是恒红, 同样零信息量**。本 Spec 把 (b) 腿的恒绿换成了整条闸门在若干成文合法场景下的恒红。

**D2「两者都不能作为承重路径来源」的论证不成立**:

- 「`${ARIA_PLUGIN_ROOT}` 全仓从未被赋值」—— 属实但推不出结论: 它**本来就**是使用方提供的 env var, 成文形态是带缺省的 `${ARIA_PLUGIN_ROOT:-aria}` (同一文件 `:262` `:559` `:610` 三处在用)。
- 「`${CLAUDE_PLUGIN_ROOT}` 实测在本运行时亦为 unset」—— 我复现了 unset (进程环境中不存在名含 `PLUGIN_ROOT` 的变量), 但它是 **Claude Code 在 plugin 加载态注入**的变量, 「仓内直调态 unset」推不出「安装态 unset」。全仓 **65 处**在用 (`agent-creator/SKILL.md:33` · `aria-report/SKILL.md:61-62` · `session-closer/SKILL.md:94,97` · `state-scanner/SKILL.md:71` · `phase-b-developer/SKILL.md:91,304,319,320` …), 且 aria/CHANGELOG.md:1696 记录有一条专门的 `${CLAUDE_PLUGIN_ROOT}` **substitution runtime test**。⇒ 以单一运行时的一次量测排除一个全仓 65 处在用的机制, 证据面不足。

**如何修 (三选一, 须在 Spec 内定死到字符级)**:

- (a) 复合解析: 先取 `${CLAUDE_PLUGIN_ROOT}` / `${ARIA_PLUGIN_ROOT}`, 两个 git-toplevel 分支作 fallback, 全不中才 abort —— 保留 D2 真正解决的问题 (子模块根 cwd), 同时不砍掉唯一覆盖安装态的那条腿;
- (b) 显式把适用面收窄进 Spec: 声明本块**只**适用于 `aria` 子模块与 Aria 主仓, 并为 `standards` / `aria-orchestrator` / 下游采用方成文另一条路径 (否则就是 Rule #10 意义上的静默豁免);
- (c) 至少把 SC-12 扩成参数化: 主仓根 / `aria` 子模块根 / `standards` 子模块根 / 模拟安装态 (plugin 在树外) 四行都断言, 让上述失效**能红**。

现状下 SC-12 只测 `aria` 子模块根 —— 对本条失效**恒绿**, 属「负控测不到它要防的东西」。

---

## Phase 2 — 代码质量 / 按此 Spec 原样实施的正确性问题

### 优点 (Strengths)

1. **诊断主通道的选择经得起回源**: 我读了 `gate_state_helper.py:115-124`, `write_gate_state()` 确实有 `raw_message` 形参、确实无 `gate_error` 形参, `SKILL.md:255` 也确实逐字规定 `fail` 走 `raw_message`。D8 把 `gate_error` 降为 additive 副本、`raw_message` 升为必填主通道, 是本版最正确的一处改动 —— 它把 R4 的「无消费者诊断字段」真正接上了路由。
2. **占位符照抄现在会硬失败而非静默通过**: 我实测 `refs/heads/<MAIN_BRANCH>` → RC=2, `refs/heads/` → RC=2。⇒ AI 把 `<MAIN_BRANCH>` 原样抄进去时, 新核验会把它变成 `verdict=fail` 而不是 §Why 描述的那个假绿。这是本 Spec 真正的承重收益, 且我独立确认它成立。
3. **§7:148 的自反性**: 主动把 `gate_error` 示例的 `branch` 写成占位符以免与 SC-2 对撞 —— 这是「条款间交叉一致性」被认真做过的正面证据。
4. **分支字面量类的兄弟位置扫全了**: 我做了全 `aria/` python sweep, 该形状确实只有 `worktree_manager.py:170` 与 `fetch_gate.py:55` 两处, 非目标列全了, 且 `worktree_manager.py` 的实际路径 (`state-scanner/lib/`, 非 `scripts/lib/`) Spec 写对了。

### Important (应该修复)

#### M1 — SC-3 (期望 **1**) 与 D1/§1/§2/Impact 的「**两处都要改成强制 helper 调用**」互斥

**锚点**: `proposal.md:180` (SC-3) ⟂ `:42-44` (§1) · `:68` (§2) · `:158` (D1) · `:226` (Impact)

- D1 逐字: 「两处散文一起收敛为**强制 helper 调用**」「只改一处等于没改」; Impact 逐字: 「**两处**散文流程重整 (`### 步骤执行` :99 段 + `### C.2.4` :218 段)」。
- SC-3 逐字: `grep -c 'python3 "$GATE" --pr-branch'` **期望 1**, 且自称「**D1 承重断言**」。
- 两处都放调用块 ⇒ 计数 2 ⇒ SC-3 红; 只放一处 ⇒ D1 的「两处都要改成 helper 调用」未落地, 而 `### 步骤执行` (名字就是「步骤执行」, 是 AI 走流程时最先读的那段) 将只剩折叠说明、无可执行入口。
- 一条**计数恰为 1** 的断言在逻辑上不可能是「两处都要有」的承重断言。这是同一文件内「既立判据又违反它」的第 4 次实例。

**修法**: 把「§1 的块放在哪一处 / 另一处放什么 (指针? 折叠块? 什么都不放?)」写死到字符级, 并把 SC-3 的期望值改成与之一致 (若两处都放则期望 2, 并另加一条断言禁止两块内容漂移)。参考 memory `spec-underdetermination`: 承重算法必须钉到字符级, 否则两个实现者会得出相反结果。

#### M2 — 非目标声称 `no_ci_fallback` / stub backend 语义「由 SC-10 机械钉住」, 但 SC-10 钉不住它们

**锚点**: `proposal.md:217` (非目标) · `:187` (SC-10) · `pre_merge_gate.py:328` `:338` `:345`

SC-10 只走 `enabled=false` 这一条早退 (`:328`)。`no_ci_fallback` 走的是 `:338` (`backend is None`), stub backend NIE 走的是 `:366`/`:388`。三条是**不同分支**。

反例: 把 `_verify_branch_exists()` 插在 `:328` 与 `:338` **之间** —— SC-10 依然全绿 (enabled=false 更早返回), 但「无可用 backend + main 分支名给错」的场景由 `skip_with_warning` 绿变成 `fail`, `no_ci_fallback` 语义已破。本仓 `.aria/config.json` 实测 `no_ci_fallback: "skip_with_warning"` 是**live 配置**, 不是理论分支。

这正是 memory `delegate-verify` 的形状: 写「由 X 机械钉住」前必须去 X 核「它真做这件事吗」。

**修法**: SC-10 拆成三条 (或参数化三行): `enabled=false` / `ci_backends: []` (no-backend) / stub backend NIE, 每条都断言 `ls-remote 未被调用`。

#### M3 — D6 只锚了**前缀**, pattern 仍是 glob ⇒ 同一类的另一半未闭, 原假绿可原样复发

**锚点**: `proposal.md:96-99` (§5) · `:163` (D6)

受控裸仓 (仅 `refs/heads/master`) 实跑:

```
refs/heads/master     → RC=0   (正确)
refs/heads/mast*      → RC=0   ← 分支不存在却判「存在」
refs/heads/m[a]ster   → RC=0   ← 同上
refs/heads/maste?     → RC=0   ← 同上
refs/heads/*          → RC=0   ← 同上
```

`ls-remote` 的 pattern 是 glob, 锚定前缀只关掉了「尾段匹配」那半。任何含 `*` `?` `[` 的 `main_branch` 值仍判「存在」, 随后 `query_branch_in_flight("mast*")` 经 aether 返 `runs:[]` (我实测 aether 对任意分支名都返 `runs:[]` RC=0) ⇒ **§Why 描述的那个假绿逐字复发**, 只是入口换了一个字符类。

R2 为这一类花了一条 Critical; R4-fix 保留了只修一半的修法, 并在 D6 里以「两次独立受控实验复现」为据宣称该类已闭。

**修法**: 不要依赖退出码。取 `git ls-remote --heads <remote> <ref>` 的**输出**, 对 ref 名做**精确字符串相等**比对 (shell 侧 `grep -Fx`, python 侧 `==`); 或在传参前对 `main_branch` 做 glob 元字符校验并直接拒绝。

#### M4 — §5 退出码表**无 catch-all 行**, 且无任何 SC 钉住兜底分支

**锚点**: `proposal.md:101-110` (§5 表 + `:108` 的「本表自带完整分区」) · `:183-185` (SC-6/7/8)

- 表只有 4 行: `0` / `2` / `128` / `TimeoutExpired`。`:110` 的「⛔ 任何情形都不得当成「存在」放行」是**散文**, 表里没有 `else → fail` 这一行。实施者按表逐行写 `if/elif` 而不写 `else`, 落地就是 fail-OPEN —— memory `feedback_invariant_needs_failclosed_default` 逐字: 正向枚举对新值天然 fail-OPEN。
- SC-6 钉 rc=2, SC-7 钉 rc=128, SC-8 钉 timeout。**没有任何 SC 钉「未知 rc → fail」**。
- 表也漏了 `FileNotFoundError` / `OSError` 两个非退出码失败态 (git 不在 PATH / fd 耗尽等)。这不是假想: 同一 skill 的姊妹模块 `path_coverage.py:93` 逐字已经在 `except (subprocess.TimeoutExpired, FileNotFoundError, OSError)` —— 现成先例在 40 行外, 表却没吸收。Spec 自己的「待 R5 重点审」第 3 条正问这个, 说明作者知道有洞但没补。

**修法**: 表加一行「其余任何退出码 / 任何非 `TimeoutExpired` 异常 → `fail` + `kind="main-branch-verify-failed"`」, 并加一条 SC (例: mock 返回 rc=42 与 mock 抛 `FileNotFoundError`, 断言 `verdict=fail`)。

#### M5 — SC-8 要求在 gate 层新造第二份重试实现, 而该机制已存在

**锚点**: `proposal.md:185` (SC-8) · `:106` (§5 timeout 行) · `ci_backends/aether.py:36-39` `:164-184`

现状实测:

```
aether.py:38   RETRY_BACKOFF = (5, 15, 45)
aether.py:39   MAX_RETRY_ATTEMPTS = len(RETRY_BACKOFF)
aether.py:164  def _run_with_retry(self, args) -> tuple[int, str, str]
aether.py:180-183  except subprocess.TimeoutExpired: ... time.sleep(RETRY_BACKOFF[attempt])
```

而 `pre_merge_gate.py` **今天完全没有 `import subprocess`** (全文 2 处 `subprocess` 都在注释里)。Spec 要求 gate 层实现「3 attempts / backoff 5-15-45」, 却全篇未提这套常量与 `_run_with_retry` 已经存在、要不要复用。

⇒ 这个 change 的**根因论断**逐字是「同一算法有两份实现, 而 AI 走的是没被加固的那份」(`:19`), 而它的处方在自己新写的路径上**再造一份同算法的第二实现**。memory `fix-recurs-in-fallback` 逐字命中: 修复类 change 最易在自己新写的兜底路径重犯要治的病。

**修法**: 明写「复用 `ci_backends.aether.RETRY_BACKOFF` / `MAX_RETRY_ATTEMPTS`」或「把重试抽到共享 helper 并让 aether 侧改为调用它」, 二选一并落进 tasks; 顺带明确「gate 层要新增 `import subprocess`」这一事实 —— 它才是 `test_sc22` 转红的直接原因, Spec `:193` 已察觉现象但归因写成「24 处调用击穿基线」, 归因不准 (那 24 处是各自 TypeError, 与 `test_sc22` 的 patch 无因果)。

#### M6 — 「同形兄弟位置」只覆盖字面量类, 未覆盖 D1 自己点名的**根因类**; 最近的同形兄弟就在同一文件

**锚点**: `proposal.md:218` (非目标) · `:233` (follow-up 4 项) · `SKILL.md:189-191` + `:559`

非目标列的两处 (`fetch_gate.py` / `worktree_manager.py:170`) 属**分支字面量**类 —— 这一类我 sweep 过, 列全了 ✅。

但 D1 把根因定义为「**散文裸命令 + helper 两份实现**」。该类最近的同形兄弟在**同一个 SKILL.md 里**:

```
SKILL.md:189-191   C.2.4.5 primitive 调用:
                     - git fetch origin (bare, 更新所有 ref) — 强制, 失败 abort
                     - git -C <submodule> fetch origin — 每 submodule
                     - git -C <submodule> merge-base --is-ancestor MASTER_PTR FEATURE_PTR
SKILL.md:559       **Helper 实现**: ${ARIA_PLUGIN_ROOT:-aria}/skills/.../submodule_gate.sh
```

`submodule_gate.sh` 实测存在 (15624 bytes, 可执行)。形状与本 Spec 要治的完全一致: 散文给裸命令 + 存在一份加固过的 helper + 从无带参调用示范。非目标没提它, follow-up 四项也没有。

memory `fix-the-class` 逐字: 修实例必问「这形状还有几个兄弟位置」。

**修法**: 非目标里点名 C.2.4.5 (以及 C.2.5 的 `git-remote-helper` 降级路径) 属同一类但本次不修, 并把它加进 follow-up issue 列表。

#### M7 — Impact 表漏 `SKILL.md:262`, 实施后同一文件将并存两套互斥的 helper 路径解析约定

**锚点**: `proposal.md:226` (Impact SKILL.md 行) · `SKILL.md:262` `:559` `:610`

Impact 列出的 SKILL.md 落点是: 两处散文重整 · 四行裸命令去除 · `:270` 示例 · `:267` schema · `:279` 注记 · 步骤 6 补一句。**`:262` 不在其中**。

`:262` 逐字: `**Helper 实现**: ${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/pre_merge_gate.py`

⇒ 实施后, 同一文件里 `:243` 附近的新块用 git-toplevel 派生路径, `:262` 用 env-var 派生路径, `:559`/`:610` 也用 env-var 派生路径。**同一个 helper 在同一份文档里有两个互斥的定位约定**, 且 D2 刚刚论证过 env-var 那套「不能作为承重路径来源」—— 即本 Spec 一边宣布某约定不可用, 一边把该约定的三处原样留在同一文件里。这与本 Spec 的主旨 (「必须先把两份实现收敛成一条路径」) 直接对冲。

**修法**: 若 C1 采纳复合解析, `:262` 同步改成同一形态; 若不采纳, 至少把 `:262` 列进 Impact 并写明改成什么。

### Minor (建议修复)

1. **§3 拟补入 `SKILL.md:255` 的那句谓词不可判定, 且是 no-op** — `proposal.md:79` 逐字「若 `raw_message` 含 `gate_error` 诊断则一并 surface」。按 §7 的 schema (`:140-146`), `gate_error` 是与 `raw_message` **平级的顶层键**, 不在 `raw_message` 里面; 「raw_message 含 gate_error」在数据形状上不成立, AI 无从判断该条件何时为真。且 `SKILL.md:255` 已逐字规定 `fail` → 「输出 verdict + raw_message」, 而 §7 又规定 `raw_message` 失败时**必填** ⇒ 这句话不新增任何行为。建议改成「输出含 `gate_error` 键时, 一并 surface `gate_error.kind`」。

2. **SC-2 只禁 `main` 不禁 `master`, 允许同类硬编码原样存活** — `proposal.md:179`。`SKILL.md:270` 最自然的改法是 `"branch": "master"`, 它**通过** SC-2, 却把同一个硬编码类别原样复制了一遍 (且对以 `main` 为主干的下游采用方而言方向正好反了)。§7:148 已经示范了正解 (占位符形态) 但没写进 SC。建议 SC-2 改成同时禁 `main` 与 `master` 的正则形态。

3. **`remote` 保留缺省而 `main_branch` 必填, 两条相反判据无成文理据** — `proposal.md:93` (`remote: str = "origin"`) ⟂ `:81-89`/D5 (「参数必填」)。真正的理由是不对称的失效方向 (错 remote → 128 → fail-CLOSED; 错 branch → `runs:[]` → fail-OPEN), 这条理由成立但 Spec 一个字没写。建议补一句, 否则 Phase B 实施者或下一轮审计会重开这个问题。

4. **D9 的「在 path coverage 之前」这半条无任何 SC 钉住** — `proposal.md:116-128` / `:166`。SC-6 在核验点落到 `:358` **之后**时依然全绿 (fail + kind 照样产生), 所以 D9 只有前半条 (「在三早退之后」, 由 SC-10 部分覆盖, 见 M2) 是机械的。建议加断言: `evaluate_path_coverage` 在核验失败场景下 `assert_not_called`。

5. **SC-12 只覆盖 cwd 表两行中的一行** — `proposal.md:189`。「主仓根」那一行无断言; 且 SC-12 若在 `aria` 子模块内跑, 对 C1 描述的失效恒绿。建议参数化四行 (主仓根 / aria 子模块根 / 无 skills 的子模块根 / 树外 plugin)。

6. **Level 3 交付物在 SOT 内部有二义, Spec 未消歧** — `proposal.md:5` / `:230`。Spec 引的 `standards/openspec/project.md:118` (`| 3 | Full | Architecture changes | proposal.md + tasks.md |`) **逐字属实**, 与 CLAUDE.md:33 一致 ✅; 但同一 SOT 的 `:21` 另述「Level 3: `proposal.md` + `tasks.md` + `detailed-tasks.yaml` (双层)」。Impact 只列新建 `tasks.md`。建议在 tasks 阶段一句话定死要不要 `detailed-tasks.yaml`, 免得 Phase B 各行其是。

### 建议 (Recommendations)

- **C1 是本轮唯一的阻塞项, 且它的修法会连带改动 §1 调用块的字符**。由于 SC-3 / SC-12 都钉在那段字符上, 建议**先定 C1 的修法, 再一次性重排 §1 + SC-3 + SC-12**, 不要分两次改 —— 四轮规律显示分次改动正是新缺陷的主要来源。
- **M1/M2/M4/M5 有一个共同形状**: 承重条款用散文表达, 而钉它的 SC 覆盖面比条款窄。建议在收尾时做一次机械核对: 逐条 D1-D11, 写出「哪条 SC 在它被违反时会红」, 空白的那几条要么补 SC 要么把条款降级为非承重。这比再加一轮多席审计便宜 (memory `stop-adding-rounds`: 换新鲜眼睛 > 加轮; 但这里缺的是**映射表**不是眼睛)。
- **M3 的修法值得单独回归**: 它是「同一处第 N 次调错量」的形状 (memory `redfix-change-quantity` —— 别在退出码这个量上继续调, 换成「输出 ref 名精确相等」这个量)。

---

## Verdict

**FAIL** (1 Critical + 7 Major + 6 Minor)

| 级别 | 数 | 条目 |
|---|---|---|
| Critical | 1 | C1 |
| Major | 7 | M1 M2 M3 M4 M5 M6 M7 |
| Minor | 6 | m1–m6 |

**是否可以继续?** 需要修复。

**理由**: 事实基座 (行锚 / grep 计数 / SOT 逐字 / §Why 前提) 我逐条回源全部证实, 这是四轮里最扎实的一版; 但**新写的处方面**有一条结构性阻塞 (C1: 承重调用块在成文合法的执行位置上恒 abort, 把假绿换成恒红) 和一组「承重条款 ⟂ 钉它的 SC」错配 (M1/M2/M4/M5)。C1 不修则 Phase B 落地即在 `standards` / `aria-orchestrator` / 所有 plugin 安装态下阻死合并。

---

## 轮次记录

| 项 | 值 |
|---|---|
| 轮次 | R5 (owner 加配额后第 1 轮, `max_rounds` 4→6) |
| 席位 | code-reviewer |
| 被审版本 | R4-fix (271 行) |
| 本轮新造占比 (本席视角) | Critical 1/1 = 100% 由 R4-fix 新写; Major 6/7 由 R4-fix 新写 (M3 跨版沿用) |
| 与旧清单核对 | **未做** (按本轮指令: 范围两次重定, 只审当前文件本身) |
| 编排层 23 项机械自检 | 未复跑其数字面; 但抽验了 SC-1..SC-5 的「今日实测」列与全部行锚, 均属实 |
| 推翻的自检设计 | 无。但指出 SC-3 / SC-10 / SC-12 三条断言的**覆盖面**窄于它们自称承载的条款 (M1 / M2 / C1) |
| 只读约束 | 遵守。全部实验在 scratchpad 受控裸仓; 本仓只跑 grep / sed / git log / git ls-remote / pytest --collect-only / aether ci status; 零写入、零 commit、零 push |
