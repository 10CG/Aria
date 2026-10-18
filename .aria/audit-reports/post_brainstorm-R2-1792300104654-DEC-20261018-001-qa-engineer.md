---
checkpoint: post_brainstorm
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: PASS_WITH_WARNINGS
timestamp: 2026-10-18T05:08:24.654Z
context: DEC-20261018-001
agents: [qa-engineer]
---
drift_terminated: false
drift_check_skipped: false
is_refocus: false

## 审计结论

{"type": "issue", "severity": "major", "category": "testing", "scope": "DEC-001 裁定-9 SC 必测 fixture 矩阵 (8 态) — 回归扫描新 finding", "summary": "8 态矩阵在三面指纹的各自覆盖上不对称: 上下文面有正向态 (上下文变)、provenance 面有正向态 (provenance 变)、时间面有正向态 (时间敏感字段跨档), 唯独主面 — issue 内容面 (title/body/labels hash) — 只有负向/扰动态 (编辑但内容等价 / rebase 后 updated_at 变), 缺最基本的正向态「label 人工增删或 title·body 实质编辑 ⇒ 必须判变触发重评」。反事实检验: 若内容 hash 实现退化成常量 (回归/抄旧 scan.py 时的典型 bug), 现矩阵 8 态结构上全绿, 无一 fixture 变红 — 这正是本项目 counterfactual_test_for_every_new_sc 纪律要堵的假绿类。另缺「已关闭后重开」态: 已关闭=集合差移除后, 重开条目走新条目路径 (重评, 安全方向) 还是恢复既有记录 (漏评, 危险方向) 未钉死。建议矩阵扩为 10 态, 两态均钉为 spec 验收面; 前者是指纹机制的核心反事实, 后者与 apply_payload 自写 label 后的自触发行为 (existing 变化 ⇒ 下轮必判变) 同属 label 变更族, 应同 fixture 覆盖"}

{"type": "issue", "severity": "minor", "category": "testing", "scope": "DEC-001 裁定-9 上下文面指纹", "summary": "内容级 hash 的输入文件集未穷举: 「openspec/changes/ 内容级 hash (含 proposal/tasks)」的『含』是下界非全集 — changes/ 全树 vs 仅 proposal/tasks 两文件两种读法均合规, 若 spec 取窄读法, design.md 或 specs/ delta 的单独实质修订 (改判记录不在 proposal/tasks 里) 不触发重评, 危险方向残余; openspec/archive/ 的显式排除 (归档时 changes/ 目录消失已天然触发, 历史 archive 修订不影响在制轨判断, 排除正当) 未成文。spec 阶段须钉死精确文件集清单并绑定到「上下文变」fixture 的构造判据, 防实现各自解释"}

{"type": "issue", "severity": "minor", "category": "testing", "scope": "DEC-001 裁定-11 Rule#6 矩阵 × SOT §2 逐行对齐回归", "summary": "四行矩阵与 SOT 决策表行 1/2/3 及 §4.1 字段义务逐行对齐 (复核通过), 但漏了 SOT §2 的自主运行时附加条款: unattended (state_scanner.coordination.unattended == true) 下禁 description 改动含新增 skill, 需要时须放弃整个任务。issue-groomer 是必然 description_changed=yes 的新 skill, 若其立项/实施被派给 Layer 2 自主轨 (aria-runner), 按 SOT 该任务必须整体放弃。DEC 只说「P1 零底座依赖即可开工」未钉执行轨 — spec 阶段须显式声明走 interactive 轨 (或 owner 显式修订 SOT 条款), 否则存在派发即触条款的结构性撞车面"}

## R1 六条处置逐条验证

1. QA-M1 (Rule#6 档位矩阵) — resolved。四行矩阵覆盖 groom.py/SKILL.md/description/Tier B 四个变更面, 与 SOT 决策表行 1/2/3 及 §2 附加约束逐行对齐; 两条缺口行动项均有真锚 (本轮实证复核: Aria#213 open 且 title「41 个 skill 没有 trigger 套件」逐字吻合; ab-suite/trigger/ 目录确实不存在, 0 套件声称成立)。
2. QA-M2 (上下文指纹粒度) — resolved (危险方向已闭)。残余窄歧义见 minor finding 2。
3. QA-M3 (复用契约歧义) — resolved。矩阵自身枚举缺口见 major finding 1 (属矩阵完备性, 非 R1 歧义复发)。
4. QA-m1 (diff 交互) — resolved。
5. QA-m2 (apply_payload 基准) — resolved。
6. QA-m3 (Tier A confidence) — resolved。

## Verdict

PASS_WITH_WARNINGS — 0 Critical / 1 Major / 2 minor。v2 对 R1 六条处置全部到位且锚真实, 增量契约与 Rule #6 框架的两个危险方向已闭; 唯一 major 是 8 态验收矩阵自身的枚举缺口 — 扩两态即闭, 属收敛末段的可定位修补而非方向性返工。

## 轮次记录

R2 以 testing/Rule#6 镜头复核 v2 全部 13 项裁定 + 修订记录, 逐条验证 R1 六条处置, 并独立实证复核 0 套件现状 (ab-suite/trigger/ 不存在) 与 Aria#213 锚 (open, title 逐字吻合), 回归扫描 8 态矩阵第 9 态与裁定-11×SOT 逐行对齐。
