## 项目状态 (scan.py exit 10: 部分软错误, snapshot 可用)

**📍 当前状态**
- 分支: `feature/linked-issue-normalization` (upstream origin 同名, ahead 0 / behind 0) — 注意: 不在 master
- 模块: UPM 未配置 (无 Phase/Cycle 机读锚)
- 变更文件: 2 (未暂存 `aria` gitlink 修改 + 未跟踪目录 `aria-plugin-benchmarks/ab-results/2026-08-23-v1.67.0-linked-issue-rule6/`)
- 关联 OpenSpec: `linked-issue-normalization` — Draft, owner 2026-08-23 裁定 override 进 Phase B.1 (Rule #10 留痕); aria 子模块已在同名分支上落 2 个 commit (`8f5f5bd` TASK-001..009 归一函数 + 谓词切换, `0fe2e0d` TASK-011/012 文档同步), 但 `tasks.md` 21 项全未勾 / `detailed-tasks.yaml` 28 项全 pending (6 项 cancelled) — 进度账目滞后于代码
- 无中断工作流 (interrupt=none), 无 rebase/merge 中间态

**📊 变更分析**
- 变更类型: other ×2 (gitlink + benchmark 产物) / 复杂度 Level 1 / 架构影响 无 / 测试覆盖 无
- ⚠️ 工作树 aria 子模块 HEAD `0fe2e0d` ≠ 主仓 gitlink `9e6a17c` (v1.66.4): gitlink 尚未 bump 提交; 且相对 origin/master 落后 15 commit 属分支正常状态

**📄 需求状态**: PRD v1 Active / PRD v2 Approved; User Stories 21 (done 17 / in_progress 2 / approved 1 / pending 1); 架构文档 Active (2026-05-27, 88 天, 检查仍 OK) 但 `chain_valid=false` (parent_prd 未链接)

**📋 OpenSpec 状态**: 活跃 9 (approved 7 / pending 2); 待归档 0
- ⚠️ 设计未实施 6 个: m6-cost-model-telemetry (44d) / m6-dispatch-input-delivery (49d) / m6-e2e-resilience (41d) / m6-release-closeout (89d) / m7-agent-lifecycle (65d) / m7-fleet-aggregation (34d) — 全部卡 owner/基建门 (Blocker 3/4), 非本轨可推
- 另一 pending: `a1-entry-claim-duplicate-work-guard` (C1/C2 已裁, 待 rework 后进 A.2)
- `pre-merge-gate-no-run-for-branch` (#152) Approved, post_planning CONVERGED 2026-08-23, B.1-done

**🛡️ 审计状态**: enabled; 最近审计轨 `linked-issue-normalization-audit-trail.md` (post_planning R5 FAIL 2C+7M → owner 裁 fix 后 override, 见轨 §10)

**🔧 自定义检查**: 10/10 ✅ (版本 badge 1.66.4 / i18n README / CLAUDE.md 卫生 151 行 / plugin cache 1.66.4 / config 键 / coordination gate 有 4 次生产调用 等)

**🔄 同步状态**
- 当前分支与 origin 一致 (fresh); github 无同名分支 (no_local_tracking_ref, 特性分支正常)
- 子模块: standards / aria-orchestrator 与远程一致; aria 在特性分支, origin 一致
- 多远程 overall_parity=true, 但 ⚠️ AC-5 自洽检测对 164 条 legacy track 报 "git command failed" (即 Aria #176 的已知假阳性, 退出码 10 的来源) — 本判决当作未验证即可, 不影响操作
- gitlink 完整性: origin 三子模块 ok; github 侧 `no_published_ref` (特性分支未推 github, 合并后 C.2.5 处理)
- 🔗 Forgejo 配置: `.aria/forgejo` 配置缺失 (可选, `/forgejo-sync` 引导)

**🎫 Open Issues**: 44 (10CG/Aria); 关键: #188 四维一致性假阳性 + UPM 认不到根 / #176 AC-5 假阳性 (本次扫描正中) / #177 ↔ `linked-issue-normalization` / #156 ↔ `pre-merge-gate-no-run-for-branch` / #180 heartbeat 零生产调用 / #182 handoff status 从不收口

**📝 Handoff 感知 (⚠️ 漂移)**
- 最新 handoff: `2026-08-22-issue152-phase-a-twelve-rounds-and-the-check-that-checks-itself.md` (8.9h 前, pointer 权威), 在飞轨 = `pre-merge-gate-no-run-for-branch` (#152, simonfish/023236f2, B.1-done, 下一步 TASK-004)
- 但当前分支属于 `linked-issue-normalization` 轨, **latest.md 的 track 表里没有这一行** → 两条在飞轨并存, handoff 未登记本轨
- 并发碰撞: `tracks_multibranch.collision.kind = self_multi_container` (dev-claude / aria-runner-bot 等同 owner 多容器), 进 Phase B 前应走 phase1_gate advisory claim
- 跨 worktree: 仅 1 个 worktree, 无异地 handoff

---

## 🎯 推荐工作流 (请选一项, 或自定义组合)

**[1] 继续 `linked-issue-normalization` Phase B → C (推荐, 置信 ~80%)**
- 现状判定: 代码侧 TASK-001..012 已在 aria 子模块落地, 正在做的 AB 基准 (本目录 `2026-08-23-v1.67.0-linked-issue-rule6/`) 对应 tasks.md 4.1 (Rule #6 对 SKILL.md:176 hunk 照跑)
- 步骤: 4.1 AB 出结论 → 5.1 全量回归 (`state-scanner/tests/run_tests.py`, 基线 1322) → 5.9/5.10 版本面 bump v1.67.0 (子模块 + 主仓 14 引用点) → 5.11 双向差集断言 → C.1 提交 (aria gitlink bump + AB 结果归档 + tasks.md 勾选补账) → 5.13 委派 phase-c-integrator 开 PR + pre-merge gate (不委派合并; 子模块合并一律本地 + 双推 + ls-remote 核验)
- 先做一件小事: `tasks.md` / `detailed-tasks.yaml` 把已完成的 001..012 勾掉 (进度账目与代码同步, Rule #3)
- 跳过: A.1-A.3 (已完成, owner override 留痕)

**[2] 先补本轨的协调登记, 再回到 [1]**
- 理由: latest.md 没有 `linked-issue-normalization` 行, collision=self_multi_container; #152 轨同时在飞 (同 owner 两容器)
- 步骤: `phase1_gate.py --raw-track-id linked-issue-normalization --phase B --mode advisory --linked-issue 10CG/Aria#177` 写 claim → 在 `docs/handoff/latest.md` track 表加一行 → 继续 [1]
- 代价: 约 10 分钟, 避免两轨同时 bump 版本 (#152 目标 v1.66.5 vs 本轨 v1.67.0, 发版顺序需对齐)

**[3] 切到 #152 轨 `pre-merge-gate-no-run-for-branch` 从 TASK-004 起**
- 理由: handoff pointer 指它, Phase A 12 轮双 CONVERGED, B 前置三项 done
- 前提: 先把本分支的 gitlink 修改 stash 或提交, 再 checkout 对应分支; 两轨版本号需先裁定先后 (v1.66.5 先于 v1.67.0)

**[4] 只处理 issue / 不推代码**
- 候选: #176 (AC-5 假阳性, 本次扫描退出码 10 的直接原因, 修了就恒绿) / #188 (UPM collector 认不到根 UPM.md, 解释了上面 "UPM 未配置") — 两者都是 state-scanner 自身缺陷, 适合 `/issue-triage` 起 Level 1-2
- 或 `/session-closer` 先把本轨写进 handoff 再停

回复编号 (如 `1`) 或写自定义组合 (如 "先 2 再 1"); 选定后我再交给 workflow-runner 执行 — 本次只出推荐, 不自动启动。
