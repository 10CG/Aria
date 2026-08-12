---
checkpoint: post_spec
mode: convergence
rounds: 3
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-12T17:20:00.000Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_spec R3 汇总 — Spec A `premerge-gate-branch-existence`

## 投票

| 席位 | VOTE | VERDICT | C+M+m | 阻塞 B | R2-fix 引入 |
|---|---|---|---|---|---|
| code-reviewer | REVISE | PASS_WITH_WARNINGS | 0+5+6 = 11 | 3 | 9 |
| tech-lead | REVISE | PASS_WITH_WARNINGS | 0+6+2 = 8 | 5 | 5 |
| qa-engineer | REVISE | PASS_WITH_WARNINGS | 0+1+1 = 2 | 0 | 2 |
| knowledge-manager | REVISE | PASS_WITH_WARNINGS | 0+1+1 = 2 | 1 | 2 |
| backend-architect | **PASS** | PASS_WITH_WARNINGS | 0+1+0 = 1 | 0 | 1 |

**4 REVISE / 1 PASS** · 五席 verdict 全 `PASS_WITH_WARNINGS` · `converged: false`。
原始 **0C + 14M + 10m = 24** · 9 条 `blocks_phase_b` · R2-fix 引入 **19/24 = 79%**。

## 三轮轨迹 — 一个清晰且不乐观的形状

| 轮 | 投票 | 原始 | **Critical** | fix 引入率 | 阻塞B |
|---|---|---|---|---|---|
| R1 | 5R/0P | 26 | **6** | — | 14 |
| R2 | 3R/2P | 23 | **0** | 74% | 7 |
| R3 | **4R/1P** | 24 | **0** | **79%** ↑ | 9 |

**好的一面**: **Critical 连续两轮归零** —— B 侧 post_planning 四轮 (3→1→2→3) **从未做到**。
**坏的一面**: **Major 持平 ~13-14** · **引入率 74%→79% 继续升** · **REVISE 从 3 退回 4**。

⇒ **「兄弟位置清点」这个新方法没有压下引入率。** 它确实抓到了真东西
(R2-fix 靠它挖出第三处对撞 SC-M15), 但**每修一条仍然引入约等量新条目**。

⇒ 与 B 侧四轮**同一形状**: **对单条 finding 收敛, 对总量不收敛**。
差别只在 A 侧的**严重度天花板更低** (0 Critical vs B 的每轮 1-3 条)。

## 🔴 本轮最重的发现: 我写的 BLOCKER 块前提是假的

**`🚧 BLOCKER` 逐字断言「Level 2 ⇒ A.2/task-planner 不出 tasks.md ⇒ 三项义务的唯一载体是
一份 D.2 就会被归档的散文」, 两条出路据此写成 (i) 保持 Level 2 只留痕 / (ii) 取 Level 3 出 tasks.md。**

**tech-lead 实读证伪**:
- `task-planner/SKILL.md:52-66` 逐字:「IF tasks.md 存在 → 路径 A: 双层架构; **ELSE → 路径 B:
  从 proposal.md 分解任务 → 输出: 仅 detailed-tasks.yaml**」⇒ **无 tasks.md 触发的是路径 B,
  仍产出带 `TASK-{NNN}` 编号与逐条 status 的机读载体**;
- **实证 (非推断)**: 实跑归档目录得 **4 例**「有 `detailed-tasks.yaml` 而无 `tasks.md`」,
  逐个核 frontmatter —— `2026-05-29-aria-context-monitor` 逐字「**Level**: 2」其 yaml 有 **31 条** TASK-;
  `2026-05-30-ai-native-estimator` 「Level: 2」**21 条**; `2026-07-22-state-scanner-gate-yaml-datasource`
  「Spec Level: 2」**28 条**。

⇒ **owner 被要求在一个错误的二选一上裁定** —— (ii) 的代价被写成「交付面变大、拆分收益缩水」,
而**保持 Level 2 同样能拿到逐条 task 载体**。

⇒ **真实缺口被这个假前提遮住了, 且它在 Level 2 内可修**: 路径 B 逐字「**始终从 proposal.md 读取
`## Success Criteria` 章节**」, 而 O-1/O-2/O-3 与 F-1/F-2/F-3 **全部不在 `## Success Criteria` 里**
(在 §Impact / §Rule #6 / 文首 BLOCKER) ⇒ **能否被分解成 TASK 取决于写在哪一节, 与 Level 无关。**

**⚠️ 编排层第 14 条错误**: 我把一个该由 owner 裁的决定, 建立在一个我没有回源核实的前提上。
形状 = 第三族「只引对我的结论有利的那一段」的变体 —— 这次不是引文有偏, 是**前提根本没查**。

## 第二重: 出路 (i) 的兜底也不成立

(i) 逐字「O-1 由 phase-c-integrator §C.2.5 既有自动化 + 双推 `ls-remote` 核验兜 gitlink 那条腿」。

**实读 §C.2.5 六步**: 全流程核的是「**本地已有的那个 commit 有没有原样到达每个 remote**」,
`expected_sha` 就是本地 HEAD —— **与「那个 commit 里的 gitlink 有没有被 bump」是两条正交的轴**;
没 bump 也全绿。唯一真读 gitlink 的是 §C.2.4.5, 而 `:194` 逐字「pass: 所有 submodule pointer 是
forward bump 或 **no-change** 或 first-time」⇒ **「未 bump」= no-change = PASS**。

⇒ A 按 MINOR ship、忘了 `git add aria` ⇒ C.2.4.5 判 no-change PASS · C.2.5 六步全绿 ·
`m6-version-badge-match` 对该方向失明 ⇒ **全绿而 `clone --recursive` 拿到旧 plugin**
—— 正是 A 自己在 O-1 行点名的 B 侧 R4 Critical (TASK-017) 的形状。**memory `invariant-dimension`。**

## 第三重: 兄弟位置清点只做了 **A→B 一个方向**

R2-fix 的清点表起手是 `grep -n 'SC-M' B/proposal.md` ——「**A 是否会打爆 B 的 SC**」。
**反方向 (B 正确落地会不会打爆 A 的 SC) 一条都没查**, 而 A 新增的三条 doc 侧 SC
**全部断言 `SKILL.md` 内容 —— 正是 B 的 D1 要重写的那一段**。R3 因此抓出:

- **`SC-A-step` 的 (c-含) 腿正是 A 自己判为 landmine 的哨兵形态** —— 它要求新步骤正文标注
  「步骤 3 仍硬编码 `main`」; 而 B 落地后步骤 3 读占位符、`#137` 可闭
  ⇒ 留着标注 = **随 plugin 分发一句同页面即可证伪的假话** (违反规则 #3);
  删掉 = **在完全正确的 B 实现下必红**。两条路都坏;
- **三条禁令不含 `--pr-branch`** —— 同一张表在 `SC-M3c` 行用的前提, 正是它在 `SC-M15` 行推翻的那个;
  A 写一句「(对应 CLI 的 `--remote` / `--pr-branch` 同批传入)」即可过 A 侧 18/18 并 ship,
  而 B 折叠后 `SC-M3c` 计数 1 ≠ 0 ⇒ **B 一条负控在正确实现下必红**。

## 第四重: `SC-A14` 腿 2 的红机制建立在错误的总体上

腿 2 的「怎么会红」依赖 `sys.stdout.errors == 'strict'`，而那是**在裸 `python3 -c` 里量的,
不是在这条 SC 将要运行的总体里量的**。qa/tech-lead 用受控探针实测三种情形:
裸 python ⇒ strict/抛 · **`pytest -q` (默认 fd 捕获) ⇒ `errors=replace`/成功不抛** ·
`pytest --capture=sys` ⇒ strict/抛。且实跑 `find` 确认**无任何 pytest 配置覆盖默认值**,
而 §测试基线自己写的复跑方式就是 `pytest`。

⇒ **对坏实现恒绿**: 只做入口解码不做出口净化的实现, 在 `errors='replace'` 下三条断言全部成立
⇒ 而 R1→R2 整条修复链 (入口解码 → 出口净化) 的**唯一机械腿就是它**。

## 处置

`max_rounds` 4 (A 侧), 已用 **3**。**只剩 1 轮。**

**A 侧 Phase B 仍被阻断** (9 条 `blocks_phase_b`)。Rule #10: AI 不得自行豁免。

### 交给 owner 的判断材料 (AI 不代裁)

三轮数据现在支持一个比「拆分能收敛」更精确的结论:

**拆分把「严重度」压住了 (Critical 6→0→0, B 侧从未做到), 但没有改变「总量稳态」**
(Major ~13-14 持平, 引入率 74→79% 上升)。

⇒ 若 owner 的目标是「**不带 Critical 进 Phase B**」, A 已经连续两轮达标;
⇒ 若目标是「**收敛 (全席 PASS)**」, 三轮数据不支持"再一轮就能到"的预期。

**⚠️ 且本轮暴露: 我给 owner 的那个二选一建立在假前提上** (Level 2 并非无 task 载体)。
BLOCKER 块须先按实证重写, owner 才有可裁的真实选项。
