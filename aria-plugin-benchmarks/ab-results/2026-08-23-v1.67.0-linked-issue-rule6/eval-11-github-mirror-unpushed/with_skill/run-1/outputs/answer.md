# state-scanner 扫描结果 (eval-11: GitHub mirror 未推送复现)

Step 0: `scan.py` 退出码 **10** (部分软错误, snapshot 可用), snapshot 写到 `eval-11-github-mirror-unpushed/with_skill/outputs/state-snapshot.json`。只读扫描, 未做任何 commit / checkout / push。

## 📍 当前状态

- 主仓分支: `feature/linked-issue-normalization` (HEAD 826b356), 非 master
- 子模块: aria 在 `feature/linked-issue-normalization` (0fe2e0d) / standards detached (334c609) / aria-orchestrator master (237045a)
- 工作区: 2 个已修改文件 (`aria` gitlink、`aria-plugin-benchmarks/ab-suite/state-scanner.json`)
- 中断状态: none; git 中间态: none

## 🔄 同步状态 (Phase 0.5 remote_refresh + 1.12 multi_remote)

**remote_refresh**: 8 条 leg (4 仓 x origin/github) 全部 `fetch_ok=true`, `evidence_grade=fresh` (06:33 UTC 刚 fetch), 0 条跳过。也就是说这次判决不是靠 "Everything up-to-date" 回执, 而是刚 fetch 过的远端 ref 直接比对。

**当前分支 (feature/linked-issue-normalization)**: origin ahead 0 / behind 0; github 上没有这个分支 (`parity=unknown, reason=no_local_tracking_ref`) — feature 分支不推 mirror 属正常。

**master 跨远程比对 (用户关心的发版事件场景)** — scan.py 只比当前检出分支, 所以我额外用只读 `git ls-remote <remote> refs/heads/master` 逐个核对 (对齐 CLAUDE.md "推后逐个 ls-remote 核验" 约束):

| 仓库 | origin/master (Forgejo) | github/master | 结论 |
|------|------------------------|---------------|------|
| Aria 主仓 | 1205ec3 | 1205ec3 | 一致 |
| aria | a0fe720 | a0fe720 | 一致 |
| standards | 334c609 | 334c609 | 一致 |
| aria-orchestrator | 237045a | 237045a | 一致 |

**gitlink_integrity**: origin 三个子模块全 `ok`; github 三个为 `no_published_ref` (当前 feature 分支未发布到 github, 不是 orphaned, 不阻断)。

## ⚠️ 软错误 (exit 10)

`snapshot_consistency_inconclusive`: AC-5 对 `origin/feature/linked-issue-normalization` 的 164 条 handoff track 在 github 侧无法评估 (github 没有该分支), 而 snapshot 仍标 `overall_parity=true` 且无 reason。按契约, 这次 snapshot 自身的 parity 判决要视为**未验证** — 这正是上面我手动 ls-remote 核对 master 的原因, 核对结果与 snapshot 一致。

## 🎯 回答: 哪些 remote 需要补推

**没有。** 四个仓库的 master 在 Forgejo (origin) 与 GitHub (github) 上 SHA 完全相同, 2026-04-12 那种 "Forgejo 已合并、GitHub mirror 落后" 的状态在当前仓库**没有复现**。

附带发现 (不是补推, 是本地落后):

- 本地 `master` 分支在主仓落后 origin/github 12 个提交、aria 子模块落后 15 个、standards 落后 3 个 (因为当前在 feature 分支开发, 本地 master 没 fast-forward)。这是本地陈旧, 不影响远端一致性。如需同步 (只描述, 不执行):
  - `git fetch origin && git branch -f master origin/master` (主仓)
  - `git -C aria branch -f master origin/master` / `git -C standards branch -f master origin/master`
  - 或按 snapshot hint: `git submodule update --remote aria`

关于 "应检测到 GitHub 落后而非静默通过" 的机制说明: 当检出 master 时, multi_remote collector 在 fetch 后用 `local_refs` 算每个 enforced remote 的 ahead/behind, github 落后会直接报 `parity=behind`/`has_pending_push=true` 并压 `overall_parity=false`, 不依赖 push 回执; 本次因为检出的是 feature 分支, master 的跨远程比对不在 collector 覆盖面内, 需像上面那样用 ls-remote 补核 — 这是一个值得记下的覆盖缺口。

推荐工作流: 无需补推动作。按指令不调用 workflow-runner / phase1_gate, 到此为止。
