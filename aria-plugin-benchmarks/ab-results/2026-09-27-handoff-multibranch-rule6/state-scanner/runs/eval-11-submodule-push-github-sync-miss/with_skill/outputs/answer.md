## 结论先说

**本次扫描没有发现任何 remote 需要补推。** 当前仓库**不处于** 2026-04-12 那次事故的状态：主仓和 3 个子模块 (aria / standards / aria-orchestrator) 在 `origin` (Forgejo) 和 `github` 两个 remote 上都是 `parity=equal`，`overall_parity=true`。

这个"全部一致"的结论是**本次扫描现场 fetch 之后**比对出来的 (`evidence_grade=fresh`)，不是靠 push 回执 `Everything up-to-date` 得出的，所以不是事故里那种静默通过。

---

## Step 0: scan.py

```
python3 /home/dev/Aria/aria/skills/state-scanner/scripts/scan.py --output <scratchpad>/state-snapshot.json
exit=0 (全部采集成功, errors[] 为空)
```

## 🔄 同步状态

**新鲜度 (Phase 0.5 `remote_refresh`)**: 一共 8 条 leg (4 个仓 × 2 个 remote)，全部 `fetch_ok=true`，`consecutive_unverified=0`，fetch 时间 2026-09-27T17:20:42–47Z，没有跳过任何 remote (`skipped_remotes=[]`)。这就是这个场景要的关键点：比对用的是扫描时刚 fetch 回来的远程 ref。本地 tracking ref 过期的话，equal 会被降级成 `unknown/not_refreshed`，不会被当作已同步。

**多远程 parity (`sync_status.multi_remote`)**: `enforced_remotes = [github, origin]`

| 仓库 | 比对分支 | 本地 HEAD | origin (Forgejo) | github | 判定 |
|------|----------|-----------|------------------|--------|------|
| 主仓 `.` | feature/handoff-multibranch-subdir-path-fidelity | 4f91772 | 4f91772 equal / fresh | 4f91772 equal / fresh | 一致 |
| `aria` | feature/handoff-multibranch-subdir-path-fidelity | b181678 | b181678 equal / fresh | b181678 equal / fresh | 一致 |
| `standards` | feature/handoff-multibranch-subdir-path-fidelity | d86fc91 | d86fc91 equal / fresh | d86fc91 equal / fresh | 一致 |
| `aria-orchestrator` | master | 237045a | 237045a equal / fresh | 237045a equal / fresh | 一致 |

- `overall_parity = true`，`has_pending_push = false`，`has_unreachable_remote = false`
- **gitlink 可达性 (`gitlink_integrity[]`)**: 共 6 对 (2 个 remote × 3 个子模块)，全部 `status=ok`。意思是主仓在 origin 和 github 上已发布的 commit 所引用的子模块 gitlink，在对应子模块的同名 remote 上都拿得到，没有 orphaned gitlink，`clone --recursive` 不会断。
- 推荐规则 `multi_remote_drift` (priority 1.35) **未触发**，因为 `overall_parity` 不是 false。

### 注意：你问的是 aria 的 master，但 scan.py 比对的是"当前检出分支"

`multi_remote` 只比对各仓**当前检出的分支**。现在 aria 子模块检出的是 feature 分支，不是 master，所以 snapshot **没有直接覆盖 "aria master 在 github 上是否落后"** 这个问题。事故场景正好是 master 上的合并，这个覆盖缺口需要你知道。

为此我额外做了一次只读核对：用 `git rev-parse` 读 scan.py 刚 fetch 回来的 tracking ref，没有做任何新的 fetch 或 push。**这一步是补充核对，不属于 snapshot 字段。**

| 仓库 | 本地 master | origin/master | github/master | origin 与 github 差 (左/右) |
|------|-------------|---------------|---------------|-----------------------------|
| 主仓 | c454e35 | c454e35 | c454e35 | 0 / 0 |
| aria | 1cb3872 | 1cb3872 | 1cb3872 | 0 / 0 |
| standards | 940cb5b | 940cb5b | 940cb5b | 0 / 0 |
| aria-orchestrator | 237045a | 237045a | 237045a | 0 / 0 |

aria 的 master 在 Forgejo 和 GitHub 上都是 `1cb3872`，也就是主仓 gitlink 当前指向的那个 commit (`sync_status.submodules[aria].tree_commit`)。**这次 GitHub mirror 没有落后。**

### 如果事故状态真的出现，scan 会怎么报

假设 aria 当前在 master，Forgejo 服务端合并后本地已快进到 Forgejo，但没推 github：

- `multi_remote.submodules[aria].remotes[github]` → `parity=ahead` (本地领先 github N 个 commit)，`evidence_grade=fresh`。
- 主仓如果随后 bump 了 gitlink 并推到 github → `gitlink_integrity[(github, aria)]` → `status=orphaned`，它**恒阻断** `overall_parity` (clause 3)，`multi_remote_drift` 会走第七路，给出 `git -C aria push github master` 这样的建议。
- 已知限制：如果只是子模块 `ahead`、主仓还没 bump gitlink，按 §10.7 这属于 `has_pending_push` (正常待推送，不报警)。要到主仓 gitlink 已发布、github 上的子模块拿不到那个 commit 时才会变红。

补推后，按 CLAUDE.md 多远程推送约束 2，要对每个 remote 单独跑 `git ls-remote <remote> master` 和本地 SHA 比对，不能信 push 回执。

---

## 📍 当前状态 (简要)

- 主仓分支 `feature/handoff-multibranch-subdir-path-fidelity`，**没有配置 upstream** (`current_branch.reason=no_upstream`)。这不影响多远程 parity：`multi_remote` 按 `refs/remotes/<remote>/<branch>` 比对，两边都已存在并且一致。
- 未提交内容：`aria`、`standards` 两个 gitlink 指针有改动 (子模块 HEAD 和主仓树里记录的不同，`workdir_vs_tree=true`)；另有未跟踪目录 `aria-plugin-benchmarks/ab-results/2026-09-27-handoff-multibranch-rule6/`。
- 中断检测：`interrupt.status=none`。git 中间态：`operation=none`。
- 自定义检查：16/16 通过。
- 多终端：`tracks_multibranch.collision.kind = self_multi_container`。只有你确认进入 Phase B 时，才会在 Phase B 入口调用 `phase1_gate.py --raw-track-id "<handoff §6 carry-id>" --phase B --mode advisory --repo-path /home/dev/Aria`。这次只是扫描，**没有调用**。
- 最新 handoff：`docs/handoff/2026-09-24-session-close-199-post-planning-converged.md` (60.5h 前)。

## 🎯 推荐工作流

| 选项 | 内容 | 说明 |
|------|------|------|
| **[1] 不需要补推 (推荐)** | 无操作 | 所有 remote 一致，gitlink 全部可达，就同步这件事而言没有待办 |
| [2] 真的复现一次事故 | 在隔离沙箱里 (`file://` clone 的副本，不是真仓) 构造"aria master 已快进到 origin、github 落后"再跑 scan.py | 这个做法能验证 `ahead` 和 `orphaned` 两条路径。**不要在真仓上构造**，会造成真的镜像分叉 |
| [3] 处理当前 feature 分支的未提交内容 | C.1 提交 (`aria`/`standards` 指针 + AB 结果目录) | 和补推无关，是本分支后续工作 |
| [4] 自定义 | 告诉我要组合的步骤 | — |

请选一个编号。
