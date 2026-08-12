---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: false
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-08-12T16:05:00.000Z
context: openspec/changes/premerge-gate-branch-existence/proposal.md
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_spec R2 汇总 — Spec A `premerge-gate-branch-existence`

## 投票

| 席位 | VOTE | VERDICT | C+M+m | 阻塞 B | R1-fix 引入 |
|---|---|---|---|---|---|
| tech-lead | REVISE | PASS_WITH_WARNINGS | **0**+5+3 = 8 | 4 | 6 |
| code-reviewer | REVISE | PASS_WITH_WARNINGS | **0**+4+4 = 8 | 3 | 7 |
| knowledge-manager | REVISE | PASS_WITH_WARNINGS | **0**+1+3 = 4 | 0 | 2 |
| backend-architect | **PASS** | PASS_WITH_WARNINGS | **0**+2+0 = 2 | 0 | 2 |
| qa-engineer | **PASS** | PASS_WITH_WARNINGS | **0**+1+0 = 1 | 0 | 0 |

**3 REVISE / 2 PASS** · **五席 verdict 全部 `PASS_WITH_WARNINGS`** · aggregate verdict **PASS_WITH_WARNINGS**
(0 Critical + ≥1 Major) · `converged: false` (收敛定义 = 结论稳定 **AND** 全席 PASS)。
原始 **0C + 13M + 10m = 23** · 7 条 `blocks_phase_b` · R1-fix 引入 **17/23 = 74%**。

## ⭐ 本轮的两个决定性事实

### 1. **Critical 归零** —— 本 session 九轮审计里第一次

| Spec | 轮次 | Critical |
|---|---|---|
| B 侧 post_planning | R1 → R2 → R3 → R4 | 3 → 1 → 2 → 3 |
| **A 侧 post_spec** | **R1 → R2** | **6 → 0** |

### 2. **五席独立确认 R1 的 2C 是真闭合, 不是 paper-fix**

本轮任务书**显式要求区分「写下来」与「闭合」** (memory `feedback_paper_fix_antipattern`)。五席逐条回源后一致判定真闭合:

- **backend-architect**: 「C-1 与 C-2 均逐字回源验证为**真闭合**。实读 `SKILL.md:238-262` 确认执行流程确实给的是裸命令 (非 Helper 调用指令), 实测 `git ls-remote`…」
- **code-reviewer**: 「R1 的 2C + ~10M **实质全部闭合**, 不是「写下来」。C-1 划界承重句 = **声称缺陷**, 其唯一可能的闭合形态就是**更正后的声称 + 传播到所有承载该声称的文档**」
- **qa-engineer**: 「C-1 真闭合。三文档 (Spec A §根因+§残余暴露、B 侧抬头更正块、DEC 更正块) 本轮**独立交叉核实**, 日期一致」
- **knowledge-manager**: 「两条 Critical 均**真闭合, 非 paper-fix**」
- **tech-lead**: 「2C 都真闭合, **不是纸面修复**; ~10M 中 **11 条闭合 / 3 条部分闭合**」

⇒ **A 的划界与 Rule #6 定档现已站得住。** 剩余全部是 Major 及以下。

## ⚠️ 但 R1-fix 引入率 74%, 高于 B 侧的 71%

| | fix 引入率 |
|---|---|
| B 侧 R1→R2 | 53% |
| B 侧 R2→R3 | 70% |
| B 侧 R3→R4 | 71% |
| **A 侧 R1→R2** | **74%** |

⇒ **拆分没有降低「每轮 fix 引入新缺陷」的比率。** 它改变的是**严重度与绝对量**:
26 → 23 条, 而 **6C → 0C**。

**诚实的读法**: 拆分**不是**收敛率的解药; 它的收益在于**把 Critical 挤出去了** ——
R1 的 6C 全部出在「拆分时新写的声称」上, 修掉即归零;
而 B 侧的 Critical 每轮都从**新的条款间接缝**里长出来, 因为条款基数大得多。

## 本轮 Major 的形状 (13 条, 择要)

- **「新增 §C.2.4 编号步骤」是 Rule #6 第二行定档的唯一承重依据, 却零机械锚** ——
  16 条 SC 中唯一读 `SKILL.md` 的 `SC-A-doc` 只解析 schema json 块 (hunk ②),
  对 hunk ①(编号步骤) 与 ③(`:279` 四类→五类) **零断言**
  ⇒ 只改 hunk ② 也 16/16 全绿, 而定档依据当场不存在。
  **同形复发**: R1 抓的正是「§3 自称唯一合法插入点却零 SC」, R1-fix 用 SC-A-order 补了**代码侧**,
  **doc 侧同款顺序约束没补** (memory `fix-the-class`)。
- 🔴 **A 新增的 SKILL.md 步骤会撞 B 侧承重 `SC-M3a` 的精确计数** ——
  B 的 SC-M3a 期望 `grep -c -- '--main-branch "<MAIN_BRANCH>"'` **恰为 2**;
  A 若按最自然形态写一行带参 helper 调用示范 ⇒ 出现第 3 处 ⇒ **B 一条打磨八轮的承重红窗在完全正确的 B 实现下必红**。
  ⚠️ A **已认出该形状的另一实例并处置了** (§4 逐字「示例的 `branch` 用占位符 —— 写 `"main"` 会与 B 侧 SC 对撞」),
  **同一类只检查了一个实例**, 漏掉的恰落在两 Spec 的接缝上 (memory `fixes-contradict`)。
- **`SC-A-cli` / `SC-A-cwd` 对 backend 这个 ambient 零安排** —— 实测
  `AetherBackend.probe()` = `shutil.which("aether")`; 在没有 aether/gh 的机器上,
  接线正确与漏接线的实现**都在 `:339` 早退返 green** ⇒ 两条 SC **对正确实现恒红**。
  ⚠️ 同轮已有正解只推广了一半: 打桩边界表给 SC-A11 的注正是缺的那句;
  且 A 只防了 `origin` 这一个 ambient, **没防 backend 这个 ambient**。
- **`SC-A-doc` 的代码侧操作数未定义** —— 两种落地方式各损失它声称能力的一半。
- **Level 2 的三项义务零承载, 而「须 owner 裁量」这句本身没有消费者** ——
  A.2 读 frontmatter `Level: 2` ⇒ 不出 tasks.md ⇒ 三项义务的唯一载体是 D.2 就会被归档的散文;
  **memory `fix-recurs-in-fallback` 的「有记录 ≠ 有路由」**。

## 处置

`max_rounds` 4 (A 侧), 已用 **2**。**verdict 已由 FAIL 升到 PASS_WITH_WARNINGS, Critical 归零。**

**未收敛** (3 REVISE, 收敛要求全席 PASS)。R2-fix 后 R3。
**A 侧 Phase B 仍被本闸门阻断** (7 条 `blocks_phase_b`)。Rule #10: AI 不得自行豁免。

### R2-fix 的方向

1. 给 hunk ①/③ 补机械锚 (doc 侧顺序约束, 与 SC-A-order 同形);
2. 🔴 **消解与 B 侧 SC-M3a 的对撞** —— 二选一: A 明文规定新步骤不得含该字面 /
   A 明文声明该步骤使 SC-M3a 期望值由 2 变 3 并写进 B;
3. `SC-A-cli` / `SC-A-cwd` 补 mock backend (照 SC-A11 已有的那句);
4. `SC-A-doc` 规定代码侧操作数;
5. Level 2 的三项义务: 升 BLOCKER 字段 (A.2 入口须读) 或取 Level 3 出 tasks.md —— **owner 裁量**;
6. 两条 minor: follow-up 归属声明 (A/B 各自声称要开同一组) · 继承 B 已成文的「AB 套件对 C.2.4 覆盖薄」限定。
