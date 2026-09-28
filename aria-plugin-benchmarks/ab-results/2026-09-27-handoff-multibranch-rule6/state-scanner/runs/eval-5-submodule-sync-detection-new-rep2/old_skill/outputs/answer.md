## 结论先说

**不需要 `git submodule update`。** 本次扫描在开头就对 3 个子模块、2 个远程 (origin = forgejo.10cg.pub, github) 实际 fetch 了一轮 (8 条 fetch 全部成功, 远程引用 1 分钟前刚刷新, 证据等级 `fresh`)，结果是：**3 个子模块没有一个落后远程**。

而且要提醒一句：在你当前的状态下执行 `git submodule update` **不但没用，还会把你拉离正在开发的分支** (细节见下方"为什么不要跑")。

---

```
╔══════════════════════════════════════════════════════════════╗
║                    PROJECT STATE ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════╝

📍 当前状态
───────────────────────────────────────────────────────────────
  分支: feature/handoff-multibranch-subdir-path-fidelity (HEAD 4f91772)
  模块: — (UPM 未配置)
  Phase/Cycle: — (UPM 未配置)
  变更: 3 处 (aria 与 standards 两个子模块指针有改动 + 1 个未跟踪目录
        aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/)
  git 中间态: 无 (没有暂停中的 rebase/merge 等)
  中断的工作流: 无
  上次 handoff: 2026-09-24-session-close-199-post-planning-converged.md
                (60.4h 前, via pointer)

📊 变更分析
───────────────────────────────────────────────────────────────
  类型: 其他 3 (子模块指针 ×2 + 未跟踪目录 ×1), 无代码/测试/文档文件
  复杂度: Level 2
  架构影响: 无
  测试覆盖: 不适用
  Skill 变更: 未检出

📄 需求状态
───────────────────────────────────────────────────────────────
  配置状态: ✅ 已配置
  PRD: prd-aria-v1.md (Active) / prd-aria-v2.md (Approved)
  User Stories: 21 个 (done: 17, in_progress: 2, approved: 1, pending: 1)

🏗️ 架构状态
───────────────────────────────────────────────────────────────
  System Architecture: ✅ 存在
  路径: docs/architecture/system-architecture.md
  状态: Active
  最后更新: 2026-09-02
  需求链路: ✅ PRD (v1 + v2) → Architecture 完整

📋 OpenSpec 状态
───────────────────────────────────────────────────────────────
  活跃变更: 8 个 (approved: 8)
  已归档: 146 个
  待归档: 0 个
  设计未实施: ⚠️ 5 个
    - aria-2.0-m6-release-closeout (approved, 124 天)
    - aria-2.0-m7-agent-lifecycle (approved, 100 天)
    - aria-2.0-m6-cost-model-telemetry (approved, 79 天)
    - aria-2.0-m6-e2e-resilience (approved, 77 天)
    - aria-2.0-m7-fleet-aggregation (approved, 70 天)

🛡️ 审计状态
───────────────────────────────────────────────────────────────
  审计系统: ✅ 已启用 (convergence 模式)
  活跃检查点: post_spec, post_planning
  上次审计: post_planning — PASS (已收敛, R7)

🔧 自定义检查
───────────────────────────────────────────────────────────────
  ✅ 16/16 全部通过 (0 失败, 0 跳过)

🔄 同步状态
───────────────────────────────────────────────────────────────
  当前分支: feature/handoff-multibranch-subdir-path-fidelity (upstream 未配置)
  远程引用: 1m 前同步 (本次扫描刚 fetch, 8/8 条成功)
  ⚠️ 当前分支无 upstream 配置，无法计算 ahead/behind
     如需配置: git branch --set-upstream-to=origin/feature/handoff-multibranch-subdir-path-fidelity
     (不影响结论: 多远程比对显示本分支与 origin / github 同名分支都在 4f91772, 一致)
  子模块:
    ✅ standards: 同步 (主仓记录 940cb5b = 远程 master, 落后 0)
       ℹ️ 工作目录在 feature 分支 d86fc91, 与主仓记录不同 (这就是 `M standards`)
    ✅ aria: 同步 (主仓记录 1cb3872 = 远程 master, 落后 0)
       ℹ️ 工作目录在 feature 分支 b181678, 与主仓记录不同 (这就是 `M aria`)
    ✅ aria-orchestrator: 同步 (主仓记录 = 工作目录 = 远程 master = 237045a)

🌐 多远程一致性
───────────────────────────────────────────────────────────────
  ✅ 主仓库: 所有远程一致 (origin, github) @ 4f91772
  ✅ standards 子模块: 所有远程一致 (origin, github) @ d86fc91
  ✅ aria 子模块: 所有远程一致 (origin, github) @ b181678
  ✅ aria-orchestrator 子模块: 所有远程一致 (origin, github) @ 237045a
  ✅ gitlink 可达性: 6/6 组 (2 远程 × 3 子模块) 全部 ok, 无孤儿指针
  overall_parity: true

📝 README 同步状态
───────────────────────────────────────────────────────────────
  ✅ 子模块版本号: 一致 (plugin.json 1.73.3 = aria/README 1.73.3)

📦 插件依赖状态
───────────────────────────────────────────────────────────────
  standards 子模块: ✅ 正常 (已注册、已初始化)

🔗 Forgejo 配置检查
───────────────────────────────────────────────────────────────
  ⚠️ 检测到 Forgejo 远程 (forgejo.10cg.pub) 但缺少 CLAUDE.local.md
     建议: 运行 /forgejo-sync 可引导创建配置 (需确认)

🎫 Open Issues
───────────────────────────────────────────────────────────────
  open_count: 49 (来源: 缓存, 2026-09-27T17:09:50Z)
  标签: bug ×4; 无 blocker / critical 标签

🎯 推荐工作流
───────────────────────────────────────────────────────────────
  (见下方)
```

---

## 子模块逐个解读 (回答"是否落后远程")

扫描对每个子模块比较三个位置：**工作目录实际检出的提交** / **主仓库记录的提交 (gitlink)** / **子模块远程 master**。

| 子模块 | 工作目录 | 主仓库记录 | 远程 master (origin) | 落后远程 | 说明 |
|---|---|---|---|---|---|
| aria | `b181678` (feature 分支) | `1cb3872` | `1cb3872` | 0 | 主仓记录 = 远程最新；工作目录在 feature 分支上，且该分支两个远程都已同步到 `b181678` |
| standards | `d86fc91` (feature 分支) | `940cb5b` | `940cb5b` | 0 | 同上 |
| aria-orchestrator | `237045a` (master) | `237045a` | `237045a` | 0 | 三处完全一致 |

要点：

1. **没有子模块落后远程**。`tree_vs_remote` 三个都是 `false`，也就是主仓库记录的指针和子模块远程 master 完全相同。所以即便协作者推过子模块，这些推送在远程 master 上已经被主仓记录覆盖了，远程 master 上**没有比你本地更新的东西**。推荐规则 `submodule_drift` (子模块落后远程时触发) 本次**没有命中**。
2. `git status` 里的 `M aria` / `M standards` **不是落后，而是你本地在这两个子模块里切到了 feature 分支** (`feature/handoff-multibranch-subdir-path-fidelity`)，检出的提交和主仓记录的不同。而且这两个 feature 分支在 origin 和 github 上都已经推到同一个提交，没有未推送的内容。
3. 多远程一致性 `overall_parity = true`，6 组 gitlink 可达性检查全部 `ok`，没有"主仓指向了远程上不存在的子模块提交"这种问题。

## 为什么不要跑 `git submodule update`

- **`git submodule update` (不带 `--remote`)**：会把 aria 切到 `1cb3872`、standards 切到 `940cb5b`，并且变成 detached HEAD。结果是你离开了 feature 分支上的 `b181678` / `d86fc91`。这些提交已经推到两个远程，不会丢，但你的工作目录会被切走，之后还得手动 `git -C aria checkout feature/...` 切回来。
- **`git submodule update --remote`**：会把子模块切到远程 master，而远程 master 正好就是 `1cb3872` / `940cb5b`，效果和上一条一样，同样把你拉离 feature 分支。

两种都拿不到任何新提交，只会打乱当前开发状态。

## 本次扫描覆盖不到的一处 (建议你自己核一下)

扫描比较的是**当前分支**和**子模块远程 master**。如果协作者是在**主仓库的 master** 上提交了"子模块指针升级"(bump gitlink)，这类更新要等你把 master 合并进来才会体现，本次扫描不直接比较主仓 master 和你当前分支。可以用下面两条只读命令核实 (不会改任何东西)：

```bash
git log --oneline HEAD..origin/master                              # 主仓 master 上有没有你分支里没有的提交
git diff HEAD origin/master -- aria standards aria-orchestrator   # 这些提交里有没有改子模块指针
```

- 两条都没输出 → 确认不需要做任何事。
- 第二条有输出 → 说明 master 上升级过子模块指针，正确做法是先把 master 合并/变基进当前分支，再 `git submodule update`，而不是直接 update。

## 其他顺带发现 (与本问题无直接关系)

- **handoff 已落后于实际进度**：最新 handoff 是 09-24 的 #199 会话收尾 (60.4h 前)，但当前分支上已有 09-27 的 `10CG/Aria#195` 提交 (组 3 / 组 4 完成、owner 裁定入账等)，这些进展还没有对应的 handoff。
- **多终端碰撞提示**：协调板检测到 `self_multi_container` (同一身份在多台机器/容器上都有轨道：simonfish 与 aria-runner-bot 共用 023236f2、bfe8285d 两个容器标识)。config 里 `coordination.enabled = true`、`mode = advisory`，所以按流程只有在你确认进入 Phase B 时才会调认领闸门，命令如下 (本次**未执行**，只列出)：
  ```bash
  python3 "${CLAUDE_PLUGIN_ROOT:-aria}/skills/state-scanner/scripts/phase1_gate.py" \
    --raw-track-id "handoff-multibranch-subdir-path-fidelity" --phase B --mode advisory --repo-path "/home/dev/Aria"
  ```
- 未跟踪目录 `aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/` 还没提交。
- Forgejo 本地配置 `CLAUDE.local.md` 缺失 (只影响 /forgejo-sync 类操作)。

---

## 🎯 推荐工作流

```
  ➤ [1] 保持现状，不执行 submodule update (推荐)
      执行: 无需 git 操作; 可选跑上面两条只读命令，确认主仓 master 没有新的子模块指针升级
      理由: 3 个子模块落后远程均为 0，多远程一致，gitlink 全部可达;
            update 只会把 aria / standards 从 feature 分支切到 detached HEAD

  ○ [2] 先把主仓 master 合进来，再同步子模块 (仅当上面第二条只读命令有输出时)
      执行: git fetch origin → 合并/变基 origin/master 进当前分支 → git submodule update
      理由: 这是"协作者在主仓升级了子模块指针"的正确处理顺序
      注意: 合并后子模块会切到新指针; 你在 aria / standards feature 分支上的工作
            需要事后再切回并处理

  ○ [3] 继续当前 10CG/Aria#195 轨的收尾: 提交本地 3 处变更 (C.1)
      执行: C.1 提交 aria / standards 子模块指针 + AB 结果目录
      理由: 这 3 处是本地领先 (不是落后)，处理方式是提交，而不是 update
      注意: 子模块合并须本地 git merge + 双推，不走 Forgejo 服务端合并;
            推后对每个远程 git ls-remote 核验 SHA

  ○ [4] 自定义组合
      输入格式: "B.2 + C.1" 或 "Phase C"

🤔 选择 [1-4] 或输入自定义:
```
