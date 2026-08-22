---
round: R5
checkpoint: post_spec
mode: convergence
spec: pre-merge-gate-no-run-for-branch
seats: [A1-tech-lead, A2-backend-architect, A3-qa-engineer, A4-code-reviewer, A5-knowledge-manager]
verdicts: {A1: PASS_WITH_WARNINGS, A2: PASS_WITH_WARNINGS, A3: PASS, A4: PASS, A5: PASS}
votes: {A1: REVISE, A2: REVISE, A3: PASS, A4: PASS, A5: PASS}
verdict: PASS_WITH_WARNINGS
converged: false
oscillation: false
incomplete: false
max_rounds: 6
r4_disposition: {closed: 17, partial: 3, not_addressed: 2}
totals: {critical: 0, major: 2, minor: 16}
dedup_clusters: 4
major_trend: "23 → 21 → 18 → 5 → 2; PASS 席 0→0→0→2→3"
erratum_r4_aggregate: "R4 聚合表簇 #6 写「全部吸收 (A3 一条不采)」失实 — 实际 A2-R4-m1/m2 两条与 A3 两条未采 (A3-R5-m2 / A2 席指出); 本 R5 聚合以此勘正, v6 已补 A2 两条"
timestamp: 2026-08-22T14:05:00Z
---

# post_spec R5 聚合 — pre-merge-gate-no-run-for-branch (aria-plugin#152)

owner 加轮后的稳定性确认轮: 3/5 PASS (qa / code-reviewer / km), A1/A2 各 1 条窄 Major, 均为 v5 新文字 (SC-13 活体地点 / `<pr_branch>` 回填无 SC)。R4 5 条 Major 簇**全部 closed** (五席独立核)。

## 去重后处置表 (→ v6, 已落)

| # | 来源 | 内容 | v6 处置 |
|---|------|------|---------|
| 1 | **A1-R5-M1** + A1-m5 | SC-13 钉在主仓根, 但主仓 workflow 的 paths 全指向子模块挂载点, 主仓树内构造不出 `workflow-trigger-matched`; CLI 行无 `--state-file` ⇒ 子模块 cwd 下静默另起 state | SC-13: gate 在 **aria-plugin 根**跑 + `--state-file` 主仓**绝对路径** (正是「cwd 与 state 位置两回事」的活体检验); §3.2 所有 CLI 调用显式传 `--state-file` |
| 2 | **A2-R5-M1** + A1-m3 | v5 新加的 `<pr_branch>` 回填 + raw_message 重同步零 SC (SC-5 只查键在场) | SC-5 加 (c)(d): message 含分支名、不含字面占位、`raw_message == message`; verify-failed 后缀 + 同步 |
| 3 | A1-m1/A4-m1 · A1-m2/A4-m3 · A1-m4/A4-m2 · A4-m4 · A1-m6 · A2-R4-m1/m2 (R4 未采) | 「七个早退落点」残留 / `{o}/{r}` 残留 + `.format` 理由 / reset 签名句 / R-e 与 3d 不一致 / 零 run 第三成因 (branches 过滤) / `record` verdict≠wait 文件缺失 + `reset_retry_count` 具名 | 全部吸收 |
| 4 | A3-R5-m1/m2 · A5-R5-m1 · A2-R5-m1 | SC-15 两 skill 证据覆盖 / 聚合表失实 (见 erratum) / traps 日期对称 / `DISPATCH_VIABLE` 读取方式 (裸全局 vs 默认参捕获) | 聚合勘正; 其余三条非强制, 留 Phase B 实施时顺手 (不阻塞) |

## 席位实测亮点

- A1: `git ls-files aria` = 1 条 gitlink, 主仓 paths 过滤 workflow 实核; path_coverage 不建模 `branches` 实跑。
- A2: SC-5 触发路径逐行追 (`not_found` + mock ok) 只断言键; `started_at` 不变量与 `reset` 不冲突 (不同函数)。
- A3: `_find_project_root` 实读 + 主仓/子模块各自 `issue-triage-tests.yml` 交叉验证; SC-16 三段与 `openspec-archive SKILL.md:234` / `runtime_probe.py::probe()` / `_fold_runtime_probe_declaration` 一一对应。
- A4: v5 27 处 diff 引用/编号稳定性逐处; 4 处残留口径。
- A5: `collectors/_status.py` 实跑 → pending; owner_rulings 与 AskUserQuestion 逐字匹配; 4 处新行号全准。

## 收敛判定

未全票 (3/5) → v6 落 2M + minors → **R6 = max_rounds=6 末轮**。若 R6 5/5 PASS ⇒ CONVERGED; 否则再交 owner 三路径。
