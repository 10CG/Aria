---
checkpoint: post_spec
mode: convergence
rounds: 4
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-12T18:15:00.000Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [tech-lead]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

# post_spec R4 — tech-lead — Spec A `premerge-gate-branch-existence`

**VOTE: REVISE** · **VERDICT: PASS_WITH_WARNINGS** (0C + 6M + 5m) · 5 条 `blocks_phase_b`
· **本轮 fix 引入率 10/11 = 91%** (Major 口径 5/6 = **83%**)

---

## 0. 我本轮实跑过的命令 (所有数字的出处)

```bash
# 定档 SOT 逐行
awk 'NR>=24 && NR<=30 {printf "%d: %s\n", NR, $0}' aria/skills/spec-drafter/LEVEL_GUIDE.md
awk 'NR>=112 && NR<=120 {printf "%d: %s\n", NR, $0}' standards/openspec/project.md
awk 'NR>=153 && NR<=163 {printf "%d: %s\n", NR, $0}' aria/skills/spec-drafter/LEVEL_GUIDE.md   # 跨模块判断

# task-planner 路径 B 的真实契约
sed -n '50,75p' aria/skills/task-planner/SKILL.md
sed -n '80,110p;104,160p' aria/skills/task-planner/DUAL_LAYER_SPEC.md
grep -rn 'Success Criteria' aria/skills/task-planner/       # 仅 2 命中

# A 是否具备路径 B 文档化的两个任务源章节
grep -c '^## What$' openspec/changes/premerge-gate-branch-existence/proposal.md          # 0
grep -c '^### Key Deliverables' openspec/changes/premerge-gate-branch-existence/proposal.md  # 0

# 归档 4 例 (A 引作实证) 的任务源章节与真实任务数
for d in .../2026-05-29-aria-context-monitor .../2026-05-30-ai-native-estimator \
         .../2026-05-30-emergency-hotfix-and-audit-file-scope .../2026-07-22-state-scanner-gate-yaml-datasource; do
  grep -cE '^\s*- id: *"?TASK-' $d/detailed-tasks.yaml; grep -m1 'total_tasks:' $d/detailed-tasks.yaml
  grep -c '^## What$' $d/proposal.md; grep -c '^### Key Deliverables' $d/proposal.md
  grep -c 'TASK-' $d/detailed-tasks.yaml
done

# SC 行数双向
grep -c '^| \*\*SC-M' openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md   # 20
grep -c '^| \*\*SC-A' openspec/changes/premerge-gate-branch-existence/proposal.md        # 18

# B 侧被引行 / 迁移痕迹
awk 'NR==154||NR==156||NR==158||NR==161' openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md
grep -n 'cancelled' openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml   # 2 处, 均属 TASK-020

# 机械锚今日基线 (复核 R3-fix 的四处新判别点)
grep -n '^\*\*执行流程\*\*:' SKILL.md                      # [238, 582]
awk 'NR>238 && NR<257' SKILL.md | grep -oE '^[0-9]+(\.[0-9]+)?\.'   # 1. 2. 2.5. 3. 4. 5. 6.
awk 'NR>=277 && NR<=281' SKILL.md
grep -cE 'still (readable|works)|removed in v2\.0|仍读|v2\.0 移除' <四个文件>   # 2 / 4 / 3 / 0
awk 'NR>=236 && NR<=266' scripts/pre_merge_gate.py          # _build_output docstring :241-246

# 动态测量 (独立复跑 R3-fix 的 19/24, 非转述)
python3 <sys.settrace 探针, 记录每次 gate_check 动态调用是否执行到 pre_merge_gate.py:356>
  ⇒ tests run: 46 · failures 0 · dynamic gate_check calls: 24 · reached 356: 19
  ⇒ NOT reached caller lines: [282, 301, 311, 321, 524]      ← 与 Spec 逐字一致
```

---

## 1. R3 的 14M 是否真闭合 —— 逐条回源, 区分「写下来」与「闭合」

| R3 finding (席) | R3-fix 的处置 | 我的复核 |
|---|---|---|
| **tech-lead M-1** BLOCKER 建立在「Level 2 ⇒ 无 task 载体」这个假前提上 | 全块重写, 六项义务移入 `## Success Criteria` §交付义务 | ⚠️ **只闭合了一半**。「Level 2 也出 `detailed-tasks.yaml`」这个证伪**成立** (我复跑 4 例); 但新写的「移入 SC 章节 ⇒ 路径 B **必然**把它们读进 yaml / **⇒ 出一条 TASK**」是**第二个未回源的前提** → **F-1** |
| **tech-lead M-2** 出路 (i) 把 O-1 委派给 §C.2.5 (失效委派) | 出路 (i) 整体作废, 改为事实声明「O-1 今日无任何机械兜底」 | ✅ **真闭合**。这是本轮最干净的一处修复: 把一个假的兜底换成一句可证伪的事实, 并把「接不接受」上呈 `D-b`。**不为它编造机械锚**是正确的 (见 §3 对预判 ② 的回答) |
| **tech-lead M-3** `SC-A-step` (c-含) 是 A 自己判为 landmine 的哨兵 | 改标注对象为「本步自身的作用域边界」, (c-含) 机械腿只留 `#137` | ⚠️ **改了 3 个落点漏了第 4 个** —— §非目标 `:844` 逐字仍要求标注被作废的那条不一致 → **F-2** |
| **tech-lead M-4** 兄弟位置表对 `SC-M3c` 用的前提被自己在 `SC-M15` 行推翻 | 三条点名禁令升级为**类级** (任何 `--` flag / `aether ci status` / 任何裸命令) | ✅ **真闭合**。类级化是 `fix-the-class` 的正确形态; 我核过 (c-禁) 对 `--pr-branch` 现在天然拒绝 |
| **tech-lead M-5** `SC-A14` 腿 2 的红机制建立在 `sys.stdout.errors=='strict'` 上 | 换测量点: 在 `gate_check()` 返回的 dict 上直接对 `raw_message` / `gate_error.message` 跑 `encode("utf-8","strict")` | ✅ **真闭合, 且换的确实是「测量点」不是「不变量」**。新判据一个字节都不读 `sys.stdout` ⇒ 与 harness 捕获模式结构上无关; 且与打桩边界表「同一批 mock」不再互斥 |
| **tech-lead M-6** 「四类早退保持六键」有第四处落点 (`_build_output` docstring) | `SC-A-note` 新增 (d) 腿 + 抹空白解析规则 + §Impact 明文要求同批改 | ✅ **真闭合**。我实读 `pre_merge_gate.py:241-246` 确认: 该段今日就是中文、恰 4 项枚举、`各早退` 与 `分支 (…)` 被源码换行拆开 ⇒ **抹空白规则是必需的, 不是修辞** |
| **code-reviewer F-1** 「20/24 触达」实为 19/24, 漏第三类早退 | 改用动态测量, 三类早退与三条负控一一对齐 | ✅ **真闭合, 我独立复跑逐字复现** (46/24/19, NOT reached `[282,301,311,321,524]`) |
| **code-reviewer F-2** `SC-A14` 腿 2 恒绿 | 同 tech-lead M-5 | ✅ 真闭合 |
| **code-reviewer F-3** `SC-A10c` 放错例外集 | 移入适用集, 配平改为 11+2+3+2=18 | ✅ **真闭合**, 我核过配平与 `ci_backends/base.py` 默认 `precheck()` 恒 `(True,"")` 的理据 |
| **code-reviewer F-4** 出路 (i) 的 O-1 兜底失效 | 同 tech-lead M-2 | ✅ 真闭合 |
| **code-reviewer F-5** 清点漏 B 的 task 级预写量 | 表 1 补「方向 1 附加总体」三条 | ✅ **真闭合** (三条我逐个回源到 `tasks.md:85` / `:122` / `detailed-tasks.yaml:488`) |
| **qa-engineer QA-3-1** 清点表自称穷举却漏 7 条同名 B 侧 SC | 表 1 由 10 行扩到 20 行 + 显式弃用「穷举」二字 | ✅ **真闭合**。我实跑 `grep -c '^| \*\*SC-M'` = **20**, 并逐个核对 20 个 SC 名 (`M1…M18` 含 `M3a/b/c`) **全部在表内**, 零遗漏 |
| **knowledge-manager Major** BLOCKER「使 A.2 入口必然读到」与 `task-planner` 解析范围矛盾 | 移入 `## Success Criteria` | ⚠️ **未闭合 —— 换了一个更好的位置, 但「必然」二字原样搬了过去** → **F-1** (这是本轮最重的一条) |
| **backend-architect Major** `SC-M18` 操作数被缩小成「`SKILL.md` 的计数」 | 表 1 `SC-M18` 行改为四文件并列 | ✅ **真闭合**。我实跑四分量 = **2 / 4 / 3 / 0**, 与 Spec 逐字一致; 且 `SKILL.md` 的 4 处命中在 `:49/:285/:286/:349`, **无一在 `:279`** —— 这同时把 `SC-A-note` 的「B 不会碰它」这条判定也坐实了 |

**⇒ 14M 中 11 条真闭合 · 2 条只完成「换位置」(M-1 / KM Major, 同一根) · 1 条修了 3/4 个落点 (M-3)。**
**旧 finding 无一复发** —— 与 B 侧四轮同一形状: **执笔环节不是问题**。

---

## 2. Findings

### F-1 · 🔴 「移入 `## Success Criteria` ⇒ 路径 B **必然**出六条 TASK」在 delegate 处不成立 (Major, blocks_phase_b, 引入=是)

**位置**: `proposal.md:80-81` (处置句) · `:88`(O-1 行「⇒ 路径 B 出一条 TASK」) · `:754-768` (§交付义务) ·
`:925-926` (§Impact 风险声明的路由) × `aria/skills/task-planner/DUAL_LAYER_SPEC.md:90-93` ×
`aria/skills/task-planner/SKILL.md:59-67`

**逐字被审句** (`:80-81`): 「六项义务**移入 `## Success Criteria` 章节**的一个显式小节…**使路径 B 必然把它们读进 `detailed-tasks.yaml`**」;
`:88` 逐字「`## Success Criteria` §交付义务 O-1 (**⇒ 路径 B 出一条 TASK**)」。

**去 X 核三件事** (memory `delegate-verify`):

1. **真做吗** — `SKILL.md:67` 逐字「始终从 proposal.md 读取 `## Success Criteria` 章节」⇒ **读, 成立**。
2. **方式合约吗** — ⛔ **不成立**。`DUAL_LAYER_SPEC.md:90-93` 把路径 B 的解析内容逐字分派为三项**并各带用途**:
   `## What 章节: **功能概述**` / `### Key Deliverables: **交付物列表**` / `## Success Criteria 章节: **验收标准**`。
   而 `DUAL_LAYER_SPEC.md:104-152` 的 yaml schema 里，「验收标准」的落点是**每条 task 内的 `verification:` 字段**，
   不是 task 本身。我实跑 `grep -rn 'Success Criteria' aria/skills/task-planner/` = **仅 2 命中**
   (`SKILL.md:67` + `DUAL_LAYER_SPEC.md:93`)，**全 skill 无任何一句把 SC 条目转成 TASK**;
   `SKILL.md:74-84` 的「分解规则/分解策略」全部是**粒度与拆分**规则，输入侧一个字未提 SC。
3. **失败会发红吗** — ⛔ 不会。A 自己的 §交付义务 表「有机械闸门吗」列对六项**全部写「没有」**。

**两条实测把「必然」打掉**:

- **A 恰好缺路径 B 文档化的两个任务源章节**: 我实跑
  `grep -c '^## What$'` = **0** · `grep -c '^### Key Deliverables'` = **0**。
  ⇒ 路径 B 用来产任务的两个输入 A 一个都没有, 唯一在场的那个章节按 SOT 是**验收标准**。
- **A 自己援引的 4 个归档先例反着说话**: 我实跑每个目录的
  `grep -cE '^\s*- id: *"?TASK-'` 与 `metadata.total_tasks` (4/4 相等) 与两个任务源章节是否在场 ——

  | 归档 spec | 真实任务数 | `## What` | `### Key Deliverables` |
  |---|---|---|---|
  | `2026-05-29-aria-context-monitor` | **9** | 1 | 1 |
  | `2026-05-30-ai-native-estimator` | **8** | 1 | 1 |
  | `2026-05-30-emergency-hotfix-and-audit-file-scope` | **8** | 1 | 1 |
  | `2026-07-22-state-scanner-gate-yaml-datasource` | **10** | **0** | **0** |

  **3/4 的先例都带着 A 没有的那两个章节**; 唯一同样两缺的那个 (`state-scanner-gate-yaml-datasource`)
  其 proposal 有 **16 条 SC** 而 yaml 只有 **10 条 task** ⇒ **SC → TASK 在真实路径 B 上并非 1:1**。

**它在什么实现下会红**: A.2 对本 proposal 跑 `/task-planner` 路径 B, 产出的 `detailed-tasks.yaml` 中
**不存在**分别对应 O-1/O-2/O-3/F-1/F-2/F-3 的六条 `TASK-{NNN}` (最可能的形态: 六项被并进某条任务的
`verification:` 列表, 或干脆只进「发版」类的一条任务)。此时 `:80-81`/`:88`/`:925-926` 三处声称当场为假,
而**无任何闸门会发红** —— 与 R3 KM Major 指控的失效路径逐字同形, 只是换了一个章节。

**为什么这条比 R3 那条更该被处理**: R3 的处方是「把路由方式钉死」, R3-fix 选择的是「换一个被读到的章节」,
但**「被读到」与「被转成 task」是两个量**。诚实的收口是把 `:80-81`/`:88` 的**机械语气**降为
「**A.2 执行者的义务** (`:768` 那句祈使句本身就是正确形态), **无机械闸门保证它出**」——
这与 O-1 那一列自己写的「有机械闸门吗: 没有」才自洽。**不需要新写任何断言, 只需删掉两处「必然/⇒ 出一条 TASK」。**

**连带影响 (这是给 owner 的实质材料)**: `D-c` 现在的框架逐字是「移入 `## Success Criteria` 后,
**Level 2 已能拿到逐条 `TASK-{NNN}` 载体**…取 Level 3 的**增量收益只剩** `tasks.md` 那层粗粒度勾稽」。
若 F-1 成立, 这个「增量收益只剩」再次低估了留在 Level 2 的代价 ——
**R3-fix 把一个建立在假前提上的二选一, 换成了另一个建立在未核实前提上的二选一。**

---

### F-2 · 🔴 §非目标 `:844` 仍逐字要求 R3 已作废的那条 landmine 标注 (Major, blocks_phase_b, 引入=是)

**位置**: `proposal.md:842-844` (§非目标 第 2 条) × `:195-212` (§残余暴露 R3 框) × `:703` (`SC-A-step` (c-含)) × `:896` (§Impact hunk ①)

**逐字**: `:844`「由此产生的「新步骤用 `<MAIN_BRANCH>` 而**步骤 3 硬编码 `main`**」这条不一致,
按 §残余暴露在**该步骤处逐字标注**」。

**而 R3-fix 恰恰把这条要求作废了**: `:206-208` 逐字「上一版标注的是**另一个步骤的当下状态**,
本版改为标注**本步骤自身的作用域边界**」; `:703` 的 (c-含) 机械腿已删去 `步骤 3` 这个 token, 只留 `#137`;
`:896` 的 §Impact hunk ① 也已改为「标注本步自身的作用域边界」。

**我实跑 `git diff 017eb54 ff847fb` 确认**: R3-fix 改了 §残余暴露、`SC-A-step`、§Impact **三个落点**,
`:844` **一个字节未动** —— 与它自己本轮在 `SKILL.md:279` ↔ `_build_output` docstring 上诊断出的
「同一陈述的落点数没清点」是**同一个病, 在同一轮里同时犯**(memory `fix-the-class`)。

**它在什么实现下会红**: Phase B 实施者按 §非目标 (它是「不做什么/怎么做」的清单式章节, 实施者最常直读)
在新步骤处写下「⚠️ 步骤 3 仍硬编码 `main`」——

- 该句**不含**任何 `--` flag / `aether ci status` / 裸命令 ⇒ **`SC-A-step` (c-禁) 三腿全过**;
- 该句含 `#137` (§非目标 上下文与 §Impact 都要求指向它) ⇒ **(c-含) 也过**;
- ⇒ **A 侧 18/18 全绿并 ship**, 而随 plugin 分发给第三方的 `SKILL.md` 里留下一句
  **B 的 D1 落地当天即可在同一页面证伪的假话** (违反规则 #3) —— 正是 R3 tech-lead M-3 判 `blocks_phase_b` 的那个后果。

**最小修法**: `:844` 后半句改为与 `:206-208` 同措辞 (标注本步自身的作用域边界 + 指向 `#137`), 或直接删去该半句并引 §残余暴露。

---

### F-3 · 🔴 DEC §5.3 是 owner 裁定的 **A.1 迁移动作**, A 既未执行也未列为待裁项, 而是自行改成「D.2 handoff 必写项」(Major, blocks_phase_b, 引入=否)

**位置**: `docs/decisions/DEC-20260812-001-...md:122-128` × `proposal.md:267` (表 1 行) · `:779-783` (§交付义务 末段)

**逐字 SOT**: DEC `:122`「## 5. **迁移动作 (Phase A.1, 待执行)**」, 其下五条**同一个动作清单**, 第 1 条逐字
「新建 `openspec/changes/premerge-gate-branch-existence/proposal.md` (Level 2), 承接 §2 A 侧」——
**即本被审文件**; 第 3 条逐字「B 的 `detailed-tasks.yaml` **删去迁往 A 的任务时须留 cancelled 痕迹, 不得静默删**
(同 TASK-020 的条件任务纪律)」。DEC 抬头逐字「**裁定人**: owner (2026-08-12…)」·「**状态**: Approved」。

**实测今日状态**: 我实跑 `grep -n 'cancelled' B/detailed-tasks.yaml` = **2 处, 两处都是 TASK-020 的条件触发纪律**
(`:107` / `:1031`), **与迁移无关**; 逐个解析 21 条任务的 `status` ⇒ **TASK-001…TASK-021 全部 `pending`**,
其中 `TASK-003`(spike 存在性核验) / `TASK-004`(异常重试复用) / `TASK-005`(测试隔离接缝) / `TASK-007`(`--remote`) /
`TASK-008`(`_verify_branch_exists` 实现) / `TASK-009`(`raw_message`+`gate_error`) **六条的规格已整体过户给 A**
(逐条对得上 DEC §2 A 侧承接表的六行)。

**A 的处置**: `:267` 逐字「**A 本轮不改 B** (跨轨改会撞车, 见 F-3 同款理由) ⇒ **列为 A 的 D.2 handoff 必写项**」。
**问题不在这个判断本身合不合理, 而在它的性质**: 这是把一条 **owner 已裁定、明确挂在 A.1 名下**的动作,
由 AI 单方面**改期 (A.1 → D.2) + 改形态 (yaml 内 cancelled 痕迹 → handoff 散文)**。
我实跑 `grep -n 'DEC-20260812-001\|DEC §' A/proposal.md` ⇒ A 全文引 DEC 的 **§2 / §3 / §6 各一处, §5 零命中**
—— **A 从未在文本里承认这条义务的存在**, 因此 owner 在 `D-a`/`D-b`/`D-c` 三条待裁点上**看不到它**。

**它在什么实现下会红**: A ship 后, 任何执行 B 的实施者 (或 B 的下一轮 post_planning) 拿到的是
**七条 `pending` 且规格已迁走的任务**; 按 `tasks.md:77` 逐字 `TASK-008 _verify_branch_exists() … 插入点 = 三个早退之后`
去实现, 得到**第二份 `_verify_branch_exists` 定义 / merge conflict** —— 正是 A 自己在 `:267` 写下的那个后果。
owner 裁定的 `cancelled` 痕迹**就是为拦这一条而存在的**, 而它今日 `grep` 计数为 0。

**为什么这落在 A 而不是 B** (逐字论证, 应 R4 纪律): 该动作在 DEC 里**不在 B 的章节**, 而在
「§5 迁移动作 (**Phase A.1**, 待执行)」这张**与「新建 A 的 proposal」同一张**清单上; A.1 = 本文件的产出阶段。
**它不是 B 的 finding, 是 A.1 未交付的一件事。**

**最小修法**: 二选一, 都在 A 内可完成 —— (i) A.1 内执行 DEC §5.3 (只在 B 的 yaml 上给六条加 `status: cancelled` + 迁移留痕);
或 (ii) 若坚持「跨轨改会撞车」, 则把它**升为文首 BLOCKER 的第四条待裁点 `D-d`**, 逐字写明「owner 裁定的 A.1 动作,
A 请求改期到 D.2 / 改由 B 侧执行」——⛔ **不得由 A 自行降级为 handoff 备忘** (规则 #10 同形)。

---

### F-4 · Level 2 定档的 (b)「跨模块」腿仍是自造判据, SOT 自己的四条件 OR 列表四缺三 (Major, blocks_phase_b, 引入=是)

**位置**: `proposal.md:12-13` × `aria/skills/spec-drafter/LEVEL_GUIDE.md:153-163`

R3 tech-lead m-1 的原话是「SOT 的**「跨模块」腿全文未被逐字评估**」(memory `exact-exception-condition`)。
R3-fix 的回应逐字 (`:12-13`):
「(b) **跨模块 = NO** —— 代码面落在**单一 skill** `phase-c-integrator` 的 3 个文件内 (§Impact 逐行列明);
发版同步面是任何 MINOR 插件发版都有的**仪式**, 不是本 change 的模块面」。

**而 SOT 对「跨模块」有一个成文的四条件 OR 列表** (我实读 `LEVEL_GUIDE.md:153-163` 逐字):

```
跨模块条件 (满足任一):
  - 涉及 2 个及以上模块
  - 修改 shared/ 目录
  - 需要 API 契约变更
  - 影响多个子模块
跨模块 → 自动提升为 Level 3
```

**A 评估的是「落在几个文件/几个 skill」—— 这个谓词一个字都不在上面四条里。** 逐条对账:

| SOT 条件 | A 有没有评估 | 我的实测/判读 |
|---|---|---|
| 涉及 2 个及以上模块 | 部分 (以「单一 skill」代之) | 大概率 NO |
| 修改 `shared/` 目录 | **零评估** | NO |
| **需要 API 契约变更** | **零评估** | ⚠️ **可能 YES** —— A 给 `gate_check()` 加形参、给 `_build_output` 加形参、并往 `SKILL.md` §C.2.4 的 **Output schema** 加 `gate_error` 键 (A 自己 §4/§Impact 逐字如此)。additive 也是契约变更; SOT 这一条**未限定「破坏性」** |
| 影响多个子模块 | 以「发版仪式」一句带过 | 大概率 NO (只 `aria` 一个子模块) |

**它在什么实现下会红**: owner 或下一位复核者按 `LEVEL_GUIDE.md:156-160` 逐条对账, 只要**四条中任何一条判 YES**,
`:162` 逐字「**自动提升为 Level 3**」⇒ `:15` 的「Q2 = NO ⇒ Level 2」当场不成立, 而 `D-c` 呈给 owner 的
建议 (「维持 Level 2」) 是**以 Q2=NO 为前提**写的。**这正是 R3 m-1 指控的同一件事: 用精神匹配代替字段级匹配。**

⚠️ **我不主张 A 应该是 Level 3** —— 我主张的是: **这条腿到 R4 仍未按 SOT 的字段走完**,
而 `D-c` 是 Phase B 的前置裁定点, 它的输入必须是走完的。

---

### F-5 · Level 的 (c)「Breaking」腿的答案是版本定档的函数, 而同文件 `:119` 明文判两者「不得合并处理」(Major, blocks_phase_b, 引入=是)

**位置**: `proposal.md:13-15` (leg (c) + Q2=NO ⇒ Level 2) × `:114-117` (`D-c`) × `:119` × `:971-975` (版本待裁点)
× `LEVEL_GUIDE.md:29` × `CLAUDE.md` 版本管理段

**三句逐字并列**:

1. `:13-14`「(c) **Breaking = NO** —— API 形状层零破坏 (§版本), 运行时行为翻转已单列 §行为兼容面并**已作为 owner 待裁点留痕**」⇒ `:15`「Q2 = NO ⇒ **Level 2**」;
2. `:971-974`「⚠️ **版本定档留给 owner 复议的点**: 「一个此前恒 `green` 的闸门开始 `fail`」是否够得上 CLAUDE.md 的「**破坏性变更须 MAJOR**」? 本 Spec 判 **MINOR**…**该判断是 AI 作出的, 按规则 #10 留痕请复议**」;
3. `:119`「本块**不含**版本定档 (MINOR vs MAJOR) 那个待裁点…是**另一件事**…两处都须 owner 裁, **不得合并处理**」。

**矛盾**: `LEVEL_GUIDE.md:29` 的 Q2 第三腿逐字就是 **Breaking**; CLAUDE.md 逐字把 MAJOR 系于「破坏性变更」。
⇒ **owner 若在 (2) 上裁「运行时翻转够得上破坏性 ⇒ MAJOR」, 则 (1) 的 leg (c) 当场翻成 YES ⇒ Q2 = YES ⇒ Level 3。**
即: **版本裁定的输出就是 Level 裁定的一个输入**, 而 `:119` 逐字命令两者「不得合并处理」,
`D-c` 也把 Level 2 vs 3 呈现为一个纯粹的**成本收益题**(「增量收益只剩 `tasks.md` 那层粗粒度勾稽」),
**通篇不提它其实是规则驱动的**。

**它在什么实现下会红**: owner 分两次裁 —— 先在 `D-c` 批「维持 Level 2」, 后在 §行为兼容面 批「MAJOR」。
两条裁定各自看都合理, 合起来产出一个**违反 `LEVEL_GUIDE.md:29+162` 的档位组合** (Breaking=YES 而 Level=2)。
`:975` 已经预见了 MAJOR 对**划界**的后果 (「拆分收益会显著缩水, 须重议划界」), 却**没预见它对 Level 的后果**。

**最小修法**: `D-c` 里加一句依赖声明 ——「**本条的 (c) 腿以「版本裁定 = MINOR」为前提; 若版本裁 MAJOR,
则按 `LEVEL_GUIDE.md:29/:162` Q2 = YES ⇒ 本条自动改判 Level 3, 无需二次裁量**」, 并把 `:119`
的「不得合并处理」收窄为「**不得混为一题, 但须按序裁: 先版本, 后 Level**」。

---

### F-6 · 【复核执笔方预判 ①】`SC-A-step (a)(b)` 的「A 此侧无法断言」**过度收口** —— 承重的顺序不变量有 fold-invariant 的测量点 (Major, 不阻塞, 引入=是)

**执笔方的预判**: 「表 2 中它**明确拒绝断言**的 `SC-A-step (a)(b)` 行会被打」, 并主张这是
「本就只能诚实标注、无法机械化」。**我的回答: 这一条是「修错了」的一半 —— 不可断言的只有「编号」, 而编号恰是它自己声明的非承重量。**

**位置**: `proposal.md:304` (表 2 该行) × `:703` (`SC-A-step` (a)(b)) × `:896` (§Impact hunk ① 逐字)
× `openspec/changes/premerge-gate-mainbranch-failclosed/proposal.md:158`

**三句并列**:

- `:896` §Impact hunk ① 逐字:「(位于步骤 **2** 与 **2.5** 之间, 号建议 `2.2`; **号本身非承重, 承重的是它落在 2 与 2.5 之间**)」;
- `:703` `SC-A-step` (a)(b) 测的是:「按出现顺序提取**行首步骤编号** (`^[0-9]+(\.[0-9]+)?\.`)…(a) 存在编号 `N` 满足 `2 < N < 2.5`; (b) `N` 在提取序列中的**位置**恰在 `2` 与 `2.5` 之间」——**两腿都建立在「行首编号存在」这个表示形式上**;
- `:304` 表 2 逐字:「⚠️ **如实标注: A 此侧无法断言, 且不为它编造断言。** 折叠后行首编号是否保留取决于 B 尚未写出的落地文本」。

⇒ **Spec 自己说编号非承重, 然后把唯一的机械腿钉在编号上, 再因为编号会随 B 的折叠而不确定, 宣布整条无法断言。**
被牺牲掉的是**承重的那个量 (顺序)**, 而顺序有一个与折叠形态无关的测量点:

> 在同一区块内按**出现位置**断言 `resolve_ci_backend` 的出现 index < 新核验步标识 (如函数名 `_verify_branch_exists` / `#137`) 的 index < `evaluate_path_coverage(` 的 index。

这三个 token 是**步骤 2 / 新步骤 / 步骤 2.5 各自的内容锚**, 折叠 (`<details>` 包一层) 对它们的**相对顺序零影响**;
而这**正是执笔方本轮在 (c-含) 上亲自走通的第三条路** ——「**换的是标注什么/测什么, 不是自圆其说**」。
同一份文件在同一轮里, 一处走通了这条路, 另一处没走。

**委派也不覆盖被委派的量**: `:304` 逐字「**归属已成文在 B 侧**: B `:156` 逐字「折叠块须**补上 §3 新增的分支存在性核验步**」
⇒ **B 的 D1 自带重验本步的义务**」。我实读 B 侧 (该句实际在 **`:158`**, 见 F-8): 它保证的是
**「折叠块里要有这一步」**, 对**编号是否保留 / 步骤间顺序**一个字未提 ⇒ 委派的量 ≠ 被委派的量 (memory `delegate-verify`)。

**它在什么实现下会红**: B 的 D1 把步骤 1-5 折进 `<details>` 并改用无序列表 (折叠块内保留编号并非 B 的任何 SC 所要求) ⇒
`^[0-9]+(\.[0-9]+)?\.` 提取序列为空 ⇒ `SC-A-step` (a)(b) 在**完全正确的 B 实现下**从「必红」退化为「无从求值」,
而 A 已按「无法断言」交付, 无人接。改用内容序断言的实现在同一场景下仍可正常求值。

**⇒ 给 owner 的一句话**: 预判 ① 只有 **1/3 对** —— 「折叠后行首编号是否保留」确实不可断言 (这部分诚实标注是对的),
但由此推出「(a)(b) 整体无法断言」是**把非承重量的不可测, 当成了承重量的不可测**。

---

### f-7 · 表 2 的方向 2 归纳 `3 类 + 1 条 + 14 条 = 18` 是自相矛盾的划分 (minor, 引入=是)

**位置**: `proposal.md:314-317`

逐字:「18 条中 **B 落地会打爆的是 3 类** …另有 **1 条** (`SC-A-step (a)(b)`) A 此侧结构上无法断言…**其余 14 条**实测不受影响。」

**我按表 2 逐行清点 (总体 = A 的 18 行 SC; 范围 = 今日该文件; 计数法 = 逐行读表 2 的「判定」列并映射回 SC 名)**:

- 🔴 打爆: `SC-A10` · `SC-A10b` · `SC-A10c` (同一行三条) + `SC-A-baseline` = **4 行**;
- ⚠️ 无法断言: `SC-A-step` = **1 行** (它同时又在「3 类」的第一类 `(c-含)` 里 ⇒ **双计**);
- ✅ 不受影响: `SC-A-doc` · `SC-A-note` · `SC-A-cli` · `SC-A-sc22` + 9 条 (`A6/A13/A-zero/A7/A8/A11/A14/A-order/A-cwd`) = **13 行**。

⇒ **4 + 1 + 13 = 18**, 不是 3 + 1 + 14。且「一切不显式传 `main_branch` 的新 fixture」这**一类**按
`:311` 自己逐字「(但**全部适用**上面那条「必须显式传 `main_branch`」)」**覆盖到那 9 条**, 远不止 1 行。

**它在什么实现下会红**: 任何人拿归纳句当清单去核 Phase B 的处置面, 会漏掉「9 条也要显式传参」这半边
(虽然表体里写着), 并在核 18 条配平时数不平。**逐行判定全部正确, 错的只有归纳的算术** —— 故 minor。

---

### f-8 · R3-fix 新写文本中的四处 `file:line` 锚未命中被引文本 (minor, 引入=是)

逐条实读复核 (`awk 'NR==<n>'`):

| 引用处 | Spec 逐字声称 | 实读那一行 | 真实位置 |
|---|---|---|---|
| `:10` | 「逐字照 SOT `spec-drafter/LEVEL_GUIDE.md:26` 的 **Q2 三腿**」 | `:26` = `│      ├─ YES ─────▶ LEVEL 1 (Skip)     │` —— **Q1 的 YES 分支, 结论是 Level 1** | Q2 在 **`:29`** |
| `:15` | 「`standards/openspec/project.md:116` 逐字「**2 \| Minimal \| Medium features (1-3 days) \| proposal.md**」」 | `:116` = `\| 1 \| Skip \| Simple fixes, typos \| No spec needed \|` | 该行是 **`:117`** |
| `:304` | 「B `:156` 逐字「折叠块须**补上 §3 新增的分支存在性核验步**」」 | B `:156` = `` `<details><summary>helper 内部算法…</summary>` … `</details>`。`` | 该句是 B **`:158`** |
| `:200` | 「B `:161` 逐字把**步骤 1-5 整体折叠**」 | B `:161` = 「🔴 **折叠块之外必须留下 `<MAIN_BRANCH>` 的取值来源** (**SC-M16** 钉住)…」 | 折叠那句是 B **`:154`/`:156`** |

**被引内容全部真实存在**(四处结论均不受影响), 错的是可复跑性 —— 与 R2 抓的 `:337`→`:335`、
R3 抓的 `ls | grep` 得 55 属同一形状 (memory `reporter-miscite`)。
⚠️ 其中**第一处最误导**: `:26` 逐字指向的是「LEVEL **1**」, 而句子用它论证「Level **2**」。

---

### f-9 · BLOCKER 实证 2 的四个 TASK 数是「含 `TASK-` 的行数」, 真实任务条目是它的 1/3 (minor, 引入=是)

**位置**: `proposal.md:64-66`

逐字:「逐个核 frontmatter: `2026-05-29-aria-context-monitor` …/ **31** 条 `TASK-` · `…ai-native-estimator` … **21** 条 ·
`…emergency-hotfix-and-audit-file-scope` … **19** 条 · `…state-scanner-gate-yaml-datasource` … **28** 条」。

**三项并列**:
- **总体**: Spec 数的是「`detailed-tasks.yaml` 中**含 `TASK-` 串的行**」(含 `dependencies:` / `notes:` / 散文交叉引用);
  我数的是「**任务条目**」;
- **范围**: 今日 `/home/dev/Aria/openspec/archive/` 的同四个目录;
- **计数法**: Spec = `grep -c 'TASK-'`; 我 = `grep -cE '^\s*- id: *"?TASK-'`, **并与各文件 `metadata.total_tasks` 交叉核对, 4/4 相等**。

| 目录 | Spec 报 | `grep -c 'TASK-'` (复现 Spec) | 任务条目 | `metadata.total_tasks` |
|---|---|---|---|---|
| aria-context-monitor | 31 | **31** ✅ | **9** | 9 |
| ai-native-estimator | 21 | **21** ✅ | **8** | 8 |
| emergency-hotfix-… | 19 | **19** ✅ | **8** | 8 |
| state-scanner-gate-yaml-… | 28 | **28** ✅ | **10** | 10 |

⇒ Spec 的数**逐个可复现**, 但它量的不是它声称的东西 (「**条** `TASK-`」在语境里指的是任务条数),
**3-4 倍膨胀**; 与本文件自己在 `SC-M3` 上抓的「前缀伪命中」是同一类计数法错误。
**承重结论 (路径 B 仍出带编号的机读载体) 不变** ⇒ minor。

---

### f-10 · §4 `:500` 声称「把该段改写为英文不在本 Spec 授权范围内 (**§非目标**)」, 而 §非目标九条中无此条 (minor, 引入=是)

**位置**: `proposal.md:500` × `:841-853` (§非目标 全部九条)

我实读 §非目标 九条 (`--main-branch` 缺省 / `SKILL.md` 既有裸命令与折叠块 / `aether.py` / `main_branch` 自动解析 /
`path_coverage.py` / `aether` CLI 语义 / `workflow-runner` schema / `no_ci_fallback` / 同形兄弟位置) ——
**无一条涉及 `_build_output` docstring 的语言**。

**它在什么实现下会红**: 实施者把 §非目标 当作「不做什么」的 SOT 清单 (它就是干这个的), 顺手把该 docstring
改写成英文 (整份文件除该段外首行本就是英文, 统一语言是很自然的动作) ⇒ `SC-A-note` (d) 腿的中文 token
(`各早退分支(…)保持…六键不变`) 零命中 ⇒ **对一个行为完全合规的实现恒红** —— 这正是 `:498-499` 自己点名要防的失效方向。
**约束本身写在 `:500` 是有效的, 缺的只是它没落进 §非目标** ⇒ minor + 一行修法 (§非目标 补一条)。

---

### f-11 · 表 1 称「这 6 条正是 DEC §2 点名过户给 A 的号段」, DEC §2 实为 **7 条** (含 `SC-M10`) (minor, 引入=是)

**位置**: `proposal.md:267` (表 1 行) · `:311` (表 2 行「DEC §2 过户号段」) × `DEC-20260812-001:42`

DEC `:42` 逐字:「**SC**: SC-M6 · M7 · M8 · **M10** · M11 · M13 · M14 (行为面, 已打磨八轮)」= **7 条**;
DEC `:114` 再次逐字列同一组 7 条。A 两处都写「6 条」并列举 `M6/M7/M8/M11/M13/M14`。

**覆盖面无缺口** —— A 确有 `SC-A10`, 且表 1 把 `SC-M10` 单列一行核销 (「A 的同款负控是 `SC-A10`」);
B 侧 `tasks.md:77` 也逐字把 `SC-M10` 挂在 `TASK-008`(即过户给 A 的那条实现任务) 上, **方向与 DEC 一致**。
⇒ 错的只是对**划界 SOT 的转述**。**它在什么实现下会红**: 任何人拿 DEC §2 与 A 对账「A 是否接全了」,
会得到 7 vs 6 的差并去找那条不存在的缺口 ⇒ minor。

---

## 3. 直接回答任务书的四个问题

### 问题 3 —— 复核执笔方自己预判的三处

| 预判 | 我出条目了吗 | 是「修错了」还是「本就只能诚实标注」 |
|---|---|---|
| ① 表 2 中拒绝断言的 `SC-A-step (a)(b)` | **是 → F-6 (Major)** | **修错了 (部分)**。不可断言的是「折叠后行首编号是否保留」; **承重的顺序不变量可断言且有 fold-invariant 的测量点** (内容序: `resolve_ci_backend` < 新步骤锚 < `evaluate_path_coverage`)。§Impact `:896` 自己逐字写着「**号本身非承重**」, 而 (a)(b) 恰恰只测号。**这正是执笔方本轮在 (c-含) 上走通的同一条第三路** —— 一处走通了, 这处没走 |
| ② §交付义务「完成判据」是人工判据 (贴 `git show --stat`) | **否 —— 我不在此出条目** | **本就只能诚实标注**。O-1 断言的是「**某次未来的发布提交里 gitlink 被 bump 了**」, 这是**发布时点的仓状态**, 不是代码性质 ⇒ **任何随 A 一起 merge 的单测都测不到它** (它在 merge 之后才发生)。A 已把「要不要先补一个 gitlink 方向的 custom check」正确地上呈为 `D-b` 并注明「那会新开一个 change, 不在 A 的交付面内」。**这是 R3 M-2 的正确闭合形态, 不应被 R4 逼着编造机械量** (memory `false_green_dual_is_permanent_red`: 为它硬造一个量只会得到恒绿或恒红)。⚠️ 唯一需要改的是 **F-1** —— 不是这一列, 而是同一张表旁边那句「⇒ 路径 B 出一条 TASK」的机械语气 |
| ③ `SC-A-note` (d) 腿 token 与语言绑定 | **是, 但只出 minor → f-10** | **收口方向对, 落点没落地**。`:497-501` 的处理 (点名风险 + 禁止改语言 + 说明为什么恒红) 是正确且完整的; 缺的只是它声称的家 (§非目标) 里没有这一条。我实读 `pre_merge_gate.py:241-246` 确认该段今日确为中文且 `各早退` / `分支 (…)` 被源码换行拆开 ⇒ **抹空白规则是必需品而非修辞**, (d) 腿本体我判**真闭合** |

### 问题 4 —— 复核四条「不同意」与双向清点表

**关于对 tech-lead 二元框架的反驳 (「换的不是是否标注, 而是标注什么」)**: **这个第三条路成立, 我认可。**
`:207-208` 给出的那句 (「本步只核验 `main_branch` 在 `<remote>` 上存在, 不保证后续步骤查询的是同一个分支;
两处分支名的收敛见 `#137`」) **陈述的是本步的契约而非别处的缺陷**, 在 B 落地前后都为真;
`#137` 退化为溯源指针与 `SKILL.md:242`(`aria-plugin #122`) / `:253`(`#126`) 的既有惯例同形 (我实读确认)。
⚠️ **但这条走通的路只走到了三个落点** —— 第四个落点 §非目标 `:844` 仍写着旧要求 (**F-2**),
而**同一条路本可以再走一次去救 `SC-A-step (a)(b)`** (**F-6**)。

**表 1 (20 行) 有没有数漏**: **没有。** 我实跑 `grep -c '^| \*\*SC-M'` = **20**, 并逐名核对
`M1/M2/M3a/M3b/M3c/M4/M5/M6/M7/M8/M9/M10/M11/M12/M13/M14/M15/M16/M17/M18` **20/20 全部在表内**;
`SC-M3` 前缀伪命中的诊断我复跑属实 (`grep -o 'SC-M[0-9]*'` 会把 `SC-M3a/b/c` 各计一个 `SC-M3`)。
`SC-M18` 的四文件操作数我实跑 = **2/4/3/0**, 与 Spec 逐字一致。

**表 2 (18 条) 有没有数漏**: **覆盖无缺口** (18/18 逐条在表内, 我按 SC 名核对),
**但归纳的算术错了** (f-7), 且其中一行的判定过度收口 (F-6)。

---

## 4. 席位结论 —— 划界自足性 / 定档 / 与 B 的边界

**划界自足性**: **代码面自足** (§1–§6 + 18 条 SC 足以让一个未读 B 的实施者写出正确实现),
**交付面不自足**: 六项交付义务的路由是**声称的机械路由 + 实际的执行者纪律** (F-1),
且 owner 裁定的 A.1 迁移动作有一条**从未落地也从未上呈** (F-3)。

**定档**: Level 2 的三腿走一遍是**方向正确的新结构**, 但 (b) 用自造谓词代替 SOT 的四条件 OR 列表 (F-4),
(c) 的答案是另一个未裁问题的函数而同文件明令不得合并处理 (F-5), 两处 SOT 锚还都错行 (f-8)。
**MINOR 定档本身我认可** (additive API + `:435` 唯一接线点 + 25 个调用点零破坏, 我核过口径),
`:971-975` 的规则 #10 留痕形态标准。

**与 B 的边界**: **重叠已被两张表压到很低** —— A→B 的 5 条拒绝域全部被类级禁令覆盖;
B→A 的 3 类全部有处置。**残余的缺口只有一条, 且不在 SC 层**: B 的 `TASK-003…009` 七条仍 `pending`
且无 `cancelled` 痕迹 (F-3) —— 这是 A/B 之间**唯一一处「两侧都以为对方会处理」的真实风险**。

---

## 5. 本轮 fix 引入率 (三项并列, 不修饰)

**总体** = 本席 R4 的 11 条 finding; **范围** = R3-fix 版 (`ff847fb`) 的 `proposal.md`;
**计数法** = 逐条判「该条指控的文本 / 矛盾是否由 `git diff 017eb54 ff847fb` 引入」。

⇒ **10 / 11 = 91%** (仅 F-3 为存量)。**Major 口径 = 5 / 6 = 83%。**

**对照**: R3 tech-lead 自报 5/8 = 63%; R3 aggregate 全席 19/24 = 79%。
`git diff --numstat` 实测 R3-fix = **+384 / −77** —— 三轮里体量最大的一次改动。

⇒ 按 memory `marginal-return-negative` 的判据 (「本轮 fix 引入的 major 占比 > 1/2 即到拐点」),
**本席数据 83% 已明确越过拐点**; 按 `stop-adding-rounds` 的判据 (「major 数是否还在降」),
本席 R3 6M → R4 6M **持平**。**「再加一轮」不是可支持的处方; 「换新鲜眼睛」或「owner 降级裁定」才是。**

**同时必须记录的正面事实** (否则下一轮会把它们改掉):
Critical **连续三轮归零** (B 侧四轮从未做到) · **R1 的 2C 与 R2/R3 的旧 finding 无一复发** ·
本轮 14M 中 **11 条真闭合**且其中 4 条 (19/24 动态测量 / SC-M18 四分量 / `_build_output` docstring / 表 1 的 20 行)
我**独立复跑逐字复现**。**执笔环节仍然不是问题** —— 问题是**每修一条仍引入约等量同形状的新条目**,
而 R3-fix 的三处最大新增 (BLOCKER 全块重写 / 表 2 / §交付义务) 恰好贡献了本席 6 条 Major 中的 5 条,
**印证执笔方自己给出的结构性理由: 对尚不存在的文本 (B 的落地文本 / A.2 的产出) 的断言, 是产 finding 最多的类别。**

---

## 6. 判定

**VERDICT: PASS_WITH_WARNINGS** (0 Critical + 6 Major + 5 minor) · **VOTE: REVISE** · 5 条 `blocks_phase_b`。

- **不判 FAIL**: 无 Critical。A 的代码面规格自足、可实施, 18 条 SC 逐条有今日实测与红机制,
  且 R4 的 3 条 Critical 确属 B 侧, 我逐条核过**无一污染 A**;
- **不判 PASS**: F-1/F-2/F-3 三条各自会让「完全合规的实施者」产出与 Spec 意图相反的结果,
  F-4/F-5 使 `D-c` 这个 Phase B 前置裁定点的输入不完整。

**若 owner 的目标是「不带 Critical 进 Phase B」**: A 已连续三轮达标, 且本轮六条 Major 中
**F-2 / f-8 / f-10 / f-11 是逐行可改的小改** (合计 < 10 行), **F-1 是删两处措辞**,
**F-3 是二选一 (执行 DEC §5.3 或升为 `D-d`)** —— **这五条不需要再开一轮审计就能收口**;
真正需要 owner 表态的只有 **F-4 / F-5 (定档的两条腿) 与 F-6 (要不要为承重顺序补一个 fold-invariant 断言)**。
