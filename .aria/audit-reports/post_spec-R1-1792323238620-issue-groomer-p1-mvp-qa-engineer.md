---
checkpoint: post_spec
mode: convergence
rounds: 1
converged: null
oscillation: false
overridden_by_user: false
degraded: false
verdict: FAIL
timestamp: 2026-10-18T11:33:58.620Z
context: issue-groomer-p1-mvp
agents: [qa-engineer]
---
drift_terminated: false
drift_check_skipped: false
is_refocus: false

## 审计结论

{"id":"QA-R1-M1","severity":"Major","lens":"SC 验收面完备性 + fixture 可构造性 + 反事实纪律","location":"proposal.md SC-1 + What Changed 4 + tasks 1.3/2.3","finding":"SC-1 的全称反事实主张「任一指纹分量实现退化成常量 ⇒ 对应态必红」与 fixture mandate 不匹配。分量级反事实仅对 ⑩ 钉死; R5 聚合报告移交给 spec 的两条分量级要求 (③ 上下文面四分量各设独立反事实变体 / ⑩ 补「既有评论编辑、无新评论」判别用例) 被错挂到 Tier B lane — proposal 把三条附注放在 Tier B fixture bullet、tasks 放在 2.3、#240 body 也收录 — 而真正执行 SC-1 判绿的 task 1.3 不含任何一条。后果一: SC-1 判绿时点早于变体产生时点, 1.3 全绿时分量级覆盖缺席。后果二 (直接假绿向量): 语料样本 6 条 comment 全部 created_at==updated_at、零编辑形态 — 不补判别用例, max(created_at)/count 类错误代理实现可全绿通过 ⑩ 与 SC-1。后果三: ⑨ provenance 面 (harness/model id 两分量) 同样无分量级 mandate, SC-1 全称主张在该面落空。","fix":"task 1.3 增列: ③ 态按四分量各设独立变体; ⑨ 态按 harness 与 model id 各设变体; ⑩ 补 comment-edit 判别 fixture (合成 updated_at>created_at 样本); 三条移交附注从 2.3 与 #240 body 移回 1.3, #240 勘正为仅 Tier B 语义项"}

{"id":"QA-R1-M2","severity":"Major","lens":"Rule #6 档位矩阵 vs SOT + SC 可机械验收 + Rule #10","location":"proposal.md SC-6 + Rule #6 矩阵 description 行 + tasks 3.1/3.2","finding":"SC-6 把 4b 义务写成「4b 处置留痕 (#239)」— 字面判绿允许 4b 未跑、仅留痕即绿, 与 SOT skill-benchmark-exemption.md §4.1 硬约束冲突 (description_changed=yes 而 scenario4b 为空/not_required/n/a ⇒ 不合规; 套件未经 owner 审阅 ⇒ 结果不能作门; fail/void ⇒ 不得 ship)。#239 解锁路径 = owner 审阅 20 条 seed query, 不在本 cycle 控制面内; task 3.2「如已解冻则入库」隐含未解冻仍可走完发版。未解冻分支的 ship 语义未定义且不在 2.2 五项待裁之内 — 留给 Phase 3 临场判断, 正是 Rule #10 禁区 (四类白名单中「结构性前提不成立」指审的对象未产生; 这里对象已产生, 缺的是量具, 不映射)。另: DEC 裁定-11 该行结论句「结构性填不出合规 rule6_note」在矩阵迁移中被删, 丢失冲突显式记载 (ab-suite/trigger/ 目录实测为空, 该前提成立)。","fix":"SC-6 拆两分支写死: 已解冻 ⇒ 4b 照跑且 pass 才绿; 未解冻 ⇒ Rule #6 义务未完成, ship 阻塞并升 owner 裁定 (比照 Rule #8 stub abort 语义)。或将该 ship 语义增为第六项待裁。矩阵 description 行恢复 DEC 括注"}

{"id":"QA-R1-m1","severity":"Minor","lens":"rule6_note 预填形式 vs SOT §4.1","location":"proposal Rule #6 矩阵 + tasks 3.1","finding":"四行矩阵自称「rule6_note 预填」但 SOT §4.1 是五字段单条 YAML (decision_table_row/description_changed/scenario1/scenario4b/negctrl); 多面变更如何折叠为条目未说明; negctrl 全程未出现。另第一行「场景 1 + SC 级结构化测试替代」措辞易误读为 substitute 之外还要跑场景 1 AB (SOT 第一行语义是替代, worked examples 均只 substitute)。","fix":"3.1 写明按变更面各成一条 §4.1 格式 (四条) 或声明折叠规则; 预填 negctrl 口径; 第一行措辞澄清"}

{"id":"QA-R1-m2","severity":"Minor","lens":"测试任务覆盖","location":"tasks 1.3","finding":"1.3 枚举与 SC 集合双向不对齐: SC-2 分页终止测试、SC-4 的 baseline no-diff fixture 与 top-N 上限 fixture、SC-5 差集+幂等 fixture 均未在 1.3 枚举; 反向 taxonomy 自检在 1.3 有任务无 SC 锚。","fix":"1.3 改为逐 SC 映射枚举, 补 baseline-run 与 top-N fixture; taxonomy 自检升 SC 或标注超额"}

{"id":"QA-R1-m3","severity":"Minor","lens":"fixture 可构造性","location":"proposal SC-5","finding":"幂等 oracle 前提「forgejo 对已有 label 的 add 为 no-op」未实证; 若 fixture 以 mock 实现该 no-op, 断言循环自证。差集断言本身不依赖该前提。","fix":"Phase 1 前对 10cg.local 实测一次 duplicate label add (结果落 references), 差集断言保持 harness 无关, no-op 仅作幂等语义注记不入 mock"}

{"id":"QA-R1-m4","severity":"Minor","lens":"SC 可机械验收 (dogfood)","location":"proposal SC-7 + tasks 4.1","finding":"dogfood SC 无判绿标准:「实跑 + 与手工梳理结果对照」未定义对照产物与通过判据。","fix":"定义验收产物: 全量条数对账 + 与 2026-10-18 手工梳理的差异逐条归因清单"}

{"id":"QA-R1-m5","severity":"Minor","lens":"语料契约","location":"proposal Why 节 + Deliverables + tasks 1.3","finding":"三份快照仅全量份路径在 proposal 正文, 另两份只在 DEC 与 #240 body; 「不复制入库」成立文但 scratchpad 未跟踪 ⇒ 语料无持久性保障且无再生成路径声明。","fix":"proposal 附三份完整路径 + 各自再生成命令, 或显式声明 scratchpad 唯一落点并接受风险"}

观察 (非 finding): ⑧ 态构造需确定性时钟 seam; task 2.2 第 11 态裁定选 last-writer-wins 时裁定后无挂靠实施任务建议补挂; 正面确认: #238/#239/#240 live 复核实存吻合 / ab-suite/trigger/ 空目录前提成立 / 三语料实存 / 10 态 by-reference 迁移无丢失改写 / ⑩ 括注忠实 / interactive 轨与 SOT §2 一致 / Validation Note 处置诚实。

## Verdict

FAIL。2 Major: M1 — SC-1 全称分量级反事实主张缺对应 fixture mandate, R5 移交要求错挂 Tier B lane 致判绿时点覆盖缺席, 叠加语料零编辑形态构成 ⑩ 态可证伪的直接假绿向量; M2 — SC-6 以「处置留痕」弱化 SOT §4.1 硬义务, #239 未解冻分支 ship 语义未定义且不入待裁清单, 构成 Rule #10 暴露面, 并在矩阵迁移中删除 DEC 冲突记载句。无 Critical; 两 Major 均为定点修订, 修订后应进下轮。

## 轮次记录

R1 qa-engineer 席: 通读 proposal/tasks + DEC-001 + Rule #6 SOT, 溯源 R4/R5 报告与聚合报告, live 复核三单/trigger 目录/三语料与 comment 时间戳形态; 产出 2 Major / 5 Minor / 3 观察, verdict FAIL。
