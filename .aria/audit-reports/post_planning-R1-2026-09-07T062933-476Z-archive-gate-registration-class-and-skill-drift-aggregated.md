---
checkpoint: post_planning
round: 1
mode: convergence
verdict: FAIL
converged: false
scope_ok: true
counts: 1C/~20M/~15m (四席原始 36 条; 反驳席推翻 1)
clusters: 1C
teams: [aria:tech-lead, aria:backend-architect, aria:qa-engineer, aria:code-reviewer]
sibling_probe: no_sibling_found
timestamp: 2026-09-07T06:29:33.477Z
context: openspec/changes/archive-gate-registration-class-and-skill-drift/tasks.md
drift_terminated: false
drift_check_skipped: true
oscillation: false
overridden_by_user: false
degraded: false
max_rounds: 5
rounds_total: 1
---

# post_planning R1 — archive-gate-registration-class-and-skill-drift

## Round 1

- **Sibling probe**: `no_sibling_found`
- **对象**: tasks.md (A.2 产物); proposal 已过 post_spec R1→R5, 本轮**不重审设计**

### 逐席 verdict

| 席 | verdict | 原始 | 结论 |
|---|---|---|---|
| aria:tech-lead (1:1 覆盖) | PASS_WITH_WARNINGS | 12 | **覆盖面完整**: B/C/D/E/SC 五维**零漏项**, 一个孤儿 (E-1)。12 条全落在「转写时丢了 proposal 的承重限定词」这一形状 |
| aria:backend-architect (可执行性) | PASS_WITH_WARNINGS | 8 | 8 条会让两个独立执笔者产出不同东西 |
| aria:qa-engineer (验收闭环) | **FAIL** | 6 | **1C + 4M + 1m** |
| aria:code-reviewer (风险与顺序) | PASS_WITH_WARNINGS | 10 | 「核心问题不在写什么, 在**什么时候写、谁先写**」 |

## Critical — C-4 的触发条件写反了 (ACC 席)

tasks.md 原文: 「**C-4** **B-1 落地后**重跑 C-1 锚点唯一性 —— **B-2** 改 `:318` 会威胁它」。
**同一行里触发条件写 B-1, 而它自己写着威胁来自 B-2。** proposal `:90` 与 SC-5 都明写「B2 落地后」。

主控复核: C1 的 SKILL.md 侧锚点是 `"(> 归档 SHA 回链:[^"]*填入)"`, 只有 `:317` 以「填入」结尾。B-1 只把 `:317` 内的 `Step2` 换成 `Step 7`, **锚点数恒为 1**; 唯一能把它推到 2 的是 B-2 对 `:318` 的改写。
⇒ 按字面执行, **守卫在风险发生前就被打勾**, 而 B-2 真正落地后无人复核 ⇒ SC-5 该条名存实亡。**已订正为 B-2 之后。**

## 主控独立复核的三条 (两条确证, 一条部分不成立)

| finding | 复核 |
|---|---|
| RISK: 「TG-B/TG-C disjoint 被 C-3 证伪, 且 `test_gate_yaml_datasource.py:237` 逐字断言那个串会与 C-V2 打架」 | **结论对, 理由错。** 全仓 `grep -rn '归档 SHA 回链' aria/skills/*/tests/` **零命中** ⇒ 无测试断言那个串。但**结论成立**: C-3 的基线态确实要**读** TG-B 正在改的 SKILL.md ⇒ 基线态必须排在 B-1/B-2 之前; 其余四态用 `CLAUDE_PLUGIN_ROOT` 指向 scratchpad 夹具即可 (Phase A.1 就是这么跑的), **tasks.md 没写明这一点** |
| RISK: 「主仓本地 master 落后 origin/master 7 个 commit」 | **确证且更糟**: 实测 local `9f25a66` vs origin/master `2f7ad0c` = **落后 8 个**。并发轨在我合并 PR `10CG/Aria#202` 后又 ship 了 8 次 |
| EXEC: 「E-5 的 grep 方法论对 `aria/CHANGELOG.md` 是错的 —— 它是 append-only」 | **确证。** `aria/CHANGELOG.md:13` 是 `## [1.71.1] - 2026-09-06`, **历史条目, 改了就是伪造历史**。我把它算进「23 处要同步的版本串」是实打实的错 ⇒ 要改的是 **22 处 / 12 文件**, 外加 CHANGELOG **新增**一条 |

## R1 修订 (tasks.md 119 → 138 行, 勾选项 44 → 62)

**结构性四项**:
1. **顺序依赖显式化**: 「TG-B/TG-C disjoint」改为**有条件**并行 —— C-3 基线态必须在 B-1/B-2 之前; C-4 必须在 **B-2** 之后; 其余四态用夹具不写仓内文件。
2. **验收补全**: B-V1 拆成 B-V1a (区段外==0) + **B-V1b (区段内按内容钉死)** —— 原版只编码了 SC-1 的一半, 丢掉的那半正是 B-6 的守卫; 新增 **B-V7** (B-2 专属验收, 因通用 post-condition 对 `:317`/`:318` 是**空检查**); 新增 **C-V3** (C-2 注册生效核验 —— 原版「注册了但没被扫到」与 Part A 的零触达故事同构)。
3. **反自证加固**: B-V2 要求把六条改后原文**逐条抄进 tasks**; B-V6 要求 CHANGELOG 条目**点名**改的 Step 与退役项; **E-V1 改为对 handoff 文件 grep 四个固定字符串, 缺一即红** (原版纯执笔者自觉)。
4. **顺序与并发**: 新增 E-0 的「卡住时怎么办」(只挡 E-9, 不挡 E-2..E-8) + **E-0b** (SC-11 若得 (b) 裁定的补跑任务, 原版无落点) + **E-7a** (merge 前 fetch + local-master parity 断言) + E-9 的 GitHub 补推步骤。

**已知风险从 3 条增到 6 条**: 补「并发轨在飞 (master 落后 8)」「负控夹具必须还原 (若图省事改了仓内 `spec_complete.py` 须 checkout 还原)」「服务端合并的 GitHub 补推」。

**B-V3 从绝对行号改为按内容**: 原写「唯一命中在 `:275`」, 而前面几个 B 任务会移动行号 ⇒ 改为断言该行**内容**。

## 机械自检的自证

修订后跑 `check_bare_issue_refs.py`, **立刻抓到我在本次修订里新引入的 2 处裸引用** (`#165` / `#202`)。修完两文件均 rc 0。
—— 这条检查从 post_spec R3 建立到现在, 已经抓到主控自己 **3 次**违反 (R3 修订前 3 处 / R4 新增 3 处 / 本次 2 处)。它是本 cycle 里唯一一条持续产出的机械守卫。
