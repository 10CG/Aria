---
round: R1
checkpoint: post_planning
mode: convergence
spec: pre-merge-gate-no-run-for-branch
context: openspec/changes/pre-merge-gate-no-run-for-branch/detailed-tasks.yaml
seats: [A1-tech-lead, A2-backend-architect, A3-qa-engineer, A4-code-reviewer, A5-knowledge-manager]
verdicts: {A1: FAIL, A2: PASS_WITH_WARNINGS, A3: PASS_WITH_WARNINGS, A4: PASS_WITH_WARNINGS, A5: PASS_WITH_WARNINGS}
votes: {A1: REVISE, A2: REVISE, A3: REVISE, A4: REVISE, A5: REVISE}
verdict: FAIL
converged: false
incomplete: false
totals: {critical: 1, major: 14, minor: 16}
dedup_clusters: 12
timestamp: 2026-08-22T19:40:00Z
---

# post_planning R1 聚合 — pre-merge-gate-no-run-for-branch (detailed-tasks.yaml v1 → v2)

五席 REVISE。A.2/A.3 派生层三个结构错 (memory `postplanning_catches_a3_derivation_blindspot` 再实证): `status: skipped` 不在归档门 done 白名单 (C1) / INV-3 条件组只编码了 TASK-007 而 rule 列的四个落点分属四任务 (四席独立命中) / TASK-007 把 RED 与 GREEN 合进单任务单 agent 破坏 INV-2 配对。覆盖层: SC 16 条均有承载 (A3/A4 逐条核), §5 20 行全承载 (A4), 但三条 SC 子条款 (SC-3 末句 / SC-11(d) reset 成功路径 / INV-5 grep 落 TASK-011) 漏。

## 处置表 (→ v2, 已落)

| # | 来源 | 内容 | v2 处置 |
|---|---|---|---|
| 1 | **A1-C1** + A3-m1 + A5-m2 | `skipped` 不在 `detailed_tasks.py` done 白名单 {done, completed} ⇒ 条件跳过后 spec 永远 complete=false + d_payload 假 deferred | 禁用 `skipped`; 条件整任务 false ⇒ `status: completed` + notes 首词 `N/A —` (先例惯例); `readiness_rule` 写进 metadata; `metadata.dispatch_viable: null` 占位 |
| 2 | A1-M2 + A2-M1 + A4-M1 + A5-M1 + A1-M1 | INV-3 `encoded_as`「其余任务无条件」与 rule 互斥: §2.1 `.replace` (TASK-006) / 3.3 (a) 行 + 2.3 渲染句 + dispatchable 字段文档 (TASK-011) / CHANGELOG 不提 (TASK-015) 都在条件组; skipped 下游就绪语义未定 | TASK-006/011/015 加 `conditional_parts` + 依赖边 → TASK-001; INV-3 rule/encoded_as 重写列全四落点; readiness_rule 定义 completed(N/A) 视为满足 |
| 3 | A1-M5 | TASK-007 RED+GREEN 同任务同 agent | 拆 TASK-007a (qa, RED) → TASK-007b (be, GREEN); total 18 |
| 4 | A1-M4 | 守卫 TASK-004 依赖 TASK-003 (落在被守护变更之后 ⇒ 自证快照); SC-7 无坏实现对照 | deps → [TASK-000], 钉基线 9e6a17c 入 docstring; SC-7 加「多/少一键」mutation; exec_order 前移到 2 之前 (gate 轨首位) |
| 5 | A1-M3 | INV-1「两文件共现」是无向检查 | 有向: 父提交上 `_normalize_pr_ci_status([])=='pending'` 且本 commit 同含两文件; 验证者 = main-loop (子 agent 不 commit) |
| 6 | A1-M6 + A4-m3 | traps §六 三写者无序 (TASK-001/011 双写 TASK-0a 行; TASK-011 无边到 001; :241 终计数未定) | 建节权 = TASK-001 (标题 + TASK-0a 行); TASK-011 上方插四行且依赖 001; TASK-014 末尾追加 + 终改 :241 |
| 7 | A1-M7 + A1-m5 | 主仓 5 类改动只有版本点有提交承载; 无主仓 B.1 分支 (字面 = 直推共享 master); 核验漏 github + ls-remote 重试 | TASK-015 (ii) 主仓 feature 分支承载全部 5 类 + PR/本地 merge + 双 remote 核验 (重试) + 不带路径 git status |
| 8 | A3-M1 / A3-M2 / A3-M3 | SC-3 末句跨路径一致未承载 / SC-11(d) reset 成功路径未列 / INV-5 grep 未落 TASK-011 | TASK-005 加 SC-3 末句用例; TASK-008 加两条成功路径; TASK-011 verification 加 INV-5 grep |
| 9 | A5-M2 | TASK-001 的 traps 行 + memory 修正无 verification | 加两条 verification (建节 + 证据串 grep 可核) |
| 10 | A4-m1 | **v1.66.4 无 tag** (`git describe` = v1.66.3-15-g9e6a17c, 对方 ship 漏打) | TASK-015 补打 v1.66.4@9e6a17c (version-management §4.3) |
| 11 | A4-m2 / A4-m4 / A4-m5 / A4-m6 / A1-m4 / A3-m2 | TASK-011 deps 缺 010; SC-14 机检脚本无落点; 「直调不可达」措辞反义; metadata.dispatch_viable 占位; TASK-002 test_ci_backends 歧义 (实核只在 test_pre_merge_gate.py); dispatchable 字段文档无承载; SC-15 绑定名约定 | 逐条吸收 (SC-14 → `tests/test_doc_sync_no_run.py`; 绑定名 `NotFoundVerdictTests.test_trigger_matched_message`) |
| 12 | A1-m1/m2/m3/m6/m7 · A5-m1/m3 | schema 偏离 (parent 字段 — 沿 #179 先例保留; estimated_hours int 沿先例; A.3 reason 缺) / 估时 <4h 未声明 / exec_order 与并行互斥读法 / Rule #10 off 检查点留痕 / runtime_probe 14d 时窗 / main-loop 非表内 agent / 缺 execution_order·agent_summary | agent_reason 逐任务 / estimation_note + tdd_note / exec_order_note / audit_checkpoints_note / TASK-016 时窗条款 / agent_summary.note / execution_order + agent_summary 段 |

## 席位实测亮点

- A1: `spec_complete.py` 实跑 skipped vs completed 两态; 六早退点在 9e6a17c 已全存在 (守卫可前移); `git describe` 无 v1.66.4 tag。
- A2: TASK-003/007/009 行号/签名逐字核; `.replace` 在 false 分支为 no-op (非 fail-open ⇒ Major 非 Critical)。
- A3: SC-1/2/4/6 基线实跑 (pending / green / wait+无 kind / 无 gate_error) 与 RED/GUARD 标注一致。
- A4: §5 20 行逐行承载; 版本 14 点行号全对; #152 评论已实发 (12:40Z)。
- A5: `main-loop` 在归档先例 17 次使用; `detailed_tasks.py` done 白名单实读。

## 收敛判定

R1 REVISE (5/5) → v2 落 12 簇 → R2。
