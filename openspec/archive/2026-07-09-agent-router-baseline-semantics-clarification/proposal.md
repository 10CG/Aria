# Proposal: agent-router 基线层 5 处文本模糊补明 (aria-plugin#99)

> **Status**: done
> **Shipped**: 2026-07-09 v1.55.1 — aria-plugin PR#100 merged `8fea71d`, #99 auto-closed; pre-merge review 0C/4I/2M 全修
> **Level**: 2 (Minimal)
> **Created**: 2026-07-09
> **Source**: aria-plugin#99 (v1.55.0 fixture runner ambiguity_notes 收纳, 5 处均 v1.0.0 起 pre-existing)
> **Carry-id**: carry-followup-99

## Why

`agent-router-auto-project-agent-injection` (v1.55.0) 的 48-run structural fixture 中, runner 以 ambiguity_notes 反馈 5 处基线层文本模糊。均标注「不影响本次结果」且属 Stage 1 基线既有性质 (v1.55.0 OOS), 但双跑一致性依赖 runner 自行补齐语义 —— 语义未成文即潜在分叉点。本 change 逐处补明, 不改变既有意图行为。

## What Changes

全部为 `aria/skills/agent-router/` 两文件的 prose 语义补明 (0 代码):

1. **关键词匹配语义成文** (`ROUTING_RULES.md §关键词匹配规则`): 补 preamble —
   词边界全词匹配 (与 §CAP-1 L1 同准绳, SQL 不匹配 SQLAlchemy)、大小写不敏感、
   匹配对象 = task 文本 (files 路径不参与 — 路径信号由 FP 规则专责)、
   同一表行多关键词任一命中即触发且每行至多计一次、不同行可叠加、总分上限 1.0 (既有)。
2. **task_type 自动推断程序成文** (`ROUTING_RULES.md §任务类型规则` preamble + `SKILL.md §输入参数`):
   未显式传 task_type 时, 以 TT 表「触发关键词」为唯一推断依据, 对 task 文本做词边界
   逐字命中 (非语义联想); 命中行产出该 TT 候选, 多行命中各自产出, 零命中 = TT 类不产出候选。
3. **SKILL 摘要表 `frontend/**` 行对齐 canonical** (`SKILL.md §路由规则` + `ROUTING_RULES.md` FP-022 注):
   摘要表行 `frontend/**/* → general-purpose 0.70` 改为对齐 FP-022
   (`frontend-developer 0.85`); 同时在 ROUTING_RULES FP-022~025 补诚实注 —
   frontend-developer 非插件内置 roster (不在 §Agent 能力矩阵), 命中时按「Agent 不存在」
   错误处理回退 general-purpose, 除非项目级 `.aria/agents/frontend-developer.md` 提供同名 Agent。
4. **recommend 兜底条文化** (`ROUTING_RULES.md §Fallback 规则`): recommend 输出不足
   max_candidates 时以 general-purpose (confidence 0.50 约定填充值, 非规则得分) 补足末位;
   general-purpose 已凭规则得分入池时不重复添加、用实际得分。
5. **threshold 比较明文** (`ROUTING_RULES.md §置信度计算` + `SKILL.md §输入参数` threshold 行):
   一律取 `>=` (恰等 threshold → auto 合格), 与既有 recommend 触发条件
   `confidence < threshold` (SKILL §推荐模式) 及 §CAP-4 R-b(2) `match_rate >= threshold` 互补一致。

随手项: ROUTING_RULES.md footer「最后更新 2026-01-22」陈旧, 同步为本次日期。

## Impact

- **版本**: aria-plugin v1.55.0 → **v1.55.1** (PATCH — 语义补明/文本修复, 无新功能);
  SKILL 1.2.0 → 1.2.1, ROUTING_RULES 1.1.0 → 1.1.1。
- **行为影响**: 第 3 项摘要表行是唯一「可见变化」(0.70/general-purpose → 0.85/frontend-developer
  + 回退注), 但 ROUTING_RULES 已是 canonical (v1.2.0 §93 banner 声明), 实际裁决本应按 FP-022 —
  属对齐非变更。其余 4 项均为把 runner 已按最合理解释执行的语义写成文。
- **Rule #6**: prose 语义补明 (doc-dominant, 0 代码), 按 smoke+defer 惯例
  (memory `feedback_smoke_defer_extends_to_inline_ai_guidance`); 5 处补明文本以
  aria-plugin#99 逐条覆盖自查代替全量 fixture 重跑 (v1.55.0 48-run 基线已建立,
  下次触碰 router 逻辑的 cycle 顺带回归)。
- **不做**: Fallback 层级「confidence > 0.7」等 #99 未列事项不动 (最小切口)。

## Verification

- 5 处补明逐条对照 #99 原文自查 (每处 grep 落地验证)。
- 一致性检查: 新文本与 §CAP-1/CAP-4/优先级处理/推荐模式触发条件无冲突。
- 版本 5 文件同步检查 (plugin.json / marketplace.json / VERSION / CHANGELOG.md / README.md)。
