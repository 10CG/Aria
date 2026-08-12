---
checkpoint: post_planning
mode: convergence
rounds: 4
converged: false
oscillation: false
overridden_by_user: false
degraded: true
verdict: FAIL
timestamp: 2026-08-12T02:00:00.000Z
context: openspec/changes/premerge-gate-mainbranch-failclosed/detailed-tasks.yaml
agents: [tech-lead, backend-architect, qa-engineer, code-reviewer, knowledge-manager]
drift_terminated: false
drift_check_skipped: true
is_refocus: false
---

# post_planning R4 汇总 — `max_rounds` 走满

> 被审对象 = R3-fix 后的 A.2 产物 (`e970943`)。**`max_rounds = 4` 已耗尽。**
> 按 audit-engine, 未收敛 + max_rounds 耗尽 ⇒ **触发降级策略, 这是 owner 裁量, 不是 AI 判断。**

## 投票

| 席位 | VOTE | VERDICT | C+M+m | 阻塞 B | fix 引入 |
|---|---|---|---|---|---|
| code-reviewer | REVISE | FAIL | 1+4+6 = 11 | 3 | 9 |
| tech-lead | REVISE | FAIL | 1+5+2 = 8 | 3 | 4 |
| knowledge-manager | REVISE | PASS_WITH_WARNINGS | 0+4+0 = 4 | 0 | 2 |
| qa-engineer | REVISE | FAIL | 1+1+1 = 3 | 0 | 3 |
| backend-architect | REVISE | PASS_WITH_WARNINGS | 0+2+0 = 2 | 0 | 2 |

**5 REVISE / 0 PASS** (四轮里第一次零 PASS 票) · verdict **FAIL** · `converged: false`。
原始 **3C + 16M + 9m = 28** · **6 条 `blocks_phase_b`** · fix 引入 **20/28 = 71%**。

## 四轮完整轨迹

| 轮 | 投票 | 原始 | 去重 | 阻塞 B | fix 引入 | 干预手段 |
|---|---|---|---|---|---|---|
| R1 | 4R/1P | 52 | 3C+12M+8m | 6 | — | 原作者执笔 |
| R2 | 4R/1P | 30 | 1C+~13M | 12 | **53%** | 换人执笔 |
| R3 | 4R/1P | 27 | 2C+~13M | 10 | **70%** | 换人执笔 + 机械交叉检查 |
| R4 | **5R/0P** | 28 | 3C+~13M | 6 | **71%** | 同上 + 停止预写量 + 对抗验证 |

## ⭐ 本轮最重要的结论: 这个循环**对单条 finding 收敛, 对总量不收敛**

**五席独立确认 R2 与 R3 的 findings 全部闭合、无一复发。** tech-lead 逐条回源:
> 「R2 的 1C + ~13M **无一复发**, R3 的 2C + 三条事实错误亦已闭合 …
> 本轮 8 条 findings 中**没有一条是旧条目的复发**。」

⇒ **执笔环节不是问题** —— 每一轮都真的修好了上一轮点名的东西。
⇒ 问题在于**每轮 fix 引入约等量的新缺陷** (53% → 70% → 71%), 且**去重 Major 四轮持平在 ~13**。

这是一个**稳态**, 不是一条收敛曲线。再加轮只会在同一水平线上换一批 finding。

## 机械交叉检查: 有实质提升, 但仍不足以支撑它被读出的结论

R4/tech-lead 在隔离副本做了 **8 个不在其自带对抗套件覆盖内**的构造: **4 拒 / 4 放行**
(对比 R3 的 **1/5** —— 拒绝能力确有实质提升)。放行的四个:

| 构造 | 为何逃逸 |
|---|---|
| A 删掉 TASK-011 对 SC-M12 的落地复跑认领 (**原样复现 R2 那条 Major**) | `RED_CTX` 五个字面串认不出 TASK-001 那条「明确不建红窗 + 理由」bullet ⇒ 把**免责说明**记成转绿认领 ⇒ SC 表 20 行中 **4 行结构性 fail-OPEN** |
| B 抽掉 SC-M6 两个半边的 DAG 序 | CHECK1 注释逐字「不收『半边归 TASK-xxx』这类措辞」—— 而「按半边拆分认领」**正是 R3-fix 自己新造**的移交形态 ⇒ **本轮新造的那一类移交正是它明文不管的那一类** |
| C 行号做成活验收量但写「行号必须是 262 与 559」(不带冒号) | `QUANT` 正则强制比较符紧接冒号锚 |
| E 与 §6 相反的插入点写成「紧随 evaluate_path_coverage 执行」 | CHECK4 **拒的是动词表里的词, 不是关系** (同一冲突用「必须落在…之后」则被正确拒绝) |

**恒绿/零覆盖面**: CHECK4 三条回归子项是硬编码串存在性 · **CHECK5 因「今日实测非数字」直接 skip 9/20 行**
(⚠️ 主 loop 在 R4 之前已独立构造出这条: 整列删掉比伪造更常见, 而它被"跳过"放行) ·
CHECK1 的定向断言只覆盖 **20/82 = 24%** 的 (task, 被点名 TASK) 提及 · CHECK6 对 tasks.md 组标题顺序承诺天然失明。

**仍是「只修实例不修类」的产物**: `RED_CTX`/`HANDOFF`/`HISTORY`/`QUANT_EXEMPT`/`PRESCRIBE`
全部是从本 Spec 当前文本采下的**字面串**。

⇒ 席位的判词值得逐字记下:
> 「tasks.md:7 与 metadata.audit_state 的『12/12 构造被拒』**在字面上为真** (对它自己挑的 12 个),
> 但读者会读出的『R2 那两个形状已被机械杜绝』**为假**。」

## 三条 Critical (择要)

1. **`TASK-017` 第 9 项「主仓 gitlink」判据在 Phase B 结构上不可求值, 且照字面求值会产出它自己引用的 Aria #165**
   —— `CLAUDE.md` 约束 1 规定子模块合并本地做、主仓**随后**才 bump gitlink ⇒ 该 SHA 由 **Phase C.2** 产生。
   实施者若为让断言成立而在 Phase B bump gitlink 到 feature 分支 tip ⇒ **正是 orphaned gitlink** (已四次复发)。
   ⚠️ **同一次提交里 TASK-015 做对了这个拆分并把规则提升为 `metadata.evaluation_time_convention`,
   而同轮新写的 TASK-017 没做** —— 又一次「只修实例不修类」。
2. `.aria/config.template.json` 的 **legacy 键名面零机械断言** —— SC-M18 这个**类级**修复
   把「唯一受众在仓外的落点」**显式排除**在外。构造一个「删光承诺措辞但两个键原样留着」的实现,
   **20 行 SC + §6.1 三用例 + TASK-021 终局收口全绿**, 而每个新采用方 clone 后第一次跑 gate 即撞硬失败。
3. (第三条见 qa-engineer 报告)

## 一条 Major 值得单独看

**`CLAUDE.md:113` 的既有陈述被 TASK-020 条件性证伪, 而无任务承接、DAG 上无序。**
`:113` 逐字「无可用 backend 按 `no_ci_fallback` 显式降级」; 而 §6.1 用例二规定
「`enabled=true` + legacy key + 无可用 backend ⇒ `fail`」⇒ 该输入类结构上走不到 `:339` 的降级。
`TASK-016` 只锚在「新增第三条阻断腿 = 分支存在性」, 对这第四条阻断行为**零覆盖**,
且 `dependencies` 不含 `TASK-020`、拓扑上无序。直接抵触不可协商规则 **#3「文档与代码必须同步更新」**。

## ⚠️ 编排层第 8 条错误 (code-reviewer 席位抓到)

R4 的任务书里「被审对象 = R2-fix (`0dd26ce`)」**已陈旧** —— 实际被审对象是 R3-fix (`e970943`)。
成因: 我用 `sed` 从 R3 脚本改出 R4 脚本时只替换了轮次号, **漏了正文里的基线描述**。
席位自行实测纠正了口径并照常完成审计, 未造成错审, 但这是我第 8 条自身错误。

## 处置 — `max_rounds` 结构性耗尽, 降级策略是 owner 裁量

按 audit-engine `report-storage.md`: `converged: false` + `drift_terminated: false`
⇒ **触发降级策略**。本报告 frontmatter 已置 `degraded: true`。
**这不是 AI 的判断, 是协议走到终点。** (⚠️ 我在 R3 后曾以「大概没用」为由想停在 R3 —— 那是
Rule #10 之外的性价比理由, 已纠正并跑满 R4。)

### 交给 owner 的三个方向 (AI 不代裁, 但给出本轮新增的判据)

1. **拆 Spec** —— **四轮数据现在直接支持它**: 去重 Major 四轮持平在 ~13, 而每轮 fix 引入 ~71%;
   同时**旧 finding 无一复发**。这个组合说明**问题不在执笔也不在审计, 在被审对象的规模**:
   21 条任务 / 70 est_hours / 跨两仓 20 个路径 / 20 行 SC —— 条款间的隐含前提数量已超过
   任何单轮 fix 能同步的范围。原始缺陷 (#137 那条恒绿腿) 仍可用**小时级**最小改关掉。
2. **接受当前结论 + `converged: false` 留痕** —— 有 `phase-c-integrator-ci-path-coverage` 先例
   (owner 2026-07-26 裁定 [1] 接受)。R4 的 6 条 `blocks_phase_b` 须逐条明示"接受"或"先修"。
3. **超配 R5** —— post_spec 曾由 owner 把 max_rounds 4→6。但四轮趋势 (零 PASS 票 / Critical 3→1→2→3)
   不支持"再一轮就能收敛"的预期。

**Phase B 仍被本闸门阻断** (6 条 `blocks_phase_b`, 含 3 条 Critical)。Rule #10: AI 不得自行豁免。
