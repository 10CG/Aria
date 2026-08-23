## 状态扫描结果 (scan.py exit 10 — 部分软错误, snapshot 可用)

### 📍 当前状态
- 分支: `feature/linked-issue-normalization` (主仓 Aria), HEAD `826b356`
- detached HEAD: **否** | shallow clone: **否** | git 中间态 (rebase/merge): **无**
- 工作区: 2 个未提交项 — `aria` 子模块指针变动 (未暂存) + 本次 AB 结果目录 (未跟踪)
- 中断检测: 无进行中的 workflow

### 🔄 同步状态 (远程刚 fetch 过, 证据新鲜度 fresh, 1 分钟内)

**1. 相对自己的 upstream (`origin/feature/linked-issue-normalization`)**: ahead 0 / behind 0, 无分叉 —— **这条线不需要 `git pull`**, 远程分支和本地完全一致。

**2. 相对主分支 `origin/master` (你真正关心的那条)**: 本地 `rev-list` 补充核对, **你的 feature 分支落后 origin/master 12 个 commit, 领先 0 个**。这 12 个 commit 全是 #152 (pre-merge-gate-no-run-for-branch) 轨的 ship 产物, 含 aria-plugin v1.66.5 发布同步 (gitlink 9e6a17c → a0fe720, CLAUDE.md / VERSION / README 版本串) 和两次 Phase D 归档。

**3. 子模块 `aria`** (你的 feature 分支在子模块里同名): 相对子模块 `origin/master` **落后 15 / 领先 2**; 主仓 gitlink 指向的 `9e6a17c` 也已被 master 推到 `a0fe720` (v1.66.5)。`standards` / `aria-orchestrator` 与远程一致。

**4. 多远程 parity**: origin (Forgejo) 与本地相等; github 远程上没有该 feature 分支的 tracking ref (`no_local_tracking_ref`), 正常 —— feature 分支只推到了 origin。

### 结论: 需不需要拉?

- `git pull` (拉自己的 upstream): **不需要**, 已同步。
- **需要的是把 master 合进来**: 你怀疑的事是真的 —— master 有 12 个新 commit 你的分支没有。建议 (read-only 扫描, 以下命令由你自己执行):

```bash
# 主仓: 把 master 并入 feature 分支 (fetch 已由扫描完成, 可直接 merge)
git merge origin/master
# 子模块 aria: 同样并入 master (领先 2 + 落后 15, 会产生 merge commit)
git -C aria merge origin/master
```

注意点:
- 主仓 merge 会带来 gitlink 变动 (→ a0fe720), 而你本地 `aria` 工作区已指向自己分支的 `0fe2e0d`, 合并后需要在子模块里再做一次上面第二条 merge, 再在主仓 `git add aria` 让 gitlink 指向合并后的子模块 commit。
- v1.66.5 已 ship, 本轨 ship target 已定 v1.67.0, 合并后记得核对 5 文件版本同步面是否被 master 的版本串覆盖。

### ⚠️ 扫描软错误 (exit 10)
`snapshot_consistency`: 对 github 远程上 164 个 legacy handoff track 的 AC-5 核验命令失败 (github 没有这条 feature 分支), 因此 `overall_parity=true` 这一判决在本次扫描中应视为**未验证**; 不影响上面的 ahead/behind 数字 (那些来自 origin 的本地 tracking ref, fresh)。

### 🎯 推荐工作流
- **[1] 先同步再继续 (推荐)**: 按上面两条 merge 把 origin/master 并入主仓与 aria 子模块, 解决可能的冲突后继续 Phase B。
- [2] 暂不合并, 继续开发: 可行但 12+15 个 commit 的差距会在 C.2 合并时集中爆发, 且 pre-merge gate 要求分支与 master 无 in-flight 分叉, 不建议。
- [3] 仅查看: 不做任何操作。

不代你执行 git 操作; 请确认选哪一项。
