---
checkpoint: post_planning
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-07-09T01:24:43.799Z
context: openspec/changes/agent-router-auto-project-agent-injection/detailed-tasks.yaml
agents: [knowledge-manager]
drift_terminated: false
drift_check_skipped: false
is_refocus: false
---

## 审计结论

对 `detailed-tasks.yaml` (18 task) 按五个维度核验: 三层对齐 / 依赖图 / 粒度与可执行性 / 分工合理性 / Phase 归属自洽性, 并额外核验角色侧重 (proposal What §1-§6 逐段承接、note 字段一致性、术语一致性)。

**做对的地方 (不挑刺, 明确记录)**:
- What §1-§6 全部子项均有 task 承接, 未发现孤儿内容; AC-1..AC-16 全部 16 条均有明确 task 归属 (TASK-013 承接 13 条裁决类 + TASK-014 承接 AC-3 + TASK-015 承接 AC-15 + TASK-017/018 承接拆分后的 AC-9a/9b), 无遗漏。
- Decision Records B1-B12 全部可追溯到对应 task, B7 (发现 A → M7) 正确识别为 OOS 不需要 task。
- 依赖字段构成合法 DAG, 未发现循环依赖。
- 术语一致性 (我的角色侧重项): "两段式"/"吸收"/"惰性" 三个 Rev4 关键术语在 detailed-tasks.yaml 中使用准确, 与 proposal Rev4 一致。
- §132/§145/§205/§277/§305/§323/§383/§393/§438/L17/L449 等 detailed-tasks.yaml 引用的 SKILL.md 章节号, 经源文件抽查 (`sed -n` + `grep -n`) 逐一核实真实存在, 行号精确 (§205 step3 现状确认只有 4 个平级子项、§393 确认是文末孤儿段、§277 确认是 legacy 配置文件位置) —— proposal 与 task 前提均未虚构。
- TASK-009 (`.aria/config.template.json` 补 agent_router 块) 与 TASK-010 (taxonomy 头注) 的前提均经实地核验成立 (现文件确无对应内容)。
- 分工策略 (main-loop 亲验 TG-A/B, subagent 并行 TG-D 实跑, main-loop 机械步 TG-C/E) 声明与实际 agent 字段逐一对照一致, 未发现违反自身声明的分配。

**发现的问题**: 0 Critical + 3 Major + 2 Minor。三条 Major 集中在两类根因: (1) TASK-009/TASK-011 的 Phase 归属在 execution_order 叙述、note 字段、tasks.md 收尾句三处表述不一致, 且 TASK-018 未把二者列为依赖前置 (结构性缺口, 不影响 aria 子模块侧 TG-A/B/D 的核心工作); (2) 两处"验证清单窄于任务范围"的缺口, 其中 TASK-014 (AC-3 旧文本来源未定) 与 TASK-006 (删除误导性措辞未入验证清单) 因分别关系到 Rule #4 零回归判定的有效性、以及本 Spec 自身"消除文档漂移"的核心诉求, 缺乏下游兜底, 定为 major; TASK-003/TASK-005 的同类缺口因有 TG-D fixture 测试兜底, 定为 minor。

## Verdict

**PASS_WITH_WARNINGS** (0 Critical + 3 Major + 2 Minor)
**vote: REVISE** —— 存在 major 项, 建议规划先补一轮小修 (三条 major 均为"加一两句话"级别的低成本修订, 非推倒重来), 再进 B.1, 而非直接执行。

| 维度 | 结果 |
|------|------|
| 三层对齐 (detailed-tasks.yaml ↔ tasks.md ↔ proposal Rev4) | What/AC/Decision 全覆盖, 无孤儿; 但 tasks.md 自身滞后于 Rev4 (minor) |
| 依赖图 (DAG 完整性) | 无循环依赖; 但 TASK-018 缺 TASK-009/011 依赖边 (major); TASK-014 隐藏依赖 (旧 SKILL 文本来源) 未显式化 (major) |
| 粒度与可执行性 | 任务边界合理 (SKILL.md 相关改动按耦合度合并, 主仓 PR 按原子提交单元合并), 两处 verification 覆盖窄于 title (1 major + 1 minor) |
| 分工合理性 | agent 字段与声明策略逐一吻合, 并行窗声明 (013∥014∥015) 经检查无共享可变状态冲突风险 |
| Phase 归属自洽性 | TASK-009/011/018 三处 Phase C 注记不一致 (major, 已详述) |

## 核验锚点

**Major-1**: `detailed-tasks.yaml` execution_order 把 TASK-009/010/011 归入 "可与 TG-D 并行"(暗示 Phase B), 但 TASK-009/TASK-011 各自 `note` 字段明写 "Phase C 主仓分支落地", `tasks.md:42` 收尾句又把 009/011/018 三者统一归为 Phase C 一组; 同时 TASK-018.dependencies 仅 `[TASK-017]`, 未含 TASK-009/TASK-011, 与其 title "TASK-009/011 落地" 及 deliverables 逐字重叠 (`.aria/config.template.json` / `US-011.md` / `DEC-20260621-001-*.md`) 相矛盾。

**Major-2**: TASK-012 (fixture harness) 依赖 TASK-008 (此时 SKILL.md 已被覆写为 v1.2.0), verification 只提注入"新"文本; TASK-014 需要"旧 SKILL 文本 vs 新"做 AC-3 零回归对照, 但两任务均未指定旧文本 (git ref/SHA) 的获取方式 —— proposal 自身"双跑不一致=fail 回炉, 无容忍阈值"的严格要求下, 未锚定的 git ref 会造成自身判定不稳定。

**Major-3**: TASK-006 (§393 改写) verification 仅 3 条, 遗漏 proposal §6 明定 5 子项中的"删「已生效」暗示"与"措辞修正为「FP/TT/技术栈/关键词(基线)+capabilities(项目级)」"两项; 经抽查 SKILL.md L393-449 现状确认该误导性框定语确实存在, 且无任何下游 AC 对"旧表述已被删除"做专项核对 (AC-9a 只做"新内容存在性" grep, 不做"旧表述缺失性"核对)。鉴于这正是本 Spec 存在的根本理由 (文档漂移), 该验证缺口具有方法论自洽性意义。

**Minor-1**: TASK-003 (2.5/2.6 未入 verification) 与 TASK-005 (step4 侧别聚合未入 verification) —— 有 TG-D AC-6/AC-10/AC-5 结构化 fixture 测试独立兜底, 风险低。

**Minor-2**: `tasks.md:3` 仍标注 "Rev3", TASK-003 一行残留 R3 期措辞 ("基线逐字"/未定义的 "R-c") —— detailed-tasks.yaml 本身已正确按 Rev4 校正, 仅建议顺手回填 tasks.md 保持参照物同步, 避免误导后续读者。
