---
round: R1
checkpoint: post_spec
mode: convergence
spec: pre-merge-gate-no-run-for-branch
seats: [A1-tech-lead, A2-backend-architect, A3-qa-engineer, A4-code-reviewer, A5-knowledge-manager]
verdicts: {A1: FAIL, A2: PASS_WITH_WARNINGS, A3: PASS_WITH_WARNINGS, A4: FAIL, A5: PASS_WITH_WARNINGS}
votes: {A1: REVISE, A2: REVISE, A3: REVISE, A4: REVISE, A5: REVISE}
verdict: FAIL
converged: false
incomplete: false
totals: {critical: 2, major: 23, minor: 21}
dedup_clusters: 17
timestamp: 2026-08-22T07:05:00Z
note: A5 首次 dispatch API 断线未落盘, 重派一次成功 (audit-engine 错误处理: 重试一次)
---

# post_spec R1 聚合 — pre-merge-gate-no-run-for-branch (aria-plugin#152)

五席一致 REVISE。方案方向 (backend 零 run → `not_found`; gate `wait` + `gate_error` 显影; 不放行) **五席均认可**, 0 席质疑 AD-2 的 wait-vs-fail-vs-green 结论。两条 Critical (A1-C1 / A4-C1) 同根, 与 A2-M2 / A3-M1 共四席独立命中: **升级处方的「计数量 / 一次性守卫 / 计时基准」三者都没钉死** ⇒ runner 真停摆时退化为每周期自动 push/dispatch 的循环。

## 去重后处置表 (→ v2)

| # | 来源 | 内容 | v2 处置 |
|---|------|------|---------|
| 1 | **A1-C1 + A4-C1 + A3-M1 + A2-M2** | 升级处方无一次性守卫; `retry_count` 归零唯一现成路径 (`clear+write`) 连带重置 `started_at` ⇒ 1800s 上界失效; dispatch 成功但 run 未被领 → 再 dispatch (治盲区的手落进同一盲区) | 删「retry_count 归零」; `gate_state` 加 `no_run_observations` (int) + `no_run_escalation_done` (bool); 每 episode **至多一次**自动动作; 动作后若再次达阈 → 直接 user prompt (exit 2 语义); `started_at`/`retry_count` 不动; `gate_state_helper.py` 纳入落点, 加 `record_gate_error_kind()` / `should_escalate_no_run()` / `mark_no_run_escalation_done()` 三函数 + 单测 |
| 2 | A1-M1 + A4-M1 | 判定式读 `retry_count` 但其自增在 verdict 之后 ⇒ 「第 2 次重查 ~90s」实为第 3 次 ~210s; 两实施者必分叉 | 计数量换成 `no_run_observations` (含初次, helper 内单点自增); 阈值默认 **3** (= 初次 + 30s + 90s); 键改名 `no_run_escalation_observations` (与量同名); AD-4 秒数对齐 |
| 3 | A1-M4 | `gate_error_kind` 有记录无路由; 「重复观测」与判定式不同构 | 删 `gate_error_kind`; 判定式真用 `no_run_observations` (连续同 kind 计数, 非同 kind 归零); 「episode 内 `not_found` 单调 (tasks 端点全量历史无截断, A1 实测 2458/2458)」写成显式不变量入 traps §6 |
| 4 | A2-M3 | 旋钮两消费方 (gate 校验 / workflow-runner 读原始 config) | 单一校验点 = gate; gate 把生效值作**机读字段** `gate_error.escalate_after_observations` 输出; workflow-runner 只消费 gate 输出, 不读原始 key |
| 5 | A4-M3 | 升级判定在两个 Skill 各写一遍 (traps §五 同病) | 判定**只**在 workflow-runner 2.5 (机械实现 = `gate_state_helper.should_escalate_no_run`, 散文引用它); §C.2.4 步骤 6 只做 surface + 承载处方文本, 入口「仅由 2.5 转入」 |
| 6 | A1-M2 + A4-M6 | message 以 decision 为键, 但 covered 含 3 reason; `empty-diff`/`workflow-files-changed` 下 matched=[] 渲染自相矛盾; pc=None 时 gate_error 与 path_coverage 不同场 | message 按 `(decision, reason)` 钉 5 档封闭表; SC-2/3 参数化全 9 reason + None; SC-5 拆 enabled/disabled 两变体; :290 改条件措辞 |
| 7 | A1-M5 | (a) 轴缺 PR 分支存在性核验, §1:47「由 #137 2.2 兜底」不成立 (2.2 只核 main); 分支不存在会被误归因 #152 并在假因上执行处方 | `_verify_main_branch_exists` 泛化为 `_verify_branch_exists(branch, remote)`; `not_found` 路径对 `pr_branch` 核验: 不存在 → 新 kind `pr-branch-not-found` `verdict=fail`; 核验失败 → 保持 `no-run-for-branch` + message 附注。kind 封闭集 4 |
| 8 | A1-M6 | §1 对 (b) 轴「空 runs = 正确语义」与 Why/AD-2 赖以立论的事实 (tasks 只列已领) 矛盾; (a)(b) 共用数据源, (b) 腿同形分钟级 fail-open 被书面封死 | §1:47 改为 **scope 声明**; Impact「不受影响」改「本 spec 不改 (b) 轴, 同形盲区另案」; traps §6 记录; Phase D 立案 aria-plugin issue |
| 9 | A3-M2 + A1-M3 + A4-M5 | Rule #6 选错判据表行; 3 份 AB 资产 (fixtures 实为 7 非 6) 结构上到不了 `not_found`; 同目录 NEG-3 (#126) 先例走的是第三行 | rule6_note 改**第三行**: 点名行为 + 定向 fixture `NEG-4-no-run-for-branch.json` (含 `_target_behavior`/`_discriminating_question`/`_arm_expectations`) + 套件缺口 issue; 引 #126/NEG-3 为先例 |
| 10 | A3-M3 + A4-m5 + A1-m4 | AD-4 阈值依据薄; SC-13 只验结构性一侧且 dispatch 后立刻再跑 gate 会 flaky | 误升级代价经 #1 设计后**有界** (至多一次多余 dispatch, 无 commit 污染) ⇒ 阈值敏感度降; SC-13 改「轮询至非 not_found 或 600s」+ 记录 dispatch→领取 Δt 作 AD-4 首个数据点; 离线侧信道经本 session 实测不可行 (tasks 的 created_at=run_started_at 同值) |
| 11 | A4-M7 + A5-M3 | `workflow_dispatch` 未真触发; memory `reference_forgejo_new_branch_paths_filter_no_run` 写「gitea-1.22 系不可用」与本 session 探针 (400 ref is empty) 互斥; AD-5 建在未验前提上 | Phase B **TASK-0**: throwaway 分支真触发一次 (记 HTTP 码 / 是否建 run / 领取 Δt); 成功 → 修正 memory; 失败 → AD-5 改「处方 2 为主, dispatch 可选」。spec 显式写两种结果各自的落点 |
| 12 | A2-M1 + A4-m2 | 新 elif 须插在 `elif main_in_flight_runs:` **之前**, 否则 not_found×main-busy 吞 gate_error (verdict 仍 wait ⇒ 只有 kind 断言能红) | §2 伪码标注插入位置 + 代码防呆注释; SC-4 红窗声明改「红在 `gate_error.kind`」并强制断言 kind |
| 13 | A4-M4 + A4-M2 + A2-m2 | §5 同步面漏 7 处 (:172-183 摘要块 / :292-302 第二配置表 / :241 计数 / 两处 docstring / workflow-runner :313+:326 / schema :125 / config.template.json); `write_gate_state` 无新入参; format_version 是否 bump 未定 | §5 改逐行号清单 (14 处); helper 入参 `gate_error_kind`; format_version **不 bump** (可选块内 additive 键 + 防御 `.get()`, 与 v1.1 读者兼容), 明写 |
| 14 | A5-M1 | `DEC-20260731-001`「wait 真正意味着 CI 在跑或该跑没跑完」被 #152 证伪, spec 零引用 | §5 加: DEC-20260731-001 **append-only 修正案**段 (不重写原文), 指向本 spec; Cross-refs 引用 |
| 15 | A5-M2 | F3 (`pull_request` 触发面结构性死亡) 满足 traps 收录判据未列入 §6 | traps §6 收录 F1/F3/tasks 全量历史/(b) 轴同形/端点 404 五条 |
| 16 | A5-M4 | 版本同步面「5 文件」口径沿用 CLAUDE.md 被 #177 指错的框架 (`marketplace.json` 2 处 version) | 改「引用点」口径 + 点名 marketplace.json `:3`/`:16`; 引 #177 |
| 17 | A2-m1 / A2-m3+A1-m1+A4-m4 / A1-m2+A4-m6 / A1-m3+A3-m3 / A1-m5 / A1-m6 / A3-m1+A4-m1 / A4-m3 / A5-m1 / A5-m2 | cfg=None 防御 / SC-7 七落点 + 「六键」措辞 / pc=None·workflow-files-changed 下处方 1 不可用 / 伪码穿 gate_error + `_result` 调用点必改 / dispatch 绕过 CIBackend 抽象 / AD-1 转述 A 失真 / reason 9=8 规则+internal-error·行号 :276·fixtures 7 / message 子串闭集 / kind 二维消歧表 / #152 收尾留言 | 逐条吸收 (见 v2 对应段) |

## 席位实测亮点

- A1: `aether ci status --branch zzz-no-such-branch-152` → `runs=[]` 与存在分支零 run **逐字节同形** (M5 实证); tasks 端点 returned==total_count 三仓核验 (M4/M6 前提); Aether CLI 源码 `status.go:45-47` 确认 (a)(b) 共用 `/actions/tasks`。
- A2: 误序 elif 模拟 (`not_found + main_inflight=[{id:1}]` → gate_error 被吞) ; `gate_state_helper.write_gate_state` 归零路径实读。
- A3: SC-6 mutation test (漏 return) 真区分好坏实现; 三份 AB 资产逐条 json 遍历, NEG-3 `_description` 逐字引用。
- A4: 7 处同步面逐 grep 行号; dispatch 路由复跑 400; 早退落点实数 7。
- A5: `marketplace.json` `:3`/`:16` 双 version 实核 (#177 属实); DEC-20260731-001 原文逐字比对。

## 未被任何席质疑 (稳定项, v2 不动)

F1/F2/F3 三事实; 基线 `compute_verdict([], "not_found")` → green 的潜伏 fail-open 与「§1 §2 同 commit」; AD-2 wait 结论; AD-3 复用 `gate_error`; AD-6 不动 Aether/上游; Level 2 判定; Status 行机读格式; Rule #10 brainstorm 豁免定性 (A5 核: `post_brainstorm` config 显式 off ⇒ 白名单第一类, 非自行豁免); #122/#126/#137/BA-8 引用准确。

## 收敛判定

R1 REVISE (5/5) → v2 落上表 17 簇 → R2。
