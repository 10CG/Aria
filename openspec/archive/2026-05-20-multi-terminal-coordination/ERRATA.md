# ERRATA — multi-terminal-coordination

> **不修改本目录 `tasks.md` / `proposal.md` 本身**(归档记录保持原样,不回改历史勾选);本 ERRATA.md 是**回溯纠错落点**,记录归档后发现的标记失真,并链接接续 Spec。

## 问题

本 Spec 归档 `tasks.md` 中以下两处标记为 `[x]`(已完成),但与同期 / 后续设计文档、代码现实不符:

1. **2.5「急切认领闸门集成 state-scanner」**(`tasks.md:29`)—— 勾选完成,但**纠错发现时**(2026-07-04,接活前) `aria/skills/state-scanner/references/layer-l-integration.md`(live 设计文档)曾自陈:
   - 文档标题曾写 "P3 TASK-024 将把 `phase1_gate` 集成到 state-scanner 主流程"(`:4`,未来时,归档后仍未来时)
   - 末尾状态段曾明确 "TASK-024/025 是 P3 scope, 本文档仅记录设计意图供 P3 实施参考"(`:77`)

   > **注**(避免自相矛盾):**接续 Spec (`interactive-session-dedup-coordination`) 的 task 4.2(b) 已把 `layer-l-integration.md` 同步为 "TASK-024 已完成 / advisory 接活"**(注:母 spec 的 TASK-017 是 track_board 任务, 与本 doc-sync 无关, 勿混淆),故上述 `:4`/`:77` 引用描述的是**接活前(纠错发现时)**的状态,不是当前 live 文档措辞 —— 当前该文档已与代码一致。
2. **P3(Section 3, `tasks.md:35-42` 全部 8 项)**—— 全部勾选 `[x]`,但集成本体(TASK-024:把 `phase1_gate.run_gate()` 接入 state-scanner 主流程/AI 编排层)**从未落地**:`run_gate()` 在 scan.py / collectors / config 中**零调用点**(仅注释与文档引用),是勾选完成、实际死代码(dead code on-arrival)的样本。

## 现状(2026-07-04 确认)

`phase1_gate.py` 的 reconcile / claim 读写 / race 处理等组件(P2 部分,2,934 行,含单测)**本身是真实存在且经测试的**;失真的是"集成"这一层 —— TASK-024(把该引擎接入 AI 编排层调用路径)在纠错发现时从未实施,`layer-l-integration.md` 当时对此保持诚实(曾写"将...集成"未来时),但母 Spec `tasks.md` 的 2.5/P3 勾选与该诚实描述自相矛盾。**(纠错后:接续 Spec Phase 1 (P1) 完成 TASK-024 集成,其 task 4.2(b) 已把 `layer-l-integration.md` 同步为"已完成",矛盾消除。)**

## 接续

上述缺口由 **`interactive-session-dedup-coordination`**(DEC-20260704-002)接续完成:

- Phase 1(P1,任务 1.1-1.5)完成 TASK-024 集成:AI 编排层(state-scanner 阶段 2 推荐 → 用户确认 → `phase-b-developer`/`branch-manager` Phase B 启动前)调用 `phase1_gate.run_gate()`,对齐 `layer-l-integration.md:15` "闸门不在 scan.py 内自动执行"的既有设计约束(非改设计,是补齐设计早已声明、代码从未兑现的接线)。
- 同时把该 Spec 期间发现的"勾选完成 ≠ 运行现实"问题作为方法论修法示范(见下)。

详见 [`interactive-session-dedup-coordination/proposal.md`](../../changes/interactive-session-dedup-coordination/proposal.md)(§Why.2 次因分析 + §What.1 接线设计)与 [`tasks.md` 1.1-1.5](../../changes/interactive-session-dedup-coordination/tasks.md)。

## 与 #134 `archive_type` / `design_deferred` 机制的关系

`aria-archive-completeness-gate`(Forgejo #134,v1.42.0+)与本 ERRATA 处理的是**同一类失真的两个不同时间点**,不重复也不互相替代:

| 维度 | #134 `archive_type` / `design_deferred` | 本 ERRATA |
|------|------------------------------------------|-----------|
| 介入时机 | **归档前**(D.1 `openspec-archive` SKILL Step1/Step2 gate) | **归档后回溯**(已归档多月才发现标记失真) |
| 机制 | 写入侧结构化 frontmatter 标注(`archive_type: implementation-deferred` + `archived_reason`),消费侧 collector 识别并在 state-scanner 看板 surface `design_deferred[]` | 人工 / 审计发现失真后,新增 `ERRATA.md` 文档记录问题 + 接续方案,**不回改**历史 `[x]` |
| 适用对象 | 归档动作发生时**已知**设计未实施的 Spec(设计者当下即可标注) | 归档时**未被发现**、后续才暴露的勾选失真(本案:2026-05-20 归档,2026-07-04 才经 #94/#95 事故复盘发现) |
| 是否改变归档记录本身 | 是(写入 frontmatter,发生在归档动作内) | 否(归档 `tasks.md`/`proposal.md` 保持原样,ERRATA.md 是旁路追加文档) |

**关系总结**:#134 是**预防性**机制(归档时诚实标注,防止新增此类失真);本 ERRATA 是**回溯性**机制(处理 #134 上线前 —— 或 #134 未能覆盖 —— 已产生的历史失真)。`ERRATA.md` 作为归档目录下的独立文件,是本项目**回溯场景的落点惯例**:后续任何审计(尤其 [#95](https://forgejo.10cg.pub/10CG/aria-plugin/issues/95) 系统性修复 —— archive gate 交叉核对 tasks.md vs 成功标准 + `[x]` 真实性抽验 + pre-#134 孤儿 sweep)在发现同类历史失真时,可复用本文件作为格式参照,在对应归档目录下新增同名 `ERRATA.md`,而不回改已归档的 `tasks.md`/`proposal.md`。

## References

- 接续 Spec: [`interactive-session-dedup-coordination`](../../changes/interactive-session-dedup-coordination/proposal.md)(DEC-20260704-002)
- 决策记录: [DEC-20260704-002](../../../docs/decisions/DEC-20260704-002-interactive-session-duplicate-prevention.md) / 母决策 [DEC-20260519-001](../../../docs/decisions/DEC-20260519-001-multi-terminal-coordination.md)
- 关联 Issue: [aria-plugin #94](https://forgejo.10cg.pub/10CG/aria-plugin/issues/94)(双子星防重复失效)/ [aria-plugin #95](https://forgejo.10cg.pub/10CG/aria-plugin/issues/95)(勾选≠运行病根,系统性修复独立排期)
- 设计文档(自陈 deferred 的诚实来源): [`aria/skills/state-scanner/references/layer-l-integration.md`](../../../aria/skills/state-scanner/references/layer-l-integration.md)
- #134 机制: `aria/skills/openspec-archive/SKILL.md`(D.1 写入侧 gate)+ `aria/skills/state-scanner/references/state-snapshot-schema.md`(`archive_type` / `design_deferred` schema)
