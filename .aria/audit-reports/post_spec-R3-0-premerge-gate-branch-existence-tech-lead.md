---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-12T17:40:00.000Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R3 — tech-lead — Spec A `premerge-gate-branch-existence`

**VOTE: REVISE** · **VERDICT: PASS_WITH_WARNINGS** (0C + 6M + 2m) · 5 条 `blocks_phase_b`

席位视角: 划界是否自足 / Level 2 与 MINOR 定档 / 与 B 侧的边界有无重叠或缺口。

---

## 0. 我实跑过的命令 (所有数字的出处)

```bash
git rev-parse HEAD                                    # 017eb54 (R2-fix)
git -C aria rev-parse --short HEAD                    # af87cae  ← 与 proposal 声明基线一致
cd aria/skills/phase-c-integrator && python3 -m pytest tests/ -q   # 111 passed  ← §测试基线属实

# SC-A-step 的今日基线 (逐字复跑其判据)
grep -n '^\*\*执行流程\*\*:\|^\*\*Subprocess 调用规范\*\*:' SKILL.md   # 238 / 257 / 582 ← 锚属实
sed -n '238,257p' SKILL.md                            # 编号序列 = 1. 2. 2.5. 3. 4. 5. 6. ⇒ (2,2.5) 内零编号 ⇒ 今日必红 ✅

# SC-A-doc 的两条解析规则 (逐字复跑)
python3 -c "json.loads(<:265-277 块>)"                # JSONDecodeError: Expecting ',' delimiter: line 2 column 22 ✅
python3 -c "re.findall(r'^  \"([A-Za-z_]+)\":', blk, re.M)"   # 恰 7 键 ✅ 与 _build_output 今日实产 7 键相等 ✅
sed -n '232,263p' scripts/pre_merge_gate.py           # 六固定键 + path_coverage 条件加键 = 7 ✅

# SC-A-note 的今日基线
grep -n '各早退分支' SKILL.md                          # 唯一命中 :279, 括号内恰 4 项, 无 main-branch ✅ (a) 今日绿
grep -n 'gate_error\|无 path_coverage' SKILL.md       # 零命中 ⇒ (b)(c) 今日红 ✅

# 可达前提
sed -n '325,348p' scripts/pre_merge_gate.py           # :328 enabled / :338 backend is None → _no_ci_output / :345 precheck ✅
sed -n '424,445p' scripts/pre_merge_gate.py           # main() 无 --remote, gate_check 调用无 remote=, return 0 ✅

# B 侧对撞面
grep -n 'SC-M' openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md   # SC-M1..M18 (M3 拆 a/b/c)
sed -n '343,364p' .../mainbranch-failclosed/proposal.md   # 逐条实读 SC-M1/M2/M3a/M3b/M3c/M15/M16/M18/M4/M5
sed -n '155,165p' .../mainbranch-failclosed/proposal.md   # :161 D1 折叠步骤 1-5 逐字属实 ✅
grep -c -- '--pr-branch' aria/skills/phase-c-integrator/SKILL.md   # 0

# 本轮新增的三处回源 (下面三条 finding 的出处)
sed -n '570,600p' SKILL.md                            # C.2.5 执行流程六步, 逐字无 gitlink bump
sed -n '183,196p' SKILL.md                            # C.2.4.5 submodule gate: no-change ⇒ PASS
sed -n '50,68p' aria/skills/task-planner/SKILL.md     # A.2.1 路径 B: 无 tasks.md ⇒ 从 proposal.md 分解 ⇒ 出 detailed-tasks.yaml
for d in openspec/archive/*/; do [ -f $d/detailed-tasks.yaml ] && [ ! -f $d/tasks.md ] && echo $d; done   # 4 例
grep -m1 -i 'level' openspec/archive/2026-05-29-aria-context-monitor/proposal.md   # "**Level**: 2 (Minimal — proposal.md only …)"
grep -c 'TASK-' openspec/archive/2026-05-29-aria-context-monitor/detailed-tasks.yaml    # 31
grep -c 'TASK-' openspec/archive/2026-07-22-state-scanner-gate-yaml-datasource/detailed-tasks.yaml  # 28

# pytest 捕获模式对 SC-A14 腿 2 的影响 (受控探针)
python3 -c "print(sys.stdout.errors)"                 # strict        (裸 python)
pytest <probe> -q            (默认 fd 捕获)            # TYPE=EncodedFile  ERRORS=replace  ⇒ 写孤立代理码位 **不抛**
pytest <probe> -q --capture=sys                       # TYPE=CaptureIO    ERRORS=strict   ⇒ 抛 UnicodeEncodeError
find aria -maxdepth 4 -name 'pytest.ini' -o -name 'pyproject.toml' -o -name 'setup.cfg'   # 零命中 ⇒ 默认 fd 捕获生效
```

**A 承自九轮的事实层面, 本轮第三次回源, 无一条需要下调。** R2-fix 引入的所有**数字**我逐个复跑,
**全部属实**: doc 侧 7 键 / code 侧 7 键 / `json.loads` 确实失败 / 编号序列 `1. 2. 2.5. 3. 4. 5. 6.` /
`--main-branch` 全文件零行 / 两套 ab-suite 均在 / 111 passed / 基线 SHA `af87cae`。
**本轮的 6 条 Major 全部不是数字错, 而是「这个数/这条委派要判的那件事, 在目标处不成立」。**

---

## 1. R2 的 13M 是否真闭合 —— 区分「写下来」与「闭合」

我按本席 R2 报告的 5M+3m 逐条回源 (aggregate 的另 8 条 Major 由其余四席提, 我只对我能实测的部分表态)。

| R2 finding | R2-fix 的处置 | 真闭合? |
|---|---|---|
| **M-1** hunk ① 零机械锚 (Rule #6 第二行唯一承重依据) | 新增 `SC-A-step` 三腿 + 对抗性验证 (1 好 + 5 坏) | ✅ **真闭合**。我复跑今日基线 ⇒ (a) 红; 三腿各自可红我逐条核过。**但 (c-含) 这条腿新造了一个反向 landmine → M-3** |
| **M-2** 与 B 侧 `SC-M3a` 对撞 | 取 (i) 写死「新步骤不得含 `--main-branch`」+ 收进 `SC-A-step` (c) | ✅ **真闭合**, 且拒绝 (ii) 的论证我认可 (见 §3)。**但清点本身不穷尽 → M-4, 且方向单一 → M-3** |
| **M-3** `SC-A-cli`/`SC-A-cwd` 的 backend ambient | 新增「可达前提」块, 一次性定义适用集 10 / 例外 3 / 不适用 3 | ✅ **真闭合**。10+3+3+2(元断言) = **18** = SC 表行数, 我逐条点过无遗漏; `_no_ci_output` 默认 green 与 `resolve_ci_backend` 模块级可打桩两条我实读确认 |
| **M-4** `SC-A-doc` 代码侧操作数未定义 | §4 钉死 `gate_error` **必须经 `_build_output` 产出** + 两条解析规则 | ✅ **真闭合**, 两条规则我逐条复跑属实。**但它把 `_build_output` 拖进 A 的改动面, 而该函数 docstring 是第四处未上锚的落点 → M-6** |
| **M-5** Level 2 三项义务零承载 | 上提为文首 🚧 BLOCKER 块 + 两条出路 | ⚠️ **只完成了「写下来」与「换位置」, 没有闭合** —— 两条出路**都**建立在未回源核验的前提上 (→ **M-1 / M-2**)。这是本轮最典型的「写下来 ≠ 闭合」 |
| **m-1** follow-up 归属 | F-1/F-2/F-3 + 去重规则 + 如实标注单向性 | ✅ 真闭合 |
| **m-2** AB 套件有效性限定未继承 | 逐字继承 B `:383` + 反向假绿说明 | ✅ 真闭合 (两套件我实测均在) |
| **m-3** 标注指向 B 侧 change_id 会悬空 | 改指 issue `#137` + 两条理由 | ✅ 措辞闭合。**但改指 `#137` 恰是 M-3 的成因之一** —— 见下 |

⇒ **本席 8 条中 7 条真闭合、1 条 (M-5) 只完成路由。旧 finding 无一复发** ——
与 B 侧四轮、A 侧两轮的同一观察一致: **执笔不是瓶颈, 新表面才是** (memory `marginal-return-negative`)。

---

## 2. Findings

### M-1 · 🔴 BLOCKER 块的承载前提在 `task-planner` 处被证伪: **Level 2 并非「无 task 载体」** (blocks_phase_b)

**Locator**: `proposal.md:29-49` (🚧 BLOCKER 块) × `:587-588` (F-1/F-2/F-3 同一句) × `:618` (§Impact 风险声明)
× `aria/skills/task-planner/SKILL.md:52-66` × `aria/skills/phase-a-planner/SKILL.md:237-238`

BLOCKER 块逐字: 「Level 2 ⇒ A.2/task-planner **不出** `tasks.md` ⇒ 下面三项义务的**唯一载体**是一份 D.2 就会被
归档的散文」; 三项义务的「今日的唯一载体」列逐字全是「§X 的散文」; 两条出路逐字是
「**(i)** 保持 Level 2 —— 接受『三项只在本文件留痕』」 / 「**(ii)** 取 Level 3 —— 出 `tasks.md`, 三项各出一条 task」。

我去目标处实读 `task-planner/SKILL.md` §A.2.1 (`:52-66`), **逐字**:

```
读取策略:
  IF tasks.md 存在:
    → 路径 A: 解析 tasks.md (OpenSpec 标准格式)
    → 输出: 双层架构
  ELSE:
    → 路径 B: 从 proposal.md 分解任务
    → 输出: 仅 detailed-tasks.yaml
  始终从 proposal.md 读取 ## Success Criteria 章节
```

**「无 `tasks.md`」触发的不是「无载体」, 而是路径 B ⇒ 仍产出 `detailed-tasks.yaml`** —— 一份带
`TASK-{NNN}` 编号与逐条 status 的机读任务载体, 正是 post_planning 审计消费的那个文件。
`phase-a-planner/SKILL.md:237-238` 的示例逐字亦是「A.1: 创建 **Level 2** Spec → …; A.2: 分解为 5 个任务」。

**实证 (不是推断)**: 本仓 `openspec/archive/` 133 个归档里, **4 个有 `detailed-tasks.yaml` 而无 `tasks.md`**;
逐个核其 frontmatter —— `2026-05-29-aria-context-monitor` 逐字「**Level**: 2 (Minimal — proposal.md only …)」,
其 `detailed-tasks.yaml` 有 **31** 条 `TASK-`; `2026-05-30-ai-native-estimator` 逐字「**Level**: 2」, **21** 条;
`2026-07-22-state-scanner-gate-yaml-datasource` 逐字「**Spec Level**: 2」, **28** 条。

**它在什么实现下会红 / 怎么被证伪**: 直接跑 A.2 即证伪 —— Level 2 的 A 会拿到一份 `detailed-tasks.yaml`,
而 BLOCKER 逐字断言「唯一载体是散文」。**危害不在措辞**:

1. **owner 被要求在一个错误的二选一上裁定** —— (ii) 的代价被写成「A 的交付面变大, 拆分收益缩水」,
   而真实情况是**保持 Level 2 也能拿到逐条 task 载体**, 二者的成本差远小于文中所述;
2. **真实缺口被这句话遮住了, 而它是可修的**: 路径 B 逐字「**始终从 proposal.md 读取 `## Success Criteria` 章节**」
   —— O-1/O-2/O-3 与 F-1/F-2/F-3 **全部不在** `## Success Criteria` 里 (在 §Impact / §Rule #6 / 文首 BLOCKER),
   能否被分解成 TASK **取决于它们写在哪一节**, 与 Level 无关。最小修法是 Level 2 内可做的:
   把六项写进 A.2 必然读到的位置, 而不是升 Level。

⚠️ 这条**不是**指控 A 违反规则 #10 —— A 留痕请复议, 程序正确。指控的是: **留痕的内容在目标处不成立**
(memory `delegate-verify`: 写「由 X 保证 / X 不做这件事」前必去 X 源码核三件事)。

**introduced_by_r2fix: false** —— 同一前提的更早版本在 R1-fix `:394` 已逐字在场
(「Level 2 = proposal only ⇒ 上面这张清单没有 checkbox 承载」)。**R2-fix 做的是把它上提为
「未裁定不得进 Phase B」的闸门并加上关于 A.2 行为的机制声称**, 即**放大**而非引入。如实归给 R1-fix。

---

### M-2 · 🔴 出路 (i) 把 O-1 委派给 §C.2.5, 而 §C.2.5 对「主仓 gitlink 未 bump」结构上失明 (blocks_phase_b)

**Locator**: `proposal.md:46` (出路 (i)) × `aria/skills/phase-c-integrator/SKILL.md:570-596` (§C.2.5)
× 同文件 `:183-196` (§C.2.4.5)

出路 (i) 逐字: 「**O-1 由 phase-c-integrator §C.2.5 既有自动化 + 双推 `ls-remote` 核验兜 gitlink 那条腿**」。
我去目标处实读 §C.2.5 **执行流程六步**逐字:

```
1. 快照 expected_sha = git rev-parse HEAD (合并后本地 master HEAD)
2. 枚举子模块: git submodule status --recursive
3. 确定 ENFORCED_REMOTES
4. Per-Remote Matrix Gating: a. 推子模块 → c. 推主仓库 → d. verify_parity_post_push(main_repo, branch, expected_sha, [REMOTE])
5/6. 全通过 → Phase D / 任一阻断 → 输出修复命令
```

**它核的是「本地已有的那个 commit 有没有原样到达每个 remote」, 不是「那个 commit 里的 gitlink 有没有被 bump」。**
`expected_sha` 是**合并后本地 master HEAD** —— 若该 commit 根本没 bump gitlink, 六步全绿。
CLAUDE.md 约束 2 的双推 `ls-remote` 核验是同一个量 (per-remote SHA 一致性), 同样与 gitlink 内容无关。

更进一步: 唯一真的读 gitlink 的机制是 **§C.2.4.5 submodule pointer regression gate**, 而它 `:194` 逐字
「pass: 所有 submodule pointer 是 forward bump 或 **no-change** 或 first-time」—— **「未 bump」= no-change = PASS**。

**它在什么实现下会红**: 不会红。A 按 MINOR ship, `aria` 子模块 5 文件全改、主仓 `VERSION` 与 badge 全改、
**唯独忘了 `git add aria`** ⇒ C.2.4.5 判 no-change PASS · C.2.5 六步全绿 · `m6-version-badge-match`
按 A 自己的实证「对该方向结构上失明」⇒ **全绿, 而 GitHub `clone --recursive` 拿到旧 plugin**。
这正是 A 自己在 O-1 行点名的 B 侧 R4 Critical (`TASK-017` 漏 gitlink) 的形状。

⇒ **出路 (i) 用一个与 O-1 失明方向完全相同的机制去兜 O-1。** 它不是「兜得不够」, 是**根本不在那条轴上**
(memory `invariant-dimension`: 机械不变量的维度须匹配错误的维度; 无向的一致性检查对方向性错误天然免疫)。
⇒ owner 若选 (i), 会以为 gitlink 那条腿有兜底, 而它没有。

**修法**: 要么如实把 (i) 改成「O-1 **无**机械兜底, 接受纯人工纪律」(诚实但更糟), 要么给出真的读
「主仓 gitlink 是否指向子模块 post-merge SHA」的判据。**⛔ 不得保留现文的委派** ——
它比「承认没有兜底」更危险 (memory `feedback_paper_fix_antipattern` 的 advisory 形状)。

**introduced_by_r2fix: false** —— R1-fix `:398` 逐字已有「由 phase-c-integrator §C.2.5 的既有自动化 +
双推 `ls-remote` 核验兜住 gitlink 那条腿」。R2-fix 把它上提到文首并**扩大到覆盖 O-2/O-3**, 未回源核。如实归 R1-fix。

---

### M-3 · 🔴 `SC-A-step` 的 (c-含) 腿是 A 自己判为 landmine 的那种哨兵 —— 兄弟位置清点**只做了 A→B 一个方向** (blocks_phase_b)

**Locator**: `proposal.md:451` (`SC-A-step` (c-含)) × `:124` / `:606` (标注须指向 `#137`) × `:163-166`
(A 逐字拒绝哨兵 SC 的理由) × B `proposal.md:343` (`SC-M1`) / `:346` (`SC-M3b`)

`SC-A-step` (c-含) 逐字要求 A 新增步骤的正文「**同时含** `步骤 3` 与 `#137`」,
「怎么会红」列逐字「加了步骤但**不标注**与步骤 3 的不一致 / 不指向 `#137` ⇒ 红」。
被标注的那条「不一致」逐字是 (`:122`)「**步骤 3 仍逐字硬编码 `main`**」。

**B 侧 D1 落地后这条不一致不复存在**: B `:343` `SC-M1` 断言 `grep -c 'aether ci status' SKILL.md` **= 0**
(注解逐字「一条断言覆盖 `:167`/`:168`/`:243`/`:244` 全部四行」), 而步骤 3 今日逐字就是
`aether ci status --branch main --in-flight --json` (我实读 `SKILL.md:243`); B `:346` `SC-M3b` 再禁
`--main-branch` 后跟字面 `main`/`master`。⇒ B 正确落地后, 步骤 3 读 `<MAIN_BRANCH>` 占位符, **不再硬编码 `main`**,
且 A 自己 `:166` 逐字「闭环判据挂 B 侧 D1」⇒ **`#137` 届时可闭**。

**它在什么实现下会红 / 两条路都坏**:
- **留着标注** ⇒ 随 plugin 分发给第三方的 `SKILL.md` 里, 步骤 2.2 逐字断言「步骤 3 仍硬编码 `main`, 见 #137」,
  而步骤 3 就在它下面三行、已不含 `main`, `#137` 已关。**文档说了一句当场可被同一页面证伪的假话** (违反规则 #3);
- **删掉标注** ⇒ `SC-A-step` (c-含) **在完全正确的 B 实现下必红** —— 与 R2 抓的 `SC-M3a` 对撞**同形, 方向相反**。

⇒ **A 逐字拒绝过这个形态**: `:163-166`「唯一能机械化的形态是『**断言缺陷仍在**』的哨兵 —— 它在 **B 落地后必须被删,
是 landmine** ⇒ **不编造这条量**」。(c-含) 正是一条「断言缺陷仍在」的哨兵 —— 只不过它断言的是
「**关于**缺陷的那句话仍在」。**认出了类, 在同一份文件里又造了一个** (memory `fix-the-class`)。

**这也是对任务书问题 3 的直接回答**: 兄弟位置表的清点口径逐字是「**A 是否会打爆 B 的 SC**」——
`grep -n 'SC-M' B/proposal.md` 起手, 10 条逐条判 A 是否落在**B 的**拒绝域内。
**反方向 (B 正确落地会不会打爆 A 的 SC) 一条都没查**, 而 A 本轮新增的三条 doc 侧 SC 全部断言
`SKILL.md` 内容 —— 那正是 B 的 D1 要重写的那一段。清点不是「数漏了一条兄弟」, 是**漏了半个坐标轴**。

**修法** (A 内可做, 不改 B): 把 (c-含) 的操作数从「断言那句不一致仍在」换成**不随 B 漂移的量** ——
例如只要求标注含 `#137` 这一个稳定外部锚 (issue 关了引用也不假), 去掉对「步骤 3 硬编码 `main`」这一
**会被 B 修好的事实**的断言 (memory `redfix-change-quantity`: 换量, 不是调阈值)。

**introduced_by_r2fix: true** —— `SC-A-step` 与「指向 `#137`」两处均为 R2-fix 新写 (diff 确认)。

---

### M-4 · 兄弟位置表对 `SC-M3c` 用的前提, 正是同一张表在 `SC-M15` 行推翻的那个前提 (blocks_phase_b)

**Locator**: `proposal.md:153` (SC-M3c 行) × `:154` (SC-M15 行) × `:451` (`SC-A-step` (c) 三禁)
× B `proposal.md:347` (SC-M3c) / `:161` (D1 折叠范围)

同一张表的相邻两行:

| 行 | A 是否会打爆 | 逐字理由 |
|---|---|---|
| `:153` **SC-M3c** (`<details>` 块内含 `--pr-branch` 的**块数** = 0) | **不会** | 「A **不建折叠块** (§非目标 逐字)」 |
| `:154` **SC-M15** (`<details>` 块内可执行命令字面量行数 = 0) | 🔴 **会, 且这条最隐蔽** | 「B 的 D1 把**步骤 1-5 整体折叠** (B `:161` 逐字) ⇒ **A 的步骤届时就在折叠块内**」 |

**两行的前提互斥。** 我实读 B `:155-161` 确认 SC-M15 行的前提是对的 (D1 折叠 `helper 内部算法` 块,
范围是步骤 1-5, 且逐字要求「折叠块须**补上 §3 新增的分支存在性核验步**」)。
⇒ 按正确前提, **SC-M3c 与 SC-M15 是同一个「A 的文本会落进 B 的折叠块」暴露面的两条腿**,
而 `SC-A-step` 的 (c) 三禁 (`--main-branch` / `aether ci status` / 以 `aether `·`git `·`python3 `·`bash ` 起头的命令)
**只覆盖 SC-M15 那条腿, 不含 `--pr-branch`**。

**它在什么实现下会红**: A 把新步骤写成 `verify_main_branch_exists(main_branch, remote)`,
并在同一步骤正文里加一句括注对齐 CLI 面 ——「(对应 CLI 的 `--remote` / `--pr-branch` 同批传入)」。
逐条过 `SC-A-step` (c): 不含 `--main-branch` ✅ · 不含 `aether ci status` ✅ · 无行以那四个命令起头 ✅
⇒ **A 侧 18/18 全绿, A ship**。B 落地 D1 折叠步骤 1-5 ⇒ 该 `<details>` 块含 `--pr-branch` ⇒
`SC-M3c` 计数 **1 ≠ 0** ⇒ **B 一条负控在完全正确的 B 实现下必红**, 而 A 早已 ship、看不到。
—— 与 R2 抓到的 `SC-M15` **逐字同一机制**, 只差一个 flag 名。

补充: `grep -c -- '--pr-branch' SKILL.md` 今日 = **0**, 所以这不是「今天就错」, 是**禁令集不闭合**。
一张自称「穷举 / 逐条判 / 不再挑一个修」的表, 在它自己新造的正确前提下**没有回头重判前面的行**
(memory `fixes-contradict`: 每条单独看都对, 但 A 违反 B 的隐含前提)。

**修法**: 一个 token —— (c) 的禁令表加 `--pr-branch`, 并把 SC-M3c 行的理由改成与 SC-M15 同一条。

**introduced_by_r2fix: true** (兄弟位置表整体为 R2-fix 新增)。

---

### M-5 · `SC-A14` 腿 2 的红机制建立在 `sys.stdout.errors == 'strict'` 上, 而在本套件的默认运行方式下该值实测为 `'replace'` (blocks_phase_b)

**Locator**: `proposal.md:446` (`SC-A14` 腿 2 的「今日实测」与「怎么会红」两列) × `:349-359` (§5 出口净化)
× `:489` (打桩边界「必须 mock」档) × `scripts/pre_merge_gate.py:438`

`SC-A14` 腿 2 逐字: 期望「**进程退出码 == 0** 且 stdout 是可 `json.loads` 的单行 JSON 且其 `verdict=="fail"`」;
今日实测列逐字「`sys.stdout.errors == 'strict'` (R2 实跑)」; 怎么会红列逐字
「`surrogateescape` 解码后不做出口净化就塞进 `raw_message` 的实现必红 —— `sys.stdout.write` 抛 `UnicodeEncodeError`」。

**那个 `'strict'` 是在裸 python 里量到的, 不是在这条 SC 将要运行的总体里量到的。** 我用受控探针实测三种情形:

| 运行方式 | `sys.stdout` 类型 | `.errors` | 写孤立代理码位 |
|---|---|---|---|
| 裸 `python3 -c` | `TextIOWrapper` | `strict` | **抛 `UnicodeEncodeError`** |
| `pytest -q` (**默认 fd 捕获**) | `EncodedFile` | **`replace`** | **成功, 不抛** |
| `pytest -q --capture=sys` | `CaptureIO` | `strict` | 抛 |

并且 `find aria -maxdepth 4 -name pytest.ini -o -name pyproject.toml -o -name setup.cfg` = **零命中**
⇒ 本套件**没有任何配置覆盖默认值**, 而 §测试基线自己写的复跑方式就是 `pytest`。

**它在什么实现下会绿 (= 该 SC 抓不到它唯一要抓的缺陷)**: Phase B 照 §5 做入口 `surrogateescape` 解码、
**不做出口净化**, 把含孤立代理码位的 `raw_message` 交给 `main()` ⇒ `json.dumps(..., ensure_ascii=False)` 成功返回
⇒ `sys.stdout.write` 在 `errors='replace'` 下**成功写出** (代理位被替换成 U+FFFD) ⇒ `main()` 返回 **0** ·
stdout 仍是**合法单行 JSON** · `verdict=="fail"` ⇒ **腿 2 的三条断言全部成立 ⇒ 绿。**
⇒ 这条 SC 与被测实现无关地绿 = **假绿**, 正是它自己援引的 memory `feedback_false_green_dual_is_permanent_red`
的另一面; 而 R1→R2 的整条修复链 (入口解码 → 出口净化) 的**唯一**机械腿就是它。

**第二层 (欠定)**: 「**进程退出码**」只有 spawn 子进程才观测得到, 而打桩边界表 `:489` 逐字把腿 2 放进
「**必须 mock**」档并说「注入的是**同一批** mock, 只是断言点移到进程出口」—— 子进程里注入不了 in-process mock。
三种自然读法 (`capsys` / `capfd` / 真子进程) 里, 一种可红、一种恒绿、一种造不出探针 ⇒
两个独立实现者会得到相反结果 (memory `spec-underdetermination`, 本 Spec 自己在 `SC-A-doc` 两条解析规则处
刚为同一个病开过药)。

**修法**: 把腿 2 的判据从「进程退出码 / stdout 可解析」换成**不依赖 harness 捕获模式的量** ——
直接断言进入 `raw_message` / `gate_error.message` 的字符串**不含孤立代理码位**
(`s.encode('utf-8', 'strict')` 不抛 / `all(not 0xD800 <= ord(c) <= 0xDFFF for c in s)`)。
那是 §5 逐字钉死的那件事本身, 且与 pytest 捕获模式无关。

**introduced_by_r2fix: true** (腿 2 为 R2-fix 新增, diff 确认)。

---

### M-6 · 「早退分支保持六键不变」这句枚举有**第四处**落点, 且正在 §4 要求 A 修改的那个函数里

**Locator**: `scripts/pre_merge_gate.py:241-247` (`_build_output` docstring) × `proposal.md:295-303`
(§4 R2 钉死「必须经 `_build_output` 产出」) × `:491` (打桩边界表逐字「三条一一对应 …… 无第四处」)

我实读 `_build_output` 的 docstring (`:241-247`) 逐字:

```
v1.65.0+ (#122, BA-6): `path_coverage` 是 additive 可选键 — 仅当评估已执行
且流程走到 compute_verdict 最终路径时在场 (path_coverage 非 None); 各早退
分支 (enabled:false / no-backend / precheck 失败 / backend query 失败) 保持
既有六键不变。
```

—— 与 `SKILL.md:279` 的归纳句**是同一句话的第二份拷贝** (同样 4 项枚举、同样「保持六键不变」)。
而 §4 的 R2 钉死逐字要求 A **给 `_build_output` 加一个 `gate_error: dict | None = None` 形参**,
即这段 docstring **就在 A 的 hunk 里**; A 又新增第五类早退 (核验失败 = **六键 + `gate_error`**)。

**它在什么实现下会红**: 都不会红。三条 doc 侧 SC 的操作数逐字全部限定在 `SKILL.md`
(`SC-A-doc` = json 块 `:265-277` · `SC-A-note` = §C.2.4「枚举归层注记」段 · `SC-A-step` = 执行流程区块),
**无一条读 `.py` 的 docstring 一个字节** ⇒ 落地后 **18/18 全绿**, 而 A 亲手改过的那个函数的 docstring
仍宣称「各早退分支 (4 项) 保持既有六键不变」, 与它自己新增的第五类分支矛盾 (规则 #3)。

⚠️ 打桩边界表 `:491` 的「无第四处」严格说只声称「没有第四处 `SKILL.md` hunk」, 字面不假;
**但整轮方法的口径是「这形状还有几个兄弟位置」**, 而这一处兄弟**比 `SKILL.md:279` 离代码更近**
—— 它是同一句话在 A 必改文件里的拷贝。清点跑在了「hunk 数」这个量上, 没跑在「同一陈述的落点数」上。

**修法**: §Impact 的 `pre_merge_gate.py` 行加一句「同批更新 `_build_output` docstring 的四类枚举」,
或把 `SC-A-note` 的操作数扩为「`SKILL.md:279` **与** `_build_output` docstring 两处同步」。

**introduced_by_r2fix: true** —— 「必须经 `_build_output` 产出」与「无第四处」两句均为 R2-fix 新写。

---

### m-1 · Level 2 定档用的是本 Spec 自造的三条判据, SOT 的「跨模块」腿从未逐字评估

**Locator**: `proposal.md:6-7` (抬头定档句) × `standards/openspec/project.md:112-118`
× `aria/skills/spec-drafter/LEVEL_GUIDE.md:19-48`

抬头逐字用三条判据定 Level 2: 「无架构变更 · 无跨仓**内容**同步面 · 无破坏性**契约**变更」。
SOT 的判据我实读: `project.md:114-118` 表 = 「2 | Minimal | **Medium features (1-3 days)** | proposal.md」/
「3 | Full | **Architecture changes** | proposal.md + tasks.md」; `LEVEL_GUIDE.md` 决策流程图 Q2 逐字
「是否**架构变更 / 跨模块 / Breaking**? → YES → Level 3」。

⇒ SOT 的三条腿是「架构变更 / **跨模块** / Breaking」+ 一条工期腿; A 用「无跨仓**内容**同步面」
**替换**掉了「跨模块」这条腿, 而「跨仓内容同步面」这个概念在 SOT 里不存在, 是 R1-fix 为消解
R1 抓到的自我推翻而新造的。**「跨模块」这条腿全文没有被逐字评估过**
(memory `exact-exception-condition`: 援引成文判据须逐字核对确切条件, 非精神/类推)。

**它在什么实现下会红**: 不会红 —— 我独立按 SOT 走了一遍 Q2: A 的代码面落在**单一 skill**
(`phase-c-integrator` 的 3 个文件), 发版同步面是**任何** MINOR 插件发版都有的仪式而非本 change 的模块面
⇒ **Q2 = NO ⇒ Level 2 成立**, 结论我不推翻。报这条是因为**依据链不是从 SOT 派生的**,
而定档正是本 BLOCKER 要 owner 裁的那件事的输入。修法: 一句话 —— 逐字引 SOT 的三腿并说明每腿为何 NO。

**introduced_by_r2fix: false** (三条判据为 R1-fix 措辞)。

---

### m-2 · 兄弟位置表把 `SC-M18` 的断言总体缩小成「`SKILL.md` 的计数」, 实为**四个文件并列**

**Locator**: `proposal.md:156` (SC-M18 行) × B `proposal.md:364`

A 的表逐字: 「`SC-M18` | `still (readable\|works)\|removed in v2\.0\|仍读\|v2\.0 移除` **在 `SKILL.md` 的计数** | 0」。
我实读 B `:364` 逐字: 该 pattern 跑在**删除面其余四个文件**上 —— `.../scripts/pre_merge_gate.py` ·
`.../phase-c-integrator/SKILL.md` · `.../tests/test_pre_merge_gate.py` · `.aria/config.template.json`,
期望 `0 / 0 / 0 / 0`。**其中 `pre_merge_gate.py` 与 `tests/test_pre_merge_gate.py` 都是 A 要改的文件。**

**它在什么实现下会红**: 结论不变 (A 不碰 v2.0 弃用面, 不会写那四条措辞), 所以这不是对撞漏判;
但一张**以穷举为唯一价值**的表, 在一行上把断言总体缩到了 1/4 —— 若下一轮有人据此判「A 改 `.py` 与测试
不碰任何 B 侧 SC」, 会用一个已缩小的总体作输入 (memory `critique-repeats-error`: 并列总体/范围/计数法)。

**introduced_by_r2fix: true** (兄弟位置表为 R2-fix 新增)。

---

## 3. 复核执笔方的四条「不同意」与两条 owner 裁量项

| # | 执笔方的判断 | 我的复核 |
|---|---|---|
| 1 | 不同意 `SC-M3a` 二选一对等, 取 (i), 论证 (ii) **结构上更差** | ✅ **正确**。我实读 B `:345` 期望恰 **2** + 注解逐字「两处散文各一条」; 取 (ii) 确会使该期望值取决于 A/B ship 顺序 ⇒ 随时序漂移的量。且跨轨改 B 会撞车 (B 正在自己的 post_planning 轨上)。**但这条正确不能传染** —— 它只消除了 A→B 方向, B→A 方向仍开着 (M-3) |
| 2 | 不同意「带参 CLI 示范是新步骤最自然形态」 | ✅ **正确**。我实读 `SKILL.md:242` 步骤 2.5 = `evaluate_path_coverage(main_branch, pr_branch)`、步骤 2 = `resolve_ci_backend(cfg)`, **同编号列表内两处先例都是函数调用形态**。CLI 示范确属 B 侧 D1 交付物, A 写它是越界在先 |
| 3 | 不同意「doc 侧 7 键是人工数的」—— 数本来就对, 欠定的是解析规则 | ✅ **正确**。我复跑 `json.loads` ⇒ `JSONDecodeError: Expecting ',' delimiter: line 2 column 22`; 复跑 `^  "([A-Za-z_]+)":` ⇒ 恰 7 键, 与 `_build_output` 今日实产 7 键相等。两条解析规则是**规定**不是建议, 判断正确 |
| 4 | 同意 #137 耐久性是缺陷、不同意它在 A 内可修 ⇒ 路由进 BLOCKER `O-3`, 不假装修好 | ⚠️ **分类正确, 路由无效**。「A 内不可修 (唯一出路是仓外动作)」我认可; **但它路由到的那个 BLOCKER 本身建立在被证伪的前提上 (M-1), 且 `O-3` 的落点依赖 owner 选 (i) 才成立** ⇒ 诚实地标注了缺陷, 却把它交给了一个坏掉的接收端 |
| A | owner 裁量项 **MINOR vs MAJOR** | ✅ **分类正确, 我不加码** (与 R2 结论一致): 带默认值 kwarg 对 25 个调用点零破坏 · additive 可选键与 `path_coverage` 同构 · `:68`/`:116` 弃用承诺不触发。「恒 green 的闸门开始 fail 够不够 MAJOR」确属 owner |
| B | owner 裁量项 **BLOCKER 三义务 (i)/(ii)** | ❌ **分类错误**: 它被写成「Level 2 无载体 vs Level 3 有载体」的二选一, 而 Level 2 已有 `detailed-tasks.yaml` 载体 (M-1), 且 (i) 的兜底不存在 (M-2)。**⛔ 不得以此形态交给 owner** —— 两个选项的代价与收益都是错的 |

---

## 4. 划界自足性 / 定档 / 边界 — 席位结论

**划界 (split_soundness)**: **拆分方向依然成立, 且 A 的完成定义仍然诚实。** A 的价值主张限定在
`gate_check()` 层、残余暴露有可现场复现的精确形态、连带更正在 B 与 DEC 两处实测已落 (R2 复核过, 本轮未回退)。
代码面纯 additive 我第三次复核仍成立。
**但「自足」这一轮暴露的不是新接缝, 是同一条接缝的另一半**: R2 修好了「A 往共享 `SKILL.md` 写的东西
会不会打爆 B」, **没有问「B 正确落地会不会打爆 A 写进去的东西」** (M-3) ——
A 的 doc 侧交付物 (一个编号步骤 + 一句关于步骤 3 的断言) 全部住在 B 的 D1 要重写的那一段里,
这条边界**只要 A 先 ship 就一定会被 B 碰**, 而它今天只有单向护栏。

**Level 2 定档**: **判据结论 (Level 2) 我复核后仍然成立** (按 SOT `LEVEL_GUIDE.md` Q2 逐条走: 非架构变更 /
代码面单 skill / 非 Breaking)。**但定档周边的两个论断都错了**: 「Level 2 ⇒ 无 task 载体」(M-1, 被
`task-planner:52-66` 与三个归档 Level 2 先例证伪) 与「(i) 有机械兜底」(M-2, 被 `SKILL.md:570-596` 证伪)。
⇒ **我不主张升 Level 3**; 我主张**在 Level 2 内把六项义务写到 A.2 必然消费的位置**, 并把 BLOCKER 重写为
一个前提正确的裁量点。

**MINOR 定档**: 技术上仍正确, 与 R2 结论一致, 不加码。

**与 B 侧边界**: 静态归属 (D1/D5/折叠块/24 处补参/v2.0 弃用面/`config.template.json`/B 侧发版面与 AB 留 B)
逐条与 DEC §2 一致, **无 scope creep**。发现的重叠/缺口共四处: **M-3 (承重, 反向对撞)** ·
**M-4 (`SC-M3c` 未纳入禁令集)** · m-2 (`SC-M18` 总体缩小) · 以及 R2 已闭合的 `SC-M3a`。
**B 侧 R4 的 3 条 Critical 我逐条核过, 确属 B, 未搬运任何一条到 A**; M-2 引用 `TASK-017` 只作**同形先例**,
论证完全落在 A 自己的 §C.2.5 委派上。

---

## 5. 本轮 fix 引入率 (三项并列, 不修饰)

**总体** = 本席本轮报的 **8** 条 findings; **范围** = R2-fix 版 (`017eb54`) 的 `proposal.md`;
**计数法** = 逐条判「该 finding 指控的**文本**是否由 R2-fix 新写/新改」, 用 `git diff e165df4 017eb54` 回源, 逐条标注。

| finding | introduced_by_r2fix | 回源依据 |
|---|---|---|
| M-1 BLOCKER 承载前提 | **false** | R1-fix `:394` 已逐字有同一前提; R2 只是上提 + 加机制声称 |
| M-2 (i) 委派 §C.2.5 | **false** | R1-fix `:398` 逐字已有该委派 |
| M-3 `SC-A-step` (c-含) landmine | **true** | `SC-A-step` + 「指向 #137」均 R2 新写 |
| M-4 `SC-M3c` 前提互斥 | **true** | 兄弟位置表 R2 新增 |
| M-5 `SC-A14` 腿 2 假绿 | **true** | 腿 2 R2 新增 |
| M-6 `_build_output` docstring | **true** | §4「必须经 `_build_output` 产出」+「无第四处」均 R2 新写 |
| m-1 Level 判据非 SOT 派生 | **false** | R1-fix 措辞 |
| m-2 `SC-M18` 总体缩小 | **true** | 兄弟位置表 R2 新增 |

⇒ **5 / 8 = 62.5%**。

**可比性**: 与本席 R2 的 **6/8 = 75%** **可直接比** —— 同一席位、同一总体定义 (单席 findings)、
同一计数法 (逐条判文本归属)、同一范围类型 (上一版 fix 的 proposal)。⇒ **75% → 62.5%, 真的降了。**
与任务书给的 74% / B 侧 53/70/71% **不可比** —— 那些的总体是**五席去重后的 Major**, 计数法与量纲都不同
(memory `critique-repeats-error`: 三项任一不同只能写「不可比」)。

**「兄弟位置清点」这个新方法起作用了吗 —— 分开答两件事**:
1. **在它覆盖的方向上, 起作用了。** R2 那种「同一类只修一个实例」的复发, 本轮**一条都没有**:
   backend ambient 的类级修复 (适用集 10 / 例外 3 / 不适用 3, 我逐条核过覆盖等于 18 行) ·
   名单去重 (删一处而非同步两处) · doc 侧三 hunk 一一上锚 —— 三处都做对了, 且做的是**类**不是实例。
2. **但它没有降到 50% 以下, 原因是可诊断的**: 本轮 5 条新引入里, **3 条 (M-3/M-4/m-2) 就出在这张清点表本身**,
   1 条 (M-5) 出在新增的 SC 腿, 1 条 (M-6) 出在新钉死的落地方式。
   **每件新手段都造出一个新表面** (memory `marginal-return-negative`), 而清点表这件手段的表面特别大 ——
   它是一张**关于别的文档的断言表**, 每一行都是一条可被独立证伪的跨仓声称。
   ⇒ 方法本身值得留下; **但它需要一条自反规则: 清点表建成后, 用它自己新造的前提回头重判前面的行**
   (M-4 就是没做这一步), **并把方向补齐** (M-3 就是只做了一个方向)。

是否据此收敛 / 停轮 / 换席由汇总席判定, 单席无权 (`converged: null`)。
