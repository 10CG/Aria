---
track-id: pre-merge-gate-no-run-for-branch
owner-container: simonfish/023236f2
phase: B.1-done
status: active
updated-at: 2026-08-22T20:50:00Z
---

# Session Handoff (2026-08-22) — #152 Phase A 十二轮 + B 三前置: 审计抓到的是「检查自身」

> **一句话**: `/state-scanner` → owner 裁 aria-plugin#152 修法 A′ → Level 2 spec 走完 Phase A (post_spec 7 轮 / post_planning 5 轮, 共三次 owner 加轮, 全部 CONVERGED) → Phase B 前置三项 done (claim / 两仓分支 / dispatch 探针)。会话收尾 (session-closer, leaf), 上下文 76% 时停。
>
> ⭐ **这段对话最该留下的一件事**: 十二轮里 Critical→0 之后的 Major 几乎全是**上一轮为了修 Major 而新写的检查本身**不成立 (恒红 / 恒真 / 管道 exec 必崩 / worktree 里没有新测试 = 伪红) 或「处置表说改了、机检字段没改」(exec_order 四席命中)。对策已落成习惯: **每条新检查先在基线亲跑三态再写进规格 + 处置落盘后跑程序化断言**。新 memory `feedback_new_mechanical_check_must_run_at_baseline_first`。

## §0 入口 (新 session 优先读)

- **本轨**: `pre-merge-gate-no-run-for-branch` (aria-plugin#152), claim **active** (`s-a637@2033`, 未释放 — B 未完), owner-container `simonfish/023236f2`。
- **分支**: 主仓 `feature/152-no-run-for-branch` @ `b11d089` (origin 已推); aria `feature/152-no-run-for-branch` @ `e33d6a8` (origin 已推; 基线 `9e6a17c` = v1.66.4)。主仓 master 上的 A 产物: spec `4824d8a`, yaml `118563f` (双端 equal)。主仓工作树 aria gitlink 偏到 `e33d6a8` **有意未提交** (TASK-015 bump)。
- **下一步 = TASK-004** (守卫@基线, qa) 起, 按 `detailed-tasks.yaml` v5 两轨并行 (gate 轨 004→002→003→005→006→007a→007b ∥ helper 轨 008→009 / 010a→010), `dispatch_viable=true` ⇒ 条件组 007a/007b **执行**。
- **版本目标 v1.66.5** (v1.66.4 已被 #179 占用); TASK-015 须补打 v1.66.1@`3b97c35` 与 v1.66.4@`9e6a17c` 两个漏掉的 tag。
- **runtime_probe 时窗**: TASK-014 活体写 production 记录后 **14 天内**须完成 TASK-016 归档, 否则重跑活体。

## §1 已完成 (按时间顺序)

1. `/state-scanner` 推荐 → owner 选 [1] #152 → 三面 fetch (无撞车; bfe8285d 在 #179) → 实读 gate 代码 → AskUserQuestion 四档 (A′/A/B/C) → owner 裁 **A′ 显影+处方不放行**。
2. **A.1** spec v1→v7, post_spec 7 轮五席 convergence: Major 23→21→18→5→2→1→0; R2 识别「AI 自动执行处方」子设计是最大发生器 → **v3 设计收缩** (改 ~90s 提前交人 + gate 渲染处方命令), owner 复议接受; max_rounds 4→6→7 两次 owner 加轮; R7 5/5 PASS。主仓 `4824d8a` 双推。#152 评论 19598 (裁定 + spec 入口)。
3. 期间对方容器 ship **v1.66.4** (#179): ff + 触点 diff 为空复核, spec 版本目标改 v1.66.5。
4. **A.2/A.3** detailed-tasks.yaml v1→v5, post_planning 5 轮: Major 14→10→7→6→0; R1 C1 = `skipped` 不在归档门白名单; R2 = 「声称≠字段」+ 断链; R3/R4 = 新写检查自身不成立; owner 加轮 4→5; R5 5/5 PASS。主仓 `118563f` 双推。
5. **B 前置**: TASK-000 phase1_gate claim passed/push_success/overlap []; TASK-000b 两仓分支; TASK-001 dispatch 探针 → `dispatch_viable=true` (HTTP 204, 2s 建 run) + traps §六 建节 + memory 勘正; 主仓 `b11d089` / aria `e33d6a8` 推 origin feature 分支。
6. Memory: 新 1 (check-runs-at-baseline-first) + 追记 2 (marginal-return 切除发生器 / scoped-add yaml 层同形) + 勘正 1 (forgejo dispatch 可用·盲区未复现)。

## §2 未完成 / Carry-forward 清单 (AI 内省, load-bearing)

- 🔴 **#152 盲区没有复现** (TASK-001 副产品): master tip 起新分支 + path-matched 首推, push run **正常建立** (31967, 13s)。与 #152 现场差异条件未定 (runner 忙闲 / commit 数 / before=0000 的 diff 基准)。spec Why F3 已降级为「观测一次, 条件未定」; 机制对零 run 任一来源仍成立。**请 owner 知悉**: 问题陈述比立案时弱, 但 mid_post_spec 闸门 config off, 我以 append-only 追记处理而非重开审计 (Rule #10 留痕请复议)。
- 🟡 **dispatch 成对 run 同 `started_at`** (31968 success / 31969 failure): gate `_normalize_pr_ci_status` 取最近 run 时 tie ⇒ 处方 (a) 后可能读到 failure。须在 TASK-007b 渲染文案 + §3.3 (a) 行提示; 若要机制化 (tie 时按 run id / 全部 success 才 passing) 属 scope 外, 建议 Phase D 立案。
- 🟡 **Phase B 全量 17 任务 ≈46h 未做** (TASK-004…016); 前置已清, 从 TASK-004 起。
- 🟡 **§6 Phase D 待办**: #152 收尾留言 / (b) 轴另案 issue / #127 追加 NEG-4 评论 (TASK-012)。
- 🟡 **v1.66.1 / v1.66.4 tag 漏打** (对方 ship 未打; A4 实核两 remote 均无) → TASK-015。
- 🟡 post_spec R4 聚合表一处笔误 (A3-m1→A3-M1) 已在 R5 聚合 erratum; post_spec 聚合 R1-R7 frontmatter 后补 `verdict:` 标量 (collector 读 map 为 None) — 机械已绿。
- ⏸️ 承前: aria-orchestrator 工作树停 `feature/m6-cost-model-telemetry@92acce5` 有意排除; M6 三门; backlog (#138/#180/#182/#154)。

**机械补漏 (autofill 交叉核验)**: `unfinished` 197 条中本轨 17 条 = yaml 里 pending 的 17 任务, 与上文「Phase B 全量未做」一致, 零额外补漏; `consistency_check` 9 flags 全 `active_change_not_in_upm` (Aria 无 UPM, 恒亮); `sync` 零告警 (feature 分支 origin=equal; github=unknown 属 feature 分支无镜像, 非分叉); scan exit 10 = AC-5 在 feature 分支对 github 不可评 (#176 形状)。

## §3 关键风险 / 已知陷阱

- 两容器并发: bfe8285d 本日同时收尾 (`a355943`); 开工前仍须三面 fetch + 查 #152 有无别 track (本 session 零撞车, 但对方 ship 了 v1.66.4 — 版本号被占是真实发生的)。
- 主仓 master 与 feature 分支并存: A 产物在 master, B 前置在 feature; TASK-015 (ii) 把主仓 5 类改动随 feature 分支 PR/merge 一起落, 不要在 master 上直改。
- `gate_state_helper.py` 运行时零消费方 (F7) — 本 spec 第一次接 CLI; `runtime_probe:` 首个采用者 — D.2 归档门若有未覆盖缺陷会在本 spec 暴露 (R-f)。

## §4 实战教训 (memory 沉淀来源)

```
[候选 memory] — 本 session 已写
- feedback_new_mechanical_check_must_run_at_baseline_first (新): 新写的 grep 负控/计数/管道 exec/worktree 回退必须先在基线亲跑三态 (基线/目标/坏实现) 再写进规格; R3/R4 全部 Major 都是检查自身恒红·恒真·必崩·伪红
- feedback_audit_marginal_return_goes_negative (追记): 拐点的另一处置 = 切除发生器子设计 (自动写动作 15-19/44 Major) 而非缩小编辑面; 判据 = 连续两轮最大单一来源且不在 owner 裁定字面内 ⇒ 切除并复议
- feedback_scoped_git_add_splits_claim_from_landing (追记): yaml 层同形 — 处置表「exec_order 前移」只改散文没改字段 (四席命中) / 换依赖边切断传递链; 对策 = 处置落盘后跑程序化断言 (拓扑/闭包/双向一致/求和)
- reference_forgejo_new_branch_paths_filter_no_run (勘正): dispatch API 在 gitea-1.22 可用 (HTTP 204, 按文件名寻址, 成对 run); #152 盲区 2026-08-22 探针未复现, 恒中口径降级
[未写下经验]
- 「max_rounds 耗尽 → owner 加轮 → 下一轮全票」本 session 三次重复 (4→6→7 / 4→5); owner 偏好形式全票而非 override。未写成 memory: 可能是 owner 偏好 (user 类), 两次以上再定
- 四元组收敛判定在「每轮唯一 Major 是上轮 fix 副产品」形态下实际靠 owner 加轮终结; audit-engine 的 oscillation/收敛公式对这种「单调递减到 1 再到 0」形态没有专门出口 — 可能是 audit-engine 的改进点 (先观察)
```

## §5 多维度同步状态 (机械 + 人工)

| 维 | 状态 |
|---|---|
| UPM | 无 (Aria 不配置), 9 flag 恒亮 |
| OpenSpec | 活跃 9; 本轨 `pre-merge-gate-no-run-for-branch` = Approved (post_spec+post_planning 双 CONVERGED), yaml 3/20 done; pending_archive 0 (#179 已归档) |
| User Story | 21 (done 17 / in_progress 2 / approved 1 / pending 1), 本轨无 US 变动 |
| PRD | 无变动 |

## §6 Next session 入口 + 优先级建议

入口: `/aria:state-scanner` → 它会看到本轨 claim active + 本 handoff → 进 Phase B。**开工前**: fetch 三面 (master / coord ref / issue 板) + `git -C aria checkout feature/152-no-run-for-branch` 确认在分支上 (非 detached)。按 yaml: ① TASK-004 守卫@基线 (qa) → ② TASK-002 RED → ③ TASK-003 GREEN (INV-1 同 commit, 主控提交并跑 yaml 里 block scalar 的 `inv1` 四合取) … 两轨可并行派子 agent (subagent 不 commit, 主控统一提交; memory workflow-file-domain)。TASK-007a/b 执行 (dispatch_viable=true)。

## §7 提交清单 (commit hash + multi-remote parity)

```
[main master]   4824d8a (A.1) → 118563f (A.2) | origin==github (ls-remote 逐个核验)
[main feature]  feature/152-no-run-for-branch = b11d089 | origin=equal (github 不推 feature)
[aria feature]  feature/152-no-run-for-branch = e33d6a8 | origin=equal; 基线 9e6a17c (v1.66.4)
[aria master]   9e6a17c | origin==github (未动)
[standards]     334c609 (未动)
[coord ref]     claims/023236f2/s-a637@2033.yaml active (已 push)
[aria-orchestrator] feature/m6-cost-model-telemetry@92acce5 (有意排除, 承前)
本 handoff commit: 见 git log (master, 双推)
```

## §8 Memory entries this session (1 new + 2 追记 + 1 勘正)

- `feedback_new_mechanical_check_must_run_at_baseline_first.md` (新, 已入索引)
- `feedback_audit_marginal_return_goes_negative.md` (追记 2026-08-22)
- `feedback_scoped_git_add_splits_claim_from_landing.md` (追记 2026-08-23)
- `reference_forgejo_new_branch_paths_filter_no_run.md` (勘正 + 索引 hook 改)

## Cross-references

- Spec: `openspec/changes/pre-merge-gate-no-run-for-branch/{proposal.md,detailed-tasks.yaml}` · 审计 `.aria/audit-reports/post_spec-R{1..7}-1787379154696-*` / `post_planning-R{1..5}-1787403030672-*`
- Issue: aria-plugin#152 (评论 19598) · #127 (NEG-4 缺口, TASK-012) · Aria#177 (版本引用点口径)
- 并发轨: [2026-08-22 bfe8285d 会话收尾](./2026-08-22-session-close-179-full-cycle-and-147-supersession.md) · 前序本容器收尾 [2026-08-22 credential-defense](./2026-08-22-session-close-credential-defense-and-mirror-collisions.md)
- traps §六: `aria/skills/phase-c-integrator/references/pre-merge-gate-empirical-traps.md` (feature 分支 e33d6a8)
