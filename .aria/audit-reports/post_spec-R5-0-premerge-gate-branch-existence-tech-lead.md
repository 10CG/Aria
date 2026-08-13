---
checkpoint: post_spec
mode: convergence
rounds: 5
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-13T10:40:00.000Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R5 — Spec A `premerge-gate-branch-existence` · 席位 tech-lead

**VOTE: REVISE** · **VERDICT: PASS_WITH_WARNINGS** · **0C + 6M + 4m = 10** ·
本轮 `introduced_by_r4fix` = **7/10 = 70%**

审视角度 (席位): 划界是否自足 / Level 2 与 MINOR 定档 / 与 B 侧的边界有无重叠或缺口。

---

## 0. 本轮我实跑过的命令 (所有数字的出处)

```bash
# SOT 行锚 (R4-fix 新写的四条更正, 逐条复核)
sed -n '24,34p'  aria/skills/spec-drafter/LEVEL_GUIDE.md          # :26 / :29
sed -n '150,166p' aria/skills/spec-drafter/LEVEL_GUIDE.md         # :156-160 / :162
sed -n '114,120p' standards/openspec/project.md                   # :116 / :117
grep -n '模块检测\|模块映射\|检测方法' aria/skills/spec-drafter/LEVEL_GUIDE.md   # 127 / 130 / 135

# 全文件重复锚扫描 (任务书第 4 问)
grep -n '\*\*执行流程\*\*:'            aria/skills/phase-c-integrator/SKILL.md   # [238, 582]
grep -n 'Subprocess 调用规范'          aria/skills/phase-c-integrator/SKILL.md   # [257]  唯一
grep -n '\*\*Output schema\*\*\|\*\*配置参数\*\*:' …/SKILL.md                    # [264,281,501,523]
grep -n '^### C\.2\.4'                 aria/skills/phase-c-integrator/SKILL.md   # [218, 306, 376]  ← 三命中
grep -n 'evaluate_path_coverage'       …/SKILL.md   # [242]  唯一
grep -n 'resolve_ci_backend'           …/SKILL.md   # [241, 319]
grep -c '#137'                          …/SKILL.md   # 0
grep -rn '_build_output' …/scripts/pre_merge_gate.py # 1 def(:232) + 7 调用
grep -n 'def test_sc22\|class _ProbeCacheResetMixin' …/tests/test_pre_merge_gate.py  # 710 / 59

# SC 侧可求值性
python3 -c "re.findall(r'^  \"([A-Za-z_]+)\":', SKILL.md[265:277], re.M)"   # 7 键
sed -n '232,263p' …/scripts/pre_merge_gate.py        # _build_output 6+1=7 键, docstring :241-246 四类
sed -n '264,282p' …/SKILL.md                          # json 块 :265-277, 注记 :279, 配置参数 :281

# B 侧对账
grep -c '^| \*\*SC-M' B/proposal.md                   # 20
grep -c '^| \*\*SC-A' A/proposal.md                   # 18
sed -n '150,165p;340,372p' B/proposal.md              # :154 :156 :158 :161 :345 :358-361 :366-369
python3 -c "yaml.safe_load(B/detailed-tasks.yaml)"    # 21 task · pending 15 / cancelled 6 · 字段恒 12
git show ff847fb:…/detailed-tasks.yaml | sed -n '488p'    # 旧 :488 命中
sed -n '488p' …/detailed-tasks.yaml                       # 今日 = "  verification:"

# O-1 gitlink 证据命令
git diff --submodule=short -- aria                    # 0 行
git show --submodule=short fb5ed36 -- aria            # ±Subproject commit 两行
git show --submodule=short 98ad1f5 -- aria            # 0 行

# 划界洞
grep -cE '分支存在性|main-branch-not-found' CLAUDE.md  # 0
grep -n 'Rule #8\|规则 #8' A/proposal.md               # 唯一命中 :174 (症状陈述)
sed -n '113p;79p;35p' CLAUDE.md
```

---

## 1. R4 的 12M (去重 10) 是否真闭合 —— 逐条回源

| # | R4 finding | 处置 | 我的复核判定 |
|---|---|---|---|
| F-1 (TL) | 「移入 SC ⇒ 路径 B 必然出六条 TASK」不成立 | 已改 | ✅ **真闭合**。`task-planner/SKILL.md:59-67` 逐字复核成立; `DUAL_LAYER_SPEC.md:90-93` 三项各带用途; `grep -rn 'Success Criteria' task-planner/` 实跑 = **2**。四处落点 (`:98-111` / `:155` / `:982` / `:1028-1031`) 口径一致, 均改为「读得到 ≠ 出 TASK」 |
| F-2 (TL+QA+CR) | §非目标 landmine 标注第四份拷贝 | 已改 | ✅ **真闭合**。`grep -n '步骤 3'` 得 8 处, 其中**要求标注**的四处 (`:248` `:355` `:942` `:996`) 口径统一为「只标注本步作用域边界 + `#137`」; `:239-240` 是 proposal 自述残余形态, 非标注要求。**无第五份拷贝** |
| F-3 (TL) | DEC §5.3 owner 裁定被降级为 handoff 备忘 | 已执行 | ⚠️ **半闭合**。文件层面属实 (21 条一条未删 / pending 15 / cancelled 6 / 字段恒 12, 我 yaml 解析复核); 但**「碰撞面已在源头消除」这句被两件事证伪** → Major-2 (TASK-013 重叠) · Major-3 (6 条悬空依赖边) |
| F-4 (TL) | Level (b) 跨模块腿是自造判据 | 已改 | ⚠️ **半闭合**。四条件**枚举**已逐字照 `LEVEL_GUIDE.md:156-160`+`:162` ✅, 但**条件① 的求值仍是自造谓词** → Major-4 |
| F-5 (TL) | Breaking 腿是版本定档的函数 | 已改 | ✅ **闭合**, 依赖声明 + 按序裁写死。但按序裁的**题面**把版本收窄为二选一 → Major-5 |
| F-6 (TL) | `SC-A-step (a)(b)` 过度收口 | **明确不修** | ❌ **理由不成立** → Major-6 |
| M-1 (QA) | `SC-A-note` 锚点在全文件不唯一 | 已改 | ✅ **内层两锚闭合** (`grep` 实测 264/281/501/523, 「章节内首个匹配」规则已写死)。**外层界定锚 `### C.2.4` 仍三命中** → minor-8 |
| M-2 (CR) | `SC-A10c` 与可达前提配方相反 | 已改 | ✅ **真闭合**。`precheck()→(False,…)` 例外补回; 配平 11+2+3+2 = 18, 与 `grep -c '^| \*\*SC-A'` 实跑 **18** 相等, 无重复计数 |
| M-3 (CR) | 两条 SOT 行锚不落在被引文本上 | 已改 | ✅ **真闭合**。`LEVEL_GUIDE.md:26` 实读 = 「YES ▶ LEVEL 1 (Skip)」· `:29` = 「Q2: 是否架构变更/跨模块/Breaking?」· `project.md:116` = Level 1 行 · `:117` = Level 2 行 —— 四条逐字对上 |
| M-4 (CR) | O-1 的 gitlink 证据命令恒空 | 已换命令 | ✅ **真闭合, 且换的是量不是阈值**。三跑实测: `git diff --submodule=short -- aria` = 0 行; `git show --submodule=short fb5ed36 -- aria` = ±Subproject 两行; 对未 bump 的 `98ad1f5` = 0 行 ⇒ 两向可区分 |

**归纳: 10 条里 6 条真闭合 · 2 条半闭合 · 1 条闭合但留残余 · 1 条明确不修且理由不成立。**
**「旧 finding 无一原样复发」这个四轮特征在 R5 仍成立** —— 我未发现任何一条 R4 点名的缺陷被原样留下。

---

## 2. Findings

### M-1 · CLAUDE.md:113 Rule #8 的 SOT 同步在 A/B 划界里**无归属**, 而它的触发点是 A 的 ship (Major, blocks_phase_b, 引入=否)

**locator**: `openspec/changes/premerge-gate-branch-existence/proposal.md:174` (全文唯一一次提 Rule #8) ·
`:204-207` (§Why ⛔ 不在本 Spec 范围清单) · `:990-1017` (§Impact 表, 无 CLAUDE.md 行)

**实测**:
- `grep -n 'Rule #8\|规则 #8' A/proposal.md` ⇒ **唯一命中 `:174`**, 逐字「Rule #8 pre-merge gate 的「main 无 in-flight CI run」这条腿在本项目上**恒真**」—— 症状陈述, 不是义务;
- `CLAUDE.md:113` 逐字「phase-c-integrator C.2.4 验证 **(a) 本 PR CI passing; (b) main 无 in-flight CI run**」= **两条腿**;
- A §2 表逐字新增第三条会 BLOCK 合并的腿: `verdict=fail` + `gate_error.kind="main-branch-not-found"`;
- `grep -cE '分支存在性|main-branch-not-found' CLAUDE.md` = **0**;
- B 侧 `detailed-tasks.yaml` **TASK-016** 逐字 title「**CLAUDE.md 规则 #8 同步 — 新增第三条阻断腿**」, `deliverables: [CLAUDE.md]`, `status: **pending**`, `dependencies: ['TASK-008']` —— 而 TASK-008 (`_verify_branch_exists() 实现 + 插入点`) 正是本轮被标 `cancelled` 迁往 A 的六条之一。其 notes 逐字「本 Spec 改写了 Rule #8 指名的 SOT 段」。

**怎么会红**: A 按 MINOR 独立 ship 当天, `CLAUDE.md:113` 枚举的两条腿与 gate 实际的三条阻断腿不一致
⇒ 直接违反不可协商规则 **#3** (文档与代码必须同步更新)。任何执行者照 A 的 §Impact 表落地, 都**不会**碰 CLAUDE.md ——
表里根本没有这一行, §非目标也没排除它。

**为什么这落在 A 的范围内 (不是搬 B 的 finding)**: A 自己 `:209-211` 逐字立过判据 ——
「二者的触发点都是「**本 change 自己的发版**」。A 按 MINOR **独立发版** ⇒ A 有 A 的那一份, **义务结构上无法转移**给一个至今
「不具备进 Phase B 条件」的姊妹 Spec」。这句用来把发版同步面与 Rule #6 AB 从 B 拉回 A, **逐字同样适用于 Rule #8 SOT 同步**:
使 `:113` 陈旧的是 A 的阻断腿, 不是 B 的 D1。A 既未认领也未排除 ⇒ **划界不自足的实证**。

---

### M-2 · R4-fix 断言「碰撞面已在源头消除」, 但 B 的 **TASK-013 (pending)** 与 A 的 hunk ②③ 是同一份交付物 (Major, blocks_phase_b, 引入=是)

**locator**: A `:316` 与 `:869-872` (「⇒ 碰撞面**已在源头消除**, 不再依赖 handoff 纪律」) · B `detailed-tasks.yaml` TASK-013

**实测 (yaml 解析, 非行号)**: TASK-013 `status: pending` · `deliverables: [aria/skills/phase-c-integrator/SKILL.md]` ·
verification 逐字两条:
1. 「Output schema 块**含 gate_error** 且示例的 branch 用占位符」;
2. 「早退注记**逐字仍是四类** (含 backend query 失败) … **内容锚** =「各早退分支 (no-backend / precheck 失败 / backend query 失败 / enabled:false) 保持六键不变」那句 (行号以 af87cae 为准 = `:279`)」。

而 A §Impact 逐字: hunk ② =「Output schema json 块 (`:265-277`) 增 `gate_error`」· hunk ③ =「`:279` 归纳句由**四类早退**扩为**五类**」。
⇒ **同一个 json 块与同一句注记, A 与 B 各有一条 pending 的交付要求。**

**怎么会红 (两向)**:
- (i) A 先 ship ⇒ B 执行者照 TASK-013 再往 schema 加一次 `gate_error` ⇒ **重复键 / 同行 merge conflict** —— 正是 A 自己为六条 cancelled 任务写下的后果 (「第二份定义 / merge conflict」);
- (ii) B 执行者照 `tasks.md:85` 上游同批的 `tasks.md:96` 逐字「`:279` **四类**早退注记同步 (逐字是四类)」把 A 新增的第五类句**删掉** ⇒ A 的 `SC-A-note` **(b)(c) 转红**。

**为什么 R4-fix 的过户普查漏了它**: 普查的总体是「**规格已整体过户**的任务」(六条), TASK-013 是**部分重叠** ——
它的 verification 一半归 A (schema `gate_error`)、一半归 B (`:270` 示例占位符 / SC-M2)。
A 的表 1 只清点了三条**任务级预写量** (24 处 / 0 处 / 111), 没清点**任务级所有权**; 表 2 (B→A) 更是**连任务级总体都没有**。
⇒ `fix-the-class`: 方向 1 加了「附加总体」, 方向 2 没加。

---

### M-3 · 本轮写入 B 的 `cancelled` 标记, 在 B 的 DAG 上留下 **6 条指向 cancelled 节点的依赖边** (Major, 引入=是)

**locator**: B `detailed-tasks.yaml` (由 A 的 R4-fix commit `f5b845c` 写入) · A `:869-872` 的闭合声明

**实测** (解析 yaml 后逐条求交, 非目视):

```
cancelled = [TASK-003, 004, 005, 007, 008, 009]
PENDING TASK-011 → [003]        # SKILL.md 两处散文收敛 (B 的承重 D1)
PENDING TASK-012 → [009]
PENDING TASK-013 → [009]
PENDING TASK-016 → [008]        # CLAUDE.md 规则 #8 同步
PENDING TASK-020 → [009]
PENDING TASK-021 → [008, 009]   # 终局全量收口
```

**怎么会红**: B 的执行编排对「依赖已 cancelled」无定义 —— 一个执行者判「前置未完成 ⇒ 不可调度」(含 B 的**承重 D1** 与**终局收口**),
另一个判「cancelled 视同满足」⇒ **两个独立执行者得相反结果** (memory `spec-underdetermination`)。
且 A `:872` 逐字「**本段不再承载它** —— 它已在源头消除, 不需要靠 D.2 纪律兜」把交接面也一并撤了 ⇒ 无人接住这 6 条边。

**范围说明**: 我核过这次写入**没有**造成内容损失 —— 我用 yaml 解析对 `ff847fb` 与今日两版做规范化比对,
差异**恰为** 6 条 task 的 `status`+`notes` 与 `metadata`, 其余字段逐字节相等 (606 行删除全部来自 YAML 折行重排)。
本条报的不是内容损失, 是**依赖边未随状态迁移**。

---

### M-4 · Level 条件 ①「涉及 2 个及以上模块」的**求值**仍是自造谓词 —— F-4 只闭合了「枚举」那一半 (Major, blocks_phase_b, 引入=是)

**locator**: A `:18`

**实测**: A `:18` 逐字「① **涉及 2 个及以上模块** = **NO** (代码面全在 `phase-c-integrator` **一个 skill** 内, §Impact 逐行列明)」。
但 SOT `LEVEL_GUIDE.md` **`:127-151`「模块检测」**逐字给出:
- `:130` **检测方法** 三步: 「1. 从需求描述提取模块关键词 / 2. 分析涉及的文件路径前缀 / 3. 检查是否跨模块」;
- `:135-151` **模块映射** 四个模块, 各带关键词与路径前缀: `mobile`(mobile/**) · `backend`(关键词 **Python, FastAPI, API**, 路径 backend/**) · `shared`(shared/**) · `standards`(关键词 **规范, Skill, OpenSpec, 标准, 文档**, 路径 standards/**, .claude/**)。

「skill」**不是** SOT 的模块单位, 它一个字都不在 `:135-151` 里。照 SOT 逐字求值:
- **路径侧**: `aria/skills/phase-c-integrator/**` 对五个前缀 (`mobile/** backend/** shared/** standards/** .claude/**`) **零命中** ⇒ 不可判;
- **关键词侧**: A 的需求描述同时命中 `standards` (「Skill / 规范 / 文档」—— A 改的就是 SKILL.md) 与 `backend` (「Python / API」—— A 改 `.py` 并新增 API 形参) ⇒ **≥2 模块** ⇒ 条件① **YES** ⇒ `:162` 逐字「**自动提升为 Level 3**」。

**怎么会红**: 两个独立复核者照 `LEVEL_GUIDE.md:130-151` 逐字求值, 得到的是「零命中/不可判」或「≥2 模块」,
**没有任何一条路径得出 A 写的 NO** ⇒ owner 在 `D-c` 上拿到的输入是错的。
而 A 自己为条件③ 立的规矩逐字是「**成文条件的解释问题, 不是 AI 的裁量空间**」(规则 #10 + memory `exact-exception-condition`)
—— 同一规矩**未施于①**。若条件① 也上呈, `D-c` 的题面就不是「(b) 的条件③ 待裁」而是「条件① 与 ③ 两条待裁」。

---

### M-5 · 版本定档 (MINOR) 全程未过成文 SOT, 而 R4-fix 刚把「先裁版本」定为第一顺位 (Major, blocks_phase_b, 引入=是)

**locator**: A `:1034-1054` (§版本) · `:165` (按序裁) · `:1075-1079` (留 owner 复议点)

**实测**:
- A §版本 全节的定档理由逐字只有「全部为 additive: 新增**带默认值**的可选参数 · 新增核验步 · 新增 **additive 可选**输出键」+「API 形状层零破坏面」;
  **零引用** `CLAUDE.md:79` 与 `standards/conventions/version-management.md`;
- `CLAUDE.md:79` 逐字「SemVer。Aria 约定: **新增 Skill / Skill 架构重构 = MINOR+; 文档更新 / bug 修复 = PATCH**」——
  A 既非新增 Skill, 又已在 Level (a) 腿上**自答**「**架构变更 = NO**」(`:13`) ⇒ 落不到 MINOR+ 那一桶, 逐字落进「bug 修复 / 文档更新 = **PATCH**」;
- `version-management.md:52-55` Minor 触发条件四项, 末项逐字「**功能增强（向下兼容）**」; `:67-70` Patch 触发条件四项, 末项逐字「**Bug 修复**」——
  **两条同时命中, 且 SOT 无优先级规则** (对比 `LEVEL_GUIDE.md:162` 明写「满足任一 ⇒ 自动提升」);
- **对照**: B 侧 `detailed-tasks.yaml` 的 `ship_target` 字段逐字写「定档依据: **CLAUDE.md:35「破坏性变更须 MAJOR」与 :79「MINOR+」两条下界求交唯一解**」
  —— 姊妹 Spec 做了字段级对账, A 没做。

**怎么会红**: A `:165` 逐字规定「**先版本 (MINOR vs MAJOR), 后 Level (2 vs 3)**」, 题面只给两个选项。
任何照 `CLAUDE.md:79` 逐字求值的裁定者得到的是**第三个选项 PATCH**, 它不在选项集里
⇒ owner 在一个被 AI 预先收窄的选项集上作第一顺位裁定 —— 与 A 自己在 `D-c(i)` 立的判据同款违反。
连带: A `:36-37` 与 §Impact `:1017` 都以「**MINOR 独立发版**」为前提推出整张发版同步面与 O-1, 该前提未经 SOT 检验。

---

### M-6 · ⛔ 不修框的核心理由「改法今日欠定」被本 Spec 自己的 `(c-含)` 腿证伪; 且「不是价值评估」的声明与它自己的理由 1、3 矛盾 (Major, 引入=是)

**locator**: A `:369-392`

**(A) 理由 2 不成立**。它逐字称「『新步骤锚』这个 token **今日不存在** … **在这个 token 定死之前, (a)(b) 的新判据无法写成两个独立实现者会得同一结果的形式**」。
但同一份 Spec 的 `SC-A-step` **(c-含)** 已经把一个**必然出现在新步骤正文里**的 token 钉死了 —— `:786` 逐字「且**含** `#137`」。实测:
- `grep -c '#137' aria/skills/phase-c-integrator/SKILL.md` = **0** (今日零命中 ⇒ A ship 后唯一);
- `grep -c '#137' B/proposal.md` = **9** (`:15 :20 :45 :73 :75 :77 :79 :83 :428`), 我逐行实读 —— **全部**是 issue 归属/闭环讨论与「不得据 A ship 关闭 #137」, **无一**要求把 `#137` 写进 `SKILL.md` ⇒ B 正确落地也不会引入第二个 `#137`;
- 另两个锚在 §C.2.4 内唯一: `evaluate_path_coverage` 全文件 **1** (`:242`) · `resolve_ci_backend` **2** (`:241` 在 §C.2.4 内 / `:319` 在 §C.2.4.X 内)。

⇒ **今日就能写成确定形式**: 按出现位置断言 `resolve_ci_backend` < `#137` < `evaluate_path_coverage`,
配「§C.2.4 内首个匹配」——而这条规则**本轮刚由 `SC-A-note` 现成写下**。
理由 2 的另一半「编 `#137` 则与 (c-含) 腿共用同一 token, 两腿耦合成一个量」**不是失效理由**: 共用 token 只带来冗余
(缺 `#137` 时两腿同红), 不产生欠定; 而 `SC-A-order` 两腿合一、`SC-A-note` (a)(d) 共用 token, A 自己都接受了这种耦合。

**(B) 「这不是价值评估」的声明与自己的理由清单矛盾**。框末 `:391` 逐字「**这不是「不值得改」的价值评估** (那会撞规则 #10), 而是「改法本身今日欠定」」, 而:
- 理由 1 逐字「**在引入率 93% 时新开一条机械判据, 是本轮可选动作里预期新增条目最多的那个**」= 纯成本论证;
- 理由 3 逐字「不补的残余风险**有界**且已定位 … 不会造成假绿」= 纯风险论证。
⇒ 三条理由里只有一条属「欠定」, 而那一条经 (A) 不成立 ⇒ **实际支撑不修的只剩两条价值/风险评估**。

**怎么会红**: Phase B 实施者被本框告知「今日写不成」, 于是不写 —— B 折叠若改用无序列表, (a)(b) 从「必红」退化为「无从求值」;
而按上面的测量点它今日就是 **baseline-failing** 的 (`#137` 今日零命中 ⇒ 必红), 完全满足 A 自己对 SC 的准入标准。

**⚠️ 我对这条的定性**: 我**不认为**「不修」本身撞规则 #10 —— 拒绝一条审计处方并留痕请复议, 与「跳过 enabled 闸门」不是一回事。
我报的是**理由不成立**, 以及**它没进 owner 的待裁点**: `D-a`/`D-b`/`D-c` 三条里没有它, 而 A 自己 `:873-875` 刚刚把
「AI 自作主张的流程判断 ⇒ owner 在三个待裁点上看不到它」认定为要治的形状。**同一形状在同一轮里换了个位置复发。**

---

### m-7 · `detailed-tasks.yaml:488` 两处引用被 R4-fix 自己的写入作废 (minor, 引入=是)

**locator**: A `:327` (表 1) · A `:863` (D.2 handoff 段, 本轮新写)

**实测**: `git show ff847fb:…/detailed-tasks.yaml | sed -n '488p'` = 「- 实测 24 处 gate_check( 调用点、显式传 main_branch 的 0 处 — 补完后应为 24/24」✅ (写下时正确);
今日 `sed -n '488p' …/detailed-tasks.yaml` = `  verification:`; 该句今日在 **`:308`**。
位移由 R4-fix 自己的 commit `f5b845c` 造成 (`--numstat` = 142/606, YAML 折行重排)。
另两条锚仍命中: `tasks.md:85` = TASK-010「既有 **24 处**」✅ · `tasks.md:122` = 「变更前基线 **111**」✅。

**怎么会红**: 照 A 复跑的人在 `:488` 读到 `verification:` 一行, 与被引内容无关 (memory `reporter-miscite`)。
**实质结论不受影响** —— 该句仍在文件里, 只是行号变了。

---

### m-8 · `SC-A-note` 的**外层区块界定锚** `### C.2.4` 在全文件前缀匹配下三命中, 「首个匹配」限定只写给了内层两个锚 (minor, 引入=是)

**locator**: A `:787`

**实测**: A `:787` 逐字「**两个锚一律取 `### C.2.4` 标题行 (今日 `:218`) 之后、下一个 `###` 标题行 (今日 `:306`) 之前的首个匹配**」——
「首个匹配」修饰的是 `**Output schema**` / `**配置参数**:` 这两个**内**锚; 区块界定锚 `### C.2.4` 自身无唯一性限定。
`grep -n '^### C\.2\.4' SKILL.md` ⇒ **三行**: `218` (`### C.2.4 Pre-Merge Precondition Gate`) · `306` (`### C.2.4.**X** CI Backends`) · `376` (`### C.2.4.**5** Submodule Pointer Regression Gate`)。

**怎么会红**: 取末次匹配的实现从 `:376` 起抓 §C.2.4.5 区块 —— **正是本条自己列写的失效形态**「(a) 恒绿、(b)(c) 恒红, 与 A 在 `:279` 的真实编辑是否正确完全脱钩」。
今日的 `:218/:306` 两个行号是唯一的消歧信息, 而**同一条 SC 在 `:356` 逐字自称「本 SC 是内容锚不是行号锚」**。
最小修法: 把界定锚写成「`^### C\.2\.4 ` (**编号后须跟空格**) 的首个匹配」。

**⚠️ 全文件重复扫描的完整结果 (任务书第 4 问)**: `**Subprocess 调用规范**:` = **1** (唯一, 终点锚安全) ·
`**执行流程**:` = 2 (已有「首个」限定 ✅) · `**Output schema**`/`**配置参数**:` = 4 (本轮已加章节内首个匹配 ✅) ·
`evaluate_path_coverage` = 1 ✅ · `resolve_ci_backend` = 2 (§C.2.4 内唯一 ✅) · `#137` = 0 ✅ ·
`def test_sc22…` = 1 ✅ · `class _ProbeCacheResetMixin` = 1 ✅ ·
`_build_output` = 8 处 (1 def + 7 调用), 但 (d) 腿逐字用 `ast.get_docstring`, 与出现次数无关 ✅。
⇒ **该类今日只剩这一个实例。**

---

### m-9 · §4 的「`raw_message` 须**明确区别于「无 in-flight run」**」是承重承诺, 无机械锚, 且**未进** A 自己的「无机械锚」诚实清单 (minor, 引入=否)

**locator**: A `:523-524`

**实测**: A `:523-524` 逐字「失败时须写入人类可读诊断, **含分支名与 remote 名**, 且**明确区别于「无 in-flight run」**」。
SC 表里 `SC-A6` / `SC-A7` / `SC-A8` / `SC-A14` 只断言「`raw_message` **含分支名与 remote 名**」, **无一条**断言后半句。
A 对另外三处无锚承诺 (`SC-A-cwd` 的诚实限制 `:784` · `(c-含)` 措辞 `:260-261` · `SC-A-step (a)(b)` `:390`) 都做了显式声明, **唯独本条没有**。

**怎么会红**: 一个把 `raw_message` 写成 `no in-flight runs found for 'master' on 'origin'` 的实现**同时含分支名与 remote 名**
⇒ SC-A6/A7/A8/A14 全绿, 而 §4 的承重区分被违反 —— 这个区分正是 §症状「两态不可区分」在**人类可见通道**上的那一半;
机读那一半 (`gate_error.kind`) A 自己已声明「全仓零消费者, 本 Spec **不依赖**它发红」(`:546-548`)。

---

### m-10 · §交付义务 放进 `## Success Criteria` **章节**, 与 A 拒绝它们进 SC **表**的理由落在同一份 SOT 上 (minor, 引入=否)

**locator**: A `:837-849`

**实测**: A `:847-849` 逐字「本小节**不入 SC 计数** … 它们**不是可证伪的机械判据**, 混进 SC 表会污染「每条 SC 都带今日实测值」这个性质」;
但 `DUAL_LAYER_SPEC.md:93` 逐字把 `## Success Criteria` **章节**的用途分派为「**验收标准**」, 而 R4-fix 自己 `:100-102` 刚复核确认
「验收标准」的落点是**每条 task 内的 `verification:` 字段**。
⇒ 六条自陈**不可证伪**的义务被路由进 B 路径产出的 `verification:` 面。

**怎么会红**: A.2 路径 B 产出的 `detailed-tasks.yaml` 里出现不可求值的 verification 条目;
A 用来拒绝它们进 SC 表的理由 (memory `falsifiable_evidence_for_binary_acceptance`) 逐字适用于它们进 `verification:` 字段。
计数面本身无误 —— `grep -c '^| \*\*SC-A'` 实跑 **18**, 六条义务行以 `| **O-1** |` 起头不命中 ✅。

---

## 3. 任务书四问的直接回答

### 问题 1 —— R4 的 12M 里修的那些真闭合了吗

见 §1 表。**6 真闭合 / 2 半闭合 (F-3、F-4) / 1 闭合留残余 (QA M-1) / 1 明确不修且理由不成立 (F-6)。**
两条半闭合的共同形状是同一个: **闭合了「写下来的那一层」, 没闭合「它要判的对象那一层」** ——
F-3 改了状态字段却没改依赖边; F-4 抄对了条件却用自造谓词求值。

### 问题 2 —— 引入率与执笔方的可证伪预测

执笔方预测: **总数 14–20 (点估 17) · Critical 0 · Major 5–8 · 引入率 70–85%**。
**我这一席的实测: 10 条 (0C + 6M + 4m) · 引入率 7/10 = 70%。** 逐项评估:

| 预测项 | 我席的证据 | 判定 |
|---|---|---|
| Critical **0** | 我未发现任何 Critical; 与 R2–R4 三轮 0C 一致 | ✅ **准** |
| 引入率 **70–85%** | 我席 **70%**, 落在区间**下沿**, 且远低于 R4 的 93% | ✅ **准, 且「少改」策略确有效** (触点 25→12) |
| Major **5–8** (**全轮**) | **我一席就有 6 条** | ⚠️ **大概率被突破** |
| 总数 **14–20** (点估 17) | 我一席 10 条 | ⚠️ 若各席重叠低, 会偏上限或突破 |

**给 owner 的关键信号 (这条比数字重要)**: 我这 6 条 Major 里, **引入=否的两条 (M-1 Rule #8 划界洞 · m-9 raw_message 无锚) 是四轮 45 席从未碰过的老洞**;
它们浮出来**不是因为多跑了一轮**, 而是因为我换了扫描轴 —— 从「逐句复核文本」换成「**逐条追归属**」(A 的每条承诺归 A 还是归 B、B 的每条 pending task 归谁) 与「**任务级双向清点**」。
M-2 / M-3 也来自同一轴 (B 的任务级构件, 而 A 的表 2 从未建过任务级总体)。
⇒ 与 memory `stop-adding-rounds` 一致: **换新鲜眼睛/换轴 > 加轮**。R5 的边际产出为正, 但产出来自**换轴**, 不来自**轮次**。
若 R6 仍沿同轴复核文本, 我预期回到「换一批同量级 Major」。

### 问题 3 —— 主动留痕自查该不该被计为 finding

**我的答案: 不该, 我没有把它计入。** 三条理由:

1. **交付物里没有假陈述。** 那个编造的计数在发布前已被删除; 我独立复跑三个量 (`evaluate_path_coverage` = **1** · `resolve_ci_backend` = **2** · `#137` = **0**), 与 ⛔ 框留下的更正值**全部一致**。审计判的是交付物, 不是起草过程。
2. **计它会把「诚实」定价为负。** 若自查留痕计 finding, 而静默删除不计, 最优策略就是**不留痕** —— 审计等于在奖励隐瞒。这与本 Spec 反复援引的 `feedback_paper_fix_antipattern` / `predict-then-measure` 方向相反。
3. **它反而是本轮少数可验证的正面证据。** 「起草时写下一个数、随后实跑推翻」这个动作本身正是 memory `critique-repeats-error` 要求的动作, 而且这次它**真的抓住了**一个会污染结论的错值。

**但第二层观察是真的, 且我认为 owner 应该拿到它**: 承载这次留痕的 ⛔ 框有 **24 行 (`:369-392`)**, 其唯一功能是**论证不做一件事**;
而我这轮的 Major-6 恰好整条落在这个框里。⇒ **「拒绝做某事」的论证文本, 与「做某事」的交付文本, 同样是净增审计表面。**
但结论不是「所以别留痕」, 而是: **拒绝应当以一行登记在 owner 的待裁点上 (`D-a`/`D-b`/`D-c` 旁), 而不是以 24 行在原地辩论。**
按这个改法, 本轮 15 条「不修」会产生一份 15 行的待裁清单 (新增表面 ≈ 15 行), 而不是散落在全文各处的若干论证框。
—— 这也正是 A `:58` 逐字「本版明确拒绝修的项与理由, **逐条写在它们各自的位置**, 不集中成清单」这个选择该被复议的地方。

### 问题 4 —— 全文件重复锚扫描

已做, 完整结果见 **m-8** 末段。结论: R4 qa-engineer 抓的那一类**今日只剩一个实例** (`SC-A-note` 的外层界定锚 `### C.2.4`, 三命中),
其余锚点或**全文件唯一**, 或**已加「章节内/首个匹配」限定**。**内层两锚 (Output schema / 配置参数) 确已真闭合。**

---

## 4. 席位结论 —— 划界自足性 / 定档 / 与 B 的边界

**划界自足性: 不自足。** 至少一条由 A 的 ship 触发的义务 (CLAUDE.md:113 Rule #8 SOT 同步) **既不在 A 的交付面, 也不在 A 的 ⛔ 非目标清单**,
落在两个 Spec 之间; 而 A 自己 `:209-211` 已经写下了判断这类归属的正确判据 (「触发点是本 change 自己的发版 ⇒ 无法转移」), 只是没用它扫一遍全部承诺。

**定档: 两个档位都建立在自造谓词上, 且方向相反。**
Level 的**条件枚举**已逐字过 SOT (R4-fix 的真进步), 但**条件① 的求值**没有 (M-4);
版本档**整节**没过 SOT (M-5), 而 R4-fix 刚把版本裁定放到 Level 裁定**之前** —— 越前的那个输入越没经过字段级对账。

**与 B 的边界: 有重叠也有缺口, 且都在「任务级」这一层。**
重叠 = TASK-013 (M-2); 缺口 = TASK-016 所承载的 Rule #8 同步 (M-1) + 6 条悬空依赖边 (M-3)。
A 的双向清点表在 **SC 级**做得很扎实 (我逐条复核 B 的 20 行 SC 与 A 的 18 行 SC, 表 1/表 2 的实质判定我未发现错误);
**它只在 A→B 方向补了「任务级附加总体」, B→A 方向没补** —— 三条 Major 全部落在这个未建的总体里。

**投票 REVISE 的理由**: 6 条 Major 中 4 条 `blocks_phase_b`, 其中两条 (M-4 / M-5) 直接污染 owner 在 `D-c` 与「先裁版本」上的输入,
一条 (M-1) 是规则 #3 的实质违反面, 一条 (M-2) 会在 A ship 当天产生跨 Spec 的重复交付。

**⚠️ 我未做的事 (如实标注)**: 我**没有**重跑 A 的 18 条 SC 的对抗性 fixture (「1 好 + N 坏」);
`SC-A-doc` / `SC-A-note` 的今日取值我实跑复核了 (doc 侧 7 键 == code 侧 7 键; 两处枚举各恰 4 项且三个 token 零命中 ⇒ baseline-failing 成立),
但**拒绝能力**我只对 `SC-A-note` (a) 做了推理复核, 未构造坏实现实跑。
