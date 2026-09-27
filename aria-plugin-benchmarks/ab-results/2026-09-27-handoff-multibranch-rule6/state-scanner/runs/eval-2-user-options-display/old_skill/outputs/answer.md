scan.py 已跑完 (退出码 0, `errors[]` 为空, snapshot schema `1.0`)。下面是按 state-scanner 格式整理的状态和可选操作。

```
╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝
```

**先说一件要紧的: handoff 视图落后了。** snapshot 的 `handoff.latest_path` 指向 `2026-09-24-session-close-199-post-planning-converged.md` (60.2h 前, 来源 pointer)。原因是当前在 feature 分支上, 这个工作树里的 `latest.md` 是旧的。`origin/master` 上的 `latest.md` 已经指向 **`2026-09-27-session-close-195-task025-legacy-issue-204.md`** (09-27 13:07Z)。下面的推荐以 master 上这份最新 handoff 的 §0 / §6 为准, 我是用 `git show origin/master:...` 读的, 没有切分支。

---

### 📍 当前状态
- 分支: `feature/handoff-multibranch-subdir-path-fidelity` @ `4f91772` (比 master 多 13 个提交; `origin/master` = `c454e35`)
- 模块 / Phase·Cycle: UPM 未配置 (`upm.configured=false`, 本仓没有运行时 UPM, 这是已知情况)
- 变更: 3 项, 都不是要提交的内容:
  - `M aria`: aria 在 feature `b181678`, gitlink 仍指 `1cb3872`
  - `M standards`: standards 在 feature `d86fc91`, gitlink 仍指 `940cb5b`
  - 未跟踪 `aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/`: TASK-026 的 AB 产物, 正在进行中
  - handoff 明确说这两处 `M` 是正常的中间态, gitlink 前进归 TASK-030 / TASK-031, **不要 `git add`**
- 关联 OpenSpec: `handoff-multibranch-subdir-path-fidelity` (approved, `10CG/Aria#195`, Phase B, 组 5 剩 TASK-026~032 + 034)
- 中断检测: `interrupt.status = none`; git 操作: `none` (没有暂停中的 rebase / merge)
- 上次 handoff:
  - 本树: `2026-09-24-...-converged.md` (60.2h 前, via pointer), 已落后
  - master: `2026-09-27-session-close-195-task025-legacy-issue-204.md`
- 进程环境: `ARIA_COORDINATION_NO_PUSH=1` 已设置, 说明这就是 handoff §6 所说的「AB 会话」

### 📊 变更分析
- 类型: other ×3 (两个子模块 gitlink + 一个未跟踪目录); 代码 / 测试 / 文档都是 0
- 复杂度: Level 2 (沿用活跃 Spec 的级别)
- 架构影响: 无
- 测试覆盖: 不适用 (工作区没有代码变更)

### 📄 需求状态
- 配置状态: ✅ 已配置
- PRD:
  - `prd-aria-v1.md`: Active
  - `prd-aria-v2.md`: 原文为 `Approved (Draft → Approved 2026-04-11 …)`, 但 collector 归一成了 pending。这是已知误判, 见 `10CG/aria-plugin#198`, 实际状态是 Approved
- User Stories: 21 个 (done 17 / in_progress 2 / approved 1 / pending 1)
- 优先项 (`priority_items`):
  - US-026 in_progress: M6 sub-Spec 收尾, 剩 Spec #2 + #4
  - US-007 in_progress
  - US-003 pending

### 🏗️ 架构状态
- System Architecture: ✅ 存在, 路径 `docs/architecture/system-architecture.md`
- 状态: Active, 最后更新 2026-09-02
- 需求链路: ✅ 完整 (PRD v1 + v2 → Architecture)

### 📋 OpenSpec 状态
- 活跃变更: 8 个 (全部 approved)
- 已归档: 146 个; 待归档: 0 个
- ⚠️ 设计未实施: 5 个

| id | status | staleness_days | 未勾任务 |
|---|---|---|---|
| aria-2.0-m6-release-closeout | approved | 124 | 41/41 |
| aria-2.0-m7-agent-lifecycle | approved | 100 | 18/18 |
| aria-2.0-m6-cost-model-telemetry | approved | 79 | 25/38 |
| aria-2.0-m6-e2e-resilience | approved | 77 | 25/40 |
| aria-2.0-m7-fleet-aggregation | approved | 70 | 20/20 |

  这几个都卡在 CLAUDE.md 记录的 M6 owner / 基建门上, 不是被遗忘了。

### 🛡️ 审计状态
- 审计系统: ✅ 已启用 (convergence 模式, `max_rounds` 5)
- 活跃检查点: post_spec, post_planning; 其余都是 off
- 上次审计: post_planning, 属于 `pre-merge-completeness-gate-change-scope`, 2026-09-24 R7, 结果 **PASS (已收敛)**
- 没有未收敛报告

### 🔧 自定义检查
16/16 全部通过 (✅ OK), 没有失败项。包括 `m6-version-badge-match` (1.73.3)、`plugin-cache-currency`、`main-project-version-consistency` (1.7.5)、`forgejo-app-token-liveness`、`coordination-gate-invocation`、`claude-md-changelog-free` (152 行) 等。

### 🔄 同步状态
- 当前分支: 没有配置 upstream (`no_upstream`), 所以 ahead / behind 无值
  - 多远程对比显示 `github` 和 `origin` 都是 `4f91772`, parity=equal, 证据 fresh, 说明这个分支已经双推了, 只是本地没设跟踪分支
- 多远程: ✅ `overall_parity = true`
  - 主仓和 standards / aria / aria-orchestrator 三个子模块在两端都一致, 证据都是 fresh, refs 1 分钟前刷新
- gitlink 完整性: 6 组 (2 remote × 3 子模块) 全部 `ok`
- 子模块漂移: `tree_vs_remote` 全为 false, 不触发 `submodule_drift`
  - aria 和 standards 的 `workdir_vs_tree=true` 就是上面说的 feature 中间态
- 📝 README: ✅ aria plugin 1.73.3 与 README 一致
- 📦 插件依赖: ✅ standards 子模块已注册、已初始化
- 🔗 Forgejo 配置检查: ⚠️ 检测到 Forgejo 远程 (forgejo.10cg.pub), 但缺少 `CLAUDE.local.md`。建议: 运行 /forgejo-sync 可引导创建配置 (需确认)
- 多终端 / 协调:
  - `tracks_multibranch.collision.kind = self_multi_container`
  - 同一身份的两个容器是 `simonfish/023236f2` 和 `simonfish/bfe8285d`
  - `coordination.enabled=true`, 所以不走 rule 1.54, 而是在进入 Phase B 时由 phase1_gate 处理
  - 协调 ref 拉取成功, 本地已有协调 ref
  - ⚪ 同机多身份说明 (信息级): identity `023236f2` 和 `bfe8285d` 都同时对应 `aria-runner-bot` 与 `simonfish` 两个 owner
- 本轨 claim (据 09-27 handoff):
  - `s-48ca@0612` (#195, phase B) 与 `s-73b9@1606` (#199, A.2) 都是 active
  - 心跳时间 09-27 12:35Z / 12:36Z, 按扫描时刻算约 4.4h, 离 24h 的 SWEEP_TTL 还远

### 🎫 Open Issues
- open 49 个 (来源 cache, 09-27 16:54Z 拉取)
  - `10CG/Aria` 20 个
  - `10CG/aria-plugin` 20 个
  - `10CG/aria-standards` 7 个
  - `10CG/aria-orchestrator` 2 个
- 没有 blocker / critical label, 不触发 `open_blocker_issues`
- 标了 `bug` 的有 4 个:
  - Aria#221: secret-guard 缺口, 可以通过列举进程绕过凭据保护
  - Aria#218: state-scanner 在没有 handoff 指针时按 mtime 判最新
  - Aria#217: session-closer 的 stdout 跟随 OS locale
  - Aria#199: pre_merge gate 缺 change_id 维度
- 与本轨直接相关: aria-plugin#204 (TASK-025 开出的遗留缺口单)、aria-plugin#202 (同容器换 session 再认领会新建第二条 claim)

### 🔬 Skill 变更 AB 状态
主仓工作区没有检出 SKILL.md 变更 (`skill_changes.detected=false`, 因为改动在子模块 feature 分支 `b181678` 上, 不在主仓 diff 里)。本轨 Rule #6 AB 就是 TASK-026, 未跟踪的 `ab-results/2026-09-27-handoff-multibranch-rule6/` 说明它正在进行。

---

### 🎯 推荐工作流

**给 AI 自己的约束:**
- **心跳**: 按 SKILL.md, 持有 active claim 的会话每次入口都要调:
  ```
  python3 ".../state-scanner/scripts/phase1_gate.py" --heartbeat-only --raw-track-id "handoff-multibranch-subdir-path-fidelity" --phase A.1 --repo-path "/home/dev/Aria"
  ```
  本次**没有执行**, 原因有两个:
  - 本评测禁止调用 phase1_gate
  - 09-27 handoff §6 明确说 AB 会话 (`ARIA_COORDINATION_NO_PUSH=1`) **跳过心跳**, 因为推不出去, 还会破坏 TASK-026 第 1 条
  
  AB 之后第一个普通会话**最晚 2026-09-28 12:35Z** 前要刷两条 claim 的心跳。
- **认领闸**: 本轨已经持有 claim `s-48ca@0612`, 所以不再对它跑 `phase1_gate --phase B` (会因为 aria-plugin#202 新建第二条 active claim), 续命只用 `--heartbeat-only`。

**可选操作:**

➤ **[1] feature-dev: 继续 #195 Phase B, 完成 TASK-026 Rule #6 AB (推荐)**
- 执行: B.2 (TASK-026, 按 verification 走完) → 第 3 步 `git fetch origin +refs/aria/coordination:refs/aria/coordination` 强制对齐 → 退出本 AB 进程
- 跳过: A.* (Spec 已 approved, post_planning 已收敛); 本会话内的心跳和认领闸 (原因见上)
- 理由:
  - 09-27 handoff §6 的第一优先级就是这一项
  - 当前进程带着 `NO_PUSH=1`, 正是为 TASK-026 准备的
  - 工作区里已经有进行中的 AB 产物
  - 本轨在 C.2 合并, 也就解开了 #199 的 B.1 入口门

○ **[2] AB 之后的普通会话: 刷心跳 → TASK-027 起**
- 执行: 新开一个不带 `NO_PUSH` 的会话 → 刷 `s-48ca@0612` 和 `s-73b9@1606` 两条心跳 (推后逐 remote 核验) → TASK-027 (并入 standards `session-handoff.md`, 升 1.4.0) → TASK-028~032 + 034 → C.1 → C.2
- 理由: 09-27 handoff §6 第 2 条和 owner 09-27「照建议」的裁定 (决策单 `.aria/decisions/2026-09-27-195-199-owner-rulings-pending-items.md`)
- 前提: 做完 [1] 之后才轮到它

○ **[3] 续做 in-progress User Story (resume_in_progress_us, 规则 1.88)**
- 对象: US-026 (M6 sub-Spec Spec #2 + #4) / US-007
- 理由: `priority_items` 里有 in_progress 项
- 注意: M6 各 Spec 都卡在 owner / 基建门上 (Blocker 3 / Blocker 4), 实际能推进的部分很少; 建议先看 `openspec/changes/aria-2.0-m6-*/proposal.md` 的门顺序

○ **[4] 自定义组合**
- 输入格式: `"B.2 + C.1"` 或 `"Phase B"`
- 可以附带这几件小事:
  - 运行 `/forgejo-sync` 补 `CLAUDE.local.md`
  - triage 4 个 `bug` issue, 尤其是 Aria#221 安全类
  - 给当前 feature 分支设 upstream (`git push -u`, 需 owner 授权推送)

🤔 选择 [1-4] 或输入自定义:

**不应该做的** (09-27 handoff 原文要点):
- `git add aria` / `git add standards` 或 bump gitlink
- 勾 `tasks.md` 的 checkbox
- 在 AB 会话里刷心跳或跑 phase1_gate
- 提交里加 `Co-Authored-By: Claude` 行 (owner 09-27 裁定)
