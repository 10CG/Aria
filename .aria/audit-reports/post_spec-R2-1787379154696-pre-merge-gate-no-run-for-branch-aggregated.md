---
round: R2
checkpoint: post_spec
mode: convergence
spec: pre-merge-gate-no-run-for-branch
seats: [A1-tech-lead, A2-backend-architect, A3-qa-engineer, A4-code-reviewer, A5-knowledge-manager]
verdicts: {A1: FAIL, A2: PASS_WITH_WARNINGS, A3: PASS_WITH_WARNINGS, A4: PASS_WITH_WARNINGS, A5: PASS_WITH_WARNINGS}
votes: {A1: REVISE, A2: REVISE, A3: REVISE, A4: REVISE, A5: REVISE}
verdict: FAIL
converged: false
incomplete: false
r1_disposition: {closed: 28, partial: 12, not_addressed: 0}
totals: {critical: 1, major: 21, minor: 18}
dedup_clusters: 14
major_trend: "R1 23 → R2 21 (持平); R2 Major 中 ≥ 2/3 落在 v2 新条款 ⇒ 边际转负拐点 (memory stop-adding-rounds / marginal-return-negative) ⇒ v3 缩面而非补丁"
timestamp: 2026-08-22T09:05:00Z
---

# post_spec R2 聚合 — pre-merge-gate-no-run-for-branch (aria-plugin#152)

五席一致 REVISE。R1 17 簇**方向**全部被认可 (0 not_addressed), 但 12 项 partial + 21 条新 Major 几乎全部长在 v2 为「自动执行处方」新写的条款上 (一次性守卫 / 求值时点 / dispatch 可用性 / TASK-0 成环 / prompt 语义 / 伪码 vs 2.3)。**信号**: 自动写动作这个子设计本身是审计面的发生器 —— 而它不在 owner 裁定 A′ (显影 + 处方, 不放行) 的字面里, 是 v1 起草时的加码。

## 去重后处置表 (→ v3)

| # | 来源 | 内容 | v3 处置 |
|---|------|------|---------|
| 1 | **A1-R2-C1** | `gate_state_helper.py` 运行时**零消费方** (SKILL.md 无一引用, 无 main(); docstring 自陈 reference 实现) ⇒ AD-7「机械实现」只到文档层, SC-11 在生产从不执行的代码上取绿 | helper 加 CLI (`record` / `clear`), workflow-runner SKILL 散文改为 **经 subprocess 调 CLI 维护 gate_state** (镜像 `phase1_gate.py` 先例); CLI 追加 append-only `.aria/gate-state-telemetry.jsonl`; 主仓 state-check `gate-state-helper-invocation` (14d 窗口, 镜像 `coordination-gate-invocation`) 作运行时探针 |
| 2 | A1-R2-M1 + A2-R2-M1 | `no_run_escalation_done` 跨 `write_gate_state` 整块重建会静默丢; `mark_*` 不落盘, Ctrl-C/resume 重武装 | **设计收缩**: 删自动动作 ⇒ 删 `done` 字段; 只剩 `no_run_observations`, 由 CLI `record` 单点读-改-写落盘; SC-11 断言跨两次 `record` 的 carry-forward |
| 3 | A1-R2-M2 + A4-R2-M1 | 求值相对自增的顺序仍未钉 (R1 #2 换量重犯), 默认 3 落 t≈210 非 90 | CLI `record` **先自增后返回** `{no_run_observations, should_prompt}`; SKILL 3c' 步骤 = 调 record, 3d exit conditions 消费其返回; 时间轴表钉死 (初次 obs=1 t=0 / #1 obs=2 t≈30 / #2 obs=3 t≈90 ⇒ prompt) |
| 4 | A1-R2-M3 + A4-R2-M3 | 2.1 伪码 `verdict=WAIT` 写死 vs 2.3 不存在→fail 互斥; `pr_branch_check` 形参类型/None 语义未定 | PR 分支不存在改为 `gate_check` **第八个早退** (`_build_output(verdict=fail, kind=pr-branch-not-found)`), `compute_verdict` 不感知分支核验, 删 `pr_branch_check` 形参 |
| 5 | A4-R2-M2 | 别名实现细节分叉: 改参数名致 `:449` 关键字调用 TypeError; 改调用点致 mixin `:85-89` 旧名打桩 28 测试失效走真 ls-remote | 钉死: 新函数 `_verify_branch_exists(branch, remote, timeout)`; 旧名保留为**保关键字签名的包装** (`main_branch=` 形参不变), `:449` 字面不改; PR 核验调新名; 测试 mixin 对两个名各打一桩 |
| 6 | A1-R2-M5 + A4-R2-M5 + A3 (#10 partial) | TASK-0 与 SC-13 互为前置成环; 失败分支连锁处置 (§4 死字段 / SC-8/9 / 2.2 表 / 处方 1) 未列; dispatch 2xx 但 600s 零 run 无第三分支 | TASK-0 拆为 **TASK-0a (实现前纯 API 探针, 不依赖本 spec 代码)** 结果=布尔 `dispatch_viable` 落 traps §6 (仓内 SOT, memory 为镜像); §4 **无条件**实现 (字段恒算, 测试恒跑); 只有 prompt 文案里「dispatch 命令」一句随布尔取舍; SC-13 在实现后跑, 三分支结果 (not_found→passing / 600s 仍 not_found 记拥堵数据点 / 4xx 记权限) |
| 7 | A1-R2-M6 + A4-R2-M4 + A1-R2-m4 | 2.5 是「不退出的 exit condition」; 2.6 continue 后状态未定 ⇒ 每轮复弹; 处方 3 与 2.6 双弹同形 prompt; 多 workflow 部分 2xx fall-through 未定 | **设计收缩**: 删 2.5 自动动作与 2.6; 只留**一条** exit condition 2.5 = `should_prompt` → 「no-run prompt」(定义一次): `continue` ⇒ CLI `record --reset-observations` (obs=0, 其余不动) 回 loop; `abort` ⇒ fail。无自动 dispatch/commit ⇒ 无幂等/部分成功问题 |
| 8 | A1-R2-M4 + A3-R2-M1 + A4-R2-M7 | NEG-4 未登记 catalog `fixtures[]` (+`test_case_in_unit_tests`), 有记录无路由; 缺口 issue 已存在 **aria-plugin#127 (open)**; 序列型行为 fixture 无消费机制 | 点名行为收缩为**两条可单步证伪**: (i) surface `gate_error.message` 原文 (ii) `should_prompt=true` 时出 prompt 而非继续等; NEG-4 登记进 catalog + 绑 SC 测试; 缺口追加到 #127 评论, 删「若无则新开」 |
| 9 | A2-R2-M2 + A4-R2-M6 + A1-R2-m3 + A2-R2-m2 | `DEFAULT_CONFIG` 未列落点 (state-check `config-template-key-currency` 实测 FAIL); 校验点「只在 gate_check」与 SC-2/3 直调 compute_verdict 矛盾; §3.3 误引 SC-10 | 单函数 `_effective_escalation_threshold(cfg) -> int` 为唯一校验点, `compute_verdict` 与 `gate_check` 都经它; `DEFAULT_CONFIG` 加键列入落点; SC-3 对该函数断言; 引用勘正 |
| 10 | A4-R2-M8 | §5 仍漏 3 处: workflow-runner SKILL `:249-264` gate_state JSON 块 + `:345` 字段枚举 / schema `:38-52` JSON 块 / `aether.py:218` docstring | §5 补三行 (17 处) |
| 11 | A5-R2-M1 | DEC 修正案弱于先例 (DEC-20260702-001:124-128「前向指针」段格式: 原文不回改 + 文末日期化段 + 小节内 📌 指针) | §5 按先例格式钉死两处写法 |
| 12 | A5-R2-M2 | 主仓侧版本引用点未按 #177 列 (漏 `CLAUDE.md:5` 版本行 — 注: 那是主项目版本非插件版本, 本 PATCH 不动; 漏 `README.md:242` `Plugin Version:` 行) | 主仓侧引用点枚举: `README.md:8` badge + `:242` Plugin Version 行 + gitlink; `CLAUDE.md:5` 是主项目版本 (2.0.0), 本 spec 不动但点名 |
| 13 | A5-R2-M3 | 三个 Phase D 待立 issue 只是散文承诺, 无机械路由; #152「立案时」时态不对 (0 评论) | 新增 `## Phase D 待办 (AI, D.1 执行, 归档门前置)` 清单 + #152 评论改为「A.1 批准后」; A.2 task-planner 把该清单转成 tasks |
| 14 | A1-R2-m1 + A4-R2-m1 + A2-R2-m1 / A1-R2-m2 / A4-R2-m2 / A4-R2-m3 / A4-R2-m4 / A5-R2-m1 / A5-R2-m2 / A1-R2-m5 / A1-R2-m6 / A2-R2-m3 | reason 族 = **8** (7 规则终态 + internal-error; `path_coverage.py:36` 自写 9 是既有错) 且三档带 `: <detail>` 载荷须**前缀匹配** / 所有 kind 走副本通道 + SC 断言 / `pr-branch-not-found` 的 path_coverage 在场随 enabled 条件化 / Impact 补全 additive / `:362→:363` / traps §6 删 F1 (读码可得) / memory 修正须带证据 / 直调 §C.2.4 时处方段不可达声明 / unknown 三档 remedies=[] (解析器读不懂的 workflow 不让 AI 手工猜) / mixin mock 惯例明说 | 逐条吸收 |

## 席位实测亮点

- A1: `grep -rn gate_state_helper` 全 SKILL.md 零命中 (C1 根据); 2.5/2.6 与 exit 2 `retry_count` 重置的互作推演。
- A2: `config-template-key-currency` 用合成模板**复现 FAIL**; `write_gate_state` 整块重建实读。
- A3: episode 状态机穷举 (归零后再达阈路由正确); `test_gate_state_helper.py` 22 测试无 exact-keys 断言 (无回归); `forgejo GET issues/126` 追到 #127。
- A4: 别名两种实现各自的失效面实测 (TypeError / 28 测试走真 ls-remote); 14 处行号全准 + 3 漏。
- A5: DEC 全目录先例格式; #177 全文; #152 当前 0 评论。

## 收敛判定

R2 REVISE (5/5), Major 持平 ⇒ **v3 缩面** (删自动动作子设计, helper 真接线) → R3 (max_rounds=4, 剩 2 轮)。v3 的设计收缩偏离 v1 对 A′ 的扩写, 在 spec 头部向 owner 显式标出。
