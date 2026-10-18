---
checkpoint: post_spec
mode: convergence
rounds: 2
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-10-18T11:47:22.119Z
context: issue-groomer-p1-mvp
agents: [qa-engineer]
---
drift_terminated: false
drift_check_skipped: false
is_refocus: false

## 审计结论

{"id":"QA2-M1","severity":"Major","type":"fix-introduced-regression","location":"proposal.md SC-6 + tasks.md 4.2","summary":"SC-6 两分支重写把 v1 SC-6 的另三个 Rule #6 义务面从 SC 集合移除且无任何其他 SC 承接: (a) 场景 1 AB 照跑 (矩阵第二行); (b) Tier B 定向 fixture (判据表第三行三条件, #240/task 2.2); (c) rule6_note 四条成文 (DEC 裁定-11 行动项明言「档位终裁随 rule6_note 成文」)。v1 SC-6 原文四 facet 全列 (git show f8ba952 逐字核对); v2 SC-6 的 green 条件仅剩 4b 分支, 且 task 4.2 ship 前置亦不含 3.1/2.2 ⇒ SC 全绿 + ship gate 均不再蕴含 Rule #6 矩阵 discharge。义务仍有 task 承载 (3.1/2.2) 但无判绿锚点 — Phase 3 削减时无红灯, 与 R1 QA-M1 同类锚定缺失。","fix":"SC-6 扩为四 facet 全列 (两分支 + 场景 1 AB pass + 第三行三条件齐备 + rule6_note 成文合规), 或新增 SC-10 承接后三项; 4.2 ship 前置补「task 3.1/2.2 完成」"}

{"id":"QA2-m1","severity":"minor","type":"coverage-enumeration-gap","location":"tasks.md 1.3","summary":"1.3 逐 SC 映射在 SC-4 处 facet 不完备: SC-4 文本五 facet 中「复用规则」(Tier A 判据输入快照跨档 ⇒ 重分类) 与「provenance 门」(Tier B provenance 不匹配 ⇒ stale-assessment) 无 fixture 项枚举。SC-1 的 ③⑧⑨ 态测指纹翻转检测侧, 不覆盖复用/门决策后果侧 — 该两 facet 实现退化成常量时无 mandated fixture 必红。","fix":"1.3 SC-4 项补两条 fixture 枚举: 判据输入变而分类输出同 ⇒ 重分类不复用; provenance 变 ⇒ stale-assessment"}

### 八条处置逐条验证

1. [QA-M1] SC-1 分量级 mandate 错挂 — resolved (mandate 归 1.3 与 SC-1 同相; 分量数对 DEC 裁定-9 实核无误; #240 勘正 live 复核通过; 假绿向量堵死)。
2. [QA-M2] SC-6 弱化 — resolved (原弱化面全闭合; 两分支写死 + 门⑥ + 括注恢复 + 0 套件前提实测成立; 对 SOT §4.1 逐条对照 4b 轴无剩余弱化面) — **但修复引入 QA2-M1 回归**。
3. [QA-m1] rule6_note 折叠 — resolved (五字段对 SOT §4.1 模板逐字核对 × 四面不折叠 + negctrl + substitute 措辞)。
4. [QA-m2] 1.3 逐 SC 映射 — resolved @SC 粒度 (facet 级余 QA2-m1)。
5. [QA-m3] no-op live 实测 — resolved (非阻断观察: 「Phase 1 前」时序限定词 tasks 1.3 未携带, A.2 补序)。
6. [QA-m4] dogfood 判绿 — resolved (SC-7 + 4.1 显式引用 + 三处一致)。
7. [QA-m5] 语料契约 — resolved (三路径逐一核对实存 + 再生成命令 + 单点风险显式)。
8. [观察] 时钟 seam + 11 态补挂 — resolved。

### 回归扫描 + SC 集合完备性复检

SC 编号 v1→v2 无错位; SC-9 新增映射闭合; 任务集 v1→v2 无丢失 (旧 2.2→0.1 六项化; 旧 2.3→新 2.2; v2 4.2 增 ship 净增益); 外证核查均通过 (DEC ①-⑩ 恰 10 态 / trigger 0 套件 / comment 29237 同步 / 语料三文件); 无振荡 (两 finding 均为 v2 新面, 非原 finding 重开)。

## Verdict

FAIL — 0C / 1M / 1m。八条 R1 处置全部落实且经五路取证 (comment 29237 / DEC 枚举 / 语料文件 / ab-suite 目录 / v1 git 快照), 但 SC-6 重写过度窄化把 v1 已锚定的三个 Rule #6 义务面从判绿集合挤出且无承接 — Rule #6 为不可协商规则, discharge 不再被 SC 全绿蕴含属 Major; PASS 需 0C+0M, 故 FAIL 待 v3。

## 轮次记录

R2 验证轮: 8/8 处置 resolved, 但捕获 fix 引入回归 QA2-M1 (SC-6 窄化失锚) + facet 级枚举缺口 QA2-m1, 判 FAIL 进 v3。
