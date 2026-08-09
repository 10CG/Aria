---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-08-09T12:52:52.516Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
agents: [code-reviewer]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_planning R1 — code-reviewer

被审对象: `openspec/changes/premerge-gate-mainbranch-failclosed/tasks.md` + `detailed-tasks.yaml` (19 条)
参照物: 同目录 `proposal.md` (post_spec R1–R5 未收敛, owner override 放行, 已知三条实现细节有意降为 spike)
镜头: 断言维度匹配 / 敷衍实现可否过关 / 委派复用目标核实 / 任务间接缝 / 修实例不修类 / 两份文件一致性

## 审计结论

### 先说成立的部分 (实读实跑确认)

- **proposal 的 SC「今日实测」列 5 条 grep 全部复跑一致**: SC-1=4 / SC-2=1 / SC-3=0 / SC-4=1,1,1 / SC-5=1。
- **测试基线 111 实跑复现**: `python3 -m pytest tests/ -q` → `111 passed`; 46+25+40 与 proposal §测试基线 逐字一致。
- **`ls-remote` 三轮受控实验全部复现** (裸仓 `bare1` 只含 `refs/heads/wip/master`): `git ls-remote --heads o master` RC=0 且返回 `wip/master`; 带 `--exit-code` 仍 RC=0。裸仓 `bare2` 只含 `refs/heads/master` 时 `refs/heads/mast*` / `refs/heads/m[a]ster` / `refs/heads/maste?` / `refs/heads/*` **全返 RC=0 且命中** ⇒ SC-13 对「锚定 pattern」实现确实是可证伪的红, 是 R2 承重 Critical 的有效闭合腿。
- **TASK-005 notes 的跨模块 patch 断言经受控实跑证实**: `path_coverage.subprocess is subprocess` → True; 在 `mock.patch.object(pc_module.subprocess,"run",_forbidden)` 作用域内从**另一个**模块调 `subprocess.run` 被拦截。且实测 `hasattr(pre_merge_gate,"subprocess")` → **False** (gate 目前不 import subprocess) ⇒ TASK-008 一落地 `test_sc22` 必转红, 该任务的存在理由成立。
- **TASK-016 的先例经核**: `7661e96` 在**主仓**存在, `git show` 确认同一提交内既 bump aria gitlink 又改写 CLAUDE.md 规则 #8 正文 (L432-444) — 先例与所述粒度一致。
- **TASK-018 / TASK-019 的锚点全部实读命中**: `CLAUDE.md:113` 只写 `pre-merge gate` 不写 `gate_check` (故须含无下划线写法, 实跑该口径 173 命中含 CLAUDE.md 1 条); `fetch_gate.py:55 _DEFAULT_BRANCH_FALLBACKS=("master","main")`; `worktree_manager.py:170 base_branch: str = "master"`; `SKILL.md:189-191` 三条裸 git 命令; `gate_error` 全仓 .py/.md **零命中**, `write_gate_state` (`gate_state_helper.py:115`) 签名确无该形参。
- **TASK-006 是全清单里唯一做对了「grep 断言 + 行为断言」双腿的任务**: SC-4 三条 grep 单独看可被 `default="main"` → `default='main'` 这种改法绕过, 但 SC-9 (`gate_check(pr_branch=...)` 不传 `main_branch` ⇒ TypeError) 是真行为断言, 敷衍实现过不去。**这正是下面 C2 指出 TASK-011 缺的那条腿的模板。**

### 总判断

按 owner 裁定的设计意图 —— 「组 0 是 TDD 前置 (先看到红), 三条实现细节写成 spike」 —— 逐条核验后: **spike 那半成立, TDD 前置那半只落地了 4/13。** 承载真实行为契约的 SC-6..SC-13 八条既无 owning task、无 deliverable、也无红窗要求 (C1); 而全清单最承重的 TASK-011 (D1) 的两条机械断言都不带「位置」这个恰是病灶所在的维度 (C2)。

## Verdict

**FAIL** (2 Critical + 8 Major + 5 Minor)

---

## Critical

### C1 — 组 0 的「先看到红」只覆盖 4/13 条 SC; SC-6~SC-13 无 owning task、无 deliverable、无红窗

**锚点**: `detailed-tasks.yaml` TASK-001 `verification` (:40-44, 只列 SC-1/SC-3/SC-4/SC-5) · TASK-008 `deliverables` (:174-175) · `tasks.md:17`

**实读/实跑**: 对 yaml 做结构分析, 交付 `tests/test_pre_merge_gate.py` 的只有 **TASK-001 / TASK-005 / TASK-010** 三条 —— TASK-001 只写 4 条 grep 断言, TASK-005 写隔离接缝, TASK-010 补 24 处既有调用。TASK-008 的 verification 逐字写「SC-6 / SC-13 / SC-7 / SC-8 全绿」, 但它的 `deliverables` 只有 `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py`, **不含测试文件**。同理 SC-9 挂 TASK-006 (deliverable 只有 `pre_merge_gate.py`)、SC-10/SC-11 挂 TASK-008、SC-12 挂 TASK-002 (deliverable 是「回写 proposal.md §1」)、SC-13 挂 TASK-003 (deliverable 是「回写 proposal.md §5」)。

对照 `proposal.md:282` 逐字「本 change **新增 12**」—— TASK-001 只写 4 条, 余下 8 条无人交付。

**为什么重要**: 这一条直接决定 owner 裁定成不成立。owner 的裁定是「停止改文档, 用 TDD 接管」, 组 0 是该裁定唯一的落地物; 而 TDD 真正要接管的恰恰是编排层五轮验证不了的**行为面** (存在性核验 / 退出码分区 / 重试 / 负控), 也就是 SC-6..SC-13。现状是: grep 面上了 TDD, 行为面退回「实现完了再补测试」。本 Spec 自己在 TASK-001 notes 里逐字写着「五轮里编排层写出过**两次恒红断言与一次恒绿断言**」—— 那正是 test-after 在本仓的稳定失效方式。

**如何修**: 加一条 (或拆两条) 组 0 任务, deliverable = `tests/test_pre_merge_gate.py`, 内容 = SC-6/7/8/9/10/11/13 的空壳 + 每条贴实施前实跑红输出; SC-12 因需四种 cwd 参数化, 单列。TASK-008 的 verification 改为「上述用例由红转绿, 且 diff 显示测试文件在实现之前提交」。

---

### C2 — TASK-011 (D1 承重) 的两条机械断言都不带「位置」维度, 敷衍实现可全过

**锚点**: `detailed-tasks.yaml` TASK-011 `verification` (:233-236) · `proposal.md:198` (SC-3) · `proposal.md:196` (SC-1) · `tasks.md:46`

**实读**: TASK-011 的四条 verification 里只有前两条是机械的 ——
- `SC-1 grep -c 'aether ci status' SKILL.md` 由 4 转 **0**
- `SC-3 grep -c -- '--pr-branch' SKILL.md` 由 0 转 **2**

两条都是**全文件计数**。第三、四条 (「折叠块须补上存在性核验步」「去掉全部可执行命令字面量 …… **须人工核**」) 是散文。

**构造敷衍实现** (镜头 2): 把两条 `pre_merge_gate.py --pr-branch <PR_BRANCH> …` 写进 `<details><summary>helper 内部算法 (供理解与排障, ⛔ 不要手工执行)</summary>` 折叠块里, 而 `### 步骤执行` 与 `### C.2.4` 的规范流程只留自然语言描述。结果: SC-1 = 0 ✅ · SC-3 = 2 ✅ · 折叠块含存在性核验步 ✅ —— **全过**, 而 AI 面向的规范流程里仍然没有一条可执行的 helper 调用。这与本 Spec 要治的病 (`proposal.md:32` 逐字「**AI 走散文那份**」) 逐字同形。

**维度分析** (镜头 1): 病灶的量是「**规范流程段落里有没有 helper 调用**」, 是一个带位置的量; SC-1/SC-3 测的是「**整份文件里某字符串出现几次**」, 无向、无位置。无向断言对位置错误天然免疫 ⇒ 可全绿而病灶原样存在。

**对照证据**: 同一份清单的 TASK-006 用 SC-9 (TypeError) 给同类可绕过的 grep 断言补了行为腿 —— 实测 SC-4 的 `grep -c 'default="main"'` 只要把双引号换单引号就能转 0 而缺省仍在, 是 SC-9 兜住的。**TASK-011 没有等价物, 而它比 TASK-006 承重。**

**如何修**: 把 SC-3 换成带范围的断言, 例: 用 `awk` 取 `### 步骤执行` 与 `### C.2.4` 两段各自的行区间 (且排除 `<details>`…`</details>` 之间), 断言每段区间内 `--pr-branch` 计数 == 1; 再加一条「`<details>` 起始行号 > 该段调用行号」的顺序断言。这样断言的量才落在病灶所在的维度上。

---

## Major

### M1 — `--main-branch` 改必填后, 没有任何断言要求 SKILL.md 新写的两条调用带上它; 且 TASK-011 不依赖 TASK-006

**锚点**: TASK-006 (:133-146) · TASK-011 `dependencies: [TASK-002]` (:229) · `proposal.md:207` (SC-12)

**实读**: TASK-006 把 CLI `--main-branch` 由 `default="main"` 改 `required=True`。TASK-011 往 SKILL.md 写两条调用, 但 SC-3 只数 `--pr-branch`, SC-4 第三条 `grep -c -- '--main-branch main'` 的对象是 **`pre_merge_gate.py`**, 与 SKILL.md 无关。全 19 条里没有一条断言 SKILL.md 的调用含 `--main-branch`。

SC-12 的验收逐字是「四种全部可达并正常执行 (**非 `No such file`**)」—— 它测的量是「文件找不找得到」; 而 D5 造出的新失效是「必填参数缺失」(argparse 退出 2)。两个不同维度, SC-12 对后者恒绿。

**依赖图使之从「假设」变成「大概率」**: TASK-011 的 dependencies 是 `[TASK-002]`, **不含 TASK-006**。即 TASK-011 (agent: tech-lead) 完全可以在 TASK-006 (agent: backend-architect) 之前执行 —— 那时 CLI 里 `--main-branch` 还带缺省, 写调用的人合理地只写 `--pr-branch`。TASK-006 之后无人回头复检。

**后果**: SOT 里躺着一条一执行就 argparse 退出 2 的命令, 而 SKILL.md 的命令正是 AI 照抄的那份。(相对 C2 降一档的理由: 这条是**响的**失败, 不是假绿。)

**修**: TASK-011 dependencies 补 TASK-006; SC-3 的同段区间断言里同时要求 `--main-branch` 出现且取真值 (本项目 `master`)。

---

### M2 — Rule #6 的 AB (TASK-015) 依赖漏了两个同样改 SKILL.md 的任务

**锚点**: TASK-015 `dependencies: [TASK-011, TASK-013]` (:299)

**实跑**: 对 yaml 做 deliverables 反查, 交付 `SKILL.md` 的是 **TASK-011 / TASK-012 / TASK-013 / TASK-014** 四条; TASK-015 的依赖只有其中两条。

TASK-014 要改 `:262 / :559 / :610` 的 helper 定位约定 —— 那是运行时指令面; TASK-012 可能改步骤 6 措辞。按 CLAUDE.md 规则 #6 判据表第二行 (「`description` 或指令流程变动 ⇒ 一律照跑, 零裁量」, 本 Spec 自己在 `proposal.md:220` 引用的同一条款), AB 必须跑在**最终**的 SKILL.md 上。现在的依赖允许 AB 跑完之后 TASK-012/TASK-014 再改 SKILL.md ⇒ 合规义务落在了一个不是交付物的版本上。

**修**: TASK-015 dependencies 改为 `[TASK-011, TASK-012, TASK-013, TASK-014]`。

---

### M3 — TASK-012/013/014 的全部验证锚点是绝对行号, 而 TASK-011 就在它们上游重排这些行

**锚点**: TASK-011 `dependencies` 被 TASK-012 (:249) / TASK-013 (:267) / TASK-014 (:284) 三者共同依赖 · TASK-012 引 ":252-255" · TASK-013 引 ":267 / :270 / :279" · TASK-014 引 ":262 / :559 / :610"

**实读**: TASK-011 要重整 `:99` 段与 `:218` 段、插入 `<details>` 折叠块、删四行裸命令、加两条调用 ⇒ `:218` 之后的行号必然整体位移。而 TASK-012/013/014 的 verification 逐字就是那些位移前的绝对行号。执行时这些锚点已不指向所述内容, 验证要么无法逐字执行, 要么静默指向别的行。

**对照姊妹先例**: `openspec/changes/linked-issue-normalization/detailed-tasks.yaml:33` 在 `scope_repos` 里钉了 `head: "af87cae"` baseline SHA (且 :39 为主仓钉 `head: "2cf2569"`, 并留了「R3-fix 时更新」的注)。**本文件的 `scope_repos` (:6-17) 没有 `head` 字段。**

**修**: metadata.scope_repos 补 `head` (aria 当前 `af87cae`); TASK-012/013/014 的锚点改成内容锚 (如 `grep -n '枚举归层注记'` / `grep -n '路由决策'` / `grep -n 'Helper 实现'`), 或显式写「行号以 `head` SHA 为准, TASK-011 落地后按内容重定位」。

---

### M4 — TASK-002 的 spike 输入有两处与实读/实测相反, 且都指向 spike 必须回答的那个问题

**锚点**: TASK-002 `verification` 第三条 (:63) 与 `notes` (:64-68) · `proposal.md:64` · `proposal.md:70` · layer 主要在 proposal, 但逐字进了 TASK-002/TASK-014

**(a) `CLAUDE_PLUGIN_ROOT` vs `ARIA_PLUGIN_ROOT` 写反了。** `proposal.md:64` 逐字: 「仓内的真实约定是 `${CLAUDE_PLUGIN_ROOT}` (66 处引用, `ARIA_PLUGIN_ROOT` 仅 5 处), `SKILL.md:262` / `:559` / `:610` **均用它**。」

实跑 `grep -n 'PLUGIN_ROOT' skills/phase-c-integrator/SKILL.md` 逐字输出:
```
262:**Helper 实现**: `${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/pre_merge_gate.py` (stdlib + subprocess only)
559:**Helper 实现**: `${ARIA_PLUGIN_ROOT:-aria}/skills/phase-c-integrator/scripts/submodule_gate.sh` (Bash, stdlib + git only)
610:**降级策略**: 检测 `test -f "${ARIA_PLUGIN_ROOT:-aria}/skills/git-remote-helper/SKILL.md"` 存在性 …
737:python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/aria-token-telemetry/scripts/token_telemetry.py" --project-root .
```
三行**全部**是 `ARIA_PLUGIN_ROOT` —— 恰是全仓 5 处 `ARIA_PLUGIN_ROOT` 里的 3 处 (实跑全仓计数: CLAUDE_PLUGIN_ROOT 67 / ARIA_PLUGIN_ROOT 5, 另 2 处在 `aria/CHANGELOG.md:2796` 与 `state-scanner/references/sync-detection.md:587`)。本文件唯一的 `CLAUDE_PLUGIN_ROOT` 在 `:737`, 属 aria-token-telemetry, 与 phase-c-integrator 自己的 helper 无关。

TASK-002 verification 逐字「须核 CLAUDE_PLUGIN_ROOT (仓内 66 处引用) 与 SKILL.md:262/:559/:610 的既有约定是否可直接沿用」—— 把 spike 引向一个该 SKILL.md 从未对自己 helper 用过的变量。

**顺带一个 spike 输入里缺的关键事实**: `${ARIA_PLUGIN_ROOT:-aria}` 的缺省 `aria` 是**相对路径**, 只在主仓根成立; 而 `SKILL.md:242` 契约逐字要求「在执行 C.2 合并的目标仓根内调用 (子模块合并 → **子模块根**)」, 那时它解析为 `<aria-root>/aria/skills/...` 不存在。⇒ **既有约定本身已经不满足 SC-12 四种 cwd 里的三种**, 不是「是否可直接沿用」而是「已知不可沿用」。这个事实没进 spike 输入。另实测本 Bash 上下文 `CLAUDE_PLUGIN_ROOT` 与 `ARIA_PLUGIN_ROOT` **均 unset**, 而 phase-c-integrator 的 helper 正是由 AI 从这类 shell 里发起的。

**(b) 「helper 至少 3 个副本位置」与实测不符, 且漏掉唯一的 fail-OPEN 方向。** `proposal.md:70` 把「主仓 `aria/skills/...`」与「子模块根 `skills/...`」列为两个副本位置 —— 实跑 `find / -name pre_merge_gate.py` 显示仓内只有**一个**物理文件 `/home/dev/Aria/aria/skills/phase-c-integrator/scripts/pre_merge_gate.py`, 那是同一文件的两种相对写法。真实的多副本在**版本化 plugin cache**:
```
marketplaces/10CG-aria-plugin/skills/.../pre_merge_gate.py   identical
cache/10CG-aria-plugin/aria/1.65.5/skills/.../pre_merge_gate.py   identical
cache/10CG-aria-plugin/aria/1.63.0/skills/.../pre_merge_gate.py   DIFFERS (67 lines)
cache/10CG-aria-plugin/aria/1.56.1/skills/.../pre_merge_gate.py   DIFFERS (67 lines)
```
`1.56.1` 那份实测 `grep -c 'path_coverage'` = **0** (整个 #122 特性都没有)。SC-12 只钉「四种 cwd 可达」, **不钉「不得解析到过期副本」** —— 而解析到过期副本是这个维度上唯一会静默产生错行为的方向。

**修**: 更正 `proposal.md:64` / `:70`; TASK-002 verification 增一条「所选形态解析出的 helper 须与当前工作树同版本 (可用 `diff` 或版本串断言), 解析到旧版即 abort」。

---

### M5 — TASK-014 的「全文无互斥两套」把范围拉进两个本 Spec 明确不碰的面, 与 TASK-019(5) 直接冲突

**锚点**: TASK-014 `verification` (:288) · TASK-019 verification 第 (5) 项 (:375) · `proposal.md:245` §Impact

**实读**: TASK-014 要求「`SKILL.md:262` / `:559` / `:610` 的 helper 定位形态与 TASK-002 定稿一致, **全文无互斥两套**」。而实读这三行:
- `:262` = 本 change 的 `pre_merge_gate.py` — 在范围内 ✅
- `:559` = **`submodule_gate.sh`** 的 Helper 实现行 (§C.2.4.5) —— TASK-019 第 (5) 项逐字把「C.2.4.5 的 `SKILL.md:189-191` 裸 git 命令 + `submodule_gate.sh`」列为「与 D1 根因**同类**的最近兄弟」, 且组 4 标题逐字「follow-up issue (**本 Spec 不修**)」
- `:610` = **`git-remote-helper`** 的降级策略行 (§C.2.5), 与本 change 完全无关

`proposal.md:245` §Impact 的 SKILL.md 变更清单逐字只有「两处散文流程重整 · 四行裸命令去除 · `:270` 示例 · `:267` schema 增 `gate_error` · `:279` 四类早退注记同步 · 步骤 6 的 `fail` 分支补一句」—— **不含 `:559` / `:610`**。

且 TASK-018 的 blast-radius 口径 `pre_merge_gate|gate_check|pre-merge gate` 结构上看不见这两处 (实跑该口径 173 命中, 无一条来自 `submodule_gate.sh` 或 `git-remote-helper`) ⇒ 改了也没有影响面分析。

**镜头 5 备注**: 「不修类只修实例」在本清单里其实处理得不错 (TASK-019 把 `fetch_gate.py:55` / `worktree_manager.py:170` / `submodule_gate.sh` 三个同形兄弟都开了号)。问题出在反方向: TASK-014 悄悄把其中一个兄弟拉回了范围内, 而 TASK-019 同时声明它在范围外。

**修**: TASK-014 的范围限定到 `:262`, 并显式写「`:559` / `:610` 的同款约定归 TASK-019(5) 的 issue, 本 Spec 不改, 因此本 change 落地后 SKILL.md 内**有意**并存两套 —— 这是已知残留而非遗漏」; 或者反过来把 `:559`/`:610` 正式纳入 §Impact 并给 TASK-018 补口径。二选一, 但不能像现在这样两条任务各说各话。

---

### M6 — TASK-004 点名的两个「复用」目标实读后都不能被直接复用, 而唯一可行的复用路径不在 scope 内, 也无任务承接

**锚点**: TASK-004 `verification` 第四条 (:105) 与 `notes` (:106-108) · `metadata.scope_repos[aria].paths` (:9-12) · `proposal.md:126` · `proposal.md:231` §非目标

TASK-004 逐字「⛔ **不得再造**」, 并点名两个复用目标。实读两处源码:

**(a) `path_coverage.py` 的 `_run_git` (:78-98, 三合一在 :93)** — 三个问题:
1. 它**不重试**。SC-8 逐字要求「按 `SKILL.md:259` 重试后 fail」, `:259` 逐字是「max 3 attempts retry (backoff 5s/15s/45s)」。
2. 它把「异常」与「非零退出码」折叠成**同一个返回形状**: 异常路径 `return False, "", f"{type(exc).__name__}: {exc}"`; 非零路径 `return False, "", summary[0] or f"git exit {returncode}"`。调用方拿到的只有一个字符串。而 SC-7 (非零退出码 ⇒ **未重试**) 与 SC-8 (TimeoutExpired ⇒ **重试 3 次**) 的分流恰恰要求这两者可判别 —— 靠字符串前缀 `"TimeoutExpired: "` 嗅探是唯一通道。
3. 它是模块私有符号 (`_` 前缀), 且 `proposal.md:231` §非目标 逐字「**不改** `path_coverage.py` 代码与行为」。

**(b) `ci_backends/aether.py` 的 `_run_with_retry` (:164-187, 常量在 :38-39)** — 结构上跑不了 git:
- 它是 `AetherBackend` 的**实例方法**, 逐字 `subprocess.run([self.binary] + args, ...)`;
- `self.binary = binary or shutil.which("aether")`, 且构造器在 aether 不在 PATH 时 `raise RuntimeError` (:56-61);
- 即「复用」它必须先把它从 AetherBackend 抽出来。

**关键接缝**: 抽取重构落在 `skills/phase-c-integrator/scripts/ci_backends/aether.py`, 而 `metadata.scope_repos[aria].paths` (:9-12) 逐字只有 `SKILL.md` / `scripts/pre_merge_gate.py` / `tests/test_pre_merge_gate.py`; `proposal.md` §Impact 表也没有这一行; 19 条任务里**没有任何一条的 deliverables 含 `aether.py`**。TASK-004 自己的 deliverable 只是「spike 结论回写 proposal.md §5 退出码表」。

⇒ 任务清单命令「不得再造」, 却把唯一不再造的路关在了 scope 之外。留下的 escape hatch (notes 逐字「若是「新写一份」, 必须显式论证为何不能复用」) 于是成了默认路径 —— 而这正是这份 Spec 要治的病 (同一算法两份实现) 在自己的修复里复发。

**修**: 二选一并写死 —— (i) 把 `ci_backends/aether.py` (或新建 `scripts/_subproc.py`) 加进 `scope_repos.paths` + §Impact, 并给 TASK-004 或新任务配上抽取的 deliverable 与「抽取后 `test_ci_backends.py` 25 条零回归」验证; (ii) 承认不复用, 把 notes 的论证义务升级为一条可核的 verification (点明复用不成立的**结构性**理由: 实例方法绑 `self.binary` / 私有 + 非目标 / 无重试 / 异常与退出码不可判别)。

---

### M7 — 无任何任务要求「全部 SC 同时为绿」; 唯一的全量测试检查点不在引入 git 子进程的那条任务的下游

**锚点**: TASK-010 `dependencies: [TASK-006]` (:212) 与 verification 第三条 (:218) · TASK-008 `dependencies: [TASK-003, TASK-004, TASK-005]` (:173)

**实读**: 全清单唯一的整体断言是 TASK-010 的「全量 111 tests 绿 (test_pre_merge_gate 46 + test_ci_backends 25 + test_path_coverage 40)」。它的依赖链是 TASK-010 ← TASK-006 ← TASK-001, **与 TASK-008 平行、不在其下游**。

而 TASK-008 才是插入 `git ls-remote` 子进程的那条。实跑证据: `hasattr(pre_merge_gate, "subprocess")` → **False** (现在不 import), 且受控实跑证实 `mock.patch.object(pc_module.subprocess, "run", ...)` 对任何模块发起的 `subprocess.run` 都生效 ⇒ TASK-008 落地后, `test_sc22` 以及**既有 24 条 `gate_check(` 用例**都会撞上新子进程。谁负责让它们重新变绿, 没有任务写: TASK-005 (接缝) 在 TASK-008 **上游**, TASK-010 (补参) 在**旁支**, TASK-008 自己的 verification 只列 SC-6/7/8/13 + SC-10/SC-11 + 两条早退, **不含 `test_sc22` 仍绿、也不含全量绿**。

顺带: 「全量 **111**」这个数在 TASK-001 加完 4 条断言之后就已经不成立了 (实跑当前 `111 passed`, proposal:282 又说本 change 新增 12)。一个执行时必然对不上的数字, 会诱使执行者把它当近似值忽略, 从而连带忽略这条唯一的整体断言。

**修**: 加一条收口任务 (依赖 TASK-008/009/010/011/012/013/014), verification = 「`pytest tests/ -q` 全绿且计数 == 111 + 本 change 新增数」+「SC-1..SC-13 逐条复跑, 贴输出」。这也顺带修掉 C2/M1 指出的「SC-3 可被下游任务改红而无人复检」。

---

### M8 — ship_target 四处不一致; 且 MAJOR ⇒ v2.0.0 会触发被改文件自带的弃用到期承诺, 无任务承接

**锚点**: `detailed-tasks.yaml:19` · `proposal.md:12` · `proposal.md:257` · `tasks.md:69` · `pre_merge_gate.py:68` / `:116`

**四处逐字**:
| 位置 | 逐字 |
|---|---|
| `detailed-tasks.yaml:19` | `ship_target: "MAJOR — 破坏性签名变更 …"` |
| `proposal.md:12` (header) | 「**ship target**: **地板 = MINOR** … MINOR vs MAJOR **待 owner 裁**」 |
| `proposal.md:257` (§版本) | 「**结论: MAJOR。** 上一版写「地板 = MINOR, MINOR vs MAJOR 待裁」是**逻辑错误**」 |
| `tasks.md:69` (未决 3) | 「**版本 MAJOR 的确认** … 或写下「不构成对外破坏性变更」的论证」 |

proposal 的 header 与它自己的 §版本 直接互斥 (§版本 明说 header 那句是错的却没改 header); tasks.md 把它挂成未决; yaml 已经当成定论。

**衍生问题**: 实测 `aria/.claude-plugin/plugin.json` version = `1.65.5` ⇒ MAJOR = **v2.0.0**。而被改的那个文件里逐字写着:
- `pre_merge_gate.py:68`: `# Old keys still readable until v2.0; new key wins on conflict (Hard #9).`
- `pre_merge_gate.py:116`: `f"will be removed in v2.0"` (DeprecationWarning 文案)

即 ship v2.0.0 会让 `_OLD_TO_NEW` (`primitive_preference` / `no_aether_fallback`) 的移除承诺到期 —— 那是**另一个**破坏性变更, 落在同一个被改的文件里。19 条任务、§非目标、§Impact 均未提及; TASK-017/TASK-018 的口径也不会把它捞出来 (它们找的是 `pre_merge_gate|gate_check|pre-merge gate` 的引用点, 不是版本承诺)。

**修**: 先统一四处 (建议以 §版本 的 MAJOR 为准, 同步改 proposal header 并删 tasks.md 未决 3); 再加一条任务或明确的 §非目标 条款处理 v2.0 弃用到期 —— 「随 v2.0.0 一并移除 legacy alias」或「本次不移除, 把承诺改写为 v3.0 并说明理由」。

---

## Minor

### m1 — TASK-001 的「四条必红」漏了 SC-2, 与它自己给出的理由不自洽
**锚点**: TASK-001 verification (:40-44) · `tasks.md:17`
SC-2 (`grep -c '"branch": "main"' SKILL.md`, 期望 0 / 实跑当前 **1**, 命中 `SKILL.md:270`) 与 SC-1/3/4/5 同类 —— 纯 grep、当前红、零裁量。它只出现在 TASK-013 的 verification 里, 没有红窗。而 TASK-001 的 notes 逐字「红窗本身必须先被验证, 否则后续「变绿」不构成证据」对 SC-2 同样适用。修: TASK-001 改「五条必红断言」。

### m2 — TASK-005 的第二条验证恒真
**锚点**: TASK-005 verification 第二条 (:123) · `tests/test_pre_merge_gate.py:710-724`
「SC-6/SC-13 能用真实 git 受控裸仓运行, **不被该守卫误拦**」—— 实读 `test_sc22` 的 patch 是**单个测试方法内的 `with` 块** (:719-724), 结构上不可能影响别的测试方法。该条无论实现怎么写都绿。真正承重的是第一条 (「用一个故意违规的桩验证它会红」), 那条是好断言。顺带: `test_sc22_no_real_git_subprocess_**in_suite**` 这个名字本身就over-claim —— 它只覆盖自己 `with` 块内的一次 `gate_check`, 不是 suite 级。(预先存在, 不由本 change 引入。)

### m3 — TASK-007 的「同一个 remote 值」断言, 其量在被测面上不存在
**锚点**: TASK-007 verification 第一条 (:161) · `ci_backends/aether.py:189-199` · `proposal.md:132`
逐字「核验与 in-flight 查询使用同一个 **remote 值**与同一个 cwd」。实读 in-flight 那侧: `AetherBackend._query` 逐字 `args = ["ci","status","--branch",branch,"--json"]` + `_run_with_retry` 的 `subprocess.run([self.binary]+args, ...)` —— **没有 remote 参数, 也不传 cwd**。aether 走 API 平面, 根本没有 remote 概念。对比 `proposal.md:132` 逐字只承诺「同一个 `main_branch` 值且同一个 cwd」(不含 remote)。⇒ yaml 这条比 proposal 多出来的那半是恒绿的; 且 tasks.md 的 TASK-007 完全没有这条。修: 删「remote 值」, 保留 cwd 那半并给出可核方式 (例: 断言 `ls-remote` 调用不传 `cwd=`, 与 aether 一致继承进程 cwd)。

### m4 — tasks.md 与 detailed-tasks.yaml 两处不一致 + 一处陈旧
**锚点**: `tasks.md:17` vs yaml TASK-001 deliverables (:38) 与 `metadata.scope_repos` (:9-12) · `tasks.md:67`
(a) tasks.md 逐字「建 `test_premerge_gate_mainbranch.py` (**或并入既有文件**)」, 而 yaml 的 deliverable 与 scope paths 都只允许既有 `tests/test_pre_merge_gate.py` —— 新文件路径不在 scope 内。二选一要写死。
(b) `tasks.md:67` 未决 1「`detailed-tasks.yaml` **是否补**」在 yaml 已存在的前提下陈旧 (且 `standards/openspec/project.md` 的两处表述不一致这一事实经实读确认: `:21` 逐字「Level 3: `proposal.md` + `tasks.md` + `detailed-tasks.yaml` (双层)」, `:118` 逐字「proposal.md + tasks.md」)。
(c) 同段未决 2 (post_planning 闸门) 正由本次审计闭合。三条未决都应在 Phase B 起点前清掉, 否则执行者面对一份自称「未决」的清单。

### m5 — TASK-004 的「非零非 2」在 proposal 的 catch-all 表上凿了一个未定义的分区
**锚点**: TASK-004 verification 第一条 (:102) · `proposal.md:117-124`
proposal §5 退出码表逐字只有四行 (精确匹配 / 取到列表但无精确匹配 / TimeoutExpired / **其余一切**), 并明写「本表以「其余一切」收口 (catch-all), **不是正向枚举** —— 正向枚举对未来新增返回码天然 fail-OPEN」。yaml 写成「**非零非 2** 退出码 ⇒ verify-failed」, 把 2 从 catch-all 里挖出去却没说它归哪一档。「2」只在用 `--exit-code` 时才产生 (受控实跑: 带 `--exit-code` 时 glob 命中仍 RC=0), 而 proposal 采的「对返回 ref 名做精确比对」根本不需要 `--exit-code` ⇒ 这半句把一个已被 Spec 明确删掉的实现假设又带了回来。第三条 catch-all bullet 事实上兜住了 2 (不至于 fail-OPEN), 故列 Minor。修: 删「非 2」, 或写明「若实现采 `--exit-code`, 2 归 not-found 档」。

---

## 轮次记录

| 轮 | 席位 | 结论 | Critical | Major | Minor |
|---|---|---|---|---|---|
| R1 | code-reviewer | FAIL | 2 | 8 | 5 |

**R1 说明**: 本席按六个镜头逐条核验 19 条任务。所有 finding 均基于实读源码或受控实跑 (git 裸仓三组 / pytest 111 passed / 跨模块 patch 拦截 / `find` 副本枚举 / yaml 结构分析 / `git show 7661e96`), 无一条基于推断。

**收敛提示 (供编排层)**: 两条 Critical 的修法都是**加断言/加任务**而非改文档措辞 —— C1 加一条组 0 测试任务, C2 把 SC-3 换成带区间的断言。这与 owner「停止改文档、用 TDD 接管」的裁定同向, 不会重蹈 post_spec 五轮「fix 引入新 Major」的形状。M1/M2/M3/M7 是纯依赖图与锚点修正 (改 `dependencies` 字段 + 加 `head` SHA), 机械且低风险。M4/M5/M6/M8 需要 owner 或 proposal 层的一句裁定 (变量约定 / `:559`+`:610` 归属 / `aether.py` 是否入 scope / ship_target 与 v2.0 弃用), 建议一次性问清再进 Phase B。
