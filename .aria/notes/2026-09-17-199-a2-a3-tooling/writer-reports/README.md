# 10CG/Aria#199 A.2/A.3 返修的派单与执笔报告 (v2.4 – v2.12)

> **为什么在仓里**: owner 2026-09-27 裁定落仓 (决策单 `.aria/decisions/2026-09-27-195-199-owner-rulings-pending-items.md` 第 3c 项)。计划 `detailed-tasks.yaml` 的 `revision_log` 与轨级 handoff 引用的「同族扫描 160 个候选改 46 条」「9 张新建机制交互表」以及 v2.6 的三份机器清单 (序号引用 342 行 / 协调 ref 写入路径 8 条 / custom checks 16 条加 7 个探针), 原本只在 2026-09-24 会话的主控 scratch (`/tmp/...`) 里, 仓内产物无法复核 —— 即 post_planning R6 聚合流程记录第 5 条指出的可审计性缺口。
> **性质**: 历史产物, 逐字节原样落仓 (sha256 与源文件逐一比对一致)。不按现行写法规范回改, 与审计报告同属存量。

## 文件

| 文件 | 内容 | 对应计划版本 |
|---|---|---|
| `v2.4-dispatch.md` / `v2.4-writer-report.md` | 主控派单 / 执笔报告: R4 四题 Major + 四条同处 minor; 请裁 9 条 | v2.4 `b686185` |
| `v2.5-dispatch.md` / `v2.5-writer-report.md` | R5 五题 Major + 两条同处 minor + 「空输出即通过」同族扫描 (160 个候选改 46 条) + 9 张新建机制交互表; 请裁 10 条 | v2.5 `e7a1782` |
| `v2.6-dispatch.md` / `v2.6-writer-report.md` | R6 五条 minor + 三份机器清单; 请裁 2 条 | v2.6 `320d523` |
| `v2.7-dispatch.md` / `v2.7-writer-report.md` | R7 六条 minor + R2 – R5 未处置的 20 个键 + 决策单 2026-09-27 第 3 项 + `10CG/Aria#195` 合并后的基线平移; 实质改动候选 10 条; 请裁 11 条 | v2.7 `7ef09ea` |
| `v2.8-dispatch.md` / `v2.8-writer-report.md` | R8 的 1 条 Major (aria 发版文件集扩为六个) + 7 条 minor + 决策单 2026-09-29 第 2 项的追认记录; 改变执行者动作的 4 条; 请裁 6 条 | v2.8 `f231287` |
| `v2.9-dispatch.md` / `v2.9-writer-report.md` | R9 三簇 minor + 发版终核逐个取值点 (决策单 2026-09-29 第 6 项) + 第 7 项的追认记录; 改变执行者动作的 3 条; 请裁 6 条 | v2.9 `59a3e9b` |
| `v2.10-dispatch.md` / `v2.10-writer-report.md` | post_planning R10 收敛后只含 minor 的返修: R10 四条 minor + 决策单 2026-09-30 第 3 项的追认记录; 改变执行者动作的 1 条; 请裁 6 条; 按决策单 2026-09-27 第 3a 项不重开审计 | v2.10 `e0d50e6` |
| `v2.11-dispatch.md` / `v2.11-writer-report.md` | Phase B 执行中回退 Phase A (决策单 `.aria/decisions/2026-09-30-199-b2-group1-spec-drift-rulings.md` 第 7 项): 既有结构约束冲突的处置 (修法 (a) 允许集逐字加入口脚本名) + 同单第 1 – 6 项并入读前必看 + Phase B 计划缺口登记; 改变执行者动作的 5 条; 请裁 8 条; 之后开 post_planning R11 只审本版改动 | v2.11 (随该版同一提交落仓, 主仓 feature 分支) |
| `v2.12-dispatch.md` / `v2.12-writer-report.md` | post_planning R11 收敛后只含 minor 的返修: R11 的 8 键 minor + 决策单 `.aria/decisions/2026-09-30-199-b2-group1-spec-drift-rulings.md` 第 8 项 (请裁 1 批准 (a)、2 – 7 追认、8 补格) 的落地; 改变执行者动作的 8 条; 请裁 9 条; 按决策单 2026-09-27 第 3a 项不重开审计 | v2.12 (随该版同一提交落仓, 主仓 feature 分支) |

**v2.7 起执笔报告来源不同**: harness 拒绝执笔子代理写报告文件。v2.7 的执笔实例没有绕过, 把报告全文附在最终回复里; v2.8 起派单直接要求以最终回复交报告。各份 `*-writer-report.md` 都是主控用脚本从该实例的运行记录里取出的最终回复, 逐字节原样 (v2.7 前五行是回复摘要、frontmatter 在代码块内; v2.8 / v2.9 以 frontmatter 开头; v2.10 在 frontmatter 前多一行说明; v2.11 / v2.12 以 frontmatter 开头, 由动态工作流里的执笔代理出稿, 取自该工作流运行日志 journal.jsonl 里的返回值); 落仓前都做过凭据形态扫描, 零命中。

## 未落仓

- 各版 `writer-work/` 与 `repo/` (中间脚本、复跑环境与仓库副本, v2.4 – v2.6 三版合计约 790MB; v2.7 – v2.12 同样不落仓)。报告里引用的这些路径因此不可达; 需要复跑时按各报告的「复跑入口」一节在新的 scratch 里重建。

## 请裁项的去向

v2.4 – v2.6 三批请裁共 21 条, 已由 owner 2026-09-27 裁定, 逐条结论见上述决策单第 3b 项。v2.7 的 11 条请裁由 owner 2026-09-29 全部追认 (第 7 条附条件), 10 条实质改动候选经 post_planning R8 复核, 见决策单 `.aria/decisions/2026-09-29-199-r8-and-v2.8-owner-rulings.md`。v2.8 的 6 条请裁由 owner 2026-09-29 按多数全部追认 (决策单第 7 项)。v2.9 的 6 条请裁由 owner 2026-09-30 按多数裁 (决策单 `.aria/decisions/2026-09-30-199-r10-converged-v2.10-owner-rulings.md` 第 3 项)。v2.10 的 6 条请裁由 owner 2026-09-30 全部追认 (决策单 `.aria/decisions/2026-09-30-199-r10-converged-v2.10-owner-rulings.md` 第 7 项; 本版之后不再开审计轮)。v2.11 的 8 条请裁经 post_planning R11 五席表态后, 由 owner 2026-10-01 裁定: 第 1 条批准、第 2 – 7 条追认、第 8 条补格 (owner 委托主控建议) —— 决策单 `.aria/decisions/2026-09-30-199-b2-group1-spec-drift-rulings.md` 第 8 项。v2.12 的 9 条请裁待 owner 复议 (本版按第 3a 项不重开审计, 主控核验后续跑 Phase B)。本目录的报告保持原样, 不回写裁定结果。
