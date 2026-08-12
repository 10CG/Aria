# Proposal: premerge-gate-branch-existence

> **Status**: 📝 **Draft (A.1)** — 由 [DEC-20260812-001](../../../docs/decisions/DEC-20260812-001-premerge-gate-spec-split.md) 从
> `premerge-gate-mainbranch-failclosed` 拆出的 **A 侧**。
> **Created**: 2026-08-12
> **Spec Level**: **2** (proposal only) —— 无架构变更 (§5 已**钉死** A 不动 `aether.py`) ·
> 无跨仓**内容**同步面 (不碰 v2.0 弃用删除面 / `.aria/config.template.json` 键名面) · 无破坏性**契约**变更。
> ⚠️ **两处不能省略的限定** (R1): (a) **发版同步面照常适用** —— MINOR ship 必触发 CLAUDE.md 的
> 「子模块 5 文件 + 主仓 gitlink + VERSION + badge + i18n」, 清单落 §Impact (Level 2 无 tasks.md 承载);
> (b) **契约不破但运行时行为翻转**, 见 §行为兼容面。
> **版本**: **MINOR** —— 本 change 全部为 additive (新增可选参数 + 新增核验步 + 新增 additive 输出键),
> **API 形状层零破坏面** ⇒ 不触发 `pre_merge_gate.py:68/:116` 的 v2.0 弃用到期承诺
> **关联 Issue**: [aria-plugin #137](https://forgejo.10cg.pub/10CG/aria-plugin/issues/137)
> **代码落点**: `aria/` 子模块 `skills/phase-c-integrator/`; Spec 落主仓 (Rule #5)
> **姊妹 Spec**: `premerge-gate-mainbranch-failclosed` (B 侧, Level 3, MAJOR)
>
> ⚠️ **本 Spec 的输入不是从零起草的** —— 下列材料承自 A/B 拆分前的八轮 40 席审计
> (post_spec R1–R5 + post_planning R1–R4), 逐条注明来源。**但拆分后的组合是新的, 须重新过 post_spec。**
>
> 📌 **本版 = R1-fix** (post_spec R1: 5 REVISE / 0 PASS, 6C+14M+6m)。R1 的两条 Critical 都出在
> **拆分时新写的声称**上 (划界承重句的适用层 / Rule #6 定档), 不在承自八轮的事实上 ——
> 处置逐条内联在各节, 不在本文件累积审计叙事 (memory `audit-trail-not-in-spec`)。

---

## Why

### 症状 (承前, 逐字保留)

Rule #8 pre-merge gate 的「main 无 in-flight CI run」这条腿在本项目上**恒真**。
后端**结构上无法区分**「分支不存在」与「分支没有 in-flight run」—— 实测 `--branch main`
与 `--branch master` 返回完全同形 (`status:ok`, `runs:[]`, RC=0); `ci_backends/aether.py:117-135`
只在 aether 自身失败时抛。二者都产出 `InFlightStatus(runs=[])` ⇒ 判 **green**。

### 根因 (承前, 逐字保留 —— ⚠️ 拆分时漏引的就是这一段)

> 「**同一算法有两份实现, 而 AI 走的是没被加固的那份**」——
> `SKILL.md` §C.2.4 的散文流程共两处、合计 4 行可照抄的裸命令 (`:167` `:168` `:243` `:244`),
> 而 `gate_check()` 完整实现了同一套流程。**AI 走散文那份**; SKILL.md 从无带参 helper 调用示范。

### 本 Spec 的范围判定 (DEC-20260812-001 §3)

**存在性核验单独就消除了 `gate_check()` 这份实现里的那个不可区分性** —— 传 `--main-branch main`
而 `main` 在远端不存在时, 核验判 `fail` + `kind="main-branch-not-found"`, **不再 green**。

> ⚠️ **限定必须带着走** (R1 四席独立命中): 上句**只在 `gate_check()` 层成立**。
> DEC §3 与本节上一版都只引了 §症状 (后端不可区分性), **漏引了紧邻的 §根因** ——
> 于是「消除不可区分性」被读成了「关掉恒绿腿」。**两份实现里只加固了一份**, 残余见下节。

⇒ 本 Spec **只做这一件事** (加上它在文档侧的必要同步, 见下), 且它在代码面是**纯 additive**:
- `gate_check(..., remote: str = "origin")` **带默认值** ⇒ 既有 **25 个**调用点全部零破坏
  (⚠️ 但 `main():435` **必须**改一行接线, 口径见 §版本);
- 新增核验步插在既有早退之后 ⇒ 既有分支语义零改动;
- `gate_error` 是 **additive 可选键** ⇒ 六键 schema 零改动。

⚠️ **文档侧不是可选的** (R1): 往 `gate_check()` 插新步 ⇒ 必须同批给 `SKILL.md` §C.2.4 执行流程补对应
**编号步骤** (v1.65.0 补步骤 2.5 的同形先例)。**这件与执行流程的同步必须在 A 内解决, 不能推给 B** ——
否则文档流程与 helper 流程当场分叉 (违反规则 #3)。**代价**: 它使 Rule #6 落**第二行 ⇒ 照跑 AB** (见 §Rule #6)。

**⛔ 不在本 Spec 范围** (全部留 B 侧):
`--main-branch` 改必填 (破坏性, 拉 MAJOR 与弃用面) · `SKILL.md` 两处散文流程 (`:167` `:168` `:243` `:244`
四行裸命令) 收敛为 helper 调用 (D1) · 折叠块 · helper 路径解析 spike · v2.0 弃用删除面 ·
**B 侧自己的**发版同步面与 Rule #6 AB。

> ⚠️ **发版同步面与 Rule #6 AB 不可整体划给 B** (R1 更正): 二者的触发点都是「**本 change 自己的发版**」。
> A 按 MINOR **独立发版** ⇒ A 有 A 的那一份, **义务结构上无法转移**给一个至今「不具备进 Phase B 条件」
> 的姊妹 Spec。此处只排除 B 侧那一份 (弃用删除面 / `config-loader` 三件套)。A 的份额见 §Rule #6 与 §Impact。

> **为什么必填留 B**: 它是**纵深防御的第二层** (防「显式传错分支名」), 价值真实,
> 但**不是关掉恒绿腿的必要条件**; 而它一旦进来就拉着 MAJOR ⇒ v2.0 弃用到期承诺
> ⇒ 跨两仓 5 文件 + 两个 legacy key + `.aria/config.template.json` 这个仓外受众落点。

### ⚠️ 残余暴露 —— A ship **不**构成 #137 闭环

**逐字声明**: **A 落地后, `SKILL.md` 散文裸命令这条执行路径仍恒绿, 直到 B 侧 D1 收敛两份实现。
A ship 不构成 aria-plugin #137 的闭环, 不得据 A ship 关闭 #137。**

三条实测支撑 (R1 四席独立复现):

| 证据 | 实测 |
|---|---|
| `SKILL.md:243` 逐字 | `aether ci status --branch main --in-flight --json` —— **分支名硬编码**, 且这是 §C.2.4 **执行流程编号步骤本体** (非注释/折叠块) |
| 本仓 `git ls-remote --heads origin main` | **零行 + RC=0** ⇒ `:243` 那条命令**今日就是恒绿腿的活体** |
| `workflow-runner/SKILL.md` grep `pre_merge_gate.py` | **零命中**; 唯一表述是 `:329`/`:351`「re-invoke: phase-c-integrator C.2.4」⇒ **编排层把执行交回散文流程** |

**残余的精确形态** (A 落地后仍成立, 这是可现场复现的那句): 本 Spec 给执行流程新增的核验步用
`<MAIN_BRANCH>` 占位符, 而**步骤 3 仍逐字硬编码 `main`** —— 在 `main ≠ master` 的仓上二者**指向不同分支**:
按散文逐字执行 ⇒ 核验步查 `master` (存在, 放行) → 步骤 3 查 `main` (`runs:[]`, RC=0) ⇒ **verdict 仍 green**。
⇒ 本 Spec 要求在新增步骤处**逐字标注这条不一致**并指向 B 侧 D1 (见 §Impact 的 `SKILL.md` 行)。

**为什么不为它建 SC**: 散文路径由 AI 读文档执行, **没有任何机械 harness 能"执行 SKILL.md 散文"**;
唯一能机械化的形态是「断言缺陷仍在」的哨兵 —— 它在 B 落地后必须被删, 是 landmine
(memory `feedback_false_green_dual_is_permanent_red`: 判据是「该信号在健康常态下应是什么值」)。
⇒ **不编造这条量**。残余以上面那句可现场复现的声明留痕, 闭环判据挂 B 侧 D1。

---

## What Changes

### 1. 新增 `--remote` 参数 (additive)

`gate_check(..., remote: str = "origin")` / CLI `--remote`, 默认 `origin`。

**失效方向不对称的理由** (承 B 侧原 R5 结论): 错 `remote` 走 **128** ⇒ fail-CLOSED;
错 `branch` 走 `runs:[]` ⇒ fail-OPEN。**这就是 `remote` 可以有缺省的理由**
(而 `main_branch` 能否有缺省是 B 侧的题目)。

### 2. 分支存在性核验 — 判据是**精确字符串比对**, 不是 pattern 匹配, 更不是退出码

在查 in-flight **之前**, 独立核验 `<main_branch>` 在 `<remote>` 上确实存在。

**⚠️ 三次受控实验才收敛到正确判据** (前两次均 fail-OPEN):

| 修法 | 实测 | 结论 |
|---|---|---|
| 裸分支名 `--heads <r> master` | 远端只有 `refs/heads/wip/master` 时返 **RC=0** (尾段 glob) | ❌ fail-OPEN |
| 锚定 `--heads <r> "refs/heads/master"` | **锚定也关不掉 glob** —— 受控裸仓实测 `refs/heads/mast*` / `refs/heads/m[a]ster` / `refs/heads/maste?` **仍全部命中** | ❌ 仍 fail-OPEN |
| **对返回的 ref 名做精确字符串比对** | 不依赖 pattern 语义 | ✅ **本 Spec 采用** |

⇒ 判据: **远端返回的 ref 名列表中, 是否存在一条 `== "refs/heads/" + main_branch` 的精确匹配**。

**🔴 两条更底层的事实 (2026-08-11 主 loop 受控裸仓实验; 八轮 40 席从未浮出)**:

- **`ls-remote` 零命中亦返 `rc=0`** —— 实测 `refs/heads/wibble` (不存在) ⇒ **rc=0 + 零行输出**
  ⇒ **任何以退出码判存在性的实现, 对本 Spec 的主场景天然 fail-OPEN**。
  ⇒ **判据必须落在解析出的 ref 名列表上, 不得读退出码。**
- **⛔ 不得使用 `--exit-code`** —— 实测它使「无命中」返 **rc=2**。那是实现者最可能选的
  「更简单」替代路径, 但本 Spec 的退出码表以「其余一切非零 ⇒ `main-branch-verify-failed`」收口
  ⇒ **一个合法缺失的分支会被误分类成「查询失败」而非「分支不存在」**。
  ⚠️ **抓住它的是 `SC-A-zero`, 不是 SC-A6** (R1 更正 —— 上一版此处写「SC-M6」, 既是悬空引用[A 号段是 `SC-A*`],
  归因也错): 受控实测 `--exit-code` 实现下, SC-A6 (远端有 `wip/master`) 与 SC-A13 (`mast*`) 的 ref 列表**非空** ⇒
  rc=0 ⇒ 精确比对判 `not-found` ⇒ **两条都绿, 结构上碰不到这条分支**; 只有**零命中**的 SC-A-zero 拿到 **rc=2**
  ⇒ 落 catch-all ⇒ `verify-failed` ≠ `not-found` ⇒ 红。
  ⇒ **SC-A-zero 是「⛔ 不得用 `--exit-code`」的唯一机械锚, 不得删。**

**具体实现形态** (是否仍借 `ls-remote` 取列表 / 如何解析) = **Phase B spike**;
验收由 **SC-A6 + SC-A13 + SC-A-zero 三条**钉住 (R1 更正: 上一版漏了 SC-A-zero,
而它正是唯一能红的那条 —— 见上一段的 `--exit-code` 归因)。

| 情形 | 判据 | 输出 | 重试? |
|---|---|---|---|
| ref 列表含**精确匹配** | — | 继续原流程 | — |
| ref 列表**取到了但无精确匹配** | 分支不存在 | `verdict=fail` + `gate_error.kind="main-branch-not-found"` | **否** |
| subprocess timeout (`TimeoutExpired`) | 查询失败 | 按 `SKILL.md:259` 既有规范重试; 仍超时 ⇒ `fail` + `kind="main-branch-verify-failed"` | **是** |
| **其余一切** — 非零退出码 (实测 remote 名不存在 / 坏 URL / 网络不可达均为 **128**) · `FileNotFoundError` (git 二进制缺失, **抛异常无退出码**) · `OSError` · **`UnicodeDecodeError`** (见下) · 输出不可解析 · **任何未枚举情形** | 查询失败 | `verdict=fail` + `kind="main-branch-verify-failed"` | **否** |

> 本表以「其余一切」**收口 (catch-all)**, 不是正向枚举 —— 正向枚举对未来新增返回码天然 fail-OPEN。
> **不援引 `SKILL.md:260` 的 exit 1-126**: 实测真实失败码是 **128**, 在区间外; 且 `:260` 自带
> `127 → no_ci_fallback` 会使 verdict 变 **green**。

> ⚠️ **`UnicodeDecodeError` 必须显式点名** (R1): git **不保证 ref 名是合法 UTF-8**, 而实跑
> `python3 -c "print(issubclass(UnicodeDecodeError, OSError))"` = **False**
> (MRO: `UnicodeDecodeError → UnicodeError → ValueError`) ⇒ §5 指定的三合一 except 元组
> `(TimeoutExpired, FileNotFoundError, OSError)` **结构上接不住它**。照 §5 两轴逐字照做
> 且用 `text=True` 的实现会让它**裸抛穿过 `gate_check()`**, 而 `workflow-runner` 的 verdict 路由
> 只有四条臂、**无异常臂** ⇒ 路由未定义。由 **SC-A14 的参数化探针**钉住 (不是靠再列一个枚举)。

> ⚠️ **catch-all「不重试」的权衡, 显式记录而非留给实现者推断** (R1): git 对**一切**远端错误
> (坏 remote 名 / DNS / TCP reset / 认证) 统一返 **128** ⇒ 本表把「瞬时网络故障」与「永久性坏 remote 名」
> 合并为不可重试的 fatal; 而 `workflow-runner/SKILL.md:337` 逐字 exit condition 3「`verdict=fail` → 转为
> stop (fatal)」⇒ 一次短暂不可达即 fatal、不可 resume。**本 Spec 仍取不重试**, 理由: fail-CLOSED 与
> catch-all 的设计正确性优先, 且今日 aether 路径遇网络错误同样直接 fail (A 只是把失败点提前)。
> **代价已知且在 168h 无人值守场景下会被放大** —— 若实测成为可用性问题, 走 follow-up, **不在本 Spec 放宽**。

⛔ 任何情形都不得当成「存在」放行。

### 3. 核验点 = 三个早退**之后**、`evaluate_path_coverage` **之前**

**5 个逻辑锚位 / 8 个行号** —— 已由主 loop 逐个实读命中 (基线 `af87cae`, 落地时按内容锚重定位)。
> 计数法 (R1 更正; 上一版只写「五个行锚」却列了 8 个行号): **逻辑锚位 5** =
> `enabled` / no-backend / precheck / path-coverage / in-flight; **行号 8** = 下方括号内逐个。

```
:328  if not cfg["enabled"]:            → 早退 (green)
:338  if backend is None:               → 早退
:344  ok, precheck_err = backend.precheck()
:345  if not ok:                        → 早退 (fail)
★ 存在性核验 (本 Spec 新增)              ← 唯一合法插入点
:356  pc: dict[str, Any] | None = None
:357  if cfg.get("path_coverage_enabled", True):
:358      pc = evaluate_path_coverage(main_branch=main_branch, pr_branch=pr_branch)
:366  in_flight = backend.query_branch_in_flight(main_branch)
```

**在三早退之后**: 否则 owner 显式关闭的闸门与 `no_ci_fallback` 既有降级会被变成 `fail`。
**在 path coverage 之前**: 它更早消费 `main_branch`, 放它之后等于放行一次未核验的使用。

⚠️ **「唯一合法插入点」这句由 `SC-A-order` 机械钉住** (R1) —— 上一版对三个早退写了「`assert ls-remote 未被调用`」
的因果断言, 却对 `evaluate_path_coverage` 这条**同族顺序约束零断言** ⇒ 把核验插在 `:358` **之后**的实现
12/12 全绿而本节被违反 (`path_coverage` 先跑但 `decision=unknown` 不改 verdict)。
**认出了类只推广了一半** —— 讽刺的是本 Spec 自己在 SC-A10b 就写着「兄弟早退不同步则该类只修了一个实例」
(memory `fix-the-class`)。次生实害: 违规实现下 `main_branch` 不存在会先让
`git diff --name-only <main>...<pr>` 失败 ⇒ `decision=unknown` ⇒ 按 `SKILL.md:253` 的 surface 义务
AI 必须报「path coverage 评估失败 (`reason=git-diff-failed`)」, **把人指向 git/main ref, 而真因是分支名不存在**。

#### 查询作用域 (cwd 轴) —— 正面规定, 不只否定式

⛔ **不得为解析路径而 `cd`** —— 那会使 `ls-remote` 查错仓 (主仓与 `aria` 子模块都有 `master`, 会 RC=0 假通过)。

✅ **正面规定** (R1 补 —— 上一版只给了上面那条否定式, 没答"那用哪个 cwd"):
存在性核验的 git 子进程 **必须与 `evaluate_path_coverage` 同源仓根** —— 即从**进程 cwd** 出发, 按
`path_coverage.py:_repo_root()` 同款 (`git rev-parse --show-toplevel`) 解析, 并**显式**作为 `cwd=` 传给 subprocess
(`path_coverage.py:78/:91` 的 `_run_git(args, cwd)` 形状)。
⛔ **不得从 `__file__` / 脚本所在目录解析** —— helper 住在 `aria` 子模块内, 那样会去查 `aria-plugin.git` 的 `origin`,
而不是 C.2 正在合并的目标仓。这与 `SKILL.md` 步骤 2.5 已有的执行上下文契约逐字一致
(「在执行 C.2 合并的目标仓根内调用 (子模块合并 → 子模块根)」)。

> **实测背景**: `git -C /home/dev/Aria remote -v` → `10CG/Aria.git`; `git -C /home/dev/Aria/aria remote -v` →
> `10CG/aria-plugin.git` —— `origin` 这个名字在两个仓解析到**两个不同 repo, 且两边都有 `master`**。
> 由 `SC-A-cwd` 钉住可证伪的那一半 (见 SC 表的诚实限制说明)。

### 4. 诊断信息: `raw_message` 是主通道, `gate_error` 是 additive 副本

`SKILL.md:255` **逐字**规定 `fail` 的 surface 通道是 `raw_message`
(「`fail` → BLOCK + 输出 verdict + raw_message, phase-c-integrator return failure」),
且 `write_gate_state()` 签名无 `gate_error` 形参。

- **`raw_message` 主通道 (必填)**: 失败时须写入人类可读诊断, **含分支名与 remote 名**,
  且**明确区别于「无 in-flight run」**;
- **`gate_error` 是 additive 可选结构化副本** (沿用 v1.65.0 `path_coverage` 先例):

```json
"gate_error": {
  "kind": "main-branch-not-found",
  "remote": "origin",
  "branch": "<MAIN_BRANCH>",
  "message": "同 raw_message"
}
```

> 示例的 `branch` 用**占位符**而非真值 —— 写 `"main"` 会与 B 侧的 SC 对撞。
> ⚠️ **已知**: `gate_error` 全仓**零消费者** (实测 `grep -rn 'gate_error' aria/` = 0),
> `workflow-runner` 的 verdict 路由只有四条臂、**无异常臂**。
> ⇒ 本 Spec **不依赖**它发红; 发红完全由 `verdict="fail"` + `raw_message` 承担。

**在场范围**: `SKILL.md:279` 逐字是**四类早退** (`enabled:false` / no-backend / precheck 失败 /
backend query 失败) 保持**六键不变**; `gate_error` **只在本 Spec 新增的核验失败路径在场**。

⇒ 落地后该注记须新增**第五类早退** (本 Spec 的核验失败): 它是 **六键 + `gate_error`**、**无 `path_coverage`**
(核验在 path coverage **之前**判 fail, 评估器根本没跑)。这一条与 `_build_output` 的实产键集的一致性
由 `SC-A-doc` 机械钉住。

### 5. 异常与重试: 按**轴**分派两个既有先例, ⛔ 不得再造

| 轴 | 先例 | 实测状况 |
|---|---|---|
| **异常枚举** | `path_coverage.py:93` 的 `(TimeoutExpired, FileNotFoundError, OSError)` 三合一 | ✅ 可复用的是**这条 except 元组的枚举**, **不是** `_run_git()` 函数本身 (它把异常与非零退出码折成同一 `ok=False`, 使 SC-A7/A8 无从分辨)。🔴 **R1: 这条元组本身不够** —— 实跑 `issubclass(UnicodeDecodeError, OSError)` = **False** ⇒ 逐字照抄该元组 + `text=True` 的实现会让 `UnicodeDecodeError` **裸抛穿过 `gate_check()`**。⚠️ 本 Spec **不规定怎么补** (扩 except / 换 bytes+`surrogateescape` 均可, 属 Phase B), 只由 **SC-A14 的参数化探针**钉住「§2 的 catch-all 必须真的 catch-all」 |
| **重试** | `aether.py:38` 的 `RETRY_BACKOFF=(5,15,45)` / `MAX_RETRY_ATTEMPTS=3` | ✅ **正是 `SKILL.md:259` 逐字规定的那套**; ⚠️ 但 `_run_with_retry(:164-187)` 硬绑 `[self.binary]`、**只捕 `TimeoutExpired`** (docstring 自陈「other exceptions bubble up」)、无 `cwd` 参数、`text=True` 严格解码 (对 git 输出会抛 `UnicodeDecodeError`, 见 `path_coverage.py:81-84` 的 #124 教训) |

⇒ **复用 = 复用「枚举」与「常量值」, 不复用函数体。**

🔒 **钉死 (R1; 上一版把 `aether.py` 写成"条件性入 scope", 使 `:6` 的「无架构变更」悬在一个未决 spike 上)**:
**A 不动 `ci_backends/aether.py`** —— gate 层**自建私有 runner** (形状可复制 `path_coverage.py:78-102`:
`cwd` 形参 + **bytes + `surrogateescape` 解码** + 三合一 except。⚠️ 那两件是**配套的** ——
只抄 except 元组而用 `text=True` 就会撞上上表的 `UnicodeDecodeError`), **只引用** `aether.py:38` 的常量值
(`RETRY_BACKOFF=(5,15,45)` / `MAX_RETRY_ATTEMPTS=3`; `pre_merge_gate.py:251` 已有从
`ci_backends.aether` import 常量的先例)。

- **机械判据**: 落地分支 `git diff --stat` **不得出现** `ci_backends/aether.py` —— 出现即违反本节。
- **为什么不在 A 里抽取共享 helper**: 它是**跨 backend 抽象层的结构改动**, 且**零既有测试保护** ——
  实跑 `grep -c '_run_with_retry' tests/test_ci_backends.py` = **0** (全 `tests/` 目录亦 0), 那 25 条
  **系统性绕过它** ⇒ 「25 tests 全绿」作为行为等价判据**恒绿**。A 既给不出可用的等价判据, 就不动它。
- 抽取共享重试 helper 本身**留 follow-up** (与 `fetch_gate.py` / `worktree_manager.py` 同形位置一并处理)。

### 6. 测试隔离接缝

`test_sc22_no_real_git_subprocess_in_suite` (`:710`) 的 patch **本就全局生效**
(`import subprocess` 使模块对象共享 —— 主 loop 实读 `:718` `mock.patch.object(pc_module.subprocess, "run", ...)` 确认)。
⇒ 本 Spec 新增 gate 层 subprocess 后该守卫会**转红**。

⚠️ **受影响面比上一版写的大得多** (R1 实测, 上一版只点了 `test_sc22` 一处):
实跑 `grep -c 'gate\.gate_check(.*main_branch' tests/test_pre_merge_gate.py` = **0**, 六处多行调用
(`:311`/`:321`/`:394`/`:524`/`:654`/`:675`) 亦逐个实读确认未传 ⇒ **24/24 既有调用全部不传 `main_branch`**,
全部落到默认值 `"main"`; 而本仓 origin **无 `main`** ⇒ 落地后**这 24 处全部触达新核验**
(未打桩时还会各自 spawn 一次真实 `ls-remote` 子进程)。

⇒ **接缝形状已有先例, 不需要新发明**: `_ProbeCacheResetMixin` (`tests/test_pre_merge_gate.py:59-80`)
就是 v1.65.0 为**同一个问题**建的 —— 其 docstring 逐字「既有测试不因 `path_coverage_enabled` 默认 true
触发真实 git 子进程 (SC-22)」, 做法是在 `setUp` 里统一 `mock.patch.object(gate, "evaluate_path_coverage", ...)`。
本 Spec 沿用同一形状 (mixin 统一打桩**新核验的模块级入口**), **不逐条改 24 个调用点**。

须建**独立打桩接缝**, 使 `test_sc22` 守卫**保持有效而非被放宽**; 同时保证
SC-A6 / SC-A13 / SC-A-zero / SC-A-cwd / SC-A-cli 能绕过该 mixin 用真实 git 受控裸仓。
**粒度 (函数级 vs subprocess 级) 由 Phase B spike 定** —— 但「mixin 统一打桩 + 需要真 git 的 SC 显式退出打桩」
这个**分层**是本 Spec 规定的, 不是 spike 的自由度。

---

## Success Criteria

> SC 编号用 **`SC-A*`** 前缀 —— 与 B 侧的 `SC-M*` 及既有 `test_path_coverage.py` / `test_pre_merge_gate.py`
> 的 SC 号段**全部不冲突** (B 侧曾因编号冲突被 post_planning 判 Critical, 此处预防)。
> **计数法 = 下表行数**: **16 条** = 上一版 12 + R1 新增 4 (`SC-A-order` / `SC-A-cli` / `SC-A-cwd` / `SC-A-doc`)。

| SC | 断言 | 期望 | 今日实测 | 怎么会红 |
|----|------|------|------|---------|
| **SC-A6** | 受控裸仓: 远端只有 `refs/heads/wip/master`, 传 `--main-branch master` | `verdict=fail` + `kind=="main-branch-not-found"` + **`raw_message` 含分支名与 remote 名** | 今日无核验 ⇒ green | 必红。**承重断言**。**用真实 `ls-remote`, 不打桩** |
| **SC-A13** | 受控裸仓: 远端只有 `refs/heads/master`, 传 `--main-branch 'mast*'` (及 `m[a]ster` / `maste?`) | `verdict=fail` + `kind=="main-branch-not-found"` | 三 pattern 实测对该远端**全返 RC=0 且命中** | **锚定 pattern 实现必红** —— 本条钉住「精确比对」而非「锚定」 |
| **SC-A-zero** | 受控裸仓: 远端只有 `refs/heads/master`, 传 `--main-branch develop` (**零命中**) | `verdict=fail` + `kind=="main-branch-not-found"` | `rc=0` + **零行输出** | **读退出码的实现必红** (它会把 rc=0 当成功) |
| **SC-A7** | `ls-remote` 返 **128** (指向不存在路径的 remote, 或 mock) | `fail` + `kind=="main-branch-verify-failed"` + **`raw_message` 含分支名与 remote 名**, **未重试** | `git ls-remote --heads /tmp/does-not-exist-repo-xyz master` ⇒ **确定性 rc=128** (R1 复跑) | 当「不存在」→ 误报 / 当「存在」→ 恒绿, 两向都红; `raw_message` 写空串亦红 |
| **SC-A8** | `ls-remote` 抛 `TimeoutExpired` (**mock**; 须 mock `time.sleep`) | 3 attempts 后 `fail` + `kind=="main-branch-verify-failed"` + **`raw_message` 含分支名与 remote 名** | — | 未按 `:259` 重试的实现红; 未 mock sleep 致 >60s 亦红; `raw_message` 写空串亦红 |
| **SC-A10** | 负控: `enabled=false` 早退 | 六键不变、无 `gate_error`, **且 `assert ls-remote 未被调用`** | — | 缺后半条因果断言则健康与不健康实现都绿 |
| **SC-A10b** | 负控: no-backend (`:338`) 早退 | 同上, **各带 `assert ls-remote 未被调用`** | — | 兄弟早退不同步则该类只修了一个实例 |
| **SC-A10c** | 负控: precheck 失败 (`:345`) 早退 | 同上 | — | 同上 |
| **SC-A11** | 负控: **受控裸仓中分支确实存在** + mock backend 提供 in-flight runs | `verdict=wait` 不变 | — | 核验不得改变正常路径判决 (恒判 `not-found` 的实现红)。⚠️ 本条**不得打桩核验入口** —— 打了就退化为恒真, 见打桩边界表 |
| **SC-A14** | catch-all **参数化探针**: 逐个喂 `FileNotFoundError` / `OSError` / 输出不可解析 / **`UnicodeDecodeError`** / **任取一个不在实现 `except` 元组里的异常类** | 一律 `fail` + `kind=="main-branch-verify-failed"` + **`raw_message` 含分支名与 remote 名** | `issubclass(UnicodeDecodeError, OSError)` = **False** (R1 实跑) | **照 §5 两轴逐字照做 + `text=True` 的实现必红** —— `UnicodeDecodeError` 裸抛穿过 `gate_check()`。上一版只喂三个**已枚举**输入 ⇒ 抓不到它自己声称要抓的那类实现 (空真) |
| **SC-A-order** | 存在性核验判 `fail` 时 **`assert evaluate_path_coverage 未被调用`** | 未被调用 | — | **把核验插在 `:358` 之后的实现必红** —— 这是 §3「唯一合法插入点」的**唯一**机械锚 (上一版 12 条 SC 无一钉住它, 违规实现 12/12 全绿) |
| **SC-A-cli** | 走 **`main(argv=[...])`** 真实 CLI 入口: 受控工作仓 W (其 `origin` → 受控裸仓 R, R **有** `refs/heads/master`), 进程 cwd = W, 传 `--main-branch master --remote <指向不存在路径>` | `verdict=fail` + `kind=="main-branch-verify-failed"` | `grep -n "main(argv" tests/` = **零命中** ⇒ CLI 入口今日**零测试覆盖** | **只加 `add_argument("--remote")` 而漏 `:435` 的 `remote=args.remote` 的实现必红** —— 漏接线时查的是 W 的 `origin`(=R, 有 `master`) ⇒ 不 fail ≠ 期望。⚠️ fixture 必须自带受控 `origin`, **不得依赖 ambient origin** (否则漏接线实现会因无网络也返 128 而**意外全绿**) |
| **SC-A-cwd** | 同一实现、同一参数 (`main_branch="master"`, `remote="origin"`), 分别以进程 cwd = W₁ (`origin` → 裸仓 R₁, **无** `master`) 与 cwd = W₂ (`origin` → 裸仓 R₂, **有** `master`) 各跑一次 | W₁ ⇒ `fail`+`not-found`; W₂ ⇒ **不因核验 fail** | 实测 `origin` 在主仓解析到 `Aria.git`、在 `aria` 子模块解析到 `aria-plugin.git`, **两边都有 `master`** | **任何不从进程 cwd 解析仓根的实现必红** (常量路径 / `__file__` / 脚本目录 ⇒ 两次得**同一**判决)。⚠️ **诚实限制**: 本条**不能**区分「继承 ambient cwd」与「显式传 `cwd=`」—— 两者都过。那条要求由 §3 正面规定承担, **无机械锚**, 不为它编造断言 |
| **SC-A-doc** | doc↔code 一致性: 从 `SKILL.md` §C.2.4 Output schema json 块**实际解析**出的键名集合 (⛔ 不得硬编码 doc 侧) == `_build_output` 的实产键全集 (六固定键 ∪ `path_coverage` ∪ `gate_error`) | 相等 | 今日 doc 侧 7 键 / code 侧 7 键 | **只落 `.py` 而漏 `SKILL.md` schema 键 (或反之) 的实现必红**; 单独回退 `SKILL.md` 那个 hunk 亦必红。⚠️ **本条不是 Rule #6 substitute** (见 §Rule #6), 它只防 doc 漂移 |
| **SC-A-sc22** | 既有 `test_sc22` (`:710`) 落地后**仍 PASS 且仍能拦住真实 git 子进程** | 用一个**故意违规的桩**验证它会红 | 今日 PASS | 被放宽 (而非建接缝) 的实现红 |
| **SC-A-baseline** | `phase-c-integrator` 全量套件 | **111 + 新增 ≥ 全绿** | **111 passed** (2026-08-11 实跑) | 任何回归红 |

**打桩边界 (逐条覆盖 —— 上一版只覆盖 5/12 条, 且 SC-A7 那条理据已被实测证伪)**:

| 档位 | SC |
|---|---|
| **真实 `ls-remote` + 受控裸仓** (⛔ 不得打桩) | SC-A6 · SC-A13 · SC-A-zero · **SC-A-cwd** · **SC-A-cli** · **SC-A11** (⚠️ R1: 若把核验入口打桩, 本条就不再验"核验放行了一个真实存在的分支", 退化为恒真 —— 须用**分支确实存在**的受控裸仓 + mock backend 提供 in-flight runs) |
| **两种手段皆可** | **SC-A7** —— ⚠️ R1 更正: 上一版逐字「必须 mock (真实 `ls-remote` 无法产出确定性 128)」, 该理据**实测为假** (`git ls-remote --heads /tmp/does-not-exist-repo-xyz master` ⇒ **确定性 rc=128**); 且 B 侧 `:358-361` 早在 post_planning R3 就把同一句更正过, A 承接时把更正丢了 |
| **必须 mock** (真实环境结构上造不出) | SC-A8 (`TimeoutExpired` + mock `time.sleep`) · SC-A14 (`FileNotFoundError` = git 二进制缺失 / `UnicodeDecodeError` / 任取异常类) |
| **走 §6 的 mixin 打桩接缝** (断言"未被调用", 需可观测的打桩点) | SC-A10 · SC-A10b · SC-A10c · **SC-A-order** |
| **纯文件读取, 不涉 subprocess** | **SC-A-doc** |
| **元断言 / 全量跑** | SC-A-sc22 · SC-A-baseline |

---

## Rule #6

`rule6_note`: **第二行 —— 照跑 AB, 零裁量。本 Spec 不申请任何豁免。**

> 🔴 **这是 R1 改判** (上一版判第一行 + 提名 SC-A6/A13/A-zero 作 substitute)。改判的三条依据:

**(a) 本 change 确实改 `SKILL.md` 的指令流程。** SOT
[`skill-benchmark-exemption.md:33`](../../../standards/conventions/skill-benchmark-exemption.md) 逐字
「`description` 或**指令流程变动 ⇒ 一律第二行**」。A 往 `gate_check()` 中间插新步, 而**同形先例
v1.65.0 落地时同批给 `SKILL.md` §C.2.4 执行流程补了编号步骤 2.5** (实读 `SKILL.md:242` 命中)。
⇒ **这件与执行流程的同步必须在 A 内解决, 不能推给 B** (否则文档流程与 helper 流程当场分叉, 违反规则 #3)。
本 Spec 因此**明确要求**新增对应编号步骤 (见 §Impact 的 `SKILL.md` 行) ⇒ **指令流程变动**成立。

**(b) 即便撇开 (a)、只看 §Impact 的 ② ③ 两处"描述性" hunk, 也进不了第一行。** SOT `:33` 是**「仅当…才可能」的必要条件**:
「仅当变动是**事实性同步** (溯源注释 / 行号勘正 / 术语修正) 且 frontmatter `description` 零变动」。
A 的两处 hunk 是**为本 change 新产生的行为写新文档** (schema 新增一个此前不存在的键 / 归纳句从四类扩到五类),
**不属那三项穷举中的任何一项**。落到 SOT `:31` 第四行逐字「**拿不准 ⇒ 照跑 (宁跑勿豁)**」。

**(c) 上一版提名的 substitute 对它声称替代的对象恒绿。** SOT `:28` 第一行的处置逐字要求 substitute 是
「SC 级 **baseline-failing** 单元/集成测试」。SC-A6 / A13 / A-zero 断言的**全是 `gate_check()` 返回的 dict**
(`verdict` / `gate_error.kind` / `raw_message`), **无一条读 `SKILL.md` 一个字节** ⇒
在落地分支上单独 `git checkout HEAD -- .../SKILL.md` 回退 `SKILL.md` 侧**全部** hunk、保留全部 `.py` 与测试,
`pytest -k "sc_a6 or sc_a13 or sc_a_zero"` **三条仍全绿** ⇒ 不满足 baseline-failing 的定义性要求。
> ⚠️ 新增的 **`SC-A-doc` 确实对那个 schema hunk baseline-failing**, 但**本 Spec 不拿它当 substitute** ——
> 因为 (a) 已使定档落到第二行, substitute 通道**结构上不再适用**。SC-A-doc 只作防 doc 漂移用。

**(d) 三处互斥已消除。** 上一版 `:196` 主张第一行 (= 申请豁免) × `:201` 逐字「不申请任何豁免」×
`:39` 把「Rule #6 AB」整体划归 B 侧 —— 三者不可能同时为真。现在: 定档第二行 ⇒ 不申请豁免 ⇒ 一致;
且 §Why 的 ⛔ 清单已更正为「**B 侧自己的** Rule #6 AB」—— **Rule #6 的触发点是本 change 自己的发版**
(CLAUDE.md 逐字「Skill 变更发版前须过 Rule #6 benchmark」), A 按 MINOR 独立发版,
**AB 义务结构上无法转移**给一个至今「不具备进 Phase B 条件」的姊妹 Spec。

> **A.2 仍须逐行点名** `SKILL.md` 的每处变动 (SOT `:33` 的留痕要求对第二行同样有用),
> 但**不再以此换取豁免**。AB 形态照 v1.65.0 先例 (CHANGELOG 逐字「Rule #6 照跑 AB
> (3 eval × with/old/without 三臂)」), 具体 eval 选取属 A.2/Phase B。

---

## 非目标

- **不改** `--main-branch` 的缺省 (B 侧 D5);
- **不改** `SKILL.md` 两处散文流程的**既有** 4 行裸命令 (`:167` `:168` `:243` `:244`) / 不建折叠块 (B 侧 D1)。
  ⚠️ **但 A 必须新增执行流程编号步骤** (v1.65.0 步骤 2.5 先例) —— 二者不矛盾: 新增一步 ≠ 收敛既有两处。
  由此产生的「新步骤用 `<MAIN_BRANCH>` 而步骤 3 硬编码 `main`」这条不一致, 按 §残余暴露在**该步骤处逐字标注**;
- **不动** `ci_backends/aether.py` (§5 已钉死; 机械判据 = `git diff --stat` 不得出现该文件);
- **不引入** `main_branch` 自动解析 —— 实测 `ls-remote --symref` 存在 RC=0 但无 `ref:` 行两态 (unborn / detached), 需独立设计;
- **不改** `path_coverage.py` 代码与行为;
- **不改** `aether` CLI 返回语义;
- **不改** `workflow-runner` 的 `gate_state` schema;
- **不动** `no_ci_fallback` / stub backend 既有降级语义 —— 由 **SC-A10 / A10b / A10c 三条**机械钉住;
- **不修**同形兄弟位置 —— `phase-d-closer/fetch_gate.py` 的字面 `("master","main")` 回落 ·
  `state-scanner/lib/worktree_manager.py:170` 的 `base_branch: str = "master"`。
  ⚠️ **Phase B 实施者不得照抄 `fetch_gate.py`**。开 follow-up。

---

## Impact

| 文件 | 变更 |
|------|------|
| `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py` | `--remote` / `remote` 参数 (**含 `main()` `:435` 处的 `remote=args.remote` 接线** — 唯一落地点) · `_verify_branch_exists()` (自建私有 runner, 显式 `cwd=`) · `raw_message` 诊断 + `gate_error` additive 键 · 核验点插入 |
| `aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py` | `SC-A*` 新增用例 · **扩 `_ProbeCacheResetMixin` (`:59-80`) 统一打桩新核验入口** (v1.65.0 同款接缝, 覆盖 24/24 既有调用) · 需真 git 的 SC 显式退出打桩 |
| `aria/skills/phase-c-integrator/SKILL.md` | **三处** (R1 更正 —— 上一版写「仅描述性 2 处」且 `:267` 行锚偏): ① **§C.2.4 执行流程新增编号步骤** (位于步骤 **2** 与 **2.5** 之间, 号建议 `2.2`; **号本身非承重, 承重的是它落在 2 与 2.5 之间**) + **在该步骤处逐字标注**它与步骤 3 硬编码 `main` 的不一致并指向 B 侧 D1 ⇒ **指令流程变动 ⇒ Rule #6 第二行**; ② Output schema json 块 (`:265-277`, 新键紧邻 `path_coverage` `:275`) 增 `gate_error`; ③ `:279` 归纳句由**四类早退**扩为**五类** (第五类 = 本 Spec 核验失败: 六键 + `gate_error`, **无** `path_coverage`) |
| `aria/skills/phase-c-integrator/scripts/ci_backends/aether.py` | ⛔ **不入 scope** (§5 钉死; 只引用其 `:38` 常量值)。抽取共享重试 helper **留 follow-up** |
| 外部 | **无外部动作** —— 不改 #137 body, 不发评论。留痕与否由 owner 决定。⚠️ **不得据 A ship 关闭 #137** (§残余暴露) |
| 发版同步面 | **MINOR 独立发版 ⇒ CLAUDE.md 整张清单照常适用**: `aria` 子模块 5 文件 (`plugin.json` SOT + `marketplace.json` + `VERSION` + `CHANGELOG.md` + `README.md`) + **主仓 gitlink** + 主仓 `VERSION` + root README badge + i18n README (**仅正文实质变更才重译**, #140 B 档) + **Rule #6 AB**。⚠️ **Level 2 无 `tasks.md` 承载此清单** —— 见下方风险声明。不触发 v2.0 弃用删除面 |

> ⚠️ **发版清单的机械承载缺口 (R1, 如实标注)**: Level 2 = proposal only ⇒ 上面这张清单**没有 checkbox 承载**,
> 而 custom check `m6-version-badge-match` 比的是 badge ↔ `plugin.json`, **对「主仓 gitlink 未 bump」这个方向
> 结构上失明** (post_planning R3 已实证)。姊妹 Spec B 的 R4 三条 Critical 之一正是 `TASK-017` 漏 gitlink。
> ⇒ **本 Spec 不假装它有机械兜底**。两条出路 (**须 owner 裁量, A 不自行决定**):
> **(i)** 接受"清单只在本节留痕", 由 phase-c-integrator §C.2.5 的既有自动化 + 双推 `ls-remote` 核验兜住 gitlink 那条腿;
> **(ii)** 把 Level 提到 **3** 并出 `tasks.md` 承载该清单。
> ⛔ **不得**以「Level 低 / 变更小」自行降级 (规则 #10)。

### 版本

**MINOR。** 全部为 additive: 新增**带默认值**的可选参数 · 新增核验步 (插在既有早退之后, 既有分支语义零改动) ·
新增 **additive 可选**输出键。

**调用点口径 (R1 更正 —— 上一版逐字「既有 24 处 `gate_check(` 调用零改动」漏计第 25 处)**:
三项并列 (memory `critique-repeats-error`) —— **总体** = `aria/` 内可执行的 `gate_check(` 调用点;
**范围** = 基线 `af87cae`; **计数法** = `grep`。
实跑 `grep -c 'gate\.gate_check(' tests/test_pre_merge_gate.py` = **24** (那是"测试内"这个**更小的总体**);
`grep -rn 'gate_check(' aria/ --include=*.py` 另得 `pre_merge_gate.py:298` (def, **非调用**) 与
**`:435`** (`main()` 内真实调用) ⇒ **真实调用点 = 25**。

- **加带默认值的 kwarg 对 25 处全部零破坏** ⇒ MINOR 结论**不受影响**;
- 但 **`:435` 恰是 `--remote` 唯一必须改的那一行** —— 写「24 处零改动」会把它排除在读者视野外,
  而漏改它 ⇒ `--remote` 静默 no-op。由 **`SC-A-cli`** 钉住。

⇒ **不触发** `pre_merge_gate.py:68/:116` 的「removed in v2.0」弃用到期承诺 (那是 B 侧的题目)。

### 行为兼容面 (R1 新增 —— 上一版逐字「零破坏面」**只覆盖了 API 形状, 未覆盖运行时翻转**)

**翻转的确切条件**: 调用方**未显式传 `main_branch`** (落到默认 `"main"`) **且** 目标仓的 `<remote>` 上
**没有 `main`** ⇒ verdict 从 `green` **翻为 `fail`**。

**实测在场**: 本仓 `git ls-remote --heads origin main` = **零行 + RC=0**;
`tests/test_pre_merge_gate.py` **24/24** 既有调用**全部**未传 `main_branch` (§6 已逐个实读);
CLI 侧 `pre_merge_gate.py:427` 的 `--main-branch` 默认值亦是 `"main"`。

**定性**: 这个翻转**正是本 Spec 要修的那个假绿**, 不是回归 —— 但它是**运行时行为翻转**, 必须写明而非藏在
「零破坏面」四个字后面。

**迁移说明**: 调用方须**显式传真值** (本项目 `master`)。这条要求**已有成文先例, 不是新发明** ——
`SKILL.md` 步骤 2.5 的执行上下文契约逐字:「`main_branch` 显式传真值 (本项目 `master`), 不依赖 CLI default」。
⇒ Phase B 落地时, 既有 24 处调用**要么**经 §6 的 mixin 打桩隔离, **要么**显式传真值; **不得**靠放宽核验来保绿。

> ⚠️ **版本定档留给 owner 复议的点**: 「一个此前恒 `green` 的闸门开始 `fail`」是否够得上 CLAUDE.md 的
> 「破坏性变更须 MAJOR」? 本 Spec 判 **MINOR**, 理由: 输出 schema 与函数签名向后兼容 (API 形状不变),
> 翻转的是**被修复的缺陷本身**, 且 CLAUDE.md 版本规则把 MAJOR 系于**破坏性契约变更**而非行为修正。
> **该判断是 AI 作出的, 按规则 #10 留痕请复议** —— 若 owner 认为运行时翻转足以拉 MAJOR,
> A 就与 B 的 MAJOR 面重叠, 拆分收益会显著缩水, 须重议划界。

### 测试基线

`phase-c-integrator` 现 **111 tests** (`test_pre_merge_gate.py` 46 + `test_ci_backends.py` 25 +
`test_path_coverage.py` 40) —— **2026-08-11 主 loop 实跑 `111 passed` 确认, 红窗前提成立。**

---

## 承自八轮审计的输入 (逐条注明来源, 供 post_spec 复核)

| 事实 | 来源 | 已实测? |
|---|---|---|
| 插入点 **5 个逻辑锚位 / 8 个行号** (`:328`/`:338`/`:344`/`:345`/`:356`/`:357`/`:358`/`:366`) | 原 §6 | ✅ 主 loop 逐行实读命中 (8/8) |
| `SKILL.md:255` = `fail` 的 surface 通道是 `raw_message` | 原 §7 | ✅ 逐字实读 |
| `SKILL.md:279` = **四类**早退保持六键 | 原 §7 | ✅ 逐字实读 |
| `SKILL.md:259`/`:260` 重试规范与退出码映射 (含 `127 → no_ci_fallback`) | 原 §5 | ✅ 逐字实读 |
| 锚定 pattern 仍 fail-OPEN | 原 §5 (两次实验) + 主 loop 第三次受控裸仓 | ✅ |
| **`ls-remote` 零命中亦返 rc=0** | **主 loop 2026-08-11 新发现** | ✅ 受控裸仓 |
| **`--exit-code` 无命中返 rc=2** | **主 loop 2026-08-11 新发现** | ✅ 受控裸仓 |
| `test_sc22` patch 全局生效 + `:723` 未传 `main_branch` | 原 §测试隔离 | ✅ 实读 |
| `gate_error` 全仓零消费者 / workflow-runner 仅四条臂 | post_planning R1 对抗复核 | ✅ 实跑 |
| `_run_with_retry` 硬绑 binary / 只捕 TimeoutExpired / 无 cwd / `text=True` | post_planning R2/R3 | ✅ 实读 |
| `test_ci_backends.py` 25 tests **零命中** `_run_with_retry` ⇒ 该判据恒绿 | post_planning R2 | ✅ 实跑 |
| 测试基线 111 passed | 主 loop | ✅ 实跑 |
| **`SKILL.md:243` 硬编码 `--branch main` 且是执行流程编号步骤本体** | **post_spec R1 四席** | ✅ 逐字实读 + R1-fix 复跑 |
| **本仓 `ls-remote --heads origin main` = 零行 + RC=0** | **post_spec R1 四席** | ✅ R1-fix 复跑 |
| **`workflow-runner` 全文零命中 `pre_merge_gate.py`** | **post_spec R1 tech-lead** | ✅ 实跑 |
| **v1.65.0 同形先例: 照跑 AB + 同批补 `SKILL.md` 编号步骤 2.5** | **post_spec R1 tech-lead** | ✅ CHANGELOG + `SKILL.md:242` 逐字 |
| **`issubclass(UnicodeDecodeError, OSError)` = False** | **post_spec R1 code-reviewer** | ✅ R1-fix 复跑 |
| **`ls-remote` 指向不存在路径 ⇒ 确定性 rc=128 (非 mock 亦可复现)** | **post_spec R1 qa-engineer** | ✅ R1-fix 复跑 |
| **24/24 既有 `gate_check(` 调用全部不传 `main_branch`** | **R1-fix 执笔方新测** | ✅ 实跑 + 六处多行调用逐个实读 |
| **`_ProbeCacheResetMixin:59-80` = v1.65.0 同问题的既有接缝** | **R1-fix 执笔方新测** | ✅ 实读 |
| **真实调用点 25 (测试 24 + `main():435`)** | **post_spec R1 三席** | ✅ 实跑 |

⚠️ **拆分后的组合是新的** —— 上表每条单独已验, 但**它们在本 Spec 里的组合关系未经审计** ⇒ 须走 post_spec。
