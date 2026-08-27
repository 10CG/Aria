---
checkpoint: post_spec
round: 5
role: skill-reviewer
verdict: REVISE
scope_ok: true
counts: 4C/10M/4m
---

# post_spec R5 — a1-entry 三份 Spec — skill-reviewer 席 (Claude Code Skill 指令面质量)

> **⚠️ 落盘说明**: 本席工具集仅 `Read/Grep/Glob` (无 `Write`/`Bash`), **无法自行写盘**;
> 回执由**主控代为落盘**并逐条复核 (复核见各条下方)。本席无法跑 `git show`, 改以已 checkout 的 `aria/`
> 工作树实读; **间接佐证工作树 == `d50f9c3`**: 三份 Spec 断言的行号逐条实读**全部命中, 无一漂移**
> (`phase-a-planner:9` / `spec-drafter:10` / `branch-manager:146` / `phase-b-developer:86,88,92` /
> `state-scanner:149,178` / `config-loader:134,140` / `execution-modes.md:84,113` / `phase1_gate.py:1191` / `spec-drafter:429`)。
>
> **本席是四轮以来第一个从「SKILL.md 作为 AI 运行时真读的指令面」这个维度审的席位。**

**counts**: 母 2C/6M/2m · 字段 1C/2M/1m · 探针 1C/2M/1m · **combined 4C/10M/4m**

## 🔴 母 C1 — rule6_note「实数 6 处」漏 5 个处方性 hunk, 且按**文件目录**划范围违反 Rule #6 逐字判据

`proposal.md:591` 写「本 Spec 涉及的 **SKILL.md / frontmatter** 改动 = 实数 **6** 处」, 而 Impact 表实际要改的
AI-可读面 = **11 hunk / 9 文件**: 漏了 `phase-b-developer/SKILL.md:92` · `branch-manager/SKILL.md:146` 块 ·
`phase-d-closer/SKILL.md:51-52,:55` · `references/layer-l-integration.md:15,:45` · `docs/coordination-ref-schema.md §3.2`。

**为什么是 Critical**: 漏掉的三处 SKILL.md hunk 改的是 **`--raw-track-id "<…>"` 占位串** —— AI 逐字复制进命令行的字面,
纯处方性·运行时指令面。CLAUDE.md Rule #6 判据表逐字「**不按文件目录判**」, 而 `:591` 恰恰按目录划了范围。
三处的 AB 套件**均实存** ⇒ 应落第二行「照跑, 零裁量」, **现在一档没有**。

**主控复核**: 成立。

## 🔴 母 C2 ⭐ — 「照跑现有 AB」会让 benchmark 对**生产** `refs/aria/coordination` 产生真实 push

三腿实测:
- `lib/coordination_ref.py:322` 逐字 `push: bool = True`; `:347` 逐字 `git push <remote> refs/aria/coordination`;
- `phase-b-developer/SKILL.md:97-98` 逐字「"无 coordination 基础设施"**不是**有效 skip 条件, **write_claim auto_bootstrap 会自动建 ref 并 push 到项目 origin**」;
- `ab-suite/phase-a-planner.json` eval **id 1** prompt 逐字 `Execute Phase A for new feature: Add OAuth2 social login support (GitHub + Google). No existing spec. Run A.1 → A.2 → A.3 in sequence.` —— **真实 feature, 不命中任何 skip 条件**。

⇒ C1 扩权后 `phase-a-planner` 持 `Bash`, 正文又新增「A.1 起草前**必调** `phase1_gate.py`」⇒ **跑 AB 套件即在 benchmark 容器里执行真 claim 写入 + 真 push**,
污染生产 coordination ref。正是 memory `sync≠push-auth` 点名的形状。

**处方**: rule6_note 的「照跑」档各加硬前提「**跑本套件前 harness 必须置 `state_scanner.coordination.enabled = false`,
或在无 `origin` 的临时 fixture 仓内跑**」, 并同批写进 `AB_TEST_OPERATIONS.md` 的该套件条目;
新增 **SC-34 (代码)**: 断言 `AB_TEST_OPERATIONS.md` 内两条目各含字面 `coordination.enabled = false`; baseline 必红。

**主控复核**: **三腿逐字实读全部确认。这是本轮最有价值的发现** —— 四轮审计无人看过「扩权 + 新指令」与
「照跑现有 AB eval 的**实际 prompt**」的交互。**且它与三份 Spec 的收敛无关, 不该被收敛节奏挟持 (见本席建议 (c))。**

## 🟠 母 M1–M6 / m1–m2 (摘要, 全部带实读证据)

- **M1** SC-22 ③ 把**本 Spec 自己在 §2.2 ③ 证伪过**的「编排层记忆」谓词复制进两个新落点, 且带「**或等价的**」逃逸口 ⇒ 幂等靠一条不可机械判定的记忆断言, 而 `:384` 逐字「没有它, 一次 A.1 会写两条 claim + 两次外向推送」。**处方**: 改为「含逐字串 `check: coordination ref 内按 (container_id, session_id) 定位到本 session 的 active claim` 且含字面 `claims/`」, **删去「或等价的…」整个括号**。
- **M2** 新锚点在三份 SKILL.md 造**同名标题**, 而既有那份 (`branch-manager:146`) 标题里逐字写着 `Part A1` 但块内命令是 `--phase B` 且**无 `--linked-issue`/`--include-terminal`** ⇒ AI grep 到它照抄即主机制零输入。**处方**: SC-22 ① 正则加 `[^\n]*A\.1`, 加 ④「块内不得出现字面 `--phase B`」; Impact 补一句 `branch-manager:146` 的 `Part A1` 须改 `Part B1` 或删。
- **M3** `phase-a-planner/SKILL.md:62-99` 的 A.1 全部动作在**单个 ```yaml 围栏块**内, 而 SC-22 ① 要求新标题**不在围栏内** ⇒ 按 YAML 表执行的 AI **没有任何指针**指向那个前置标题 —— 与 §Why 引 R3/M6 论证的「埋进长列表会被静默跳过」是**同一病的镜像**。**处方**: SC-22 加 ⑤, 要求围栏内 `A.1 - Spec 管理:` 项下含逐字 `precondition: 见「前置: REQUIRE claim」小节 (MUST, 在本表之前执行)`。
- **M4** Level 1 路径 (`phase-a-planner:67` `skip_if: complexity: Level1`) 下前置 claim 跑不跑**无定义**; 若跑 ⇒ 每个 typo 修复写一条 claim + 一次外向 push 且**永不 release ⇒ 僵尸 claim**。实测 `ab-suite/spec-drafter.json` eval **id 1** 正是 `判断规范等级: 用户请求 '修复登录页面一个 typo'` ⇒ 照跑时两臂不可辨。**处方**: §2.5 skip 条件补「判定 Level 1 ⇒ 前置 claim 零调用」+ SC-9 补该臂。
- **M5** SC-22 的「**步骤块**」边界全文未定义 ⇒ ②③ 退化为全文 `assertIn` (把四个字面量写进 `## 相关文档` 也绿) —— 与 SC-22 自己批判裸 `assertIn` 的理由同形。**处方**: 加边界定义句 (标题匹配行起至下一个 `^#{1,4}[ \t]` 行止, ②③④⑤ 只在该切片求值)。
- **M6** `state-scanner/SKILL.md:178` 逐字「完整设计意图 (…acquire_claim+heartbeat+release 调用关系…) 见 references/layer-l-integration.md」, 而 Impact 把 heartbeat 全部设计放进 **SKILL.md**、对该 reference **只**要求订正既有错误 ⇒ `:178` 变**假指针** (memory `delegate-verify`)。**处方**: 把三级回落表 + 遥测分区边界 + fail-CLOSED 谓词整体落 reference, SKILL.md 缩为「触发条件一句 + CLI 一行 + fail-soft 一句 + 指针」。
- **m1** 「A.0 已被占用」的措辞把**标题锚点**与**散文标签**混为一谈: 实读 `spec-drafter` 全部 `^#{1,6} ` 标题里**无任何 `A.0`** (只在 `:30`/`:369` 的条目与流程图行内)。更强的真实理由是「`A.0` 在十步循环 SOT 里 = state-scanner, 而本步骤发生在 **A.1**」。
- **m2** SC-22 ① 的 `text` 未绑定文件; 若拼接 `skills/**/SKILL.md`, `branch-manager:146` 会让断言 **baseline 即绿**。**处方**: 写死两个文件路径逐一断言。

### ✅ 本席核验为真、无 finding (下轮免重复)
`--phase A.1` **不会被 argparse 拒** (`phase1_gate.py:1191` 无 `choices=`, 只有 `--mode` 有) ·
`grep -rn "前置: REQUIRE claim" aria/` 全仓**恰 1 命中** (= `branch-manager:146`) ⇒ 新锚点在两个目标文件里**未被占用** ·
两处 `allowed-tools` 逐字与 Spec 断言一致 · `DEFAULTS.json` grep `coordination` = **0** (描述性档 baseline 必红属实) ·
`test_coordination_default_lockin.py:53/:55/:56` 确为两条裸 `assertIn` · `execution-modes.md` 全文 grep `state-scanner` = **0** (§2.2「审计轮内不触发」属实)。

## 🔴 字段 C1 ⭐ — AI 运行时真正复制的模板不在变更面内, 且被本 Spec 的条款**明令禁止修**

实读 `spec-drafter/SKILL.md:127-162` 的 `### Level 2 预览` 围栏 —— 那是一份完整 proposal 骨架, 头部**只有两行**
(`:139` `> **Level**` / `:140` `> **Status**`)。而 SOT `standards/openspec/templates/proposal-minimal.md:3-5` 是**三行**
(多 `Created`), 且 SOT 有 `## Impact` 段而预览骨架**没有** ⇒ **内联骨架已与 SOT 漂移两处**。

**这份内联骨架才是 AI 渲染预览时照抄的对象**, 不是 standards 模板。而本 Spec `:557` 逐字
「声明该字段为必填 + 写法引本 Spec §3; **不重复模板正文**」⇒ **落地后预览骨架仍不含「关联 Issue」行**,
AI 产出的 proposal 大概率缺字段 ⇒ **本 Spec 的立项目标 (提升字段可得性) 在主路径上不成立**; SC-7 的正确臂在预览环节即失效。

**处方**: Impact `:557` 拆两 hunk —— hunk A 保持正文声明; **hunk B (新)**: 预览围栏内 `:140` 后插
`> **Created**: {YYYY-MM-DD}` 与 `` > **关联 Issue**: `无` ``, 并把「不重复模板正文」限定为
「不重复 SOT 的 `## Why`/`## What`/`## Tasks` 等**正文段**; 头部 blockquote 因是**运行时被复制的预览骨架**属例外, 须与 SOT 逐行对齐」。
**SC-7 加代码臂 (SC-7a)**: 断言预览围栏内含逐字 `> **关联 Issue**:`; **baseline 必红** (实测该文件 grep `关联 Issue` = **0**)。

**主控复核**: **逐条实读全部确认** (`:139-140` 两行 / SOT 三行 / SOT 有 `## Impact` 而预览 grep = 0 / 全文 `关联 Issue` = 0)。**成立且严重。**

## 🟠 字段 M1 / M2 / m1

- **M1** `:429` 被当作「委托契约」是**过读**: 实读 `spec-drafter/SKILL.md:424-433` 的 `## 相关文档` 是**纯链接清单**, `:429` 与「十步循环概览」「state-scanner」并列, **无任何祈使语气**。而 C1 的漂移实测恰好**证伪**了「它委托给 standards」——**它不委托, 它有自己的副本, 而且副本已经旧了。**
- **M2** `无` 是 **CJK-only 哨兵**, 撞跨项目分发面: 实测 `ab-suite/spec-drafter.json` eval **id 2** prompt 明确要求「生成**英文** proposal」⇒ 合规实现必须往英文 proposal 里写一个汉字; 写 `None`/`N/A`/`none` 一律判 `BAD_TOKEN` ⇒ 照跑时该 eval 两臂语义冲突。**属 owner 权限面, 按 Rule #10 上呈不自裁**: (i) 哨兵集扩为 `{"无","none"}` / (ii) 维持 `无` 但 SOT 与 SKILL.md 各加「英文 proposal 亦同, 不得译写」并同批更新该 eval 的 expectations。
- **m1** 与母 Spec 同文件的 hunk 归属未钉死 ⇒ 补一句「frontmatter `:10` 的 `allowed-tools` hunk **归母 Spec, 本 Spec 一字节不碰**; 正文 hunk 二者物理不相邻, 任意顺序 merge 无冲突」。

## 🔴 探针 C1 — audit-engine 侧唯一被机械钉住的指令是一个**9 字名词短语**

Spec `:370-371` 要求插入的字面串是 **`每轮入口: 竞品 spec 探针`** —— 无动词、无脚本路径、无参数、无 verdict 消费;
**SC-17 的断言就是「全文计数恰 2 次」**。SKILL.md 侧 (Impact `:513`) 只要求「新增小节 + 与 Step 0 消歧」,
**未规定该小节须含任何字面量, 全表无对应 SC**。
⇒ 一个「插两行短语 + 写一段消歧散文」的实现 **SC-17 全绿**, 而运行时 AI 无从知道跑什么命令。
唯一钉消费措辞的 **SC-16 是行为类, 宿主是尚不存在的 `ab-suite/audit-engine.json`** ⇒ 本 Spec 的**全部指令面保障**
压在一个「A.2 才建、且 Rule #6 要求必须经 `/skill-creator` 产出」的套件上 —— memory `feedback_completion_signals_vs_runtime_invocation` 的形状。
**处方**: (i) 插入串改为可执行形 (含脚本路径 + 两个参数 + verdict 三档消费, 两块仍逐字相同故 SC-17 计数不变);
(ii) 新增 **SC-19 (代码)**: SKILL.md 该小节须含四个字面量 `sibling_spec_probe.py` / `verdict` / `not_established` / `未能核实` 且标题行不在围栏内; **baseline 必红**。

## 🟠 探针 M2 / M3 / m1

- **M2** 同一文件内两处**相反指令**: `:156-163` 逐字「本 Spec 采用该模式, **逐字钉死**」+ 给出 `sys.path` 代码; 而 Impact `:519` 逐字「跨 skill 复用的形态**待 A.2 定**…复制或 import 由 A.2 定」。**根因: 主控 R4 的 import 补丁块落盘时没有回灌 Impact 段** —— memory `fixes-contradict` 的接缝形状。**处方**: `:519` 整段替换为指向 §3 + 追加「`resolve_enforced_remotes` 亦经同一路径 import, 不得复制」。
- **M3** 指令面被拆到三个文件且**无一处含完整调用契约**, 与本 skill 既有 progressive-disclosure 体例 (`audit-engine/SKILL.md:236-237` 逐字「权威可执行版见 references/…」) 相反; **最承重的 stdout 契约 (§7 十二字段) 无落点**。**处方**: SKILL.md 放概述 + 指针, `execution-modes.md` 新增一节承载 §7/§9 契约。
- **m1** SC-17 的「恰 2 次」保守性只写在「新表面」段, **没写进 §8** (实现者读 §8 落地) ⇒ §8 表下补一句。

## 收敛判断

**1. 母 Spec 已过边际产出拐点。** 本席 8 条 finding 中 **6 条落在 R3/rework v3/R4 自己新写的条款上**
(C1 rule6_note 整段重写 · C2 「照跑」是 R1-rework 订正后的处置 · M1 SC-22 ③ 新增 · M2 锚点本轮换名 ·
M3 「标题级而非 YAML 列表」是 R3/M6 的 fix · M5 SC-22 边界新增) ⇒ **6/8 = 75% > 1/2**, 命中
memory `marginal-return-negative` 的判据 (判据是「本轮 fix 引入的占比」, 不是数字是否归零)。
且 M1↔§2.2③、M3↔§Why/R3-M6、M5↔SC-22 自己批判裸 `assertIn` 的理由, **全是同一份 Spec 内部自我矛盾** ——
不是「审得不够」, 是**执笔端在自己的修复路径上复现要治的病** (memory `fix-recurs-in-fallback`, 已四次实证)。**再加一轮 = 换一批同形缺陷。**

**2. 三份的 4 条 Critical 里有 3 条是同一个类级缺陷** (母 M1/M5 + 探针 C1 + 字段 C1 的共同形状 =
**「机械断言钉住了指令的外形, 没钉住指令的可执行性」**) ⇒ 应一次性统一处置 (memory `fix-the-class`):
在母 Spec 新增 **D17「SKILL.md 指令块的机械断言三要件」** —— ① 块边界逐字定义; ② 块内须含**至少一条可直接执行的完整命令行**而非概念名;
③ 块内须含 fail 分支的**消费措辞字面**。两子 Spec 各引用 D17, 不各自重发明。**一处定义消掉三处 Critical。**

**3. 两份子 Spec 已在重复母 Spec 的接缝病** (探针 M2 与母历史上的「Impact 与正文两读」逐字同形;
字段 M1 与 memory `delegate-verify` 逐字同形) ⇒ 换执笔席不会自动解决, 须把 D17 与 `delegate-verify` 写进起草约束。

**4. 给 owner 的选项 (列全, 不预设)**:
- **(a)** 母 Spec **停止审计轮**, 4C/10M 交**执笔席之外**的人一次性落 (memory `fix-writer-bottleneck`), 落完只做**一次机械核验轮** (跑全部「怎么会红」的负控), 不再多席主观审;
- **(b)** 先落 D17 类级处方再让三份各自吸收;
- **(c)** **把 C2 (AB 外向 push) 单独抽出先行处置** —— 它是唯一一条「不修就会在跑 benchmark 时污染生产 `refs/aria/coordination`」的条目, 与三份 Spec 的收敛无关, **不该被它们的收敛节奏挟持**;
- **(d)** 维持现状再跑 R6 —— **本席不推荐** (第 1 点的 75%);
- **(e)** 本席**没有**看到「合并三份回一份」的必要性证据: 三者收敛面确实不同, owner 08-23 方向 b 的拆分判断**在本轮实读下仍然成立**;
  但 memory `split-makes-seams` 点名的接缝缺陷**已出现两处** ⇒ 建议 A.2 前做一次**只看接缝**的跨文件核验 (任一侧执笔席都看不见)。

**本席未修改任何被审文件** (结构上不可能 — 无 Write/Edit/Bash)。
