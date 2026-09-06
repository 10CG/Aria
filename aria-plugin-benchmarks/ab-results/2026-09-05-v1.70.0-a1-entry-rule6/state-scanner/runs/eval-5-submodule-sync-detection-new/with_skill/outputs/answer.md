已跑完 Step 0 机械扫描 (`scan.py --output .aria/state-snapshot.json`, **exit 0 / `errors[]` 为空**, schema 1.0), 下面是基于 snapshot 的完整状态与结论。

---

## ✅ 直接回答: **不需要 `git submodule update`, 而且现在跑它会造成损失**

三个子模块**没有一个落后远程**。三条判据全部指向同一结论:

- `sync_status.submodules[].drift.tree_vs_remote` = **false** (3/3) — 主仓记录的 gitlink 与子模块远程默认分支**逐字相同**
- `behind_count` = **0**, `ahead_count` = **0** (3/3), `hint` = **null**, `hint_type` = **null** — 推荐规则 `submodule_drift` (priority 1.97) 的触发条件 `任一子模块 tree_vs_remote == true` **未满足**, 未触发
- `sync_status.multi_remote.overall_parity` = **true**, `gitlink_integrity[]` **6/6 = ok** (2 remote × 3 子模块, 零 `orphaned` / 零 `orphan_unverified`)

你现在 `git status` 看到的 ` M aria` / ` M standards` / ` M aria-orchestrator` 三个 dirty 子模块, **不是"落后远程"**, 而是另一个正交维度: `workdir_vs_tree = true` (3/3) —— 本地 checkout 的子模块 HEAD 与主仓 gitlink 不同, 因为三个子模块被**有意**切到了 feature 分支上。

```
                  workdir HEAD (你 checkout 的)   主仓 gitlink (tree)   远程默认分支 (remote)
standards         bb5d375  feature/a1-entry-…     cc864ee         ==    cc864ee
aria              ab3dbd0  feature/a1-entry-…     7dd0135         ==    7dd0135
aria-orchestrator 92acce5  feature/m6-cost-model… 237045a         ==    237045a
                  └── workdir_vs_tree = true      └────── tree_vs_remote = false (无落后)
```

**为什么现在跑是有害的**:

1. `git submodule update` (不带 `--remote`) = 把子模块工作区**重置到 gitlink 记录的 commit** 并进入 detached HEAD ⇒ 三个 feature 分支的 checkout 位置全部丢失 (分支 ref 还在, 但工作区离开分支; 未提交内容会被覆盖)。
2. `git submodule update --remote` = 拉远程 tracking 分支再移动 ⇒ 同样把你从 feature 分支上带走。
3. 真正意义上的"同步"这里无事可做: 三个子模块**当前分支**在各自远程上 `ahead=0 / behind=0`。

最新交接 `docs/handoff/2026-09-05-2200-…md` §0 第 1 条也逐字写着这三个 dirty 子模块「**全部有意**, 不要 `git add`」(gitlink bump 归 TASK-038/8.2, 要等各自合 master 之后)。

**关于"其他协作者推了 submodule 更新"**: 本轮证据是**新鲜**的, 不是陈旧缓存 —— Phase 0.5 `remote_refresh` 对 4 个仓 × 2 个 remote 共 **8 条 leg 全部 `fetch_ok=true`** (23:07:50–23:07:56Z, generation 107, `skipped_count=0`), 所有 remote 的 `evidence_grade` 均为 `fresh`。若真有协作者推了子模块更新, 它会表现为 `tree_vs_remote=true` + `behind_count>0` (并自动给出 `git submodule update --remote <path>` 的 hint), 或表现为主仓落后 upstream。**两者当前都为 0。**

---

```
╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝
```

## 📍 当前状态
```
  分支: feature/a1-entry-claim-duplicate-work-guard (与 origin 同名分支同步, ahead 0 / behind 0)
  模块: — (UPM 未配置)
  Phase/Cycle: UPM 未配置; workflow-state 显示上一 cycle (linked-issue-field-availability)
               status=completed @ D.4 2026-09-02 — 非中断态, 不提示 Resume
  变更: 4 项 (3 个 dirty 子模块 aria/standards/aria-orchestrator + 1 个 untracked 目录
        aria-plugin-benchmarks/ab-results/2026-09-05-v1.70.0-a1-entry-rule6/); 暂存区为空
  关联 OpenSpec: a1-entry-claim-duplicate-work-guard (approved, 进度 31/40)
  上次 handoff: 2026-09-05-2200-a1-entry-31of40-followups-and-resilient-push-defect.md
                (0.55h ago, via pointer) — 已读取, §6 入口指引已纳入下方推荐
```

## 📊 变更分析
```
  类型: other × 4 (code 0 / test 0 / docs 0 / config 0)
  复杂度: Level 2
  架构影响: 无
  测试覆盖: 无对应测试变更
  Skill 变更: 未检出 (skill_changes.detected=false) → 不触发 Rule #6 AB 区块
```

## 📄 需求状态
```
  配置状态: ✅ 已配置
  PRD: prd-aria-v1.md (Active) / prd-aria-v2.md (Approved → 归一 pending)
  User Stories: 21 个 (done 17, in_progress 2, approved 1, pending 1)
  优先项 (priority_items): US-026 (in_progress) / US-007 (in_progress) / US-003 (pending)
```

## 🏗️ 架构状态
```
  System Architecture: ✅ 存在
  路径: docs/architecture/system-architecture.md
  状态: Active | 最后更新: 2026-09-02
  需求链路: ✅ 完整 (parent PRDs: prd-aria-v1.md, prd-aria-v2.md)
```

## 📋 OpenSpec 状态
```
  活跃变更: 7 个 (approved: 7)
  已归档: 142 个
  待归档: 0 个
  设计未实施: ⚠️ 5 个 (design_deferred, 设计定稿但实施未做 — 勿误判完成)
    - aria-2.0-m6-release-closeout   (approved, 41/41 未勾, staleness 103d)
    - aria-2.0-m7-agent-lifecycle    (approved, 18/18 未勾, staleness 65d)
    - aria-2.0-m6-cost-model-telemetry (approved, 25/38 未勾, staleness 58d)
    - aria-2.0-m6-e2e-resilience     (approved, 25/40 未勾, staleness 55d)
    - aria-2.0-m7-fleet-aggregation  (approved, 20/20 未勾)
```

## 🛡️ 审计状态
```
  审计系统: ✅ 已启用 (convergence 模式, max_rounds=5)
  活跃检查点: post_spec, post_planning (其余 5 个 off)
  上次审计: ⚠️ pre_merge — PASS (**未收敛**, converged=false)
    时间: 2026-09-02T18:10:11Z
    报告: .aria/audit-reports/pre_merge-R5-2026-09-02T174050-955Z-linked-issue-field-availability-aggregated.md
  建议: 该报告属已归档的 linked-issue-field-availability cycle, 可查阅后接受结论或重触发
```

## 🔧 自定义检查
```
  ✅ 14/14 全部通过 (0 FAIL / 0 STALE)
  issue-cache-freshness / silknode-contract-deferral-expiry / m6-version-badge-match /
  m6-claude-md-version / m6-arch-doc-stale / i18n-readme-translation-currency /
  claude-md-changelog-free / coordination-gate-invocation / config-template-key-currency /
  plugin-cache-currency / main-project-version-consistency / forgejo-app-token-liveness /
  linked-issue-field-availability / plugin-version-arch-docs-match
```

## 🔄 同步状态
```
  当前分支: feature/a1-entry-claim-duplicate-work-guard
            (最新, 与 origin/feature/a1-entry-claim-duplicate-work-guard 同步 — ahead 0 / behind 0)
  远程引用: 本轮 Phase 0.5 remote_refresh 8/8 leg fetch 成功 (evidence_grade=fresh)
            (`remote_refs_age="1m"` 已 DEPRECATED — 它测的是本次 scan 自己刚做的 fetch, 不作陈旧度判据)
  子模块 (drift 检测, tree vs remote):
    ✅ standards:         同步 (gitlink cc864ee == 远程 cc864ee, behind 0 / ahead 0)
    ✅ aria:              同步 (gitlink 7dd0135 == 远程 7dd0135, behind 0 / ahead 0)
    ✅ aria-orchestrator: 同步 (gitlink 237045a == 远程 237045a, behind 0 / ahead 0)
  ℹ️ 三者 workdir_vs_tree=true — 本地 checkout 停在 feature 分支, 与 gitlink 不同。
     这是有意状态 (gitlink bump 归本 Spec 的 8.2), **不是落后**, 不要用 submodule update 去"修"它。
  📝 README 版本一致性: ✅ aria README 1.69.1 == plugin.json 1.69.1
  📦 插件依赖: ✅ standards 子模块已注册且已初始化
  🔗 Forgejo 配置检查: ⚠️ 检测到 Forgejo 远程 (forgejo.10cg.pub) 但缺少 CLAUDE.local.md 配置块
     建议: 运行 /forgejo-sync 可引导创建配置 (需确认) — 非阻塞
```

## 🌐 多远程一致性 (enforced_remotes: origin, github)
```
  ✅ 主仓库:              两远程一致 (origin=github=5d9b568, evidence_grade=fresh)
  ✅ standards 子模块:    两远程一致 (origin=github=bb5d375)
  ✅ aria 子模块:         两远程一致 (origin=github=ab3dbd0)
  ℹ️ aria-orchestrator:   origin=92acce5 equal; github parity=unknown
                          (reason=no_local_tracking_ref — 分支 feature/m6-cost-model-telemetry
                          尚未推到 github; evidence_grade=fresh ⇒ 良性 unknown,
                          既不触发 multi_remote_drift(1.35) 也不触发 has_unpublished_branch(1.36))
  ✅ gitlink 完整性: 6/6 (remote × 子模块) = ok — 零 orphaned / 零 orphan_unverified
  ⇒ overall_parity = true
```

## 🎫 Open Issues
```
  平台: Forgejo — open_count 47 (4 个仓聚合)
    10CG/Aria 20 · 10CG/aria-plugin 20 · 10CG/aria-standards 5 · 10CG/aria-orchestrator 2
  📌 #196 [Aria] [契约][aria-orchestrator] unattended 的 Layer 1→2 env 传递三腿契约未定义
  📌 #195 [Aria] state-scanner: handoff_multibranch 递归枚举但只留 basename  [bug]
  📌 #193 [Aria] 同容器 git 身份漂移产生双 owner-container 串 — collision 分类失效
  📌 #188 [Aria] 四维一致性检查恒假阳性 + UPM collector 认不到仓库根 UPM.md
  无 blocker/critical label (label_summary 仅 bug×1) ⇒ 不触发 open_blocker_issues(1.99) 降级
  数据来源: cache (fetched 23:04:18Z) | ttl 15m
  ⚠️ 计数存疑: Aria 与 aria-plugin **恰好各报 20 = config `limit=20` 上限**且无截断标记
     (上次交接 §2 M2 已记录同款静默截断: 报 46 vs 实拉 65)。47 应视为**下界**, 非真实总数。
```

## 🎯 推荐工作流

> 按 SKILL.md「handoff awareness mandatory」, 已读取最新 handoff (0.55h ago); 其 §6 入口优先级**高于**通用规则。命中的通用规则为 `resume_in_progress_us`(1.88) 与 `audit_unconverged`(1.9); `submodule_drift`(1.97) / `branch_behind_upstream`(1.98) / `multi_remote_drift`(1.35) / `custom_check_*` **均未触发**。

```
  ➤ [1] 续做 a1-entry-claim-duplicate-work-guard (推荐, 31/40)
        执行: (前置) Rule #6 AB → 7.6 (TASK-036) → Group 8 发版 8.1 → 8.4 → 8.2 (vNEXT=1.70.0)
        ⛔ 前置未解除: handoff §3 第 1 条 —— `ARIA_COORDINATION_NO_PUSH` 实测 UNSET, 且这是
           **会话级**前置, 会话内 export 补不上。需 owner 以
           `ARIA_COORDINATION_NO_PUSH=1 claude --resume` 重启会话后再经 /skill-creator 跑六套件。
        理由: 唯一在制 cycle, Spec approved, 剩余 9 条已逐条列明

    [2] 修 carry-issue-scan-open-count-truncation
        执行: A.1 (Level 2 Spec) → B.2 → C.1
        理由: 本轮再次实证 (见上方 🎫 区块告警) —— 与 #182/#173「证据越少越宽松」同族

    [3] 修 aria-plugin#169 resilient_push non-FF 恢复路径
        执行: B.1 → B.2 → C.1
        理由: 影响 acquire_claim + heartbeat 两条写路径, claim 可静默丢失; 已开单未修

    [4] 自定义组合 (输入格式: "B.2 + C.1" 或 "Phase B")
```

**两条本次未替你执行的操作** (均涉及写/推, 需你明确确认):

- **claim heartbeat**: 本容器持 active claim `a1-entry-claim-duplicate-work-guard`, 上次刷新 21:40:06Z, sweep 死线 **2026-09-06T21:40Z**。按 handoff §3 第 4 条, 正确顺序是**先 fetch 再刷**:
  ```bash
  git fetch origin '+refs/aria/coordination:refs/aria/coordination'
  python3 -B aria/skills/state-scanner/scripts/phase1_gate.py \
    --raw-track-id "a1-entry-claim-duplicate-work-guard" \
    --phase B --heartbeat-only --repo-path /home/dev/Aria
  ```
  顺序反了会被强制 fetch 冲掉 (2026-09-05 已实证冲掉过一次 heartbeat commit)。
- **phase1_gate 认领闸门**: `tracks_multibranch.collision.kind = self_multi_container`
  (groups: `dev-claude` / `simonfishgit/dev-claude`), `coordination.enabled=true` ⇒ 按契约,
  闸门在**你确认进入 Phase B 时**才由编排层调用, 不在只读扫描里自动跑。本次为只读扫描, 未调用。

🤔 选择 [1-4] 或输入自定义:
