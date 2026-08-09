# Proposal: premerge-gate-mainbranch-failclosed

> **Status**: 📝 **Approved for Phase B (owner override)** — post_spec 跑满 **R1–R5, 25 个 agent-run**, `converged: **false**`, `overridden_by_user: **true**` (owner 2026-08-09)。
>
> ⚠️ **闸门状态必须被如实读**: 这**不是收敛**。owner 依据五轮量化数据 (每轮 fix 引入 73–100% 的新 Major, 总量五轮持平 21→26→22→27→21) 裁定**停止「审计→改文档」循环, 改由 Phase B 的 TDD 承接剩余缺陷**。`max_rounds` 6 中已用 5, 余 1 轮未用。
>
> 📌 **本版的处方边界 (R5 后新增)**: 凡编排层**无法验证**的实现细节, 本 Spec **不再规定**, 一律降为 `tasks.md` 里的 **Phase B spike** —— 五轮实证「继续规定」只会产出新缺陷。**Spec 负责钉住『什么算对』(SC), 不负责钉住『怎么写』。**
> **Created**: 2026-08-08
> **Spec Level**: **3** (原 2 — R4/knowledge-manager 指出范围重定后未重核。判据表逐字「Level 3 = Architecture changes, 输出 proposal.md + **tasks.md**」; 本 Spec 的 9 条阻塞项 + AB + 外部 issue + 多文件同步须 `tasks.md` 承载, 同姊妹 Spec `linked-issue-normalization` 升级理由)
> **关联 Issue**: [aria-plugin #137](https://forgejo.10cg.pub/10CG/aria-plugin/issues/137)
> **代码落点**: `aria/` 子模块 `skills/phase-c-integrator/`; Spec 落主仓 (Rule #5)
> **ship target**: **MAJOR** (见 §版本 — CLAUDE.md:35「破坏性变更须 MAJOR」与 :79「MINOR+」两条下界求交, 唯一解 MAJOR)。⚠️ 待 owner 确认, 且 MAJOR ⇒ v2.0.0 会激活 `pre_merge_gate.py:68/:116` 自带的弃用到期承诺 (TASK-020 承接)。号段落地时计算, 不预写字面量
> **审计轨迹**: `.aria/audit-reports/premerge-gate-mainbranch-failclosed-audit-trail.md` (append-only)。**不一致时以本文件为准** — 该文件记录的是当时判断, 可能已被后续轮次推翻

---

## Why

### 症状

Rule #8 pre-merge gate 的「main 无 in-flight CI run」这条腿在本项目上**恒真**。后端结构上无法区分「分支不存在」与「分支没有 in-flight run」—— 实测 `--branch main` 与 `--branch master` 返回完全同形 (`status:ok`, `runs:[]`, RC=0); `ci_backends/aether.py:117-135` 只在 aether 自身失败时抛。二者都产出 `InFlightStatus(runs=[])` ⇒ 判 green。

### 根因: 同一算法有两份实现, 而 AI 走的是没被加固的那份

`SKILL.md` 里 C.2.4 的散文流程**共有两处**, 合计 **4 行**可照抄的裸命令 (实测 `grep -c 'aether ci status' SKILL.md` = **4**):

| 小节 | 起始行 | 裸命令行 |
|---|---|---|
| `### 步骤执行` | `:99` | `:167` `:168` |
| `### C.2.4 Pre-Merge Precondition Gate (v1.3.0+)` | `:218` | `:243` `:244` |

而 `gate_check()` 完整实现了同一套流程 (实测 precheck / resolve_ci_backend / evaluate_path_coverage / query_branch_in_flight / query_pr_ci / compute_verdict 六项全在)。**AI 走散文那份**; SKILL.md 从无带参 helper 调用示范。

**实测**: `aether ci status --branch '<main-branch>' --in-flight --json` → `runs:[]` RC=0 ⇒ **把字面量换成占位符也是同一个假绿**。

⇒ 只加固 helper 的参数缺省对真实执行路径无效。**必须先把两份实现收敛成一条路径。**

### #137 的处置

#137 报的 helper 缺省是真缺陷, 但它只是两个病因之一; 散文裸命令那条未被它覆盖。

⚠️ **本 Spec 不对 #137 正文的对错做任何裁定, 也不执行任何外部动作** (R5 两席独立 Forgejo 实读后收敛):

- 该 issue 唯一评论 (id **18015**, 编排层前一 session 所写) 逐字是「**我在正文里对 (a) 那条腿的判断是错的**」—— 而本 Spec 的 R4-fix 版曾断言「#137 正文关于 (a) 腿的陈述成立」并计划发一条 supersede 它的评论。**那会在公开 issue 上推翻作者本人的自撤回。**
- 根因: 编排层把两个不同的「(a) 主张」混为一件事 —— body 说「(a) 腿也是绿的」(已被 18015 撤回) 与「(a) 讲的 `not_applicable` 通路真实存在」(成立) 是两句话。
- 另: 本 Spec 前几版使用的 (a)/(b) 标签与 `CLAUDE.md:113` 的 canonical 编号相反。

⇒ **处置: 不打删除线, 不发 supersede 评论, 不改 body。** 若需在 #137 留痕, 由 owner 决定内容与时机。§Impact 的「外部」行已相应改为 no-op。

---

## What Changes

### 1. `SKILL.md` 两处散文流程一起收敛为强制 helper 调用 (承重)

**两处都要改** —— 只改 `### C.2.4` 会留下 `### 步骤执行` 里同款的 `:167`/`:168`, 与本 Spec 要治的病同形。

**要求 (what)**: `SKILL.md §C.2.4` 必须给出一条**可直接执行的 helper 调用**, 取代散文裸命令。

**具体路径解析形态 = Phase B spike, 本 Spec 不规定 (R5 后降级)**。

> **为什么降级**: R4-fix 曾在此规定「两分支 `git rev-parse --show-toplevel` 解析」, R5 四席独立实测该形态在 `standards` / `aria-orchestrator` 子模块根与 **plugin 市场安装态**下全不可达 ⇒ 触发 abort ⇒ **把假绿换成了对所有第三方采用方的恒红**。
>
> 且当时的论据「`${ARIA_PLUGIN_ROOT}` 全仓从未被赋值」是**测错总体** —— 编排层 grep 的是「仓内何处 set 它」, 而它由插件运行时**在仓外**设置。

**spike 的输入 (已实证事实, 供 Phase B 直接使用)**:

| 事实 | 实测值 | 来源 |
|---|---|---|
| **两个环境变量并存, 且 `phase-c-integrator/SKILL.md` 内部用的是 `ARIA_` 那个** | 该文件内 `ARIA_PLUGIN_ROOT` **3 处** (`:262` `:559` `:610`) / `CLAUDE_PLUGIN_ROOT` **1 处** (`:737`); 全仓则 `CLAUDE_` **66 处** / `ARIA_` **5 处** | post_planning R1 四席独立命中 + 编排层复核 |
| **helper 的物理拷贝数 ≠ 访问路径数** | `find` 得 **5 条路径**: marketplaces · 仓内 · cache/1.65.5 · cache/1.63.0 · cache/1.56.1。但**主仓根与 aria 子模块根解析到同一 inode** (是同一个文件); 真正能独立漂移的是 plugin 安装态那份, 且旧 cache 版本内容不同 | post_planning R1 两席 (各自指出不同的错法) + 编排层复核 |
| `SKILL.md:242` 契约要求合并时 cwd = **目标仓根** (子模块合并 → 子模块根) | — | 既有 |

> ⚠️ **上一版这两行都写错了**: 称「`:262/:559/:610` 均用 `CLAUDE_PLUGIN_ROOT`」(实为 `ARIA_`, 方向相反) · 称「3 个副本位置」(把同一 inode 数了两次, 又漏了三份 cache)。**两条都是 spike 的输入 —— 输入错则 spike 必错**, 故此处列出实测值而非结论, 由 spike 自行判断该沿用哪个约定。

**spike 的验收条件 (SC-M12 钉住, 不可协商)**: 所选形态须在**四种 cwd** 下均可达 —— 主仓根 / `aria` 子模块根 / 其他子模块根 / plugin 安装态。**不可达时须 abort 而非放行**, 但 abort 不得在健康常态下发生 (否则是恒红)。

⛔ **不得为解析路径而 `cd`** —— 那会使 §5 的 `ls-remote` 查错仓 (主仓与 aria 子模块都有 `master`, 会 RC=0 假通过)。

### 2. 两处散文的 5 步移入折叠块, 且**去掉全部可执行命令字面量**

`<details><summary>helper 内部算法 (供理解与排障, ⛔ 不要手工执行)</summary>` … `</details>`。

- 折叠块须**补上 §3 新增的分支存在性核验步** (否则折叠块自称描述 helper 内部算法却漏掉本 change 唯一会 BLOCK 合并的那一步);
- 折叠块**不是**保护机制 —— 折叠对 AI 文本阅读无隐藏效果, 真正的保护是**去掉命令字面量** (SC-M2 钉住)。

### 3. `SKILL.md §C.2.4` 的**步骤 6 不动** (归属声明)

步骤 6 (`:252-255`) 是**纯 AI 义务**: 路由决策 + v1.65.0 / #126 两条强制 surface 警告 (helper 只输出 JSON, 不产文案), 且是 `DEC-20260731-001` 逐字记载的 owner 交换条件。

⇒ **它留在折叠块外, 保持命令式**, 本 change 不修改其语义。仅在其 `fail` 分支的措辞里补一句「若 `raw_message` 含 `gate_error` 诊断则一并 surface」。

### 4. helper 三处 `main` 字面量去掉, 参数必填

| 落点 | 现状 | 改为 |
|---|---|---|
| `:427` CLI | `add_argument("--main-branch", default="main", help="Main branch to check (default: main)")` | `add_argument("--main-branch", required=True, help="Main branch to check (required)")` — **help 文案同批改** |
| `:300` 函数签名 | `main_branch: str = "main",` | `main_branch: str,` |
| `:21` docstring | `[--main-branch main]` | `--main-branch <MAIN_BRANCH>` |

**破坏面**: 既有 **24 处** `gate_check(` 调用点 (实测显式传 `main_branch` 的 **0** 处) 全部 `TypeError`, 须逐处补 `main_branch="master"`。

### 5. 新增 `--remote` + 分支存在性核验

`gate_check(..., remote: str = "origin")` / CLI `--remote`, 默认 `origin`。查 in-flight **之前**:

**要求 (what)**: 在查 in-flight 之前, 独立核验 `<main_branch>` 在 `<remote>` 上**确实存在**, 且该判定**不得依赖 `ls-remote` 的 pattern 匹配语义**。

⚠️ **两次修法都不够, 第三次才对** (三轮受控实验):

| 修法 | 实测 | 结论 |
|---|---|---|
| 裸分支名 `--heads <r> master` | 远端只有 `refs/heads/wip/master` 时返 **RC=0** (尾段 glob) | ❌ fail-OPEN |
| 锚定 `--heads <r> "refs/heads/master"` | 关掉了尾段匹配, **但** `refs/heads/mast*` / `m[a]ster` / `maste?` / `*` 仍**全返 RC=0** | ❌ 仍 fail-OPEN (name 含 glob 元字符时) |
| **对返回的 ref 名做精确字符串比对** | 不依赖 pattern 语义 | ✅ **本 Spec 采用** |

⇒ 判据是「**远端返回的 ref 名列表中, 是否存在一条 `== "refs/heads/" + main_branch` 的精确匹配**」。具体实现形态 (是否仍借 `ls-remote` 取列表 / 如何解析) = **Phase B spike**; 验收由 SC-M6 + 新增 SC-M13 钉住。

| 情形 | 判据 | 输出 | 重试? |
|---|---|---|---|
| ref 列表含**精确匹配** | — | 继续原流程 | — |
| ref 列表**取到了但无精确匹配** | 分支不存在 | `verdict=fail` + `gate_error.kind="main-branch-not-found"` | **否** |
| subprocess timeout (`TimeoutExpired`) | 查询失败 | 按 `SKILL.md:259` 既有规范重试; 仍超时 ⇒ `fail` + `kind="main-branch-verify-failed"` | **是** |
| **其余一切** — 非零退出码 (实测 remote 名不存在 / 坏 URL / 网络不可达均为 **128**, 用法错误 129) · `FileNotFoundError` (git 二进制缺失, **抛异常无退出码**) · `OSError` · 输出不可解析 · **任何未枚举情形** | 查询失败 | `verdict=fail` + `kind="main-branch-verify-failed"` | **否** |

> **本表以「其余一切」收口 (catch-all), 不是正向枚举** —— 正向枚举对未来新增返回码天然 fail-OPEN。**不援引 `SKILL.md:260` 的 exit 1-126**: 实测真实失败码是 128, 在区间外; 且 `:260` 自带 `127 → no_ci_fallback` 会使 verdict 变 green。
>
> **异常处理可复用同包先例**: `path_coverage.py:93` 已有 `(TimeoutExpired, FileNotFoundError, OSError)` 三合一。**重试逻辑亦不得再造** —— `ci_backends/aether.py:38` 已有 `RETRY_BACKOFF=(5,15,45)` / `MAX_RETRY_ATTEMPTS` / `_run_with_retry`; 在一份治「同一算法两份实现」的 Spec 里再造第二份是自相矛盾 (R5 两席命中)。复用形态 = Phase B spike。

⛔ 任何情形都不得当成「存在」放行。

**层级声明**: 本核验产出的是 gate 层的 `gate_error.kind`, **不是**把 `ci_backends/base.py:29` 的 backend 层 `not_found` 提升为 gate 输出 (`SKILL.md:279` 逐字记载 gate 目前不产生它, 本 Spec 不改变)。

**已知残留限制**: `ls-remote` 走 git 平面, CI backend 走 API 平面, 二者不保证同源。本 Spec 只保证核验与 in-flight 查询使用**同一个 `main_branch` 值**且**同一个 cwd**。

### 6. 核验点: 三个早退**之后**、`evaluate_path_coverage` **之前**

```
:328 enabled=false     → 早退 (green)
:338 no backend        → 早退
:345 precheck 失败     → 早退 (fail)          [:344 是 precheck() 调用行]
★ 存在性核验 (本 Spec 新增)
:358 evaluate_path_coverage(main_branch=...)   [:356 是 pc=None, :357 是条件行]
:366 query_branch_in_flight(main_branch)
```

**在三早退之后**: 否则 owner 显式关闭的闸门与 `no_ci_fallback` 既有降级会被变成 `fail`。
**在 path coverage 之前**: 它更早消费 `main_branch`, 放它之后等于放行一次未核验的使用。

### 7. `verdict` 三态封闭; 诊断信息**主通道是 `raw_message`**

`verdict` 仍是 `green` / `wait` / `fail`。理由: `pre_merge_gate.py:47-49` / `SKILL.md:267` schema / `SKILL.md:252-255` 路由 / `gate_state_helper.py:32-34` 四处均封闭枚举, 且 `gate_state_helper.py:147` 是 `"status": verdict` 原样写入无校验。

**诊断信息的落点** (R4: `gate_error` 无消费者 —— `SKILL.md:255` 逐字规定 `fail` 的 surface 通道是 `raw_message`, `write_gate_state()` 签名亦无该形参):

- **`raw_message` 是主通道 (必填)**: 失败时须写入人类可读诊断, 含分支名与 remote 名, 且**明确区别于「无 in-flight run」**;
- `gate_error` 是 **additive 可选结构化副本** (沿用 v1.65.0 `path_coverage` 先例), 供未来机读消费:

```json
"gate_error": {
  "kind": "main-branch-not-found",
  "remote": "origin",
  "branch": "<MAIN_BRANCH>",
  "message": "同 raw_message"
}
```

> 示例的 `branch` 用占位符而非真值 —— 若写 `"branch": "main"`, 该 schema 搬进 `SKILL.md:267` 后会与 SC-M2 直接对撞。

**在场范围**: `SKILL.md:279` 逐字是**四类早退** (`enabled:false` / no-backend / precheck 失败 / **backend query 失败**) 保持六键不变; `gate_error` 只在本 Spec 新增的核验失败路径在场。

---

## 决策记录

| # | 决策 | 要点 |
|---|------|------|
| **D1** | **两处散文一起收敛为强制 helper 调用** | 承重。只改一处等于没改 (R4 实测另一处有同款 2 行) |
| **D2** | 路径用**两分支解析 + 不可达即 abort**, 不用环境变量 | 实测无单一形态跨两种 cwd 可达; `ARIA_PLUGIN_ROOT` 全仓未赋值, `CLAUDE_PLUGIN_ROOT` 运行时亦 unset |
| **D3** | ⛔ 不得为解析路径而 `cd` | 会使核验查错仓 (两仓都有 `master` ⇒ 假通过) |
| **D4** | 步骤 6 **留折叠块外不动** | 纯 AI 义务 + `DEC-20260731-001` owner 交换条件 |
| **D5** | helper 三处字面量去掉 + 参数必填 | 只改 CLI 会留函数签名这条内部路径恒绿 |
| **D6** | 存在性核验 pattern **锚定 `refs/heads/<name>`** | 裸分支名是尾段 glob (两次独立受控实验复现) |
| **D7** | 退出码分区**自带完整表**, 不援引 `:260` | 实测失败码是 128, 在 1-126 之外; 且 `:260` 的 127 分支会变 green |
| **D8** | `verdict` 三态封闭; **`raw_message` 为诊断主通道**, `gate_error` 为 additive 副本 | 第四枚举值四处无人认识; `gate_error` 目前无消费者 |
| **D9** | 核验点在三早退之后、path coverage 之前 | 之前会改 owner 关闭闸门的语义; 之后会放行未核验的使用 |
| **D10** | Rule #6 落**第二行「照跑 AB, 零裁量」** | SOT 直接管辖条款, 见 §Rule #6 |
| **D11** | Level **3**; 版本**地板 MINOR** | 判据表输出栏 + CLAUDE.md:79 分别直接管辖 |

---

## Success Criteria

> **每条 grep 断言的 pattern 与今日计数均已实跑**, 输出见下表「今日实测」列。SC-M1..SC-M5 零裁量。

| SC | 断言 (逐字可复跑) | 期望 | 今日实测 | 怎么会红 |
|----|------|------|------|---------|
| **SC-M1** | `grep -c 'aether ci status' aria/skills/phase-c-integrator/SKILL.md` | **0** | **4** | 必红。**一条断言覆盖 `:167`/`:168`/`:243`/`:244` 全部四行** |
| **SC-M2** | `grep -c '"branch": "main"' .../SKILL.md` | **0** | **1** | 必红 (`:270`) |
| **SC-M3a** | `grep -c -- '--main-branch "<MAIN_BRANCH>"' .../SKILL.md` | **2** | **0** | 必红 —— **D1 承重红窗**。断言的是**占位符形态**, 两处散文各一条 |
| **SC-M3b** | `grep -cE -- '--main-branch +(main\|master)([[:space:]]\|$)' .../SKILL.md` | **0** | **0** | **负控**: 写死字面值的实现在此必红。⚠️ **本条是 PC1 的修复** —— 上一版只断言 `--pr-branch` 存在, 而 `--main-branch main` 写死能通过全部断言 (实测 0/0/2 全过)。**断言的量必须是病灶所在的量** |
| **SC-M3c** | 提取 `<details>…</details>` 全部折叠块, 统计其中含 `--pr-branch` 的块数 | **0** | **0** | **负控**: 把调用藏进折叠块的实现在此必红。⚠️ 修复 code-reviewer 指出的第二个失明面 —— SC-M1/M3a 都是**全文件计数, 无位置维度**, 而病灶逐字是「AI 走散文那份」, **位置就是病灶所在的量** |

> **SC-M3a/b/c 已做对抗性验证** (不只验当前值): 构造「好实现 (占位符+调用在折叠块外)」「坏实现 A (写死 `--main-branch main`)」「坏实现 B (调用藏进折叠块)」三个 fixture 实跑 —— 好实现全过, **两个坏实现各被 M3b / M3c 拒绝**。
| **SC-M4** | `grep -c 'default="main"' .../pre_merge_gate.py` / `grep -c 'main_branch: str = "main"' ...` / `grep -c -- '--main-branch main' ...` | **0 / 0 / 0** | **1 / 1 / 1** | 必红 |
| **SC-M5** | `grep -c 'default: main' .../pre_merge_gate.py` (help 文案) | **0** | **1** | 必红 |
| **SC-M6** | 受控裸仓: 远端只有 `refs/heads/wip/master`, 传 `--main-branch master` | `verdict=fail` + `kind=="main-branch-not-found"` + **`raw_message`** 含分支名与 remote 名 | — | 今日无核验 ⇒ green ⇒ 必红。**承重断言 (D6)**。**用真实 `ls-remote`, 不打桩** |
| **SC-M7** | `ls-remote` 返回 **128** (mock 或指向不存在的 remote 名) | `fail` + `kind=="main-branch-verify-failed"`, **未重试** | — | 当「不存在」→ 误报 / 当「存在」→ 恒绿, 两向都红 |
| **SC-M8** | `ls-remote` 抛 `TimeoutExpired` (**mock**; 须 mock `time.sleep`) | 3 attempts 后 `fail` + `kind=="main-branch-verify-failed"` | — | 未按 `:259` 重试的实现红; 未 mock sleep 致 >60s 亦红 |
| **SC-M9** | `gate_check(pr_branch=...)` 不传 `main_branch` | `TypeError` | — | 现状签名有缺省 ⇒ 静默成功 ⇒ 必红。**唯一覆盖内部调用路径**。(本 skill 的函数名是 `gate_check`; `run_gate` 属 `state-scanner/phase1_gate.py`) |
| **SC-M10** | 负控: `enabled=false` 早退 | 六键不变、无 `gate_error`, **且 `assert ls-remote 未被调用`** | — | 缺后半条因果断言则健康与不健康实现都绿 (D9 守不住) |
| **SC-M11** | 负控: 分支存在且有 in-flight | `verdict=wait` 不变 | — | 核验不得改变正常路径判决 |
| **SC-M12** | **参数化四种 cwd** 跑 §1 的调用: 主仓根 / `aria` 子模块根 / `standards` 子模块根 / 模拟 plugin 安装态 | **四种全部可达并正常执行** (非 `No such file`) | — | 上一版的两分支解析在后两种下必红 (R5 四席实测)。⚠️ 上一版 SC-M12 只测一种 cwd, 对该失效**恒绿** |
| **SC-M13** | 受控裸仓: 远端只有 `refs/heads/master`, 传 `--main-branch 'mast*'` (及 `m[a]ster` / `maste?`) | `verdict=fail` + `kind=="main-branch-not-found"` | — | **锚定 pattern 实现必红** —— 实测这三个 pattern 对该远端全返 RC=0。**本条钉住「精确比对」而非「锚定」, 是 R2 承重 Critical 的真正闭合腿** |

**打桩边界 (前一版自相矛盾, 本版钉死)**: **只有 SC-M6 用真实 `ls-remote` + 受控裸仓**; SC-M7 / SC-M8 必须 mock (真实 `ls-remote` 无法产出确定性 128 或 timeout)。

**测试隔离 (R4/QC4)**: `test_sc22_no_real_git_subprocess_in_suite` (`:710`) 的 patch **本就全局生效** (`import subprocess` 使模块对象共享 —— 受控实验证实, 前一版的相反陈述已作废)。⇒ D5 落地后既有 ~24 处调用会**击穿该基线使其转红**。`tasks.md` 须含一条前置任务: 为既有调用补 `main_branch="master"` **并**为 gate 层核验建独立打桩接缝, 使 `test_sc22` 保持有效而非被放宽。

---

## Rule #6

`rule6_note`: **判据表第二行 —— 处方性 · 运行时指令面 ⇒ 照跑 AB, 零裁量。不申请任何豁免。** SOT: `standards/conventions/skill-benchmark-exemption.md`。

**定档依据 (直接管辖条款)**: SOT「SKILL.md 有变动时的附加约束」段逐字 —— **「`description` 或指令流程变动 ⇒ 一律第二行」**。D1 是指令流程变动, 无需也不得再讨论「套件测不测得到」。

> SOT 对第三行的措辞是「**典型**: authoring 向导」—— authoring 是**举例不是定义**, 真实判据是「覆盖范围外」。本 Spec 不走第三行, 此处仅避免把举例当规则复用。

⇒ ship 前须过 `ab-suite/phase-c-integrator.json` 与 `ab-suite/phase-c-integrator-pre-merge-gate.json`, 结果存 `ab-results/`。**已知**: 两套件对 C.2.4 覆盖薄 (承 aria-plugin #127), 本 Spec **不以此降档**, 且诚实声明**D1 的行为证据主要由 SC-M1 / SC-M3a-c / SC-M12 承担**, AB 是合规义务而非本 change 的主要证据来源。

---

## 非目标

- **不引入** `main_branch` 自动解析 —— R2 实测 `ls-remote --symref` 存在 RC=0 但无 `ref:` 行两态 (unborn / detached), 需独立设计。必填 + 存在性核验已足以关闭本 Spec 的失效模式;
- **不改** `path_coverage.py` 代码与行为;
- **不改** `aether` CLI 返回语义;
- **不改** `branch-manager` 合并动作 (aria-plugin #136);
- **不改** `workflow-runner` 的 `gate_state` schema;
- **不改** `SKILL.md` 步骤 6 的语义 (D4);
- **不动** `no_ci_fallback` / stub backend 既有降级语义 —— 由 **SC-M10** 机械钉住;
- **不修**同形兄弟位置 —— `phase-d-closer/fetch_gate.py` 的字面 `("master","main")` 回落 · `state-scanner/lib/worktree_manager.py:170` 的 `base_branch: str = "master"` (与 `pre_merge_gate.py:300` 完全同形)。⚠️ **Phase B 实施者不得照抄 `fetch_gate.py`**。开 follow-up。

---

## Impact

| 文件 | 变更 |
|------|------|
| `aria/skills/phase-c-integrator/SKILL.md` | **两处**散文流程重整 (`### 步骤执行` :99 段 + `### C.2.4` :218 段) · 四行裸命令去除 · `:270` 示例 · `:267` schema 增 `gate_error` · `:279` 四类早退注记同步 · 步骤 6 的 `fail` 分支补一句 |
| `.../scripts/pre_merge_gate.py` | `:21` `:300` `:427` + help 文案 · `--remote` / `remote` 参数 · `_verify_branch_exists()` · `raw_message` 诊断 + `gate_error` additive 键 · 核验点插入 |
| `.../tests/test_pre_merge_gate.py` | SC-M1..SC-M12; 既有 **24 处**调用补 `main_branch="master"`; `test_sc12` (`:663`) 断言改 `"master"`; **为 gate 层核验建独立打桩接缝** |
| **`CLAUDE.md`** | 规则 #8 那段须同步 —— 本 Spec 给 pre-merge gate **新增第三条阻断腿**。先例: v1.31.0 CI backend 抽象化在同一提交同步过 Rule #8 (`commit 7661e96`) |
| `openspec/changes/.../tasks.md` | **新建** (Level 3) —— 承载 9 条阻塞项 + AB + 外部 issue |
| AB | 两套件照跑, 结果存 `ab-results/` |
| 外部 | **无外部动作** —— 不改 #137 body, 不发 supersede 评论 (见 §Why)。留痕与否由 owner 决定 |
| 发版同步面 | 按**引用点整仓差集**枚举 (非文件白名单)。⚠️ 上一版缺此行, 而姊妹 Spec 同日开出的 **Aria #177** 正是预警「下次会原样重犯」—— 本 Spec 是该预言的即时复现样本, 此行为补入 |
| follow-up issue | (1) `main_branch` 自动解析设计面; (2) `fetch_gate.py` / `worktree_manager.py:170` 同形回落; (3) `workflow-runner` `gate_state` 无 `gate_error` 位置; (4)「显式传错分支名」此前零测试覆盖 |

### 版本

**结论: MAJOR。** 上一版写「地板 = MINOR, MINOR vs MAJOR 待裁」是**逻辑错误** (R5 两席 + 归档先例佐证):

- `MINOR+` 是**下界, 不是枚举** —— MAJOR 满足「MINOR+」;
- CLAUDE.md:35「**破坏性变更须 MAJOR**」是**下界为 MAJOR**;
- 本 Spec 自认 D5 (CLI 参数由可选变必填, 24 处既有调用 `TypeError`) 是破坏性变更;
- ⇒ 两条下界求交, **唯一解是 MAJOR**。上一版的「地板 = MINOR」给下游留了看似合规的违规口。

⚠️ 若 owner 认为本变更**不构成对外破坏性变更** (例如判定该 helper 无对外契约地位), 则须**显式写下该论证**并据此改档 —— 不能靠「地板」措辞绕过。

号段落地时按 `plugin.json` 当前版本计算, 不预写字面量。

### 风险

**blast radius** —— 依赖旧缺省的调用方转硬失败。Phase B 核验口径 (含 `pre-merge gate` 这个不含下划线的写法, 否则搜不到 `CLAUDE.md`):

```bash
grep -rniE 'pre_merge_gate|gate_check|pre-merge gate' \
  --include='*.py' --include='*.md' --include='*.sh' --include='*.json' --include='*.yaml' --include='*.yml' \
  aria/ aria-orchestrator/ standards/ docs/ CLAUDE.md
```

⚠️ 该口径**结构上看不见外部采用方** (Kairos 等)。作为破坏性变更, follow-up 须含下游通告项。

### 测试基线

`phase-c-integrator` 现 **111** tests (`test_pre_merge_gate.py` 46 + `test_ci_backends.py` 25 + `test_path_coverage.py` 40)。本 change 新增 12, 修改既有 24 处调用 + 1 处断言 + 1 处守卫接缝。

---

## 待 R5 重点审

本版是 **R4-fix**, 按四轮规律**最大风险在本轮新写的内容**。请优先验:

1. **§1 的四行调用块**是否真的在两种 cwd 下都可达、且 abort 分支真会阻断 (⚠️ 前一版正是在这里恒红/不可达);
2. **SC 表「今日实测」列**逐条复跑 —— 该列是本版新引入的自陈, 按本项目实证自陈必须回源;
3. **§5 退出码表**是否穷尽 (`FileNotFoundError` / 非 git 目录 / `--exit-code` 与 `--heads` 组合的其他返回码);
4. **§7 的 `raw_message` 主通道**是否与 `SKILL.md:252-255` 步骤 6 的既有措辞真的衔接得上 (D4 声称只补一句);
5. **条款间交叉一致性** —— 本版新增 D1-D11 十一条, 前四版每一版都出现过「同一文件内既立判据又违反它」(已发生 3 次)。
