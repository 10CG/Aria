# 决策: DEC-20260625-001 - session-closer 综合方案 (会话收尾正交仪式)

> **日期**: 2026-06-25 | **模式**: technical
> **来源**: brainstorm (本对话, 5 决策逐个收敛) | **承接**: DEC-20260605-001-skills-matrix-optimization (轴 2)
> **Authored by**: Claude Opus 4.8 via `aria:brainstorm`, 2026-06-25
> **ship_target**: aria-plugin v1.49.0 → **v1.50.0** (MINOR, 新 skill; 旧 spec 的 v1.40.0 已过期, A.1 spec-drafter 须 cat plugin.json 复验) | 主仓 1.7.1

---

## 背景

owner 在第三方项目用 Aria, 输入 "执行对话收尾" 期望走一套 5 步会话收尾 (0 本地/远程同步 / 1 未完成任务讨论 / 2 待固化经验 / 3 UPM·US·Spec·PRD 四维一致 / 4 收尾+交接), 但实际命中**十步循环 Phase D** (phase-d-closer)。owner 明确诉求: **对话维度的 skill 激活不应与十步循环 skill 混淆**。

调研发现: 该 5 步**之前已立项实现** —— Spec `session-closeout-internalization` (Approved, Phase A.2 CONVERGED, **Phase B 9/10** + Rule #6 benchmark +28.5% owner 签字), 但**从未 ship**, 搁浅在 3 个未合并 feature 分支上 ~3 周 (主仓 `b398557` / aria `776e140` / standards `f7b7f42`), 唯一未做 = TASK-010 发版。

旧 Spec AD-1 选了「**薄入口 → 委托 phase-d-closer `closeout_only` 模式**」, 主动否决「纯新 skill」(理由 DRY: 避免模板/enforcement 双维护)。本对话重新评估后, owner 偏好「**独立 leaf skill**」(正交平级仪式), 三点理由:
1. **概念完整**: 会话 ≠ 周期; 把会话收尾建成 cycle 收尾器的一个 flag 是 leaky abstraction。
2. **trigger 消歧更干净**: 旧 Spec 因 phase-d 仍是引擎, 没法摘掉 description 里的「收尾/handoff」→ **Gap 1 撞车未根治** (实测 phase-d description feature 分支与 master 一字不差)。
3. **owner 的 step 1/2 字面是「查看当前对话」= 对话内省**, 旧 Spec 恰把它降级 best-effort (AC-3 不计入 falsify)。

## 约束条件

| 类型 | 约束 | 影响 |
|------|------|------|
| 概念 | 会话收尾 = 与十步循环**正交平级**的仪式, 非 cycle 收尾子模式 | 独立 leaf skill, 不路由穿过 phase-d |
| DRY | handoff-write (模板填充 + Rule #9 路径 + latest.md 指针) 不得双维护 | 抽共享 canonical 原语, 两 skill 引用不复制 |
| 第三方通用 | 第三方项目只加载 plugin description + standards, **不加载 Aria CLAUDE.md** | 消歧 load-bearing = description + standards; CLAUDE.md 仅自用 |
| 复用 | 旧实现 854 行 ~70-80% 与入口架构无关, 不浪费已验证成果 | cherry-pick 脚本/测试/钩子, 重写入口 |
| advisory-over-hardlock | 触发器/校验器 advisory 不硬 block (承袭 v1.37.0 #133 哲学) | leaf skill 终结于写 handoff, 绝不自动调 phase-a/b/c/d |
| Rule #6 | 新 skill 强制 benchmark | 架构重心变 → 旧 +28.5% 不可直接迁移 |

## 考虑的方案 / 5 决策收敛

| # | 决策点 | 选项 | 定稿 |
|---|--------|------|------|
| **D1** | 结构基石 (共享原语形态 + closeout_only 去留) | A 共享 ref 文档+删 closeout_only / B 共享 helper 脚本 / C 保留 phase-d D.3 当引擎 | **A** — `references/handoff-write-mechanics.md` 当 canonical SOT, session-closer 与 phase-d D.3 都引用; **删 closeout_only**; phase-d 仅 description 收紧 |
| **D2** | 分支策略 | A cherry-pick 重组到新分支 / B rebase 旧 3 分支 / C 混合 | **A** — 当前 master(v1.49.0)新分支 cherry-pick, 弃 closeout_only(+29)/薄入口(+86)包袱, 无需 revert |
| **D3** | 对话内省 ⨯ 机械 autofill 结合 | A AI 内省优先+autofill 兜底 / B 机械优先+AI 补充 / C 并行合并去重 | **A** — AI 先内省本对话出未完成/经验, autofill 再机械交叉核验补漏 (snapshot 有但 AI 没提的 flag); 对话 awareness 一等公民, 机械 backstop |
| **D4** | trigger 消歧力度+锚 | A 中度 rebind+standards 锚 / B 只删最强撞词 / C 激进负向消歧 | **A** — phase-d 使用场景 rebind 到 cycle-explicit (删「写 session handoff」+ 裸「收尾」); session-closer 强绑会话; standards 加「周期收尾 vs 会话收尾」消歧节; CLAUDE.md note |
| **D5** | Rule #6 benchmark | A 脚本单测照搬+capability AB 重跑 / B 复用旧+28.5% / C 暂不定 | **A** — 3 脚本 deterministic 单测照搬; 新 leaf-skill capability AB 重跑 (旧重心=thin-entry 机械, 新重心=对话内省, 不可迁移) |

## 最终选择

**综合方案** = 独立 leaf skill (D1) + 共享 `references/handoff-write-mechanics.md` 原语 (D1) + cherry-pick 重组 (D2) + AI 内省优先 + 机械 autofill 兜底 (D3) + 中度 description rebind + standards 消歧锚 (D4) + capability AB 重跑 (D5)。

**架构**:
```
owner "对话收尾"/"session closeout"      phase-b/c context-monitor 消费点
        │                                       │ (occupancy≥阈值+未交接)
        ▼                                       ▼
 aria:session-closer (独立 leaf)          closeout_trigger.py (advisory nudge)
        ├── step1/2: AI 内省对话 → 未完成线程+待固化经验   ← 一等公民
        ├── step0/3: handoff_autofill + consistency_check 机械交叉核验补漏  ← backstop
        ├── step4: 按 references/handoff-write-mechanics.md 写 docs/handoff/
        └── 终结 (leaf, 不调 phase-a/b/c/d)
 phase-d-closer D.3 ──► 同一 references/handoff-write-mechanics.md (canonical)
 closeout_only: 删 | phase-d 仅 description 收紧 + 引用 ref
```

## 实现增量 (相对旧 Spec 9/10)

| 处置 | 内容 |
|------|------|
| ✅ 照搬复用 | `handoff_autofill.py` / `consistency_check.py` / `closeout_trigger.py` + 3 测试 + phase-b/c context-monitor 钩子 + standards §2.2.1 |
| 🔧 重写 | `session-closeout/SKILL.md` → 独立 `session-closer` leaf skill (对话内省优先 + 自有 handoff-write 编排引用共享 ref) |
| 🆕 新建 | `aria/skills/session-closer/references/handoff-write-mechanics.md` (canonical 共享原语) |
| ✂️ 弃 | phase-d closeout_only 编辑 (+29); 旧薄入口 (+86) |
| 🔧 改 | phase-d-closer description 收紧 + 引用 ref; standards「周期vs会话收尾」消歧节; CLAUDE.md note |
| 🆕 新增 AC | 对话内省 capability (AI 内省 catches > without); autofill 交叉核验补漏 flag |

> 旧 Spec 的 AC-1~AC-8 + TASK-003/004/005/006/007 大部分可继承; 重点改 TASK-001 (closeout_only→删) / TASK-002 (薄入口→leaf) + 新增共享 ref 原语 TASK + 对话内省 AC。

## 理由

1. **概念正交性 > DRY 教条**: 会话与周期是不同工作单元, 强行同构会 leak; 共享 ref 原语已中和 DRY 顾虑 (单一 SOT, 引用不复制), 故无需为 DRY 牺牲概念干净。
2. **第三方痛点根治**: Gap 1 撞车的根因是 phase-d 仍当引擎; 独立 leaf + description 收紧才能让 phase-d 干净摘掉「收尾/handoff」卖点。
3. **对话内省是 owner 真实诉求**: step 1/2 字面就是审视对话; 机械 autofill 当兜底 (AI 漏了 snapshot 补) 兼得对话一等公民 + 机械可靠性。
4. **不浪费已验证成果**: cherry-pick 留住 ~70-80% (3 脚本+测试+benchmark 方法), 工时仅 ~4.5-6h。

## 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| 共享 ref 文档与 phase-d D.3 prose 漂移 | ref 为单一 SOT, 两处**引用不复制**; structural test 守 drift |
| 对话内省 capability AB 在 in-repo 被稀释 (旧实证 eval-0 delta=0) | 接受 in-repo 是保守下界, 跨项目价值更高 ([[feedback_process_vs_content_skills]]) |
| 第三方 CLAUDE.md 不加载致消歧失效 | description + standards 是 load-bearing (D4 已锚定) |
| 复用脚本接口随 v1.39→v1.49 漂移 | 已评估: 消费的 collector 接口完好 (additive-only schema 守住), openspec.carry_forward_inventory 仍产出 |
| leaf skill 重写引入回归 | 复用旧 3 测试 + 新增对话内省/补漏 AC; phase-d 向后兼容 (description 改不动 D.1/D.2/D.3 逻辑) |

## 开放项 (本 Spec 不含)

- DEC-20260605-001 轴 1 (agent 补全) + 轴 3 (自主推进) — 独立未来工作, 与本 cycle 无关。
- 旧 3 feature 分支 (b398557/776e140/f7b7f42): cherry-pick 取料后**保留为归档 trail**, 不合并不删除 (owner 可后续清理)。

---

**下一步**: Phase A.1 spec-drafter 据本 DEC 修订 Spec (新 changes dir `session-closer-synthesis`, 复用旧 AC/脚本) → A.2 post_spec audit (预算集中此处, post_brainstorm 从轻符合近期实践)。
