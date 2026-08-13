# Proposal: premerge-gate-branch-existence

> **Status**: 📝 **Draft (A.1)** — 由 [DEC-20260812-001](../../../docs/decisions/DEC-20260812-001-premerge-gate-spec-split.md) 从
> `premerge-gate-mainbranch-failclosed` 拆出的 **A 侧**。
> **Created**: 2026-08-12
> **Spec Level**: **2** (proposal only)。**R3 更正定档依据的来源** (R3 tech-lead minor): 上一版用的是
> 本 Spec 自造的三条判据 (「无架构变更 · 无跨仓**内容**同步面 · 无破坏性**契约**变更」), 其中「跨仓内容
> 同步面」这个概念在 SOT 里**不存在**, 而 SOT 的「跨模块」腿**全文未被逐字评估** (memory
> `exact-exception-condition`: 援引成文判据须字段级匹配, 不是精神匹配)。
> ⇒ **逐字照 SOT `spec-drafter/LEVEL_GUIDE.md:29` 的 Q2 三腿走一遍**「是否**架构变更 / 跨模块 / Breaking**?
> → YES → Level 3」 (🔴 **R4 更正行锚**: 上一版写 `:26`, 实跑 `sed -n '26p'` 得的是 Q1 分支的
> 「YES ▶ LEVEL 1 (Skip)」行 —— 引文内容准确, 行号错位 3 行):
> (a) **架构变更 = NO** —— §5 已钉死 A 不动 `ci_backends/aether.py`, 不碰 backend 抽象层;
> (b) **跨模块 = 🔴 R4 改判: 三条 NO + 一条上呈 `D-c`** —— 上一版逐字「代码面落在**单一 skill** 的 3 个
> 文件内 / 发版同步面是仪式」**仍是自造谓词**, 那两句一个字都不在 SOT 的条件里 (R4 tech-lead,
> `blocks_phase_b`; 我实读 `LEVEL_GUIDE.md:156-160` 复核成立 —— 这正是 R3 m-1 点名却未真正闭合的那条腿)。
> SOT 逐字给的是**四条件 OR 列表**「满足任一 ⇒ `:162` **自动提升为 Level 3**」, 逐条对账:
> ① **涉及 2 个及以上模块** = **NO** (代码面全在 `phase-c-integrator` 一个 skill 内, §Impact 逐行列明);
> ② **修改 `shared/` 目录** = **NO** (本仓无该目录, §Impact 三文件均不在);
> ③ **需要 API 契约变更** = ⚠️ **AI 不自行判定, 上呈 `D-c`** —— A 要给 `gate_check()` 与 `_build_output`
> 加形参、给 `SKILL.md` Output schema 加 `gate_error` 键 (§4/§Impact 逐字), 这些**是**契约变更; 而 SOT
> 该条**未限定「破坏性」** ⇒「additive 契约变更算不算」是**成文条件的解释问题, 不是 AI 的裁量空间**
> (规则 #10 + memory `exact-exception-condition`);
> ④ **影响多个子模块** = **NO** (代码落 `aria/` 一个子模块; Spec 落主仓是 Rule #5 强制的落点, 不是模块面);
> (c) **Breaking = NO, 但该答案以「版本裁定 = MINOR」为前提** (🔴 R4 新增依赖声明, 见 `D-c`) ——
> API 形状层零破坏 (§版本), 运行时行为翻转已单列 §行为兼容面并**已作为 owner 待裁点留痕**。
> ⇒ **(a)(c) 两腿 = NO, (b) 的条件 ③ 待 `D-c` 裁**; 三腿全 NO 时 ⇒ **Level 2**
> (`standards/openspec/project.md:117` 逐字「2 | Minimal | Medium features (1-3 days) | proposal.md」
> —— 🔴 **R4 更正行锚**: 上一版写 `:116`, 该行逐字是 `| 1 | Skip | Simple fixes, typos | No spec needed |`)。
> ⚠️ **两处不能省略的限定** (R1): (a) **发版同步面照常适用** —— MINOR ship 必触发 CLAUDE.md 的
> 「子模块 5 文件 + 主仓 gitlink + VERSION + badge + i18n」, **清单本体落 §Impact「发版同步面」行 (唯一 SOT),
> **A.2 落点**落 `## Success Criteria` §交付义务 `O-1`** (🔴 **R3 更正** —— 上一版此处逐字「Level 2 无 tasks.md
> 承载」, 该前提被 `task-planner` 路径 B 证伪, 见文首 BLOCKER; 🔴 **R4 再收窄「可执行载体」四个字** ——
> 路径 B **必读**该章节是真的, **必然为它出一条 TASK 不是**, 详见文首 R4 更正框);
> (b) **契约不破但运行时行为翻转**, 见 §行为兼容面。
> **版本**: **MINOR** —— 本 change 全部为 additive (新增可选参数 + 新增核验步 + 新增 additive 输出键),
> **API 形状层零破坏面** ⇒ 不触发 `pre_merge_gate.py:68/:116` 的 v2.0 弃用到期承诺
> **关联 Issue**: [aria-plugin #137](https://forgejo.10cg.pub/10CG/aria-plugin/issues/137)
> **代码落点**: `aria/` 子模块 `skills/phase-c-integrator/`; Spec 落主仓 (Rule #5)
> **姊妹 Spec**: `premerge-gate-mainbranch-failclosed` (B 侧, Level 3, MAJOR)
>
> ⚠️ **本 Spec 的输入不是从零起草的** —— 下列材料承自 A/B 拆分前的**九轮 45 席**审计
> (post_spec R1–R5 + post_planning R1–R4), 逐条注明来源。**但拆分后的组合是新的, 须重新过 post_spec。**
> (R2 更正: 上一版写「八轮 40 席」, 少算一整轮。**R3 再更正的是命令, 不是数** (R3 code-reviewer):
> 上一版给的 `ls .aria/audit-reports/ | grep mainbranch-failclosed` 实跑得 **55** 行
> (= 45 席报告 + 9 个 aggregate + 1 个 `…-audit-trail.md`), 照它复跑的人会得 55 ≠ 45。
> 三项并列 (memory `critique-repeats-error`): **总体** = `.aria/audit-reports/` 内文件名含
> `mainbranch-failclosed` 的**席位报告**; **范围** = 今日 `/home/dev/Aria`; **计数法** =
> `ls .aria/audit-reports/ | grep mainbranch-failclosed | grep -vE 'aggregate|audit-trail' | wc -l`
> ⇒ 实跑 **45** = 9 轮 × 5 席。该数只作修辞, 非任何机械判据的输入。)
>
> 📌 **本版 = R3-fix** (post_spec R3: 4 REVISE / 1 PASS, **0C**+14M+10m; **Critical 连续两轮归零**)。
> fix 引入率 R1→R2 **74%** → R2→R3 **79%** —— 三轮 Major 持平 ~13-14, **对单条 finding 收敛、对总量不收敛**。
> **本版的首要目标仍是压低引入率**, 手段有三: (1) 一律逐处最小改、⛔ 不重写 (唯一例外是文首 BLOCKER 块,
> 它建立在一个被证伪的前提上, 由 owner 裁的输入必须先正确); (2) **凡新写的断言必须答「它在什么实现下会红」**,
> 答不出就不写; (3) **凡换掉一个量, 换的必须是「测量点」而非「被测的不变量」** ——
> 上一版有一处正是在这里失手 (`SC-A14` 腿 2 换到了一个 harness 会替它吞掉异常的测量点)。
> **本版明确拒绝修的项与理由, 逐条写在它们各自的位置**, 不集中成清单。
> 处置逐条内联在各节, 不在本文件累积审计叙事 (memory `audit-trail-not-in-spec`)。

---

## 🚧 BLOCKER — 待 owner 裁定 (**A.2 入口必读, 未裁定不得进 Phase B**)

> 🔴 **R3 全块重写 —— 上一版建立在一个我从未回源核实的前提上** (R3 tech-lead + knowledge-manager,
> 均判 `blocks_phase_b`)。上一版逐字断言「Level 2 ⇒ A.2/task-planner 不出 `tasks.md` ⇒ 三项义务的唯一
> 载体是一份 D.2 就会被归档的散文」, 并据此把两条出路写成 (i) 保持 Level 2 只留痕 / (ii) 取 Level 3 出
> `tasks.md`。**这个前提是假的**, 于是 owner 被要求在一个**不存在的成本**上二选一。
> 形状 = memory `delegate-verify` 的镜像面: 写「X 结构上做不到」之前同样必须去 X 核。

**R3 执笔方逐条回源复核 (三条命令我本轮独立复跑, 非转述审计席结论):**

1. `aria/skills/task-planner/SKILL.md:59-67` 逐字: 「`IF tasks.md 存在` → 路径 A: 解析 tasks.md → 输出: 双层架构;
   `ELSE` → **路径 B: 从 proposal.md 分解任务 → 输出: 仅 detailed-tasks.yaml**; **始终从 proposal.md 读取
   `## Success Criteria` 章节**」⇒ **无 `tasks.md` 触发的是路径 B, 仍产出带 `TASK-{NNN}` 编号与逐条
   `status` 的机读载体。**
2. 实证 (非推断) —— 我实跑
   `for d in openspec/archive/*/; do [ -f $d/detailed-tasks.yaml ] && [ ! -f $d/tasks.md ] && echo $d; done`
   得 **4 例**, 逐个核 frontmatter: `2026-05-29-aria-context-monitor` 逐字「**Level**: 2」/ **31** 条 `TASK-` ·
   `2026-05-30-ai-native-estimator`「**Level**: 2」/ **21** 条 · `2026-05-30-emergency-hotfix-and-audit-file-scope`
   「**Level**: 2」/ **19** 条 · `2026-07-22-state-scanner-gate-yaml-datasource`「**Spec Level**: 2」/ **28** 条。
   ⇒ **4/4 都是 Level 2** (R3 tech-lead 报「三例」, 我复跑得四例 —— 方向一致, 数更强)。
3. **真实缺口在「写在哪一节」, 与 Level 无关**: `task-planner/DUAL_LAYER_SPEC.md:90-93` 逐字把路径 B 的
   **解析内容穷举为三项**「`## What` 章节 / `### Key Deliverables` / `## Success Criteria` 章节」。
   我实跑 `grep -n '^## '` 得 A 的章节 = `🚧 BLOCKER` / `Why` / `What Changes` / `Success Criteria` /
   `Rule #6` / `非目标` / `Impact` / `承自九轮审计的输入`; **标题行**计数 `grep -c '^### Key Deliverables'` = **0**。
   > ⚠️ **计数法必须行首锚定, 这是本轮自查抓到并当场换掉的一处** (留痕): 初稿写的是不带 `^` 的
   > `grep -c '### Key Deliverables'`, 而**本段正文自己就含这个串** ⇒ 实跑得 **4**, 那条命令从写下的
   > 那一刻起就不可能得 0。**判据与被判据的对象在同一份文档里, 描述它就满足了它** ——
   > 与 B 侧 `:143` 记录的同一形状 (那里也是初稿自绿、自查换成标题行锚定)。
   ⇒ **A 唯一能被路径 B 必然读到的章节是 `## Success Criteria`** (SKILL.md:67 与 DUAL_LAYER_SPEC 两处
   逐字一致); 而 O-1/O-2/O-3 与 F-1/F-2/F-3 上一版**全部写在 `## Impact` / `## Rule #6` / 本块**里 ——
   **三处都在路径 B 的解析范围之外**。**把「写在抬头」当路由**这件事本身就是上一版的第二个未核实前提。

⇒ **本轮的处置**: 六项义务**移入 `## Success Criteria` 章节**的一个显式小节 (见该节末 `### 交付义务`),
使路径 B **必然读到**它们。

> 🔴 **R4 更正 —— 上一版这里逐字写「使路径 B **必然**把它们读进 `detailed-tasks.yaml`」, 那一步在
> delegate 处不成立** (R4 tech-lead, `blocks_phase_b`; 我本轮回源复跑复核成立, 非转述):
> `DUAL_LAYER_SPEC.md:90-93` 把路径 B 的三个解析源**各带用途**分派 —— 逐字「`## What` 章节: 功能概述 /
> `### Key Deliverables`: 交付物列表 / `## Success Criteria` 章节: **验收标准**」, 而 `:104-152` 的 yaml
> schema 里「验收标准」的落点是**每条 task 内的 `verification:` 字段, 不是 task 本身**;
> 我实跑 `grep -rn 'Success Criteria' aria/skills/task-planner/` = **仅 2 命中** (`SKILL.md:67` +
> `DUAL_LAYER_SPEC.md:93`), **全 skill 无一句把 SC 条目转成 TASK**; `SKILL.md:74-84` 的分解规则输入侧
> 也一个字未提 SC。另两项实测: `grep -c '^## What$'` = **0** 且 `grep -c '^### Key Deliverables'` = **0**
> ⇒ **路径 B 文档化的两个任务源章节 A 一个都没有**。
> ⇒ **「读到」是必然的** (`SKILL.md:67` 逐字「**始终**从 proposal.md 读取 `## Success Criteria` 章节」),
> **「出六条 TASK」不是** —— 后者是 **A.2 执行者的义务** (§交付义务 抬头的祈使句), **无机械闸门**,
> 与该表「有机械闸门吗」列六项全写「没有」自洽。**本 Spec 不假装它有** (与 O-1 同一处理)。
> ⚠️ 形状 = memory `delegate-verify` 第 (2) 问「**方式合约吗**」: R3 只把义务**换了位置**,
> 没核被委派方是否以那个方式消费它。

本块自此**只保留真正需要 owner 裁的那部分**。

**三项义务与它们「漏做会不会红」的实测 (这部分 R3 五席复核无异议, 逐字保留):**

| # | 义务 | 移入后的载体 | 漏做时会红吗 |
|---|---|---|---|
| **O-1** | 发版同步面 (`aria` 子模块 5 文件 + **主仓 gitlink** + 主仓 `VERSION` + root README badge + i18n) | `## Success Criteria` §交付义务 O-1 (🔴 **R4 更正**: 路径 B **必读该章节**; **「出一条 TASK」无机械保证**, 见上框) | **不会** —— custom check `m6-version-badge-match` 比的是 badge ↔ `plugin.json`, **对「主仓 gitlink 未 bump」这个方向结构上失明** (post_planning R3 已实证; 姊妹 Spec B 的 R4 三条 Critical 之一 `TASK-017` 漏 gitlink 就是这形状的已实现版本) |
| **O-2** | **Rule #6 照跑 AB** (本轮改判第二行后**新揽**的义务) | 同上, O-2 | **不会** —— 无任何闸门读 proposal 散文 |
| **O-3** | 「**不得据 A ship 关闭 #137**」+ 是否在 #137 上留评论 | 同上, O-3 | **不会**, 且**出一条 TASK 也不够** —— 在 #137 上留评论是**仓外写动作**, TASK 只能把它排上日程, 不能授权它 |

> 🔴 **上一版出路 (i) 给 O-1 的兜底是失效委派, 一并作废** (R3 tech-lead + code-reviewer, 我本轮实读复核):
> 上一版逐字「O-1 由 phase-c-integrator §C.2.5 既有自动化 + 双推 `ls-remote` 核验兜 gitlink 那条腿」。
> 实读 `phase-c-integrator/SKILL.md:583-593` 的 §C.2.5 六步: `expected_sha = git rev-parse HEAD` (合并后
> **本地** master HEAD) → 枚举子模块 → 确定 `ENFORCED_REMOTES` → per-remote 推送 +
> `verify_parity_post_push(main_repo, branch, expected_sha, [REMOTE])`。**全流程核的是「本地已有的那个
> commit 有没有原样到达每个 remote」, 与「那个 commit 里的 gitlink 有没有被 bump」是两条正交的轴**;
> CLAUDE.md 多远程硬约束 2 的双推 `ls-remote` 核验比的是同一个量。唯一真读 gitlink 的是 §C.2.4.5, 而
> `SKILL.md:194` 逐字「pass: 所有 submodule pointer 是 forward bump 或 **no-change** 或 first-time」
> ⇒ **「未 bump」= no-change = PASS**。
> ⇒ **失效路径**: A 按 MINOR ship, 子模块 5 文件全改、主仓 `VERSION` 与 badge 全改, 唯独忘了
> `git add aria` ⇒ C.2.4.5 判 no-change PASS · C.2.5 六步全绿 · `m6-version-badge-match` 对该方向失明
> ⇒ **全绿而 `clone --recursive` 拿到旧 plugin** (memory `invariant-dimension`: 无向检查对方向性错误天然免疫)。
> ⇒ **O-1 今日没有任何机械兜底, 本 Spec 不假装它有。** 这是一个**事实**, 不是一个选项。

### 真正需要 owner 裁的 (⛔ AI 不自行决定, 规则 #10) —— 三条, 全部与 Level 无关

- **D-a (仓外写动作授权)**: O-3 的评论 + `### Follow-up 归属` 的 **F-1/F-2/F-3 三个 issue**, 都是**仓外写动作**。
  A 侧 D.2 执行时是否获授权做这些? **⚠️ 上一版在这件事上有两个口径** (R3 code-reviewer): §Impact「外部」行
  逐字「**无外部动作** —— 不改 #137 body, 不发评论」, 而 Follow-up 归属表把三个 issue 逐字派给「A 侧, A 的 D.2」。
  **本轮统一为: 四件仓外写动作 (1 评论 + 3 issue) 一并归入 D-a, 由 owner 一次裁定**, §Impact 与归属表均改为引用本条。
- **D-b (无兜底的 O-1 是否接受)**: 上面已证 O-1 结构上无机械兜底。owner 需明确: 接受「靠 D.2 执行纪律」,
  还是要求 A ship 前先补一个 gitlink 方向的 custom check (那会**新开一个 change**, 不在 A 的交付面内)。
- **D-c (Level 2 vs 3)**: 🔴 **R4 把本条从「成本收益题」改回「规则驱动题」** (R4 tech-lead ×2,
  均 `blocks_phase_b`) —— 它有**两个规则输入, 都不是 AI 能自行了结的**, 上一版通篇只呈现了成本面:
  - **(i) SOT 跨模块条件 ③「需要 API 契约变更」** (逐条对账见抬头): A 确实要给 `gate_check()` /
    `_build_output` 加形参、给 Output schema 加键; SOT 该条**未限定「破坏性」** ⇒ 若判 YES,
    `LEVEL_GUIDE.md:162` 逐字「**自动提升为 Level 3**」, **不留成本收益的余地**。
  - **(ii) 依赖版本裁定 (新增依赖声明)**: Q2 的第三腿就是 Breaking (`LEVEL_GUIDE.md:29`), 而
    §行为兼容面 末尾正把「恒 green 的闸门开始 fail 够不够 MAJOR」留给 owner ⇒ **本 Spec (c) 腿的
    `Breaking = NO` 以「版本裁定 = MINOR」为前提; 若裁 MAJOR, 则按 `LEVEL_GUIDE.md:29` + `:162`
    自动改判 Level 3**, 同样无需再走成本收益。
  - **成本面 (仅在上面两个输入都指向 NO 时才是决定性的)**: 移入 `## Success Criteria` 后,
    六项义务**已落在路径 B 的解析范围内** (⚠️ 是「**读得到**」, **不是**「必然出六条 `TASK-{NNN}`」——
    见文首 R4 更正框); 取 Level 3 的增量收益 = `tasks.md` 那层粗粒度勾稽 + parent 映射
    (`DUAL_LAYER_SPEC.md:76-79`) **外加把六项义务钉成 checkbox**。
  ⇒ 本 Spec 仍**建议维持 Level 2**, 但按规则 #10 留痕请复议 —— 定档本身是 AI 判断。

> ⚠️ 本块**不含**版本定档 (MINOR vs MAJOR) 那个待裁点 —— 它在 §行为兼容面 末尾, 是**另一件事**
> (那是「行为翻转够不够 MAJOR」, 这里是「档位」)。
> 🔴 **R4 收窄上一版的「两处都须 owner 裁, 不得合并处理」** (R4 tech-lead, `blocks_phase_b`):
> 原措辞会诱导 owner 把两处当**互不相干**的题分别裁, 而 `D-c` 的 (c) 腿是版本裁定的**函数**
> ⇒ 分别裁可能产出**违反 `LEVEL_GUIDE.md:29` + `:162` 的组合** (Breaking=YES 而 Level=2)。
> ⇒ 改为: **不得混为一题, 但须按序裁 —— 先版本 (MINOR vs MAJOR), 后 Level (2 vs 3)**;
> 版本裁 MAJOR 时 Level 不必再裁, 直接 Level 3。

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
| `workflow-runner/SKILL.md` grep `pre_merge_gate.py` (**带 `.py` 后缀**) | **零命中**; **调用**层面的表述只有 `:329`/`:351` 两处「re-invoke: phase-c-integrator C.2.4」⇒ **编排层把执行交回散文流程** |

> ⚠️ **R2 更正 (措辞过强)**: 上一版写「**唯一**表述是 `:329`/`:351`」。实跑不带后缀的
> `grep -rn "pre_merge_gate" aria/skills/workflow-runner/` 另得 **3 处** (`SKILL.md:342` 读
> `phase_c_integrator.pre_merge_gate.*` 配置 · `:373` `poll_chunk_seconds` · `gate_state_helper.py:37`),
> 「唯一」二字被 `:342` 证伪。**承重结论不变** —— 那 3 处**只读配置键, 无一是 helper 调用**,
> 故「编排层不直调 helper 脚本」仍成立; 更正的是量词, 不是结论。

**残余的精确形态** (A 落地后仍成立, 这是可现场复现的那句): 本 Spec 给执行流程新增的核验步**按步骤 2.5
同款形态**写成参数化的 helper **函数**调用 (`main_branch` 由调用方显式传真值 —— 这正是 `SKILL.md` 步骤 2.5
执行上下文契约逐字已有的要求「`main_branch` 显式传真值 (本项目 `master`), 不依赖 CLI default」),
而**步骤 3 仍逐字硬编码 `main`** —— 在 `main ≠ master` 的仓上二者**指向不同分支**:
按散文逐字执行 ⇒ 核验步查 `master` (存在, 放行) → 步骤 3 查 `main` (`runs:[]`, RC=0) ⇒ **verdict 仍 green**。

> 🔴 **R3 改标注的形态 —— 上一版要求标注的那句话是一颗 landmine, 而它正是本 Spec 自己在下面
> 拒绝过的哨兵形态** (R3 tech-lead, `blocks_phase_b`; 我本轮实读 B `:154`/`:156` 与
> `SKILL.md:243` 复核成立 —— 🔴 **R4 更正行锚**: 上一版写 B `:156`/`:161`, 其中 `:161` 逐字是
> 「折叠块**之外**必须留下 `<MAIN_BRANCH>` 的取值来源」, 与「折叠」这件事无关; 承载「5 步移入折叠块」的
> 是 **B `:154`** 的节标题, 折叠标记本体在 **B `:156`**)。
> **上一版逐字要求**「在新增步骤处**逐字标注这条不一致**」, 并由 `SC-A-step` 的 (c-含) 腿要求正文
> 同时含 `步骤 3` 与 `#137`。**问题**: 被标注的那条不一致 (「步骤 3 仍硬编码 `main`」) 是一个
> **会被 B 的 D1 修好的瞬时事实** —— B `:154` 逐字把步骤 1-5 整体折叠 (标记本体见 B `:156`)、`SC-M1` 断言
> `grep -c 'aether ci status' SKILL.md` = **0** (注解逐字「一条断言覆盖 `:167`/`:168`/`:243`/`:244`
> 全部四行」), 而 `SKILL.md:243` 今日逐字就是 `aether ci status --branch main --in-flight --json`。
> ⇒ B 正确落地后**两条路都坏**: 留着标注 = 随 plugin 分发给第三方一句**同页面即可证伪的假话**
> (违反规则 #3); 删掉标注 = `SC-A-step` (c-含) **在完全正确的 B 实现下必红**。
> ⇒ **换掉的是「标注什么」, 不是「换一个量来自圆其说」** (本轮硬约束: 不得为文档自洽而更换断言度量的量):
> 上一版标注的是**另一个步骤的当下状态**, 本版改为标注**本步骤自身的作用域边界** ——
> 「**本步只核验 `main_branch` 在 `<remote>` 上存在, 不保证后续步骤查询的是同一个分支; 两处分支名的
> 收敛见 `#137`**」。这句在 B 落地前后**都为真** (它陈述的是本步的契约, 不是别处的缺陷),
> `#137` 则退化为**溯源指针** —— 与本文件既有惯例同形 (`:242` 逐字 `(v1.65.0+, aria-plugin #122; …)`、
> `:253` 的 `#126`), issue 关闭后引用仍合法。
> ⇒ `SC-A-step` (c-含) 的**机械腿只保留 `#137` 这一个 token**; 「措辞是否真的陈述了作用域边界」
> **无机械锚, 如实标注**, 与 `SC-A-cwd` 的诚实限制同一处理 (⛔ 不为它编造第二个量)。

> 🔴 **R2: 与 B 侧 `SC-M3a` 的对撞, 二选一已选定 —— 取 (i), 写死如下** (R2 tech-lead, `blocks_phase_b`)。
> **对撞的确切形态**: B 侧 `:345` 逐字 `SC-M3a` = `grep -c -- '--main-branch "<MAIN_BRANCH>"' .../SKILL.md`
> 期望**恰为 2**「两处散文各一条」(我实跑今日基线 = **0**, 且全文件 `grep -n -- '--main-branch'` = **零行**)。
> A 若把新步骤写成一行**带参 CLI 调用示范**, 就会出现第 3 处该字面 ⇒ B 一条承重红窗
> **在完全正确的 B 实现下必红**。
> ⇒ **A 明文规定: 新增步骤的正文⛔ 不得含字面 `--main-branch`** (由 `SC-A-step` 的第三腿机械钉住)。
> **这不是为躲 grep 而扭曲交付物** —— A 自己援引的同形先例 **步骤 2.5 就是函数调用形态**
> (`evaluate_path_coverage(main_branch, pr_branch)`, 实读 `SKILL.md:242`), **不是 CLI 示范**;
> 步骤 2 亦然 (`resolve_ci_backend(cfg)`)。**CLI 示范形态属 B 侧 D1 的交付物** (把两处散文的 4 行裸命令
> 收敛为带参 helper 调用) —— A 写它就是替 B 交付, 越界在先, 撞 SC 在后。
> ⇒ **B 侧 `SC-M3a` 的期望值维持 2, A 不改 B。**
> ⚠️ **未取 (ii) 的理由**: 改成 3 需要 A 反向修改 B 的承重 SC, 而 A/B 的 ship 顺序未定 ——
> 若 `SC-M3a` 以持久测试形态落地, 「2 还是 3」取决于哪侧先 ship, 期望值会成为一个**随时序漂移的量**
> (memory `feedback_freshness_must_be_fetched_not_measured` 同形: 把不该由本侧决定的量写死进本侧)。
> 🔴 **R3: 这条点名禁令已被下方兄弟位置表升级为类级** (⛔ 不得含**任何**以 `--` 起头的 CLI flag 字面量) ——
> 起因是 `SC-M3c` 证明点名法对下一个 flag 名天然失明。本框的结论不变, 拒绝域变宽。

#### 🔴 兄弟位置**双向**清点 —— A↔B 对撞面 (R2 建表, **R3 补上缺的那半个坐标轴**)

> 🔴 **R3: 上一版的清点只做了 A→B 一个方向, 且它自称的「穷举」经不起对抗** (R3 五席里四席各自
> 独立命中同一处; 我本轮逐条复跑核实)。上一版起手命令逐字是 `grep -n 'SC-M' B/proposal.md` ——
> 问的是「**A 会不会打爆 B 的 SC**」; **反方向 (B 正确落地会不会打爆 A 的 SC) 一条都没查**,
> 而 A 新增的三条 doc 侧 SC **全部断言 `SKILL.md` 内容 —— 正是 B 的 D1 要重写的那一段**。
> 另有三处总体被悄悄缩小 (逐条见下)。
> ⚠️ **本轮不再写「穷举」二字** —— 上一版的教训正是「声称穷举的机制, 穷举本身未经复核就先被采信」。
> 改为**写明三项并列, 让读者可复跑** (memory `critique-repeats-error`)。

**清点口径 (三项并列, 两个方向各一套):**

- **方向 1 (A→B)** — **总体** = B `proposal.md` SC 表的**全部表行**; **范围** = 今日
  `openspec/changes/premerge-gate-mainbranch-failclosed/`; **计数法** =
  `grep -c '^| \*\*SC-M' B/proposal.md` ⇒ 实跑 **20**。
  ⚠️ 上一版据 `grep -o 'SC-M[0-9]*'` 得 21 个 token, 其中 `SC-M3` 是 `SC-M3a/b/c` 的**前缀伪命中**,
  非独立 SC ⇒ **真实总体是 20 行**, 上一版只列了其中 **10 条**。
- **方向 1 附加总体 (R3 新增)** — B 的**任务级预写量**也断言到 A 会改的文件, 上一版把总体收窄成
  「B 侧全部**断言到「A 会碰的文件」的 SC**」而标题写「**全部**兄弟位置」, 二者不等 (R3 code-reviewer)。
  ⇒ 补 `tasks.md` / `detailed-tasks.yaml` 里的预写量三条 (见表 1 末段)。
- **方向 2 (B→A)** — **总体** = A 本 Spec SC 表的**全部表行** (`grep -c '^| \*\*SC-A' A/proposal.md`
  ⇒ 实跑 **18**); 逐条问「**B 按其 proposal 正确落地后, 这条还成立吗**」。

##### 表 1 — 方向 A→B: A 落地会不会打爆 B 的量 (20 行 SC + 3 条任务级预写量, 逐条核销)

| B 侧 SC | 断言的量 (逐字) | 期望 | A 是否会打爆 | A 的处置 |
|---|---|---|---|---|
| **SC-M1** | `grep -c 'aether ci status' SKILL.md` | **0** | **会** —— 若 A 把新步骤写成 `aether ci status …` 形状 | ⛔ 由 `SC-A-step` (c) 禁令覆盖 (函数调用形态天然满足) |
| **SC-M2** | `grep -c '"branch": "main"' SKILL.md` | **0** | **会** —— 若 hunk ② 的 `gate_error` 示例把 `branch` 写成真值 | ✅ **R1 已处置** (§4 逐字「示例的 `branch` 用占位符」) |
| **SC-M3a** | `grep -c -- '--main-branch "<MAIN_BRANCH>"' SKILL.md` | **2** | **会** —— 见上框 | ⛔ 由 `SC-A-step` (c) 禁令覆盖 |
| **SC-M3b** | `--main-branch` 后跟字面 `main`/`master` (带不带引号) 的计数 | **0** | 不会 (根本不含 `--main-branch`) | 同上, **一条禁令覆盖多个 SC** |
| 🔴 **SC-M3c** | `<details>` 块内含 `--pr-branch` 的块数 | **0** | 🔴 **会 —— 上一版判「不会」是错的** (R3 tech-lead)。上一版理由逐字「A 不建折叠块」, 但**同一张表的 `SC-M15` 行自己推翻了它**: B 的 D1 把步骤 1-5 整体折叠 (B `:161` 逐字), **A 的新步骤届时就在折叠块内** ⇒ A 正文若含 `--pr-branch` (例如为对齐 CLI 面写一句「对应 `--remote` / `--pr-branch` 同批传入」), B 落地当天 `SC-M3c` 计数 1 ≠ 0 必红。**同一暴露面的两条腿, 上一版只覆盖了一条** | ⛔ **由 `SC-A-step` (c) 的禁令覆盖 —— 且本轮把该禁令从「点名三个字面量」升级为类级** (见下方 ⚠️) |
| 🔴 **SC-M15** | `<details>` 块内**可执行命令字面量**行数 (pattern = 以 `aether ` / `git ` / `python3 ` / `bash ` 起头的行内/围栏 code) | **0** | 🔴 **会, 且这条最隐蔽** —— 同上, A 的步骤届时在折叠块内 | ⛔ 由 `SC-A-step` (c) 禁令覆盖 |
| **SC-M16** | 折叠块**外**存在 ≥1 处说明 `<MAIN_BRANCH>` 取值来源的段落 | **≥1** | 不会 —— 方向相反 (A 加文本只可能帮它转绿, 且该腿由 B 自己的 D1 交付) | 无需约束 |
| 🔴 **SC-M18** | 同一 pattern (`still (readable\|works)\|removed in v2\.0\|仍读\|v2\.0 移除`) 跑在**四个文件**上: `pre_merge_gate.py` / `phase-c-integrator/SKILL.md` / `tests/test_pre_merge_gate.py` / `.aria/config.template.json` | **0/0/0/0** | 不会 (判定不变) —— A 不碰 v2.0 弃用面, 新增文本不含该 pattern | ⚠️ **R3 更正操作数** (三席同时命中): 上一版把总体缩写成「在 `SKILL.md` 的计数」= **1/4**。我实跑四个分量今日值 = **2 / 4 / 3 / 0**, 与 B `:364` 逐一对上; 其中**前三个里有两个正是 A 要直接编辑的文件**。结论不变但**拒绝域比上一版给的宽** ⇒ 落地时**不得**据「只要不动 `SKILL.md` 就安全」放心在 `.py` / 测试里写下带 `removed in v2.0` 形状的兼容注释 |
| **SC-M4 / SC-M5** | `pre_merge_gate.py` 的 `default="main"` / `main_branch: str = "main"` / `--main-branch main` / help 文案 `default: main` | **0** | 不会 —— A **不改** `--main-branch` 缺省 (§非目标 逐字), 新增的是 `--remote`(默认 `origin`) / `remote: str = "origin"` / help「default: origin」, 四条 pattern 全不命中 | 无需约束 |
| **SC-M6 · M7 · M8 · M11 · M13 · M14** (6 条) | 行为型断言 (受控裸仓 / 128 / `TimeoutExpired` / `wait` 不变 / glob pattern / `UnicodeDecodeError`) | 见 B 表 | **SC 层面不会** —— 这 6 条正是 `DEC-20260812-001 §2` 点名**过户给 A** 的号段 (A 侧同款 = `SC-A6`/`A7`/`A8`/`A11`/`A13`/`A14`), A 的实现就是它们要断言的东西 | 🔴 **R4 改判处置 —— 上一版把一条 owner 已裁定的 A.1 动作自行降级成了 handoff 备忘** (R4 tech-lead, `blocks_phase_b`, `introduced_by_r3fix: false` = 真实历史遗留): **`DEC-20260812-001 §5.3` 逐字「B 的 `detailed-tasks.yaml` 删去迁往 A 的任务时**须留 `cancelled` 痕迹, 不得静默删**」, DEC 抬头逐字「裁定人: owner」「状态: Approved」, 且该条与「新建 A 的 proposal」**同在 §5「迁移动作 (Phase A.1, 待执行)」这一张清单上** ⇒ 它是 A.1 的动作, 不是 D.2 的备忘 (规则 #10: AI 不得把 enabled 的 owner 决定降级/改序)。✅ **该动作已执行** (owner 已批准的动作, 非新决定): B 的 `TASK-003/004/005/007/008/009` **六条**已标 `status: cancelled` + 逐条 notes 留痕 (⛔ 不得再实现 + 指向 A 侧承接)。我本轮实测复核: 21 条 task **一条未删**, status 分布 = **`pending` 15 / `cancelled` 6**。⚠️ **上一版那句「七条全部 pending」的「七」也是错的**: `TASK-006` = 「`pre_merge_gate.py` 三处 `main` 字面量去除 + 参数必填 + help 文案」= **B 自己 D5 的交付物, 从未过户**, 今日正确地仍为 `pending`。⇒ 碰撞面**已在源头消除**, 不再依赖 handoff 纪律 |
| **SC-M9** | `gate_check(pr_branch=...)` 不传 `main_branch` ⇒ `TypeError` | — | **A→B 方向不会** —— A 不改 `main_branch` 缺省 (§非目标 逐字) | ⚠️ **R3 补核销** (R3 knowledge-manager: 上一版对它既未列也未在任何排除说明里出现, 是**静默遗漏**而非显式核销)。**⚠️ 它在反方向上会打爆 A —— 见表 2** |
| **SC-M10** | 负控 `enabled=false` 早退, **两个 fixture 变体** (干净 config / 含 legacy key 的 config) | 六键不变 + `assert ls-remote 未被调用` | 不会 —— A 的同款负控是 `SC-A10`, 断言方向一致; A 不碰 legacy key 面 (§Why ⛔ 清单) | 无需约束 |
| **SC-M12** | 参数化**五种 cwd** 跑 B §1 的 helper 调用 | 五种全部可达 | 不会 —— A **不建** B §1 那个 helper 调用面 (§非目标 逐字) | ⚠️ 与 A 的 `SC-A-cwd` **同轴不同物**: `SC-M12` 约束「helper 脚本从哪些 cwd **够得到**」, `SC-A-cwd` 约束「gate 内部 subprocess **用哪个** cwd」。两者的 ⛔ 条款一致 (**均禁为解析路径而 `cd`**, A §3 与 B §1 逐字同句) ⇒ 无矛盾 |
| **SC-M17** | 同一 pattern 跑在 `config-loader/SKILL.md` | **0** | 不会 —— 目标是**另一个 skill**, A 不碰 | 无需约束 |

**方向 1 附加总体 — B 的任务级预写量 (R3 新增, 上一版零覆盖):**

| B 侧预写量 (逐字) | 位置 | A 是否会打爆 | A 的处置 |
|---|---|---|---|
| 「既有 **24 处** `gate_check(` 调用补 `main_branch="master"`」 | B `tasks.md:85` (TASK-010) | 🔴 **会** —— A 的 13 条行为 SC 各需 ≥1 条新用例 ⇒ A ship 当天 `grep -c 'gate\.gate_check(' tests/test_pre_merge_gate.py` **> 24** | 声明 + 交 D.2 handoff (同上, **A 不改 B**) |
| 「实测 24 处 `gate_check(` 调用点、**显式传 `main_branch` 的 0 处** — 补完后应为 24/24」 | B `detailed-tasks.yaml:488` | 🔴 **会** —— A 的 `SC-A6`/`A13`/`A-zero`/`A-cwd`/`A-cli` 逐字要求**显式传** `main_branch` ⇒「0 处」当场为假 | 同上 |
| 「贴出 collected 数与变更前基线 **111** 的差值」 | B `tasks.md:122` (TASK-021) | 🔴 **会** —— A 新增用例后 111 不再是 B 的「变更前基线」 | 同上; **A 自己的 `SC-A-baseline` 在反方向上有对称问题, 见表 2** |

⇒ **方向 1 归纳**: 20 行 SC 中 **A 落在其拒绝域内的是 5 条** (M1 · M2 · M3a · **M3c** · M15) ——
其中 M2 R1 已处置, M1/M3a/M15 R2 已处置, **M3c 是本轮新补的第五条**;
另 6 条行为型 SC 与 3 条任务级预写量属**任务层面碰撞**, 不由 SC 承载, 交 D.2 handoff + `D-a`;
其余实测无对撞。

> 🔴 **R3 把三条点名禁令升级为类级禁令** (memory `fix-the-class`: 修实例必问「这形状还有几个兄弟位置」)。
> 上一版逐条点名 `--main-branch` / `aether ci status` / 裸命令三个字面量, 而 `SC-M3c` 证明**点名法对
> 下一个 flag 名天然失明** —— 三条禁令里没有 `--pr-branch`, 于是一句「(对应 CLI 的 `--remote` /
> `--pr-branch` 同批传入)」即可过 A 侧 18/18 并 ship, 而 B 折叠后 `SC-M3c` 必红。
> ⇒ **禁令改为**: 新增步骤正文 ⛔ **不得含任何以 `--` 起头的 CLI flag 字面量** (覆盖 `--main-branch` ·
> `--pr-branch` · `--branch` · `--json` · `--in-flight` **及一切 B 侧将来新增的 flag**) ·
> ⛔ **不得含 `aether ci status`** · ⛔ **不得含以 `aether `/`git `/`python3 `/`bash ` 起头的可执行命令字面量。**
> **为什么这不是「为躲 grep 扭曲交付物」**: A 援引的同形先例**步骤 2.5 本来就是函数调用形态**
> (`evaluate_path_coverage(main_branch, pr_branch)`, 实读 `SKILL.md:242`), 步骤 2 亦然
> (`resolve_ci_backend(cfg)`) —— 函数调用形态**天然一个 `--` token 都没有**。
> CLI 示范形态属 B 侧 D1 的交付物, A 写它是越界在先、撞 SC 在后。
> ⚠️ 这些禁令**只约束 A 新增的那一个步骤**, 不约束 `SKILL.md` 既有内容 (既有 4 行裸命令归 B 侧 D1)。

##### 表 2 — 方向 B→A: B 正确落地会不会打爆 A 的 SC (R3 新增, 18 条逐条过)

| A 侧 SC | 操作数 | B 会改动它吗 (实测依据) | 判定 |
|---|---|---|---|
| `SC-A-doc` | `SKILL.md` §C.2.4 Output schema json 块 (`:265-277`) 的**顶层**键集 | **会碰该块** —— B 的 `SC-M2` 目标 `"branch": "main"` 我实读在 **`:270`, 就在块内** | ✅ **不打爆** —— `:270` 缩进 **4 空格**, 被本 SC 钉死的正则 `^  "([A-Za-z_]+)":` (行首**恰两**空格) 天然排除; 我实跑该正则今日仍得 **7** 键, 与 `_build_output` 实产 7 键相等 |
| `SC-A-step (a)(b)` | `:238` 与 `:257` 之间区块的行首步骤编号序列 | **会** —— B §2 把步骤 1-5 折进 `<details>`, A 的新步骤在其内 | ⚠️ **如实标注 (🔴 R4 收窄 —— 上一版这句范围开大了)**: **不可断言的是 (a)(b) 所用的「行首编号」这个表示形式**, 折叠后编号是否保留取决于 B 尚未写出的落地文本, 在此侧写死「折叠后也应如何」是钉合成 fixture (memory `gate_tracks_reality_synthetic_fixture`)。**但承重的量是「顺序」不是「编号」** (§Impact hunk ① 逐字「号本身非承重, 承重的是它落在 2 与 2.5 之间」), 而顺序**有**与折叠形态无关的测量点 —— 按出现位置断言三个内容锚的相对次序 (`resolve_ci_backend` < 新步骤锚 < `evaluate_path_coverage`)。⇒ **上一版由「编号不可测」推出「整条不可断言」, 是把非承重量的不可测当成了承重量的不可测** (R4 tech-lead; 我复核成立, 且这正是本 Spec 在 (c-含) 上已经走通过的同一条路)。**本轮明确不补这条断言, 理由见下方 ⛔ 框。** 🔴 **R4 同时更正委派锚与委派范围**: 上一版引 B `:156`, 我实读该句在 **B `:158`**; 且它逐字只保证「折叠块须**补上** §3 新增的分支存在性核验步」= **存在性**, 对**编号是否保留 / 步骤间顺序一个字未提** (memory `delegate-verify`: 引一行说「X 本就做这件事」须确认那行讲的就是这件事) ⇒ **委派只接住了「这一步不会丢」, 没接住「它在正确的位置」** |
| `SC-A-step (c-禁)` | 该步骤正文 | 会 (步骤进折叠块 ⇒ 落入 `SC-M3c`/`SC-M15` 的判域) | ✅ **本轮升级为类级禁令后不打爆** (见上方 ⚠️) |
| `SC-A-step (c-含)` | 该步骤正文须含的 token | 🔴 **会打爆** —— 上一版要求含 `步骤 3` 并标注「步骤 3 仍硬编码 `main`」, 而 B 的 `SC-M1` 使 `aether ci status` 归零 (覆盖 `:243` 步骤 3 本体) | ✅ **本轮已改判据** —— (c-含) 只保留 `#137` 这一个 token, 标注对象改为**本步自身的作用域边界** (见 §残余暴露 的 R3 框) |
| `SC-A-note` | `SKILL.md` §C.2.4「枚举归层注记」段 (今日 `:279`) | **不会** —— 我实跑 B `SC-M18` 的 pattern 在 `SKILL.md` 的 4 处命中是 **`:49` `:285` `:286` `:349`, 无一在 `:279`**; B §3 明文「步骤 6 不动」, §2 只折叠步骤 1-5 | ✅ **不打爆** (B 删 `:285`/`:286` 会使行号下移, 但本 SC 是**内容锚**不是行号锚) |
| 🔴 **SC-A10 / A10b / A10c 及一切新 fixture** | `gate_check()` 调用签名 | 🔴 **会打爆** —— B 的 D5 + `SC-M9` 使 `main_branch` **必填** (B `SC-M9` 逐字: 不传 `main_branch` ⇒ 期望 `TypeError`) | 🔴 **本轮处置**: **A 明文要求 —— A 新增的每一条用例都必须显式传 `main_branch`**, 含三条负控 (它们只需 `enabled=false` / backend `None` / precheck 返 `(False,…)` 早退, **与是否传 `main_branch` 正交**)。⚠️ 这条**上一版完全没有** —— 反方向从未被查 |
| `SC-A-cli` | `main(argv=[… --main-branch master --remote …])` | 会 (B 使 `--main-branch` 必填) | ✅ **不打爆** —— A 已显式传该 flag |
| 🔴 **SC-A-baseline** | 「`111` + 新增 ≥ 全绿」 | 🔴 **会打爆** —— B 的 TASK-010/021 会改测试数, 111 是**「A 先 ship」这个时序下**才成立的量 | 🔴 **本轮加时序限定**: 111 = **基线 `af87cae` 且 B 未 ship** 时的量 (`SC-A-baseline` 行已改); 若 B 先 ship, 本条须以 B ship 后的实测数重定基线, **不得照抄 111** (memory `freshness_must_be_fetched_not_measured`) |
| `SC-A6` · `A13` · `A-zero` · `A7` · `A8` · `A11` · `A14` · `A-order` · `A-cwd` (9 条) | `gate_check()` 的返回值与调用序 | **不会** —— B 侧同款是 `SC-M6/M13/M7/M8/M11/M14` (DEC §2 过户号段), **断言方向与期望值逐字一致**; B 的 §1 helper 路径面与 A §3 的 cwd 面 ⛔ 条款同句 | ✅ 不打爆 (但**全部适用上面那条「必须显式传 `main_branch`」**) |
| `SC-A-sc22` | `test_sc22` (`:710`) 仍 PASS 且仍拦得住真实 git 子进程 | **会同文件编辑** —— B 的 TASK-005/010 也改 `test_sc22` 所在文件, 且 B 已成文「其函数体除补必填实参外零改动」 | ✅ 不打爆 —— A 建**独立打桩接缝**而非放宽守卫, 与 B 的约束同向 |

⇒ **方向 2 归纳**: 18 条中 **B 落地会打爆的是 3 类** —— `SC-A-step (c-含)` (本轮已改判据) ·
**一切不显式传 `main_branch` 的新 fixture** (本轮新增明文要求) · `SC-A-baseline` 的 111 (本轮加时序限定);
另有 1 条 (`SC-A-step (a)(b)`) **其「行首编号」表示形式在此侧不可断言 (承重的「顺序」则另有 fold-invariant
的测量点, 本轮明确不补, 见下框)**, B 侧 `:158` 的承接只覆盖「该步不会丢」这一半;
其余 14 条实测不受影响。

> ⛔ **R4 明确不修项 —— 不给 `SC-A-step` 补「内容序」那条腿 (本轮唯一一条「席位判对了、但我选择不改」)**。
> **席位判对的部分我已在表内如实吸收**: (a)(b) 的不可断言只及于「编号」这个表示形式, 承重的「顺序」确实
> 另有 fold-invariant 的测量点。**不补的三条理由, 逐条可证伪**:
> 1. **它是新增断言面, 不是修正**。本轮 fix 引入率已达 **93%** (28 条里 26 条由上一轮 fix 自造),
>    而 `SC-A-step` 是全表被返工最多的一条 (R2 新增 → R3 改三处 → R4 仍在争)。**在引入率 93% 时新开
>    一条机械判据, 是本轮可选动作里预期新增条目最多的那个。**
> 2. **它自己带着一个未解的 `spec-underdetermination`, 且落在三个锚里最要紧的那个上**: 「新步骤锚」这个
>    token **今日不存在**, 要由本 Spec 现编 —— 编 `_verify_branch_exists` 则该 token 是否出现在
>    `SKILL.md` 由实现者自由决定 (§Impact 只要求写成 **helper 调用形态**, **未规定函数名须进文档**);
>    编 `#137` 则与 (c-含) 腿共用同一 token, 两腿耦合成一个量。**在这个 token 定死之前, (a)(b) 的新判据
>    无法写成两个独立实现者会得同一结果的形式。**
>    ⚠️ **本条的一半是我自查推翻的**: 起草本框时我写下「另两个锚也不唯一 ——
>    `grep -c 'evaluate_path_coverage' SKILL.md` = 3 (`:242`/`:249`/`:583`)」, 随后实跑得
>    **`evaluate_path_coverage` = 1** (仅 `:242`, **唯一**) · **`resolve_ci_backend` = 2**
>    (`:241` 在 §C.2.4 内 · `:319` 在 §C.2.4.X 内 ⇒ 套用本轮为 `SC-A-note` 新加的**章节内首个匹配**规则后
>    **在 §C.2.4 内唯一**)。⇒ **那半个理由不成立, 已删除, 不并入结论** (memory `critique-repeats-error`:
>    指控别人量错时最容易在指控里犯同款 —— 这次是在「论证别人的锚不唯一」时自己编了个计数)。
>    **剩下成立的是「新步骤锚未定」这一条**, 它单独已足以支撑「今日写不成」。
> 3. **不补的残余风险有界且已定位**: 风险 = B 折叠时改用无序列表 ⇒ (a)(b) 从「必红」退化为「无从求值」。
>    它**不会造成假绿** (无从求值 ≠ 判 PASS), 且 (c) 三禁一含、`SC-A-doc`、`SC-A-note` 三条不依赖编号,
>    hunk ① 的存在性仍被 B `:158` 接住。
> ⇒ **处置**: 本条**留给 Phase B 在写 `SC-A-step` 用例时按上面的测量点补**, 并**如实登记为 A 的已知缺口** ——
> ⛔ 不在本轮 Spec 层新造判据。**这不是「不值得改」的价值评估** (那会撞规则 #10), 而是「改法本身今日欠定」;
> 若 owner 要求本轮补, 须先裁定新步骤锚 token 的写法。

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

**🔴 两条更底层的事实 (2026-08-11 主 loop 受控裸仓实验; **九轮 45 席**从未浮出)**:

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
> 合并为不可重试的 fatal; 而 `workflow-runner/SKILL.md:335` 逐字 exit condition 3「`verdict=fail` → 转为
> stop (fatal)」(R2 更正行锚: 上一版写 `:337`, 实读那行是**空行**, 被引的 exit condition 3 在 `:335`;
> 内容属实, 只有锚错 —— 承自 R1 tech-lead minor 未订正, 属 memory `reporter-miscite` 形状)
> ⇒ 一次短暂不可达即 fatal、不可 resume。**本 Spec 仍取不重试**, 理由: fail-CLOSED 与
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
- **`gate_error` 是 additive 可选结构化副本** (沿用 v1.65.0 `path_coverage` 先例)。
  🔴 **R2 钉死落地方式**: 它**必须经 `_build_output()` 产出** —— 即照 `path_coverage` 同款加一个
  `gate_error: dict | None = None` 形参, 在 `_build_output` 内 `if gate_error is not None: out["gate_error"]=…`
  (实读 `pre_merge_gate.py:232-263`, `path_coverage` 就是这个形状)。
  ⛔ **不得**在 `gate_check()` 内直接 `out["gate_error"] = {...}` 事后附加。
  **为什么这条必须写死** (R2 tech-lead): `SC-A-doc` 的**代码侧操作数**逐字是「`_build_output` 的实产键全集」,
  而上一版从未规定 `gate_error` 走哪条路 ⇒ 两种落地各损失它声称能力的一半 ——
  事后附加 ⇒ 代码侧 7 键 vs doc 侧 8 键 ⇒ **对完全合规的实现必红**;
  为躲这条而把代码侧硬编码成 8 个字面 ⇒「`SKILL.md` 有 `gate_error` 而 `.py` 从不产出」这个方向**全绿**
  ⇒ 它自称的「或反之」不成立。钉死出口后, 「实产键全集」才是一个**可从代码实测**的良定义操作数。

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
(核验在 path coverage **之前**判 fail, 评估器根本没跑)。

> 🔴 **R3: 这句枚举有第四处落点, 而且就在 A 自己要改的那个函数体里** (R3 tech-lead; 我本轮实读复核)。
> 实读 `pre_merge_gate.py:241-246` 的 `_build_output` **docstring** 逐字:
> 「…`path_coverage` 是 additive 可选键 — 仅当评估已执行且流程走到 compute_verdict 最终路径时在场
> (path_coverage 非 None); **各早退分支 (enabled:false / no-backend / precheck 失败 / backend query 失败)
> 保持既有六键不变。**」—— 与 `SKILL.md:279` 是**同一句话的第二份拷贝** (同样 4 项枚举、同样「保持六键不变」)。
> 而本节上面的 R2 钉死逐字要求 A 给 `_build_output` **加 `gate_error: dict | None = None` 形参** ⇒
> **这段 docstring 就在 A 的 hunk 里**, A 又新增第五类早退。
> ⇒ **落地后若不同批更新它, A 亲手改过的那个函数的 docstring 会与它自己新增的分支矛盾 (违反规则 #3)。**
> **为什么上一版漏了它**: 三条 doc 侧 SC 的操作数**逐字全部限定在 `SKILL.md`**, 一个字节都不读 `.py` docstring;
> 而 R2 的清点跑在「**hunk 数**」这个量上 (打桩边界表逐字「三条一一对应 §Impact 的三处 `SKILL.md` hunk,
> 无第四处」), **没跑在「同一陈述的落点数」上** —— 而这一处兄弟比 `SKILL.md:279` **离代码更近**
> (memory `fix-the-class`: 修实例必问「这形状还有几个兄弟位置」)。
> ⇒ **本 Spec 明文要求**: 更新 `SKILL.md:279` 的同一批改动内, **必须同步更新 `_build_output` 的 docstring**,
> 使其枚举与 `SKILL.md:279` 一致 (第五类 = 核验失败: 六键 + `gate_error`, **无** `path_coverage`)。
> ⚠️ **且须沿用该段落既有的中文措辞** —— 我实读 `:243-246` 确认该段今日**本就是中文**
> (英文只在 docstring 首行), 本 change 是**改一段既有中文**而非新写散文。
> **这条不是文体偏好, 是 `SC-A-note` (d) 腿的前提**: (d) 与 `SKILL.md` 侧共用同一批逐字 token,
> 若 Phase B 顺手把该段改写成英文, **(d) 会对一个行为完全合规的实现恒红**
> (memory `false_green_dual_is_permanent_red`: 恒红与假绿同样零信息)。
> ⇒ **把该段改写为英文不在本 Spec 授权范围内** (§非目标); 真要改语言, 须与 `SKILL.md:279`
> **同批同措辞**改并同步改 (d) 的 token —— 那是另一件事, 不搭在本 change 上。
> **机械锚 = `SC-A-note` 新增的第 (d) 腿** (⛔ **不新开 SC** —— 它钉的是同一个约束在另一份文件上的落点,
> 拆成新 SC 等于把「同类只覆盖一个实例」这个病复制进 SC 编号, 与 `SC-A-order` 两腿合一同一处理)。

> 🔴 **R2 更正委派对象** (R2 code-reviewer, `blocks_phase_b`): 上一版逐字写「这一条…由 `SC-A-doc` 机械钉住」,
> 是**失效的委派** —— `SC-A-doc` 断言的操作数是 `SKILL.md` 的 **Output schema json 块** (实读 `:265-277`),
> 而这条注记住在 **`:279` 的散文归纳句**里, **在 json 块外**。两个方向它都碰不到:
> (a) 只改 json 块、把 `:279` 原样留作「四类」⇒ `SC-A-doc` 全绿 (它一个字节都不读 `:279`);
> (b) 在核验失败路径上也塞了 `path_coverage` 的实现 (直接违反本节) ⇒ 键的**并集**不变 ⇒ 仍全绿。
> ⇒ **改由 `SC-A-note` 钉住** (R2 新增, 见 SC 表)。`SC-A-doc` 只管 json 块那一处, 不再声称管这处
> (memory `delegate-verify`: 写「由 X 保证」前必去 X 核它真做不做这件事)。

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

> 🔴 **R2 追加的第三件 (与前两件同样是配套的): 出口净化** —— 上一版只钉了**入口**解码策略,
> 于是把 `UnicodeDecodeError` 从 `gate_check()` 内部挪到了 **`main()` 的出口边界**上, 换了个异常名复发
> (memory `fix-recurs-in-fallback`: 修复最易在自己新写的兜底路径重犯要治的病)。
> **实测** (R2 backend-architect, 我复跑确认): `b"...\xff\xfe..."` 经 `surrogateescape` 解码得含**孤立代理码位**
> 的 `str`; `json.dumps(..., ensure_ascii=False)` 对它**成功**返回, 但 `pre_merge_gate.py:438` 的
> `sys.stdout.write(...)` 在 `sys.stdout.errors == 'strict'` 下抛 **`UnicodeEncodeError`** ⇒ 进程**非 0 退出、
> 不打印任何 verdict**, 直接违反模块 docstring 逐字契约「`Exit code: 0 = success (any verdict)`」。
> ⇒ **钉死**: 凡进入 `raw_message` / `gate_error.message` 的解码结果, **必须先做一次有损净化**
> (如 `s.encode("utf-8", "replace").decode("utf-8")`), 使其**不含孤立代理码位**。
> ⚠️ **本 Spec 不动 `:438` 的 `ensure_ascii=False`** —— 那是既有行为, 改它属另一件事; A 只负责**不往里塞
> 它序列化不出去的字节**。由 **`SC-A14` 的第二腿**机械钉住。

> 🔴 **R3 换掉腿 2 的操作数 —— 上一版的红机制在本套件的默认运行方式下不成立, 对坏实现恒绿**
> (R3 tech-lead + code-reviewer, 二席各自独立实测; 我本轮第三次独立复跑, 逐条列出)。
> **上一版腿 2 的期望逐字是「进程退出码 == 0 且 stdout 是可 `json.loads` 的单行 JSON」, 红机制逐字是
> 「`sys.stdout.write` 抛 `UnicodeEncodeError`」, 而「今日实测」列写的 `sys.stdout.errors == 'strict'`
> 是在裸 `python3 -c` 里量的 —— 不是在这条 SC 将要运行的总体里量的。**
> 我用同一段写入代码 (探针写文件避开捕获) 实测四种 harness:
>
> | harness | `sys.stdout` 类型 | `.errors` | 写入含孤立代理码位的串 |
> |---|---|---|---|
> | `python3 -c …` (裸) | `TextIOWrapper` | `strict` | **抛 `UnicodeEncodeError`** |
> | **`python3 -m pytest -q`** (**默认 fd 捕获**) | `EncodedFile` | **`replace`** | **成功写出, 不抛** |
> | `pytest -q --capture=sys` | `CaptureIO` | `strict` | 抛 |
> | `pytest -q -s` | `TextIOWrapper` | `strict` | 抛 |
>
> 且我实跑 `find aria -maxdepth 4 \( -name pytest.ini -o -name pyproject.toml -o -name setup.cfg -o -name tox.ini \)`
> = **零命中** (仓根同样零命中) ⇒ **无任何配置覆盖 pytest 的默认捕获**, 而 §测试基线自己写的复跑方式
> 逐字就是 `python3 -m pytest -q`。
> ⇒ **上一版腿 2 对坏实现恒绿**: 只做入口 `surrogateescape` 解码、**不做出口净化**的实现, 在
> `errors='replace'` 下 `sys.stdout.write` 成功 (代理位替换为 U+FFFD) ⇒ 退出码 0 · stdout 是合法单行
> JSON · `verdict=="fail"` ⇒ **三条断言全部成立**。而 R1→R2 整条修复链 (入口解码 → 出口净化) 的
> **唯一机械腿就是它** (memory `false_green_dual_is_permanent_red` / `test_asserts_what_its_name_claims`)。
> **第二个独立缺陷**: 「**进程退出码**」这个操作数只有 spawn 子进程才观测得到, 而打桩边界表逐字把腿 2
> 放进「必须 mock」档并说「注入的是**同一批 mock**, 只是断言点移到进程出口」—— **子进程里注入不了
> in-process mock**, 两句自相矛盾。
> ⇒ **本轮换量的方向**: **不是**换一个更容易绿的量, 而是把判据从「**harness 会不会替我们把字节吞掉**」
> 换到「**A 自己是否履行了 §5 钉死的那条义务**」—— 后者正是本条要抓的缺陷本体, 且与 harness 捕获模式
> **结构上无关** (硬约束: 不得为文档自洽而更换断言度量的量; 此处换的是**测量点**, 被测的不变量未变)。
> **新腿 2 见 SC 表。**

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
全部落到默认值 `"main"`; 而本仓 origin **无 `main`** ⇒ 落地后**这 24 处中的 19 处触达新核验**
(未打桩时会各自 spawn 一次真实 `ls-remote` 子进程)。

> 🔴 **数量两次更正: 24 → 20/24 (R2) → **19/24** (R3)**。
> **R2 的更正方向对了但落成了一个错的等式** (R3 code-reviewer): 上一版逐字「这 24 处**全部**触达」与
> §3 的核验点定位 + `SC-A10`/`SC-A10b` **直接矛盾** —— 那两条 SC 存在的理由正是「这两类**必须不**触达」;
> R2 据「逐行实读」把它改成「结构上够不到核验的**恰是 4 处**」, 而 R2 席位原话给的是「**至少** 4 处」这个
> 正确的**下界** —— **R2-fix 把正确的下界改成了错误的等式** (memory `redfix-change-quantity` 的镜像面)。
> **R3 改用动态测量, 不再靠实读推断** —— 我本轮用 `sys.settrace` 在整套 46 条测试上记录每次
> `gate_check` 动态调用是否执行到 §3 钉的插入点 (`pre_merge_gate.py:356`), 实跑输出:
> `tests run: 46 · dynamic gate_check calls: 24 · reached insertion point: 19 · NOT reached: [282, 301, 311, 321, 524]`。
> **三项并列**: **总体** = `tests/test_pre_merge_gate.py` 内 `gate.gate_check(` 的**动态调用**(同为 24);
> **范围** = 基线 `af87cae`; **计数法** = 逐调用点判是否执行到 `:356` (**动态**, 非逐行实读)。
> ⇒ **19 处触达 (须经 mixin 打桩隔离) + 5 处不触达 (且必须继续不触达)**:
> `:301` (`config={"enabled": False}` ⇒ 在 `:328` 返回) · `:311` · `:321` · `:524`
> (三处外层均 `mock.patch.object(gate, "resolve_ci_backend", return_value=None)` ⇒ 在 `:339` 返回) ·
> 🔴 **`:282`** (`test_case_f_outdated_binary_fails_fast`, 其 `:276` 逐字
> `mock_backend.precheck.return_value = (False, …)` ⇒ 在 `:345` 返回)。
> 🔴 **比数字更实在的是分类矛盾**: 本 Spec 有**三条**负控 `SC-A10`/`SC-A10b`/`SC-A10c` 对应**三道**早退,
> 而上一版「必须继续够不到」的名单只含 `enabled=false` 与 `backend is None` **两类** ——
> **第三类 (precheck 失败) 在仓里现成有实例 (`:282`) 却未点名**, 于是它既未进 mixin 名单也未进负控名单,
> **落在两张表之间**。⇒ 本版把三类**全部**点名, 与三条负控 SC 一一对齐。
> 危害不在数字本身: Phase B 若照「24/24」或「20/4」去设计 mixin 覆盖面与红窗预期, 会得到与 Spec 相反的实测。

⇒ **接缝形状已有先例, 不需要新发明**: `_ProbeCacheResetMixin` (`tests/test_pre_merge_gate.py:59-80`)
就是 v1.65.0 为**同一个问题**建的 —— 其 docstring 逐字「既有测试不因 `path_coverage_enabled` 默认 true
触发真实 git 子进程 (SC-22)」, 做法是在 `setUp` 里统一 `mock.patch.object(gate, "evaluate_path_coverage", ...)`。
本 Spec 沿用同一形状 (mixin 统一打桩**新核验的模块级入口**), **不逐条改 24 个调用点**。

须建**独立打桩接缝**, 使 `test_sc22` 守卫**保持有效而非被放宽**; 同时保证**下方「打桩边界」表中
「⛔ 不得打桩」档的全部 SC, 以及「两种手段皆可」档取真实 git 路径时的 SC**, 能绕过该 mixin 用真实 git 受控裸仓。

> 🔴 **R2: 这里改成从表**派生**而不再手写名单** (R2 code-reviewer, `blocks_phase_b`)。
> 上一版手写「SC-A6 / SC-A13 / SC-A-zero / SC-A-cwd / SC-A-cli」**漏了 `SC-A11`**, 而打桩边界表把
> `SC-A11` 放在「⛔ 不得打桩」档并逐字警告「若把核验入口打桩, 本条就不再验『核验放行了一个真实存在的分支』,
> **退化为恒真**」—— 同一份文件对同一条 SC 给出两个互斥处置, 照本节的名单实现就会**重新造出本轮刚修掉的空真**。
> **两处名单同步不了就不该有两处名单** ⇒ 名单**唯一 SOT = 打桩边界表**, 本节只引用不复制
> (memory `fix-the-class`: 认出了类只修它在一处的实例)。
**粒度 (函数级 vs subprocess 级) 由 Phase B spike 定** —— 但「mixin 统一打桩 + 需要真 git 的 SC 显式退出打桩」
这个**分层**是本 Spec 规定的, 不是 spike 的自由度。

---

## Success Criteria

> SC 编号用 **`SC-A*`** 前缀 —— 与 B 侧的 `SC-M*` 及既有 `test_path_coverage.py` / `test_pre_merge_gate.py`
> 的 SC 号段**全部不冲突** (B 侧曾因编号冲突被 post_planning 判 Critical, 此处预防)。
> **计数法 = 下表行数**: **18 条** = 上一版 12 + R1 新增 4 (`SC-A-order` / `SC-A-cli` / `SC-A-cwd` / `SC-A-doc`)
> + **R2 新增 2** (`SC-A-step` / `SC-A-note`, 均为 doc 侧机械锚)。

> 🔴 **可达前提 (R2 新增 —— 全表适用的一条, 不是逐条注)** (R2 tech-lead + code-reviewer, `blocks_phase_b`):
> §3 把核验点钉在 `backend is None` (`:338`) 与 precheck 失败 (`:345`) **两道早退之后** ⇒
> **凡断言「核验确实发生了」的 SC, 其 fixture 必须显式提供一个可解析的 CI backend**
> (mock backend: `probe()`→`True` · `precheck()`→`(True, "")` · `query_branch_in_flight` 返受控值;
> 走 `main(argv=...)` 的 `SC-A-cli` 同样适用 —— `resolve_ci_backend` 是模块级函数, `mock.patch.object(gate, …)` 对
> CLI 路径一样生效), **⛔ 不得依赖 ambient 的 `aether` / `gh` binary**。
> **适用集 (11 条)**: `SC-A6` · `SC-A13` · `SC-A-zero` · `SC-A7` · `SC-A8` · `SC-A11` · `SC-A14` · `SC-A-order` ·
> `SC-A-cli` · `SC-A-cwd` · 🔴 **`SC-A10c`** (R3 移入, 见下)。
> 🔴 **`SC-A10c` 是本配方在 `precheck()` 一项上的唯一例外 (R4 补回 —— 上一版把这个括注在移动中丢了)**
> (R4 code-reviewer, `blocks_phase_b`; 我实读 R3-fix 前版本确认该限定原文即在, 移入时未随迁):
> **`SC-A10c` 必须打桩 backend (这正是它移入适用集的理由), 但其 `precheck()` 必须返 `(False, …)`**
> —— 它断言的就是 `:345` 那道早退。**照本配方给它配 `(True, "")` ⇒ gate 不早退 ⇒ 核验执行 ⇒
> 它自己那条「`assert ls-remote 未被调用`」在完全正确的实现下必败 = 恒红**; 而照 SC 行实现又与本条文
> 冲突 ⇒ **两个独立实现者得相反结果** (memory `spec-underdetermination`)。
> ⇒ **配方逐字收窄为**: 适用集全体须提供可解析 backend 且 `probe()`→`True`;
> **`precheck()`→`(True, "")` 适用于除 `SC-A10c` 外的 10 条**。
> **例外 (2 条)**: `SC-A10` (`enabled=false` —— 在 `:328` 返回, **早于 backend 解析**, 结构上与 backend 无关,
> 是唯一真正的 ambient-free 例外) · `SC-A10b` (backend **必须**为 `None` ⇒ **须 mock `resolve_ci_backend` 返 `None`**,
> ⛔ **同样不得依赖 ambient「这台机器碰巧没有 binary」** —— 例外的是「不提供可用 backend」这一点,
> **不是**「可以不显式控制 backend 解析结果」)。
> **不适用 (3 条不进 `gate_check`)**: `SC-A-doc` · `SC-A-step` ·
> `SC-A-note`; `SC-A-sc22` / `SC-A-baseline` 是元断言/全量跑, 由适用集各条自身满足前提即可。
> ⇒ **配平: 11 + 2 + 3 + 2 = 18 = SC 表行数** (`grep -c '^| \*\*SC-A'` 实跑 = 18)。
>
> 🔴 **R3 更正: 上一版把 `SC-A10c` 放在例外集的哪一边错了** (R3 code-reviewer; 我本轮实读三处复核):
> 例外集的定义是「本就要打这两道早退, **故免除提供可解析 backend 的要求**」, 但 `SC-A10c` 要求
> **precheck 返 `(False, …)`** —— 实读 `ci_backends/base.py:79-85` 的默认 `precheck()` docstring 逐字
> 「**Default: always (True, "")**」⇒ **要让 precheck 失败, 必须 mock 一个 backend**, 它比适用集里任何一条
> 都更需要打桩 backend, 不是更不需要。**仓内现成的正解**: `tests/test_pre_merge_gate.py:272`
> `test_case_f_outdated_binary_fails_fast` 逐字 `mock_backend = mock.MagicMock(spec=AetherBackend)` +
> `mock_backend.precheck.return_value = (False, …)` + `mock.patch.object(gate, "resolve_ci_backend", return_value=mock_backend)`
> —— **既有先例就是打桩 backend 的**。
> ⇒ **上一版的失效方向**: 干净 CI runner (无 `aether`/`gh`) 上不打桩 backend 的 `SC-A10c` ⇒
> `resolve_ci_backend` 返 `None` ⇒ 在 `:339` `_no_ci_output` 返 green ⇒「六键不变 + 无 `gate_error` +
> `ls-remote` 未被调用」**三条断言全成立 ⇒ 绿**, 但走的是 `SC-A10b` 的分支, **precheck 早退从未执行**
> ⇒ 一个把核验错插在 `:345` 之前的实现照样全绿; 本机则相反, 真 shell out 到 binary, 判决随其版本漂移。
> ⚠️ **这条自称是「同一 ambient 只防了一个」的类级修复, 却漏了自己例外集里的成员** ——
> memory `fix_the_class` 的又一实例, 且这次漏的位置**就在修复本身内部**。
> **理由 (实测)**: `AetherBackend.probe()` = `shutil.which("aether")` (实读 `ci_backends/aether.py:62-69`),
> GHA stub = `shutil.which("gh")`; 我实跑 `which aether` = `/usr/local/bin/aether` (**本机有, 干净 CI runner 没有**)。
> 无 backend 时 `:339` `_no_ci_output` 按默认 `skip_with_warning` 返 **green** ⇒ **接线正确的实现与漏接线的实现
> 同为 green** ⇒ 上述 SC 与被测实现**无关地全红 = 恒红 = 零信息**
> (memory `feedback_false_green_dual_is_permanent_red`), 并连带打破 `SC-A-baseline`; 有 binary 时则真的
> shell out 到 binary, 结果随其版本漂移。
> ⚠️ **本条是「同一 ambient 只防了一个」的类级修复**: 上一版只防了 `origin` 这个 ambient
> (`SC-A-cli` 逐字「不得依赖 ambient origin`」), **没防 `backend` 这个 ambient**; 而同批的 `SC-A11` 注里
> 恰好写对了那句 (「+ mock backend 提供 in-flight runs」) —— **认出了类只推广了一半** (memory `fix-the-class`)。
> 故此处**不逐条补注**, 一次性对全表定义适用集与例外集。

> 🔴 **前向兼容前提 (R3 新增 —— 全表适用的第二条, 来自方向 2 清点)**: **A 新增的每一条用例都必须
> 显式传 `main_branch`**, 含三条负控 `SC-A10` / `SC-A10b` / `SC-A10c`。
> **理由 (实读 B 侧, 非推断)**: B 的 D5 使 `--main-branch` 必填, 其 `SC-M9` 逐字断言
> 「`gate_check(pr_branch=...)` 不传 `main_branch` ⇒ **`TypeError`**」⇒ **B 落地当天, A 留下的任何
> 不传 `main_branch` 的 fixture 全部 `TypeError`**。三条负控只需 `enabled=false` / backend 为 `None` /
> precheck 返 `(False, …)` 即可早退, **与是否显式传 `main_branch` 正交** ⇒ 传了不损失任何断言能力。
> ⚠️ **这条上一版完全没有** —— R2 的兄弟位置清点只问了「A 会不会打爆 B」, 没问「B 会不会打爆 A」,
> 而 A 的 SC 表恰好落在 B 的 D5 拒绝域的下游。
> ⚠️ **与既有 24 处的关系**: 那 24 处**不是** A 的交付面 (§6 已定: A 只建 mixin 打桩接缝, **不逐条改**),
> 补参归 B 的 `TASK-010`。本条只约束 **A 新写的用例**。

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
| **SC-A14** | **两腿**。**腿 1 (函数边界)**: catch-all **参数化探针** —— 逐个喂 `FileNotFoundError` / `OSError` / 输出不可解析 / **`UnicodeDecodeError`** / **任取一个不在实现 `except` 元组里的异常类**。**腿 2 (出口净化, R3 改判据)**: 喂**含孤立代理码位**的 stderr 探针 (`b"fatal: ... \xff\xfe ..."`), 在 `gate_check()` 返回的 dict 上**直接**断言 —— 对 `out["raw_message"]` 与 (在场时) `out["gate_error"]["message"]` 各跑一次 `s.encode("utf-8", "strict")` | 腿 1: 一律 `fail` + `kind=="main-branch-verify-failed"` + **`raw_message` 含分支名与 remote 名**。腿 2: **两次 `encode` 均不抛 `UnicodeEncodeError`**, 且 `verdict=="fail"` + `kind=="main-branch-verify-failed"` | `issubclass(UnicodeDecodeError, OSError)` = **False** (R1 实跑); 腿 2 今日无核验 ⇒ 无 `raw_message` 可测 ⇒ **今日必红** | 腿 1: **照 §5 两轴逐字照做 + `text=True` 的实现必红** —— `UnicodeDecodeError` 裸抛穿过 `gate_check()`。腿 2: **`surrogateescape` 解码后不做出口净化就塞进 `raw_message` 的实现必红** —— 该串含孤立代理码位 ⇒ `encode("utf-8","strict")` 抛 `UnicodeEncodeError`; 做了净化的实现两次 encode 均通过。⚠️ **R3 换掉了上一版的操作数** (「进程退出码 + stdout 可 `json.loads`」): 那个量在 `python3 -m pytest -q` 默认 fd 捕获下 `sys.stdout.errors=='replace'` ⇒ **对它唯一要抓的坏实现恒绿**, 且「进程退出码」与打桩边界表逐字「注入同一批 mock」互斥 (子进程注不进 in-process mock)。**新判据不读 `sys.stdout` 一个字节** ⇒ 与 harness 捕获模式结构上无关, 四种 harness 下同判。⚠️ **腿 2 是 R1-fix 自己开的口**: R1 钉了入口解码却把同一个病挪到出口 (memory `fix-recurs-in-fallback`) |
| **SC-A-order** | **两腿 —— 同一条「核验不得被 path coverage 左右」的两个轴**。**腿 1 (顺序轴)**: 存在性核验判 `fail` 时 **`assert evaluate_path_coverage 未被调用`**。**腿 2 (条件轴, R2 新增)**: 同一 fixture 另跑一次, `config={"path_coverage_enabled": False}` | 腿 1: 未被调用。腿 2: 仍 `verdict=fail` + `kind=="main-branch-not-found"` | — | 腿 1: **把核验插在 `:358` 之后的实现必红**。腿 2: **把核验代码误嵌进 `:357` 的 `if cfg.get("path_coverage_enabled", True):` 块内的实现必红** —— 那是紧邻插入点的最自然误植位置, 而今日 18 条 SC **全部用默认配置** (该键隐式 `True`) ⇒ 对此类误植全绿 (R2 qa-engineer)。⚠️ 两腿合一条而非新开一条: 它们钉的是**同一个约束**的两个维度, 拆开等于把「同类只覆盖一个实例」这个病复制进 SC 编号 |
| **SC-A-cli** | 走 **`main(argv=[...])`** 真实 CLI 入口: 受控工作仓 W (其 `origin` → 受控裸仓 R, R **有** `refs/heads/master`), 进程 cwd = W, 传 `--main-branch master --remote <指向不存在路径>` | `verdict=fail` + `kind=="main-branch-verify-failed"` | `grep -n "main(argv" tests/` = **零命中** ⇒ CLI 入口今日**零测试覆盖** | **只加 `add_argument("--remote")` 而漏 `:435` 的 `remote=args.remote` 的实现必红** —— 漏接线时查的是 W 的 `origin`(=R, 有 `master`) ⇒ 不 fail ≠ 期望。⚠️ fixture 必须自带受控 `origin`, **不得依赖 ambient origin** (否则漏接线实现会因无网络也返 128 而**意外全绿**) |
| **SC-A-cwd** | 同一实现、同一参数 (`main_branch="master"`, `remote="origin"`), 分别以进程 cwd = W₁ (`origin` → 裸仓 R₁, **无** `master`) 与 cwd = W₂ (`origin` → 裸仓 R₂, **有** `master`) 各跑一次 | W₁ ⇒ `fail`+`not-found`; W₂ ⇒ **不因核验 fail** | 实测 `origin` 在主仓解析到 `Aria.git`、在 `aria` 子模块解析到 `aria-plugin.git`, **两边都有 `master`** | **任何不从进程 cwd 解析仓根的实现必红** (常量路径 / `__file__` / 脚本目录 ⇒ 两次得**同一**判决)。⚠️ **诚实限制**: 本条**不能**区分「继承 ambient cwd」与「显式传 `cwd=`」—— 两者都过。那条要求由 §3 正面规定承担, **无机械锚**, 不为它编造断言 |
| **SC-A-doc** | doc↔code 一致性 (**限 hunk ②, 即 json 块那一处**): 从 `SKILL.md` §C.2.4 Output schema json 块 (`:265-277`) **实际解析**出的**顶层**键名集合 (⛔ 不得硬编码 doc 侧) == `_build_output` 的实产键全集 (六固定键 ∪ `path_coverage` ∪ `gate_error`) | 相等 | doc 侧 **7** / code 侧 **7** (R2 复跑, 见下两条解析规则) | **只落 `.py` 而漏 `SKILL.md` schema 键 (或反之) 的实现必红**; 单独回退 `SKILL.md` 那个 hunk 亦必红。⚠️ **本条不是 Rule #6 substitute** (见 §Rule #6), 它只防 doc 漂移。⚠️ **不管 `:279` 那句归纳** —— 那处由 `SC-A-note` 管 |
| **SC-A-step** | **hunk ① 的机械锚 (R2 新增; R3 钉死两处抽取边界 + 升级 (c))**。取 `SKILL.md` §C.2.4 中 `**执行流程**:` 的**首个**匹配 (今日 `:238`) 与 `**Subprocess 调用规范**:` (今日 `:257`) **之间**的区块, 按出现顺序提取行首步骤编号 (`^[0-9]+(\.[0-9]+)?\.`), 断言三腿: **(a)** 存在编号 `N` 满足 `2 < N < 2.5`; **(b)** `N` 在提取序列中的**位置**恰在 `2` 与 `2.5` **之间**; **(c) 类级三禁一含** —— **「该步骤正文」= 自 `N` 的编号行起, 到下一个行首步骤编号行之前的全部文本 (含缩进续行)**; 该正文 ⛔ **不含任何以 `--` 起头的 CLI flag 字面量** · ⛔ **不含** `aether ci status` · ⛔ **不含**以 `aether `/`git `/`python3 `/`bash ` 起头的可执行命令字面量; 且**含** `#137` | (a)(b)(c) 全部成立 | 实跑该区块编号序列 = `1. 2. 2.5. 3. 4. 5. 6.` ⇒ **区间 (2, 2.5) 内零编号** ⇒ **今日必红** | **(a)** 只落 `.py` 与测试、一个字节不动执行流程的实现必红 —— 这正是 R2 点名的「16/16 全绿而 Rule #6 第二行的**唯一**定档依据当场不存在」那个洞。**(b)** 加了步骤但落在 2.5 之后 ⇒ 红 (§Impact ① 逐字「承重的是它落在 2 与 2.5 之间」)。**(c-禁 1/2/3)** 把步骤写成**任何带 flag 的 CLI 示范** / `aether ci status` 形状 / 任何裸命令 ⇒ 红 —— 分别对应 B 侧 `SC-M3a`+`SC-M3b`+**`SC-M3c`** · `SC-M1` · `SC-M15` 的拒绝域, 清点见 §残余暴露 的**双向**兄弟位置表。**(c-含)** 加了步骤但不指向 `#137` ⇒ 红。🔴 **R3 三处改动的理由**: (1) 起点锚**必须写明「首个」** —— 我实跑扫描全文件, `**执行流程**:` 命中 **`[238, 582]`** (`:582` 属 §C.2.5), 取末次匹配的实现得起点 582 > 终点 257 ⇒ **空/负区间 ⇒ 三腿与被测实现无关地全红 = 恒红** (R3 code-reviewer); (2) 「该步骤正文」**必须写明抽取边界** —— 否则把违规命令写在**缩进续行**上的坏实现, 在「只取编号行」的实现下被误判 GREEN, 两种同样合理的抽取给出相反判决 (R3 qa-engineer, memory `spec-underdetermination`); (3) **(c-禁 1) 由点名 `--main-branch` 升级为「任何 `--` flag」** —— 点名法对下一个 flag 名天然失明, `SC-M3c` 的 `--pr-branch` 即为实例; **(c-含) 删去 `步骤 3` 这个 token** —— 它要求标注一个**会被 B 修好的瞬时事实**, 留着 = 分发一句可证伪的假话、删掉 = 在正确的 B 实现下必红, 两条路都坏 (见 §残余暴露 的 R3 框)。⚠️ 与 `SC-A-order` **同形**: R1 给**代码侧**顺序约束补了锚, **doc 侧同款顺序约束没补** (memory `fix-the-class`) |
| **SC-A-note** | **hunk ③ 的机械锚 (R2 新增)**。🔴 **R3 钉死区块边界** (上一版逐字「含 `各早退分支` 的那**段**」, 而「段」无机械定义): 取 `SKILL.md` §C.2.4 中 **Output schema 的 json 围栏结束行 (` ``` `) 之后、`**配置参数**:` 之前**的全部文本 (今日 = `:278`–`:280`)。🔴 **R4 补「首个匹配」限定 —— 这两个锚在全文件都不唯一, 与 `SC-A-step` 旧锚同款病, 而同一 commit 里只给 `SC-A-step` 加了这条限定** (R4 qa-engineer, `blocks_phase_b`; 我实跑 `grep -n '\*\*Output schema\*\*\|\*\*配置参数\*\*:' SKILL.md` = **四行** `264` / `281` / `501` / `523`, 其中 `:501`+`:523` 落在 `### C.2.4.5 Submodule Pointer Regression Gate` (`:376`–`:569`) 内、结构模式逐字同形): **两个锚一律取 `### C.2.4` 标题行 (今日 `:218`) 之后、下一个 `###` 标题行 (今日 `:306`) 之前的首个匹配**, ⛔ 不得对锚点短语做不限章节的全文件搜索。**不加这条会怎么坏 (实测形态)**: 取末次匹配的实现从 `:501` 起抓 §C.2.4.5 的文本块, 该块永远不含 `gate_error`/`main-branch`/`无 path_coverage`, 也永远满足负控形态 ⇒ **(a) 恒绿、(b)(c) 恒红, 与 A 在 `:279` 的真实编辑是否正确完全脱钩** (memory `false_green_dual_is_permanent_red`)。⚠️ **`SC-A-step` 的起点/终点锚同受本条约束** —— 它已有的「首个」限定与本条同义, 此处一并统一表述, 不改其判据。断言四腿: **(a) 负控** —— 「保持六键不变」那对括号内的枚举**仍恰 4 项**且**不含** `main-branch`; **(b)** 该区块**另有**一处同时含 `gate_error` 与 `main-branch`; **(c)** 该区块含逐字 `无 path_coverage`; 🔴 **(d) 第四处落点 (R3 新增)** —— 对 `pre_merge_gate.py` 中 `_build_output` 的 **docstring** (经 `ast.get_docstring` 取, ⛔ 不得按行号切) 跑 (a)(b)(c) 同款三问。🔴 **两个操作数共用一条解析规则 (R3 钉死)**: 先 `re.sub(r'\s+', '', 区块)` **抹掉全部空白**再匹配, token 相应写作 `各早退分支(…)保持…六键不变` / `gate_error` / `main-branch` / `无path_coverage` | (a)(b)(c)(d) 全部成立 | 我逐条实跑 (两操作数各一遍): **`SKILL.md` 区块 = `:278`–`:280`** ⇒ (a) 枚举 `no-backend/precheck失败/backendquery失败/enabled:false` = **恰 4 项**且无 `main-branch` ✅ · (b) **零命中** · (c) **零命中**; **docstring = `:241`–`:246`** ⇒ (a) 枚举 `enabled:false/no-backend/precheck失败/backendquery失败` = **恰 4 项** ✅ · (b) **零命中** · (c) **零命中** ⇒ **(b)(c)(d) 今日必红, (a) 今日绿 (负控本就该绿)** | **(b)(c)** 只改 json 块、把 `:279` 原样留作「四类」的实现必红 (`SC-A-doc` 对它双向失明, 一个字节都不读)。**(a)** 把第五类**塞进**「保持六键不变」括号的实现必红 —— 那会把「六键 **+ `gate_error`**」错报成六键, 是本 hunk 最可能的错法。**(c)** 把第五类写成也带 `path_coverage` 的实现必红 (直接违反 §4)。**(d)** 只改 `SKILL.md:279`、把 A 自己要加形参的那个函数的 docstring 原样留作「四类」的实现必红 —— 那正是上一版 18/18 全绿而规则 #3 被违反的那条缝。⚠️ **区块边界改法的理由**: 上一版按「含 `各早退分支` 的那段」取, 而 `:279` 今日是单行段落、`:280` 为空行 ⇒ **完全合规**的实现若把第五类另起一段写, (b)(c) 对它**必红** (R3 code-reviewer)。新边界的两个锚都是稳定标题/围栏, 合规实现无论分几段都落在区块内。⚠️ **抹空白这条规则不是修辞, 是本轮实测逼出来的**: docstring 里那句话被 Python 源码换行拆成 `各早退` + `分支 (…)`, 我实跑确认 —— **不抹空白则 `各早退分支` 这个锚在 docstring 里零命中 ⇒ (d) 与被测实现无关地恒红**; 换成「压成单空格」也不行 (CJK 换行处会留下一个空格)。⛔ 不写死这条规则, (d) 就是又一个 `spec-underdetermination` (与 `SC-A-doc` 的两条解析规则同一处理)。⚠️ 逐字 token (`无 path_coverage`) 由 §4 规定, 不是本 SC 自造 |
| **SC-A-sc22** | 既有 `test_sc22` (`:710`) 落地后**仍 PASS 且仍能拦住真实 git 子进程** | 用一个**故意违规的桩**验证它会红 | 今日 PASS | 被放宽 (而非建接缝) 的实现红 |
| **SC-A-baseline** | `phase-c-integrator` 全量套件 | **111 + 新增 ≥ 全绿** | **111 passed** (2026-08-11 实跑) | 任何回归红。🔴 **R3 加时序限定** (方向 2 清点新发现): **`111` 是「基线 `af87cae` 且 B 尚未 ship」这个时序下的量** —— B 的 `TASK-010`/`TASK-021` 会改同一套件的用例数与调用形状。⇒ 若 B 先 ship, 本条**必须以 B ship 后的实跑数重定基线, ⛔ 不得照抄 111** (memory `freshness_must_be_fetched_not_measured`: 新鲜度只能获取不能测量)。A 侧对称的那一半 (A ship 打爆 B 的 `111` 与 `24 处`) 见 §残余暴露 表 1 末段 |

> 🔴 **`SC-A-doc` 的两条解析规则 (R2 补 —— 上一版逐字「实际解析」但没说怎么解析)** (R2 backend-architect + code-reviewer):
> **规则 1 — ⛔ 不得用 `json.loads`**: 我实跑该块 ⇒ `json.JSONDecodeError: Expecting ',' delimiter: line 2 column 22`
> (因 `"verdict": "green" | "wait" | "fail"` 是 **pipe 联合伪类型**语法, 不是合法 JSON)。照字面用
> `json.loads` 的实现**与被测实现无关地红**。
> **规则 2 — 只取顶层键**: 该块内另含 **9 个嵌套键** (`in_flight_runs` 元素的 `run_id`/`branch`/`started_at`/
> `elapsed_seconds` + `path_coverage` 的 `decision`/`workflows_scanned`/`matched_workflows`/`changed_files_count`/
> `reason`)。朴素 `"key":` 正则实测取到 **16** 键, 与 code 侧 7/8 键**永不相等 ⇒ 恒红**。
> ⇒ **判据钉死为**: 块内**行首恰两个空格**的 `"<key>":` 行 (正则 `^  "([A-Za-z_]+)":`, 多行模式)。
> 我实跑该正则 ⇒ 恰得 **7** 键 `verdict / pr_ci_status / in_flight_runs / primitive_used /
> primitive_version_sha / raw_message / path_coverage`, 与 `_build_output` 今日实产 7 键相等 ✅。
> (`path_coverage` 的值是**同行内联对象**, 其嵌套键不在行首 ⇒ 被该正则天然排除 —— 实测确认。)
> ⚠️ 这两条是**规定**而非建议: 不写死解析规则, 「实际解析」这四个字就是欠定, 两个独立实现者会得到相反结果
> (memory `spec-underdetermination`)。

> ✅ **`SC-A-step` 的拒绝能力已对抗性验证 (R2 执笔方实跑, 非只验今日取值)** ——
> memory `adversarial-fixture`: 验断言要验它**拒不拒得掉坏实现**, 不是当前取值对不对。
> 用 1 个好实现 + **5 个像样的坏实现**跑判据, 结果逐条命中**预期的那条腿**:
> 今日基线 ⇒ `RED(a)` · 好实现 ⇒ `GREEN` · 步骤落在 2.5 之后 ⇒ `RED(b)` · 写成带参 CLI 示范 ⇒ `RED(c-禁1)` ·
> 写成 `aether ci status` ⇒ `RED(c-禁2)` · 写成 `git ls-remote` 裸命令 ⇒ `RED(c-禁3)` · 缺 `#137` 标注 ⇒ `RED(c-含)`。
> ⇒ 三腿**各自独立可红**, 不是靠 (a) 一条撑起来的 (若只有 (a), 后 4 个坏实现全绿)。
> `SC-A-note` 同法验过: 今日 (b)(c) 红、(a) 绿 (负控今日本就该绿), 把第五类塞进六键括号的坏实现被 (a) 拒绝。
> ⚠️ **R3 如实标注: 上面这份对抗性验证是对 R2 版判据跑的, R3 改了三处后须重跑, 本轮未重跑。**
> R3 新增/改动的四个判别点各自的红机制已在 SC 行内逐条写明, 但**「1 好 + N 坏」的成套复跑属 Phase B**:
> (i) 起点锚取末次匹配 ⇒ 应 `RED(恒红)` (已由实跑 `[238, 582]` 证明区间为负, 非推断);
> (ii) 违规命令写在缩进续行 ⇒ 应 `RED(c-禁3)`; (iii) 正文含 `--pr-branch` ⇒ 应 `RED(c-禁1)`;
> (iv) `SC-A-note` (d) 只改 `SKILL.md` 不改 docstring ⇒ 应 `RED(d)` (已由实读 `:241-246` 今日文本证明 baseline-failing)。
> **不声称已验 = 不把「写下来」当「验过」** (memory `feedback_paper_fix_antipattern`)。

**打桩边界 (逐条覆盖 —— 上一版只覆盖 5/12 条, 且 SC-A7 那条理据已被实测证伪)**:

> ⚠️ **R2 收窄档位标签的含义**: 「⛔ 不得打桩」**只禁打桩核验入口 / `ls-remote` 子进程**,
> **从不禁止打桩 CI backend** —— 恰恰相反, 见上方「可达前提」: 该档全部成员都**必须**打桩 backend。
> 上一版的标签与它自己成员 `SC-A11` 行内的「+ mock backend」当场冲突 (R2 code-reviewer)。
> **本表是绕过 §6 mixin 的名单的唯一 SOT** (§6 已改为引用本表, 不再复制名单)。

| 档位 | SC |
|---|---|
| **真实 `ls-remote` + 受控裸仓** (⛔ 不得打桩核验入口 / `ls-remote`; **backend 必须打桩**) | SC-A6 · SC-A13 · SC-A-zero · **SC-A-cwd** · **SC-A-cli** · **SC-A11** (⚠️ R1: 若把核验入口打桩, 本条就不再验"核验放行了一个真实存在的分支", 退化为恒真 —— 须用**分支确实存在**的受控裸仓 + mock backend 提供 in-flight runs) |
| **两种手段皆可** | **SC-A7** —— ⚠️ R1 更正: 上一版逐字「必须 mock (真实 `ls-remote` 无法产出确定性 128)」, 该理据**实测为假** (`git ls-remote --heads /tmp/does-not-exist-repo-xyz master` ⇒ **确定性 rc=128**); 且 B 侧 `:366-369` (🔴 **R4 更正行锚**: 上一版写 `:358-361`, 我实读那四行是 B 的 `SC-M12`/`SC-M13`/`SC-M14`/`SC-M15` 表行, 与打桩边界无关; 被引的「打桩边界 (前一版自相矛盾, 本版钉死)」+「⚠️ 上一版此段有**两处**自相矛盾」在 `:366`–`:369`。该错锚**承自 R2-fix, 非本轮引入**, 是 memory `reporter-miscite` 的一个未清实例) 早在 post_planning R3 就把同一句更正过, A 承接时把更正丢了。⚠️ **被这条锚支撑的实质结论不受影响** —— 「真实 `ls-remote` 可产出确定性 128」我实跑复现 `rc=128` |
| **必须 mock** (真实环境结构上造不出) | SC-A8 (`TimeoutExpired` + mock `time.sleep`) · SC-A14 **两腿** (腿 1: `FileNotFoundError` = git 二进制缺失 / `UnicodeDecodeError` / 任取异常类; **腿 2** 注入含孤立代理码位的 stderr 探针 —— 🔴 **R3: 与腿 1 同一进程内、同一批 mock, 断言点在 `gate_check()` 的返回值上**, 不再走 `main(argv=…)` 与进程退出码。上一版把「进程出口」与「同一批 mock」写在同一档里, 二者互斥 —— 子进程注不进 in-process mock) |
| **走 §6 的 mixin 打桩接缝** (断言"未被调用", 需可观测的打桩点) | SC-A10 · SC-A10b · SC-A10c · **SC-A-order** (**两腿同档** —— 腿 2 只改 `config`, 打桩形态不变) |
| **纯文件读取, 不涉 subprocess** | **SC-A-doc** · **SC-A-step** · **SC-A-note** (三条一一对应 §Impact 的三处 `SKILL.md` hunk ①②③。🔴 **R3 更正上一版的「无第四处」**: 那句只声称**没有第四处 `SKILL.md` hunk**, 是对的; 但清点跑在「**hunk 数**」上而非「**同一陈述的落点数**」上, 于是漏掉 `pre_merge_gate.py:241-246` 的 `_build_output` docstring —— 它是 `SKILL.md:279` 那句枚举的**第二份拷贝**, 且就在 A 要加形参的那个函数里。已由 **`SC-A-note` 的第 (d) 腿**接住, ⇒ `SC-A-note` 的操作数现为**两份文件**, 本档「纯文件读取」的定性不变) |
| **元断言 / 全量跑** | SC-A-sc22 · SC-A-baseline |

---

### 交付义务 (**非 SC** —— R3 新增, 它们放在这一节是为了**被 A.2 读到**)

> 🔴 **本小节是 R3 对「有记录 ≠ 有路由」的真修法, 也是 R3 唯一新增的结构** (R3 tech-lead + knowledge-manager)。
> **为什么放在 `## Success Criteria` 里**: `task-planner/SKILL.md:67` 逐字「**始终从 proposal.md 读取
> `## Success Criteria` 章节**」, `DUAL_LAYER_SPEC.md:90-93` 把路径 B 的解析内容**穷举为三项**
> 「`## What` 章节 / `### Key Deliverables` / `## Success Criteria` 章节」——
> 我实跑**标题行**计数 `grep -c '^### Key Deliverables'` = **0** ⇒ **`## Success Criteria` 是 A 唯一能被路径 B
> 必然读到的章节** (⚠️ 必须行首锚定, 理由见文首 BLOCKER 的自查留痕)。
> 上一版把这六项写在 `## Impact` / `## Rule #6` / 文首 BLOCKER 里, **三处都在解析范围之外** ——
> 「写在抬头 ⇒ A.2 入口必然读到」这句本身是第二个未回源核实的前提。
> ⚠️ **本小节不入 SC 计数**: 计数法逐字是「**下表行数**」= **18**, 本小节不含 SC 表行
> (实跑 `grep -c '^| \*\*SC-A'` = **18**, 与抬头一致)。它们**不是可证伪的机械判据**, 混进 SC 表会污染
> 「每条 SC 都带今日实测值」这个性质 (memory `falsifiable_evidence_for_binary_acceptance`)。

**A.2 须为下列六项各出一条 task; ⛔ 不得因「Level 2 / 变更小」跳过 (规则 #10):**

| # | 义务 | 完成判据 | 有机械闸门吗 |
|---|---|---|---|
| **O-1** | 发版同步面: `aria` 子模块 5 文件 (`plugin.json` SOT + `marketplace.json` + `VERSION` + `CHANGELOG.md` + `README.md`) + **主仓 gitlink** + 主仓 `VERSION` + root README badge + i18n README | 逐项贴出 `git show --stat` / `git diff` 证据; **gitlink 一项须贴 `git show --submodule=short <ship-commit> -- aria` 显示指针前后两个 SHA** (🔴 **R4 换命令** —— R4 code-reviewer: 上一版给的 `git diff --submodule=short` **在提交后恒空**, 对它唯一要防的方向零区分力。我本轮实测三跑: 干净工作树上 `git diff --submodule=short -- aria` = **0 行**, 且**已 bump 与从未 bump 的仓上同为 0 行** ⇒ 贴 0 行输出与漏 `git add aria` 的证据**逐字节相同**; 换用的命令实测 `git show --submodule=short fb5ed36 -- aria` 输出含 `-Subproject commit 183836b…` / `+Subproject commit af87cae…` 两行, 而对未 bump 的 commit (`98ad1f5`) 输出 **0 行** ⇒ **两向可区分**。memory `redfix-change-quantity`: 换的是**量**, 不是阈值; 与同格另一半 `git show --stat` 的 commit 基准也对齐了) | **没有** —— 见文首 `D-b`: `m6-version-badge-match` 只比 badge ↔ `plugin.json`; §C.2.4.5 判 no-change = PASS; §C.2.5 与双推 `ls-remote` 核的是另一条轴。**本 Spec 不假装它有** |
| **O-2** | **Rule #6 照跑 AB** (第二行, 零裁量) | 两套件 `ab-suite/phase-c-integrator.json` + `ab-suite/phase-c-integrator-pre-merge-gate.json` 各跑完, 结果落 `ab-results/`; 并**带上 §Rule #6 已成文的有效性限定** | 没有 —— 无闸门读 proposal 散文 |
| **O-3** | 「**不得据 A ship 关闭 #137**」的仓外落点 | 见文首 `D-a` (**仓外写动作, 须 owner 授权**) | 没有 |
| **F-1** | 抽取共享重试 helper (`_run_with_retry` 跨 backend 抽象) 开 follow-up issue | 见文首 `D-a` | 没有 |
| **F-2** | catch-all 不重试在 168h 无人值守下的可用性权衡, 开 follow-up issue | 见文首 `D-a` | 没有 |
| **F-3** | 同形兄弟位置 (`fetch_gate.py` / `worktree_manager.py:170`) 开 follow-up issue | 见文首 `D-a` + 本文 §非目标 的去重规则 | 没有 |

**A 的 D.2 handoff 另须写明 (非 task, 是交接事实)**: A ship 会打爆 B 侧三条任务级预写量
(`tasks.md:85` 的「24 处」· `detailed-tasks.yaml:488` 的「显式传 0 处」· `tasks.md:122` 的基线 `111`)。
**A 不改 B 的这三处**(跨轨改会撞车), 但**必须交接**。逐条依据见 §残余暴露 的**表 1**。

> 🔴 **R4 更正 —— 上一版把「六条已过户任务仍 pending」也塞在本段, 那不是交接事实, 是 owner 已裁定的
> A.1 动作** (R4 tech-lead, `blocks_phase_b`; **非本轮 fix 引入**): `DEC-20260812-001 §5.3` 逐字要求
> 「B 删去迁往 A 的任务时**须留 `cancelled` 痕迹, 不得静默删**」, 状态 Approved。
> ✅ **已执行** —— B 的 `TASK-003/004/005/007/008/009` **六条**已标 `cancelled` + 逐条 notes 留痕;
> 我实测复核 status 分布 = **`pending` 15 / `cancelled` 6**, 21 条一条未删。
> ⚠️ 上一版的「七条」也是错的: `TASK-006` 是 B 自己 D5 的交付物, 从未过户, 今日正确地仍 `pending`。
> ⇒ **本段不再承载它** —— 它已在源头消除, 不需要靠 D.2 纪律兜。
> ⚠️ **留痕 (规则 #10 自查)**: 上一版把这条降级为 handoff 备忘时, A 全文对 `DEC §5` **零引用**
> ⇒ owner 在 `D-a`/`D-b`/`D-c` 三个待裁点上**看不到它** —— 这正是「AI 自作主张的流程判断」那个形状,
> 与本 Spec 反复援引的规则 #10 同款。本轮已改。

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
在落地分支上单独 **`git checkout <BASE_SHA> -- .../SKILL.md`** (⚠️ **R2 更正命令**: 上一版写
`git checkout HEAD -- …`, 而落地分支上该 hunk **已在 `HEAD` 里** ⇒ 那条命令恢复的正是**已改的**版本,
**是 no-op**, 照它复跑会得到「三条仍全绿」却根本没回退过, 误以为验证了本条; 须以**基线 SHA** 为源)
回退 `SKILL.md` 侧**全部** hunk、保留全部 `.py` 与测试,
`pytest -k "sc_a6 or sc_a13 or sc_a_zero"` **三条仍全绿** ⇒ 不满足 baseline-failing 的定义性要求。
> 定档结论不受此命令错误影响 —— **(a) 一条已足以定第二行**; 更正的是可复跑性。
> ⚠️ 新增的 **`SC-A-doc` / `SC-A-step` / `SC-A-note` 确实对那三处 hunk baseline-failing**, 但**本 Spec 不拿它们当 substitute** ——
> 因为 (a) 已使定档落到第二行, substitute 通道**结构上不再适用**。三条只作防 doc 漂移用。

**(d) 三处互斥已消除。** 上一版 `:196` 主张第一行 (= 申请豁免) × `:201` 逐字「不申请任何豁免」×
`:39` 把「Rule #6 AB」整体划归 B 侧 —— 三者不可能同时为真。现在: 定档第二行 ⇒ 不申请豁免 ⇒ 一致;
且 §Why 的 ⛔ 清单已更正为「**B 侧自己的** Rule #6 AB」—— **Rule #6 的触发点是本 change 自己的发版**
(CLAUDE.md 逐字「Skill 变更发版前须过 Rule #6 benchmark」), A 按 MINOR 独立发版,
**AB 义务结构上无法转移**给一个至今「不具备进 Phase B 条件」的姊妹 Spec。

> **A.2 仍须逐行点名** `SKILL.md` 的每处变动 (SOT `:33` 的留痕要求对第二行同样有用),
> 但**不再以此换取豁免**。AB 形态照 v1.65.0 先例 (CHANGELOG 逐字「Rule #6 照跑 AB
> (3 eval × with/old/without 三臂)」), 具体 eval 选取属 A.2/Phase B。

> 🔴 **继承 B 已成文的有效性限定 (R2 补 —— A 是本轮改判后才新揽这份义务的, 承接时没把限定带过来)**:
> ship 前须过 **`ab-suite/phase-c-integrator.json`** 与 **`ab-suite/phase-c-integrator-pre-merge-gate.json`**
> (我实跑 `ls aria-plugin-benchmarks/ab-suite/` 确认两套件均在), 结果存 `ab-results/`。
> **已知局限**: 两套件对 **§C.2.4 覆盖薄** (承 aria-plugin #127) —— 逐字承自 B 侧 `:383`。
> **本 Spec 不以此降档** (第二行零裁量), 但**诚实声明: A 的行为证据主要由 `SC-A*` 承担, AB 是合规义务
> 而非本 change 的主要证据来源**。
> ⚠️ **不写这句的失效方向是反向的假绿**: A.2 若选到覆盖薄的 eval ⇒ 三臂无差异 ⇒ 结果被读成
> 「AB 通过 = 行为已验证」, 即 memory `feedback_false_green_dual_is_permanent_red` 所指的测量剧场。
> ⚠️ **不新开套件缺口 issue** —— #127 已在, B 侧亦已登记同一缺口; 归属见 §非目标 的 follow-up 归属块。

---

## 非目标

- **不改** `--main-branch` 的缺省 (B 侧 D5);
- **不改** `SKILL.md` 两处散文流程的**既有** 4 行裸命令 (`:167` `:168` `:243` `:244`) / 不建折叠块 (B 侧 D1)。
  ⚠️ **但 A 必须新增执行流程编号步骤** (v1.65.0 步骤 2.5 先例) —— 二者不矛盾: 新增一步 ≠ 收敛既有两处。
  🔴 **R4 修正本条的第二半句 —— 它是同一陈述的第四份拷贝, R3 只改了另外三份** (R4 tech-lead + qa-engineer
  + code-reviewer 三席独立命中, 均 `blocks_phase_b`; memory `fix-the-class`, 且 R3 正是在诊断出同款病的
  那一轮里漏了自己这一处)。**上一版逐字**「由此产生的『新步骤用 `<MAIN_BRANCH>` 而步骤 3 硬编码 `main`』
  这条不一致, 按 §残余暴露在**该步骤处逐字标注**」—— 那正是 §残余暴露 的 R3 框判定为 **landmine** 并已作废的
  标注对象 (「步骤 3 仍硬编码 `main`」是**会被 B 的 D1 修好的瞬时事实**: 留着 = 随 plugin 分发给第三方一句
  同页面即可证伪的假话, 违反规则 #3)。⇒ **本条改为**: 新增步骤处**只标注本步自身的作用域边界**并指向 `#137`,
  ⛔ **不得标注「步骤 3 硬编码 `main`」这条会过期的事实** —— 与 §残余暴露 R3 框 · `SC-A-step` (c-含) ·
  §Impact hunk ① 三处口径统一 (那三处已是 R3 改后的口径, 本条是最后一处);
- **不动** `ci_backends/aether.py` (§5 已钉死; 机械判据 = `git diff --stat` 不得出现该文件);
- **不引入** `main_branch` 自动解析 —— 实测 `ls-remote --symref` 存在 RC=0 但无 `ref:` 行两态 (unborn / detached), 需独立设计;
- **不改** `path_coverage.py` 代码与行为;
- **不改** `aether` CLI 返回语义;
- **不改** `workflow-runner` 的 `gate_state` schema;
- **不动** `no_ci_fallback` / stub backend 既有降级语义 —— 由 **SC-A10 / A10b / A10c 三条**机械钉住;
- **不修**同形兄弟位置 —— `phase-d-closer/fetch_gate.py` 的字面 `("master","main")` 回落 ·
  `state-scanner/lib/worktree_manager.py:170` 的 `base_branch: str = "master"`。
  ⚠️ **Phase B 实施者不得照抄 `fetch_gate.py`**。开 follow-up (归属见下)。

### Follow-up 归属 (R2 新增 —— 上一版 4 处承诺全无归属/编号)

**计数法必须写明** (memory `critique-repeats-error`): **总体** = 本 Spec 全文里**承诺将来开 issue** 的提法;
**范围** = R2-fix 版; **计数法** = `grep -n 'follow-up'` 后**逐处人工判性质**, ⛔ 不含本表自身、不含交叉引用。
⇒ **4 处文本 = 3 件事** (§5 与 §Impact `aether.py` 行讲同一件)。逐处列明并**钉死归属**:

| # | 承诺 | 位置 | 归属 |
|---|---|---|---|
| F-1 | 抽取共享重试 helper (`_run_with_retry` 跨 backend 抽象) | §5 末条 | **A 侧, A 的 D.2** |
| F-2 | catch-all 不重试在 168h 无人值守下的可用性权衡 | §2 catch-all 权衡框 | **A 侧, A 的 D.2** |
| F-3 | 同形兄弟位置 (`fetch_gate.py` / `worktree_manager.py:170`) | 本节上一条 | **A 侧, A 的 D.2** (见下方去重规则) |
| (F-1 重复登记) | 同 F-1, 措辞重复 | §Impact `aether.py` 行 | **同 F-1, 不是第 4 件事** |

⚠️ 逐处实跑 `grep -n 'follow-up'` 核对 —— 4 处**文本**承诺实为 **3 件事** (`§5` 与 `§Impact aether.py` 行讲的是同一件)。
本表**不引入第四件** —— 我起草本表时一度按 B 侧清单补了一条 A 里根本不存在的 follow-up, 自查 grep 时发现并删除
(memory `feedback_cross_doc_claim_verify_at_target`: 归属表也得回源核, 不能照抄姊妹 Spec)。

> 🔴 **F-3 的去重规则 (R2 tech-lead minor: A 与 B 各自声称要为同一组同形位置开 issue, 双方都可能以为对方做了)**:
> B 侧 follow-up 清单 **(2)** 与 F-3 **是同一件事**。⇒ **先 ship 的一侧开, 后 ship 的一侧只回填 issue 号、不重复开。**
> A 是独立 MINOR、B 至今「不具备进 Phase B 条件」⇒ **实际大概率由 A 开**; A 开出后把号写进 A 的 D.2 handoff。
> ⚠️ **如实标注这条规则的单向性**: 它写在 A 里, B 下次修订前**读不到**它 ⇒ 残余风险 = **重复登记一个 issue**
> (危害小), 已消除的是**两侧都不开**那个方向 (危害大)。**不在本轮改 B** —— B 正处在自己的 post_planning 轨上,
> 跨轨改它会撞车 (memory `feedback_concurrent_feature_collision_claim_before_build`)。
> 🔴 **R3 更正两处** (R3 tech-lead + code-reviewer):
> **(1) 承载**: 上一版逐字「Level 2 无 `tasks.md`, 唯一载体是 D.2 会归档的散文」——
> **这个前提是假的** (`task-planner` 路径 B 仍出 `detailed-tasks.yaml`, 实证见文首)。
> F-1/F-2/F-3 已与 O-1/O-2/O-3 一并移入 **`## Success Criteria` §交付义务**, **A.2 须为各出一条 task**
> (🔴 **R4 改措辞**: 上一版逐字「**由** A.2 路径 B 各出一条 task」把它写成了机制, 而它是**执行者义务**
> —— 路径 B 必读该章节, 但不把 SC 条目转成 TASK, 见文首 R4 更正框), **不再依赖 Level 定档**。
> **(2) 授权口径统一**: 上一版把「开三个 issue」自派给「A 侧, A 的 D.2」, 而同一份文件的 §Impact「外部」行
> 逐字写「**无外部动作**」—— **一件事两个口径**, 执行者必须临场裁量该不该做外向动作, 而「临场裁量」
> 正是 O-3 被上提 owner 的理由。⇒ **三个 issue 与 O-3 的评论合并为文首 `D-a` 一次裁定**;
> 归属规则 (谁开 / 去重) 不变, 变的只是**开之前须先有授权**。

---

## Impact

| 文件 | 变更 |
|------|------|
| `aria/skills/phase-c-integrator/scripts/pre_merge_gate.py` | `--remote` / `remote` 参数 (**含 `main()` `:435` 处的 `remote=args.remote` 接线** — 唯一落地点) · `_verify_branch_exists()` (自建私有 runner, 显式 `cwd=`) · `raw_message` 诊断 + `gate_error` additive 键 (经 `_build_output` 新形参产出, §4 已钉死) · 核验点插入 · 🔴 **同批更新 `_build_output` 的 docstring (`:241-246`) 的四类早退枚举 → 五类** (R3 新增: 它是 `SKILL.md:279` 那句枚举的第二份拷贝, 且就在本 change 要加形参的那个函数里 ⇒ 不更新即违反规则 #3; **锚 = `SC-A-note` 的第 (d) 腿**) |
| `aria/skills/phase-c-integrator/tests/test_pre_merge_gate.py` | `SC-A*` 新增用例 (**每条须显式传 `main_branch`**, 见 SC 表的前向兼容前提) · **扩 `_ProbeCacheResetMixin` (`:59-80`) 统一打桩新核验入口** (v1.65.0 同款接缝, 覆盖**触达核验的 19/24** 既有调用 —— 🔴 **R3 动态实测更正**, `:282`/`:301`/`:311`/`:321`/`:524` **五处**结构上够不到核验且必须继续够不到, 三类早退与三条负控 SC 一一对齐, 见 §6) · 需真 git 的 SC 按「打桩边界」表显式退出打桩 |
| `aria/skills/phase-c-integrator/SKILL.md` | **三处, 各有一条机械锚** (R2: 上一版只有 ② 有锚, ①③ **零断言** ⇒ 只改 ② 也 16/16 全绿, 而 ① 恰是 Rule #6 第二行定档的**唯一**承重依据): ① **§C.2.4 执行流程新增编号步骤** (位于步骤 **2** 与 **2.5** 之间, 号建议 `2.2`; **号本身非承重, 承重的是它落在 2 与 2.5 之间**) + **在该步骤处标注本步自身的作用域边界**并指向 `#137` (🔴 **R3 改标注对象** —— 上一版逐字要求「标注它与**步骤 3 硬编码 `main`** 的不一致」, 那是一个会被 B 的 D1 修好的**瞬时事实**, 留着=分发假话/删掉=正确实现下必红, 详见 §残余暴露 的 R3 框) ⇒ **锚 = `SC-A-step`**; ② Output schema json 块 (`:265-277`, 新键紧邻 `path_coverage` `:275`) 增 `gate_error` ⇒ **锚 = `SC-A-doc`**; ③ `:279` 归纳句由**四类早退**扩为**五类** (第五类 = 本 Spec 核验失败: 六键 + `gate_error`, **无** `path_coverage`) ⇒ **锚 = `SC-A-note`**。⇒ 三处合计 **指令流程变动 ⇒ Rule #6 第二行** |

> 🔴 **hunk ① 的两条落地硬约束 (R2 新增, 均由 `SC-A-step` 机械钉住)**:
> **约束 1 — 形态**: 该步骤须写成**参数化的 helper 函数调用**形态 (照步骤 2.5 的
> `evaluate_path_coverage(main_branch, pr_branch)` 与步骤 2 的 `resolve_ci_backend(cfg)`),
> ⛔ **正文不得含任何以 `--` 起头的 CLI flag 字面量 / `aether ci status` / 任何裸命令字面量**
> (🔴 **R3 把第一条由点名 `--main-branch` 升级为类级** —— 点名法对下一个 flag 名天然失明, B 侧
> `SC-M3c` 的 `--pr-branch` 即为实例) ——
> 三条禁令分别对应 B 侧 `SC-M3a`+`SC-M3b`+`SC-M3c` / `SC-M1` / `SC-M15` 的拒绝域,
> 逐条清点见 §残余暴露 的**双向兄弟位置表**
> (CLI 示范形态属 B 侧 D1 的交付物, A 写它是越界在先、撞 SC 在后)。
> **约束 2 — 指向**: 标注只写**本步自身的作用域边界** + 指向 **issue `#137`** 这个稳定外部锚,
> ⛔ **不得引 B 侧的 openspec `change_id`** (R2 tech-lead minor)。两条理由:
> (a) 我实跑 `ls openspec/changes/` —— B 今日名为 `premerge-gate-mainbranch-failclosed`,
> 而 `DEC-20260812-001 §6` 逐字把「B 是改名还是新建 + 归档旧的」列为**未决项** ⇒ 写建议名今日即悬空,
> 写现名则 B 改名后悬空, **两条路都通向悬空引用**;
> (b) `SKILL.md` 是**随 plugin 分发给第三方采用者**的文件, 把他们指向 Aria 内部 change id 对其**恒悬空**
> (memory `memory-store-local` 记的同一形状)。
> ⚠️ 本约束**只改标注的指向对象, 不改 §残余暴露 的闭环判据** —— 闭环判据仍挂 B 侧 D1 (那句在 proposal 内, 不进 `SKILL.md`)。
| `aria/skills/phase-c-integrator/scripts/ci_backends/aether.py` | ⛔ **不入 scope** (§5 钉死; 只引用其 `:38` 常量值)。抽取共享重试 helper **留 follow-up** |
| 外部 | 🔴 **R3 统一口径**: 上一版本行逐字「**无外部动作** —— 不改 #137 body, 不发评论」, 而 §非目标 的 Follow-up 归属表同时把**三个 issue** 派给「A 侧, A 的 D.2」—— **同一份文件对同一类动作两个口径** (R3 code-reviewer)。⇒ **本行改为**: A 的交付面内**零外部写动作**; 潜在的四件仓外写动作 (**在 #137 留 1 条评论 + 开 F-1/F-2/F-3 三个 issue**) **全部归入文首 `D-a`, 由 owner 一次授权**, ⛔ A 不自行决定。⚠️ **无论授权与否, `不得据 A ship 关闭 #137` 这条禁令都成立** (§残余暴露) —— 授权只决定它有没有仓外落点 |
| 发版同步面 | **MINOR 独立发版 ⇒ CLAUDE.md 整张清单照常适用**: `aria` 子模块 5 文件 (`plugin.json` SOT + `marketplace.json` + `VERSION` + `CHANGELOG.md` + `README.md`) + **主仓 gitlink** + 主仓 `VERSION` + root README badge + i18n README (**仅正文实质变更才重译**, #140 B 档) + **Rule #6 AB**。🔴 **R3 更正承载**: 上一版逐字「**Level 2 无 `tasks.md` 承载此清单**」—— 前提已被证伪 (`task-planner` 路径 B 仍出 `detailed-tasks.yaml`, 见文首)。**本行是清单本体的唯一 SOT; 其 A.2 落点 = `## Success Criteria` §交付义务 `O-1`** (路径 B **必读该章节**; 🔴 **R4**: **不**保证为它出一条 TASK, 见下框)。⚠️ **仍无机械兜底** —— 见下方风险声明与文首 `D-b`。不触发 v2.0 弃用删除面 |

> ⚠️ **发版清单的机械承载缺口 (R1 如实标注; R2 上提)**: Level 2 = proposal only ⇒ 上面这张清单**没有 checkbox 承载**,
> 而 custom check `m6-version-badge-match` 比的是 badge ↔ `plugin.json`, **对「主仓 gitlink 未 bump」这个方向
> 结构上失明** (post_planning R3 已实证)。姊妹 Spec B 的 R4 三条 Critical 之一正是 `TASK-017` 漏 gitlink。
> ⇒ **本 Spec 不假装它有机械兜底**。
> 🔴 **R3 更正路由 (上一版的「上提到文首」不构成路由)**: R2 逐字称「A.2 的入口必然读到文首」,
> 但 `task-planner/DUAL_LAYER_SPEC.md:90-93` 把路径 B 的解析内容**穷举为三项**, **不含文首 BLOCKER 块**
> (R3 knowledge-manager; 我实读复核)。⇒ **本清单的落点现为 `## Success Criteria` §交付义务 `O-1`**
> (路径 B 逐字「始终从 proposal.md 读取 `## Success Criteria` 章节」), **文首 BLOCKER 只保留待 owner 裁的
> `D-b` (无兜底是否接受)**。两处都不复述清单本体 —— **清单本体的唯一 SOT 是本行**。
> 🔴 **R4 收窄「载体」二字** (同文首 R4 更正框): 路径 B **必读**该章节是真的, **必然为 O-1 出一条 TASK 不是**
> —— `DUAL_LAYER_SPEC.md:93` 把 `## Success Criteria` 的用途分派为「**验收标准**」(落 `verification:` 字段),
> 全 skill 无一句把 SC 条目转成 TASK。⇒ **移入只买到「A.2 一定看得见」, 没买到机械承载**;
> 这与本框「不假装它有机械兜底」**同向**, 不构成新缺口, 但上一版的「可执行载体」四个字言过其实。
> ⛔ **不得**以「Level 低 / 变更小」自行降级 (规则 #10)。

### 版本

**MINOR。** 全部为 additive: 新增**带默认值**的可选参数 · 新增核验步 (插在既有早退之后, 既有分支语义零改动) ·
新增 **additive 可选**输出键。

**调用点口径 (R1 更正 —— 上一版逐字「既有 24 处 `gate_check(` 调用零改动」漏计第 25 处)**:
三项并列 (memory `critique-repeats-error`) —— **总体** = `aria/` 内可执行的 `gate_check(` 调用点;
**范围** = 基线 `af87cae`; **计数法** = `grep`。
实跑 `grep -c 'gate\.gate_check(' tests/test_pre_merge_gate.py` = **24** (那是"测试内"这个**更小的总体**);
`grep -rn 'gate_check(' aria/ --include=*.py` 在该测试文件之外另得 **7 行** (🔴 **R3 更正列举** ——
上一版逐字只说「另得 `:298` 与 `:435`」, 照它复跑的人会多得 5 行并怀疑口径, R3 code-reviewer):
`pre_merge_gate.py:298` (def, **非调用**) · **`:435`** (`main()` 内真实调用) ·
`ci_backends/base.py:11` `:106` · `ci_backends/github_actions.py:8` `:40` `:48` (**后 5 行全是
docstring/字符串里的提及, 非可执行调用点**, 与本段「可执行的 `gate_check(` 调用点」这个总体一致)
⇒ **真实调用点 = 25**。

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
⇒ Phase B 落地时, 既有 24 处中**触达核验的 19 处** (R3 动态实测) 要么经 §6 的 mixin 打桩隔离、要么显式传真值;
**另 5 处** (`:282`/`:301`/`:311`/`:321`/`:524`) **结构上够不到核验, 且必须继续够不到**
(那正是 `SC-A10` / `SC-A10b` / **`SC-A10c`** 三条负控要钉的 —— `:282` 是 precheck 失败那一类, 上一版漏点名)。
⛔ **两类都不得靠放宽核验来保绿。**

> ⚠️ **版本定档留给 owner 复议的点**: 「一个此前恒 `green` 的闸门开始 `fail`」是否够得上 CLAUDE.md 的
> 「破坏性变更须 MAJOR」? 本 Spec 判 **MINOR**, 理由: 输出 schema 与函数签名向后兼容 (API 形状不变),
> 翻转的是**被修复的缺陷本身**, 且 CLAUDE.md 版本规则把 MAJOR 系于**破坏性契约变更**而非行为修正。
> **该判断是 AI 作出的, 按规则 #10 留痕请复议** —— 若 owner 认为运行时翻转足以拉 MAJOR,
> A 就与 B 的 MAJOR 面重叠, 拆分收益会显著缩水, 须重议划界。

### 测试基线

`phase-c-integrator` 现 **111 tests** (`test_pre_merge_gate.py` 46 + `test_ci_backends.py` 25 +
`test_path_coverage.py` 40) —— **2026-08-11 主 loop 实跑 `111 passed` 确认, 红窗前提成立。**

---

## 承自九轮审计的输入 (逐条注明来源, 供 post_spec 复核)

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
