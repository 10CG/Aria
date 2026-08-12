# DEC-20260812-001 — `premerge-gate-mainbranch-failclosed` 拆分为 A / B 两个 Spec

> **裁定人**: owner (2026-08-12, 经 audit-engine §降级策略 `AskUserQuestion` 三路径选择)
> **触发**: post_planning `max_rounds = 4` 走满未收敛 (R4: 5 REVISE / 0 PASS, 3C+16M+9m, 6 条 `blocks_phase_b`)
> **状态**: Approved — 待 Phase A.1 落地
> **关联**: aria-plugin [#137](https://forgejo.10cg.pub/10CG/aria-plugin/issues/137) · 本 Spec 四轮 aggregate · [handoff 2026-08-11 §11](../handoff/2026-08-11-adjudication-authoring-swap-and-the-mechanical-crosscheck.md)

---

## 1. 为什么拆 (四轮数据)

| 轮 | 投票 | 原始 | 去重 Major | 阻塞B | fix 引入 | 干预手段 |
|---|---|---|---|---|---|---|
| R1 | 4R/1P | 52 | 12 | 6 | — | 原作者执笔 |
| R2 | 4R/1P | 30 | ~13 | 12 | 53% | 换人执笔 |
| R3 | 4R/1P | 27 | ~13 | 10 | 70% | + 机械交叉检查 |
| R4 | **5R/0P** | 28 | ~13 | 6 | **71%** | + 停止预写量 + 对抗验证 |

**决定性组合** (R4 五席独立确认):
- **旧 finding 无一复发** —— 每轮都真的修好了上一轮点名的东西 ⇒ **执笔环节不是问题**;
- **去重 Major 四轮持平在 ~13**, 每轮 fix 引入 ~71% ⇒ **这是稳态, 不是收敛曲线**;
- 试过三种结构性干预 (换人执笔 / 机械交叉检查 / 停止预写量), 无一改变该稳态。

⇒ **问题不在执笔, 也不在审计, 在被审对象的规模**: 21 条任务 / 70 est_hours /
跨两仓 20 个路径 / 20 行 SC —— **条款间的隐含前提数量已超过任何单轮 fix 能同步的范围**。

## 2. 划界 (⚠️ 与最初设想不同, 依据见 §3)

### Spec A — `premerge-gate-branch-existence` (小, **MINOR**, 纯 additive)

**目标**: 关掉 Rule #8 那条恒绿腿。**这是 #137 报的原始缺陷。**

| 承接 | 来源 |
|---|---|
| 新增 `--remote` / `remote: str = "origin"` | 原 §5 |
| 分支存在性核验 (**对返回的 ref 名做精确字符串比对**, 不读退出码, ⛔ 不得用 `--exit-code`) | 原 §5 + 本 session 受控裸仓实验 |
| 核验点 = 三早退**之后** / `evaluate_path_coverage` **之前** (`:345` 后 / `:356` 前, 五个行锚已实测) | 原 §6 |
| 诊断落 `raw_message` (主通道) + `gate_error` (additive 副本) | 原 §7 |
| 测试隔离接缝 (`test_sc22` 守卫保持有效而非被放宽) | 原 TASK-005 |
| 异常/重试复用 (**按轴分派**: 异常 ← `path_coverage.py:93` 元组 / 重试 ← `aether.py:38`) | 原 TASK-004 |

**SC**: SC-M6 · M7 · M8 · M10 · M11 · M13 · M14 (行为面, 已打磨八轮)
**Level**: 2 (proposal only) —— 无架构变更, 无跨仓同步面
**版本**: **MINOR** (纯 additive, 见 §3)

### Spec B — `premerge-gate-prose-helper-convergence` (大, **MAJOR**)

| 承接 | 来源 |
|---|---|
| `SKILL.md` 两处散文流程收敛为强制 helper 调用 (承重 D1) | 原 §1 |
| 5 步移入折叠块 + 去掉全部可执行命令字面量 | 原 §2 |
| 步骤 6 归属声明 | 原 §3 |
| helper 三处字面量去掉 + **参数必填** (D5, **破坏性**) | 原 §4 |
| 24 处调用补 `main_branch="master"` | 原 TASK-010 |
| helper 路径解析形态 spike (**题目是锚点未定论, 不是变量名**) | 原 TASK-002 |
| v2.0 弃用到期承诺承接 (跨两仓 5 文件, 两个 legacy key) | 原 TASK-020 |
| 发版同步面 9 项 (含**主仓 gitlink**) | 原 TASK-017 |
| Rule #6 AB (含 `config-loader` 三件套) | 原 TASK-015 |

**Level**: 3 · **版本**: **MAJOR** · 继续走 post_spec / post_planning 审计

---

## 3. ⭐ 关键依据: 为什么把「参数必填」留在 B 而不是放进 A

最直觉的分法是「A = 参数必填」, **但那会把复杂度原样带过去**:
`--main-branch` 改必填 = 破坏性变更 ⇒ 拉着 **MAJOR** ⇒ MAJOR 拉着
`pre_merge_gate.py:68/:116` 的 **v2.0 弃用到期承诺** ⇒ 跨两仓 5 文件、两个 legacy key、
`.aria/config.template.json` 这个仓外受众落点 ⇒ A 根本不是小时级。

**而存在性核验单独就足以关掉恒绿腿**, 依据是本 Spec `§症状` 自己的逐字表述:

> 「后端**结构上无法区分**『分支不存在』与『分支没有 in-flight run』—— 实测 `--branch main`
> 与 `--branch master` 返回完全同形 (`status:ok`, `runs:[]`, RC=0) … 二者都产出
> `InFlightStatus(runs=[])` ⇒ 判 green。」

⇒ 存在性核验**正是直接消除这个不可区分性**的那一步: 传 `--main-branch main` 而 `main`
在远端不存在 ⇒ 核验判 `fail` + `kind="main-branch-not-found"`, **不再 green**。

> ## 🔴 更正 (2026-08-12, A 侧 post_spec R1 — 四席独立命中)
>
> **⚠️ 本 §3 的论证有一处引用缺口, 但裁定结论 (拆分方向 + A/B 划界) 不变。** owner 原文保留在上,
> 本块只补被漏掉的限定 —— 不改写裁定。
>
> **缺口**: 上面这段只引了原 Spec 的 **`§症状`** (后端不可区分性), **漏引了紧邻的 `§根因`**:
>
> > 「**同一算法有两份实现, 而 AI 走的是没被加固的那份**」——
> > `SKILL.md` §C.2.4 散文流程共两处 4 行裸命令 (`:167` `:168` `:243` `:244`), 而 `gate_check()`
> > 完整实现了同一套流程。**AI 走散文那份**; SKILL.md 从无带参 helper 调用示范。
>
> **后果**: 「存在性核验单独就足以关掉恒绿腿」这句**只在 `gate_check()` 层成立**。
> 实测三条: `SKILL.md:243` 逐字硬编码 `aether ci status --branch main --in-flight --json` 且是
> **执行流程编号步骤本体**; 本仓 `git ls-remote --heads origin main` = **零行 + RC=0** ⇒ 那条命令
> **今日就是恒绿腿的活体**; `workflow-runner/SKILL.md` grep `pre_merge_gate.py` = **零命中**
> (唯一表述是「re-invoke: phase-c-integrator C.2.4」⇒ 编排层把执行交回散文流程)。
>
> **不变的**: 拆分方向 · A/B 划界 · 「D5 留 B」这一刀 · A 以 MINOR 独立交付的可行性
> (R1 五席一致确认「拆分对」; tech-lead 逐条回源 11/11 命中, 两个受控裸仓实验全部复现)。
> **变的只有 A 的完成定义**: A 必须写明**残余暴露**, 且 **A ship 不构成 #137 闭环, 不得据此 close #137**
> —— 闭环判据挂 B 侧 D1。§2 的 B 侧承接表因此新增一条隐含义务: **D1 是 #137 的闭环腿**, 不只是重构。
>
> 连带更正: §2 表中 A 侧「**SC**: SC-M6 · M7 · M8 · M10 · M11 · M13 · M14」的号段已在 A 落地时
> 改用 `SC-A*` 前缀 (防与 B 的 `SC-M*` 对撞); §2 A 侧「Level 2 —— 无架构变更, 无跨仓同步面」中的
> 「无跨仓同步面」应读作「无跨仓**内容**同步面」—— **发版同步面对 A 照常适用** (A 独立 ship MINOR),
> Rule #6 AB 亦同 (义务系于本 change 自己的发版, 结构上无法转移给 B)。

且 `§5` 的签名逐字是 `gate_check(..., remote: str = "origin")` —— **带默认值, 纯 additive,
零破坏面** ⇒ **MINOR** ⇒ **不触发 v2.0 弃用删除面**。

**D5 (参数必填) 是纵深防御的第二层** (防「显式传错分支名」), 价值真实但**不是关掉恒绿腿的必要条件**。

## 4. A 的起点比从零好得多 (不是重来一遍)

- **SC-M6 / M7 / M8 / M10 / M11 / M13 / M14 已经过八轮 40 席打磨**, 且本 session 新增两条
  实证写进了 §5: `ls-remote` **零命中亦返 rc=0** (故判据必须落在解析出的 ref 名列表上) ·
  `--exit-code` 无命中返 **rc=2** (会被 catch-all 误分类, ⛔ 禁用);
- `§6` 的五个插入点行锚**已逐个实读命中** (`:328` / `:338` / `:344` / `:345` / `:356` / `:357` / `:358` / `:366`);
- `test_sc22` 的三条前提**已实测确认** (patch 全局生效 / `:723` 确未传 `main_branch` / 加 subprocess 后必转红);
- 测试基线 **111 passed** 已复跑, 红窗前提成立;
- 受控裸仓 fixture 的构造方法已跑通。

## 5. 迁移动作 (Phase A.1, 待执行)

1. 新建 `openspec/changes/premerge-gate-branch-existence/proposal.md` (Level 2), 承接 §2 A 侧;
2. 现 `premerge-gate-mainbranch-failclosed` **改名/重定范围**为 B 侧, 并在其抬头
   **逐字留痕**「A 侧已拆出, 本 Spec 只保留 …」+ 指向本 DEC;
3. B 的 `detailed-tasks.yaml` 删去迁往 A 的任务时**须留 cancelled 痕迹**, 不得静默删
   (同 TASK-020 的条件任务纪律);
4. A 与 B **各自独立走 post_spec**; 四轮 aggregate 与 `xcheck.py` 作为两侧共同的输入材料保留;
5. R4 的 6 条 `blocks_phase_b` 逐条判归 A 还是 B —— **其中 3 条 Critical 全部属 B 侧**
   (`TASK-017` gitlink 求值时点 / `config.template.json` 键名面 / `CLAUDE.md:113` 同步)
   ⇒ **A 侧不继承任何 Critical**。

## 6. 本 DEC 未决

- A 的 change_id 命名待定 (上文 `premerge-gate-branch-existence` 为建议值);
- B 是改名还是新建 + 归档旧的, 待定 (涉及 36 + N 份审计报告的引用完整性);
- 本 session 记录的 **5 个仓外缺陷**仍未开 issue (外向动作待授权)。
