# Proposal: premerge-gate-mainbranch-failclosed

> # ⛔ 范围已重定 (2026-08-12) — 本 Spec 现为 **B 侧**
>
> **裁定**: [DEC-20260812-001](../../../docs/decisions/DEC-20260812-001-premerge-gate-spec-split.md) (owner,
> 经 audit-engine §降级策略 `AskUserQuestion` 三路径选择)。
> **触发**: post_planning `max_rounds = 4` **走满未收敛** (R1→R4: 4R/1P · 4R/1P · 4R/1P · **5R/0P**;
> 去重 Major **四轮持平 ~13**; 每轮 fix 引入 53%→70%→**71%**; 而**旧 finding 无一复发**)
> ⇒ 问题在**被审对象的规模**, 不在执笔也不在审计。
>
> **已拆出 A 侧**: [`premerge-gate-branch-existence`](../premerge-gate-branch-existence/proposal.md)
> (Level 2, **MINOR**, 纯 additive) —— 承接 **分支存在性核验 + `--remote` + `raw_message` 诊断 +
> 测试隔离接缝 + 异常/重试按轴复用**。
>
> 🔴 **更正 (2026-08-12, A 侧 post_spec R1 四席独立命中)**: 上一版此处逐字写「即**关掉 #137 那条恒绿腿
> 所需的全部内容**」—— **该句不成立, 已作废**。A 承接的是**关掉 `gate_check()` 那份实现里的恒绿腿**所需的内容;
> 而本 Spec §根因逐字「**同一算法有两份实现, 而 AI 走的是没被加固的那份**」—— `SKILL.md:243`
> (§C.2.4 执行流程编号步骤本体) 仍硬编码 `aether ci status --branch main`, 且本仓
> `git ls-remote --heads origin main` 实测**零行 + RC=0** ⇒ **A ship 后散文路径仍恒绿**。
> ⇒ **#137 的闭环判据挂在本侧 D1** (两处散文收敛为 helper 调用), **不得据 A ship 关闭 #137**。
> 详见 A 侧 §残余暴露。
>
> **本 Spec (B 侧) 保留**: `SKILL.md` 两处散文收敛为 helper 调用 (承重 D1) · 折叠块 ·
> **`--main-branch` 改必填 (D5, 破坏性)** · 24 处调用补参 · helper 路径解析 spike ·
> **MAJOR** · v2.0 弃用到期承诺承接 (跨两仓 5 文件) · 发版同步面 9 项 · Rule #6 AB。
>
> ⚠️ **R4 的 3 条 Critical 全部属本侧** (`TASK-017` gitlink 求值时点 / `.aria/config.template.json`
> 键名面零机械断言 / `CLAUDE.md:113` 被 TASK-020 条件性证伪而无任务承接)。**A 侧不继承任何 Critical。**
>
> 📌 **下方正文与 `tasks.md` / `detailed-tasks.yaml` 尚未按 A/B 划界重写** —— 迁往 A 的条款
> (原 §5 / §6 / §7 的一部分 + TASK-003/004/005/007/008/009) **须留 cancelled 痕迹而非静默删**
> (同 TASK-020 的条件任务纪律)。**这是 Phase A.1 的待办, 见 DEC §5。**
>
> ---

> **Status**: 📝 **Approved for Phase B (owner override)** — post_spec 跑满 **R1–R5, 25 个 agent-run**, `converged: **false**`, `overridden_by_user: **true**` (owner 2026-08-09)。
> ⚠️ **该 Status 写于拆分前, 现已陈旧** —— post_planning 其后跑满 R1–R4 均 FAIL, Phase B 入口
> 被该闸门阻断 (6 条 `blocks_phase_b`), 拆分裁定即因此而来。**本侧当前不具备进 Phase B 的条件。**
>
> ⚠️ **闸门状态必须被如实读**: 这**不是收敛**。owner 依据五轮量化数据 (每轮 fix 引入 73–100% 的新 Major, 总量五轮持平 21→26→22→27→21) 裁定**停止「审计→改文档」循环, 改由 Phase B 的 TDD 承接剩余缺陷**。`max_rounds` 6 中已用 5, 余 1 轮未用。
>
> 📌 **本版的处方边界 (R5 后新增)**: 凡编排层**无法验证**的实现细节, 本 Spec **不再规定**, 一律降为 `tasks.md` 里的 **Phase B spike** —— 五轮实证「继续规定」只会产出新缺陷。**Spec 负责钉住『什么算对』(SC), 不负责钉住『怎么写』。**
> **Created**: 2026-08-08
> **Spec Level**: **3** (原 2 — R4/knowledge-manager 指出范围重定后未重核。判据表逐字「Level 3 = Architecture changes, 输出 proposal.md + **tasks.md**」**直接管辖**; 本 Spec 的 **TDD 前置 / 实现 / SKILL.md / 合规与同步面 / follow-up 五组共 21 条任务**须 `tasks.md` 承载, 同姊妹 Spec `linked-issue-normalization` 升级理由。⚠️ 上一版此处与 §Impact 均写「**9 条阻塞项**」—— 该数与本 Spec 内任何可数集合都对不上 (§What Changes 7 / `tasks.md` checkbox 21 / 组 0 五条 / SC 17 / 决策 11), 是范围重定前的陈旧数, **已删**; Level 3 由判据表条款直接管辖, 不需要这个数)
> **关联 Issue**: [aria-plugin #137](https://forgejo.10cg.pub/10CG/aria-plugin/issues/137)
> **代码落点**: `aria/` 子模块 `skills/phase-c-integrator/`; Spec 落主仓 (Rule #5)。⚠️ **落点跨两个仓** —— TASK-020 的删除面含主仓 `.aria/config.template.json` (见 §Impact)
> **ship target**: **MAJOR** (见 §版本 — CLAUDE.md:35「破坏性变更须 MAJOR」与 :79「MINOR+」两条下界求交, 唯一解 MAJOR)。**2026-08-10 依 owner 授权裁定确认 MAJOR**, 不再是「待确认」(Rule #10 留痕: 该裁定由 AI 依 owner 显式授权作出, **须写入 handoff 请复议**)。MAJOR ⇒ v2.0.0 会激活 `pre_merge_gate.py:68/:116` 自带的弃用到期承诺 (TASK-020 承接)。号段落地时计算, 不预写字面量
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
>
> ⚠️ **2026-08-10 补测 —— 两个方向必须一起读, 只读一半会推出相反的错结论**:
> (a) 在 C.2.4 的**实际执行路径** (AI 用 Bash 工具敲命令) 上, `CLAUDE_PLUGIN_ROOT` 与 `ARIA_PLUGIN_ROOT` **双双 unset** (实跑)。早前「harness 自动注入 `CLAUDE_PLUGIN_ROOT`」那条实证取自 **PreToolUse hook 执行上下文** —— 与 Bash 工具上下文是**两个环境** (Aria #178 的题目), **不可互相援引**;
> (b) **但 `CLAUDE_PLUGIN_ROOT` 是目前唯一能指向仓外安装根的机制**。实测两个真实采用方 `/home/dev/Kairos` 与 `/home/dev/SilkNode` **都有 `.aria/`、都没有 `aria/` 与 `skills/`**, helper 实际位于仓外 `/home/dev/.claude/plugins/marketplaces/10CG-aria-plugin/skills/phase-c-integrator/scripts/` (已 ls 确认)。
> ⇒ **任何「cwd 相对候选探测」结构上都够不到它**。故 **⛔ 不得把 `CLAUDE_PLUGIN_ROOT` 降为非承重可选覆盖** —— 那等于让承重路径结构上到不了 plugin 安装态, 即原样重犯上一段那条恒红。

**spike 的输入 (已实证事实, 供 Phase B 直接使用)**:

| 事实 | 实测值 | 来源 |
|---|---|---|
| **两个环境变量并存, 且 `phase-c-integrator/SKILL.md` 内部用的是 `ARIA_` 那个** | **⚠️ 必须带计数法读** (总体 = `aria` 子模块, 范围 = git-tracked)。**按行数**: 该文件内 `ARIA_` **3 行** (`:262` `:559` `:610`) / `CLAUDE_` **1 行** (`:737`); 子模块内 `CLAUDE_` **65 行** / `ARIA_` **5 行**。**按 occurrence** (`git grep -o`): 该文件内 **4 / 1**; 子模块内 `CLAUDE_` **66** / `ARIA_` **7** | post_planning R1 四席 + 编排层 2026-08-10 三项口径对齐复跑 |
| **helper 的物理拷贝数 ≠ 访问路径数** | `find` 得 **5 条路径**: marketplaces · 仓内 · cache/1.65.5 · cache/1.63.0 · cache/1.56.1。但**主仓根与 aria 子模块根解析到同一 inode** (是同一个文件); 真正能独立漂移的是 plugin 安装态那份, 且旧 cache 版本内容不同 | post_planning R1 两席 (各自指出不同的错法) + 编排层复核 |
| `SKILL.md:242` 要求 cwd = **目标仓根** (子模块合并 → 子模块根) | ⚠️ **作用域限于步骤 2.5「Path coverage 评估」** —— 实读该句讲的是 `evaluate_path_coverage(main_branch, pr_branch)` 的调用上下文, **不是 C.2 合并全流程的契约**。引用它必须带这个限定 | 既有 + 编排层 2026-08-10 实读更正 |
| `SKILL.md:610` 要求路径 **相对项目根** | 逐字:「(路径相对项目根; `ARIA_PLUGIN_ROOT` 环境变量优先)」 | 编排层 2026-08-10 实读 |
| **仓内已 ship 的同类先例 (spike 应援引而非再造)** | `aria/hooks/submodule-gate-telemetry.sh:60-62` 实读 = 「`${CLAUDE_PLUGIN_ROOT:-}` 优先 → 不中则自定位 → 仍不中即 `exit 0` (fail-closed)」。**可移植的是这个结构** (显式优先序 + 不中即收口), ⚠️ **不是 `BASH_SOURCE` 本身** —— hook 是脚本自己定位自己, 而 C.2.4 是 AI 照 `SKILL.md` 敲一条命令, 敲之前没有 `BASH_SOURCE`。⛔ 亦**不得**据此把「cwd 相对候选」升为主路径 (第 5 种 cwd 结构上够不到, 见上文 (b)) | post_planning R2/backend-architect + 编排层实读 |

> ⚠️ **上一版本表的前两行都写错了** (末两行是本版新增): 称「`:262/:559/:610` 均用 `CLAUDE_PLUGIN_ROOT`」(实为 `ARIA_`, 方向相反) · 称「3 个副本位置」(把同一 inode 数了两次, 又漏了三份 cache)。**两条都是 spike 的输入 —— 输入错则 spike 必错**, 故此处列出实测值而非结论, 由 spike 自行判断该沿用哪个约定。
>
> ⚠️ **本版又抓到第三处**: 上一版的「全仓 `CLAUDE_` **66 处** / `ARIA_` **5 处**」是**混口径** —— 66 是 occurrence 数、5 是行数, **没有任何单一计数法能同时给出这一对**。引用计数前必须并列写出「总体 / 范围 / 计数法」三项 (memory `critique-repeats-error`)。

**🔴 spike 的真正题目是「锚点未定论」, 不是「变量名选错」** (2026-08-10 实读):

上表末两行是**一对互斥锚点** —— `:242` 把 **gate 运行时的 cwd** 钉在目标仓根 (子模块合并时 = 子模块根), `:610` 把 **helper 文件的查找起点**钉在项目根; 而 `${VAR:-aria}` 的 `:-aria` 回落在两个变量都 unset 时**把二者压成同一个相对路径**, 于是子模块合并下这两条钉子指向不同目录。

> ⚠️ **引用边界**: `:242` 只管步骤 2.5 的调用上下文, `:610` 只管 C.2.5 的降级探测 —— **本段主张的是「两条钉子在同一次子模块合并里不能同时成立」, 不是「`:242` 是 C.2 全流程契约」**。越过这个边界即是本项目已有前科的 `:242` 误引 (memory `delegate-verify`)。

⇒ **把 `ARIA_` 换成 `CLAUDE_`、或退役掉其中一个, 锚点矛盾原封不动** —— 那是换标签不是换病灶所在的量。

⇒ **TASK-002 必须先定锚点**: 项目根 / 目标仓根 / **仓外安装根** 三选一, 或给出显式优先序; **再**谈用什么机制表达它。变量归属是 spike 的**产出**, 不是它的输入 —— 本 Spec 与 `tasks.md` 均不预先定死 (依赖方向: TASK-014 ← TASK-002)。

#### 🔴 spike 的第二件产出: **TASK-014 的验收判据本身** (R3-fix 新增, 这是一次「换手段类别」不是「换量」)

**本 Spec 不再预写 TASK-014 的机械验收量。** 理由是**结构性**的, 逐字记录以防第五次:

> TASK-014 要断言的是「`SKILL.md:262`/`:559` 两处已改为定稿形态 F」。而 **F 的类型本身是 TASK-002 的产出** —— 本节把可移植物定为「显式优先序 + 不中即收口」这个**结构** (援引 `submodule-gate-telemetry.sh:60-62`, 那是 3 行 bash)。F 可能是一个路径字符串, 也可能是一个多候选探测块; **在 spike 跑完之前, 连「被比较的东西是不是一个字符串」都未定**。
> ⇒ 任何在 A.2 阶段预写的量都必须先假设 F 的形状, 而每一次假设错都产出一个恒红或恒绿的量。**已连续四次**: (a)「全文无互斥两套」(今日已假, 实存 4 套) → (b)「2 个落点全部为定稿形态」(SC-M3a 要求新增 2 条 ⇒ 实为 4) → (c)「旧形态命中集合恰为 `{:610}`」(与「不得按行号核」自相矛盾 ⇒ 恒红) → (d)「两处路径表达式**逐字 == 同一个 F**」(实读 `:262` 尾段 `pre_merge_gate.py`、`:559` 尾段 `submodule_gate.sh`, **两个不同脚本名**, 不可能同时逐字等于同一个 F ⇒ 恒红)。
> TASK-014 的 notes 逐字写着「若第四次再来, 请优先怀疑『拿 grep 计数当验收』这个手段本身在此不适用」。**第四次来了, 故本轮执行那句话。**

⇒ **改法 = 把判据的产出时点移到有信息的那一刻**, 而不是再造第五个量:

1. **TASK-002 的 deliverable 增加一项**: 回写 proposal §1 时, 除 F 的定稿形态外, **必须同时写下 TASK-014 的可复跑验收命令与期望值**, 落成 §1 下的一个**四级标题小节**, 标题行逐字为 `#### TASK-014 验收判据 (由 TASK-002 spike 产出)`。写得出什么量, 取决于 F 落成什么形状 —— 那时才有信息。
2. **TASK-014 的验收 (1)/(2) 改为**: 「执行 §1 该小节给出的命令并贴出实跑输出, 结论为期望值」。⇒ **在 TASK-014 求值时它是完全机械的**; 在 A.2 阶段它是一条**对交付面的结构性要求**, 不是一个假的量。
3. **机械可查的红**: `grep -cE '^#### +TASK-014 验收判据' proposal.md` = **0** ⇒ 该小节尚不存在 ⇒ TASK-014 结构上无法开工。**这条今日就红** (已实跑 = 0), 且不预设 F 的任何形状。
   > ⚠️ **本条的第一版本身就是绿的, 当场自查抓到并换掉** —— 初稿写的是 `grep -c 'TASK-014 验收判据' proposal.md` = 0, 而本节这几段**正文自己就含这个串**, 实跑得 **2** ⇒ 它从写下的那一刻起就不可能红。换成**标题行锚定** (`^#### `) 后今日实测 0。留痕的价值在于: 这正是本 Spec 反复产出的那个形状 —— **判据与被判据的对象在同一份文档里, 描述它就满足了它** (memory `false_green_dual_is_permanent_red` 的镜像面)。
4. **⚠️ 残余的人工裁量必须诚实标注, 不得再包装成机械量**: 「落地文本是否**真的**是 F 所描述的那个形态」这一判断, 在 F 是「结构」而非「字符串」时**无法机械表达**。⇒ 该残余由 **TASK-014 的声明留痕 + TASK-019 (6) issue 正文**承担, 并**列为 owner 裁量项**写入 handoff。**诚实标注优于第五个假量。**

**spike 的验收条件 (SC-M12 钉住, 不可协商)**: 所选形态须在**五种 cwd** 下均可达 —— 主仓根 / `aria` 子模块根 / `standards` 子模块根 / `aria-orchestrator` 子模块根 / **采用方仓根 (有 `.aria/`、无 `aria/` 无 `skills/`, 插件装在仓外)**。**不可达时须 abort 而非放行**, 但 abort 不得在健康常态下发生 (否则是恒红)。

> ⚠️ **「模拟 plugin 安装态」这个措辞已作废**: 它曾被取成「cwd = marketplace 目录本身」—— 那样候选 1 直接命中, 是一个**假绿且不对称**的 fixture (对现状发红、对己方发绿)。真形态是「**cwd = 采用方仓根, 插件在仓外**」, 实测 `/home/dev/Kairos` 与 `/home/dev/SilkNode` 即此形态。第 5 种 cwd 必须按真形态搭。
>
> 本条同时是两个已被否决形态的判别器: R4-fix 的「两分支 `git rev-parse` 解析」在第 3/4/5 种下红; 「cwd 相对多候选探测为主路径」在第 5 种下红 (结构上够不到仓外)。

⛔ **不得为解析路径而 `cd`** —— 那会使 §5 的 `ls-remote` 查错仓 (主仓与 aria 子模块都有 `master`, 会 RC=0 假通过)。

### 2. 两处散文的 5 步移入折叠块, 且**去掉全部可执行命令字面量**

`<details><summary>helper 内部算法 (供理解与排障, ⛔ 不要手工执行)</summary>` … `</details>`。

- 折叠块须**补上 §3 新增的分支存在性核验步** (否则折叠块自称描述 helper 内部算法却漏掉本 change 唯一会 BLOCK 合并的那一步);
- 折叠块**不是**保护机制 —— 折叠对 AI 文本阅读无隐藏效果, 真正的保护是**去掉命令字面量**。
  ⚠️ **上一版把这条委派给 SC-M2 是误派** (post_planning R2/code-reviewer): SC-M2 的量是**输出示例**里的 `"branch": "main"` (唯一命中 `:270`), 与「可执行命令字面量」无关 —— 一个保留 `:240` 的 `aether --help | grep -q` 的实现能让 SC-M1/M2/M3a/M3b/M3c **五条全绿**而本要求被违反。⇒ 本要求改由 **SC-M1** (四行 `aether ci status`) + **SC-M15** (折叠块内可执行命令字面量计数 = 0, 覆盖 `:240` 这类非 `aether ci status` 形状) 两条共同钉住, **不再留「须人工核」的裁量腿**;
- 🔴 **折叠块之外必须留下 `<MAIN_BRANCH>` 的取值来源** (**SC-M16** 钉住)。实测 `SKILL.md:242` 是全文件**唯一**告知「本项目传 `master`」的一行, 而它属**步骤 2.5**, 正落在本节要整体折叠的 1-5 步之内。
  ⚠️ **注意 `:242` 并不满足 SC-M16 的判据** —— 它写的是 `main_branch` (小写、无尖括号), 全文件 `<MAIN_BRANCH>` 今日**零命中** ⇒ SC-M16 今日值 = **0**, 它是 baseline-failing 断言。落地要求是**两件事同时成立**: 占位符出现 (SC-M3a) + 其取值说明位于折叠块外。终态叠加 (`--main-branch` 必填 + SC-M3a 要求写占位符 + SC-M3b 禁字面值) 会让 AI 在折叠块外读到一个带占位符的必填参数, 而唯一说明取什么值的句子躺在一个自称「⛔ 不要手工执行」的块里。⇒ 折叠块外须存在 ≥1 处说明 `<MAIN_BRANCH>` 取值来源的指令。

### 3. `SKILL.md §C.2.4` 的**步骤 6 不动** (归属声明)

步骤 6 (`:252-255`) 是**纯 AI 义务**: 路由决策 + v1.65.0 / #126 两条强制 surface 警告 (helper 只输出 JSON, 不产文案), 且是 `DEC-20260731-001` 逐字记载的 owner 交换条件。

⇒ **它留在折叠块外, 保持命令式**, 本 change 不修改其语义。其 `fail` 分支**仅在既有措辞未覆盖 `raw_message` 的 surface 时**才补一句「若 `raw_message` 含 `gate_error` 诊断则一并 surface」。

> ⚠️ **本行由确定式改为条件式** (post_planning R2/tech-lead): 实读 `SKILL.md:255` 逐字已是「`fail` → BLOCK + 输出 verdict + **raw_message**, phase-c-integrator return failure」⇒ **大概率零改动**。上一版此处与 §Impact 均写确定式「补一句」, 与 `tasks.md` TASK-012 / `detailed-tasks.yaml` 的条件式 (「若既有措辞已覆盖则**不加句**, 避免 no-op 编辑」) 直接矛盾; **本版让确定式一侧改口**, 断言的量 (步骤 6 语义未变 + 折叠块外) 未动。

### 4. helper 三处 `main` 字面量去掉, 参数必填

| 落点 | 现状 | 改为 |
|---|---|---|
| `:427` CLI | `add_argument("--main-branch", default="main", help="Main branch to check (default: main)")` | `add_argument("--main-branch", required=True, help="Main branch to check (required)")` — **help 文案同批改** |
| `:300` 函数签名 | `main_branch: str = "main",` | `main_branch: str,` |
| `:21` docstring | `[--main-branch main]` | `--main-branch <MAIN_BRANCH>` |

**内部修补面 (口径必须带着读)**: 既有 **24 处** `gate_check(` 调用点全部 `TypeError`, 须逐处补 `main_branch="master"` (TASK-010)。

> **24 的三项口径**: 总体 = `tests/test_pre_merge_gate.py` **单文件** · 范围 = 该文件全部行 · 计数法 = 含 `gate_check(` 的**行数**; 其中显式传 `main_branch` 的 **0** 处。放宽总体到全 `phase-c-integrator/**/*.py` 则得 **31** 行 (去掉 `def gate_check(` 为 30) —— 多出的 6 处中 5 处是 `ci_backends/{base,github_actions}.py` 的 docstring/散文提及, 1 处是 CLI `:435` 的真实调用而它**已显式传** `main_branch=args.main_branch`, D5 下不会 TypeError。**不写明口径, 下一个复核者会数出 30/31 并以为本 Spec 错了。**
>
> ⚠️ **这 24 处全部在本 skill 自己的测试文件内, 故它不构成对外破坏面** —— MAJOR 的承重腿见 §版本, 不在这里。

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

**⚠️ 上表只框到了「pattern 语义」这一层, 底下还有更基础的两条 (2026-08-10 受控裸仓实跑, 六轮审计从未浮出)**:

- 🔴 **`ls-remote` 零命中亦返 `rc=0`** —— 受控裸仓 (远端只有 `refs/heads/master`) 传 `refs/heads/wibble` ⇒ **rc=0 + 零行输出**。
  ⇒ **判据必须落在解析出的 ref 名列表上, 不得读退出码判存在性**。任何以退出码判存在性的实现, 对「分支不存在」这个**本 Spec 的主场景**天然 fail-OPEN —— 而这正是本 change 要治的病。
- 🔴 ⛔ **不得使用 `--exit-code`** —— 实测它使「无命中」返 **rc=2**。那是实现者最可能选的「更简单」替代路径, 但下表以「其余一切非零退出码 → `main-branch-verify-failed`」收口 ⇒ **一个合法缺失的分支会被误分类成「查询失败」而非「分支不存在」**。
  该禁令由 **TASK-003 / TASK-008 的零命中用例**钉住 (受控裸仓 + `--main-branch develop` ⇒ 须得 `kind=="main-branch-not-found"`); 现有 SC-M6 / SC-M13 两个场景**都有命中**, 结构上碰不到这条分支, 故不能靠它们代管。

| 情形 | 判据 | 输出 | 重试? |
|---|---|---|---|
| ref 列表含**精确匹配** | — | 继续原流程 | — |
| ref 列表**取到了但无精确匹配** | 分支不存在 | `verdict=fail` + `gate_error.kind="main-branch-not-found"` | **否** |
| subprocess timeout (`TimeoutExpired`) | 查询失败 | 按 `SKILL.md:259` 既有规范重试; 仍超时 ⇒ `fail` + `kind="main-branch-verify-failed"` | **是** |
| **其余一切** — 非零退出码 (实测 remote 名不存在 / 坏 URL / 网络不可达均为 **128**, 用法错误 129) · `FileNotFoundError` (git 二进制缺失, **抛异常无退出码**) · `OSError` · 输出不可解析 · **任何未枚举情形** | 查询失败 | `verdict=fail` + `kind="main-branch-verify-failed"` | **否** |

> **本表以「其余一切」收口 (catch-all), 不是正向枚举** —— 正向枚举对未来新增返回码天然 fail-OPEN。**不援引 `SKILL.md:260` 的 exit 1-126**: 实测真实失败码是 128, 在区间外; 且 `:260` 自带 `127 → no_ci_fallback` 会使 verdict 变 green。
>
> **复用是按轴分派的两个先例, 不是三选一** (2026-08-10 对抗复核更正 —— 把 A/B/C 框成单选是误框):
>
> | 轴 | 成文先例 | 可复用的是什么 |
> |---|---|---|
> | **异常** | `path_coverage.py:93` 的 `(TimeoutExpired, FileNotFoundError, OSError)` 三元组 | **那条元组的枚举**。⛔ **不是** `_run_git()` 函数本身 —— 它 docstring 明写「Never raises」, 把异常路径 (`:93-94`) 与非零退出码 (`:99-100`) **双双折叠成 `ok=False`** ⇒ SC-M7 (128, 不重试) 与 SC-M8 (timeout, 重试 3 次) 在其返回形状上**无从分辨**; 且撞 §非目标「不改 `path_coverage.py`」 |
> | **重试** | `ci_backends/aether.py:38` `RETRY_BACKOFF=(5,15,45)` / `MAX_RETRY_ATTEMPTS`, `:164-187` `_run_with_retry` | **重试循环本身**。它的参数**正是 `SKILL.md:259` 逐字规定的那套**, 复用它是唯一不造第二套语义的路径 |
>
> **形态已裁 (D-4)**: `ci_backends/aether.py` **入 scope** —— 抽 `_run_with_retry` (`:164-187`) 的重试循环为与 binary/argv 无关的共享 helper, `AetherBackend._run_with_retry` 改薄包装; gate 层调同一个 helper。**但下列四条使「薄包装 + 字节等价」这个说法低估了改动面, 必须一并规定**:
>
> 1. 🔴 **`_run_with_retry` 结构上交付不出本节的 catch-all**: `:168` docstring 逐字「other exceptions bubble up」, `:180` 只 `except TimeoutExpired`。而上表兜底行要求 `FileNotFoundError` / `OSError` / 输出不可解析 / **任何未枚举情形**一律 `fail`。⇒ **gate 层仍必须自建异常包裹层** (用异常轴那条元组), 重试 helper 不代管这一层。
> 2. 🔴 **解码轴此前完全没被考虑**: `aether.py:176` 用 `text=True`; 而 gate 要跑的恰是 `git ls-remote` —— git **不保证** ref 名是合法 UTF-8, `text=True` 的严格解码会抛 `UnicodeDecodeError`, 它**不是** `TimeoutExpired` ⇒ 不被捕 ⇒ **违反本节兜底行**。同包 `path_coverage.py:78-84` 正是为此写 bytes + `surrogateescape` (#124 教训, docstring 逐字记载)。⇒ 共享 helper 至少要多出 **decode 策略** 与 **timeout** 两个参数。
> 3. **`cwd` 是承重不变量而 `_run_with_retry` 没有该参数** (`_run_git` 有): D3 + 本节「同一个 cwd」使「`ls-remote` 跑在哪个仓」承重 —— 主仓与 `aria` 子模块**都有 `master`**, 查错仓即假通过。⇒ 共享 helper 须显式接 `cwd`。
> 4. **超时哨兵 `return -1` (`:187`) 与信号致死的 `-1` (SIGHUP) 别名**, 而 D7 要求 gate「退出码分区自带完整表」⇒ gate 层不得直接把 helper 的 `-1` 当退出码读, 须有可区分的 timeout 信号。
>
> 🔴 **等价判据不能用「`test_ci_backends.py` 25 tests 保持全绿」** —— 实测 `grep -c '_run_with_retry' tests/test_ci_backends.py` = **0**, 那 25 条**系统性绕过**它 (改 mock `subprocess.run` 或 `_query`), 其**异常选择行为零覆盖**。抽取时若把 `except TimeoutExpired` 放宽成三元组 (为服务 gate 的 catch-all, 这是最自然的写法), 会**静默改掉 aether 的异常契约而 25 条全绿** ⇒ 该判据恒绿。
> ⇒ **等价判据换量**: 须新建**直接针对 `_run_with_retry` 的用例**, 至少钉住 (a) **只有** `TimeoutExpired` 触发重试、其余异常照旧 bubble up (放宽成三元组时该用例必红); (b) backoff 序列 `5/15/45` 与 3 attempts (须 mock `time.sleep`); (c) 超时哨兵与真实退出码可区分。25 tests 全绿降为**必要不充分**条件。

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

⚠️ **本节只管本 change 新增的存在性核验这一个插入点。TASK-020 的 legacy-key fail-CLOSED 是位置不同的另一个插入点, 见 §6.1 —— 两节不得互相援引。**

### 6.1 TASK-020 的 legacy-key fail-CLOSED 插入点 (post_planning R2 唯一 Critical 的闭合)

```
:325 _normalize_config()      ⛔ 不得放这里 — 它是 gate_check 的第一条可执行语句, 在 enabled 早退之前
:328 enabled=false          → 早退 (green)
★ legacy-key 硬失败 (TASK-020 新增)          ← 唯一合法插入点
:337 resolve_ci_backend(cfg)                  [消费 ci_backends ← 旧键 primitive_preference 的新键]
:338 no backend → _no_ci_output(cfg["no_ci_fallback"])  [消费 no_ci_fallback ← 旧键 no_aether_fallback 的新键]
:345 precheck 失败          → 早退 (fail)
★ 存在性核验 (§6, 本 change 的另一处新增)
```

**在 `enabled` 早退之后**: `enabled` **不是**别名键 (`_OLD_TO_NEW` 实读只有 `primitive_preference` / `no_aether_fallback` 两个) ⇒ 读它不依赖任何翻译; 且 owner 显式关闭的闸门不得因一个已不再被消费的陈旧键而 BLOCK —— 与 D9/§6/**SC-M10** 是同一条理由, 本节与它们**同向**。
**在 `resolve_ci_backend` 之前**: 旧键所**承载的意图**, 其首个消费者分别在 `:337` (`ci_backends` ← `primitive_preference`) 与 `:339` (`no_ci_fallback` ← `no_aether_fallback`)。若把硬失败推到三早退**之后** (与存在性核验同点), 一个设了 `no_aether_fallback: "abort"` 又恰好无可用 backend 的采用方, 会**先**在 `:339` 用 **DEFAULT 的 `skip_with_warning`** 静默降级放行, 硬失败根本没机会触发 —— **正是 TASK-020 要治的那条 fail-OPEN 原样复发** (memory `fix-recurs-in-fallback`)。

> ⚠️ **上一版此处的承重理由是错的, 本版更正** (post_planning R3/tech-lead, 编排层复跑坐实): 上一版逐字写「**两个别名键**的首个消费者分别在 `:337` 与 `:339`」。实读 `:337` 是 `resolve_ci_backend(cfg)`、`:339` 是 `_no_ci_output(cfg["no_ci_fallback"])` —— 它们消费的是**翻译后的新键**, **从不接触旧键名**。**旧键名本身的首个消费者是 `:325` 的 `_normalize_config`。** 理由说错了, 但结论 (插入点在 `:337` 之前) 不变 —— 变的是它下面必须再加一条规定, 见下。

🔴 **判定的输入必须是未归一化的原始 `config` 入参, 不是 `cfg`** (承重, 与位置同等级):

实读 `_normalize_config`: `:101 out = dict(config)` / `:111 del out[old]` / `:120 out[new] = _translate_value(old, out.pop(old))` / `:121 return out` ⇒ 它在返回前就把**旧键名** `del`/`pop` 掉; 而 `:325 user_normalized = _normalize_config(config or {})` / `:326 cfg = {**DEFAULT_CONFIG, **user_normalized}`。

⇒ **在被本节钉死的插入点上 (`:328` 之后 / `:337` 之前), 手边的 `cfg` 结构上不含任何旧键名。** 只规定位置而不规定判定输入, 则「读 `cfg` 判 legacy key 是否在场」——**该位置最自然的写法**——对用例 (ii) 必红 (旧键永不命中 ⇒ 不触发硬失败 ⇒ 照常走到 `:339` 用翻译后的 `skip_with_warning` 放行, `verdict ≠ fail`)。

⇒ 条款: **fail-CLOSED 的存在性判定读 `gate_check()` 的原始 `config` 形参** (或任何在 `_normalize_config` 之前捕获的旧键名快照), **不得读 `cfg` / `user_normalized`**。⚠️ 这不改变**插入点位置** —— 判定**发生**在 `:328` 之后 / `:337` 之前, 只是它**读**的那份 dict 来自 `:325` 之前。两者是正交的两条规定, 上一版只写了前一条。

⇒ 该插入点由三条用例**唯一确定** (缺任一条, 两个独立实施者即可得相反结果 —— 这正是 R2 判 Critical 的形状):

| 输入 | 期望 | 排除掉的错实现 |
|---|---|---|
| `enabled=false` + 任一 legacy key | `green` + 六键不变 + 无 `gate_error` (= **SC-M10 的交叉输入变体**) | 放进 `_normalize_config` 或 `enabled` 早退之前 |
| `enabled=true` + `no_aether_fallback` + 无可用 backend | `fail` + `raw_message` 点名旧键 | 放到三早退之后 |
| `enabled=true` + 任一 legacy key + backend 正常 | `fail` + `raw_message` | 完全没实现 |

**信号通道 (承重, 不得偏离)**: 硬失败**必须**产出 `verdict="fail"` + `raw_message` 的正常六键输出, 由 `main()` 正常 `print` 后退出; **不得**以未捕获异常穿过 `gate_check()` / `main()`。理由实读: `:325` 前后与 `main()` 对 `gate_check()` 的调用**均无 `try/except`**, `if __name__ == "__main__": sys.exit(main())` 外再无兜底 ⇒ 裸 `raise` 会让进程崩溃、stdout 无 JSON、`verdict` 从未被构造; 而 `workflow-runner/SKILL.md:354-357` 的 verdict 路由只有四条臂 (green / fail / timeout / Ctrl-C), **无异常臂**, `gate_error` 全仓零消费者。
⇒ **验收必须含一条走 CLI 真实路径的用例** (`main()` 或 `python3 pre_merge_gate.py …`), 断言 stdout 是可解析 JSON 且 `verdict == "fail"`。**只在 `_normalize_config` 上做 `assertRaises` 的单元断言不满足本条** —— 那种写法会让这个 Critical 在 CI 里保持沉默, 只在真实采用方跑 CLI 时以 traceback 现形 (post_planning R2/backend-architect)。

> **与 §非目标「不动 `no_ci_fallback` 既有降级语义」的关系**: 本插入点只对**含旧键名**的 config 触发。v2.0 后旧键已不是合法键, 而只用新键 `no_ci_fallback` 的 config 到达 `:339` 的路径与语义**零改变**。

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
| **D2** | 具体路径解析形态**降级为 TASK-002 spike** (R5 后, 见 §1) | Spec 只钉 **SC-M12** (五种 cwd 全可达, 不可达即 abort) 与 **D3** (不得为解析路径而 `cd`)。⚠️ 上一版逐字写「两分支解析 + 不可达即 abort, 不用环境变量」, 与 §1 已降级的结论**直接矛盾**, 且其论据「`ARIA_PLUGIN_ROOT` 全仓未赋值」已被 §1 判为测错总体 |
| **D3** | ⛔ 不得为解析路径而 `cd` | 会使核验查错仓 (两仓都有 `master` ⇒ 假通过) |
| **D4** | 步骤 6 **留折叠块外不动** | 纯 AI 义务 + `DEC-20260731-001` owner 交换条件 |
| **D5** | helper 三处字面量去掉 + 参数必填 | 只改 CLI 会留函数签名这条内部路径恒绿 |
| **D6** | 存在性核验对**返回的 ref 名做精确字符串比对**, 不依赖 `ls-remote` 的 pattern 语义, 且**不得读退出码** | 裸分支名是尾段 glob; 而**锚定也关不掉 glob** —— 受控裸仓实测 `refs/heads/mast*` / `refs/heads/m[a]ster` / `refs/heads/maste?` 仍**全部命中**。另: 零命中亦返 rc=0 (§5)。⚠️ 上一版写「锚定 `refs/heads/<name>`」, 已被该实验推翻 |
| **D7** | 退出码分区**自带完整表**, 不援引 `:260` | 实测失败码是 128, 在 1-126 之外; 且 `:260` 的 127 分支会变 green |
| **D8** | `verdict` 三态封闭; **`raw_message` 为诊断主通道**, `gate_error` 为 additive 副本 | 第四枚举值四处无人认识; `gate_error` 目前无消费者 |
| **D9** | 核验点在三早退之后、path coverage 之前 | 之前会改 owner 关闭闸门的语义; 之后会放行未核验的使用 |
| **D10** | Rule #6 落**第二行「照跑 AB, 零裁量」** | SOT 直接管辖条款, 见 §Rule #6 |
| **D11** | Level **3**; 版本 **MAJOR** | Level 由判据表输出栏直接管辖; 版本由 CLAUDE.md:35「破坏性变更须 MAJOR」与 :79「MINOR+」两条**下界求交**, 唯一解 MAJOR (见 §版本)。⚠️ 上一版写「版本**地板 MINOR**」, 与抬头及 §版本 的 MAJOR 自相矛盾, 且「地板」措辞给下游留了看似合规的违规口 |

---

## Success Criteria

> **每条 grep 断言的 pattern 与今日计数均已实跑**, 输出见下表「今日实测」列。SC-M1..SC-M5 零裁量。

| SC | 断言 (逐字可复跑) | 期望 | 今日实测 | 怎么会红 |
|----|------|------|------|---------|
| **SC-M1** | `grep -c 'aether ci status' aria/skills/phase-c-integrator/SKILL.md` | **0** | **4** | 必红。**一条断言覆盖 `:167`/`:168`/`:243`/`:244` 全部四行** |
| **SC-M2** | `grep -c '"branch": "main"' .../SKILL.md` | **0** | **1** | 必红 (`:270`) |
| **SC-M3a** | `grep -c -- '--main-branch "<MAIN_BRANCH>"' .../SKILL.md` | **2** | **0** | 必红 —— **D1 承重红窗**。断言的是**占位符形态**, 两处散文各一条 |
| **SC-M3b** | `grep -cE -- "--main-branch +['\"]?(main\|master)['\"]?([[:space:]]\|$)" .../SKILL.md` | **0** | **0** | **负控**: 写死字面值 (**裸的与带引号的都算**) 的实现在此必红。⚠️ **本条是 PC1 的修复** —— 上一版只断言 `--pr-branch` 存在, 而 `--main-branch main` 写死能通过全部断言 (实测 0/0/2 全过)。**断言的量必须是病灶所在的量**。<br>⚠️ **本版扩了拒绝域** (post_planning R2/code-reviewer): 上一版 pattern 不含引号 ⇒ 额外写一条 `--main-branch "master"` 示例可从中逃逸, 而本行的声称是「写死字面值必红」—— **声称强于拒绝域**。已实测: 新 pattern 今日仍 **0** (拒绝域扩大但今日值不变), 且对合成串 `--main-branch "master"` / `--main-branch master` 各命中 1、对 `--main-branch "<MAIN_BRANCH>"` 零命中 |
| **SC-M3c** | 提取 `<details>…</details>` 全部折叠块, 统计其中含 `--pr-branch` 的块数 | **0** | **0** ⚠️**空真** | **负控**: 把调用藏进折叠块的实现在此必红。⚠️ 修复 code-reviewer 指出的第二个失明面 —— SC-M1/M3a 都是**全文件计数, 无位置维度**, 而病灶逐字是「AI 走散文那份」, **位置就是病灶所在的量**。<br>⚠️ **今日的 0 是空真, 不得当正面证据读**: 实测 `SKILL.md` 内 `<details>` 块数 = **0**, 「含 `--pr-branch` 的块数 = 0」是因为**根本没有块**, 不是因为调用在块外。本条今日的信息量全部来自 :204 已验过的**拒绝能力**; 要等 TASK-011 建出折叠块后它才开始有正面信息量 |

> **SC-M3a/b/c 已做对抗性验证** (不只验当前值): 构造「好实现 (占位符+调用在折叠块外)」「坏实现 A (写死 `--main-branch main`)」「坏实现 B (调用藏进折叠块)」三个 fixture 实跑 —— 好实现全过, **两个坏实现各被 M3b / M3c 拒绝**。
| **SC-M4** | `grep -c 'default="main"' .../pre_merge_gate.py` / `grep -c 'main_branch: str = "main"' ...` / `grep -c -- '--main-branch main' ...` | **0 / 0 / 0** | **1 / 1 / 1** | 必红 |
| **SC-M5** | `grep -c 'default: main' .../pre_merge_gate.py` (help 文案) | **0** | **1** | 必红 |
| **SC-M6** | 受控裸仓: 远端只有 `refs/heads/wip/master`, 传 `--main-branch master` | `verdict=fail` + `kind=="main-branch-not-found"` + **`raw_message`** 含分支名与 remote 名 | — | 今日无核验 ⇒ green ⇒ 必红。**承重断言 (D6)**。**用真实 `ls-remote`, 不打桩** |
| **SC-M7** | `ls-remote` 返回 **128** (mock 或指向不存在的 remote 名) | `fail` + `kind=="main-branch-verify-failed"`, **未重试** | — | 当「不存在」→ 误报 / 当「存在」→ 恒绿, 两向都红 |
| **SC-M8** | `ls-remote` 抛 `TimeoutExpired` (**mock**; 须 mock `time.sleep`) | 3 attempts 后 `fail` + `kind=="main-branch-verify-failed"` | — | 未按 `:259` 重试的实现红; 未 mock sleep 致 >60s 亦红 |
| **SC-M9** | `gate_check(pr_branch=...)` 不传 `main_branch` | `TypeError` | — | 现状签名有缺省 ⇒ 静默成功 ⇒ 必红。**唯一覆盖内部调用路径**。(本 skill 的函数名是 `gate_check`; `run_gate` 属 `state-scanner/phase1_gate.py`) |
| **SC-M10** | 负控: `enabled=false` 早退。**两个 fixture 变体, 缺一不可**: (a) 干净 config; (b) **含任一 legacy key 的 config** (交叉输入) | 六键不变、无 `gate_error`, **且 `assert ls-remote 未被调用`** | — | 缺后半条因果断言则健康与不健康实现都绿 (D9 守不住)。⚠️ **变体 (b) 是本版新增** (post_planning R2 Critical): 上一版 fixture 不含 legacy key ⇒ 整套断言对「TASK-020 的硬失败被放进 `_normalize_config`」这个交叉输入**失明**, 而受影响的正是 TASK-020 点名要保护的人群里 `enabled=false` 的那部分 (他们的每次合并被 BLOCK)。插入点规定见 **§6.1** |
| **SC-M11** | 负控: 分支存在且有 in-flight | `verdict=wait` 不变 | — | 核验不得改变正常路径判决 |
| **SC-M12** | **参数化五种 cwd** 跑 §1 的调用: 主仓根 / `aria` 子模块根 / `standards` 子模块根 / `aria-orchestrator` 子模块根 / **采用方仓根 (有 `.aria/`、无 `aria/` 无 `skills/`, 插件装在仓外)** | **五种全部可达并正常执行** (非 `No such file`) | — | **两个已被否决形态的判别器**: 「两分支 `git rev-parse` 解析」在第 3/4/5 种下红 (R5 四席实测); 「cwd 相对多候选探测为主路径」在第 5 种下红 (结构上够不到仓外)。⚠️ 上一版只测一种 cwd, 对该失效**恒绿**; 且上一版的「模拟 plugin 安装态」曾被取成 cwd = marketplace 目录本身 —— 那让候选 1 直接命中, 是**假绿且不对称的 fixture**, 已作废。第 5 种须按真形态搭 (实测 `/home/dev/Kairos` `/home/dev/SilkNode` 即此形态) |
| **SC-M13** | 受控裸仓: 远端只有 `refs/heads/master`, 传 `--main-branch 'mast*'` (及 `m[a]ster` / `maste?`) | `verdict=fail` + `kind=="main-branch-not-found"` | — | **锚定 pattern 实现必红** —— 实测这三个 pattern 对该远端全返 RC=0。**本条钉住「精确比对」而非「锚定」, 是 R2 承重 Critical 的真正闭合腿** |
| **SC-M14** | 共享重试 helper 的 `subprocess` 抛 `UnicodeDecodeError` (**mock**) | `fail` + `kind=="main-branch-verify-failed"`, **未重试**, 且异常不逸出 `gate_check()` | — | 照搬 `aether.py:176` 的 `text=True` 而不换 decode 策略的实现在此必红 —— 它不是 `TimeoutExpired`, 不被 `:180` 捕获 ⇒ 裸抛穿过 gate。⚠️ **本条是给 §5 catch-all 里唯一无编号的那一支补编号** (post_planning R2/qa-engineer): 无编号的行为要求不会被任何机械勾稽点找到, 只能靠人工读散文 |
| **SC-M15** | 提取 `<details>…</details>` 全部折叠块, 统计块内**可执行命令字面量**行数 (pattern = 行内 code 或 fenced code 中以 `aether ` / `git ` / `python3 ` / `bash ` 起头的串) | **0** | **0** ⚠️**空真** (今日 `<details>` 块数 = 0) | 保留 `:240` 的 `aether --help \| grep -q`、或任何非 `aether ci status` 形状可执行字面量的实现在此必红。**它是 §2「去掉全部可执行命令字面量」的机械腿** —— R2/code-reviewer 构造的逃逸实现 (SC-M1/M2/M3a/M3b/M3c 五条全绿而要求被违反) 在此被拒。<br>⚠️ 与 SC-M3c 同为空真, **今日的 0 不得当正面证据**, 要等 TASK-011 建出折叠块后才有正面信息量 |
| **SC-M16** | 折叠块**之外**存在 ≥1 处说明 `<MAIN_BRANCH>` 取值来源的指令 (判据: 同时含 `<MAIN_BRANCH>` 与「本项目」或 `master` 的段落, 且该段落不在任何 `<details>` 块内) | **≥1** | **0** | **必红** —— 它是 **baseline-failing 断言, 不是守恒断言**。今日 `SKILL.md` 全文件 `<MAIN_BRANCH>` **零命中** (`grep -c -- '<MAIN_BRANCH>' SKILL.md` → **0**), 故满足判据的段落数今日必为 0。转绿路径: SC-M3a 使 `<MAIN_BRANCH>` 占位符出现 (TASK-011), **且**其取值说明被留在折叠块外。<br>⚠️ **红窗已并入 TASK-001** |
| **SC-M17** | `grep -cE 'still (readable\|works)\|removed in v2\.0\|仍读\|v2\.0 移除' aria/skills/config-loader/SKILL.md` | **0** | **2** (`:249` `:257`) | 必红。**双重身份**: (a) TASK-020 删除面在 `config-loader` 这个**另一个 skill** 上的机械腿; (b) Rule #6 判据表第三行要求的「**可证伪定向 fixture**」—— 该 skill 全无 AB 套件 (实跑 `ls ab-suite/ \| grep -i config` = 空), 见 §Rule #6 |
| **SC-M18** | 同一条承诺措辞 pattern 跑在删除面**其余四个文件**上: `grep -cE 'still (readable\|works)\|removed in v2\.0\|仍读\|v2\.0 移除' <f>`, `<f>` ∈ {`.../scripts/pre_merge_gate.py`, `.../phase-c-integrator/SKILL.md`, `.../tests/test_pre_merge_gate.py`, `.aria/config.template.json`} | **0 / 0 / 0 / 0** | **2 / 4 / 3 / 0** | 必红 (前三个)。⚠️ **本条是 post_planning R3/backend-architect 的闭合**: 上一版**只有 `config-loader` 一个文件**被提升为机械 SC (SC-M17), 其余四个文件只有散文描述今日计数、**无任何 `→0` 的断言** ⇒ 存在一个能通过 SC-M10/SC-M17/三条插入点 fixture/CLI 真实路径用例/TASK-021 终局复核**全部检查**、而 `pre_merge_gate.py:68`/`:116` 的 `will be removed in v2.0` **原样留在已发布的 v2.0.0 里**的实现。<br>⚠️ `.aria/config.template.json` 今日已是 0 (它只有键名面 `:75` `:78`, 无承诺措辞) ⇒ 该分量是**负控**, 守的是「TASK-020 不得往模板里补写承诺措辞」; 其**键名面**归零由 TASK-020 的中英并列枚举口径管辖, 不并入本 SC |

**打桩边界 (前一版自相矛盾, 本版钉死)**: **SC-M6 与 SC-M13 用真实 `ls-remote` + 受控裸仓**, §5 的**零命中用例** (`--main-branch develop`) 同属这一档。**SC-M8 必须 mock** —— 真实 `ls-remote` 无法产出确定性 timeout。**SC-M14 必须 mock** —— 靠真实环境构造非法 UTF-8 的 git ref 名依赖 git 版本/文件系统细节, 不确定性高且与本 Spec「不得用依赖环境可达性的手段」自相矛盾 (⚠️ 本句是 post_planning R3/qa-engineer 的闭合: SC-M14 是 R2-fix 新增的 SC, 其自身表格行虽写了 `(mock)` 括注, 但本段自称是打桩边界的**唯一权威入口**却漏了它)。**SC-M7 两种手段皆可**: 「指向不存在的 remote 名」经受控实验实测**确定性返 128** (非 mock 亦可复现), 或直接 mock; 唯**不得**用依赖网络可达性的手段。

> ⚠️ 上一版此段有**两处**自相矛盾, 本版一并更正: (a) 逐字写「**只有 SC-M6** 用真实 `ls-remote`」, 而 SC-M13 自身的定义 (见上表) 逐字就是「受控裸仓」; (b) 逐字写「SC-M7 **必须** mock (真实 `ls-remote` 无法产出确定性 128)」, 而 SC-M7 自身的定义允许「指向不存在的 remote 名」这一**非 mock** 手段, 且受控实验证明它确实确定性返 128。
> **两处改的都是陈旧的摘要一侧 —— SC-M7 断言的量 (128 ⇒ `fail` + `verify-failed` + 未重试) 未动。**

**测试隔离 (R4/QC4)**: `test_sc22_no_real_git_subprocess_in_suite` (`:710`) 的 patch **本就全局生效** (`import subprocess` 使模块对象共享 —— 受控实验证实, 前一版的相反陈述已作废)。⇒ D5 落地后既有 ~24 处调用会**击穿该基线使其转红**。`tasks.md` 须含一条前置任务: 为既有调用补 `main_branch="master"` **并**为 gate 层核验建独立打桩接缝, 使 `test_sc22` 保持有效而非被放宽。

---

## Rule #6

`rule6_note`: **判据表第二行 —— 处方性 · 运行时指令面 ⇒ 照跑 AB, 零裁量。不申请任何豁免。** SOT: `standards/conventions/skill-benchmark-exemption.md`。

**定档依据 (直接管辖条款)**: SOT「SKILL.md 有变动时的附加约束」段逐字 —— **「`description` 或指令流程变动 ⇒ 一律第二行」**。D1 是指令流程变动, 无需也不得再讨论「套件测不测得到」。

> SOT 对第三行的措辞是「**典型**: authoring 向导」—— authoring 是**举例不是定义**, 真实判据是「覆盖范围外」。本 Spec 不走第三行, 此处仅避免把举例当规则复用。

⇒ ship 前须过 `ab-suite/phase-c-integrator.json` 与 `ab-suite/phase-c-integrator-pre-merge-gate.json`, 结果存 `ab-results/`。**已知**: 两套件对 C.2.4 覆盖薄 (承 aria-plugin #127), 本 Spec **不以此降档**, 且诚实声明**D1 的行为证据主要由 SC-M1 / SC-M3a-c / SC-M12 承担**, AB 是合规义务而非本 change 的主要证据来源。

#### `config-loader` 这个 skill 的 Rule #6 归档 (post_planning R2/tech-lead 指出的覆盖缺口)

TASK-020 的删除面含 **`aria/skills/config-loader/SKILL.md:249` `:257`** —— 那是**另一个 skill**, 本轮新入 scope, 而**它全无 AB 套件** (实跑 `ls aria-plugin-benchmarks/ab-suite/ | grep -i config` → 空)。上一版对它**无 `rule6_note` / 无 substitute SC / 无套件缺口 issue**, 三样全无。

`rule6_note` (config-loader): **判据表第三行 —— 处方性 · 套件覆盖外**。「照跑」在这里**结构上不可能** (被照跑的对象不存在), 故走 SOT 为该行规定的三件套, **三样全给**:

1. **点名行为**: 本 change 对该文件的改动仅限「两行 legacy key 别名的 v2.0 到期措辞随代码同批删除」, **不触碰该 skill 的任何运行时指令流程、不改 `description`**;
2. **可证伪定向 fixture**: **SC-M17** (今日 2 → 期望 0, baseline-failing);
3. **套件缺口开 issue**: TASK-019 第 **(8)** 项。

> ⚠️ **Rule #10 留痕**: 这是 AI 作出的判据行归属判断, **须写入 handoff 请复议**。若复议认为该改动属第二行, 则须先建 `config-loader` 的 AB 套件再跑 —— **不得**以「改动小 / 1:1 派生」为由跳过 (CLAUDE.md 规则 #10 明列的四类白名单不含这些)。
> ⚠️ `phase-c-integrator` 那两套件**不受本段影响, 原样照跑第二行零裁量**。

---

## 非目标

- **不引入** `main_branch` 自动解析 —— R2 实测 `ls-remote --symref` 存在 RC=0 但无 `ref:` 行两态 (unborn / detached), 需独立设计。必填 + 存在性核验已足以关闭本 Spec 的失效模式;
- **不改** `path_coverage.py` 代码与行为;
- **不改** `aether` CLI 返回语义;
- **不改** `branch-manager` 合并动作 (aria-plugin #136);
- **不改** `workflow-runner` 的 `gate_state` schema;
- **不改** `SKILL.md` 步骤 6 的语义 (D4);
- **不动** `no_ci_fallback` / stub backend 既有降级语义 —— `enabled=false` 那条由 **SC-M10** 机械钉住; `:338` no-backend 与 `:345` precheck 失败**两条不在 SC-M10 覆盖内**, 由 **TASK-008 的两条专用用例**钉住, **且那两条用例须各带同款因果断言 `assert ls-remote 未被调用`** (⚠️ 上一版只要求「各有一条用例」—— 少了因果断言则: 把核验错插在 `:338`/`:345` **之前**的实现, 只要 fixture 的 `main_branch` 恰好指向真实存在的分支 (最省事的写法), 就会静默跑一次 `ls-remote` 再照常早退, 返回六键与健康实现完全相同 ⇒ 测试全绿而 D9 对这两条分支从未被验证; post_planning R2/qa-engineer)。⚠️ 上一版此行还让 SC-M10 一条代管三条早退, `detailed-tasks.yaml` 已记录该缺口而正文未回写, 本版一并补齐;
  ⚠️ **TASK-020 的 legacy-key 硬失败是本条的例外面, 但只对含旧键名的 config 生效** —— 它在 `:337` **之前**触发 (§6.1), 而只用新键 `no_ci_fallback` 的 config 到达 `:339` 的路径与语义**零改变**;
- **不修**同形兄弟位置 —— `phase-d-closer/fetch_gate.py` 的字面 `("master","main")` 回落 · `state-scanner/lib/worktree_manager.py:170` 的 `base_branch: str = "master"` (与 `pre_merge_gate.py:300` 完全同形)。⚠️ **Phase B 实施者不得照抄 `fetch_gate.py`**。开 follow-up。

---

## Impact

| 文件 | 变更 |
|------|------|
| `aria/skills/phase-c-integrator/SKILL.md` | **两处**散文流程重整 (`### 步骤执行` :99 段 + `### C.2.4` :218 段) · 四行裸命令去除 · `:270` 示例 · `:267` schema 增 `gate_error` · `:279` 四类早退注记同步 · 步骤 6 的 `fail` 分支**条件式**补句 (既有措辞已覆盖则零改动, 见 §3) · **TASK-020 删除面 `:48` `:49` `:285` `:286` `:349` `:350` `:351`** (7 行; ⚠️ 早前清单只列 6 行, 漏 `:349` —— 那行逐字是「Legacy alias (auto-translated + DeprecationWarning, removed in v2.0):」; ⚠️ **这 7 个行号以 `af87cae` 为准, TASK-011 落地后 `:285+` 必然位移 —— 一律按内容锚重定位, 不得按行号核**) · `:262`/`:559` 定位约定 (TASK-014) |
| `.../scripts/pre_merge_gate.py` | `:21` `:300` `:427` + help 文案 · `--remote` / `remote` 参数 · `_verify_branch_exists()` · `raw_message` 诊断 + `gate_error` additive 键 · 核验点插入 · **TASK-020: `_OLD_TO_NEW` (`:68-72`) 与 `:79` `:82` `:85` `:89` `:108` `:116` 的软弃用路径** |
| **`.../scripts/ci_backends/aether.py`** | **新入 scope (D-4, 2026-08-10 裁定)** —— 抽 `_run_with_retry` (`:164-187`) 的重试循环为与 binary/argv 无关的共享 helper; 自身改**薄包装**保持行为等价 |
| `.../tests/test_ci_backends.py` | **须新增**针对 `_run_with_retry` **本身**的直接用例 —— 实测 `grep -c '_run_with_retry'` = **0**, 现有 25 条系统性绕过它, 其异常选择行为零覆盖 ⇒ 「25 tests 全绿」是**恒绿判据**, 只能当必要不充分条件 |
| `.../tests/test_pre_merge_gate.py` | SC-M1..**SC-M18** 中落在本文件的那些 (SC-M17 落 `config-loader/SKILL.md`, 由 TASK-020 承; SC-M18 跨四个文件); 既有 **24 处**调用补 `main_branch="master"` (口径见 §4); `test_sc12` (`:663`) 断言改 `"master"`; **为 gate 层核验建独立打桩接缝**; **TASK-020: 三个 `test_old_key_*` (`:407` `:421` `:433`) 由「断言翻译成功 + DeprecationWarning」改为断言硬失败**。⚠️ **`test_sc22` (`:710-724`) 的守卫函数体, 除其 `gate_check(` 调用行补必填实参外零改动** (见 TASK-005) |
| `aria/skills/config-loader/SKILL.md` | **TASK-020 删除面** —— `:249` `:257` 两处「alias still works, emits DeprecationWarning, removed in v2.0」措辞随 v2.0 到期同批改。⚠️ 该文件属**另一个 skill**, 上一版 Impact 表未提 |
| 🔴 **`.aria/config.template.json` (主仓)** | **TASK-020 删除面, 且在另一个仓** —— `:75` `primitive_preference` / `:78` `no_aether_fallback` 两个 legacy key。它是 CLAUDE.md 指定的**采用方复制源**; 本仓 live `.aria/config.json` 实测 legacy 命中 **0** ⇒ **受影响的是采用方不是本仓**。⚠️ 上一版 Impact 表完全未提该文件, 也未声明本 change 的落点跨两个仓 |
| **`CLAUDE.md`** | 规则 #8 那段须同步 —— 本 Spec 给 pre-merge gate **新增第三条阻断腿**。先例: v1.31.0 CI backend 抽象化在同一提交同步过 Rule #8 (`commit 7661e96`) |
| `openspec/changes/.../tasks.md` + `detailed-tasks.yaml` | **新建** (Level 3) —— 承载 **组 0 TDD 前置 / 组 1 实现 / 组 2 SKILL.md / 组 3 合规与同步面 / 组 4 follow-up** 五组共 **21** 条任务 (⚠️ 本版新增 **TASK-021 终局全量收口** —— 上一版唯一一次「重跑全量套件」挂在拓扑 L4 的 TASK-008 上, 其后仍有 4 条任务改被测文件, 全清单无终局收口, post_planning R2/code-reviewer `blocks_phase_b`)。⚠️ 上一版此行写「9 条阻塞项」(不可核的陈旧数, 已删), 且两文件曾 19 checkbox vs 20 task **不同步** (TASK-020 只在 yaml), 本版补齐 |
| AB | `phase-c-integrator` 两套件照跑 (第二行零裁量), 结果存 **`aria-plugin-benchmarks/ab-results/`** (主仓 tracked 目录, 已补入 `scope_repos[Aria].paths` —— ⚠️ 上一版它是唯一「真实仓内路径却未被 scope 声明」的 deliverable)。`config-loader` 走判据表**第三行三件套**, 见 §Rule #6 |
| 外部 | **无外部动作** —— 不改 #137 body, 不发 supersede 评论 (见 §Why)。留痕与否由 owner 决定 |
| 🔴 **发版同步面 (8 文件 **+ 主仓 gitlink**, TASK-017 承接)** | 按**引用点整仓差集**枚举 (非文件白名单), **但下列 8 个已知文件落点必须在最终清单内且已在 `scope_repos.paths`**: aria 子模块 `.claude-plugin/plugin.json` · `.claude-plugin/marketplace.json` · `VERSION` · `CHANGELOG.md` · `README.md`; 主仓 `VERSION` · `README.md` (`:8` 的 `Plugin-v1.65.5-blue` badge) · `README.{ja,ko,zh}.md` (**仅正文实质变更才重译**, CLAUDE.md #140 B 档)。<br>🔴 **第 9 项落点 = 主仓 gitlink (非文件, 本版新增)**: `CLAUDE.md:81` 的 canonical 清单逐字是「aria 子模块 5 文件 + **主仓 gitlink** + 主仓 VERSION + root README badge + i18n README」, 而实跑 `grep -rniE 'gitlink\|子模块指针\|submodule pointer' openspec/changes/premerge-gate-mainbranch-failclosed/` 在上一版**零命中** ⇒ 上一版的 8 项是 canonical 清单的**真子集, 独缺 gitlink** (post_planning R3, tech-lead 与 knowledge-manager 独立交叉命中)。**且它结构上逃得过本 Spec 现有的验证方法** —— TASK-017 用的是「整仓引用点**文本**差集」, 而 gitlink 是 git **树对象**指针, 不是任何文件里的文本。⇒ 判据换成树对象层可跑的一条: 主仓根 `git rev-parse HEAD:aria` **== aria 子模块落地 commit 的 SHA** (实跑确认该命令在主仓 rc=0)。失效方向 = 落地后 root README badge 写新版本而 gitlink 仍指旧 SHA ⇒ `clone --recursive` 拿到旧插件 (**Aria #165 同族**), 而 `m6-version-badge-match` 比的是 badge ↔ `plugin.json`, **对该方向失明**。<br>⚠️ **主仓 `VERSION` 不并入「与版本 SOT 一致」判据**: 它是 meta-repo 的**独立版本线** (今日 1.7.3 vs plugin.json 1.65.5, `standards/conventions/version-management.md §4.3` 分发型 vs meta-repo 分类), 二者**永远不该相等** ⇒ 把它并进去要么恒红、要么诱使实施者把主仓版本线从 1.7.x 直推到 2.0.0。CLAUDE.md 逐字规定「必须与版本 SOT 一致」的**派生文件是 4 个** (`marketplace.json` / `VERSION` / `CHANGELOG.md` / `README.md`), **全部在 aria 子模块内**。<br>⚠️ **上一版这 8 个文件全无 task、全不在 scope** (post_planning R2/tech-lead, `blocks_phase_b`): 20 条任务做完后 `plugin.json` 仍是 **1.65.5** 而代码里的 `will be removed in v2.0` 已被执行 ⇒ **一个 1.65.x 版本违背了自己的承诺**; 且 custom check `m6-version-badge-match` 比的是 badge ↔ `plugin.json`, 两边都没动 ⇒ **对该失效方向 fail-OPEN**。类级根因见 **Aria #177** —— 本 Spec 一度是该预言的即时复现样本 |
| follow-up issue | (1) `main_branch` 自动解析设计面; (2) `fetch_gate.py` / `worktree_manager.py:170` 同形回落; (3) `workflow-runner` `gate_state` 无 `gate_error` 位置 —— 实测 `grep -rn 'gate_error' aria/` = **0 命中**, 且 `workflow-runner/SKILL.md:354-357` 的 verdict 路由只有四条臂 (green / fail / timeout / Ctrl-C), **没有「gate 抛异常」这条臂**; (4)「显式传错分支名」此前零测试覆盖; (5) C.2.4.5 的 `SKILL.md:189-191` 裸 git 命令 + `submodule_gate.sh` (与 D1 根因**同类**的最近兄弟); (6) **helper 定位形态的其余落点** —— `SKILL.md:310` (裸 `aria/`) · `:392` (skill 目录相对) · `:610` (`ARIA_` + 可执行探测/降级分支) · `:737` (`CLAUDE_`) · **跨文件** `state-scanner/references/sync-detection.md:587` (与 `:262`/`:559` 同属 v1.15.2 一次拉平的等价类, 见 TASK-014)。⚠️ **`:557` 已从本枚举移除** —— 实读它逐字是 v1.28.0 host-cron 迁移段的 `standalone scripts/submodule-tripwire-audit.sh`, 是 **tripwire 独立脚本, 不是 helper 定位形态** (post_planning R2/code-reviewer); 它仍留在 TASK-014 的负控白名单里作「零改动」要求 (无害), 但**不得作为形态实例写进 issue 正文**; (7) **`standards/openspec/project.md` 自身 `:21` (双层) 与 `:118` (单层) 两处表述矛盾** —— 转记 standards 维护者 (⚠️ `tasks.md` 早前逐字称「TASK-019 已纳入」而清单里从来没有它, post_planning R2/knowledge-manager); (8) **`config-loader` 无 AB 套件的套件缺口** (判据表第三行第三件, 见 §Rule #6) |

### 版本

**结论: MAJOR** —— 2026-08-10 依 owner 授权裁定**确认**, 不再是「待裁」(Rule #10 留痕: 须写入 handoff 请复议)。上一版写「地板 = MINOR, MINOR vs MAJOR 待裁」是**逻辑错误** (R5 两席 + 归档先例佐证):

- `MINOR+` 是**下界, 不是枚举** —— MAJOR 满足「MINOR+」;
- CLAUDE.md:35「**破坏性变更须 MAJOR**」是**下界为 MAJOR**;
- ⇒ 两条下界求交, **唯一解是 MAJOR**。上一版的「地板 = MINOR」给下游留了看似合规的违规口。

#### 破坏面论证 —— 本版**更换承重腿**

⚠️ 上一版用「D5 使 **24 处** `gate_check(` 调用 `TypeError`」当破坏面。**该论证作废**: 实测那 24 处**全部在本 skill 自己的测试文件内**, 唯一的非测试调用 `pre_merge_gate.py:435` 已显式传 `main_branch=args.main_branch`, D5 下不会 TypeError (口径见 §4) ⇒ **它是内部修补面, 不构成对外破坏面**。承重腿改为:

1. **本仓可自证的现实缺陷 (最硬的一条)** —— `--main-branch` 现有缺省是 `"main"`, 而**本仓主干就是 `master`** (`git symbolic-ref --short HEAD` = `master`)。⇒ D1 所治的「Rule #8 那条腿恒绿」在 Aria 自己身上是**现实态而非假想态**, 且**在本仓内即可证实** (`grep -c -- '--main-branch main' pre_merge_gate.py` = **1**)。该缺省不是无害默认值, **移除它改变的是既有行为语义, 不是纯 additive**。这条比「采用方可能已固化 CLI 调用行」硬 —— 后者需要仓外证据。
2. **对外 CLI 契约变更** —— `--main-branch` 由可选变必填, 依赖旧缺省的调用方转硬失败。⚠️ 该面的枚举口径**结构上看不见仓外采用方** (见 §风险), 故只能**声明不能计数**; **不得**写成「所有采用方都会炸」那类不可证伪的主张。
3. *(从属, 非承重)* **配置契约变更** —— MAJOR = v2.0.0 ⇒ 两个 legacy key 的软弃用到期, 处置由「静默翻译 + `DeprecationWarning`」变为 fail-CLOSED (TASK-020)。

> **legacy key 的破坏面必须按精确口径写** (2026-08-10 对抗复核更正, 编排层复跑坐实):
> 模板 `.aria/config.template.json:75-77` 的 `primitive_preference: ["aether-ci-cli"]` **恰等于** `ci_backends/__init__.py:17` `BACKENDS = [AetherBackend, GitHubActionsBackend]` 的 auto-detect 首位; `:78` 的 `no_aether_fallback: "skip_with_warning"` **恰等于** `pre_merge_gate.py:56` `DEFAULT_CONFIG["no_ci_fallback"]`。
> ⇒ **对逐字照抄模板的项目, 删 alias 在这两个键的值语义上近乎 no-op**。真正会漂移的是**改过这些值**的采用方 (例如设了 `no_aether_fallback: "abort"`), 且漂移方向还取决于装了什么 CLI。
> ⇒ 这恰好是 **fail-CLOSED 必要**的理由: 「静默忽略 legacy key」对**改过值的那类采用方**正好是 fail-OPEN (他们的 `abort` 意图被无声换成 `skip_with_warning`)。同时也意味着**模板必须同批改** —— 否则每个新采用方一开箱就撞硬失败。

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

`phase-c-integrator` 现 **111** tests (`test_pre_merge_gate.py` 46 + `test_ci_backends.py` 25 + `test_path_coverage.py` 40) —— 2026-08-10 实跑 `python3 -m pytest -q` 复核: **111 passed**, 且**当前全绿** ⇒ TASK-001 的红窗前提成立。

本 change 新增的**机械断言 = SC-M1..SC-M18, 按编号计 18 条 / 按 SC 表行计 20 行** (SC-M3 拆 a/b/c 占 3 行; 计数法必须写明, memory `critique-repeats-error`) (⚠️ R2-fix 由 13 增至 17: **SC-M14** UnicodeDecodeError catch-all 补编号 · **SC-M15** 折叠块内零可执行命令字面量 · **SC-M16** 折叠块外保留 `<MAIN_BRANCH>` 取值来源 · **SC-M17** `config-loader` 的 v2.0 到期措辞归零; ⚠️ **R3-fix 再 +1 = 18**: **SC-M18** 删除面其余四文件的承诺措辞归零) (其中 SC-M3 拆 a/b/c、SC-M4 含三条 grep、SC-M18 含四条 grep, 故落到测试**用例**数会更多 —— 用例数由 Phase B 定, 本文件不预写)。⚠️ 上一版写「新增 12」, 与任何计数法都对不上, 已换成可核的量。另修改既有 24 处调用 + 1 处断言 + 1 处守卫接缝。

**D-4 的等价判据 (⚠️ 本版换量)**: 曾写「`test_ci_backends.py` 25 tests 保持全绿 = 等价的唯一证据」—— **那是恒绿判据**: 实测 `grep -c '_run_with_retry' tests/test_ci_backends.py` = **0**, 那 25 条系统性绕过它 (改 mock `subprocess.run` 或 `_query`), **异常选择行为零覆盖** ⇒ 把 `except TimeoutExpired` 放宽成三元组会静默改掉 aether 的异常契约而 25 条全绿。
⇒ 等价判据换成**针对 `_run_with_retry` 本身的新建直接用例** (只捕 `TimeoutExpired` / backoff `5,15,45` × 3 attempts / 超时哨兵可区分); 25 tests 全绿降为**必要不充分**条件。

---

## 待 R4 重点审 (本节 2026-08-12 随 R3-fix 重写; 上一版仍写「待 R5 重点审 / 本版是 R4-fix」, 是 post_spec 轮次的陈旧残留)

本版是 **post_planning R3-fix**, 且是 `max_rounds=4` 的**最后一次 fix**。八轮实证**最大风险始终在本轮新写的内容** (fix 引入占比 73–100% → 53% → 70%)。请优先验:

1. 🔴 **SC 表「今日实测」列** —— R3 在此抓到一条假值 (SC-M16 声称 1, 实测 0)。本轮已把该列纳入 `xcheck.py CHECK5` **实跑回源**, 请独立复跑而非采信;
2. 🔴 **TASK-014 的处置是否可接受** —— 本轮**不再预写机械量**, 改为「判据由 TASK-002 随 F 一并产出」+ 残余**明确列为 owner 裁量项**。这是**手段类别的更换**, 请判断它是诚实标注还是变相回避;
3. 🔴 **本轮新增/改写的条款是否又制造了新的恒红或恒绿** —— 重点看 TASK-005/TASK-021 的 `test_sc22` 作用域收窄、§6.1 新增的「判定读原始 `config`」、SC-M18、TASK-017 的 gitlink 判据;
4. **`xcheck.py` 自身** —— 它上一版被 R3 用 5 个构造证伪 4 个。本版附对抗验证脚本 (`xcheck_adversarial.py`, 12/12 构造被拒), 请**继续构造新的坏实现**而不是复核它当前取值;
5. **条款间交叉一致性** —— 前七版每一版都出现过「同一文件内既立判据又违反它」(已发生 4 次, 最近一次是本轮执笔当场自查抓到的「判据串写进正文导致它自己恒绿」)。
