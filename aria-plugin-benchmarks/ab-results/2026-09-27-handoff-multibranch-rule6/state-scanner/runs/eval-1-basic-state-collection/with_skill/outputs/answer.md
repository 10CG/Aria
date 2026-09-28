# 项目状态扫描 (state-scanner)

scan.py 已跑完：退出码 0，`errors[]` 为空，snapshot 版本 `1.0`，通过入口检查。
中断检测：`interrupt.status = none`。git 中间态：`operation = none`，没有冲突。

## 1. 当前状态
- 分支：`feature/handoff-multibranch-subdir-path-fidelity`（这是 `10CG/Aria#195` 的分支），HEAD = `4f91772`
- 模块 / Phase·Cycle：本仓没有运行时 UPM（`upm.configured=false`），所以不显示
- 变更：3 项，都不是代码
  - `aria`：子模块检出在 feature `b181678`，主仓记录的指针仍是 `1cb3872`
  - `standards`：子模块检出在 feature `d86fc91`，主仓记录的指针仍是 `940cb5b`
  - 未跟踪目录：`aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/`
- 关联 OpenSpec：`handoff-multibranch-subdir-path-fidelity`（approved，现处 Phase B 组 5）
- **本会话环境**：`ARIA_COORDINATION_NO_PUSH=1`，说明这就是上一份 handoff 说的「TASK-026 AB 会话」
- **交接文档**：scan 通过 pointer 读到的是 `2026-09-24-session-close-199-post-planning-converged.md`（60.1h 前，via pointer）。**但这份已经过时**。本 feature 分支的 `docs/handoff/` 没有合进 master 上后来提交的交接文档。`tracks_multibranch` 在 `master` 上找到了本轨更新的三份：`2026-09-25-195-b1-and-group2-red-to-green.md`（active, phase B）、`2026-09-26-session-close-195-group3-group4-complete.md`、`2026-09-27-session-close-195-task025-legacy-issue-204.md`（最新，13:07Z）。origin/master 上的 `latest.md` 也指向 09-27 这份。**下面的推荐以 09-27 这份为准。**
- 跨 worktree：只有 1 个 worktree，`global_latest_elsewhere = null`

## 2. 变更分析
- 类型：其他 3 项（2 个子模块指针偏移 + 1 个未跟踪的 AB 结果目录）。没有代码、测试或文档变更
- 复杂度：Level 2
- 架构影响：无
- 测试覆盖：本次变更里没有测试文件
- Skill 变更检测：主仓里没检出 SKILL.md 变更（`skill_changes.detected=false`）。原因是 state-scanner 的改动在 aria 子模块 feature `b181678` 里，不在主仓 diff 中。**按 Rule #6，这些改动发版前必须过 AB**，这正是本轨 TASK-026 要做的事

## 3. 需求状态
- 配置状态：已配置
- PRD：
  - `prd-aria-v1.md`：Active
  - `prd-aria-v2.md`：原文是「Approved (Draft → Approved 2026-04-11 …)」，但被归成了 `pending`。这是已知的误判，见 `10CG/aria-plugin#198`，实际状态是 Approved
- User Stories：21 个。done 17 / in_progress 2（US-007、US-026）/ approved 1（US-028）/ pending 1（US-003）
- 优先项（`priority_items`）：US-026（M6，Spec #2 和 #4 还没做）、US-007、US-003

## 4. 架构状态
- System Architecture：存在
- 路径：`docs/architecture/system-architecture.md`
- 状态：Active；最后更新 2026-09-02
- 需求链路：完整（引用了 `prd-aria-v1.md` 和 `prd-aria-v2.md`）

## 5. OpenSpec 状态
- 活跃变更：8 个，全部 approved
  - `handoff-multibranch-subdir-path-fidelity`（`10CG/Aria#195`，本分支，Phase B 组 5）
  - `pre-merge-completeness-gate-change-scope`（`10CG/Aria#199`，A.2 已收敛，要等 #195 完成 C.2 才能开始 B.1）
  - 另外 6 个是 M6/M7：`aria-2.0-m6-cost-model-telemetry` / `-dispatch-input-delivery` / `-e2e-resilience` / `-release-closeout`，`aria-2.0-m7-agent-lifecycle` / `-fleet-aggregation`
- 已归档：146 个
- 待归档：0 个
- 设计完成但没实施：5 个（都已设计定稿、实施没做，**不要当成已完成**）
  - `aria-2.0-m6-release-closeout`：41/41 任务没勾，已放 124 天
  - `aria-2.0-m7-agent-lifecycle`：18/18 没勾，100 天
  - `aria-2.0-m6-cost-model-telemetry`：25/38 没勾，79 天
  - `aria-2.0-m6-e2e-resilience`：25/40 没勾，77 天
  - `aria-2.0-m7-fleet-aggregation`：20/20 没勾，70 天
  - 这 5 个都卡在 M6 的 owner/基建门上（Luxeno 延迟、168h 运营跑），不是遗漏

## 6. 审计状态
- 审计系统：已启用
- 上次审计：`post_planning` R7 —— PASS，已收敛（2026-09-24，`10CG/Aria#199`；报告 `.aria/audit-reports/post_planning-R7-2026-09-24T121027-000Z-pre-merge-completeness-gate-change-scope-aggregated.md`）
- 没有未收敛的审计

## 7. 自定义检查
- 16/16 全部通过，0 失败，0 跳过
- 通过的检查包括：版本徽章、CLAUDE.md 版本、i18n README、插件缓存（installed=1.73.3=sot）、主项目版本 1.7.5 共 9 处一致、应用级 token 活性、协调闸近期调用（3 次）、`no-unresolved-version-placeholder` 等

## 8. 同步状态
- 当前分支：没配置 upstream（`no_upstream`），所以 ahead/behind 是空的
- 多远程 parity：**`overall_parity = true`**（`github` 和 `origin` 都在 1 分钟前刚 fetch，证据等级 fresh）
  - 主仓 feature：本地 `4f91772` = github = origin
  - `aria` feature：`b181678`，两端都一致
  - `standards` feature：`d86fc91`，两端都一致
  - `aria-orchestrator` master：`237045a`，两端都一致
  - 子模块指针可达性：6/6 为 ok
- 子模块偏移：`aria` 和 `standards` 的 `workdir_vs_tree=true`（检出的提交 ≠ 指针）。这是 handoff 写明的**正常中间态**：指针 bump 归 TASK-030/031，**不要 `git add aria standards`**
- 协调 ref：fetch 成功，本地 `e911132`；本轨两条 claim 都是 active
  - `s-48ca@0612`（#195，phase B）：心跳 `2026-09-27T12:35:55Z`，约 4.4h 前
  - `s-73b9@1606`（#199，phase A.2）：心跳 `12:36:25Z`，约 4.4h 前
- README 版本：aria plugin.json 1.73.3 = README 1.73.3，一致
- 插件依赖：standards 子模块已注册、已初始化
- Forgejo 配置：检测到 Forgejo 远程（`forgejo.10cg.pub`），但缺 `CLAUDE.local.md`。建议：运行 `/forgejo-sync` 可以引导创建（要你确认才做）
- 多分支碰撞提示（`tracks_multibranch.collision.kind = self_multi_container`）：身份键 `023236f2` 和 `bfe8285d` 各自同时出现在 `simonfish` 和 `aria-runner-bot` 两个 owner 名下。只是提示，不阻断

## 9. Open Issues
- 49 个 open（来自 cache，fetched 16:54Z），分 4 个仓：10CG/Aria、10CG/aria-plugin、10CG/aria-standards、10CG/aria-orchestrator；有 `bug` label 的 4 个
- 和本轨 / 当前工作直接相关的：
  - `10CG/aria-plugin#204`：state-scanner 读 handoff 时仍按扁平布局处理（本轨 TASK-025 开的遗留缺口单）
  - `10CG/Aria#218` [bug]：没有指针时按 mtime 判断哪份 handoff 最新，rebase/checkout 后会指错。本次 pointer 过时属于同一族现象
  - `10CG/aria-plugin#202`：`phase1_gate` 的 self-resume 按 (container, session) 匹配，同一容器换 session 后会新建第二条 claim
  - `10CG/Aria#199` [bug]：pre_merge 完整性闸少了 `change_id` 维度（并发轨）
- 其他 bug：`10CG/Aria#221`（secret-guard 通过进程表可以绕过）、`10CG/Aria#217`（session-closer 的 stdout 随 OS locale 变化）
- 没有 blocker/critical label

## 10. 推荐工作流

先说一件事：按 SKILL.md，入口本来要为持有的 active claim 调一次心跳。命令如下：
```
python3 /home/dev/Aria/aria/skills/state-scanner/scripts/phase1_gate.py \
  --heartbeat-only --raw-track-id "handoff-multibranch-subdir-path-fidelity" --phase B --repo-path /home/dev/Aria
```
**这次没有执行。** 原因有两个：
- 本会话带着 `ARIA_COORDINATION_NO_PUSH=1`。09-27 handoff §3 风险 1 明确说：AB 会话里不要刷心跳，也不要跑 `phase1_gate`。在这里写协调 ref 推不出去，会让本地领先 origin，直接破坏 TASK-026 第 1 条的前提
- 两条 claim 的心跳离现在约 4.4h，离 24h 回收阈值还远。AB 结束后的第一个普通会话，最晚要在 **2026-09-28 12:35Z** 前刷新

**[1] 继续 `10CG/Aria#195` TASK-026：Rule #6 AB（推荐）**
- 执行：B.2（benchmark，用 `/skill-creator`），在当前 feature 分支上做
  - (1) 核对 `git ls-remote origin refs/aria/coordination` 是否等于本地 `e911132`，不相等就不开跑
  - (2) 在子进程里实测 `no_push_requested_by_env()` 返回 True
  - (3) with 臂 = aria `b181678`；old 臂 = 基线 `1cb3872`，用一次性 worktree，建在 scratchpad
  - (4) 按 `detailed-tasks.yaml` 里 TASK-026 的 verification 逐条走完
  - (5) 最后执行 `git fetch origin +refs/aria/coordination:refs/aria/coordination` 强制对齐，然后退出这个进程
- 跳过：A.*（Spec 已批、计划已锁）、C.*（TASK-027~031 要在 AB 之后、不带该变量的新会话里做）
- 理由：09-27 handoff 定的下一步就是 TASK-026，本会话的环境变量也正是为它准备的。未跟踪的 `2026-09-27-handoff-multibranch-rule6/` 说明 AB 可能已经开始，请先看这个目录里有什么，再决定续跑还是重跑
- 会碰到的 owner 点：要不要授权发 AB 套件缺口 issue（`owner_gates` 第 5 项）；如果 delta ≤ 0 或回归面无效，要先请 owner 裁定，再进 TASK-027（第 6 项）

**[2] 只看不动：确认交接和并发轨状态**
- 执行：读 origin/master 上的 `docs/handoff/2026-09-27-session-close-195-task025-legacy-issue-204.md` 和决策单 `.aria/decisions/2026-09-27-195-199-owner-rulings-pending-items.md`。这个会话不做任何写操作
- 理由：适合你只想先对齐上下文、这次不打算跑 AB 的情况

**[3] 退出本会话，开一个普通会话（不带 `ARIA_COORDINATION_NO_PUSH`）**
- 执行：刷两条 claim 心跳 → 处理别的事（比如 `10CG/Aria#199` 的 v2.7 返修输入整理、`/forgejo-sync` 补 `CLAUDE.local.md`）
- 理由：如果今天不打算跑 AB，这个带变量的会话不适合做任何需要推协调 ref 的事
- 代价：TASK-026 往后推；而且 `#199` 的 B.1 要等 `#195` 完成 C.2，所以也跟着往后推

**[4] 自定义组合**
- 输入格式："B.2 + C.1" 或 "Phase B"

请选 [1-4]，或输入自定义组合。

不要做的：
- 不要 `git add aria standards`（指针 bump 归 TASK-030/031）
- 不要对本轨再跑认领闸（会新建第二条 claim，见 `10CG/aria-plugin#202`）
- 不要勾 `tasks.md` 的 checkbox（统一在 Phase D 的 TASK-032 做）
- 提交不加 `Co-Authored-By: Claude`（owner 2026-09-27 裁定）
