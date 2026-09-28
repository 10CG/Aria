# 状态扫描结果 (state-scanner v3.1.1)

scan.py 已跑完：退出码 0，全部采集成功，`errors[]` 为空。结果写在评测产出目录的 `state-snapshot.json` (没有写仓库内的 `.aria/state-snapshot.json`)。本次扫描里 8 条远程取数 (主仓 + 3 个子模块，每个仓都有 `origin` 和 `github` 两个远程) 全部 `fetch_ok=true`，时间在 1 分钟内，所以下面的同步结论是新取回的数据 (`evidence_grade=fresh`)，不是旧缓存。

## 先说结论：不需要 `git submodule update`，而且现在跑会出问题

- **3 个子模块都没有落后远程。** 每个子模块都是 `behind_count=0`、`ahead_count=0`、`tree_vs_remote=false`，`hint_type` 为空，所以没有触发 `submodule_drift` 规则。主仓记录的 gitlink 和子模块远程默认分支完全一致。
- **`aria` 和 `standards` 里有你自己本地 checkout 的提交，主仓还没记录它们** (`workdir_vs_tree=true`，也就是 `git status` 里的 ` M aria` / ` M standards`)：

| 子模块 | 当前 checkout (head) | 主仓记录的 gitlink (tree) | 远程默认分支 | 当前分支在两个远程上 |
|--------|---------------------|--------------------------|--------------|----------------------|
| standards | `d86fc91` (分支 `feature/handoff-multibranch-subdir-path-fidelity`) | `940cb5b` | `940cb5b` | origin / github 都是 `d86fc91`，一致 |
| aria | `b181678` (分支 `feature/handoff-multibranch-subdir-path-fidelity`) | `1cb3872` | `1cb3872` | origin / github 都是 `b181678`，一致 |
| aria-orchestrator | `237045a` (master) | `237045a` | `237045a` | 一致，完全同步 |

- **为什么不要跑：**
  - 不带参数的 `git submodule update` 会把 `aria` 和 `standards` 切回主仓记录的 `1cb3872` / `940cb5b`，变成 detached HEAD，离开你正在做的 feature 分支。提交不会丢，因为它们已经推到两个远程上了，但工作现场会被打乱。
  - `git submodule update --remote` 也一样：远程默认分支就是 `1cb3872` / `940cb5b`，所以结果还是把 checkout 切走。
- **"别人推了子模块更新"这件事，本次扫描没有看到。** 刚取回的远程默认分支和主仓记录一致，远程上没有你本地没有的新提交。如果你听说的更新是推到了别的分支，那它不在"落后默认分支"这个检测范围里。

真正要做的是另一件事：等 feature 工作确定后，在主仓 `git add aria standards` 提交 gitlink 更新，这就是把你这边子模块的新提交"记录进"主仓。按项目约束 1，子模块合并到 master 时必须本地 `git merge` 然后双推，不能用 Forgejo 服务端合并。

---

📍 **当前状态**
- 分支: `feature/handoff-multibranch-subdir-path-fidelity` (HEAD `4f91772`)
- 模块 / Phase·Cycle: 未配置 UPM (`upm.configured=false`)
- 变更文件: 3 个
  - `aria` (子模块指针)
  - `standards` (子模块指针)
  - 未跟踪目录 `aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/`
- 关联 OpenSpec: `handoff-multibranch-subdir-path-fidelity` (Approved)
- 中断状态: 无 (`interrupt.status=none`)
- git 中间态: 无 (`operation=none`)

📊 **变更分析**
- 变更类型: other×3 (两个子模块指针 + 一个 AB 结果目录)
- 复杂度: Level 2
- 架构影响: 无
- 测试覆盖: 无测试文件变更
- Skill 变更检测: 未检出 SKILL.md 变更

📄 **需求状态**
- 已配置
- PRD:
  - `prd-aria-v1.md` (active)
  - `prd-aria-v2.md` (Approved，归一后为 pending)
- User Stories: done 17 / in_progress 2 / approved 1 / pending 1

🏗️ **架构状态**
- `docs/architecture/system-architecture.md` 存在，状态 Active，最后更新 2026-09-02
- 需求链路完整 (`chain_valid=true`，上游是 v1 和 v2 两份 PRD)

📋 **OpenSpec 状态**
- 活跃变更 8 个 (全部 approved)，已归档 146 个，待归档 0 个
- ⚠️ 设计未实施 5 个:

| 变更 | 状态 | 停滞天数 |
|------|------|----------|
| aria-2.0-m6-release-closeout | approved | 124 |
| aria-2.0-m7-agent-lifecycle | approved | 100 |
| aria-2.0-m6-cost-model-telemetry | approved | 79 |
| aria-2.0-m6-e2e-resilience | approved | 77 |
| aria-2.0-m7-fleet-aggregation | approved | 70 |

🛡️ **审计状态**
- 审计已启用
- 上次审计: `post_planning` 检查点，PASS，已收敛，2026-09-24 (`pre-merge-completeness-gate-change-scope`，R7 聚合报告)

🔧 **自定义检查**
- 16/16 通过，0 失败 (含 `plugin-cache-currency`、`plugin-version-arch-docs-match`、`coordination-gate-invocation` 等)

🔄 **同步状态**
- 当前分支: `feature/handoff-multibranch-subdir-path-fidelity`
  - 没有配置 upstream (`no_upstream`)，所以按 upstream 算的 ahead/behind 为空
  - 多远程比对: 本地 `4f91772` 与 origin、github 两边一致 (`parity=equal`)，也就是分支已经推到两个远程
- 远程引用: 1 分钟前同步
- 多远程总体一致: `overall_parity=true`
  - 没有待推送 (`has_pending_push=false`)
  - 没有不可达的远程
- 子模块:
  - ✅ aria-orchestrator: 同步
  - ℹ️ aria: 不落后远程；本地 checkout `b181678` 与主仓记录 `1cb3872` 不同 (你的 feature 分支提交，已推送，主仓 gitlink 待提交)
  - ℹ️ standards: 不落后远程；本地 checkout `d86fc91` 与主仓记录 `940cb5b` 不同 (同上)
- gitlink 可达性: 3 个子模块 × 2 个远程，6 项全部 `ok`，没有孤立 gitlink，`clone --recursive` 不会断
- 📝 README 版本: aria-plugin 1.73.3，与 README 一致
- 🔗 Forgejo 配置: 检测到 forgejo.10cg.pub 远程，但 Forgejo 配置缺失 (可用 `/forgejo-sync` 引导创建，需要你确认)

🎫 **Open Issues**
- open 49 个，其中 bug 标签 4 个。近期几条:
  - 10CG/Aria#221 secret-guard 进程列举旁路 (bug)
  - #220 latest.md History prepend 缺机械核验
  - #219 只读机读进度接口
  - #218 state-scanner handoff 无指针时按 mtime 判最新 (bug)
  - #217 session-closer stdout 跟随 locale (bug)

**交接 (handoff awareness)**
- 最新 handoff 是 `docs/handoff/2026-09-24-session-close-199-post-planning-converged.md`，由 pointer 指定，距今约 60 小时，frontmatter 完整，没有放错位置的文件
- 跨 worktree: 只有 1 个 worktree，别处没有更新的 handoff
- 多轨道碰撞: `tracks_multibranch.collision.kind=self_multi_container`，涉及轨道 `simonfish/023236f2`、`simonfish/bfe8285d`，这两条轨道同时被 `aria-runner-bot` 和 `simonfish` 碰过。按规则 1.54 这只是提示，不阻断。另一个容器 (或自主运行时) 可能在同一仓库做事，开工前请留意。

🎯 **推荐工作流**

针对你的问题 (子模块是否落后远程)，推荐是：**不执行 `git submodule update`**。

- [1] **(推荐) 只看状态，不动子模块**
  - 你的子模块没有落后，本次扫描到此结束，不启动工作流
  - 理由: `behind_count` 全部为 0，`overall_parity=true`
- [2] **把子模块新提交记录进主仓** (如果 feature 工作已到一个节点)
  - 走 C.1 提交: `git add aria standards` 后按 Conventional Commits 提交 gitlink 更新 (注意别误把 AB 结果目录混进去，或者分开提交)
  - 理由: `workdir_vs_tree=true`，主仓 gitlink 还指着旧提交
- [3] **继续当前 feature 开发** (`handoff-multibranch-subdir-path-fidelity`，Approved)
  - 走 B.2 → C.1
  - 进入 Phase B 前，编排层会执行下面这条 advisory 认领命令。本次只列出、不执行:

    ```
    python3 /home/dev/Aria/aria/skills/state-scanner/scripts/phase1_gate.py --raw-track-id "<handoff §6 选定的 carry-id>" --phase B --mode advisory --repo-path /home/dev/Aria
    ```

  - 如果本会话持有 active claim，每次扫描入口还会跑一次心跳。同样只列出、不执行:

    ```
    python3 /home/dev/Aria/aria/skills/state-scanner/scripts/phase1_gate.py --heartbeat-only --raw-track-id "<carry-id>" --phase A.1 --repo-path /home/dev/Aria
    ```

- [4] **如果你确实想放弃子模块上的本地 feature checkout，回到主仓记录的版本**
  - 执行 `git submodule update aria standards`
  - 后果: 两个子模块变成 detached HEAD，停在 `1cb3872` / `940cb5b`；feature 分支提交仍在远程，不会丢
  - 除非你就是要这样，否则不建议

跳过项: 不需要 `git pull` (主仓分支与两个远程一致)；不需要 `git submodule update --remote` (远程默认分支没有新提交)。

请回复 [1]-[4]，或者自定义步骤组合 (比如 "C.1")。
