# 决策: DEC-20260722-001 - AB baseline 污染: 根因修复优先 (CLAUDE.md 收官方规格), C 降级为备选

> **日期**: 2026-07-22 | **模式**: technical (brainstorm) | **触发**: aria-plugin #116 (triage confirmed/major, [issuecomment-16750](https://forgejo.10cg.pub/10CG/aria-plugin/issues/116#issuecomment-16750))

## 背景

AB `without_skill` baseline 被 CLAUDE.md 自动加载污染 (skill 设计术语可被 baseline 逐字搬运), 且污染会顺 `AB_TEST_OPERATIONS.md:153` 判据反噬测试集 (删掉真有区分度的断言)。issue 备选 A (仓外隔离) / B (prompt 剥离, 已判死) / C (认账 + 改判据为 new-vs-old) / D (钉产出形态, 正交)。

brainstorm 初版收敛到「C+D 先行 + 生命周期分工 + A 后校准」, 前提是「**in-repo baseline 恒被污染, 结构性不可消除**」。**owner 质疑该前提**: CLAUDE.md 该描述项目, 但不该描述 skill 设计内部。经查 Claude Code 官方文档 (memory / best-practices / skills) 证实:

- CLAUDE.md 只放「每 session 都该知道的稳定事实」; **明确排除**频繁变化的信息 / 长解释 / 逐文件描述; 多步骤流程与局部知识应**移到 skill** (按需加载, 渐进披露)。
- 官方行数目标 **≤200 行**; 超长文件降低指令遵循度。
- 当时 CLAUDE.md 为 639 行, 污染源 4 术语全部位于「项目状态」段的 ship 叙事 —— 恰是官方排除项 (频繁变化 + skill 设计内部), 非 CLAUDE.md 合法内容。

⇒ **「恒污染」前提仅在 CLAUDE.md 违规臃肿时成立**。修根 (文档收规) 优于修症状 (改测量方法)。与 memory `feedback_perpetual_red_check_may_encode_stale_convention` 同族: 先质疑前提, 再动手。

## 决策

1. **根因修复 (本 commit 落地)**: CLAUDE.md 按官方规格重写, 639 → 149 行。ship 叙事 / 版本流水 / 规则详情移交各 canonical 家 (aria/CHANGELOG.md / docs/handoff/ / openspec archive+changes / standards conventions SOT — 全部预先核实存在), CLAUDE.md 保留规则判据本体 + 指针。「项目状态」段收到 hygiene 规范自身规定的 15-20 行配方。
2. **污染面测量**: 修复前 4 术语 (evidence_grade / gitlink_integrity / fail-CLOSED / overall_parity) 各 1 次 → 修复后 **全部 0** (含大小写变体)。
3. **enforcement 收紧**: `claude-md-changelog-free` 行数预算 640 → **200** (官方目标即执行线), 消掉「行数不超但单行爆表」的钻空子空间; check 提示语补「skill 设计术语回涨」维度。
4. **C / 生命周期分工 / A 均不采纳, 降为备选**: 待下一次真实 Rule #6 触发的 AB 实测残余污染。若 baseline 仍显著搬运 → 重启 C (new-vs-old 共模抵消) + 生命周期分工 (新 skill 走 A 仓外隔离); 若干净 → skill-vs-no-skill canonical 问题在本仓恢复可答, C 全套不需要。
5. **D (钉产出形态) + `:153` 判据修正保留为 #116 剩余 scope**: 两者与污染**独立成立** (genre confound 是三臂产出形态不齐; `:153` 在任何污染水平下都该先语义分档再决定拆/删), 不因根因修复而消失。

## 考虑的方案

| 方案 | 状态 |
|------|------|
| C+D 先行 + 生命周期分工 + A 校准 (brainstorm 初版) | **被本决策取代** — 其前提「恒污染」被官方文档 + 根因修复证伪为条件性 |
| B prompt 剥离 | 否决 (context 无法真「不读」, 不可验证) |
| E 清空项目状态段全部术语但保留叙事 | 否决 → 被「叙事本就不该在 CLAUDE.md」取代 (更强形式) |
| **根因修复 + 重测 + C 留备选 (本决策)** | **采纳** |

## 风险与缓解

| 风险 | 缓解 |
|------|------|
| 精简后 AI 失去项目状态细节 | 细节在 canonical 家 (proposal.md / handoff / CHANGELOG), `/state-scanner` live 查; CLAUDE.md 留指针 |
| 残余污染仍存在 (skill 名 / 规则术语属合法内容) | 决策 4 重测门; 备选方案完整保留于 #116 + 本 DEC |
| 状态段回涨复发 | 预算 200 硬执行 (check warning) + hygiene 规范 15-20 行配方 |
| 精简误删 load-bearing 规则 | 10 条规则判据本体 + owner 裁决表 (Rule #6 决策表 / #10 白名单 / 多远程两约束) 全部保留, 仅剪事故叙事与重复 |

## 后续

- [ ] 下一次 Rule #6 AB: 按决策 4 实测 baseline 残余搬运, 据此裁 C 去留 (记录到 #116)
- [ ] #116 剩余 scope (D + `:153`): `AB_TEST_OPERATIONS.md` 文档修订, 独立小 cycle
- [ ] 官方 ≤200 行预算若被合法内容顶破 → 届时再裁剪或提级讨论, 不静默放宽 check
