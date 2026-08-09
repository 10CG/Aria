---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-08T21:04:12.627Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R3 — tech-lead 席 (架构与流程镜头)

## 审计结论

本轮按要求只审**当前这份 186 行文件**, 不回核 R1/R2 旧清单。结论: **减法的方向对, 但两处砍得不对**, 且减法自身引入了若干条款间交叉不一致。

一句话概括: **「必填」这个机械兜底, 装在了 AI 按 SKILL.md 走时根本不会经过的那扇门上**; 而 AI 真正会经过的那扇门 (`SKILL.md:243` 的 raw aether 命令), 本 Spec 给的处方仍然是散文 + 占位符 —— 恰是 §Why:29 自己控诉的形态。被砍掉的「分支存在性核验」正是唯一能拦住占位符路径的东西。

以下每条都实读了锚点。所有断言均可用报告内给出的只读命令复跑。

---

## 一、复核 Spec 自留的三条待审点

### (a) 「必填」是否关掉了所有静默路径 —— **代码层面: 是。文档/行为层面: 否**

**代码层面复核通过**, 且比 Spec 自述更严格地核过:

| 复核项 | 实测 | 结论 |
|---|---|---|
| `DEFAULT_CONFIG` 是否含 `main_branch` | `pre_merge_gate.py:53-65` 实读 9 键 (`enabled` / `ci_backends` / `no_ci_fallback` / `wait_timeout_seconds` / `wait_check_intervals` / `primitive_call_timeout_seconds` / `poll_chunk_seconds` / `user_escape_hatch` / `path_coverage_enabled`) | ✅ 无 |
| `_normalize_config` alias 翻译层是否映射出 `main_branch` | `pre_merge_gate.py:69-72` `_OLD_TO_NEW` 只有两条: `primitive_preference→ci_backends`, `no_aether_fallback→no_ci_fallback`; `_translate_value` (`:75-91`) 只改这两个键的值形状 | ✅ 无 |
| 是否有 config 文件注入路径 | `_load_config_from_file` (`:410-421`) 只取 `phase_c_integrator.pre_merge_gate` 子块整体, 之后 `{**DEFAULT_CONFIG, **user_normalized}` (`:326`); `main_branch` 是**函数形参不是 cfg 键**, 即使用户在 config 里写 `main_branch` 也不会被读 | ✅ 关得干净 |
| 仓内 `main_branch` 赋值点 | 全仓 grep: `pre_merge_gate.py:300` (签名缺省) / `:436` (CLI 透传); 另 `:359` `:366` 是**读取**不是赋值。`path_coverage.py:411` 的 `main_branch` 已是必填 | ✅ 只有两条 |
| 仓外调用方 | `aria-orchestrator/` grep `pre_merge_gate|gate_check|main-branch|C.2.4` → **零命中**; `aria/` 内 `.sh/.json/.yaml/.yml` 亦零命中 | ✅ 仓内无第三条路径 |

⇒ Spec 在 :184 的结论「关得干净」**属实**, 我独立复核确认, 且 alias 层无隐患。

**但这个结论回答的不是真正的问题。** 见下方 C1: `main_branch` 参数只存在于 `main()` 与 `gate_check()` 两个入口, 而 `SKILL.md` 全文**从未示范过带参数的 helper 调用** (`grep -n "pre_merge_gate.py" SKILL.md` 只有 `:262` 一处, 是「Helper 实现: <路径>」的说明句, 不是可执行命令)。AI 被指令执行的是 `:167` 与 `:243` 的 **raw aether 命令**。必填参数对那条路径零作用。

### (b) §移出面 四条是否真解耦 —— **三条真解耦, 第二条 (存在性核验) 被本 Spec 自己拉了回来**

| 移出项 | 解耦复核 |
|---|---|
| 自动解析 (`symbolic-ref`/`ls-remote --symref`) | ✅ 真解耦。本 Spec 不引入任何 subprocess, 无残留依赖 |
| **分支存在性核验** | ❌ **未解耦** — 见 C1。§移出面:73 的理由是「它治的是『显式传了错值』, 与本 Spec 治的『缺省是错值』是两个缺陷」, 但 §同步面:59 把 `:243` 的字面 `main` 换成占位符 `<main-branch>` 后, **新造出一个『显式传了错值』的实例** (占位符被逐字粘贴)。两个缺陷不再 disjoint |
| `verdict` 第四态 / `gate_error` | ✅ 真解耦, 且理由**实证成立**: `workflow-runner/SKILL.md:253` 确为 `"status": "waiting \| green \| fail"`, 与 gate verdict `{green,wait,fail}` (`pre_merge_gate.py:47-49`) 确实不同一, 存在翻译层 |
| `main_branch_resolved` 回显 | ✅ 依赖前两项, 移出一致 |
| (a) 腿 `not_applicable` 通路 | ✅ 本 Spec 确不改 `path_coverage.py`; 但 §非目标 措辞有偏差, 见 m4 |

### (c) SC-M4 / SC-M5 两条 grep 的漏检 —— **SC-M5 通过, SC-M4 不通过**

实测 (可复跑):

```
$ grep -c '"main"' aria/skills/phase-c-integrator/scripts/pre_merge_gate.py
2                      # :300 与 :427 —— 不是 Spec 声称的 3
$ grep -c -- '--branch main' aria/skills/phase-c-integrator/SKILL.md ; grep -c '"branch": "main"' ...SKILL.md
2 ; 1                  # 合计 3 ✓ 与 :167/:243/:270 逐一对应
```

SC-M5 的「3」对; **SC-M4 的「3」错** —— 详见 M1。proposal.md:186 把两者并列写成「实测当前命中数分别为 3 / 3」, 其中一半是错的。

---

## 二、Findings

### C1 (Critical) — 「必填」装在 AI 走不到的门上; `:243` 占位符化后, 「复制粘贴命令」这条路径**仍然静默放行**

**锚点**: `proposal.md:59` (§同步面 `:243` 行) · `proposal.md:73` (§移出面存在性核验的解耦理由) · `proposal.md:29` (§Why「唯一现有约束是散文不是兜底」) · `aria/skills/phase-c-integrator/SKILL.md:167` `:243` `:262` · `aria/skills/phase-c-integrator/scripts/ci_backends/aether.py:117-125`

**事实链** (每一环都实读):

1. §Why:29 点名三条会中招的路径: 「人工直调 / 新写的编排 / **复制粘贴命令**」。
2. `SKILL.md` 给 AI 的可执行命令只有两处, 都是 **raw aether**:
   - `:167` `aether ci status --branch main --in-flight --json (查 main 是否有 in-flight)`
   - `:243` 步骤 3 `aether ci status --branch main --in-flight --json` — 标注「**无条件执行**」
   全文**没有**一处示范 `pre_merge_gate.py --pr-branch … --main-branch …`; `:262` 只写了 helper 的文件路径。
3. 本 Spec 对这两处的处方是「换成占位符 `<main-branch>`」(§同步面:59-60)。
4. 若 AI 照 §Rule #6 ① 自己声明的行为模型 (`proposal.md:124`「**AI 会照抄它**」) 照抄占位符, 实跑的是 `aether ci status --branch '<main-branch>' --in-flight --json`。
5. 该分支不存在。§Why:27 已实测「分支不存在」与「分支无 in-flight run」在后端**合流**; 我在代码层独立确认: `aether.py:117-125` `query_branch_in_flight` 只在 `ok` 为假时抛 `AetherQueryError`, 否则 `data.get("runs") or []` → `InFlightStatus(runs=[])`; `pre_merge_gate.py:215-220` 见 `main_in_flight_runs == []` 判 **green**。
6. ⇒ **同一个假绿, 只是从「查 `main`」变成「查 `<main-branch>`」。**

**这就是「砍掉某项后哪条路径重新变成静默放行」的具体答案**: 砍掉「分支存在性核验」后, `:243` 占位符被逐字粘贴这条路径静默放行。存在性核验是这条路径上**唯一**的拦截物 —— 它能把 `runs:[]` 拆成「分支不存在 (error)」与「分支存在且空 (green)」两态。

**同时构成条款间交叉不一致** (本轮被点名要找的那种):

- §移出面:73 断言两个缺陷 disjoint ⇒ 可以分开做;
- §同步面:59 的动作**制造**了对方那个缺陷的新实例;
- ⇒ D4 的解耦前提被 D3 的动作违反。单看 D3 对 (「只改 `:242` 散文等于没改」正确), 单看 D4 对 (存在性核验现有写法确实 fail-OPEN, 见 :73), 合起来漏。

**为什么五席并行审计容易漏**: D3 属「文档同步面」镜头, D4 属「范围裁剪」镜头, 缺陷落在两者接缝。

**最小修法** (不引入新失败面, 与 D2 精神一致, 三选一或组合):

- **(推荐)** 把 `SKILL.md:243` 步骤 3 的命令**换成 helper 调用** `python3 ${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/pre_merge_gate.py --pr-branch <PR_BRANCH> --main-branch <本仓真实主分支>` —— 这样 AI 的文档路径直接落到 argparse 的 `required=True` 上, 「必填」才真正可达; 零新增代码;
- 或: `:243` 保留 raw 命令但同批加一句硬指令「占位符必须替换为实际分支名; 若查询返回 `runs:[]`, 须先确认该分支在 remote 上存在再判 green」;
- 或: 把「分支存在性核验」搬回本 Spec (与 D2「零新增失败面」冲突, 不推荐)。

`introduced_by_r2fix: true` (§同步面 / D3 / D4 均为本版新写) · `cut_too_much: true`

---

### C2 (Critical) — Rule #6 落「第三行」的两条依据均被证伪; 该处置构成对已启用闸门的降级

**锚点**: `proposal.md:90` (D5) · `proposal.md:112-128` (§Rule #6 处置) · `standards/conventions/skill-benchmark-exemption.md:33` `:30` `:37-40` `:55` `:67` · `aria-plugin-benchmarks/ab-results/2026-07-31-v1.65.0-122-rule6/eval-2/with_skill/answer.md:88-92`

**依据 (i) 被 SOT 原文推翻。** SOT `:33` 逐字写:

> **SKILL.md 有变动时的附加约束**(承前): 仅当变动是**事实性同步**(溯源注释 / 行号勘正 / 术语修正)且 frontmatter `description` 零变动, 才可能落进第一行; 须在 spec 里**逐行点名**该变动并声明非指令语义变更。`description` 或**指令流程变动 ⇒ 一律第二行**。

`SKILL.md:243` 是 §C.2.4 **执行流程 步骤 3** 的运行时指令行 (行内自带「**无条件执行, 不因 not_applicable 免除**」), 改的正是 AI 要执行的那条命令 —— 定义上是「指令流程变动」。而第三行的判据 (SOT `:30` / `:67`) 明确是「它治的行为在固定测试集覆盖范围之外 (**典型: authoring 向导 —— 给 spec 作者读的处方, 而套件测的是 skill 运行时行为**)」。`:243` 恰恰**就是** skill 运行时行为面, 是第三行 typical case 的反面。

**依据 (ii) 被本仓自己的 AB 归档结果证伪。** proposal.md:118 断言:

> `ab-suite/phase-c-integrator.json` 的 3 个 eval 覆盖 C.1 / C.2 / C.2.5, **C.2.4 零命中**。

实读 `ab-results/2026-07-31-v1.65.0-122-rule6/eval-2/with_skill/answer.md`:

- `:4` 「依据: phase-c-integrator SKILL.md v1.65.0 (C.1-C.2 编排 + **C.2.4**/C.2.4.5/C.2.5 gate 链)」
- `:88` 「**C.2.4 Pre-Merge Precondition Gate 重跑** (`pre_merge_gate.enabled: true` 默认)」
- `:91` 「**查 main in-flight**: 若 main 正有 CI run … → 同样 wait」

即: `phase-c-integrator.json` 的 eval-2 (prompt 实读 = 「Phase C C.2 merge … Conflict detected … Handle gracefully」) **确实**驱使 AI 产出 C.2.4 in-flight 查询行为, 且产出的正是本 Spec 要改的那条腿。「C.2.4 零命中」是对 prompt 字面的判断, 不是对 AI 行为的测量 —— 而 Rule #6 判据表问的是「**那个行为 AB 套件测不测得到**」。

（另两条依据 —— `phase-c-integrator-pre-merge-gate.json` `type=workflow_skill_subextension` / 7 fixture / **0 prompt 0 双臂**, 以及 `benchmark.md:173` 的 "not feasible in mock environments. Deferred to production dogfood." —— 我实读均**属实**。但它们只证明**那一个** sub-extension 套件测不到, 不能推及 `phase-c-integrator.json` 这个真·prompt 套件。）

**⇒ 正确归类是第二行「处方性 · 运行时指令面 → 照跑 AB, 零裁量」**; 即便认为存疑, Rule #6 判据表第四行「拿不准 → 照跑 (宁跑勿豁)」也指向同一处置。当前把它落第三行 = 用一条被证伪的「测不到」把「照跑」降级为「建 fixture 替代」, 落在 CLAUDE.md 规则 #10 与 memory `no-self-exempt-gates` / `exact-exception-condition` 正中央。注 `proposal.md:90` 标注「owner 重裁」——**owner 的裁定是基于 :116-118 这三条依据作出的, 其中一条经查为假**, 因此这不是「质疑 owner 权限」, 而是「呈给 owner 的事实需要更正后再裁」。

**附带 (可并入本条修复)**: SOT `:55` 要求「**无论走哪一行**, 都要在 spec/tasks 留 `rule6_note` 引用本规范」。`grep -rn "rule6_note" openspec/changes/premerge-gate-mainbranch-failclosed/` → **零命中**。

**修法**: 改为照跑 AB (第二行), §Rule #6 段落改写为「照跑 + 套件缺口另开 issue」, 并补 `rule6_note`。§Rule #6 ② 的定向 fixture 可保留为**加分项**而非替代品 —— 顺带说明: 它现在也不可执行, 见 M6。

`introduced_by_r2fix: true` · `cut_too_much: false`

---

### M1 (Major) — SC-M4「机械 grep, 零裁量, 现状三处命中」不成立; 改后 `:21` 不改它照绿 = 假绿

**锚点**: `proposal.md:105` (SC-M4) · `proposal.md:186` (「实测 3 / 3」) · `pre_merge_gate.py:21`

`:21` 实读 (含 `cat -A` 核过无隐藏字符):

```
    pre_merge_gate.py --pr-branch <branch> [--main-branch main] [--config-file path]
```

**它没有引号。** SC-M4 写的模式是 `` `"main"` 字面量 ``:

- 用 `grep '"main"'` → 命中 **2 行** (`:300` `:427`), 结构上**永远覆盖不到 `:21`**;
- 放宽成无引号 `grep 'main'` → 命中 **20 行**, 含 `:4` 散文 / `:171` `:201` `:215` 等变量名 / `:424` `def main(` / `:443` `__main__` ⇒ 需要人工挑拣, 「零裁量」不成立。

**不存在恰好命中 3 的零裁量 grep。** 后果: 修完 `:300`/`:427` 后 `grep '"main"'` 返 0, SC-M4 判绿, 而 `:21` 的 `[--main-branch main]` 可以原样留下 —— 那行改后是**主动错误信息** (方括号表示可选 + 展示了一个已不存在的缺省), 且它正是 D1「三处同批」里唯一没有运行时兜底的一处。这就是 memory `false-green-dual` / `redfix-change-quantity` 的形状: 断言存在, 但它在目标缺陷上恒绿。

**修法**: SC-M4 拆成两条断言 —— (1) `grep -n '"main"' pre_merge_gate.py` 命中数 == 0 (覆盖 `:300`/`:427`); (2) `grep -n -- '--main-branch main' pre_merge_gate.py` 命中数 == 0 (覆盖 `:21`, 零裁量, 今日命中 1 必红)。并把 `:186` 的「3 / 3」更正为「2+1 / 3」。

`introduced_by_r2fix: true` · `cut_too_much: false`

---

### M2 (Major) — 减法把版本级别的**理由**删了, 却在同一次减法里**放大了破坏面**; PATCH 与 CLAUDE.md「破坏性变更须 MAJOR」正面冲突, §Impact 无下游采用方行

**锚点**: `proposal.md:10` (ship target PATCH) · `proposal.md:91` (D6) · `proposal.md:153` · `proposal.md:155-159` · 被删的旧 D7 (`git diff` 可见)

三件事叠在一起:

1. **旧版有 D7「PATCH 而非 MINOR」并给了理由** (「无行为面扩大 … 且会使某些此前 green 的调用转 error, 那是修复不是回归」)。本次减法把 **D7 整行删除**, PATCH 的**结论保留**、**理由消失**。D6 只管「版本号不预写字面量」(这条我核过, 成立且必要 —— 并发姊妹 Spec `linked-issue-normalization` ship target 是 v1.66.0 MINOR, 抢号确有非单调风险), **不管级别**。
2. **破坏面在同一次减法里变大了**: 旧 §Impact 写「既有用例**逐字不改**」; 新版 `:155` 标题直接是「**既有测试必然要动 (原「逐字不改」的说法已证伪)**」, `:157` 记 24 处 `gate_check(` 全部 `TypeError` + `:159` 1 处断言改写。我实测确认: `grep -c "gate_check(" tests/test_pre_merge_gate.py` = **24**; `test_sc12_default_true_lock` 定义在 `:663`, 断言在 `:668-670` 逐字 `main_branch="main"`。⇒ 支撑旧 D7 的那句「无行为面扩大」已被本版自己推翻, 而结论没跟着重审。
3. **CLAUDE.md §核心概念 协作原则**逐字写「向后兼容 (**破坏性变更须 MAJOR**)」。本改动对 `gate_check()` 是签名破坏, 对 CLI 是既有有效调用失效。更关键: **aria-plugin 是对外分发插件** (CLAUDE.md 尾部「插件: https://github.com/10CG/aria-plugin」; memory `project_kairos_adopter` / `feedback_secret_guard_plugin_upstream_dogfood` 记录了 Kairos / SilkNode 采用)。对**主分支确实叫 `main`** 的下游, 现有缺省是**正确**的, 本改动把他们能跑的调用变成硬失败。§Impact 表 (`:145-153`) 逐行看, **没有下游采用方这一行**。

「Aria 主分支是 master」是**本项目**事实, 修法却落在**共享分发面**上 —— 这是本 Spec 最大的架构口径问题, 而它的论证痕迹恰好被减法删掉了。

**修法**: 恢复一条版本级别决策 (D7′), 显式回答三问: (a) 相对 CLAUDE.md「破坏性变更须 MAJOR」为何可判 PATCH; (b) 下游采用方影响是否已评估 (「已确认无下游依赖」或「接受破坏并写进 CHANGELOG BREAKING 段」二选一); (c) 是否考虑过**两段式** (先 `main_branch: str | None = None` + 缺省时 raise/warn, 下个 MAJOR 再改硬必填) 以兼顾 fail-closed 与兼容。

`introduced_by_r2fix: true` · `cut_too_much: true`

---

### M3 (Major) — §SC 序言「无新增 subprocess、无网络、无打桩策略分歧」与 SC-M1/SC-M2 的 **RED 基线跑法**冲突

**锚点**: `proposal.md:97` (序言) vs `proposal.md:102` (SC-M1) `:103` (SC-M2) · `pre_merge_gate.py:337` `:344` `:366` `:430-436` · `tests/test_pre_merge_gate.py` 24 处 mock

绿的一侧没问题 (改后 argparse/`TypeError` 在函数体前就抛)。**问题在必须实跑的 RED 一侧** —— SOT `standards/conventions/skill-benchmark-exemption.md:40` 明确要求「可证伪性须实证 (把改动回退, 该 fixture 必须转红)」, 所以 RED 跑不能省。

今日代码下:

- **SC-M2** `gate_check(pr_branch="feat/x")` 不传 `main_branch` → 签名有缺省 ⇒ 直接进函数体 → `:337` `resolve_ci_backend` → `AetherBackend.probe()` (`aether.py:69` `shutil.which("aether")`) → `:344` `backend.precheck()` (**subprocess** `aether ci status --help`) → `:366` `query_branch_in_flight("main")` (**真实网络**)。
- **SC-M1** `main(["--pr-branch","feat/x"])` 同上, 且额外读 **CWD 的 `.aria/config.json`** (`:430` argparse default) ⇒ 结果依赖运行目录。

⇒ RED 结果在「机器上有 aether」与「没有」两种环境下**红的原因不同** (前者真打网络, 后者走 `_no_ci_output` 返回 dict)。既有 24 处调用**无一例外**包在 `mock.patch.object(gate, "resolve_ci_backend", …)` 里, 正说明缺这层就不 hermetic。序言那句「无打桩策略分歧」在 SC-M1 上尤其不成立: 要 hermetic 就得造一个带 `ci_backends: []` 的临时 config 文件并传 `--config-file`, 那本身就是一种打桩策略选择。

**修法**: SC-M1/M2 显式规定 RED/GREEN 两跑的隔离手段 (SC-M2: `config={"ci_backends": []}` 或沿用既有 `mock.patch.object`; SC-M1: `--config-file <tmp>` 内含 `ci_backends: []`), 并把序言那句改成「不新增**生产代码**的 subprocess/网络; 测试侧沿用既有 `resolve_ci_backend` 打桩接缝」。

`introduced_by_r2fix: true` · `cut_too_much: false`

---

### M4 (Major, 条款间交叉) — §非目标末条「降级语义结构上不受影响」不成立: 必填检查发生在**所有**早退分支之前

**锚点**: `proposal.md:139` (§非目标末条) vs `proposal.md:46` (What Changes #2) · `pre_merge_gate.py:298-302` `:328-335` `:137-141` `:339`

§非目标:139 逐字写「不动 `no_ci_fallback` / stub backend 既有降级语义 —— 本 Spec **不在 `gate_check` 内新增任何早退前的逻辑**, 该语义结构上不受影响」。

把「函数体内不受影响」当成了「结构上不受影响」。参数绑定检查发生在**函数体之前**, 因而严格早于:

- `:328-335` `if not cfg["enabled"]` 早退 (config 显式关闸门);
- `:137-141` `ci_backends: []` 显式禁用 (AC-4.5 里被称作「用户绕过 CI backend 集成的规范方式」);
- `:339` `_no_ci_output(cfg["no_ci_fallback"])` 降级。

⇒ **「把闸门关掉」不再足以让调用通过**: 一个设了 `enabled: false` 的下游, 今天 `gate_check(pr_branch=…)` 得到干净的 green skip, 改后得 `TypeError`。这不必然是错的设计 (可以论证「无论闸门开关, 调用方都该说清主分支」), 但 §非目标 现在的断言**是错的**, 而 §非目标 正是读者用来判断影响面的地方。

与 C1 合看更有意思: 必填**在闸门关掉时也强制**, 却**在 AI 真正走的 raw 命令路径上完全不强制** —— 强度分布正好反了。

**修法**: §非目标末条改为诚实表述「`enabled:false` / `ci_backends:[]` / `no_ci_fallback` 的**内部语义**不变, 但参数绑定发生在它们之前, 因此这些早退路径的调用方同样须传 `main_branch`」, 并在 §Impact 记一句。

`introduced_by_r2fix: true` · `cut_too_much: false`

---

### M5 (Major) — 审计叙事寄生在交付面文档里, 且已自相矛盾; 与本仓 2026-08-07 owner 已裁定的做法相反

**锚点**: `proposal.md:3-5` (§Status 闸门留痕) · `proposal.md:171-186` (§审计轨迹 + §待 R3 重点审) · `openspec/changes/linked-issue-normalization/proposal.md:8`

1. **本仓已有 owner 裁定的相反做法**: 一天前 (2026-08-07) `linked-issue-normalization/proposal.md:8` 逐字写「**本文件只规定「要建什么」**。「规定是怎么来的」(三轮审计轨迹 / … / 全部订正留痕) 已于 2026-08-07 整体移出至 **审计轨** `.aria/audit-reports/linked-issue-normalization-audit-trail.md`」, 标题栏还写着「**重构**: 2026-08-07 (owner 裁定: 交付面与审计史切开)」。本 Spec 走的是反方向, 且与 memory `audit-trail-not-in-spec` 记录的教训相反 (「append-only 审计叙事与收敛型交付面**不能同居一文**」)。
2. **它已经在自相矛盾**: `:5` 写「实跑 2 轮即停 … **下一道验证是 Phase B 的 SC-M1..M5 实跑, 不是第三个读文档的 agent**」—— 而 R3 正在跑。`:173-176` 的轨迹表无 R3 行, `:182` 的「待 R3 重点审」把待办写在了本该收敛的交付面里。任何读这份 proposal 的下游 (Phase B 实施者 / archive 时的 knowledge-manager) 都会读到一个与事实不符的闸门状态。
3. 这正是 memory `feedback_spec_frontmatter_reflects_reality` 与 `audit-trajectory-placeholder-footgun` 的形状: 提交进 Spec 的过程性状态会立刻腐坏。

**修法**: 把 §Status 的闸门留痕 / §审计轨迹 / §待 R3 重点审 三段整体移到 `.aria/audit-reports/premerge-gate-mainbranch-failclosed-audit-trail.md` (照抄姊妹 Spec 的做法), proposal 顶部只留一行指针 + 一句「本文件不同步审计史」。**切开不重写** —— 内容本身不必改。

`introduced_by_r2fix: true` · `cut_too_much: false`

---

### M6 (Major) — Rule #6 第三行的三件事, ② 按 Spec 写的路径与格式**不可执行**

**锚点**: `proposal.md:125` (§Rule #6 ②) · `aria-plugin-benchmarks/ab-suite/` 目录实况 · `ab-suite/phase-c-integrator.json` 结构

Spec 要求「新建 `ab-suite/fixtures/c24-main-branch-literal.json`」。实测:

- `ls -d aria-plugin-benchmarks/ab-suite/fixtures` → **No such file or directory**; 套件既有约定是 `ab-suite/<skill>.json` (eval 集) + `ab-suite/<skill>-<x>-fixtures/` (fixture 目录), 没有共享 `fixtures/` 层。
- `ab-suite/phase-c-integrator.json` 的 eval 字段实读为 `{id, name, prompt}` —— **没有断言 / grader 字段**。②要求的「断言其产出的命令不含字面 `main`」在该 schema 里无处安放; 真要做, 它得是一条**新 eval + 人工/LLM grading**, 不是一个「fixture」。
- ②的对照实验 (「用改动前的 SKILL.md 跑同一 fixture 必须失败」) 本身可行 —— `ab-results/2026-07-31-v1.65.0-122-rule6/` 里 `skill-snapshot-v1.64.1-SKILL.md` + `skill-candidate-v1.65.0-SKILL.md` 的双臂快照模式就是现成先例。所以**卡点只在路径与 schema**, 不在方法。

⇒ 按 Spec 字面执行会先撞目录不存在、再撞 schema 无断言位。Spec `:128` 自带的兜底 (「② 做不出可证伪结果则回落照跑 AB」) 恰好在这里生效 —— 与 C2 的结论合流: **本来就该照跑**。

**修法**: 若采纳 C2 改为照跑, 本条自然消解, ② 降级为「顺带新增一条 eval 到 `ab-suite/phase-c-integrator.json`」(路径与 schema 都对得上)。若仍坚持第三行, 必须先改正路径 (`ab-suite/phase-c-integrator-c24-fixtures/`) 并说明断言由什么承载。

`introduced_by_r2fix: true` · `cut_too_much: false`

---

### m1 (Minor) — `rule6_note` 缺失

**锚点**: `standards/conventions/skill-benchmark-exemption.md:55` · `grep -rn "rule6_note" openspec/changes/premerge-gate-mainbranch-failclosed/` → 零命中。SOT 要求「无论走哪一行」都要留。Level 2 无 tasks.md ⇒ 应落在 proposal 里 (加一行 frontmatter 式字段或 §Rule #6 段首)。

### m2 (Minor) — 「387 行砍到 186 行」不可核; R1/R2 的被审 artifact 从未进 git

**锚点**: `proposal.md:3` · `proposal.md:180`

`git show HEAD:openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md | wc -l` = **179**; 工作树 = 186; `git diff --stat` = **114 insertions / 107 deletions**, 净 **+7 行**。387 行那一版**从未提交**, 十份席位报告在 `.aria/audit-reports/` 全部 untracked (`.aria/` 本身未被 gitignore, `git check-ignore` rc=1 ⇒ 是没 add 不是被忽略)。

⇒ §审计轨迹 引用的证据链指向 git 里不存在的 artifact 版本; 「大幅减法」这个本轮审计的**框架前提**本身不可核 (memory `cross-doc-claim-verify-at-target` / `scoped-add-splits-claim` 正是这个形状)。不影响技术结论, 但下次 owner 复议时无法重建被审对象。**修法**: 提交 R1/R2 报告与被审快照, 或在 §审计轨迹 注明「被审版本未入 git, 仅存于当时工作树」。

### m3 (Minor) — SC-M5 只覆盖 §同步面 4 行中的 3 行; `:167` 改后仍留同行的 `main` 注解

**锚点**: `proposal.md:106` (SC-M5 只点 `:167`/`:243`/`:270`) vs `proposal.md:62` (§同步面第 4 行 `:242` 散文) · `SKILL.md:167`

- `:242` 的散文改动 (「你必须记得传」→「必填, 不传即报错」) **没有任何断言腿** —— 而 §Why:29 把 `:242` 称作「唯一现有约束」, 它最该被钉住。
- `SKILL.md:167` 实读全行: `aether ci status --branch main --in-flight --json (查 main 是否有 in-flight)` —— 改掉 `--branch main` 后, **同一行**尾部的「(查 main 是否有 in-flight)」仍在, SC-M5 的两个模式都扫不到。与 D3 要根除的字面量同处一行, 属「砍不干净」。

### m4 (Minor) — 缺省移除后的文档陈旧点未列入 §Impact (规则 #3)

**锚点**: `aria/skills/phase-c-integrator/scripts/path_coverage.py:19` (docstring「main_branch 由调用方显式传真值 (**不依赖 "main" 默认**)」—— 缺省移除后该括注指向一个不存在的东西) · `openspec/changes/linked-issue-normalization/detailed-tasks.yaml:77-81` 与 `tasks.md:161` (in-flight 姊妹 Spec, 逐字记录「缺省 'main' 而本项目是 'master' ⇒ 调用时必须显式」作为 workaround 理由, 修复后理由陈旧)。

另: §非目标:134 写「`main_branch` **仍**由调用方显式传入 … (与现状同)」—— 「仍」与「与现状同」不准确, 现状是**有缺省**, 改后才是必须显式。

（已核**排除**: `openspec/changes/phase-c-integrator-ci-path-coverage/` 虽在 `changes/` 下但其 proposal 顶部标 **⛔ SUPERSEDED**, 不构成 in-flight 冲突。）

### m5 (Minor) — §风险 的 blast-radius 核查处方口径不足

**锚点**: `proposal.md:163` — `grep -rn "pre_merge_gate\|gate_check" aria/ --include=*.py --include=*.md`。排除 `.sh/.json/.yaml/.hcl`, 排除 `aria-orchestrator/` (v2.0 Layer 2 跑完整十步循环, 结构上是潜在调用方), 且对外部采用方天然不可见 (与 M2 同源)。

我替它跑了更宽的版本: `aria-orchestrator/` 与 `aria/` 内非 py/md 文件**均零命中** ⇒ **当下答案是对的**。但作为一次 breaking change 的核查处方, 口径应写成 `grep -rn "pre_merge_gate\|gate_check" -I aria/ aria-orchestrator/` (不限扩展名) + 一句「外部采用方无法机械核, 须走 CHANGELOG BREAKING 通告」。

---

## 三、六条决策自洽性小结 (tech-lead 镜头)

| 决策 | 自洽 | 说明 |
|---|---|---|
| D1 三处字面量同批 | ⚠️ | 方向对, 但 `:21` 那一处**没有可执行的验证腿** (M1) |
| D2 必填不解析 | ⚠️ | 「零新增失败面」在**代码**层成立; 但它把兜底放在了 AI 走不到的入口 (C1), 且代价 (breaking) 的记录被删 (M2) |
| D3 `:243`/`:167`/`:270` 同批 | ❌ | 对 `:243` 的诊断精准, 处方不足 —— 占位符化留下同形假绿 (C1) |
| D4 存在性核验移出 | ❌ | 解耦前提被 D3 的动作违反 (C1) |
| D5 Rule #6 第三行 | ❌ | 两条依据均被证伪 (C2) |
| D6 版本号不预写 | ✅ | 成立且必要 —— 姊妹 Spec `linked-issue-normalization` ship target v1.66.0 (MINOR), 抢号确有非单调风险。但它**不覆盖版本级别**, 而级别的理由被删了 (M2) |

**§非目标 与 §移出面 的边界**: 两段职责划分清楚 (§移出面 = 本可以做但另起 Spec; §非目标 = 本 Spec 不碰), 无重叠、无遗漏 —— 唯一问题是 §非目标 末条的断言本身不成立 (M4)。

**与 aria-plugin #136 / #137 / Rule #8 SOT 的关系**: #136 (branch-manager 合并动作) 确与本 Spec 正交, §非目标:136 成立。#137 的订正处理 (§Why:33-35, body 加删除线 + 指向 comment 18015) 是诚实的做法, 且 `path_coverage.py:24` 规则 1「git diff 失败 → unknown → fail-toward-covered」我核过属实 ⇒ 「只有 (b) 腿成立」的订正正确。Rule #8 SOT (`SKILL.md §C.2.4`) 的关系仍成立, 但**本 Spec 修完后 SOT 里那条腿的兜底强度取决于 C1 怎么修** —— 若按推荐修法把 `:243` 换成 helper 调用, Rule #8 的 (b) 腿才第一次有了机械兜底。

---

## Verdict

**FAIL** — 2 Critical + 6 Major + 5 Minor。

两条 Critical 都不是「减法砍掉的东西太多」这种笼统判断, 而是可复现的具体路径:

- **C1**: `:243` 占位符被逐字粘贴 → 分支不存在 → `runs:[]` → green。修法零新增失败面 (把 `:243` 换成 helper 调用即可), 不需要把「存在性核验」搬回来。
- **C2**: Rule #6 归类依据被 SOT 原文 + 本仓 AB 归档结果双向证伪 ⇒ 应回落「照跑 AB」。

值得说明的是: **减法本身是对的**。§Why 的诊断、D1/D2 的代码侧修法、(a) 项「关得干净」的结论、#137 的订正 —— 这些我都独立复核并确认成立。问题集中在**减法的边缘**: 被删的理由 (M2)、被留下但失去验证腿的条款 (M1/m3)、以及一条「移出」与一条「同步」之间的接缝 (C1)。

**建议**: 不再加审计轮次 (memory `stop-adding-rounds` / `marginal-return-negative`)。C1/C2 两条是**定点修**, 改完直接进 Phase B; M1/M3 在写测试时自然吸收; M2/M5 是文档动作; M4/m1-m5 是逐行订正。

## 轮次记录

| 轮 | 席位 | vote | 本席 C/M/m | 备注 |
|---|---|---|---|---|
| R1 | 5 | 5/5 REVISE | — | 审的是自动解析版 (git HEAD `ab4da15`, 179 行) |
| R2 | 5 | 5/5 REVISE | — | 审的是 387 行版 (未提交, 不可核 — 见 m2) |
| **R3** | 本席 tech-lead | **REVISE** | **2 / 6 / 5** | 审当前 186 行减法版; 未回核 R1/R2 旧清单 |

**本轮取向**: 全部 findings 均给 `file:line` / `§章节` 锚点且逐一实读; 关键事实 (grep 命中数 / DEFAULT_CONFIG 键数 / alias 表 / 24 处调用 / eval-2 答卷 / SOT 第 33、55 行 / 姊妹 Spec 的审计轨切分 / HEAD 行数) 均以只读命令实测, 未依赖 Spec 自述。未修改本仓任何文件。

**收敛信号**: 本席 2 Critical 中 **C1 属「砍不干净」** (cut_too_much), **C2 属「归类依据证伪」**; 6 Major 中 M2 属「砍过头」(理由被删而结论保留)。若 R3 其余席位的 major 主要落在 M1/M3/M4 这类**订正型**而非**结构型**, 则本 Spec 已接近可交付, 定点修后不必再加轮。
