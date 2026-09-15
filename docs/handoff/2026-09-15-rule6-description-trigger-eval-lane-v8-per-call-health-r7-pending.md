---
track-id: rule6-description-change-trigger-eval-lane
owner-container: simonfish/bfe8285d
phase: A.1
status: active
updated-at: 2026-09-15T14:24:46Z
---

# Aria — Session Handoff (2026-09-15) — `10CG/Aria#211` Rule #6 description 维度: spec v8 + 场景 4b 逐调用健康检查实验 (v6a / v6b), post_spec R7 待跑

> **一句话**: `10CG/Aria#211` triage (confirmed / major / next-cycle, comment 23915) → 场景 4 基线实跑 → Level 2 spec `rule6-description-change-trigger-eval-lane` 过 post_spec R1–R6 未收敛; owner 09-15 两次裁定 (max_rounds 5→7 并收窄范围; R6 后「修 v8、跑 R7 当最后一次检查」+「D2 故障识别先做实验再重新设计」); 实验 v6a 暴露「任一调用不健康即作废」太严, 按重跑前锁定的修订预登记改为 v6b 并三组全部重跑; v8 已本地提交 (`15ab323`), **R7 未跑** —— 账号七日用量窗口 99% (21:00Z 重置), 跑 R7 前等 owner 定时机。
>
> **本段最该记住的**: (1) 编排器运行时行为一律以代码为准 —— v7 照搬 `layer-boundary-contract.md` 的「默认自动重试、反复告警」, R6 三席读代码判 major, 实际是不重试、默认不告警的静默终态 (已并入 memory `feedback_never_write_unverified_impossibility_claims`)。(2) 看到数据后改判定规则要可审计: v6b 写明修订理由、重跑前锁定 (hash + 时间)、A / B / C 全部重跑、并声明此后不再改。
>
> **Next session 入口**: 读本 doc §0 → `/aria:state-scanner` → §6。

---

## §0 入口 (新 session 优先读)

1. 本轨 claim `rule6-description-change-trigger-eval-lane-bfe8285d` (active, 本容器)。主仓 master 本地领先两端 12 个提交 (含本 handoff 自身的提交), **未推送**; 远端 master 仍为 `ca0d898`, 两端一致、无分叉。推送按多远程两条约束: 双推后逐个 `git ls-remote <remote> master` 核验。
2. spec v8 @ `15ab323`: `openspec/changes/rule6-description-change-trigger-eval-lane/proposal.md`。post_spec R1–R6 各席报告与聚合在 `.aria/audit-reports/` (R6 聚合末尾记 owner 裁定)。基线与实验在 `aria-plugin-benchmarks/ab-results/2026-09-13-rule6-description-trigger-eval-baseline/` (RESULT.md v7; `v6-per-call-health-opus5/` 根下是 v6b, `v6a/` 是原预登记那一批)。
3. 双子星 `simonfish/023236f2` 手上的 `10CG/Aria#195` / `10CG/Aria#199` (A.2) 本容器不碰。

---

## §1 已完成 (UTC)

| 时间 | 事件 | 证据 |
|---|---|---|
| 09-13 | aria-plugin v1.73.3 发版, `10CG/aria-plugin#196` 关闭 | 上一份 handoff `ca0d898` (已双推) |
| 09-13 | `10CG/Aria#211` triage: confirmed / major / next-cycle, 回帖 comment 23915 | `a154a51` (triage 文件) |
| 09-13 | 场景 4 基线 v1–v4; spec v1; post_spec R1 FAIL 1C / 14M | `298d0e4` |
| 09-14 | v2–v6 与 R2–R5 (major 10 → 5 → 3 → 6), max_rounds 5 耗尽未收敛 | `55bc9f3` `0c41e53` `e822829` `f169a0b` `3b2215e` |
| 09-15 | owner 裁定加 2 轮并先收窄自主模式 → v7; R6: 6 键 5 问题, 0C | `c3a5903` / `cc0af1f` |
| 09-15 | owner 裁定: 修 v8 跑 R7 当最后一次检查; D2 故障识别先实验再重设计 | R6 聚合末尾 |
| 09-15 13:09Z | v6a 预登记锁定 → 故障矩阵 17/17、真实报错探针符合; 真实两臂负控 2 次 API 重试风暴 (真故障) | `v6a/` |
| 09-15 13:51Z | v6b 修订预登记锁定 → 故障矩阵 24/24、反事实 5 例转红、探针符合; 安全点提交 | `76959c8` |
| 09-15 | v6b 真实两臂: 被评臂 pass、负控臂 valid, 两臂 120 次调用全部健康 (11m33s / 12m13s) | `real/` |
| 09-15 | spec v8 + RESULT v7 | `15ab323` |

---

## §2 AI 流程判断 (Rule #10, 请 owner 复议)

1. **预登记之后修订判定规则 (v6b)**: 理由是 v6a 真实两臂里 2/120 次调用撞上 API 重试风暴 (逐条核实是真故障、非误报), 按「任一不健康即作废」一轮全部健康的概率约 13%, 规则不可用。修订在重跑前写定并锁定, A / B / C 全部重跑, 并写明此后不再修订。
2. 真实调用用 `claude-opus-5` (与 v5 同; Fable 额度耗尽后本 session 改用 Opus 5)。真实 `claude -p` 调用累计约 240 次 (两批全量两臂) 加少量探针, 在原预登记的成本上限边上。
3. 新增 OQ-9 (新增 skill 算不算「description 变动」), v8 按推荐「算」起草, 待 owner 裁。
4. 七日用量 99% 时先做本地安全点提交 (`76959c8`), 再跑真实调用; 未推送。
5. R6 聚合去重沿 R2 口径: backend-architect 的 architecture/§Impact+§D5.6 与 documentation 同题, 单独计键并交叉注明 (6 键 5 问题)。
6. 沿用未决项: 20 条 query 未经 owner 审阅 (OQ-3); Level 2 与 LEVEL_GUIDE 跨模块规则的关系 (OQ-4)。

---

## §3 关键事实 (均按代码或数据核实)

- runner `initial.sh` Step 10 会把工作区里未提交的改动 `git add -A` 后代为提交; changes / redo 模式有 diff 且推送成功即 PASS。runner 提示词却要求「不要带着半成品提交」。
- `container_crash` 不在可重试集合; tick 标 S_FAIL 不告警; 失败分析默认关闭 (`ARIA_FAILURE_ANALYSIS_ENABLED` 无部署配置设置); `fail_detail` 只有退出码与 alloc id。`layer-boundary-contract.md` §S_FAIL handling 与代码不一致。
- 编排器代码与作业定义里 `unattended` 零命中, `.aria/config.json` 的 coordination 只有 `enabled` / `mode` ⇒ `10CG/Aria#196` 修好前自主禁令在 runner 里不会触发。
- skill-creator `run_eval.py`: 报错 / 超时 / 非零退出都记成「未触发」, 看到第一个判定事件就 kill 进程; 输出流里没有 query 原文 (所以 v6b 垫片另存)。
- 账号七日用量窗口 utilization 0.99、status allowed_warning, 21:00Z 重置 (输出流 rate_limit_event, 09-15 13:5x 读到)。

---

## §4 未推送与待办

- 主仓 12 个本地提交 (含本 handoff 自身的提交)待双推 (逐个 ls-remote 核验)。
- R7 (5 席, 并发 3; 本 session 的派发提示词草稿在 scratchpad, 会话结束即不可用 —— 新 session 按 R6 提示词结构重建, 要点: 对账 R6 五个问题; 各席重跑 `fault_matrix.py`; tech-lead 席判断 v6b 事后修订是否正当; qa 席对检查脚本做对抗测试)。
- R7 后: 若无 major, 由 owner 选「接受当前结论」; 然后 OQ-1–OQ-9 裁定 → Phase B (T0–T8, 含 T2b 工具搬入 `aria-plugin-benchmarks/tools/trigger-eval/`)。
- T6: 开三张 issue (D5.2 / D5.3 / D5.6) + 上游反馈 (渠道待 owner 定)。

---

## §6 Next

1. owner 定 R7 时机: 现在跑 (可能撞七日上限, 撞上则本账号所有调用停到 21:00Z) 或 21:00Z 重置后跑。
2. 跑 R7 → 聚合 → 如实报 owner。
3. 按 owner 裁定进 OQ 裁定与 Phase B。
